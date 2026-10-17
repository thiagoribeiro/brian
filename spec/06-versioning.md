# Versioning

BRIAN uses explicit schema and plugin versions.

---

## Message version

Every BRIAN message includes:

```json
{
  "schema": "brian.message",
  "version": "1.0"
}
```

---

## Plugin versioning

Plugin blocks include:

```json
{
  "type": "plugin",
  "plugin": "approval",
  "version": "1.0",
  "schema_version": "1.0"
}
```

Version identity:

```text
plugin name + plugin version + block schema version
```

---

## Compatibility rules

- Breaking changes should use a new major version.
- Apps should render unknown versions using fallback.
- Agents should not emit plugin versions that are not present in the catalog.
- Plugins should support old state where practical.
- State update events should include enough data for clients to re-render current state.

---

## Fallback requirement

Every plugin block should include `fallback_markdown`.

This is the compatibility baseline.
