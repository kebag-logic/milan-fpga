#!/usr/bin/env python3
"""Compare tracked bytes, modes, index and required submodules to their commits."""
import hashlib, os, stat, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def check(repo, commit):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == commit
    entries = git(repo, 'ls-tree', '-rz', commit).split(b'\0')
    expected = []
    links = {}
    count = 0
    for row in entries:
        if not row: continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected.append(mode + b' ' + oid + b' 0\t' + name)
        rel = os.fsdecode(name)
        path = repo / rel
        if mode == b'160000':
            links[rel] = oid.decode()
            continue
        if mode == b'120000':
            assert path.is_symlink(), rel
            data = os.fsencode(os.readlink(path))
        else:
            info = path.lstat()
            assert stat.S_ISREG(info.st_mode), rel
            assert bool(info.st_mode & 0o111) == (mode == b'100755'), rel
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), rel
        count += 1
    assert git(repo, 'ls-files', '--stage', '-z').split(b'\0')[:-1] == expected
    print(f'PASS {repo.name}: {count} tracked blob bytes/modes; complete index equals {commit}')
    return links
head = '011aaa6f080321e0a89f915720ebb3ee14807a16'
assert git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() == '5b11a07de8c4f69999277424aa8d9b704c297a96'
links = check(root, head)
for path in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'):
    assert (root / path / '.git').is_file(), path
    check(root / path, links[path])
    print('GITLINK', path, links[path])
print('UNINITIALIZED external gitlink retained:', links['external'])
status = git(root, 'status', '--porcelain=v1', '--untracked-files=all').decode()
assert not status, status
print('PASS clean source checkout, including untracked-file status')
commit = git(root, 'cat-file', 'commit', '0cad829e1af15b9c96b0ef3d10d109b9721154c5')
print('EVIDENCE COMMIT SIGNATURE:', 'present' if b'\ngpgsig ' in commit else 'absent (unsigned; hashes are not signature authentication)')
