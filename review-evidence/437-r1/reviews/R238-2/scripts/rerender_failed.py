#!/usr/bin/env python3
"""Re-render the rows of a fuzz_diff.py receipt whose first render hit the API's
secondary rate limit, sequentially, and rewrite their verdicts in place.

Usage: rerender_failed.py <in.jsonl> <out.jsonl>
"""
import hashlib
import json
import sys
import time

sys.path.insert(0, sys.argv[0].rsplit("/", 1)[0])
from fuzz_diff import render  # noqa: E402
from probe import rendered_headings  # noqa: E402

rows = [json.loads(line) for line in open(sys.argv[1], encoding="utf-8")]
tally = {}
for row in rows:
    if row["verdict"] == "render-failed":
        time.sleep(0.5)
        request, response, code = render(row["page"])
        github = rendered_headings(response.decode())
        x, y = row["A"], row["B"]
        row.update(github=github, exit=code, response_bytes=response.decode(),
                   request_sha256=hashlib.sha256(request).hexdigest(),
                   response_sha256=hashlib.sha256(response).hexdigest(),
                   verdict="render-failed" if code else
                   "regression" if x == github and y != github else
                   "fix" if y == github and x != github else "both-wrong")
    tally[row["verdict"]] = tally.get(row["verdict"], 0) + 1
with open(sys.argv[2], "w", encoding="utf-8") as out:
    for row in rows:
        out.write(json.dumps(row, sort_keys=True) + "\n")
print(json.dumps(tally, sort_keys=True))
