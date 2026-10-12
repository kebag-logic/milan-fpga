#!/usr/bin/env python3
"""R624-4: recompute lane B16's key figures from the packet's primary summaries, without the author's check.

usage: recompute_b16.py <author packet root> <out.json>

Reads only packet files: B0's and B16c's b9 grades (per-block THD+N and events), the alignments, the
point-(d) decodes and the poll traces (eight raw words per poll, decoded by docs/reference/REGISTER_MAP.md:
MCSRV_STAT [2:0] state, [6] actuator busy; SLIP_LB [15:0] dups; CRF_RATE and AAFM_RATE signed, 512 per ppm;
AAFM_STAT [0] locked, [1] valid, [2] enabled, [15:8] restarts, [31:16] largest deviation ns).
Prints and writes the recomputed values; the reviewer compares them with the page by hand in REPORT.md.
"""
import json
import statistics
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

R = Path(sys.argv[1])
OUT = Path(sys.argv[2])
J = lambda p: json.loads((R / p).read_text())
r2 = lambda x, n=2: float(Decimal(str(x)).quantize(Decimal(1).scaleb(-n), ROUND_HALF_UP))
res = {}

# ---- B0 and B16c at (c): floor rule of b9_thdn.py (event-free and within 3 dB of each tone's event-free median)
for run in ("b0-2", "bcrf", "baaf"):
    g = J(f"summary/{run}/c-b9-grade.json")
    bl = g["blocks"]
    free = [b for b in bl if b["events"] == 0]
    med = {c: statistics.median(b[c]["thdn_db"] for b in free) for c in ("ch0", "ch1")}
    floor = [b for b in free if all(b[c]["thdn_db"] <= med[c] + 3.0 for c in ("ch0", "ch1"))]
    fl = {b["block"] for b in floor}
    deg = [b["block"] for b in free if b["block"] not in fl]
    runs = []
    for k in deg:
        if runs and runs[-1][1] == k - 1:
            runs[-1][1] = k
        else:
            runs.append([k, k])
    out = {"blocks": len(bl), "events": sum(b["events"] for b in bl), "at_floor": len(floor), "degraded": len(deg),
           "runs": runs}
    for c in ("ch0", "ch1"):
        th_f = [b[c]["thdn_db"] for b in floor]
        th_a = [b[c]["thdn_db"] for b in bl]
        out[c] = {"floor_median": r2(statistics.median(th_f)), "floor_worst": r2(max(th_f)),
                  "all_median": r2(statistics.median(th_a)), "all_worst": r2(max(th_a)),
                  "worst_block": max(bl, key=lambda b: b[c]["thdn_db"])["block"]}
    if run == "b0-2":
        aa, ab = J("summary/b0-2/align-a-c.json"), J("summary/b0-2/align-b-c.json")
        cov = aa["covered_recording_frames"]
        whole = [b["block"] for b in bl if b["start"] >= cov[0] and b["start"] + 48000 <= cov[1]]
        inside = [k for k in deg if k in whole]
        out["overlap"] = {"a_frames": aa["compared_equal"], "b_frames": ab["compared_equal"],
                          "a_diff": aa["frames_differing"], "b_diff": ab["frames_differing"],
                          "seconds": round(cov[1] / 48000, 4), "whole_blocks": [min(whole), max(whole)],
                          "inside": len(inside), "beyond": len(deg) - len(inside),
                          "runs_beyond": sum(1 for a, b in runs if a > max(whole)),
                          "worst_inside": {c: [r2(max(bl[k][c]["thdn_db"] for k in inside)),
                                               max(inside, key=lambda k: bl[k][c]["thdn_db"])] for c in ("ch0", "ch1")}}
    res[f"c:{run}"] = out

# ---- point (d): blocks wholly inside the playback at the loop's floor (per-block THD+N within 3 dB of the median)
for run in ("pts2", "b0-2", "bcrf", "baaf"):
    d = J(f"summary/{run}/d-extcap-pair.json")
    row = d["rows"][0] if "rows" in d else d
    o = {}
    for t in ("tone_997", "tone_9973"):
        if t not in row:
            continue
        pb = row[t]["per_block"]
        playing = [i for i, b in enumerate(pb) if b["level_dbfs"] > -200]
        first = playing[0]
        whole = [i for i in playing if i > first and i < len(pb) - 0] if run != "pts2" else [i for i in playing if i > first]
        medv = row[t]["median"]["thdn_db"]
        atf = [i for i in whole if pb[i]["thdn_db"] <= medv + 3.0]
        o[t] = {"blocks": len(pb), "silent_before": first, "start_block": first, "whole": len(whole),
                "whole_at_floor": len(atf), "not_at_floor": [i for i in whole if i not in atf],
                "median_thdn": r2(medv)}
    res[f"d:{run}"] = o
    try:
        dl = J(f"summary/{run}/d-loop-decode.json")
        res[f"d:{run}"]["decode"] = {k: dl.get(k) for k in ("decoded", "skips", "repeats", "net_step_frames", "torn")}
        if "first_decoded_frame" in dl:
            res[f"d:{run}"]["decode"]["span_s"] = round((dl["last_decoded_frame"] - dl["first_decoded_frame"] + 1) / 48000, 2)
    except FileNotFoundError:
        pass

# ---- B16c poll traces


def s32(h):
    v = int(h, 16)
    return v - (1 << 32) if v & 0x80000000 else v


ST = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}
for run in ("bcrf", "baaf"):
    rc = J(f"r2/{run}-poll-receipt.json")
    marks = rc["marks_after_set_s"]
    lines = (R / f"r2/{run}-poll-trace.tsv").read_text().splitlines()
    hdr = lines[0].split("\t")
    polls = []
    for ln in lines[1:]:
        f = dict(zip(hdr, ln.split("\t")))
        polls.append({"n": int(f["n"]), "t0": float(f["start_after_set_s"]), "t1": float(f["start_after_set_s"]) + float(f["length_ms"]) / 1000,
                      "st": ST[int(f["0x8f8"], 16) & 7], "busy": bool(int(f["0x8f8"], 16) & 0x40), "lo16": int(f["0x8f8"], 16) & 0xffff,
                      "lb": int(f["0x8d4"], 16) & 0xffff, "tdm": int(f["0x8d8"], 16),
                      "crf": s32(f["0x748"]) / 512, "aafs": int(f["0x8e0"], 16), "aafr": s32(f["0x8e4"]) / 512})
    fl = next(i for i, p in enumerate(polls) if p["st"] == "LOCKED")
    la = max(i for i in range(fl) if polls[i]["st"] == "ACQUIRE")
    win = [p for p in polls if marks["window-start"] <= p["t0"] and p["t1"] <= marks["window-end"]]
    win2 = [p for p in polls if marks["window-start"] <= p["t0"] < marks["window-end"]]
    steps = []
    for a, b in zip(polls, polls[1:]):
        if b["lb"] != a["lb"]:
            steps.append({"from_s": round(a["t0"], 3), "to_s": round(b["t1"], 3), "d": b["lb"] - a["lb"], "st": [a["st"], b["st"]]})
    after_locked = [s for s in steps if s["from_s"] >= polls[fl]["t0"]]
    o = {"lock_bracket": [round(polls[la]["t0"], 3), round(polls[fl]["t1"], 3)], "polls_last_acq_first_lock": [polls[la]["n"], polls[fl]["n"]],
         "window_polls_t1_inside": len(win), "window_polls_t0_inside": len(win2),
         "window_states": sorted({p["st"] for p in win2}), "window_busy": sum(p["busy"] for p in win2),
         "window_trim_lo16": sorted({hex(p["lo16"]) for p in win2}),
         "window_crf_ppm": [r2(min(p["crf"] for p in win2)), r2(max(p["crf"] for p in win2))],
         "window_tdm": sorted({p["tdm"] for p in win2}),
         "slip_lb": [polls[0]["lb"], polls[-1]["lb"]], "steps": steps, "steps_after_first_locked": after_locked,
         "binds_s": marks["binds"]}
    if run == "baaf":
        o["window_aafm_stat"] = sorted({hex(p["aafs"]) for p in win2})
        o["window_aafm_ppm"] = [r2(min(p["aafr"] for p in win2)), r2(max(p["aafr"] for p in win2))]
    res[f"poll:{run}"] = o

OUT.write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1)[:12000])
