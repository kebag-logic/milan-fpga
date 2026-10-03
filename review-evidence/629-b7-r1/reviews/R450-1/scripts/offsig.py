#!/usr/bin/env python3
"""For every capture-path cluster in the six B7 windows: lost duration, the expected number of
one-frame-short capture packets inside it at the case's measured capture deficit, and whether
its net step is off the 48 n + 12 signature. Usage: offsig.py <packet-author-dir>"""
import json, math, sys
ROOT = sys.argv[1]
tot_exp = 0.0
tot_obs = 0
for c in ["a0", "a1", "a2", "b0", "bcrf", "baaf"]:
    g = json.load(open(f"{ROOT}/summary/{c}/grade.json"))
    deficit = 48000 - g["frame_rate_ratio"]["external_capture"]["rate"]
    w0 = g["window"]["start_frame"]
    exp_c = 0.0
    rows = []
    for k in g["skip_clusters"]:
        steps = k["steps"]
        off = ((sum(steps) - 12 * len(steps) + 24) % 48) - 24
        lost_s = k["lost_frames"] / 48000
        lam = deficit * lost_s
        exp_c += lam
        if off:
            p_ge = 1 - sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(abs(off)))
            rows.append(dict(cluster=k["cluster"], at_s=round((k["first_frame"] - w0) / 48000, 1), lost_frames=k["lost_frames"],
                             lost_ms=round(lost_s * 1000, 1), frames_off=off, expected_short=round(lam, 4),
                             p_at_least_that_many_short=round(p_ge, 4)))
    obs = sum(-r["frames_off"] for r in rows if r["frames_off"] < 0)
    if c != "a0":
        tot_exp += exp_c
        tot_obs += obs
    print(json.dumps(dict(case=c, deficit_fps=round(deficit, 3), clusters=len(g["skip_clusters"]),
                          lost_s=round(sum(k["lost_frames"] for k in g["skip_clusters"]) / 48000, 3),
                          expected_short_frames_all_clusters=round(exp_c, 2), observed_short_frames=obs, off_clusters=rows)))
print(json.dumps(dict(non_control_expected_short=round(tot_exp, 2), non_control_observed_short=tot_obs)))
