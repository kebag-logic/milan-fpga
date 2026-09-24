#!/usr/bin/env python3
"""Build and run the milan_dp legs of the suite's own `run` recipe on a tree.

The build and run commands are taken from `make -n run` in the suite
directory, so every leg is elaborated with exactly the flags the recipe uses;
nothing is re-typed here. Prerequisite generators run first, sequentially.
Builds then run with bounded parallelism (--par, each verilator build with
VERILATOR_JOBS=--vjobs), and the built binaries run with the same bound. The
render mutation campaign (`python3 render_mutants.py`) is excluded unless
--with-render-mutants is given.

Every leg's build and run output is written to <out>/<leg>.build.log and
<out>/<leg>.run.log, and <out>/LEGS.txt records per leg: build exit, run
exit, the harness's own `checks: N failures: M` line (or the last RESULT
line), and the sha256 of milan_datapath.sv and sim_nxn.cpp it was built from.

Usage:
  run_milan_dp_legs.py --suite <tree>/tb/verilator/milan_dp --out <dir>
      [--legs obj_nxn,obj_notify,...] [--par 4] [--vjobs 2]
      [--dp-src <path>] [--with-render-mutants]
"""
import argparse
import concurrent.futures as cf
import hashlib
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def joined_lines(text: str) -> list[str]:
    out, cur = [], ""
    for line in text.splitlines():
        if line.endswith("\\"):
            cur += line[:-1] + " "
            continue
        cur += line
        out.append(cur.strip())
        cur = ""
    if cur:
        out.append(cur.strip())
    return [l for l in out if l]


def mdir_of(cmd: str) -> str:
    m = re.search(r"--Mdir\s+(\S+)", cmd)
    return m.group(1) if m else "obj_dir"


def tally(log: str) -> str:
    m = re.findall(r"checks:\s*(\d+)\s+failures:\s*(\d+)", log)
    r = re.findall(r"RESULT:\s*(\w+)", log)
    parts = []
    if m:
        parts.append("checks %s failures %s" % m[-1])
    if r:
        parts.append("RESULT %s" % r[-1])
    if not parts:
        tail = [l for l in log.splitlines() if l.strip()][-1:] or ["<no output>"]
        parts.append("last: " + tail[0][:160])
    return "; ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--legs", default="")
    ap.add_argument("--par", type=int, default=4)
    ap.add_argument("--vjobs", type=int, default=2)
    ap.add_argument("--dp-src", default="")
    ap.add_argument("--with-render-mutants", action="store_true")
    a = ap.parse_args()
    suite = Path(a.suite).resolve()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    make_vars = ["VERILATOR_JOBS=%d" % a.vjobs]
    if a.dp_src:
        make_vars.append("DP_SRC=%s" % a.dp_src)
    dry = subprocess.run(["make", "-n", "run"] + make_vars, cwd=suite, env=env,
                         capture_output=True, text=True)
    (out / "make-n-run.txt").write_text(dry.stdout + dry.stderr)
    if dry.returncode != 0:
        print("make -n run failed", file=sys.stderr)
        return 2
    cmds = joined_lines(dry.stdout)
    prereq, builds, runs = [], {}, {}
    for c in cmds:
        if c.startswith("verilator "):
            builds[mdir_of(c)] = c
        elif c.startswith("./obj_"):
            runs[c.split("/")[1]] = c
        elif c.startswith("python3 render_mutants.py"):
            if a.with_render_mutants:
                runs["render_mutants"] = c
        elif c.startswith("python3 ") or c.startswith("sha256sum"):
            prereq.append(c)
    want = [l for l in a.legs.split(",") if l] or sorted(builds)
    dp = Path(a.dp_src) if a.dp_src else suite / "../../../hdl/milan/milan_datapath.sv"
    ident = "milan_datapath.sv sha256 %s; sim_nxn.cpp sha256 %s; sim_main.cpp sha256 %s" % (
        sha(dp.resolve()), sha(suite / "sim_nxn.cpp"), sha(suite / "sim_main.cpp"))
    vv = subprocess.run(["verilator", "--version"], capture_output=True, text=True, env=env).stdout.strip()
    with (out / "LEGS.txt").open("w") as f:
        f.write("suite %s\n%s\nverilator %s\nlegs %s\n" % (suite, ident, vv, ",".join(want)))
    for c in prereq:
        p = subprocess.run(c, shell=True, cwd=suite, env=env, capture_output=True, text=True)  # noqa: S602 - recipe line from make -n
        with (out / "prereq.log").open("a") as f:
            f.write("$ %s\n%s%sexit=%d\n" % (c, p.stdout, p.stderr, p.returncode))
        if p.returncode != 0:
            print("prerequisite failed: " + c, file=sys.stderr)
            return 2

    def build(leg: str):
        t0 = time.time()
        p = subprocess.run(builds[leg], shell=True, cwd=suite, env=env,  # noqa: S602
                           capture_output=True, text=True)
        (out / ("%s.build.log" % leg)).write_text("$ %s\n%s%sexit=%d\n" % (builds[leg], p.stdout, p.stderr, p.returncode))
        return leg, p.returncode, time.time() - t0

    def run(leg: str):
        t0 = time.time()
        p = subprocess.run(runs[leg], shell=True, cwd=suite, env=env,  # noqa: S602
                           capture_output=True, text=True)
        (out / ("%s.run.log" % leg)).write_text("$ %s\n%s%sexit=%d\n" % (runs[leg], p.stdout, p.stderr, p.returncode))
        return leg, p.returncode, time.time() - t0, tally(p.stdout)

    bres = {}
    with cf.ThreadPoolExecutor(max_workers=a.par) as ex:
        for leg, rc, dt in ex.map(build, [l for l in want if l in builds]):
            bres[leg] = (rc, dt)
    rres = {}
    runnable = [l for l in want if l in runs and bres.get(l, (1,))[0] == 0]
    if "render_mutants" in runs:
        runnable.append("render_mutants")
    with cf.ThreadPoolExecutor(max_workers=a.par) as ex:
        for leg, rc, dt, t in ex.map(run, runnable):
            rres[leg] = (rc, dt, t)
    with (out / "LEGS.txt").open("a") as f:
        f.write("%-16s %-8s %-10s %-8s %-10s %s\n" % ("leg", "build", "build_s", "run", "run_s", "tally"))
        for leg in want + (["render_mutants"] if "render_mutants" in runs else []):
            b = bres.get(leg, ("-", 0))
            r = rres.get(leg, ("NOT RUN", 0, ""))
            f.write("%-16s %-8s %-10.0f %-8s %-10.0f %s\n" % (leg, b[0], b[1], r[0], r[1], r[2]))
    print((out / "LEGS.txt").read_text())
    bad = [l for l in want if bres.get(l, (1,))[0] != 0 or rres.get(l, (1,))[0] != 0]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
