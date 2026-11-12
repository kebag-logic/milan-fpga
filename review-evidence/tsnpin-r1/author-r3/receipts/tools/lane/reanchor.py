"""Replace the old/new text of named Mutant(...) entries with the stack's own plants of the same name at the new pin."""
import ast, json, sys
from pathlib import Path
stack = {p["name"]: p for p in json.load(open(sys.argv[1]))}
names = set(sys.argv[3].split(","))
path = Path(sys.argv[2]); src = path.read_text(); lines = src.splitlines(keepends=True)
offs = [0]
for l in lines: offs.append(offs[-1] + len(l))
def split_long(piece, room):
    """Split one line piece at spaces so each part's literal fits in room columns."""
    out, cur = [], ""
    for word in piece.split(" "):
        cand = word if not cur else cur + " " + word
        if cur and len(json.dumps(cand + " ")) > room:
            out.append(cur + " "); cur = word
        else:
            cur = cand
    out.append(cur)
    return out
def lit(s, col, wrapped=False):
    """A double-quoted Python literal of s, split at newlines to stay within 120 columns at column col."""
    parts, cur = [], ""
    for chunk in s.split("\n")[:-1]:
        piece = chunk + "\n"
        cand = cur + piece
        if cur and col + 2 + len(json.dumps(cand)) > 119:
            parts.append(cur); cur = piece
        else:
            cur = cand
    tail = s.split("\n")[-1]
    if tail:
        cand = cur + tail
        if cur and col + 2 + len(json.dumps(cand)) > 119:
            parts.append(cur); cur = tail
        else:
            cur = cand
    if cur: parts.append(cur)
    room = 119 - col - 2
    fine = []
    for p in parts:
        fine.extend(split_long(p, room) if len(json.dumps(p)) > room else [p])
    enc = [json.dumps(p) for p in fine]
    if len(enc) == 1: return enc[0]
    if wrapped: return ("\n" + " " * col).join(enc)
    return "(" + ("\n" + " " * (col + 1)).join(enc) + ")"
edits = []
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "Mutant" and isinstance(node.args[0], ast.Constant) \
            and node.args[0].value in names:
        p = stack[node.args[0].value]
        for idx, key in ((2, "old"), (3, "new")):
            a = node.args[idx]
            start = offs[a.lineno - 1] + a.col_offset; end = offs[a.end_lineno - 1] + a.end_col_offset
            wrapped = src[:start].rstrip().endswith("(") and src[end:].lstrip().startswith(")")
            edits.append((start, end, lit(p[key], a.col_offset, wrapped), node.args[0].value, key))
done = {e[3] for e in edits}
assert done == names, sorted(names - done)
for start, end, text, n, k in sorted(edits, reverse=True):
    src = src[:start] + text + src[end:]
path.write_text(src)
print(path.name, "rewrote", sorted(done))
