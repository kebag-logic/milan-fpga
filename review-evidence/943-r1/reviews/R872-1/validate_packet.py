#!/usr/bin/env python3
"""Replay focused executables and inspect source/evidence identity without edits."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
archive = packet / 'scratch/review-evidence/943-r1'

def command(name, argv):
    with (packet / (name + '.log')).open('w') as log:
        log.write('COMMAND ' + repr(argv) + '\n'); log.flush()
        result = subprocess.run(argv, cwd=repo, stdout=log, stderr=subprocess.STDOUT,
                                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return name, result.returncode

jobs = []
for shape in ('1x1', '8x8'):
    for interface in (1, 2):
        name = f'focused-{shape}-if{interface}'
        executable = next((packet / 'scratch' / name).glob('aecp-mailbox-*/suite'))
        selected = '*' if shape == '1x1' else 'AppOutputs.*:Core.TheRunningCheckObservesEveryStreamBriefly:Face.TheRunningCheckReadsOneWindowWordAStream'
        jobs.append(('validated-' + shape + '-if' + str(interface), [str(executable), '--gtest_filter=' + selected]))
for point in ('1x1/1if', '8x8/1if'):
    jobs.append(('flip-grade-' + point.replace('/', '-'), [sys.executable, '-B', '-I', str(repo / 'tb/verilator/ctrl_service_budget/flip_grade.py'), '--check', '--point', point]))
with ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(lambda pair: command(*pair), jobs))
for name, rc in results:
    print(name, 'rc', rc)

entries = json.loads((archive / 'MANIFEST.json').read_text())
for entry in entries:
    path = archive / entry['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['published_sha256'], str(path)
print('published archive manifest verified:', len(entries), 'files')
for point, count in [('1x1', 40), ('8x8-1if', 33)]:
    text = (archive / f'author-r1/receipts/budget/arm-a-aecp-rows-{point}-211c1ede.txt').read_text()
    rows = re.findall(r'([0-9.]+) \(([0-9.]+)\) fits$', text, re.M)
    assert len(rows) == count and all(float(a) <= float(b) for a, b in rows)
    print('published arm A AECP rows checked:', point, count, 'all within their printed bounds')
for shape in ('1x1', '8x8'):
    old = (packet / ('old-code-' + shape + '.log')).read_text()
    cur = (packet / ('focused-' + shape + '-if1.log')).read_text()
    failed = lambda log: set(re.findall(r'^\[  FAILED  \] ([\w.]+) \(', log, re.M))
    print('old production code failures:', shape, sorted(failed(old)))
    print('current failures:', shape, sorted(failed(cur)))
    assert failed(cur).issubset(failed(old))
plants = json.loads((packet / 'plants.json').read_text())
assert len(plants) == 16 and all(p['caught'] for p in plants)
print('independent named plants:', len(plants), 'caught')

def git(*args, cwd=repo):
    return subprocess.check_output(['git', *args], cwd=cwd)

assert git('rev-parse', 'HEAD').decode().strip() == '502b041cc0bd0e4ea230b8a3a65f553ab69df3ff'
assert git('write-tree').decode().strip() == git('rev-parse', 'HEAD^{tree}').decode().strip()
count = 0
for record in git('ls-files', '--stage', '-z').split(b'\0'):
    if not record: continue
    meta, name = record.split(b'\t', 1)
    mode, oid, stage = meta.split()
    assert stage == b'0'
    path = repo / os.fsdecode(name)
    if mode == b'160000':
        if (path / '.git').exists():
            assert git('rev-parse', 'HEAD', cwd=path).strip() == oid
            assert not git('status', '--porcelain', '--untracked-files=no', cwd=path)
            print('initialized gitlink verified:', os.fsdecode(name), oid.decode())
        else:
            print('uninitialized gitlink retained:', os.fsdecode(name), oid.decode())
        continue
    data = os.fsencode(os.readlink(path)) if mode == b'120000' else path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert actual == oid.decode(), os.fsdecode(name)
    if mode != b'120000':
        actual_mode = b'100755' if path.stat().st_mode & stat.S_IXUSR else b'100644'
        assert mode == actual_mode, os.fsdecode(name)
    count += 1
assert not git('status', '--porcelain', '--untracked-files=all')
print('tracked blob bytes and modes verified:', count, '; index equals HEAD tree; working tree clean')
paths = ['sw/mailbox/mailbox.yaml', 'docs/design/MAILBOX_SPLIT.md', 'sw/firmware/ctrl/test/sink_mutants.py', 'tb/verilator/ctrl_service_budget/talker_notice.py', 'sw/firmware/ctrl/test/ctrl_configs.py']
for path in paths:
    assert git('show', '0839453f:' + path) == git('show', 'HEAD:' + path), path
    print('unchanged from base:', path)
print('post-evidence changes:', git('diff', '--stat', '211c1ede', 'HEAD').decode().strip())
assert all(rc == 0 for _, rc in results)
