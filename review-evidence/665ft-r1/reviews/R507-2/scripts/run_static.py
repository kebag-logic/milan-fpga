#!/usr/bin/env python3
"""Focused source/documentation and coverage-gate checks, joined in foreground."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
tasks = [
    ('coverage-selftest', [sys.executable, '-B', 'sw/firmware/gtest/fw_coverage.py', '--selftest']),
    ('ci-scope', [sys.executable, '-B', 'scripts/ci_scope.py', '--selftest']),
    ('ci-events-check', [sys.executable, '-B', 'scripts/ci_events.py', '--check']),
    ('ci-events-selftest', [sys.executable, '-B', 'scripts/ci_events.py', '--selftest']),
    ('docs-check', [sys.executable, '-B', 'scripts/docs_check.py']),
    ('doc-paths', [sys.executable, '-B', 'scripts/check_doc_paths.py']),
    ('cpp-idiom', [sys.executable, '-B', 'scripts/check_cpp_idiom.py']),
    ('python-idiom', [sys.executable, '-B', 'scripts/check_py_idiom.py']),
    ('diff-check', ['git', 'diff', '--check', '423ac5d910d09ab189b3acc39ae3ae1d10d50b19', 'HEAD']),
]
def run(task):
    name, argv = task
    receipts = packet/'receipts'
    (receipts/f'{name}.command').write_text(' '.join(argv)+'\n')
    with (receipts/f'{name}.log').open('w') as output:
        r = subprocess.run(argv, cwd=root, env=dict(os.environ, TMPDIR=str(packet/'scratch'),
            PYTHONDONTWRITEBYTECODE='1', PYTHON_CPU_COUNT='1'), stdout=output, stderr=subprocess.STDOUT, check=False)
    (receipts/f'{name}.rc').write_text(f'{r.returncode}\n')
    print(f'{name}: rc={r.returncode}',flush=True)
    return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,tasks))
raise SystemExit(1 if any(results) else 0)
