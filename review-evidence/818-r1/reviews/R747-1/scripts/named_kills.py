#!/usr/bin/env python3
"""For each mutant of the reviewed head's mutant tables, apply it to a disposable copy of the gate modules,
run the gate self-test, and record the first failing arm (the AssertionError / arm label that killed it).

usage: named_kills.py <repo> <outdir> <jobs> [table ...]   (tables: SET_MUTANTS MUTANTS POPULATION_MUTANTS ...)
"""
import concurrent.futures, importlib.util, shutil, subprocess, sys, re
from pathlib import Path

repo, out, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
tables = sys.argv[4:] or ["SET_MUTANTS"]
ooc = repo / "syn/ooc"
spec = importlib.util.spec_from_file_location("m", ooc / "pp_resource_gate_mutants.py")
sys.path.insert(0, str(ooc))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
FILES = ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py",
         "pp_resource_gate_set_selftest.py", "pp_placement.py", "pp_placement_selftest.py")
TARGET = {"RANK_MUTANTS": "pp_baseline_rank.py", "PLACEMENT_MUTANTS": "pp_placement.py"}
out.mkdir(parents=True, exist_ok=True)
jobs_list = []
for t in tables:
    for name, change in getattr(m, t).items():
        jobs_list.append((t, name, TARGET.get(t, "pp_resource_gate.py"), change))

def run(job):
    t, name, target, (old, new) = job
    folder = out / "work" / re.sub(r"[^A-Za-z0-9_.-]", "_", f"{t}-{name}")
    folder.mkdir(parents=True)
    for f in FILES:
        shutil.copy2(ooc / f, folder / f)
    src = (folder / target).read_text()
    if src.count(old) != 1:
        return f"{t}\t{name}\tNOT-UNIQUE({src.count(old)})\t"
    (folder / target).write_text(src.replace(old, new))
    r = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                       capture_output=True, text=True, timeout=900)
    text = r.stdout + r.stderr
    killer = ""
    for line in text.splitlines():
        if "AssertionError" in line or line.startswith(("route", "resource gate", "Traceback")) and "PASS" not in line:
            pass
    errs = [l for l in text.splitlines() if l.startswith("AssertionError") or "Error:" in l]
    killer = errs[-1][:300] if errs else text.strip().splitlines()[-1][:300] if text.strip() else ""
    shutil.rmtree(folder)
    return f"{t}\t{name}\trc={r.returncode}\t{killer}"

with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    for line in pool.map(run, jobs_list):
        print(line, flush=True)
