#!/usr/bin/env python3
"""Print the parent idiom gates' findings, with line and detail, for the named files.

Usage: sites.py PARENT FILE...  (FILE relative to PARENT; .py and .cpp/.h)
Uses the parent's own scan functions, so the sites are exactly what its gates count.
"""
import importlib
import sys
from pathlib import Path

parent = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(parent / "scripts"))
py = importlib.import_module("check_py_idiom")
cpp = importlib.import_module("check_cpp_idiom")

for rel in sys.argv[2:]:
    text = (parent / rel).read_text()
    if rel.endswith(".py"):
        counts, sites = py.scan(text, rel)
        for key, found in sites.items():
            for lineno, detail in found:
                print(f"{rel}:{lineno}: {key}: {detail}")
        print(f"{rel}: {len(text.splitlines())} lines; nonzero "
              f"{ {k: v for k, v in counts.items() if v} }")
    else:
        code = cpp.blank_non_code(text)
        for item in cpp.long_functions(code):
            print(f"{rel}: long function: {item}")
