#!/usr/bin/env python3
"""R222-3: replace every other reviewer's comment body in a saved GitHub
comments receipt by its SHA-256, so this packet carries no other reviewer's
report. A body is redacted when its first token is an `[R<n>...]` identity
other than `[R222]`. Writes the file in place and prints what it replaced.
Usage: 19_redact_other_reviewers.py <comments.json>...
"""
import hashlib
import json
import re
import sys

for path in sys.argv[1:]:
    data = json.load(open(path))
    n = 0
    for c in data:
        body = c.get("body") or ""
        m = re.match(r"\[(R\d+[^\]]*)\]", body)
        if m and not m.group(1).startswith("R222"):
            digest = hashlib.sha256(body.encode()).hexdigest()
            c["body"] = f"<redacted by R222-3: [{m.group(1)}] body, sha256 {digest}>"
            n += 1
            print(f"{path.rsplit('/', 1)[-1]}: comment {c['id']} [{m.group(1)}] -> sha256 {digest}")
    json.dump(data, open(path, "w"), indent=1)
    print(f"{path.rsplit('/', 1)[-1]}: {n} body(ies) redacted")
