#!/usr/bin/env python3
"""Rebuild the five standalone images against the merged dev firmware."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
packet = Path(__file__).resolve().parent
out = packet / 'scratch/standalone-images'
argv = [sys.executable, 'sw/firmware/ctrl/test/ctrl_image.py', '--base', 'd5858bbe', '--out', str(out)]
for shape in sorted((root / 'configs').glob('endstation_*.yaml')):
    argv.extend(['--shape', shape.stem])
subprocess.run(argv, check=True)
rows = []
for head in sorted((out / 'head').rglob('ctrl_app.elf')):
    rel = head.relative_to(out / 'head')
    base = out / 'base' / rel
    assert head.read_bytes() == base.read_bytes(), rel
    rows.append({'shape': rel.parts[0], 'bytes': head.stat().st_size,
                 'sha256': hashlib.sha256(head.read_bytes()).hexdigest()})
assert len(rows) == 5
(packet / 'standalone-images.json').write_text(json.dumps(rows, indent=2) + '\n')
print('standalone image equality: 5/5, bytes and SHA-256')
