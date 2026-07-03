# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""RGMII PHY for the Alinx AX7101 (RTL8211E) — RX-clock-inverted variant of s7rgmii.

LiteEth's stock `LiteEthPHYRGMII` (s7rgmii) samples the RGMII RX data with a
*non-inverted* RX clock plus an IDELAY on the data. On the AX7101 that never aligns:
on hardware the FPGA MAC reports RGMII **preamble errors** at both `rx_delay=0` and
`rx_delay=2 ns`, and the IDELAY range (~0..2.5 ns) can't reach the sampling point this
board needs (~half a clock period).

The Alinx vendor design (`SRC/15_ethernet_test/.../util_gmii_to_rgmii.v`) instead
**inverts** the RX clock — `BUFG(.I(~rgmii_rxc))` — moving the sample point into the
centre of the data eye. This PHY is `s7rgmii` with exactly that one change (RX clock
inversion in the CRG), reusing LiteEth's RGMII RX/TX datapath unmodified. `rx_clk_invert`
and the IDELAY/`tx_delay` remain knobs so the timing can still be tuned per board.
"""

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.gen import LiteXModule
from litex.soc.cores.clock import S7PLL
from litex.soc.interconnect.csr import CSRStorage

from litex.soc.interconnect import stream
from liteeth.common import eth_phy_description
from liteeth.phy.common import LiteEthPHYHWReset
from liteeth.phy.s7rgmii import LiteEthPHYRGMIITX
try:
    from liteeth.phy.common import LiteEthPHYMDIO
except ImportError:  # older/newer liteeth layouts
    LiteEthPHYMDIO = None


class MilanRGMIIRX(LiteXModule):
    """RGMII RX matching the Alinx AX7101 vendor design: raw IBUF data straight into an
    IDDR clocked by the (inverted) eth_rx clock, with **no IDELAY**. LiteEth's stock RX
    always inserts an IDELAYE2 whose ~0.6 ns floor mis-aligns sampling on this board —
    the vendor `util_gmii_to_rgmii.v` uses none. Datapath logic (valid/data/last) is
    identical to LiteEth's."""
    def __init__(self, pads):
        self.source = source = stream.Endpoint(eth_phy_description(8))
        rx_ctl_ibuf  = Signal()
        rx_ctl       = Signal()
        rx_data_ibuf = Signal(4)
        rx_data      = Signal(8)
        self.specials += [
            Instance("IBUF", i_I=pads.rx_ctl, o_O=rx_ctl_ibuf),
            Instance("IDDR", p_DDR_CLK_EDGE="SAME_EDGE_PIPELINED",
                i_C=ClockSignal("eth_rx"), i_CE=1, i_S=0, i_R=0,
                i_D=rx_ctl_ibuf, o_Q1=rx_ctl, o_Q2=Signal()),
        ]
        for i in range(4):
            self.specials += [
                Instance("IBUF", i_I=pads.rx_data[i], o_O=rx_data_ibuf[i]),
                # Q1/Q2 SWAPPED vs stock: inverting the RX clock swaps which DDR edge
                # captures the low vs high nibble, so without this every SFD (0xD5)
                # arrives nibble-swapped (0x5D) → 100% preamble errors (hardware-
                # confirmed: +1 preamble error per frame). Swapping restores byte order.
                Instance("IDDR", p_DDR_CLK_EDGE="SAME_EDGE_PIPELINED",
                    i_C=ClockSignal("eth_rx"), i_CE=1, i_S=0, i_R=0,
                    i_D=rx_data_ibuf[i], o_Q1=rx_data[i+4], o_Q2=rx_data[i]),
            ]
        rx_ctl_d = Signal()
        self.sync += rx_ctl_d.eq(rx_ctl)
        last = Signal()
        self.comb += last.eq(~rx_ctl & rx_ctl_d)
        self.sync += [source.valid.eq(rx_ctl), source.data.eq(rx_data)]
        self.comb += source.last.eq(last)


class _MilanRGMIICRG(LiteXModule):
    def __init__(self, clock_pads, pads, with_hw_init_reset, tx_delay=2e-9,
                 hw_reset_cycles=256, rx_clk_invert=True):
        self._reset = CSRStorage(description="PHY reset.")

        # --- RX clock ---  INVERTED for the AX7101 (matches the Alinx vendor design),
        # so RXD is sampled in the centre of the eye instead of on the transition edge.
        self.cd_eth_rx = ClockDomain()
        eth_rx_clk_ibuf = Signal()
        eth_rx_clk_int  = Signal()
        self.specials += Instance("IBUF", i_I=clock_pads.rx, o_O=eth_rx_clk_ibuf)
        self.comb += eth_rx_clk_int.eq(~eth_rx_clk_ibuf if rx_clk_invert else eth_rx_clk_ibuf)
        self.specials += Instance("BUFG", i_I=eth_rx_clk_int, o_O=self.cd_eth_rx.clk)

        # --- TX clock --- (identical to s7rgmii: PLL off eth_rx, phase = tx_delay)
        self.cd_eth_tx         = ClockDomain()
        self.cd_eth_tx_delayed = ClockDomain(reset_less=True)
        tx_phase = 125e6*tx_delay*360
        assert tx_phase < 360
        self.pll = pll = S7PLL()
        pll.register_clkin(ClockSignal("eth_rx"), 125e6)
        pll.create_clkout(self.cd_eth_tx,         125e6, with_reset=False)
        pll.create_clkout(self.cd_eth_tx_delayed, 125e6, phase=tx_phase)

        eth_tx_clk_obuf = Signal()
        self.specials += [
            Instance("ODDR", p_DDR_CLK_EDGE="SAME_EDGE",
                i_C=ClockSignal("eth_tx_delayed"), i_CE=1, i_S=0, i_R=0,
                i_D1=1, i_D2=0, o_Q=eth_tx_clk_obuf),
            Instance("OBUF", i_I=eth_tx_clk_obuf, o_O=clock_pads.tx),
        ]

        # --- Reset ---
        self.reset = reset = Signal()
        if with_hw_init_reset:
            self.hw_reset = LiteEthPHYHWReset(cycles=hw_reset_cycles)
            self.comb += reset.eq(self._reset.storage | self.hw_reset.reset)
        else:
            self.comb += reset.eq(self._reset.storage)
        if hasattr(pads, "rst_n"):
            self.comb += pads.rst_n.eq(~reset)
        self.specials += [
            AsyncResetSynchronizer(self.cd_eth_tx, reset),
            AsyncResetSynchronizer(self.cd_eth_rx, reset),
        ]


class MilanRGMIIPHY(LiteXModule):
    dw          = 8
    tx_clk_freq = 125e6
    rx_clk_freq = 125e6
    def __init__(self, clock_pads, pads, with_hw_init_reset=True, tx_delay=2e-9,
                 rx_delay=0e-9, iodelay_clk_freq=200e6, hw_reset_cycles=256,
                 rx_clk_invert=True):
        self.crg = _MilanRGMIICRG(clock_pads, pads, with_hw_init_reset, tx_delay,
                                  hw_reset_cycles, rx_clk_invert)
        self.tx  = ClockDomainsRenamer("eth_tx")(LiteEthPHYRGMIITX(pads))
        self.rx  = ClockDomainsRenamer("eth_rx")(MilanRGMIIRX(pads))  # no IDELAY (Alinx)
        self.sink, self.source = self.tx.sink, self.rx.source
        # rx_delay / iodelay_clk_freq are accepted for API compat but unused: this RX
        # samples raw data with the inverted clock (no IDELAYE2), matching the vendor.
        if LiteEthPHYMDIO is not None and hasattr(pads, "mdc"):
            self.mdio = LiteEthPHYMDIO(pads)
