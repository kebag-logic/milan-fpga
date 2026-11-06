#!/usr/bin/env python3
"""Apply the parent's check_cpp_idiom.scan() rules to the C++ files this PR touches."""
import importlib.util, pathlib, subprocess, sys
import sys; sys.path.insert(0, sys.argv[1].rsplit("/",1)[0])
gate, tree, base = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
spec = importlib.util.spec_from_file_location("cpp_gate", gate)
m = importlib.util.module_from_spec(spec); sys.modules["cpp_gate"] = m; spec.loader.exec_module(m)
names = subprocess.run(["git", "-C", str(tree), "diff", "--name-only", base, "HEAD"], text=True, capture_output=True, check=True).stdout.split()
bad = 0
for n in names:
    if not n.endswith((".cpp", ".hpp", ".h", ".c")): continue
    c = m.scan((tree / n).read_text(errors="replace"), "protocol-processor/" + n)
    nz = {k: v for k, v in c.items() if v}
    print(n, nz or "all rules 0"); bad += bool(nz)
print("files with a count:", bad)
