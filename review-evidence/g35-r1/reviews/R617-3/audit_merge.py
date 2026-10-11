#!/usr/bin/env python3
"""Read-only three-way content and final worktree/index audit."""
import argparse
import hashlib
import os
import re
import subprocess
from pathlib import Path

HEAD = '49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c'
TREE = '526a366bd9aff5cd8d0ad0278217dab22ac921ea'
BASE = '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d'
PREV = 'a70e38804cb16435c089d024c58e8c3fb4d39ff6'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', type=Path)
    ap.add_argument('--packet', type=Path, default=Path(__file__).resolve().parent)
    a = ap.parse_args()
    repo = a.repo.resolve()
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args])
    def tree(ref):
        result = {}
        for item in git('ls-tree', '-rz', ref).split(b'\0'):
            if not item:
                continue
            meta, path = item.split(b'\t', 1)
            mode, typ, oid = meta.decode().split()
            result[path.decode()] = (mode, typ, oid)
        return result
    def blob(entry):
        return git('cat-file', 'blob', entry[2]) if entry else b''
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    parents = git('show', '-s', '--format=%P', HEAD).decode().split()
    assert parents[0] == PREV and len(parents) == 2
    main_parent = parents[1]
    assert main_parent.startswith('155de137')
    assert git('merge-base', *parents).decode().strip() == BASE
    print('head', HEAD, '\ntree', TREE, '\nparents', *parents, '\nmerge-base', BASE)
    ts = [tree(ref) for ref in [BASE, PREV, main_parent, HEAD]]
    work = a.packet / 'scratch' / 'merge-audit'
    work.mkdir(parents=True, exist_ok=True)
    conflicts = []
    for path in sorted(set().union(*[set(t) for t in ts])):
        b, l, r, h = [t.get(path) for t in ts]
        if l == r:
            expected = l
        elif l == b:
            expected = r
        elif r == b:
            expected = l
        else:
            assert l and r and b and l[:2] == r[:2] == b[:2]
            for label, entry in [('left', l), ('base', b), ('right', r)]:
                (work / label).write_bytes(blob(entry))
            run = subprocess.run(['git', 'merge-file', '-p', str(work/'left'),
                                  str(work/'base'), str(work/'right')], capture_output=True)
            assert run.returncode in (0, 1), run.stderr
            if run.returncode:
                conflicts.append(path)
                (work / (path.replace('/', '_') + '.conflict')).write_bytes(run.stdout)
                # The declared resolution is main's new documentation with only
                # the fixed #35 risk entry removed. Check the whole blob exactly.
                right = blob(r)
                lines = right.splitlines(keepends=True)
                removed = [line for line in lines if b'issues/35)' in line]
                assert len(removed) == 1, (path, removed)
                resolved = b''.join(line for line in lines if line not in removed)
                assert h[:2] == r[:2] and blob(h) == resolved, path
                print('CONFLICT RESOLVED EXACTLY:', path)
                print('  sole removal from main:', removed[0].decode().strip())
                continue
            expected = (l[0], l[1], hashlib.sha1(
                b'blob ' + str(len(run.stdout)).encode() + b'\0' + run.stdout).hexdigest())
            print('AUTOMERGED:', path)
        assert h == expected, (path, h, expected)
    assert conflicts == ['README.md', 'docs/MANAGER.md'], conflicts
    print('PASS: every other path, blob, and mode equals its plain three-way result')
    protected = [p for p in ts[1] if p.startswith(('hdl/', 'tb/'))]
    assert all(ts[1][p] == ts[3][p] for p in protected)
    print('PASS:', len(protected), 'hdl/ and tb/ paths unchanged from prior reviewed head')
    for path,start,end in [
        ('docs/INTEGRATION.md','## Receive interface','## Transmit interface'),
        ('docs/HDL_DEVELOPER.md','## Receive path','## Event arbitration'),
    ]:
        before=blob(ts[1][path]).decode()
        after=blob(ts[3][path]).decode()
        assert before.split(start,1)[1].split(end,1)[0] == after.split(start,1)[1].split(end,1)[0]
        print('PASS: earlier-reviewed receive contract text unchanged:',path)
    print('PASS: root Makefile differs from prior head only by OOC checker selftest')
    root_diff = git('diff', PREV, HEAD, '--', 'Makefile').decode()
    assert [s for s in root_diff.splitlines() if s.startswith('+') and not s.startswith('+++')] == [
        '+\tpython3 syn/ooc/check_ooc_clock.py --selftest']
    index = {}
    for row in git('ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        meta, path = row.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        index[path.decode()] = (mode, oid)
    assert index == {p: (e[0], e[2]) for p, e in ts[3].items()}
    count = 0
    links = []
    for path, (mode, typ, oid) in ts[3].items():
        if mode == '160000':
            links.append((path, oid))
            continue
        f = repo/path
        raw = os.readlink(f).encode() if mode == '120000' else f.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert actual == oid, path
        actual_mode = '120000' if f.is_symlink() else ('100755' if f.stat().st_mode & 0o111 else '100644')
        assert actual_mode == mode, path
        count += 1
    assert not links, links
    assert git('status', '--porcelain=v1', '--untracked-files=all') == b''
    assert not git('diff', '--check', BASE, HEAD)
    print('PASS:', count, 'tracked filesystem bytes/modes and all index entries match exact tree')
    print('PASS: no nested submodule gitlinks; worktree and index clean; diff whitespace clean')

if __name__ == '__main__':
    main()
