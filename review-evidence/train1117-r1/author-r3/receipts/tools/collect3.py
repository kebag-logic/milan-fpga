#!/usr/bin/env python3
"""collect3.py OUT: round 3's receipts into OUT/receipts, each file at most 200 KB; a larger one becomes
<name>.stub.txt with its size, sha256 and last 60 lines."""
import hashlib
import shutil
import sys
from pathlib import Path

S = Path('<scratch>')
out = Path(sys.argv[1]) / 'receipts'
LIMIT = 200 * 1024
SOURCES = [
    ('steps/s9', S / 'q/r3-s9', '*'), ('steps/tip', S / 'q/r3-tip', '*'),
    ('steps', S / 'q', 'r3-s9.summary*'), ('steps', S / 'q', 'r3-tip.summary*'),
    ('steps', S / 'q', 'over-base-flip_check.txt'), ('steps', S, 's9-mergetree.txt'),
    ('firmware', S / 'logs', 'r3-s9-fw*.log*'),
    ('twin', S / 'logs', 'r3-s9-twin.log*'),
    ('release', S / 'rel3', '*.txt'), ('release', S / 'rel3', '*.log'), ('release', S / 'rel3', '*.log.rc'),
    ('ledger', S / 'logs', 'r3-s9-ledger.log*'), ('ledger', S / 's9', 'plat-ledger.log'),
    ('ledger', S / 's9', 'ctrl_memory.log'), ('ledger', S / 's9', 'fixture-summary.txt'),
    *[(f'ledger/s9-{pt}', S / 's9/pl' / pt, 'size.json') for pt in ('1x1-if1', '1x1-if2', '8x8-if1', '8x8-if2')],
    ('invalid-838e2d21', S / 'logs/r3-invalid', '*.log*'), ('invalid-838e2d21/q', S / 'logs/r3-invalid/q-r3-s9', '*'),
    ('attribution', S / 'attr', '*.py'), ('attribution', S / 'attr', '*.sh'),
    ('attribution/out', S / 'attr/out', '*'), ('attribution/logs', S / 'attr/logs', '*'),
    *[(f'attribution/legs/{h}', S / f'attr/b/{h}', '*.log') for h in ('s9', 'hot-after', 'hot-keep')],
    ('hot', S / 'attr/hot', '*.py'), ('hot', S / 'attr/hot', '*.sh'), ('hot', S / 'attr/hot', '*.txt'),
    ('hot', S / 'attr/hot', '*.log'), ('hot', S / 'attr/hot', 'order.summary'), ('hot', S / 'attr/hot', '*.pcs'),
    ('hot/diff', S / 'attr/hot', '*.diff'),
    ('conflicts/s9', S / 's9', '*.res.py'),
    ('tools', S / 'tools', 'blocks.py'), ('tools', S / 'tools', 'collect3.py'), ('tools', S / 'tools', 'legs.py'),
    ('tools', S / 'bin', '*.sh'), ('tools', S / 'checks', 's8.tsv'),
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
