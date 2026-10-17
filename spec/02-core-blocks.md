# Core Blocks

Core blocks are generic, low-state blocks defined directly by BRIAN.

They should not require plugin-owned tables or complex state machines.

---

## markdown

Safe Markdown text.

```json
{
  "type": "markdown",
  "text": "## Result\n\nThe workflow completed successfully."
}
```

Recommended Markdown support:

- headings
- bold / italic
- inline code
- fenced code blocks
- lists
- links
- blockquotes
- simple tables

Do not allow:

- raw HTML
- script tags
- iframes
- remote image embedding through Markdown

Images should use the `image` block.

---

## notice

Highlighted info/warning/success/error message.

```json
{
  "type": "notice",
  "level": "warning",
  "text": "This action requires approval."
}
```

Allowed levels:

```text
info
success
warning
error
```

---

## image

First-class image block.

```json
{
  "type": "image",
  "url": "mxc://example/media_01HX...",
  "alt": "Backyard layout",
  "caption": "Generated concept view",
  "mime_type": "image/png",
  "width": 1024,
  "height": 768
}
```

Use transport-owned media URIs where possible.

Avoid arbitrary remote URLs unless your app explicitly allows them.

---

## audio

First-class audio block.

```json
{
  "type": "audio",
  "url": "mxc://example/audio_01HX...",
  "mime_type": "audio/mpeg",
  "duration_ms": 42000,
  "transcript": "Optional transcript text"
}
```

---

## file

Generic file attachment.

```json
{
  "type": "file",
  "url": "mxc://example/file_01HX...",
  "filename": "report.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 123456
}
```

---

## divider

Visual separator.

```json
{
  "type": "divider"
}
```

---

## key_value

Structured key/value display.

```json
{
  "type": "key_value",
  "items": [
    {
      "key": "Status",
      "value": "Running"
    },
    {
      "key": "Execution",
      "value": "exec_123"
    }
  ]
}
```

---

## actions

Simple action buttons that publish auditable events.

```json
{
  "type": "actions",
  "actions": [
    {
      "id": "open_details",
      "label": "Open details",
      "style": "secondary",
      "event": {
        "type": "m.ui.action",
        "content": {
          "action": "open_details",
          "target": "exec_123"
        }
      }
    }
  ]
}
```

Important:

```text
Buttons should not call hidden APIs directly.
Buttons should publish auditable events.
```

For stateful actions, prefer a plugin block.

---

## reference

Reference to another event, message, artifact, or external entity.

```json
{
  "type": "reference",
  "title": "Original alert",
  "event_id": "evt_01HX...",
  "room_id": "room_01HX...",
  "description": "This message resolves the alert opened earlier."
}
```
