#!/usr/bin/env python3
"""collect.py OUT: copy this lane's check receipts into OUT/receipts, each file at most 200 KB; a larger one becomes
<name>.stub.txt with its size, sha256 and last 60 lines. Sources are listed below, relative to the scratch root."""
import hashlib
import shutil
import sys
from pathlib import Path

S = Path('<scratch>')
out = Path(sys.argv[1]) / 'receipts'
LIMIT = 200 * 1024
SOURCES = [
    ('steps/s1', S / 'q/s1', '*'), ('steps/s2', S / 'q/s2', '*'), ('steps/s3', S / 'q/s3', '*'),
    ('steps/s4', S / 'q/s4', '*'), ('steps/s5', S / 'q/s5', '*'), ('steps/s6', S / 'q/s6', '*'),
    ('steps/s2b', S / 'q/s2b', '*'), ('steps/s6b', S / 'q/s6b', '*'),
    *[(f'steps/{d.name}', d, '*') for d in sorted((S / 'q').glob('r2-*')) if d.is_dir()],
    ('steps', S / 'q', '*.summary'), ('steps', S / 'q', 's6.summary.keep'), ('steps', S / 'q', 'over-*.txt'),
    ('steps', S / 'q', 'base-flip_check.log'), ('steps', S / 'q', 's2b-flip_check.log'), ('steps', S / 'q', 'pyidiom-*.txt'),
    ('firmware', S / 'logs', 's*-fw*.log'), ('firmware', S / 'logs', 's*-fw*.log.rc'),
    ('firmware', S / 'logs', 'tip-fw*.log*'), ('firmware', S / 'logs', 'r2-s5-cov.log*'), ('firmware', S / 'logs', 's5-cov.log*'),
    ('firmware/cut-by-restart', S / 'logs/cut-by-restart', '*'),
    ('release', S / 'rel', '*.txt'), ('release', S / 'rel', '*.bins'), ('release', S / 'rel', '*.log'),
    ('release', S / 'rel', '*.log.rc'),
    ('legs', S / 'logs/legs', '*'),
    ('tools', S / 'tools', '*.py'), ('tools', S / 'bin', '*.sh'), ('tools', S / 'bin', '*.py'),
    ('tools/survey', S / 'tools/survey', '*'), ('tools', S / 'checks', '*.tsv'),
    ('conflicts', S, 's*-conflicts.txt'), ('conflicts/s6', S / 's6', 'fix_s6.patch'),
    *[(f'conflicts/s{k}/hunks', S / f's{k}/hunks', '*') for k in range(1, 8)],
    ('survey', S / 'survey', '*.txt'), ('survey', S / 'survey', '*.diff'), ('survey', S / 'survey', '*.out'),
    ('survey/p1x1', S / 'survey/p1x1', '*.txt'), ('survey/p1x1', S / 'survey/p1x1', '*.out'),
    ('survey/p1x1', S / 'survey/p1x1', '*.json'),
    *[(f'budget/p1x1/{v}', S / f'budget/p1x1/{v}', 'parts.json') for v in ('none', 'aep', 'vd', 'ap')],
    *[(f'budget/p1x1/{v}/part{k}', S / f'budget/p1x1/{v}/part{k}', n) for v in ('none', 'aep', 'vd', 'ap')
      for k in range(8) for n in ('table.md', 'results.json')],
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


n = 0
for where, root, pattern in SOURCES:
    if not root.is_dir():
        continue
    for f in sorted(root.glob(pattern)):
        if f.is_file():
            put(f, out / where / f.name)
            n += 1
print(f'{n} files collected into {out}')
