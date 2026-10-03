#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: run each of the PR's 25 gate mutants and print WHY its self-test fails.

Usage: probe_pr_mutant_reasons.py <checkout>
"""
import concurrent.futures, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(sys.argv[1]).resolve() / "syn/ooc"
sys.path.insert(0, str(ROOT))
from pp_resource_gate_mutants import MUTANTS  # noqa: E402

def run(item):
    name, (old, new) = item
    src = (ROOT / "pp_resource_gate.py").read_text()
    assert src.count(old) == 1, name
    with tempfile.TemporaryDirectory(prefix="r446-prm-") as tmp:
        d = Path(tmp)
        for s in ("pp_baseline_rank.py", "pp_resource_gate_selftest.py"):
            shutil.copy2(ROOT / s, d / s)
        (d / "pp_resource_gate.py").write_text(src.replace(old, new))
        r = subprocess.run([sys.executable, "-B", str(d / "pp_resource_gate.py"), "--selftest"],
                           capture_output=True, text=True, timeout=300)
        lines = (r.stdout + r.stderr).splitlines()
        err = [l for l in lines if l.startswith(("AssertionError", "KeyError", "TypeError", "ValueError", "IndexError",
                                                 "NameError", "AttributeError"))]
        arm = next((l for l in lines if " arm " in l and "wanted" in l), "")
        return name, r.returncode, (err[-1] if err else "")[:110], arm.strip()[:120]

with concurrent.futures.ThreadPoolExecutor(16) as pool:
    for name, rc, err, arm in pool.map(run, MUTANTS.items()):
        kind = "ARM" if err.startswith("AssertionError") else "CRASH"
        print(f"rc={rc} {kind:<5} {name:<30} | {err} | {arm}")
