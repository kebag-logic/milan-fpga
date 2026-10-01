#!/usr/bin/env python3
"""Re-derive the page's derived numbers and timeline conversions from packet values."""
from datetime import datetime, timezone
fs = 22677480 / 472.46770409
plan = 24575738.53 / 2 / 256
ts = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%H:%M:%S.%f")[:-3] + "Z"
first, last = 1790828225.206684, 1790828700.8204749
trig, wake, xrun, lastsamp = 68038.252028915, 68513.969698, 68514.389804905, 68513.73166509
r = {
    "fs_endpoints": fs, "bclk_256fs": 256 * fs, "plan_fs": plan, "plan_ppm": (plan / 48000 - 1) * 1e6,
    "ppm_48k": (fs / 48000 - 1) * 1e6, "ppm_plan": (fs / plan - 1) * 1e6,
    "frames_x32_bytes": 22831104 * 32, "seconds_at_48k": 22831104 / 48000,
    "frames_x32_rate_MBps": 48000 * 32 / 1e6, "full_630s_MB": 630 * 48000 * 32 / 1e6,
    "first_bytes_utc": ts(first), "last_bytes_utc": ts(last),
    "wake_after_trigger_s": wake - trig, "wake_mapped_utc": ts(first + (wake - trig)),
    "xrun_after_wake_s": xrun - wake, "lastsample_before_wake_s": wake - lastsamp,
    "lastsample_after_trigger_s": lastsamp - trig,
    "slip_tdm_ppm_395_in_774.27s": 395 / 774.27 / plan * 1e6, "slip_tdm_per_s": 395 / 774.27,
    "last_residual_vs_rms": (1.17, 1.234),
}
for k, v in r.items():
    print(f"{k}: {v}")
