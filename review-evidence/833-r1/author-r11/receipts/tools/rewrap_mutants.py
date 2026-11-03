"""Re-lay MUTANTS entries whose words take three or more lines: control and words on a hanging indent.

usage: python3 -I rewrap_mutants.py SUPPORT.py [--write]
Only layout changes. The dict is compared with the original, value for value, before anything is written.
"""
import ast
import sys
from pathlib import Path

path = Path(sys.argv[1])
src = path.read_text()
lines = src.splitlines(keepends=True)
module = ast.parse(src)
node = next(n for n in module.body if isinstance(n, ast.AnnAssign) and getattr(n.target, "id", "") == "MUTANTS")
edits = []  # (first line index, last line index of words, replacement lines)
for key, value in zip(node.value.keys, node.value.values):
    if not isinstance(value, ast.Tuple) or len(value.elts) < 3:
        continue
    control, words = value.elts[0], value.elts[1]
    if words.end_lineno - words.lineno + 1 < 3 or key.lineno != words.lineno:
        continue
    head = f'    "{key.value}": (\n'
    body = f'        "{control.value}", "{words.value}",\n'
    if len(body.rstrip("\n")) > 120:
        continue
    # The words end with '",' on their last line; nothing else may share those lines.
    first, last = key.lineno - 1, words.end_lineno - 1
    assert lines[last].rstrip().endswith('",'), (key.value, lines[last])
    edits.append((first, last, [head, body]))
for first, last, new in reversed(edits):
    lines[first:last + 1] = new
out = "".join(lines)
before = ast.literal_eval(ast.unparse(node.value))
after_node = next(n for n in ast.parse(out).body if isinstance(n, ast.AnnAssign) and n.target.id == "MUTANTS")
after = ast.literal_eval(ast.unparse(after_node.value))
assert before == after and list(before) == list(after), "MUTANTS changed"
print(f"{len(edits)} entries re-laid, {len(src.splitlines()) - len(out.splitlines())} lines saved; MUTANTS identical")
for first, _last, new in edits:
    print("  ", new[0].strip())
if "--write" in sys.argv:
    path.write_text(out)
