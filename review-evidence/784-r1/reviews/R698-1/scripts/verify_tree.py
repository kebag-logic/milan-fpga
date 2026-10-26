"""Verify worktree bytes and modes directly, independently of index flags."""
import hashlib
import os
import pathlib
import stat
import subprocess
import sys

root = pathlib.Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])

head = git('rev-parse', 'HEAD').decode().strip()
assert head == '42dbe6bd42c950a7acedce56fcf29b82543123c6'
tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
assert tree == '5fdfce709af95cf8bfe7efc1083cca5162b62d1f'
expected = {}
links = {}
for entry in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not entry:
        continue
    header, name = entry.split(b'\t', 1)
    mode, kind, oid = header.decode().split()
    path = root / os.fsdecode(name)
    expected[name] = (mode, oid)
    if kind == 'commit':
        links[os.fsdecode(name)] = oid
        continue
    st = path.lstat()
    if mode == '120000':
        assert stat.S_ISLNK(st.st_mode), name
        data = os.fsencode(os.readlink(path))
    else:
        assert stat.S_ISREG(st.st_mode), name
        assert bool(st.st_mode & 0o111) == (mode == '100755'), name
        data = path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert actual == oid, name
index = {}
for entry in git('ls-files', '-s', '-z').split(b'\0'):
    if not entry:
        continue
    header, name = entry.split(b'\t', 1)
    mode, oid, stage = header.decode().split()
    assert stage == '0'
    index[name] = (mode, oid)
assert index == expected
assert git('diff', '--name-only', 'd385b38e', 'HEAD', '--', '.github') == b''
assert len(links) == 6
for name, oid in links.items():
    path = root / name
    populated = (path / '.git').exists()
    if populated:
        got = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD']).decode().strip()
        assert got == oid, name
    print('GITLINK', name, oid, 'checkout verified' if populated else 'not initialized; tree/index pin verified')
print('HEAD', head)
print('TREE', tree)
print('TRACKED_BYTES_MODES_INDEX_PASS', len(expected) - len(links), 'blobs')
print('WORKFLOWS_BYTE_IDENTICAL_TO_BASE_PASS')
print('STATUS', git('status', '--porcelain=v1').decode().strip() or 'clean')
