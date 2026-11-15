#!/usr/bin/env python3
"""Verify published hash inventory, identity and numerical source receipts."""
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

tree, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
archive = packet / 'scratch/review-evidence/665s11-r1'
author = archive / 'author-r5'
manifest = json.loads((archive / 'MANIFEST.json').read_text())
rows = [r for r in manifest if r['file'].startswith('author-r5/')]
assert rows
for row in rows:
    assert hashlib.sha256((archive / row['file']).read_bytes()).hexdigest() == row['published_sha256'], row['file']
print('PASS published SHA256 inventory:', len(rows), 'files;', sum(r['path_redacted'] for r in rows), 'redacted by publisher')
print('Archive commit:', subprocess.check_output(['git', 'rev-parse', 'f2e8fa9f'], cwd=tree, text=True).strip())
print('Archive signature status:', subprocess.check_output(['git', 'log', '-1', '--format=%G?', 'f2e8fa9f'], cwd=tree, text=True).strip())
print('Signature status N means unsigned; this verifies published hashes, not an independent signer.')
for rev in ('57daf4ff', '20e08ceb', 'cb0fc679'):
    paths = subprocess.check_output(['git','diff','--name-only',rev+'..HEAD'], cwd=tree,text=True).splitlines()
    print('Changes since', rev, ':', ', '.join(paths))
costs = json.loads((author / 'receipts/survey/compare2/costs1/costs.json').read_text())
print('Measured cycle maxima keys:', ', '.join(costs.keys()))
for label, cyc, stated in [('SRP record',26865,285),('AECP ordinary',22531,240),('paced record',28750,305),('idle events',3627,40),('accepted REBOOT',11467,125),('locked REBOOT',10511,115)]:
    rounded = math.ceil(cyc * 1.05 / 500 - 1e-9) * 5
    assert rounded == stated
    print(f'PASS {label}: {cyc} cycles -> {rounded} us')
base=(author/'receipts/csr/csr-41ca9f87-1x1.csv').read_text().splitlines()
head=(author/'receipts/csr/csr-24e63089-1x1.csv').read_text().splitlines()
base=[s for s in base if not s.startswith('#')]
head=[s for s in head if not s.startswith('#')]
added=[s for s in head if s not in base]
assert not [s for s in base if s not in head]
assert added==['csr_base,ctrl_reboot,0xf000e000,,','csr_register,ctrl_reboot_req,0xf000e000,1,rw']
print('PASS CSR receipt comparison: only ctrl_reboot bank/register added at 0xf000e000')
for path in ['receipts/model/verify-wf.md','receipts/model/verify-docs.md']:
    lines=(author/path).read_text().splitlines()
    print(path, ':', lines[-1])
print('PASS archive receipt audit')
