"""anchor_scan.py <base-ctrl_loop.h> <head-ctrl_loop.h> <py files...>: every Python string literal (constant parts of
f-strings included) of at least 4 characters that occurs in either ctrl_loop.h, whose occurrence count differs between
base and head. A text plant or reader anchored on such a literal could change meaning at head."""
import ast, sys
base, head = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
seen, changed = 0, []
for path in sys.argv[3:]:
    tree = ast.parse(open(path, encoding="utf-8").read(), path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) >= 4:
            s = node.value
            if s in base or s in head:
                seen += 1
                if base.count(s) != head.count(s):
                    changed.append(f"{path}:{node.lineno}: {s!r:.80} base={base.count(s)} head={head.count(s)}")
print(f"literals found in ctrl_loop.h: {seen}; with a changed count: {len(changed)}")
print("\n".join(changed))
