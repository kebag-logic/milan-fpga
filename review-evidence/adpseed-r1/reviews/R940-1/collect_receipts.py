#!/usr/bin/env python3
"""Collect text evidence, normalize machine-local paths, and seal a manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
p.add_argument('--dependency-prefix', type=Path, required=True)
p.add_argument('--compiler-bin', type=Path, required=True)
a = p.parse_args()
root = a.source.resolve()
packet = Path(__file__).resolve().parent
work = packet / 'scratch'
receipts = packet / 'receipts'
for src, dst in [(work / 'plants/results.json', receipts / 'plant-results.json'),
                 (work / 'plants/message-markers.json', receipts / 'plant-message-markers.json'),
                 (work / 'rv32/results.json', receipts / 'rv32-results.json')]:
    shutil.copyfile(src, dst)
for directory in sorted((work / 'plants').iterdir()):
    if not directory.is_dir() or directory.name == 'baseline':
        continue
    target = receipts / 'plants' / directory.name
    target.mkdir(parents=True, exist_ok=True)
    for src in list(directory.glob('*.xml')) + list(directory.glob('*.log')):
        shutil.copyfile(src, target / src.name)
for kind in ('debug', 'release'):
    shutil.copyfile(work / 'rv32' / kind / 'smoke.log', receipts / ('rv32-' + kind + '-smoke.log'))

def git(*args):
    return subprocess.check_output(['git', *args], cwd=root).decode().strip()
base = 'a795471c0abc4e38f7e5146b4e539dd607b6f501'
dev = '9e1cd60facf4f5da9f211420723e4f9d3adb0652'
common = git('merge-base', dev, 'HEAD')
dev_tree = git('rev-parse', dev + '^{tree}')
common_tree = git('rev-parse', common + '^{tree}')
assert dev_tree == common_tree
registered = json.loads((root / 'tests/mutations.json').read_text())
prior = json.loads(git('show', base + ':tests/mutations.json'))
old_names = {x['name'] for x in prior}
new = sorted(x['name'] for x in registered if x['name'] not in old_names)
author = (receipts / 'author-tsn-c-stack-mutation.log').read_text()
caught = [line.split(' ', 1)[1] for line in author.splitlines() if line.startswith('CAUGHT ')]
assert len(caught) == len(set(caught)) == len(registered) == 510
assert set(caught) == {x['name'] for x in registered}
assert len(new) == 21
local = (receipts / 'plants.log').read_text()
assert all('CAUGHT ' + name + '\n' in local for name in new)
(receipts / 'evidence-audit.json').write_text(json.dumps({
    'head': git('rev-parse', 'HEAD'), 'base': base,
    'changed_paths': git('diff', '--name-only', base, 'HEAD').splitlines(),
    'dev_linux': dev, 'common_ancestor': common, 'identical_tree': dev_tree,
    'author_unique_caught_exactly_matches_registered': len(caught),
    'new_plants_all_locally_caught': new,
    'standards_read': {
        'IEEE 1722.1-2021 6.2.4.2.2': '04130737d1283a55b001ca9375d9cdc96cb79ebe78ea17c5e2c34f0e36f018d7',
        'Milan v1.2 5.6.3.5.2 and 5.6.3.5.3': '6bb902be1c1de8c44f4c4c583a645b0b37e0b2dac27870486ce229e68ce3bba8'
    }}, indent=2) + '\n')

raw = work / 'raw-receipts'
shutil.copytree(receipts, raw, dirs_exist_ok=True)
substitutions = [(str(packet), '<PACKET>'), (str(root), '<SOURCE>'),
                 (str(a.dependency_prefix), '<DEPENDENCIES>'), (str(a.compiler_bin), '<COMPILER_BIN>')]
for f in receipts.rglob('*'):
    if f.is_file():
        text = f.read_text()
        for before, after in substitutions:
            text = text.replace(before, after)
        f.write_text(text)
files = sorted(f for f in packet.rglob('*') if f.is_file() and 'scratch' not in f.relative_to(packet).parts
               and f.name not in ('MANIFEST.sha256', 'REPORT.md'))
(packet / 'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest() + '  ' + f.relative_to(packet).as_posix() + '\n' for f in files))
print(json.dumps({'published_receipts_and_scripts': len(files), 'new_plants_verified': len(new),
                  'author_campaign_verified': len(caught), 'manifest': 'MANIFEST.sha256'}))
