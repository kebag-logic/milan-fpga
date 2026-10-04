#!/usr/bin/env python3
"""[R453-2] Check the round-2 author packet on milan-fpga's evidence branch.

Usage: evidence_manifest_check.py PP232_R1_DIR
PP232_R1_DIR is review-evidence/pp232-r1 of a checkout of branch pp232-review-evidence
(commit 83482f957cef27bd8968f5a4e1831f7b570b6f1d). Checks every author-r2 file's sha256
against MANIFEST.json's published_sha256, that no author-r2 file is unlisted, and that
the inner evidence-r2/MANIFEST.sha256 equals MANIFEST.json's original_sha256 per file
(path-redacted files differ in bytes from the author's originals by design).
"""
import hashlib, json, os, sys
from pathlib import Path
root = Path(sys.argv[1]); os.chdir(root)
m = {e["file"]: e for e in json.load(open("MANIFEST.json"))}
fails = 0
files = {str(Path(d, f)) for d, _, fs in os.walk("author-r2") for f in fs}
for f in sorted(files):
    e = m.get(f)
    h = hashlib.sha256(open(f, "rb").read()).hexdigest()
    if e is None:
        print("FAIL unlisted", f); fails += 1
    elif e["published_sha256"] != h:
        print("FAIL published sha256", f); fails += 1
listed = [k for k in m if k.startswith("author-r2/")]
missing = [k for k in listed if k not in files]
for k in missing:
    print("FAIL listed but absent", k); fails += 1
inner = {}
for line in open("author-r2/evidence-r2/MANIFEST.sha256"):
    h, p = line.split(None, 1)
    inner["author-r2/evidence-r2/" + p.strip().lstrip("*").removeprefix("./")] = h
for k, h in inner.items():
    if m.get(k, {}).get("original_sha256") != h:
        print("FAIL inner manifest vs original_sha256", k); fails += 1
red = sum(1 for k in listed if m[k].get("path_redacted"))
print(f"author-r2 files {len(files)}, listed {len(listed)}, inner-manifest entries {len(inner)}, path-redacted {red}")
print("RESULT", "PASS" if not fails else f"FAIL ({fails})")
sys.exit(1 if fails else 0)
