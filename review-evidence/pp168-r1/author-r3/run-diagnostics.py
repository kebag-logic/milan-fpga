#!/usr/bin/env python3
"""Run unchanged ACMP suites and a focused STOP diagnostic outside the tree."""
import argparse
import os
from pathlib import Path
import subprocess
from concurrent.futures import ThreadPoolExecutor

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
p.add_argument("--scratch", type=Path, required=True)
p.add_argument("--output", type=Path, required=True)
p.add_argument("--compiler", type=Path, required=True)
a = p.parse_args()
env = dict(os.environ, VERILATOR=str(a.compiler))

def run(name, cmd, cwd):
    with (a.output / (name + ".log")).open("w") as log:
        result = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    (a.output / (name + ".rc")).write_text(str(result.returncode) + "\n")
    print(name, "rc", result.returncode, flush=True)
    return result.returncode

def listener():
    work = a.scratch / "listener-diagnostic"
    work.mkdir(parents=True, exist_ok=True)
    if run("listener-rom", ["python3", str(a.repo / "hdl/acmp/rom/gen_ltn_rom.py"), "-o", "ltn_rom.hex"], work):
        return 1
    sources = [a.repo / x for x in ["hdl/common/pp_pkg.sv", "hdl/acmp/pp_acmp_pkg.sv", "hdl/acmp/KL_pp_acmp_listener.sv"]]
    flags = ["--cc", "--exe", "--build", "-j", "16", "--top-module", "KL_pp_acmp_listener",
             "-GSTRM_TIMEOUT_CYC_P=32", "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
             "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM", "-CFLAGS",
             "-std=c++17 -O2 -I" + str(a.repo / "tb/acmp_listener") + " -Wall -Wextra"]
    if run("listener-diagnostic-build", [str(a.compiler), *flags, *map(str, sources),
                str(a.output / "stop-diagnostic.cpp"), "-o", "listener-diagnostic"], work):
        return 1
    binary = str(work / "obj_dir/listener-diagnostic")
    baseline = run("listener-baseline", [binary, "--baseline"], work)
    diagnostic = run("stop-diagnostic", [binary], work)
    return int(baseline != 0 or diagnostic != 1)

def talker():
    work = a.scratch / "talker-baseline"
    work.mkdir(parents=True, exist_ok=True)
    flags = "--cc --exe --build -j 16 --top-module KL_acmp_talker -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS \"-std=c++17 -O2 -Wall -Wextra\""
    return run("talker-baseline", ["make", "-j16", "-f", str(a.repo / "tb/acmp_talker/Makefile"),
               "HDL=" + str(a.repo / "hdl"), "CPP=" + str(a.repo / "tb/acmp_talker/sim_main.cpp"),
               "VFLAGS=" + flags, "run"], work)

with ThreadPoolExecutor(max_workers=2) as pool:
    jobs = [pool.submit(listener), pool.submit(talker)]
    results = [job.result() for job in jobs]
raise SystemExit(any(results))
