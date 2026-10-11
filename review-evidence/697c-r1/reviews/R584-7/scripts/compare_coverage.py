#!/usr/bin/env python3
"""usage: compare_coverage.py <base fw_coverage log> <head fw_coverage log>
Compares the per-file raw line and branch counts the two fw_coverage.py --check runs print, mapping each
pre-move core path to its tsn-c-stack path."""
import re, sys
MAP = {"sw/firmware/ctrl/adp/adp.c": "third_party/tsn-c-stack/src/adp.c",
       "sw/firmware/ctrl/acmp/acmp.c": "third_party/tsn-c-stack/src/acmp.c",
       "sw/firmware/ctrl/maap/maap.c": "third_party/tsn-c-stack/src/maap.c",
       "sw/firmware/ctrl/wire/wire.h": "third_party/tsn-c-stack/include/wire.h"}
row = re.compile(r"^(\S+\.[ch])\s+(\d+/\d+)\s+(\d+/\d+)\s+lines")
def table(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        m = row.match(line)
        if m:
            out[MAP.get(m[1], m[1])] = (m[2], m[3])
    return out
b, h = table(sys.argv[1]), table(sys.argv[2])
print(f"files: base {len(b)} head {len(h)}; only base {sorted(b.keys() - h.keys())}; only head {sorted(h.keys() - b.keys())}")
diff = [(k, b[k], h[k]) for k in sorted(b.keys() & h.keys()) if b[k] != h[k]]
print(f"files whose raw (lines, branches) differ: {len(diff)}")
for d in diff: print("  ", d)
tot = lambda t, i: tuple(sum(int(v[i].split('/')[j]) for v in t.values()) for j in (0, 1))
print(f"totals base lines {tot(b,0)} branches {tot(b,1)}; head lines {tot(h,0)} branches {tot(h,1)}")
