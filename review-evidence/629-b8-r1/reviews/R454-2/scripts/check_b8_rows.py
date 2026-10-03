#!/usr/bin/env python3
"""Check the B8 section's evidence and raw hash rows against the published
evidence tree (git archive of the pinned evidence commit).

usage: check_b8_rows.py PAGE EVIDENCE_ROOT [ROUND2_REDACTION_JSON]
  EVIDENCE_ROOT is the extracted review-evidence/629-b8-r1 directory.
Prints one line per row; exit 0 when every row matches.
"""
import hashlib, json, os, re, sys

page, root = sys.argv[1], sys.argv[2]
r2red = sys.argv[3] if len(sys.argv) > 3 else None
text = open(page, encoding="utf-8").read()
sec = text[text.index("### B8: artifact hashes"):]
author = os.path.join(root, "author")
manifest = {e["file"]: e for e in json.load(open(os.path.join(root, "MANIFEST.json")))}
raw = json.load(open(os.path.join(author, "RAW-ARTIFACTS.json")))
rawtxt = json.dumps(raw)
bad = 0
row = re.compile(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", re.M)
raw_part, ev_part = sec.split("| Evidence file |")
for m in re.finditer(r"^\| (Tone proof|SW|CRFLL|PC) \| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", raw_part, re.M):
    run, name, size, sha = m.group(1), m.group(2), int(m.group(3).replace(",", "")), m.group(4)
    ok = sha in rawtxt and str(size) in rawtxt
    bad += not ok
    print(f"RAW {'OK ' if ok else 'BAD'} {run} {name} size_in_RAW={str(size) in rawtxt} sha_in_RAW={sha in rawtxt}")
n_ev = 0
for m in row.finditer(ev_part):
    name, size, sha = m.group(1), int(m.group(2).replace(",", "")), m.group(3)
    n_ev += 1
    p = os.path.join(author, name)
    b = open(p, "rb").read()
    got = hashlib.sha256(b).hexdigest()
    me = manifest.get("author/" + name, {})
    ok = got == sha and len(b) == size and me.get("published_sha256") == sha
    bad += not ok
    extra = ""
    if me.get("original_sha256") != me.get("published_sha256"):
        extra = f" original={me.get('original_sha256','')[:8]}"
    print(f"EV  {'OK ' if ok else 'BAD'} {name} bytes={len(b)}/{size} sha={got==sha} manifest_published={me.get('published_sha256')==sha}{extra}")
# identity verdict triple
idv = [hashlib.sha256(open(os.path.join(author, d, "identity-verdict.txt"), "rb").read()).hexdigest()
       for d in ("identity", "identity-resume", "identity-postboot")]
print("IDENTITY triple equal:", len(set(idv)) == 1)
bad += len(set(idv)) != 1
# grade_b8 masking record
g = manifest["author/tools/grade_b8.py"]
print("MANIFEST grade_b8 original prefix", g["original_sha256"][:8], "published prefix", g["published_sha256"][:8])
red = json.load(open(os.path.join(author, "redaction.json")))
names = [f.get("file", f.get("path")) if isinstance(f, dict) else f for f in (red["files"] if isinstance(red["files"], list) else red["files"].keys())]
print("published redaction.json entries:", len(names), "has grade_b8:", any("grade_b8" in str(n) for n in names))
if r2red:
    red2 = json.load(open(r2red))
    files2 = red2["files"]
    items = files2.items() if isinstance(files2, dict) else [(f.get("file", f.get("path")), f) for f in files2]
    n2 = 0
    for k, v in items:
        n2 += 1
        if "grade_b8" in str(k):
            print("round-2 redaction.json grade_b8:", {kk: (vv[:8] if isinstance(vv, str) else vv) for kk, vv in v.items()} if isinstance(v, dict) else v)
    print("round-2 redaction.json entries:", n2)
print("evidence rows:", n_ev, "bad:", bad)
sys.exit(1 if bad else 0)
