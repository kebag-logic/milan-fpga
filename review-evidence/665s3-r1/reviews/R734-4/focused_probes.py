#!/usr/bin/env python3
"""Focused platform baselines and three fault controls, all builds in scratch."""
import concurrent.futures, os, pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build, ctrl_mutants, plat_arms, fw_gtest
scratch = out / "scratch/probes"
scratch.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(scratch)

def probe(name):
    work = scratch / name
    work.mkdir(parents=True, exist_ok=True)
    build = fw_gtest.Build(jobs=4)
    mutation = next((m for m in ctrl_mutants.MUTANTS if m.name == name), None)
    if mutation:
        src, stack = ctrl_mutants.plant(mutation, work)
    else:
        src, stack = ctrl_build.CTRL, ctrl_build.STACK
    tree = ctrl_build.Tree(src, work / "build", work / "reuse", build, stack)
    if name in ("console-baseline", "plat-command-read-past-its-end"):
        result = plat_arms.arm_plat(tree)
    else:
        result = plat_arms.arm_platboot(tree, 2 if name == "boot-if2-baseline" else 1)
    (out / (name + ".log")).write_text(result.log)
    (out / (name + ".rc")).write_text(str(result.rc) + "\n")
    ok = ctrl_mutants.caught(mutation.test, mutation.needle, result) if mutation else result.rc == 0
    print(name, "PASS" if ok else "FAIL", "arm rc", result.rc, flush=True)
    return ok

baseline = ["console-baseline", "boot-if1-baseline", "boot-if2-baseline"]
plants = ["plat-command-read-past-its-end", "plat-saved-state-after-mailbox-open", "plat-store-service-unbound"]
results = []
for names in (baseline, plants):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results.extend(pool.map(probe, names))
raise SystemExit(0 if all(results) else 1)
