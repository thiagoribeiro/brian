# Canonical Examples

This document contains end-to-end examples that clarify how BRIAN blocks, plugins, surfaces, and state updates work together.

---

## Monthly bills checklist

User intent:

```text
Create a monthly checklist of bills I need to pay and keep it visible until everything is paid.
```

This is not just a chat message.

It is an active, stateful, user-facing object.

---

## Desired flow

```text
1. A system or planner creates a monthly bills checklist instance.
2. The app receives a BRIAN message containing a checklist plugin block.
3. The checklist appears in the chat timeline for auditability.
4. Because the checklist is open and incomplete, the app promotes it to the Active/Pinned surface.
5. The user marks bills as paid over time.
6. Each item update emits a plugin command event.
7. The checklist plugin validates the command.
8. The checklist plugin records timestamped state transitions.
9. The checklist plugin emits a plugin state update event.
10. When every required item is completed, the checklist enters a terminal/completed state.
11. The app removes it from pending/active items unless the user manually pinned it.
```

---

## Source of truth

```text
Timeline = historical/audit log.
Checklist plugin = source of truth for item state.
Active surface = projection of pending/current working set.
```

---

## Checklist message

```json
{
  "type": "m.ui.message",
  "content": {
    "schema": "brian.message",
    "version": "1.0",
    "body": [
      {
        "type": "plugin",
        "plugin": "checklist",
        "version": "1.0",
        "schema_version": "1.0",
        "instance_id": "monthly_bills_2026_05",
        "surface": {
          "default": "pinned",
          "auto_pin": true,
          "priority": "high",
          "dismissible": true
        },
        "view": {
          "title": "May 2026 bills",
          "status": "open",
          "items": [
            {
              "id": "electricity",
              "label": "Electricity bill",
              "checked": false,
              "due_date": "2026-05-10"
            },
            {
              "id": "internet",
              "label": "Internet bill",
              "checked": false,
              "due_date": "2026-05-15"
            }
          ]
        },
        "fallback_markdown": "**May 2026 bills**\n- [ ] Electricity bill\n- [ ] Internet bill"
      }
    ]
  }
}
```

---

## Command event

When the user marks the electricity bill as paid, the app emits:

```json
{
  "type": "m.plugin.command",
  "content": {
    "plugin": "checklist",
    "instance_id": "monthly_bills_2026_05",
    "command": "check_item",
    "payload": {
      "item_id": "electricity"
    }
  }
}
```

---

## State update event

The checklist plugin validates the command and emits:

```json
{
  "type": "m.plugin.state.updated",
  "content": {
    "plugin": "checklist",
    "instance_id": "monthly_bills_2026_05",
    "state": {
      "status": "open",
      "items": [
        {
          "id": "electricity",
          "label": "Electricity bill",
          "checked": true,
          "checked_at": "2026-05-06T14:30:00Z",
          "checked_by": "user_123"
        },
        {
          "id": "internet",
          "label": "Internet bill",
          "checked": false,
          "due_date": "2026-05-15"
        }
      ]
    }
  }
}
```

---

## Completion behavior

When all required items are checked:

```text
checklist.status = completed
auto_pin = false
active_items projection removes it from pending items
user_pin may keep it visible if manually pinned
```
