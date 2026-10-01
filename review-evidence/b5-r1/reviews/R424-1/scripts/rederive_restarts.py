#!/usr/bin/env python3
"""Re-derive the restart distribution, growth fit and per-cycle rows from summary.json.
usage: rederive_restarts.py <author dir>"""
import json, statistics, sys, math
from pathlib import Path
A = Path(sys.argv[1])
s = json.load(open(A / "summary/a-long/summary.json"))
cy = s["cycles"]
print("cycles", len(cy), "initial restart_s", s["initial_bind"]["restart_s"],
      "initial frames before first valid", s["initial_bind"]["frames_before_first_valid"])
rs = [c["restart_s"] for c in cy]
dem = [c for c in cy if c["demonstrated_restart"]]
print("demonstrated", len(dem), "below 1 s", sum(c["restart_s"] < 1 for c in dem),
      "all stopped", all(c["stopped"] for c in cy), "valid in hold", sum(c["valid_frames_in_hold"] for c in cy),
      "statuses", {c["status"] for c in cy} | {c["unbind_status"] for c in cy})
srt = sorted(rs)
p95 = srt[math.ceil(0.95 * len(srt)) - 1]
print("min %.4f median %.4f p95 %.4f max %.4f" % (srt[0], statistics.median(rs), p95, srt[-1]))
lv = [c["last_valid_after_unbind_s"] for c in cy]
print("last valid after unbind min/max %.4f %.4f" % (min(lv), max(lv)))
print("hold min/max %.3f %.3f" % (min(c["hold_s"] for c in cy), max(c["hold_s"] for c in cy)))
print("cmd_to_response ms min/max", min(c["cmd_to_response_ms"] for c in cy), max(c["cmd_to_response_ms"] for c in cy))
fc = [c["restart_from_command_s"] for c in cy]
print("from command min/max %.4f %.4f" % (min(fc), max(fc)))
print("non-zero frames before first valid in any cycle:", [(c["cycle"], c["frames_before_first_valid"]) for c in cy
      if c["frames_before_first_valid"]["valid"] or c["frames_before_first_valid"]["other"]])
print("stalls in restart:", [(c["cycle"], c["capture_stalls_bind_to_first_valid"]) for c in cy if c["capture_stalls_bind_to_first_valid"]])
x = [c["cycle"] for c in cy]; n = len(x); mx = sum(x) / n; my = sum(rs) / n
sxx = sum((a - mx) ** 2 for a in x); b = sum((a - mx) * (r - my) for a, r in zip(x, rs)) / sxx
a0 = my - b * mx; ssr = sum((r - (a0 + b * a)) ** 2 for a, r in zip(x, rs)); se = math.sqrt(ssr / (n - 2) / sxx)
t = 2.048407  # Student t, 0.975, df 28
print("slope %+.6f CI [%+.6f, %+.6f] df %d; first ten median %.4f last ten median %.4f" %
      (b, b - t * se, b + t * se, n - 2, statistics.median(rs[:10]), statistics.median(rs[-10:])))
# excluding cycle 1 (after the 660 s window)
x2, r2 = x[1:], rs[1:]; n2 = len(x2); mx2 = sum(x2) / n2; my2 = sum(r2) / n2
sxx2 = sum((a - mx2) ** 2 for a in x2); b2 = sum((a - mx2) * (r - my2) for a, r in zip(x2, r2)) / sxx2
a2 = my2 - b2 * mx2; ssr2 = sum((r - (a2 + b2 * a)) ** 2 for a, r in zip(x2, r2)); se2 = math.sqrt(ssr2 / (n2 - 2) / sxx2)
t2 = 2.051831  # df 27
print("cycles 2-30 slope %+.6f CI [%+.6f, %+.6f]" % (b2, b2 - t2 * se2, b2 + t2 * se2))
rows = {int(l.split("|")[1]): [v.strip() for v in l.split("|")[2:-1]] for l in
        open(sys.argv[2]).read().splitlines() if l.startswith("| ") and l.split("|")[1].strip().isdigit()}
mism = 0
for c in cy:
    st = "yes, %s ms" % "/".join(f"{v:.1f}" for v in c["capture_stalls_bind_to_first_valid"]) if c["capture_stalls_bind_to_first_valid"] else "no"
    mine = [f"{c['hold_s']:.3f}", "yes" if c["stopped"] else "no", f"{c['last_valid_after_unbind_s']:.4f}",
            f"{c['restart_s']:.4f}", f"{c['restart_from_command_s']:.4f}", st, "PASS" if c["pass_1s"] else "FAIL"]
    if rows.get(c["cycle"]) != mine: mism += 1; print("ROW MISMATCH", c["cycle"], rows.get(c["cycle"]), mine)
print("page cycle rows compared:", len(rows), "mismatches", mism)
