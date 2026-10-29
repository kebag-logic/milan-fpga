#!/usr/bin/env python3
"""Reviewer probe: print what LiteX hashes into the VexiiRiscv netlist name for the split boot SoC's export, and
stop before any generation (nothing is written into the LiteX tree).

usage (the product LiteX interpreter): r733_netlist_inputs.py CHECKOUT BUILD_DIR SHAPE ELF N_IF
"""
import sys
from pathlib import Path

checkout, build_dir, shape, elf, n_if = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), int(
    sys.argv[5])
sys.path.insert(0, str(checkout / "tb/verilator/ctrl_split_boot"))
import boot_soc  # noqa: E402
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv  # noqa: E402


class Stop(Exception):
    pass


def dump() -> None:
    print("NETLIST", VexiiRiscv.netlist_name)
    for k, v in vars(VexiiRiscv.soc_args).items():
        print("SOC_ARG", k, repr(v))
    for name in ("reset_address", "litedram_width", "xlen", "memory_regions", "vexii_args", "with_opensbi",
                 "with_supervisor"):
        print("FIELD", name, repr(getattr(VexiiRiscv, name, None)))
    raise Stop()


VexiiRiscv.generate_netlist = staticmethod(dump)
try:
    boot_soc.build(build_dir, shape, elf, n_if)
except Stop:
    pass
