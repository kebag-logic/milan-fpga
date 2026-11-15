#!/usr/bin/env python3
"""Verify raw tracked bytes, modes and index at HEAD, including required pins.
Usage: python3 -B verify_source.py SOURCE PACKET
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

source, packet = [Path(p).resolve() for p in sys.argv[1:]]
HEAD = '1215bd82f4444ee9d4d9b552a711279a1a5bc1d8'
TREE = 'a547c5a7fae9de4f6e7c0aa1ec4e768325dbdc9f'

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def check(root, expected):
    actual = git(root, 'rev-parse', 'HEAD').decode().strip()
    assert actual == expected, (actual, expected)
    entries = git(root, 'ls-tree', '-rz', expected).split(b'\0')
    index = git(root, 'ls-files', '--stage', '-z').split(b'\0')
    expected_index = []
    pins = {}
    count = 0
    for entry in entries:
        if not entry:
            continue
        fields, name = entry.split(b'\t',1)
        mode, kind, oid = fields.split()
        expected_index.append(mode+b' '+oid+b' 0\t'+name)
        if kind == b'commit':
            pins[os.fsdecode(name)] = oid.decode()
            continue
        path = root / os.fsdecode(name)
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, name
            data = path.read_bytes()
        measured = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert measured == oid.decode(), name
        count += 1
    assert sorted(x for x in index if x) == sorted(expected_index)
    return {'head':actual, 'raw_blobs_and_modes_verified':count, 'index_matches':True, 'gitlinks':pins}

assert git(source,'rev-parse','HEAD^{tree}').decode().strip() == TREE
result = {'source':check(source,HEAD),'tree':TREE,'submodules':{}}
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis',
             'third_party/tsn-c-stack','third_party/lwSRP'):
    root = source/name
    assert (root/'.git').is_file(), name
    result['submodules'][name] = check(root,result['source']['gitlinks'][name])
result['status_porcelain'] = git(source,'status','--porcelain=v1','--untracked-files=all').decode()
assert result['status_porcelain'] == ''
result['delta_files'] = git(source,'diff','--name-only','056d619d..HEAD').decode().splitlines()
result['new_comment_identifier_hits'] = []
import re
diff = git(source,'diff','--unified=0','056d619d..HEAD','--','sw/firmware/ctrl/test').decode()
for line in diff.splitlines():
    if line.startswith('+') and not line.startswith('+++') and re.search(r'\bR\d+|issuecomment-|\bB\d+\b|\bround \d+|\blane\b',line):
        result['new_comment_identifier_hits'].append(line)
assert not result['new_comment_identifier_hits']
(packet/'source-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
