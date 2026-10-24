#!/usr/bin/env python3
"""Sanitize an n8n workflow export before sharing it publicly.

What it does:
  * removes instance-specific metadata (workflow id, versionId, instanceId)
  * clears pinned data and sets the workflow to inactive
  * strips credential ids and gives credentials generic names
  * regenerates webhook ids so public URLs cannot be guessed from the export
  * applies optional text replacements (--replace "old=>new")
  * fails if any --forbid term (case-insensitive) is still present

Usage:
  python3 sanitize_n8n_export.py input.json output.json \
      --replace "Acme Ltd=>the brand" --forbid acme --forbid my_upload_profile
"""
import argparse, json, re, sys, uuid

GENERIC_CRED_NAMES = {
    "openAiApi": "OpenAI account",
    "tavilyApi": "Tavily account",
    "openRouterApi": "OpenRouter account",
    "uploadPostApi": "Upload-Post account",
    "httpHeaderAuth": "Webhook Header Auth",
}
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),          # OpenAI / OpenRouter style keys
    re.compile(r"tvly-[A-Za-z0-9_-]{16,}"),        # Tavily keys
    re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),  # JWTs
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{16,}"),
]

def replace_strings(obj, rules):
    if isinstance(obj, dict):
        return {k: replace_strings(v, rules) for k, v in obj.items()}
    if isinstance(obj, list):
        return [replace_strings(v, rules) for v in obj]
    if isinstance(obj, str):
        for old, new in rules:
            obj = obj.replace(old, new)
    return obj

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--replace", action="append", default=[], help='"old=>new" text replacement')
    ap.add_argument("--set-param", action="append", default=[], help='"Node name.param=value"')
    ap.add_argument("--forbid", action="append", default=[], help="term that must not remain")
    a = ap.parse_args()

    wf = json.load(open(a.input, encoding="utf-8"))
    for key in ("id", "versionId", "meta", "shared", "homeProject", "triggerCount"):
        wf.pop(key, None)
    wf["pinData"] = {}
    wf["active"] = False
    wf["tags"] = []

    for node in wf.get("nodes", []):
        if "webhookId" in node:
            node["webhookId"] = str(uuid.uuid4())
        for ctype, cred in (node.get("credentials") or {}).items():
            node["credentials"][ctype] = {"id": "", "name": GENERIC_CRED_NAMES.get(ctype, ctype)}

    for item in a.set_param:
        target, value = item.split("=", 1)
        name, param = target.rsplit(".", 1)
        for node in wf["nodes"]:
            if node["name"] == name:
                node["parameters"][param] = value

    rules = [tuple(r.split("=>", 1)) for r in a.replace]
    wf = replace_strings(wf, rules)

    text = json.dumps(wf, indent=2, ensure_ascii=False)
    problems = [t for t in a.forbid if t.lower() in text.lower()]
    problems += [p.pattern for p in SECRET_PATTERNS if p.search(text)]
    if problems:
        sys.exit(f"Refusing to write {a.output}: still contains {problems}")
    open(a.output, "w", encoding="utf-8").write(text + "\n")
    print(f"OK  {a.output}")

if __name__ == "__main__":
    main()
