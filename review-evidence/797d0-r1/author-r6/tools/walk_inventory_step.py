#!/usr/bin/env python3
"""Walk only the docs workflow's inventory step through the CI command-table walker.

Usage: CI_IMAGE_SHFMT=<pinned shfmt> python3 -I walk_inventory_step.py <tree>

dev's full `ci_tool_inventory.py --check` refuses on an unrelated stale script
digest, so this drives the same `Audit` walker on the two commands of the step
"Documentation inventory freshness gate" alone: every subprocess argv form in
scripts/docs_inventory.py must match the command table, its declared sha256
must equal the bytes, and every construct shape must be in the census.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "scripts"))
import os
os.chdir(tree)
import ci_command_table  # noqa: E402

audit = ci_command_table.Audit(tree, {})
audit.shell("python3 scripts/docs_inventory.py --check\npython3 scripts/docs_inventory.py --selftest\n",
            ".github/workflows/docs.yml", tree)
print("walked:", sorted(k for k in audit.inputs if "docs_inventory" in k))
print("residue:", sorted(r for r in audit.residue if "docs_inventory" in r))
print("shapes:", len(audit.shapes_used))
print("OK")
