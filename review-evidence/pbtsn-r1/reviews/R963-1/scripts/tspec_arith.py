#!/usr/bin/env python3
"""Recompute docs/POCKETBEAGLE.md's class A reservation total from its stated TSpec frame sizes:
42 octets of per-frame media overhead, the 46-octet minimum Ethernet payload, 8000 frames per second."""
sizes = {'AAF 8 ch': 217, 'AAF 4 ch': 121, 'CRF': 29}
streams = ['AAF 8 ch', 'AAF 8 ch', 'AAF 4 ch', 'AAF 4 ch', 'CRF']
total = 0
for s in streams:
    bps = (max(sizes[s], 46) + 42) * 8 * 8000
    total += bps
    print(f'{s}: {bps / 1e6:.3f} Mb/s')
print(f'total {total / 1e6:.3f} Mb/s; 75% of 100 Mb/s = 75.000 Mb/s; under limit: {total < 75e6}')
