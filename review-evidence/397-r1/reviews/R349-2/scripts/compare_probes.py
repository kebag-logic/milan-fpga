#!/usr/bin/env python3
"""Compare round-2 probe reruns with the round-1 probe logs.

Usage: compare_probes.py <round1-receipts-dir> <runs-dir> <author-receipts-dir>
P1: unchanged round-1 paced driver log vs round-1 log (byte identity).
P2: unchanged round-1 split-WIP driver log vs round-1 log (byte identity), if present.
P3: head queued-input run; strip only the new passive lines (ticks, aem_read) and compare
    with the round-1 P3 log; also compare the head run with the published queued receipt.
"""
import hashlib, json, re, sys
from pathlib import Path
r1, runs, auth = map(Path, sys.argv[1:4])
h = lambda b: hashlib.sha256(b).hexdigest()
for name, old in (('P1', 'probe_uart_paced.raw.log'), ('P2', 'probe_wip_split.raw.log')):
    new = runs / name / 'raw.log'
    if not new.exists():
        print(name, 'not run'); continue
    a, b = (r1 / old).read_bytes(), new.read_bytes()
    print(f'{name}: round1 {h(a)[:16]} rerun {h(b)[:16]} identical={a == b} bytes={len(a)}/{len(b)}')
q = (runs / 'queued1x1' / 'raw.log').read_text()
stripped = re.sub(r'\nEVENT cycle=\d+ kind=(ticks|aem_read)[^\n]*\n', '', q)
old = (r1 / 'probe_queued.raw.log').read_text()
print(f'P3: stripped head queued-input log identical to round-1 P3 log: {stripped == old} '
      f'(round1 {h(old.encode())[:16]}, stripped {h(stripped.encode())[:16]})')
res = json.loads((runs / 'queued1x1' / 'result.json').read_text())
pub = json.loads((auth / 'round2-1x1-queued-input.json').read_text())
print('P3: head queued-input log equals published receipt log:', res['log_sha256'] == pub['log_sha256'],
      '| rows/heartbeat/liveness/findings equal:',
      all(res[k] == pub[k] for k in ('rows', 'heartbeat', 'liveness', 'budget_findings')))
print('P3 heartbeat:', res['heartbeat'])
print('P3 liveness:', [(x['command_index'], x['backed'], round(x['sampled_by_sys_cycle'] / 1e5, 5)) for x in res['liveness']])
