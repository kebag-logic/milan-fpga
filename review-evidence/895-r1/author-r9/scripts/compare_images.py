#!/usr/bin/env python3
"""compare_images.py A.txt B.txt [LEDGER_A LEDGER_B]: the image_sha.py lists of two ledger.sh runs compared file by
file (relative paths, so clone paths drop out): the same set, how many differ, and each differing file. A file is
counted one-interface or two-interface by its image directory (`-if1` / `-if2` in the path, the harness's two arms
8x8/2if, and each shape's split export `plat/<shape>/split-soc`, which plat_ledger.py builds at one interface).
With the two ledger directories, each differing object and ELF is shown as the lines of `objdump -d` (instructions
with their bytes) and of `objdump -s` (every section's contents) that differ, so a reader sees which instruction or
word moved and that nothing else did."""
import difflib
import re
import subprocess
import sys
from pathlib import Path

OBJDUMP = 'riscv32-buildroot-linux-gnu-objdump'


def read(p):
    out = {}
    for line in Path(p).read_text().splitlines():
        h, name = line.split(' ', 1)
        out[name] = h
    return out


def kind(name):
    if re.search(r'-if2\b|/arm-|^arm-', name):
        return 'two'
    if re.search(r'-if1\b|/split-soc/', name):
        return 'one'
    return 'unclassified'


def dump(path, flag):
    text = subprocess.run([OBJDUMP, flag, str(path)], capture_output=True, text=True, check=True).stdout
    return [l for l in text.splitlines()[2:] if l.strip()]  # drop the file-name header


a_name, b_name = sys.argv[1], sys.argv[2]
a, b = read(a_name), read(b_name)
ledgers = [Path(p) for p in sys.argv[3:5]]
diff = sorted(n for n in a if n in b and a[n] != b[n])
print(f'{Path(a_name).stem} against {Path(b_name).stem}: {len(a)} and {len(b)} files, the same set: '
      f'{set(a) == set(b)}; differ: {len(diff)}')
for k in ('one', 'two', 'unclassified'):
    names = [n for n in diff if kind(n) == k]
    print(f'  {k}-interface images: {len(names)}')
    for n in names:
        print(f'    {n}')
if ledgers:
    for n in diff:
        rel = n.removesuffix(' [loadable]')
        pa, pb = ledgers[0] / rel, ledgers[1] / rel
        for flag, what in (('-d', 'instructions'), ('-s', 'section contents')):
            da, db = dump(pa, flag), dump(pb, flag)
            lines = [l for l in difflib.unified_diff(da, db, lineterm='', n=0) if l[:1] in '+-'
                     and not l.startswith(('+++', '---'))]
            print(f'\n## {n}: {what}, {len(lines)} differing line(s)')
            for l in lines[:40]:
                print('  ' + l)
