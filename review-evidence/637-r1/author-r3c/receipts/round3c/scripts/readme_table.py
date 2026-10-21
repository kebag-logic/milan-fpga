#!/usr/bin/env python3
"""Rewrite the milan_dp README campaign table's Failures column from one
campaign's verdict lines.

usage: readme_table.py <README.md> <campaign.log> [--write]

Each table row `| n | leg | mutant | checks | F of T |` is matched to the
campaign line `[PASS] mutant caught: <mutant> - breaks ... (its tallies
report F failure(s) across T checks)` by the mutant's text. Every row must
match exactly one caught line and every caught line one row. Without
--write it prints the rows that would change and writes nothing.
"""
import re
import sys

readme, log = sys.argv[1], sys.argv[2]
write = "--write" in sys.argv[3:]
caught = {}
for line in open(log, errors="replace"):
    m = re.match(r'\[PASS\] mutant caught: (.*?) - breaks .*\(its tallies report (\d+) '
                 r'failure\(s\) across (\d+) checks\)\s*$', line)
    if m:
        if m.group(1) in caught:
            raise SystemExit(f"two caught lines for {m.group(1)!r}")
        caught[m.group(1)] = (int(m.group(2)), int(m.group(3)))
lines = open(readme).read().split("\n")
row = re.compile(r'^\| (\d+) \| ([^|]+) \| (.+?) \| (.+) \| (\d+) of (\d+) \|$')
seen = set()
changed = 0
for i, line in enumerate(lines):
    m = row.match(line)
    if not m:
        continue
    name = m.group(3)
    if name not in caught:
        raise SystemExit(f"row {m.group(1)}: no caught line for {name!r}")
    seen.add(name)
    f, t = caught[name]
    new = line[:m.start(5)] + f"{f} of {t} |"
    if new != line:
        changed += 1
        print(f"row {m.group(1)}: {m.group(5)} of {m.group(6)} -> {f} of {t}")
    lines[i] = new
missing = set(caught) - seen
if missing:
    raise SystemExit(f"caught lines with no row: {sorted(missing)}")
print(f"{len(seen)} rows matched, {changed} changed")
if write:
    open(readme, "w").write("\n".join(lines))
