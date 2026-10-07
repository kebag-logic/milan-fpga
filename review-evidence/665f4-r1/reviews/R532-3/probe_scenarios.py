#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run srp_probe.cpp against the exact head and against reviewer plants.

Usage: probe_scenarios.py --repo <checkout at the head> --out <scratch dir>
The head tree is exported with `git archive HEAD` into <out>/tree; the checkout's
own lwSRP submodule (verified at the pin by the harness) is used read-only.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from probe_srp import REVIEWER, failing  # noqa: E402

PLANTS = {n: (o, w) for n, o, w, _ in REVIEWER}
SELECT = ["head", "RP3-declared-only-from-replaced-slot", "RP5-withdraw-domain-vid-on-unbind",
          "RP10-declared-inheritance-any-stream"]


def one(job):
    name, tree, lwsrp, out = job
    tree, out = Path(tree), Path(out)
    sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
    sys.path.insert(0, str(tree / "sw/firmware/gtest"))
    import ctrl_build, fw_gtest, srp_arms  # noqa: E401
    work = out / "work" / name
    shutil.rmtree(work, ignore_errors=True)
    src = work / "ctrl"
    shutil.copytree(tree / "sw/firmware/ctrl", src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    if name != "head":
        old, new = PLANTS[name]
        p = src / "srp/srp_mbx.c"
        t = p.read_text()
        assert t.count(old) == 1, name
        p.write_text(t.replace(old, new))
    rows = []
    for nif in (1, 2):
        b = fw_gtest.Build(jobs=2)
        try:
            res = srp_arms.arm_srp(ctrl_build.Tree(src, work / f"b{nif}", work / f"r{nif}", b), Path(lwsrp), nif,
                                   test=("srp_probe.cpp", "*"))
        except Exception as e:  # a refusal class is not importable in the parent
            rows.append({"if": nif, "refusal": f"{type(e).__name__}: {e}"[:4000]})
            continue
        (out / "logs").mkdir(parents=True, exist_ok=True)
        (out / "logs" / f"{name}-if{nif}.log").write_text(res.log)
        rows.append({"if": nif, "rc": res.rc, "failing": [f for f in failing(res.log) if "." in f]})
    shutil.rmtree(work, ignore_errors=True)
    return {"name": name, "rows": rows}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    repo, out = a.repo.resolve(), a.out.resolve()
    tree = out / "tree"
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    arc = subprocess.run(["git", "-C", str(repo), "archive", "HEAD"], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tree)], input=arc, check=True)
    for sub in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
        (tree / sub).rmdir()
        (tree / sub).symlink_to(repo / sub)  # read-only use of the checked-out pins
    shutil.copyfile(HERE / "srp_probe.cpp", tree / "sw/firmware/ctrl/test/srp_probe.cpp")
    jobs = [(n, str(tree), str(repo / "third_party/lwSRP"), str(out)) for n in SELECT]
    results = []
    with ProcessPoolExecutor(4) as pool:
        for r in pool.map(one, jobs):
            results.append(r)
            print(json.dumps(r), flush=True)
    (out / "results-scenarios.json").write_text(json.dumps(results, indent=1))
    shutil.rmtree(tree, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
