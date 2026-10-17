# Changelog

## Unreleased

- Runtime integration chapter (`spec/10-runtime-integration.md`) and canonical Approval lifecycle fixture.
- Agent delegation (`spec/11-agent-delegation.md`): `delegation` and `expected_revision` on `m.plugin.command`, audited results, `m.plugin.command.rejected`.
- `agent_status` plugin (`spec/12-agent-status.md`) and its block/request schemas.
- Plugin creation request schemas (`schemas/requests/`).
- Delegation references the origin message by per-room `request_room_seq` (was `request_stream_pos`).
- `scripts/check-contracts.py` for offline schema/catalog/fixture validation.
- Licensed under Apache-2.0.

## 0.3.0

Added surfaces and active block projection model.

Includes:

- `spec/08-surfaces-and-pinning.md`
- `spec/09-canonical-examples.md`
- `surface` block metadata
- catalog-level surface policies
- active item projection schema
- surface dismissed / user pinned event schemas
- monthly bills checklist canonical example

## 0.2.0

Added future plugin specs, schemas, examples, and catalog lifecycle status.

Future plugins:

- checklist
- poll
- plan
- timeline
- table
- chart
- log_stream
- document_collab
- integration_preview
- memory_card
- webhook_trigger

## 0.1.0

Initial draft package for BRIAN / Agent Blocks.

Includes:

- README
- overview spec
- message model
- core block spec
- plugin model
- catalog model
- security model
- versioning model
- JSON Schemas
- example payloads
