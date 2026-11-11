#!/usr/bin/env python3
"""Probe: the same edge lines under dev 46c971fa's MULTI_DECL_RE, swapped into the head's scan()."""
import importlib.util, re, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cci", repo / "scripts" / "check_cpp_idiom.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.MULTI_DECL_RE = re.compile(
    rf"^[ \t]*{m._DECL_TYPE}[ \t]+\**[A-Za-z_]\w*[^;()\n]*,[^;()\n]*;[ \t]*$", re.M)
for line in ("int a[2][2] = {{1, 2}, {3, 4}}, b = 0;\n", "int a[2][2] = {{1, 2}, {3, 4}};\n",
             "int a = 1, b = 2;\n", "uint32_t x[3] = {1, 2, 3};\n", "int a{1}, b{2};\n",
             "int a = f(1, 2), b;\n"):
    print(repr(line.strip()), m.scan(line)["multi-declarator declaration"])
