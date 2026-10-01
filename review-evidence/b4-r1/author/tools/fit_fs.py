#!/usr/bin/env python3
"""Frame rate of the McASP0 capture against the SoC board's CLOCK_MONOTONIC
(offline, no bench access).

usage: fit_fs.py <soc-capture.log> <capture.raw size in bytes> [<json_out>]

Reads the status samples that run_timing.py prints while arecord records:
/proc/asound/card0/pcm0c/sub0/status with tstamp_mode ENABLE and tstamp_type
MONOTONIC, so `tstamp` is the CLOCK_MONOTONIC time at which the kernel last
moved `hw_ptr`, the count of frames the receiver has written since the
trigger. Only RUNNING samples of the capture's own trigger are used.

It reports:
- fs from the first and last sample (frames between them over the time
  between them), and a least-squares line through all samples;
- the residuals of every sample from that line, in frames and microseconds,
  which bound the timing granularity (the pointer step plus the latency from
  the pointer moving to its timestamp);
- the pointer step seen (greatest common divisor of the hw_ptr deltas);
- the endpoint uncertainty, (|r_first| + |r_last|) / span, from the
  residuals, and a worst case of one pointer step at each end;
- a coarse cross-check from /proc/uptime (10 ms resolution) at each sample;
- BCLK = 256 x fs, which assumes the master's frame of eight 32-bit slots.
The SoC board's crystal tolerance is not measured here and is not included.
"""
import json
import math
import re
import sys
from functools import reduce


def main():
    log, nbytes = sys.argv[1], int(sys.argv[2])
    txt = open(log, "rb").read().decode("latin-1").replace("\r", "")
    blocks = re.split(r"\nU (\d+\.\d+) \d+\.\d+\n", txt)
    samples = []
    for i in range(1, len(blocks) - 1, 2):
        up, b = float(blocks[i]), blocks[i + 1]
        st = re.search(r"state: (\w+)", b)
        if not st or st.group(1) != "RUNNING":
            continue
        g = {k: re.search(k + r"\s*: (\S+)", b) for k in ("trigger_time", "tstamp", "hw_ptr", "appl_ptr", "avail", "avail_max")}
        if any(v is None for v in g.values()):
            continue
        samples.append(dict(uptime=up, trigger=g["trigger_time"].group(1), tstamp=float(g["tstamp"].group(1)),
                            hw_ptr=int(g["hw_ptr"].group(1)), appl_ptr=int(g["appl_ptr"].group(1)),
                            avail=int(g["avail"].group(1)), avail_max=int(g["avail_max"].group(1))))
    triggers = sorted({s["trigger"] for s in samples})
    trig = samples[0]["trigger"]
    samples = [s for s in samples if s["trigger"] == trig]
    n = len(samples)
    t = [s["tstamp"] for s in samples]
    h = [s["hw_ptr"] for s in samples]
    span_t, span_f = t[-1] - t[0], h[-1] - h[0]
    fs_end = span_f / span_t
    tm, hm = sum(t) / n, sum(h) / n
    sxx = sum((x - tm) ** 2 for x in t)
    fs_fit = sum((x - tm) * (y - hm) for x, y in zip(t, h)) / sxx
    a = hm - fs_fit * tm
    res = [y - (a + fs_fit * x) for x, y in zip(t, h)]
    deltas = [y - x for x, y in zip(h, h[1:])]
    step = reduce(math.gcd, deltas)
    rms = math.sqrt(sum(r * r for r in res) / n)
    se_fit = math.sqrt(sum(r * r for r in res) / (n - 2) / sxx)
    end_unc = (abs(res[0]) + abs(res[-1])) / span_t
    step_unc = 2 * step / span_t
    up_span = samples[-1]["uptime"] - samples[0]["uptime"]
    fs_up = span_f / up_span
    out = dict(
        log=log.split("/")[-1], capture_bytes=nbytes, capture_frames=nbytes // 32,
        capture_seconds_at_48k=nbytes / 32 / 48000, samples=n, triggers_seen=len(triggers), trigger_time=trig,
        first=samples[0], last=samples[-1], span_s=round(span_t, 9), span_frames=span_f,
        fs_endpoints_hz=round(fs_end, 4), fs_fit_hz=round(fs_fit, 4), fs_fit_std_error_hz=round(se_fit, 5),
        ppm_vs_48k_endpoints=round((fs_end / 48000 - 1) * 1e6, 3), ppm_vs_48k_fit=round((fs_fit / 48000 - 1) * 1e6, 3),
        ppm_vs_plan_47999_4893_endpoints=round((fs_end / 47999.4893 - 1) * 1e6, 3),
        residual_rms_frames=round(rms, 3), residual_max_abs_frames=round(max(abs(r) for r in res), 3),
        residual_rms_us=round(rms / fs_fit * 1e6, 2), residual_max_abs_us=round(max(abs(r) for r in res) / fs_fit * 1e6, 2),
        hw_ptr_step_gcd_frames=step,
        endpoint_uncertainty_hz=round(end_unc, 4), endpoint_uncertainty_ppm=round(end_unc / fs_end * 1e6, 3),
        one_step_each_end_uncertainty_hz=round(step_unc, 4), one_step_each_end_ppm=round(step_unc / fs_end * 1e6, 3),
        fs_uptime_crosscheck_hz=round(fs_up, 3), uptime_span_s=round(up_span, 2),
        bclk_hz_endpoints=round(256 * fs_end, 1), bclk_hz_fit=round(256 * fs_fit, 1),
        avail_max_frames=max(s["avail_max"] for s in samples),
        residuals_frames=[round(r, 2) for r in res])
    s = json.dumps(out, indent=1)
    print(s)
    if len(sys.argv) > 3:
        open(sys.argv[3], "w").write(s + "\n")


if __name__ == "__main__":
    main()
