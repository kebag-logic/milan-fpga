#!/usr/bin/env python3
"""merge_words.py FILE BASE: resolve each conflict region of FILE (git's markers, ours then theirs, equal line counts)
line by line with a word-level three-way merge against BASE (stage 1): every change #902's side made to the base
words is applied to this branch's line where this branch left those words unchanged, so each side's text stands where
it states its own figures. Refuses (rc 1) a region whose word changes overlap, and prints every applied change."""
import difflib
import sys
from pathlib import Path


def base_line(base, ours, theirs):
    return max(base, key=lambda b: difflib.SequenceMatcher(None, b, theirs, autojunk=False).quick_ratio()
               + difflib.SequenceMatcher(None, b, ours, autojunk=False).quick_ratio())


def merge(b, o, t):
    bw, ow, tw = b.split(' '), o.split(' '), t.split(' ')
    ours_changed = set()
    for tag, i1, i2, _, _ in difflib.SequenceMatcher(None, bw, ow, autojunk=False).get_opcodes():
        if tag != 'equal':
            ours_changed.update(range(i1, max(i2, i1 + 1)))
    # map base word index -> ours word index for unchanged words
    to_ours = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, bw, ow, autojunk=False).get_opcodes():
        if tag == 'equal':
            to_ours.update({i1 + k: j1 + k for k in range(i2 - i1)})
    edits = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, bw, tw, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        span = range(i1, max(i2, i1 + 1))
        if ours_changed.intersection(span) or (tag == 'insert' and (i1 - 1 in ours_changed and i1 in ours_changed)):
            return None, f'overlap at base words {i1}-{i2}: [{" ".join(bw[i1:i2])}] -> [{" ".join(tw[j1:j2])}]'
        if tag == 'insert':
            at = to_ours[i1] if i1 in to_ours else to_ours[i1 - 1] + 1
            edits.append((at, at, tw[j1:j2]))
        else:
            edits.append((to_ours[i1], to_ours[i2 - 1] + 1, tw[j1:j2]))
    out = ow[:]
    for a, z, words in sorted(edits, reverse=True):
        print(f'  apply: [{" ".join(out[a:z])}] -> [{" ".join(words)}]')
        out[a:z] = words
    return ' '.join(out), None


path, base = Path(sys.argv[1]), Path(sys.argv[2]).read_text().splitlines()
lines = path.read_text().splitlines(keepends=False)
res, i, bad = [], 0, 0
while i < len(lines):
    if not lines[i].startswith('<<<<<<< '):
        res.append(lines[i])
        i += 1
        continue
    j = lines.index('=======', i)
    k = next(n for n in range(j, len(lines)) if lines[n].startswith('>>>>>>> '))
    ours, theirs = lines[i + 1:j], lines[j + 1:k]
    assert len(ours) == len(theirs), (i, len(ours), len(theirs))
    for o, t in zip(ours, theirs):
        b = base_line(base, o, t)
        if o == b:
            res.append(t)
            print(f'line {i}: theirs (ours unchanged)')
        elif t == b:
            res.append(o)
            print(f'line {i}: ours (theirs unchanged)')
        else:
            print(f'line {i}: word merge')
            m, err = merge(b, o, t)
            if err:
                print('  REFUSED', err)
                bad += 1
                res.append(o)
            else:
                res.append(m)
    i = k + 1
path.write_text('\n'.join(res) + '\n')
sys.exit(1 if bad else 0)
