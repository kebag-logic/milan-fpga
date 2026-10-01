#!/usr/bin/env python3
"""Reviewer-side recomputation of the round 3 figures of the B5 page, written
independently of b5_attrib.py / b5_round3.py, from the published inputs only.

usage: indep_figures.py <a472_packet_dir> <receipts_dir_with_restored_a-long-reads.u16>
Pure standard library (no numpy).
"""
import csv, hashlib, json, sys
from pathlib import Path

pk, rd = Path(sys.argv[1]), Path(sys.argv[2])
rec = (rd / "a-long-reads.u16").read_bytes()
print("record sha256", hashlib.sha256(rec).hexdigest(), len(rec), "B")
gaps = [rec[i] | rec[i + 1] << 8 for i in range(0, len(rec), 2)]   # us, interval ending at read r=1..R
R = len(gaps)
t = [0]
for x in gaps:
    t.append(t[-1] + x)
D = [t[r] * 48000 / 1e6 - 480 * r for r in range(R + 1)]
g = [None] + [x / 1000 for x in gaps]
s = json.load(open(pk / "summary/a-long/summary.json"))["continuity"]
c0, c1 = s["window"]
assert c1 - c0 == 480 * R
ev = list(csv.DictReader(open(pk / "summary/a-long/continuity-events.csv")))
skips = []
for e in ev:
    if e["kind"] == "skip":
        f = int(e["frames"]); k = int(e["frame"])
        skips.append(dict(frames=f, frame=k, r=(k - c0) // 480 + 1))
multi = sorted([e for e in skips if e["frames"] >= 2], key=lambda e: e["r"])
cls = lambda lo, hi: [e for e in skips if lo <= e["frames"] <= hi]
for name, lo, hi in (("one-frame", 1, 1), ("2..59", 2, 59), (">=60", 60, 10**9), (">=240", 240, 10**9)):
    x = cls(lo, hi); print(f"skips {name}: {len(x)} events, {sum(e['frames'] for e in x)} frames")
print("repeats", sum(1 for e in ev if e["kind"] == "repeat"))

# A: stalls and alignment
stalls = [r for r in range(1, R + 1) if g[r] > 15.0]
excess = sum((g[r] - 10.0) * 48 for r in stalls)
print(f"stalls {len(stalls)}, excess {excess:.1f} frames")
sp = [(stalls[i + 1] - stalls[i]) for i in range(len(stalls) - 1)]
ts = [t[r] / 1e6 for r in stalls]
d = sorted(ts[i + 1] - ts[i] for i in range(len(ts) - 1))
print(f"stall spacing s: min {d[0]:.3f} median {d[len(d)//2]:.4f} max {d[-1]:.3f}")
S = set(stalls)
big = cls(60, 10**9)
al, na = [], []
for e in big:
    lag = next((o for o in (0, 1, 2) if e["r"] - o in S), None)
    (al if lag is not None else na).append((e, lag))
from collections import Counter
print(f">=60 stall-aligned (stall 0..2 reads before): {len(al)}, {sum(e['frames'] for e,_ in al)} frames, lags {dict(Counter(l for _,l in al))}")
for e, _ in na:
    near = min(abs(e["r"] - x) for x in stalls)
    iv = max(g[max(1, e["r"] - 2):e["r"] + 1])
    print(f"  NOT aligned: {e['frames']} frames, read {e['r']}, host {t[e['r']]/1e6:.2f} s, longest interval {iv:.2f} ms, nearest stall {near} reads")
after = Counter()
for st in stalls:
    after[sum(1 for e in cls(240, 10**9) if 0 <= e["r"] - st <= 2)] += 1
print("stalls by number of >=240 skips 0..2 reads after:", dict(after))

# B: floor test (W+1 = 11 reads, guards 3 before / 2 after), clusters joined under 16 reads
W, GB, GA, JOIN, TOL = 10, 3, 2, 16, 4.0
def step(a, b):
    lo, hi = a - GB - W, b + GA + W
    if lo < 0 or hi > R:
        return None
    return min(D[b + GA:hi + 1]) - min(D[lo:a - GB + 1])
cl = []
for e in multi:
    if cl and e["r"] - cl[-1][-1]["r"] < JOIN:
        cl[-1].append(e)
    else:
        cl.append([e])
B = [c for c in cl if all(e["frames"] < 60 for e in c)]
Bst = [c for c in B if any(g[r] > 15.0 for r in range(max(1, c[0]["r"] - 2), c[-1]["r"] + 1))]
print(f"clusters {len(cl)}; off-stall (2..59 only) {len(B)}, of them with a stall {len(Bst)}")
k1 = [c for c in B if abs(step(c[0]["r"], c[-1]["r"]) - 48) <= TOL and abs(step(c[0]["r"], c[-1]["r"]) - sum(e["frames"] for e in c)) > TOL]
print(f"off-stall clusters with a 1 ms floor step: {len(k1)}")
mr = [e["r"] for e in multi]
import bisect
def free(r, m):
    return bisect.bisect_left(mr, r - m) == bisect.bisect_right(mr, r + m)
pos = [r for r in range(GB + W, R - GA - W) if free(r, JOIN + 4)]
x = [step(r, r) for r in pos]
bigi = [i for i, v in enumerate(x) if abs(v) > TOL]
grp = []
for i in bigi:
    if grp and pos[i] - pos[grp[-1][-1]] <= 2 * JOIN:
        grp[-1].append(i)
    else:
        grp.append([i])
gm = [max((x[i] for i in gg), key=abs) for gg in grp]
n1 = sum(1 for v in gm if abs(v - 48) <= TOL)
print(f"clear positions {len(pos)}; groups |step|>4: {len(grp)}, 1 ms groups {n1}")
rate_read = n1 / len(pos)
exp16 = len(B) * JOIN * rate_read
span = [JOIN + c[-1]["r"] - c[0]["r"] for c in B]
expspan = sum(span) * rate_read
print(f"chance, 16-read window per cluster: {exp16:.2f}; with each cluster's own span (16 + b - a): {expspan:.2f}; "
      f"cluster spans min {min(span)} median {sorted(span)[len(span)//2]} max {max(span)}")
# C: linearity of the planted control at 300 positions
import random
random.seed(117)
pick = random.sample(pos, 300)
worst = 0.0
for r in pick:
    base = step(r, r)
    for m in (6, 12, 24):
        Dp = D[:r - 1] + [v + m for v in D[r - 1:]]
        lo, hi = r - GB - W, r + GA + W
        v = min(Dp[r + GA:hi + 1]) - min(Dp[lo:r - GB + 1])
        worst = max(worst, abs(v - base - m))
print(f"planted control: max |recovered - unplanted - plant| over 300 positions x 3 plants = {worst:.3g}")
