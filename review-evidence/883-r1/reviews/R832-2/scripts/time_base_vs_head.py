#!/usr/bin/env python3
"""Time the base (46c971fa) and head multi-declarator patterns on one long
never-matching line. Usage: python3 -I time_base_vs_head.py <checkout>"""
import importlib.util, re, sys, time
from pathlib import Path
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cci", root / "scripts" / "check_cpp_idiom.py")
cci = importlib.util.module_from_spec(spec); spec.loader.exec_module(cci)
OLD = re.compile(rf"^[ \t]*{cci._DECL_TYPE}[ \t]+\**[A-Za-z_]\w*[^;()\n]*,[^;()\n]*;[ \t]*$", re.M)
for n in (2000, 5000):
    line = "int a" + ", x" * n + "\n"
    for name, rx in (("base", OLD), ("head", cci.MULTI_DECL_RE)):
        t = time.perf_counter(); rx.search(line); dt = time.perf_counter() - t
        print(f"n={n} {name} {dt*1000:8.1f} ms")
