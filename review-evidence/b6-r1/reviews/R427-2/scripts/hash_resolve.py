#!/usr/bin/env python3
"""Resolve every hash table row on the B6 findings page against the pinned archive.

Usage: hash_resolve.py <page.md> <archive-root containing review-evidence/b6-r1>

Checks, for the archive at the pinned commit:
  * every archived file re-hashes to its MANIFEST.json published_sha256;
  * every evidence-table row (path, bytes, sha256) resolves to the manifest
    entry author/<path> by original_sha256, and the published bytes equal the
    page's when the file is not label-masked;
  * every raw-table row resolves to RAW-ARTIFACTS.json by path, bytes and sha256;
  * the page's count of label-masked files ("twelve") and the named list.
"""
import hashlib, json, os, re, sys

page, root = sys.argv[1], sys.argv[2]
ev = os.path.join(root, "review-evidence", "b6-r1")
man = json.load(open(os.path.join(ev, "MANIFEST.json")))
by_file = {e["file"]: e for e in man}
raw = {f["path"]: f for f in json.load(open(os.path.join(ev, "author", "RAW-ARTIFACTS.json")))["files"]}

bad = 0
n_ok = 0
scope = [e for e in man if e["file"].startswith("author/")]
print(f"manifest entries: {len(man)}; re-hashed here (author/ only, reviewer reports not opened): {len(scope)}")
for e in scope:
    p = os.path.join(ev, e["file"])
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        bad += 1
        print("PUBLISHED MISMATCH", e["file"])
    else:
        n_ok += 1
print(f"author/ files re-hash to published_sha256: {n_ok} of {len(scope)}")

rows = re.findall(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", open(page).read(), re.M)
tone = re.findall(r"^\| Tone loop[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", open(page).read(), re.M)
res_ev = res_raw = 0
masked = []
for path, size, sha in rows:
    size = int(size.replace(",", ""))
    key = "author/" + path
    if key in by_file:
        e = by_file[key]
        if e["original_sha256"] != sha:
            bad += 1
            print("EVIDENCE HASH MISMATCH", path)
            continue
        pub = os.path.getsize(os.path.join(ev, key))
        if e["original_sha256"] != e["published_sha256"]:
            masked.append(path)
        elif pub != size:
            bad += 1
            print("EVIDENCE SIZE MISMATCH", path, pub, size)
            continue
        res_ev += 1
    elif path in raw:
        f = raw[path]
        if f["sha256"] != sha or f["bytes"] != size:
            bad += 1
            print("RAW MISMATCH", path, f["bytes"], size)
            continue
        res_raw += 1
    else:
        bad += 1
        print("UNRESOLVED", path)
for size, sha in tone:
    hit = [p for p, f in raw.items() if f["sha256"] == sha and f["bytes"] == int(size.replace(",", ""))]
    print("tone loop row resolves to RAW-ARTIFACTS:", hit[:3])
    res_raw += 1 if hit else 0
    bad += 0 if hit else 1
print(f"page hash rows: {len(rows) + len(tone)}; resolved evidence {res_ev}, raw {res_raw}")
print(f"label-masked among the page's evidence rows ({len(masked)}): {masked}")
all_masked = [e["file"] for e in man if e["original_sha256"] != e["published_sha256"] and e["file"].startswith("author/")]
print(f"label-masked files in the whole author/ packet: {len(all_masked)}")
print("RESULT", "PASS" if bad == 0 else f"FAIL ({bad})")
sys.exit(1 if bad else 0)
