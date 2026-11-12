#!/usr/bin/env python3
"""Probe check_cpp_idiom.py's multi-declarator rule at the reviewed head.

Usage: python3 -I probe_cpp_multidecl.py <checkout>

Loads <checkout>/scripts/check_cpp_idiom.py as a module, then compares the
head's MULTI_DECL_RE with the base's (46c971fa) pattern on a fixed corpus of
one-line declarations, printing each line's verdict under both. Read-only.
"""
import importlib.util
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cci", root / "scripts" / "check_cpp_idiom.py")
cci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cci)

OLD = re.compile(rf"^[ \t]*{cci._DECL_TYPE}[ \t]+\**[A-Za-z_]\w*[^;()\n]*,[^;()\n]*;[ \t]*$", re.M)
NEW = cci.MULTI_DECL_RE

# (line, how many declarators it really has)
CORPUS = [
    ("uint32_t adp_last_aidx[4] = {0, 0, 0, 0};", 1),
    ("uint32_t a[2] = {0, 0}, b = 1;", 2),
    ("int a{1}, b{2};", 2),
    ("int a, b;", 2),
    ("int a = 1;", 1),
    ("uint32_t m[2][2] = {{0, 0}, {0, 0}};", 1),
    ("uint32_t m[2][2] = {{0, 0}, {0, 0}}, n = 1;", 2),
    ("int n = 1, m[2][2] = {{0, 0}, {0, 0}};", 2),
    ("uint8_t k[3] = {1, 2, 3}, *p = k;", 2),
]
print(f"{'real':>4} {'base':>4} {'head':>4}  line")
for line, real in CORPUS:
    o = 1 if OLD.search(line + "\n") else 0
    n = 1 if NEW.search(line + "\n") else 0
    want = 1 if real > 1 else 0
    tag = "" if n == want else "   <-- head verdict wrong"
    print(f"{real:>4} {o:>4} {n:>4}  {line}{tag}")
