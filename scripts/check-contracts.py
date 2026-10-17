#!/usr/bin/env python3
"""Validate local schemas and runtime fixtures; never fetch remote schemas."""

import argparse
import json
from pathlib import Path
from jsonschema import Draft202012Validator

parser = argparse.ArgumentParser()
parser.add_argument("--check-consumers", action="store_true")
args = parser.parse_args()
ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def expand(obj, path):
    if isinstance(obj, list):
        return [expand(x, path) for x in obj]
    if not isinstance(obj, dict):
        return obj
    if "$ref" in obj:
        target = (path.parent / obj["$ref"]).resolve()
        return expand(read(target), target)
    return {key: expand(value, path) for key, value in obj.items() if key != "$id"}


files = list((ROOT / "schemas").rglob("*.json"))
for path in files:
    Draft202012Validator.check_schema(expand(read(path), path))
catalog = read(ROOT / "catalog/brian-catalog-1.0.json")
assert len({p["name"] for p in catalog["plugins"]}) == len(catalog["plugins"])
assert next(p for p in catalog["plugins"] if p["name"] == "workflow")["commands"] == [
    "refresh"
]
validators = {
    event: Draft202012Validator(
        expand(read(ROOT / "schemas/events" / name), ROOT / "schemas/events" / name)
    )
    for event, name in {
        "m.ui.message": "ui-message-1.0.json",
        "m.plugin.command": "plugin-command-1.0.json",
        "m.plugin.state.updated": "plugin-state-updated-1.0.json",
        "m.plugin.instance.created": "plugin-instance-created-1.0.json",
        "m.ui.surface.preference.updated": "surface-preference-updated-1.0.json",
        "m.plugin.command.rejected": "plugin-command-rejected-1.0.json",
    }.items()
}
for fixture in (ROOT / "examples/runtime").glob("*.json"):
    for event in read(fixture):
        validators[event["type"]].validate(event["content"])
if args.check_consumers:
    for path in files:
        asset = (
            ROOT.parent
            / "agent-blocks/internal/catalog/assets"
            / str(path.relative_to(ROOT / "schemas")).replace("/", "__")
        )
        client = (
            ROOT.parent
            / "nimchat/packages/brian/schemas"
            / path.relative_to(ROOT / "schemas")
        )
        assert read(path) == read(asset) == read(client), f"Schema drift: {path}"
print(
    f"{len(files)} schemas valid; catalog unique; runtime fixtures valid; consumer copies checked: {args.check_consumers}."
)
