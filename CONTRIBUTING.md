# Contributing

Issues and pull requests are welcome.

- Spec changes go in `spec/`, with matching updates to `schemas/`, `catalog/` and `examples/`.
- Run `python scripts/check-contracts.py` before opening a PR (CI runs it too).
- If you change a schema that is copied into [agent-blocks](https://github.com/thiagoribeiro/agent-blocks) or [nimchat](https://github.com/thiagoribeiro/nimchat), run `python scripts/check-contracts.py --check-consumers` with those repos checked out as siblings and update the copies.
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`…).
- By contributing you agree that your contributions are licensed under the Apache License 2.0.
