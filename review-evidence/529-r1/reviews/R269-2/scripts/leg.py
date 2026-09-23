#!/usr/bin/env python3
"""Build and run one tb/verilator/milan_dp sim_nxn leg from the suite's own recipe.

The recipe is taken from `make -n run` in the suite directory, so the flags are the
Makefile's and not a second copy. Only three things are overridden, each through a
variable the Makefile itself exposes or through the object directory:
  DP_SRC          the datapath source (a mutated copy for a probe, else the tree's)
  VERILATOR_JOBS  C++ build parallelism
  --Mdir          an absolute object directory, so probes never share one

usage: leg.py TREE LEG MDIR LOG [--dp-src PATH] [--jobs N] [--keep]
  LEG is one of nxn, nxndv, nxn8, nxn4c, notify.
Exit status: 0 when the harness exits 0, 1 when it exits non-zero, 2 when the
build fails. The object directory is removed afterwards unless --keep is given.
Environment: VERILATOR names the simulator executable.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time


def recipe(suite, leg, dp_src, jobs, verilator):
    out = subprocess.run(
        ["make", "-n", "run", f"VERILATOR={verilator}", f"VERILATOR_JOBS={jobs}",
         f"DP_SRC={dp_src}"],
        cwd=suite, capture_output=True, text=True, check=True).stdout
    joined = out.replace("\\\n", " ")
    hits = [ln for ln in joined.splitlines()
            if f"--Mdir obj_{leg} " in ln and ln.rstrip().endswith(f"-o Vmilan_dp_{leg}")]
    if len(hits) != 1:
        raise SystemExit(f"expected one recipe for {leg}, found {len(hits)}")
    return hits[0]


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree")
    ap.add_argument("leg", choices=["nxn", "nxndv", "nxn8", "nxn4c", "notify"])
    ap.add_argument("mdir")
    ap.add_argument("log")
    ap.add_argument("--dp-src", default=None)
    ap.add_argument("--jobs", default="1")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    verilator = os.environ.get("VERILATOR", "verilator")
    suite = os.path.join(a.tree, "tb", "verilator", "milan_dp")
    dp = a.dp_src or os.path.join(a.tree, "hdl", "milan", "milan_datapath.sv")
    dp = os.path.abspath(dp)
    mdir = os.path.abspath(a.mdir)
    cmd = recipe(suite, a.leg, dp, a.jobs, verilator)
    cmd = cmd.replace(f"--Mdir obj_{a.leg} ", f"--Mdir {mdir} ", 1)
    os.makedirs(mdir, exist_ok=True)
    hdr = [f"leg={a.leg}", f"datapath_sha256={sha(dp)}",
           f"harness_sha256={sha(os.path.join(suite, 'sim_nxn.cpp'))}",
           f"crf_rx_sha256={sha(os.path.join(a.tree, 'hdl/ieee1722/crf/KL_crf_rx.sv'))}"]
    t0 = time.time()
    with open(a.log + ".build", "w") as bl:
        rc_b = subprocess.run(cmd, shell=True, cwd=suite, stdout=bl,
                              stderr=subprocess.STDOUT).returncode
    t1 = time.time()
    if rc_b != 0:
        with open(a.log, "w") as lg:
            lg.write("\n".join(hdr) + f"\nbuild_exit={rc_b}\nBUILD FAILED\n")
        if not a.keep:
            shutil.rmtree(mdir, ignore_errors=True)
        return 2
    exe = os.path.join(mdir, f"Vmilan_dp_{a.leg}")
    with open(a.log, "w") as lg:
        lg.write("\n".join(hdr) + f"\nbuild_exit=0 build_s={t1 - t0:.0f}\n")
        lg.flush()
        rc = subprocess.run([exe], cwd=suite, stdout=lg,
                            stderr=subprocess.STDOUT).returncode
    t2 = time.time()
    with open(a.log, "a") as lg:
        lg.write(f"\nrun_exit={rc} run_s={t2 - t1:.0f}\n")
    if not a.keep:
        shutil.rmtree(mdir, ignore_errors=True)
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
