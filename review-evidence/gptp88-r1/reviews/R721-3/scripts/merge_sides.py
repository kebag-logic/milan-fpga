#!/usr/bin/env python3
"""Compare a side's change (base..side) with the same side re-expressed on the
merge (other..merge): lines added/removed by the side that the merge does not
carry are printed. Usage: merge_sides.py REPO BASE SIDE OTHER MERGE FILE..."""
import subprocess, sys, collections
repo, base, side, other, merge, *files = sys.argv[1:]
def delta(a, b, f):
    out = subprocess.run(["git", "-C", repo, "diff", "-U0", a, b, "--", f],
                         capture_output=True, text=True, check=True).stdout
    add, rem = collections.Counter(), collections.Counter()
    for l in out.splitlines():
        if l.startswith("+++") or l.startswith("---"): continue
        if l.startswith("+"): add[l[1:].strip()] += 1
        elif l.startswith("-"): rem[l[1:].strip()] += 1
    return add, rem
for f in files:
    sa, sr = delta(base, side, f)
    ma, mr = delta(other, merge, f)
    miss_a = sa - ma; miss_r = sr - mr
    extra_a = ma - sa; extra_r = mr - sr
    print(f"== {f}: side +{sum(sa.values())}/-{sum(sr.values())}  on-merge +{sum(ma.values())}/-{sum(mr.values())}")
    for k, v in miss_a.items(): print("  side-added not carried:", v, repr(k[:150]))
    for k, v in miss_r.items(): print("  side-removed not carried:", v, repr(k[:150]))
    for k, v in extra_a.items(): print("  merge-added beyond side:", v, repr(k[:150]))
    for k, v in extra_r.items(): print("  merge-removed beyond side:", v, repr(k[:150]))
