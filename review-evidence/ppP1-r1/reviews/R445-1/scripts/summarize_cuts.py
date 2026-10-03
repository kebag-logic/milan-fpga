#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R445-1: summarize a tb/pp_top D3KR run log: its tally, its exit status,
and every FAIL line counted by (record type, check kind, what the device held
at the cut). Usage: summarize_cuts.py RUN_LOG [RUN_RC]"""
import collections
import re
import sys

log = open(sys.argv[1], errors="replace").read().splitlines()
rc = open(sys.argv[2]).read().strip() if len(sys.argv) > 2 else "?"
tally = [l for l in log if re.match(r"^(D3KR|D3V?|AD): \d+ checks", l)]
fails = [l for l in log if l.startswith("FAIL")]
print(f"rc {rc}; {'; '.join(tally) or 'no tally'}; {len(fails)} FAIL lines")
by = collections.Counter()
seeds = collections.defaultdict(set)
for l in fails:
    m = re.search(r"D3KR (\w+)(?: seed (0x[0-9A-F]+))?", l)
    typ = m.group(1) if m else "?"
    rest = re.search(r"\(([a-zA-Z ]+) at rest\)", l)
    if "persists" in l:
        kind = "later change persists"
    elif "PASSIVE" in l:
        kind = "binding probes PASSIVE"
    elif "premise" in l:
        kind = "premise"
    elif "calibration" in l:
        kind = "calibration"
    else:
        kind = "restore verdict"
    by[(typ, kind, rest.group(1) if rest else "-")] += 1
    if m and m.group(2):
        seeds[typ].add(m.group(2))
for (typ, kind, cls), n in sorted(by.items()):
    print(f"  {n:4d}  {typ:5s} {kind:24s} at rest: {cls}")
for typ, s in sorted(seeds.items()):
    print(f"  failing seeds {typ}: {len(s)}: {' '.join(sorted(s))}")
