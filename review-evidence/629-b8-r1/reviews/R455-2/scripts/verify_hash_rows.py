#!/usr/bin/env python3
"""Check every B8 hash row on the page against the published packet.

usage: verify_hash_rows.py PAGE PACKET_DIR
PACKET_DIR is review-evidence/629-b8-r1 extracted at the pinned commit.
Prints one line per row and a summary; exit 1 on any mismatch.
"""
import hashlib, json, os, re, sys

page, pk = sys.argv[1], sys.argv[2]
text = open(page, encoding="utf-8").read()
sec = text[text.index("### B8: artifact hashes"):]
man = {e["file"]: e for e in json.load(open(os.path.join(pk, "MANIFEST.json")))}
raw = json.load(open(os.path.join(pk, "author/RAW-ARTIFACTS.json")))
red = json.load(open(os.path.join(pk, "author/redaction.json")))["files"]
rawtxt = json.dumps(raw)
bad = 0

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

rows = re.findall(r"^\| (.+?) \| ([0-9,]+) \| `([0-9a-f]{64})` \|$", sec, re.M)
nraw = nev = 0
for r in rows:
    if r[0].count("|"):  # raw row: Run | file | bytes | sha
        nraw += 1
        size, h = int(r[1].replace(",", "")), r[2]
        ok = h in rawtxt and str(size) in rawtxt
        # find exact record for size/hash pairing
        pair = False
        def walk(o):
            global pair
            if isinstance(o, dict):
                vals = list(o.values())
                if h in vals and size in vals:
                    pair = True
                for v in vals: walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(raw)
        print(("OK  " if pair else "BAD ") + "raw " + r[0].split("|")[1].strip() + " " + r[0].split("|")[0].strip())
        bad += not pair
        continue
    nev += 1
    name = re.match(r"`([^`]+)`", r[0]).group(1)
    size, h = int(r[1].replace(",", "")), r[2]
    rel = "author/" + name
    p = os.path.join(pk, rel)
    st = []
    if not os.path.isfile(p):
        st.append("missing")
    else:
        if os.path.getsize(p) != size: st.append("size %d" % os.path.getsize(p))
        if sha(p) != h: st.append("sha")
    e = man.get(rel)
    if not e: st.append("no-manifest")
    elif e["published_sha256"] != h: st.append("manifest-published")
    m = re.search(r"as run `([0-9a-f]{8})\.\.\.`", r[0])
    if m and e:
        # as-run hash: the page says MANIFEST.json's original for grade_b8.py,
        # redaction.json's original for the tools the lane packet masked
        rr = red.get(name, {})
        src = [x for x in (e["original_sha256"], rr.get("original_sha256", "")) if x.startswith(m.group(1))]
        if not src:
            st.append("as-run %s in neither MANIFEST nor redaction.json" % m.group(1))
    if "identity-verdict" in name:
        for d in ("identity-resume", "identity-postboot"):
            q = os.path.join(pk, "author", d, "identity-verdict.txt")
            if not os.path.isfile(q) or sha(q) != h: st.append(d + " differs")
    print(("BAD " if st else "OK  ") + rel + (" " + ",".join(st) if st else ""))
    bad += bool(st)
print("raw rows %d, evidence rows %d, failures %d" % (nraw, nev, bad))
sys.exit(1 if bad else 0)
