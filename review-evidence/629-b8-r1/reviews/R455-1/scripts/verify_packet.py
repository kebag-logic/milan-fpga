#!/usr/bin/env python3
"""Verify the published B8 evidence tree against its MANIFEST.json, and the
B8 page's evidence-hash table (rows with a 64-hex hash) against the files.

usage: verify_packet.py <evidence-root: review-evidence/629-b8-r1> <page.md> <out.txt>
"""
import hashlib
import json
import os
import re
import sys

root, page, out = sys.argv[1:4]
L = []
m = json.load(open(os.path.join(root, "MANIFEST.json")))
bad = red = 0
listed = set()
for e in m:
    p = os.path.join(root, e["file"]); listed.add(e["file"])
    if not os.path.exists(p):
        L.append(f"MISSING {e['file']}"); bad += 1; continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != e["published_sha256"]:
        L.append(f"MISMATCH {e['file']}"); bad += 1
    if e["original_sha256"] != e["published_sha256"] or e.get("path_redacted"):
        red += 1; L.append(f"publication-redacted {e['file']} path_redacted={e.get('path_redacted')}")
allf = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs} - {"MANIFEST.json"}
L.append(f"MANIFEST.json entries {len(m)}; bad {bad}; publication-redacted {red}; unlisted {sorted(allf - listed)}")
txt = open(page).read().splitlines()
start = next(i for i, l in enumerate(txt) if l.startswith("### B8: artifact hashes"))
ok = nb = 0
for l in txt[start:]:
    mm = re.match(r"\| `([^`]+)`.*\| ([\d,]+) \| `([0-9a-f]{64})` \|", l)
    if not mm:
        continue
    rel, size, h = mm.group(1), int(mm.group(2).replace(",", "")), mm.group(3)
    p = os.path.join(root, "author", rel)
    if not os.path.exists(p):
        L.append(f"page row not in packet (raw file, outside packet): {rel}"); continue
    d = open(p, "rb").read()
    good = len(d) == size and hashlib.sha256(d).hexdigest() == h
    ok += good; nb += (not good)
    if not good:
        L.append(f"PAGE ROW BAD {rel}")
L.append(f"page evidence rows verified {ok}; bad {nb}")
open(out, "w").write("\n".join(L) + "\n")
print("\n".join(L[-6:]))
