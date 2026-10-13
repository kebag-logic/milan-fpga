#!/usr/bin/env python3
"""R624-10: recompute lane B16's headline bench figures from per-block and per-poll receipts.

usage: python3 -I spot_check_r624_10.py <published author-r10 packet> <out.json>

Reads only packet files: summary/<run>/c-b9-grade.json (per-block THD+N), r2/<run>-poll-trace.tsv (every poll's
raw console words), r2/<run>-poll-receipt.json (only its span boundaries) and runs/<run>/events.jsonl. Decodes
the words by docs/reference/REGISTER_MAP.md: MCSRV_STAT 0x8F8 [2:0] state (3 ACQUIRE, 4 LOCKED), [31:16]
signed trim in 1/16 ppm; CRF_RATE 0x748 and AAFM_RATE 0x8E4 signed, 512 units per ppm; AAFM_STAT 0x8E0.
Rounds half up to the page's precision.
"""
import csv
import json
import statistics as st
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

P, OUT = Path(sys.argv[1]), Path(sys.argv[2])


def r(x, q="0.01"):
    return str(Decimal(repr(x)).quantize(Decimal(q), ROUND_HALF_UP))


def s16(x):
    x &= 0xFFFF
    return x - 0x10000 if x & 0x8000 else x


def s32(x):
    return x - (1 << 32) if x & 0x80000000 else x


res = {}
for run in ("b0-2", "bcrf", "baaf"):
    g = json.loads((P / f"summary/{run}/c-b9-grade.json").read_text())
    blocks, deg = g["blocks"], set(g["summary"]["degraded_event_free_blocks"])
    x = dict(blocks=len(blocks), events=len(g["events"]), at_floor=len(blocks) - len(deg), degraded=len(deg),
             phase_net_frames=g["phase_net_frames"])
    for ch, tone in (("ch0", "997"), ("ch1", "9973")):
        a = [b[ch]["thdn_db"] for b in blocks]
        f = [b[ch]["thdn_db"] for b in blocks if b["block"] not in deg]
        x[tone] = dict(all_median=r(st.median(a)), all_worst=r(max(a)), floor_median=r(st.median(f)),
                       floor_worst=r(max(f)), largest_block_ppm=r(max(abs(b[ch]["ppm"]) for b in blocks), "0.001"),
                       worst_block=max(blocks, key=lambda b: b[ch]["thdn_db"])["block"])
    if run == "b0-2":
        d, runs = sorted(deg), []
        a0 = p = d[0]
        for v in d[1:] + [None]:
            if v != p + 1:
                runs.append([a0, p])
                a0 = v
            p = v
        x.update(runs=runs, inside_blocks_0_33=sum(1 for v in d if v <= 33), beyond=sum(1 for v in d if v > 33),
                 runs_beyond=sum(1 for q in runs if q[0] > 33),
                 block7=[r(blocks[7]["ch0"]["thdn_db"]), r(blocks[7]["ch1"]["thdn_db"])])
    res[run] = x
for run in ("bcrf", "baaf"):
    rows = list(csv.DictReader(open(P / f"r2/{run}-poll-trace.tsv"), delimiter="\t"))
    span = json.loads((P / f"r2/{run}-poll-receipt.json").read_text())["spans"]["window-start..window-end"]
    for q in rows:
        q["t"] = float(q["start_after_set_s"])
        q["end"] = q["t"] + float(q["length_ms"]) / 1000
        q["w"] = int(q["0x8f8"], 16)
    first = next(i for i, q in enumerate(rows) if q["t"] > 0 and q["w"] & 7 == 4)
    last_acq = max(i for i in range(first) if rows[i]["w"] & 7 == 3)
    win = [q for q in rows if span["from_s"] <= q["t"] and q["end"] <= span["to_s"]]
    res[run]["poll"] = dict(
        lock_bracket=[r(rows[last_acq]["t"], "0.001"), r(rows[first]["end"], "0.001")],
        bracket_polls=[rows[last_acq]["n"], rows[first]["n"]], window_polls=len(win),
        window_locked=sum(1 for q in win if q["w"] & 7 == 4),
        word_0x34=sum(1 for q in win if q["w"] & 0xFFFF == 0x34), word_0x74=sum(1 for q in win if q["w"] & 0xFFFF == 0x74),
        trim_ppm=[min(s16(q["w"] >> 16) / 16 for q in win), max(s16(q["w"] >> 16) / 16 for q in win)],
        crf_rate_ppm=[r(min(s32(int(q["0x748"], 16)) / 512 for q in win)), r(max(s32(int(q["0x748"], 16)) / 512 for q in win))],
        aafm_rate_ppm=[r(min(s32(int(q["0x8e4"], 16)) / 512 for q in win)), r(max(s32(int(q["0x8e4"], 16)) / 512 for q in win))],
        aafm_stat=sorted({q["0x8e0"] for q in win}), slip_tdm=sorted({q["0x8d8"] for q in rows}),
        states_last_12=[q["w"] & 7 for q in rows[-12:]])
    ev = [json.loads(x) for x in open(P / f"runs/{run}/events.jsonl") if x.strip().startswith("{")]
    res[run]["clock_sources"] = [{k: e[k] for k in ("tag", "who", "src", "status", "readback")}
                                 for e in ev if e.get("kind") == "set-clock"]
    fin = next(e for e in ev if e.get("kind") == "final")
    res[run]["final"] = dict(equal_to_found=fin["equal_to_found"], differ=fin["differ"], clk_dut=fin["clk-dut"],
                             clk_peer=fin["clk-peer"])
OUT.write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps({k: {"floor": v.get("at_floor"), "997": v["997"]["all_median"], "9973": v["9973"]["all_median"],
                      "poll": v.get("poll", {}).get("lock_bracket")} for k, v in res.items()}))
