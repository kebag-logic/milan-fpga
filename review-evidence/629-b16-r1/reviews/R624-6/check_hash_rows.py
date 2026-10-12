#!/usr/bin/env python3
"""R624-6: every `| `path` (...) | bytes | `sha256` |` row in a text, checked against the packet.

usage: check_hash_rows.py <packet root> <evidence MANIFEST.json> <round dir name> <text file> [<first line>]
For each row naming a packet file: the bytes and SHA-256 must equal the file in the packet and the
manifest's original_sha256 for it; a raw file (not in the packet) is checked against RAW-ARTIFACTS.json."""
import hashlib, json, os, re, sys
pkt, man, rd, txt = sys.argv[1:5]
first = int(sys.argv[5]) if len(sys.argv) > 5 else 1
m = {e["file"][len(rd) + 1:]: e for e in json.load(open(man)) if e["file"].startswith(rd + "/")}
raw = json.dumps(json.load(open(os.path.join(pkt, "RAW-ARTIFACTS.json"))))
row = re.compile(r"^\| (?:`[^`]+`(?:, `[^`]+`)* \| )?`([^`]+)`[^|]*\| ([\d,]+|Withheld) \| `([0-9a-f]{64})` \|$")
ok = bad = rawn = 0
for n, line in enumerate(open(txt, encoding="utf-8"), 1):
    if n < first:
        continue
    x = row.match(line.strip())
    if not x:
        continue
    path, size, sha = x.groups()
    fp = os.path.join(pkt, path)
    if os.path.isfile(fp):
        b = open(fp, "rb").read()
        good = (size == f"{len(b):,}" and hashlib.sha256(b).hexdigest() == sha and m.get(path, {}).get("original_sha256") == sha)
        ok += good; bad += not good
        if not good:
            print("BAD", n, path, size, sha[:12], len(b), hashlib.sha256(b).hexdigest()[:12], m.get(path, {}).get("path_redacted"))
    else:
        rawn += 1
        if sha not in raw:
            bad += 1; print("RAW-NOT-LISTED", n, path, sha[:12])
print(json.dumps(dict(text=os.path.basename(txt), packet_rows_ok=ok, bad=bad, raw_rows=rawn)))
sys.exit(1 if bad else 0)
