#!/usr/bin/env python3
"""Heartbeat strobes inside each erase WIP window of a raw log (device-length polling evidence).

Usage: erase_heartbeats.py <raw.log>
For every erase (flash opcode 0xd8) lists the strobes (0x93c <- 1) inside [erase, erase+wait]
and the maximum spacing, including the window edges.
"""
import re, sys
raw = open(sys.argv[1]).read()
er = [(int(c), int(w)) for c, w in re.findall(r'^EVENT cycle=(\d+) kind=flash opcode=216 wait_cycles=(\d+)', raw, re.M)]
hb = [int(c) for c in re.findall(r'^EVENT cycle=(\d+) kind=write address=2364 value=1 ', raw, re.M)]
for c, w in er:
    inside = [h for h in hb if c <= h <= c + w]
    sp = [b - a for a, b in zip(inside, inside[1:])]
    print(f'erase at {c / 1e5:.5f} ms, WIP {w / 1e5:.3f} ms: {len(inside)} strobes inside; '
          f'max strobe spacing {max(sp) / 1e5 if sp else float("nan"):.5f} ms; '
          f'erase->first {((inside[0] - c) / 1e5) if inside else float("nan"):.5f} ms; '
          f'last->WIP end {((c + w - inside[-1]) / 1e5) if inside else float("nan"):.5f} ms')
