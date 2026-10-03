#!/usr/bin/env python3
"""R449-3: compare each campaign arm's measured failing-check count with the
count recorded for it in a README table row whose first cell is `arm` and
whose last cell starts with an integer.

usage: readme_counts.py <README.md> <campaign log> [<line-from> <line-to>]
The log lines read are "<arm>: rc=N failures=F named=K KILLED".
"""
import re
import sys

readme, log = sys.argv[1], sys.argv[2]
lo, hi = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1, 10**9)
rec = {}
for line in open(readme, encoding="utf-8"):
    # a first cell may group arms: `base`, `-suffix`, ... (each suffix appends to base)
    m = re.match(r"^\|\s*((?:`[a-z0-9-]+`(?:,\s*)?)+)\s*\|.*\|\s*(?:the same\s+)?(\d+)\b[^|]*\|\s*$", line)
    if m:
        names = re.findall(r"`([a-z0-9-]+)`", m.group(1))
        base = names[0].split("-")
        # a suffix may replace any number of the base's trailing words
        arms = [names[0]] + ["-".join(base[:k]) + s for s in names[1:] if s.startswith("-")
                             for k in range(1, len(base) + 1)] \
            + [s for s in names[1:] if not s.startswith("-")]
        for arm in arms:
            rec.setdefault(arm, []).append(int(m.group(2)))
meas = {}
for n, line in enumerate(open(log, encoding="utf-8"), 1):
    if lo <= n <= hi:
        m = re.match(r"^([a-z0-9-]+): rc=\d+ failures=(\d+) named=\d+ (\S+)", line)
        if m:
            meas[m.group(1)] = (int(m.group(2)), m.group(3))
bad = 0
for arm, (f, verdict) in meas.items():
    r = rec.get(arm)
    if r is None:
        print(f"NO RECORD {arm}: measured {f} ({verdict})"); bad += 1
    elif f not in r:
        print(f"MISMATCH  {arm}: measured {f}, README {r}"); bad += 1
    else:
        print(f"EQUAL     {arm}: {f}")
print(f"{len(meas)} arms read, {len(meas) - bad} equal to their README record, {bad} not")
sys.exit(1 if bad else 0)
