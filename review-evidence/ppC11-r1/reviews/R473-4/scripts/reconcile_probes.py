#!/usr/bin/env python3
"""Post-verdict verification of exact prior findings and optional follow-ups."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--scratch', type=Path, required=True)
a = p.parse_args()
def run(cmd):
    r = subprocess.run(cmd, cwd=a.source, text=True, capture_output=True)
    return r.returncode, r.stdout + r.stderr
failures = 0
probe = a.source / 'tb/reviewer-reconciliation-probe.md'
assert not probe.exists()
try:
    for name, body, token in [
        ('round1-braces', 'T-NVM-{RS-DEADLINE, RS-TYPO}', 'T-NVM-RS-TYPO'),
        ('round1-prose-suffix', 'P-TX-shaped', 'P-TX'),
        ('round2-composition', 'T-ADP-\n// DELAY(-STRT)', 'T-ADP-DELAY-STRT'),
        ('round2-healthy-composition', 'T-ADP-\n// DELAY(-START)', None),
        ('round2-missing-base', 'P-REVIEWER-MISSING-1', 'P-REVIEWER-MISSING-1'),
    ]:
        probe.write_text(body)
        direct_rc, direct = run([sys.executable, 'scripts/check-ids.py'])
        make_rc, make = run(['make', '-j16', 'ids'])
        good = (direct_rc, make_rc) == ((1, 2) if token else (0, 0))
        good = good and (token is None or (token in direct and token in make))
        failures += not good
        print(json.dumps({'case': name, 'body': body, 'direct_rc': direct_rc, 'make_rc': make_rc,
                          'pass': good, 'direct': direct, 'make': make}))
finally:
    probe.unlink()
with tempfile.TemporaryDirectory(dir=a.scratch, prefix='reconciliation-') as td:
    temp = Path(td)
    figure = (a.source / 'scripts/check-figures.py').read_text()
    mutants = {
        'no-foreignObject': figure.replace('for tag in ("image", "feImage", "foreignObject"):',
                                           'for tag in ("image", "feImage"):'),
        'no-root-namespace': figure.replace('if svg.tag != f"{SVG_NS}svg":', 'if False:'),
        'empty-inventory-accepted': figure.replace('if not names:', 'if False:'),
        'missing-inventory-heading-accepted': figure.replace('if at < 0:', 'if False:'),
        'no-feImage': figure.replace('for tag in ("image", "feImage", "foreignObject"):',
                                     'for tag in ("image", "foreignObject"):'),
    }
    for name, body in mutants.items():
        assert body != figure
        path = temp / (name + '.py')
        path.write_text(body)
        rc, output = run([sys.executable, str(path), '--selftest'])
        good = rc == 1 and 'SELFTEST FAIL:' in output
        failures += not good
        print(json.dumps({'mutation': name, 'rc': rc, 'killed': good, 'stdout': output}))
    ids = (a.source / 'scripts/check-ids.py').read_text()
    path = temp / 'one-continuation-only.py'
    path.write_text(ids.replace('while broken:', 'if broken:'))
    rc, output = run([sys.executable, str(path), '--selftest'])
    assert rc == 0  # existing optional coverage limitation, not an acceptance failure
    probe.write_text('T-ADP-\n// DELAY-\n// STRT')
    try:
        healthy_rc, healthy = run([sys.executable, 'scripts/check-ids.py'])
        mutant_rc, mutant = run([sys.executable, str(path), '--root', str(a.source)])
        assert healthy_rc == 1 and mutant_rc == 0
        print(json.dumps({'suggestion': 'successive-continuation-negative-plant',
                          'selftest_rc': rc, 'selftest': output,
                          'healthy_rc': healthy_rc, 'healthy': healthy,
                          'mutant_rc': mutant_rc, 'mutant': mutant}))
        for body in ['T-BUDGET-AECP-TYP /\n-XX', 'T-BUDGET-AECP-TYP\n/ -XX',
                     'T-BUDGET-AECP-TYP / -\nXX', 'T-ADP-DELAY\n(-STRT)']:
            probe.write_text(body)
            rc, output = run([sys.executable, 'scripts/check-ids.py'])
            assert rc == 0
            print(json.dumps({'suggestion': 'whitespace-wrap-outside-current-grammar',
                              'body': body, 'rc': rc, 'stdout': output}))
    finally:
        probe.unlink()
print(f'Prior-finding verification failures: {failures}')
raise SystemExit(bool(failures))
