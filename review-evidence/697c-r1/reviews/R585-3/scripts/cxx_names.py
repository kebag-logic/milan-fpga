#!/usr/bin/env python3
"""Every C++-suffixed name ctrl_configs.cxx_sources reads from the builders that resolves under none of its
bases (so its C++ source is never followed), and the firmware units it judges as C++.
Usage: cxx_names.py <checkout> <work>"""
import ast, sys
from pathlib import Path
co, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(co / "sw/firmware/ctrl/test")); sys.path.insert(0, str(co / "sw/firmware/gtest"))
import ctrl_configs as c, ctrl_boundary as b
for path, text in c.builder_texts().items():
    if path.suffix == ".py":
        names = [n.value for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Constant) and
                 isinstance(n.value, str) and n.value.endswith(c.CXX_SUFFIXES) and not n.value.split()[1:]]
    else:
        names = [w for w in text.replace("\\\n", " ").split() if w.endswith(c.CXX_SUFFIXES)]
    for name in names:
        hits = [base for base in (path.parent, c.HERE, c.STACK, c.ROOT, c.PP)
                if ((base / name.removeprefix(c.STACK_PREFIX)) if base == c.STACK else (base / name)).is_file()]
        if not hits:
            alt = [p for p in (c.CTRL / name, c.ROOT / "sw/firmware" / name) if p.is_file()]
            print(f"UNRESOLVED {c.rel(path)}: {name!r}" + (f"  (exists as {c.rel(alt[0])})" if alt else ""))
units, unfollowed = b.cxx_units(b.Trees(c.CTRL, c.STACK), work)
print("C++ UNITS", len(units)); [print("  ", u.relative_to(c.CTRL)) for u in units]
print("UNFOLLOWED", unfollowed)
