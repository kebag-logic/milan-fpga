#!/usr/bin/env python3
"""Per-file C++ idiom counts (the parent's check_cpp_idiom.py scan() at dev
57b8c867) for every C++ file the PR touches, at base, at 3407c84 and at head.
Focused on the touched files only; this is not the parent's full gate."""
import importlib.util, os, subprocess, sys
from pathlib import Path
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))  # code_quality_scope.py (parent 57b8c867) beside it
spec = importlib.util.spec_from_file_location("cpp", here / "parent_check_cpp_idiom_57b8c867.py")
cpp = importlib.util.module_from_spec(spec); spec.loader.exec_module(cpp)
clone = sys.argv[1] if len(sys.argv) > 1 else os.environ["CLONE"]
revs = {"base": "c951a9ff0cb5851fb159d33e966e5a2a9a188fe3", "3407c84": "3407c84",
        "head": "b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745"}
files = ["tb/maap/sim_main.cpp", "tb/pp_top/sim_main.cpp", "tb/rx_validator/sim_main.cpp"]
for f in files:
    for name, rev in revs.items():
        src = subprocess.run(["git", "-C", clone, "show", f"{rev}:{f}"], capture_output=True,
                             text=True, check=True).stdout
        counts = {k: v for k, v in cpp.scan(src).items() if v}
        print(f"{f} @{name}: {counts}")
