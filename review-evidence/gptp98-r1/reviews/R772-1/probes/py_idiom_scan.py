#!/usr/bin/env python3
"""Reviewer probe: the parent's check_py_idiom.scan() over one gptp tree.

usage: py_idiom_scan.py <parent check_py_idiom.py> <gptp-tree>
Prints every non-zero finding per module and the totals. The parent script
is loaded from its own path with a stub code_quality_scope module.
"""
import importlib.util
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here / "stub"))
spec = importlib.util.spec_from_file_location("pyidiom", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
tree = Path(sys.argv[2]).resolve()
totals: dict[str, int] = {}
for p in sorted(tree.rglob("*.py")):
    rel = p.relative_to(tree).as_posix()
    counts, sites = mod.scan(p.read_text(errors="replace"), rel)
    for k, v in counts.items():
        totals[k] = totals.get(k, 0) + v
        if v:
            print(f"{rel}: {k} {v}: {sites[k]}")
print("TOTALS", {k: v for k, v in totals.items() if v})
