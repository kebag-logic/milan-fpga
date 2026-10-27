#!/usr/bin/env python3
"""Write each file of a zero-context patch as BASE plus a chosen subset of its hunks, so a round's
edits can be committed in logical steps; every hunk's pre-image is BASE's, so any subset applies.

usage: stage_hunks.py CHECKOUT BASE PATCH HUNKS
BASE is the commit the patch was taken against (not HEAD, which moves as the steps are committed).
HUNKS is a comma-separated list of 1-based hunk numbers, counted across the patch in order.
"""
import re
import subprocess
import sys
from pathlib import Path

checkout, base, patch = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]).read_text()
chosen = {int(h) for h in sys.argv[4].split(',')}
files: dict[str, list] = {}
name, n = None, 0
for line in patch.splitlines(keepends=True):
    if line.startswith('+++ '):
        name = line[6:].rstrip('\n')
        files.setdefault(name, [])
    elif line.startswith('@@'):
        n += 1
        m = re.match(r'@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@', line)
        start, length = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
        files[name].append([n, start, length, [], []])
    elif line.startswith('-') and not line.startswith('---'):
        files[name][-1][3].append(line[1:])
    elif line.startswith('+') and not line.startswith('+++'):
        files[name][-1][4].append(line[1:])
for name, hunks in files.items():
    head = subprocess.run(['git', '-C', str(checkout), 'show', f'{base}:{name}'], capture_output=True, text=True,
                          check=True).stdout.splitlines(keepends=True)
    out, at = [], 0
    for number, start, length, old, new in hunks:
        if number not in chosen:
            continue
        # A pure insertion's start is the line after which it goes; a change's is its first old line.
        first = start if length == 0 else start - 1
        out += head[at:first]
        assert head[first:first + length] == old, (name, number)
        out += new
        at = first + length
    out += head[at:]
    (checkout / name).write_text(''.join(out))
    print(f'{name}: {sum(1 for h in hunks if h[0] in chosen)} of {len(hunks)} hunks')
