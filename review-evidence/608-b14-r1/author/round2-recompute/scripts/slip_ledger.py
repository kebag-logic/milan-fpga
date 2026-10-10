#!/usr/bin/env python3
"""Account for every SLIP_LB frame from the as-found read to the final read, by phase.

Inputs, all in the archived packet: item2/summary/switches.json (each phase's
start and end SLIP_LB dups) and the console reads of 0x900008d4.
SLIP_LB dups = little-endian word [15:0]; 2 dups per slipped frame on this lane.

usage: slip_ledger.py <packet-author-dir>
"""
import json
import re
import sys

A = sys.argv[1]


def console_lb(rel):
    t = open(f"{A}/{rel}", errors="replace").read()
    m = re.search(r"cmd='mem_read 0x900008d4 12'.*?\n0x900008d4\s+((?:[0-9a-f]{2} ){4})", t, re.S)
    return int.from_bytes(bytes.fromhex(m.group(1).replace(" ", "")), "little") & 0xFFFF


sw = json.load(open(f"{A}/item2/summary/switches.json"))
af = [console_lb("item2/setup/dut-before.txt"), console_lb("item2/setup2/dut-before.txt")]
first_before = sw[0]["slip_lb_before"][0]
transient = sum(x["slip_lb_transient_dups"] for x in sw if x["to_source"] == 2)
aaf_after = sum(x["slip_lb_after_dups"] for x in sw if x["to_source"] == 2)
crf = sum(x["slip_lb_end"][0] - x["slip_lb_before"][0] for x in sw if x["to_source"] == 1)
returns = sum(x["slip_lb_end"][0] - x["slip_lb_before"][0] for x in sw if x["to_source"] == 0)
within = between = 0
for prev, cur in zip(sw, sw[1:]):
    d = cur["slip_lb_before"][0] - prev["slip_lb_end"][0]
    if prev["run"] == cur["run"]:
        within += d
    else:
        between += d
last_end = sw[-1]["slip_lb_end"][0]
teardown = console_lb("item2/teardown/dut-after.txt")
prebind = console_lb("soak/console-prebind.txt")
s000 = console_lb("soak/console-soak-000.txt")
s005 = console_lb("soak/console-soak-005.txt")
s010 = console_lb("soak/console-soak-010.txt")
rest = [console_lb(f"soak/console-soak-{i:03d}.txt") for i in range(10, 121, 5)]
final = console_lb("restore/console-final.txt")

rows = [
    ("as found (05:17:01, 05:20:08 reads)", af),
    ("setup binds to cycle 1's first set", first_before - af[1]),
    ("INTERNAL to AAF, before the settle boundary", transient),
    ("INTERNAL to AAF, after the boundary", aaf_after),
    ("AAF to CRF holds", crf),
    ("returns to INTERNAL, 15 s holds", returns),
    ("INTERNAL between cycles of one run", within),
    ("INTERNAL between runs", between),
    ("item 2 last poll to teardown read", teardown - last_end),
    ("items 3 and 4 (teardown read to soak pre-bind read)", prebind - teardown),
    ("across the soak bind (pre-bind to soak-000)", s000 - prebind),
    ("soak-000 to soak-005", s005 - s000),
    ("soak-005 to soak-010", s010 - s005),
    ("soak-010 to soak-120 and final", final - s010),
]
total = 0
for name, dups in rows:
    if isinstance(dups, list):
        print(f"{name:55s} reads {dups}")
        continue
    total += dups
    print(f"{name:55s} {dups:4d} dups {dups / 2:5.1f} frames")
print(f"{'total':55s} {total:4d} dups {total / 2:5.1f} frames; final read {final} = {final:#x}")
print(f"soak-010..soak-120 reads constant: {len(set(rest)) == 1} ({rest[0]:#x})")
assert total == final - af[1]
