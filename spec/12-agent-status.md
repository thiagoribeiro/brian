# Agent status

The `agent_status` plugin reports the progress of one agent request: context
gathering, waiting for the model, tool calls, formatting and publication.
Background work started by the request keeps the report active until it
finishes; later executions belong to the `workflow` plugin.

## Contract and authorship

Catalog entry: plugin `agent_status`, version `1.0`, no commands. Schemas:
`schemas/plugins/agent-status-block-1.0.json` and
`schemas/requests/agent-status-create-data-1.0.json`. Only the agent runtime
creates and updates reports. They are excluded from agent-facing creation and
editing tools and from the instance index used as model context.

Identity is `request_id` + room + owner; the instance uses the idempotency key
`agent-status:<request_id>`. Timestamps are UTC RFC 3339. Snapshots keep at
most 200 steps, report `history_total`, and keep up to 100 concurrent
activities. Each call has its own ID, including parallel calls. Entries carry
state, timestamps and duration; they never contain arguments, model output or
internal reasoning.

States: `running`, `waiting_user`, `completed`, `failed`, `interrupted`.
A failed tool call ends its own entry; the request may continue.
How the model signals that it is waiting for clarification is up to the
connector (for example a reply prefix marker that the connector strips before
persisting or sending the text); it must not add tools, model rounds or
classification calls.

## Transport and recovery

Private authenticated endpoint:
`POST /plugins/agent_status/instances/{id}/updates` with `room_id`,
`owner_id`, `producer_id` and `state`. The router requires the internal token;
the plugin requires an allowlisted producer, the original identity and a valid
snapshot. Older sequences never replace the view; replays are idempotent;
reusing a sequence with different content is a conflict.

The plugin publishes one initial `m.ui.message` and then snapshots as
`m.plugin.state.updated`, using its journal and stable transaction IDs.
Clients keep their usual publisher/room/revision checks. Clients without a
renderer show the envelope's Markdown fallback.

Recommended producer behavior:

- Persist steps immediately; batch publications up to 1 s; publish terminal
  states immediately.
- Retry with backoff from 1 s up to 30 s.
- Heartbeat every 15 s without adding steps. Clients show "no recent update"
  after 60 s while keeping the last known state.
- Instrumentation is best effort and must never block tools or the reply.

On restart, requests with a ready reply only resend it and finalize the
report. Requests that lost their execution become `interrupted` and are not
re-admitted to the model. Recovering a card publication never re-runs a tool.

Transports may exclude `agent_status` events from push notifications; other
events keep their normal delivery.

## Client behavior

Cards start collapsed: latest status, indicator and expand control. Expanding
shows history, timestamps, durations and results. The expanded/collapsed
choice is a local per-user preference and survives updates and reconnects.
The header shows the most recent active activity and counts the others.
`running` and `waiting_user` appear on the active surface automatically;
terminal states leave it, preserving manual pins and the timeline anchor.
There are no cancel controls and no streaming of the reply.

## Deployment notes

Emission should be disabled by default. Deploy schemas, router/plugin and
clients before enabling it. Clients must be built with the trusted agent and
publisher IDs so cards render interactively instead of as fallback.
The plugin token is exclusive to the plugin and never shipped to clients.
