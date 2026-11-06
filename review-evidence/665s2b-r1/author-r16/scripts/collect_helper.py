#!/usr/bin/env python3
"""Copy a helper's (or an early grade's) receipts into receipts/measure/<name>/ with host paths redacted: its driver
log or regrade log, its table.md and results.json.gz (or their sha256 and size when over 200 KB), the build's
build.json and image sha256, and a label.
usage: collect_helper.py NAME BUILD RESULTS_DIR LOG LABEL"""
import gzip, hashlib, re, sys
from pathlib import Path
T = Path('$VALIDATION_STORAGE/665s2b-a683u')
R = Path('$MANAGEMENT/2026-09-23/665s2b-a683u/receipts/measure')
SUBS = [('$VALIDATION_STORAGE/665s2b-a683u', '<scratch>'), ('$VALIDATION_STORAGE', '<tmp>'), ('$LANES', '<lanes>'),
        ('$VALIDATION_TOOLS', '<tools>'), ('$VALIDATION_STORAGE/scratch', '<tools>'), ('$WORKSPACE_HOME', '$HOME')]
def redact(t):
    for a, b in SUBS:
        t = t.replace(a, b)
    return t
name, build, results, log, label = sys.argv[1:6]
out = R / name; out.mkdir(parents=True, exist_ok=True)
(out / 'label.txt').write_text(label + '\n')
lines = [l for l in Path(log).read_text(errors='replace').splitlines() if not re.match(r'^[│├└ ]', l) and not l.startswith('COMMAND')]
(out / 'run.log').write_text(redact('\n'.join(lines)) + '\n')
b, r = T / 'builds' / build, Path(results)
(out / 'build.json').write_text(redact((b / 'build.json').read_text()))
(out / 'table.md').write_text(redact((r / 'table.md').read_text()))
data = gzip.compress((r / 'results.json').read_bytes(), mtime=0)
if len(data) <= 200_000:
    (out / 'results.json.gz').write_bytes(data)
else:
    (out / 'results.json.gz.sha256').write_text(f'{hashlib.sha256(data).hexdigest()}  {len(data)} B (over 200 KB, kept off)\n')
elf = (b / 'image/ctrl_app.elf').read_bytes()
(out / 'image.txt').write_text(f'ctrl_app.elf sha256 {hashlib.sha256(elf).hexdigest()} {len(elf)} B\n')
print(name, sorted(p.name for p in out.iterdir()))
