#!/usr/bin/env python3
"""Check every B4-cited SHA-256 on the findings page against the public packet.

Usage: check_b4_hashes.py <page.md> <extracted review-evidence/117-hive-r1 dir>

For each row of the "B4 artifact in packet" table, report whether the cited
hash equals the published file's bytes, and otherwise whether MANIFEST.json
maps it (original_sha256 -> published_sha256) with the published copy matching
and the page listing it as redacted. Exit 1 on any unexplained mismatch.
"""
import hashlib
import json
import pathlib
import re
import sys

page = pathlib.Path(sys.argv[1]).read_text()
root = pathlib.Path(sys.argv[2])
manifest = {e["file"]: e for e in json.loads((root / "MANIFEST.json").read_text())}
author_manifest = {}
for line in (root / "author" / "MANIFEST.sha256").read_text().splitlines():
    h, name = line.split(maxsplit=1)
    author_manifest[name.lstrip("*").removeprefix("./")] = h

table = re.findall(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|$",
                   page.split("| B4 artifact in packet | SHA-256 |", 1)[1].split("\n\n", 1)[0],
                   re.M)
redacted_listed = dict(re.findall(r"^- `([^`]+)`: `([0-9a-f]{64})`\.$", page, re.M))
bad = 0
print(f"table rows: {len(table)}; listed redacted: {len(redacted_listed)}")
for name, cited in table:
    f = root / "author" / name
    actual = hashlib.sha256(f.read_bytes()).hexdigest()
    m = manifest.get(f"author/{name}", {})
    am = author_manifest.get(name)
    if actual == cited:
        status = "MATCHES-PUBLISHED"
        ok = name not in redacted_listed
    else:
        mapped = m.get("original_sha256") == cited and m.get("published_sha256") == actual
        status = "REDACTED-MAPPED" if mapped else "UNEXPLAINED"
        ok = mapped and redacted_listed.get(name) == cited
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {name:26s} {status:18s} cited={cited[:12]} "
          f"published={actual[:12]} author_manifest={'=' if am == cited else (am or '-')[:12]} "
          f"MANIFEST.json orig={m.get('original_sha256','-')[:12]} pub={m.get('published_sha256','-')[:12]}")
for name in redacted_listed:
    if name not in dict(table):
        bad += 1
        print(f"BAD listed-redacted {name} not in table")
print("RESULT", "PASS" if bad == 0 else f"FAIL ({bad})")
sys.exit(1 if bad else 0)
