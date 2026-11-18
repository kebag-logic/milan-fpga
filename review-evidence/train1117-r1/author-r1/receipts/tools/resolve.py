#!/usr/bin/env python3
"""Resolve a diff3-style conflicted file hunk by hunk.

usage: resolve.py <file> <choice> [<choice> ...]
Each choice applies to the next hunk, in order: 'ours', 'theirs', 'ours+theirs', 'theirs+ours', or '@<path>' (the
replacement text read from <path>). The number of choices must equal the number of hunks; the file is rewritten
only when every hunk is resolved, and no conflict marker may survive."""
import sys
from pathlib import Path


def main():
    path = Path(sys.argv[1])
    choices = sys.argv[2:]
    lines = path.read_text().splitlines(True)
    out, i, n = [], 0, 0
    while i < len(lines):
        if lines[i].startswith('<<<<<<< '):
            ours, base, theirs, part = [], [], [], 'o'
            i += 1
            while not lines[i].startswith('>>>>>>> '):
                l = lines[i]
                if l.startswith('||||||| '):
                    part = 'b'
                elif l == '=======\n':
                    part = 't'
                else:
                    {'o': ours, 'b': base, 't': theirs}[part].append(l)
                i += 1
            if n >= len(choices):
                sys.exit(f'{path}: more hunks than choices ({len(choices)})')
            c = choices[n]
            n += 1
            if c == 'ours':
                out += ours
            elif c == 'theirs':
                out += theirs
            elif c == 'ours+theirs':
                out += ours + theirs
            elif c == 'theirs+ours':
                out += theirs + ours
            elif c.startswith('@'):
                out.append(Path(c[1:]).read_text())
            else:
                sys.exit(f'unknown choice {c}')
        else:
            out.append(lines[i])
        i += 1
    if n != len(choices):
        sys.exit(f'{path}: {n} hunks, {len(choices)} choices')
    text = ''.join(out)
    for m in ('<<<<<<< ', '>>>>>>> ', '||||||| '):
        if any(l.startswith(m) for l in text.splitlines()):
            sys.exit(f'{path}: a marker survives')
    path.write_text(text)
    print(f'{path}: {n} hunk(s) resolved: {" ".join(choices)}')


main()
