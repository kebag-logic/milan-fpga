#!/usr/bin/env python3
"""Write a reviewed one-substitution patch: usage make_patch.py <repo> <file> <out.patch>
reading OLD and NEW from the files given by env MP_OLD, MP_NEW (exact text, unique)."""
import difflib, os, sys
from pathlib import Path
repo, target, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
old = Path(os.environ['MP_OLD']).read_text()
new = Path(os.environ['MP_NEW']).read_text()
src = (repo / target).read_text()
assert src.count(old) == 1, ('occurrences', src.count(old))
dst = src.replace(old, new)
text = ''.join(difflib.unified_diff(src.splitlines(keepends=True), dst.splitlines(keepends=True),
                                    'a/' + target, 'b/' + target, n=3))
text = '\n'.join(l.rstrip(' \t') if l.startswith(('---', '+++')) else l for l in text.split('\n'))
out.write_text(text)
