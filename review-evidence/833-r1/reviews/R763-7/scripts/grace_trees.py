#!/usr/bin/env python3
"""Copy <repo>/scripts under <outdir>/<name>/scripts with one mutant applied (review probe).

Usage: python3 grace_trees.py <repo> <outdir> NAME...
NAME is a committed MUTANTS entry, a reviewer entry of r7_mutants.py, or `none`.
"""
import ast
import shutil
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import process_test_support as pts  # noqa: E402

source = (Path(__file__).resolve().parent / "r7_mutants.py").read_text()
scope: dict = {}
exec(compile(ast.parse(source[source.index("OPEN = "):source.index("names = ")]), "r7", "exec"), scope)
for name in sys.argv[3:]:
    changes = pts.MUTANTS[name][2:] if name in pts.MUTANTS else (scope["MINE"][name],)
    root = out / name
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(repo / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = root / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in changes:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    product.write_text(text)
    print(f"{name}: {root}")
