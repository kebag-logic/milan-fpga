#!/usr/bin/env python3
"""R843-6-F1's sweep at a tree: every tracked text file (git ls-files; svg figures apart) searched for the figures the
hold-off had before round 13, 69.84, 2,026 (with 2026 cs, 2026u and li a3,2026), and for 70 ms (70 ms, 70ms, 70u,
at 70) within 200 characters of 8x8/1if, CTRL_LOOP_TX_MS, THE TRANSMIT, the hold-off or the tx row. Prints each hit
with its context, for the scope to be read off it. usage: python3 -I sweep.py TREE"""
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
head = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
files = subprocess.run(['git', '-C', str(root), 'ls-files'], capture_output=True, text=True).stdout.split()
OLD = re.compile(r'69\.84|2,026|\b2026 ?cs\b|\b2026u\b|li a3,2026')
SEVENTY = re.compile(r'\b70 ?ms\b|\b70u\b|\bat 70\b')
NEAR = re.compile(r'8x8/1if|CTRL_LOOP_TX_MS|THE TRANSMIT|hold-off|tx row', re.I)
print(f'# R843-6-F1 sweep at {head}: {OLD.pattern} anywhere; {SEVENTY.pattern} within 200 characters of {NEAR.pattern}')
hits = 0
for name in files:
    path = root / name
    if name.endswith('.svg') or not path.is_file():
        continue
    try:
        text = path.read_text()
    except (UnicodeDecodeError, OSError):
        continue
    for n, line in enumerate(text.splitlines(), 1):
        for pattern, near in ((OLD, False), (SEVENTY, True)):
            for m in pattern.finditer(line):
                if near and not NEAR.search(line[max(0, m.start() - 200):m.end() + 200]):
                    continue
                hits += 1
                print(f'{name}:{n}: ...{line[max(0, m.start() - 150):m.end() + 80]}...')
print(f'{hits} hit(s)')
