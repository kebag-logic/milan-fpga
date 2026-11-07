#!/usr/bin/env python3
"""Re-pin scripts/docs_inventory.py in ci/image/command-table.json with the table's own helpers.

usage: repin848.py <repository root>
No script writes this digest; earlier lanes changed that one line. This uses the table's hash and serializer,
and refuses unless the result differs from the old file in exactly one line.
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
sys.dont_write_bytecode = True
import ci_command_table  # noqa: E402
import ci_tool_inventory  # noqa: E402

table_path = root / ci_command_table.TABLE
before = table_path.read_text(encoding="utf-8")
table = json.loads(before)
if ci_tool_inventory.serialized(table) != before:
    raise SystemExit("the table does not round-trip through its serializer before the edit")
entry = table["scripts"]["scripts/docs_inventory.py"]
old = entry["sha256"]
new = ci_command_table.sha256(root / "scripts/docs_inventory.py")
entry["sha256"] = new
after = ci_tool_inventory.serialized(table)
changed = [n for n, (a, b) in enumerate(zip(before.split("\n"), after.split("\n")), 1) if a != b]
if len(before.split("\n")) != len(after.split("\n")) or len(changed) != (0 if old == new else 1):
    raise SystemExit(f"expected one changed line, got {changed}")
table_path.write_text(after, encoding="utf-8")
print(f"old {old}\nnew {new}\nchanged lines {changed}")
