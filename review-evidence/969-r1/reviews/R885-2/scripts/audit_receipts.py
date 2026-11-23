#!/usr/bin/env python3
"""Extract concise public gate results and check source provenance and probe identity.
Usage: python3 -I audit_receipts.py CHECKOUT PACKET
"""
import gzip
import hashlib
from pathlib import Path
import re
import subprocess
import sys

root, packet = (Path(p).resolve() for p in sys.argv[1:])
pub = packet/'scratch/published/author-r2/receipts'
lines = []
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
for rev in ('f02d44cd', 'ecd5bf41', '5dba2089'):
    paths = git('diff', '--name-only', rev, 'HEAD').decode().splitlines()
    lines += [f'{rev}..HEAD changed paths:'] + paths
lines += ['Firmware production C/H inputs since f02d44cd: ' +
          ('UNCHANGED' if not git('diff', 'f02d44cd', 'HEAD', '--', 'sw/firmware/**/*.c', 'sw/firmware/**/*.h') else 'CHANGED')]
for path in sorted((pub/'firmware').iterdir()):
    if 'FAILED' in path.name or not any(s in path.name for s in ('5dba2089', 'ecd5bf41', 'shard1', 'shard2')):
        continue
    text = gzip.decompress(path.read_bytes()).decode() if path.suffix == '.gz' else path.read_text()
    lines += [f'PUBLIC {path.relative_to(pub)}']
    lines += [ln for ln in text.splitlines() if re.search(r'RESULT:|caught.*escaped|of \d+ caught|arms PASS|firmware.*PASS|srp_mbx.c\s', ln)][-5:]
    if 'shard3' in path.name:
        early = [ln for ln in text.splitlines() if ln.startswith('[ok] feedback-early-')]
        lines += [f'Early plant results: {len(early)}']
        for shape in ('endstation_ax7101_1x1_tdm8, 1 interface]', 'endstation_ax7101_1x1_tdm8, 2 interfaces]',
                      'endstation_ax7101_8x8, 1 interface]'):
            lines.append(f'{shape}: {sum(shape in ln for ln in early)}')
text = (pub/'docs/docs-workflow-e816c74d.txt').read_text()
rows = [ln for ln in text.splitlines() if re.match(r'^\d+[-\w]*\s+rc=', ln)]
lines += [f'Docs commands {len(rows)}; rc=0 {sum("rc=0 " in ln for ln in rows)}']
lines += [ln for ln in rows if 'rc=0 ' not in ln]
for rel in ('ledger/fixture-stand-in-8x8-1if.txt', 'budget/hot-section-f02d44cd.txt',
            'budget/leaveall-build-with-the-kept.txt'):
    lines += [f'PUBLIC {rel}', (pub/rel).read_text()]

for role, old_path, local in (
    ('internal', 'reviews/R885-1/scripts/stale_count_probe.cpp', 'r885_1_stale_count_probe.inc'),
    ('external', 'reviews/R886-1/probes.cpp', 'r886_1_probes.inc')):
    old = git('show', f'1cd9d3fd:review-evidence/969-r1/{old_path}')
    now = (packet/'scripts'/local).read_bytes()
    # The public external source's single include is supplied by probes.cpp instead.
    adjusted = old.replace(b'#include "srp_mbx.cpp"\n', b'\n')
    same = now == old or now == adjusted
    lines.append(f'{role} prior probe source: exact (include supplied by wrapper if needed)={same}; '
                 f'published sha256={hashlib.sha256(old).hexdigest()}')

(packet/'receipts/public-receipt-audit.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(ln for ln in lines if not ln.startswith(('docs/', 'sw/', 'tb/')) and '\n' not in ln))
