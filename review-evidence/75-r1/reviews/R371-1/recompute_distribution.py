#!/usr/bin/env python3
"""Recompute the #75 reconnect distribution, growth and table cross-checks.

Usage: recompute_distribution.py <HANDOFF.md> <findings page .md>
Inputs are the published evidence-packet HANDOFF.md cycle ledger and the
findings page under review. Prints every recomputed figure and every
mismatch; exits 1 if any mismatch is found.
"""
import math
import re
import statistics
import sys


def ledger(path):
    rows = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\| (listener|talker) \| \1-(\d{3}) \| ([\d.]+) \| (\d+) \| (\d+) \| ([\d.]+) \| (\d+) \|", line)
        if m:
            d, c = m.group(1), int(m.group(2))
            resp, first, lat = int(m.group(4)), int(m.group(5)), float(m.group(6))
            rows.setdefault(d, {})[c] = dict(hold=float(m.group(3)), resp=resp, first=first,
                                             lat=lat, lat_ns=first - resp, over=int(m.group(7)))
    return rows


def page_cycles(path):
    rows = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\| DUT (listener|talker) \| (\d+) \| ([\d.]+) \| (\d+) / (\d+) \| (\d+) / (\d+) \| (\d+) / (\d+) \| (\d+) / (\d+) \| (\d+) / (\d+) \| (\w+) \|", line)
        if m:
            g = m.groups()
            rows.setdefault(g[0], {})[int(g[1])] = dict(lat=float(g[2]), pdus=(int(g[3]), int(g[4])),
                                                        la=(int(g[5]), int(g[6])), ta=(int(g[7]), int(g[8])),
                                                        lst=(int(g[9]), int(g[10])), rdy=(int(g[11]), int(g[12])),
                                                        res=g[13])
    return rows


def nearest_rank(vals, p):
    s = sorted(vals)
    return s[math.ceil(p / 100 * len(s)) - 1]


def slope(xs, ys):
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def main():
    L = ledger(sys.argv[1])
    P = page_cycles(sys.argv[2])
    bad = 0
    for d in ("listener", "talker"):
        led, pg = L[d], P[d]
        print(f"== {d}: ledger cycles {len(led)} page cycles {len(pg)}")
        if sorted(led) != list(range(1, 101)) or sorted(pg) != list(range(1, 101)):
            print("MISMATCH cycle numbering"); bad += 1
        for c in range(1, 101):
            r = led[c]
            if abs(r["lat_ns"] / 1e9 - r["lat"]) > 1e-9:
                print(f"MISMATCH {d} {c}: first-resp {r['lat_ns']} vs latency {r['lat']}"); bad += 1
            if f"{r['lat']:.6f}" != f"{pg[c]['lat']:.6f}":
                print(f"MISMATCH {d} {c}: ledger {r['lat']} page {pg[c]['lat']}"); bad += 1
            if pg[c]["res"] != "PASS" or r["lat"] >= 1.0 or r["over"] != 0:
                print(f"NOTE {d} {c}: result {pg[c]['res']} lat {r['lat']} over {r['over']}"); bad += 1
            if not (1.9995 < r["hold"] < 2.01):
                print(f"NOTE {d} {c}: hold {r['hold']}")
        lat = [led[c]["lat"] for c in range(1, 101)]
        print(f"min {min(lat):.9f} median {statistics.median(lat):.9f} p95(nr) {nearest_rank(lat, 95):.9f} max {max(lat):.9f} below1s {sum(x < 1 for x in lat)}")
        s_sorted = sorted(lat)
        print(f"  sorted[49]={s_sorted[49]:.9f} sorted[50]={s_sorted[50]:.9f} (median = mean of both for n=100)")
        print(f"  p95 alternatives: sorted[94]={s_sorted[94]:.9f} sorted[95]={s_sorted[95]:.9f} linear={statistics.quantiles(lat, n=20, method='inclusive')[-1]:.9f}")
        xs = list(range(1, 101))
        print(f"slope {slope(xs, lat):.6f} s/cycle; first10 median {statistics.median(lat[:10]):.6f} last10 median {statistics.median(lat[90:]):.6f}")
        # robustness of the trend claim: slope without the top-3 outliers, and Spearman rho
        rank = {v: i for i, v in enumerate(sorted(lat))}
        rho = 1 - 6 * sum((rank[v] - (i)) ** 2 for i, v in enumerate(lat)) / (100 * (100 ** 2 - 1))
        print(f"  spearman rho(cycle, latency) {rho:.4f}")
        half = (statistics.median(lat[:50]), statistics.median(lat[50:]))
        print(f"  halves median {half[0]:.6f} {half[1]:.6f}")
        for b in range(10):
            blk = lat[b * 10:(b + 1) * 10]
            print(f"  block {b*10+1}-{b*10+10}: median {statistics.median(blk):.6f} max {max(blk):.6f}")
        # sum of per-cycle PDUs vs whole PDU totals on the page
        print(f"  sum PDUs DUT {sum(pg[c]['pdus'][0] for c in pg)} bridge {sum(pg[c]['pdus'][1] for c in pg)}")
        print(f"  sum LeaveAll DUT {sum(pg[c]['la'][0] for c in pg)} bridge {sum(pg[c]['la'][1] for c in pg)}")
        print(f"  sum TA decl DUT {sum(pg[c]['ta'][0] for c in pg)} bridge {sum(pg[c]['ta'][1] for c in pg)}")
        print(f"  sum Listener decl DUT {sum(pg[c]['lst'][0] for c in pg)} bridge {sum(pg[c]['lst'][1] for c in pg)}")
        print(f"  sum Ready DUT {sum(pg[c]['rdy'][0] for c in pg)} bridge {sum(pg[c]['rdy'][1] for c in pg)}")
        # arrival phase of first AVTP relative to response: granularity check
        firsts = sorted({round((led[c]['first'] % 100_000_000) / 1e6, 1) for c in led})
        print(f"  first-AVTP ns mod 100 ms (ms, distinct values): {firsts[:12]}{' ...' if len(firsts) > 12 else ''} count {len(firsts)}")
    print("MISMATCHES", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
