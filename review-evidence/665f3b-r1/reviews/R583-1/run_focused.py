#!/usr/bin/env python3
"""Run the assigned firmware seams concurrently, retaining each result."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import sys
import traceback

def arm(task):
    repo, packet, name = task
    repo, packet = Path(repo), Path(packet)
    sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
    import ctrl_arms
    import ctrl_build
    import ctrl_reuse
    import fw_gtest
    import srp_arms
    out = packet / "scratch" / name
    out.mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = str(packet / "scratch")
    try:
        ctrl_build.stack_pin()
        ctrl_reuse.cut_reuse(out / "reuse")
        tree = ctrl_build.Tree(ctrl_build.CTRL, out / "build", out / "reuse", fw_gtest.Build(jobs=4))
        if name.startswith("srp"):
            interfaces = int(name[-1])
            test = "test_acmp_mbx.cpp" if "composition" in name else "srp_mbx.cpp"
            result = srp_arms.arm_srp(tree, repo / "third_party/lwSRP", interfaces, test=test)
        else:
            result = getattr(ctrl_arms, "arm_" + name)(tree)
        rc, log = result.rc, result.log
    except Exception:
        rc, log = 2, traceback.format_exc()
    (packet / (name + ".log")).write_text(log)
    (packet / (name + ".rc")).write_text(str(rc) + "\n")
    return {"arm": name, "rc": rc}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--jobs", type=int, default=3)
    args = p.parse_args()
    names = ("adp", "acmp", "acmpif2", "maap", "maap_if2", "srp-composition-1", "srp-composition-2", "srp-unit-2")
    with concurrent.futures.ProcessPoolExecutor(max_workers=min(args.jobs, 3)) as pool:
        futures = [pool.submit(arm, (str(args.repo.resolve()), str(args.packet.resolve()), n)) for n in names]
        results = []
        for f in concurrent.futures.as_completed(futures):
            row = f.result()
            results.append(row)
            print(json.dumps(row), flush=True)
    (args.packet / "focused-results.json").write_text(json.dumps(results, indent=2) + "\n")
    sys.exit(any(r["rc"] for r in results))
