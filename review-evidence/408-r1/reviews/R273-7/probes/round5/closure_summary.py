#!/usr/bin/env python3
"""R273-7: summarise closure_extend.py's jsonl. Part A: recorded-vs-GCC
(one file per invocation) mismatches, `outside` vs refused-by-allowlist
mismatches, closes, and each raw HOLE classified. Parts B/C: every raw HOLE
classified as (GCC refuses, reader reads names) / (reader refuses, GCC reads)
/ (both read names and differ). Optional second argument: a previous
round's jsonl; B/C cells are then compared cell by cell.
usage: closure_summary.py <this.jsonl> [<previous.jsonl>]"""
import collections, json, sys
rows = [json.loads(l) for l in open(sys.argv[1])]
def cls(r):
    if r["kind"] != "HOLE":
        return r["kind"]
    if r["gcc"] is None and r["reader"] is not None:
        return "HOLE: GCC refuses, reader reads names"
    if r["reader"] is None and r["gcc"] is not None:
        return "HOLE: reader refuses, GCC reads (fail-closed)"
    return "HOLE: BOTH READ NAMES AND DIFFER"
c = collections.Counter((r["part"], cls(r)) for r in rows)
for k in sorted(c):
    print(f"  {k[0]} {k[1]}: {c[k]}")
A = [r for r in rows if r["part"] == "A"]
print(f"Part A: {len(A)} gate cells; recorded-vs-GCC mismatches: "
      f"{sum(1 for r in A if not r['record_vs_gcc'])}; outside-vs-allowlist "
      f"mismatches: {sum(1 for r in A if r['outside'] != (r['pin'] == 'SUBSET_CHARACTER_PIN'))}")
for r in A:
    if r["kind"] == "HOLE":
        print(f"  A HOLE {r['label']!r}: reader={r['reader']} gcc={r['gcc']} recorded={r['recorded']}")
differ = [r for r in rows if cls(r) == "HOLE: BOTH READ NAMES AND DIFFER"]
print(f"cells where both read names and differ: {len(differ)}")
for r in differ:
    print("  ", r["part"], r["label"], r["reader"], r["gcc"])
if len(sys.argv) > 2:
    prev = {(r["part"], r["label"]): r for r in map(json.loads, open(sys.argv[2])) if r["part"] in "BC"}
    now = {(r["part"], r["label"]): r for r in rows if r["part"] in "BC"}
    keys = ("S", "pin", "reader", "gcc", "kind")
    changed = [k for k in now if k not in prev or any(now[k][x] != prev[k][x] for x in keys)]
    print(f"B/C vs previous: {len(now)} cells now, {len(prev)} before, {len(changed)} changed or new, "
          f"{len(set(prev) - set(now))} gone")
    for k in changed[:20]:
        print("   changed", k)
