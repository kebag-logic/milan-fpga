#!/usr/bin/env python3
"""Plant three missing grader guards in memory and ask the advertised self-test to detect them.
Usage: python3 -I probe_selftest_coverage.py CHECKOUT PACKET
No repository file is modified. Exit 1 means at least one plant escaped.
"""
from pathlib import Path
import sys

root, packet = (Path(p).resolve() for p in sys.argv[1:])
target = root/'tb/verilator/ctrl_service_budget/kept_grade.py'
text = target.read_text()
plants = [('no-build-over-cost-finding', "for o in builds['over'] if o['kind'] != 'step']", "for o in builds['over'] if False]"),
          ('no-missing-json-finding', "if not (results / f'{name}.log').is_file()]",  # adapted: the standalone guard is now the absent log's
           'if False]'),
          ('no-paired-group-requirement', 'if len(self.ran) < len(OWED_KINDS):', 'if False:')]
lines = []
escaped = 0
for name, old, new in plants:
    assert text.count(old) == 1
    ns = dict(__file__=str(target), __name__='review_mutant')
    exec(compile(text.replace(old, new), str(target), 'exec'), ns)
    checks = ns['selftest']()
    survived = all(ok for _, ok, _ in checks)
    escaped += survived
    lines.append(f'{name}: {"ESCAPED" if survived else "CAUGHT"}; {sum(ok for _, ok, _ in checks)}/{len(checks)} self-tests pass')
(packet/'receipts/selftest-coverage-probes.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
sys.exit(int(bool(escaped)))
