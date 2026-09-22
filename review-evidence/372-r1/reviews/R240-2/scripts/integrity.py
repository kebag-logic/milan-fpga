#!/usr/bin/env python3
"""Prove tracked bytes/kinds/modes and exact index, including required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
repo = Path(sys.argv[1]).resolve()
head = '059c3a60b8290873ed9fd14673f9981e8af754ce'
tree = '600468436fb9435a6b15c41db0156e5304848cb6'

def git(path, *args):
    return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(path), *args])

def check(path, revision):
    assert git(path, 'rev-parse', 'HEAD').decode().strip() == revision
    records = git(path, 'ls-tree', '-rz', revision).split(b'\0')[:-1]
    expected_index = []
    files, links = [], {}
    for record in records:
        meta, filename = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = os.fsdecode(filename)
        expected_index.append(mode.encode() + b' ' + oid.encode() + b' 0\t' + filename)
        if kind == 'commit':
            links[name] = oid
            continue
        file = path / name
        st = file.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = '100755' if st.st_mode & stat.S_IXUSR else '100644'
            assert actual_mode == mode, name
            data = file.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, name
        files.append(dict(path=name, mode=mode, blob=oid, bytes=len(data)))
    assert git(path, 'ls-files', '--stage', '-z').split(b'\0')[:-1] == expected_index
    flags = git(path, 'ls-files', '-v', '-z').split(b'\0')[:-1]
    assert all(item[:1] == b'H' for item in flags), 'hidden or sparse index entries'
    status = git(path, 'status', '--porcelain=v1', '--untracked-files=all').decode()
    assert not status, status
    return dict(head=revision, tree=git(path, 'rev-parse', revision+'^{tree}').decode().strip(),
                index_records=len(records), files=files, gitlinks=links,
                status=status, hidden_index_entries=0)

result = check(repo, head)
assert result['tree'] == tree
result['required_submodules'] = {}
for name in ['third_party/verilog-axis', 'protocol-processor', 'gptp-processor']:
    sub = repo / name
    assert sub.is_dir() and not sub.is_symlink()
    assert (sub / '.git').is_file(), name
    assert git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip() == str(repo)
    result['required_submodules'][name] = check(sub, result['gitlinks'][name])
print(json.dumps(result, indent=2))
