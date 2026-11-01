#!/usr/bin/env python3
"""Walk only the docs workflow's register reference step through the CI
command-table walker (the full ci_tool_inventory.py --check needs the CI image).
Usage: CI_IMAGE_SHFMT=<pinned shfmt> python3 -I walk_regref_step.py <tree>"""
import os
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "scripts"))
os.chdir(tree)
import ci_command_table  # noqa: E402

audit = ci_command_table.Audit(tree, {})
audit.shell("python3 scripts/gen_register_reference.py --check\n"
            "python3 scripts/gen_register_reference.py --selftest\n"
            "python3 docs/diagrams/memory_map.gen.py --check\n", ".github/workflows/docs.yml", tree)
print("walked:", sorted(k for k in audit.inputs if "register" in k or "memory_map" in k or "check_doc_style" in k))
print("residue:", sorted(r for r in audit.residue if "register" in r or "memory_map" in r))
print("OK")
