#!/usr/bin/env python3
"""Reproduce the round-3 scope and public approval-table checks, read-only."""
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
PR_JSON = Path(sys.argv[2])
HEAD = '4dab80ae4564ef8d6e1030564dcea4ba19235ee6'
APPROVED = '8fb296e3e02985aee27ef04cb08278836b734a14'
DEV = '30e3c018b9add0cb182d8f1229eeec062218130d'
MERGE = 'f48d47cd93cc4b46fad3e537dee661fc2cd3ee6d'
BASE = '423ac5d910d09ab189b3acc39ae3ae1d10d50b19'
FILES = ['REQUIREMENTS.md', 'docs/design/MAILBOX_SPLIT.md', 'docs/reference/FR_NFR.md']
ENV = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0'}


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], env=ENV)


def norm(text):
    text = re.sub(r'\[([^\]]+)\]\([^\n]*?\)', r'\1', text)
    return ' '.join(html.unescape(text.replace('<br>', '\n')).split())


assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == 'bcca74ee4dd8c8a4a45b26e0b7accda5131f9ce1'
assert git('show', '-s', '--format=%P', MERGE).decode().split() == [APPROVED, DEV]
calculated = git('merge-tree', '--write-tree', APPROVED, DEV).decode().strip()
assert calculated == git('rev-parse', MERGE + '^{tree}').decode().strip()
print('PASS: approved text and dev merge reproduces exact merge tree', calculated)
changed = git('diff', '--name-only', MERGE, HEAD).decode().splitlines()
assert changed == FILES, changed
print('PASS: authored round-3 delta contains exactly three Markdown files')
for file in FILES:
    before = git('show', APPROVED + ':' + file)
    assert before == git('show', MERGE + ':' + file)
    print('PASS: pre-filter bytes equal approved head:', file, hashlib.sha256(before).hexdigest())
for left, right, title in [(BASE, HEAD, 'full requested base delta'), (APPROVED, HEAD, 'approved-to-head delta'), (MERGE, HEAD, 'authored filter delta')]:
    patch = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames', left, right)
    print(title, 'bytes', len(patch), 'sha256', hashlib.sha256(patch).hexdigest())
protected = ['sw/mailbox/mailbox.yaml', 'hdl/milan/mailbox', 'sw/firmware/ctrl', 'tb/verilator/mbx', 'docs/ARCHITECTURE_HW_SW_SPLIT.md']
assert not git('diff', '--raw', APPROVED, HEAD, '--', *protected)
print('PASS: mailbox contract, RTL, firmware, executable suite, and split architecture unchanged')

pr = json.loads(PR_JSON.read_text())
assert pr['head']['sha'] == HEAD
body = pr['body']
section = body.split('## Requirement text for owner approval\n', 1)[1].split('\n## ', 1)[0]
assert '**approved at 8fb296e3**' in section
rows = [line for line in section.splitlines() if line.startswith('| ')][1:]
assert len(rows) == 19, len(rows)
sources = {ref: {file: norm(git('show', ref + ':' + file).decode()) for file in FILES} for ref in [APPROVED, HEAD]}
for row in rows:
    cells = row.strip('| ').split(' | ')
    assert len(cells) == 3, cells[0]
    label, old, new = cells
    for ref, cell in [(APPROVED, old), (HEAD, new)]:
        if cell == 'Absent':
            continue
        matches = [file for file, text in sources[ref].items() if norm(cell) in text]
        assert matches, (label, ref)
    print('PASS: approval old/new text matches source:', label)
print('PASS: public owner-approval section has 19 filter-only rows')
