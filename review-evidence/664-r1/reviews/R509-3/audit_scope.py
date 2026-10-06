#!/usr/bin/env python3
"""Reproduce merge provenance and source-versus-approval text comparisons."""
import html
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
PACKET = Path(sys.argv[2]).resolve()
HEAD = '4dab80ae4564ef8d6e1030564dcea4ba19235ee6'
APPROVED = '8fb296e3e02985aee27ef04cb08278836b734a14'
DEV = '30e3c018b9add0cb182d8f1229eeec062218130d'
MERGE = 'f48d47cd93cc4b46fad3e537dee661fc2cd3ee6d'
FILES = ['REQUIREMENTS.md', 'docs/design/MAILBOX_SPLIT.md', 'docs/reference/FR_NFR.md']

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], env=dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')).decode()

assert git('rev-parse', 'HEAD').strip() == HEAD
assert git('show', '-s', '--format=%P', MERGE).strip().split() == [APPROVED, DEV]
computed = git('merge-tree', '--write-tree', APPROVED, DEV).strip()
assert computed == git('rev-parse', MERGE + '^{tree}').strip()
print(f'PASS merge provenance: two ordered parents; independent merge tree {computed} equals {MERGE}')
changed = git('diff', '--name-only', MERGE, HEAD).splitlines()
assert sorted(changed) == sorted(FILES)
for name in FILES:
    assert git('rev-parse', f'{APPROVED}:{name}') == git('rev-parse', f'{MERGE}:{name}')
    print(f'PASS {name}: merge preserves approved blob; only the ingress commit changes it')
paths = git('diff', '--name-only', DEV, HEAD).splitlines()
assert all(path.endswith('.md') for path in paths)
print(f'PASS live-dev comparison: {len(paths)} Markdown paths; no RTL, code, tests, generated interface or gitlink delta')
(PACKET / 'ingress.diff').write_text(git('diff', '--no-ext-diff', '--no-textconv', MERGE, HEAD))

def normalize(text):
    text = html.unescape(text).replace('<br>', '\n')
    text = re.sub(r'\[([^\]]+)\]\([^\n]*?\)', r'\1', text)
    return ' '.join(text.split())

sources = {side: {name: normalize(git('show', f'{rev}:{name}')) for name in FILES}
           for side, rev in [('old', APPROVED), ('new', HEAD)]}
body = (PACKET / 'public-pr-body.md').read_text()
section = body.split('## Requirement text for owner approval\n')[1].split('\n## ')[0]
assert 'approved at 8fb296e3' in section
rows = [line.split('|')[1:-1] for line in section.splitlines() if line.startswith('|')][2:]
assert len(rows) == 19
for row in rows:
    assert len(row) == 3
    label, old, new = [cell.strip() for cell in row]
    for side, value in [('old', old), ('new', new)]:
        if value == 'Absent':
            continue
        value = normalize(value)
        assert any(value in text for text in sources[side].values()), f'{label}: {side} cell differs from source'
    print(f'PASS owner-approval old/new source parity: {label}')
print('PASS 19 owner-approval entries; unchanged timing, placement and VERSION rows are outside this table')
