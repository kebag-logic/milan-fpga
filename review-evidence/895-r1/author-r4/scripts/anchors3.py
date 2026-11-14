#!/usr/bin/env python3
"""anchors3.py TREE OURS THEIRS: every string literal (ast, at least 12 characters) of a planted-defect or edit
module of TREE's work tree that is an anchor in its own lineage (present in a firmware/harness file at the revision
whose copy of the module the work tree carries: OURS, THEIRS, or either when both changed it) and is absent from the
work tree's file: an anchor the merge breaks. Exit 1 when any is found."""
import ast, re, subprocess, sys
from pathlib import Path
tree, ours, theirs = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
def git(*a):
    return subprocess.run(['git', '-C', str(tree), *a], capture_output=True, text=True)
def show(rev, f):
    r = git('show', f'{rev}:{f}')
    return r.stdout if r.returncode == 0 else None
mods = [m for m in git('ls-files', 'sw/firmware/*.py', 'tb/verilator/*.py', 'scripts/*.py').stdout.split()
        if re.search(r'mutant|plant|hooks|variant|build\.py|campaign|defect', m)]
files = [f for f in git('ls-files', 'sw/firmware', 'tb', 'hdl').stdout.split()
         if re.search(r'\.(c|h|cpp|hpp|sv|py|S|ld)$', f)]
changed = set(git('diff', '--name-only', ours, theirs).stdout.split())
cand = [f for f in files if f in changed]
cache = {}
def text(rev, f):
    if (rev, f) not in cache:
        cache[rev, f] = show(rev, f) if rev else ((tree / f).read_text() if (tree / f).is_file() else None)
    return cache[rev, f]
broken = 0
for m in mods:
    now = (tree / m).read_text()
    lineage = [r for r in (ours, theirs) if show(r, m) == now] or [ours, theirs]
    for node in ast.walk(ast.parse(now)):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) >= 12:
            for f in cand:
                cur = text(None, f)
                if cur is None or node.value in cur:
                    continue
                if any((text(r, f) or '').find(node.value) >= 0 for r in lineage):
                    broken += 1
                    print(f"{m}:{node.lineno} [{'/'.join(r[:8] for r in lineage)}]: {f}: {node.value[:110]!r}")
print(f"{broken} anchors broken")
sys.exit(1 if broken else 0)
