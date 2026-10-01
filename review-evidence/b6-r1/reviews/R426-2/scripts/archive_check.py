#!/usr/bin/env python3
"""Re-hash the archived lane packet against its manifest and resolve every
SHA-256 the findings page prints.
Usage: archive_check.py <extracted review-evidence/b6-r1 dir> <page.md>"""
import hashlib, json, os, re, sys
root, page = sys.argv[1], sys.argv[2]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
bad = 0
for e in man:
    p = os.path.join(root, e["file"])
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        bad += 1; print("PUBLISHED MISMATCH", e["file"])
print(f"manifest entries {len(man)}, published re-hash mismatches {bad}")
listed = {e["file"] for e in man}
ondisk = set()
for d, _, fs in os.walk(root):
    for f in fs:
        ondisk.add(os.path.relpath(os.path.join(d, f), root))
print("files on disk not in manifest:", sorted(ondisk - listed - {"MANIFEST.json"}))
print("manifest files missing on disk:", sorted(listed - ondisk))
masked = [e for e in man if e["original_sha256"] != e["published_sha256"]]
print(f"entries whose original differs from published: {len(masked)}")
for e in masked:
    print("  differs:", e["file"], "path_redacted=", e.get("path_redacted"))
text = open(page).read()
rows = re.findall(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", text, re.M)
by_orig = {}
for e in man:
    by_orig.setdefault(e["original_sha256"], []).append(e["file"])
raw = json.load(open(os.path.join(root, "author", "RAW-ARTIFACTS.json")))
rawtext = json.dumps(raw)
resolved = unres = 0
for name, size, h in rows:
    cand = "author/" + name
    ent = next((e for e in man if e["file"] == cand), None)
    if ent:
        how = "original" if ent["original_sha256"] == h else "MISMATCH"
        pub = "published-equal" if ent["published_sha256"] == h else "published-differs"
        sz = os.path.getsize(os.path.join(root, cand))
        print(f"  page {name}: manifest {how}, {pub}, page bytes {size}, published bytes {sz}")
        if how == "original": resolved += 1
        else: unres += 1
    elif h in rawtext:
        print(f"  page {name}: found in RAW-ARTIFACTS.json"); resolved += 1
    else:
        print(f"  page {name}: UNRESOLVED"); unres += 1
tone = re.search(r"Tone loop \(`b6_tone.py`\) \| [\d,]+ \| `([0-9a-f]{64})`", text)
print("tone loop hash on page:", tone.group(1) if tone else None, "in RAW-ARTIFACTS:", bool(tone and tone.group(1) in rawtext))
print(f"page hash rows {len(rows)}: resolved {resolved}, unresolved {unres}")
sys.exit(1 if bad or unres else 0)
