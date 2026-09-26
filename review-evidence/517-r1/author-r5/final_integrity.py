import hashlib
import json
import subprocess
from pathlib import Path
from run_gate import OUT, ROOT, run


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', *args], cwd=cwd, text=True).strip()


head = git('rev-parse', 'HEAD')
assert head == '1d694677c8f376ec44e3b59b1d7fa7abccda106b'
assert git('branch', '--show-current') == '517-bounded-simulation-pool'
origin = git('remote', 'get-url', 'origin')
assert origin == 'https://github.com/kebag-logic/milan-fpga.git'
status = git('status', '--porcelain=v1')
assert not status, status
assert not git('diff', '--cached', '--name-only', 'HEAD')
message = git('log', '-1', '--format=%B')
assert len(message.splitlines()) == 1, message
changed = git('diff', '--name-only', 'HEAD^', 'HEAD').splitlines()
expected = [
    'docs/testing/TESTING.md', 'tb/verilator/milan_dp/Makefile',
    'tb/verilator/milan_dp/README.md', 'tb/verilator/milan_dp/sim_nxn.cpp',
    'tb/verilator/milan_dp/sim_pool.py', 'tb/verilator/milan_dp/test_sim_pool.py',
    'tb/verilator/milan_dp/test_sim_pool_backpressure.py',
]
assert changed == expected, changed
submodules = []
for line in (OUT / 'initial-submodules.txt').read_text().splitlines():
    old, relative, *_ = line.split()
    location = ROOT / relative
    now = git('rev-parse', 'HEAD', cwd=location)
    substatus = git('status', '--porcelain=v1', cwd=location)
    assert now == old and not substatus, (relative, old, now, substatus)
    submodules.append(dict(path=relative, head=now, clean=True))
probe = Path('/tmp/517-a324-evidence/review-evidence/517-r1/reviews/R246-1/scripts/integrity.py')
assert run('reviewer-integrity', ['python3', str(probe), str(ROOT), head]) == 0
verdict = (OUT / 'reviewer-integrity.log').read_text()
assert 'INTEGRITY: PASS' in verdict and 'mismatches: 0' in verdict
assert run('final-diff-check', ['git', 'diff', '--check']) == 0
assert run('commit-diff-check', ['git', 'diff', '--check', 'HEAD^', 'HEAD']) == 0
hashes = json.loads((OUT / 'public-probe-hashes.json').read_text())
base = probe.parents[2]
for relative, expected_hash in hashes.items():
    actual = hashlib.sha256((base / relative).read_bytes()).hexdigest()
    assert actual == expected_hash, relative
(OUT / 'public-probes-unchanged.json').write_text(json.dumps(dict(
    source_commit='f0ff6b8f51b6f1da6b1f9d37f3bf2feb9f369576',
    verified=len(hashes), unchanged=True), indent=2)+'\n')
body = json.loads(subprocess.check_output(['gh', 'pr', 'view', '524', '--repo',
                  'kebag-logic/milan-fpga', '--json', 'body'], text=True))['body']
assert body == (OUT / 'PR-ORIGINAL.md').read_text(), 'PR body changed during validation; reconcile it before handoff'
result = dict(head=head, branch=git('branch', '--show-current'), origin=origin,
              clean=True, index_matches_head=True, commit_subject=message,
              changed=changed, submodules=submodules, public_probe_hashes_unchanged=True,
              current_pr_body_matches_saved_original=True)
(OUT / 'final-integrity.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result), flush=True)
