#!/usr/bin/env python3
"""Verify HEAD, index records, tracked raw blob bytes/modes and required submodule pins.
Usage: python3 identity_check.py REPOSITORY
"""
import hashlib
import os
import pathlib
import stat
import subprocess
import sys

root = pathlib.Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(where, *args):
    return subprocess.check_output(['git', '-C', str(where), *args], env=env)
def check(where, revision):
    expected = {}
    for line in git(where, 'ls-tree', '-rz', revision).split(b'\0'):
        if line:
            meta, path = line.split(b'\t', 1)
            mode, kind, oid = meta.split()
            expected[path] = (mode, oid)
    index = {}
    for line in git(where, 'ls-files', '--stage', '-z').split(b'\0'):
        if line:
            meta, path = line.split(b'\t', 1)
            mode, oid, stage = meta.split()
            assert stage == b'0' and path not in index, ('index stages', path)
            index[path] = (mode, oid)
    assert index == expected, 'index differs from pinned tree'
    blobs = 0
    links = {}
    for raw, (mode, oid) in expected.items():
        p = where/os.fsdecode(raw)
        if mode == b'160000':
            links[os.fsdecode(raw)] = oid.decode()
            continue
        st = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), raw
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), raw
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert mode == actual_mode, ('mode', raw)
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual == oid, ('blob', raw)
        blobs += 1
    return blobs, links
head = git(root, 'rev-parse', 'HEAD').decode().strip()
tree = git(root, 'rev-parse', 'HEAD^{tree}').decode().strip()
assert head == '234bc149ff888eb96659ecaaa5ce6e4fb27319d4'
assert tree == '9b54edcc9bd235b734ad559291cdf1ec6da4716c'
n, links = check(root, head)
print('HEAD', head, '\nTREE', tree)
print('superproject:', n, 'tracked blobs and modes match; index matches')
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'):
    pin = links[name]
    actual = git(root/name, 'rev-parse', 'HEAD').decode().strip()
    assert actual == pin, name
    assert (root/name/'.git').is_file(), ('not a registered checkout', name)
    n, _ = check(root/name, pin)
    print(name, pin, n, 'tracked blobs/modes match; index matches')
print('external:', links['external'], '(uninitialized, not required)')
print('STATUS', git(root, 'status', '--porcelain').decode().strip() or 'clean')
print('RESULT: PASS')
