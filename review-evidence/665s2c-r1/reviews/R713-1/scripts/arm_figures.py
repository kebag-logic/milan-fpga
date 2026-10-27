"""Per archived arm: the worst pass over every group, and the CPI and bus-wait figures summed over
every group's run summary. usage: arm_figures.py RUNS_DIR"""
import json
import sys
from pathlib import Path

def split(v):
    n, total, *_ = (int(x) for x in v.split('/'))
    return n, total

for arm in sorted(Path(sys.argv[1]).iterdir()):
    groups = [json.loads(p.read_text()) for p in arm.glob('*.json') if p.stem != 'results']
    if not groups:
        continue
    worst = max(((g['passes']['worst']['cycles'], g['group']) for g in groups if g['passes'].get('worst')), default=None)
    cpu = sum(int(g['summary']['cpu']) for g in groups)
    instr = sum(int(g['summary']['instr']) for g in groups)
    fetch = [split(v) for g in groups for k, v in g['summary'].items() if k.startswith('fetch_')]
    data = [split(v) for g in groups for k, v in g['summary'].items() if k.startswith(('load_', 'store_'))]
    fn, fw = sum(n for n, _ in fetch), sum(w for _, w in fetch)
    dw = sum(w for _, w in data)
    print(f'{arm.name}: worst pass {worst[0]:,} ({worst[0]/50000:.2f} ms) {worst[1]}; CPI {cpu/instr:.2f}; '
          f'fetch/1000 instr {1000*fn/instr:.1f}; mean fetch wait {fw/fn:.1f}; fetch waits/cycles {fw/cpu:.3f}; '
          f'data waits/cycles {dw/cpu:.3f}')
