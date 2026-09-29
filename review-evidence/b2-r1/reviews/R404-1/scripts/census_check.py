#!/usr/bin/env python3
"""Independent start/end census comparison ignoring transport-only fields
(seq, rtt_ms, t). Usage: census_check.py <restore dir>"""
import json, sys
from pathlib import Path
d = Path(sys.argv[1])
TRANSIENT = {"seq", "rtt_ms", "t"}
def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k not in TRANSIENT}
    return x
def load(f):
    out = {}
    for l in open(f):
        r = json.loads(l)
        out[(r.get("role"), r.get("what"))] = strip(r)
    return out
s, e = load(d / "census-start.jsonl"), load(d / "census-end.jsonl")
nc = [k for k in s if not str(k[1]).startswith("counter")]
diff = [k for k in nc if s[k] != e.get(k)]
print("keys", len(s), len(e), "same key set", set(s) == set(e))
print("non-counter reads", len(nc), "equal", len(nc) - len(diff), "differ", diff)
st = [k for k in e if str(k[1]).startswith("state-")]
print("stream states", len(st), "conn_count>0 at start", [k for k in st if s[k]["response"].get("conn_count")],
      "at end", [k for k in st if e[k]["response"].get("conn_count")])
for k in sorted(k for k in s if str(k[1]).startswith("counter")):
    a, b = s[k]["response"].get("counters"), e[k]["response"].get("counters")
    if a != b:
        print("counter moved", k, a, "->", b)
