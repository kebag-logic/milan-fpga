"""Verify raw tracked bytes, file modes, index and all required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parent
ENV = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'}

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)

def verify(root, expected):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == expected
    rows = git(root, 'ls-tree', '-rz', expected).split(b'\0')
    blobs, links = 0, {}
    for row in rows:
        if not row:
            continue
        header, raw_path = row.split(b'\t',1)
        mode, kind, oid = header.split()
        relative = os.fsdecode(raw_path)
        path = root / relative
        if kind == b'commit':
            links[relative] = oid.decode()
            continue
        status = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(status.st_mode), relative
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(status.st_mode), relative
            actual_mode = b'100755' if status.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, relative
            data = path.read_bytes()
        actual = hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        assert actual == oid.decode(), relative
        blobs += 1
    tree = git(root, 'rev-parse', expected+'^{tree}').decode().strip()
    assert git(root, 'write-tree').decode().strip() == tree
    assert not git(root, 'status', '--porcelain=v1', '--untracked-files=no')
    return {'head': expected, 'tree': tree, 'raw_blobs_and_modes_checked': blobs,
            'index_matches': True, 'gitlinks': links}

result = {'superproject': verify(ROOT, '1c4d722cb1d0279f0ec44b0fbe87c810adfb9267'), 'submodules': {}}
for path, pin in result['superproject']['gitlinks'].items():
    if path == 'external':
        continue
    sub = ROOT / path
    assert (sub / '.git').is_file(), path
    result['submodules'][path] = verify(sub, pin)
(PACKET/'restore-check.json').write_text(json.dumps(result, indent=2)+'\n')
print('PASS: exact tracked bytes, modes, index and five required submodule pins verified; external gitlink unchanged')
