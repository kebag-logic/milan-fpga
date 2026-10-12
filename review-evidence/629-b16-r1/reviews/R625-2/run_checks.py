#!/usr/bin/env python3
"""Run focused, offline checks. Arguments: repository evidence packet markdown-python.

All children are waited for in this foreground process. Scratch files stay under packet/scratch.
No hardware command, whole-repository build bank, or publication operation is invoked.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

repo, evidence, packet, mdpython = map(Path, sys.argv[1:5])
repo, evidence, packet = [p.resolve() for p in (repo, evidence, packet)]
# Preserve a virtual environment's executable path rather than resolving its symlink.
mdpython = mdpython.absolute()
logs = packet / 'checks'
logs.mkdir(exist_ok=True)
tmp = packet / 'scratch' / 'checks'
tmp.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(tmp),
           OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
jobs = [
    ('docs-check', [str(mdpython), 'scripts/docs_check.py']),
    ('doc-style', [str(mdpython), 'scripts/check_doc_style.py']),
    ('toc-check', [str(mdpython), 'scripts/gen_toc.py', '--check']),
    ('toc-anchors', [str(mdpython), 'scripts/gen_toc.py', '--verify-anchors']),
    ('em-dash', [str(mdpython), 'scripts/check_em_dash.py', '--base', 'c20c85bd']),
    ('doc-paths', [str(mdpython), 'scripts/check_doc_paths.py']),
    ('diff-check', ['git', 'diff', '--check', 'c20c85bd', 'HEAD']),
    ('alignment-controls', [sys.executable, str(evidence/'tools/align_b16.py'), 'control', 'synth', '-', '-', str(logs/'alignment-controls.json')]),
    ('tap-controls', [sys.executable, str(evidence/'tools/tone_points_b16.py'), 'control', str(logs/'tap-controls.json')]),
    ('grade-controls', [sys.executable, str(evidence/'tools/b9_thdn.py'), 'controls', str(logs/'grade-controls.json')]),
    ('b0-receipt', [sys.executable, '-I', str(evidence/'tools/r2_b0_receipt.py'), str(evidence), str(logs/'b0-recomputed.json')]),
]

def scrub(s):
    for path, label in [(str(mdpython), '<markdown-python>'), (str(evidence), '<evidence>'),
                        (str(packet), '<packet>'), (str(repo), '<repository>'),
                        (sys.executable, '<python>')]:
        s = s.replace(path, label)
    return s

def run(job):
    name, cmd = job
    start = time.monotonic()
    try:
        p = subprocess.run(cmd, cwd=repo, env=env, capture_output=True, text=True, timeout=240)
        result = dict(name=name, command=[scrub(x) for x in cmd], rc=p.returncode,
                      seconds=round(time.monotonic()-start, 3))
        (logs/(name+'.log')).write_text(scrub(p.stdout+p.stderr))
    except subprocess.TimeoutExpired:
        result = dict(name=name, command=[scrub(x) for x in cmd], rc=124, seconds=240)
        (logs/(name+'.log')).write_text('TIMEOUT\n')
    (logs/(name+'.rc')).write_text(str(result['rc'])+'\n')
    return result

selected = set(sys.argv[5:])
if selected:
    jobs = [job for job in jobs if job[0] in selected]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, jobs))
(logs/('results-retry.json' if selected else 'results.json')).write_text(json.dumps(results, indent=2)+'\n')
for result in results:
    print(result['name'], 'rc', result['rc'], 'seconds', result['seconds'])
same = (logs/'b0-recomputed.json').read_bytes() == (evidence/'r2/b0-2-receipt.json').read_bytes()
print('B0 receipt byte reproduction:', same)
sys.exit(0 if all(x['rc']==0 for x in results) and same else 1)
