#!/usr/bin/env python3
"""collect2.py OUT: round 2's receipts into OUT/receipts, each file at most 200 KB; a larger one becomes
<name>.stub.txt with its size, sha256 and last 60 lines. Sources are listed below, relative to the scratch root."""
import hashlib
import shutil
import sys
from pathlib import Path

S = Path('<scratch>')
out = Path(sys.argv[1]) / 'receipts'
LIMIT = 200 * 1024
SOURCES = [
    # quick checks at each round-2 head
    ('steps/s7', S / 'q/r2-s7', '*'), ('steps/fix', S / 'q/r2-fix', '*'), ('steps/s8', S / 'q/r2-s8', '*'),
    ('steps', S / 'q', 'r2-s7.summary*'), ('steps', S / 'q', 'r2-fix.summary*'), ('steps', S / 'q', 'r2-s8.summary*'),
    ('steps', S / 'q', 'over-base-flip_check.txt'),
    # the four firmware shards at each head, the gate and coverage runs
    ('firmware', S / 'logs', 'r2-s7-fw*.log*'), ('firmware', S / 'logs', 'r2-fix-fw*.log*'),
    ('firmware', S / 'logs', 'r2-s8-fw*.log*'), ('firmware', S / 'logs', 's7-cov.log*'),
    ('firmware', S / 'logs', 'fix-cov.log*'), ('firmware', S / 'logs', 's8-cov.log*'),
    ('firmware', S / 'logs', 's8-gate.log*'), ('firmware', S / 'logs', 's8fix-gate.log*'),
    # the ledger's measurements
    ('ledger', S / 'logs', 's7-plat-ledger*.log*'), ('ledger', S / 'logs', 's8-plat-ledger*.log*'),
    ('ledger', S / 'logs', 'pl-tip.log*'), ('ledger', S / 'logs', 'pl-931.log*'),
    ('ledger', S / 'logs', 's7-ctrl_memory.log'), ('ledger', S / 'logs', 's8-ctrl_memory.log*'),
    *[(f'ledger/{st}-{pt}', S / pl / pt, 'size.json') for st, pl in (('s7', 's7r2/pl2'), ('s8', 's8/pl2'),
      ('tip', 's7r2/pl-tip'), ('931', 's7r2/pl-931')) for pt in ('1x1-if1', '1x1-if2', '8x8-if1', '8x8-if2')],
    # decision 3's attribution
    ('attribution', S / 'attr', '*.py'), ('attribution', S / 'attr', '*.sh'), ('attribution/out', S / 'attr/out', '*'),
    ('attribution/logs', S / 'attr/logs', '*'),
    *[(f'attribution/legs/{h}', S / f'attr/b/{h}', '*.log') for h in
      ('base', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 'fix', 's8', '931', '931-np')],
    # resolutions and tools
    ('conflicts/s7', S / 's7r2', '*.res.py'), ('conflicts/s7', S / 's7r2', '*.res.final.py'),
    ('conflicts/s8', S / 's8', '*.res.py'),
    ('tools', S / 'tools', 'blocks.py'), ('tools', S / 'tools', 'collect2.py'), ('tools', S / 'bin', '*.sh'),
    ('tools', S / 'checks', 's7.tsv'), ('tools', S / 'checks', 'fix.tsv'), ('tools', S / 'checks', 's8.tsv'),
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
