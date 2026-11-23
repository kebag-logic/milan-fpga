#!/usr/bin/env python3
"""Verify published hashes, unchanged test inputs, and measured ledgers."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
packet = out / 'scratch/review-evidence/gptpsw-r1'
manifest = json.loads((packet / 'MANIFEST.json').read_text())
entries = [x for x in manifest if x['file'].startswith('author-r4/')]
for row in entries:
    path = packet / row['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['published_sha256'], row['file']
print(f'Published author-r4 manifest: {len(entries)} hashes match')
commit = '98bc6f22bc3c42bd78c1585b6e3bdca2018d25f1'
raw = subprocess.check_output(['git', 'cat-file', 'commit', commit], cwd=root)
print('Evidence commit signature present:', b'\ngpgsig ' in raw)
for ancestor, paths in [
    ('631dc544', ['sw/firmware','tb','hdl']),
    ('a6323318', ['hdl']),
    ('e81cecdb', ['tb','hdl']),
]:
    changed = subprocess.check_output(['git','diff','--name-only',ancestor,'HEAD','--',*paths],cwd=root,text=True)
    print(f'Input changes since {ancestor}: {changed.strip() or "none"}')
r = packet / 'author-r4/receipts'
for kind in ('gptp','plain'):
    result = subprocess.run([sys.executable,'-B',str(root/'tb/verilator/ctrl_service_budget/egress_ledger.py'),
        '--point','8x8-1if',str(r/f'harness-631dc544/{kind}-8x8-1if')],
        cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (out/f'egress-{kind}.log').write_text(result.stdout)
    print(f'{kind} held ledger rc={result.returncode}')
    assert result.returncode == 0
expected = [line.strip() for line in (root/'sw/firmware/ctrl/plat/ctrl_split_hot.txt').read_text().splitlines()
            if line.strip() and not line.startswith('#')]
kept = [line.strip() for line in (r/'hotlist/gptp/kept.txt').read_text().splitlines() if line.strip()]
assert expected == kept, 'hot list differs from published filtered order'
print(f'Hot list equals published filtered order: {len(expected)} entries')
print('gPTP entries:',sum(line.split()[0] in ('gptp','gptp_mbx') for line in expected))
print('Memory table vs ledger:')
for line in (root/'docs/design/SPLIT_CONTROL_MEMORY.md').read_text().splitlines():
    if line.startswith('| `8x8-') and 'image_gptp' in line:
        print(line)
for line in (root/'sw/litex/ctrl_memory.py').read_text().splitlines():
    if '"image_gptp"' in line:
        print(line.strip())
