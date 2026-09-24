#!/usr/bin/env python3
"""Split a published literal MUTANTS list into N files of verbatim entries, so each replay fits a bounded command.

usage: split_published_mutants.py PUBLISHED_PY OUT_PREFIX N
"""
import ast, hashlib, pathlib, sys
src, prefix, parts = pathlib.Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
text = src.read_text(encoding="utf-8")
entries = next(ast.literal_eval(n.value) for n in ast.parse(text).body
               if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "MUTANTS" for t in n.targets))
print(f"# {src.name} sha256 {hashlib.sha256(text.encode()).hexdigest()} entries {len(entries)}")
for k in range(parts):
    chunk = entries[k::parts]
    out = pathlib.Path(f"{prefix}-{k}.py")
    out.write_text(f"MUTANTS = {chunk!r}\n", encoding="utf-8")
    print(out.name, len(chunk))
