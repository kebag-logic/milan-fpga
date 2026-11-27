#!/usr/bin/env python3
"""Round R957-4 probes of PR #993 (issue #977): plant each claimed defect in memory and report which path refuses it.

Usage: python3 -I probe_r957_4.py TREE
TREE is a checkout of the tree under test (its tb/verilator/ctrl_service_budget is imported). Nothing is written.
"""
import sys
from pathlib import Path
from unittest import mock

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import flip_grade  # noqa: E402
import load_grade  # noqa: E402


def failed(checks):
    return [name for name, ok, _ in checks if not ok]


def flip_check(point):
    """flip_grade --check --point POINT's findings, as main() computes them for a held-load point."""
    load = {p: c for p, c in flip_grade.FLIP.items() if p == point}
    return flip_grade.findings(flip_grade.ROOT, ceiling=load) if load else []


print(f'tree {tree}')
print(f"FLIP {flip_grade.FLIP}")
have_new = hasattr(flip_grade, 'RULED_FLIP')
print(f'post-fix names present: {have_new}')

# 1. the loads and the deliveries term at the head
for point in ('8x8/1if', '1x1/1if'):
    tot = load_grade.total(load_grade.ROOT, point) if hasattr(load_grade, 'total') else None
    print(f'{point}: DELIVERY_US {load_grade.DELIVERY_US.get(point)} us', f'load {tot}' if tot is not None else '')

# 2. the head's adapters
print('head: flip_checks failed', failed(flip_grade.flip_checks()))
print('head: ceiling_checks failed', failed(load_grade.ceiling_checks()))

# 3. the external F1 mutation: 8x8/2if 0.70 -> 0.71, through both adapters
with mock.patch.dict(flip_grade.FLIP, {'8x8/2if': 0.71}):
    print('8x8/2if at 0.71: flip controls escaped', flip_grade.controls(flip_grade.ROOT))
    print('8x8/2if at 0.71: flip_checks failed', failed(flip_grade.flip_checks()))
    print('8x8/2if at 0.71: ceiling_checks failed', failed(load_grade.ceiling_checks()))

# 4. an escape neither adapter names, planted in each adapter's own controls
with mock.patch.object(flip_grade, 'controls', lambda root, f=flip_grade.controls: [*f(root), 'probe: unnamed']):
    print('unnamed flip escape: flip_checks failed', failed(flip_grade.flip_checks()))
with mock.patch.object(load_grade, 'controls', lambda root, f=load_grade.controls: [*f(root), 'probe: unnamed']):
    print('unnamed load-gate escape: ceiling_checks failed', failed(load_grade.ceiling_checks()))

# 5. the 8x8/1if ceiling: at 0.79 (head), at 0.77 (the owner-ruled figure), and its edge
print('8x8/1if flip --check findings at the head:', flip_check('8x8/1if'))
with mock.patch.dict(flip_grade.FLIP, {'8x8/1if': 0.77}):
    print('8x8/1if flip --check findings at 0.77:', flip_check('8x8/1if'))
    print('8x8/1if at 0.77: flip controls escaped', flip_grade.controls(flip_grade.ROOT))
for edge in (0.790, 0.791, 0.78214, 0.7900001):
    print(f'over({edge}, {flip_grade.FLIP["8x8/1if"]}) = {flip_grade.over(edge, flip_grade.FLIP["8x8/1if"])}')
with mock.patch.dict(flip_grade.FLIP, {'8x8/1if': 0.80}):
    print('8x8/1if at 0.80: flip controls escaped', flip_grade.controls(flip_grade.ROOT))
if have_new:
    with mock.patch.dict(flip_grade.FLIP, {'8x8/1if': 0.80}), \
            mock.patch.dict(flip_grade.RULED_FLIP, {'8x8/1if': 0.80}):
        print('FLIP and RULED_FLIP both at 0.80: flip controls escaped', flip_grade.controls(flip_grade.ROOT))

# 6. the deliveries floor (internal F1): the measurement by the rule, a figure under it, and the head's
if hasattr(load_grade, 'DELIVERY_MEASURED'):
    for point, cyc in load_grade.DELIVERY_MEASURED.items():
        print(f'{point}: DELIVERY_MEASURED {cyc} cycles, by the rule {load_grade.rule_us(cyc)} us, '
              f'DELIVERY_US {load_grade.DELIVERY_US[point]} us')
    for point, beside in load_grade.DELIVERY_BESIDE.items():
        print(f'{point}: beside ' + ', '.join(f'{k} {v} cycles = {load_grade.rule_us(v)} us' for k, v in beside.items()))
    print('head delivery_findings', load_grade.delivery_findings(load_grade.ROOT))
    for us in (155, 159, 160):
        with mock.patch.dict(load_grade.DELIVERY_US, {'8x8/1if': us}):
            print(f'8x8/1if DELIVERY_US {us}: delivery_findings', load_grade.delivery_findings(load_grade.ROOT))
    with mock.patch.dict(load_grade.DELIVERY_US, {'1x1/1if': 195}):
        print('1x1/1if DELIVERY_US 195: delivery_findings', load_grade.delivery_findings(load_grade.ROOT))
    with mock.patch.dict(load_grade.DELIVERY_US, {'8x8/1if': 125}):
        print('8x8/1if DELIVERY_US 125 (the prior figure): delivery_findings',
              load_grade.delivery_findings(load_grade.ROOT))
import load_deliveries  # noqa: E402
print('load_deliveries.controls escaped', load_deliveries.controls(load_grade.ROOT))
print('load_grade.findings at the head', load_grade.findings(load_grade.ROOT))
