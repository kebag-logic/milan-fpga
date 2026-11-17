"""Verify raw tracked bytes, Git modes, index and required submodules. Usage: CHECKOUT."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '9aa55d3b382750353709c3ba9ff6f6416938e83b'
TREE = 'fc52e64fd482c3185620b6d00048c2b2608f7d06'
root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)

def verify(repo, head):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == head
    records = git(repo, 'ls-tree', '-rz', head).split(b'\0')
    expected = {}
    links = {}
    count = 0
    for record in filter(None, records):
        meta, rawpath = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        path = repo / os.fsdecode(rawpath)
        expected[rawpath] = (mode, oid)
        if kind == b'commit':
            links[os.fsdecode(rawpath)] = oid.decode()
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), path
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), path
            actualmode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert actualmode == mode, path
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, path
        count += 1
    index = {}
    for record in filter(None, git(repo, 'ls-files', '-sz').split(b'\0')):
        meta, path = record.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and path not in index
        index[path] = (mode, oid)
    assert index == expected, 'index differs from head tree'
    assert not git(repo, 'status', '--porcelain', '--untracked-files=all'), 'nonclean checkout'
    return count, links

assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
count, links = verify(root, HEAD)
print('HEAD', HEAD)
print('TREE', TREE)
print('ROOT:', count, 'tracked blobs match raw bytes and modes; index exact; clean')
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
             'third_party/tsn-c-stack', 'third_party/lwSRP'):
    count, _ = verify(root / name, links[name])
    print('SUBMODULE:', name, links[name], count, 'tracked blobs/modes and index exact; clean')
print('EXCLUDED: external is uninitialized; no review execution depends on it')
print('PASS: exact head bytes, modes, index and all five required review submodule gitlinks')
