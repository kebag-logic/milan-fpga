"""Reproduce the four assigned BDD controls without changing the source tree.

Run from the output directory with MILAN_SOURCE pointing at the candidate.
All copied source files live in a temporary directory outside the receipts.
"""
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

SOURCE = Path(os.environ['MILAN_SOURCE']).resolve()
OUT = Path(__file__).resolve().parent.parent
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
SIGNATURE = 'lwsrp_stream_gate must be ACTIVE AND the per-source real grant and nothing else'


def run_arm(root, name, expected_rc):
    log = OUT / 'receipts' / f'bdd-{name}.log'
    with log.open('w') as stream:
        result = subprocess.run(
            ['rtk', 'proxy', sys.executable, '-m', 'behave', '--no-capture',
             '-f', 'plain', 'features/milan_streaming_licence.feature'],
            cwd=root / 'tests', text=True, stdout=stream,
            stderr=subprocess.STDOUT, timeout=300,
        )
    output = log.read_text()
    expected_summary = ('5 scenarios passed, 0 failed' if expected_rc == 0
                        else '4 scenarios passed, 1 failed')
    ok = result.returncode == expected_rc and expected_summary in output
    if expected_rc:
        ok = ok and SIGNATURE in output
    print(f'{name}: rc={result.returncode}, '
          f'{"PASS" if ok else "FAIL"} ({expected_summary})', flush=True)
    if not ok:
        print(output)
        raise SystemExit(1)


original_bytes = {name: (SOURCE / name).read_bytes() for name in FILES}
with tempfile.TemporaryDirectory(prefix='milan-551-bdd-', dir='/tmp') as name:
    root = Path(name)
    for relative, data in original_bytes.items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    target = root / 'hdl/milan/milan_datapath.sv'
    original = target.read_text()
    pattern = r'(\bassign\s+lwsrp_stream_gate\s*=\s*)([^;]+)(;)'
    matches = list(re.finditer(pattern, original))
    assert len(matches) == 1, 'expected exactly one gate assignment'
    assert re.sub(r'\s+', '', matches[0][2]) == f'{ACTIVE}&{GRANT}'
    run_arm(root, 'clean-before', 0)
    for name, expression in MUTANTS.items():
        changed, count = re.subn(
            pattern, lambda match: match[1] + expression + match[3], original)
        assert count == 1 and changed != original
        target.write_text(changed)
        run_arm(root, name, 1)
    target.write_text(original)
    run_arm(root, 'clean-after', 0)
assert all((SOURCE / name).read_bytes() == data
           for name, data in original_bytes.items()), 'source tree changed'
print('PASS: all four mutants caught; clean controls pass before and after.')
