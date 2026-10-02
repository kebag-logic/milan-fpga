#!/usr/bin/env python3
"""Compare each campaign's per-arm failing-check counts with tb/pp_top/README.md.

Reads this review's head results (receipt layout under <receipts>) and the
README of the reviewed clone; prints one line per mismatch and a summary per
campaign (notify, D3, dispatch, ACMP). Arms recorded in other suites' READMEs
(D3's tb/acmp_nvm and tb/rx_validator arms) are listed as having no row here.

usage: readme_counts.py <clone> <receipts>
"""
import glob
import json
import re
import sys

clone, rec = sys.argv[1], sys.argv[2]
lines = open(f"{clone}/tb/pp_top/README.md").read().splitlines()


def table_after(pred):
    i = next(k for k, l in enumerate(lines) if pred(l))
    k = i
    while not lines[k].startswith("|"):
        k += 1
    rows = {}
    while k < len(lines) and lines[k].startswith("|"):
        cells = [c.strip() for c in lines[k].strip("|").split("|")]
        m = re.match(r"`?([A-Za-z0-9_\-]+)`?", cells[0])
        if m:
            rows[m.group(1)] = cells
        k += 1
    return rows


def lead(cell):
    m = re.match(r"(\d+)", cell)
    return int(m.group(1)) if m else None


def report(name, results, rows):
    mm = 0
    for arm, n in sorted(results.items()):
        c = rows.get(arm)
        if c is None or lead(c[-1]) != n:
            mm += 1
            print(f"{name} {arm}: README {c[-1] if c else 'no row'} head {n}")
    print(f"{name}: {len(results)} head arms, {len(rows)} README rows, {mm} without an equal row")


notify = {r["mutant"]: len(r["failing_checks"]) for f in glob.glob(f"{rec}/notify/*.results.json")
          for r in json.load(open(f)) if not r["mutant"].startswith("golden")}
report("notify", notify, table_after(lambda l: l.startswith("### Mutation record: `notify_mutants.py`")))

d3 = {r["mutant"]: len(r["failing_checks"]) for f in glob.glob(f"{rec}/d3/slice_*.json")
      for r in json.load(open(f))}
report("d3", d3, table_after(lambda l: "At the lane head all 83 are KILLED" in l))

disp = {}
for f in glob.glob(f"{rec}/dispatch/chunk_*.stdout"):
    for l in open(f):
        m = re.match(r"(\S+): rc=\d+ failures=(\d+) named=\d+ (KILLED|UNPROVEN)", l)
        if m:
            disp[m.group(1)] = int(m.group(2))
report("dispatch", disp, table_after(
    lambda l: "The last column is how many checks each arm failed at the lane head" in l))

acmp = {r["mutant"].split("@")[0]: len(r["failing_checks"]) for r in json.load(open(f"{rec}/acmp/results.json"))
        if r["mutant"].endswith("@pp_top")}
i = next(k for k, l in enumerate(lines) if "all 19 KILLED" in l and "Measured" in l)
rows = {}
for l in lines[i:i + 40]:
    m = re.match(r"\| `([a-z0-9_]+)` \|.*\| (\d+)[^|]*\|\s*$", l)
    if m:
        rows[m.group(1)] = [m.group(2)]
report("acmp(pp_top)", acmp, rows)
