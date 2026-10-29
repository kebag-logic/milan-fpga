"""For each file, the lines each side added over the merge base that the head no longer holds (whitespace-stripped).
usage: merge_sides.py BASE LANE S1 HEAD FILE..."""
import subprocess, sys
base, lane, s1, head, *files = sys.argv[1:]
def lines(rev, f):
    r = subprocess.run(['git', 'show', f'{rev}:{f}'], capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else []
for f in files:
    b, h = set(map(str.strip, lines(base, f))), set(map(str.strip, lines(head, f)))
    for side, rev in (('lane', lane), ('S1', s1)):
        added = [l for l in map(str.strip, lines(rev, f)) if l and l not in b]
        gone = [l for l in added if l not in h]
        print(f'{f}: {side} added {len(added)}, absent at head {len(gone)}')
        for l in gone[:40]:
            print(f'    - {l[:150]}')
