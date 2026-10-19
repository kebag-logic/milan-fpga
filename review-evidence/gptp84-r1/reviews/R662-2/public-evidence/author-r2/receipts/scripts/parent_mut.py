#!/usr/bin/env python3
"""Plant one gptp-processor mutant in a disposable scratch parent and run
the gptp_shadow suite (`make run`, suite only) with the companion applied.

usage: parent_mut.py <parent-tree> <patch> <logdir>

Arms: the unmutated control, then each mutant below (exact-text, taken from
the lane's engine mutants.py). Writes <logdir>/<arm>.log and rc.txt; the
tree's gptp-processor and sim_main.cpp are restored afterwards.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ENGINE = "gptp-processor/hdl/top/KL_gptp_engine.sv"
ARMS = [
    ("control", None, None),
    ("no-thisclock",
     "  wire       path_append_w = (ann_pub_count_clamped_w != 4'd0) &&\n"
     "                             (ann_pub_count_clamped_w != 4'd8);\n",
     "  wire       path_append_w = 1'b0;\n"),
    ("appended-source",
     "                    pub_path_r[64*pk +: 64] <= rom_clock_id_w;\n",
     "                    pub_path_r[64*pk +: 64] <= frame_cid_r;\n"),
]


def run(argv, cwd, **kw):
    return subprocess.run(argv, cwd=cwd, check=True, **kw)


def main() -> int:
    tree, patch, logdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    sub = tree / "gptp-processor"
    top = subprocess.run(["git", "-C", str(sub), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert Path(top) == sub.resolve(), top
    logdir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["PATH"] = "<pinned-tools>:" + env["PATH"]
    env["TMPDIR"] = "<scratch>/tmpdir"
    run(["git", "apply", str(patch)], tree)
    try:
        for name, old, new in ARMS:
            run(["git", "checkout", "--", "hdl/top/KL_gptp_engine.sv"], sub)
            if old is not None:
                path = tree / ENGINE
                text = path.read_text()
                assert text.count(old) == 1, name
                path.write_text(text.replace(old, new))
            run(["make", "-C", "tb/verilator/gptp_shadow", "clean"], tree,
                stdout=subprocess.DEVNULL)
            with open(logdir / f"{name}.log", "w", encoding="utf-8") as log:
                rc = subprocess.run(["make", "-C", "tb/verilator/gptp_shadow",
                                     "run", "-j8"], cwd=tree, env=env,
                                    stdout=log, stderr=subprocess.STDOUT).returncode
            with open(logdir / "rc.txt", "a", encoding="utf-8") as f:
                f.write(f"{name} rc={rc}\n")
            print(f"{name} rc={rc}", flush=True)
    finally:
        run(["git", "checkout", "--", "hdl/top/KL_gptp_engine.sv"], sub)
        run(["git", "checkout", "--", "tb/verilator/gptp_shadow/sim_main.cpp"], tree)
        run(["make", "-C", "tb/verilator/gptp_shadow", "clean"], tree,
            stdout=subprocess.DEVNULL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
