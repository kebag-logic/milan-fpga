"""R296-3: rerun the four stream-gate BDD mutants against a copy of the head.

Usage: MILAN_SOURCE=<clone at head> PACKET=<packet dir> python3 bdd_mutants.py
Copies only the files the licence feature reads into PACKET/scratch, mutates
the single lwsrp_stream_gate assignment there, and never writes the clone.
Receipts: PACKET/receipts/bdd-<arm>.log.
"""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

SOURCE = Path(os.environ['MILAN_SOURCE']).resolve()
PACKET = Path(os.environ['PACKET']).resolve()
FILES = (
    'tests/features/milan_streaming_licence.feature',
    'tests/steps/milan_streaming_licence_steps.py',
    'tests/behave.ini',
    'tests/environment.py',
    'hdl/milan/milan_datapath.sv',
    'hdl/ieee1722/aaf/KL_aaf_packetizer.sv',
    'docs/testing/MILAN_V12_AUDIT_2026-08-16.md',
)
ACTIVE = 'pp_cd_srp_active_w[SRP_TALKERS_C-1:0]'
GRANT = 'pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0]'
MUTANTS = {
    'active-only': ACTIVE,
    'raw-grant-only': GRANT,
    'or': f'{ACTIVE} | {GRANT}',
    'extra-term': f'{ACTIVE} & {GRANT} & cfg_lwsrp_enable',
}
SIGNATURE = ('lwsrp_stream_gate must be ACTIVE AND the per-source real grant '
             'and nothing else')
PATTERN = r'(\bassign\s+lwsrp_stream_gate\s*=\s*)([^;]+)(;)'


def run_arm(root, name, expect_fail):
    log = PACKET / 'receipts' / f'bdd-{name}.log'
    with log.open('w') as stream:
        result = subprocess.run(
            [sys.executable, '-m', 'behave', '--no-capture', '-f', 'plain',
             'features/milan_streaming_licence.feature'],
            cwd=root / 'tests', text=True, stdout=stream,
            stderr=subprocess.STDOUT, timeout=300)
    out = log.read_text()
    summary = re.search(r'(\d+) scenarios? passed, (\d+) failed', out)
    passed, failed = (int(summary[1]), int(summary[2])) if summary else (-1, -1)
    if expect_fail:
        ok = result.returncode != 0 and failed == 1 and SIGNATURE in out
    else:
        ok = result.returncode == 0 and failed == 0 and passed > 0
    print(f'{name}: rc={result.returncode} passed={passed} failed={failed} '
          f'{"PASS" if ok else "FAIL"}', flush=True)
    return ok


before = {f: (SOURCE / f).read_bytes() for f in FILES}
root = PACKET / 'scratch' / 'bdd-mutant-tree'
shutil.rmtree(root, ignore_errors=True)
for rel, data in before.items():
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_bytes(data)
target = root / 'hdl/milan/milan_datapath.sv'
original = target.read_text()
matches = list(re.finditer(PATTERN, original))
assert len(matches) == 1, 'expected exactly one gate assignment'
assert re.sub(r'\s+', '', matches[0][2]) == f'{ACTIVE}&{GRANT}'
results = [run_arm(root, 'clean-before', False)]
for name, expr in MUTANTS.items():
    changed, count = re.subn(PATTERN, lambda m: m[1] + expr + m[3], original)
    assert count == 1 and changed != original
    target.write_text(changed)
    results.append(run_arm(root, name, True))
target.write_text(original)
results.append(run_arm(root, 'clean-after', False))
assert all((SOURCE / f).read_bytes() == d for f, d in before.items()), \
    'source clone changed'
if all(results):
    print('RESULT PASS: 4/4 mutants caught; clean arms pass before and after')
else:
    print('RESULT FAIL')
    sys.exit(1)
