#!/usr/bin/env python3
"""Check every SHA-256 the lane B7 section of the findings page cites against the packet.

usage: check_page_hashes.py <findings page> <path to review-evidence/629-b7-r1/author>
Raw files: against each run's events.jsonl raw-file records (size and SHA-256).
Evidence files and tools: against the retained file, or for a masked file against
redaction.json's original_sha256. Prints one line per row and a summary; rc 1 on a mismatch.
"""
import hashlib, json, os, re, sys
page, root = sys.argv[1], sys.argv[2]
text = open(page).read()
sec = text[text.index("### B7: artifact hashes"):]
rows = re.findall(r"^\| `?([^|`]+?)`?(?: \([^|]*\))? \| ([\d,]+) \| `([0-9a-f]{64})` \|$", sec, re.M)
raw = {}
for case in os.listdir(f"{root}/runs"):
    p = f"{root}/runs/{case}/events.jsonl"
    if os.path.exists(p):
        for l in open(p):
            d = json.loads(l)
            if d.get("kind") == "raw-file":
                raw[f"{case}/{d['file']}"] = (d["bytes"], d["sha256"])
red = json.load(open(f"{root}/redaction.json"))["files"]
bad = 0
for name, size, sha in rows:
    size = int(size.replace(",", ""))
    name = name.strip()
    if name.startswith("Tone loop"):
        got = ("tone", [v for k, v in raw.items() if k.endswith("serve/tone.raw")])
        ok = all(v == (size, sha) for v in got[1]) and got[1]
    elif name in raw:
        ok = raw[name] == (size, sha)
    elif os.path.exists(f"{root}/{name}"):
        b = open(f"{root}/{name}", "rb").read()
        h = hashlib.sha256(b).hexdigest()
        ok = (h == sha and len(b) == size) or (name in red and red[name]["original_sha256"] == sha)
    else:
        ok = None
    print(("OK  " if ok else "MISS" if ok is None else "BAD ") + f" {name} {size} {sha[:12]}")
    bad += ok is not True
print(f"rows {len(rows)} problems {bad}")
sys.exit(1 if bad else 0)
