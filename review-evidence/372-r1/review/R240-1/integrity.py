#!/usr/bin/env python3
"""R240 read-only byte/kind/mode/index and required-submodule verification."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path('$VALIDATION_STORAGE/reviews/r240-372-r1')
OUT = Path(__file__).resolve().parent
HEAD = '60c5225fe5f93209bf313c51b7a722f25f9aaa7d'
TREE = '64182178131d03f157fe1a4ec767edee618bc6ff'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0')

def git(repo, *args):
    return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(repo), *args], env=env)

def inspect(repo, commit):
    records = []
    for row in git(repo, 'ls-tree', '-rz', commit).split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        path = repo / os.fsdecode(name)
        if kind == 'commit':
            records.append(dict(path=os.fsdecode(name), mode=mode, oid=oid, gitlink=True))
            continue
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode), path
            raw = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), path
            assert bool(st.st_mode & 0o111) == (mode == '100755'), path
            raw = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert actual == oid, (path, oid, actual)
        records.append(dict(path=os.fsdecode(name), mode=mode, oid=oid, sha256=hashlib.sha256(raw).hexdigest()))
    expected_tree = git(repo, 'rev-parse', commit + '^{tree}').decode().strip()
    index_tree = git(repo, 'write-tree').decode().strip()
    assert index_tree == expected_tree, (repo, index_tree, expected_tree)
    return dict(head=git(repo, 'rev-parse', 'HEAD').decode().strip(), tree=expected_tree,
                index_tree=index_tree, records=records,
                status=git(repo, 'status', '--porcelain=v1', '--untracked-files=normal').decode())

def main():
    parent = inspect(ROOT, HEAD)
    assert parent['head'] == HEAD and parent['tree'] == TREE
    subs = {}
    pins = {r['path']:r['oid'] for r in parent['records'] if r.get('gitlink')}
    for name in ('third_party/verilog-axis', 'protocol-processor', 'gptp-processor'):
        path = ROOT / name
        assert path.is_dir() and not path.is_symlink()
        assert (path / '.git').is_file(), name
        superproject = git(path, 'rev-parse', '--show-superproject-working-tree').decode().strip()
        assert Path(superproject).resolve() == ROOT.resolve(), (name, superproject)
        subs[name] = inspect(path, pins[name])
        assert subs[name]['head'] == pins[name]
    result = dict(parent=parent, required_submodules=subs)
    target = OUT / (sys.argv[1] + '-integrity.json')
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(receipt=str(target), head=HEAD, tree=TREE,
         parent_files=len(parent['records']), submodules={n:dict(head=s['head'], files=len(s['records']))
         for n,s in subs.items()}, initial_or_final=sys.argv[1])))

if __name__ == '__main__':
    main()
