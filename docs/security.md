# Security

## Secrets

| Secret | Where it lives |
|---|---|
| Webhook Header Auth value | n8n credential + your front end's server-side config. Never in browser code. |
| OpenAI, Tavily, OpenRouter, Upload-Post keys | n8n credentials only |

The workflow JSON files in this repository reference credentials by type and a generic name only. They contain no keys, no credential ids, no instance id and no pinned data, and their webhook ids were regenerated.

## Before you share or commit your own export

Exports can leak data even though n8n never writes credential values into them. Pinned data, test executions and hard-coded values in nodes can all carry personal or secret information. Run:

```bash
python3 scripts/sanitize_n8n_export.py my-export.json workflows/my-export.json \
  --replace "My Company=>the brand" \
  --set-param "Upload photos.user=YOUR_UPLOAD_POST_PROFILE" \
  --forbid "my company" --forbid "my-upload-profile"
```

The script removes instance metadata, clears pinned data, strips credential ids, regenerates webhook ids, scans for common key formats, and refuses to write the file if a forbidden term remains.

## Threat model (summary)

| Threat | Example | Control |
|---|---|---|
| Spoofing | Someone calls the webhook directly to post spam | Header Auth on both webhooks, HTTPS only, secret kept server-side |
| Unauthenticated test form | Someone finds the form URL and burns AI credit | Deactivate or delete the form trigger in production |
| Tampering | A fake "image" (script or huge file) sent to publish | Front end decodes base64 strictly, checks the type from the bytes, caps size |
| Information disclosure | Secrets or personal data in exports or executions | Sanitize exports; enable execution pruning; restrict n8n access |
| Cost abuse | Repeated generation burns credit | Rate-limit in the front end; set provider spend caps |
| Script injection | AI output rendered as HTML in the front end | Render AI output as text only; allow only http(s) source links |
| Double posting | A timeout hides a post that went out; a retry duplicates it | Never auto-retry publish; duplicate guard in the front end |

## AI-specific risks

| Risk | Control |
|---|---|
| Prompt injection through search results or the topic | Prompts treat search results and inputs as data, not instructions; the agent's only tool is web search, so it cannot post or read files |
| Made-up facts or quotes | Accuracy rules in the prompt, sources returned with every draft, human review before publishing |
| Off-brand or harmful content | Tone rules, restricted topics in the image prompt, human approval |
| Image rights | Image prompts forbid real people, logos, text and copyrighted characters |

## Reporting a vulnerability

Please open a private security advisory on GitHub rather than a public issue.
