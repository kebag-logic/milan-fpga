#!/usr/bin/env python3
"""R624-5: recompute B16c's poll figures from the published per-poll trace and the run's own marks,
independently of the packet's receipt tools.

usage: recompute_b16c_poll.py <author packet> <out.json>

Servo state = MCSRV_STAT[2:0] (docs/reference/REGISTER_MAP.md 0x8F8): 3 ACQUIRE, 4 LOCKED, 0 IDLE.
Trim = MCSRV_STAT[31:16] signed, 1/16 ppm. SLIP_LB dups = 0x8D4 (as the page's start value 162 reads).
Times are the trace's start_after_set_s (poll start relative to the DUT's set) and length_ms.
"""
import json, sys
from pathlib import Path

pk, out = Path(sys.argv[1]), Path(sys.argv[2])
NAME = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}
res = {}
for run in ("bcrf", "baaf"):
    rows = [l.split("\t") for l in (pk / f"r2/{run}-poll-trace.tsv").read_text().splitlines()]
    hdr, rows = rows[0], rows[1:]
    ix = {h: i for i, h in enumerate(hdr)}
    ev = [json.loads(l) for l in (pk / f"runs/{run}/events.jsonl").read_text().splitlines()]
    marks = next(e for e in ev if e["kind"] == "poll-summary")["marks_raw"]
    ws = (marks["window-start"] - marks["dut-set"]) / 1e9
    we = (marks["window-end"] - marks["dut-set"]) / 1e9
    polls = []
    for r in rows:
        st = int(r[ix["0x8f8"]], 16)
        trim = st >> 16
        trim = (trim - 65536 if trim & 0x8000 else trim) / 16
        polls.append(dict(n=int(r[0]), s=float(r[1]), e=float(r[1]) + float(r[2]) / 1000, state=NAME[st & 7],
                          busy=bool(st & 0x40), drp_mismatch=bool(st & 0x10), trim=trim,
                          slip_lb=int(r[ix["0x8d4"]], 16), word=st & 0xffff))
    win = [p for p in polls if p["s"] >= ws and p["e"] <= we]
    first_locked = next(i for i, p in enumerate(polls) if p["state"] == "LOCKED")
    states = {}
    for p in win:
        states[p["state"]] = states.get(p["state"], 0) + 1
    steps = []
    for a, b in zip(polls, polls[1:]):
        if b["slip_lb"] != a["slip_lb"]:
            steps.append(dict(between=[a["n"], b["n"]], after_set_s=[round(a["s"], 3), round(b["e"], 3)],
                              delta=b["slip_lb"] - a["slip_lb"], states=[a["state"], b["state"]]))
    after_lock = [s for s in steps if s["between"][0] >= polls[first_locked]["n"]]
    res[run] = dict(
        window_s=[round(ws, 3), round(we, 3)], window_polls=len(win), window_states=states,
        window_busy=sum(p["busy"] for p in win), window_word_0x34=sum(p["word"] == 0x34 for p in win),
        window_word_0x74=sum(p["word"] == 0x74 for p in win),
        trim_range=[min(p["trim"] for p in win), max(p["trim"] for p in win)],
        lock_bracket_from_last_acquire_start=[round(polls[first_locked - 1]["s"], 3), round(polls[first_locked]["e"], 3)],
        last_acquire_poll=polls[first_locked - 1]["n"], first_locked_poll=polls[first_locked]["n"],
        acq_locked_all_drp_mismatch=all(p["drp_mismatch"] for p in polls if p["state"] in ("ACQUIRE", "LOCKED")),
        left_locked_after_first_lock=[p["n"] for p in polls[first_locked:] if p["state"] != "LOCKED" and p["s"] < we],
        slip_lb_first_last=[polls[0]["slip_lb"], polls[-1]["slip_lb"]], slip_steps=steps,
        slip_steps_after_lock=after_lock, polls_total=len(polls))
out.write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps({r: {k: v for k, v in d.items() if k != "slip_steps"} for r, d in res.items()}, indent=1))
for r in res:
    for s in res[r]["slip_steps"]:
        print(r, s)
