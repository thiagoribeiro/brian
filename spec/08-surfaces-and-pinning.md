# Surfaces and Pinning

BRIAN messages are usually rendered in a chronological chat timeline.

However, some blocks are not just messages. They represent active state that should remain visible and easy to access while the conversation continues.

Examples:

- open polls
- pending approvals
- running workflows
- incomplete checklists
- forms waiting for input
- open alerts
- waiting callbacks
- active reminders

BRIAN supports this through surface hints and catalog-level surface policies.

---

## Core rule

```text
The timeline is the audit log.
The active surface is the user's working set.
Pinned blocks are projections, not separate truth.
```

The timeline remains append-only and auditable.

The active/pinned area is derived from message blocks, plugin state, user preferences, and catalog rules.

---

## Recommended app surfaces

A BRIAN renderer (for example [nimchat](https://github.com/thiagoribeiro/nimchat)) should support at least three conceptual surfaces:

```text
1. Chat timeline
   Normal chronological conversation.

2. Active / Pinned surface
   Important stateful blocks that need continued visibility.

3. Details / Focus surface
   Expanded view for a selected block, workflow, poll, form, checklist, or task.
```

Optional future surfaces:

```text
Room dashboard
Search/history
Files/media
Notifications/inbox
```

---

## Surface hint

A block may include a `surface` field.

Example:

```json
{
  "type": "plugin",
  "plugin": "checklist",
  "version": "1.0",
  "schema_version": "1.0",
  "instance_id": "checklist_123",
  "surface": {
    "default": "pinned",
    "auto_pin": true,
    "priority": "normal",
    "dismissible": true
  },
  "view": {
    "title": "Launch checklist",
    "status": "open"
  },
  "fallback_markdown": "**Checklist:** Launch checklist"
}
```

---

## Surface fields

| Field | Required | Description |
|---|---:|---|
| `default` | no | Preferred surface: `timeline`, `pinned`, `modal`, `panel`, `archive`. |
| `auto_pin` | no | Whether the block is eligible for automatic pinning. |
| `priority` | no | `low`, `normal`, `high`, or `urgent`. |
| `dismissible` | no | Whether the user may dismiss it from active surfaces. |
| `expires_at` | no | Optional ISO timestamp after which the active projection may expire. |

---

## Surface kinds

```text
timeline
  Render only in the chronological chat timeline.

pinned
  Eligible for active/pinned surface.

modal
  Can open as a focused modal interaction.

panel
  Can appear in a side panel, bottom sheet, or details view.

archive
  Primarily discoverable through history/search.
```

---

## Auto pinning vs user pinning

There are two independent kinds of pinning.

```text
auto_pin
  Controlled by block/plugin state and catalog rules.

user_pin
  Manually pinned by a user for quick access.
```

A completed poll may stop being auto-pinned but remain visible if a user manually pinned it.

---

## Catalog-level surface policy

The catalog should define default surface behavior for each plugin.

Example:

```json
{
  "name": "poll",
  "version": "1.0",
  "status": "future",
  "surfaces": {
    "default": "pinned",
    "auto_pin_when": ["open"],
    "auto_unpin_when": ["closed", "cancelled"],
    "supports_user_pin": true,
    "supports_focus_view": true
  }
}
```

---

## Suggested defaults

```text
markdown
  timeline only

notice
  timeline; optionally pinned if warning/error and unresolved

image/audio/file
  timeline + media/files surface

approval
  auto-pinned while pending
  unpinned when approved/rejected/expired/cancelled

workflow
  auto-pinned while running/waiting/failed
  unpinned when completed/cancelled unless user-pinned

form_stateful
  auto-pinned while draft/submitted-with-errors/waiting-for-input
  unpinned when validated/submitted/expired/cancelled

checklist
  auto-pinned while open and incomplete
  unpinned when completed/archived/cancelled

poll
  auto-pinned while open
  unpinned when closed/cancelled

plan
  auto-pinned while proposed/approved/running
  unpinned when completed/cancelled/rejected

webhook_trigger
  auto-pinned while waiting
  unpinned when received/expired/cancelled/failed
```

---

## Active item projection

The active surface should not be a separate source of truth.

It should be derived from:

```text
message blocks
plugin instance state
plugin state update events
user pin/dismiss preferences
catalog surface rules
```

An implementation may maintain a local or server-side projection:

```text
active_items(room_id, user_id)
```

Suggested fields:

```text
room_id
user_id
plugin
instance_id
source_event_id
state
priority
auto_pinned
user_pinned
dismissed_at
updated_at
```

---

## User dismissal

If a block is dismissible, the user may remove it from their active surface.

Dismissal should not mutate plugin state.

It only affects that user's projection.

Example:

```json
{
  "type": "m.ui.surface.dismissed",
  "content": {
    "plugin": "checklist",
    "instance_id": "monthly_bills_2026_05",
    "surface": "pinned"
  }
}
```

---

## Agent behavior

Agents should understand that some blocks are not just messages.

When creating a poll, checklist, approval, or workflow, the agent should expect the block to remain active until the plugin state reaches a terminal state.

The agent should not repost the same block repeatedly just to keep it visible.

Correct behavior:

```text
create plugin instance
publish one message with the plugin block
let state updates update both timeline rendering and active projection
```
