#!/usr/bin/env python3
"""Independent re-derivation of the B5 round-2 attribution figures (reviewer-written;
does not import the author's tool).

usage: r425_rederive.py <a-long-reads.u16> <round-1 author packet dir>

Inputs: the derived read record (uint16 LE microsecond differences, one per read of
480 frames), summary/a-long/summary.json and summary/a-long/continuity-events.csv.
"""
import csv, hashlib, json, sys
from pathlib import Path
import numpy as np

rec, pk = Path(sys.argv[1]), Path(sys.argv[2])
FS, PER = 48000, 480
print(f"record sha256 {hashlib.sha256(rec.read_bytes()).hexdigest()}")
gap = np.fromfile(rec, dtype="<u2").astype(np.int64)            # us
R = len(gap)
t_us = np.concatenate(([0], np.cumsum(gap)))
s = json.load(open(pk / "summary/a-long/summary.json"))["continuity"]
c0, c1 = s["window"]
assert c1 - c0 == PER * R
ev = list(csv.DictReader(open(pk / "summary/a-long/continuity-events.csv")))
for e in ev:
    e["frame"], e["frames"], e["step"] = int(e["frame"]), int(e["frames"]), int(e["step"])
    e["r"] = (e["frame"] - c0) // PER + 1        # read that delivers the frame
sk = [e for e in ev if e["kind"] == "skip"]
print(f"events {len(ev)}; skips {len(sk)}; repeats {sum(e['kind']=='repeat' for e in ev)}")

# ---- window and count drift
wt = s["window_time"][1] - s["window_time"][0]
print(f"window_time {wt:.6f} s -> 48 kHz {wt*FS:.1f} frames; captured {c1-c0}; deficit {wt*FS-(c1-c0):.1f} (rounded {round(wt*FS-(c1-c0))})")
print(f"record elapsed {t_us[-1]} us -> deficit {t_us[-1]*FS/1e6-(c1-c0):.1f}")
print(f"captured audio {(c1-c0)/FS:.2f} s in {wt:.2f} s")

# ---- stalls: interval ending at read r (r=1..R) is gap[r-1]
stall_r = np.flatnonzero(gap > 15000) + 1
print(f"stalls (>15 ms) {len(stall_r)}; interval {gap[stall_r-1].min()/1e3:.2f}..{gap[stall_r-1].max()/1e3:.2f} ms")
sp = np.diff(t_us[stall_r]) / 1e6
print(f"stall spacing s: min {sp.min():.3f} median {np.median(sp):.4f} max {sp.max():.3f}; window/stalls {wt/len(stall_r):.3f}")
exc = ((gap[stall_r-1] - 10000) * FS / 1e6).sum()
print(f"stall excess over 10 ms: {exc:.1f} frames")
sset = set(stall_r.tolist())
def lag(e):
    for o in (0, 1, 2):
        if e["r"] - o in sset:
            return o
    return None
g60 = [e for e in sk if e["frames"] >= 60]
al = [lag(e) for e in g60]
print(f"skips >=60: {len(g60)}, {sum(e['frames'] for e in g60)} frames; stall 0..2 reads before: {sum(a is not None for a in al)}; "
      f"lags {dict((k, al.count(k)) for k in sorted(set(a for a in al if a is not None)))}")
g240 = [e for e in sk if e["frames"] >= 240]
per = {}
for e in g240:
    a = lag(e)
    if a is not None:
        per.setdefault(e["r"] - a, 0); per[e["r"] - a] += 1
print(f"stalls with a >=240 skip 0..2 reads after: {len(per)} of {len(stall_r)}; counts per stall {sorted(set(per.values()))}; "
      f">=240 skips {len(g240)}")
for e in g60:
    if lag(e) is None:
        w = gap[max(0, e['r'] - 3):e['r']]
        print(f"  unaligned skip {e['frames']} frames: longest interval in the 3 reads up to it {w.max()/1e3:.2f} ms")

# ---- 2..59 class, clusters, distance to nearest stall
small = [e for e in sk if 2 <= e["frames"] < 60]
print(f"skips 2..59: {len(small)}, {sum(e['frames'] for e in small)} frames; multiples of 6: {sum(e['frames']%6==0 for e in small)}; exactly 6: {sum(e['frames']==6 for e in small)}")
multi = sorted([e for e in sk if e["frames"] >= 2], key=lambda e: e["r"])
JOIN = 16
cl = []
for e in multi:
    if cl and e["r"] - cl[-1][-1]["r"] < JOIN:
        cl[-1].append(e)
    else:
        cl.append([e])
A = [c for c in cl if any(e["frames"] >= 60 for e in c)]
B = [c for c in cl if not any(e["frames"] >= 60 for e in c)]
nA = sum(1 for c in A for e in c if e["frames"] < 60)
fA = sum(e["frames"] for c in A for e in c if e["frames"] < 60)
nB = sum(len(c) for c in B); fB = sum(e["frames"] for c in B for e in c)
print(f"clusters {len(cl)}: with a >=60 skip {len(A)} (2..59 inside: {nA}, {fA} frames); 2..59 only {len(B)} ({nB} skips, {fB} frames)")
dist = [min(abs(e["r"] - st) for st in stall_r) for c in B for e in c]
print(f"off-stall 2..59 skips: reads to the nearest stall min {min(dist)}, median {int(np.median(dist))}")

# ---- floor-step test, reviewer's own formulation and a parameter grid
D = t_us * FS / 1e6 - PER * np.arange(R + 1)
def step(a, b, W, GB, GA):
    lo, hi = a - GB - W, b + GA + W
    if lo < 0 or hi > R:
        return None
    return D[b + GA:hi + 1].min() - D[lo:a - GB + 1].min()
for (W, GB, GA) in ((10, 3, 2), (6, 3, 2), (15, 4, 3), (20, 3, 2)):
    kinds = {"none": 0, "1ms": 0, "match": 0, "other": 0}
    for c in B:
        f = sum(e["frames"] for e in c)
        v = step(c[0]["r"], c[-1]["r"], W, GB, GA)
        k = "match" if abs(v - f) <= 4 else "none" if abs(v) <= 4 else "1ms" if abs(v - 48) <= 4 else "other"
        kinds[k] += 1
    sA = sum(step(c[0]["r"], c[-1]["r"], W, GB, GA) for c in A)
    print(f"floor W={W+1} GB={GB} GA={GA}: off-stall clusters {kinds}; stall-cluster step sum {sA:.1f} vs {sum(e['frames'] for c in A for e in c)}")

# ---- 1 ms step base rate at clear positions vs at off-stall clusters
W, GB, GA = 10, 3, 2
mr = np.array([e["r"] for e in multi])
clear = [r for r in range(GB + W, R - GA - W) if not np.any(np.abs(mr - r) <= JOIN + 4)]
x = np.array([step(r, r, W, GB, GA) for r in clear])
hit = np.array(clear)[np.abs(x - 48) <= 4]
groups = 0; last = -10**9
for r in hit:
    if r - last > 2 * (W + GB + GA + 1):
        groups += 1
    last = r
span = W + GB + GA + 1
print(f"clear positions {len(clear)}; 1 ms step groups {groups}; independent windows ~{len(clear)//span}; "
      f"rate per window {groups/(len(clear)/span):.4f}; expected among {len(B)} clusters {len(B)*groups/(len(clear)/span):.2f}")

# ---- one-frame slips
one = [e for e in sk if e["frames"] == 1]
zeros = [z["start"] for z in s["silent_stretches"]]
done_extra = 0
pos = []
events = sorted(ev, key=lambda e: e["frame"])
acc = 0; k = 0
contentpos = {}
for e in events:
    contentpos[id(e)] = (e["frame"] - c0) + acc - sum(1 for z in zeros if z < e["frame"])
    acc += e["step"] - 1
sl = []
for e in one:
    if sl and e["frame"] - sl[-1][-1]["frame"] <= 12:
        sl[-1].append(e)
    else:
        sl.append([e])
pc = [contentpos[id(x[0])] for x in sl]
spc = np.diff(pc)
sing = spc[spc < 100000]
print(f"one-frame skips {len(one)} -> slip events {len(sl)} ({sum(len(x)==2 for x in sl)} pairs); spacing min {sing.min()} median {np.median(sing):.0f} max {sing.max()}; doubles {spc[spc>=100000].tolist()}")
print(f"  {np.median(sing)/FS:.4f} s; {1e6/np.median(sing):.2f} ppm")
