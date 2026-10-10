#!/usr/bin/env python3
# Reviewer probe (R590-1, #640 lane M2). Emit Verilog for a harness that holds
# only the seven retained crossings, built by one tree's own milan_soc code,
# with every endpoint field on a top-level port (nothing trimmed).
#
#   xing_harness.py <tree>/sw/litex <out.v> base|head
#
# base: `_axis_dp_cdc` for the MAC crossings and LiteX's AXILiteClockDomainCrossing
#       built inline exactly as add_milan_datapath did at the base.
# head: the same plus `_payload_in_block_ram` on both MAC crossings, and
#       `_cross_csr_bus` for the CSR crossing.
import sys
from pathlib import Path

soc_dir, out, mode = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(soc_dir))
import milan_soc as soc  # noqa: E402
assert Path(soc.__file__).resolve().parent == soc_dir.resolve(), soc.__file__

from migen import ClockDomain, Module, Signal  # noqa: E402
from litex.gen import LiteXModule  # noqa: E402
from litex.gen.fhdl.verilog import convert  # noqa: E402
from litex.soc.interconnect import axi  # noqa: E402

MAC_LAYOUT = [("data", 64), ("keep", 8)]


class Harness(LiteXModule):
    def __init__(self):
        self.ios = set()
        for name in ("sys", "milan", "macsys", "macdp"):
            cd = ClockDomain(name)
            setattr(self, f"cd_{name}", cd)
            self.ios |= {cd.clk, cd.rst}
        rename = {"sys": "macsys", "milan": "macdp"}
        tx = soc._axis_dp_cdc(self, "mac_tx_cdc", MAC_LAYOUT, "milan",
                              to_datapath=False, rename=rename)
        rx = soc._axis_dp_cdc(self, "mac_rx_cdc", MAC_LAYOUT, "milan",
                              to_datapath=True, rename=rename)
        if mode == "head":
            soc._payload_in_block_ram(self.mac_tx_cdc)
            soc._payload_in_block_ram(self.mac_rx_cdc)
        for ends in (tx, rx):
            for ep in (ends.sys, ends.dp):
                self.ios |= set(ep.flatten())
        master = axi.AXILiteInterface(data_width=32, address_width=32)
        if mode == "head":
            slave = soc._cross_csr_bus(self, master, "milan")
        else:
            slave = axi.AXILiteInterface(data_width=32, address_width=32)
            self.submodules.milan_axil_cdc = axi.AXILiteClockDomainCrossing(
                master, slave, cd_from="sys", cd_to="milan")
        for bus in (master, slave):
            for name in ("aw", "w", "b", "ar", "r"):
                self.ios |= set(getattr(bus, name).flatten())


h = Harness()
out.write_text(str(convert(h, ios=h.ios, name="xing_top")))
print(f"wrote {out}")
