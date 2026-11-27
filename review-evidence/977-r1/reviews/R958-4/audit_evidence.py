#!/usr/bin/env python3
"""Verify published author evidence directly from Git objects; never open review reports."""
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
revision = '6208d96398000bce22a2fedc14788fee68b9f4ae'
prefix = 'review-evidence/977-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
def blob(path):
    return git('show', revision + ':' + prefix + path)

manifest = json.loads(blob('MANIFEST.json'))
entries = [e for e in manifest if e['file'].split('/')[0] in
           ('author', 'author-text', 'author-r10', 'author-r11', 'author-r12')]
out = {'evidence_commit': revision, 'manifest_checks': [], 'elf_maps': {}, 'delivery_arithmetic': {}}
for entry in entries:
    digest = hashlib.sha256(blob(entry['file'])).hexdigest()
    assert digest == entry['published_sha256'], entry['file']
    out['manifest_checks'].append({'file': entry['file'], 'sha256': digest})
identity_paths = ['author-r12/receipts/elf-identity-3256d1d2.txt',
                  'author-r11/receipts/r11b/elf-identity-3181a3ec.txt',
                  'author-r10/receipts/r10d/elf-identity-final.txt']
reference = None
for path in identity_paths:
    sections = []
    current = {}
    for line in blob(path).decode().splitlines():
        match = re.fullmatch(r'([a-f0-9]{64})  (.+\.elf)', line)
        if match:
            name = match[2]
            if name in current:
                sections.append(current)
                current = {}
            current[name] = match[1]
    if current:
        sections.append(current)
    assert len(sections) == 2 and all(len(x) == 80 for x in sections), (path, [len(x) for x in sections])
    assert sections[0] == sections[1], path
    if reference is None:
        reference = sections[0]
    assert reference == sections[0], path
    out['elf_maps'][path] = {'maps': 2, 'entries_per_map': 80, 'all_equal': True,
                             'distinct_hashes': len(set(sections[0].values()))}
out['elf_hashes'] = reference
for shape, sinks in [('1x1', 2), ('8x8-1if', 9)]:
    text = blob(f'author-r12/receipts/meas/deliv-{shape}-e59cf6ea.txt').decode()
    best = {}
    count = 0
    unique = set()
    for line in text.splitlines():
        if 'record at bus ' not in line:
            continue
        count += 1
        win = re.search(r'window (\d+) passes, (\d+) ordinary passes', line)
        assert int(win[1]) == 2 * sinks + 1 and int(win[2]) > 0
        unique.add((line.split()[0], re.search(r'record at bus (\d+)', line)[1]))
        for match in re.finditer(r'(after|before 50 ms|before 500 ms) ([\d,]+): excess ([\d,]+), ([\d,]+) a sink', line):
            label, baseline, excess, share = match.groups()
            excess = int(excess.replace(',', ''))
            stated = int(share.replace(',', ''))
            assert abs(stated - excess / sinks) <= 0.5
            if excess / sinks > best.get(label, {}).get('cycles_per_sink', -1):
                best[label] = {'cycles_per_sink': excess / sinks,
                               'us_by_rule': 5 * math.ceil(excess / sinks / 100 * 1.05 / 5),
                               'line': line}
    assert count == 40 and set(best) == {'after', 'before 50 ms', 'before 500 ms'}
    out['delivery_arithmetic'][shape] = {'rows': count, 'unique_group_record_pairs': len(unique), 'maxima': best}
raw_commit = git('cat-file', 'commit', revision)
out['commit_has_signature_header'] = b'\ngpgsig ' in raw_commit.split(b'\n\n', 1)[0]
out['signature_limit'] = 'Hash integrity checked; no cryptographic signature established.'
out['total_author_files_verified'] = len(entries)
print(json.dumps(out, indent=2))
