#!/usr/bin/env python3
"""Reviewer probe (R392-2): count the INTERNAL-source beat crossings in the
DOUT 70 s S32_LE capture and say which cluster each one falls in.

Independent of any author tool. Clusters use the page's rule (discontinuities
closer than 50 ms, 2,400 frames, are one cluster). A "pure beat" cluster is a
short one (span <= 100 frames) that nets exactly one dropped frame. The beat
line p0 + k*T is fitted to the pure-beat clusters, every crossing of that line
inside the capture's own-tag region is enumerated, and each crossing is
assigned to the cluster whose extent (+/- 100 frames) contains it.

Usage: r392_2_dout_crossings.py dout-long.raw [author-attribution.json]
Frame numbers are recording frames (first frame of a cluster = the frame
after the first discontinuity), the page's convention.
"""
import json, sys
import numpy as np

GAP = 2400
w = np.fromfile(sys.argv[1], dtype="<u4").reshape(-1, 8)
a = 2048  # first DMA period is all zero, excluded as on the page
ordv = ((w[a:, 0] >> 8) & 0xFFFF).astype(np.int64)
d = (ordv[1:] - ordv[:-1]) % 65536
ev = np.nonzero(d != 1)[0]
cl = []
if ev.size:
    groups = np.split(ev, np.nonzero(np.diff(ev) > GAP)[0] + 1)
    for g in groups:
        dd = d[g]
        rep = int(np.sum(dd == 0))
        drop = int(np.sum(dd[dd != 0] - 1))
        cl.append({"first": int(g[0]) + a + 1, "last": int(g[-1]) + a + 1,
                   "repeated": rep, "dropped": drop})
short = [c for c in cl if c["last"] - c["first"] <= 100 and c["dropped"] - c["repeated"] == 1]
# Seed the line at the first short net-one-drop cluster with the nominal
# 93,990-frame beat, keep clusters within 60 frames of it, refit, repeat.
p0, T = float(short[0]["first"]), 93990.0
for _ in range(4):
    pure = [c for c in short if abs((c["first"] - p0) / T - round((c["first"] - p0) / T)) * T <= 60]
    x = np.array([c["first"] for c in pure], dtype=np.float64)
    k = np.round((x - p0) / T)
    T, p0 = np.polyfit(k, x, 1)
lo, hi = a, w.shape[0] - 1
kmin = int(np.ceil((lo - p0) / T)); kmax = int(np.floor((hi - p0) / T))
cross = []
for kk in range(kmin, kmax + 1):
    p = p0 + kk * T
    home = [i for i, c in enumerate(cl) if c["first"] - 100 <= p <= c["last"] + 100]
    cross.append({"k": kk, "predicted_frame": round(float(p)), "cluster": home[0] if home else None})
in_pure = [c for c in cross if c["cluster"] is not None and cl[c["cluster"]] in pure]
in_other = [c for c in cross if c["cluster"] is not None and cl[c["cluster"]] not in pure]
missing = [c for c in cross if c["cluster"] is None]
out = {
    "frames": int(w.shape[0]), "clusters": len(cl),
    "total_repeated": sum(c["repeated"] for c in cl), "total_dropped": sum(c["dropped"] for c in cl),
    "pure_beat_clusters": len(pure),
    "pure_beat_repeated": sum(c["repeated"] for c in pure),
    "pure_beat_dropped": sum(c["dropped"] for c in pure),
    "pure_beat_spacing_range": [int(v) for v in (np.diff(x).min(), np.diff(x).max())] if len(x) > 1 else [],
    "fitted_period_frames": round(float(T), 3), "fitted_p0": round(float(p0), 1),
    "crossings_in_capture": len(cross),
    "crossings_in_pure_beat_clusters": len(in_pure),
    "crossings_in_other_clusters": [{**c, "cluster_first": cl[c["cluster"]]["first"],
                                     "cluster_last": cl[c["cluster"]]["last"],
                                     "cluster_repeated": cl[c["cluster"]]["repeated"],
                                     "cluster_dropped": cl[c["cluster"]]["dropped"]} for c in in_other],
    "crossings_without_cluster": missing,
}
if len(sys.argv) > 2:
    att = json.load(open(sys.argv[2]))
    kind = {c["first_frame"]: c["kind"] for c in att["clusters"]}
    out["author_kind_of_other_crossing_clusters"] = {str(c["cluster_first"]): kind.get(c["cluster_first"]) for c in out["crossings_in_other_clusters"]}
    out["author_kind_of_pure_beat_clusters"] = sorted(set(kind.get(c["first"]) for c in pure))
    rows = {}
    for c in att["clusters"]:
        r = rows.setdefault(c["kind"], [0, 0, 0]); r[0] += 1; r[1] += c["repeats"]; r[2] += c["skips"]
    out["author_rows"] = rows
    per = {}
    for c in cl:
        r = per.setdefault(kind.get(c["first"]), [0, 0, 0]); r[0] += 1; r[1] += c["repeated"]; r[2] += c["dropped"]
    out["reviewer_rows_by_author_kind"] = per
    out["short_net_one_drop_clusters_off_the_line"] = [c["first"] for c in short if c not in pure]
    out["cluster_firsts_agree_with_author"] = sorted(kind) == sorted(c["first"] for c in cl)
json.dump(out, sys.stdout, indent=1); print()
