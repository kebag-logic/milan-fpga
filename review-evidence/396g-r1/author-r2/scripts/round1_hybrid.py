#!/usr/bin/env python3
"""Run the round-2 release test class against the round-1 planner code.

Usage: python3 -I round1_hybrid.py <round-1 planner.py> <round-2 planner.py> <scratch dir>

Writes <scratch>/hybrid.py: the round-1 file with its _ReleaseGateChecks class
replaced by the round-2 class, then runs that file's --self-test. Each round-2
arm that names a fix must fail (FAIL or ERROR) there; the log lists them.
"""
import subprocess
import sys
from pathlib import Path

old_text = Path(sys.argv[1]).read_text()
new_text = Path(sys.argv[2]).read_text()
scratch = Path(sys.argv[3])
start, end = "class _ReleaseGateChecks:", "class _ConcurrencyChecks:"
new_class = new_text[new_text.index(start):new_text.index(end)]
hybrid = old_text[:old_text.index(start)] + new_class + old_text[old_text.index(end):]
scratch.mkdir(parents=True, exist_ok=True)
(scratch / "hybrid.py").write_text(hybrid)
run = subprocess.run([sys.executable, "-B", str(scratch / "hybrid.py"), "--self-test"],
                     capture_output=True, text=True, timeout=900)
lines = run.stderr.splitlines()
names = sorted({line.split()[1] for line in lines if line.startswith(("FAIL: ", "ERROR: "))})
print(f"hybrid self-test rc={run.returncode}")
for name in names:
    kinds = sorted({line.split()[0].rstrip(":") for line in lines
                    if line.startswith(("FAIL: ", "ERROR: ")) and line.split()[1] == name})
    print(f"{'/'.join(kinds)}: {name}")
print(lines[-3] if len(lines) >= 3 else "")
print(lines[-1] if lines else "")
