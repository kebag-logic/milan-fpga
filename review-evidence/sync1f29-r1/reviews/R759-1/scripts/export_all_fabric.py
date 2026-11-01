#!/usr/bin/env python3
"""Gateware export (no Vivado) of a tree's five shipped configs, all-fabric, without --build.

usage: export_all_fabric.py <tree> <outroot> [config ...]
The arty configs are exported at 100 MHz as MAILBOX_SPLIT.md "Default build" records, since this LiteX
checkout refuses their 83.333 MHz. Each export is a fresh process with PYTHONHASHSEED=0; rc per config in <outroot>/<cfg>.rc.
"""
import concurrent.futures as cf, os, subprocess, sys
from pathlib import Path

CFGS = ["ax7101_1x1_tdm8", "ax7101_8x8", "arty_4x4", "arty_8ch", "arty_current"]

def run(tree, out, c):
    env = dict(os.environ, PYTHONHASHSEED="0")
    odir = out / c
    odir.mkdir(parents=True, exist_ok=True)
    log = (out / f"{c}.log").open("w")
    cfg = f"configs/endstation_{c}.yaml"
    r = subprocess.run([sys.executable, "sw/builder/endstation_builder.py", cfg], cwd=tree, env=env, stdout=log, stderr=log)
    if r.returncode:
        return c, r.returncode
    code = ("import sys;sys.path.insert(0,'sw/builder');import endstation_builder as eb;"
            f"print(' '.join(eb.emit_soc_argv(eb.load_config('{cfg}'))))")
    argv = subprocess.run([sys.executable, "-c", code], cwd=tree, env=env, capture_output=True, text=True, check=True).stdout.split()
    if c.startswith("arty"):
        argv[argv.index("--sys-clk-freq") + 1] = "100e6"
    cmd = [sys.executable, "sw/litex/milan_soc.py", *argv, "--entity-gen-dir", f"configs/generated/endstation_{c}",
           "--output-dir", str(odir)]
    log.write("CMD " + " ".join(cmd) + "\n"); log.flush()
    r = subprocess.run(cmd, cwd=tree, env=env, stdout=log, stderr=log)
    (out / f"{c}.rc").write_text(f"{r.returncode}\n")
    return c, r.returncode

def main():
    tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    cfgs = sys.argv[3:] or CFGS
    with cf.ThreadPoolExecutor(5) as ex:
        res = list(ex.map(lambda c: run(tree, out, c), cfgs))
    print(res)
    return max(r for _, r in res) != 0

sys.exit(main())
