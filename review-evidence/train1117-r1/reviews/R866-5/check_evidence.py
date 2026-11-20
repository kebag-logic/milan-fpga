#!/usr/bin/env python3
"""Check a published evidence extraction and exercise its portable verifier.

Usage: python3 check_evidence.py ARCHIVE_ROOT OUTPUT
ARCHIVE_ROOT contains MANIFEST.json and author-r6/ and author-r7/.
All altered copies stay under OUTPUT/scratch/.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

archive, output = map(Path, sys.argv[1:])
author = archive / 'author-r7'
gating = author / 'receipts/step16/gating'
verifier = gating / 'loaded-identity/tools/verify_published.py'
output.mkdir(parents=True, exist_ok=True)
rows = json.loads((archive / 'MANIFEST.json').read_text())
checked = 0
for row in rows:
    if row['file'].split('/')[0] not in ('author-r6', 'author-r7'):
        continue
    path = archive / row['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['published_sha256'], row['file']
    checked += 1
print(f'Published archive SHA256 entries verified: {checked}')

old = archive / 'author-r6'
old_files = {str(p.relative_to(old)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in old.rglob('*') if p.is_file()}
new_files = {str(p.relative_to(author)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in author.rglob('*') if p.is_file()}
changed = sorted(p for p in old_files.keys() | new_files.keys() if old_files.get(p) != new_files.get(p))
allowed_files = {'HANDOFF-r5.md', 'PR-BODY.md', 'INDEX.md',
                 'receipts/step16/gating/bench-images-8c5e2b4f.txt'}
allowed_prefixes = ('receipts/step16/gating/loaded-identity/',
                    'receipts/step16/gating/1x1/build/', 'receipts/step16/gating/8x8/build/')
assert all(p in allowed_files or p.startswith(allowed_prefixes) for p in changed)
print(f'Evidence delta: {len(changed)} files; no changes outside the authorized set')
(output / 'evidence-delta.txt').write_text('\n'.join(changed) + '\n')

def run(label, root, expected, diagnostic):
    result = subprocess.run([sys.executable, '-B', str(verifier), str(root)],
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output / f'{label}.log').write_text(result.stdout)
    (output / f'{label}.rc').write_text(str(result.returncode) + '\n')
    assert result.returncode == expected, (label, result.returncode)
    assert diagnostic in result.stdout, label
    print(f'{label}: rc {result.returncode}; expected diagnostic found')

run('verify-published', gating, 0, 'verify_published: PASS')
scratch = output / 'scratch/receipt-plants'
if scratch.exists():
    shutil.rmtree(scratch)
scratch.mkdir(parents=True)
shutil.copytree(author / 'receipts/step16/images', scratch / 'images')

def plant(label, change, diagnostic):
    target = scratch / 'gating'
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(gating, target)
    change(target)
    run(label, target, 1, diagnostic)

def firmware(root):
    f = root / '8x8/build/image_manifest.json'
    obj = json.loads(f.read_text())
    obj['ctrl_firmware']['sha256'] = '0' * 64
    f.write_text(json.dumps(obj))

def bitstream(root):
    f = root / '1x1/artifacts.sha256'
    f.write_text('\n'.join('0' * 64 + s[64:] if s.endswith('alinx_ax7101.bit') else s
                           for s in f.read_text().splitlines()) + '\n')

def product(root):
    f = root / 'loaded-identity/1x1.txt'
    text = f.read_text()
    start = text.index('product ELF ') + len('product ELF ')
    f.write_text(text[:start] + '0' * 64 + text[start + 64:])

def payload(root):
    f = root / '8x8/build/image_manifest.json'
    obj = json.loads(f.read_text())
    obj['bitstream']['bitstream_payload_sha256'] = '0' * 64
    f.write_text(json.dumps(obj))

plant('plant-firmware', firmware, '8x8/1if firmware: FAIL')
plant('plant-bitstream', bitstream, '1x1/1if bitstream: FAIL')
plant('plant-product', product, '1x1/1if product: FAIL')
plant('plant-payload', payload, '8x8/1if bitstream: FAIL')

for point in ('1x1', '8x8'):
    receipt = (gating / f'loaded-identity/{point}.txt').read_text()
    for check in ('elf-header', 'segments', 'loaded', 'not-loaded', 'symtab', 'rom-words', 'manifest',
                  'identity-gate', 'objects'):
        assert f'CHECK {check}: PASS' in receipt
    loaded = receipt.split('CHECK loaded: PASS', 1)[1].split('CHECK not-loaded:', 1)[0]
    sections = [s for s in loaded.splitlines() if s.strip().startswith('| .')]
    assert len(sections) == 5
    for line in sections:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        assert cells[-1] == 'yes' and cells[-2] == cells[-3]
    assert "by section: {'.symtab': 2474}" in receipt
    print(f'{point}: all 5 allocated-section rows and all 9 receipt checks agree; difference confined to .symtab')

for name, failures in (('loaded-byte-flipped', ('segments', 'loaded', 'not-loaded', 'rom-words')),
                       ('bitstream-digest-altered', ('manifest',))):
    receipt = (gating / f'loaded-identity/plants/{name}.txt').read_text()
    for check in failures:
        assert f'CHECK {check}: FAIL' in receipt
    assert ': FAIL:' in receipt
    print(f'Published byte-level plant {name}: named failures verified (receipt inspection)')
print('PASS')
