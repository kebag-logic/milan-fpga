#!/usr/bin/env python3
"""Check receipt completeness and write the publishable packet manifest."""
import hashlib, json, pathlib
packet=pathlib.Path(__file__).resolve().parents[1]
receipts=packet/'receipts'
labels=('shape-441-serial','shape-43-serial','make-probes-441','make-probes-43',
        'guard-selftest','ooc-selftest','cache-selftest','list-hermetic',
        'fixture-selftest','fixture-receipts','docs-changed','diff-check','sweep-replay','shipping-flows','exact-tree')
report=(packet/'REPORT.md').read_text()
positive=report.startswith('[R567] POSITIVE')
for label in labels:
    result=json.loads((receipts/(label+'.json')).read_text())
    assert result['rc']==0,label
refused=json.loads((receipts/'refusal-results.json').read_text())
assert json.loads((receipts/'docs-example-52.json').read_text())['rc']!=0
assert json.loads((receipts/'docs-example-64.json').read_text())['rc']==0
assert len(refused)==6 and all(row['rc']!=0 for row in refused)
shipping=json.loads((receipts/'shipping-flows-results.json').read_text())
assert len(shipping)==10
assert {(row['shape'],row['flow']) for row in shipping} == {(name,flow) for name in ('arty_current','arty_4x4','arty_8ch','ax7101_8x8','ax7101_1x1_tdm8') for flow in ('run.sh','ooc.sh')}
assert all(row['rc']==0 for row in shipping)
assert report.splitlines()[0] in [f'[R567] {verdict} - exact head 759d1d248fad095ab07bfcc480a0828117501f39' for verdict in ('POSITIVE','NEGATIVE')]
assert report.endswith('R567-1 FINISHED\n') and 'SKELETON' not in report
files=[packet/'REPORT.md']
for directory in ('scripts','receipts','public/review-evidence/641-r1'):
    files.extend(p for p in (packet/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
lines=[]
for file in sorted(set(files)):
    lines.append(hashlib.sha256(file.read_bytes()).hexdigest()+'  '+str(file.relative_to(packet)))
(packet/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print(f'{len(files)} publishable files; mandatory focused receipts accounted for')
