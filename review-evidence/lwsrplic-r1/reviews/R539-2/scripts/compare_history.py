#!/usr/bin/env python3
"""Pair every original/revised commit using exact preserved identity and message."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

old, new = map(Path, sys.argv[1:3])
removed = bytes.fromhex('434c415544452e6d64').decode()
def git(repo, *args):
    return subprocess.check_output(['git','-C',str(repo),*args])
def commits(repo):
    out = {}
    for oid in git(repo,'rev-list','--all').decode().splitlines():
        raw = git(repo,'cat-file','commit',oid)
        header, message = raw.split(b'\n\n',1)
        key = b'\n'.join(line for line in header.splitlines() if line.startswith((b'author ',b'committer ',b'encoding '))) + b'\n\n' + message
        assert key not in out
        out[key] = (oid, raw)
    return out
def tree(repo, oid):
    out = {}
    for entry in git(repo,'ls-tree','-rz',oid).split(b'\0'):
        if entry:
            meta,name=entry.split(b'\t',1)
            out[name.decode()] = meta.decode().split()
    return out
before, after = commits(old), commits(new)
assert before.keys() == after.keys(), (len(before), len(after))
mapping = {before[k][0]:after[k][0] for k in before}
removed_trees, removed_lines, signatures = 0, 0, 0
for key in before:
    a, ar = before[key]
    b, br = after[key]
    oldparents = [line[7:].decode() for line in ar.split(b'\n\n',1)[0].splitlines() if line.startswith(b'parent ')]
    newparents = [line[7:].decode() for line in br.split(b'\n\n',1)[0].splitlines() if line.startswith(b'parent ')]
    assert [mapping[x] for x in oldparents] == newparents
    ta,tb = tree(old,a),tree(new,b)
    if removed in ta:
        del ta[removed]
        removed_trees += 1
    assert ta.keys() == tb.keys(), (a,b)
    for name,entry in ta.items():
        assert entry[:2] == tb[name][:2], (a,b,name)
        if entry[2] != tb[name][2]:
            assert name == 'doc/architecture.md', (a,b,name)
            content = git(old,'cat-file','blob',entry[2])
            cleaned = b''.join(line for line in content.splitlines(keepends=True) if removed.encode() not in line)
            assert content != cleaned
            assert cleaned == git(new,'cat-file','blob',tb[name][2]), (a,b,name)
            removed_lines += 1
    signatures += b'\ngpgsig ' in ar and b'\ngpgsig ' not in br
    print('PASS',a,b,'identity/message/parent-map/allowed-tree-delta')
print('Paired commits:',len(mapping))
print('Original file removals across commit trees:',removed_trees)
print('Architecture line removals across commit trees:',removed_lines)
print('Commit signatures removed by rewriting:',signatures)
print('Authorship, committer identity/timestamps, message bytes, parent topology, other blobs/modes: PASS')
for name in ['apache-2.0','docs-public','f4-stack','main','mark2-port','tests-harness']:
    revised=git(new,'rev-parse','refs/remotes/origin/'+name).decode().strip()
    original=next(a for a,b in mapping.items() if b==revised)
    oldtree=git(old,'rev-parse',original+'^{tree}').decode().strip()
    newtree=git(new,'rev-parse',revised+'^{tree}').decode().strip()
    print('BRANCH',name,'old',original,'new',revised,'oldtree',oldtree,'newtree',newtree,'tree_equal',oldtree==newtree)
head='4eba61b7b1c49fc9b7260a487240ca86f9d38168'
original=next(a for a,b in mapping.items() if b==head)
assert original=='1a1d6cbe4f971d2d346b948dd2e9716421f211e9'
assert git(old,'rev-parse',original+'^{tree}') == git(new,'rev-parse',head+'^{tree}')
print('Exact reviewed head tree preserved: PASS')
