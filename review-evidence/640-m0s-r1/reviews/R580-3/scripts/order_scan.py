#!/usr/bin/env python3
"""List every gate invocation in Python sources whose literal command word is followed by an option.

Usage: python3 -I order_scan.py <repo-root>
Scans calls to cli(...), main([...]) and *.main([...]) and any list/tuple literal beginning with a
"check"/"record" string. Reports option-before-directory orders, and prints every inspected site so a
reader can audit what was covered. Exit 0 = no option-first site found, 1 = at least one found.
"""
import ast
import sys
from pathlib import Path

root = Path(sys.argv[1])
bad = 0
sites = 0
for path in sorted(root.glob("syn/**/*.py")) + sorted(root.glob("scripts/**/*.py")):
    try:
        tree = ast.parse(path.read_text(), str(path))
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        seqs = []
        if isinstance(node, ast.Call):
            seqs.append(node.args)
        if isinstance(node, (ast.List, ast.Tuple)):
            seqs.append(node.elts)
        for seq in seqs:
            if not seq or not isinstance(seq[0], ast.Constant) or seq[0].value not in ("check", "record"):
                continue
            if len(seq) < 2:
                continue
            sites += 1
            second = seq[1]
            option_first = isinstance(second, ast.Constant) and isinstance(second.value, str) \
                and second.value.startswith("--")
            text = ast.get_source_segment(path.read_text(), node) or ""
            tag = "OPTION-FIRST" if option_first else "ok"
            if option_first:
                bad += 1
            print(f"{tag}\t{path.relative_to(root)}:{node.lineno}\t{text[:110]!r}")
print(f"sites {sites} option-first {bad}")
sys.exit(1 if bad else 0)
