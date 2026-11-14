"""Round 1's 8x8/1if measurements, from its graded legs: each poll kind's heaviest (the grade JSONs'
passes.polls.heaviest) and the heaviest SRP record handler (srp_mbx:receive spans in the logs), by leg.
usage: python3 -I r1_heaviest.py <builds-dir> <leg>..."""
import json
import re
import sys
from pathlib import Path

builds = Path(sys.argv[1])
legs = sys.argv[2:]
kinds: dict[str, tuple[int, str]] = {}
spans: dict[str, tuple[int, str]] = {}
WANT = ('srp_mbx:receive', 'srp_mbx:apply_receive', 'srp_mbx:build_mrpdu', 'mrp_attr_visit')
for leg in legs:
    res = builds / leg / 'results'
    for js in sorted(res.glob('*.json')):
        if js.name == 'results.json':
            continue
        d = json.loads(js.read_text())
        heavy = d.get('passes', {}).get('polls', {}).get('heaviest', {})
        for k, v in heavy.items():
            if v > kinds.get(k, (0, ''))[0]:
                kinds[k] = (v, f'{leg}/{js.stem}')
        log = js.with_suffix('.log')
        if not log.exists():
            continue
        with log.open() as fh:
            for line in fh:
                if line.startswith('SPAN ') and line.rstrip().endswith(WANT):
                    f = line.split()
                    if f[5] in WANT and int(f[3]) > spans.get(f[5], (0, ''))[0]:
                        spans[f[5]] = (int(f[3]), f'{leg}/{js.stem}')
print('# legs:', ' '.join(legs))
print('# poll kinds, heaviest CPU cycles (grade JSON passes.polls.heaviest)')
for k, (v, where) in sorted(kinds.items()):
    print(f'{k:16s} {v:>9,} {where}')
print('# traced spans, heaviest CPU cycles')
for k, (v, where) in sorted(spans.items()):
    print(f'{k:24s} {v:>9,} {where}')
