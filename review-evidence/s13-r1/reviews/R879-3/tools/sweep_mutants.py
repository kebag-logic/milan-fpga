#!/usr/bin/env python3
"""Reviewer mutants of syn/resmap/soc_sweep.py's prepare()/command_export() wiring, each run through --selftest from
an untracked sibling copy (so the module's own directory and plan are used), removed afterwards.
Usage: python3 -I sweep_mutants.py <repo>"""
import subprocess, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
src = (repo / "syn/resmap/soc_sweep.py").read_text()
probe = repo / "syn/resmap/_r879_probe_soc_sweep.py"
MUTANTS = [
    ("control: unmodified", None, None),
    ("A: command_export hard-codes all-fabric instead of reading the plan",
     "    base = prepare(work, plan_placement(plan))", "    base = prepare(work, \"all-fabric\")"),
    ("B: command_export writes under soc/ before prepare()",
     "    base = prepare(work, plan_placement(plan))",
     "    (work / \"soc\").mkdir(parents=True, exist_ok=True)\n    base = prepare(work, plan_placement(plan))"),
    ("C: prepare drops --entity-gen-dir",
     "    return [*params[\"argv\"], \"--entity-gen-dir\", str(tree / \"configs/generated\" / yosys_sweep.BASE_CONFIG)]",
     "    return [*params[\"argv\"]]"),
    ("D: prepare refuses but names no image",
     "name platform image(s) {missing} that the", "name platform image(s) that the"),
    ("E: prepare checks images against the builder output, not the export tree",
     "    missing = missing_images(params[\"argv\"], tree)", "    missing = missing_images(params[\"argv\"], out)"),
    ("F: prepare asks the builder for a fixed all-fabric",
     "                    \"--placement\", placement], cwd=tree", "                    \"--placement\", \"all-fabric\"], cwd=tree"),
    ("G: prepare skips git_listable",
     "    git_listable(tree)\n", "    pass\n"),
]
caught = 0
results = []
for label, old, new in MUTANTS:
    text = src if old is None else src.replace(old, new, 1)
    if old is not None and text == src:
        results.append(f"== {label}: PLANT DID NOT APPLY"); continue
    probe.write_text(text)
    r = subprocess.run([sys.executable, "-B", str(probe), "--selftest"], cwd=repo, capture_output=True, text=True)
    fails = [l for l in (r.stdout + r.stderr).splitlines() if "FAILED" in l or "Error" in l]
    verdict = ("PASS (control)" if r.returncode == 0 else "control FAILED") if old is None else \
              ("CAUGHT" if r.returncode != 0 else "SURVIVED")
    caught += old is not None and r.returncode != 0
    results.append(f"== {label}: exit {r.returncode}: {verdict}")
    results += [f"   {l[:240]}" for l in fails[:3]]
probe.unlink()
print("\n".join(results))
print(f"mutants caught: {caught} of {len(MUTANTS) - 1}")
