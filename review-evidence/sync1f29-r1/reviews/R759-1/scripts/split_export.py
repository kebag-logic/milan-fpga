#!/usr/bin/env python3
"""Export the split placement's SoC of the tree in the cwd, refusing to generate a CPU netlist into the shared install.
usage: split_export.py <config> <elf> <outdir>"""
import runpy, subprocess, sys
from litex.soc.cores.cpu.vexiiriscv import core
cfg, elf, out = sys.argv[1:4]
def refuse(*a, **k):
    raise SystemExit(f"REFUSED: the CPU netlist {core.VexiiRiscv.netlist_name} is not cached; not generating it into the shared install")
core.VexiiRiscv.generate_netlist = staticmethod(refuse)
code = ("import sys;sys.path.insert(0,'sw/builder');import endstation_builder as eb;"
        f"print(' '.join(eb.emit_soc_argv(eb.load_config('{cfg}'))))")
argv = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout.split()
sys.argv = ["sw/litex/milan_soc.py", *argv, "--entity-gen-dir", "configs/generated/" + cfg.split("/")[-1][:-5], "--ctrl-mailbox", "--ctrl-firmware", elf, "--output-dir", out]
sys.path.insert(0, "sw/litex")
runpy.run_path("sw/litex/milan_soc.py", run_name="__main__")
