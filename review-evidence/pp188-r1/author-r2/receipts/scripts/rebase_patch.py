#!/usr/bin/env python3
"""Rebase a one-hunk text-substitution patch onto the current file: the same
removed and added lines, fresh context. usage: rebase_patch.py <repo> <patch>"""
import difflib, re, sys
from pathlib import Path
repo, patch = Path(sys.argv[1]), Path(sys.argv[2])
lines = patch.read_text().splitlines(keepends=True)
target = lines[0][len('--- a/'):].strip()
minus = [l[1:] for l in lines[3:] if l.startswith('-')]
plus = [l[1:] for l in lines[3:] if l.startswith('+')]
src = (repo / target).read_text()
old, new = ''.join(minus), ''.join(plus)
assert src.count(old) == 1, (patch, src.count(old))
dst = src.replace(old, new)
out = difflib.unified_diff(src.splitlines(keepends=True), dst.splitlines(keepends=True),
                           'a/' + target, 'b/' + target, n=3)
text = ''.join(out)
text = re.sub(r'^(--- a/\S+|\+\+\+ b/\S+)\s*$', r'\1', text, flags=re.M)
patch.write_text(text)
