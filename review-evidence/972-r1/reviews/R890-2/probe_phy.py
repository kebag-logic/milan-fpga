#!/usr/bin/env python3
"""Run the current platform suite against current and prior PHY code in disposable trees."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import os
import shutil
import subprocess
import sys

def run_one(root, out, label, rev):
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
    import fw_gtest
    import plat_arms
    from ctrl_build import Tree
    from ctrl_reuse import cut_reuse
    work = out / "scratch" / ("probe-" + label)
    src = work / "ctrl"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(root / "sw/firmware/ctrl", src, ignore=shutil.ignore_patterns("__pycache__"))
    source = subprocess.check_output(["git", "--no-replace-objects", "-C", str(root), "show",
                                      rev + ":sw/firmware/ctrl/plat/ctrl_plat_phy.c"])
    (src / "plat/ctrl_plat_phy.c").write_bytes(source)
    tree = Tree(src, work / "build", work / "reuse", fw_gtest.Build(jobs=8))
    cut_reuse(tree.reuse)
    result = plat_arms.arm_platboot(tree, 1)
    log = f"Suite from 77a74b2f; PHY source {rev}; jobs 8\n" + result.log
    # Public receipts use neutral placeholders for the disposable workspace.
    log = log.replace(str(out), "<packet>").replace(str(root), "<review-clone>")
    (out / ("phy-" + label + ".log")).write_text(log)
    (out / ("phy-" + label + ".rc")).write_text(str(result.rc) + "\n")
    print(label, "rc", result.rc, flush=True)
    return label, result.rc, log

def main():
    root = Path(sys.argv[1]).resolve()
    out = Path(__file__).resolve().parent
    with ProcessPoolExecutor(max_workers=2) as pool:
        work = [pool.submit(run_one, root, out, label, rev) for label, rev in
                [("head", "77a74b2f4e289c5a5a89687e07a6925cfedf6860"),
                 ("prior", "0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b")]]
        results = [f.result() for f in work]
    for label, rc, log in results:
        if label == "head":
            assert rc == 0, "current platform suite failed"
        else:
            assert rc == 1 and "[FAIL] PlatPhy.P22" in log and "[FAIL] PlatPhy.P23" in log, "prior defects not detected"
    print("PASS: current platform suite passes; prior PHY fails P22 and P23.")

if __name__ == "__main__":
    main()
