#!/usr/bin/env python3
"""Independent re-derivation of fs from the SoC board's PCM status samples.

usage: recompute_fs.py <soc-capture.log>

Parses every status block (state, trigger_time, tstamp, hw_ptr, avail_max)
and the 'U <uptime>' line before it, keeps the RUNNING samples, and derives
fs by endpoints and by least squares, the residuals, the hw_ptr step GCD and
the uptime cross-check. Prints one JSON object.
"""
import json
import math
import re
import sys
from functools import reduce

PLAN = 24575738.53 / 2 / 256


def parse(path):
    samples, cur, up = [], None, None
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"^U (\d+\.\d+) ", line)
        if m:
            up = float(m.group(1))
            continue
        m = re.match(r"^(state|trigger_time|tstamp|hw_ptr|appl_ptr|avail|avail_max)\s*:\s*(\S+)", line)
        if not m:
            continue
        k, v = m.groups()
        if k == "state":
            cur = {"state": v, "uptime": up}
            samples.append(cur)
        elif cur is not None:
            cur[k] = v
    return samples


def main():
    s = parse(sys.argv[1])
    run = [x for x in s if x["state"] == "RUNNING"]
    trig = sorted({x["trigger_time"] for x in run})
    t = [float(x["tstamp"]) for x in run]
    n = [int(x["hw_ptr"]) for x in run]
    T, N = t[-1] - t[0], n[-1] - n[0]
    fs_end = N / T
    tm, nm = sum(t) / len(t), sum(n) / len(n)
    sxx = sum((a - tm) ** 2 for a in t)
    fs_ls = sum((a - tm) * (b - nm) for a, b in zip(t, n)) / sxx
    icpt = nm - fs_ls * tm
    res = [b - (icpt + fs_ls * a) for a, b in zip(t, n)]
    rms = math.sqrt(sum(r * r for r in res) / len(res))
    steps = [b - a for a, b in zip(n, n[1:])]
    g = reduce(math.gcd, [n[0]] + steps)
    up = [x["uptime"] for x in run]
    fs_up = N / (up[-1] - up[0])
    out = dict(
        status_blocks=len(s), running=len(run), states=sorted({x["state"] for x in s}),
        running_triggers=trig, max_avail_max_running=max(int(x["avail_max"]) for x in run),
        first=dict(tstamp=t[0], hw_ptr=n[0]), last=dict(tstamp=t[-1], hw_ptr=n[-1]),
        span_s=round(T, 8), span_frames=N, fs_endpoints=round(fs_end, 4), fs_lsq=round(fs_ls, 4),
        ppm_vs_48k_endpoints=round((fs_end / 48000 - 1) * 1e6, 3),
        ppm_vs_48k_lsq=round((fs_ls / 48000 - 1) * 1e6, 3),
        plan_fs=round(PLAN, 4), plan_ppm_vs_48k=round((PLAN / 48000 - 1) * 1e6, 3),
        ppm_vs_plan_endpoints=round((fs_end / PLAN - 1) * 1e6, 3),
        bclk_256fs=round(256 * fs_end, 1),
        residual_rms_frames=round(rms, 3), residual_rms_us=round(rms / fs_ls * 1e6, 2),
        residual_max_abs_frames=round(max(abs(r) for r in res), 3),
        residual_max_abs_us=round(max(abs(r) for r in res) / fs_ls * 1e6, 2),
        residual_first=round(res[0], 2), residual_last=round(res[-1], 2),
        endpoint_unc_hz=round((abs(res[0]) + abs(res[-1])) / T, 4),
        endpoint_unc_ppm=round((abs(res[0]) + abs(res[-1])) / T / fs_end * 1e6, 3),
        one_step_each_end_hz=round(2 * g / T, 4), one_step_each_end_ppm=round(2 * g / T / fs_end * 1e6, 3),
        hw_ptr_gcd=g, fs_uptime=round(fs_up, 3), uptime_span=round(up[-1] - up[0], 2),
        uptime_res_ppm=round(0.02 / (up[-1] - up[0]) * 1e6, 1),
        last_sample_after_trigger_s=round(t[-1] - float(trig[0]), 4),
        first_sample_after_trigger_s=round(t[0] - float(trig[0]), 4),
        xrun_triggers=sorted({x["trigger_time"] for x in s if x["state"] == "XRUN"}),
        xrun_hw_ptr=sorted({x.get("hw_ptr") for x in s if x["state"] == "XRUN"}),
        xrun_appl_ptr=sorted({x.get("appl_ptr") for x in s if x["state"] == "XRUN"}),
    )
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
