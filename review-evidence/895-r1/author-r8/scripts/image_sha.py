#!/usr/bin/env python3
"""image_sha.py LEDGER_DIR: the sha256 of every image ledger.sh linked under LEDGER_DIR (the platform's at each
shape, the size fixture's at each point, the harness's two 8x8/2if arms): each ctrl_app.elf's loadable bytes
(objcopy -O binary) and every linked object, one line a file, relative to LEDGER_DIR, sorted. Objects carry no debug
or macro sections, so equal bytes are equal code at one clone path or another."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
lines = []
for elf in sorted(root.rglob('ctrl_app.elf')):
    with tempfile.NamedTemporaryFile(suffix='.bin') as f:
        subprocess.run(['riscv32-buildroot-linux-gnu-objcopy', '-O', 'binary', str(elf), f.name], check=True)
        lines.append((hashlib.sha256(Path(f.name).read_bytes()).hexdigest(), str(elf.relative_to(root)) + ' [loadable]'))
    for o in sorted(elf.parent.rglob('*.o')):
        lines.append((hashlib.sha256(o.read_bytes()).hexdigest(), str(o.relative_to(root))))
for h, n in sorted(lines, key=lambda x: x[1]):
    print(h, n)
