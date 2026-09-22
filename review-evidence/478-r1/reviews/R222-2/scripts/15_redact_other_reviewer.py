#!/usr/bin/env python3
"""Replace the body of any `[R221]`-led comment in the saved PR comment
receipt with a placeholder carrying its SHA-256 and length, without printing
it. The R221 report was not opened by this round; this keeps the receipt to
what the round used while leaving the record verifiable against GitHub."""
import hashlib
import json
import sys

path = sys.argv[1]
data = json.load(open(path, encoding="utf-8"))
for c in data:
    body = c.get("body") or ""
    if body.lstrip().startswith("[R221]"):
        digest = hashlib.sha256(body.encode()).hexdigest()
        c["body"] = f"<[R221] comment body not opened by R222; sha256 {digest}, {len(body)} chars>"
        print(f"redacted comment {c['id']}: sha256 {digest}")
json.dump(data, open(path, "w", encoding="utf-8"), indent=1)
