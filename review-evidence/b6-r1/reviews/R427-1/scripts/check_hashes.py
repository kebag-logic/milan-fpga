#!/usr/bin/env python3
"""Check every hash row on the findings page against the published evidence.

usage: check_hashes.py <page.md> <evidence-root review-evidence/b6-r1>
Evidence rows: page sha256 must equal MANIFEST.json original_sha256 for author/<path>;
unmasked files must also hash to it and have the page's byte count.
Raw rows: page (path, bytes, sha256) must equal a RAW-ARTIFACTS.json entry.
Also re-hashes every published file against MANIFEST.json published_sha256.
"""
import hashlib, json, os, re, sys

page, root = sys.argv[1], sys.argv[2]
man = {e["file"]: e for e in json.load(open(os.path.join(root, "MANIFEST.json")))}
raw = json.load(open(os.path.join(root, "author/RAW-ARTIFACTS.json")))["files"]
rawmap = {f["path"]: f for f in raw}
fail = 0
pub_bad = 0
for f, e in man.items():
    p = os.path.join(root, f)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        pub_bad += 1; print("PUBLISHED-MISMATCH", f)
print(f"published files re-hashed: {len(man)}, mismatches: {pub_bad}")
masked = [f for f, e in man.items() if e["original_sha256"] != e["published_sha256"]]
print(f"masked files: {len(masked)}")
for f in masked: print("  masked", f)
rows = re.findall(r"^\| (.+?) \| ([\d,]+) \| `([0-9a-f]{64})` \|$", open(page).read(), re.M)
print(f"page hash rows: {len(rows)}")
raw_prefix = ("a0/", "a1/", "a2/", "bint/", "bcrf/")
for label, nbytes, sha in rows:
    nb = int(nbytes.replace(",", ""))
    m = re.match(r"`([^`]+)`", label)
    path = m.group(1) if m else None
    if path and path.startswith(raw_prefix):
        r = rawmap.get(path)
        ok = r is not None and r["sha256"] == sha and r["bytes"] == nb
        print(("OK  " if ok else "FAIL"), "raw", path, nb, sha[:12], "" if ok else r)
    elif path is None:  # tone loop
        hits = [r for r in raw if r["sha256"] == sha and r["bytes"] == nb]
        ok = bool(hits)
        print(("OK  " if ok else "FAIL"), "raw(label)", label[:30], nb, sha[:12], f"{len(hits)} entries")
    else:
        e = man.get("author/" + path)
        ok = e is not None and e["original_sha256"] == sha
        note = ""
        if ok and e["original_sha256"] == e["published_sha256"]:
            sz = os.path.getsize(os.path.join(root, "author/" + path))
            if sz != nb: ok = False; note = f"size {sz}"
            else: note = "unmasked, bytes+hash equal"
        elif ok:
            note = "masked: original_sha256 equal, size of original not checkable"
        print(("OK  " if ok else "FAIL"), "evidence", path, nb, sha[:12], note)
    fail += not ok
print("RESULT", "PASS" if fail == 0 and pub_bad == 0 else f"FAIL {fail}")
sys.exit(1 if fail or pub_bad else 0)
