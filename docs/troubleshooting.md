# Troubleshooting

Start in **n8n → Executions**: every run shows each node's input, output and time.

| Symptom | Likely cause | Fix |
|---|---|---|
| Reply has no `content` | Respond to Webhook is not fed by Build result, or a field name changed | Check the Build result → Respond to Webhook connection and the field names in [api.md](api.md) |
| `sources` always empty | Field renamed (for example `source` instead of `sources`) | Rename it in Build result |
| "Publishing failed" but the post is live | Result read from the wrong key | Find platform result must pick the platform's own entry |
| `'r' expects a object but we got '[object Object]'` | A space before `{{` in an expression field | Delete everything outside `{{ … }}` |
| Convert to File: "… is not set" | The source field holds an expression instead of a field name | Set it to `body.image_base64` in Fixed mode |
| Aspect ratio ignored or rejected | Leading spaces in the value, or `size`/`quality` sent as well | Value must start with `{{`; send only `aspect_ratio` |
| OpenRouter 404 "No model found" | A chat model id used for images | Use an image model id |
| OpenAI 403 "Project does not have access to model" | Image model not enabled for your OpenAI project | Use OpenRouter for images, as these workflows do |
| Image has grey borders or empty areas | Prompt asked for space for text | Keep the "full-bleed, no empty space" rules in Generate Image |
| X post over 280 characters | Model ignored the limit | Shorten in review; keep the limits in words in the Write Agent message |
| 404 "webhook not registered" | Workflow inactive, or the test URL is used | Activate the workflow; use the production URL |
| 403 from the webhook | Header name or value does not match | Align the Header Auth credential and the client |
| Upload-Post "still processing" | Slow platform upload went async | Check the Upload-Post dashboard before publishing again |
| Very slow runs (minutes) | Tavily advanced depth or raw content turned on, or no agent iteration cap | Basic depth, 5 results, raw content off, max 5 iterations |
