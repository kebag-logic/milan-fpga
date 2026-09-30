#!/usr/bin/env python3
"""Reviewer chunk runner for tb/pp_top/acmp_mutants.py (exact head a9ce0fa2).

Imports the author's driver from --root and calls its own judge() so the
KILLED/SURVIVED rule is the driver's, but lets a reviewer run goldens and
mutants in separate foreground calls. Records append to OUTPUT/records.jsonl.
Extra reviewer mutants (edits given as JSON) use the same judge().

  run_acmp_mutants_chunk.py --root TREE --output DIR --verilator V
        (--golden SUITE_DIR ... | --only LABEL ... | --extra FILE.json) [--jobs N]
"""
import argparse, concurrent.futures, importlib.util, json, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--root", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True)
ap.add_argument("--verilator", required=True)
ap.add_argument("--golden", nargs="*", default=[])
ap.add_argument("--only", nargs="*", default=[])
ap.add_argument("--extra", type=Path)
ap.add_argument("--jobs", type=int, default=1)
a = ap.parse_args()
spec = importlib.util.spec_from_file_location("am", a.root / "tb/pp_top/acmp_mutants.py")
am = importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
out = a.output.resolve(); out.mkdir(parents=True, exist_ok=True)
work = (a.root.resolve(), out, a.verilator)
suites = {m.suite.directory: m.suite for m in am.MUTANTS}
jobs = []
for d in a.golden:
    jobs.append(("golden-" + Path(d).name, suites[d], (), ()))
for m in am.MUTANTS:
    if am.label_of(m) in a.only:
        jobs.append((am.label_of(m), m.suite, m.edits, m.checks))
if a.extra:
    for x in json.loads(a.extra.read_text()):
        jobs.append((x["label"], suites[x["suite"]],
                     tuple(tuple(e) for e in x["edits"]), tuple(x["checks"])))
missing = set(a.only) - {j[0] for j in jobs}
if missing:
    sys.exit(f"unknown labels: {sorted(missing)}")
with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as pool:
    futs = [pool.submit(am.judge, *j, work) for j in jobs]
    recs = [f.result() for f in futs]
with (out / "records.jsonl").open("a") as s:
    for r in recs:
        s.write(json.dumps(r) + "\n")
for r in recs:
    print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "run_rc", "missing")}),
          "failing:", len(r.get("failing_checks", [])))
sys.exit(0 if all(r["verdict"] in ("PASS", "KILLED") for r in recs) else 1)
