#!/usr/bin/env python3
"""Check each B13 short bind: formats matched before bind, bind and unbind
succeeded, and the bind-command to unbind-command hold is at least 2 s.

Usage: check_binds.py <evidence author dir>
"""
import json
import sys

ev = sys.argv[1]
holds, bad = [], []
for n in range(1, 101):
    c = json.load(open(f"{ev}/start-{n:03d}.json"))
    f = c["formats"][-1]
    b, u = c["bind_unbind"][0], c["bind_unbind"][-1]
    hold_ms = (u["t_cmd"] - b["t_cmd"]) / 1000.0
    holds.append(hold_ms)
    if not (f["talker_format"] == f["listener_format"] and b["ev"] == "bind" and u["ev"] == "unbind"
            and b["status"] == "Success" and u["status"] == "Success" and hold_ms >= 2000.0
            and len(c["formats"]) == 1):
        bad.append((n, f["talker_format"], f["listener_format"], b["status"], u["status"], hold_ms))
print(f"INFO hold ms min {min(holds):.3f} max {max(holds):.3f}")
print(f"CHECK {'PASS' if not bad else 'FAIL'} 100 binds: format matched, bind/unbind Success, hold >= 2 s {bad[:3]}")
sys.exit(1 if bad else 0)
