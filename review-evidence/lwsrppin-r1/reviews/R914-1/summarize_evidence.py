#!/usr/bin/env python3
"""Recount public receipts and local reproduction logs without importing author scripts."""
from pathlib import Path
import hashlib
import json
import re
import sys

packet = Path(__file__).resolve().parent
public = packet / "scratch/review-evidence/lwsrppin-r1"
manifest = json.loads((public / "MANIFEST.json").read_text())
checked = 0
for item in manifest:
    if not item["file"].startswith("author/"):
        continue
    path = public / item["file"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item["published_sha256"], item["file"]
    checked += 1
print("public manifest entries verified:", checked)
receipts = public / "author/receipts"
for directory, pattern in [(receipts / "own-leaveall", "*.log"), (packet, "own-*.log")]:
    for path in sorted(directory.glob(pattern)):
        text = path.read_text()
        # Published combined logs announce each arm; local logs each contain one.
        blocks = re.split(r"(?=^=== ARM )", text, flags=re.M)
        for i, block in enumerate(blocks):
            rows = re.findall(r"OWN-LA input=(\d+) offset_ms=(\d+) leaveall_ms=(\d+) withdrawn_ms=(\d+) lv_ms=(none>)?(\d+) peer_left_ms=(\d+)", block)
            if not rows:
                continue
            unsent = sum(bool(row[4]) for row in rows)
            worst = max(int(row[5])-int(row[3]) for row in rows if not row[4])
            print(path.name, "block", i, "withdrawals", len(rows), "unsent", unsent, "worst_ms", worst)
            print("held:", re.findall(r"OWN-LA held .*", block))
for path in sorted((receipts / "harness").glob("results-*.json")):
    data = json.loads(path.read_text())
    groups = data["results"]
    shares = [g["passes"]["share"] for g in groups if g.get("passes")]
    print(path.name, "groups",len(groups), "work",sum(s["passes"] for s in shares),
          "over",sum(s["over"] for s in shares), "worst_cycles",max(g["passes"]["worst"]["cycles"] for g in groups if g.get("passes")))
for path in sorted((receipts / "twin").glob("dbba60e6-plants-*.log")):
    text = path.read_text()
    print(path.name)
    refusals = re.findall(r"^plant ([^:]+): REFUSED by (.*)$", text, re.M)
    names = sorted({name for name, _ in refusals})
    print("refusals", len(refusals), "distinct plants", len(names), names)
    assert len(refusals) == 32 and len(names) == 16
    assert all(sum(name == n for name, _ in refusals) == 2 for n in names)
firmware = (receipts / "firmware/gate-0.log").read_text()
print("firmware passing arms:", len(re.findall(r"^\[ok\] arm", firmware, re.M)))
print("firmware cases in passing verdicts:", sum(map(int, re.findall(r"verdict: PASS \((\d+) tests", firmware))))
