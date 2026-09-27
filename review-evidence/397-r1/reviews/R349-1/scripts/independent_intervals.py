#!/usr/bin/env python3
"""Reviewer-owned re-derivation of probed intervals from a raw event log.

Usage: independent_intervals.py <receipt.json | raw.log> [label]
Parses EVENT lines itself (no harness code). Reports: reset-release-to-PP_CTRL[0]
write, each 'milan_nvm' (status) command interval, every heartbeat strobe (0x93c
value 0x1) and the largest gap between consecutive strobes, attributing which
command intervals the gap spans. ms = system cycles / 100 MHz; CPU cycles = sys/2.
"""
import json, re, sys
from pathlib import Path

src = Path(sys.argv[1])
raw = json.loads(src.read_text())['raw_log'] if src.suffix == '.json' else src.read_text()
ev = [dict(kind=m[2], cycle=int(m[1]), **{k: int(v) for k, v in re.findall(r'(\w+)=(\d+)', m[3])})
      for m in re.finditer(r'^EVENT cycle=(\d+) kind=(\w+)(.*)$', raw, re.M)]
cmds = ['milan_status', 'milan_gettime', 'milan_nvm', 'milan_nvm commit', 'milan_nvm commit', 'milan_nvm',
        'milan_nvm wipe', 'milan_nvm', 'milan_nvm invalid', 'milan_settime 0 0',
        'milan_settime 18446744073 709551615', 'milan_settime 18446744073 709551616', 'milan_settime invalid',
        'milan_utc 0 0 37', 'milan_utc 18446744073709551615 0 1', 'milan_utc invalid 0 0', 'milan_status']
ms = lambda c: c / 100_000
RESET_RELEASE = 64  # sim_main: sys_reset falls after 128 half-periods = 64 rising edges
en = next(e for e in ev if e['kind'] == 'write' and e['address'] == 0x920 and e['value'] & 1)
print(f'boot reset->PP_CTRL[0]=1: sys={en["cycle"] - RESET_RELEASE} cpu={(en["cycle"] - RESET_RELEASE + 1)//2} ms={ms(en["cycle"] - RESET_RELEASE):.5f}')
st = {e['index']: e['cycle'] for e in ev if e['kind'] == 'command_start'}
nd = {e['index']: e['cycle'] for e in ev if e['kind'] == 'command_end'}
for i, c in enumerate(cmds):
    if c == 'milan_nvm':
        print(f'cmd[{i}] {c}: sys={nd[i]-st[i]} ms={ms(nd[i]-st[i]):.5f}')
hb = [e['cycle'] for e in ev if e['kind'] == 'write' and e['address'] == 0x93c and e['value'] == 1]
print('heartbeat strobes (ms):', [round(ms(h), 3) for h in hb])
pairs = list(zip(hb, hb[1:] + [nd[max(nd)]]))
a, b = max(pairs, key=lambda p: p[1] - p[0])
print(f'max gap: {ms(b-a):.5f} ms from {ms(a):.3f} to {ms(b):.3f}' + (' (tail to final prompt)' if b == nd[max(nd)] else ''))
span = [f'{i}:{cmds[i]}' for i in st if st[i] < b and nd[i] > a]
print('  command intervals overlapped by the gap:', span)
idle = sum(max(0, min(b, st[i+1]) - max(a, nd[i])) for i in range(len(cmds) - 1) if i + 1 in st)
print(f'  console idle (prompt->next input) inside the gap: {idle} sys cycles')
