#!/usr/bin/env python3
"""Rebuild the SLIP_LB phase ledger from the archived packet.

Usage: slip_lb_ledger.py <packet-author-dir>
Sources: item2/summary/switches.json, item2/cyc*/events.jsonl, and the
console dumps (mem_read 0x900008d4: SLIP_LB low 16 bits = dups).
"""
import json, re, sys, datetime
from pathlib import Path

A = Path(sys.argv[1])

def console_slip(path):
    out, ts = [], None
    for line in open(path, errors="replace"):
        m = re.match(r"### (\S+) cmd='mem_read 0x900008d4", line)
        if m:
            ts = m.group(1)
            continue
        m = re.match(r"0x900008d4\s+((?:[0-9a-f]{2} ){4})", line)
        if m and ts:
            b = bytes.fromhex(m.group(1).replace(" ", ""))
            out.append((ts, int.from_bytes(b, "little")))
            ts = None
    return out

sw = json.load(open(A / "item2/summary/switches.json"))
ph = {"setup": 0, "aaf": 0, "crf": 0, "int_hold": 0, "between_cycles": 0, "between_runs": 0}
asfound = [console_slip(A / p) for p in ("item2/setup/dut-before.txt", "item2/setup2/dut-before.txt")]
print("as found:", asfound)
ph["setup"] = sw[0]["slip_lb_before"][0] - asfound[-1][-1][1]
for i, x in enumerate(sw):
    kind = x["tag"].split("-")[1]
    d = x["slip_lb_end"][0] - x["slip_lb_before"][0]
    ph["int_hold" if kind == "int" else kind] += d
    if i:
        gap = x["slip_lb_before"][0] - sw[i - 1]["slip_lb_end"][0]
        if gap:
            same_run = x["run"] == sw[i - 1]["run"]
            if kind != "aaf":
                print("UNEXPECTED within-cycle gap", x["tag"], gap)
            ph["between_cycles" if same_run else "between_runs"] += gap
# run boundary durations from events
runs = sorted({x["run"] for x in sw})
bounds = []
for r in runs:
    ev = [json.loads(l) for l in open(A / f"item2/{r}/events.jsonl")]
    bounds.append((r, ev[0]["t"], ev[-1]["t"]))
gaps = [round(bounds[i + 1][1] - bounds[i][2], 1) for i in range(len(bounds) - 1)]
print("between-run wall gaps (first event of next run minus last event of previous), s:", gaps)
td = console_slip(A / "item2/teardown/dut-after.txt")
pre = console_slip(A / "soak/console-prebind.txt")
soak = {n: console_slip(A / f"soak/console-soak-{n:03d}.txt") for n in range(0, 121, 5)}
fin = console_slip(A / "restore/console-final.txt")
print("item2 last phase end:", sw[-1]["slip_lb_end"][0], "teardown:", td, "prebind:", pre)
print("soak reads:", {k: v[0][1] for k, v in soak.items()}, soak[0][0][0], soak[5][0][0], soak[10][0][0])
print("final:", fin)
ph["last_poll_to_teardown"] = td[-1][1] - sw[-1]["slip_lb_end"][0]
ph["items3_4"] = pre[-1][1] - td[-1][1]
ph["across_soak_bind"] = soak[0][0][1] - pre[-1][1]
steps = [(k, soak[k][0][1] - soak[k - 5][0][1]) for k in range(5, 121, 5) if soak[k][0][1] != soak[k - 5][0][1]]
print("soak steps between 5-minute reads:", steps)
ph["soak"] = soak[120][0][1] - soak[0][0][1]
ph["soak_end_to_final"] = fin[-1][1] - soak[120][0][1]
tot = sum(ph.values())
print("phase dups:", ph)
print("phase frames:", {k: v / 2 for k, v in ph.items()})
print("total dups %d (0x%x), frames %s" % (tot, tot, tot / 2))
