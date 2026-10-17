# Runtime integration

Canonical events are `m.ui.message` (`content.schema = brian.message`),
`m.plugin.command`, `m.plugin.state.updated`, `m.plugin.instance.created`,
`m.ui.surface.dismissed`, and `m.ui.surface.preference.updated`.
Historical `brian.message`, `brian.block.action`, `brian.block.patch` and
`m.agent.ui.message` event types must not be implemented.

The transport (for example [nimlet](https://github.com/thiagoribeiro/nimlet))
carries these payloads unchanged and does not depend on BRIAN or its plugins.
Consumers own missed-event recovery and deduplication. A workflow engine
(for example Trama) owns durable multi-step execution; domain endpoints remain idempotent
even if repeated admission creates multiple executions.

Plugin identity is `(room_id, plugin, instance_id)`. Views and updates carry
a positive `revision`; clients ignore older revisions and match only inside
the same room. A state update is trusted only from the configured service
publisher. A human-authored event with the same type is not authoritative.

Surface preferences apply to the authenticated event sender only. Pinning or
dismissing never changes plugin state. Timeline records remain append-only;
focus and active surfaces render the latest trusted view.

The runtime catalog is the intersection of this specification and installed
plugins. `future` entries are unavailable until implemented. `refresh` is a
runtime command which republishes the authoritative view through the transport;
clients never fetch state directly from plugins.

Approval decides permission, not execution success. The action remains owned
by the requesting connector and is bound to the requester, room, resource and
frozen arguments. Cancellation of provider executions is cooperative.

Command results may include `command_event_id` to settle an in-flight client
interaction, including a refresh which does not increment revision.
Permanent refusals are published as `m.plugin.command.rejected` and correlate
the original event ID. Invalid commands must not poison a consumer cursor.

`schemas/requests/*-create-data-1.0.json` describes the data argument accepted
when creating each installed plugin. A creation capability is distinct from
commands on an existing instance. Workflow only supports refresh; changing
its execution belongs to the provider/owning connector, under domain policy.

The first installation can seed a consumer cursor at a documented cutoff.
That is an adoption decision, not a change to transport delivery guarantees.
On subsequent starts, the consumer-owned durable cursor always wins.
