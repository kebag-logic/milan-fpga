#!/usr/bin/env python3
"""R624-10: every packet-file hash row of lane B16's section, against the published round-10 packet.

usage: python3 -I check_hash_rows.py <findings.md> <published review-evidence/629-b16-r1 dir> <out.json>

A row is a table line of the section whose first cell names a packet path in backticks and whose last cell is
a 64-hex SHA-256 in backticks, with the size in the cell before it. Rows naming raw bench files (pcap, raw,
jsonl kept outside the packet) are matched against the packet's RAW-ARTIFACTS.json instead. For a packet file,
the row must equal the MANIFEST.json `original_sha256` of `author-r10/<path>` and, when that file is not
path-redacted, the published file's size and SHA-256.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

doc, pub, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
lines = doc.read_text(encoding="utf-8").split("\n")
s = next(i for i, x in enumerate(lines) if x.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
man = {e["file"]: e for e in json.loads((pub / "MANIFEST.json").read_text())}
raw = json.loads((pub / "author-r10/RAW-ARTIFACTS.json").read_text())
rawsha = {}
for f in raw["files"]:
    rawsha.setdefault(f.get("sha256"), []).append(f)
ROW = re.compile(r"^\|(.*)\|\s*([\d,]+|Withheld|-)\s*\|\s*`([0-9a-f]{64})`\s*\|$")
res, bad = [], 0
for i in range(s, len(lines)):
    m = ROW.match(lines[i])
    if not m:
        continue
    cells = [c.strip() for c in m.group(1).split("|")]
    size, sha = m.group(2), m.group(3)
    path = next((re.match(r"`([^`]+)`", c).group(1) for c in cells if re.match(r"`[^`]+`", c)), None)
    e = man.get(f"author-r10/{path}") if path else None
    if e:
        p = pub / e["file"]
        ok = e["original_sha256"] == sha
        if not e.get("path_redacted"):
            b = p.read_bytes()
            ok = ok and hashlib.sha256(b).hexdigest() == sha and f"{len(b):,}" == size
        kind = "packet"
    else:
        hits = rawsha.get(sha, [])
        sizes = [h.get("bytes") for h in hits]
        ok = bool(hits) and (any(isinstance(b, str) and b.startswith("withheld") for b in sizes) if size == "Withheld"
                             else any(isinstance(b, int) and f"{b:,}" == size for b in sizes))
        kind = "raw"
    bad += not ok
    res.append(dict(line=i + 1, path=path, kind=kind, size=size, sha256=sha, ok=ok))
out.write_text(json.dumps(dict(rows=len(res), bad=bad, packet=sum(r["kind"] == "packet" for r in res),
                               raw=sum(r["kind"] == "raw" for r in res), results=res), indent=1) + "\n")
print("rows", len(res), "packet", sum(r["kind"] == "packet" for r in res), "raw", sum(r["kind"] == "raw" for r in res),
      "bad", bad)
for r in res:
    if not r["ok"]:
        print("BAD", r)
