#!/usr/bin/env python3
"""Check every SHA-256 / byte row of the lane B15 section against the
published packet.

usage: check_doc_hashes.py <findings.md> <packet-root review-evidence/629-tone-r1>
Exit 0 only if every evidence row equals the file bytes, its MANIFEST.json
published_sha256 and original_sha256, and every raw row equals
RAW-ARTIFACTS.json.
"""
import hashlib, json, os, re, sys

doc, root = sys.argv[1], sys.argv[2]
text = open(doc, encoding="utf-8").read()
sec = text[text.index("## Dev 5603c353, 2026-10-10: lane B15"):]
man = {e["file"]: e for e in json.load(open(os.path.join(root, "MANIFEST.json")))}
raw = {f["path"]: f for f in json.load(open(os.path.join(root, "author/RAW-ARTIFACTS.json")))["files"]}
bad = 0

ev = sec[sec.index("| Evidence file | Bytes | SHA-256 |"):]
for m in re.finditer(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", ev, re.M):
    rel, nbytes, sha = m.group(1), int(m.group(2).replace(",", "")), m.group(3)
    path = os.path.join(root, "author", rel)
    data = open(path, "rb").read()
    got = hashlib.sha256(data).hexdigest()
    e = man["author/" + rel]
    ok = (got == sha and len(data) == nbytes and e["published_sha256"] == sha
          and e["original_sha256"] == sha)
    bad += not ok
    print(("OK  " if ok else "BAD ") + f"evidence {rel} bytes={len(data)}/{nbytes} "
          f"file={got == sha} pub={e['published_sha256'] == sha} orig={e['original_sha256'] == sha}")

rw = sec[sec.index("| Run | Raw file | Bytes | SHA-256 |"):sec.index("**Where the packet is.**")]
for m in re.finditer(r"^\| `?(\w+| ?Tap probe)`? \| `([^`]+)`[^|]*\| ([^|]+) \| `([0-9a-f]{64})` \|$", rw, re.M):
    run, name, nb, sha = m.group(1).strip(), m.group(2), m.group(3).strip(), m.group(4)
    key = name if run == "Tap probe" else f"{run}/{name}"
    r = raw.get(key)
    ok = r is not None and r["sha256"] == sha and (
        (nb == "Withheld" and isinstance(r["bytes"], str)) or
        (nb != "Withheld" and r["bytes"] == int(nb.replace(",", ""))))
    bad += not ok
    print(("OK  " if ok else "BAD ") + f"raw {key} {nb} {sha[:8]}")

# Masked tool: as-run hash in redaction.json
red = json.load(open(os.path.join(root, "author/redaction.json")))
s = json.dumps(red)
asrun = re.search(r"as run `([0-9a-f]+)\.\.\.`", sec).group(1)
print(("OK  " if asrun in s else "BAD ") + f"redaction.json holds as-run prefix {asrun}")
bad += asrun not in s
print("BAD ROWS:", bad)
sys.exit(1 if bad else 0)
