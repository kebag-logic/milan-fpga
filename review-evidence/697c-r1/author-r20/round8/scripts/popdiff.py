"""Scratch (round 8): the judged facts of two captures (popcmp.py's output) compared: what the first holds that the
second does not, and the other way, grouped by kind.

usage: popdiff.py <first.json> <second.json>
"""
import collections
import json
import sys

a, b = (json.load(open(p)) for p in sys.argv[1:3])
for what in ("facts", "edges"):
    sa, sb = {tuple(x) for x in a[what]}, {tuple(x) for x in b[what]}
    print(f"{what}: first {len(sa)}, second {len(sb)}, shared {len(sa & sb)}")
    for label, only in (("only in the first", sa - sb), ("only in the second", sb - sa)):
        kinds = collections.Counter((x[0] if what == "edges" else "source", x[-2]) for x in only)
        print(f"  {label}: {len(only)} {dict(kinds)}")
        for x in sorted(only)[:60]:
            print("    ", x)
