#!/usr/bin/env python3
"""Run the focused source/documentation checks without building hardware."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
commands = [
    ('docs-check', ['scripts/docs_check.py']),
    ('doc-style', ['scripts/check_doc_style.py']),
    ('doc-paths', ['scripts/check_doc_paths.py']),
    ('toc-check', ['scripts/gen_toc.py', '--check']),
    ('em-dash', ['scripts/check_em_dash.py', '--base', 'c6bd08c6']),
    ('python-idiom', ['scripts/check_py_idiom.py']),
    ('test-evidence', ['scripts/measure_test_evidence.py', '--check']),
]
env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
def run(task):
    label, args = task
    renderer = packet / 'scratch/markdown-env/bin/python'
    executable = str(renderer) if label in ('toc-check', 'em-dash') and renderer.exists() else sys.executable
    r = subprocess.run([executable, *args], cwd=repo, env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=540)
    (packet / 'receipts' / (label + '.log')).write_text(r.stdout)
    (packet / 'receipts' / (label + '.rc')).write_text(str(r.returncode) + '\n')
    print(label, r.returncode, r.stdout[-900:], flush=True)
    return {'check': label, 'command': [executable, *args], 'rc': r.returncode}
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands))
(packet / 'receipts/static-checks.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(any(r['rc'] for r in results))
