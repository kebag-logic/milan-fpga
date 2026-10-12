#!/usr/bin/env python3
"""Offline reviewer campaigns. Usage: python run_review.py REPO AUTHOR_PACKET OUT --jobs 8.

Run with the interpreter holding the repository's locked Markdown dependencies.
All child commands are joined in this foreground process. No bench access.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('out', type=Path)
p.add_argument('--jobs', type=int, default=8)
a = p.parse_args()
repo, packet, out = (x.resolve() for x in (a.repo, a.packet, a.out))
scratch = out / 'scratch' / 'campaigns'
receipts = out / 'receipts'
scratch.mkdir(parents=True, exist_ok=True)
receipts.mkdir(parents=True, exist_ok=True)
page = repo / 'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
check = packet / 'tools/check_b16_figures.py'
py = sys.executable
head = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch), GIT_NO_REPLACE_OBJECTS='1')

def safe(s):
    for source, target in sorted(((str(repo), '{repo}'), (str(packet), '{packet}'),
                                  (str(out), '{review}'), (py, '{python}')),
                                 key=lambda x: -len(x[0])):
        s = s.replace(source, target)
    return s

def run(name, cmd):
    r = subprocess.run(list(map(str, cmd)), cwd=repo, env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=540)
    (receipts / (name + '.log')).write_text(safe(r.stdout))
    (receipts / (name + '.rc')).write_text(str(r.returncode) + '\n')
    return dict(name=name, command=safe(' '.join(map(str, cmd))), rc=r.returncode)

jobs = []
jobs.append(('figures', [py, '-I', check, page, packet, receipts / 'figures-rows.tsv',
                         receipts / 'figures-coverage.tsv', '--repo', repo, '--show', '200']))
for round_ in range(3, 8):
    jobs.append((f'controls-r{round_}', [py, '-I', packet / f'tools/r{round_}_check_controls.py',
                check, page, packet, scratch / f'controls-r{round_}', receipts / f'controls-r{round_}.json']))
jobs.append(('self-probes-r7', [py, '-I', packet / 'tools/r7_self_probes.py', check, page, packet,
                              scratch / 'self-probes-r7', receipts / 'self-probes-r7.json']))
jobs.append(('evidence-mapping', [py, '-I', packet / 'tools/r7_evidence_receipt.py', repo,
                                'fa974c3f1f9a1ef3a461ebb3b090b1915faaf251', head,
                                receipts / 'evidence-mapping.json']))

# Only load the public wrapper's argument/schema table. Each historical probe executes unmodified.
saved = sys.argv
sys.argv = ['r7_probe_reruns.py', str(repo), str(packet), str(packet / 'tools/review-probes'),
            str(scratch / 'historical'), head, py]
meta = runpy.run_path(str(packet / 'tools/r7_probe_reruns.py'), run_name='probe_metadata')
sys.argv = saved
probe_results = {}
for name, (script, want, public_path, argv, result_path, read) in meta['PROBE'].items():
    src = packet / 'tools/review-probes' / script
    got = hashlib.sha256(src.read_bytes()).hexdigest()
    assert got == want, (name, got, want)
    work = scratch / name
    (work / 'receipts').mkdir(parents=True, exist_ok=True)
    (work / 'scratch').mkdir(parents=True, exist_ok=True)
    jobs.append((name, [py, '-I', src, *argv(work)]))
    probe_results[name] = (result_path(work), read, got, public_path)
for name, args in [
    ('docs-check', ['scripts/docs_check.py']),
    ('doc-style', ['scripts/check_doc_style.py']),
    ('toc-check', ['scripts/gen_toc.py', '--check']),
    ('toc-anchors', ['scripts/gen_toc.py', '--verify-anchors']),
    ('em-dash', ['scripts/check_em_dash.py', '--base', 'c20c85bd']),
    ('doc-paths', ['scripts/check_doc_paths.py']),
]:
    jobs.append((name, [py, *args]))
jobs.append(('diff-check', ['git', 'diff', '--check', 'c20c85bd', head]))

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=min(max(a.jobs, 1), 16)) as pool:
    todo = {pool.submit(run, n, cmd): n for n, cmd in jobs}
    for future in concurrent.futures.as_completed(todo):
        name = todo[future]
        try:
            result = future.result()
            if name in probe_results:
                path, read, sha, public_path = probe_results[name]
                raw = json.loads(path.read_text())
                result.update(probe_sha256=sha, published_path=public_path, reading=read(raw))
                (receipts / (name + '.json')).write_text(safe(json.dumps(raw, indent=2)) + '\n')
        except Exception as e:
            result = dict(name=name, error=safe(str(e)))
        results.append(result)
        print(name, 'rc', result.get('rc'), 'error', result.get('error', ''), flush=True)
        (receipts / 'campaign-results.json').write_text(safe(json.dumps(
            dict(head=head, jobs=min(max(a.jobs, 1), 16), results=sorted(results, key=lambda x: x['name'])), indent=2)) + '\n')

