#!/usr/bin/env python3
"""Reviewer probe: the real milan_soc.CtrlMemory with the largest image's sram
banks (65536, 32768, 8192, 4096, 2048: 112,640 B populated).  Every word address
from the populated end to the top of the 224 KiB region, sampled every 1 KiB plus
the last word, must answer err, and a write there must land in no bank.
Usage: probe_region_top.py <repo>"""
import sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path[:0] = [str(repo / "sw/litex")]
from migen import ClockDomain, Module, run_simulation
import ctrl_memory, milan_soc
import test_ctrl_memory as t
banks = (65536, 32768, 8192, 4096, 2048)
class B(Module):
    def __init__(self):
        self.clock_domains.cd_sys = ClockDomain("sys")
        self.submodules.ram = milan_soc.CtrlMemory(ctrl_memory.RAM, banks, None)
b = B()
base = ctrl_memory.RAM.origin // 4
populated = sum(banks) // 4
top = ctrl_memory.RAM.size // 4
probe = sorted(set(range(populated, top, 256)) | {populated, top - 1})
seen = {}
def run():
    seen["w"] = []
    for a in probe:
        seen["w"].append((a, (yield from t.access(b.ram.bus, base + a, we=1, dat=0x5A5A5A5A))))
    seen["lo"] = []
    for a in range(0, populated, 997):
        seen["lo"].append((a, (yield from t.access(b.ram.bus, base + a))))
run_simulation(b, run())
bad = [(hex((a) * 4), r) for a, r in seen["w"] if r[0] != "err"]
alias = [(hex(a * 4), r) for a, r in seen["lo"] if r[1] == 0x5A5A5A5A]
print(f"region top probe: {len(probe)} addresses in [0x{populated*4:x}, 0x{top*4:x}); "
      f"non-err answers: {len(bad)} (first {bad[:3]}); populated words aliased by those writes: {len(alias)} (first {alias[:3]})")
print("RESULT:", "PASS" if not bad and not alias else "FAIL")
sys.exit(0 if not bad and not alias else 1)
