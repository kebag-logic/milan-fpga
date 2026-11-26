#!/usr/bin/env python3
"""Issue #113: verify published evidence bytes and the untouched source checkout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HEAD = 'af11b3ef631eb44cdc1730cfb31bedda95c33dc5'
TREE = 'de4e33ba9c752220bdb0567cb6b9b5ec6c7c7e2a'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', type=Path)
    ap.add_argument('packet', type=Path)
    args = ap.parse_args()
    repo, packet = args.repo.resolve(), args.packet.resolve()
    def git(*argv):
        return subprocess.check_output(['git', *argv], cwd=repo)
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    assert subprocess.run(['git', 'symbolic-ref', '-q', 'HEAD'], cwd=repo, stdout=subprocess.DEVNULL).returncode == 1
    assert not git('status', '--porcelain=v1')
    index = {}
    for row in git('ls-files', '--stage', '-z').split(b'\0'):
        if row:
            meta, path = row.split(b'\t')
            mode, blob, stage = meta.split()
            assert stage == b'0'
            index[path] = (mode, blob)
    count, links = 0, []
    for row in git('ls-tree', '-rz', HEAD).split(b'\0'):
        if not row:
            continue
        meta, path = row.split(b'\t')
        mode, kind, blob = meta.split()
        assert index.pop(path) == (mode, blob)
        p = repo / os.fsdecode(path)
        if mode == b'160000':
            links.append((os.fsdecode(path), blob.decode()))
            assert subprocess.check_output(['git', '-C', str(p), 'rev-parse', 'HEAD']).strip() == blob
            continue
        data = os.readlink(p).encode() if mode == b'120000' else p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == blob.decode(), p
        if mode != b'120000':
            assert bool(p.stat().st_mode & 0o111) == (mode == b'100755'), p
        count += 1
    assert not index
    print('PASS source HEAD', HEAD, 'tree', TREE)
    print('PASS tracked working bytes, executable modes and index:', count, 'blobs')
    print('PASS required nested gitlinks:', json.dumps(links))
    print('PASS source worktree clean; no source edits required')
    manifest = json.loads((packet / 'scratch/consumer-manifest.json').read_text())
    author = packet / 'scratch/public-author'
    for entry in manifest:
        p = author / entry['file'].removeprefix('author/')
        assert hashlib.sha256(p.read_bytes()).hexdigest() == entry['published_sha256'], p
    print('PASS public author packet:', len(manifest), 'published SHA-256 hashes verified')
    logs = author / 'receipts/logs'
    for name, count in (('', 179), ('-abort', 64)):
        a = (logs / ('engine/base' + name + '.norm')).read_bytes()
        b = (logs / ('engine/head' + name + '.norm')).read_bytes()
        assert a == b and len(a.splitlines()) == count
        for label in ('base', 'head'):
            raw = (logs / ('engine/' + label + name + '/log')).read_text()
            normalized = ''.join(line for line in raw.splitlines(keepends=True)
                                 if not line.startswith('- Verilator') and 'g++' not in line and not line.startswith('verilator --cc'))
            assert normalized.encode() == a
            expected = '0' if not name else '2'
            assert (logs / ('engine/' + label + name + '/result')).read_text().startswith('rc=' + expected + ' ')
        print('PASS author real-engine pair', name or 'clean', 'recomputed normalization;', count, 'identical lines')
    raw = (logs / 'plants-r1.log').read_text()
    assert all(f'PASS [{arm}] control, no plant: rc=0, 73 PASS, 0 FAIL' in raw for arm in ('old', 'new'))
    pairs = {}
    for arm, name, failures in re.findall(r'CAUGHT \[(old|new)\] (.*): rc=1, (\d+) failing checks', raw):
        pairs.setdefault(name, {})[arm] = int(failures)
    assert len(pairs) == 13 and all(p['old'] == p['new'] and p['old'] > 0 for p in pairs.values())
    print('PASS author 13 mutation pairs: same nonzero failing-check counts; both controls 73/73')
    ratchets = (logs / 'consumer-ratchets-af11b3e.log').read_text()
    assert HEAD in ratchets and 'budgets vs dev-soft-core: unchanged' in ratchets and ratchets.count('rc=0') == 2
    assert '3 <= 3 wall-clock-dependent suite file(s)' in ratchets
    assert 'too many parameters: 7 <= 7' in ratchets
    print('PASS author exact-head consumer receipt: both rc=0, unchanged budgets asserted; no independent consumer rerun')


if __name__ == '__main__':
    main()
