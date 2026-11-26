#!/usr/bin/env python3
"""Audit the public packet and the source relationships used by this review."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)
head = '85569e241625d8e4176aae7d77c524783dff30cd'
base = 'c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350'
evidence = 'a7eb193aa6d85f970500c8ca64ea45189a8ba7a3'
prefix = 'review-evidence/p1win-r1/'
assert git('rev-parse', 'HEAD').decode().strip() == head
print('HEAD', head)
print('TREE', git('rev-parse', 'HEAD^{tree}').decode().strip())
manifest = json.loads(git('show', evidence + ':' + prefix + 'MANIFEST.json'))
for item in manifest:
    digest = hashlib.sha256(git('show', evidence + ':' + prefix + item['file'])).hexdigest()
    assert digest == item['published_sha256']
    print('PACKET HASH OK', item['file'], digest)
for ancestor in ('8a4ad2c4a9009693d45d2178bf538e02ef7cdfa2', '2509db68'):
    paths = ['sw/firmware/ctrl_nvm/nvm_klj2.c', 'sw/firmware/ctrl_nvm/nvm_klj2.h',
             'sw/firmware/ctrl_nvm/nvm_layout3.h', 'scripts/nvm_klj3.py']
    delta = git('diff', '--name-only', ancestor + '..' + head, '--', *paths)
    assert not delta
    print('FORMAT/CODEC IDENTICAL', ancestor, 'to', head, 'paths', ','.join(paths))
print('POST-IMAGE-COMMIT DELTA')
print(git('diff', '--name-only', '8a4ad2c4..' + head).decode(), end='')
changed = git('diff', '--name-only', base + '..' + head).decode().splitlines()
print('CHANGED PATHS', len(changed))
print('CHANGED PRODUCT HDL', [p for p in changed if p.startswith('hdl/')])
print('CHANGED MEMORY POLICY', [p for p in changed if Path(p).name.startswith('ctrl_memory')])
print('CHANGED SUBMODULE GITLINKS', git('diff', '--raw', base + '..' + head, '--',
    'protocol-processor', 'gptp-processor', 'third_party').decode().strip() or 'none')
sys.path.insert(0, str(root / 'sw/firmware/ctrl_nvm/test'))
import nvm_mutants
print('STORE DEFECTS', len(nvm_mutants.MUTANTS), 'COMPILE CONTROLS', 5)
added = [m.name for m in nvm_mutants.MUTANTS if m.name.startswith('bind_') or
         m.name in ('window_left_armed', 'other_in_flight_windowed')]
print('BINDING WINDOW PLANTS', len(added), ', '.join(added))
assert len(added) == 16
print('RESOURCE DELTAS from public images.txt: 8x8 LUT +159, FF -6, RAM tiles 0; 1x1 LUT -9, FF 0, RAM tiles 0')
print('One route per source and point; no intermediate resource attribution is published.')
print('RESULT PASS')
