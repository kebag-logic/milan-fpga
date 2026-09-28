"""Verify candidate bytes, pinned checkout roots and bounded evidence files."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT = Path('$LANES/602-phc-step-mr')
OUT = Path(__file__).resolve().parent
START = '471892a9bcc2d26fdcfc19db01949ecea83c5e0f'


def git(*args, directory=ROOT):
    """Read Git, checking a submodule's root before every call inside it."""
    if directory != ROOT:
        top = subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(directory), 'rev-parse', '--show-toplevel'], text=True).strip()
        assert top == str(directory), (top, directory)
    return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(directory), *args])


head = git('rev-parse', 'HEAD').decode().strip()
assert git('remote', 'get-url', 'origin').decode().strip() == 'https://github.com/kebag-logic/milan-fpga.git'
assert git('branch', '--show-current').decode().strip() == '602-phc-step-mr'
assert not git('status', '--porcelain'), 'worktree must be clean'
assert not git('diff', '--name-only', START, head, '--', 'hdl', 'configs', 'sw', 'gptp-processor', 'protocol-processor', 'third_party', 'external')
immutable_blobs = 0
for entry in git('ls-tree', '-rz', START, '--', 'hdl', 'configs', 'sw').split(b'\0'):
    if not entry:
        continue
    header, name = entry.split(b'\t', 1)
    mode, kind, oid = header.split()
    if kind != b'blob':
        continue
    p = ROOT / name.decode()
    if mode == b'120000':
        assert p.is_symlink(), str(p)
        data = os.fsencode(os.readlink(p))
    else:
        assert p.is_file() and not p.is_symlink(), str(p)
        assert bool(p.stat().st_mode & 0o111) == (mode == b'100755'), str(p)
        data = p.read_bytes()
    actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual == oid.decode(), str(p)
    immutable_blobs += 1
subjects = git('log', '--format=%s', START+'..HEAD').decode().splitlines()
bodies = git('log', '--format=%b', START+'..HEAD').decode().strip()
assert len(subjects) == 1 and not bodies
submodules = {}
for rel in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    directory = ROOT / rel
    pin = git('ls-tree', head, rel).decode().split()[2]
    assert git('rev-parse', 'HEAD', directory=directory).decode().strip() == pin
    assert not git('status', '--porcelain', directory=directory)
    population = git('ls-tree', '-rz', pin, directory=directory).split(b'\0')
    count = 0
    for entry in population:
        if not entry:
            continue
        header, name = entry.split(b'\t', 1)
        mode, kind, oid = header.split()
        if kind != b'blob':
            continue
        p = directory / name.decode()
        if mode == b'120000':
            assert p.is_symlink(), str(p)
            data = os.fsencode(os.readlink(p))
        else:
            assert p.is_file() and not p.is_symlink(), str(p)
            assert bool(p.stat().st_mode & 0o111) == (mode == b'100755'), str(p)
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual == oid.decode(), str(p)
        count += 1
    submodules[rel] = {'pin':pin, 'blobs_verified':count, 'clean':True}
receipts = []
for p in sorted(OUT.glob('*.json')):
    record = json.loads(p.read_text())
    if not isinstance(record, dict) or record.get('head') != head or 'log' not in record:
        continue
    if record.get('final_evidence') is False:
        continue
    assert record['rc'] == 0, p.name
    log = Path(record['log']).read_bytes()
    assert len(log) == record['bytes'] and hashlib.sha256(log).hexdigest() == record['sha256'], p.name
    receipts.append(p.name)
inputs = json.loads((OUT/'input-fingerprints.json').read_text())
for record in inputs:
    data = Path(record['path']).read_bytes()
    assert len(data) == record['bytes'], record['path']
    assert hashlib.sha256(data).hexdigest() == record['sha256'], record['path']
body = (OUT/'PR-BODY.md').read_text()
assert body.splitlines()[0] == '[A383]' and 'Closes #602' in body
assert '## Round 3' in body and '/home/' not in body
assert (OUT/'REVIEW-READY.md').read_text().startswith('[A397] REVIEW READY\n')
files = [p for p in OUT.rglob('*') if p.is_file()]
assert all(p.stat().st_size <= 200000 for p in files)
report = {'head':head, 'starting_head':START, 'clean':True, 'immutable_paths':['hdl','configs','sw','submodules'],
          'immutable_blobs_verified':immutable_blobs, 'subjects':subjects, 'empty_commit_bodies':True, 'submodules':submodules,
          'read_only_inputs_verified':len(inputs), 'pr_body_format_valid':True, 'verified_receipts':receipts, 'output_files':len(files), 'largest_output_bytes':max(p.stat().st_size for p in files)}
(OUT/'final-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
