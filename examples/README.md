# Examples

Set your values in a local `.env` (copy `.env.example`; never commit `.env`):

```bash
cp .env.example .env    # then edit .env
set -a; source .env; set +a
```

## Generate a draft

```bash
curl -sS -X POST "$N8N_BASE_URL/webhook/social-content" \
  -H "Content-Type: application/json" \
  -H "$N8N_WEBHOOK_HEADER: $N8N_WEBHOOK_SECRET" \
  --max-time 170 \
  -d @examples/generate-request.json | tee draft.json
```

The reply follows [generate-response.sample.json](generate-response.sample.json). Review and edit the draft before publishing.

## Publish (this creates a real post)

```bash
curl -sS -X POST "$N8N_BASE_URL/webhook/social-publish" \
  -H "Content-Type: application/json" \
  -H "$N8N_WEBHOOK_HEADER: $N8N_WEBHOOK_SECRET" \
  --max-time 120 \
  -d @examples/publish-request.json
```

To publish with the generated image, add `"include_image": true`, `"image_base64"`, `"image_mime"` and `"alt_text"` from the draft to the request body.

Do not retry a publish that timed out until you have checked the platform: the post may already be live.
