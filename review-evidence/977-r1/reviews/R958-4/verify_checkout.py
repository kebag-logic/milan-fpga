#!/usr/bin/env python3
"""Check exact tracked bytes, modes, index and required submodule pins without trusting status."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = '3256d1d21e525e564eb92d1cf721750ddf44fde2'
required = {'protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/lwSRP', 'third_party/tsn-c-stack'}
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(at, *args):
    return subprocess.check_output(['git', '-C', str(at), *args], env=env)
def verify(at, revision, recurse=False):
    assert git(at, 'rev-parse', 'HEAD').decode().strip() == revision
    tree = git(at, 'ls-tree', '-rz', revision)
    expected_index = {}
    count = 0
    links = {}
    for row in tree.split(b'\0'):
        if not row:
            continue
        meta, rawpath = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        name = os.fsdecode(rawpath)
        expected_index[rawpath] = (mode, oid, b'0')
        target = at / name
        if kind == b'commit':
            links[name] = {'pin': oid.decode(), 'initialized': (target / '.git').exists()}
            if recurse and name in required:
                assert (target / '.git').is_file() and not target.is_symlink()
                links[name]['verification'] = verify(target, oid.decode())
            continue
        st = target.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            content = os.fsencode(os.readlink(target))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert mode == actual_mode, name
            content = target.read_bytes()
        actual_oid = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        assert actual_oid == oid.decode(), name
        count += 1
    index = {}
    for row in git(at, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, oid, stage = meta.split()
            assert path not in index
            index[path] = mode, oid, stage
    assert index == expected_index, 'index differs from committed tree'
    return {'head': revision, 'tree': git(at, 'rev-parse', revision + '^{tree}').decode().strip(),
            'tracked_blobs_verified': count, 'index_equal': True, 'gitlinks': links}

out = verify(root, head, True)
assert out['tree'] == '6810c12ebf0f060a9557e3fbe356a99cffef8c2a'
files = ['sw/firmware/ctrl/' + p for p in ['app/ctrl_app.h', 'app/ctrl_app_srp.c',
         'loop/ctrl_loop.h', 'srp/srp_mbx.c', 'srp/srp_mbx.h', 'plat/ctrl_split_hot.txt']]
out['product_token_equality_to_25ff0632'] = {}
def tokens(text, path):
    if path.endswith('.txt'):
        return [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith('#')]
    regex = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*.*?\*/'
    text = re.sub(regex, lambda m: ' ' if m[0].startswith(('/',)) else m[0], text, flags=re.S)
    return re.findall(r'\w+|[^\s]', text)
for name in files:
    before = git(root, 'show', '25ff0632:' + name).decode()
    after = (root / name).read_text()
    assert tokens(before, name) == tokens(after, name), name
    out['product_token_equality_to_25ff0632'][name] = True
out['status_porcelain'] = git(root, 'status', '--porcelain=v1').decode()
assert not out['status_porcelain']
print(json.dumps(out, indent=2))
