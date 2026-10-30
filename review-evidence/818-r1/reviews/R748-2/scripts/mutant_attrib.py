#!/usr/bin/env python3
"""Run named mutants of the gate (from the campaign's tables, plus extra JSON edits) and record what kills each.

usage: mutant_attrib.py <syn/ooc dir> <delta.json> <extra.json> <out.tsv>
A mutant is killed by a named arm when the self-test's failure line is an AssertionError naming an arm or check;
any other exception is recorded as such.
"""
import concurrent.futures, importlib.util, json, shutil, subprocess, sys, tempfile
from pathlib import Path
here, delta, extra, out = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), json.loads(Path(sys.argv[3]).read_text()), Path(sys.argv[4])
spec = importlib.util.spec_from_file_location("campaign", here / "pp_resource_gate_mutants.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
table = {}
for group, target in (("POPULATION_MUTANTS", "pp_resource_gate.py"), ("MUTANTS", "pp_resource_gate.py"),
                      ("SET_MUTANTS", "pp_resource_gate.py"), ("RANK_MUTANTS", "pp_baseline_rank.py"),
                      ("PLACEMENT_MUTANTS", "pp_placement.py")):
    for name, change in getattr(mod, group).items():
        table[name] = (target, change)
jobs = [(n, "campaign", *table[n]) for n in [*delta["added"], *delta["rewritten"], "timing fall", "timing fall boundary"]]
jobs += [(e["name"], "extra", e.get("target", "pp_resource_gate.py"), (e["old"], e["new"])) for e in extra]
FILES = ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py",
         "pp_resource_gate_set_selftest.py", "pp_placement.py", "pp_placement_selftest.py")
def run(tmp, name, origin, target, change):
    src = (here / target).read_text(); old, new = change
    if src.count(old) != 1:
        return name, origin, "NOT-UNIQUE", "", ""
    folder = Path(tmp) / name.replace(" ", "_").replace("'", "")
    folder.mkdir()
    for f in FILES: shutil.copy2(here / f, folder / f)
    (folder / target).write_text(src.replace(old, new))
    r = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"], capture_output=True, text=True, timeout=900)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    err = next((l for l in reversed(lines) if l.startswith("AssertionError")), None) or next((l for l in reversed(lines) if l.startswith("pp_resource_gate.Refusal") or "Error:" in l[:60]), lines[-1] if lines else "")
    kind = "arm" if err.startswith("AssertionError") else ("survived" if r.returncode == 0 else "exception")
    return name, origin, str(r.returncode), kind, err[:400]
with tempfile.TemporaryDirectory(prefix="r748-mut-") as tmp, concurrent.futures.ThreadPoolExecutor(16) as pool:
    rows = list(pool.map(lambda j: run(tmp, *j), jobs))
out.write_text("mutant\torigin\trc\tkilled by\tfailing line\n" + "".join("\t".join(r) + "\n" for r in rows))
for r in rows: print("\t".join(r[:4]))
