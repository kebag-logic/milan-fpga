#!/usr/bin/env python3
"""Exercise live shell definitions and hostile verdicts with disposable commands."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
root, packet = (Path(arg).resolve() for arg in sys.argv[1:3])
(packet / 'scratch').mkdir(exist_ok=True)
(packet / 'receipts').mkdir(exist_ok=True)
sys.path.insert(0, str(root / 'scripts'))
from measure_test_evidence import runner_contract

source = (root / 'scripts/run_all_suites.sh').read_text()
function = re.search(r'^suite_timeout\(\) \{\n.*?^\}', source, re.M | re.S)[0]
loop = source[source.index('run_suites() {'):source.index('\nmain() {')]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
env.pop('SUITE_TIMEOUT', None)
defaults = {'capture_coherence': 2400, 'milan_dp_mclk': 3600, 'milan_dp': 4800,
            'milan_dp_gptp': 5400, 'mmcm_servo': 1800, 'milan_dp_render': 1800,
            'capture_coherence_typo': 1800, 'milan_dp_mclk_extra': 1800}
results = []
for override in (None, '', '17', '0', '0.1'):
    current = dict(env)
    if override is not None:
        current['SUITE_TIMEOUT'] = override
    for suite, default in defaults.items():
        p = subprocess.run(['bash', '-c', function + '\nsuite_timeout "$1"', 'probe', suite],
                           env=current, text=True, capture_output=True, timeout=10)
        expected = str(default) if override in (None, '') else override
        assert p.returncode == 0 and p.stdout == expected + '\n', (suite, override, p)
        results.append(dict(probe='selection', suite=suite, override=override, result=expected))

assert runner_contract(source) == []
for old, new in [('SUITE_TIMEOUT:-2400', 'SUITE_TIMEOUT:-1800'),
                 ('SUITE_TIMEOUT:-3600', 'SUITE_TIMEOUT:-1800'),
                 ('SUITE_TIMEOUT:-4800', 'SUITE_TIMEOUT:-3600'),
                 ('SUITE_TIMEOUT:-5400', 'SUITE_TIMEOUT:-7200'),
                 ('SUITE_TIMEOUT:-1800', 'SUITE_TIMEOUT:-2400'),
                 ('capture_coherence)', 'capture_coherence_typo)'),
                 ('milan_dp_mclk)', 'milan_dp_render)'),
                 ('milan_dp)', 'milan_dp_render)'),
                 ('milan_dp_gptp)', 'milan_dp)'),
                 ('TMO=$(suite_timeout "$suite")', 'TMO=1800')]:
    assert source.count(old) == 1, (old, source.count(old))
    failures = runner_contract(source.replace(old, new))
    assert failures, old
    results.append(dict(probe='budget-mutation', old=old, new=new, rejected=failures))

with tempfile.TemporaryDirectory(dir=packet / 'scratch', prefix='limit-probes-') as directory:
    fixture = Path(directory)
    (fixture / 'scripts').mkdir()
    (fixture / 'bin').mkdir()
    for name in ('suite_tally.py', 'suite_shards.py'):
        shutil.copyfile(root / 'scripts' / name, fixture / 'scripts' / name)
    fake_timeout = fixture / 'bin/timeout'
    fake_timeout.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
assert sys.argv[2:4] == ['make', '-C']
suite = Path(sys.argv[4]).name
with open(os.environ['PROBE_CALLS'], 'a') as out:
    out.write(json.dumps({'suite': suite, 'deadline': sys.argv[1]}) + '\\n')
mode = os.environ['PROBE_MODE']
if mode == 'masked':
    print('1 checks: 0 PASS, 1 FAIL')
elif mode not in ('124', '137'):
    print('1 checks: 1 PASS, 0 FAIL')
raise SystemExit(int(mode) if mode.isdecimal() else 0)
''')
    fake_timeout.chmod(0o755)
    script = fixture / 'probe.sh'
    script.write_text('set -u\nROOT="$1"\nOUT="$2"\nSHARD=0/1\n'
                      'suites=(capture_coherence milan_dp_mclk milan_dp milan_dp_gptp mmcm_servo)\n'
                      + function + '\n' + loop + '\nrun_suites\nsummarise\n')
    for mode, expected_rc in [('pass', 0), ('124', 92), ('137', 92), ('1', 5), ('masked', 5)]:
        out = fixture / ('out-' + mode)
        out.mkdir()
        calls = fixture / ('calls-' + mode + '.jsonl')
        current = dict(env, PATH=str(fixture / 'bin') + os.pathsep + env['PATH'],
                       PROBE_MODE=mode, PROBE_CALLS=str(calls))
        p = subprocess.run(['bash', str(script), str(fixture), str(out)], env=current,
                           capture_output=True, text=True, timeout=20)
        assert p.returncode == expected_rc, (mode, p.returncode, p.stdout, p.stderr)
        measured = [json.loads(line) for line in calls.read_text().splitlines()]
        assert len(measured) == 5
        assert all(int(row['deadline']) == defaults[row['suite']] for row in measured)
        if mode in ('124', '137'):
            assert p.stdout.count('result UNKNOWN') == 5
            assert 'passed: 0   failed: 0   timed out: 5' in p.stdout
        results.append(dict(probe='loop-verdict', mode=mode, rc=p.returncode, calls=measured))
        # Receipts retain output, with disposable paths represented portably.
        (packet / 'receipts' / ('loop-' + mode + '.log')).write_text(
            (p.stdout + p.stderr).replace(str(fixture), '$PROBE_ROOT'))

(packet / 'receipts/limit-probes.json').write_text(json.dumps(results, indent=2) + '\n')
print('PASS: 40 default/empty/explicit/boundary selections; 10 armed budget mutations; 5 live loop verdict cases')
print('Loop cases: PASS, timeout 124, killed 137, failure, masked failure; all selected deadlines checked')
print('Limits: loop functions are live source; launched commands are disposable fixtures, not RTL builds')
