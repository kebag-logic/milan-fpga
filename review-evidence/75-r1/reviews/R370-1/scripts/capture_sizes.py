"""Rank the per-cycle raw capture sizes published in the page's artifact table.

usage: capture_sizes.py <page.md>
Joins each size with the page's per-cycle restart value and reports where the
sub-2 ms (below one 500 PDU/s CRF period) cycles fall in the size ranking.
"""
import math, re, statistics, sys
text = open(sys.argv[1]).read()
size = {(m[1], int(m[2])): int(m[3]) for m in re.finditer(r'^\| `(listener|talker)-(\d{3})/tap\.pcap` \| (\d+) \|', text, re.M)}
lat = {(m[1], int(m[2])): float(m[3]) for m in re.finditer(r'^\| DUT (listener|talker) \| (\d+) \| ([0-9.]+) \|', text, re.M)}
for d in ('listener', 'talker'):
    keys = sorted(k for k in size if k[0] == d)
    s = [size[k] for k in keys]
    med = statistics.median(s)
    rank = sorted(keys, key=lambda k: -size[k])
    print(f'{d}: {len(keys)} captures, median {med:.0f} bytes')
    print('  largest eight:', [(k[1], size[k], f'+{size[k]-med:.0f}', lat[k]) for k in rank[:8]])
    sub = [k for k in keys if lat[k] < 0.002]
    print('  sub-2 ms cycles and their size rank:', [(k[1], lat[k], size[k], rank.index(k) + 1) for k in sub])
    if len(sub) == 3:
        top = max(rank.index(k) + 1 for k in sub)
        print(f'  chance that 3 random cycles all rank within the top {top}: {math.comb(top, 3) / math.comb(100, 3):.2e}')
print('reference: one 2 s hold of 500 PDU/s CRF is about 1000 records of about 104 bytes (16 pcap + 28 tap envelope + 60 frame), about 104 KB')
