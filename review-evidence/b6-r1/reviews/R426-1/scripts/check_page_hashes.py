#!/usr/bin/env python3
"""Check every SHA-256 and byte count cited by the B6 findings page against
the evidence packet: published bytes, MANIFEST.json original_sha256, and
RAW-ARTIFACTS.json. Usage: check_page_hashes.py <page.md> <evidence-root>"""
import hashlib, json, os, re, sys

page, root = sys.argv[1], sys.argv[2]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
byfile = {m["file"]: m for m in man}
raw = json.load(open(os.path.join(root, "author/RAW-ARTIFACTS.json")))

def walk(o, acc):
    if isinstance(o, dict):
        h = o.get("sha256") or o.get("hash")
        if isinstance(h, str):
            acc.append(o)
        for v in o.values():
            walk(v, acc)
    elif isinstance(o, list):
        for v in o:
            walk(v, acc)
    return acc
rawents = walk(raw, [])
rawhash = {}
for e in rawents:
    rawhash.setdefault(e.get("sha256") or e.get("hash"), []).append(e)

rows = re.findall(r"^\| (.+?) \| ([\d,]+) \| `([0-9a-f]{64})` \|$", open(page).read(), re.M)
bad = 0
for label, size, h in rows:
    size = int(size.replace(",", ""))
    m = re.match(r"`([^`]+)`", label)
    name = m.group(1) if m else label
    cand = "author/" + name
    if cand in byfile:
        ent = byfile[cand]
        p = os.path.join(root, cand)
        pub = hashlib.sha256(open(p, "rb").read()).hexdigest()
        ok = ent["original_sha256"] == h
        st = "OK-original" if ok else "MISMATCH"
        note = "masked" if ent["original_sha256"] != ent["published_sha256"] else "unmasked"
        sizenote = ""
        if ent["original_sha256"] == ent["published_sha256"]:
            sz = os.path.getsize(p)
            sizenote = "size-ok" if sz == size else f"SIZE-MISMATCH pub={sz}"
            if pub != h:
                st = "PUBLISHED-BYTES-MISMATCH"
        else:
            sizenote = "size-unverifiable(masked)"
        print(f"{st:24} {note:9} {sizenote:26} {name}")
        bad += st != "OK-original" or "MISMATCH" in sizenote
    elif h in rawhash:
        e = rawhash[h][0]
        sz = e.get("bytes", e.get("size"))
        sizenote = "size-ok" if sz == size else f"SIZE? raw={sz}"
        print(f"{'OK-raw':24} {'':9} {sizenote:26} {name}")
        bad += sz != size
    else:
        print(f"{'NOT-FOUND':24} {'':9} {'':26} {name} {h}")
        bad += 1
print(f"rows={len(rows)} bad={bad}")
sys.exit(1 if bad else 0)
