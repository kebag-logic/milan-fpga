#!/usr/bin/env python3
"""Run R435-2's r2_plants.py PLANTS (its table, read-only) on TREE and print,
for each, the failing test names (r2_plants.py prints only its last lines)."""
import importlib.util, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
spec = importlib.util.spec_from_file_location("p435", "$REVIEWS/ppC8-r435-2-packet/scripts/r2_plants.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
def run(plant):
    name, rel, old, new, what = plant
    copy = work / name; shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(tree / "hdl/aecp/desc", copy / "hdl/aecp/desc")
    shutil.copytree(tree / "tb/desc_store", copy / "tb/desc_store", ignore=shutil.ignore_patterns("obj_dir"))
    text = (copy / rel).read_text(encoding="utf-8")
    if text.count(old) != 1: return f"{name} INVALID"
    (copy / rel).write_text(text.replace(old, new), encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"], cwd=copy / "tb/desc_store", capture_output=True, text=True)
    fails = sorted({l.split(" (__main__")[0] + (" " + l.split(") (")[1].rstrip(")") if ") (" in l else "") for l in r.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))})
    shutil.rmtree(copy)
    return f"{name} {'KILLED' if r.returncode else 'SURVIVED'} {fails[:3]}"
with ThreadPoolExecutor(12) as pool:
    for line in pool.map(run, p.PLANTS): print(line)
