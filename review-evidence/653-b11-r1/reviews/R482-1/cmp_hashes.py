#!/usr/bin/env python3
"""Compare the page's capture table (name, bytes, sha256) and per-cycle 12-hex
prefixes with RAW-ARTIFACTS.json and the grader JSON in the public evidence."""
import json, re, sys
page, raw, grade = sys.argv[1:4]
txt = open(page, encoding="utf-8").read()
rows = re.findall(r"^\| `(b11-a535-[^`]+\.pcap)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$", txt, re.M)
rawd = {f["path"].rsplit("/", 1)[1]: f for f in json.load(open(raw))["files"]}
bad = 0
for name, size, sha in rows:
    r = rawd.get(name)
    ok = r is not None and r["sha256"] == sha and r["bytes"] == int(size.replace(",", ""))
    bad += not ok
    print(("OK  " if ok else "BAD ") + name)
cyc = re.findall(r"^\| (C0 \(control\)|A\d\d|R\d\d) \|.*\| `([0-9a-f]{12})` \|$", txt, re.M)
full = {n.split("-")[-1].split(".")[0]: s for n, _, s in rows}
for c, pre in cyc:
    k = "C0" if c.startswith("C0") else c
    ok = full.get(k, "").startswith(pre)
    bad += not ok
    print(("OK  " if ok else "BAD ") + "prefix " + k)
print("page capture rows", len(rows), "cycle rows", len(cyc), "mismatches", bad)
sys.exit(1 if bad or len(rows) != 23 or len(cyc) != 23 else 0)
