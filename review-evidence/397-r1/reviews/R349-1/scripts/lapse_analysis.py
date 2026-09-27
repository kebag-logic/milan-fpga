#!/usr/bin/env python3
"""Heartbeat strobes and nvm_backed transitions in a raw event/UART log.

Usage: lapse_analysis.py <raw.log>
Lists heartbeat strobes (0x93c <- 0x1), the largest strobe-to-strobe or
strobe-to-final-prompt gap, and for each command the reported backed= bit
(from 'milan_nvm' output) or PP_STAT bit 6 (from 'milan_status' output).
"""
import re, sys
raw = open(sys.argv[1]).read()
ms = lambda c: c / 100_000
hb = [int(c) for c in re.findall(r'^EVENT cycle=(\d+) kind=write address=2364 value=1 ', raw, re.M)]
ends = [(int(c), int(i)) for c, i in re.findall(r'^EVENT cycle=(\d+) kind=command_end index=(\d+)', raw, re.M)]
starts = {int(i): int(c) for c, i in re.findall(r'^EVENT cycle=(\d+) kind=command_start index=(\d+)', raw, re.M)}
print('heartbeat strobes (ms):', [round(ms(h), 3) for h in hb])
last = ends[-1][0]
a, b = max(zip(hb, hb[1:] + [last]), key=lambda p: p[1] - p[0])
print(f'max gap {ms(b - a):.5f} ms: {ms(a):.3f} -> {ms(b):.3f}' + (' (to final prompt)' if b == last else ''))
chunks = re.split(r'^EVENT cycle=\d+ kind=command_start index=\d+.*$', raw, flags=re.M)[1:]
for (end, idx), text in zip(ends, chunks):
    m = re.search(r'backed=([01])', text)
    p = re.search(r'PP_STAT=([0-9a-f]{8})', text)
    state = f'backed={m[1]}' if m else (f'PP_STAT[6]={(int(p[1], 16) >> 6) & 1}' if p else '-')
    print(f'cmd[{idx:2}] {ms(starts[idx]):9.3f} -> {ms(end):9.3f} ms  {state}  (since last strobe at end: {ms(end - max([h for h in hb if h <= end] or [0])):.3f} ms)')
