#!/usr/bin/env python3
"""collect9.py OUT: ruling item 4 at 1x1/1if as the owner decided (#665 issuecomment-7044585511), committed as 8c5e2b4f,
into OUT/receipts/step16, each file at most 200 KB, a larger one a <name>.stub.txt with its size, sha256 and last 60
lines (collect5.py's rule): the patched tree's checks and the controls' mutation runs (item4b/), the gates at the head
(gates/), the images (images/), the 1x1/1if full re-measure (measure/) and the two gating bench bitstreams (gating/).
Run sanitize.py and index.py on OUT afterwards."""
import hashlib
import shutil
import sys
from pathlib import Path

S = Path('<scratch>')
out = Path(sys.argv[1]) / 'receipts' / 'step16'
LIMIT = 200 * 1024
REV = '8c5e2b4f0a487690cf0168f08b55e7f7be91a09c'
M, MO = S / 'r6meas' / REV, S / 'r6meas/out' / REV
G, W = S / 'r9gates', S / 'gate15'
ARMS = ('none', 'answering-ports', 'answering-every-port', 'valid-destinations', 'answering-later', 'shutdown-entry',
        'talker-notices', 'declaring-outputs')
SOURCES = [
    # the patched tree's checks before the commit, and each re-anchored control against a broken detector
    ('item4b/tools', S / 'checks', 'r8-item4[cde].tsv'), ('item4b', S / 'r8cut/q-item4e', 'control-mutations.log'),
    # the gates at the head: the shards, the twin, the receive monitor, the boundary twice, the boot, the ledger
    ('gates', G, '*.log'), ('gates', G, '*.rc'), ('gates/led', G / 'led', '*.log'), ('gates/led/fx', G / 'led/fx', '*.log'),
    ('gates', G, 'boot-*.log'),
    # the images
    ('images', G, 'img-*.txt'), ('images', G / 'img', 'hashes.txt'), ('images', S / 'r9gates', 'product-*.txt'),
    # the 1x1/1if full re-measure at the head
    ('measure', S / 'r6meas', f'analyse-*-{REV}.log'),
    *[('measure/legs-1x1', M / '1x1', g) for g in ('*.build.log', '*[a-z].log', '*.resume.log')],
    *[(f'measure/legs-1x1/{a}', M / f'1x1/{a}', 'parts.json') for a in ARMS],
    ('measure/out', MO, '*'),
    *[('measure/out/survey-1x1', MO / 'survey-1x1', g) for g in ('*.txt', '*.out', '*.json')],
    *[(f'measure/out/survey-1x1/{v}', MO / f'survey-1x1/{v}', g) for v in ('ordinary-costs', 'long-costs')
      for g in ('*.txt', '*.json')],
    ('measure', S / 'r8cut', f'project-*-{REV[:8]}.txt'), ('measure', S / 'r8cut', f'cputable-*{REV[:8]}*.md'),
    ('measure', S / 'r8cut', f'*-vs-*{REV[:8]}*.txt'),
    # the gating bench bitstreams: the chain's log, its tools, the argv, the identity gate, the artifacts, the floors
    ('gating', W, 'gate-*.log'), ('gating', W, 'gate-*.log.rc'), ('gating/tools', W / 'tools', '*'),
    *[(f'gating/{p}', W / f'work/g{p}', g) for p in ('1x1', '8x8')
      for g in ('argv.txt', 'identity.log', 'artifacts.sha256', 'signoff.txt', 'standin.log')],
    ('tools', S / 'tools', 'collect9.py'),
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
    ('item4b/q-item4c.txt', S / 'r8cut/q-item4c', '*.log'), ('item4b/q-item4d.txt', S / 'r8cut/q-item4d', '*.log'),
    ('item4b/q-item4e.txt', S / 'r8cut/q-item4e', '*.log'),
    ('gates/q.txt', G / 'q', '*.log'), ('gates/docswf.txt', G / 'docswf', '*.log'),
    ('measure/legs-1x1/parts-1x1.txt', M / '1x1', '*.part*.log'),
    ('measure/legs-1x1/parts-rc-1x1.txt', M / '1x1', '*.part*.rc'),
]


n = 0
for dest, root, pattern in JOINED:
    files = sorted(f for f in root.glob(pattern) if f.is_file())
    if not files:
        continue
    text = ''.join(f'==== {f.name}\n' + (lambda s: s if s.endswith('\n') else s + '\n')(f.read_text(errors='replace'))
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
