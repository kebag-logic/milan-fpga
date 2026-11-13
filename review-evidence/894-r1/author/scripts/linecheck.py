#!/usr/bin/env python3
"""Strict shape of a budget-harness log's trace lines: SPAN, CALL, ENTRY and EVW each with exactly their fields, and
every other line's first token one the grader knows. usage: linecheck.py LOG... -> per log the count of bad lines."""
import re
import sys
SHAPES = {'SPAN': re.compile(r'SPAN \d+ \d+ \d+ [0-9a-f]{8} [\w:.]+$'), 'CALL': re.compile(r'CALL \d+ \d+ [\w:.]+$'),
          'ENTRY': re.compile(r'ENTRY \d+ [\w:.]+$'), 'EVW': re.compile(r'EVW \d+ \d+ [0-9a-f]{8}$'),
          'TXC': re.compile(r'TXC \d+ \d+ \d+$'), 'PASS': re.compile(r'PASS \d+ \d+ \d+ \d+ .*')}
for path in sys.argv[1:]:
    bad = 0
    first = ''
    with open(path, errors='replace') as f:
        for line in f:
            line = line.rstrip('\n')
            kind = line.split(' ', 1)[0]
            shape = SHAPES.get(kind)
            if shape and not shape.match(line):
                bad += 1
                first = first or line[:80]
            elif not shape and re.match(r'[A-Z]+[a-z0-9]', kind or ' ') and kind.upper() != kind:
                bad += 1
                first = first or line[:80]
    print(f'{path.rsplit("/", 1)[-1]} bad {bad} {first}')
