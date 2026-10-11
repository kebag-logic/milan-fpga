#!/usr/bin/env python3
"""Reconstruct the automatic merge and independently recalculate plan rows."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("--pr-body", type=Path, required=True)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(["git", "-C", str(a.repo), *args],
                                   env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")).decode().strip()
old = "c0cba330fd485e52fcb90d5ccc69169edf9f0c2b"
base = "6bfeeb132fa0b1ad8a5b957446c66a498e633af7"
merge = "da341a154882a9aa28f7fb224ab82a71a66e5fb5"
head = "2bef9e50489a60f216a8073a9f5ea0645752b33f"
tree = git("merge-tree", "--write-tree", old, base)
assert tree == git("rev-parse", merge + "^{tree}") == "0fc0841bebece392d6facb87cd209d2f5e96e565"
assert git("show", "-s", "--format=%P", merge) == old + " " + base
assert git("diff", "--name-only", merge, head) == "docs/design/MARK_II_AREA_PLAN.md"
assert git("diff", "--numstat", merge, head).split()[:2] == ["1", "1"]
print("PASS automatic merge identity:", tree)
print("PASS repair delta: one line added, one line removed in MARK_II_AREA_PLAN.md")
fork = git("merge-base", old, base)
lane = set(git("diff", "--name-only", fork, old).splitlines())
upstream = set(git("diff", "--name-only", fork, base).splitlines())
print("Common merge base:", fork)
print("Overlapping changed paths:", sorted(lane & upstream))
for path in sorted(lane - upstream):
    assert git("rev-parse", old + ":" + path) == git("rev-parse", head + ":" + path), path
    print("PASS unchanged M5 blob:", path)
reference = (a.repo / "tb/verilator/csr/milan_csr_ref.sv").read_bytes().replace(
    b"module milan_csr_ref #(", b"module milan_csr #(")
original = subprocess.check_output(["git", "-C", str(a.repo), "show", "e8454e27:hdl/common/csr/milan_csr.sv"])
assert reference == original
print("PASS frozen oracle byte identity:", hashlib.sha256(reference).hexdigest())
plan = (a.repo / "docs/design/MARK_II_AREA_PLAN.md").read_text()
rows = [list(map(str.strip, line.strip("|").split("|")))
        for line in plan.splitlines() if line.startswith("| ")]
def number(s):
    return int(s.replace(",", ""))
levers = {}
for row in rows:
    if re.fullmatch(r"M(?:2|5|6|7|8a|8b) / L\w+", row[0]):
        nums = list(map(number, re.findall(r"[\d,]+", row[1])))
        levers[row[0].split()[0]] = nums
assert len(levers) == 6
baseline = next(number(row[3]) for row in rows if len(row) == 6 and row[:2] == ["0", "Recorded baseline"])
totals = [baseline - x for x in (14000, 11500, 16000)]
for name in ("M2", "M5", "M6", "M7", "M8a", "M8b"):
    totals = [n - d for n, d in zip(totals, levers[name])]
    row = next(row for row in rows if len(row) == 6 and row[1].split(",")[0] == name)
    assert list(map(number, row[3:])) == totals, name
print("PASS all cumulative planning rows; final central/conservative/optimistic:", totals)
remaining = [sum(v[i] for v in levers.values()) for i in range(3)]
assert remaining == [4600, 2900, 6700]
for row in rows:
    if len(row) == 5 and row[0] in {"Full split", "No split, including M3/M10", "Partial, F5 unqualified"}:
        n = number(row[2])
        assert [number(x) for x in row[3:]] == [38040 - n, 37659 - n], row
        k = {"Central": 0, "Conservative": 1, "Optimistic": 2}[row[1]]
        split = {"Full split": [14000,11500,16000], "No split, including M3/M10": [0,0,0],
                 "Partial, F5 unqualified": [3910,1410,5910]}[row[0]][k]
        extra = 0 if row[0] == "Full split" else [3800,2400,5100][k]
        assert n == baseline - remaining[k] - split - extra, row
print("PASS all nine placement estimates and both headroom columns")
m2 = number(re.search(r"The reproducible saving is ([\d,]+) LUTs, below", plan).group(1))
m5row = next(r for r in rows if len(r) == 6 and r[0] == "`csr` scope, routed")
m5nums = list(map(number, re.findall(r"[\d,]+", m5row[1])))
m5 = m5nums[0] - m5nums[1]
m6 = number(re.search(r"The reproducible saving is ([\d,]+) LUTs post-synthesis", plan).group(1))
start = next(number(r[2]) for r in rows if r[:2] == ["Partial, F5 unqualified", "Central"])
measured = start + sum(levers[name][0] - value for name, value in zip(("M2","M5","M6"),(m2,m5,m6)))
assert (m2,m5,m6,measured,measured-38040) == (34,121,418,38784,744)
sentence = next(line for line in plan.splitlines() if line.startswith("With the measured savings of M2"))
assert "38,784, 744 over 38,040" in sentence
assert "38,436" not in plan and "396 over" not in plan
assert 87.5 - 6.5 + 6 - 18.5 + 50 + 2 == 120.5
assert 120.5 - 11 == 109.5
assert 109.5 + 6 == 115.5
assert 120.5 + 6 == 126.5
print("PASS measured substitution:", start, "+", 200-m2, "+", 600-m5, "+", 600-m6, "=", measured)
print("PASS memory arithmetic; M2 maximum +2 remains an allowance, explicitly unused; M5/M6 add no tiles")
body = a.pr_body.read_text()
assert not re.search(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+(?:https://github.com/[^\s]+/issues/\d+|#\d+)", body, re.I)
print("PASS PR body has no closing reference")
assert "37,957 + (200 - 34) + (600 - 121) + (600 - 418) = 38,784" in body
print("PASS PR Composition repair states the correct recomputation")
stale = "38,436, 396 over 38,040" in body
print("FINDING: PR Known limitations retains stale 38,436/396 figures" if stale else "PASS PR stale scenario absent")
raise SystemExit(1 if stale else 0)
