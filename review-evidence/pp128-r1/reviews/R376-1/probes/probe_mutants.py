#!/usr/bin/env python3
"""Run reviewer_probes against named mutants from own_mutants.py.
Usage: probe_mutants.py <exported-tree> <scratch-dir> <receipt> name...
"""
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("om", here.parent / "scripts/own_mutants.py")
om = importlib.util.module_from_spec(spec); spec.loader.exec_module(om)
src, scratch, receipt = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
rtl = Path("hdl/acmp/KL_acmp_talker.sv")
out = []
for name in sys.argv[4:]:
    text = (src / rtl).read_text()
    for old, new in om.MUTANTS[name]:
        assert text.count(old) == 1, name
        text = text.replace(old, new)
    tree = scratch / name
    shutil.rmtree(tree, ignore_errors=True)
    for d in ("hdl", "tb/acmp_talker", "tb/common"):
        shutil.copytree(src / d, tree / d, ignore=shutil.ignore_patterns("obj_dir"))
    (tree / rtl).write_text(text)
    r = subprocess.run([str(here / "run_probes.sh"), str(tree), str(scratch / (name + "-build"))],
                       capture_output=True, text=True, check=False)
    block = f"== {name} (rc={r.returncode})\n" + r.stdout
    print(block, flush=True); out.append(block)
    shutil.rmtree(tree); shutil.rmtree(scratch / (name + "-build"), ignore_errors=True)
receipt.write_text("".join(out))
