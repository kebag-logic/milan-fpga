#!/usr/bin/env python3
"""Verify both merge contributions and every tracked byte/mode/index entry."""
import argparse, collections, hashlib, json, os, stat, subprocess
from pathlib import Path

HEAD = 'd52bd7f277c6339b13fe7c8ebe849b25f3e14638'
TREE = '7b74e9bc8bee72a089f20b38578ac6d64b474b96'
BASE = 'e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8'
FIRST = '2139f3dc10161b456dfbd51d2f73a63f9164e041'
p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(a.repo), *args])
def tree(ref):
    rows = {}
    for entry in git('ls-tree', '-rz', ref).split(b'\0'):
        if entry:
            meta, path = entry.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            rows[path.decode()] = (mode, kind, oid)
    return rows
parents = git('show', '-s', '--format=%P', HEAD).decode().split()
assert parents[0] == FIRST and len(parents) == 2
assert parents[1].startswith('7e5415e0')
assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
b, f, m, h = [tree(x) for x in (BASE, FIRST, parents[1], HEAD)]
changed = lambda x,y: {k for k in x.keys() | y.keys() if x.get(k) != y.get(k)}
decl, donor = changed(b,f), changed(b,m)
assert decl == {'hdl/packet_engine/KL_pp_originator.sv', 'hdl/packet_engine/KL_pp_rx_validator.sv'}
assert not decl & donor
assert changed(f,h) == donor and changed(m,h) == decl
for k in h:
    assert h[k] == (f[k] if k in decl else m[k]), k
    if k in decl:
        old = git('show', f'{BASE}:{k}').splitlines()
        new = git('show', f'{HEAD}:{k}').splitlines()
        assert collections.Counter(old) == collections.Counter(new), k
        moved = {'hdl/packet_engine/KL_pp_originator.sv':
                 [b'logic                cancel_hit_w;', b'logic [IFL_AW_C-1:0] cancel_ix_w;'],
                 'hdl/packet_engine/KL_pp_rx_validator.sv':
                 [b'logic       fifo_ne_w, fifo_full_w, vq_ne_w, vq_full_w;',
                  b'logic       push_w, vd_push_w, vd_val_w, rd_fire_w, retire_w;']}[k]
        strip_moves = lambda lines: [line for line in lines if line.strip() and line.strip() not in moved]
        assert strip_moves(old) == strip_moves(new), k
index = {}
for row in git('ls-files', '--stage', '-z').split(b'\0'):
    if row:
        meta, path = row.split(b'\t',1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        index[path.decode()] = (mode, oid)
assert index == {k:(v[0],v[2]) for k,v in h.items()}
rows=[]
for name,(mode,kind,oid) in sorted(h.items()):
    path=a.repo/name
    if kind == 'commit':
        assert subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD']).decode().strip()==oid
        rows.append(dict(path=name,mode=mode,gitlink=oid)); continue
    data=os.readlink(path).encode() if mode=='120000' else path.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    actualmode='120000' if path.is_symlink() else ('100755' if path.stat().st_mode & stat.S_IXUSR else '100644')
    assert actual == oid and actualmode == mode, name
    rows.append(dict(path=name,mode=mode,blob=oid,sha256=hashlib.sha256(data).hexdigest()))
assert not git('status','--porcelain=v1','--untracked-files=all','--ignored').strip()
result=dict(head=HEAD,tree=TREE,base=BASE,parents=parents,pp22_paths=sorted(decl),main_paths=sorted(donor),
            overlap=[],merge_contributions_exact=True,pp22_lines_unchanged=True,index_matches=True,
            tracked_entries=len(rows),gitlinks=[r for r in rows if 'gitlink' in r],files=rows)
a.output.write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS exact tree, disjoint contributions: {len(decl)} declaration files + {len(donor)} main files; {len(rows)} tracked entries; {len(result["gitlinks"])} gitlinks')
