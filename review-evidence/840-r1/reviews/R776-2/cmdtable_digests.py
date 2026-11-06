#!/usr/bin/env python3
"""Compare every sha256 the command table records with the file it names.
usage: cmdtable_digests.py <repo> <rev> [<rev> ...]"""
import hashlib, json, subprocess, sys
repo = sys.argv[1]
def show(rev, path):
    r = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def walk(node, path=()):
    if isinstance(node, dict):
        if 'sha256' in node and path: yield path[-1], node['sha256']
        for k, v in node.items(): yield from walk(v, path + (k,))
    elif isinstance(node, list):
        for v in node: yield from walk(v, path)
res = {}
for rev in sys.argv[2:]:
    table = json.loads(show(rev, 'ci/image/command-table.json'))
    bad = []; n = 0
    for name, digest in walk(table):
        data = show(rev, name)
        if data is None: continue
        n += 1
        if hashlib.sha256(data).hexdigest() != digest: bad.append(name)
    res[rev] = set(bad)
    print(rev[:12], 'digests compared', n, 'mismatches', len(bad))
    print('  ' + ' '.join(sorted(bad)))
revs = sys.argv[2:]
if len(revs) == 2:
    print('added by', revs[0][:12], sorted(res[revs[0]] - res[revs[1]]))
    print('removed by', revs[0][:12], sorted(res[revs[1]] - res[revs[0]]))
