#!/usr/bin/env python3
"""Word-level three-way merge of each diff3 hunk of a file.

usage: wordmerge.py <file> [--hunks 1,3,...] [--dry]
For each selected hunk, base->ours and base->theirs are diffed word by word (difflib over \\S+ and whitespace
tokens). Edits that touch disjoint base ranges are both applied; an insertion at the same point as the other side's
insertion keeps ours then theirs. Overlapping edits leave the hunk unresolved and are printed. Without --dry the
file is rewritten with every cleanly merged hunk resolved (the rest left as conflicts)."""
import difflib
import re
import sys
from pathlib import Path

TOK = re.compile(r'\s+|[^\s]+')


def toks(s):
    return TOK.findall(s)


def edits(base, side):
    sm = difflib.SequenceMatcher(None, base, side, autojunk=False)
    return [(i1, i2, side[j1:j2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']


def merge3(base_s, ours_s, theirs_s):
    b, o, t = toks(base_s), toks(ours_s), toks(theirs_s)
    eo, et = edits(b, o), edits(b, t)
    # each edit: (start, end, replacement); check overlaps
    allx = [(s, e, r, 'o') for s, e, r in eo] + [(s, e, r, 't') for s, e, r in et]
    allx.sort(key=lambda x: (x[0], x[1], x[3]))
    for (s1, e1, r1, w1), (s2, e2, r2, w2) in zip(allx, allx[1:]):
        if w1 == w2:
            continue
        # overlap of base ranges (an insertion is an empty range)
        if s2 < e1 or (s1 == s2 and (e1 > s1 or e2 > s2) and not (e1 == s1 == s2 == e2)):
            if r1 == r2 and s1 == s2 and e1 == e2:
                continue  # the same edit on both sides
            return None, (s1, e1, ''.join(r1), w1, s2, e2, ''.join(r2), w2, ''.join(b[max(0, s1 - 8):e2 + 8]))
    out, pos = [], 0
    seen = set()
    for s, e, r, w in allx:
        key = (s, e, tuple(r))
        if key in seen:
            continue
        seen.add(key)
        out += b[pos:s]
        out += r
        pos = max(pos, e)
    out += b[pos:]
    return ''.join(out), None


def main():
    path = Path(sys.argv[1])
    sel = None
    if '--hunks' in sys.argv:
        sel = {int(x) for x in sys.argv[sys.argv.index('--hunks') + 1].split(',')}
    dry = '--dry' in sys.argv
    lines = path.read_text().splitlines(True)
    out, i, n, done, left = [], 0, 0, [], []
    while i < len(lines):
        if lines[i].startswith('<<<<<<< '):
            start = i
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
            n += 1
            if sel is None or n in sel:
                merged, why = merge3(''.join(base), ''.join(ours), ''.join(theirs))
                if merged is not None:
                    out.append(merged)
                    done.append(n)
                    i += 1
                    continue
                left.append(n)
                print(f'hunk {n}: overlapping edits:\n  ours/theirs at base tokens {why[0]}-{why[1]} / {why[4]}-{why[5]}'
                      f'\n  {why[3]}: {why[2][:300]!r}\n  {why[7]}: {why[6][:300]!r}\n  base near: {why[8][:300]!r}')
            out += lines[start:i + 1]
        else:
            out.append(lines[i])
        i += 1
    print(f'{path}: {n} hunk(s); merged {done}; left {left}')
    if not dry:
        path.write_text(''.join(out))


main()
