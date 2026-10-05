"""Verify tracked working bytes, file kinds, executable modes, index and pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '2263c6288956a5edd841df62252326780edd4870'
TREE = '04234de69a17538c76eff84e001cb4ec2c742a04'

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def verify(root, revision):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == revision
    index = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0', path
        index[path] = (mode, oid)
    entries = {}
    blobs = 0
    links = {}
    for entry in git(root, 'ls-tree', '-rz', 'HEAD').split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        entries[name] = (mode, oid)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        p = root / os.fsdecode(name)
        st = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert (b'100755' if st.st_mode & 0o111 else b'100644') == mode, name
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), name
        blobs += 1
    assert index == entries, 'index does not equal committed tree'
    return dict(head=revision, tree=git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(), blobs=blobs, gitlinks=links, bytes_modes_index_equal=True)

root = Path(sys.argv[1]).resolve()
results = {'parent': verify(root, HEAD)}
assert results['parent']['tree'] == TREE
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    sub = root / name
    assert (sub / '.git').is_file(), 'required registered submodule missing'
    assert git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(root)
    results[name] = verify(sub, results['parent']['gitlinks'][name])
results['external'] = 'Not required by this review; committed gitlink verified in the parent index.'
print(json.dumps(results, indent=2))
