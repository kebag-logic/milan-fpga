"""anchors.py OLD_TREE NEW_TREE FILE...: every string literal of the firmware test modules (sw/firmware/ctrl/test,
tb/) that occurs in an OLD_TREE source FILE but not in NEW_TREE's: an anchor the change would break."""
import ast, sys
from pathlib import Path
old, new = Path(sys.argv[1]), Path(sys.argv[2])
files = sys.argv[3:]
srcs = {f: ((old / f).read_text(), (new / f).read_text()) for f in files}
mods = list((new / 'sw/firmware/ctrl/test').glob('*.py')) + list((new / 'tb').rglob('*.py'))
broken = []
for m in mods:
    try:
        tree = ast.parse(m.read_text())
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) >= 12:
            for f, (o, n) in srcs.items():
                if node.value in o and node.value not in n:
                    broken.append((str(m.relative_to(new)), f, node.value[:90]))
for b in sorted(set(broken)):
    print(b)
print(len(set(broken)), 'broken anchors')
