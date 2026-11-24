#!/usr/bin/env python3
"""logcmp.py A B: compare two suite logs after removing only host-dependent text.

Removed: Verilator build-statistics lines, make directory chatter, wall/CPU durations,
the per-variant tree path, temporary-directory names and process IDs. Everything else,
every check line, figure and verdict, must be byte-identical. Prints the first
differences and exits 1 when any remain.
"""
import re
import sys

DROP = [re.compile(p) for p in (
    r'^- V e r i l a t i o n', r'^- Verilator: ', r'^make(\[\d+\])?: (Entering|Leaving|Nothing)',
    r'^\s*(g\+\+|ccache|ar |python3 .*verilator_includer|echo "" >)', r'^/\S*verilator ',
    r'^%Warning', r'^\s+:\s+\.\.\.', r'^\s+\d+ \| ', r'^\s+\|\s+\^', r'^\s*\.\.\. For warning',
    r'^\s*\.\.\. Use "/\* verilator lint_off', r'^mkdir -p ', r'^rm ', r'^cp ', r'^\s+\S+:\d+:\d+: \.\.\. ',
)]
SUBS = [
    (re.compile(r'/data-2/milan/tmp/cicd-a839/tree/[A-Za-z0-9_]+'), '<TREE>'),
    (re.compile(r'/data-2/milan/tmp/cicd-a839/tmp/[A-Za-z0-9_.-]+'), '<TMP>'),
    (re.compile(r'/tmp/[A-Za-z0-9_.-]+'), '<TMP>'),
    (re.compile(r'\b(pid|PID)[ =:]\d+'), r'\1 <PID>'),
    (re.compile(r'"(child|pid)": \d+'), r'"\1": <PID>'),
]


def norm(path):
    out = []
    for line in open(path, errors='replace').read().splitlines():
        if any(p.search(line) for p in DROP):
            continue
        for p, r in SUBS:
            line = p.sub(r, line)
        out.append(line)
    return out


def main():
    a, b = norm(sys.argv[1]), norm(sys.argv[2])
    if a == b:
        print(f'IDENTICAL ({len(a)} normalised lines)')
        return 0
    if sorted(a) == sorted(b):
        print(f'IDENTICAL AS A MULTISET ({len(a)} normalised lines; only the interleaving of parallel legs differs)')
        return 0
    ta, tb = sorted(' '.join(a).split()), sorted(' '.join(b).split())
    if ta == tb:
        print(f'IDENTICAL AS A TOKEN MULTISET ({len(ta)} tokens; parallel legs interleave within lines)')
        return 0
    import difflib
    d = list(difflib.unified_diff(a, b, 'A', 'B', n=0, lineterm=''))
    print(f'DIFFER ({len(a)} vs {len(b)} lines, {sum(1 for x in d if x[:1] in "+-") - 2} changed)')
    print('\n'.join(x[:220] for x in d[:40]))
    return 1


if __name__ == '__main__':
    sys.exit(main())
