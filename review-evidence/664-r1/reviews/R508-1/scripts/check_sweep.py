#!/usr/bin/env python3
"""Reproduce the four documented searches and compare both published hit ledgers."""
from pathlib import Path
import re
import subprocess
import sys

root, handoff_path = map(Path, sys.argv[1:3])
handoff = handoff_path.read_text()
patterns = {
    "Q1": r"NFR-SCOUT-0[123]",
    "Q2": r"never on firmware|fabric-only|fabric.only|no firmware round trip|never becomes a packet|all per-frame protocol",
    "Q3": r"(?i)(ADP|ACMP|AECP|MAAP|SRP|protocol control).{0,70}(fabric|processor)|(fabric|processor).{0,70}(ADP|ACMP|AECP|MAAP|SRP|protocol control)",
    "Q4": r"NFR-LAT-02|NFR-SCUP-0[24]|NFR-REL-02|FR-CTRL-04",
}
for label, revision in [("Base", "423ac5d910d09ab189b3acc39ae3ae1d10d50b19"), ("Candidate", "a27808375427859dc357f6bfd0a88842062b20ed")]:
    files = subprocess.check_output(["git", "-C", str(root), "ls-tree", "-r", "--name-only", revision], text=True).splitlines()
    found = set()
    for filename in files:
        if not filename.endswith(".md"):
            continue
        text = subprocess.check_output(["git", "-C", str(root), "show", f"{revision}:{filename}"]).decode("utf-8")
        for number, line in enumerate(text.split("\n"), 1):
            for query, pattern in patterns.items():
                if re.search(pattern, line):
                    found.add((query, f"{filename}:{number}"))
    section = handoff.split(f"### {label} hit ledger\n", 1)[1].split("\n##", 1)[0]
    listed = {(q, loc): disposition for q, loc, disposition in re.findall(r"\| (Q[1-4]) \| `([^`]+)` \| ([A-Z]) \|", section)}
    print(label, revision, "reproduced", len(found), "published", len(listed))
    for record in sorted(found - set(listed)):
        print("UNLISTED", *record)
    for record in sorted(set(listed) - found):
        print("UNREPRODUCED", *record)
    assert found == set(listed), f"{label} ledger mismatch"
    for query in patterns:
        print(query, sum(q == query for q, _ in found))
    print("PASS exact hit-locator coverage; semantic dispositions require independent review")
