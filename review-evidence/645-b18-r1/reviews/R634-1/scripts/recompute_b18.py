#!/usr/bin/env python3
"""Independent recompute of the B18 per-cycle poll figures from the raw counter logs.

usage: python3 -I recompute_b18.py <b18_author_dir> [<b17_author_dir>]
Reads cycles/cNN/poll.jsonl and events.jsonl only; prints one line per cycle and the lane totals.
Time base: the bind event's t_bind_local (the CONNECT_RX command time on the poll host).
"""
import json, sys, datetime, decimal
from pathlib import Path

D = decimal.Decimal
NAMES = {"0x8d4": "SLIP_LB", "0x8d8": "SLIP_TDM", "0x8dc": "RENDER_STAT", "0x8f8": "MCSRV_STAT",
         "0x8e0": "AAFM_STAT", "0x8e4": "AAFM_RATE", "0x738": "CRF_CTRL", "0x748": "CRF_RATE"}


def r2(x):
    return D(repr(x)).quantize(D("0.01"), rounding=decimal.ROUND_HALF_EVEN)


def lane(root):
    root = Path(root)
    out = []
    for cdir in sorted((root / "cycles").glob("c[0-9][0-9]")):
        ev = [json.loads(l) for l in open(cdir / "events.jsonl")]
        polls = [json.loads(l) for l in open(cdir / "poll.jsonl")]
        bt = [e for e in ev if e["kind"] == "bind-time"][0]["t_bind_local"]
        unb = [e for e in ev if e["kind"] == "unbind"][0]["t_cmd_local"]
        bind = [e for e in ev if e["kind"] == "bind"][0]
        st = {e["when"]: e for e in ev if e["kind"] == "state"}
        readable = [p for p in polls if p.get("words")]
        vals = {}
        for p in readable:
            for a, v in p["words"].items():
                vals.setdefault(NAMES.get(a, a), []).append(int(v, 16))
        changes = {k: sorted(set(v)) for k, v in vals.items() if len(set(v)) > 1}
        slip = vals["SLIP_LB"]
        # RENDER_STAT after the bind: first poll whose prefill bit is 0, and first converged
        after = [p for p in readable if p["t0"] >= bt]
        rs = lambda p: int(p["words"]["0x8dc"], 16)
        pf0 = next(p for p in after if not rs(p) & 0x100)
        cv = next(p for p in after if rs(p) & 0x200 and not rs(p) & 0x100)
        tail = [p for p in readable if p["t0"] >= cv["t0"]]
        fills = sorted({rs(p) & 0xFF for p in tail})
        unbound = [p for p in readable if unb <= p["t0"] < bt]
        out.append(dict(
            cycle=cdir.name,
            bind_utc=datetime.datetime.fromtimestamp(bt, datetime.timezone.utc).strftime("%H:%M:%S.%f")[:12],
            polls=len(polls), readable=len(readable),
            first=str(r2(polls[0]["t0"] - bt)), last=str(r2(polls[-1]["t1"] - bt)),
            last_t0=str(r2(polls[-1]["t0"] - bt)),
            slip_lb=(hex(slip[0]), hex(slip[-1]), sorted(set(slip))),
            slip_tdm=sorted(set(vals["SLIP_TDM"])),
            changed=sorted(changes), mcsrv=sorted({hex(x) for x in vals["MCSRV_STAT"]}),
            others_zero=all(set(vals[k]) == {0} for k in ("AAFM_STAT", "AAFM_RATE", "CRF_CTRL", "CRF_RATE")),
            unbound_prefill_fill0=all(rs(p) & 0x1FF == 0x100 for p in unbound[1:]) if unbound else None,
            first_unbound_poll=(str(r2(unbound[0]["t0"] - bt)), hex(rs(unbound[0]))) if unbound else None,
            prefill0_by=str(r2(pf0["t1"] - bt)), converged_by=str(r2(cv["t1"] - bt)),
            fill_after_conv=(fills[0], fills[-1]),
            conv_held=all(rs(p) & 0x300 == 0x200 for p in tail),
            rails=sorted({rs(p) >> 16 for p in readable}),
            bind_status=bind["status"], bind_flags=bind["flags"],
            clk=(st["start"]["clk_dut"], st["end"]["clk_dut"], st["start"]["clk_peer"], st["end"]["clk_peer"]),
            end_bound=st["end"]["rx_dut_0"],
        ))
    return out


def main():
    rows = lane(sys.argv[1])
    for r in rows:
        print(json.dumps(r))
    allslip = sorted({v for r in rows for v in r["slip_lb"][2]})
    print("LANE polls", sum(r["polls"] for r in rows), "readable", sum(r["readable"] for r in rows),
          "SLIP_LB values", allslip, "first", min(r["first"] for r in rows), max(r["first"] for r in rows),
          "last", min(r["last"] for r in rows), max(r["last"] for r in rows))
    if len(sys.argv) > 2:
        rows17 = lane(sys.argv[2])
        for r in rows17:
            print("B17", r["cycle"], r["bind_utc"], r["polls"], r["first"], r["last"], r["slip_lb"][:2])
        print("B17 last range", min(r["last"] for r in rows17), max(r["last"] for r in rows17))


if __name__ == "__main__":
    main()
