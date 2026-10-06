#!/usr/bin/env python3
"""Check that every soak sequence gap is bridged by the overlapping segment.

Usage: check_overlap.py <evidence author dir>

For each gap in overlap-recovery.json, decode the raw headers of the recovered
packets and require: the recovered run starts at the 'before' packet (same tap
time and header bytes), ends at the 'after' packet, and its sequence numbers
advance by exactly one modulo 256 with a strictly increasing tap time.
"""
import json
import sys

ev = sys.argv[1]
d = json.load(open(f"{ev}/overlap-recovery.json"))
fails = 0
print(f"INFO segment_gaps={d['segment_gaps']} recovered={d['recovered_gaps']} "
      f"unrecovered={d['unrecovered_gaps']} listed={len(d['gaps'])}")
for g in d["gaps"]:
    pk = g["recovered"]["packets"]
    seq = [bytes.fromhex(p["header"])[2] for p in pk]
    tap = [p["tap_ns"] for p in pk]
    ok = (pk[0]["header"] == g["before"]["header"] and pk[0]["tap_ns"] == g["before"]["tap_ns"]
          and pk[-1]["header"] == g["after"]["header"] and pk[-1]["tap_ns"] == g["after"]["tap_ns"]
          and all((b - a) % 256 == 1 for a, b in zip(seq, seq[1:]))
          and all(b > a for a, b in zip(tap, tap[1:]))
          and g["recovered"]["capture"] != g["before"]["capture"])
    print(f"CHECK {'PASS' if ok else 'FAIL'} {g['segment']} {g['role']} subtype {g['subtype']} "
          f"seq {seq[0]}..{seq[-1]} ({len(pk)} pkts) from {g['recovered']['capture']}")
    fails += not ok
ok = len(d["gaps"]) == 9 == d["recovered_gaps"] and d["unrecovered_gaps"] == 0
print(f"CHECK {'PASS' if ok else 'FAIL'} nine gaps listed and all recovered")
fails += not ok
print(f"RESULT fails={fails}")
sys.exit(1 if fails else 0)
