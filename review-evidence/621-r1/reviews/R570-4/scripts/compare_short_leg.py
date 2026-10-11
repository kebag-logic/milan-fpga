#!/usr/bin/env python3
"""R570-4: compare the gmstep check transcript of the full clean leg (taken
from the milan_dp_gm_steps suite log, up to its first tally) with a
--no-small-steps run. Pass iff the short transcript equals the full one with
exactly one contiguous block removed, and every removed check is one the #621 phase grades ('621:' or its\ngrade_the_licence 'licence:' calls), 86 in all.

Usage: python3 -I compare_short_leg.py <suite log> <short leg log>
"""
import re, sys

PAT = re.compile(r"^\s*\[( ok |FAIL)\]\s+(.*?)(?:\s+got=(\S+) exp=(\S+))?\s*$")

def checks(path, stop=None):
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        if stop and stop in line:
            break
        m = PAT.match(line)
        if m:
            out.append((m.group(1), m.group(2).strip(), m.group(4)))
    return out

full = checks(sys.argv[1], stop="== gmstep: checks:")
short = checks(sys.argv[2])
names_full = [c[1] for c in full]; names_short = [c[1] for c in short]
i = 0
while i < len(short) and full[i][1:] == short[i][1:]:
    i += 1
j = 0
while j < len(short) - i and full[-1 - j][1:] == short[-1 - j][1:]:
    j += 1
removed = full[i:len(full) - j]
# The #621 phase (sim_gmstep.cpp check_small_grandmaster_steps) grades 2 x
# (selection 2 + 2 steps x (1 + 12 '621:' + 7 grade_the_licence)) + 2 restore
# = 86 checks, every one named '621:' or 'licence:'.
in_phase = all(n[1].startswith(("621:", "licence:")) for n in removed)
print(f"removed block all in the #621 phase = {in_phase}; size 86 = {len(removed) == 86}")
ok = (i + j == len(short) and in_phase and len(removed) == 86
      and all(c[0] == " ok " for c in full + short))
print(f"full={len(full)} short={len(short)} prefix={i} suffix={j} removed={len(removed)}")
print(f"removed all '621:' = {all(n[1].startswith('621:') for n in removed)}; "
      f"every check ok = {all(c[0] == ' ok ' for c in full + short)}")
print(f"distinct removed names: {sorted(set(n[1] for n in removed))}")
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
