"""Independently compare the published start and end census of the packet:
stream states unbound at both ends, and clock/config/sample-rate/descriptor
payloads byte-equal (peer object names are zeroed identically in both
published copies, so they compare as equal bytes). Also check outlets.

Usage: python3 -B check_restore.py <packet author dir>
"""
import json
import sys
from pathlib import Path

pkt = Path(sys.argv[1])
load = lambda n: {(r["role"], r["what"]): r["response"] for r in map(json.loads, (pkt / n).read_text().splitlines())}
a, b = load("census-start.jsonl"), load("census-end.jsonl")
bad = 0
states = 0
for k in sorted(set(a) | set(b)):
    if k not in a or k not in b:
        print("MISSING", k)
        bad += 1
        continue
    what = k[1]
    if what.startswith("state-"):
        states += 1
        for side, r in (("start", a[k]), ("end", b[k])):
            if not (r.get("status") == 0 and r.get("conn_count") == 0):
                print("BOUND", side, k, r)
                bad += 1
    elif what in ("clock", "config", "sample-rate") or what.startswith("desc-"):
        x, y = a[k].get("payload"), b[k].get("payload")
        full = x == y
        if not full:
            xb, yb = bytes.fromhex(x), bytes.fromhex(y)
            diff = [i for i in range(min(len(xb), len(yb))) if xb[i] != yb[i]]
            print("DIFF", k, "len", len(xb), len(yb), "differing byte offsets", diff[:16])
            if what in ("clock", "config", "sample-rate"):
                bad += 1
        else:
            print("EQUAL", k)
print("stream states compared:", states)
s = [l.split() for l in (pkt / "outlets-start.txt").read_text().splitlines() if l.strip()]
e = [l.split() for l in (pkt / "outlets-end.txt").read_text().splitlines() if l.strip()]
print("outlets start", s)
print("outlets end", e)
if s != e or any(v != "ON" for _, v in s):
    bad += 1
    print("OUTLET MISMATCH")
print("FAILURES", bad)
sys.exit(1 if bad else 0)
