"""Replay assigned reviewer probes in this lane, restoring mutation bytes."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

ROOT = Path('$LANES/582-baremetal-clock')
OUT = Path(__file__).resolve().parent
R354 = Path('$REVIEWS/582-r354-2-packet')
R355 = Path('$REVIEWS/582-r355-2-packet')
START = '77998f14b16bf7605956332d0f0ac8af0cecab5a'
assert Path.cwd().resolve() == ROOT
(OUT / 'probes').mkdir(exist_ok=True)
results = []


def run(name, command, expected=0, required=(), stdin=None):
    with tempfile.TemporaryDirectory(prefix='582-r3-cache-') as cache:
        env = {**os.environ, 'PYTHONPYCACHEPREFIX': cache}
        proc = subprocess.run(command, cwd=ROOT, env=env, input=stdin,
                              capture_output=True, text=True, timeout=1800)
    output = proc.stdout + proc.stderr
    raw = output.encode()
    assert len(raw) <= 200_000, (name, len(raw))
    log = OUT / 'probes' / f'{name}.log'
    log.write_bytes(raw)
    record = dict(name=name, command=command, returncode=proc.returncode,
                  expected=expected, size=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                  log=str(log.relative_to(OUT)))
    results.append(record)
    (OUT / 'probe-results.json').write_text(json.dumps(results, indent=2) + '\n')
    assert proc.returncode == expected, (name, proc.returncode, output[-4000:])
    for token in required:
        assert token in output, (name, token, output[-4000:])
    print(f'PASS {name}: rc {proc.returncode}; expected {expected}', flush=True)
    return output


# Load the reviewer's exact mutation declarations; do not run its copy loop.
source = R355 / 'scripts/30_mutants.py'
tree = ast.parse(source.read_text())
prefix = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == 'restore':
        break
    prefix.append(node)
scope = {'__file__': str(source)}
with patch.object(sys, 'argv', [str(source), str(ROOT), str(ROOT), sys.executable]):
    exec(compile(ast.Module(body=prefix, type_ignores=[]), str(source), 'exec'), scope)

selected = {'C1', 'C4', 'C5', 'S9', 'R1', 'R2'}
for label, rel, old, new, command, cwd in scope['MUTANTS']:
    key = label.split()[0]
    if key not in selected:
        continue
    assert cwd == '.'
    path = ROOT / rel
    original = path.read_bytes()
    try:
        text = original.decode()
        assert text.count(old) == 1, (key, text.count(old))
        path.write_text(text.replace(old, new))
        control = key.startswith('C')
        diagnostic = ('clock accepted before platform' if key == 'S9'
                      else 'gPTP ROM does not use configured Milan clock')
        run(key, command, 0 if control else 1, () if control else (diagnostic,))
        print(f'{"CONTROL-PASS" if control else "KILLED"} {label}', flush=True)
    finally:
        path.write_bytes(original)
    assert path.read_bytes() == original

# Probe 39 deliberately reports assertions in text, so grade the text too.
with tempfile.TemporaryDirectory(prefix='582-equal-clock-') as scratch:
    run('equal-clocks', [sys.executable, str(R355 / 'scripts/39_rom_test_equal_clocks.py'),
                        str(ROOT), scratch], required=(
        'builder accepts the variant:', 'SKIP system-clock control: sys_clk_hz == milan_clk_hz',
        'test_gptp_rom_clock: PASS'))

run('usage-defaults', [sys.executable, str(R354 / 'scripts/soc_usage_probe.py'), START],
    required=('non-help keyword differences: none', 'failures=0'))
help_text = run('no-milan-help', [sys.executable, 'sw/litex/milan_soc.py', '--help'])
help_text = ' '.join(help_text.split())
assert 'CLI smoke path only; cannot finish a bare-metal image because firmware requires the Milan entity' in help_text

# Replay the classification inputs from the reviewer's script without pipelines.
for name, page, verdict in (
        ('tap-classification', 'docs/AAF_LATENCY_TAPS.md', 'true'),
        ('plain-doc-control', 'docs/README.md', 'false')):
    answer = run(name, [sys.executable, 'scripts/ci_scope.py'], stdin=page + '\n')
    assert answer.strip() == verdict, (page, answer)

policy = (ROOT / 'docs/testing/CI_WORKFLOWS.md').read_text()
table = policy.split('| Reader |', 1)[1].split('\n\n', 1)[0]
assert 'test_clock_contract.py' not in table and 'AAF_LATENCY_TAPS.md' not in table
assert 'Its reader is absent from `DOCS_JOB_PY`.' in policy
assert 'The tap page remains relevant under the #582 decision.' in policy
print('FIXED F1/SG5: tap page is relevant, outside the documentation-only table; reader exclusion explicit')
print('FIXED SG1: help and documented smoke-path limitation agree; defaults unchanged')
print('FIXED SG7: accepted equal-clock variant passes and reports only the system-control skip')
print('PASS: mutation sources restored; all assigned probes meet their expected results')
