#!/usr/bin/env python3
"""Compare scripts/docs_inventory.json between two commits of a checkout and
check the removed-entry claims of PR #825 round 8.
Usage: python3 -I inventory_delta.py <repo> <old-rev> <new-rev>"""
import json, subprocess, sys, re
repo, old_rev, new_rev = sys.argv[1:4]
def show(rev, path):
    return subprocess.check_output(['git', '-C', repo, 'show', f'{rev}:{path}'], text=True)
old = json.loads(show(old_rev, 'scripts/docs_inventory.json'))
new = json.loads(show(new_rev, 'scripts/docs_inventory.json'))
for k in old:
    if k != 'findings':
        print(f'key {k}: unchanged={old[k] == new.get(k)}')
print('keys equal:', sorted(old) == sorted(new))
oid = [f['id'] + '|' + f['page'] for f in old['findings']]
nid = [f['id'] + '|' + f['page'] for f in new['findings']]
removed = [x for x in oid if x not in nid]
added = [x for x in nid if x not in oid]
print('old count', len(oid), 'new count', len(nid))
print('removed', len(removed), removed)
print('added', added)
# every kept entry byte-identical and in same relative order
oldkept = [f for f in old['findings'] if f['id'] + '|' + f['page'] in nid]
print('kept entries identical and same order:', oldkept == new['findings'])
rem_ids = sorted({x.split('|')[0] for x in removed})
print('removed ids', rem_ids)
pages = {'docs/reference/REGISTER_MAP.md', 'docs/reference/REGISTER_MAP_CLASSES.md'}
print('removed pages subset of two register pages:', {x.split('|')[1] for x in removed} <= pages)
left = [f['id'] + '|' + f['page'] for f in new['findings'] if f['id'] in rem_ids]
print('rows of removed ids left in json:', left)
for p in sorted(pages):
    print('remaining on', p, [f['id'] for f in new['findings'] if f['page'] == p])
for i in ('D0-040', 'D0-057'):
    print(i, 'pages', [f['page'] for f in new['findings'] if f['id'] == i])
audit = show(new_rev, 'docs/DOCUMENTATION_AUDIT.md')
for i in rem_ids:
    hits = [l for l in audit.splitlines() if re.search(r'\b' + i + r'\b', l)]
    print('audit lines naming', i, len(hits))
print('audit re-verify count', audit.count('| re-verify: quote not found |'))
oaudit = show(old_rev, 'docs/DOCUMENTATION_AUDIT.md')
print('old audit re-verify count', oaudit.count('| re-verify: quote not found |'))
for p in sorted(pages):
    for a, tag in ((oaudit, 'old'), (audit, 'new')):
        n = sum(1 for l in a.splitlines() if '| re-verify: quote not found |' in l and l.split('|')[2].strip().find(p.split('/')[-1] + ']') >= 0)
        print(tag, p, 're-verify rows', n)
