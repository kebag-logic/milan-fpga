#!/usr/bin/env python3
"""Probe 1: mixed channel counts at the full 16-stream-per-port shape.
Probe 2: reachability of per-phase loads under the page's phase policy
(fewest running streams, ties 0, 1, 3, 4, 2, 5), with stops and restarts,
at most 16 streams per port.

Reuses the class-level shaper model in cbs_model.py (same directory)."""
import os
import sys
from fractions import Fraction as F
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cbs_model as m  # noqa: E402


def aaf_bits(n):
    f = 24 * n + 24 + 22          # actual AVTPDU + Ethernet header with tag + FCS
    f = max(f, 68)
    return (f + 20) * 8


def aaf_bw(n):
    return F((1536 * n + 4288) * 1000)


def config(phase_channels, with_crf=True, crf_phase=None):
    frames = [[aaf_bits(n) for n in ph] for ph in phase_channels]
    slope = sum(aaf_bw(n) for ph in phase_channels for n in ph)
    if with_crf:
        frames[crf_phase].append(m.CRF)
        slope += m.BW_CRF
    return frames, slope


def probe_mixed():
    out = []
    loads = [3, 3, 2, 3, 3, 2]
    # k eight-channel streams in one phase, all others one-channel
    best = None
    for heavy_phase in range(6):
        for k in range(1, loads[heavy_phase] + 1):
            pc = [[1] * n for n in loads]
            for j in range(k):
                pc[heavy_phase][j] = 8
            for c in range(6):
                fr, sl = config(pc, True, c)
                w, _ = m.simulate(fr, sl)
                if best is None or w > best[0]:
                    best = (w, heavy_phase, k, c)
    out.append(f"preferred loads, k x 8-ch in one phase, rest 1-ch, CRF anywhere: worst wait "
               f"{m.us(best[0]):.3f} us (heavy phase {best[1]}, k {best[2]}, CRF phase {best[3]})")
    # exhaustive over which streams are 8-ch vs 1-ch (2^16 is large; use per-phase counts)
    import itertools
    best2 = None
    ranges = [range(n + 1) for n in loads]
    for heavy in itertools.product(*ranges):
        pc = [[8] * h + [1] * (n - h) for h, n in zip(heavy, loads)]
        fr, sl = config(pc, True, 2)
        w, _ = m.simulate(fr, sl, periods=30)
        if best2 is None or w > best2[0]:
            best2 = (w, heavy)
    out.append(f"preferred loads, CRF phase 2, every split of 8-ch/1-ch per phase: worst wait "
               f"{m.us(best2[0]):.3f} us, 8-ch streams per phase {best2[1]}")
    base = F(7 * 32, 12288000) + F(200, 10**9) + 6 * F(64, 50 * 10**6) + \
        2 * F(22, 50 * 10**6) + F(m.BE) / m.R + F(1, 10**6)
    out.append(f"page's other terms (with its 0.200 CDC) {m.us(base):.3f} us; total at that wait "
               f"{m.us(base + best2[0]):.3f} us")
    return out


def probe_reach():
    order = [0, 1, 3, 4, 2, 5]
    start = (0,) * 6
    seen = {start}
    stack = [start]
    while stack:
        s = stack.pop()
        if sum(s) < 16:
            mn = min(s)
            ph = next(p for p in order if s[p] == mn)
            t = list(s); t[ph] += 1; t = tuple(t)
            if t not in seen:
                seen.add(t); stack.append(t)
        for p in range(6):
            if s[p]:
                t = list(s); t[p] -= 1; t = tuple(t)
                if t not in seen:
                    seen.add(t); stack.append(t)
    full = sorted(s for s in seen if sum(s) == 16)
    return [f"reachable states {len(seen)}; reachable 16-stream load vectors: {full}"]


if __name__ == "__main__":
    print("\n".join(probe_reach() + probe_mixed()))
