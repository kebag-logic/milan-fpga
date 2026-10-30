#!/usr/bin/env python3
"""Usage: python3 verify-delta.py SOURCE PACKET. Read-only source checks."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root, packet = (Path(x).resolve() for x in sys.argv[1:])
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.dont_write_bytecode = True
head = '0ea635ea22eeb6d97335c4e814eede1ac0d67ebc'
tree = '1833cde6be59abcfb24e1ba5b461c8fa8159fc2b'

def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])

assert git('rev-parse', 'HEAD').decode().strip() == head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == tree
assert git('write-tree').decode().strip() == tree
subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', '18a4dc1', head], check=True)
blobs, links = 0, []
for entry in git('ls-tree', '-rz', head).split(b'\0'):
    if not entry:
        continue
    meta, path = entry.split(b'\t', 1)
    mode, kind, oid = meta.decode().split()
    file = root / path.decode()
    if kind == 'commit':
        links.append((path.decode(), oid))
        continue
    data = os.readlink(file).encode() if mode == '120000' else file.read_bytes()
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert digest == oid, path
    if mode in ('100644', '100755'):
        assert bool(file.stat().st_mode & 0o111) == (mode == '100755'), path
    blobs += 1
status = git('status', '--porcelain=v1').decode()
assert not status, status
rows = [f'HEAD {head}', f'TREE and index {tree}', f'Checked {blobs} tracked blobs and modes; all exact.',
        f'Submodule gitlinks: {links}', 'Round-1 head is an ancestor; worktree and index clean.']
for base in ('a9e84b66', '18a4dc1'):
    paths = git('diff', '--name-only', base, head).decode().splitlines()
    nonmd = [p for p in paths if not p.endswith('.md')]
    assert set(nonmd) <= {'Makefile', 'scripts/check-doc-inventory.py', 'scripts/check-links.py'}
    rows.append(f'{base}..HEAD: {len(paths)} paths; non-Markdown: {nonmd}; RTL, test sources, generators, generated artifacts and workflows byte/mode unchanged.')
(packet / 'final-integrity.log').write_text('\n'.join(rows) + '\n')
print('\n'.join(rows))

# Compare every README-derived input of the unchanged NVM figures gate.
sys.path.insert(0, str(root / 'tb/nvm_port'))
spec = importlib.util.spec_from_file_location('nvm_figures', root / 'tb/nvm_port/measure_figures.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
snapshots = []
for rev in ('a9e84b66', '18a4dc1', head):
    readme = packet / 'scratch' / ('nvm-' + rev + '.txt')
    readme.write_bytes(git('show', rev + ':tb/nvm_port/README.md'))
    module.README = readme
    flat = module.flat_readme()
    snap = {'arm_rows': module.readme_arm_rows(), 'matrix': module.readme_matrix(),
            'coverage': module.claim_coverage(flat), 'sizes': module.readme_figures(393, flat),
            'figures': module.FIGURE_RE.findall(flat),
            'claims': [(name, [re.findall(pattern, flat) for pattern in patterns])
                       for name, patterns, _ in module._all_claims()],
            'waivers': [re.findall(pattern, flat) for pattern, _ in module.WAIVERS]}
    snapshots.append(snap)
assert snapshots[0] == snapshots[1] == snapshots[2]
assert not snapshots[-1]['coverage'] and not snapshots[-1]['sizes']
receipt = {'equal_base_round1_head': True, 'executed_figures_campaign': False, 'derived_inputs': snapshots[-1]}
(packet / 'nvm-derived-inputs.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('NVM figure gate: all README-derived inputs equal across base, round 1, and exact head; no campaign execution asserted.')
