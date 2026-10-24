# Webhook API

Both workflows are called with `POST` and a JSON body, and both require the Header Auth header you configured (for example `X-API-Key: <secret>`). Field names must match exactly: extra fields are ignored, and missing or misspelt fields are treated as empty.

| Endpoint | Workflow | Typical time |
|---|---|---|
| `POST https://<your-n8n-host>/webhook/social-content` | Content Generation | 9 s text only, 17 s with image |
| `POST https://<your-n8n-host>/webhook/social-publish` | Content Publish | about 16 s with image |

Both reply synchronously. Set client timeouts generously: about 170 s for generation (the image call alone may take up to 120 s) and 120 s for publishing. Respond to Webhook may wrap the reply in a one-item array (`[ { … } ]`), so unwrap it if present.

## 1. Generate request

| Field | Type | Required | Allowed values |
|---|---|---|---|
| `topic` | string | yes | 5–500 characters recommended |
| `platform` | string | yes | `facebook`, `linkedin`, `x` |
| `mode` | string | yes | `professional`, `business`, `educational`, `funny`, `inspirational`, `storytelling`, `thought_leadership`, `promotional`, `casual`, `hot_take` |
| `include_image` | boolean | yes | `true` to generate an image |
| `include_hashtags` | boolean | no | defaults to `true` |

```json
{
  "topic": "How small businesses save time with AI automation",
  "platform": "linkedin",
  "mode": "professional",
  "include_image": true,
  "include_hashtags": true
}
```

## 2. Generate response

| Field | Type | Notes |
|---|---|---|
| `title` | string | Hook line |
| `alternatives` | string[] | Up to 2 alternative hooks |
| `content` | string | Post body |
| `hashtags` | string[] | Empty when hashtags were not requested |
| `sources` | `{title, url}[]` | Pages the agent used; show them for fact checking |
| `platform` | string | Echo of the normalized platform |
| `has_image` | boolean | `true` when an image was generated |
| `image_base64` | string | Base64 image, empty when there is none |
| `image_mime` | string | For example `image/png` |
| `alt_text` | string | Accessibility text for the image |

If an image was requested but `has_image` is `false`, the image step failed and the text post is still usable. Validate `image_base64` (decodable, PNG/JPEG/WebP, size cap) before showing or re-sending it.

## 3. Publish request

| Field | Type | Required | Notes |
|---|---|---|---|
| `platform` | string | yes | `facebook`, `linkedin` or `x` |
| `final_text` | string | yes | Exactly what is posted: title, content and hashtags joined by blank lines |
| `include_image` | boolean | yes | `true` to post with the image |
| `image_base64` | string | when image | The approved image |
| `image_mime` | string | when image | MIME type of the image |
| `alt_text` | string | when image | Image alt text |
| `title`, `content`, `hashtags` | | optional | Accepted for logging; `final_text` is what gets posted |

Check `final_text` against the platform limit before sending: X 280, LinkedIn 3,000, Facebook 63,206 characters.

## 4. Publish response

| Field | Type | Meaning |
|---|---|---|
| `success` | boolean | The platform accepted the post, or Upload-Post accepted it for background processing |
| `post_url` | string | Link to the live post, when the platform returns one |
| `error` | string | Platform or Upload-Post error text when `success` is `false` |
| `message` | string | `Posted to <platform>.` or a "still processing" note |

`success` is taken from the platform's own entry in the Upload-Post response, not from Upload-Post's top-level `success`, which can be `true` even when the platform rejected the post.

**Never retry a publish automatically.** A timeout can hide a post that did go out; check the platform before trying again. A short duplicate guard in the front end (for example, refusing the same text within 2 minutes) prevents double posts.

See [../examples](../examples) for complete sample payloads.
