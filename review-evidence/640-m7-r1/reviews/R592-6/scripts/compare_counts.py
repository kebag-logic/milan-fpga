#!/usr/bin/env python3
"""Compare the CI policy page's worker counts with rtl.yml and the O9 fixture.

Usage: python3 -I compare_counts.py <repo checkout>
Exit 0 when every documented figure agrees, 1 otherwise.
"""
import pathlib
import re
import sys

WORDS = {"four": 4, "five": 5, "six": 6, "seven": 7}

root = pathlib.Path(sys.argv[1])
rtl = (root / ".github/workflows/rtl.yml").read_text()
doc = (root / "docs/testing/CI_WORKFLOWS.md").read_text()
src = (root / "scripts/ci_events.py").read_text()

shards = [len(m.group(1).split(","))
          for m in re.finditer(r"^\s+shard: \[([0-9, ]+)\]", rtl, re.M)]
totals = [int(m.group(1)) for m in re.finditer(r"^\s+total: \[(\d+)\]", rtl, re.M)]
expects = [int(m.group(1)) for m in re.finditer(r"--require-target-sha --expect (\d+)", rtl)]
print(f"rtl.yml shard-list lengths {shards}, totals {totals}, --expect {expects}")

m = re.search(r"worker matrix size, (\w+) for Verilator and (\w+) for Yosys", doc)
doc_counts = [WORDS.get(m.group(1)), WORDS.get(m.group(2))] if m else None
print(f"CI_WORKFLOWS.md verifier sentence -> {doc_counts}")
lit = re.findall(r"`--expect \d+`", doc)
print(f"CI_WORKFLOWS.md literal --expect values: {lit or 'none'}")

fx = re.search(r"def _m_shard_denominator_stale.*?(?=\ndef )", src, re.S).group(0)
base = re.search(r'assert shard == \[([0-9, ]+)\]', fx).group(1)
restated = re.search(r'_restate_shards\(w, "verilator-shards", "(\d+)"\)', fx).group(1)
appended = re.search(r"shard\.append\((\d+)\)", fx).group(1)
grown = len(base.split(",")) + 1
print(f"fixture: base {len(base.split(','))} shards, grows to {grown}, "
      f"stale total {restated}, new shard index {appended}")
ex = re.search(r"With a matrix of (\w+) and a stale total of (\w+), the check "
               r"fails before\s+shard (\d+)/(\d+)'s", doc)
print(f"CI_WORKFLOWS.md example: {ex.groups() if ex else None}")

ok = (shards == totals == expects
      and doc_counts == expects
      and not lit
      and ex is not None
      and WORDS.get(ex.group(1)) == grown
      and WORDS.get(ex.group(2)) == int(restated)
      and int(ex.group(3)) == int(appended)
      and int(ex.group(4)) == grown)
print("AGREE" if ok else "DISAGREE")
sys.exit(0 if ok else 1)
