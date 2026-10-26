#!/usr/bin/env python3
"""R699-2's mutant N15 ported to the round-4 line it targets; the planner self-test must fail.

Usage: python3 -I port_n15.py <export root> <work dir>

N15 ("located_within never reported") replaced `if first < index:` before
`event["located_within"]`. Round 4 widened that test to `if first < last:`;
the port changes only the anchor, keeping the replacement `if False:`.
Prints KILLED when the self-test of the mutated copy exits non-zero.
"""
import pathlib
import subprocess
import sys

root, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
OLD = '    if first < last:\n        event["located_within"]'
NEW = '    if False:\n        event["located_within"]'
text = (root / "tb/tools/torture_campaign.py").read_text(encoding="utf-8")
assert text.count(OLD) == 1, "anchor"
work.mkdir(parents=True, exist_ok=True)
(work / "torture_campaign.py").write_text(text.replace(OLD, NEW), encoding="utf-8")
run = subprocess.run([sys.executable, "-B", str(work / "torture_campaign.py"), "--self-test"],
                     capture_output=True, text=True, timeout=600, check=False)
failing = sorted({line.split(" ")[1] for line in run.stderr.splitlines() if line.startswith("FAIL: ")})
print("KILLED" if run.returncode else "SURVIVED", "N15 ported: located_within never reported", failing)
