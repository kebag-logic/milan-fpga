"""Run the production docs check with each expected-failure mutant applied.

usage: python3 -I xfail_real_tree.py <receipts-dir> <tree-copy>
rc 0 for a mutant means the wider rule finds no copy of that form on a real page.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("checker_mutants", Path(sys.argv[1]) / "checker_mutants.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
tree = Path(sys.argv[2])
target = tree / "scripts/check_docs.py"
source = target.read_text(encoding="utf-8")
try:
    for label, (old, new, _) in module.MUTANTS.items():
        if not label.startswith("xfail_"):
            continue
        assert old in source, label
        target.write_text(source.replace(old, new, 1), encoding="utf-8")
        run = subprocess.run([sys.executable, "-B", "scripts/check_docs.py"], cwd=tree, capture_output=True, text=True)
        print(f"{label} rc={run.returncode} | {run.stdout.strip().splitlines()[0]}")
        for line in run.stdout.splitlines()[1:6]:
            print(f"    {line.strip()[:150]}")
finally:
    target.write_text(source, encoding="utf-8")
