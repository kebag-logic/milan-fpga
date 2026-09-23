#!/usr/bin/env python3
"""Build and run one milan_dp leg with the suite's own `run` recipe line.

usage: leg.py <suite_dir> <recipe.txt> <leg> <log> [--dp <datapath.sv>]
              [--harness <sim_nxn copy in suite_dir>] [--mdir <dir>]

<recipe.txt> is `make -n run VERILATOR_JOBS=8` captured in <suite_dir>.
Only the datapath source, the harness file and the object directory are
substituted; every flag, shape and -G/-D comes from the recipe line.
Writes the build and run output to <log> and prints the tally line.
"""
import argparse
import hashlib
import os
import re
import shlex
import subprocess
import sys

LEGS = {  # leg -> (Mdir in the recipe, binary)
    "main": ("obj_dir", "Vmilan_dp_sim"),
    "nxn": ("obj_nxn", "Vmilan_dp_nxn"),
    "nxndv": ("obj_nxndv", "Vmilan_dp_nxndv"),
    "nxn8": ("obj_nxn8", "Vmilan_dp_nxn8"),
    "nxn4c": ("obj_nxn4c", "Vmilan_dp_nxn4c"),
    "notify": ("obj_notify", "Vmilan_dp_notify"),
}
DP_REL = "../../../hdl/milan/milan_datapath.sv"


def recipe_lines(path):
    """The recipe with backslash continuations joined."""
    out, cur = [], ""
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.endswith("\\"):
                cur += line[:-1] + " "
                continue
            out.append(cur + line)
            cur = ""
    return out


def pick(lines, leg):
    mdir, binary = LEGS[leg]
    for line in lines:
        if not line.startswith("verilator ") or f"-o {binary}" not in line:
            continue
        m = re.search(r"--Mdir (\S+)", line)
        if (m.group(1) if m else "obj_dir") == mdir:
            return line
    sys.exit(f"no recipe line for {leg}")


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("suite")
    ap.add_argument("recipe")
    ap.add_argument("leg", choices=sorted(LEGS))
    ap.add_argument("log")
    ap.add_argument("--dp")
    ap.add_argument("--harness")
    ap.add_argument("--mdir")
    a = ap.parse_args()

    line = pick(recipe_lines(a.recipe), a.leg)
    toks = shlex.split(line)
    mdir, binary = LEGS[a.leg]
    dp = a.dp or os.path.join(a.suite, DP_REL)
    harness = "sim_main.cpp" if a.leg == "main" else "sim_nxn.cpp"
    if a.dp:
        toks = [a.dp if t == DP_REL else t for t in toks]
    if a.harness:
        toks = [a.harness if t == harness else t for t in toks]
        harness = a.harness
    if a.mdir:
        if "--Mdir" in toks:
            toks[toks.index("--Mdir") + 1] = a.mdir
        else:
            toks[1:1] = ["--Mdir", a.mdir]
        mdir = a.mdir

    with open(a.log, "w", encoding="utf-8") as log:
        log.write(f"leg: {a.leg}\n")
        log.write(f"datapath: {os.path.abspath(dp)} sha256 {sha(dp)}\n")
        hp = os.path.join(a.suite, harness)
        log.write(f"harness: {os.path.abspath(hp)} sha256 {sha(hp)}\n")
        log.write(f"build: {shlex.join(toks)}\n")
        log.flush()
        b = subprocess.run(toks, cwd=a.suite, stdout=log, stderr=subprocess.STDOUT)
        log.write(f"build exit: {b.returncode}\n")
        if b.returncode != 0:
            print(f"{a.leg}: BUILD FAILED ({b.returncode})")
            return 2
        log.flush()
        r = subprocess.run([os.path.join(mdir, binary)], cwd=a.suite,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True)
        log.write(r.stdout)
        log.write(f"run exit: {r.returncode}\n")
    tally = [ln for ln in r.stdout.splitlines()
             if re.search(r"checks: \d+|\d+ checks, \d+ failures", ln)]
    fails = [ln for ln in r.stdout.splitlines() if "[FAIL]" in ln]
    print(f"{a.leg}: run exit {r.returncode}; {len(fails)} [FAIL] lines; "
          f"last: {tally[-1].strip() if tally else '(no tally line)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
