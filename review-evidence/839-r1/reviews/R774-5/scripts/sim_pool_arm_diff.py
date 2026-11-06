#!/usr/bin/env python3
"""Print how `make -n run` differs from the sim-pool test's expected leg list.

Usage: sim_pool_arm_diff.py <tree-root> [make-variable=value ...]
"""
import difflib
import importlib.util
import shlex
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("sp", root / "tb/verilator/milan_dp/test_sim_pool.py")
sp = importlib.util.module_from_spec(spec)
sys.modules["sp"] = sp
spec.loader.exec_module(sp)
expected = []
for banner, exe in sp.LEGACY_LEGS:
    if banner is not None:
        expected += ["--banner", banner]
    expected.append(exe)
import subprocess
dry = subprocess.run(["make", "-n", "-C", str(sp.HERE), "run", *sys.argv[2:]], env=sp.clean_env(),
                     capture_output=True, text=True, check=False)
print("make rc", dry.returncode, dry.stderr[:300])
lines = sp.logical_lines(dry.stdout)
at = [k for k, line in enumerate(lines) if "sim_pool.py" in line]
print("runner lines", len(at))
words = shlex.split(lines[at[0]])[4:]
print("legs expected", len(sp.LEGACY_LEGS), "words expected", len(expected), "words got", len(words))
for line in difflib.unified_diff(expected, words, "expected", "make -n", lineterm="", n=1):
    print(line[:200])
