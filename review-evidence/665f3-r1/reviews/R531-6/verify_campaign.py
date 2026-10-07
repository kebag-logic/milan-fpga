#!/usr/bin/env python3
"""Prove exact, disjoint campaign population and preservation of earlier fixtures."""
import argparse
import dataclasses
import json
from pathlib import Path
import re
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path)
ap.add_argument('--catalog-only', action='store_true')
a = ap.parse_args()
root = a.root.resolve()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import acmp_mutants
import acmp_review_mutants
import ctrl_mutants

old = subprocess.check_output(['git', '-C', str(root), 'show',
                              '13e71513:sw/firmware/ctrl/test/acmp_review_mutants.py'], text=True)
namespace = {}
exec(compile(old, '<round6-public-fixtures>', 'exec'), namespace)
previous = namespace['MUTANTS']
current = acmp_review_mutants.MUTANTS
assert current[:len(previous)] == previous
assert len(current) == len(previous) + 4
names = [m.name for m in ctrl_mutants.MUTANTS]
assert len(names) == len(set(names)) == 469
assert not ctrl_mutants.unnamed_tests()
assert len(acmp_mutants.MUTANTS) == 273
receipt = dict(catalog_total=len(names), acmp_total=len(acmp_mutants.MUTANTS),
               unchanged_prior_review_fixtures=len(previous),
               added=[dataclasses.asdict(m) for m in current[len(previous):]],
               unnamed_tests=ctrl_mutants.unnamed_tests())
if not a.catalog_only:
    all_caught = []
    slices = []
    for i in range(3):
        text = (packet / f'campaign-{i}.log').read_text()
        assert int((packet / f'campaign-{i}.rc').read_text()) == 0
        assert '[ESCAPED]' not in text
        assert text.endswith('test_ctrl_firmware: PASS\n')
        caught = re.findall(r'^\[ok\] mutant (\S+) \(', text, re.M)
        expected = [m.name for m in ctrl_mutants.sliced((i+1,3))]
        assert caught == expected
        all_caught += caught
        slices.append(dict(slice=f'{i+1}/3', caught=len(caught), rc=0))
    assert sorted(all_caught) == sorted(names)
    assert len(set(all_caught)) == len(all_caught)
    receipt.update(slices=slices, complete_disjoint_union=True, caught_total=len(all_caught))
print(json.dumps(receipt, indent=2))
