#!/usr/bin/env python3
"""anchors.py TREE BASE FILE... -- MODULE...: every string literal (ast) of each Python MODULE that occurs in a FILE
at git revision BASE of TREE and no longer occurs in the work tree's FILE: a planted defect's or an edit's anchor this
change would break. Literals under 12 characters are skipped. Exit 1 when any is found."""
import ast
import subprocess
import sys
from pathlib import Path

tree, base = Path(sys.argv[1]), sys.argv[2]
sep = sys.argv.index('--')
files, modules = sys.argv[3:sep], sys.argv[sep + 1:]
old = {f: subprocess.run(['git', '-C', str(tree), 'show', f'{base}:{f}'], capture_output=True, text=True,
                         check=True).stdout for f in files}
new = {f: (tree / f).read_text() for f in files}
broken = 0
for mod in modules:
    src = (tree / mod).read_text()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) >= 12:
            for f in files:
                if node.value in old[f] and node.value not in new[f]:
                    broken += 1
                    print(f"{mod}:{node.lineno}: {f}: {node.value[:110]!r}")
print(f"{broken} anchors broken")
sys.exit(1 if broken else 0)
