#!/usr/bin/env python3
"""Recompute the PR-body figures from the author's published perf receipts.

usage: packet_figures.py RECEIPTS_DIR   (review-evidence/cicd-r1/author/receipts)
"""
import sys


def rd(path):
    out = {}
    for line in open(path):
        p = line.strip().split(",")
        if len(p) > 3 and p[0] and p[0][0].isdigit():
            out[p[2]] = float(p[0])
    return out


def pct(a, b):
    return 100.0 * (b / a - 1.0)


def main():
    e = sys.argv[1]
    print("probes.vlt, whole suite task-clock (ab/base vs ab/pub):")
    for s in ("crf_rx", "mmcm_servo", "aaf_clock_meter", "maap"):
        x, y = rd(f"{e}/ab/base.{s}.perf"), rd(f"{e}/ab/pub.{s}.perf")
        print(f"  {s:16s} {x['task-clock:u']/1e3:8.1f} -> {y['task-clock:u']/1e3:8.1f} s  {pct(x['task-clock:u'], y['task-clock:u']):+.1f} %")
    x, y = rd(f"{e}/talker/ts_flat.perf"), rd(f"{e}/talker/ts_vlt.perf")
    for k in ("instructions:u", "L1-icache-load-misses:u"):
        print(f"  talker_step {k:26s} {pct(x[k], y[k]):+.2f} %")
    print("budget harness testbench -Os -> -O3, paired runs:")
    for a, b in (("base", "tbO3"), ("base-2", "tbO3-2"), ("base-3", "tbO3-3")):
        x, y = rd(f"{e}/budget/{a}.perf"), rd(f"{e}/budget/{b}.perf")
        print(f"  {a:7s}->{b:7s} task-clock {pct(x['task-clock:u'], y['task-clock:u']):+.1f} %  "
              f"L1d misses {x['L1-dcache-load-misses:u']/1e9:.3f} -> {y['L1-dcache-load-misses:u']/1e9:.3f} G "
              f"{pct(x['L1-dcache-load-misses:u'], y['L1-dcache-load-misses:u']):+.1f} %")
    xs = sum(rd(f"{e}/budget/{n}.perf")["L1-dcache-load-misses:u"] for n in ("base", "base-2", "base-3"))
    ys = sum(rd(f"{e}/budget/{n}.perf")["L1-dcache-load-misses:u"] for n in ("tbO3", "tbO3-2", "tbO3-3"))
    print(f"  L1d misses, mean of three vs three: {pct(xs, ys):+.1f} %")
    print("ccache receipts as published:")
    for n in ("nocc", "cold", "warm"):
        print(f"  ccache/{n}.time: {open(f'{e}/ccache/{n}.time').read().strip()}")


if __name__ == "__main__":
    main()
