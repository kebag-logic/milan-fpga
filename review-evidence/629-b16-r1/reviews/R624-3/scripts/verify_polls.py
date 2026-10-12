#!/usr/bin/env python3
"""Reviewer-side recomputation of B16c's console-poll figures from the published traces alone
(r2/<case>-poll-trace.tsv): the LOCKED bracket (start of the last ACQUIRE poll to the end of the first
LOCKED poll), the window's poll count and servo states, the trim range, SLIP_LB steps and their servo
states, and MCSRV_STAT bit 4 at ACQUIRE/LOCKED polls. MCSRV_STAT per docs/reference/REGISTER_MAP.md
0x8F8: [2:0] state, [4] DRP config mismatch, [6] fine-PS busy, [31:16] signed trim in 1/16 ppm.

usage: verify_polls.py <author packet root> <out.json>
"""
import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
STATES = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}
res = {}
for case in ("bcrf", "baaf"):
    lines = (ROOT / f"r2/{case}-poll-trace.tsv").read_text().splitlines()
    head = lines[0].split("\t")
    rows = [dict(zip(head, x.split("\t"))) for x in lines[1:]]
    marks = json.loads((ROOT / f"r2/{case}-poll-receipt.json").read_text())["marks_after_set_s"]
    P = []
    for r in rows:
        st = int(r["0x8f8"], 16)
        t0 = Decimal(r["start_after_set_s"])
        t1 = t0 + Decimal(r["length_ms"]) / 1000
        trim = ((st >> 16) - (1 << 16) if st >> 31 else st >> 16) / 16
        P.append(dict(n=int(r["n"]), t0=t0, t1=t1, state=STATES[st & 7], bit4=bool(st & 0x10), busy=bool(st & 0x40),
                      trim=trim, slip_lb=int(r["0x8d4"], 16), slip_tdm=int(r["0x8d8"], 16), aafm=r["0x8e0"]))
    after = [p for p in P if p["t0"] >= 0]
    fl = next(p for p in after if p["state"] == "LOCKED")
    la = [p for p in after if p["n"] < fl["n"] and p["state"] == "ACQUIRE"][-1]
    ws, we = Decimal(str(marks["window-start"])), Decimal(str(marks["window-end"]))
    win = [p for p in P if p["t0"] >= ws and p["t1"] <= we]
    locked_after = [p for p in P if p["n"] >= fl["n"]]
    steps = []
    for a, b in zip(P, P[1:]):
        if b["slip_lb"] != a["slip_lb"]:
            steps.append(dict(polls=[a["n"], b["n"]], from_s=str(a["t0"]), to_s=str(b["t1"]),
                              states=[a["state"], b["state"]], word=[hex(a["slip_lb"]), hex(b["slip_lb"])]))
    acq_locked = [p for p in P if p["state"] in ("ACQUIRE", "LOCKED")]
    res[case] = dict(
        polls=len(P),
        lock_bracket=[str(la["t0"]), str(fl["t1"]), la["n"], fl["n"]],
        window_polls=len(win), window_states=sorted({p["state"] for p in win}),
        window_busy=sum(p["busy"] for p in win),
        window_trim=[min(p["trim"] for p in win), max(p["trim"] for p in win)],
        window_slip_tdm=sorted({p["slip_tdm"] for p in win}),
        window_aafm=sorted({p["aafm"] for p in win}),
        bit4_at_acq_locked=[sum(p["bit4"] for p in acq_locked), len(acq_locked)],
        steps_after_first_locked=[s for s in steps if s["polls"][0] >= fl["n"]],
        steps=steps,
        last_states=[p["state"] for p in P[-12:]],
    )
OUT.write_text(json.dumps(res, indent=1, default=str))
for c, r in res.items():
    print(c, json.dumps({k: v for k, v in r.items() if k != "steps"}, default=str))
    for s in r["steps"]:
        print("  step", s)
