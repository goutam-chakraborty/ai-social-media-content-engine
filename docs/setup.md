# Setup

This guide takes you from a fresh n8n instance to a first generated and published post.

## 1. Prerequisites

| Requirement | Notes |
|---|---|
| n8n, self-hosted | Tested on 2.43.6. Must be reachable over HTTPS if a front end calls it. |
| OpenAI API key | Used by all three AI steps (`gpt-4.1-mini`). |
| Tavily API key | Web search. The free tier (1,000 credits a month) covers about 500 posts. |
| OpenRouter API key | Image generation. Needs a positive balance. |
| Upload-Post account | With the Facebook Page, LinkedIn profile/page and/or X account you want to post to connected to one Upload-Post profile. |

## 2. Install the community nodes

In n8n go to **Settings → Community nodes → Install** and add:

- `@tavily/n8n-nodes-tavily`
- `n8n-nodes-upload-post`

Restart n8n if it asks you to.

## 3. Create credentials

Create these in **Credentials → Add credential**. The imported workflows look for the names in the right-hand column, but any name works as long as you select it in each node.

| Credential type | Suggested name | Used by |
|---|---|---|
| OpenAI API | `OpenAI account` | OpenAI Chat Model |
| Tavily API | `Tavily account` | tavily_search |
| OpenRouter API | `OpenRouter account` | Generate Image |
| Upload-Post API | `Upload-Post account` | Upload photos, Post text only |
| Header Auth | `Webhook Header Auth` | Webhook (both workflows) |

For **Header Auth**, choose a header name (for example `X-API-Key`) and a long random value, for example from `openssl rand -hex 32`. Your front end sends this header on every call. Never commit the value.

## 4. Import the workflows

1. **Workflows → Import from file** → `workflows/social-media-content-generation.json`.
2. Open every node that shows a credential warning and select your credential.
3. Repeat for `workflows/social-media-content-publish.json`.

## 5. Configure

| Where | What to change |
|---|---|
| Publish workflow → **Upload photos** and **Post text only** → *User* | Replace `YOUR_UPLOAD_POST_PROFILE` with your Upload-Post profile name. |
| Generation workflow → **Write Agent** → *System Message* | Describe your brand in the first line ("You are a senior social media copywriter for …") and adjust the `promotional` tone rule. |
| Generation workflow → **Title chain** and **Image Prompt** → system messages | Same brand description in the first line. |
| Generation workflow → **OpenAI Chat Model** | Change the model if needed (see the note on GPT-4.1 retirement in the README). |
| Generation workflow → **Generate Image** → *model* | Any OpenRouter image model id. |

Optional but recommended:

- Turn on **Retry On Fail** (2 tries, 5 s wait) for **Write Agent**, **Title chain** and **Generate Image**.
- Set execution pruning (for example 14 days) so stored executions, which contain images and request data, do not pile up.
- Set monthly spend limits in OpenAI and OpenRouter.

## 6. Activate and test

1. Activate both workflows. Use the **Production URL** shown on each Webhook node (`/webhook/social-content` and `/webhook/social-publish`), not the test URL.
2. **Generation without a front end:** open the **On form submission** node, copy its production form URL, and submit a topic. The run appears in **Executions**.
3. **Generation via webhook:** follow [examples/README.md](../examples/README.md).
4. **Publishing:** every successful publish is a real post. Test with a throwaway account or a post you are happy to keep. To re-run later nodes without posting again, open a past execution, choose **Copy to editor**, and execute only the nodes after the Upload-Post node.

## 7. Before you go live

- [ ] Both workflows active, production URLs used by the front end
- [ ] Header Auth secret set in n8n and in the front end, nowhere else
- [ ] Upload-Post profile has every platform you plan to use connected
- [ ] OpenRouter balance above the minimum
- [ ] Decide whether to keep the n8n form trigger: it has no authentication, so anyone with its URL can start a generation run (it cannot publish). Deactivate or delete it in production if the URL could leak.
- [ ] Test cases in [testing.md](testing.md) pass
