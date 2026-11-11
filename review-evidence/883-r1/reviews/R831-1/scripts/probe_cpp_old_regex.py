#!/usr/bin/env python3
"""Probe: load the head's check_cpp_idiom.py, swap MULTI_DECL_RE back to the
dev 46c971fa pattern, and run the selftest and the tree scan. The new brace
initialiser arm must fail by name; prints the tree's multi-declarator count."""
import importlib.util, re, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cci", repo / "scripts" / "check_cpp_idiom.py")
m = importlib.util.module_from_spec(spec)
sys.argv = [str(repo / "scripts" / "check_cpp_idiom.py")] + sys.argv[2:]
spec.loader.exec_module(m)
m.MULTI_DECL_RE = re.compile(
    rf"^[ \t]*{m._DECL_TYPE}[ \t]+\**[A-Za-z_]\w*[^;()\n]*,[^;()\n]*;[ \t]*$", re.M)
sys.exit(m.main())
