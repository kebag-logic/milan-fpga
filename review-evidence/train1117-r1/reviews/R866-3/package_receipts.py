#!/usr/bin/env python3
"""Keep selected original public receipts and hash the publishable packet."""
import hashlib
from pathlib import Path
import shutil
import sys

out = Path(sys.argv[1]).resolve()
source = out / 'scratch/review-evidence/train1117-r1/author-r5/receipts'
selected = [
    'step12c/images/images-14.txt', 'step12c/images/release-export-14.txt',
    'step12c/images/hashes.txt', 'step11/images/hashes-b1f1161b.txt',
    'step12c/ledger/plat-ledger.log', 'step12c/logs/r5-q14.log',
    'step12c/logs/r5-g14-fw0.log', 'step12c/logs/r5-g14-fw1.log.stub.txt',
    'step12b/logs/r5-g13-fw2.log.stub.txt', 'step12b/logs/r5-g13-fw3.log.stub.txt',
    'step12b/logs/r5-g13-boot.log', 'step12b/logs/r5-g13-rxmon.log',
    'step12b/images/gateware13.txt', 'step12/images/split-gateware-12.txt',
    'step12/fit/fit-1x1.log', 'step12/fit/fit-8x8.log',
]
for point in ('1x1', '8x8'):
    selected += ['step12b/gating/'+point+'/'+name for name in
                 ('signoff.txt', 'identity.log', 'artifacts.sha256', 'image_manifest.json')]
for name in selected:
    target = out / 'published' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / name, target)
report = (out / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R866] POSITIVE - exact head 0839453f6d7135063e904bcaf4ac1852ad6b522a'
assert report.splitlines()[-1] == 'R866-3 FINISHED'
assert 'SKELETON' not in report
for lens in ('Conformance', 'RTL', 'Robustness', 'Tests', 'Docs'):
    assert '| '+lens+' | CLEAN |' in report
paths = sorted(p for p in out.rglob('*') if p.is_file() and 'scratch' not in p.relative_to(out).parts
               and p.name != 'MANIFEST.sha256')
manifest = ''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(out))+'\n' for p in paths)
(out / 'MANIFEST.sha256').write_text(manifest)
print('Publishable files:', len(paths))
print('Report validated; scratch excluded; manifest written')
