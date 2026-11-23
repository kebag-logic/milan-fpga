#!/usr/bin/env python3
"""cost_compare.py ROOT BASE HEAD OUT: per point, the most measured of each cost the harness grades, over every group of
every arm both trees ran (ROOT/<tree>/<point>/<arm>/g/<group>/results.json and its log): each poll item's heaviest
(poll_grade), each pass given whole (whole_grade), THE RETRY's heaviest round, each tier-2 slice's longest, the
longest work pass, and the longest record of each channel's handler (SPAN lines of <module>:frame, receive and their
kin, the testbench's record spans), with where each was measured. Writes OUT/costs.json and OUT/costs.txt (base, head,
head/base) and prints the table. Read only."""
import collections
import json
import sys
from pathlib import Path

root, base, head, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])


def measure(tree: str, both: set) -> dict:
    most = collections.defaultdict(lambda: (0, ''))

    def note(point, key, cycles, at):
        k = (point, key)
        if cycles > most[k][0]:
            most[k] = (cycles, at)
    for run in sorted((root / tree).glob('*/*/g/*')):
        point, arm, group = run.parts[-4], run.parts[-3], run.parts[-1]
        if (point, arm, group) not in both:
            continue
        g = next(x for x in json.loads((run / 'results.json').read_text())['results'] if x['group'] == group)
        p, at = g.get('passes', {}), f'{arm}/{group}'
        for k, v in p.get('polls', {}).get('heaviest', {}).items():
            note(point, f'poll.{k}', v, at)
        for k, v in p.get('stated', {}).get('heaviest', {}).items():
            note(point, f'whole.{k}', v, at)
        for v in p.get('rounds', {}).get('heaviest', {}).values():
            note(point, 'round', v, at)
        for k, v in p.get('slices', {}).get('longest', {}).items():
            note(point, f'slice.{k}', v, at)
        note(point, 'pass.longest', p.get('worst', {}).get('cycles') or 0, at)
        with open(run / f'{group}.log', errors='replace') as f:
            for line in f:
                if line.startswith('SPAN '):
                    parts = line.split()
                    name = parts[-1]
                    if name.endswith((':frame', ':receive', ':on_frame', ':apply_receive')):
                        note(point, f'record.{name}', int(parts[3]), at)
    return most


def runs(tree: str) -> set:
    return {(r.parts[-4], r.parts[-3], r.parts[-1]) for r in (root / tree).glob('*/*/g/*') if (r / 'results.json').is_file()}


both = runs(base) & runs(head)
a, b = measure(base, both), measure(head, both)
out.mkdir(parents=True, exist_ok=True)
rows, lines = [], []
for point in sorted({k[0] for k in a} | {k[0] for k in b}):
    n = sum(1 for x in both if x[0] == point)
    lines.append(f'== {point}: {n} groups both ran')
    lines.append(f'{"cost":<34} {"base":>9} {"head":>9} {"head/base":>9}  where (base | head)')
    for key in sorted({k[1] for k in a if k[0] == point} | {k[1] for k in b if k[0] == point}):
        x, y = a[(point, key)], b[(point, key)]
        ratio = f'{y[0] / x[0]:.3f}' if x[0] else '-'
        lines.append(f'{key:<34} {x[0]:>9,} {y[0]:>9,} {ratio:>9}  {x[1]} | {y[1]}')
        rows.append(dict(point=point, cost=key, base=x[0], head=y[0], base_at=x[1], head_at=y[1]))
(out / 'costs.json').write_text(json.dumps(rows, indent=1) + '\n')
(out / 'costs.txt').write_text('\n'.join(lines) + '\n')
print('\n'.join(lines))
