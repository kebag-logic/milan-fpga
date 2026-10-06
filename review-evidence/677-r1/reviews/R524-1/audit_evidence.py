#!/usr/bin/env python3
"""Compare public campaign receipts with exact source catalogues and exclusions."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path.cwd()
PACKET = Path(__file__).resolve().parent
BASE = '6714181d0c8a16e2983f85b724f4d688f5111835'
HEAD = '6c94e9f5f496ac25f8c4e31f9e3685c725de29f3'


def source(path, rev):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)


def catalogue(text):
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'MUTANTS'
                                               for t in node.targets):
            return {ast.literal_eval(item.args[0]): ast.dump(item) for item in node.value.elts}
    raise AssertionError('catalogue absent')


report = {'head': HEAD, 'base': BASE}
manifest = {r['file']: r for r in json.loads((PACKET / 'public/MANIFEST.json').read_text())}
verified = []
for row in json.loads((PACKET / 'public/retrieval.json').read_text()):
    if row['local'] == 'MANIFEST.json':
        continue
    digest = hashlib.sha256((PACKET / 'public' / row['local']).read_bytes()).hexdigest()
    assert digest == manifest[row['local']]['published_sha256']
    verified.append(row['local'])
report['published_manifest_verified'] = verified

for module in ('ctrl', 'ctrl_nvm'):
    filename = 'ctrl_mutants.py' if module == 'ctrl' else 'nvm_mutants.py'
    path = f'sw/firmware/{module}/test/{filename}'
    before, after = catalogue(source(path, BASE)), catalogue(source(path, HEAD))
    assert set(before) <= set(after)
    assert all(after[name] == value for name, value in before.items())
    report[module] = {'base_mutants': len(before), 'head_mutants': len(after),
                      'baseline_definitions_unchanged': True,
                      'added': sorted(set(after) - set(before))}
    if module == 'ctrl_nvm':
        receipts = json.loads((PACKET / 'public/author/nvm-campaign.json').read_text())
        assert receipts['head'] == HEAD and receipts['caught'] == len(after)
        records = receipts['records']
        assert Counter(x['name'] for x in records) == Counter(after.keys())
        assert all(x['finding'] == '' for x in records)
        text = '\n'.join(p.read_text() for p in sorted((PACKET / 'public/author/logs').glob('nvm-batch-*.log')))
        counts = Counter(re.findall(r'self-test OK: (\S+)', text))
        assert counts == Counter(after.keys()), counts
        report[module]['public_raw_kills_exactly_once'] = len(counts)
    else:
        text = (PACKET / 'public/author/logs/ctrl.log').read_text()
        counts = Counter(re.findall(r'\[ok\] mutant (\S+)', text))
        assert counts == Counter(after.keys())
        assert 'mutants: 79 of 79 caught' in text
        report[module]['public_raw_kills_exactly_once'] = len(counts)

path = 'sw/firmware/gtest/README.md'
def exclusions(text):
    return [line.split('|')[1:5] for line in text.splitlines()
            if line.startswith('| `sw/firmware/')]
before, after = exclusions(source(path, BASE)), exclusions(source(path, HEAD))
assert before == after
report['coverage_exclusions'] = {'rows': len(after), 'identity_and_excluded_items_unchanged': True,
                                  'adp_rows': sum('ctrl/adp/adp.c' in x[0] for x in after)}
changed = subprocess.check_output(['git', 'diff', '--name-only', BASE, HEAD], text=True).splitlines()
assert all(p.startswith('sw/firmware/') for p in changed)
report['changed_paths'] = changed
report['diff_changes_no_rtl_shipping_image_builds_workflows_or_gitlinks'] = True
(PACKET / 'evidence-audit.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
