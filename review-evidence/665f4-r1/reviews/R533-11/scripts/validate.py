#!/usr/bin/env python3
"""Focused round-11 controls. Run from the candidate root; products stay in scratch."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

PACKET = Path(__file__).resolve().parents[1]
ROOT = Path.cwd().resolve()
SCRATCH = PACKET / "scratch"
RECEIPTS = PACKET / "receipts"

def worker(interfaces, jobs):
    sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
    import srp_arms
    import srp_mutants
    import fw_gtest
    from ctrl_build import Tree, CTRL
    out = SCRATCH / f"focused-if{interfaces}"
    build = fw_gtest.Build(jobs=jobs)
    tree = Tree(CTRL, out / "build", out / "reuse", build)
    failures = []
    for suite in ("test_acmp_mbx.cpp", "srp_app.cpp", "srp_mbx.cpp", "srp_rx_retry.cpp", "srp_walk.cpp"):
        result = srp_arms.arm_srp(tree, ROOT / "third_party/lwSRP", interfaces, test=suite)
        print(result.log, flush=True)
        if result.rc: failures.append(suite)
    sanitized = Tree(CTRL, out / "asan", out / "asan-reuse",
                     fw_gtest.Build(jobs=jobs, address_sanitizer=True))
    result = srp_arms.arm_srp(sanitized, ROOT / "third_party/lwSRP", interfaces,
                            test=("test_acmp_mbx.cpp", "SrpBinding.*:SrpFeedback.*"))
    print("SANITIZED COMPOSITION", result.log, flush=True)
    if result.rc: failures.append("sanitized-composition")
    selected = tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(("feedback-", "r10-")))
    srp_mutants.DEFECTS = selected
    if srp_mutants.campaign(out / "mutants", ROOT / "third_party/lwSRP", jobs, interfaces):
        failures.append("mutants")
    for log in (out / "mutants").glob("*.log"):
        (RECEIPTS / f"if{interfaces}-{log.name}").write_text(log.read_text())
    print(json.dumps({"interfaces": interfaces, "plants": len(selected), "failures": failures}), flush=True)
    return bool(failures)

def run_one(name, argv):
    start = time.monotonic()
    with (RECEIPTS / f"{name}.log").open("w") as log:
        rc = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT).returncode
    (RECEIPTS / f"{name}.rc").write_text(str(rc) + "\n")
    return {"name": name, "argv": argv, "rc": rc, "seconds": round(time.monotonic()-start, 3)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", type=int)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["TMPDIR"] = str(SCRATCH)
    if args.worker:
        return worker(args.worker, args.jobs)
    tasks = [(f"focused-if{n}", [sys.executable, "-B", str(Path(__file__).resolve()),
              "--worker", str(n), "--jobs", str(args.jobs)]) for n in (1, 2)]
    tasks.append(("coverage", [sys.executable, "-B", "sw/firmware/gtest/fw_coverage.py",
                  "--check", "--jobs", str(args.jobs), "--keep", str(SCRATCH / "coverage")]))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda t: run_one(*t), tasks))
    (RECEIPTS / "validation.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return int(any(r["rc"] for r in results))

if __name__ == "__main__":
    raise SystemExit(main())
