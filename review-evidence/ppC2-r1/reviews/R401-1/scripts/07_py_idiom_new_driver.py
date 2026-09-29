#!/usr/bin/env python3
"""The parent's check_py_idiom.py scan() (dev 57b8c867) on the PR's new
tb/maap/mutants.py at head. Focused on the one new Python file only."""
import importlib.util, os, subprocess, sys
from pathlib import Path
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
spec = importlib.util.spec_from_file_location("py", here / "parent_check_py_idiom_57b8c867.py")
py = importlib.util.module_from_spec(spec); spec.loader.exec_module(py)
clone = sys.argv[1] if len(sys.argv) > 1 else os.environ["CLONE"]
src = subprocess.run(["git", "-C", clone, "show", "b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745:tb/maap/mutants.py"],
                     capture_output=True, text=True, check=True).stdout
counts, sites = py.scan(src, "protocol-processor/tb/maap/mutants.py")
print("tb/maap/mutants.py @head:", {k: v for k, v in dict(counts).items() if v}, dict(sites) if any(dict(counts).values()) else "")
