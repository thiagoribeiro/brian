# Future Plugins

This document defines draft specifications for future BRIAN plugins.

These plugins are intentionally not required by MVP clients.

They may have:

- specs
- schemas
- examples
- catalog entries

But their catalog `status` must be `future` or `experimental` until implemented.

---

## Lifecycle status

Catalog entries should include:

```text
mvp
future
experimental
deprecated
```

Rules:

```text
Agents must not emit future plugins unless the runtime catalog says they are installed and supported.
Apps must fallback gracefully when a plugin is unknown or unsupported.
Future plugin schemas are design contracts, not MVP requirements.
```

---

## checklist

Shared checklist state.

Use cases:

- home tasks
- workflow preparation
- deployment checklist
- shopping/planning list
- maintenance routine

States:

```text
open
completed
archived
cancelled
```

Commands:

```text
check_item
uncheck_item
add_item
remove_item
reorder_item
complete
archive
cancel
```

---

## poll

Lightweight voting and choice selection.

Use cases:

- family decisions
- team decisions
- agent asks a group to choose one option
- choose between proposed plans

States:

```text
open
closed
cancelled
```

Commands:

```text
vote
change_vote
close
cancel
```

---

## plan

Agent-generated execution plan with user-visible steps.

Use cases:

- show proposed steps before execution
- track progress through a multi-step agent task
- allow the user to approve/modify plan steps

States:

```text
draft
proposed
approved
running
completed
cancelled
rejected
```

Commands:

```text
approve
reject
modify
start
cancel
```

---

## timeline

Structured timeline of related events.

Use cases:

- workflow progress
- incident lifecycle
- alert opened/closed/reopened
- agent task history

May be a direct block if read-only.
Should become a plugin if it dynamically aggregates events or owns state.

---

## table

Structured tabular view.

Use cases:

- search results
- tool output
- comparison lists
- inventory/status data

Can be a direct block if static.
Can become a plugin if sortable/filterable/stateful.

---

## chart

Chart/metric visualization.

Use cases:

- workflow latency
- system metrics
- expense summaries
- usage summaries
- sensor history

Should be plugin-owned if it refreshes, queries data, or maintains chart state.

---

## log_stream

Log/trace viewer.

Use cases:

- workflow execution logs
- agent tool execution logs
- system diagnostics
- home automation logs

Likely plugin-owned because it may need pagination, streaming, filtering, and permissions.

---

## document_collab

Lightweight document/card state.

Use cases:

- shared notes
- agent-generated drafts
- editable plans
- decision records

Should be plugin-owned if it supports editing/versioning.

---

## integration_preview

Structured preview for external systems.

Use cases:

- GitHub PR
- calendar event
- email thread
- workflow execution
- Home Assistant entity
- Mikrotik status

The preview renderer can be generic, but provider-specific integrations should own fetching/refreshing state.

---

## memory_card

Human-visible view of agent memory/context.

Use cases:

- show what the agent remembered
- ask user to confirm a memory
- edit/delete memory
- show source references

This belongs to a memory plugin/runtime, not the chat transport.

---

## webhook_trigger

Represents an external callback/waiting state.

Use cases:

- waiting for workflow callback
- waiting for external approval
- waiting for long-running process

Useful for callback/scheduler architectures.
