#!/usr/bin/env python3
"""Read-only exact-byte, merge, adoption and evidence checks. Run from the candidate."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

HEAD = '5428b044176f95248e6916dc00dd89c0df154078'
BASE = 'e21c1ca024d37ea188ad15b5c8f9c2dae18628df'
OLD = 'ead8036035affd53ef4b29979190f2f4f67084c0'
PIN = '2ad2f845dd583f8310075fa2380cb60a04fd091a'
EVIDENCE = '8d4e0732588d09f1f94f41aea7c7c39110da09a2'
ROOT = Path.cwd()
PACKET = Path(__file__).resolve().parent
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(*args, cwd=ROOT, extra=None):
    return subprocess.check_output(['git', *args], cwd=cwd, env=env | (extra or {}))

def tree(rev, cwd=ROOT):
    result = {}
    for entry in git('ls-tree', '-rz', rev, cwd=cwd).split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        result[os.fsdecode(name)] = (mode, kind, oid)
    return result

def integrity(cwd, rev):
    expected = tree(rev, cwd)
    errors = []
    links = {}
    for name, (mode, kind, oid) in expected.items():
        path = cwd / name
        if mode == '160000':
            links[name] = oid
            continue
        try:
            st = path.lstat()
            if mode == '120000':
                assert stat.S_ISLNK(st.st_mode)
                content = os.fsencode(os.readlink(path))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode & 0o111) == (mode == '100755')
                content = path.read_bytes()
            actual = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
            assert actual == oid
        except (OSError, AssertionError):
            errors.append(name)
    expected_tree = git('rev-parse', rev + '^{tree}', cwd=cwd).decode().strip()
    index_tree = git('write-tree', cwd=cwd).decode().strip()
    flags = git('ls-files', '-v', cwd=cwd).decode().splitlines()
    hidden = [line for line in flags if line[0] != 'H']
    assert not errors and expected_tree == index_tree and not hidden, (errors, hidden)
    return dict(blobs=len(expected)-len(links), tree=expected_tree, index_tree=index_tree,
                byte_mode_errors=errors, hidden_index_flags=hidden, gitlinks=links)

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
result = {'head': HEAD, 'integrity': {'parent': integrity(ROOT, HEAD)}}
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    pin = result['integrity']['parent']['gitlinks'][sub]
    assert git('rev-parse', 'HEAD', cwd=ROOT/sub).decode().strip() == pin
    result['integrity'][sub] = integrity(ROOT/sub, pin)

merges = []
for rev in git('rev-list', '--first-parent', '--merges', BASE+'..'+HEAD).decode().split():
    parents = git('show', '-s', '--format=%P', rev).decode().split()
    merged = git('merge-tree', '--write-tree', *parents).decode().splitlines()
    actual = git('rev-parse', rev+'^{tree}').decode().strip()
    assert merged == [actual]
    merges.append(dict(head=rev, parents=parents, computed_tree=merged[0], conflict_free=True))
result['merges'] = merges

top='hdl/top/protocol_processor_top.sv'
before=git('show', OLD+':'+top, cwd=ROOT/'protocol-processor')
after=git('show', PIN+':'+top, cwd=ROOT/'protocol-processor')
assert before == after
result['processor_top_sha256'] = hashlib.sha256(after).hexdigest()
result['processor_changed_rtl'] = git('diff', '--name-only', OLD, PIN, '--', 'hdl', cwd=ROOT/'protocol-processor').decode().splitlines()

paths=git('diff','--name-only','591a5752',HEAD).decode().splitlines()
assert len(paths)==24
for p in paths:
    assert tree(BASE)[p] == tree(HEAD)[p]
result['imported_paths_unchanged_from_dev'] = paths
result['parent_lane_delta'] = git('diff','--name-only',BASE,HEAD).decode().splitlines()

with tempfile.TemporaryDirectory(dir=PACKET/'scratch', prefix='patch-index-') as tmp:
    ien={'GIT_INDEX_FILE':str(Path(tmp)/'index')}
    git('read-tree',BASE,extra=ien)
    patches=[]
    for name in ('parent-adoption-148-6c22d3ca.patch','parent-adoption-22-28f9666f.patch'):
        patch=git('show',EVIDENCE+':review-evidence/682-r1/author/'+name)
        path=Path(tmp)/name;path.write_bytes(patch)
        git('apply','--cached',str(path),extra=ien)
        patches.append(dict(name=name,sha256=hashlib.sha256(patch).hexdigest()))
    for path in ('tb/verilator/milan_dp/sim_nxn.cpp','scripts/xvlog.budget'):
        assert git('show',':'+path,extra=ien) == git('show',HEAD+':'+path)
    result['adoption_patch_replay']={'patches':patches,'exact_final_blobs':True}

base=json.loads(git('show',BASE+':syn/ooc/pp_resource_baseline.json'))
head=json.loads(Path('syn/ooc/pp_resource_baseline.json').read_text())
result['resource_baseline_keys']=list(head)
def policies(x):
    if isinstance(x,dict):
        found = []
        for k,v in x.items():
            if k in ('tolerance','floor','ceiling'): found.append((k,v))
            elif isinstance(v,(dict,list)): found.extend(policies(v))
        return found
    if isinstance(x,list): return [p for v in x for p in policies(v)]
    return []
assert policies(base) and policies(base)==policies(head)
result['resource_policies_unchanged']=True
print(json.dumps(result,indent=2))
