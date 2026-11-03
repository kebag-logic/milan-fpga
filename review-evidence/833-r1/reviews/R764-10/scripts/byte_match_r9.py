#!/usr/bin/env python3
"""Match the published R763-9 natural mutants' literal edits byte for byte against MUTANTS at the head.

usage: byte_match_r9.py NATURAL.py HEAD_TREE MANIFEST.json
Only the literal assignments TERM, PARENT, LIMIT and MUTANTS are evaluated; nothing else in the probe runs.
"""
import ast, hashlib, json, sys
from pathlib import Path

src = Path(sys.argv[1]).read_bytes()
manifest = json.loads(Path(sys.argv[3]).read_text())
entries = manifest.get("files", manifest) if isinstance(manifest, dict) else manifest
want = None
for e in (entries if isinstance(entries, list) else [dict(path=k, **(v if isinstance(v, dict) else {"sha256": v})) for k, v in entries.items()]):
    if str(e.get("path", "")).endswith("reviews/R763-9/natural.py"):
        want = e
print("natural.py sha256", hashlib.sha256(src).hexdigest(), "manifest entry", want)
ns = {}
for node in ast.parse(src).body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("TERM", "PARENT", "LIMIT", "MUTANTS") for t in node.targets):
        exec(compile(ast.Module([node], []), "natural", "exec"), {"__builtins__": {}}, ns)
sys.path.insert(0, str(Path(sys.argv[2]) / "scripts"))
import process_test_support as pts
for name, edits in ns["MUTANTS"].items():
    head = pts.MUTANTS.get(name)
    print(f"{name}: {'in MUTANTS' if head else 'NOT in MUTANTS'}"
          + (f", edits byte-identical: {list(head[2:]) == [tuple(e) for e in edits]}, control {head[0]}" if head else ""))
