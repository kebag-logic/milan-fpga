#!/usr/bin/env python3
"""collect8.py OUT: the SRP cut's receipts (#665's ruling of 2026-11-20) into OUT/receipts, each file at most 200 KB,
a larger one a <name>.stub.txt with its size, sha256 and last 60 lines (collect5.py's rule): the cut's profile and its
measurements on the way (srpcut/), and the head's gates, images and full CPU re-measure (step15/). Run sanitize.py and
index.py on OUT afterwards."""
import hashlib
import shutil
import sys
from pathlib import Path

S = Path('<scratch>')
out = Path(sys.argv[1]) / 'receipts'
LIMIT = 200 * 1024
REV = '92de01f756299c7d83bd6945dbf62d4b311a683e'
M, MO = S / 'r6meas' / REV, S / 'r6meas/out' / REV
C = S / 'r8cut'
ARMS = ('none', 'answering-ports', 'answering-every-port', 'valid-destinations', 'answering-later', 'shutdown-entry',
        'talker-notices', 'declaring-outputs')
SOURCES = [
    # the profile: committed-PC traces split by function, of c1e95dc1's image and of the cut's
    ('srpcut/profile', C, '*-record-*.txt'), ('srpcut/profile', C, '*-reclaim-*.txt'), ('srpcut/profile', C, '*-records-*.txt'),
    ('srpcut/profile', C, 'reclaim-pcs.txt'), ('srpcut/profile', C, 'tr*.log'),
    # srp-talker-held alone on each version's image, as the full re-measure reads it
    *[(f'srpcut/measure/{m}', C / m, p) for m in ('m1', 'm2', 'm4', 'm5') for p in ('survey.out', 'run.log')],
    *[(f'srpcut/measure/{m}', C / f'{m}/survey/ordinary-costs', 'costs.txt') for m in ('m1', 'm2', 'm4', 'm5')],
    ('srpcut/measure', C, 'm[1-5].log'),
    # the tests, the plants, the old adapter's failures, the SRP arms, the coverage and the ledger on the way
    ('srpcut/tests', C, 'lis8.log'), ('srpcut/tests', C, 'lis-old.log'), ('srpcut/tests', C, 'srpdev4.log'),
    ('srpcut/tests', C, 'plants8.log'), ('srpcut/tests', C, 'led1.log'), ('srpcut/tests', C, 'led2.log'),
    ('srpcut/tests', C, 'cov.log'), ('srpcut/tests', C, 'project-1x1*.txt'),
    ('srpcut/tools', C, '*.py'), ('srpcut/tools', C, '*.sh'), ('srpcut/tools', S / 'checks', 'r8-*.tsv'),
    # the head's gates: at 92de01f7, shard 3 again on its plant fix, and at fb083864
    ('step15/gates', S / 'r8gates', '*.log'), ('step15/gates', S / 'r8gates', '*.rc'),
    ('step15/gates/led-92de01f7', S / 'r8gates/led', '*.log'), ('step15/gates/led-92de01f7/fx', S / 'r8gates/led/fx', '*.log'),
    ('step15/gates', S / 'r8gates', 'boot-*.log'),
    ('step15/gates-fb083864', S / 'r8gates2', '*.log'), ('step15/gates-fb083864', S / 'r8gates2', '*.rc'),
    ('step15/gates-fb083864/led', S / 'r8gates2/led', '*.log'),
    # the images
    ('step15/images', S / 'r8fit', '*.txt'), ('step15/images', S / 'r8fit', '*.log'), ('step15/images', S / 'tools', 'gateware17.py'),
    ('step15/images/tools', S / 'r8fit/tools', '*'),
    ('step15/images', S / 'r8gates2', 'img-vs-measured.txt'), ('step15/images', S / 'r8gates2/img', 'hashes.txt'),
    # the full CPU budget re-measure at 92de01f7
    ('step15/measure', S / 'r6meas', f'analyse-*-{REV}.log'),
    *[(f'step15/measure/legs-{p}', M / p, g) for p in ('1x1', '8x8-1if') for g in ('*.build.log', '*[a-z].log',
                                                                                    '*.resume.log')],
    *[(f'step15/measure/legs-{p}/{a}', M / f'{p}/{a}', 'parts.json') for p in ('1x1', '8x8-1if') for a in ARMS],
    ('step15/measure/out', MO, '*'),
    *[(f'step15/measure/out/survey-{p}', MO / f'survey-{p}', g) for p in ('1x1', '8x8-1if') for g in ('*.txt', '*.out', '*.json')],
    *[(f'step15/measure/out/survey-{p}/{v}', MO / f'survey-{p}/{v}', g) for p in ('1x1', '8x8-1if')
      for v in ('ordinary-costs', 'long-costs') for g in ('*.txt', '*.json')],
    ('step15/measure', S / 'r8cut', 'project-*-92de01f7.txt'), ('step15/measure', S / 'r8cut', 'cputable-*.md'),
    # ruling item 4 for 1x1/1if, prepared in a scratch clone and not committed: the patch and its grading
    ('step15/item4', S / 'r8cut/item4', '*'), ('step15/item4', S / 'checks', 'r8-item4.tsv'),
    ('tools', S / 'tools', 'collect8.py'),
]


def put(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    if len(data) <= LIMIT:
        shutil.copyfile(src, dst)
        return
    tail = data.decode(errors='replace').splitlines()[-60:]
    dst.with_name(dst.name + '.stub.txt').write_text(
        f'{src.name}: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}; over 200 KB, kept in scratch. '
        f'Its last {len(tail)} lines:\n' + '\n'.join(tail) + '\n')


#: Many small logs, each set one file in the receipts (each log's name, then its text), so the index stays under 200 KB.
JOINED = [
    ('step15/gates/q-92de01f7.txt', S / 'r8gates/q', '*.log'),
    ('step15/gates/docswf-92de01f7.txt', S / 'r8gates/docswf', '*.log'),
    ('step15/gates-fb083864/q-fb083864.txt', S / 'r8gates2/q', '*.log'),
    *[(f'step15/measure/legs-{p}/parts-{p}.txt', M / p, '*.part*.log') for p in ('1x1', '8x8-1if')],
    *[(f'step15/measure/legs-{p}/parts-rc-{p}.txt', M / p, '*.part*.rc') for p in ('1x1', '8x8-1if')],
]


n = 0
for dest, root, pattern in JOINED:
    files = sorted(f for f in root.glob(pattern) if f.is_file())
    text = ''.join(f'==== {f.name}\n{f.read_text(errors="replace")}' + ('' if f.read_text(errors="replace").endswith('\n') else '\n')
                   for f in files)
    target = out / dest
    target.parent.mkdir(parents=True, exist_ok=True)
    if len(text.encode()) <= LIMIT:
        target.write_text(text)
    else:
        tmp = S / 'tmp' / target.name
        tmp.write_text(text)
        put(tmp, target)
    n += 1
for where, root, pattern in SOURCES:
    if not root.is_dir():
        continue
    for f in sorted(root.glob(pattern)):
        if f.is_file() and not f.is_symlink() and not f.name.endswith('.gz'):
            put(f, out / where / f.name)
            n += 1
print(f'{n} files collected into {out}')
