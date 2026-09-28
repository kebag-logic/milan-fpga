#!/usr/bin/env python3
"""Compare probe and full XDC as constraint content: every non-set_clock_groups line in order,
and the set_clock_groups lines as a multiset of unordered group pairs (LiteX emits the
pairwise asynchronous groups in a run-dependent order under some interpreters).
Usage: xdc_relation_compare.py <a.xdc> <b.xdc> [label]"""
import collections, re, sys
def split(p):
    other, groups = [], collections.Counter()
    for line in open(p).read().splitlines():
        if line.startswith("set_clock_groups "):
            g = re.findall(r"-group (\[[^\]]*\]\])", line)
            assert len(g) == 2 and line.endswith("-asynchronous"), line
            groups[frozenset(g)] += 1
        elif line.strip():
            other.append(line)
    return other, groups
a, b = split(sys.argv[1]), split(sys.argv[2])
label = sys.argv[3] if len(sys.argv) > 3 else ""
print(f"{label} non-group lines {'IDENTICAL' if a[0] == b[0] else 'DIFFER'} ({len(a[0])}); "
      f"async group pairs {'IDENTICAL' if a[1] == b[1] else 'DIFFER'} ({sum(a[1].values())} pairs)")
