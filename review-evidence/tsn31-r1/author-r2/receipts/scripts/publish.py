#!/usr/bin/env python3
"""usage: publish.py OUT -- copy the round's receipts into OUT/receipts with host paths replaced by $SCRATCH, $TOOLS,
$LANES and $HOME; files over 200 KB are not copied, only their SHA-256 and size (receipts/not-copied.txt)."""
import hashlib
import shutil
import sys
from pathlib import Path

S = Path('$SCRATCH')
OUT = Path(sys.argv[1]) / 'receipts'
LIMIT = 200 * 1024
SUBS = [('$NODE_BIN', '$NODE_BIN'), ('$SCRATCH', '$SCRATCH'), ('$TOOLS', '$TOOLS'), ('$LANES', '$LANES'),
        ('$HOME', '$HOME')]
picks = []
g = S / 'gates'
picks += [(p, 'gates/' + p.name) for p in sorted(g.glob('*')) if p.is_file()]
picks += [(p, 'gates/val/' + p.name) for p in sorted((g / 'val').glob('*')) if p.is_file()]
picks += [(g / 'val/mutations/results.json', 'gates/val/mutations/results.json'),
          (g / 'val/conditionals/results.json', 'gates/val/conditionals/results.json'),
          (g / 'rv32/results.json', 'gates/rv32/results.json')]
r = S / 'rev'
picks += [(p, 'reviewers/' + p.name) for p in sorted(r.glob('*')) if p.is_file()]
picks += [(r / 'r811-plants-s2-anchor/results.json', 'reviewers/r811-plants-s2-anchor/results.json')]
picks += [(p, 'reviewers/r811-survivors/' + p.parent.name + '.' + p.name) for p in sorted((r / 'r811-survivors').glob('*/ctest.log'))]
picks += [(p, 'reviewers/r812-wide-gaps/' + p.parent.name + '.run.log') for p in sorted((r / 'r812-wide-gaps').glob('*/run.log'))]
for name in ('probes-escape-matrix.log', 'probes-escape-matrix.rc', 'probes-variant-wrap.log', 'probes-rv32-text.log',
             'ctl-mask.log', 'ctl-probe.log', 'cond-dev.log'):
    picks.append((S / name, 'probes/' + name.removeprefix('probes-')))
picks += [(S / 'probes/escape-matrix/results.json', 'probes/escape-matrix-results.json')]
for t in ('main', 'r1'):
    picks += [(S / f'rv32-before-{t}/results.json', f'probes/rv32-before-{t}-results.json'),
              (S / f'rv32-before-{t}.log', f'probes/rv32-before-{t}.log')]
picks += [(S / 'probes-image-sizes.txt', 'probes/image-sizes.txt')]
for step in ('c1', 'c2'):
    picks += [(p, f'steps/{step}/' + p.name) for p in sorted((S / 'steps' / step).glob('*.log'))]
    picks += [(S / 'steps' / step / 'mut/results.json', f'steps/{step}/mutation-results.json')] if step == 'c1' else []
picks += [(p, 'scripts/' + p.relative_to(S / 'scripts').as_posix()) for p in sorted((S / 'scripts').rglob('*')) if p.is_file()]
picks += [(S / 'env.sh', 'scripts/env.sh')]
skipped = []
shutil.rmtree(OUT, ignore_errors=True)
for src, rel in picks:
    if not src.exists():
        skipped.append(f'missing {rel}')
        continue
    data = src.read_bytes()
    try:
        text = data.decode()
        for a, b in SUBS:
            text = text.replace(a, b)
        data = text.encode()
    except UnicodeDecodeError:
        pass
    if len(data) > LIMIT:
        skipped.append(f'{hashlib.sha256(src.read_bytes()).hexdigest()}  {src.stat().st_size} B  {rel}')
        continue
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
(OUT / 'not-copied.txt').write_text('Files over 200 KB, by SHA-256 of the original and its size:\n' + '\n'.join(skipped) + '\n')
print(len(picks), 'picked;', len(skipped), 'not copied')
