#!/usr/bin/env python3
"""Reconcile round-8 receipts with the reviewed campaign and workflow."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
P = ROOT / 'public-round8'
HEAD = '24a292a0321df6f3516f25cb6e92e24fb1988e65'

def inventory(path, name):
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return node.value.elts
    raise AssertionError(name)

def main():
    repo = Path(sys.argv[1]).resolve()
    docs = P / 'docs_steps_24a292a0'
    summary = {}
    for directory, count in [('docs', 44), ('docs-md312', 5), ('docs-leg1-litex', 1)]:
        ledger = json.loads((docs / directory / 'receipts.json').read_text())
        assert ledger['head'] == ledger['head_after'] == HEAD
        assert len(ledger['steps']) == count
        ran = [s for s in ledger['steps'] if s['rc'] is not None]
        skipped = [s for s in ledger['steps'] if s['rc'] is None]
        assert all(s['rc'] == 0 and s['make'] == 'GNU Make 4.3' for s in ran)
        if directory != 'docs':
            assert all(s['python'] == 'Python 3.12.3' for s in ran)
        summary[directory] = {'head': HEAD, 'executed_pass': len(ran), 'skipped': skipped}
    original = json.loads((docs / 'docs/receipts.json').read_text())['steps']
    rerun = json.loads((docs / 'docs-md312/receipts.json').read_text())['steps']
    required_reruns = {(s['job'], s['id']) for s in original if s.get('python') not in (None, 'Python 3.12.3')}
    assert required_reruns == {(s['job'], s['id']) for s in rerun}
    assert (docs / 'docs-nogit/nogit_summary.txt').read_text() == 'docs_check rc=0\nfeature_status rc=0\n'
    for directory in ['legs_24a292a0', 'lint_24a292a0', 'dynmap_mutants_24a292a0']:
        assert (P / directory / 'HEAD.txt').read_text().strip() == HEAD
    for leg, verdict in [('gptp', '185 checks: 185 PASS, 0 FAIL'), ('ax1x1gptp', '== ax1x1gptp physical: checks: 155   failures: 0 ==')]:
        assert (P / 'legs_24a292a0' / (leg + '.rc')).read_text().strip() == '0'
        assert verdict in (P / 'legs_24a292a0' / (leg + '.log')).read_text()
        summary[leg] = verdict
    assert 'LINT GATE: PASS (89 violation(s) <= ratchet 89;' in (P / 'lint_24a292a0/lint.log').read_text()
    assert (P / 'dynmap_mutants_24a292a0/rc').read_text().strip() == '0'
    log = (P / 'dynmap_mutants_24a292a0/log').read_text()
    mutations = inventory(repo / 'tb/verilator/milan_dp/dynmap_mutants.py', 'MUTATIONS')
    names = [ast.literal_eval(m.elts[1]) for m in mutations]
    legs = sorted({ast.literal_eval(m.elts[0]) for m in mutations})
    assert len(names) == len(set(names)) == 63
    assert len(legs) == 5
    for name in names:
        assert log.count('[PASS] mutant caught: ' + name + ' - breaks ') == 1, name
    for leg in legs:
        assert log.count('[PASS] the unmutated gateware still passes the ' + leg + ' leg') == 1
    assert '68 checks: 68 PASS, 0 FAIL' in log
    summary['dynmap'] = {'controls_caught': len(names), 'clean_legs': legs, 'total': 68, 'all_named_results_present': True}
    controls = inventory(repo / 'tb/verilator/milan_dp_gm_steps/gmstep_mutants.py', 'CONTROLS')
    assert len(controls) == 21
    summary['gmstep'] = {'current_controls': len(controls), 'clean_legs': 2, 'total': 23, 'execution': 'unchanged round-4 coverage carried forward'}
    summary['lint'] = '89 violations <= ratchet 89; rc 0'
    summary['no_git'] = 'both archive-export checks rc 0'
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
