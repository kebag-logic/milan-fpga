#!/usr/bin/env python3
"""Search every tracked Markdown file of the head for each removed entry's quote and `also`
spellings, using the generator's own normalisation (flatten/carried_line).
Usage: python3 -I removed_quote_sweep.py <repo> <old-rev>"""
import json, subprocess, sys
repo, old_rev = sys.argv[1:3]
sys.path.insert(0, repo + '/scripts')
import docs_inventory as di
old = json.loads(subprocess.check_output(['git', '-C', repo, 'show', f'{old_rev}:scripts/docs_inventory.json'], text=True))
new = json.load(open(repo + '/scripts/docs_inventory.json'))
keep = {f['id'] for f in new['findings']}
files = subprocess.check_output(['git', '-C', repo, 'ls-files', '*.md'], text=True).split()
flats = {p: di.flatten(open(repo + '/' + p, encoding='utf-8').read()) for p in files}
print('markdown files searched', len(files))
hits = 0
for f in old['findings']:
    if f['id'] in keep:
        continue
    for s in (f['quote'], *f.get('also', [])):
        where = [p for p, fl in flats.items() if di.carried_line(fl, s) is not None]
        hits += len(where)
        print(f['id'], repr(s[:60]), '->', where or 'nowhere')
print('total pages carrying a removed statement', hits)
