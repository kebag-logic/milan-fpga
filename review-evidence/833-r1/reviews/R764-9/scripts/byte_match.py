#!/usr/bin/env python3
"""byte_match.py CLONE R8DIR: compare each round 8 reviewer edit with MUTANTS at the head, byte for byte.

Only the literal edit tables are evaluated, from the published probe sources, with no imports run."""
import ast, sys
from pathlib import Path
clone, r8 = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / "scripts"))
import process_test_support as pts

def tables(path, names):
    tree, env = ast.parse(path.read_text()), {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in names:
            exec(compile(ast.Module([node], []), str(path), "exec"), {"__builtins__": {}}, env)
    return env

published = {}
t = tables(r8 / "R763-8/r8_mutants.py", {"RESUME", "NEW_TERM", "MINE"})
alias = {"r8-resume-beside-new-live": "resume-beside-new-live",
         "r8-sigterm-trap-command-after-late-grace-resume": "sigterm-trap-command-after-resume-from-1.5s"}
for k, v in t["MINE"].items():
    published[alias[k]] = (v,)
for f in ("R764-8/probes/r764_8_live_probes.py", "R764-8/probes/r764_8_probes.py"):
    for k, v in tables(r8 / f, {"NEW", "PROBES"})["PROBES"].items():
        if k != "none":
            published[k] = tuple(v)
bad = 0
for name, edits in published.items():
    ours = tuple(pts.MUTANTS[name][2:]) if name in pts.MUTANTS else None
    same = ours == tuple(tuple(e) for e in edits)
    bad += not same
    print(f"{'MATCH' if same else 'DIFFER'} {name} -> control {pts.MUTANTS.get(name, ('?',))[0]}")
print(f"{len(published)} published round 8 edits, {len(published) - bad} byte-identical in MUTANTS")
sys.exit(1 if bad else 0)
