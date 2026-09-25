#!/usr/bin/env python3
"""Look for silent textual-merge duplicates in the registries #443 and #541 share.

Usage: check_registry_duplicates.py <clone>
A Python dict literal with a repeated key keeps only the last value, so a
clean textual merge can drop a disposition without any gate noticing.
"""
import ast
import collections
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
src = (root / "scripts/measure_test_evidence.py").read_text()
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant)]
        dup = [k for k, c in collections.Counter(keys).items() if c > 1]
        print(f"dict {names} keys={len(keys)} duplicates={dup}")
for k in ("tb/verilator/milan_dp/render_csr_controls.py", "tb/verilator/crf_rx/mutants.py"):
    print(k, "occurrences:", src.count(f'"{k}"'))
rm = (root / "docs/reference/REGISTER_MAP.md").read_text().splitlines()
print("0x8DC lines:", [i + 1 for i, l in enumerate(rm) if "`0x8DC`" in l])
print("0x738 table rows:", [i + 1 for i, l in enumerate(rm) if l.startswith("| `0x738`")])
sections = collections.Counter(l for l in rm if l.startswith("### "))
print("REGISTER_MAP duplicate section headings:", [h for h, c in sections.items() if c > 1])
t = (root / "docs/testing/TESTING.md").read_text().splitlines()
c = collections.Counter(l for l in t if l.startswith("| "))
print("TESTING.md duplicate table lines:", [k[:80] for k, v in c.items() if v > 1])
cl = (root / "docs/reference/REGISTER_MAP_CLASSES.md").read_text().splitlines()
print("REGISTER_MAP_CLASSES 0x8DC rows:", [i + 1 for i, l in enumerate(cl) if "`0x8DC`" in l])
print("REGISTER_MAP_CLASSES 0x738 rows:", [i + 1 for i, l in enumerate(cl) if "`0x738`" in l])
