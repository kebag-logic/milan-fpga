"""Independently hash tracked checkout bytes, kinds, modes and index entries."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument('checkout', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.run(['rtk', 'proxy', 'git', '-C', str(root), '--no-replace-objects', *args],
                          env=env, capture_output=True, check=True).stdout

def inspect(root, expected=None):
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    if expected:
        assert head == expected, (root, head, expected)
    entries = git(root, 'ls-tree', '-r', '-z', '--full-tree', 'HEAD').split(b'\0')[:-1]
    index = git(root, 'ls-files', '--stage', '-z').split(b'\0')[:-1]
    expected_index = []
    rows, links = [], {}
    for entry in entries:
        metadata, name = entry.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + name)
        rel = os.fsdecode(name)
        path = root / rel
        if mode == b'160000':
            links[rel] = oid.decode()
            continue
        s = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(s.st_mode), path
            data = os.fsencode(os.readlink(path))
            actual_mode = '120000'
        else:
            assert stat.S_ISREG(s.st_mode), path
            data = path.read_bytes()
            actual_mode = '100755' if s.st_mode & stat.S_IXUSR else '100644'
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), (path, actual, oid)
        assert actual_mode == mode.decode(), (path, actual_mode, mode)
        rows.append({'path':rel, 'blob':actual, 'mode':actual_mode, 'kind':kind.decode(),
                     'size':len(data), 'sha256':hashlib.sha256(data).hexdigest()})
    assert sorted(index) == sorted(expected_index), root
    status = git(root, 'status', '--porcelain=v2', '--untracked-files=all')
    assert not status, (root, status)
    index_path = Path(os.fsdecode(git(root, 'rev-parse', '--git-path', 'index').rstrip(b'\n')))
    if not index_path.is_absolute():
        index_path = root / index_path
    return {'head':head, 'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),
            'index_sha256':hashlib.sha256(index_path.read_bytes()).hexdigest(),
            'index_entries_match_head':True, 'status':'clean', 'files':rows, 'gitlinks':links}

root = a.checkout.resolve()
result = {'root':inspect(root, 'b911c11671cae329a99f5e413133b4bf6357fa7f'), 'submodules':{}}
assert result['root']['tree'] == '4dd73d4c4f2ff352e65703d476dcd44494ffdb8e'
for rel in ['third_party/verilog-axis', 'protocol-processor', 'gptp-processor']:
    sub = root / rel
    assert sub.is_dir() and not sub.is_symlink()
    superproject = git(sub, 'rev-parse', '--show-superproject-working-tree').decode().strip()
    assert Path(superproject).resolve() == root, (rel, superproject)
    result['submodules'][rel] = inspect(sub, result['root']['gitlinks'][rel])
result['submodule_status'] = git(root, 'submodule', 'status').decode()
result['result'] = 'PASS'
a.output.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'result':'PASS','head':result['root']['head'], 'root_files':len(result['root']['files']),
                  'submodules':{k: {'head':v['head'],'files':len(v['files'])} for k,v in result['submodules'].items()}}))
