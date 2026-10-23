#!/usr/bin/env python3
"""Reconcile published receipt counts against the reviewed source inventories.

Usage: python3 fetch_receipts.py; python3 audit_receipts.py REPOSITORY
No simulation or synthesis bank is executed by this script.
"""
import ast
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()
PUB = ROOT / 'scratch/public/author-r7/receipts/round7'
out = {}

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True).strip()

def read(name):
    return (PUB / name).read_text()

def inventory(path, variable):
    tree = ast.parse((REPO / path).read_text())
    value = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == variable for t in n.targets))
    return [ast.literal_eval((n.args if isinstance(n, ast.Call) else n.elts)[0]) for n in value.elts]

out['head'] = git('rev-parse', 'HEAD')
assert out['head'] == '417ec52864efc09f1e3ecd0f755cb0daa7604426'
for path, var, log in [
    ('tb/verilator/milan_dp_render/tdm8_render_mutants.py', 'MUTATIONS', 'tdm8render_mutants_d835ba12/tdm8render-campaign.log'),
    ('tb/verilator/milan_dp_render/tdm8_render_mutants.py', 'CLEAN_CONTROLS', 'tdm8render_mutants_d835ba12/tdm8render-campaign.log'),
    ('tb/verilator/milan_dp_render/tdm8_render_mutants.py', 'LEG_DEFECTS', 'tdm8render_mutants_d835ba12/tdm8render-campaign.log'),
    ('tb/verilator/milan_dp_gm_steps/gmstep_mutants.py', 'CONTROLS', 'gmstep_mutants_c2c996fa/gmstep-campaign.log'),
]:
    lines = read(log).splitlines()
    rows = []
    for name in inventory(path, var):
        passes = [s for s in lines if name in s and '[PASS]' in s]
        fails = [s for s in lines if name in s and '[FAIL]' in s]
        assert passes and not fails, (name, log)
        rows.append({'name': name, 'pass_lines': passes})
    out[var if var != 'CONTROLS' else 'GMSTEP_CONTROLS'] = {'source': path, 'receipt': log, 'count': len(rows), 'rows': rows}
assert [out[k]['count'] for k in ('MUTATIONS', 'CLEAN_CONTROLS', 'LEG_DEFECTS', 'GMSTEP_CONTROLS')] == [20, 3, 3, 21]

out['pullin'] = []
for p in sorted((PUB / 'pullin_d835ba12').glob('pullin_*.log')):
    text = p.read_text()
    counts = re.findall(r'checks:\s*(\d+)\s+failures:\s*(\d+)', text)
    assert counts and counts[-1][1] == '0' and 'RESULT: PASS' in text, p.name
    out['pullin'].append({'file': p.name, 'phases': sorted(set(re.findall(r'T647 PULLIN (\+\d+)', text))), 'checks': int(counts[-1][0]), 'failures': 0})
assert len(out['pullin']) == 19

out['sweep'] = []
for i in range(4):
    text = read(f'sweep_c2c996fa/shard{i}/summary.txt')
    suites, passed, failed, timeout = map(int, re.search(r'suites:\s*(\d+)\s+passed:\s*(\d+)\s+failed:\s*(\d+)\s+timed out:\s*(\d+)', text).groups())
    checks, failures = map(int, re.search(r'checks:\s*(\d+)\s+in-suite failures:\s*(\d+)', text).groups())
    out['sweep'].append(dict(shard=i, suites=suites, passed=passed, failed=failed, timeout=timeout, checks=checks, failures=failures))
out['sweep_total'] = {k: sum(r[k] for r in out['sweep']) for k in ('suites', 'passed', 'failed', 'timeout', 'checks', 'failures')}
assert out['sweep_total'] == dict(suites=64, passed=63, failed=0, timeout=1, checks=2190061, failures=0)

baseline = json.loads((REPO / 'syn/ooc/pp_resource_baseline.json').read_text())
dev = json.loads(git('show', 'e5b480a3:syn/ooc/pp_resource_baseline.json'))
out['resources'] = {}
for endpoint in ('route-1x1', 'ooc-1x1', 'ooc-8x8'):
    recorded = baseline['endpoints'][endpoint]['record']
    receipt = json.loads(read(f'vivado_bank_5282b8b6_r7b/{endpoint}-record.json'))
    assert recorded == receipt, endpoint
    if endpoint.startswith('ooc'):
        assert {k: v for k, v in recorded.items() if k != 'inputs_sha256'} == {k: v for k, v in dev['endpoints'][endpoint]['record'].items() if k != 'inputs_sha256'}, endpoint
    out['resources'][endpoint] = {'receipt_matches': True, 'figures': recorded['figures'], 'inputs_sha256': recorded['inputs_sha256'], 'unchanged_dev_figures': recorded['figures'] == dev['endpoints'][endpoint]['record']['figures'], 'changed_record_fields_from_dev': [k for k, v in recorded.items() if v != dev['endpoints'][endpoint]['record'].get(k)]}
out['post_d835_hardware_diff'] = git('diff', '--name-only', 'd835ba12..HEAD', '--', 'hdl', 'syn', 'configs')
assert out['post_d835_hardware_diff'] == ''
result = subprocess.run([sys.executable, str(REPO / 'syn/ooc/pp_resource_gate.py'), 'check-baseline'], cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out['check_baseline'] = {'rc': result.returncode, 'output': result.stdout}
assert result.returncode == 0
(ROOT / 'audit-receipts.json').write_text(json.dumps(out, indent=2) + '\n')
print('PASS: inventories 20 render mutations, 3 clean skew controls, 3 leg defects, 21 GM-step controls; 19 pull-in logs; sweep 63/64, 2190061 checks, zero failures; three resource records; test-only repair; baseline check.')
