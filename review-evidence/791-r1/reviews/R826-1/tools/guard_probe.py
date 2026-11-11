#!/usr/bin/env python3
"""guard_probe.py <clone>: milan_soc.exact_cpu_decode against stand-in VexiiRiscv finalize orders a re-pinned
LiteX could have. For each: whether the guard refuses, and the region list the generator would be handed
(what generate_netlist reads). Nothing is generated; LiteX's naming step is replaced by a recorder."""
import sys
from pathlib import Path
from unittest.mock import patch

clone = Path(sys.argv[1])
sys.path.insert(0, str(clone / 'sw/litex'))
import milan_soc  # noqa: E402
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv  # noqa: E402

WHOLE = [(0x0, 0x38000, 'rxc', 'p'), (0x1000_0000, 0x38000, 'rwxc', 'p'), (0x0100_0000, 0x100_0000, 'rxc', 'p')]


def shape(name, finalize):
    class StandIn(VexiiRiscv):
        def __init__(self):
            pass
        do_finalize = finalize
    cpu = StandIn()
    with patch.object(VexiiRiscv, 'generate_netlist_name', staticmethod(lambda: None)), \
            patch.object(VexiiRiscv, 'memory_regions', [], create=True):
        milan_soc.exact_cpu_decode(cpu)
        try:
            cpu.do_finalize()
            refusal = None
        except RuntimeError as exc:
            refusal = str(exc)
        handed = getattr(cpu, 'generator_regions', VexiiRiscv.memory_regions)
    exact = all(s & (s - 1) == 0 and o % s == 0 for o, s, *_ in handed)
    verdict = 'refused' if refusal else ('built exact' if exact else 'BUILT SINGLE-MASK SILENTLY')
    print(f'{name}: {verdict}; generator handed {[(hex(o), hex(s)) for o, s, *_ in handed]}')


def today(self):
    """LiteX at the pin: collect, then self.generate_netlist_name(), then generate from the class list."""
    VexiiRiscv.memory_regions = list(WHOLE)
    self.generate_netlist_name()


def class_call(self):
    """A re-pin naming through the class instead of the instance."""
    VexiiRiscv.memory_regions = list(WHOLE)
    VexiiRiscv.generate_netlist_name()


def recollect_after_name(self):
    """A re-pin that names first and (re)collects the region list after, e.g. in add_sources."""
    VexiiRiscv.memory_regions = list(WHOLE)
    self.generate_netlist_name()
    VexiiRiscv.memory_regions = list(WHOLE)


def instance_list(self):
    """A re-pin that keeps the list on the instance, which generate_netlist reads."""
    self.generator_regions = list(WHOLE)
    VexiiRiscv.memory_regions = list(WHOLE)
    self.generate_netlist_name()


for n, f in (('pinned order', today), ('class-level naming call', class_call),
             ('list re-collected after naming', recollect_after_name), ('list kept on the instance', instance_list)):
    shape(n, f)
