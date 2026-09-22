#!/usr/bin/env python3
"""Read-only public provenance capture. Requires gh, git, rtk and Python 3."""
import base64
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parents[1]
DONOR = 'Mister-M-alt/protocol-processor-control-plane-avb-milan'
PARENT = 'kebag-logic/milan-fpga'
POLICY = '483a133ed08867ea0d300d2b4a027b5b48a4282f'
EVIDENCE = 'ff273ff39b7bcb55f54e79ef4c423eb7244347b8'
HEAD = 'e0c43b03f31d6c1220dd05a110e4bb30029233a0'
BASE = 'f70ba36ecb634467e4b1c3f0dbf1239d1e12af57'
CHECKOUT = Path(os.environ.get('R252_CHECKOUT', '$VALIDATION_STORAGE/reviews/r252-pp102-r1'))
TRUSTED = Path(os.environ.get('R252_PARENT', '$VALIDATION_STORAGE/lanes/trusted-dev-20260922-512'))

def capture(name, args, cwd=CHECKOUT):
    command = ['rtk', 'proxy'] + args
    start = datetime.now(timezone.utc).isoformat()
    p = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(p.stdout)
    target.with_name(target.name + '.stderr').write_bytes(p.stderr)
    target.with_name(target.name + '.command.json').write_text(json.dumps({
        'argv': command, 'cwd': str(cwd), 'started_utc': start,
        'finished_utc': datetime.now(timezone.utc).isoformat(), 'exit': p.returncode,
        'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
        'stderr_sha256': hashlib.sha256(p.stderr).hexdigest()}, indent=2) + '\n')
    if p.returncode:
        raise RuntimeError(f'{name}: exit {p.returncode}: {p.stderr.decode(errors="replace")}')
    return p.stdout

def api(name, endpoint):
    return json.loads(capture(name, ['gh', 'api', endpoint]))

def blob_hash(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def public_batch():
    requests = []
    for n in (95, 97, 98, 102, 103):
        requests.extend([(f'public/donor-issue-{n}.json', f'repos/{DONOR}/issues/{n}'),
                         (f'public/donor-issue-{n}-comments.json', f'repos/{DONOR}/issues/{n}/comments?per_page=100')])
    requests += [
        ('public/assignment.json', f'repos/{DONOR}/issues/comments/5782563688'),
        ('public/original-finding.json', f'repos/{PARENT}/issues/comments/5781426819'),
        ('public/pr103.json', f'repos/{DONOR}/pulls/103'),
        ('public/pr103-commits.json', f'repos/{DONOR}/pulls/103/commits?per_page=100'),
        ('public/pr103-reviews.json', f'repos/{DONOR}/pulls/103/reviews?per_page=100'),
        ('public/pr103-inline.json', f'repos/{DONOR}/pulls/103/comments?per_page=100'),
        ('public/exact-head-runs.json', f'repos/{DONOR}/actions/runs?head_sha={HEAD}&per_page=100'),
        ('public/exact-head-checks.json', f'repos/{DONOR}/commits/{HEAD}/check-runs?per_page=100'),
        ('public/parent-policy-tree.json', f'repos/{PARENT}/git/trees/{POLICY}?recursive=1'),
        ('public/evidence-tree.json', f'repos/{PARENT}/git/trees/{EVIDENCE}?recursive=1'),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for name, result in zip([x[0] for x in requests], pool.map(lambda x: api(*x), requests)):
            print(name, 'captured')

def policy():
    tree = json.loads((OUT/'public/parent-policy-tree.json').read_text())
    assert not tree.get('truncated')
    entries = {e['path']: e for e in tree['tree']}
    paths = ['AGENTS.md', 'CONTRIBUTING.md', 'docs/development/CODE_QUALITY.md',
             'scripts/check_cpp_idiom.py', 'scripts/code_quality_scope.py', 'scripts/cpp_idiom.budget']
    for path in paths:
        e = entries[path]
        b = capture('parent/'+path, ['git','-C', str(TRUSTED), 'show', POLICY+':'+path])
        public = api('public/policy-blobs/'+e['sha']+'.json', f'repos/{PARENT}/git/blobs/{e["sha"]}')
        raw = base64.b64decode(public['content'])
        assert blob_hash(b) == e['sha'] == blob_hash(raw) and b == raw
        print(path, e['sha'], 'public blob == trusted immutable Git object')

def snapshots():
    capture('raw/initial-status.txt',['git','status','--porcelain=v2','--branch'])
    capture('raw/head-identity.txt',['git','show','-s','--format=fuller%n%H%n%T%n%P','HEAD'])
    capture('raw/source.diff',['git','diff','--binary',BASE,HEAD,'--'])
    capture('raw/history.txt',['git','log','-30','--format=fuller','--stat'])
    capture('raw/ls-tree.txt',['git','ls-tree','-r',HEAD])
    capture('raw/ls-files-stage.txt',['git','ls-files','--stage'])
    paths = capture('raw/tracked-files.txt',['git','ls-tree','-r','--name-only',HEAD]).decode().splitlines()
    selected = [p for p in paths if p in ('README.md','Makefile','AGENTS.md','CONTRIBUTING.md') or
                p.startswith(('tb/pp_top/','.github/workflows/','scripts/','docs/','hdl/')) or
                p in ('tb/srp_encoder/README.md','tb/srp_encoder/Makefile','tb/srp_encoder/sim_main.cpp')]
    for path in selected:
        b = capture('source/'+path,['git','show',HEAD+':'+path])
    print('source snapshots',len(selected))

def evidence():
    tree = json.loads((OUT/'public/evidence-tree.json').read_text())
    assert not tree.get('truncated')
    prefix = 'review-evidence/pp102-r1/'
    author = {'author/ORIGINAL-FAILURES.md', 'author/build-command.json',
              'author/build-artifacts.json', 'author/build-tally.txt',
              'author/focused-results.json', 'author/logs/focused-cflags.log',
              'author/logs/focused-cflags-only.log', 'author/logs/baseline-cflags.log',
              'author/logs/pp-top-full.log', 'author/logs/build-results.log',
              'author/context/tool-identity.json', 'author/context/parent-policy-identity.json',
              'author/context/checker-inputs.json'}
    selected = [e for e in tree['tree'] if e['type'] == 'blob' and e['path'].startswith(prefix)
                and (e['path'][len(prefix):].startswith('source/manager/')
                     or e['path'][len(prefix):] in author)]
    def fetch(e):
        rel = e['path'][len(prefix):]
        doc = api('public/evidence-blobs/'+e['sha']+'.json', f'repos/{PARENT}/git/blobs/{e["sha"]}')
        b = base64.b64decode(doc['content'])
        assert blob_hash(b) == e['sha'] and len(b) == e['size']
        target = OUT/'evidence'/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(b)
        return {'path': rel, 'git_blob': e['sha'], 'mode': e['mode'],
                'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(fetch, selected))
    (OUT/'raw/public-evidence-integrity.json').write_text(json.dumps(records,indent=2)+'\n')
    print('Verified public evidence blobs:',len(records))

def hosted():
    runs = api('public/hosted-current-runs.json', f'repos/{DONOR}/actions/runs?head_sha={HEAD}&per_page=100')
    for r in runs['workflow_runs']:
        jobs = api(f'public/hosted-{r["id"]}-jobs.json', f'repos/{DONOR}/actions/runs/{r["id"]}/jobs?per_page=100')
        print(r['id'],r['event'],r['status'],r['conclusion'])
        for j in jobs['jobs']:
            print(' ',j['id'],j['name'],j['status'],j['conclusion'])

if __name__ == '__main__':
    {'public': public_batch, 'policy': policy, 'source': snapshots,
     'evidence': evidence, 'hosted': hosted}[sys.argv[1]]()
