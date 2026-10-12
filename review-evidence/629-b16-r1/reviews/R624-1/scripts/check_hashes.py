#!/usr/bin/env python3
"""Check every hash row of the lane B16/B16b/B16c sections against the published packet.

usage: check_hashes.py <findings.md> <packet-dir (629-b16-r1)>
Verifies: (1) every published file's sha256 equals MANIFEST.json published_sha256;
(2) every evidence-file row (path, bytes, sha) in the B16 sections equals the
packet's original or published hash and the published file's size when unmasked;
(3) every raw-file row equals RAW-ARTIFACTS.json.
"""
import hashlib, json, os, re, sys

doc, pk = sys.argv[1], sys.argv[2]
man = json.load(open(os.path.join(pk, "MANIFEST.json")))
bad = 0
pub = {}
for e in man:
    p = os.path.join(pk, e["file"])
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    ok = h == e["published_sha256"]
    bad += not ok
    pub[e["file"][len("author-r1/"):]] = (e, os.path.getsize(p), h)
print(f"manifest: {len(man)} files, published hash mismatches: {bad}")

lines = open(doc, encoding="utf-8").read().splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
sec = lines[start:]
raw = json.load(open(os.path.join(pk, "author-r1/RAW-ARTIFACTS.json")))["files"]
rawsha = {f["sha256"]: f for f in raw}
ev_re = re.compile(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$")
raw_re = re.compile(r"^\| ([^|]+) \| `([^`]+)`[^|]*\| ([^|]+) \| `([0-9a-f]{64})` \|$")
nev = nraw = fail = 0
for l in sec:
    m = ev_re.match(l)
    if m:
        nev += 1
        path, size, sha = m.group(1), int(m.group(2).replace(",", "")), m.group(3)
        e = pub.get(path)
        if not e:
            print("EV-MISSING", path); fail += 1; continue
        ent, psize, ph = e
        shaok = sha in (ent["original_sha256"], ent["published_sha256"])
        sizeok = psize == size if sha == ph else None
        st = "OK" if shaok and sizeok is not False else "FAIL"
        if st == "FAIL": fail += 1
        print(f"EV {st} {path} doc={size}/{sha[:12]} pub={psize}/{ph[:12]} orig={ent['original_sha256'][:12]} size_checked={sizeok}")
        continue
    m = raw_re.match(l)
    if m:
        nraw += 1
        run, f, size, sha = m.group(1).strip(), m.group(2), m.group(3).strip(), m.group(4)
        r = rawsha.get(sha)
        if not r:
            print("RAW-MISSING", run, f, sha[:12]); fail += 1; continue
        rb = r["bytes"]
        sz = size.replace(",", "")
        szok = (str(rb) == sz) or (isinstance(rb, str) and size == "Withheld") or (rb == 0 and sz == "0")
        if not szok or not r["path"].endswith(f.split(",")[0]):
            st = "FAIL"; fail += 1
        else:
            st = "OK"
        print(f"RAW {st} {run} {f} doc={size} raw={r['path']}:{rb}")
print(f"evidence rows {nev}, raw rows {nraw}, failures {fail}")
sys.exit(1 if fail or bad else 0)
