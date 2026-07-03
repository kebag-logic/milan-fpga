#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Configurable single-core RISC-V SoC that BOOTS Linux with the Milan TSN NIC and
# its driver — the fully-FPGA target from docs/FULLY_FPGA_RISCV_MIGRATION.md. One
# NaxRiscv core (MMU, Linux-capable) + clock/reset + UART + integrated RAM, with the
# Milan datapath as a memory-mapped peripheral (CSR @ 0x9000_0000 + IRQs), and —
# with --full — the AXIS<->memory DMA (§A.6) and the 1G MAC + RGMII PHY (§A.7).
#
#   ./milan_soc.py                         # NIC (CSR only); elaborate + export gateware
#   ./milan_soc.py --full                  # FULL FPGA solution: NIC + DMA + MAC + PHY
#   ./milan_soc.py --with-dma / --with-mac # attach just one boundary
#   ./milan_soc.py --no-milan              # bare SoC (bring-up smoke; self-contained)
#   ./milan_soc.py --xlen 32               # RV32 + sv32 MMU (default RV64GC + sv39)
#   ./milan_soc.py --full --build          # + run Vivado P&R -> bitstream (needs Artix-7)
#   ./milan_soc.py --full --build --load   # + program the board
#
# The Artix-7 (xc7a100t) bitstream needs Vivado with Artix-7 device support. This
# box only has Spartan-7 installed, so `--build` P&R is blocked here; gateware
# EXPORT (the default, run=False) works with no vendor tools. The CPU⇄CSR path is
# proven on the softcore in sim: sw/litex/milan_sim.py -> the BIOS reads ID="MILN"
# (M-A2), evidence in sw/litex/evidence/naxriscv_reads_MILN.log.

import os
import sys
import argparse

from migen import ClockDomain, ClockSignal, ResetSignal, Instance, Signal, Mux, If
from migen.genlib.cdc import MultiReg

from litex.gen import LiteXModule
from litex.soc.interconnect import stream

from litex.build.io import DDROutput

from litex.soc.cores.clock import S7PLL
from litex.soc.interconnect import axi
from litex.soc.interconnect.csr import CSRStorage
from litex.soc.interconnect.csr_eventmanager import EventManager, EventSourceLevel
from litex.soc.integration.soc_core import SoCCore
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import Builder, builder_args, builder_argdict

# Local platform (not in upstream litex_boards).
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "platforms"))
import alinx_ax7101

# The Milan CSR window. The register OFFSETS (0x000..0x700) match docs/REGISTER_MAP.md;
# only the BASE is host-specific: on this NaxRiscv SoC an MMIO peripheral must live in
# the CPU IO region (>= 0x8000_0000, uncached), so we map it at 0x9000_0000. The Zynq
# build used 0x43C0_0000. The device-tree `reg` base must match the host (see sw/README).
MILAN_CSR_BASE = 0x9000_0000
MILAN_CSR_SIZE = 0x0001_0000  # 64 KB


# CRG ----------------------------------------------------------------------------------------------

class _CRG(LiteXModule):
    """Clock/reset: PLL the 200 MHz board clock down to the system clock.

    With `with_dram`, also produces the DDR3 PHY clocks (`sys4x`, `sys4x_dqs`); with
    `with_dram` or `with_eth`, the 200 MHz `idelay` reference + IDELAYCTRL that both
    the Artix-7 DDR3 PHY (A7DDRPHY) and the RGMII PHY (LiteEth s7rgmii) need for their
    IODELAY calibration."""
    def __init__(self, platform, sys_clk_freq, with_dram=False, with_eth=False,
                 milan_clk_freq=None):
        self.cd_sys = ClockDomain()

        clk200 = platform.request("clk200")
        rst_n  = platform.request("cpu_reset_n")

        self.pll = pll = S7PLL(speedgrade=-2)
        self.comb += pll.reset.eq(~rst_n)
        pll.register_clkin(clk200, 200e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq)
        platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin)

        if milan_clk_freq:
            # Separate, slower clock for the Milan TSN datapath (rx_filter/CAM/CBS/
            # classifier/PTP/csr). That block is dense and was the sys (100 MHz)
            # critical path, but it only has to keep up with 1 GbE: a 64-bit datapath
            # at >=50 MHz is >3 Gb/s, so running it below sys costs no throughput while
            # lifting its logic off the 100 MHz timing budget entirely. The CPU + DDR3
            # stay at sys; the CSR (AXI-Lite) crosses via AXILiteClockDomainCrossing.
            self.cd_milan = ClockDomain()
            pll.create_clkout(self.cd_milan, milan_clk_freq)
            platform.add_false_path_constraints(self.cd_sys.clk, self.cd_milan.clk)

        if with_dram:
            # A7DDRPHY needs 4x (and 4x @90° for DQS) system clocks.
            self.cd_sys4x     = ClockDomain()
            self.cd_sys4x_dqs = ClockDomain()
            pll.create_clkout(self.cd_sys4x,     4 * sys_clk_freq)
            pll.create_clkout(self.cd_sys4x_dqs, 4 * sys_clk_freq, phase=90)

        if with_dram or with_eth:
            # 200 MHz IDELAY reference + controller (DDR3 PHY + RGMII PHY IODELAYs).
            from litex.soc.cores.clock import S7IDELAYCTRL
            self.cd_idelay = ClockDomain()
            pll.create_clkout(self.cd_idelay, 200e6)
            self.idelayctrl = S7IDELAYCTRL(self.cd_idelay)


# Milan NIC ----------------------------------------------------------------------------------------

class MilanNIC(LiteXModule):
    """The Milan TSN datapath (`milan_datapath.sv`) wired into the SoC.

    `milan_datapath` is the **PS-less §A.9 wrapper** (milan_top minus the Zynq PS
    and minus the MAC) — a real, Verilator+Yosys-verified module (tb/verilator/
    milan_dp, syn/yosys). It exposes:
      * an AXI4-Lite CSR slave (milan_csr control plane) — wired here to the CPU bus;
      * three DMA AXIS ports (tx from DRAM / rx to DRAM / ts to DRAM) — the §A.6 DMA
        engine attaches here (stubbed idle for now);
      * a MAC-facing AXIS pair + MAC cfg/status — the §A.7 MAC (LiteEth `LiteEthMAC`
        or Forencich `eth_mac_1g_rgmii_fifo` + RGMII PHY) attaches here (stubbed);
      * `o_irq_csr` (link/PTP/RMON aggregate) — routed to the PLIC below.

    This makes the SoC instantiate REAL RTL (no black box). The DMA + MAC attach are
    the next migration steps (§A.6/§A.7); until then their AXIS ports are tied idle,
    which still elaborates and exports gateware and keeps the CPU⇄CSR path live
    (proven end-to-end in tb/verilator/milan_dp: CPU reads ID="MILN", M-A2).
    """
    def __init__(self, platform, axil, dma_mac_ports=None, milan_cd="sys"):
        # Interrupts, level-triggered, CPU-facing via the SoC IRQ handler. Four lines
        # match the DT/driver (tx/rx/ts-dma + csr); tx/rx/ts come from the §A.6 DMA
        # engine (held 0 until it is attached); csr is driven by the datapath.
        self.submodules.ev = ev = EventManager()
        ev.tx  = EventSourceLevel()
        ev.rx  = EventSourceLevel()
        ev.ts  = EventSourceLevel()
        ev.csr = EventSourceLevel()
        ev.finalize()
        self.comb += [ev.tx.trigger.eq(0), ev.rx.trigger.eq(0), ev.ts.trigger.eq(0)]
        add_milan_datapath(self, platform, axil, ev.csr.trigger,
                           extra_ports=dma_mac_ports, milan_cd=milan_cd)


# The milan_datapath source set (ordered: packages first). Mirrors the milan_dp
# Verilator Makefile and the syn/yosys entry — the single source of truth for what
# the §A.9 wrapper is built from.
_MILAN_DATAPATH_SOURCES = [
    "hdl/common/ethernet_packet_pkg.sv", "hdl/common/axi_stream_if.sv", "hdl/adp/adp_pkg.sv",
    "third_party/verilog-axis/rtl/axis_fifo.v", "third_party/verilog-axis/rtl/axis_demux.v",
    "third_party/verilog-axis/rtl/axis_arb_mux.v", "third_party/verilog-axis/rtl/arbiter.v",
    "third_party/verilog-axis/rtl/priority_encoder.v",
    "hdl/802_1q_traffic_shaper/traffic_class_map.sv", "hdl/802_1q_traffic_shaper/traffic_classifier.sv",
    "hdl/802_1q_traffic_shaper/credit_based_shaper.sv", "hdl/802_1q_traffic_shaper/traffic_shaping_core.sv",
    "hdl/802_1q_traffic_shaper/traffic_queues.sv", "hdl/802_1q_traffic_shaper/traffic_controller_802_1q.sv",
    "hdl/ptp_timestamp/timestamp_counter.sv", "hdl/ptp_timestamp/ptp_csr_sync.sv",
    "hdl/common/cdc_pulse.sv", "hdl/common/cdc_handshake.sv", "hdl/common/axis_mux_rr_2in_1out.sv",
    "hdl/ptp_timestamp/ptp_ts_core.sv", "hdl/ptp_timestamp/ptp_ts_top.sv",
    "hdl/common/tcam.sv", "hdl/common/rx_mac_filter.sv",
    "hdl/adp/adp_advertiser.sv", "hdl/adp/adp_tx_arbiter.sv",
    "hdl/eth_event_counter/ethernet_events.sv", "hdl/eth_event_counter/event_counter.sv",
    "hdl/csr/milan_csr.sv", "hdl/common/milan_datapath.sv",
]


def add_milan_datapath(host, platform, axil, o_irq_csr, extra_ports=None, milan_cd="sys"):
    """Instantiate `milan_datapath` and add its RTL sources — the single place the
    wrapper is wired, reused by the board SoC (`MilanNIC`) and the sim SoC
    (`milan_sim.py`). `axil` is the AXI-Lite CSR slave; `o_irq_csr` gets the datapath
    interrupt. `extra_ports` overrides/adds Instance ports to attach the DMA (§A.6)
    and MAC (§A.7) at the exposed AXIS boundary — without it, those ports are tied
    idle (still elaborates; keeps the CPU⇄CSR path live). Instance ports for RTL
    signals already named `i_*`/`o_*` get the doubled migen prefix (e.g. milan port
    `i_i_mac_speed`, `o_o_irq_csr`) — that is correct, not a typo."""
    # Run the datapath in `milan_cd`. When that is not `sys`, cross the CPU's
    # AXI-Lite CSR bus (sys) into `milan_cd` with an async-FIFO CDC — so the dense
    # datapath logic leaves the sys (100 MHz) timing budget while the CPU/DDR3 stay
    # fast. `milan_cd == "sys"` (the default, and what the sim uses) keeps the old
    # single-clock direct wiring. The DMA/MAC AXIS boundary is likewise crossed by
    # its own stream CDC in MilanDMA/MilanMAC when `milan_cd != "sys"`.
    if milan_cd != "sys":
        csr_axil = axi.AXILiteInterface(data_width=32, address_width=32)
        host.submodules.milan_axil_cdc = axi.AXILiteClockDomainCrossing(
            axil, csr_axil, cd_from="sys", cd_to=milan_cd)
        # The aggregate CSR IRQ is a level in milan_cd; 2-FF-synchronise it into the
        # sys-domain EventManager (o_irq_csr) to avoid metastability.
        irq_port = Signal()
        host.specials += MultiReg(irq_port, o_irq_csr, odomain="sys")
    else:
        csr_axil = axil
        irq_port = o_irq_csr
    ports = dict(
        # clocks / reset — the whole datapath runs in `milan_cd`
        i_axis_clk    = ClockSignal(milan_cd),  i_axis_resetn = ~ResetSignal(milan_cd),
        i_gtx_clk     = ClockSignal(milan_cd),  i_gtx_resetn  = ~ResetSignal(milan_cd),
        # AXI4-Lite CSR slave (from the CPU bus bridge, CDC'd into milan_cd above)
        i_s_axi_awaddr  = csr_axil.aw.addr[:16], i_s_axi_awvalid = csr_axil.aw.valid,
        o_s_axi_awready = csr_axil.aw.ready,
        i_s_axi_wdata   = csr_axil.w.data,  i_s_axi_wstrb = csr_axil.w.strb,
        i_s_axi_wvalid  = csr_axil.w.valid, o_s_axi_wready = csr_axil.w.ready,
        o_s_axi_bresp   = csr_axil.b.resp,  o_s_axi_bvalid = csr_axil.b.valid,
        i_s_axi_bready  = csr_axil.b.ready,
        i_s_axi_araddr  = csr_axil.ar.addr[:16], i_s_axi_arvalid = csr_axil.ar.valid,
        o_s_axi_arready = csr_axil.ar.ready,
        o_s_axi_rdata   = csr_axil.r.data,  o_s_axi_rresp = csr_axil.r.resp,
        o_s_axi_rvalid  = csr_axil.r.valid, i_s_axi_rready = csr_axil.r.ready,
        # TX/RX/TS DMA AXIS — §A.6 engine attaches here (idle stub)
        i_s_axis_tx_tdata = 0, i_s_axis_tx_tkeep = 0, i_s_axis_tx_tvalid = 0,
        i_s_axis_tx_tlast = 0,
        i_m_axis_rx_tready = 0, i_m_axis_ts_tready = 0,
        # MAC-facing AXIS — §A.7 MAC attaches here (idle stub)
        i_m_axis_mac_tx_tready = 0,
        i_s_axis_mac_rx_tdata = 0, i_s_axis_mac_rx_tkeep = 0,
        i_s_axis_mac_rx_tvalid = 0, i_s_axis_mac_rx_tlast = 0,
        # MAC status (from the external MAC; constants until §A.7)
        i_i_mac_speed = 0b10, i_i_link_up = 1, i_i_full_duplex = 1, i_i_mac_events = 0,
        # interrupt (csr aggregate; DMA-done IRQs come from §A.6). CDC'd to sys above.
        o_o_irq_csr = irq_port,
    )
    if extra_ports:
        ports.update(extra_ports)
    host.specials += Instance("milan_datapath", **ports)
    # CBS timing: the credit-based shaper's slope terms (idle_slope_per_cycle_r /
    # send_slope_per_byte_r in credit_based_shaper.sv) are wide constant-divides of
    # quasi-static config (idleSlope / link-rate — reprogrammed only by `tc cbs`,
    # then held for millions of cycles). The RTL registers the divide output
    # (stage-0 slope_pipe), and this declares the config->slope_r capture a
    # multicycle path so P&R never squeezes the divide into a single sys period —
    # the true bottleneck at 100 MHz (DDR3 needs 100 MHz, so we cannot just slow
    # sys down). Bit-exactly modelled by the Verilator CBS ref (one extra stage).
    # Real Xilinx parts only ("xc…"); the sim backend ignores/needs no XDC.
    if str(getattr(platform, "device", "")).startswith("xc"):
        # Match by *leaf* register name, not hierarchy: synthesis pulls the CBS
        # slope-compute cone toward the csr module (where its config sources live),
        # so a *u_cbs* path filter misses it. The `dont_touch` in
        # credit_based_shaper.sv keeps these regs named per queue.
        _cbs_slope = ("[get_cells -hierarchical -filter "
                      "{{NAME =~ *send_slope_per_byte_r_reg* || "
                      "NAME =~ *idle_slope_per_cycle_r_reg*}}]")
        platform.add_platform_command("set_multicycle_path 4 -setup -to " + _cbs_slope)
        platform.add_platform_command("set_multicycle_path 3 -hold -to " + _cbs_slope)
    # RTL sources for elaboration / P&R. Curated list (NOT add_source_dir) so the
    # Zynq-only milan_top.sv / milan_dma_wrapper.v are excluded from the fabric build
    # — same file set the tb/verilator/milan_dp + syn/yosys checks use.
    base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # milan-fpga/
    # Include dirs for the ``include ...`` files (ethernet_packet_pkg.sv, *.svh).
    # Vivado auto-searches source dirs; Verilator (the sim backend) needs -I.
    for inc in ("hdl/common", "hdl/802_1q_traffic_shaper", "hdl/ptp_timestamp",
                "hdl/adp", "hdl/csr", "hdl/eth_event_counter"):
        platform.add_verilog_include_path(os.path.join(base, inc))
    for f in _MILAN_DATAPATH_SOURCES:
        platform.add_source(os.path.join(base, f))


# AXIS clock-domain crossing (DMA/MAC boundary) ---------------------------------------------------

class _AxisDP:
    """Pair of stream endpoints for one AXIS lane crossing the datapath boundary:
    `.dp` is bound to the `milan_datapath` Instance, `.sys` to the sys-domain DMA/MAC."""
    def __init__(self, dp, sys):
        self.dp  = dp
        self.sys = sys

def _axis_dp_cdc(host, name, layout, milan_cd, to_datapath):
    """Cross one AXIS lane between the sys domain (DMA engine / MAC core) and the
    datapath's `milan_cd` domain with an async-FIFO `stream.ClockDomainCrossing`
    (the "use a FIFO to compensate the timing" boundary). `to_datapath=True` is a
    sys->milan_cd lane (memory->TX, MAC-RX->datapath); False is milan_cd->sys
    (datapath->RX/TS memory, datapath->MAC-TX). When `milan_cd == "sys"` there is no
    crossing: `.dp` and `.sys` are the same endpoint (direct wire)."""
    if milan_cd == "sys":
        ep = stream.Endpoint(layout)
        return _AxisDP(dp=ep, sys=ep)
    if to_datapath:                                        # sys -> milan_cd
        cdc = stream.ClockDomainCrossing(layout, cd_from="sys", cd_to=milan_cd, depth=16)
        setattr(host, name, cdc)                           # LiteXModule auto-submodule
        return _AxisDP(dp=cdc.source, sys=cdc.sink)
    cdc = stream.ClockDomainCrossing(layout, cd_from=milan_cd, cd_to="sys", depth=16)  # milan_cd -> sys
    setattr(host, name, cdc)
    return _AxisDP(dp=cdc.sink, sys=cdc.source)


# MAC (§A.7) ---------------------------------------------------------------------------------------

class MilanMAC(LiteXModule):
    """The 1G MAC + RGMII PHY (§A.7), attached at the milan_datapath MAC-facing AXIS
    boundary. Uses LiteEth's `LiteEthPHYRGMII` (Artix-7 s7rgmii) + `LiteEthMACCore`
    (preamble/CRC/padding, PHY-width conversion) and a thin stream↔AXIS adapter, so
    the Milan datapath owns *all* packet processing (classify/CBS/PTP/filter/ADP) and
    the MAC core just does L1/framing.

    `dp_ports` is the dict of `milan_datapath` Instance ports this MAC drives — pass
    it as `MilanNIC(..., dma_mac_ports=mac.dp_ports)`.

    NOTE (board-gated): the exact `last_be`↔`tkeep` byte-enable mapping and the
    link/speed status (MDIO) are wired to sensible values for elaboration; they are
    validated on hardware (there is no RGMII PHY to exercise in sim). See
    docs/FULLY_FPGA_RISCV_MIGRATION.md §A.7 and the protocol/test matrix."""
    def __init__(self, platform, data_width=64, phy_index=0, milan_cd="sys", **_rgmii):
        from liteeth.phy.gmii import LiteEthPHYGMII
        from liteeth.mac.core import LiteEthMACCore

        clk_pads = platform.request("eth_clocks", phy_index)
        pads     = platform.request("eth",        phy_index)
        # The AX7101 RTL8211E is strapped for **GMII** (8-bit SDR), per the Alinx
        # example top (`input [7:0] e_rxd`, separate rxdv/rxer, gtx=rxc). An RGMII
        # (4-bit DDR) read of this bus corrupts every byte — hardware-confirmed as 100%
        # MAC preamble errors (evidence/hw_ma3_*). LiteEthPHYGMII is the right PHY.
        # (`**_rgmii` absorbs the now-unused --rgmii-*-delay knobs for API compat.)
        self.phy  = LiteEthPHYGMII(clk_pads, pads, with_hw_init_reset=True)
        self.core = LiteEthMACCore(phy=self.phy, dw=data_width,
                                   with_preamble_crc=True, with_padding=True)

        nb = data_width // 8
        L  = [("data", data_width), ("keep", nb)]
        # The datapath-facing endpoints are in `milan_cd`; the MAC core is in sys.
        # When they differ, an async-FIFO stream CDC bridges each direction (`keep`
        # carries the last-beat byte-enable). `_axis_dp_cdc` returns the endpoint the
        # datapath binds to, wiring the CDC (or a direct pass-through) to `sys_ep`.
        tx_dp = _axis_dp_cdc(self, "mac_tx_cdc", L, milan_cd, to_datapath=False)  # dp -> MAC
        rx_dp = _axis_dp_cdc(self, "mac_rx_cdc", L, milan_cd, to_datapath=True)   # MAC -> dp
        # LiteEth's `last_be` is NOT an AXIS keep mask — it is a **one-hot pointer to the
        # last valid byte** of the final beat (liteeth/mac/padding.py Case: 0x01->1 byte,
        # 0x02->2 … 0x80->8; the RX side builds it by up-converting a single `last` bit).
        # AXIS `tkeep` is a contiguous byte mask (0xFF = 8 valid). Passing the mask straight
        # through makes the 64->8 TX StrideConverter read the *lowest* set bit -> 1 valid
        # byte, so a full word egresses as a single byte (hardware-measured `ff:00:..`) and
        # multi-beat frames never terminate -> nothing on the wire. Convert both ways:
        #   TX  keep(mask) -> last_be(one-hot of the highest set bit): keep & ~(keep>>1)
        #   RX  last_be(one-hot) -> keep(mask up to that byte):        (last_be<<1) - 1
        #
        # `loopback` (CSR, sys domain): when 1, the datapath's MAC-TX stream is fed straight
        # back into its MAC-RX stream (bypassing the LiteEth core + PHY) so a full frame can
        # be verified memory->TX-DMA->datapath->RX-DMA->memory with no wire/rig. Both are
        # AXIS keep-masks here, so no last_be conversion is needed on the loop path.
        self.loopback = CSRStorage(1, description="1 = internal MAC-TX->MAC-RX AXIS loopback")
        lb = self.loopback.storage
        self.comb += [
            # TX payload -> core.sink is driven unconditionally (harmless when valid=0);
            # only `valid`/`ready` and the RX source are muxed by `loopback`.
            self.core.sink.data.eq(tx_dp.sys.data),
            self.core.sink.last.eq(tx_dp.sys.last),
            self.core.sink.last_be.eq(tx_dp.sys.keep & ~(tx_dp.sys.keep >> 1)),
            If(lb,
                # internal loopback: datapath TX -> datapath RX (sys domain), both keep-masks
                rx_dp.sys.valid.eq(tx_dp.sys.valid),
                rx_dp.sys.data.eq(tx_dp.sys.data),
                rx_dp.sys.last.eq(tx_dp.sys.last),
                rx_dp.sys.keep.eq(tx_dp.sys.keep),
                tx_dp.sys.ready.eq(rx_dp.sys.ready),
                self.core.sink.valid.eq(0),      # nothing to the wire
                self.core.source.ready.eq(0),    # ignore wire RX
            ).Else(
                self.core.sink.valid.eq(tx_dp.sys.valid),
                tx_dp.sys.ready.eq(self.core.sink.ready),
                # core.source -> datapath RX endpoint; one-hot last_be -> keep mask on last beat
                rx_dp.sys.valid.eq(self.core.source.valid),
                rx_dp.sys.data.eq(self.core.source.data),
                rx_dp.sys.last.eq(self.core.source.last),
                rx_dp.sys.keep.eq(Mux(self.core.source.last,
                                      (self.core.source.last_be << 1) - 1, 2**nb - 1)),
                self.core.source.ready.eq(rx_dp.sys.ready),
            ),
        ]

        self.dp_ports = dict(
            o_m_axis_mac_tx_tdata  = tx_dp.dp.data,  o_m_axis_mac_tx_tkeep = tx_dp.dp.keep,
            o_m_axis_mac_tx_tvalid = tx_dp.dp.valid, o_m_axis_mac_tx_tlast = tx_dp.dp.last,
            i_m_axis_mac_tx_tready = tx_dp.dp.ready,
            i_s_axis_mac_rx_tdata  = rx_dp.dp.data,  i_s_axis_mac_rx_tkeep = rx_dp.dp.keep,
            i_s_axis_mac_rx_tvalid = rx_dp.dp.valid, i_s_axis_mac_rx_tlast = rx_dp.dp.last,
            o_s_axis_mac_rx_tready = rx_dp.dp.ready,
            # MAC status: 1G/up/full-duplex until MDIO link tracking lands (§A.7 refine);
            # RMON event pulses (i_mac_events) are 0 — the LiteEth core doesn't expose the
            # same event set as the Forencich MAC, so those RMON lanes stay 0 here.
            i_i_mac_speed = 0b10, i_i_link_up = 1, i_i_full_duplex = 1, i_i_mac_events = 0,
        )


# DMA (§A.6) ---------------------------------------------------------------------------------------

class MilanDMA(LiteXModule):
    """AXIS ↔ system-memory DMA (§A.6), attaching the milan_datapath TX/RX/TS DMA
    AXIS ports to the CPU's memory via three LiteX simple-mode DMA engines:

      * TX  — `WishboneDMAReader` : memory → `s_axis_tx`  (frames to transmit)
      * RX  — `WishboneDMAWriter` : `m_axis_rx`  → memory (received frames)
      * TS  — `WishboneDMAWriter` : `m_axis_ts`  → memory (PTP timestamp metadata)

    Each engine is `with_csr=True`, i.e. it exposes a **simple-mode** register block
    (`base` [64], `length` [32], `enable`, `done`, `loop`, `offset`) auto-mapped in
    the SoC CSR space — this is the ABI the Linux driver programs (mirrors the Zynq
    axi_dma simple mode). Each engine is its own Wishbone bus master into the SoC
    interconnect (width-adapted to the main bus automatically).

    `dp_ports` is merged with the MAC's into the single `milan_datapath` Instance.

    NOTE (board-gated): this elaborates against integrated RAM here; on the board it
    targets LiteDRAM. Descriptor/scatter-gather (Option 6b, multi-queue) is a later
    upgrade — see docs/FULLY_FPGA_RISCV_MIGRATION.md §A.6 + the protocol/test matrix."""
    def __init__(self, soc, data_width=64, milan_cd="sys"):
        from litex.soc.cores.dma import WishboneDMAReader, WishboneDMAWriter
        from litex.soc.interconnect import wishbone
        import math
        nb      = data_width // 8
        adr_w   = 32 - int(math.log2(nb))     # word-addressed wishbone

        def mk_bus():
            return wishbone.Interface(data_width=data_width, adr_width=adr_w, addressing="word")

        # Attach the DMA masters to the CPU's **coherent** DMA port when it exists
        # (NaxRiscv --with-coherent-dma exposes soc.dma_bus, which snoops the CPU caches);
        # otherwise fall back to the plain SoC bus. Without the coherent port, NaxRiscv
        # reaches DRAM via a direct LiteDRAM memory bus while these masters go through the
        # wishbone L2 — a different path, so CPU writes and DMA reads are NOT coherent
        # (hardware-confirmed: the DMA transmits stale DRAM). Coherent DMA closes that gap
        # so a CPU-written frame is DMA-read correctly without manual cache flushes.
        dma_bus = getattr(soc, "dma_bus", soc.bus)
        # `endianness="big"` = **no** byte-swap (with_byteswap=False): keep the Wishbone word
        # order == AXIS stream order == on-the-wire byte order. The LiteX default "little"
        # byte-swaps each word, which (with LiteEth's little-endian GMII path) reverses every
        # frame word vs memory — hardware-confirmed: an RX frame `ff ff ff ff ff ff 02 aa`
        # landed in memory as `aa 02 ff ff ff ff ff ff`, and TX broadcast egressed with a
        # mangled `00:02:ff:..` dst so the peer dropped it. "big" makes memory<->wire match
        # in both directions (and the internal loopback stays byte-exact, being symmetric).
        # TX: memory -> datapath (reader)
        self.tx = WishboneDMAReader(mk_bus(), endianness="big", with_csr=True)
        dma_bus.add_master("milan_dma_tx", master=self.tx.bus)
        # RX + TS: datapath -> memory (writers)
        self.rx = WishboneDMAWriter(mk_bus(), endianness="big", with_csr=True)
        dma_bus.add_master("milan_dma_rx", master=self.rx.bus)
        self.ts = WishboneDMAWriter(mk_bus(), endianness="big", with_csr=True)
        dma_bus.add_master("milan_dma_ts", master=self.ts.bus)

        # datapath-facing endpoints in `milan_cd`, async-FIFO CDC'd to the sys-domain
        # DMA engines when the domains differ (see _axis_dp_cdc). TX is mem->datapath;
        # RX/TS are datapath->mem.
        L = [("data", data_width), ("keep", nb)]
        tx_dp = _axis_dp_cdc(self, "dma_tx_cdc", L, milan_cd, to_datapath=True)
        rx_dp = _axis_dp_cdc(self, "dma_rx_cdc", L, milan_cd, to_datapath=False)
        ts_dp = _axis_dp_cdc(self, "dma_ts_cdc", L, milan_cd, to_datapath=False)
        self.comb += [
            # TX: reader.source (sys) -> datapath TX endpoint (full keep)
            tx_dp.sys.valid.eq(self.tx.source.valid), tx_dp.sys.data.eq(self.tx.source.data),
            tx_dp.sys.last.eq(self.tx.source.last),   tx_dp.sys.keep.eq(2**nb - 1),
            self.tx.source.ready.eq(tx_dp.sys.ready),
            # RX: datapath RX endpoint (sys side) -> writer.sink
            self.rx.sink.valid.eq(rx_dp.sys.valid), self.rx.sink.data.eq(rx_dp.sys.data),
            self.rx.sink.last.eq(rx_dp.sys.last),    rx_dp.sys.ready.eq(self.rx.sink.ready),
            # TS: datapath TS endpoint (sys side) -> writer.sink
            self.ts.sink.valid.eq(ts_dp.sys.valid), self.ts.sink.data.eq(ts_dp.sys.data),
            self.ts.sink.last.eq(ts_dp.sys.last),    ts_dp.sys.ready.eq(self.ts.sink.ready),
        ]

        self.dp_ports = dict(
            # TX: reader.source (mem data) -> datapath s_axis_tx
            i_s_axis_tx_tdata  = tx_dp.dp.data,  i_s_axis_tx_tkeep = tx_dp.dp.keep,
            i_s_axis_tx_tvalid = tx_dp.dp.valid, i_s_axis_tx_tlast = tx_dp.dp.last,
            o_s_axis_tx_tready = tx_dp.dp.ready,
            # RX: datapath m_axis_rx -> writer.sink
            o_m_axis_rx_tdata  = rx_dp.dp.data,  o_m_axis_rx_tvalid = rx_dp.dp.valid,
            o_m_axis_rx_tlast  = rx_dp.dp.last,  i_m_axis_rx_tready = rx_dp.dp.ready,
            # TS: datapath m_axis_ts -> writer.sink
            o_m_axis_ts_tdata  = ts_dp.dp.data,  o_m_axis_ts_tvalid = ts_dp.dp.valid,
            o_m_axis_ts_tlast  = ts_dp.dp.last,  i_m_axis_ts_tready = ts_dp.dp.ready,
        )


# SoC ----------------------------------------------------------------------------------------------

class MilanSoC(SoCCore):
    def __init__(self, platform, sys_clk_freq, xlen=64, cpu_count=1,
                 with_milan=True, with_mac=False, with_dma=False, with_dram=False,
                 main_ram_size=0x8000, milan_clk_freq=None, coherent_dma=False,
                 rgmii_tx_delay=2e-9, rgmii_rx_delay=2e-9, **kwargs):
        # ---- ONE RISC-V core, MMU, Linux-capable (NaxRiscv RV64GC/sv39 or RV32/sv32) ----
        # Populate NaxRiscv's class config exactly as the CLI path does: fill a parser
        # with its own args, take the defaults, override xlen/cpu-count, then args_read
        # (this sets xlen/data_width/gcc_triple/l2/netlist-cache/update-repo/… for us).
        from litex.soc.cores.cpu.naxriscv import NaxRiscv
        _nax_parser = argparse.ArgumentParser()
        NaxRiscv.args_fill(_nax_parser)
        _nax_args, _ = _nax_parser.parse_known_args([])
        _nax_args.xlen      = xlen
        _nax_args.cpu_count = cpu_count
        # Cache-coherent DMA: NaxRiscv then exposes a snooping `dma_bus` (soc.dma_bus) that
        # the Milan DMA masters attach to, so CPU writes and DMA reads share one coherent
        # view of DRAM (see MilanDMA). Without it the DMA reads stale DRAM (HW-confirmed).
        _nax_args.with_coherent_dma = coherent_dma
        NaxRiscv.args_read(_nax_args)

        kwargs["cpu_type"]    = "naxriscv"
        kwargs["cpu_variant"] = "standard"
        kwargs["cpu_count"]   = cpu_count
        # BIOS ROM always integrated. Main RAM: external LiteDRAM (--with-dram, needed
        # for Linux) OR integrated SRAM (self-contained smoke/sim). Don't add integrated
        # main RAM when DRAM provides it.
        kwargs.setdefault("integrated_rom_size", 0x20000)   # BIOS lives here; reset vector
        if not with_dram:
            kwargs.setdefault("integrated_main_ram_size", main_ram_size)

        SoCCore.__init__(self, platform, sys_clk_freq,
                         ident=f"Milan TSN SoC - NaxRiscv RV{xlen} {cpu_count}-core",
                         **kwargs)

        self.crg = _CRG(platform, sys_clk_freq, with_dram=with_dram, with_eth=with_mac,
                        milan_clk_freq=milan_clk_freq)

        # ---- 512 MB DDR3 (LiteDRAM, A7DDRPHY + MT41J256M16) — migration §A.3 ----
        if with_dram:
            from litedram.phy import s7ddrphy
            from litedram.modules import MT41J256M16
            self.ddrphy = s7ddrphy.A7DDRPHY(platform.request("ddram"),
                memtype        = "DDR3",
                nphases        = 4,
                sys_clk_freq   = sys_clk_freq,
                iodelay_clk_freq = 200e6)
            self.add_sdram("sdram",
                phy    = self.ddrphy,
                module = MT41J256M16(sys_clk_freq, "1:4"),
                l2_cache_size = 8192)

        if with_milan:
            # AXI-Lite bridge from the CPU bus to the Milan CSR window.
            axil = axi.AXILiteInterface(data_width=32, address_width=32)
            self.bus.add_slave("milan_csr", axil,
                               region=SoCRegion(origin=MILAN_CSR_BASE, size=MILAN_CSR_SIZE,
                                                cached=False))
            # §A.6 DMA + §A.7 MAC: attach the memory-DMA and the 1G MAC/RGMII PHY at
            # the datapath's DMA/MAC-facing AXIS boundary. Both contribute Instance
            # ports; merge them (idle stubs remain for any port neither drives).
            dp_ports = {}
            milan_cd = "milan" if milan_clk_freq else "sys"
            if with_dma:
                self.milan_dma = MilanDMA(self, data_width=64, milan_cd=milan_cd)
                dp_ports.update(self.milan_dma.dp_ports)
            if with_mac:
                self.milan_mac = MilanMAC(platform, data_width=64, milan_cd=milan_cd,
                                          rgmii_tx_delay=rgmii_tx_delay,
                                          rgmii_rx_delay=rgmii_rx_delay)
                dp_ports.update(self.milan_mac.dp_ports)
            self.milan = MilanNIC(platform, axil, dma_mac_ports=dp_ports or None,
                                  milan_cd=milan_cd)
            self.irq.add("milan", use_loc_if_exists=True)  # 4 lines -> CPU via EventManager


# Build --------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Milan single-core RISC-V Linux SoC")
    ap.add_argument("--xlen", default=64, type=int, choices=[32, 64],
                    help="NaxRiscv width (64 = RV64GC/sv39 default; 32 = RV32/sv32)")
    ap.add_argument("--cpu-count",    default=1, type=int, help="number of cores (this config: 1)")
    ap.add_argument("--sys-clk-freq", default=100e6, type=float)
    ap.add_argument("--milan-clk-freq", default=None, type=float,
                    help="run the Milan datapath in its own slower clock domain (Hz, e.g. "
                         "50e6), async-FIFO CDC'd to sys on the AXI-Lite CSR bus and the "
                         "DMA/MAC AXIS boundary — lifts the dense datapath off the 100 MHz "
                         "sys critical path (it still exceeds 1 GbE). Works with --full.")
    ap.add_argument("--main-ram-size", default=0x8000, type=lambda x: int(x, 0),
                    help="integrated main RAM size (bytes)")
    ap.add_argument("--no-milan", action="store_true", help="bare SoC, no NIC (bring-up smoke test)")
    ap.add_argument("--with-mac", action="store_true",
                    help="attach the 1G MAC + RGMII PHY (§A.7) at the datapath MAC boundary")
    ap.add_argument("--with-dma", action="store_true",
                    help="attach the AXIS<->memory DMA engines (§A.6) with simple-mode CSRs")
    ap.add_argument("--with-dram", action="store_true",
                    help="512 MB DDR3 via LiteDRAM (A7DDRPHY + MT41J256M16) — needed for Linux (§A.3)")
    ap.add_argument("--coherent-dma", action="store_true",
                    help="cache-coherent DMA (NaxRiscv snooping dma_bus; needed for correct DMA content without manual cache flushes)")
    ap.add_argument("--all-blocks", "--full", dest="all_blocks", action="store_true",
                    help="enable ALL fabric blocks: NIC + DMA + MAC + DDR3 (= --with-dma "
                         "--with-mac --with-dram). This means 'every block instantiated', NOT "
                         "a complete/validated NIC — MDIO/PHY mgmt, the kl-eth driver, DMA "
                         "scatter-gather, and on-hardware traffic (M-A3..M-A5) are still open. "
                         "(--full is a legacy alias for this flag.)")
    ap.add_argument("--rgmii-tx-delay", default=2e-9, type=float,
                    help="RGMII MAC-side TX clock delay, seconds (default 2e-9).")
    ap.add_argument("--rgmii-rx-delay", default=0e-9, type=float,
                    help="RGMII MAC-side RX IDELAY, seconds (default 0 — the AX7101 PHY uses "
                         "RX-clock inversion, not IDELAY, to centre sampling; see milan_rgmii.py).")
    ap.add_argument("--uart-baudrate", default=115200, type=int,
                    help="console UART baud (default 115200; the AX7101 factory demo uses 9600)")
    ap.add_argument("--build", action="store_true", help="run vendor P&R (needs Artix-7 in Vivado)")
    ap.add_argument("--load",  action="store_true", help="program the board over JTAG (openFPGALoader -c ft232)")
    ap.add_argument("--timing-opt", action="store_true",
                    help="aggressive Vivado place/route/phys-opt directives to squeeze out "
                         "the last ns of setup slack (slower P&R; use when WNS is marginally "
                         "negative, e.g. the 100 MHz --full CBS path)")
    builder_args(ap)
    args = ap.parse_args()

    platform = alinx_ax7101.Platform()
    soc = MilanSoC(platform, int(args.sys_clk_freq), xlen=args.xlen,
                   cpu_count=args.cpu_count, with_milan=not args.no_milan,
                   with_mac=args.with_mac or args.all_blocks,
                   with_dma=args.with_dma or args.all_blocks,
                   with_dram=args.with_dram or args.all_blocks,
                   main_ram_size=args.main_ram_size,
                   milan_clk_freq=args.milan_clk_freq,
                   coherent_dma=args.coherent_dma,
                   rgmii_tx_delay=args.rgmii_tx_delay,
                   rgmii_rx_delay=args.rgmii_rx_delay,
                   uart_baudrate=args.uart_baudrate)
    builder = Builder(soc, **builder_argdict(args))
    # Aggressive timing closure (opt-in): enables the post-place phys_opt pass
    # (off by default in LiteX) and steps place/route/phys-opt up to their
    # timing-focused directives — enough to close the marginal CBS setup path at
    # 100 MHz without further RTL pipelining.
    build_kwargs = dict(
        vivado_place_directive               = "ExtraTimingOpt",
        vivado_post_place_phys_opt_directive = "AggressiveExplore",
        vivado_route_directive               = "Explore",
        vivado_post_route_phys_opt_directive = "AggressiveExplore",
    ) if args.timing_opt else {}
    builder.build(run=args.build, **build_kwargs)  # run=False => elaborate + export gateware, no Vivado
    if args.load:
        prog = platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))


if __name__ == "__main__":
    main()
