#!/usr/bin/env python3
"""Emit the retained crossings of one milan_soc tree as Verilog, through both
emitters, for byte comparison across commits.

Usage: pinned_py.sh probe_emit.py <sw/litex dir of a tree> <out dir>

For each bench (MAC TX, MAC RX, CSR) writes <bench>.<emitter>.v with the
emitter's timestamp/comment header lines removed. MAC crossings come from a
real MilanMAC; the CSR crossing from `_cross_csr_bus` when the tree has it,
else from LiteX's AXILiteClockDomainCrossing exactly as the base tree's
add_milan_datapath built it inline. Every endpoint field is a port.
"""
import re
import sys
from pathlib import Path

soc_dir, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(soc_dir))
import milan_soc  # noqa: E402
assert Path(milan_soc.__file__).resolve().parent == soc_dir

from migen import ClockDomain, Module  # noqa: E402
from litex.soc.interconnect import axi  # noqa: E402

DOMAINS = ("sys", "milan", "macsys", "macdp")


def bench_of(build):
    m = Module()
    for name in DOMAINS:
        setattr(m, f"cd_{name}", ClockDomain(name))
        m.clock_domains += getattr(m, f"cd_{name}")
    endpoints = build(m)
    ios = set()
    for name in DOMAINS:
        cd = getattr(m, f"cd_{name}")
        ios |= {cd.clk, cd.rst}
    for ep in endpoints:
        ios |= {ep.valid, ep.ready, ep.first, ep.last}
        ios |= {s for s, _ in ep.payload.iter_flat()}
    return m, ios


def mac(which):
    def build(m):
        mac_ = milan_soc.MilanMAC(milan_soc.alinx_ax7101.Platform(),
                                  data_width=64, milan_cd="milan")
        cdc = getattr(mac_, which)
        m.submodules.dut = cdc
        return [cdc.sink, cdc.source]
    return build


def csr(m):
    master = axi.AXILiteInterface(data_width=32, address_width=32)
    if hasattr(milan_soc, "_cross_csr_bus"):
        slave = milan_soc._cross_csr_bus(m, master, "milan")
    else:
        slave = axi.AXILiteInterface(data_width=32, address_width=32)
        m.submodules.milan_axil_cdc = axi.AXILiteClockDomainCrossing(
            master, slave, cd_from="sys", cd_to="milan")
    return [getattr(i, c) for i in (master, slave) for c in ("aw", "w", "b", "ar", "r")]


HEADER = re.compile(r"^//.*(Auto-Generated|Date|Migen|LiteX|Copyright|----).*$", re.M)
for emitter in ("migen", "litex"):
    for name, build in (("mac_tx", mac("mac_tx_cdc")), ("mac_rx", mac("mac_rx_cdc")),
                        ("csr", csr)):
        m, ios = bench_of(build)
        if emitter == "migen":
            from migen.fhdl.verilog import convert
        else:
            from litex.gen.fhdl.verilog import convert
        text = str(convert(m, ios=ios, name="bench"))
        text = HEADER.sub("", text)
        (out / f"{name}.{emitter}.v").write_text(text)
        print(f"{name}.{emitter}.v {len(text)} bytes")
