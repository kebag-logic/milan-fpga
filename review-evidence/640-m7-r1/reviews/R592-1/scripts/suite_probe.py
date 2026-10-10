#!/usr/bin/env python3
"""Run existing suites on private copies of the tree, unmutated or with one
reviewer-planted defect, in parallel.

Usage: python3 -I suite_probe.py <repo> <workdir> <jobs>
Needs `verilator` (5.050) on PATH. The repository is only read: each job
copies the working tree (without .git) into <workdir>/<job>.
"""
import concurrent.futures as cf
import re
import shutil
import subprocess
import sys
from pathlib import Path

RET = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
WRITE_AT_HEAD = (RET, "      res_ns_r  [res_tail_w] <= res_ns_w;",
                 "      res_ns_r  [res_head_r] <= res_ns_w;")

# (job, suite directory, make target, mutation or None)
JOBS = [
    ("gptp_shadow_head", "tb/verilator/gptp_shadow", "run", None),
    ("gptp_txts_head", "tb/verilator/gptp_txts", "run", None),
    ("gptp_plane_head", "tb/verilator/gptp_plane", "run", None),
    ("gptp_shadow_res_write_at_head", "tb/verilator/gptp_shadow", "run",
     WRITE_AT_HEAD),
    ("gptp_txts_res_write_at_head", "tb/verilator/gptp_txts", "run",
     WRITE_AT_HEAD),
]
TALLY = re.compile(r"checks: *(\d+) +failures: *(\d+)")


def job(repo: Path, work: Path, spec) -> str:
    name, suite, target, mut = spec
    root = work / name
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(repo, root, symlinks=True,
                    ignore=shutil.ignore_patterns(".git", "obj_dir",
                                                  "gptp_ucode.hex"))
    if mut is not None:
        rel, old, new = mut
        path = root / rel
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            return f"{name}: ANCHOR count {text.count(old)}"
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
    proc = subprocess.run(["make", "-s", target, "VERILATOR_JOBS=2"],
                          cwd=root / suite, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    (work / f"{name}.log").write_text(out, encoding="utf-8")
    tallies = TALLY.findall(out)
    fails = [l.strip() for l in out.splitlines()
             if l.strip().startswith("[FAIL]")][:6]
    shutil.rmtree(root)
    return (f"{name}: make rc {proc.returncode}; tallies {tallies[-3:]}; "
            f"first failures {fails}")


def main() -> int:
    repo, work, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    work.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=jobs) as pool:
        for line in pool.map(lambda s: job(repo, work, s), JOBS):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
