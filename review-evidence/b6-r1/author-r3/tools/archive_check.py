#!/usr/bin/env python3
"""Resolve every SHA-256 on the B6 findings page against the evidence archive (read-only).

usage: archive_check.py <evidence_repo> <archive_commit> <page.md>

Reads, with `git show` only: review-evidence/b6-r1/MANIFEST.json and
review-evidence/b6-r1/author/RAW-ARTIFACTS.json at <archive_commit>, and every file the
manifest lists, which it re-hashes against published_sha256. Each 64-hex hash on the page
must equal an original_sha256 in the manifest or a sha256 in RAW-ARTIFACTS.json.
"""
import hashlib
import json
import re
import subprocess
import sys

repo, commit, page = sys.argv[1:4]
base = "review-evidence/b6-r1"


def show(path):
    return subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], check=True,
                          capture_output=True).stdout


man = json.loads(show(f"{base}/MANIFEST.json"))
raw = json.loads(show(f"{base}/author/RAW-ARTIFACTS.json"))


def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "sha256" and isinstance(v, str):
                yield v
            else:
                yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


raw_hashes = set(walk(raw))
orig = {m["original_sha256"]: m["file"] for m in man}
masked = {m["file"] for m in man if m["original_sha256"] != m["published_sha256"]}
bad = 0
for m in man:
    h = hashlib.sha256(show(f"{base}/{m['file']}")).hexdigest()
    if h != m["published_sha256"]:
        bad += 1
        print("PUBLISHED MISMATCH", m["file"])
print(f"archive {commit}: {len(man)} manifest entries, {len(man) - bad} re-hash to published_sha256, "
      f"{len(masked)} label-masked (original_sha256 differs)")
hashes = re.findall(r"`([0-9a-f]{64})`", open(page).read())
n_raw = n_orig = n_masked = 0
for h in hashes:
    if h in orig:
        n_orig += 1
        tag = "original_sha256 " + orig[h] + (" (label-masked)" if orig[h] in masked else "")
        n_masked += orig[h] in masked
    elif h in raw_hashes:
        n_raw += 1
        tag = "RAW-ARTIFACTS.json"
    else:
        tag = "UNRESOLVED"
    print(f"  {h[:16]}... {tag}")
unres = len(hashes) - n_orig - n_raw
print(f"page hashes {len(hashes)}: {n_orig} original_sha256 ({n_masked} of them label-masked), "
      f"{n_raw} RAW-ARTIFACTS.json, {unres} unresolved")
sys.exit(1 if bad or unres else 0)
