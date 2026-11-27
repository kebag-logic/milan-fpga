#!/usr/bin/env python3
"""manifest6.py OUTDIR: per arm, each group's log the regrade read (its link in r6/regrade/<point>/<variant>), the run
that wrote it (s<k>: the original shard; st, su, sv: the tail runs), bytes and sha256."""
import hashlib, os, sys
from pathlib import Path
T = Path('<scratch>/r8'); out = Path(sys.argv[1])
for p in ('1x1', '8x8-1if'):
    for d in sorted((T / 'regrade' / p).iterdir()):
        if not d.is_dir():
            continue
        lines = [f'# {p} {d.name}: each group\'s log, the run that wrote it (r7/s-<group>: the every-arm pool at 163e467f; r8/s-<group>: the rescripted reruns at ea52ec11), bytes, sha256']
        for log in sorted(d.glob('*.log')):
            real = Path(os.path.realpath(log))
            h = hashlib.sha256(real.read_bytes()).hexdigest()
            lines.append(f'{log.stem} {real.parts[-6]}/{real.parent.name} {real.stat().st_size} {h}')
        (out / f'manifest-{p}-{d.name}.txt').write_text('\n'.join(lines) + '\n')
        print(p, d.name, len(lines) - 1)
