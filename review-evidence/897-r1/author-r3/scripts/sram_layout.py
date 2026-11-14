#!/usr/bin/env python3
"""The data layout of two linked images (#909: a cost moves with the data cache's placement of the stack and .bss):
every symbol in a writable section (.data, .sdata, .bss, .sbss, the stack and the heap/arena), by name, address and
size, and the sections' addresses; prints each difference and the count. usage: sram_layout.py NM READELF BASE_ELF HEAD_ELF"""
import subprocess, sys
nm, readelf, base, head = sys.argv[1:5]
def sections(elf):
    out = {}
    for line in subprocess.run([readelf, '-SW', elf], capture_output=True, text=True, check=True).stdout.splitlines():
        p = line.replace('[ ', '[').split()
        if len(p) > 6 and p[0].startswith('[') and p[0] != '[Nr]' and 'W' in (p[7] if len(p) > 7 else ''):
            out[p[1]] = (int(p[3], 16), int(p[5], 16))
    return out
def symbols(elf, secs):
    lo = min(a for a, _ in secs.values()); hi = max(a + s for a, s in secs.values())
    out = {}
    for line in subprocess.run([nm, '-S', '--defined-only', elf], capture_output=True, text=True, check=True).stdout.splitlines():
        p = line.split()
        if len(p) == 4 and lo <= int(p[0], 16) < hi:
            out[p[3]] = (int(p[0], 16), int(p[1], 16))
        elif len(p) == 3 and lo <= int(p[0], 16) <= hi:
            out[p[2]] = (int(p[0], 16), 0)
    return out
sb, sh = sections(base), sections(head)
print('writable sections base:', {k: (hex(a), s) for k, (a, s) in sb.items()})
print('writable sections head:', {k: (hex(a), s) for k, (a, s) in sh.items()})
yb, yh = symbols(base, sb), symbols(head, sh)
diff = sorted(set(yb) ^ set(yh)) + sorted(k for k in set(yb) & set(yh) if yb[k] != yh[k])
for k in diff:
    print(f'  {k}: base {yb.get(k)} head {yh.get(k)}')
print(f'{len(yb)} writable symbols at base, {len(yh)} at head, {len(diff)} differ; sections {"equal" if sb == sh else "differ"}')
sys.exit(1 if diff or sb != sh else 0)
