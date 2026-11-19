#!/usr/bin/env python3
"""List publication inputs without publishing disposable trees."""
import hashlib
from pathlib import Path
import shutil

packet = Path(__file__).resolve().parent
source = packet / 'scratch/review-evidence/943-r1/author-r1/receipts'
published = packet / 'cited-author-receipts'
published.mkdir(exist_ok=True)
for relative in ('budget/declaring-face.patch.txt', 'budget/declaring-face-measurement.txt',
                 'budget/record-classes-1x1-211c1ede.txt', 'budget/record-classes-8x8-1if-211c1ede.txt',
                 'budget/flip-grade-1x1-1if-paced-325-trial.txt', 'ledger/points-base-vs-head.txt',
                 'release/release-image-base-vs-head.txt', 'gates/boundary-without-verilator-head-and-base.txt',
                 'twin/twin-and-plants-211c1ede.txt'):
    shutil.copyfile(source / relative, published / Path(relative).name)
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R872] NEGATIVE - exact head 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff'
assert report.splitlines()[-1] == 'R872-1 FINISHED'
assert 'SKELETON' not in report
files = sorted(p for p in packet.rglob('*') if p.is_file()
               and 'scratch' not in p.relative_to(packet).parts
               and p.name != 'MANIFEST.sha256')
lines = [hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(packet).as_posix() for p in files]
(packet / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
print('Publication inputs:', len(files), '; scratch excluded; report first/last lines verified.')
