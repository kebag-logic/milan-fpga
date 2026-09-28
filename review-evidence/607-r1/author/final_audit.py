"""Verify the completed local handoff before publishing its author status."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

root = Path('$LANES/607-xdc-clock-names')
out = Path(__file__).resolve().parent
head = '350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75'
base = '54ce877371ee6e8878cf67294e86c2a8481b62f6'
env = dict(os.environ, GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.commitGraph',
           GIT_CONFIG_VALUE_0='false')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=root, env=env, text=True,
                                   timeout=60).strip()

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

assert root.resolve() == root
assert git('rev-parse', 'HEAD') == head
assert git('branch', '--show-current') == '607-xdc-clock-names'
assert git('remote', 'get-url', 'origin') == 'https://github.com/kebag-logic/milan-fpga.git'
assert git('merge-base', base, head) == base
assert git('status', '--porcelain', '--untracked-files=all') == ''
subprocess.run(['git', 'diff', '--check', base, head], cwd=root, env=env, check=True, timeout=60)
changed = git('diff', '--name-only', base, head).splitlines()
assert set(changed) == {
    'docs/integration/BUILDING.md', 'docs/litex/LITEX_SOC.md', 'docs/testing/RUNNING_TESTS.md',
    'sw/builder/test_builder.py', 'sw/builder/test_clock_constraints.py',
    'sw/litex/clock_constraints.py', 'sw/litex/clock_constraints.tcl',
    'sw/litex/milan_soc.py', 'sw/litex/platforms/alinx_ax7101.py',
}
commits = []
for sha in git('rev-list', base + '..' + head).splitlines():
    body = git('show', '-s', '--format=%B', sha)
    assert len(body.splitlines()) == 1, (sha, body)
    commits.append(dict(sha=sha, subject=body))
assert len(commits) == 2

gates = {row['name']: row for row in json.loads((out / 'gate-results.json').read_text())}
assert len(gates) == 81
for row in gates.values():
    assert row['head'] == head and row['rc'] == 0, row['name']
    path = Path(row['log'])
    assert path.stat().st_size == row['size'] and digest(path) == row['sha256'], row['name']

validation = json.loads((out / 'sweep-validation-result.json').read_text())
assert validation['head'] == head and validation['rc'] == 0
assert digest(Path(validation['log'])) == validation['sha256']
runs = json.loads((out / 'sweep-results.json').read_text())
summary = json.loads((out / 'sweep-summary.json').read_text())
assert {row['seed'] for row in runs} == {'asl', 'eto', 'eppo'}
assert len(runs) == len(summary) == 3
for row in runs:
    assert row['head'] == head and row['rc'] == row['report_rc'] == 0, row
    directory = Path(row['directory'])
    assert str(directory.resolve()).startswith('/data/')
    generated = (directory / 'gateware/alinx_ax7101.tcl').read_text()
    assert 'set_param general.maxThreads 16\n' in generated
    assert 'milan_eth_constraints eth_clocks0_rx ' in generated
assert 'set_param general.maxThreads 16\n' in (out / 'report_seed.tcl').read_text()
for row in summary:
    assert row['head'] == head and row['margin_ok'] and row['bound_ok']
    assert not row['critical_warnings'] and row['emitted_severity_counts']['ERROR'] == 0
    assert len(row['timing']) == 4 and len(row['crossings']) == 16

inputs = json.loads((out / 'shipping-inputs.json').read_text())
installed = json.loads((out / 'installed-constraint-source.json').read_text())
inputs += installed['files']
for row in inputs:
    path = Path(row['path'])
    assert path.stat().st_size == row['size'] and digest(path) == row['sha256'], row['path']
assert git('-C', '$WORKSPACE_HOME/litex-milan/litex', 'rev-parse', 'HEAD') == installed['revision']
verified = dict(verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                unchanged=inputs)
(out / 'read-only-verification.json').write_text(json.dumps(verified, indent=2) + '\n')

body = (out / 'PR-BODY.md').read_text()
assert body.startswith('[A408]\n') and 'Closes #607' in body and '/home/' not in body
ready = (out / 'REVIEW-READY.md').read_text()
assert ready.startswith('[A408] REVIEW READY\n') and head in ready and '/home/' not in ready
assert 'acceptance 4 remains open' not in (out / 'HANDOFF.md').read_text().lower()
for path in out.iterdir():
    assert path.is_file(), path
    assert path.stat().st_size <= 200000, path
    assert path.suffix.lower() in {'.md', '.json', '.py', '.tcl', '.txt'}, path

result = dict(head=head, base=base, branch=git('branch', '--show-current'),
              origin=git('remote', 'get-url', 'origin'), worktree_clean=True,
              all_assertions_passed=True, final_gate_count=len(gates),
              completed_seed_count=len(runs), max_threads=16,
              changed_files=changed, commits=commits, read_only_inputs_unchanged=True,
              checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(out / 'final-state.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
