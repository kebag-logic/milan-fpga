#!/usr/bin/env python3
"""Reviewer-side re-derivation of the PR #628 round 2 attribution figures.

usage: rederive.py <round1_author_dir> <read_record.u16>

Written independently of the author's b5_attrib.py. Inputs are the round 1
packet's summary/a-long/summary.json and continuity-events.csv and a window
read record (uint16 LE microsecond gaps). Prints every figure the page's
Continuity section and Limits state, then a background comparison for the
delivery steps found at the 2-to-59-frame clusters away from stalls.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

FS, PER, STALL_MS = 48000, 480, 15.0


def floor_step(D, a, b, R, w=10, gb=3, ga=2):
    lo, hi = a - gb - w, b + ga + w
    if lo < 0 or hi > R:
        return None
    return float(D[b + ga:hi + 1].min() - D[lo:a - gb + 1].min())


def main(pkt, rec):
    pkt = Path(pkt)
    s = json.load(open(pkt / "summary/a-long/summary.json"))["continuity"]
    c0, c1 = s["window"]
    gap = np.fromfile(rec, dtype="<u2").astype(np.int64)
    R = len(gap)
    assert c1 - c0 == PER * R
    t = np.concatenate(([0], np.cumsum(gap))) / 1e6
    D = t * FS - PER * np.arange(R + 1)
    gms = np.concatenate(([np.nan], gap / 1000.0))
    ev = []
    for row in csv.DictReader(open(pkt / "summary/a-long/continuity-events.csv")):
        k = int(row["frame"])
        ev.append(dict(k=k, kind=row["kind"], step=int(row["step"]), n=int(row["frames"]),
                       r=(k - c0) // PER + 1))
    out = []
    p = out.append
    p(f"record gaps {R}, sum {gap.sum()} us")
    wt = s["window_time"][1] - s["window_time"][0]
    p(f"count drift from window_time: {wt * FS - (c1 - c0):.1f} frames")
    stalls = np.flatnonzero(gms[1:] > STALL_MS) + 1
    sp = np.diff(t[stalls])
    p(f"stalls {len(stalls)}; spacing median {np.median(sp):.3f} s min {sp.min():.3f} max {sp.max():.3f}")
    exc = ((gms[stalls] - 10.0) * FS / 1000).sum()
    p(f"stall excess {exc:.1f} frames")
    sk = [e for e in ev if e["kind"] == "skip"]
    ge60 = [e for e in sk if e["n"] >= 60]
    sset = set(stalls.tolist())
    after = lambda e, offs: any((e["r"] - o) in sset for o in offs)
    p(f"skips >=60: {len(ge60)}, {sum(e['n'] for e in ge60)} frames; 1-2 reads after a stall: "
      f"{sum(after(e, (1, 2)) for e in ge60)}; 0 reads after: {sum(after(e, (0,)) for e in ge60)}")
    ge240 = [e for e in sk if e["n"] >= 240]
    per = {}
    for st in stalls:
        per[int(st)] = sum(1 for e in ge240 if 1 <= e["r"] - st <= 2)
    p(f"stalls with exactly one >=240 skip 1-2 reads after: {sum(v == 1 for v in per.values())} of {len(per)}")
    for e in ge60:
        if not after(e, (0, 1, 2)):
            p(f"  unaligned skip {e['n']}: longest interval {np.nanmax(gms[max(1, e['r'] - 2):e['r'] + 1]):.2f} ms")
    small = [e for e in sk if 2 <= e["n"] < 60]
    p(f"skips 2-59: {len(small)}, {sum(e['n'] for e in small)} frames; multiples of 6 "
      f"{sum(e['n'] % 6 == 0 for e in small)}; exactly 6 {sum(e['n'] == 6 for e in small)}")
    multi = sorted([e for e in sk if e["n"] >= 2], key=lambda e: e["r"])
    cl = []
    for e in multi:
        if cl and e["r"] - cl[-1][-1]["r"] < 16:
            cl[-1].append(e)
        else:
            cl.append([e])
    A, B = [], []
    for c in cl:
        a, b = c[0]["r"], c[-1]["r"]
        row = dict(a=a, b=b, step=floor_step(D, a, b, R), big=sum(e["n"] for e in c if e["n"] >= 60),
                   sm=sum(e["n"] for e in c if e["n"] < 60), nsm=sum(e["n"] < 60 for e in c),
                   stall=bool(np.any(gms[max(1, a - 2):b + 1] > STALL_MS)))
        (A if row["big"] else B).append(row)
    p(f"clusters {len(cl)}: with a >=60 skip {len(A)} (small skips {sum(r['nsm'] for r in A)}, "
      f"{sum(r['sm'] for r in A)} frames; steps {sum(r['step'] for r in A):.1f} vs "
      f"{sum(r['big'] + r['sm'] for r in A)} frames)")
    p(f"small-only clusters {len(B)} (with stall {sum(r['stall'] for r in B)}): skips "
      f"{sum(r['nsm'] for r in B)}, {sum(r['sm'] for r in B)} frames")
    within3 = [r for r in B if abs(r["step"]) <= 3.0]
    ms1 = [r for r in B if abs(r["step"] - 48) <= 4]
    match = [r for r in B if abs(r["step"] - r["sm"]) <= 4]
    other = [r for r in B if r not in within3 and r not in ms1]
    p(f"  |step|<=3: {len(within3)} (cluster frames {min(r['sm'] for r in within3)}..{max(r['sm'] for r in within3)}); "
      f"1 ms: {len(ms1)}; step = frames: {len(match)}; other: {len(other)} "
      f"steps {[round(r['step'], 1) for r in other]} frames {[r['sm'] for r in other]}")
    # background: how often a 16-read span clear of multi-frame skips carries a 1 ms or >4 step
    mr = np.array([e["r"] for e in multi])
    pos = [r for r in range(13, R - 12) if not np.any(np.abs(mr - r) <= 20)]
    xs = np.array([floor_step(D, r, r, R) for r in pos])
    # non-overlapping spans: take every 16th clear position
    sub = xs[::16]
    p(f"background, {len(sub)} non-overlapping clear spans: 1 ms step {int(np.sum(np.abs(sub - 48) <= 4))}, "
      f"|step|>4 {int(np.sum(np.abs(sub) > 4))}; small-only clusters: 1 ms {len(ms1)} of {len(B)}, "
      f"|step|>4 {sum(abs(r['step']) > 4 for r in B)} of {len(B)}")
    # one-frame skips, slip spacing in content frames
    zeros = sorted(z["start"] for z in s["silent_stretches"])
    adv = 0
    cpos = []
    zi = 0
    for e in ev:
        while zi < len(zeros) and zeros[zi] < e["k"]:
            zi += 1
        cpos.append(e["k"] - c0 + adv - zi)
        adv += e["step"] - 1
    ones = [(c, e) for c, e in zip(cpos, ev) if e["kind"] == "skip" and e["n"] == 1]
    slips = []
    for c, e in ones:
        if slips and e["k"] - slips[-1][1] <= 12:
            slips[-1][2] += 1
            continue
        slips.append([c, e["k"], 1])
    d = np.diff([x[0] for x in slips])
    one = d[d < 100000]
    p(f"one-frame skips {len(ones)} -> {len(slips)} events ({sum(x[2] == 1 for x in slips)} single, "
      f"{sum(x[2] == 2 for x in slips)} paired); spacing {one.min()}..{one.max()} median {np.median(one):.0f} "
      f"= {np.median(one) / FS:.4f} s, {1e6 / np.median(one):.2f} ppm; doubles {d[d >= 100000].tolist()}")
    reps = np.diff([c for c, e in zip(cpos, ev) if e["kind"] == "repeat"])
    p(f"repeat spacing {reps[reps < 140000].min()}..{reps[reps < 140000].max()}; doubles {int(np.sum(reps >= 140000))}")
    tot = (c1 - c0) + sum(e["n"] for e in multi)
    p(f"share >=2 {100 * sum(e['n'] for e in multi) / tot:.3f}%, >=60 {100 * sum(e['n'] for e in ge60) / tot:.3f}%")
    print("\n".join(out))


if __name__ == "__main__":
    main(*sys.argv[1:3])
