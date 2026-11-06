#!/usr/bin/env python3
"""Diff the words `make -n run` hands sim_pool.py against test_sim_pool.LEGACY_LEGS.
Usage: sim_pool_arm_diff.py <milan_dp dir>"""
import importlib.util, shlex, subprocess, sys
from pathlib import Path
here = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("tsp", here / "test_sim_pool.py")
t = importlib.util.module_from_spec(spec); sys.modules["tsp"] = t; spec.loader.exec_module(t)
exp = []
for banner, exe in t.LEGACY_LEGS:
    if banner is not None: exp += ["--banner", banner]
    exp.append(exe)
for extra in ([], ["SIM_JOBS=1"], ["-j8"], ["NOTIFY_MDIR=obj_notify_custom", "CRFLIC_MDIR=obj_crflic_custom"]):
    d = subprocess.run(["make", "-n", "-C", str(here), "run", *extra], env=t.clean_env(), capture_output=True, text=True)
    lines = t.logical_lines(d.stdout)
    ln = [l for l in lines if "sim_pool.py" in l]
    words = shlex.split(ln[0])[4:] if ln else []
    print("variant", extra or "default", "rc", d.returncode, "words", len(words), "expected", len(exp))
    for i, (a, b) in enumerate(zip(words, exp)):
        if a != b: print("  first difference at", i, "\n   make:", repr(a), "\n   test:", repr(b)); break
    else:
        if len(words) != len(exp): print("  length differs; tail make", words[len(exp):], "tail test", exp[len(words):])
