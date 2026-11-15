#!/usr/bin/env python3
"""Reviewer probe: compare the changed non-Markdown files between two commits at their compiled/executed level.
usage: python3 -I identity_r837.py REPO BASE HEAD"""
import ast, hashlib, subprocess, sys
repo, base, head = sys.argv[1:4]
def show(c, p): return subprocess.run(['git', '-C', repo, 'show', f'{c}:{p}'], capture_output=True, check=True).stdout
def tok(src):
    return subprocess.run(['gcc', '-fpreprocessed', '-dD', '-E', '-P', '-x', 'c', '-'], input=src, capture_output=True, check=True).stdout
names = subprocess.run(['git', '-C', repo, 'diff', '--name-only', base, head], capture_output=True, text=True, check=True).stdout.split()
for p in names:
    a, b = show(base, p), show(head, p)
    if p.endswith(('.c', '.h')):
        ta, tb = tok(a), tok(b)
        print(p, 'tokens identical', ta == tb, 'lines', a.count(b'\n'), b.count(b'\n'), hashlib.sha256(tb).hexdigest()[:16])
    elif p.endswith('.py'):
        ma, mb = ast.parse(a), ast.parse(b)
        da, db = ast.get_docstring(ma), ast.get_docstring(mb)
        for m in (ma, mb):
            if da != db: m.body[0].value.value = ''
        print(p, 'AST(with positions, docstring blanked if changed) identical', ast.dump(ma, include_attributes=True) == ast.dump(mb, include_attributes=True), 'docstring changed', da != db)
    else:
        print(p, 'markdown/other')
