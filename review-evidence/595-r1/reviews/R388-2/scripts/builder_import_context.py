#!/usr/bin/env python3
"""Run gate 40's entry point (test_declaration_contracts) the way the builder
bank reaches it: with test_builder.py's sys.path order (sw/builder, avdecc,
scripts, sw/litex), then `from test_declarations import ...`, and report which
pp_srcs module the derived package read resolved to.
Usage: builder_import_context.py <tree>"""
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
for d in (tree / "sw/builder", tree / "avdecc", tree / "scripts", tree / "sw/litex"):
    sys.path.insert(0, str(d))
from test_declarations import test_declaration_contracts  # noqa: E402
import pp_srcs  # noqa: E402
assert Path(pp_srcs.__file__).resolve() == tree / "scripts/pp_srcs.py", pp_srcs.__file__
test_declaration_contracts()
print(f"OK gate-40 entry via builder import order; pp_srcs from {Path(pp_srcs.__file__).relative_to(tree)}")
