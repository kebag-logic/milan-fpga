#!/usr/bin/env python3
"""Re-derive the restart distribution and growth from summary/a-long/summary.json cycles.
usage: rederive_restarts.py <packet author dir>"""
import json, sys, math, statistics as st
s = json.load(open(sys.argv[1] + "/summary/a-long/summary.json"))
cy = s["cycles"]
print("cycles", len(cy), "statuses", {c["status"] for c in cy}, "unbind statuses", {c["unbind_status"] for c in cy})
print("all stopped", all(c["stopped"] for c in cy), "valid in hold", sum(c["valid_frames_in_hold"] for c in cy),
      "flowing before", all(c["flowing_before"] for c in cy))
rs = [c["restart_s"] for c in cy]
srt = sorted(rs)
p95 = srt[math.ceil(0.95 * len(srt)) - 1]
print(f"restart n {len(rs)} below1 {sum(r < 1 for r in rs)} min {min(rs):.4f} median {st.median(rs):.4f} p95 {p95:.4f} max {max(rs):.4f}")
print("max cycle", rs.index(max(rs)) + 1)
x = [c["cycle"] for c in cy]
mx, my = st.mean(x), st.mean(rs)
sxx = sum((a - mx) ** 2 for a in x)
b = sum((a - mx) * (r - my) for a, r in zip(x, rs)) / sxx
a0 = my - b * mx
ssr = sum((r - a0 - b * a) ** 2 for a, r in zip(x, rs))
se = math.sqrt(ssr / (len(x) - 2) / sxx)
t = 2.0484  # Student t 0.975, 28 df
print(f"slope {b:+.6f} ci95 [{b - t*se:+.6f}, {b + t*se:+.6f}] df {len(x)-2}; first10 median {st.median(rs[:10]):.4f} last10 {st.median(rs[-10:]):.4f}")
lv = [c["last_valid_after_unbind_s"] for c in cy]
print(f"last valid after unbind {min(lv)*1e3:.1f} to {max(lv)*1e3:.1f} ms")
cr = [c["cmd_to_response_ms"] for c in cy]
print(f"cmd to response {min(cr):.3f} to {max(cr):.3f} ms; from command {min(c['restart_from_command_s'] for c in cy)*1e3:.1f} to {max(c['restart_from_command_s'] for c in cy)*1e3:.1f} ms")
print("holds", min(c["hold_s"] for c in cy), max(c["hold_s"] for c in cy))
print("stalls in restart", [(c["cycle"], c["capture_stalls_bind_to_first_valid"]) for c in cy if c["capture_stalls_bind_to_first_valid"]])
print("frames before first valid non-zero", [(c["cycle"], c["frames_before_first_valid"]) for c in cy if c["frames_before_first_valid"]["valid"] or c["frames_before_first_valid"]["other"]])
print("after_3s", {k: sum(c["after_3s"][k] for c in cy) for k in cy[0]["after_3s"]})
print("offset unc ms max", max(c["offset_unc_ms"] for c in cy))
ib = s["initial_bind"]
print("initial", ib["restart_s"], ib["frames_before_first_valid"], ib["cmd_to_response_ms"])
# hold silent: time between unbind and the first valid frame of the next bind exceeds the hold
