#!/usr/bin/env python3
"""hot_census.py NM BASE.elf HEAD.elf: the hot section's functions (_ctrl_hot_start .. _ctrl_hot_end), each by its
place in the section (static functions can share a name), base against head: the section's bounds, those resized,
those at another offset only (and by how much), those unchanged, and where the changed ones lie."""
import subprocess, sys
from collections import Counter
nm = sys.argv[1]
def hot(elf):
    rows = [l.split() for l in subprocess.run([nm, '-n', '-S', elf], capture_output=True, text=True,
                                              check=True).stdout.splitlines()]
    addr = {r[-1]: int(r[0], 16) for r in rows if len(r) >= 3}
    lo, hi = addr['_ctrl_hot_start'], addr['_ctrl_hot_end']
    return [(int(r[0], 16) - lo, int(r[1], 16), r[3]) for r in rows
            if len(r) == 4 and r[2] in 'tT' and lo <= int(r[0], 16) < hi], hi - lo
(b, bs), (h, hs) = hot(sys.argv[2]), hot(sys.argv[3])
print(f'hot section: base {bs} B, {len(b)} functions; head {hs} B, {len(h)} functions')
assert [n for *_, n in b] == [n for *_, n in h], 'the functions differ in name or order'
pairs = list(zip(b, h))
resized = [(k, x, y) for k, (x, y) in enumerate(pairs) if x[1] != y[1]]
shifted = [(k, y[0] - x[0]) for k, (x, y) in enumerate(pairs) if x[1] == y[1] and x[0] != y[0]]
print(f'changed in offset or size: {len(resized) + len(shifted)}')
print(f'resized: {len(resized)}: ' + ', '.join(f'{x[2]} {x[1]} -> {y[1]} B at offset {x[0]} (moved {y[0] - x[0]:+d} B)'
                                               for _, x, y in resized))
print(f'at another offset only (the same size): {len(shifted)}, moved by {dict(Counter(d for _, d in shifted))}')
print(f'unchanged: {len(pairs) - len(resized) - len(shifted)}')
if resized:
    k0 = resized[0][0]
    print(f'after {b[k0][2]} in the section: {len(pairs) - k0 - 1} functions, {sum(1 for k, _ in shifted if k > k0)} '
          f'of them moved; before it: {k0}, {sum(1 for k, _ in shifted if k < k0)} of them moved')
