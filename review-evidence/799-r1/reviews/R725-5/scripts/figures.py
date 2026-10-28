"""Usage: figures.py <repo> <base> <head>. Prints SUITE_SECONDS and PIECE_SECONDS entries that differ."""
import ast, subprocess, sys
repo, base, head = sys.argv[1:4]
def tables(rev):
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:scripts/suite_shards.py"], capture_output=True, text=True, check=True).stdout
    out = {}
    for node in ast.parse(src).body:
        tgt = node.targets[0] if isinstance(node, ast.Assign) else getattr(node, "target", None)
        if isinstance(tgt, ast.Name) and tgt.id in ("SUITE_SECONDS", "PIECE_SECONDS") and node.value is not None:
            try: out[tgt.id] = ast.literal_eval(node.value)
            except ValueError: out[tgt.id] = None
    return out
a, b = tables(base), tables(head)
for name in ("SUITE_SECONDS", "PIECE_SECONDS"):
    x, y = a.get(name) or {}, b.get(name) or {}
    print(f"{name}: {'unparsed' if b.get(name) is None else 'parsed'}")
    for k in sorted(set(x) | set(y)):
        if x.get(k) != y.get(k): print(f"  {k}: {x.get(k)} -> {y.get(k)}")
