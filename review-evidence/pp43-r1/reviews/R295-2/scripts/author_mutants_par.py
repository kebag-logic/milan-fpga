#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reproduce the retained tb/pp_top/gsi_mutants.py verdicts in parallel.

Imports the mutation list from the tree under review (unchanged), gives each
variant its own copy of hdl/, tb/common and tb/pp_top, and applies the
wrapper's own criterion: the build must pass; a mutant is detected only if the
GI run exits 1 with a FAIL line that starts with the named check; golden must
exit 0 with "0 failures". "restored" is a second golden copy (the wrapper
restores in place; separate trees make that step a fresh unmodified copy).
usage: author_mutants_par.py --src <tree> --work <dir> --out <dir>
                             --verilator <path> [--jobs N]
"""
import argparse, importlib.util, json, shutil, subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def run(cmd, cwd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                              check=False, timeout=3600).returncode


def one(a, item):
    name, fn, old, new, count, expected = item
    tree = a.work / name
    shutil.rmtree(tree, ignore_errors=True)
    for d in ("hdl", "tb/common", "tb/pp_top"):
        shutil.copytree(a.src / d, tree / d,
                        ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
    if old:
        p = tree / fn
        s = p.read_text()
        if s.count(old) != count:
            return {"variant": name, "passed": False, "error": "edit-site count"}
        p.write_text(s.replace(old, new))
    bench = tree / "tb/pp_top"
    brc = run(["make", "gsi-build", "VERILATOR=" + a.verilator], bench,
              a.out / f"{name}-build.log")
    if brc != 0:
        return {"variant": name, "build_rc": brc, "passed": False}
    log = a.out / f"{name}-run.log"
    rrc = run(["./obj_dir/Vpp_top_sim", "--gsi-internal-only"], bench, log)
    text = log.read_text()
    named = [l for l in text.splitlines() if expected and l.startswith("FAIL: " + expected)]
    complete = "[build default," in text
    passed = complete and ((rrc == 1 and bool(named)) if expected
                           else (rrc == 0 and "0 failures" in text))
    tally = [l for l in text.splitlines() if l.startswith("[build default")]
    return {"variant": name, "build_rc": brc, "run_rc": rrc, "tally": tally,
            "named_failures": named[:3], "passed": passed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location(
        "gsi_mutants", a.src / "tb/pp_top/gsi_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    items = ([("golden", "", "", "", 0, "")] + list(mod.mutations())
             + [("restored", "", "", "", 0, "")])
    with ThreadPoolExecutor(max_workers=min(a.jobs, 8)) as ex:
        res = list(ex.map(lambda i: one(a, i), items))
    for r in res:
        print(json.dumps(r), flush=True)
    (a.out / "results.json").write_text(json.dumps(res, indent=2) + "\n")
    print(f"{sum(r['passed'] for r in res)}/{len(res)} verdicts as required")


if __name__ == "__main__":
    main()
