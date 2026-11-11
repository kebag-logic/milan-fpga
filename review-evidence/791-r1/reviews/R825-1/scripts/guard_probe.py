#!/usr/bin/env python3
"""guard_probe.py <clone>: disposable probes of milan_soc.exact_cpu_decode and split_soc.CpuPatches 'cover' at
the clone's head, against stand-ins of LiteX's VexiiRiscv finalize in several plausible re-pinned shapes.
Nothing is written to the clone. Prints one PROBE line per case with its observed outcome."""
import sys
from pathlib import Path
from unittest.mock import patch
clone = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(clone / 'sw/litex'), str(clone / 'tb/verilator/ctrl_service_budget')]
import ctrl_memory, milan_soc
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv

ROWS = [(0x0, 0x38000, 'rxc', 'p'), (0x1000_0000, 0x38000, 'rwxc', 'p'), (0x0100_0000, 0x100_0000, 'rxc', 'p'),
        (0x9000_0000, 0x1_0000, 'rw', 'p'), (0x9010_0000, 0x8000, 'rw', 'p'), (0xF000_0000, 0x1_0000, 'rw', 'p')]
PIECES = ctrl_memory.cpu_regions(list(ROWS))

def standin(shape):
    class S(VexiiRiscv):
        def __init__(self): pass
        def do_finalize(self):
            if shape == 'litex-order':          # collect, then self.generate_netlist_name() (pinned LiteX)
                VexiiRiscv.memory_regions = list(ROWS); self.generate_netlist_name()
            elif shape == 'class-call':         # collect, then VexiiRiscv.generate_netlist_name()
                VexiiRiscv.memory_regions = list(ROWS); VexiiRiscv.generate_netlist_name()
            elif shape == 'inline-name':        # collect, then name inline, no naming step
                VexiiRiscv.memory_regions = list(ROWS); VexiiRiscv.netlist_name = 'inline'
            elif shape == 'name-then-collect':  # name first, collect after (reordered)
                VexiiRiscv.memory_regions = []; self.generate_netlist_name(); VexiiRiscv.memory_regions = list(ROWS)
            elif shape == 'name-twice':         # naming step called twice
                VexiiRiscv.memory_regions = list(ROWS); self.generate_netlist_name(); self.generate_netlist_name()
            handed.append(list(VexiiRiscv.memory_regions))
    return S()

for shape in ('litex-order', 'class-call', 'inline-name', 'name-then-collect', 'name-twice'):
    handed = []
    named = []
    with patch.object(VexiiRiscv, 'generate_netlist_name', staticmethod(lambda: named.append(list(VexiiRiscv.memory_regions)))), \
         patch.object(VexiiRiscv, 'memory_regions', [], create=True):
        cpu = standin(shape)
        milan_soc.exact_cpu_decode(cpu)
        try:
            cpu.do_finalize(); refusal = None
        except RuntimeError as e:
            refusal = str(e)
        final = handed[-1] if handed else None
    exact = final is not None and all(s & (s - 1) == 0 and o % s == 0 for o, s, *_ in final)
    print(f'PROBE guard {shape}: refused={bool(refusal)} named_lists={len(named)} '
          f'generator_list_exact={exact} generator_list_is_pieces={final == PIECES}'
          + (f' refusal="{refusal}"' if refusal else ''))

import split_soc
for arm, split, label in (('cover', None, 'shipping split'), ('cover', lambda rows: list(rows), 'split removed'),
                          ('cover', split_soc.power_of_two_cover, 'cover list'), ('as-built', None, 'as-built control')):
    cp = split_soc.CpuPatches(arm)
    if split is not None:
        cp.split = split
    seen = []
    cp.netlist_name = lambda: seen.append(list(VexiiRiscv.memory_regions))
    with patch.object(VexiiRiscv, 'memory_regions', [], create=True):
        VexiiRiscv.memory_regions = cp.split_regions(list(ROWS))
        try:
            cp.generate_netlist_name(); refusal = None
        except RuntimeError as e:
            refusal = str(e)
    print(f'PROBE CpuPatches {arm} / {label}: refused={bool(refusal)} named={len(seen)} '
          f'recorded_soc_regions_whole={cp.soc_regions == [list(r) for r in ROWS]}'
          + (f' refusal="{refusal[:90]}..."' if refusal else ''))
