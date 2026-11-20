#!/usr/bin/env python3
"""verify_published.py GATING_DIR: the published gating receipts checked against one another, from the receipts alone
(R866-4-F1); no scratch, no build tree. GATING_DIR is receipts/step16/gating. At each point (1x1, 8x8):

  listed     every file of <point>/build/ has the sha256 that <point>/artifacts.sha256 lists for it
  firmware   <point>/build/image_manifest.json binds the ELF that artifacts.sha256 lists (sha256), and that ELF is the
             gating ELF loaded-identity/<point>.txt compared, with the same byte count
  bitstream  the bitstream sha256 artifacts.sha256 lists is the one bench-images-8c5e2b4f.txt gives, and the one
             loaded-identity/<point>.txt recomputed the manifest's payload binding from, which equals the manifest's
  product    the product ELF loaded-identity/<point>.txt compared is the one ../images/product-images.txt gives for the
             head's ledger link at that point (1x1-if1, 8x8-if1), by full sha256
  identity   identity.log is the identity gate's pass line, and loaded-identity/<point>.txt reports RESULT ... PASS

Exit 0 when every check holds at both points, 1 otherwise."""
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
bench = (root / 'bench-images-8c5e2b4f.txt').read_text()
failed = 0
products = {l.split()[0]: l.split()[4] for l in (root.parent / 'images/product-images.txt').read_text().splitlines()
            if l[:1].isdigit() and len(l.split()) > 4 and l.split()[3] == '8c5e2b4f'}
for point, name, led in (('1x1', '1x1/1if', '1x1-if1'), ('8x8', '8x8/1if', '8x8-if1')):
    d = root / point
    listed = {Path(n.strip()).name: h for h, n in (l.split(None, 1) for l in (d / 'artifacts.sha256').read_text()
                                                    .splitlines())}
    report = (root / f'loaded-identity/{point}.txt').read_text()
    checks = []
    for f in sorted((d / 'build').iterdir()):
        have = hashlib.sha256(f.read_bytes()).hexdigest()
        checks.append((f'listed {f.name}', listed.get(f.name) == have, f'{have} / listed {listed.get(f.name)}'))
    man = json.loads((d / 'build/image_manifest.json').read_text())
    gating = re.search(r'^gating  ELF ([0-9a-f]{64}) (\d+) bytes$', report, re.M)
    checks.append(('firmware', bool(gating) and man['ctrl_firmware']['sha256'] == listed['ctrl_app.elf'] ==
                   gating.group(1) and man['ctrl_firmware']['bytes'] == int(gating.group(2)),
                   f'manifest {man["ctrl_firmware"]["sha256"]} ({man["ctrl_firmware"]["bytes"]} B), listed '
                   f'{listed["ctrl_app.elf"]}, compared {gating.group(1) if gating else None}'))
    bit = listed['alinx_ax7101.bit']
    section = bench.split(f'## {name}', 1)[1].split('## ', 1)[0]
    rebound = re.search(r'recomputed from the \.bit \(sha256 ([0-9a-f]{64})\): (\{.*?\}): equal', report)
    checks.append(('bitstream', f'sha256:    {bit}' in section and bool(rebound) and rebound.group(1) == bit and
                   ast.literal_eval(rebound.group(2)) == man['bitstream'],
                   f'listed {bit}; bench-images {"names it" if f"sha256:    {bit}" in section else "does NOT"}; '
                   f'payload binding {man["bitstream"]}'))
    product = re.search(r'^product ELF ([0-9a-f]{64}) ', report, re.M)
    checks.append(('product', bool(product) and products.get(led) == product.group(1),
                   f'compared {product.group(1) if product else None}, product-images {led} {products.get(led)}'))
    checks.append(('identity', (d / 'identity.log').read_text().startswith('image identity: a split image whose')
                   and re.search(rf'^RESULT {re.escape(name)}: PASS', report, re.M) is not None,
                   'identity.log and the loaded-identity RESULT line'))
    for check, ok, why in checks:
        print(f'{name} {check}: {"PASS" if ok else "FAIL"} ({why})')
        failed += not ok
print(f'verify_published: {"PASS" if not failed else f"FAIL ({failed})"}')
sys.exit(1 if failed else 0)
