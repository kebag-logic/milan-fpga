#!/usr/bin/env python3
"""collect4.py OUT: round 4's receipts into OUT/receipts, each file at most 200 KB; a larger one becomes
<name>.stub.txt with its size, sha256 and last 60 lines."""
import hashlib
import shutil
import sys
from pathlib import Path

S = Path('<scratch>')
out = Path(sys.argv[1]) / 'receipts'
LIMIT = 200 * 1024
SOURCES = [
    ('step10/q', S / 'q/r4-p10', '*'),
    ('step10/firmware', S / 'logs', 'r4-p10-fw*.log*'), ('step10/twin', S / 'logs', 'r4-p10-twin.log*'),
    ('step10/ledger', S / 'logs', 'r4-p10-ledger.log*'), ('step10/ledger', S / 'p10led', 'plat-ledger.log'),
    ('step10/ledger', S / 'p10led', 'ctrl_memory.log'), ('step10/ledger', S / 'p10led', 'fixture-summary.txt'),
    ('step10/ledger-before-restatement', S / 's10', 'plat-ledger.log'),
    ('step10/ledger-before-restatement', S / 's10/fx/answering-ports', 'image.log'),
    ('step10/conflicts', S / 's10', '*.res.py'),
    ('cut', S / 'cut', '*.py'), ('cut', S / 'cut', '*.sh'), ('cut', S / 'cut', '*.perfunc.txt'),
    ('cut', S / 'cut', '*.pcs'), ('cut/cc', S / 'cut/cc', '*.c'),
    ('cut/attribution', S / 'logs', 'attr-cut*.log*'), ('cut/attribution', S / 'logs', 'trace-cut*.log*'),
    *[(f'cut/attribution/{h}', S / f'attr/b/{h}', '*.log') for h in ('cut1', 'cut2')],
    ('cut/attribution/out', S / 'attr/out', 'cut*.json'),
    ('cut/gates/firmware', S / 'logs', 'r4-cut-fw*.log*'), ('cut/gates/twin', S / 'logs', 'r4-cut-twin.log*'),
    ('hot', S / 'r4hot', '*.sh'), ('hot', S / 'r4hot', '*.py'), ('hot', S / 'r4hot', '*.txt'),
    ('hot', S / 'r4hot', '*.log'), ('hot', S / 'r4hot', 'order.summary'), ('hot', S / 'r4hot', '*.pcs'),
    ('hot', S / 'r4hot', '*.diff'), ('hot', S / 'logs', 'r4-relearn.log*'),
    ('tip/q', S / 'q/r4-tip', '*'), ('tip/firmware', S / 'logs', 'r4-tip-fw*.log*'),
    ('tip/twin', S / 'logs', 'r4-tip-twin.log*'), ('tip/ledger', S / 'logs', 'r4-tip-ledger.log*'),
    ('tip/ledger', S / 'tipled', 'plat-ledger.log'), ('tip/ledger', S / 'tipled', 'ctrl_memory.log'),
    ('tip/ledger', S / 'tipled', 'fixture-summary.txt'),
    ('measure', S / 'r4meas/out', '*'),
    ('measure/febbfc4b', S / 'r4meas/out/febbfc4b', '*'),
    ('measure/febbfc4b/survey-1x1', S / 'r4meas/out/febbfc4b/survey-1x1', '*.txt'),
    ('measure/febbfc4b/survey-1x1', S / 'r4meas/out/febbfc4b/survey-1x1', '*.json'),
    ('measure/febbfc4b/legs-1x1', S / 'r4meas/febbfc4b/1x1', '*.log'),
    ('measure/febbfc4b/legs-1x1', S / 'r4meas/febbfc4b/1x1', '*.rc'),
    ('measure/febbfc4b/survey-8x8-1if', S / 'r4meas/out/febbfc4b/survey-8x8-1if', '*.txt'),
    ('measure/febbfc4b/survey-8x8-1if', S / 'r4meas/out/febbfc4b/survey-8x8-1if', '*.json'),
    ('measure/febbfc4b/legs-8x8-1if', S / 'r4meas/febbfc4b/8x8-1if', '*.log'),
    ('measure/febbfc4b/legs-8x8-1if', S / 'r4meas/febbfc4b/8x8-1if', '*.rc'),
    ('measure/febbfc4b/survey-8x8', S / 'r4meas/out/febbfc4b/survey-8x8', '*.txt'),
    ('measure/febbfc4b/survey-8x8', S / 'r4meas/out/febbfc4b/survey-8x8', '*.json'),
    ('measure/febbfc4b/legs-8x8', S / 'r4meas/febbfc4b/8x8', '*.log'),
    ('measure/febbfc4b/legs-8x8', S / 'r4meas/febbfc4b/8x8', '*.rc'),
    ('measure/var', S / 'r4meas/out/var', '*'),
    ('measure/var/survey-1x1', S / 'r4meas/out/var/survey-1x1', '*.txt'),
    ('measure/var/survey-1x1', S / 'r4meas/out/var/survey-1x1', '*.json'),
    ('measure/var/legs-1x1', S / 'r4meas/var/1x1', '*.log'),
    ('measure/var/legs-1x1', S / 'r4meas/var/1x1', '*.rc'),
    ('measure/var/survey-8x8-1if', S / 'r4meas/out/var/survey-8x8-1if', '*.txt'),
    ('measure/var/survey-8x8-1if', S / 'r4meas/out/var/survey-8x8-1if', '*.json'),
    ('measure/var/legs-8x8-1if', S / 'r4meas/var/8x8-1if', '*.log'),
    ('measure/var/legs-8x8-1if', S / 'r4meas/var/8x8-1if', '*.rc'),
    ('measure/var/survey-8x8', S / 'r4meas/out/var/survey-8x8', '*.txt'),
    ('measure/var/survey-8x8', S / 'r4meas/out/var/survey-8x8', '*.json'),
    ('measure/var/legs-8x8', S / 'r4meas/var/8x8', '*.log'),
    ('measure/var/legs-8x8', S / 'r4meas/var/8x8', '*.rc'),
    ('measure/45af90b3', S / 'r4meas/out/45af90b3', '*'),
    ('measure/45af90b3/survey-1x1', S / 'r4meas/out/45af90b3/survey-1x1', '*.txt'),
    ('measure/45af90b3/survey-1x1', S / 'r4meas/out/45af90b3/survey-1x1', '*.json'),
    ('measure/45af90b3/legs-1x1', S / 'r4meas/45af90b3/1x1', '*.log'),
    ('measure/45af90b3/legs-1x1', S / 'r4meas/45af90b3/1x1', '*.rc'),
    ('measure/45af90b3/survey-8x8-1if', S / 'r4meas/out/45af90b3/survey-8x8-1if', '*.txt'),
    ('measure/45af90b3/survey-8x8-1if', S / 'r4meas/out/45af90b3/survey-8x8-1if', '*.json'),
    ('measure/45af90b3/legs-8x8-1if', S / 'r4meas/45af90b3/8x8-1if', '*.log'),
    ('measure/45af90b3/legs-8x8-1if', S / 'r4meas/45af90b3/8x8-1if', '*.rc'),
    ('measure/45af90b3/survey-8x8', S / 'r4meas/out/45af90b3/survey-8x8', '*.txt'),
    ('measure/45af90b3/survey-8x8', S / 'r4meas/out/45af90b3/survey-8x8', '*.json'),
    ('measure/45af90b3/legs-8x8', S / 'r4meas/45af90b3/8x8', '*.log'),
    ('measure/45af90b3/legs-8x8', S / 'r4meas/45af90b3/8x8', '*.rc'),
    ('measure/single-groups', S / 'r4meas/fanout', '*.log'),
    ('measure/single-groups', S / 'r4meas/srp', '*.log'),
    ('measure/single-groups', S / 'logs', 'early-*.log*'), ('measure/single-groups', S / 'logs', 'fan*-*.log*'),
    ('measure/single-groups', S / 'logs', 'srp-*.log*'), ('measure/single-groups', S / 'logs', 'sameimg.log*'),
    ('measure', S / 'r4meas', 'STOPPED.txt'), ('measure', S / 'r4meas', 'variant.diff'),
    ('measure/logs', S / 'logs', 'an-*.log*'),
    ('ledger/step9-tip', S / 's9fixled', 'plat-ledger.log'), ('ledger/step9-tip', S / 's9fixled', 'ctrl_memory.log'),
    ('ledger/step9-tip-before-restatement', S / 's9tipled', 'plat-ledger.log'),
    ('ledger/tip-25b2a5b7', S / 'tip2led', 'plat-ledger.log'), ('ledger/variant', S / 'varled', 'plat-ledger.log'),
    ('ledger/logs', S / 'logs', '*ledger*.log*'),
    ('steps/step9-tip-q', S / 'q/r4-s9tip', '*'),
    ('ledger/variant', S / 'varled', 'fixture-summary.txt'), ('ledger/step9-tip', S / 's9fixled', 'fixture-summary.txt'),
    ('ledger/step9-tip-before-restatement', S / 's9tipled', 'fixture-summary.txt'),
    ('ledger/step9-tip-before-restatement', S / 's9tipled/fx/answering-ports', 'image.log'),
    ('ledger/tip', S / 'tipled/fx/none', 'image.log'),
    ('tools', S / 'tools', 'blocks.py'), ('tools', S / 'tools', 'collect4.py'), ('tools', S / 'tools', 'legs.py'),
    ('tools', S / 'bin', '*.sh'), ('tools', S / 'bin', '*.py'), ('tools', S / 'checks', 's8.tsv'),
    ('tools', S / 'r4meas', '*.sh'), ('tools', S / 'r4meas', '*.py'),
    ('tools/survey', S / 'tools/survey', '*'),
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
