# Plugin Model

Plugins own stateful behavior.

A plugin block is rendered inside a normal BRIAN message but points to plugin-owned state and behavior.

---

## Plugin block envelope

```json
{
  "type": "plugin",
  "plugin": "approval",
  "version": "1.0",
  "schema_version": "1.0",
  "instance_id": "approval_123",
  "view": {
    "title": "Approve sending this message?",
    "status": "pending"
  },
  "fallback_markdown": "**Approval pending:** Approve sending this message?"
}
```

Required fields:

| Field | Description |
|---|---|
| `type` | Must be `plugin`. |
| `plugin` | Plugin name. |
| `version` | Plugin version. |
| `schema_version` | Block schema version. |
| `instance_id` | Durable plugin instance ID. |
| `view` | Renderer-facing view state. |
| `fallback_markdown` | Safe fallback rendering. |

---

## Plugin command event

User interaction with a plugin produces a normal event.

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

The transport validates communication-level authorization.

The plugin validates domain-level authorization.

Commands may optionally carry `delegation` with the originating human
`request_event_id` and `request_room_seq`. Delegated commands require
`expected_revision`. Direct Android commands keep their existing contract.
The event sender remains the configured agent. Plugins verify the original
message through transport history, its room, `room_seq` and owner, then apply
the command in their existing per-instance transaction. Approval decisions
cannot be delegated. See [LLM integration](14-llm-rich-interaction.md).

---

## Plugin state update event

Plugins publish state changes back into the room as events.

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

The app updates rendered blocks by matching:

```text
plugin + instance_id
```

---

## Agent interaction rules

Agents may:

- request plugin instance creation
- render plugin blocks using plugin-provided view state
- publish explanatory messages around plugin blocks
- consume plugin state update events
- react to completed/failed plugin states

Agents should not:

- directly mutate plugin-owned tables
- invent state transitions outside the plugin contract
- forge plugin state update events unless it is the plugin owner
- assume a plugin instance is valid without plugin confirmation

---

## Correct approval flow

```text
1. Agent decides approval is needed.
2. Agent calls ApprovalPlugin.create(...).
3. ApprovalPlugin stores approval state.
4. Agent publishes m.ui.message with an approval plugin block.
5. Transport stores and syncs the event.
6. App renders the approval block.
7. User taps Approve.
8. App publishes m.plugin.command.
9. Transport stores and syncs the command event.
10. ApprovalPlugin consumes the command, validates it, updates state.
11. ApprovalPlugin publishes m.plugin.state.updated.
12. App updates the rendered block.
13. Agent observes the state update and continues.
```

---

## Initial plugin set

Recommended first plugins:

- `approval`
- `workflow`
- `form_stateful`
- `tool_call_debug`

Recommended later plugins:

- `checklist`
- `poll`
- `plan`
- `timeline`
- `table`
- `chart`
- `log_stream`
