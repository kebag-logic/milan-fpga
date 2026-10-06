#!/usr/bin/env python3
"""Audit the public corrections against exact source objects; no source writes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

HEAD = '6c94e9f5f496ac25f8c4e31f9e3685c725de29f3'
BASE = '6714181d0c8a16e2983f85b724f4d688f5111835'
TREE = '25b32c793bd4bb6d959640094a44fb2b5c9d7a45'
ap = argparse.ArgumentParser()
ap.add_argument('checkout', type=Path)
ap.add_argument('packet', type=Path)
args = ap.parse_args()
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'}

def git(*argv):
    return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(args.checkout), *argv], env=env).decode()

def rows(rev):
    text = git('show', f'{rev}:sw/firmware/gtest/README.md')
    start = text.index('| File | Function | Statement | Uncovered | Why no input reaches it |')
    table = text[start:].split('\n\n', 1)[0].splitlines()[2:]
    parsed = [[v.strip() for v in row.strip().strip('|').split('|')] for row in table]
    assert all(len(row) == 5 for row in parsed)
    return parsed

assert git('rev-parse', 'HEAD').strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').strip() == TREE
before, after = rows(BASE), rows(HEAD)
assert len(before) == len(after) == 14
assert [r[:4] for r in before] == [r[:4] for r in after]
adp = [r for r in after if r[0] == '`sw/firmware/ctrl/adp/adp.c`']
assert len(adp) == 5
assert all('no-callback rule in `adp.h`' in r[4] for r in adp)
pr = json.loads((args.packet / 'receipts/pr-body.json').read_text())
assert pr['head']['sha'] == HEAD
bullet = next(s for s in pr['body'].splitlines() if s.startswith('- `sw/firmware/ctrl/adp/adp.h`:'))
assert 'Milan v1.2 section 5.6.3 (Advertise state machine)' in bullet
assert 'IEEE 1722.1-2021 section 6.2 (ADPDU)' in bullet
assert 'no-callback port contract' in bullet
header = git('show', f'{HEAD}:sw/firmware/ctrl/adp/adp.h')
assert 'v1.2 5.6.3, the Advertise state machine, over IEEE 1722.1-2021 6.2' in header
old = json.loads((args.packet / 'receipts/comment-6024328677.json').read_text())
correction = json.loads((args.packet / 'receipts/comment-6024757146.json').read_text())
assert 'Exclusion table unchanged (15 rows)' in old['body']
assert old['created_at'] == old['updated_at']
assert '14 data rows, unchanged from the source base; five are ADP rows.' in correction['body']
assert '6024328677' in correction['body']
paths = git('diff', '--name-only', f'{BASE}..{HEAD}').splitlines()
assert len(paths) == 26 and all(p.startswith('sw/firmware/') for p in paths)
subprocess.run(['rtk', 'proxy', 'git', '-C', str(args.checkout), 'diff', '--check', BASE, HEAD], env=env, check=True)
print(json.dumps({
    'result': 'PASS', 'head': HEAD, 'tree': TREE, 'source_base': BASE,
    'F1': {'result': 'RESOLVED', 'public_bullet': bullet, 'authority': 'sw/firmware/ctrl/adp/adp.h:9; docs/design/MAILBOX_SPLIT.md:279'},
    'F2': {'result': 'RESOLVED', 'base_data_rows': len(before), 'head_data_rows': len(after),
           'adp_data_rows': len(adp), 'excluded_identities_and_items_unchanged': True,
           'original_comment_unedited': True, 'original_created_at': old['created_at'],
           'original_updated_at': old['updated_at'], 'correction_url': correction['html_url']},
    'changed_paths': paths, 'rows': after,
    'public_pr_body_sha256': hashlib.sha256(pr['body'].encode()).hexdigest(),
    'original_comment_body_sha256': hashlib.sha256(old['body'].encode()).hexdigest(),
    'correction_body_sha256': hashlib.sha256(correction['body'].encode()).hexdigest(),
    'whitespace_check': 'PASS'
}, indent=2))
