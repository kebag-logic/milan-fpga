#!/usr/bin/env python3
"""Reviewer probe: does the gate's F2 planted-wire failure name the AXI-Lite bridge?

Usage: probe_f2_bridge.py <repo-root>

The gate's F2 arm requires a forward path whose start is named `fsm_state` and
whose end is a PHY counter `*_cnt`, and labels it "the bridge into the PHY
counter". Both the AXI-Lite-to-Wishbone bridge and LiteSPI's mmap core have an
FSM named `fsm_state`. This splits the planted-wire build's forward paths by
the start's owner: the bridge's own registers, or LiteSPI's core.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw" / "litex"))

from litex.soc.interconnect import axi  # noqa: E402
import test_soc_timing_cuts as gate  # noqa: E402

for label, stage in (("planted wires", gate.WirePHYStage), ("shipping stage", None)):
    soc = gate.build(gate.FlashSoC, None, stage=stage)
    netlist = gate.Netlist(soc.get_fragment())
    bridge = gate.registers(gate.find(soc.bus, axi.AXILite2Wishbone)[0])
    st = soc.spiflash.phy.stage
    stage_regs = gate.registers(st)
    phy = gate.registers(soc.spiflash.phy) - stage_regs
    core = gate.registers(soc.spiflash) - gate.registers(soc.spiflash.phy)
    face = gate.faces(st.phy_sink, True) + gate.faces(st.phy_source, False) + [st.phy_cs]
    index = {s.duid for s in face}
    out = {"bridge": set(), "core": set()}
    for flop in sorted(phy):
        flops, wires = netlist.cone(netlist.signals[flop])
        through = [netlist.signals[d] for d in wires & index]
        starts = set().union(*(netlist.feeding(s) for s in through)) if through else set()
        end = netlist.name(flop)
        if not end.endswith("_cnt"):
            continue
        for who, regs in (("bridge", bridge), ("core", core)):
            for s in starts & regs:
                out[who].add(f"{netlist.name(s)} -> {end}")
    print(f"{label}: into a PHY counter from the AXI-Lite bridge: {sorted(out['bridge'])}")
    print(f"{label}: into a PHY counter from LiteSPI's core: {sorted(out['core'])[:6]}")
print("RESULT: measured")
