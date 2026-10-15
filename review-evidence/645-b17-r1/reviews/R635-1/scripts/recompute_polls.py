#!/usr/bin/env python3
"""R635-1: recompute the B17 per-cycle table from the raw counter logs (poll.jsonl) and events (events.jsonl).
usage: python3 -I recompute_polls.py <author_dir>   (stdlib only; read-only)"""
import json, sys, datetime, statistics
A = sys.argv[1]
def jl(p): return [json.loads(x) for x in open(p) if x.startswith("{")]
def W(r, k):
    v = r["words"].get(k); return None if v is None else int(v, 16)
out = []
for c in range(1, 11):
    tag = f"c{c:02d}"
    ev = jl(f"{A}/cycles/{tag}/events.jsonl"); po = sorted(jl(f"{A}/cycles/{tag}/poll.jsonl"), key=lambda r: r["n"])
    g = lambda k: [e for e in ev if e["kind"] == k]
    tb = g("bind-time")[0]["t_bind_local"]; tu = g("unbind")[0]["t_cmd_local"]
    bind, unb = g("bind"), g("unbind")
    utc = datetime.datetime.fromtimestamp(tb, datetime.timezone.utc).strftime("%H:%M:%S.%f")[:12]
    ns = [r["n"] for r in po]
    gaps = [b["t0"] - a["t0"] for a, b in zip(po, po[1:])]
    miss = sum(1 for r in po if any(v is None for v in r["words"].values()))
    keys = sorted({k for r in po for k in r["words"]})
    changes = []
    prev = None
    for r in po:
        lb, td = W(r, "0x8d4"), W(r, "0x8d8")
        if prev:
            plb, ptd, pt0 = prev
            for nm, cur, old in (("SLIP_LB", lb, plb), ("SLIP_TDM", td, ptd)):
                if cur != old:
                    changes.append(dict(word=nm, dd=(cur & 0xFFFF) - (old & 0xFFFF), ds=(cur >> 16) - (old >> 16),
                                        lo=round(pt0 - tb, 3), hi=round(r["t1"] - tb, 3), width=round(r["t1"] - pt0, 3), n=r["n"]))
        prev = (lb, td, r["t0"])
    servo = sorted({W(r, "0x8f8") & 7 for r in po}); servo_sv = sorted({r["servo_state"] for r in po})
    aafm = sorted({r["words"]["0x8e0"] for r in po})
    rs = [(round(r["t1"] - tb, 3), W(r, "0x8dc")) for r in po]
    post = [(s, v) for s, v in rs if s > 0]
    pre_exit = next((s for s, v in post if not (v >> 8 & 1)), None)
    # does prefill re-enter after exit?
    after = [v for s, v in post if pre_exit is not None and s >= pre_exit]
    reenter = any(v >> 8 & 1 for v in after)
    fills = [v & 0xFF for v in after]; conv = all(v >> 9 & 1 for v in after); rails = sorted({v >> 16 for s, v in rs})
    sl = [x for x in changes if x["word"] == "SLIP_LB"]
    last_poll = round(po[-1]["t1"] - tb, 3)
    after_slip = round(last_poll - sl[-1]["hi"], 2) if sl else None
    out.append(dict(cycle=tag, bind_utc=utc, bind_status=[e["status"] for e in bind], unbind_status=[e["status"] for e in unb],
                    retries=len(g("bind-retry")), polls=len(po), n_contig=ns == list(range(len(po))),
                    first=round(po[0]["t0"] - tb, 2), last=round(po[-1]["t1"] - tb, 2), unbind_rel=round(tu - tb, 3),
                    spacing_med=round(statistics.median(gaps), 3), spacing_max=round(max(gaps), 3), spacing_min=round(min(gaps), 3),
                    missing=miss, keys=keys,
                    lb_first=W(po[0], "0x8d4"), lb_last=W(po[-1], "0x8d4"), tdm_vals=sorted({W(r, "0x8d8") for r in po}),
                    changes=changes, servo=servo, servo_field=servo_sv, aafm=aafm,
                    prefill_exit=pre_exit, prefill_reenter=reenter, fill=(min(fills), max(fills)) if fills else None,
                    converged_after=conv, rails=rails, hold_after_slip=after_slip,
                    poll_before_bind=g("bind-time")[0]["poll_before_bind_s"],
                    cycle_check=g("cycle-check")[0] if g("cycle-check") else None,
                    fmt=[(e["talker_fmt"], e["listener_fmt"], e["set"]) for e in g("format-check")],
                    poll_end=g("poll-end")[0], capture=[{k: e.get(k) for k in ("file", "bytes", "sha256", "summary", "remote_equal", "removed_from_tap")} for e in g("capture-end")],
                    states=[(e["when"], e["clk_dut"], e["clk_peer"], e["rx_dut_0"]) for e in g("state")],
                    tool=g("start")[0]["tool_sha256"], poller=g("start")[0]["poller_sha256"], finally_rebind=len(g("finally-rebind"))))
for o in out: print(json.dumps(o))
