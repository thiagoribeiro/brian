# BRIAN Overview

BRIAN means **Block-based Rich Interface Notation**.

It is a notation for rendering structured, interactive, and stateful conversations in agent-native applications.

BRIAN does not define a chat server.

BRIAN does not define persistence, room membership, delivery, authentication, or sync.

BRIAN defines the content format and interaction contract that can be transported over a chat/event substrate.

---

## Goals

BRIAN should:

- let agents emit rich messages without relying on unstructured text
- keep UI actions auditable as events
- support graceful fallback rendering
- support stateful plugin interactions
- allow app renderers and agent producers to discover supported blocks
- avoid hiding side effects behind button clicks
- separate chat permissions from plugin/domain permissions

---

## Non-goals

BRIAN does not attempt to be:

- a general chat protocol
- a federation protocol
- a workflow engine
- an agent framework
- a component runtime
- a browser iframe sandbox
- a remote code execution model
- a replacement for app-native UI

---

## Core principle

```text
Transport moves events.
BRIAN defines rich message shapes.
Plugins own state and behavior.
Apps render supported blocks.
Agents use the catalog to know what they can emit.
```

---

## Conceptual layering

```text
Application / Agent / System
  produces BRIAN messages and plugin commands

BRIAN / Agent Blocks
  defines message content, blocks, plugin envelope, catalog, fallback

Transport
  stores, orders, authorizes, and syncs events

Renderer
  turns BRIAN blocks into UI

Plugin runtime
  owns stateful interaction behavior
```

---

## Event types

BRIAN recommends the following event types:

```text
m.ui.message
m.plugin.instance.created
m.plugin.command
m.plugin.command.accepted
m.plugin.command.rejected
m.plugin.command.failed
m.plugin.state.updated
```

Transports may rename these event types, but the semantics should remain equivalent.

---

## First-class concepts

### Message

A message is a renderable container with one or more blocks.

### Core block

A core block is a stateless or low-state UI block that can be rendered directly by an app.

Examples:

- markdown
- image
- audio
- file
- notice
- key_value
- actions

### Plugin block

A plugin block points to plugin-owned state and behavior.

Examples:

- approval
- workflow
- form_stateful
- poll
- checklist

### Catalog

A machine-readable description of supported blocks, plugins, schemas, commands, and fallback rules.

### Fallback

Every plugin block should provide a `fallback_markdown` field so unknown clients can render something useful.
