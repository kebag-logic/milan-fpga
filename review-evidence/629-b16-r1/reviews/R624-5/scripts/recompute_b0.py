#!/usr/bin/env python3
"""R624-5: recompute lane B16b's B0 figures from the per-block grade and the two alignments, independently of
the packet's receipt tools; and B16c's grade summaries from their per-block data.

usage: recompute_b0.py <author packet> <out.json>

Floor = an event-free block within 3 dB of the median of the event-free blocks (the page's rule), per tone,
a block at the floor on both tones. Degraded = event-free blocks not at the floor.
"""
import json, statistics, sys
from pathlib import Path

pk, out = Path(sys.argv[1]), Path(sys.argv[2])
FS = 48000


def runs(xs):
    r = []
    for x in xs:
        if r and x == r[-1][1] + 1:
            r[-1][1] = x
        else:
            r.append([x, x])
    return r


def grade(run):
    d = json.loads((pk / f"summary/{run}/c-b9-grade.json").read_text())
    B = d["blocks"]
    ef = [b for b in B if b["events"] == 0]
    res = {"blocks": len(B), "events": len(d["events"]), "phase_net_frames": d["phase_net_frames"]}
    at = set(b["block"] for b in ef)
    for ch in ("ch0", "ch1"):
        med = statistics.median(b[ch]["thdn_db"] for b in ef)
        fl = {b["block"] for b in ef if b[ch]["thdn_db"] <= med + 3}
        at &= fl
        res[ch + "_all"] = dict(median=round(statistics.median(b[ch]["thdn_db"] for b in B), 2),
                                worst=round(max(b[ch]["thdn_db"] for b in B), 2),
                                worst_block=max(B, key=lambda b: b[ch]["thdn_db"])["block"],
                                level_median=round(statistics.median(b[ch]["level_dbfs"] for b in B), 2),
                                ppm_maxabs=round(max(abs(b[ch]["ppm"]) for b in B), 3))
    for ch in ("ch0", "ch1"):
        fb = [b for b in B if b["block"] in at]
        res[ch + "_floor"] = dict(median=round(statistics.median(b[ch]["thdn_db"] for b in fb), 2),
                                  worst=round(max(b[ch]["thdn_db"] for b in fb), 2),
                                  snr_median=round(statistics.median(b[ch]["snr_db"] for b in fb), 2))
    res["at_floor"] = len(at)
    deg = sorted(b["block"] for b in ef if b["block"] not in at)
    res["degraded"] = len(deg)
    res["degraded_runs"] = runs(deg)
    res["summary_agrees"] = (d["summary"]["blocks_at_floor"] == len(at) and
                             d["summary"].get("degraded_event_free_blocks", deg) == deg)
    return res, deg, B


res = {}
g, deg, B = grade("b0-2")
a = json.loads((pk / "summary/b0-2/align-a-c.json").read_text())
b = json.loads((pk / "summary/b0-2/align-b-c.json").read_text())
cover = min(a["covered_recording_frames"][1], b["covered_recording_frames"][1])
whole = cover // FS  # blocks 0 .. whole-1 lie wholly inside
inside = [x for x in deg if x < whole]
beyond = [x for x in deg if x >= whole]
g.update(overlap_frames_a=a["compared_equal"], overlap_frames_b=b["compared_equal"],
         overlap_s=round(a["covered_recording_frames"][1] / FS, 2), whole_blocks=[0, whole - 1],
         inside=len(inside), inside_runs=runs(inside), beyond=len(beyond), beyond_runs=runs(beyond),
         beyond_run_count=len(runs(beyond)),
         worst_inside={ch: max(((blk[ch]["thdn_db"], blk["block"]) for blk in B if blk["block"] in inside)) for ch in ("ch0", "ch1")},
         worst_beyond={ch: max(((blk[ch]["thdn_db"], blk["block"]) for blk in B if blk["block"] in beyond)) for ch in ("ch0", "ch1")},
         a_diff_slips=[a["frames_differing"], len(a["slips"]), b["frames_differing"], len(b["slips"])])
res["b0-2"] = g
for run in ("bcrf", "baaf"):
    res[run], _, _ = grade(run)
    al = {p: json.loads((pk / f"summary/{run}/align-{p}-c.json").read_text()) for p in "ab"}
    res[run]["align"] = {p: [al[p]["compared_equal"], round(al[p]["covered_recording_frames"][1] / FS, 2),
                             al[p]["frames_differing"], len(al[p]["slips"]), al[p]["verdict"]] for p in "ab"}
tot_a = sum(json.loads((pk / f"summary/{r}/align-a-c.json").read_text())["compared_equal"] for r in ("pts1", "pts2", "pts3", "b0-2"))
tot_b = 3 * 480000 + b["compared_equal"]
res["b16b_totals_vs_a_b"] = [tot_a, tot_b]
res["b16c_totals_vs_a_b"] = [res["bcrf"]["align"]["a"][0] + res["baaf"]["align"]["a"][0],
                             res["bcrf"]["align"]["b"][0] + res["baaf"]["align"]["b"][0]]
out.write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res, indent=1))
