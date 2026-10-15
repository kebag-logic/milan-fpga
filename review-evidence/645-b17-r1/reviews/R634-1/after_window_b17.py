#!/usr/bin/env python3
"""Reviewer receipt: the B17 after-slip burst figures by window, and the prefill/convergence instants.

usage: python3 -I after_window_b17.py <evidence author dir>

Bursts: peer PDUs over 20 us late (summary/cNN.json late_pdus), grouped while < 1 ms apart, as the
lane's summary tool groups them. For bursts after each slip's interval it reports the count and peak
(i) to the capture's end, as the page prints them, (ii) within the 32 s hold, and (iii) within the
last poll. It also reports the next cycle's first SLIP_LB read (the cumulative counter covering the
bursts after the last poll), the RENDER_STAT prefill/converged bracket after each bind, and the
unrounded last-poll time.
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
HOLD = 32.0
rows = []
for c in range(1, 11):
    g = json.load(open(root / f"summary/c{c:02d}.json"))
    ev = [json.loads(l) for l in open(root / f"cycles/c{c:02d}/events.jsonl")]
    po = [json.loads(l) for l in open(root / f"cycles/c{c:02d}/poll.jsonl")]
    tb = next(e for e in ev if e["kind"] == "bind")["t_cmd_local"]
    b = []
    for x in g["tap"]["late_pdus"]:
        if x["late_us"] <= 20.0:
            continue
        if b and x["s"] - b[-1]["last"] < 1e-3:
            b[-1]["last"] = x["s"]; b[-1]["peak"] = max(b[-1]["peak"], x["late_us"])
        else:
            b.append(dict(s=x["s"], last=x["s"], peak=x["late_us"]))
    s = g["poll"]["slips"][0]
    last = po[-1]["t1"] - tb
    slipped = max(z["peak"] for z in b if s["s_lo"] <= z["s"] <= s["s_hi"])
    aft = [z for z in b if z["s"] > s["s_hi"]]
    w = {"capture_end": aft, "hold_32s": [z for z in aft if z["s"] <= HOLD], "last_poll": [z for z in aft if z["s"] <= last]}
    post = [(p["t0"] - tb, p["t1"] - tb, int(p["words"]["0x8dc"], 16)) for p in po if p["t1"] > tb]
    pre_last = [(p["t0"] - tb, p["t1"] - tb, int(p["words"]["0x8dc"], 16)) for p in po if p["t1"] <= tb][-1]
    first_pf0 = next(i for i, x in enumerate(post) if not (x[2] >> 8) & 1)
    first_cv = next(i for i, x in enumerate(post) if (x[2] >> 9) & 1)
    prev_pf = (post[first_pf0 - 1] if first_pf0 else pre_last)
    rows.append(dict(cycle=f"c{c:02d}", last_poll_unrounded=round(last, 4), capture_last_peer_pdu_s=g["tap"]["streams"]["peer-aaf"]["last_s"],
                     slipped_burst_peak=slipped,
                     **{f"after_{k}": dict(n=len(v), peak=max((z["peak"] for z in v), default=None),
                                           later_than_slipped=any(z["peak"] > slipped for z in v)) for k, v in w.items()},
                     prefill_exit_bracket=(round(max(prev_pf[0], 0.0), 3), round(post[first_pf0][1], 3)),
                     first_post_bind_poll=dict(t1=round(post[0][1], 3), prefill=(post[0][2] >> 8) & 1, converged=(post[0][2] >> 9) & 1, fill=post[0][2] & 0xFF),
                     converged_first_poll_end=round(post[first_cv][1], 3),
                     first_peer_pdu_after_command_s=g["tap"]["priming"]["first_pdu_after_command_ms"] / 1e3))
for r in rows:
    print(json.dumps(r))
nxt = {}
for c in range(1, 10):
    a = [json.loads(l) for l in open(root / f"cycles/c{c:02d}/poll.jsonl")][-1]["words"]["0x8d4"]
    b0 = [json.loads(l) for l in open(root / f"cycles/c{c + 1:02d}/poll.jsonl")][0]["words"]["0x8d4"]
    nxt[f"c{c:02d}->c{c + 1:02d}"] = [a, b0, a == b0]
print(json.dumps(dict(summary=True, next_cycle_first_read_equals_last=nxt,
                      **{f"after_{k}": dict(n=[min(r[f'after_{k}']['n'] for r in rows), max(r[f'after_{k}']['n'] for r in rows)],
                                            peak=[min(r[f'after_{k}']['peak'] for r in rows), max(r[f'after_{k}']['peak'] for r in rows)],
                                            later_than_slipped=sum(r[f'after_{k}']['later_than_slipped'] for r in rows))
                         for k in ("capture_end", "hold_32s", "last_poll")})))
