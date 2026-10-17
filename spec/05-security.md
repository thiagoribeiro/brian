# Security Model

BRIAN separates communication permissions from plugin/domain permissions.

---

## Layering

```text
Transport:
  Can this participant publish this event type in this room?

Plugin:
  Can this participant execute this command on this plugin instance?

Domain system:
  Can this approved action cause an external side effect?
```

This avoids mixing chat permission with business permission.

---

## Button safety

Buttons and UI actions should not directly call hidden APIs.

They should publish auditable events.

Bad:

```text
Button directly sends money or calls external API.
```

Good:

```text
Button publishes m.plugin.command.
Plugin validates actor, state, policy, and domain rules.
Plugin executes or delegates the effect.
Plugin publishes state update.
```

---

## Fallback safety

Fallback Markdown should be safe to render.

Fallback should not contain:

- raw HTML
- scripts
- iframes
- remote image embeddings
- hidden instructions

---

## Unknown plugin behavior

If the app sees an unknown plugin:

1. render `fallback_markdown` if present
2. otherwise render unsupported plugin notice
3. do not emit unknown commands
4. do not infer command semantics from labels

---

## Event authenticity

Consumers should validate the event sender where possible.

For example, apps and agents should only trust `m.plugin.state.updated` events from the plugin/service identity authorized to manage that plugin instance.

## Limited agent delegation

Only explicitly configured agent IDs may delegate supported commands. The
plugin fetches the referenced message through the transport history and
checks event ID, room sequence (`room_seq`), room, message type and author. The source
must precede the command and belong to the instance owner. Explicit user
intent is required by the agent policy; references and card content are not
instructions. Approval decisions remain human controls.

Revision checks happen in the existing instance transaction. Temporary
history failures remain retryable; invalid origin and revision conflicts
are journaled rejections. Committed replays return the prior operation.
The journal records the real agent, requester and originating event without
impersonating the human. Transport delivery and workflow-engine contracts are unchanged.
