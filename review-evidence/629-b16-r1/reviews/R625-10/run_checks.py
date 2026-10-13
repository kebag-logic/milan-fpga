#!/usr/bin/env python3
"""Run the published offline checks concurrently; all children are awaited.

Usage: locked-python run_checks.py REPO AUTHOR_PACKET OUTPUT [--jobs N]
The output directory owns scratch copies. No source checkout is changed.
"""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('output', type=Path)
p.add_argument('--jobs', type=int, default=8)
a = p.parse_args()
repo, packet, output = (x.resolve() for x in (a.repo, a.packet, a.output))
scratch = output / 'scratch' / 'checks'
scratch.mkdir(parents=True, exist_ok=True)
receipts = output / 'receipts'
receipts.mkdir(exist_ok=True)
work = scratch / 'author-copy'
shutil.copytree(packet, work, dirs_exist_ok=True)
check = work / 'tools/check_b16_figures.py'
page = repo / 'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
py = sys.executable
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
tasks = [('figures', [py, '-B', check, page, work, receipts/'figures-rows.tsv', receipts/'figures-coverage.tsv', '--repo', repo])]
for n in range(3, 11):
    name = f'controls-r{n}'
    tasks.append((name, [py, '-B', work/f'tools/r{n}_check_controls.py', check, page, work, scratch/name, receipts/f'{name}.json']))
tasks += [
    ('review-probes', [py, '-B', work/'tools/r10_probe_reruns.py', repo, work, work/'tools/review-probes', scratch/'review-probes', 'f1b2489f5b1c929e81eeae79a469b2b27c47e340']),
    ('self-probes', [py, '-B', work/'tools/r10_self_probes.py', check, page, work, scratch/'self-probes', receipts/'self-probes.json']),
    ('reader-controls', [py, '-B', work/'tools/r10_reader_controls.py', check, repo, scratch/'reader-controls', receipts/'reader-controls.json']),
    ('parser-extents', [py, '-B', work/'tools/r10_parser_extents.py', check, repo, scratch/'parser-extents', receipts/'parser-extents.json']),
    ('diff-check', ['git', '-C', repo, 'diff', '--check', 'c20c85bd', 'HEAD']),
    ('docs-check', [py, '-B', repo/'scripts/docs_check.py']),
    ('doc-style', [py, '-B', repo/'scripts/check_doc_style.py']),
    ('toc-check', [py, '-B', repo/'scripts/gen_toc.py', '--check']),
    ('em-dash', [py, '-B', repo/'scripts/check_em_dash.py', '--base', 'c20c85bd']),
    ('doc-paths', [py, '-B', repo/'scripts/check_doc_paths.py']),
]

def public(s):
    for path, name in ((work, '{author-packet}'), (packet, '{published-packet}'), (output, '{output}'), (repo, '{repo}')):
        s = s.replace(str(path), name)
    return s

def run(task):
    name, args = task
    start = time.monotonic()
    with (scratch/f'{name}.log').open('w') as f:
        result = subprocess.run(list(map(str, args)), cwd=repo, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=3600)
    (receipts/f'{name}.log').write_text(public((scratch/f'{name}.log').read_text()))
    (receipts/f'{name}.rc').write_text(str(result.returncode)+'\n')
    r = dict(name=name, argv=[public(str(x)) if str(x) != py else '{locked-python}' for x in args], rc=result.returncode, seconds=round(time.monotonic()-start, 3))
    print(json.dumps(r), flush=True)
    return r

with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs, 16)) as pool:
    results = list(pool.map(run, tasks))
for file in sorted((work/'r10').glob('*probe-rerun.json')):
    (receipts/file.name).write_text(public(file.read_text()))
for file in receipts.glob('*.json'):
    file.write_text(public(file.read_text()))
(receipts/'commands.json').write_text(json.dumps(results, indent=2)+'\n')
print('All child commands completed.', flush=True)
