#!/usr/bin/env python3
"""Run `yosys_sweep.py shapes` IN MEMORY with the sweep source taken from a
given commit of the review clone (git show REV:syn/resmap/yosys_sweep.py),
compiled under the clone's own path, against a given plan and work dir. The
clone's files are never written.
Usage: shapes_probe_rev.py <clone> <rev> <plan.json> <work>"""
import importlib.util
import subprocess
import sys
from pathlib import Path

clone, rev, plan, work = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], sys.argv[4]
path = clone / "syn/resmap/yosys_sweep.py"
source = subprocess.run(["git", "-C", str(clone), "show", f"{rev}:syn/resmap/yosys_sweep.py"],
                        capture_output=True, text=True, check=True).stdout
sys.path.insert(0, str(path.parent))
spec = importlib.util.spec_from_file_location(path.stem, path)
module = importlib.util.module_from_spec(spec)
sys.modules[path.stem] = module
exec(compile(source, str(path), "exec"), module.__dict__)
sys.argv = [str(path), "--plan", plan, "--work", work, "shapes"]
try:
    rc = module.main()
except SystemExit as exc:
    rc = exc.code
print(f"SHAPES rc={rc} (sweep source {rev})")
