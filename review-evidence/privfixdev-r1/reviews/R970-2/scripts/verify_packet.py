#!/usr/bin/env python3
"""Reviewer probe: check a downloaded author packet against its own manifest.

Usage: verify_packet.py <dir holding MANIFEST.json and author/>
Checks every listed file's sha256 against `published_sha256`, that no file
under author/ is unlisted, that the base and head firmware manifests of the
`dev` tree are byte-identical, and counts that manifest's rows by class.
"""
import collections
import hashlib
import json
import os
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
manifest = json.loads((root / "MANIFEST.json").read_text())
listed = {entry["file"] for entry in manifest}
bad = [
    entry["file"]
    for entry in manifest
    if hashlib.sha256((root / entry["file"]).read_bytes()).hexdigest() != entry["published_sha256"]
]
on_disk = {
    str(pathlib.Path(folder, name).relative_to(root))
    for folder, _dirs, names in os.walk(root / "author")
    for name in names
}
print(f"manifest entries: {len(manifest)}; sha256 mismatches: {len(bad)} {bad}")
print(f"unlisted files under author/: {sorted(on_disk - listed)}; listed but absent: {sorted(listed - on_disk)}")
print("entries published with paths redacted:", sorted(e["file"] for e in manifest if e["path_redacted"]))

firmware = root / "author/receipts/firmware"
base, head = (firmware / "dev-base.manifest.tsv").read_bytes(), (firmware / "dev-head.manifest.tsv").read_bytes()
print("dev firmware manifests byte-identical:", base == head, hashlib.sha256(head).hexdigest())
classes = collections.Counter(row.split("\t", 1)[0] for row in head.decode().splitlines() if row)
print("dev head manifest rows by class:", dict(classes), "total", sum(classes.values()))
for name in ("dev-compare.txt",):
    rows = [r.split("\t") for r in (root / "author/receipts/gates" / name).read_text().splitlines() if "\t" in r][1:]
    print(f"{name}: gates {len(rows)}; base rc != 0: {sum(r[1] != '0' for r in rows)}; head rc != 0: {sum(r[2] != '0' for r in rows)}")
