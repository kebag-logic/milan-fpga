#!/usr/bin/env python3
"""Run timeline (CEST) of every lane-B7 run, the B-AAF SLIP_LB trace, and every non-SUCCESS AECP answer.
Usage: timeline.py <packet-author-dir>"""
import collections, datetime, glob, json, os, sys
ROOT = sys.argv[1]
tz = datetime.timezone(datetime.timedelta(hours=2))
T = lambda t: datetime.datetime.fromtimestamp(t, tz).strftime("%H:%M:%S")
print("## run timeline, CEST")
for c in ["smoke-baaf", "a0", "a1", "a2", "b0", "bcrf", "baaf", "probe"]:
    ev = [json.loads(l) for l in open(f"{ROOT}/runs/{c}/events.jsonl")]
    k = {}
    for e in ev:
        if e["kind"] in ("window-start", "window-end", "set-clock") and e["kind"] not in k:
            k[e["kind"]] = T(e["t"])
    print(f"{c:11s} first {T(ev[0]['t'])} last {T(ev[-1]['t'])} {k}")
print("## B-AAF SLIP_LB (0x8D4[15:0]) at every DUT read")
ev = [json.loads(l) for l in open(f"{ROOT}/runs/baaf/events.jsonl")]
ws = next(e["t"] for e in ev if e["kind"] == "window-start")
for e in ev:
    if e["kind"] == "dut":
        print(f"{e['tag']:13s} t-window {e['t'] - ws:7.1f} s  SLIP_LB dups {int(e['words']['0x8d4'], 16) & 0xFFFF}")
print("## AECP answers per run log (role, status)")
for f in sorted(glob.glob(f"{ROOT}/runs/*/ctl.jsonl")):
    c, bad = collections.Counter(), []
    for l in open(f):
        d = json.loads(l)
        ln = d.get("line", d)
        if isinstance(ln, dict) and ln.get("role"):
            c[(ln["role"], ln.get("status"))] += 1
            if ln.get("status") != "SUCCESS":
                bad.append(dict(cmd=ln.get("cmd"), status=ln.get("status"), what=ln.get("what"), t_tx=T(ln["t_tx"]) if "t_tx" in ln else None))
    print(os.path.relpath(f, ROOT), dict(c), bad)
