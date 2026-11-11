#!/usr/bin/env python3
"""cpupatches_probe.py <clone>: tb/verilator/ctrl_service_budget/split_soc.CpuPatches, each arm, through
milan_soc.exact_cpu_decode on a stand-in VexiiRiscv finalizing in LiteX's order, with the shipping split, with
the split undone (cpu_regions returning its list whole), and with the decode hookup absent. Prints whether the
arm refuses, the rows the generator would be handed, and the SoC regions the arm recorded. Nothing is generated."""
import sys
from pathlib import Path
from unittest.mock import patch

clone = Path(sys.argv[1])
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))
import split_soc  # noqa: E402
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv  # noqa: E402

milan_soc = split_soc.milan_soc
ctrl_memory = milan_soc.ctrl_memory
WHOLE = [(0x0, 0x38000, 'rxc', 'p'), (0x1000_0000, 0x38000, 'rwxc', 'p'), (0x0100_0000, 0x100_0000, 'rxc', 'p'),
         (0x9000_0000, 0x1_0000, 'rw', 'p')]


class StandIn(VexiiRiscv):
    def __init__(self):
        pass

    def do_finalize(self):
        VexiiRiscv.memory_regions = list(WHOLE)
        self.generate_netlist_name()


def one(arm, variant):
    named = []
    with patch.object(VexiiRiscv, 'generate_netlist_name', staticmethod(lambda: named.append(list(VexiiRiscv.memory_regions)))), \
            patch.object(VexiiRiscv, 'memory_regions', [], create=True), \
            (patch.object(ctrl_memory, 'cpu_regions', lambda rows: list(rows)) if variant == 'split undone'
             else patch.object(ctrl_memory, 'cpu_regions', ctrl_memory.cpu_regions)):
        cpu_patches = split_soc.CpuPatches(arm)
        with cpu_patches.applied():
            cpu = StandIn()
            if variant != 'hookup absent':
                milan_soc.exact_cpu_decode(cpu)
            try:
                cpu.do_finalize()
                refusal = None
            except RuntimeError as exc:
                refusal = str(exc)
    handed = named[0] if named else None
    print(f'{arm:8s} | {variant:14s} | {"REFUSED: " + refusal[:90] if refusal else "built"} | handed '
          f'{[(hex(o), hex(s)) for o, s, *_ in handed] if handed else None} | recorded SoC regions '
          f'{[(hex(o), hex(s)) for o, s, *_ in cpu_patches.soc_regions]}')


for arm in ('cover', 'as-built'):
    for variant in ('shipping split', 'split undone', 'hookup absent'):
        one(arm, variant)
