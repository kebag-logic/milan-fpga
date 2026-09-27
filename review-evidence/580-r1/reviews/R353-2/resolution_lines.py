#!/usr/bin/env python3
"""Line-level three-way audit of one conflict resolution.

Usage: resolution_lines.py <repo> <path> <base> <ours> <theirs> <merge> [adjudicated.txt]
Lines listed in the optional file are the assigned conflict replacements; they are
reported as ADJUDICATED instead of DROPPED.
A line absent from the merge is a dropped fact unless the other side removed or
replaced it relative to the base. A merge line present on neither side is new text.
"""
import subprocess
import sys


def lines(repo: str, rev: str, path: str) -> list[str]:
    return subprocess.check_output(['git', '-C', repo, 'show', f'{rev}:{path}'],
                                   stderr=subprocess.DEVNULL).decode().splitlines()


def main() -> int:
    repo, path, base, ours, theirs, merge = sys.argv[1:7]
    adjudicated = set()
    if len(sys.argv) > 7:
        with open(sys.argv[7], encoding='utf-8') as fh:
            adjudicated = set(fh.read().splitlines())
    b, o, t, m = (lines(repo, r, path) for r in (base, ours, theirs, merge))
    sb, so, st, sm = set(b), set(o), set(t), set(m)
    new = [x for x in m if x not in so and x not in st]
    fail = False
    print(f'lines: base {len(b)}, ours {len(o)}, theirs {len(t)}, merge {len(m)}')
    print(f'duplicated lines in merge: {len(m) - len(sm)}')
    print(f'merge lines on neither side: {len(new)}')
    for x in new:
        print('  NEW:', x[:160])
        fail = True
    for label, side, other in (('ours', so, st), ('theirs', st, so)):
        dropped = [x for x in side if x not in sm]
        print(f'{label} lines absent from merge: {len(dropped)}')
        for x in dropped:
            removed_by_other = x in sb and x not in other
            state = ('removed-by-other-side' if removed_by_other else
                     'ADJUDICATED' if x in adjudicated else 'DROPPED')
            print(f'  {state}: {x[:160]}')
            fail |= state == 'DROPPED'
    origin = {'both': 0, 'ours-only': 0, 'theirs-only': 0}
    for x in m:
        origin['both' if x in so and x in st else 'ours-only' if x in so else
               'theirs-only' if x in st else 'both'] += 0 if x not in so and x not in st else 1
    print('merge line origins:', origin)
    print('RESULT:', 'FAIL' if fail else 'PASS')
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
