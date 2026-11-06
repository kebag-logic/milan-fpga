#!/usr/bin/env python3
"""stand_in_scan.py ELF: the stand-in constants in the flash port's functions (lui of the timer and the window) and,
over every loaded section, any aligned word equal to the stand-in timer or window address."""
import re, struct, subprocess, sys
elf = sys.argv[1]
od = 'riscv32-linux-objdump'
dis = subprocess.run([od, '-d', elf], capture_output=True, text=True, check=True).stdout
fn, hits, seen = None, {}, set()
for line in dis.splitlines():
    m = re.match(r'[0-9a-f]+ <(.+)>:', line)
    if m:
        fn = m.group(1)
    if fn and re.match(r'(ls_|nvm_flash_litespi)', fn):
        seen.add(fn)
        m = re.search(r'\blui\s+\w+,(0x[0-9a-f]+)', line)
        if m:
            hits.setdefault(m.group(1), []).append(fn)
print(f'{len(seen)} flash port functions')
for name, value in (('timer 0xf0003800', '0xf0004'), ('window 0x20000000', '0x20000')):
    print(f'  lui {value} ({name}): {len(hits.get(value, []))} {sorted(set(hits.get(value, [])))}')
print('  other lui:', {k: len(v) for k, v in hits.items() if k not in ('0xf0004', '0x20000')})
data = open(elf, 'rb').read()
sections = re.findall(r'\]\s+(\.\S+)\s+\S+\s+([0-9a-f]{8})\s+([0-9a-f]{6})\s+([0-9a-f]{6})',
                      subprocess.run(['riscv32-linux-readelf', '-S', '-W', elf], capture_output=True, text=True).stdout)
for v in (0xf0003800, 0x20000000):
    found = [f'{name}+{i:#x}' for name, _, off, size in sections if name in ('.text', '.rodata', '.data')
             for i in range(0, int(size, 16) - 3, 4)
             if data[int(off, 16) + i:int(off, 16) + i + 4] == struct.pack('<I', v)]
    print(f'  aligned word {v:#x} in .text/.rodata/.data: {found}')
