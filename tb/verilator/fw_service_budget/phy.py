# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Simulation MDIO pin boundary with the product CSR and CDC semantics."""
from migen import Signal
from migen.genlib.cdc import MultiReg
from litex.build.generic_platform import Pins, Subsignal
from litex.gen import LiteXModule
from litex.soc.interconnect.csr import CSRStatus, CSRStorage
from litex.soc.interconnect import wishbone


class PhyBoundary(LiteXModule):
    """Replace only the PHY pins; retain firmware accesses and fabric consumers."""

    def __init__(self, platform: object) -> None:
        self.phy_mdio_w = CSRStorage(3, name="phy_mdio_w")
        self.phy_mdio_r = CSRStatus(1, name="phy_mdio_r")
        self.link_status = CSRStorage(4, reset=13, name="link_status")
        platform.add_extension([("phy", 0, Subsignal("pins", Pins(3)),
                                Subsignal("reply", Pins(1)),
                                Subsignal("publish", Pins(1)),
                                Subsignal("status", Pins(4)),
                                Subsignal("read", Pins(1)),
                                Subsignal("ack", Pins(1)),
                                Subsignal("error", Pins(1)),
                                Subsignal("data", Pins(32)))])
        pads = platform.request("phy")
        self.comb += [pads.pins.eq(self.phy_mdio_w.storage),
                      pads.publish.eq(self.link_status.re),
                      pads.status.eq(self.link_status.storage)]
        self.reader = wishbone.Interface()
        self.comb += [self.reader.cyc.eq(pads.read), self.reader.stb.eq(pads.read),
                      self.reader.we.eq(0), self.reader.sel.eq(15),
                      self.reader.adr.eq(0x90000110 >> 2),
                      pads.ack.eq(self.reader.ack), pads.error.eq(self.reader.err),
                      pads.data.eq(self.reader.dat_r)]
        self.specials += MultiReg(pads.reply, self.phy_mdio_r.status)
        link = Signal()
        duplex = Signal()
        self.specials += [MultiReg(self.link_status.storage[0], link, odomain="milan"),
                          MultiReg(self.link_status.storage[3], duplex, odomain="milan")]
        # The datapath already synchronizes speed, as in MilanMAC.
        self.dp_ports = dict(i_i_link_up=link, i_i_full_duplex=duplex,
                             i_i_mac_speed=self.link_status.storage[1:3])
