"""Foreground assigned gates, raw file receipts, and unchanged-case comparison."""
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
REPO = Path('$LANES/514-containment-retention')
BASE = '3d2f3e3131c9db5898e1db9dd3e2a35149843109'
GATES = [
    ('selftest', ['python3', 'scripts/check_merge_containment.py', '--selftest'], {}),
    ('linear', ['python3', '-B', str(OUT / 'run_linear.py'), str(REPO / 'scripts')], {}),
    ('docs-git', ['python3', 'scripts/docs_check.py'], {}),
    ('docs-no-git', ['python3', 'scripts/docs_check.py'], {'GIT_DIR': '/dev/null'}),
    ('em-dash', ['python3', 'scripts/check_em_dash.py', '--base', BASE], {}),
    ('doc-style', ['python3', 'scripts/check_doc_style.py'], {}),
    ('toc', ['python3', 'scripts/gen_toc.py', '--check'], {}),
    ('anchors', ['python3', 'scripts/gen_toc.py', '--verify-anchors'], {}),
    ('doc-paths', ['python3', 'scripts/check_doc_paths.py'], {}),
    ('python-idiom', ['python3', 'scripts/check_py_idiom.py'], {}),
    ('diff-check', ['git', 'diff', '--check'], {}),
    ('diff-check-base', ['git', 'diff', '--check', BASE, 'HEAD'], {}),
]
(OUT / 'gates').mkdir(exist_ok=True)
rows = []
for name, argv, extra_env in ([] if '--compare-only' in sys.argv else GATES):
    started = time.monotonic()
    log = OUT / 'gates' / (name + '.log')
    command = shlex.join(argv)
    print('START', name, command, flush=True)
    with log.open('w') as stream:
        result = subprocess.run(argv, cwd=REPO, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', **extra_env),
                                stdout=stream, stderr=subprocess.STDOUT, timeout=1800)
    row = dict(gate=name, command=command, env=extra_env, rc=result.returncode,
               seconds=round(time.monotonic()-started, 2), log=str(log.relative_to(OUT)))
    rows.append(row)
    (OUT / 'gates.json').write_text(json.dumps(rows, indent=2) + '\n')
    print('DONE', name, 'rc=' + str(result.returncode), row['seconds'], flush=True)
    if result.returncode:
        print(log.read_text())
        sys.exit(result.returncode)

after = (OUT / 'gates/selftest.log').read_text().splitlines()
new_cases = [line for line in after if line.startswith('  ok')]
comparisons = []
for reviewer, filename in [('R292-1', 'selftest-head.log'), ('R293-1', 'head-selftest.log'),
                           ('R292-1', 'selftest-base.log')]:
    prior = (OUT / 'before' / reviewer / filename).read_text().splitlines()
    old_cases = [line for line in prior if line.startswith('  ok')]
    remaining = iter(new_cases)
    unchanged = all(any(line == candidate for candidate in remaining) for line in old_cases)
    assert unchanged and old_cases
    comparisons.append(dict(reviewer=reviewer, file=filename, before=len(old_cases),
                            after=len(new_cases), unchanged_in_order=unchanged))
assert 'selftest: PASS' in after and not any(line.lstrip().startswith('FAIL') for line in after)
(OUT / 'case-comparison.json').write_text(json.dumps(comparisons, indent=2) + '\n')
print('CASE COMPARISON', comparisons, flush=True)
