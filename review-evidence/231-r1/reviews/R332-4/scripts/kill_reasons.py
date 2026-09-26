#!/usr/bin/env python3
"""Reviewer probe: for every mutant in the maintained list, record the final
error line of the failing self-test so a kill by the intended named refusal
can be told apart from a collateral crash.
usage: kill_reasons.py <path/to/syn/ooc>"""
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

ooc = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("m", ooc / "pp_baseline_mutants.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source = (ooc / "pp_baseline.py").read_text()
with tempfile.TemporaryDirectory(prefix="r332-4-kill-") as tmp:
    for index, (name, (old, new)) in enumerate(module.MUTANTS.items()):
        assert source.count(old) == 1, name
        target = Path(tmp) / str(index) / "syn/ooc/pp_baseline.py"
        target.parent.mkdir(parents=True)
        target.write_text(source.replace(old, new))
        r = subprocess.run([sys.executable, "-B", str(target), "--selftest"],
                           capture_output=True, text=True, timeout=120)
        lines = [line for line in r.stderr.splitlines() if line.strip()]
        last = lines[-1] if lines else "(no stderr)"
        print(f"{name}\trc={r.returncode}\t{last}")
