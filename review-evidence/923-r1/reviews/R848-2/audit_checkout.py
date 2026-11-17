#!/usr/bin/env python3
"""Check actual tracked bytes, file kinds/modes, index and required gitlinks against immutable commits."""
import ast
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
head = 'd06ded5ad3d6eb26bfd79787260adcdcc7d3f80b'
tree = 'c6c0397815848b804297d8fe001d88e722b35f49'
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'}
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)
def audit(root, commit):
    assert git(root, 'rev-parse', 'HEAD').decode().strip() == commit
    entries = git(root, 'ls-tree', '-rz', commit).split(b'\0')
    expected = {}
    links = {}
    checked = 0
    for entry in filter(None, entries):
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        name = os.fsdecode(name)
        expected[name] = (mode, oid, b'0')
        if mode == b'160000':
            links[name] = oid.decode()
            continue
        path = root / name
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid.decode(), name
        checked += 1
    index = {}
    for row in filter(None, git(root, 'ls-files', '--stage', '-z').split(b'\0')):
        meta, name = row.split(b'\t', 1)
        mode, oid, stage = meta.split()
        name = os.fsdecode(name)
        assert name not in index
        index[name] = (mode, oid, stage)
    assert index == expected, 'index differs from commit tree'
    print(root.name, commit, 'tracked blobs/modes/index PASS:', checked)
    return links

assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == tree
links = audit(repo, head)
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/tsn-c-stack', 'third_party/lwSRP'):
    audit(repo / sub, links[sub])
    assert (repo / sub / '.git').is_file(), sub
    print('Required gitlink PASS:', sub, links[sub])
delta = git(repo, 'diff', '--name-only', '70c100da', head).decode().splitlines()
expected_delta = ['sw/firmware/ctrl/aecp/README.md', 'sw/firmware/ctrl/plat/README.md',
                  'sw/firmware/ctrl/test/aecp_map_mutants.py', 'sw/firmware/ctrl/test/test_aecp.cpp',
                  'sw/litex/ctrl_memory.py']
assert delta == expected_delta, delta
path = 'sw/litex/ctrl_memory.py'
before = ast.dump(ast.parse(git(repo, 'show', '70c100da:' + path)))
after = ast.dump(ast.parse((repo / path).read_bytes()))
assert before == after
print('Delta census PASS: five expected files; ctrl_memory.py AST identical; no compiled product source or gitlink changed.')
print('Head:', head)
print('Tree:', tree)
