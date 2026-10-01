#!/usr/bin/env python3
"""Re-derive fs and the page's ppm decomposition from the capture status log.

usage: rederive_fs.py <soc-capture.log>
"""
import re, sys, json
txt = open(sys.argv[1]).read()
samples = []
for blk in re.split(r"\nU ", txt)[1:]:
    up = float(blk.split()[0])
    st = re.search(r"state: (\S+)", blk)
    ts = re.search(r"tstamp\s*:\s*([\d.]+)", blk)
    hp = re.search(r"hw_ptr\s*:\s*(\d+)", blk)
    tr = re.search(r"trigger_time:\s*([\d.]+)", blk)
    if st and st.group(1) == "RUNNING" and ts and hp:
        samples.append((up, float(ts.group(1)), int(hp.group(1)), tr.group(1)))
n = len(samples)
t = [s[1] for s in samples]; h = [s[2] for s in samples]
fs_ends = (h[-1] - h[0]) / (t[-1] - t[0])
mt, mh = sum(t) / n, sum(h) / n
fs_ls = sum((a - mt) * (b - mh) for a, b in zip(t, h)) / sum((a - mt) ** 2 for a in t)
plan = 24_575_738.53 / 2 / 256
fs_up = (h[-1] - h[0]) / (samples[-1][0] - samples[0][0])
res = dict(
    running_samples=n, triggers=sorted(set(s[3] for s in samples)),
    window_s=round(t[-1] - t[0], 3), frames_in_window=h[-1] - h[0],
    fs_first_last_hz=round(fs_ends, 4), fs_least_squares_hz=round(fs_ls, 4),
    plan_hz=round(plan, 4), plan_vs_48k_ppm=round((plan / 48000 - 1) * 1e6, 3),
    fs_vs_48k_ppm=round((fs_ends / 48000 - 1) * 1e6, 3),
    fs_vs_plan_ppm=round((fs_ends / plan - 1) * 1e6, 3),
    sum_plan_plus_relative_ppm=round((plan / 48000 - 1) * 1e6 + (fs_ends / plan - 1) * 1e6, 3),
    bclk_256fs_hz=round(256 * fs_ends, 1),
    fs_uptime_hz=round(fs_up, 3),
    endpoint_step_ppm=round(2 * 4 / (t[-1] - t[0]) / fs_ends * 1e6, 3),
    recording_630s_bytes=630 * 48000 * 32, recording_600s_bytes=600 * 48000 * 32,
    raw_bytes_frames=730_595_328 // 32, raw_seconds=730_595_328 / 32 / 48000,
    slip_tdm_ppm=round(395 / 774.3 / 48000 * 1e6, 3),
)
print(json.dumps(res, indent=1))
