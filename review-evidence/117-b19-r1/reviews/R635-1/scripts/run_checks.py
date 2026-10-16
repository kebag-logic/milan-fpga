#!/usr/bin/env python3
"""Run focused read-only checks and reproduce public tables in disposable scratch.

Usage: python3 run_checks.py SOURCE_ROOT PACKET_ROOT OUTPUT_ROOT
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys

source, packet, output = [Path(x).resolve() for x in sys.argv[1:]]
receipts = output / 'receipts'
receipts.mkdir(exist_ok=True)
checks = {
    'diff-check': ['git', 'diff', '--check', '734eb780dc93896a5961cd95180f79475a401650', 'HEAD'],
    'docs-check': ['python3', '-B', 'scripts/docs_check.py'],
    'doc-style': ['python3', '-B', 'scripts/check_doc_style.py'],
    'doc-paths': ['python3', '-B', 'scripts/check_doc_paths.py'],
}
def run(item):
    name, args = item
    r = subprocess.run(args, cwd=source, capture_output=True, timeout=180)
    (receipts / (name + '.txt')).write_bytes(r.stdout + r.stderr + f'\nRC={r.returncode}\n'.encode())
    return name, r.returncode
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, checks.items()))
print('Focused checks:', results)

scratch = output / 'scratch' / 'reproduce'
scratch.mkdir(parents=True, exist_ok=True)
(scratch / 'tools').mkdir(exist_ok=True)
script = packet / 'author/tools/gm_summary.py'
shutil.copyfile(script, scratch / 'tools/gm_summary.py')
names = [f'gm{i:02}' for i in range(1, 6)]
for name in names:
    dst = scratch / 'bench' / name
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(packet / 'author/bench' / name / 'analysis.json', dst / 'analysis.json')
r = subprocess.run(['python3', '-B', str(scratch / 'tools/gm_summary.py'), *names],
                   capture_output=True, timeout=30)
assert r.returncode == 0
for name in ('gm-steps.json', 'gm-steps.md'):
    same = (scratch / 'summary' / name).read_bytes() == (packet / 'author/summary' / name).read_bytes()
    print('Published table reproduction:', name, 'byte_equal=', same)
    assert same

def command(*args):
    return subprocess.check_output(args, cwd=source)
head = command('git', 'rev-parse', 'HEAD').decode().strip()
tree = command('git', 'rev-parse', 'HEAD^{tree}').decode().strip()
assert head == '18b98bbcecf478b903610a07667f232d944d6feb'
assert tree == 'b9e4e014079cc9497a51ccfc3870e086143b8816'
index = {}
for record in command('git', 'ls-files', '--stage', '-z').split(b'\0'):
    if record:
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0'
        index[path] = (mode, oid)
entries = {}
for record in command('git', 'ls-tree', '-r', '-z', 'HEAD').split(b'\0'):
    if record:
        meta, path = record.split(b'\t', 1)
        mode, typ, oid = meta.split()
        entries[path] = (mode, oid)
assert entries == index
blobs = 0
gitlinks = []
for path, (mode, oid) in entries.items():
    p = source / path.decode()
    if mode == b'160000':
        gitlinks.append((path.decode(), oid.decode()))
        continue
    if mode == b'120000':
        assert p.is_symlink()
        data = str(p.readlink()).encode()
    else:
        assert p.is_file() and not p.is_symlink()
        data = p.read_bytes()
        executable = bool(p.stat().st_mode & stat.S_IXUSR)
        assert executable == (mode == b'100755'), path
    measured = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
    assert measured == oid, path
    blobs += 1
assert not command('git', 'status', '--porcelain')
print('Exact head:', head)
print('Exact tree:', tree)
print('Index equals HEAD tree; tracked blob bytes and modes verified:', blobs)
print('Required gitlinks verified (contents uninitialized, not executed):')
for path, oid in gitlinks:
    print(path, oid)
print('Source status clean. No source file edited; no restoration needed.')
