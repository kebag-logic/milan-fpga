#!/usr/bin/env python3
"""Independent restore check over the published census pair: every stream
state unbound (conn_count 0), both DUT audio maps empty, and a field-by-field
start/end comparison ignoring only per-exchange fields.
usage: check_restore_census.py <census-start.jsonl> <census-end.jsonl>"""
import json, sys
VOL = {"t", "seq", "rtt_ms", "sequence_id"}
def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in VOL}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o
def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]
a, b = load(sys.argv[1]), load(sys.argv[2])
print("entries", len(a), len(b))
ka = {(r.get("role"), r.get("what")): strip(r) for r in a}
kb = {(r.get("role"), r.get("what")): strip(r) for r in b}
print("keys equal", set(ka) == set(kb))
diff = [k for k in ka if ka[k] != kb.get(k)]
print("differing entries", diff)
for name, rows in (("start", a), ("end", b)):
    st = [r for r in rows if str(r.get("what", "")).startswith(("rx-state", "tx-state"))]
    bound = [(r["role"], r["what"]) for r in st if r["response"].get("conn_count") != 0]
    maps = {}
    for r in rows:
        if str(r.get("what", "")).startswith("map-"):
            p = bytes.fromhex(r["response"]["payload"])
            maps[r["what"]] = dict(number_of_maps=int.from_bytes(p[6:8], "big"),
                                   number_of_mappings=int.from_bytes(p[8:10], "big"))
    clk = [r["response"]["payload"] for r in rows if r.get("role") == "dut" and r.get("what") == "clock"]
    sr = [r["response"]["payload"] for r in rows if r.get("role") == "dut" and r.get("what") == "sample-rate"]
    print(name, "stream states", len(st), "bound", bound, "maps", maps,
          "dut clock_source_index", int(clk[0][-4:], 16), "dut rate", int(sr[0][-8:], 16))
