#!/usr/bin/env python3
"""Recheck the bounded review delta, public receipt digests and checkout bytes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = 'd3cb3cf180f846a969f5baacf8b2bec34e4acd50'
PREV = 'e5d8a71b6fa90352eca72314c7bd2275a1b20285'
PACKETS = [('4b3b21e2104d37db96040622edfe75a5acbf2a76', 'pins1125-r1'),
           ('e185cf1181dac7690707428deda80b88537f16b0', 'pins1125-r2')]

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args],
                                   env={**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'})

def integrity(repo, revision):
    tree = git(repo, 'ls-tree', '-rz', revision)
    records = []
    count = 0
    links = []
    for entry in tree.split(b'\0'):
        if not entry:
            continue
        info, name = entry.split(b'\t', 1)
        mode, kind, oid = info.decode().split()
        records.append(mode.encode() + b' ' + oid.encode() + b' 0\t' + name)
        path = repo / os.fsdecode(name)
        if kind == 'commit':
            links.append((os.fsdecode(name), oid))
            continue
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), str(path)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), str(path)
            assert bool(st.st_mode & 0o111) == (mode == '100755'), str(path)
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid, os.fsdecode(name)
        count += 1
    actual = git(repo, 'ls-files', '--stage', '-z').split(b'\0')
    assert sorted(filter(None, actual)) == sorted(records), 'index differs from committed tree'
    return count, links

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    out = Path(__file__).resolve().parent
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == HEAD
    assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == 'eb3ebcb7e1ad48818893afad260ff060937c6c96'
    assert git(repo, 'rev-list', '--count', PREV + '..' + HEAD).strip() == b'1'
    names = git(repo, 'diff', '--name-only', PREV, HEAD).decode().splitlines()
    assert names == ['CHANGELOG.md', 'tb/verilator/gptp_shadow/sim_main.cpp'], names
    source = names[1]
    old = git(repo, 'show', PREV + ':' + source).decode()
    new = git(repo, 'show', HEAD + ':' + source).decode()
    old_comment = ('  //! How near the offset of a graded pair must be to its expected 0: the\n'
                   '  //! stamps quantise to the 8 ns tick, and the nearest wrong link value\n'
                   '  //! (-263 ns used as 0) is 263 ns away.\n')
    new_comment = ('  //! How near the offset after a graded pair must be to its expected value,\n'
                   '  //! the offset before it less kGradedOffsetNs: the stamps quantise to the\n'
                   '  //! 8 ns tick. Used delays less than this far apart are not told apart here;\n'
                   "  //! gptp_plane's phase 6 grades the used delay to the nanosecond.\n")
    assert old.count(old_comment) == 1 and new == old.replace(old_comment, new_comment)
    old_log = git(repo, 'show', PREV + ':CHANGELOG.md')
    new_log = git(repo, 'show', HEAD + ':CHANGELOG.md')
    assert new_log == old_log.replace(b'Nine planted defects each fail a named check.',
                                     b'Eleven planted defects each fail a named check.')
    assert git(repo, 'ls-tree', PREV, *names).decode().count('100644 blob') == 2
    assert git(repo, 'ls-tree', HEAD, *names).decode().count('100644 blob') == 2
    print('PASS exact head/tree and single-commit delta; exactly the stated comment and changelog replacement')
    print('PASS all other tree entries, executable source bytes and modes unchanged from ' + PREV)
    for commit, packet in PACKETS:
        root = 'review-evidence/' + packet + '/'
        manifest_data = git(repo, 'show', commit + ':' + root + 'MANIFEST.json')
        manifest = json.loads(manifest_data)
        dest = out / 'public' / packet
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'MANIFEST.json').write_bytes(manifest_data)
        checked = 0
        for entry in manifest:
            name = entry['file']
            if not name.startswith('author/receipts/'):
                continue
            data = git(repo, 'show', commit + ':' + root + name)
            assert hashlib.sha256(data).hexdigest() == entry['published_sha256'], name
            checked += 1
            if packet == 'pins1125-r2' and not name.startswith('author/receipts/tools/'):
                target = dest / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        print(f'PASS {packet}: {checked} public author receipt hashes match manifest at {commit}')
    review_commit = PACKETS[1][0]
    root = 'review-evidence/pins1125-r1/'
    manifest = json.loads(git(repo, 'show', review_commit + ':' + root + 'MANIFEST.json'))
    selected = ['reviews/R937-2/receipts/probe_p6_used_as_zero.log',
                'reviews/R938-2/receipts/clean.log',
                'reviews/R938-2/receipts/probe-summary.txt']
    for name in selected:
        entry = next(x for x in manifest if x['file'] == name)
        data = git(repo, 'show', review_commit + ':' + root + name)
        assert hashlib.sha256(data).hexdigest() == entry['published_sha256'], name
        target = out / 'public' / 'prior-probes' / Path(name).name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        print('PASS prior probe receipt SHA-256: ' + name)
    n, links = integrity(repo, HEAD)
    print(f'PASS superproject: {n} tracked blobs byte/mode exact; index exact')
    required = ['gptp-processor', 'protocol-processor', 'third_party/verilog-axis',
                'third_party/tsn-c-stack', 'third_party/lwSRP']
    for name, oid in links:
        if name not in required:
            print(f'EXCLUDED unused submodule {name} gitlink {oid}')
            continue
        sub = repo / name
        assert (sub / '.git').is_file(), 'not an initialized submodule: ' + name
        assert git(sub, 'rev-parse', 'HEAD').decode().strip() == oid, name
        n, _ = integrity(sub, oid)
        print(f'PASS {name}: gitlink/HEAD {oid}; {n} tracked blobs byte/mode exact; index exact')
    assert not git(repo, 'status', '--porcelain'), 'checkout is not clean'
    print('PASS clean checkout; no source edits or mutation builds were needed')

if __name__ == '__main__':
    main()
