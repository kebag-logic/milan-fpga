#!/usr/bin/env python3
"""Every offset and bit of the three register tables in MARK_II_STREAM_ENGINES.md is defined or
reserved exactly once, and each reset value fits its field. Usage: check_regmap_r5.py <page>"""
import re, sys
L = open(sys.argv[1], encoding='utf-8').read().split('\n')
def table(head):
    i = next(n for n, l in enumerate(L) if l.startswith(head))
    while not L[i].startswith('| Offset'):
        i += 1
    i += 2
    rows = []
    while L[i].startswith('|'):
        rows.append([c.strip() for c in L[i].strip('|').split('|')])
        i += 1
    return rows
bad = 0
for head, top, step_note in (('### Engine registers', 0x2000, 'block'), ('### Talker context', 0x40, 'ctx'), ('### Listener context', 0x80, 'ctx')):
    rows = table(head)
    words, cur = {}, None
    next_off, spans = 0, 0
    for r in rows:
        off, name, bits, field, reset, acc = r[0], r[1], r[2], r[3], r[4], r[5]
        if off:
            m = re.fullmatch(r'0x([0-9A-F]+)(?:-0x([0-9A-F]+))?', off)
            a = int(m.group(1), 16); b = int(m.group(2) or m.group(1), 16)
            if a != next_off:
                print(f'{head}: gap or overlap at {off}, expected {next_off:#x}'); bad += 1
            next_off = b + 4; cur = off; words[cur] = [name, 0]; spans += 1
        if bits == '-':
            words[cur][1] = 0xFFFFFFFF
            continue
        m = re.fullmatch(r'(\d+)(?::(\d+))?', bits)
        hi = int(m.group(1)); lo = int(m.group(2) or m.group(1))
        mask = ((1 << (hi - lo + 1)) - 1) << lo
        if words[cur][1] & mask:
            print(f'{head}: {cur} overlapping bits {bits}'); bad += 1
        words[cur][1] |= mask
        h = re.match(r'0x([0-9A-F_]+)', reset)
        if h and int(h.group(1).replace('_', ''), 16) >= 1 << (hi - lo + 1):
            print(f'{head}: {cur} {field} reset {reset} does not fit {bits}'); bad += 1
    for k, (n, mask) in words.items():
        if mask != 0xFFFFFFFF:
            print(f'{head}: {k} {n} bits not all defined: {mask:#x}'); bad += 1
    print(f'{head}: {spans} rows of offsets, ends at {next_off:#x}, expected {top:#x}', 'ok' if next_off == top else 'MISMATCH')
    bad += next_off != top
print('listener reserved octets 0x48-0x7C:', 0x80 - 0x48)
print('WMAP 22 + HEAD_POS 9 + HEAD_VALID 1 =', 22 + 9 + 1, '; HEAD_POS addresses', 2 ** 9, 'samples, the 192 kHz depth 512')
print('map span: 2.667 ms / 125 us =', round(2666.667 / 125, 2), 'packets, under 22')
print('window: 62.5 - 2.744 - 0.55 =', round(62.5 - 2.744 - 0.55, 3), 'us margin; neighbour apart', round(125 - 0.55 - 2.744, 3), 'us')
print('E_x: 2 + 200e-6 x 2917 + 0.160 =', round(2 + 200e-6 * 2917 + .16, 4), 'us')
print('sweep: 32 contexts / 31.25 ms = ', 1 / .03125, 'per s; 128 cycles / 32 =', 128 / 32, 'cycles per context')
print('save: 10 + 5.35 + 2 + 32 x 5.35 x 2 =', 10 + 5.35 + 2 + 2 * 32 * 5.35, 'ms; +5.35 =', round(10 + 5.35 + 2 + 2 * 32 * 5.35 + 5.35, 2), 'ms')
print('RESULT', 'FAIL' if bad else 'PASS', bad)
sys.exit(1 if bad else 0)
