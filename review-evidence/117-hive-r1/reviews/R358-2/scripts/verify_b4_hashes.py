#!/usr/bin/env python3
"""Check every hash in the findings page's B4 table against a published packet.

Usage: verify_b4_hashes.py <findings.md> <packet-root>
<packet-root> is an extraction of review-evidence/117-hive-r1 at the pinned commit.
Prints one line per B4 row: file, page hash, published hash, MANIFEST.json
original/published, and a classification. Exit 0 only when every row either
matches the published bytes or is one of the page's declared redacted rows whose
page hash equals MANIFEST.json original_sha256 and whose published bytes equal
MANIFEST.json published_sha256.
"""
import hashlib
import json
import pathlib
import re
import sys

page = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
root = pathlib.Path(sys.argv[2])

sec = page.split("| B4 artifact in packet | SHA-256 |", 1)[1].split("\n\n", 1)[0]
rows = re.findall(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|$", sec, re.M)
declared = dict(re.findall(r"^- `([^`]+)`: `([0-9a-f]{64})`\.$", page, re.M))
manifest = {e["file"]: e for e in json.loads((root / "MANIFEST.json").read_text())}
author_manifest = {}
for line in (root / "author" / "MANIFEST.sha256").read_text().splitlines():
    h, name = line.split(None, 1)
    author_manifest[name.lstrip("*").removeprefix("./")] = h

bad = 0
print(f"rows={len(rows)} declared_redacted={len(declared)}")
for name, h in rows:
    path = root / "author" / name
    pub = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "MISSING"
    m = manifest.get("author/" + name, {})
    am = author_manifest.get(name, "absent")
    if pub == h:
        cls = "MATCH-PUBLISHED"
        if name in declared:
            cls += "-BUT-DECLARED-REDACTED"
            bad += 1
    elif name in declared and declared[name] == h and m.get("original_sha256") == h \
            and m.get("published_sha256") == pub:
        cls = "REDACTED-MAPPED"
    else:
        cls = "UNEXPLAINED"
        bad += 1
    print(f"{name} page={h} published={pub} mj_orig={m.get('original_sha256')} "
          f"mj_pub={m.get('published_sha256')} author_manifest={am} -> {cls}")
for name in declared:
    if name not in dict(rows):
        print(f"declared-but-not-in-table {name}")
        bad += 1
print("RESULT", "PASS" if bad == 0 else f"FAIL({bad})")
sys.exit(1 if bad else 0)
