#!/usr/bin/env python3
"""Re-check lane B8's binding rule from the published run events.

For every bind in runs/{proof,sw,crfll}/events.jsonl (and the PC case's
ctl/events), require a preceding ok format-check naming the same talker and
listener, that any format set targets the listener (never the talker), that
every set-clock is on the DUT, answered SUCCESS and read back equal, and that
each run ends with clock-final == as_found and format-final equal_to_found.

usage: check_binding_rule.py <author-dir> <out.txt>
"""
import json
import sys
from pathlib import Path

root, out = Path(sys.argv[1]), Path(sys.argv[2])
lines, bad = [], 0
for run in ("proof", "sw", "crfll", "pc"):
    ev = [json.loads(x) for x in (root / "runs" / run / "events.jsonl").read_text().splitlines() if x.strip()]
    checks = []
    binds = sets = 0
    for i, e in enumerate(ev):
        k = e.get("kind")
        if k == "format-check":
            checks.append(e)
            if not e.get("ok"):
                lines.append(f"{run}: format-check not ok: {e}"); bad += 1
            s = e.get("set")
            if s and s.get("fmt") != e.get("talker_fmt"):
                lines.append(f"{run}: listener set to a format other than the talker's: {e}"); bad += 1
            if e.get("listener_after", e.get("talker_fmt")) != e.get("talker_fmt"):
                lines.append(f"{run}: listener_after != talker_fmt: {e}"); bad += 1
        elif k == "bind":
            binds += 1
            t, l = e.get("talker"), e.get("listener")
            prior = [c for c in checks if (t is None or c.get("talker") == t) and (l is None or c.get("listener") == l)]
            if not prior:
                lines.append(f"{run}: bind without a prior format-check: {e}"); bad += 1
            if e.get("status") != 0 or e.get("conn_count") != 1:
                lines.append(f"{run}: bind not SUCCESS/1: {e}"); bad += 1
        elif k == "unbind":
            if e.get("status") != 0 or e.get("conn_count") != 0:
                lines.append(f"{run}: unbind not SUCCESS/0: {e}"); bad += 1
        elif k == "set-clock":
            sets += 1
            # the PC case's tool (pc_b8.py) sets only the DUT and logs no "who" key
            if e.get("who", "dut") != "dut" or e.get("status") != "SUCCESS" or e.get("readback") != e.get("src"):
                lines.append(f"{run}: set-clock off-rule: {e}"); bad += 1
        elif k == "clock-final":
            if e.get("source") != e.get("as_found"):
                lines.append(f"{run}: clock-final != as_found: {e}"); bad += 1
        elif k == "format-final":
            if e.get("equal_to_found", e.get("equal")) is not True:
                lines.append(f"{run}: format-final not equal: {e}"); bad += 1
    kinds = sorted({e.get("kind") for e in ev})
    lines.append(f"{run}: events={len(ev)} binds={binds} format-checks={len(checks)} set-clock={sets} kinds={kinds}")
lines.append(f"VIOLATIONS {bad}")
out.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
