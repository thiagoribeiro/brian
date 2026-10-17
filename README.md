# BRIAN

**BRIAN (Block-based Rich Interface Notation)** is a JSON notation for structured, rich, interactive and stateful messages between humans, apps, agents, systems and workflows.

It defines:

- message envelopes
- core UI blocks
- plugin block envelopes
- fallback rendering
- command events
- plugin state update events
- block/plugin catalog discovery
- versioning and compatibility rules

### Related projects

| Project | Role |
|---|---|
| **BRIAN** (this repo) | Specification, JSON Schemas, catalog and examples. |
| [agent-blocks](https://github.com/thiagoribeiro/agent-blocks) | Reference implementation: router and stateful plugins (approval, workflow, checklist, poll, forms, agent status). |
| [nimlet](https://github.com/thiagoribeiro/nimlet) | Chat server used as the event transport. |
| [nimchat](https://github.com/thiagoribeiro/nimchat) | Web and Android client that renders BRIAN blocks. |

BRIAN itself is transport-agnostic; none of these are required to implement it.

---

## Why BRIAN?

Normal chat messages are good for text, but agent-native apps need richer interaction patterns:

- Markdown explanations
- images, audio, and files
- references to other messages
- approval cards
- workflow status cards
- forms
- checklists
- polls
- tool-call debug views
- fallback rendering for unsupported clients
- auditable command events instead of hidden UI actions

BRIAN defines those structures without turning the chat transport into a domain-specific product.

---

## Project boundaries

BRIAN is transport-agnostic.

It can be carried by any event system that supports ordered room events.

Recommended layering:

```text
Transport
  stores, orders, authorizes, and syncs events

BRIAN / Agent Blocks
  defines rich UI message format, core blocks, plugin block envelopes, and fallback rules

Plugins
  own stateful behavior, commands, validation, and domain-specific transitions

App
  renders supported blocks and publishes user interaction events

Agent / producer
  uses the catalog to know which blocks/plugins it can emit
```

The transport should not need to understand approval, workflow, poll, checklist, or tool-call semantics.

It only transports events.

---

## Minimal example

A BRIAN message is usually transported as an event with type `m.ui.message`.

```json
{
  "type": "m.ui.message",
  "content": {
    "schema": "brian.message",
    "version": "1.0",
    "body": [
      {
        "type": "markdown",
        "text": "The workflow is ready. Please approve before execution."
      },
      {
        "type": "plugin",
        "plugin": "approval",
        "version": "1.0",
        "schema_version": "1.0",
        "instance_id": "approval_123",
        "view": {
          "title": "Approve workflow execution?",
          "status": "pending"
        },
        "fallback_markdown": "**Approval pending:** Approve workflow execution?"
      }
    ]
  }
}
```

When the user taps a button, the app publishes an auditable command event:

```json
{
  "type": "m.plugin.command",
  "content": {
    "plugin": "approval",
    "instance_id": "approval_123",
    "command": "approve",
    "payload": {}
  }
}
```

The plugin validates the command and publishes a state update:

```json
{
  "type": "m.plugin.state.updated",
  "content": {
    "plugin": "approval",
    "instance_id": "approval_123",
    "state": {
      "status": "approved",
      "approved_by": "user_123"
    }
  }
}
```

---

## Repository layout

```text
.
├── spec/            # numbered specification chapters (start at 00-overview.md)
├── schemas/
│   ├── core/        # core blocks
│   ├── events/      # event content schemas (m.ui.message, m.plugin.*)
│   ├── plugins/     # plugin block schemas
│   └── requests/    # plugin creation data
├── examples/
│   ├── messages/
│   ├── plugins/
│   └── runtime/     # canonical event sequences
├── catalog/
│   └── brian-catalog-1.0.json
└── scripts/
    └── check-contracts.py
```

---

## MVP blocks

Core blocks:

- `markdown`
- `notice`
- `image`
- `audio`
- `file`
- `divider`
- `key_value`
- `actions`
- `reference`

Initial plugins:

- `approval`
- `workflow`
- `form_stateful`
- `tool_call_debug`

Later plugins:

- `checklist`
- `poll`
- `plan`
- `timeline`
- `table`
- `chart`
- `log_stream`

---



## Surfaces and active blocks

BRIAN supports more than a simple chronological chat timeline.

Some blocks represent active state and should remain visible while the conversation continues.

Examples:

- open polls
- incomplete checklists
- pending approvals
- running workflows
- forms waiting for input
- waiting callbacks

BRIAN models this using surface hints and catalog-level surface policies.

```text
Timeline = audit log
Active/Pinned surface = user's working set
Details/Focus surface = expanded interaction
```

A renderer such as [nimchat](https://github.com/thiagoribeiro/nimchat) can use this to keep active blocks visible without reposting messages.

See:

- `spec/08-surfaces-and-pinning.md`
- `spec/09-canonical-examples.md`
- `examples/plugins/monthly-bills-checklist-message.json`


## Future plugin specs

This repository includes draft specs and schemas for future plugins.

They are not MVP requirements.

Future plugins are marked in the catalog with:

```json
{
  "status": "future"
}
```

Agents must only emit a plugin when the runtime catalog says it is installed and supported.


## Status

BRIAN is an early-stage specification.

The API, schemas, and plugin model are expected to evolve before a stable v1 release.

---

## Runtime and agents

- [Runtime integration](spec/10-runtime-integration.md) — canonical events, identity, trust and recovery.
- [Agent delegation](spec/11-agent-delegation.md) — how an LLM agent changes blocks on behalf of a user, with audit.
- [Agent status](spec/12-agent-status.md) — progress reports for agent requests.

The [Approval fixture](examples/runtime/approval-lifecycle.json) covers creation, card, command, update and dismissal as canonical history; its timestamps are historical.

## Validating contracts

```sh
pip install jsonschema
python scripts/check-contracts.py
```

This validates every schema, the catalog and the runtime fixtures, without network access. With `--check-consumers` it also checks that the schema copies in sibling `agent-blocks` and `nimchat` checkouts are identical.

## License

[Apache License 2.0](LICENSE).
