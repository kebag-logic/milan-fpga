#!/usr/bin/env python3
"""List string constants in parent mutant drivers that match the processor tree
at the OLD pin but not at the NEW pin. Usage: anchor_delta.py <repo> <old> <new>
Every candidate string is a Python constant of at least 16 characters in a file
whose name holds 'mutant'; a string found at the old pin and absent, or found a
different number of times, at the new pin is an anchor the adoption moved."""
import ast, pathlib, subprocess, sys
repo, old, new = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
pp = repo / "protocol-processor"
def tree(rev):
    names = subprocess.run(["git", "-C", str(pp), "ls-tree", "-r", "--name-only", rev, "hdl", "tb"],
                           capture_output=True, text=True, check=True).stdout.split()
    out = {}
    for n in names:
        if n.endswith((".sv", ".svh", ".py", ".cpp", ".h", ".v")):
            b = subprocess.run(["git", "-C", str(pp), "show", f"{rev}:{n}"], capture_output=True, check=True).stdout
            out[n] = b.decode("utf-8", "replace")
    return out
o, n = tree(old), tree(new)
total = moved = 0
files = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, check=True).stdout.split()
for f in files:
    if "mutant" not in f or not f.endswith(".py") or f.startswith("protocol-processor"):
        continue
    t = ast.parse((repo / f).read_text())
    for node in ast.walk(t):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) >= 16:
            s = node.value
            co = sum(v.count(s) for v in o.values())
            if co == 0:
                continue
            total += 1
            cn = sum(v.count(s) for v in n.values())
            if cn != co:
                moved += 1
                print(f"{f}:{node.lineno}: old {co}, new {cn}: {s[:100]!r}")
print(f"{total} strings found in the old-pin processor tree, {moved} changed count at the new pin")
