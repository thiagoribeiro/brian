# Message Model

A BRIAN message is a structured message payload containing a sequence of blocks.

It is typically transported inside an event type such as `m.ui.message`.

---

## Envelope

```json
{
  "schema": "brian.message",
  "version": "1.0",
  "body": [],
  "metadata": {}
}
```

Fields:

| Field | Required | Description |
|---|---:|---|
| `schema` | yes | Must be `brian.message` for BRIAN messages. |
| `version` | yes | BRIAN message schema version. |
| `body` | yes | Ordered list of renderable blocks. |
| `metadata` | no | Optional metadata for renderers and agents. |

---

## Block ordering

`body` is ordered.

Clients should render blocks in order.

A block may reference another message/event using the `reference` block or a block-level `refs` field where supported.

---

## Message example

```json
{
  "type": "m.ui.message",
  "content": {
    "schema": "brian.message",
    "version": "1.0",
    "body": [
      {
        "type": "markdown",
        "text": "I found three options."
      },
      {
        "type": "key_value",
        "items": [
          {
            "key": "Status",
            "value": "Ready"
          }
        ]
      }
    ]
  }
}
```

---

## Block common fields

All blocks may include:

| Field | Description |
|---|---|
| `type` | Block type. Required. |
| `block_id` | Optional stable block ID within the message. |
| `refs` | Optional references to events/messages/entities. |
| `metadata` | Optional renderer metadata. |

---

## References

BRIAN supports references to other chat events/messages/entities.

Example:

```json
{
  "type": "reference",
  "title": "Original alert",
  "event_id": "evt_01HX...",
  "room_id": "room_01HX...",
  "description": "This resolution closes the alert opened earlier."
}
```

Use cases:

- alert closed referencing alert opened
- workflow result referencing workflow request
- approval referencing a proposed action
- transcript referencing an audio block
- correction referencing a previous message

---

## Fallback

Core blocks may omit fallback if the block itself is simple.

Plugin blocks should include `fallback_markdown`.

Clients that do not support a plugin block must render `fallback_markdown`.

If fallback is missing, clients should render an unsupported block notice.
