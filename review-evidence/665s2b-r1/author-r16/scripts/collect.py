#!/usr/bin/env python3
"""Copy a leg's receipts into receipts/measure/<leg>/ with host paths redacted: its driver log, build.json, table.md,
results.json.gz (or its sha256 and size when over 200 KB), the image's sha256, and a label.
usage: collect.py LEG LABEL [SUBDIR [HELPER ...]]   (SUBDIR under receipts/, default measure)"""
import gzip, hashlib, json, re, sys
from pathlib import Path

T = Path('$VALIDATION_STORAGE/665s2b-a683u')
R = Path('$MANAGEMENT/2026-09-23/665s2b-a683u/receipts/measure')
LIMIT = 200_000
SUBS = [('$VALIDATION_STORAGE/665s2b-a683u', '<scratch>'), ('$VALIDATION_STORAGE', '<tmp>'), ('$LANES', '<lanes>'),
        ('$VALIDATION_TOOLS', '<tools>'), ('$VALIDATION_STORAGE/scratch', '<tools>'), ('$WORKSPACE_HOME', '$HOME')]


def redact(text: str) -> str:
    for a, b in SUBS:
        text = text.replace(a, b)
    return text


leg, label = sys.argv[1], sys.argv[2]
out = (R.parent / sys.argv[3] if len(sys.argv) > 3 else R) / leg
out.mkdir(parents=True, exist_ok=True)
(out / 'label.txt').write_text(label + '\n')
log = T / 'logs' / f'{leg}.log'
lines = [l for l in log.read_text(errors='replace').splitlines() if not re.match(r'^[│├└ ]', l)]
(out / 'run.log').write_text(redact('\n'.join(lines)) + '\n')
# a leg finished with helper runs (finish_leg.sh): its stop and merge, its regrade, and each helper's own log
for extra in sorted((T / 'logs').glob(f'{leg}-*.log')) + [T / 'logs' / f'{h}.log' for h in sys.argv[4:]]:
    kept = [l for l in extra.read_text(errors='replace').splitlines() if not re.match(r'^[│├└ ]', l)]
    (out / extra.name.replace(f'{leg}-', '', 1) if extra.name.startswith(f'{leg}-') else out / f'helper-{extra.name}'
     ).write_text(redact('\n'.join(kept)) + '\n')
split = T / 'logs' / f'{leg}-split.txt'
if split.is_file():
    (out / 'split.txt').write_text(redact(split.read_text(errors='replace')))
b = T / 'builds' / leg
(out / 'build.json').write_text(redact((b / 'build.json').read_text()))
(out / 'table.md').write_text(redact((b / 'results/table.md').read_text()))
data = gzip.compress((b / 'results/results.json').read_bytes(), mtime=0)
if len(data) <= LIMIT:
    (out / 'results.json.gz').write_bytes(data)
else:
    (out / 'results.json.gz.sha256').write_text(f'{hashlib.sha256(data).hexdigest()}  {len(data)} B (over 200 KB, kept off)\n')
elf = (b / 'image/ctrl_app.elf').read_bytes()
(out / 'image.txt').write_text(f'ctrl_app.elf sha256 {hashlib.sha256(elf).hexdigest()} {len(elf)} B\n')
print(leg, sorted(p.name for p in out.iterdir()))
