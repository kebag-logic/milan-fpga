#!/usr/bin/env python3
"""Table identity across heads and recomputation of page figures.
Usage: table_check.py <repo> <summary.json> <round1> <round2> <head>"""
import hashlib, json, statistics, subprocess, sys, math
PAGE = "docs/findings/117_AUDIO_CONTINUITY.md"
repo, summ, revs = sys.argv[1], sys.argv[2], sys.argv[3:6]
def page(rev):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{PAGE}"], check=True,
                          capture_output=True, text=True).stdout
def tables(text):
    out, cur = [], []
    for ln in text.splitlines():
        if ln.startswith("|"):
            cur.append(ln)
        elif cur:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out
T = {r: tables(page(r)) for r in revs}
for r in revs:
    print(f"{r[:8]}: {len(T[r])} tables, {sum(len(t) for t in T[r])} table lines")
h = lambda t: hashlib.sha256("\n".join(t).encode()).hexdigest()[:16]
r1, r2, r3 = revs
print("table | head | =round2 | =round1 | header")
for i, t in enumerate(T[r3]):
    eq2 = i < len(T[r2]) and T[r2][i] == t
    eq1 = any(t == u for u in T[r1])
    print(f"{i:2d} | {h(t)} | {eq2} | {eq1} | {t[0][:60]}")
# cells that changed in table 0 between round 2 and head
for a, b in zip(T[r2][0], T[r3][0]):
    if a != b:
        ca, cb = a.split(" | "), b.split(" | ")
        diff = [k for k in range(max(len(ca), len(cb))) if (ca[k:k+1] != cb[k:k+1])]
        print("summary row changed:", ca[0][:40], "cells", diff)
# restart statistics from the per-cycle table
cyc = [t for t in T[r3] if t[0].startswith("| Cycle |")][0][2:]
rs = [float(row.split("|")[5]) for row in cyc]
fc = [float(row.split("|")[6]) for row in cyc]
lv = [float(row.split("|")[4]) for row in cyc]
s = sorted(rs); n = len(s)
def pct(p):  # linear interpolation, numpy default
    k = (n - 1) * p; f = math.floor(k); return s[f] + (s[min(f + 1, n - 1)] - s[f]) * (k - f)
x = list(range(1, n + 1)); mx = statistics.mean(x); my = statistics.mean(rs)
sxx = sum((a - mx) ** 2 for a in x); b = sum((a - mx) * (c - my) for a, c in zip(x, rs)) / sxx
res = [c - (my + b * (a - mx)) for a, c in zip(x, rs)]
se = math.sqrt(sum(e * e for e in res) / (n - 2) / sxx); tq = 2.0484071417952445  # t(0.975, 28)
print(f"restarts n={n} below1s={sum(v < 1 for v in rs)} min={s[0]} median={statistics.median(rs):.4f} p95={pct(.95):.4f} max={s[-1]}")
print(f"first10 median={statistics.median(rs[:10]):.4f} last10 median={statistics.median(rs[-10:]):.4f} slope={b:.6f} ci=[{b-tq*se:.6f}, {b+tq*se:.6f}] df={n-2}")
print(f"from-command min={min(fc)} max={max(fc)}; response delay ms {min((f-r)*1e3 for f, r in zip(fc, rs)):.1f}..{max((f-r)*1e3 for f, r in zip(fc, rs)):.1f}; last-valid {min(lv)}..{max(lv)}")
c = json.load(open(summ))["continuity"]; hist = {int(k): v for k, v in c["skip_size_histogram"].items()}
small = {k: v for k, v in hist.items() if 2 <= k <= 59}; big = {k: v for k, v in hist.items() if k >= 60}
print(f"skips 2..59: {sum(small.values())} events, {sum(k*v for k,v in small.items())} frames; multiples of 6: {sum(v for k,v in small.items() if k % 6 == 0)}; exactly 6: {small.get(6,0)}")
print(f"skips >=60: {sum(big.values())} events, {sum(k*v for k,v in big.items())} frames; one-frame {hist.get(1)}")
sec = c["seconds"]
for name, ev in (("repeat", c["repeats"]), ("one", hist[1]), ("2-59", sum(small.values())), (">=60", sum(big.values()))):
    print(f"per second {name}: {ev/sec:.3f} (over {sec} s captured)")
