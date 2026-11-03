"""Re-lay MUTANTS words that a narrow visual indent wraps over more lines than needed (layout only).

usage: python3 -I rewrap_words.py SUPPORT.py [--write]
An entry is changed only if its words then take fewer lines: the first piece stays on the entry's own line, the
rest continue at the 8-space indent the dict already gives every edit. The whole dict is compared with the
original, value for value and in order, before anything is written.
"""
import ast
import sys
from pathlib import Path

path = Path(sys.argv[1])
src = path.read_text()
lines = src.splitlines(keepends=True)


def mutants(text: str) -> ast.Dict:
    return next(n for n in ast.parse(text).body
                if isinstance(n, ast.AnnAssign) and getattr(n.target, "id", "") == "MUTANTS").value


def pieces(text: str, first: int, rest: int) -> list[str]:
    """Split at spaces, each later piece keeping its leading space, as the dict's words do."""
    out, current = [], None
    for word in text.split(" "):
        joined = word if current is None else current + " " + word
        if current is None or len(joined) <= (first if not out else rest):
            current = joined
        else:
            out.append(current)
            current = " " + word
    return [*out, current]


changes = []
for key, value in zip(mutants(src).keys, mutants(src).values):
    if not isinstance(value, ast.Tuple) or len(value.elts) < 2 or not isinstance(value.elts[1], ast.Constant):
        continue
    words = value.elts[1]
    now = words.end_lineno - words.lineno + 1
    if now < 2:
        continue
    head = lines[words.lineno - 1][:words.col_offset]
    tail = lines[words.end_lineno - 1].rstrip("\n")
    assert tail.endswith('",'), (key.value, tail)
    split = pieces(words.value, 120 - len(head) - 3, 120 - 8 - 3)
    if len(split) >= now:
        continue
    new = [f'{head}"{split[0]}"\n', *[f'        "{piece}"\n' for piece in split[1:]]]
    new[-1] = new[-1][:-1] + ",\n"
    assert all(len(line.rstrip("\n")) <= 120 for line in new), new
    changes.append((words.lineno - 1, words.end_lineno - 1, new, key.value))
for first, last, new, _name in reversed(changes):
    lines[first:last + 1] = new
out = "".join(lines)
before, after = ast.literal_eval(ast.unparse(mutants(src))), ast.literal_eval(ast.unparse(mutants(out)))
assert before == after and list(before) == list(after), "MUTANTS changed"
assert ast.dump(ast.parse(src)).replace(ast.dump(mutants(src)), "") == \
    ast.dump(ast.parse(out)).replace(ast.dump(mutants(out)), ""), "something outside MUTANTS changed"
print(f"{len(changes)} entries re-laid, {len(src.splitlines()) - len(out.splitlines())} lines saved; MUTANTS identical")
for *_lines, name in changes:
    print("  " + name)
if "--write" in sys.argv:
    path.write_text(out)
