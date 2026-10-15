#!/usr/bin/env python3
"""Reviewer recompute of the B17 per-cycle table from the raw counter logs.

usage: python3 -I recompute_b17.py <evidence author dir>

Reads cycles/cNN/events.jsonl and cycles/cNN/poll.jsonl only. Prints one JSON
line per cycle and a closing summary. It does not import or run any author tool.
"""
import datetime
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
SLIP_LB, SLIP_TDM, RENDER, MCSRV, AAFM = "0x8d4", "0x8d8", "0x8dc", "0x8f8", "0x8e0"
out = []
for c in range(1, 11):
    d = root / f"cycles/c{c:02d}"
    ev = [json.loads(l) for l in open(d / "events.jsonl")]
    po = [json.loads(l) for l in open(d / "poll.jsonl")]
    k = {}
    for x in ev:
        k.setdefault(x["kind"], []).append(x)
    unb, bnd = k["unbind"][0], k["bind"][0]
    tb = bnd["t_cmd_local"]
    tu = unb["t_cmd_local"]
    unread = [p["n"] for p in po if any(v is None for v in p["words"].values()) or len(p["words"]) != 8]
    rel0 = [p["t0"] - tb for p in po]
    rel1 = [p["t1"] - tb for p in po]
    periods = [po[i + 1]["t0"] - po[i]["t0"] for i in range(len(po) - 1)]
    lb = [int(p["words"][SLIP_LB], 16) for p in po]
    tdm = [int(p["words"][SLIP_TDM], 16) for p in po]
    changes = []
    for i in range(1, len(po)):
        if lb[i] != lb[i - 1]:
            dd = (lb[i] & 0xFFFF) - (lb[i - 1] & 0xFFFF)
            ds = (lb[i] >> 16) - (lb[i - 1] >> 16)
            changes.append(dict(lo=round(po[i - 1]["t0"] - tb, 3), hi=round(po[i]["t1"] - tb, 3),
                                width=round(po[i]["t1"] - po[i - 1]["t0"], 3), dups=dd, skips=ds,
                                region=("pre-unbind" if po[i]["t1"] < tu else "unbound" if po[i]["t1"] < tb else "bound"),
                                rest_after=round(rel1[-1] - (po[i]["t1"] - tb), 2)))
    servo = sorted({int(p["words"][MCSRV], 16) & 7 for p in po})
    aafm = sorted({p["words"][AAFM] for p in po})
    rs = [int(p["words"][RENDER], 16) for p in po]
    rails = sorted({r >> 16 for r in rs})
    # prefill exit: first poll after the bind with prefill 0, preceded (after the bind) by prefill 1
    pf_exit = None
    post = [(p, r) for p, r in zip(po, rs) if p["t1"] > tb]
    for i, (p, r) in enumerate(post):
        if not (r >> 8) & 1 and i > 0 and (post[i - 1][1] >> 8) & 1:
            pf_exit = (round(post[i - 1][0]["t0"] - tb, 3), round(p["t1"] - tb, 3))
            break
    after_exit = [r for p, r in post if pf_exit and p["t1"] - tb >= pf_exit[1]]
    fills = sorted({r & 0xFF for r in after_exit})
    conv = sorted({(r >> 9) & 1 for r in after_exit})
    pf_after = sorted({(r >> 8) & 1 for r in after_exit})
    utc = datetime.datetime.fromtimestamp(tb, datetime.timezone.utc).strftime("%H:%M:%S.%f")[:-3]
    out.append(dict(cycle=f"c{c:02d}", bind_utc=utc, polls=len(po), unreadable=unread,
                    first_rel=round(rel0[0], 2), last_rel=round(rel1[-1], 2),
                    period_min=round(min(periods), 3), period_max=round(max(periods), 3),
                    unbind_to_bind=round(tb - tu, 4), lb_first=lb[0] & 0xFFFF, lb_last=lb[-1] & 0xFFFF,
                    lb_skips=sorted({v >> 16 for v in lb}), tdm=sorted(set(tdm)), changes=changes,
                    servo_states=servo, aafm_stat=aafm, rails=rails, prefill_exit=pf_exit,
                    fill_after_exit=[min(fills), max(fills)] if fills else None, conv_after_exit=conv,
                    prefill_after_exit=pf_after, bind_status=bnd["status"], unbind_status=unb["status"],
                    bind_flags=bnd["flags"], retry="bind-retry" in k, finally_rebind="finally-rebind" in k,
                    end_check=k["cycle-check"][0], fmt=k["format-check"][0]["set"]))
for o in out:
    print(json.dumps(o))
ch = [x for o in out for x in o["changes"]]
print(json.dumps(dict(summary=True, n_changes=len(ch), all_bound=all(x["region"] == "bound" for x in ch),
                      per_cycle=[len(o["changes"]) for o in out],
                      slip_lo=min(x["lo"] for x in ch), slip_hi=max(x["hi"] for x in ch),
                      width_min=min(x["width"] for x in ch), width_max=max(x["width"] for x in ch),
                      rest_after_min=min(x["rest_after"] for x in ch), rest_after_max=max(x["rest_after"] for x in ch),
                      lb_start=out[0]["lb_first"], lb_end=out[-1]["lb_last"])))
