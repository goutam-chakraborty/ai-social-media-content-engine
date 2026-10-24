# Testing

Test generation freely. Test publishing with care: every successful publish is a real post. To re-test the later nodes of the publish workflow without posting, open a past execution, choose **Copy to editor**, and run only the nodes after Upload-Post.

| ID | Scenario | Input | Expected |
|---|---|---|---|
| T01 | Text-only LinkedIn post | LinkedIn, professional, no image | Reply in under 60 s; 150–300 words; hashtags and sources present |
| T02 | Facebook post with image | Facebook, casual, image on | Square, full-bleed image with no text in it; `alt_text` set |
| T03 | X post | X, hot_take | Body plus hashtags short enough to fit 280 characters (check in the front end) |
| T04 | No hashtags | `include_hashtags: false` | `hashtags` is empty |
| T05 | All 10 tones | One run per `mode` | Tone matches its rule in the Write Agent prompt |
| T06 | Publish text only | `include_image: false` | Text post; `success: true` |
| T07 | Publish with image | `include_image: true` | Post with image; `post_url` returned when the platform gives one |
| T08 | Image model fails | Wrong model id in Generate Image | Post returned with `has_image: false` |
| T09 | Image prompt fails | Break the Image Prompt parser example temporarily | Same as T08 |
| T10 | Platform not connected | Publish to a platform not linked in Upload-Post | `success: false`, error says the account is not connected |
| T11 | Wrong secret | Change the header value on the client | HTTP 403 from n8n |
| T12 | Workflow inactive | Deactivate workflow 1 | HTTP 404 "webhook not registered" |
| T13 | n8n form | Submit the test form with image and hashtags on | Run completes; `source` is `form` |
