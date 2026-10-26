#!/usr/bin/env python3
"""Apply one r4_reviewer_mutants.py mutant to a copy of the planner and run the round-3/4 probes on it.

Usage: python3 -I r4_mutant_probe.py <export root> <scripts dir> <work dir> <mutant id> [jobs]

Prints, per probe group, the case names whose status differs from the unmutated planner.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

root, here, work, mid = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
jobs = sys.argv[5] if len(sys.argv) > 5 else "2"
spec = importlib.util.spec_from_file_location("rm", here / "r4_reviewer_mutants.py")
src = (here / "r4_reviewer_mutants.py").read_text()
table = src[src.index("MUTANTS = ("):src.index("\n)\n", src.index("MUTANTS = (")) + 3]
ns = {}
exec(table, ns)
mutant = next(m for m in ns["MUTANTS"] if m[0].startswith(mid + " "))
text = (root / "tb/tools/torture_campaign.py").read_text()
assert text.count(mutant[1]) == 1
for name, tools in (("base", None), ("mut", None)):
    d = work / mid / name / "tb/tools"
    d.mkdir(parents=True, exist_ok=True)
    (d / "torture_campaign.py").write_text(text if name == "base" else text.replace(mutant[1], mutant[2]))
runner = here / "r4_mutant_probe_groups.py"
out = {}
for name in ("base", "mut"):
    r = subprocess.run([sys.executable, "-I", "-B", str(runner), str(work / mid / name / "tb/tools"), str(here), jobs],
                       capture_output=True, text=True, timeout=3000)
    out[name] = dict(line.split(" ", 2)[:2] for line in r.stdout.splitlines() if " " in line and not line.startswith("SUMMARY"))
diff = sorted(k for k in set(out["base"]) | set(out["mut"]) if out["mut"].get(k) != out["base"].get(k))
print(mutant[0], "cases", len(out["base"]), "differ", len(diff))
for k in diff[:12]:
    print("  ", k, out["base"].get(k), "->", out["mut"].get(k))
