#!/usr/bin/env python3
"""R591-1: emit a Verilog harness holding the seven retained crossings as one
tree's milan_soc builds them (MAC TX/RX as MilanMAC does for milan_cd="milan",
and the CSR AXI-Lite crossing as add_milan_datapath does), every channel field
exposed as a top-level port, for an out-of-context primitive-mapping check.

Usage: r591_crossing_harness.py TREE OUT.v
TREE is a checkout (base or head); its sw/litex/milan_soc.py is imported.
At a tree without `_cross_csr_bus` (the base) the stock LiteX calls the base
made inline are used, so the harness is each tree's own product construction.
"""
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
# optional third argument "axil-no-framing": AXI-Lite first/last are not ports
# (driven 0 on the master side, unused on the slave side), as in the image
AXIL_NO_FRAMING = len(sys.argv) > 3 and sys.argv[3] == "axil-no-framing"
# "axil-framing-write-only": master-side first/last are ports, slave-side are not
AXIL_WRITE_ONLY = len(sys.argv) > 3 and sys.argv[3] == "axil-framing-write-only"
sys.path.insert(0, str(tree / "sw/litex"))
import milan_soc  # noqa: E402
assert Path(milan_soc.__file__).resolve().parent == tree / "sw/litex"

from migen import ClockDomain, Module  # noqa: E402
from migen.fhdl.verilog import convert  # noqa: E402
from litex.soc.interconnect import axi  # noqa: E402

MAC_LAYOUT = [("data", 64), ("keep", 8)]


class Harness(Module):
    def __init__(self):
        self.ios = set()
        for name in ("sys", "milan", "macsys", "macdp"):
            cd = ClockDomain(name)
            setattr(self.clock_domains, f"cd_{name}", cd)
            self.ios |= {cd.clk, cd.rst}
        rename = (milan_soc._mac_cdc_rename("milan") if hasattr(milan_soc, "_mac_cdc_rename")
                  else {"sys": "macsys", "milan": "macdp"})
        tx = milan_soc._axis_dp_cdc(self, "mac_tx_cdc", MAC_LAYOUT, "milan",
                                    to_datapath=False, rename=rename)
        rx = milan_soc._axis_dp_cdc(self, "mac_rx_cdc", MAC_LAYOUT, "milan",
                                    to_datapath=True, rename=rename)
        self.submodules.mac_tx_cdc = self.mac_tx_cdc
        self.submodules.mac_rx_cdc = self.mac_rx_cdc
        if hasattr(milan_soc, "_payload_in_block_ram"):
            milan_soc._payload_in_block_ram(self.mac_tx_cdc)
            milan_soc._payload_in_block_ram(self.mac_rx_cdc)
        master = axi.AXILiteInterface(data_width=32, address_width=32)
        if hasattr(milan_soc, "_cross_csr_bus"):
            slave = milan_soc._cross_csr_bus(self, master, "milan")
        else:
            slave = axi.AXILiteInterface(data_width=32, address_width=32)
            self.submodules.milan_axil_cdc = axi.AXILiteClockDomainCrossing(
                master, slave, cd_from="sys", cd_to="milan")
        endpoints = [(ep, True) for ep in (tx.dp, tx.sys, rx.dp, rx.sys)]
        for itf in (master, slave):
            # the framing of a channel's sink side (its writer) and source side (its reader)
            for c in ("aw", "w", "b", "ar", "r"):
                writer_side = (itf is master) == (c in ("aw", "w", "ar"))
                framing = not AXIL_NO_FRAMING and (writer_side or not AXIL_WRITE_ONLY)
                endpoints.append((getattr(itf, c), framing))
        for ep, framing in endpoints:
            self.ios |= {ep.valid, ep.ready}
            if framing:
                self.ios |= {ep.first, ep.last}
            self.ios |= {s for s, _ in ep.payload.iter_flat()}


h = Harness()
out.write_text(str(convert(h, ios=h.ios, name="r591_crossings")), encoding="utf-8")
print(f"wrote {out}")
