#!/usr/bin/env python3
"""Build and execute co-simulation in an isolated, unpublished source copy."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
compiler = sys.argv[3]
copy = packet / "scratch/cosim-tree"
for rel in ("sw/firmware/ctrl", "sw/firmware/ctrl_nvm", "tb/verilator/mbx", "tb/common", "hdl/milan/mailbox"):
    shutil.copytree(root / rel, copy / rel, ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
env = dict(os.environ, VERILATOR=compiler)
tb = copy / "tb/verilator/mbx"
flags = subprocess.check_output(["make", "-s", "--no-print-directory", "print-vflags"], cwd=tb, env=env, text=True).splitlines()[1:]
flags[flags.index("-j") + 1] = "4"
import shlex
rc = subprocess.call(["make", "-j16", "run-cosim", "VFLAGS=" + shlex.join(flags)], cwd=tb, env=env)
sys.exit(rc)
