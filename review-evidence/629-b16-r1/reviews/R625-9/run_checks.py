#!/usr/bin/env python3
"""Reproduce focused offline checks. Arguments: repository evidence-root output-root.

Run with the repository's hash-locked documentation interpreter. All disposable
copies stay below output-root/scratch. No hardware or remote write is used.
"""
import concurrent.futures
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import time

repo, evidence, out = [pathlib.Path(x).resolve() for x in sys.argv[1:4]]
scratch = out / 'scratch'
receipts = out / 'receipts'
receipts.mkdir(exist_ok=True)
packet = scratch / 'run-packet'
if not packet.exists():
    shutil.copytree(evidence / 'author-r9', packet)
page = repo / 'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
check = packet / 'tools/check_b16_figures.py'
py = sys.executable
def safe(s):
    for p, label in [(packet, '{packet}'), (evidence, '{evidence}'), (repo, '{repo}'), (out, '{output}')]:
        s = s.replace(str(p), label)
    return s

jobs = [('figures', [check, page, packet, receipts/'figures-rows.tsv', receipts/'figures-coverage.tsv', '--repo', repo])]
for n in range(3,10):
    jobs.append((f'controls-r{n}', [packet/f'tools/r{n}_check_controls.py', check, page, packet,
                                 scratch/f'controls-r{n}', receipts/f'controls-r{n}.json']))
jobs.append(('review-probes', [packet/'tools/r9_probe_reruns.py', repo, packet,
                             packet/'tools/review-probes', scratch/'review-probes',
                             'cb5ff79f1f69117efba353484851eceb620e5c92']))
jobs.extend([
    ('docs-check', [repo/'scripts/docs_check.py']),
    ('em-dash', [repo/'scripts/check_em_dash.py', '--base', 'c20c85bd']),
])

def run(job):
    name, args = job
    start = time.monotonic()
    proc = subprocess.run([py, '-I', *map(str,args)], cwd=repo, capture_output=True, text=True, timeout=3600)
    (receipts/f'{name}.log').write_text(safe(proc.stdout + proc.stderr))
    (receipts/f'{name}.rc').write_text(str(proc.returncode)+'\n')
    result = dict(name=name, command=safe('python -I ' + ' '.join(map(str,args))),
                  rc=proc.returncode, seconds=round(time.monotonic()-start,3))
    print(json.dumps(result), flush=True)
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, jobs))
(receipts/'check-commands.json').write_text(json.dumps(results,indent=2)+'\n')
for p in (packet/'r9').glob('*probe-rerun.json'):
    (receipts/p.name).write_text(safe(p.read_text()))
print('Finished all foreground checks', flush=True)
