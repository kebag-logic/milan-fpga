"""Lines present at a head in a file but in neither merge parent (the resolution's own lines), plus lines the
post-merge commits add, for each file the round's delta touches outside docs/."""
import subprocess, sys
def show(rev, path):
    r = subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else []
p1, p2, merge, head = sys.argv[1:5]
files = subprocess.run(['git', 'diff', '--name-only', p1, head], capture_output=True, text=True).stdout.split()
for f in files:
    parents = set(show(p1, f)) | set(show(p2, f))
    for n, line in enumerate(show(head, f), 1):
        if line not in parents and line.strip():
            print(f'{f}:{n}: {line}')
