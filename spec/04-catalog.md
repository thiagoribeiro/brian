# Block and Plugin Catalog

The agent must not rely only on prompt text to know which UI blocks exist.

The app and agent should receive a machine-readable catalog.

The catalog tells producers and renderers:

- which core blocks are supported
- which plugin blocks are installed
- which schemas must be followed
- which event types to emit
- which commands are supported
- which plugin owns state
- whether the agent may create instances directly or must call a plugin service
- how to provide fallback rendering

---

## Catalog sources

Possible sources:

- static local JSON file
- package metadata
- plugin registry endpoint
- app configuration
- runtime discovery from installed plugins

For v1, a static JSON catalog is enough.

---

## Runtime discovery endpoint

Optional future endpoint:

```http
GET /agent-blocks/catalog
```

Response:

```json
{
  "version": "1.0",
  "core_blocks": [],
  "plugins": []
}
```

---

## Agent usage rules

The Agent Core should follow these rules:

```text
1. Read the catalog before producing rich UI.
2. Prefer core blocks for stateless presentation.
3. Use plugin blocks for stateful or domain-specific interactions.
4. Do not invent block types not present in the catalog.
5. Do not invent plugin commands not present in the catalog.
6. Follow the referenced schema for every block.
7. Include fallback_markdown for every plugin block when required.
8. For stateful plugins, create or retrieve plugin instance state before publishing the UI block.
9. Observe plugin state update events instead of mutating plugin state directly.
10. If a block/plugin is unavailable, degrade to markdown/actions.
```

---

## App usage rules

The app uses the catalog to know:

- which core blocks it can render
- which plugin renderers are installed
- which fallback behavior to use
- which commands can be emitted by a user interaction
- which plugin versions are supported

If a plugin block is unknown or unsupported:

```text
render fallback_markdown
show unsupported-plugin notice if fallback is missing
never execute unknown commands silently
```
