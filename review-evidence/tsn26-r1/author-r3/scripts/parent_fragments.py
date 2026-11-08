# SPDX-License-Identifier: MIT
# usage: parent_fragments.py PARENT_DIR OLD_TREE NEW_TREE
# Parses (never imports) the parent's ACMP mutant tables and reports each fragment that selects exactly one
# place in OLD_TREE but not in NEW_TREE.
import ast, sys
from pathlib import Path
parent, old_tree, new_tree = map(Path, sys.argv[1:4])
paths = {'ACMP_C': 'src/acmp.c', 'ACMP_H': 'include/acmp.h'}
rows = []
for name in ('acmp_mutants.py', 'acmp_review_mutants.py'):
    tree = ast.parse((parent / name).read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'Mutant' and len(node.args) >= 4:
            label, where, old = node.args[0], node.args[1], node.args[2]
            if not (isinstance(label, ast.Constant) and isinstance(where, ast.Name) and isinstance(old, ast.Constant)):
                continue
            rel = paths.get(where.id)
            if rel is None:
                continue
            before = (old_tree / rel).read_text().count(old.value)
            after = (new_tree / rel).read_text().count(old.value)
            rows.append((name, node.lineno, label.value, rel, before, after))
print('fragments parsed:', len(rows))
for name, line, label, rel, before, after in rows:
    if before == 1 and after != 1:
        print(f'{name}:{line} {label} ({rel}): matches {before} at the old tree, {after} at the new tree')
