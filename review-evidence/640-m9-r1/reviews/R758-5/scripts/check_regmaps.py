#!/usr/bin/env python3
"""Sum the engine, talker-context and listener-context register tables on the
stream-engine page: every offset covered once with no gap, every word's bits
covered 31:0 once, and each reset value wide enough for its field.

Usage: python3 -I check_regmaps.py <MARK_II_STREAM_ENGINES.md>
"""
import re
import sys

lines = open(sys.argv[1], encoding='utf-8').read().splitlines()


def tables():
    want = {'### Engine registers': (0x000, 0x2000), '### Talker context': (0x00, 0x40),
            '### Listener context': (0x00, 0x80)}
    for i, line in enumerate(lines):
        if line in want:
            rows = []
            j = i + 1
            while not lines[j].startswith('| Offset'):
                j += 1
            j += 2
            while lines[j].startswith('|'):
                rows.append([c.strip() for c in lines[j].strip('|').split('|')])
                j += 1
            yield line, want[line], rows


problems = 0
for title, (start, end), rows in tables():
    words = []
    cur = None
    for r in rows:
        if r[0]:
            m = re.fullmatch(r'0x([0-9A-F]+)(?:-0x([0-9A-F]+))?', r[0])
            lo = int(m.group(1), 16)
            hi = int(m.group(2), 16) if m.group(2) else lo
            cur = {'lo': lo, 'hi': hi, 'name': r[1], 'bits': []}
            words.append(cur)
        cur['bits'].append((r[2], r[3], r[4]))
    at = start
    for w in words:
        if w['lo'] != at:
            print(f"{title}: gap or overlap at {w['lo']:#x}, expected {at:#x}")
            problems += 1
        at = w['hi'] + 4
        spec = [b for b in w['bits'] if b[0] != '-']
        cover = set()
        for bits, field, reset in spec:
            m = re.fullmatch(r'(\d+)(?::(\d+))?', bits)
            hi = int(m.group(1))
            lo = int(m.group(2)) if m.group(2) else hi
            for b in range(lo, hi + 1):
                if b in cover:
                    print(f"{title}: {w['name']} bit {b} twice")
                    problems += 1
                cover.add(b)
            hexv = re.fullmatch(r'0x([0-9A-Fa-f_]+)', reset)
            if hexv:
                digits = hexv.group(1).replace('_', '')
                need = (hi - lo + 1 + 3) // 4
                if len(digits) != need:
                    print(f"{title}: {w['name']}.{field} {bits}: reset {reset} has {len(digits)} digits, field needs {need}")
                    problems += 1
        if spec and cover != set(range(32)):
            print(f"{title}: {w['name']} bits missing {sorted(set(range(32)) - cover)}")
            problems += 1
    if at != end:
        print(f"{title}: ends at {at:#x}, expected {end:#x}")
        problems += 1
    print(f"{title}: {len(words)} words, ends at {at:#x}")
rmatch = [i + 1 for i, l in enumerate(lines) if re.search(r'merge rules? \d', l)]
print('merge rule citations at lines', rmatch)
print('problems', problems)
sys.exit(1 if problems else 0)
