#!/usr/bin/env python3
"""Usage: sim_pool_diff.py <milan_dp-dir>: compare `make -n run` runner words with test_sim_pool.LEGACY_LEGS."""
import ast, os, shlex, subprocess, sys
from pathlib import Path
here = Path(sys.argv[1]).resolve()
tree = ast.parse((here / "test_sim_pool.py").read_text())
legs = next(ast.literal_eval(n.value) for n in tree.body
            if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "LEGACY_LEGS")
expected = []
for banner, exe in legs:
    if banner is not None:
        expected += ["--banner", banner]
    expected.append(exe)
env = {k: v for k, v in os.environ.items() if not k.startswith(("MAKE", "MFLAGS", "SIM_JOBS"))}
for extra in ([], ["SIM_JOBS=1"], ["-j8"]):
    dry = subprocess.run(["make", "-n", "-C", str(here), "run", *extra], env=env, capture_output=True, text=True)
    text = dry.stdout.replace("\\\n", " ")
    lines = [l for l in text.splitlines() if "sim_pool.py" in l]
    print("variant", extra, "rc", dry.returncode, "runner lines", len(lines))
    if lines:
        words = shlex.split(lines[0])
        got = words[4:]
        print(" head", words[:4], "n_expected", len(expected), "n_got", len(got))
        for i in range(max(len(got), len(expected))):
            a = expected[i] if i < len(expected) else None
            b = got[i] if i < len(got) else None
            if a != b:
                print("  first diff at", i, "\n   expected:", repr(a), "\n   got     :", repr(b))
                break
        else:
            print("  words identical")
