# Agent delegation

An LLM agent may read and change plugin instances on behalf of the human who
asked for it in the conversation. This section defines how such delegated
commands are expressed, verified and audited. It does not prescribe how the
agent decides which block to use.

## Choosing blocks

Agents should pick the block that matches the intent: `checklist` for tasks,
`poll` for choices, `form_stateful` for data entry, `workflow` for real
execution and `markdown` for explanations. Simple answers stay as text.
An agent only advertises plugins present in the runtime catalog of the target
client profile (see [Catalog](04-catalog.md)).

## Agent tools

A connector exposing BRIAN to an agent typically offers three read/write
operations scoped to the requesting user and the current room:

| Operation | Behavior |
|---|---|
| List instances | Instances owned by the requester in the room, paginated, with views read from the plugin. |
| Get instance | Current view, revision and allowed commands. |
| Command instance | Sends a command using a revision read during the same turn. |

A successful change invalidates the read for the next command. Names are
resolved from the listing; when ambiguous, the agent asks the user. Room,
requester and origin message are captured from the authenticated incoming
message, never from model output.

Discovery indexes are hints. Progress is confirmed only by the plugin's
journal; history or caches never confirm that a command was applied.
User clicks and state publications update indexes without starting the model.

## Command contract

`m.plugin.command` accepts two optional fields:

- `delegation`: the human message the command acts on, as
  `request_event_id` and `request_room_seq`. The agent is the event sender;
  the requester is the author of that message.
- `expected_revision`: required whenever `delegation` is present.

Commands without delegation keep their existing meaning. Result schemas accept
the agent, requester and origin audit fields.

## Verification

The plugin runtime applies the same checks on webhook delivery, sync and
reconciliation:

1. The sender is in the configured delegating-agent allowlist.
2. The origin message exists in the transport history, in the same room,
   authored by the requester, and precedes the command.
3. The requester owns the instance.
4. `expected_revision` matches the current revision inside the per-instance
   transaction.

Origin lookups happen before the transaction. Temporary verification failures
are retried, not converted into permanent rejections. Invalid origins and stale
revisions are rejected with `m.plugin.command.rejected`. A replay with the same
hash returns the previous result even if history is temporarily unavailable.
The event keeps the agent as sender; the journal records executor and origin.

Intent persistence is the connector's job: the intent is stored before
sending, recovery reuses the same transaction ID, and conflicts are never
re-applied automatically at a different revision.

## Commands available to agents

| Plugin | Delegable commands |
|---|---|
| `checklist` | Check/uncheck, add/remove/reorder, complete, archive, cancel, refresh. |
| `poll` | Vote/change vote as the requester, close, cancel, refresh. |
| `form_stateful` | Save/submit/cancel, refresh. Fields not mentioned are preserved. |
| `workflow` | Refresh only. Cancelling an execution goes through `approval`. |
| `approval` | Read only. Decisions stay with human controls. |

## Operation lookup

The router exposes `GET /plugins/{plugin}/operations/{operation}` behind
internal authentication so a connector can read the journal entry for an
operation it submitted.
