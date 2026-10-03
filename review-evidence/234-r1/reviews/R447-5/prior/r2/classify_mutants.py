#!/usr/bin/env python3
"""Classify how each shipped resource-gate mutant is killed.

Usage: classify_mutants.py <repo checkout> <scratch dir> [jobs]
Applies each MUTANTS entry of syn/ooc/pp_resource_gate_mutants.py exactly as
the shipped campaign does, runs the mutated gate's --selftest, and classifies
the failure by its final exception:
  ARM      an arm's expect() assertion on a wrong exit status or report text
  ESCAPED  an arm's assertion whose report is an exception the gate let escape
  CRASH    any other exception or a non-AssertionError exit (import, syntax...)
  SURVIVED the self-test still exited 0
"""
import concurrent.futures
import importlib.util
import re
from pathlib import Path
import shutil
import subprocess
import sys

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 16
here = repo / "syn/ooc"
spec = importlib.util.spec_from_file_location("campaign", here / "pp_resource_gate_mutants.py")
campaign = importlib.util.module_from_spec(spec)
spec.loader.exec_module(campaign)
source = (here / "pp_resource_gate.py").read_text()
shutil.rmtree(scratch, ignore_errors=True)


def run(item):
    name, change = item
    folder = scratch / name.replace(" ", "_")
    folder.mkdir(parents=True)
    for sibling in ("pp_baseline_rank.py", "pp_resource_gate_selftest.py"):
        shutil.copy2(here / sibling, folder / sibling)
    if change is None:
        changed = source
    else:
        old, new = change
        assert source.count(old) == 1, name
        changed = source.replace(old, new)
    (folder / "pp_resource_gate.py").write_text(changed)
    result = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                            capture_output=True, text=True, timeout=300)
    err = result.stderr.strip().splitlines()
    tail = err[max((i for i, line in enumerate(err) if line.startswith("Traceback")), default=0):]
    final = next((line for line in tail if re.match(r"^[A-Za-z_.]*(Error|Exception|Exit)\b", line)), "")
    escaped = any("escaped " in line for line in tail)
    first_arm = final
    if result.returncode == 0:
        kind = "SURVIVED"
    elif final.startswith("AssertionError") and escaped:
        kind = "ESCAPED"
    elif final.startswith("AssertionError"):
        kind = "ARM"
    else:
        kind = "CRASH"
    return name, result.returncode, kind, first_arm[:200]


items = [("control", None), *campaign.MUTANTS.items()]
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    rows = list(pool.map(run, items))
counts = {}
for name, rc, kind, why in rows:
    if name == "control":
        kind = "CONTROL-PASS" if rc == 0 else "CONTROL-FAIL"
    counts[kind] = counts.get(kind, 0) + 1
    print(f"{kind:9} rc={rc} {name}: {why}")
print("summary:", ", ".join(f"{k} {v}" for k, v in sorted(counts.items())), f"of {len(campaign.MUTANTS)} mutants")
shutil.rmtree(scratch, ignore_errors=True)
