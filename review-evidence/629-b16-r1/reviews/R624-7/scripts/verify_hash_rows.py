#!/usr/bin/env python3
"""R624-7: every `| `<path>` ... | <bytes> | `<sha256>` |` row in lane B16's section against a packet directory.
usage: python3 -I verify_hash_rows.py <findings.md> <packet dir> <out.json>"""
import hashlib, json, re, sys
from pathlib import Path
page, pkt, out = sys.argv[1:4]
lines = Path(page).read_text(encoding="utf-8").splitlines()
s = next(i for i, x in enumerate(lines) if x.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
row = re.compile(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$")
res = []
for i in range(s, e):
    m = row.match(lines[i])
    if not m:
        continue
    f = Path(pkt) / m.group(1)
    b = f.read_bytes() if f.is_file() else None
    res.append(dict(line=i + 1, path=m.group(1), bytes_row=int(m.group(2).replace(",", "")), sha_row=m.group(3),
                    exists=b is not None, bytes_file=len(b) if b is not None else None,
                    sha_file=hashlib.sha256(b).hexdigest() if b is not None else None))
    res[-1]["equal"] = bool(b is not None and res[-1]["bytes_file"] == res[-1]["bytes_row"] and res[-1]["sha_file"] == res[-1]["sha_row"])
summary = dict(section_lines=[s + 1, e], rows=len(res), equal=sum(r["equal"] for r in res),
               unequal=[(r["line"], r["path"]) for r in res if not r["equal"]])
json.dump(dict(summary=summary, rows=res), open(out, "w"), indent=1)
print(json.dumps(summary))
