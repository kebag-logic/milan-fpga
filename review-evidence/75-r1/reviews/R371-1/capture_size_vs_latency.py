#!/usr/bin/env python3
"""Relate published raw-capture sizes to published restart latencies.

Usage: capture_size_vs_latency.py <findings page .md> <HANDOFF.md>
Reads the page's capture index (bytes per tap.pcap) and the HANDOFF ledger
(latency, response and first-AVTP tap nanoseconds). The DUT CRF stream
advances once per 2 ms (next_timestamp - first_timestamp in the public cycle
records), so an interval shorter than one PDU period cannot show that the
stream was stopped when the response was seen. The script ranks capture
sizes per direction and reports where the sub-period cycles fall, with the
exact hypergeometric probability of that placement by chance.
"""
import math
import re
import statistics
import sys

page, handoff = sys.argv[1:3]
size = {}
for line in open(page, encoding="utf-8"):
    m = re.match(r"\| `((listener|talker)-(\d{3}))/tap\.pcap` \| (\d+) \|", line)
    if m:
        size[m.group(1)] = int(m.group(4))
lat = {}
for line in open(handoff, encoding="utf-8"):
    m = re.match(r"\| (listener|talker) \| ((?:listener|talker)-\d{3}) \| [\d.]+ \| (\d+) \| (\d+) \| ([\d.]+) \|", line)
    if m:
        lat[m.group(2)] = float(m.group(5))
PERIOD = 0.002
for d in ("listener", "talker"):
    names = sorted(n for n in lat if n.startswith(d))
    sizes = [size[n] for n in names]
    med = statistics.median(sizes)
    order = sorted(names, key=lambda n: -size[n])
    rank = {n: i + 1 for i, n in enumerate(order)}
    sub = [n for n in names if lat[n] < PERIOD]
    print(f"== {d}: {len(names)} cycles, median capture {med:.0f} bytes, min {min(sizes)}, max {max(sizes)}")
    print(f"   cycles with latency below one {PERIOD*1e3:.0f} ms PDU period: {len(sub)}")
    for n in sub:
        print(f"   {n}: latency {lat[n]:.9f} s, capture {size[n]} bytes (+{size[n]-med:.0f} vs median), size rank {rank[n]}/{len(names)}")
    print("   ten largest captures:")
    for n in order[:10]:
        print(f"     {n}: {size[n]} bytes (+{size[n]-med:.0f}), latency {lat[n]:.6f} s")
    if sub:
        k = len(sub)
        worst = max(rank[n] for n in sub)
        # P(all k chosen cycles land within the top `worst` ranks) under random placement
        p = math.comb(worst, k) / math.comb(len(names), k)
        print(f"   P(all {k} sub-period cycles within top {worst} sizes by chance) = {p:.3g}")
    big = [n for n in names if size[n] - med > 40000]
    print(f"   captures >40 kB above median: {len(big)}; of those sub-period: {sum(lat[n] < PERIOD for n in big)}")
