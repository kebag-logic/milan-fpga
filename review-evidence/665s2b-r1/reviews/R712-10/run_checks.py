#!/usr/bin/env python3
"""Run independent lightweight checks concurrently, retaining raw output and exit status."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
scratch = out / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
docs_python = os.environ.get('DOCS_PYTHON', sys.executable)
checks = {
    'docs_check': [sys.executable, '-B', 'scripts/docs_check.py'],
    'doc_style': [sys.executable, '-B', 'scripts/check_doc_style.py'],
    'em_dash': [docs_python, '-B', 'scripts/check_em_dash.py', '--base', '325514224bcc356a6b43843f1003c2323f09de25'],
    'em_dash_selftest': [docs_python, '-B', 'scripts/check_em_dash.py', '--selftest'],
    'py_idiom': [sys.executable, '-B', 'scripts/check_py_idiom.py'],
    'diff_check': ['git', 'diff', '--check', '325514224bcc356a6b43843f1003c2323f09de25', 'HEAD'],
}
def run(item):
    name, command = item
    with (out / ('local-'+name+'.log')).open('wb') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, env=env, timeout=540)
    (out / ('local-'+name+'.rc')).write_text(str(result.returncode)+'\n')
    return name, result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, checks.items()))
for name, rc in results:
    print(name, 'rc='+str(rc))
raise SystemExit(any(rc for _, rc in results))
