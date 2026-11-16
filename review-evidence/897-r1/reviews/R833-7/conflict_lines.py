"""For a file git's own merge leaves conflicted, list each side's conflict-hunk lines absent verbatim from the
committed resolution, with the hunk number, so each dropped or rewritten line can be read against its side."""
import subprocess, sys
tree, merge, path = sys.argv[1:4]
show = lambda rev: subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, text=True, check=True).stdout
conf, res = show(tree).splitlines(), set(show(merge).splitlines())
hunk, side, missing, kept = 0, None, 0, 0
for line in conf:
    if line.startswith('<<<<<<< '): hunk += 1; side = 'ours(b15da60a)'; continue
    if line == '=======' and side: side = 'theirs(70f4056f)'; continue
    if line.startswith('>>>>>>> '): side = None; continue
    if side and line.strip():
        if line in res: kept += 1
        else: missing += 1; print(f'hunk {hunk} {side} NOT VERBATIM: {line[:260]}')
print(f'{path}: {hunk} hunks, {kept} side lines kept verbatim, {missing} not verbatim')
