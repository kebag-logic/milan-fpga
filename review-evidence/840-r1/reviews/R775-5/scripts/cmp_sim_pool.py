#!/usr/bin/env python3
"""Compare `make -n run`'s runner words with test_sim_pool.py's LEGACY_LEGS.
usage: cmp_sim_pool.py <milan_dp dir>"""
import importlib.util, os, shlex, subprocess, sys
d = sys.argv[1]
spec = importlib.util.spec_from_file_location("tsp", os.path.join(d, "test_sim_pool.py"))
m = importlib.util.module_from_spec(spec); sys.modules["tsp"] = m; spec.loader.exec_module(m)
exp = []
for b, e in m.LEGACY_LEGS:
    if b is not None: exp += ["--banner", b]
    exp.append(e)
out = subprocess.run(["make", "-n", "-C", d, "run"], env=m.clean_env(), capture_output=True, text=True).stdout
line = [l for l in m.logical_lines(out) if "sim_pool.py" in l][0]
got = shlex.split(line)[4:]
print("expected words", len(exp), "actual words", len(got))
for i, (a, b) in enumerate(zip(exp, got)):
    if a != b: print("first difference at", i, "\n exp:", repr(a), "\n got:", repr(b)); break
else:
    print("common prefix equal; extra expected:", exp[len(got):], "extra actual:", got[len(exp):])
