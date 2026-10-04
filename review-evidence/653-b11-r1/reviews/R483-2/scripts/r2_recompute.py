#!/usr/bin/env python3
"""Recompute the round-2 figures of docs/findings/653_DISCONNECT_ORDER_BENCH.md
from the lane's round-1 raw files (public evidence tree, author/ directory).

Usage: r2_recompute.py <author-dir> <page.md>
Prints a receipt; exits 1 if any check fails.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

author = Path(sys.argv[1])
page = Path(sys.argv[2]).read_text(encoding="utf-8")
fails = []


def check(name, ok, detail=""):
    print(f"{'OK  ' if ok else 'FAIL'} {name} {detail}")
    if not ok:
        fails.append(name)


# 1. Control interval from the provided decoder's C0 output.
# Its time column is (S - S0)/1e6 with S the LE64 read of the tap record's
# two 32-bit words in swapped order, so a true interval in ns is dS / 2**32
# while the high word does not carry.
lines = (author / "summary/decode/b11-a535-s0b-C0.decode.txt").read_text().splitlines()
t = {}
for ln in lines:
    m = re.match(r"\s*(-?[0-9.]+) ms (\S+)\s+(.*)", ln)
    if not m:
        continue
    ms, port, rest = float(m.group(1)), m.group(2), m.group(3)
    if "AECP RSP GET_COUNTERS" in rest and "UNSOL" not in rest and port == "DUT->sw":
        t["own_rsp"] = ms
    elif "ACMP UNBIND_RX_CMD" in rest:
        t["cmd"] = ms
    elif "ACMP UNBIND_RX_RESP" in rest:
        t["rsp"] = ms
print("decoder C0 time column (ms, swapped-word scale):", t)
us = lambda a, b: (t[b] - t[a]) * 1e6 / 2**32 / 1e3
own_cmd, own_rsp, cmd_rsp = us("own_rsp", "cmd"), us("own_rsp", "rsp"), us("cmd", "rsp")
print(f"own GET_COUNTERS answer -> UNBIND_RX command : {own_cmd:.3f} us")
print(f"own GET_COUNTERS answer -> UNBIND_RX response: {own_rsp:.3f} us")
print(f"UNBIND_RX command -> response                : {cmd_rsp:.3f} us")
g = json.loads((author / "summary/o653-grade.json").read_text())
c0 = g["s0b/C0"]["wire"]
print("grade C0 own_rsp_to_cmd_us", c0["control"]["own_rsp_to_cmd_us"], "cmd_to_rsp_us", c0["cmd_to_rsp_us"],
      "order_vs_own", c0["control"]["order_vs_own"], "order", c0["order"])
check("C0 command interval rounds to 1,629.8", f"{own_cmd:,.1f}" == "1,629.8")
check("C0 response interval rounds to 1,637.3", f"{own_rsp:,.1f}" == "1,637.3")
check("decoder command interval equals grade own_rsp_to_cmd_us", round(own_cmd, 1) == c0["control"]["own_rsp_to_cmd_us"])
check("grade own+cmd_to_rsp equals response figure",
      round(c0["control"]["own_rsp_to_cmd_us"] + c0["cmd_to_rsp_us"], 1) == 1637.3)
check("page sentence carries both figures paired with their events",
      "The UNBIND_RX command left 1,629.8 µs after the probe's own\nGET_COUNTERS answer, and its response 1,637.3 µs after it." in page)
check("control reads COUNTERS_FIRST against own, RESPONSE_FIRST against push",
      c0["control"]["order_vs_own"] == "COUNTERS_FIRST" and c0["order"] == "RESPONSE_FIRST")

# 2. Library counters updates for the DUT's STREAM_INPUTs, from the probe logs.
accept = lambda ml, mu: ml == mu or ml == mu + 1
census = Counter()
per_cycle = defaultdict(list)
events_nonzero = 0
compat_seen = set()
for sess in ("s0b", "s1"):
    cyc = None
    for ln in (author / f"runs/{sess}/{sess}-probe.jsonl").read_text().splitlines():
        d = json.loads(ln)
        if d.get("ev") == "cycle_begin":
            cyc = d["tag"]
        if d.get("who") != "dut":
            continue
        if d.get("ev") in ("si_counters", "si_connection"):
            per_cycle[(sess, cyc)].append(d)
        if d.get("ev") == "si_counters":
            ml, mu = d["counters"]["ML"], d["counters"]["MU"]
            census[(f"{ml}/{mu}", d["lib_conn"], accept(ml, mu))] += 1
            events_nonzero += d.get("n_events", 0) != 0
            compat_seen.add(d.get("compat_names"))
for k, v in sorted(census.items()):
    print(f"  update {k[0]} {k[1]:13s} x{v}  accepted by the check: {k[2]}")
check("updates are exactly 0/0 Connected, 1/0 Connected, 1/1 NotConnected, 23 each",
      dict(census) == {("0/0", "Connected", True): 23, ("1/0", "Connected", True): 23,
                       ("1/1", "NotConnected", True): 23})
check("no update carried a compatibility event; Milan flag present on every update",
      events_nonzero == 0 and compat_seen == {"IEEE17221|Milan"}, str(compat_seen))

# 3. The CRF window: NotConnected -> the next counters update, and nothing between.
for cyc, want in (("R01", "95.0"), ("R02", "100.0")):
    evs = per_cycle[("s1", cyc)]
    idx_set = {e["idx"] for e in evs}
    nc = [e for e in evs if e["ev"] == "si_connection" and e["state"] == "NotConnected"][0]
    after = [e for e in evs if e["ev"] == "si_counters" and e["t"] > nc["t"]]
    before = [e for e in evs if e["ev"] == "si_counters" and e["t"] < nc["t"]]
    first = after[0]
    w = (first["t"] - nc["t"]) / 1e3
    print(f"  {cyc}: input idx {idx_set}; held before NotConnected "
          f"{before[-1]['counters']['ML']}/{before[-1]['counters']['MU']} {before[-1]['lib_conn']} "
          f"at bind+{(before[-1]['t'] - before[0]['t']) / 1e3:.1f} ms; window {w:.1f} ms; "
          f"next update {first['counters']['ML']}/{first['counters']['MU']}/{first['counters']['SI']}; "
          f"updates after NotConnected {len(after)}")
    check(f"{cyc} window {want} ms, no update inside, next carries 1/1/0",
          f"{w:.1f}" == want and idx_set == {1} and len(after) == 1
          and (first["counters"]["ML"], first["counters"]["MU"], first["counters"]["SI"]) == (1, 1, 0)
          and (before[-1]["counters"]["ML"], before[-1]["counters"]["MU"]) == (1, 0)
          and before[-1]["lib_conn"] == "Connected")

print("RESULT", "PASS" if not fails else f"FAIL {fails}")
sys.exit(1 if fails else 0)
