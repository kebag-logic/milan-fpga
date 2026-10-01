#!/usr/bin/env python3
"""Independent re-derivation of the #451 SoC-board fs figures from the public
packet's soc-capture.log (review-evidence/b4-r1/author/runs/timing-long/).

usage: rederive_fs.py <soc-capture.log>

Parses every 'state:' status block itself (does not reuse the packet's tool),
keeps the full sample list including non-RUNNING blocks, and reports the
figures the findings page states.
"""
import json
import math
import re
import sys

PLAN_AUDIO_HZ = 24_575_738.529   # docs/litex/CLOCK_DOMAINS.md Plan A
PLAN_FS = PLAN_AUDIO_HZ / 2 / 256


def main():
    txt = open(sys.argv[1], "rb").read().decode("latin-1").replace("\r", "")
    lines = txt.split("\n")
    blocks, cur = [], None
    for ln in lines:
        m = re.match(r"^U (\d+\.\d+) (\d+\.\d+)$", ln)
        if m:
            cur = {"uptime": float(m.group(1))}
            blocks.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^(state|trigger_time|tstamp|hw_ptr|appl_ptr|avail|avail_max|delay)\s*:\s*(\S+)", ln)
        if m:
            cur[m.group(1)] = m.group(2)
    states = {}
    for b in blocks:
        states[b.get("state")] = states.get(b.get("state"), 0) + 1
    run = [b for b in blocks if b.get("state") == "RUNNING"]
    trig = {b["trigger_time"] for b in run}
    t = [float(b["tstamp"]) for b in run]
    h = [int(b["hw_ptr"]) for b in run]
    n = len(run)
    fs_end = (h[-1] - h[0]) / (t[-1] - t[0])
    tm, hm = sum(t) / n, sum(h) / n
    sxx = sum((x - tm) ** 2 for x in t)
    fs_fit = sum((x - tm) * (y - hm) for x, y in zip(t, h)) / sxx
    a = hm - fs_fit * tm
    res = [y - (a + fs_fit * x) for x, y in zip(t, h)]
    rms = math.sqrt(sum(r * r for r in res) / n)
    steps = sorted({(y - x) % 4 for x, y in zip(h, h[1:])})
    g = 0
    for x, y in zip(h, h[1:]):
        g = math.gcd(g, y - x)
    hp_mod4 = sorted({x % 4 for x in h})
    span = t[-1] - t[0]
    up_span = run[-1]["uptime"] - run[0]["uptime"]
    trig_t = float(next(iter(trig)))
    out = dict(
        status_blocks=len(blocks), states=states, running=n, triggers=sorted(trig),
        first_tstamp=t[0], last_tstamp=t[-1], last_minus_trigger_s=round(t[-1] - trig_t, 3),
        span_s=round(span, 6), span_frames=h[-1] - h[0],
        fs_endpoints=round(fs_end, 4), fs_fit=round(fs_fit, 4),
        ppm_48k=round((fs_end / 48000 - 1) * 1e6, 3),
        plan_fs=round(PLAN_FS, 4), plan_ppm_48k=round((PLAN_FS / 48000 - 1) * 1e6, 3),
        ppm_vs_plan=round((fs_end / PLAN_FS - 1) * 1e6, 3),
        bclk_256fs=round(256 * fs_end, 1),
        residual_first=round(res[0], 3), residual_last=round(res[-1], 3),
        residual_rms_frames=round(rms, 3), residual_max_frames=round(max(map(abs, res)), 3),
        residual_rms_us=round(rms / fs_fit * 1e6, 2), residual_max_us=round(max(map(abs, res)) / fs_fit * 1e6, 2),
        hw_ptr_delta_gcd=g, hw_ptr_mod4=hp_mod4,
        endpoint_unc_ppm=round((abs(res[0]) + abs(res[-1])) / span / fs_end * 1e6, 3),
        step_each_end_ppm=round(2 * g / span / fs_end * 1e6, 3),
        two_max_residual_ppm=round(2 * max(map(abs, res)) / span / fs_end * 1e6, 3),
        uptime_fs=round((h[-1] - h[0]) / up_span, 3), uptime_unc_ppm=round(0.02 / up_span * 1e6, 1),
        avail_max_max=max(int(b["avail_max"]) for b in run),
        sample_spacing_s=[round(min(y - x for x, y in zip(t, t[1:])), 3), round(max(y - x for x, y in zip(t, t[1:])), 3)],
    )
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
