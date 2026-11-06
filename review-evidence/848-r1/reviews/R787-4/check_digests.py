#!/usr/bin/env python3
"""Compare every `scripts` digest in the command table with blob bytes, at each named revision.

Reports, per revision, which entries match, which differ and which name a file absent from the tree,
so a pattern already on dev can be told apart from one the reviewed merge introduced.
"""
import hashlib, json, subprocess, sys

def blob(rev, links, path):
    top = path.split('/')[0]
    if top in links:
        r = subprocess.run(['git', '-C', top, 'show', links[top] + ':' + path[len(top) + 1:]], capture_output=True)
    else:
        r = subprocess.run(['git', 'show', rev + ':' + path], capture_output=True)
    return r.stdout if r.returncode == 0 else None

def survey(rev):
    links = {l.split()[3]: l.split()[2] for l in subprocess.check_output(['git', 'ls-tree', rev]).decode().splitlines()
             if l.split()[1] == 'commit'}
    table = json.loads(subprocess.check_output(['git', 'show', rev + ':ci/image/command-table.json']))
    same, differ, absent = set(), set(), set()
    for path, entry in table['scripts'].items():
        data = blob(rev, links, path)
        if data is None:
            absent.add(path)
        elif hashlib.sha256(data).hexdigest() == entry['sha256']:
            same.add(path)
        else:
            differ.add(path)
    return same, differ, absent

revs = dict(dev='3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf', pr849='171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22',
            pr842='8ab3a930d6e2d217caf729d38c5ef17e98e292b3', head='9d5a5af78f95f655e5104056c2c0ee2cca689279')
res = {k: survey(v) for k, v in revs.items()}
for k, (s, d, a) in res.items():
    print(k, 'match', len(s), 'differ', len(d), 'absent', len(a))
dv, hd = res['dev'], res['head']
print('differ at head, not at dev:', sorted(hd[1] - dv[1]))
print('differ at dev, not at head:', sorted(dv[1] - hd[1]))
print('absent at head, not at dev:', sorted(hd[2] - dv[2]))
print('absent at dev, not at head:', sorted(dv[2] - hd[2]))
print('absent at head:', sorted(hd[2]))
for p in ('scripts/docs_inventory.py', 'tb/verilator/fw_service_budget/run.py', 'tb/verilator/nvm_capture_cpu/run.py',
          'tb/verilator/nvm_capture_cpu/soc.py'):
    print(p, 'match at head' if p in hd[0] else 'NOT MATCHED AT HEAD')
print('differ at head:', sorted(hd[1]))
