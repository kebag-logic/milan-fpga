#!/usr/bin/env python3
"""Check the published receipts against their counts and recomputed grader tables.
Usage: python3 -B check_evidence.py CHECKOUT PACKET
"""
from collections import Counter
from decimal import Decimal
import json
from pathlib import Path
import re
import sys

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
sys.path.insert(0, str(repo/'sw/firmware/ctrl/test'))
import srp_mutants
import srp_talker_mutants

src = packet/'scratch/review-evidence/895-r1/author-r2'
r = src/'receipts'
manifest = json.loads((src.parent/'MANIFEST.json').read_text())
out = packet/'receipts/published'
out.mkdir(parents=True, exist_ok=True)
selected = [
    'graders/base-load_check.log', 'graders/base-flip_check.log',
    'graders/head-load_check.log', 'graders/head-flip_check.log',
    'rom/images-base.md', 'rom/images-head.md', 'rom/deltas.md',
    'costs/least-margin.txt', 'costs/heaviest-work.txt',
    'costs/G1/costs.json', 'costs/G8/costs.json',
    'legs/mergeA1.txt', 'legs/mergeA8.txt',
    'gates/verify-table.md', 'gates/verify.rc',
    'gates/workflows/mutant-counts.txt', 'gates/out/lane/summary.txt',
    'gates/workflows/logs/rtl-fast__firmware-unit__ci_step_12.log',
    'gates/out/lane/ctrl_memory.log', 'sweep/rerun-shard1/summary.txt',
    'probes/domain-refused-path/probe-test.cpp',
    'probes/domain-refused-path/run-if1-endstation_ax7101_1x1_tdm8.log',
    'probes/domain-refused-path/run-if2-endstation_ax7101_8x8.log',
]
for point in ('A1','A8','B1','B8','N1','N8','W1','W8'):
    selected.extend(f'gates/harness/{point}-{suffix}' for suffix in
                    ('compare.txt','cmp.rc','sample.rc','regrade.rc','regrade.log'))
for path in selected:
    target = out/path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((r/path).read_bytes())
(out/'manifest-subset.json').write_text(json.dumps([x for x in manifest if
    x['file'] in ['author-r2/receipts/'+p for p in selected]], indent=2)+'\n')

rows = []
for line in (r/'gates/verify-table.md').read_text().splitlines()[2:]:
    if line.startswith('|'):
        cells = [x.strip() for x in line.split('|')[1:-1]]
        rows.append(cells)
counts = Counter(x[4] for x in rows)
assert counts == {'0':139, 'NOT RUN':226}, counts
assert all(x[5] for x in rows if x[4]=='NOT RUN')
trees = list((r/'gates').rglob('*tree-after*.txt'))
assert len(trees)==39 and all(p.read_text().strip() in ('',
    'head 18300f6e5f0c63b2ebc81d6bbc243496034f638a\nstatus:') for p in trees)
print('Published workflow gate: 139 rc 0, 226 NOT RUN with reasons; 39 tree-after receipts with empty status.')
for point in ('A1','A8','B1','B8','N1','N8','W1','W8'):
    for suffix in ('cmp.rc','sample.rc','regrade.rc'):
        assert (r/f'gates/harness/{point}-{suffix}').read_text().strip()=='0'
    assert 'image loadable bytes: IDENTICAL' in (r/f'gates/harness/{point}-compare.txt').read_text()
print('Eight final harness legs: sample/compare/regrade rc 0; loadable-image comparison IDENTICAL.')
plants = srp_talker_mutants.defects(srp_mutants.Defect)
assert len(plants)==29
log = (r/'gates/workflows/mutant-counts.txt').read_text()
kills = re.findall(r'^\[ok\] (talker-[^:]+):', log, re.M)
assert Counter(kills)==Counter({d.name:2 for d in plants})
print('29 distinct Talker plants, each appears twice in the final campaign receipt (58 kills).')
for label in ('head','base'):
    for tool, source_name in [('load_grade','load_check'),('flip_grade','flip_check')]:
        ours=(packet/f'receipts/{label}-{tool}-check.log').read_text()
        theirs=(r/f'graders/{label}-{source_name}.log').read_text()
        assert ours==theirs, (label,tool)
print('Independent base/head load and row calculations exactly match four published grader logs.')
def table(label,tool,kind):
    result={}
    for line in (packet/f'receipts/{label}-{tool}-check.log').read_text().splitlines():
        if not re.match(r'^\| (?:1x1|8x8|32x32)/',line): continue
        c=[v.strip() for v in line.split('|')[1:-1]]
        if kind=='rows' and len(c)==6:
            result[(c[0],c[1])]=Decimal(c[2])
        elif kind=='loads':
            result[(c[0],'pin')]=Decimal(c[1])
            result[(c[0],'second column')]=Decimal(c[2])
    return result
for tool,kind in [('load_grade','loads'),('flip_grade','rows')]:
    base,head=table('base',tool,kind),table('head',tool,kind)
    for key,b in base.items():
        h=head[key]
        print(f'{key[0]} {key[1]}: {b} -> {h}; delta {h-b:+}')
print('Measured least-positive row margins, from published legs (not the over-budget rows):')
for arm,b,h in [('A1','11.006','11.233'),('A8','8.973','9.718'),
                ('N1','9.080','9.036'),('N8','6.246','7.879')]:
    assert f'R3-{arm}: least margin {h} ms' in (r/'costs/least-margin.txt').read_text()
    print(f'{arm}: {b} -> {h} ms; delta {Decimal(h)-Decimal(b):+} ms')
print('Base measured margins are explicitly attributed to round-29 legs in SPLIT_CONTROL_MEMORY.md:2227; raw base legs are not included in this archive.')
print('Domain probe at both points:')
for p in sorted((r/'probes/domain-refused-path').glob('run-*.log')):
    summary=next(x for x in p.read_text().splitlines() if x.startswith('PROBE summary'))
    print(p.name,summary)
print('Evidence audit PASS')
