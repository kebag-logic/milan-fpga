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
import json
import argparse

from migen import ClockDomain, ClockSignal, ResetSignal, Instance, Signal, Mux, If, Cat, FSM, NextValue, NextState
from migen.genlib.cdc import MultiReg

from litex.gen import LiteXModule
from litex.soc.interconnect import stream

from litex.build.io import DDROutput

from litex.soc.cores.clock import S7PLL
from litex.soc.interconnect import axi
from litex.soc.interconnect.csr import CSRStorage, CSRStatus
from litex.gen.genlib.cdc import BusSynchronizer
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

# ---- QSPI flash boot ("gain time" — skip the ~4-min serial image upload) -------------------------
# The AX7101 flash is a Micron N25Q128 = 16 MB (confirmed from the Alinx repo datasheet).
# The Linux boot images total ~23 MB (14 MB kernel Image + 8.7 MB rootfs.cpio.gz + 0.26 MB
# OpenSBI + 3 KB dtb), so they do NOT all fit in 16 MB at once. Two supported layouts:
#
#   "kernel" (DEFAULT) — flash only the big, static 14 MB kernel; the BIOS pre-loads it
#       from flash into DRAM, then serialboot uploads only OpenSBI+dtb+rootfs (~9 MB).
#       Cuts the per-boot upload ~60 %. The bitstream is JTAG-loaded (not in flash).
#   "full" — flash every image and boot with ZERO serial upload. Only fits once the
#       kernel is slimmed below ~6.5 MB (see docs/QSPI_FLASHBOOT.md).
#
# Offsets are relative to the SPIFLASH region base (resolved at run time from SPIFLASH_BASE);
# each image is written as a LiteX FBI (little-endian [length][crc32][data], via crcfbigen).
# DRAM targets match the OpenSBI fw_jump map (kernel 0x4000_0000, dtb 0x40ef_0000, OpenSBI
# 0x40f0_0000 = entry with a0=hartid/a1=0, rootfs/initrd 0x4100_0000). deploy.sh writes the
# generated <build>/flashboot_layout.json so gateware + flashing never drift.
FLASHBOOT_ENTRY = 0x40F0_0000  # OpenSBI fw_jump entry
# Flash offsets (64 KB-aligned, 16 MB device) and their DRAM targets. The kernel always
# lives at offset 0. The opensbi/dtb/rootfs offsets only apply to the "full" (zero-upload)
# manifest and assume a SLIM kernel ≤ 5.5 MB (0x58_0000) — the *un*-slimmed 14 MB kernel
# does not leave room for the 8.7 MB rootfs in 16 MB, which is exactly why "full" requires
# slimming (docs/QSPI_FLASHBOOT.md). In the default "kernel" manifest only the kernel is
# flashed, so its 14 MB span (0..0xE0_0000) is free to use these otherwise-unused offsets.
FLASHBOOT_LAYOUT = {
    #  name       flash_offset      dram_addr        budget (full layout)
    "kernel":  {"offset": 0x00_0000, "addr": 0x4000_0000},  # ≤ 5.5 MB when "full"
    "opensbi": {"offset": 0x58_0000, "addr": 0x40F0_0000},  # 256 KB
    "dtb":     {"offset": 0x5C_0000, "addr": 0x40EF_0000},  # 256 KB
    "rootfs":  {"offset": 0x60_0000, "addr": 0x4100_0000},  # up to 10 MB → ends ≤ 16 MB
}
FLASHBOOT_MANIFESTS = {
    "none":   [],
    "kernel": ["kernel"],                              # partial: pre-load kernel, serial rest
    "full":   ["opensbi", "dtb", "kernel", "rootfs"],  # zero-upload (needs a slim kernel)
}


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
    def __init__(self, platform, data_width=64, phy_index=0, milan_cd="sys",
                 gtx_tx_invert=False, **_rgmii):
        from liteeth.phy.gmii import LiteEthPHYGMII
        from liteeth.mac.core import LiteEthMACCore
        from liteeth.common import eth_phy_description
        from litex.soc.interconnect.packet import PacketFIFO

        clk_pads = platform.request("eth_clocks", phy_index)
        pads     = platform.request("eth",        phy_index)
        # The AX7101 RTL8211E is strapped for **GMII** (8-bit SDR), per the Alinx
        # example top (`input [7:0] e_rxd`, separate rxdv/rxer, gtx=rxc). An RGMII
        # (4-bit DDR) read of this bus corrupts every byte — hardware-confirmed as 100%
        # MAC preamble errors (evidence/hw_ma3_*). LiteEthPHYGMII is the right PHY.
        # (`**_rgmii` absorbs the now-unused --rgmii-*-delay knobs for API compat.)
        self.phy  = LiteEthPHYGMII(clk_pads, pads, with_hw_init_reset=True,
                                   tx_clk_invert=gtx_tx_invert)
        # GMII TX output timing is otherwise UNCONSTRAINED, so the placer may put the
        # tx_data/tx_en launch FFs anywhere: measured on silicon, FFs at SLICE_X1 (next to
        # the IO column, data-vs-gtx skew ~1-2 ns) TX 10/10 frames; FFs at SLICE_X14
        # (~4-6 ns skew) TX 0/10 — outside the RTL8211E sampling window (~(0,6) ns @ 8 ns).
        # Pack the launch FFs into the IOB so clock-to-out is pad-locked on every build.
        # Plain set_property lines only — XDC does not execute TCL `if` guards (verified:
        # a guarded version was silently skipped and the FFs stayed in fabric).
        platform.add_platform_command(
            "set_property IOB TRUE [get_ports {{eth%d_tx_data[*]}}]" % phy_index)
        platform.add_platform_command(
            "set_property IOB TRUE [get_ports eth%d_tx_en]" % phy_index)
        self.core = LiteEthMACCore(phy=self.phy, dw=data_width,
                                   with_preamble_crc=True, with_padding=True)
        # Store-and-forward TX packet FIFO (HW-root-caused 2026-07-04): the bare MACCore is
        # CUT-THROUGH and GMII has no mid-frame flow control (`tx_en = sink.valid` cycle by
        # cycle), while our DMA/datapath source can drop below 1 Gbps mid-frame (Wishbone
        # wait states) -> a single `valid` bubble becomes a tx_en glitch -> the PHY emits a
        # fragment the peer NIC discards WITHOUT counting (total silence). Sim-reproduced
        # (starved source -> 6 bubbles/frame) and sim-fixed by this FIFO: it releases a
        # frame downstream only once COMPLETELY buffered, so the drain is always gapless.
        # 512 x 8 B = 4 KB >= 2 max-size frames; 8 frame slots.
        # (Full LiteEthMAC has SRAM buffering for exactly this reason; we drive the bare
        # core, so we provide it here. docs/kl-eth-tx-debug.md #Second bug.)
        self.tx_sf = PacketFIFO(eth_phy_description(data_width),
                                payload_depth=1024, param_depth=8)
        self.comb += self.tx_sf.source.connect(self.core.sink)

        nb = data_width // 8
        L  = [("data", data_width), ("keep", nb)]
        # The datapath-facing endpoints are in `milan_cd`; the MAC core is in sys.
        # When they differ, an async-FIFO stream CDC bridges each direction (`keep`
        # carries the last-beat byte-enable). `_axis_dp_cdc` returns the endpoint the
        # datapath binds to, wiring the CDC (or a direct pass-through) to `sys_ep`.
        tx_dp = _axis_dp_cdc(self, "mac_tx_cdc", L, milan_cd, to_datapath=False)  # dp -> MAC
        rx_dp = _axis_dp_cdc(self, "mac_rx_cdc", L, milan_cd, to_datapath=True)   # MAC -> dp
        # Debug/telemetry taps (sys side): datapath->MAC-TX out and MAC-RX->datapath in.
        # `MilanDebug` also taps self.core.sink/source (LiteEth in/out) and
        # self.phy.sink/source (GMII wire, eth_tx/eth_rx).
        self.dbg_tx_dp = tx_dp.sys
        self.dbg_rx_dp = rx_dp.sys
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
            self.tx_sf.sink.data.eq(tx_dp.sys.data),
            self.tx_sf.sink.last.eq(tx_dp.sys.last),
            # `last_be` is a one-hot pointer to the last valid byte and is ONLY valid on
            # the last beat — it must be 0 on every non-last beat. LiteEth's TX last-BE
            # handler asserts end-of-frame on *any* beat with `last_be != 0`
            # (LiteEthLastHandler: `source.last = (sink.last_be != 0)`, then WAIT-LAST
            # discards the rest). Driving the highest-set-bit unconditionally put
            # `last_be = 0x80` on every beat, so the 64->8 converter tagged byte 7 of the
            # FIRST beat as last -> the frame was truncated to 8 bytes and the tail (bytes
            # 8..N) discarded. Only the dst-MAC (beat 0) survived, so wire captures showed
            # a 60-byte runt and the peer dropped it (M-A3's dst-only rx_broadcast counter
            # check masked this). Gate it by `last` so only the final beat carries last_be.
            self.tx_sf.sink.last_be.eq(Mux(tx_dp.sys.last,
                                           tx_dp.sys.keep & ~(tx_dp.sys.keep >> 1), 0)),
            If(lb,
                # internal loopback: datapath TX -> datapath RX (sys domain), both keep-masks
                rx_dp.sys.valid.eq(tx_dp.sys.valid),
                rx_dp.sys.data.eq(tx_dp.sys.data),
                rx_dp.sys.last.eq(tx_dp.sys.last),
                rx_dp.sys.keep.eq(tx_dp.sys.keep),
                tx_dp.sys.ready.eq(rx_dp.sys.ready),
                self.tx_sf.sink.valid.eq(0),     # nothing to the wire
                self.core.source.ready.eq(0),    # ignore wire RX
            ).Else(
                self.tx_sf.sink.valid.eq(tx_dp.sys.valid),
                tx_dp.sys.ready.eq(self.tx_sf.sink.ready),
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


class RingDMAWriter(LiteXModule):
    """AXIS-frame -> circular-DRAM-ring **AXI burst** DMA writer (RX upgrade v2, 2026-07-04).

    v1 (wishbone) taught two HW lessons, both measured on silicon via the pipeline
    telemetry (rx_dma: 18 stall-cycles/beat @ 50 MHz):
      1. one classic-Wishbone write per 8-byte beat costs the full coherent-bus round
         trip (~38 sys cycles) -> ~21 MB/s sustained drain vs the 125 MB/s wire. Every
         frame longer than the ~70-beat upstream elasticity (LiteEth RX CDC + datapath
         FIFOs) overflowed MID-FRAME: the GMII side cannot stall the wire, so beats —
         including `last` — vanished silently and frames merged (ping -s 600 fine,
         -s 800 dead, 100% loss).
      2. any transient sink backpressure reaches LiteEth. The DMA must be ALWAYS READY.

    v2 therefore:
      * ingress = store-and-forward frame FIFO with whole-frame drop-when-full:
        `sink.ready` is CONSTANT 1, so upstream can never overflow/corrupt. The drop
        decision is taken at frame start (reserving one max frame); dropped frames
        bump `dropped`. Frames longer than `max_frame_beats` are truncated (cannot
        happen from the MAC; safety only).
      * drain = native AXI4 burst master on the NaxRiscv coherent dma_bus (the port
        is full AXI4 — the wishbone adapter was the bottleneck, not the CPU). The
        frame length is known up front, so the header streams FIRST in the same
        burst sequence; bursts are <= `burst_beats` beats, split at the ring-wrap
        and 4 KB boundaries; `wr_ptr` only advances after the LAST B response, so
        software still never observes a partial frame.
      * ring full -> the buffered frame is discarded from the FIFO, `dropped`++.

    Ring protocol (BYTES, 8-aligned, wrap via `mask`) — UNCHANGED from v1, driver-ABI
    compatible: frame slot = 8-byte header + payload padded to 8 B; header word =
    {rsvd[31:0], seq[15:0], length[15:0]} (length = padded payload bytes); frames may
    wrap the ring end (software splits the copy).

    CSRs (7 words, same footprint/order as v1 and as the simple-mode block before it —
    the DT `dma-rx` window and every downstream CSR address stay put):
      base[64] | mask[32] | wr_ptr[32] RO | rd_ptr[32] RW | enable[1] | dropped[32] RO
    """
    def __init__(self, bus, max_frame_beats=512, fifo_beats=2048, burst_beats=16):
        self.bus  = bus                 # axi.AXIInterface(data_width=64), byte-addressed
        self.sink = sink = stream.Endpoint([("data", 64), ("keep", 8)])

        self.base    = CSRStorage(64, description="Ring base address (bytes, 8-aligned).")
        self.mask    = CSRStorage(32, description="Ring size-1 (size = power of two).")
        self.wr_ptr  = CSRStatus(32,  description="HW write pointer (committed frames).")
        self.rd_ptr  = CSRStorage(32, description="SW read pointer (consumed up to here).")
        self.enable  = CSRStorage(1,  description="Ring enable.")
        self.dropped = CSRStatus(32,  description="Whole frames dropped (ingress/ring full).")

        # # #

        drops = Signal(32)
        seq   = Signal(16)
        wr    = Signal(32)              # committed ring write offset (== wr_ptr CSR)
        self.comb += [
            self.wr_ptr.status.eq(wr),
            self.dropped.status.eq(drops),
        ]

        # ---- ingress: always-ready store-and-forward, whole-frame drop ----------------
        self.data_fifo = data_fifo = stream.SyncFIFO([("data", 64)], depth=fifo_beats, buffered=True)
        self.len_fifo  = len_fifo  = stream.SyncFIFO([("beats", 11), ("csum", 16)], depth=64)

        in_frame = Signal()             # mid-frame (first beat already seen)
        in_drop  = Signal()             # this frame is being swallowed
        in_beats = Signal(11)           # beats stored for the current frame

        # TIMING (build_ring6): the checksum adders may not load the upstream CDC
        # FIFO's BRAM output directly (BRAM clk-to-out + adder cone missed 100 MHz by
        # -0.36 ns), so the stream is registered once at entry — free, because
        # sink.ready is CONSTANT 1 (no handshake to pipeline) — and the end-of-frame
        # FOLD runs one cycle AFTER the last beat (delayed length push).
        s_valid = Signal()
        s_data  = Signal(64)
        s_last  = Signal()
        self.sync += [
            s_valid.eq(sink.valid),
            s_data.eq(sink.data),
            s_last.eq(sink.last),
        ]
        self.comb += sink.ready.eq(1)   # THE invariant: upstream is never backpressured

        # RX checksum offload (CHECKSUM_COMPLETE): ones-complement sum of ALL stored
        # bytes (16-bit LE lanes, exactly what the RISC-V kernel's csum_partial computes
        # over the same memory), accumulated as beats stream in and delivered to
        # software in the frame header's spare bits — the kernel then skips its own
        # per-byte checksum pass. Invalid last-beat lanes ARE summed on purpose: the
        # padded bytes land in the skb too, so the sum matches the skb contents
        # (pskb_trim_rcsum subtracts trimmed bytes itself).
        lanes    = Signal(18)           # this beat's four 16-bit lanes, summed
        acc      = Signal(30)           # frame accumulator (512 beats max fits easily)
        acc_fin  = Signal(30)           # final acc, registered at end-of-frame
        fold_a   = Signal(17)
        csum16   = Signal(16)

        pend       = Signal()           # a length+csum push is due (1 cycle after last)
        pend_beats = Signal(11)

        fifo_free  = Signal(max=fifo_beats + 1)
        start_drop = Signal()           # drop decision, valid on the FIRST beat only
        drop_now   = Signal()
        take       = Signal()
        self.comb += [
            fifo_free.eq(fifo_beats - data_fifo.level),
            start_drop.eq((fifo_free < max_frame_beats) | ~len_fifo.sink.ready
                          | ~self.enable.storage),
            drop_now.eq(Mux(in_frame, in_drop, start_drop)),
            # store the beat unless dropping or past the truncation cap
            take.eq(s_valid & ~drop_now & (in_beats != max_frame_beats)),
            data_fifo.sink.valid.eq(take),
            data_fifo.sink.data.eq(s_data),
            lanes.eq(s_data[0:16] + s_data[16:32] + s_data[32:48] + s_data[48:64]),
            # end-of-frame double fold, one full cycle after the final accumulate
            fold_a.eq(acc_fin[:16] + acc_fin[16:]),
            csum16.eq(fold_a[:16] + fold_a[16]),
            len_fifo.sink.valid.eq(pend),
            len_fifo.sink.beats.eq(pend_beats),
            len_fifo.sink.csum.eq(csum16),
        ]
        self.sync += [
            # a pending push completes in one cycle (the len FIFO can never be full
            # here: the frame-start drop decision reserved the slot); a new end-of-
            # frame in the same cycle just re-loads pend — the old push has completed.
            pend.eq(0),
            If(s_valid,
                If(s_last,
                    in_frame.eq(0),
                    in_drop.eq(0),
                    in_beats.eq(0),
                    acc.eq(0),
                    If(drop_now,
                        drops.eq(drops + 1),
                    ).Else(
                        pend.eq(1),
                        pend_beats.eq(Mux(in_beats != max_frame_beats, in_beats + 1,
                                          max_frame_beats)),
                        acc_fin.eq(acc + Mux(take, lanes, 0)),
                    ),
                ).Else(
                    in_frame.eq(1),
                    If(~in_frame, in_drop.eq(start_drop)),
                    If(take,
                        in_beats.eq(in_beats + 1),
                        acc.eq(acc + lanes),
                    ),
                )
            )
        ]

        # ---- drain: AXI burst engine ---------------------------------------------------
        # TIMING NOTE (silicon, build_ring4): computing the burst address/length in one
        # combinational cone (ptr + done*8 -> mask -> base+off -> 4K/wrap mins -> awlen)
        # missed 100 MHz by ~0.6 ns at 512-beat widths. So the geometry runs off a small
        # REGISTERED state instead: `off_r` (next ring offset) and `rem_r` (beats left)
        # update incrementally per burst, and a PREP state registers each burst's
        # address/length before AW. Costs 1-2 cycles per <=16-beat burst — noise.
        frame_beats = Signal(11)        # payload beats of the frame being written
        total_beats = Signal(12)        # + header (registered in IDLE)
        wcnt        = Signal(9)         # W beats sent in the current burst
        disc        = Signal(11)        # beats left to discard (ring full)
        outstanding = Signal(6)         # AW issued minus B received
        off_r       = Signal(32)        # ring byte offset of the next beat to issue
        rem_r       = Signal(12)        # beats (incl. header) not yet issued
        blen_r      = Signal(10)        # burst length, registered in PREP
        addr_r      = Signal(32)        # burst address, registered in PREP
        hdr_sent    = Signal()
        frame_csum  = Signal(16)        # ones-complement sum for CHECKSUM_COMPLETE

        # ring-fit check for the WHOLE frame (header+payload+8 spare so wr never == rd
        # when full) — evaluated in CHECK from registered frame_beats.
        used, free, need = Signal(32), Signal(33), Signal(15)
        no_fit = Signal()
        self.comb += [
            used.eq((wr - self.rd_ptr.storage) & self.mask.storage),
            free.eq(self.mask.storage + 1 - used),
            need.eq(((frame_beats + 1) << 3) + 8),
            no_fit.eq(free < need),
        ]

        # burst geometry from the REGISTERED off_r/rem_r (registered again in PREP)
        cur_addr = Signal(32)
        to_wrap  = Signal(30)           # beats to the ring end
        to_4k    = Signal(10)           # beats to the next 4 KB boundary
        blen_a   = Signal(12)
        blen_b   = Signal(12)
        blen     = Signal(12)
        self.comb += [
            cur_addr.eq(self.base.storage[:32] + off_r),
            to_wrap.eq((self.mask.storage + 1 - off_r) >> 3),
            to_4k.eq((4096 - (cur_addr & 0xFFF)) >> 3),
            blen_a.eq(Mux(rem_r > burst_beats, burst_beats, rem_r)),
            blen_b.eq(Mux(blen_a > to_wrap, to_wrap, blen_a)),
            blen.eq(Mux(blen_b > to_4k, to_4k, blen_b)),
        ]

        # W beat 0 of the whole frame is the header (length known up front); commit —
        # wr_ptr/seq — still waits for the last B, so software never sees a partial frame.
        is_hdr    = Signal()
        len_bytes = Signal(16)
        self.comb += [
            is_hdr.eq(~hdr_sent),
            len_bytes.eq(frame_beats << 3),
        ]

        aw_fire = Signal()
        self.comb += [
            aw_fire.eq(self.bus.aw.valid & self.bus.aw.ready),
            self.bus.b.ready.eq(1),
        ]
        self.sync += outstanding.eq(outstanding + aw_fire - self.bus.b.valid)

        self.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            If(len_fifo.source.valid,
                len_fifo.source.ready.eq(1),        # frame is fully buffered by now
                NextValue(frame_beats, len_fifo.source.beats),
                NextValue(total_beats, len_fifo.source.beats + 1),
                NextValue(frame_csum, len_fifo.source.csum),
                NextValue(rem_r, len_fifo.source.beats + 1),
                NextValue(off_r, wr),               # header slot first
                NextValue(hdr_sent, 0),
                NextState("CHECK"),
            )
        )
        fsm.act("CHECK",
            If(~self.enable.storage | no_fit,
                NextValue(disc, frame_beats),
                NextState("DISCARD"),
            ).Else(
                NextState("PREP"),
            )
        )
        fsm.act("PREP",                             # register this burst's geometry
            NextValue(blen_r, blen),
            NextValue(addr_r, cur_addr),
            NextState("AW"),
        )
        fsm.act("AW",
            self.bus.aw.valid.eq(1),
            self.bus.aw.addr.eq(addr_r),
            self.bus.aw.len.eq(blen_r - 1),
            self.bus.aw.size.eq(3),                 # 8 bytes/beat
            self.bus.aw.burst.eq(1),                # INCR
            If(self.bus.aw.ready,
                NextValue(wcnt, 0),
                NextValue(off_r, (off_r + (blen_r << 3)) & self.mask.storage),
                NextValue(rem_r, rem_r - blen_r),
                NextState("W"),
            )
        )
        fsm.act("W",
            self.bus.w.valid.eq(is_hdr | data_fifo.source.valid),
            self.bus.w.data.eq(Mux(is_hdr,
                Cat(len_bytes, seq, frame_csum, Signal(16)),     # {0, csum, seq, len}
                data_fifo.source.data)),
            self.bus.w.strb.eq(2**len(self.bus.w.strb) - 1),
            self.bus.w.last.eq(wcnt == blen_r - 1),
            If(self.bus.w.valid & self.bus.w.ready,
                data_fifo.source.ready.eq(~is_hdr),
                NextValue(hdr_sent, 1),
                NextValue(wcnt, wcnt + 1),
                If(self.bus.w.last,
                    If(rem_r == 0,                  # updated at AW: post-burst remaining
                        NextState("WAIT_B"),
                    ).Else(
                        NextState("PREP"),
                    )
                )
            )
        )
        fsm.act("WAIT_B",
            If(outstanding == 0,
                NextValue(wr, (wr + (total_beats << 3)) & self.mask.storage),
                NextValue(seq, seq + 1),
                NextState("IDLE"),
            )
        )
        fsm.act("DISCARD",                          # ring full/disabled: pop + count
            data_fifo.source.ready.eq(1),
            If(data_fifo.source.valid,
                NextValue(disc, disc - 1),
                If(disc == 1,
                    NextValue(drops, drops + 1),
                    NextState("IDLE"),
                )
            )
        )


class RingDMAReader(LiteXModule):
    """Circular-DRAM-ring -> AXIS-frame **AXI burst** DMA reader (TX upgrade, 2026-07-04).

    Mirror image of RingDMAWriter, replacing the simple-mode WishboneDMAReader whose
    protocol capped TX two ways (both silicon-measured):
      * one classic-Wishbone read per beat = the full coherent-bus round trip per 8 B
        (same ~38 sys-cycles as the RX writer measured) -> ~21 MB/s = ~170 Mbit/s wire
        ceiling (masked so far by the CPU-bound stack, but it also throttles ACK
        egress and thereby PEER->FPGA TCP);
      * one frame in flight with a base/length/enable CSR dance + a DONE wait per
        frame -> the driver poll cadence sat in the TX hot path.

    With the ring, software memcpys a frame into the ring, writes ONE CSR (wr_ptr)
    and returns; hardware walks rd -> wr at burst speed. ~40 MTU frames queue in a
    64 KB ring, so the NIC streams back-to-back while the CPU prepares the next.

    Ring protocol (BYTES, 8-aligned, wrap via `mask`) — same slot format as RX:
      * frame slot = 8-byte header + payload padded to 8 B;
      * header word = {rsvd[47:0], length[15:0]}, length = EXACT payload bytes — the
        last AXIS beat carries the true byte mask in `keep` (the MAC glue converts it
        to LiteEth's one-hot last_be), so wire frames are no longer 8-padded;
      * frames may wrap the ring end (bursts split there; software splits its memcpy);
      * a nonsense header (len 0 or > max_frame_bytes) can only mean a software bug:
        hardware resyncs rd := wr and drops the ring content rather than streaming
        garbage to the MAC.

    Downstream elasticity: MilanMAC's store-and-forward PacketFIFO (the TX starvation
    fix) launches a frame onto GMII only when fully buffered, so this reader may be
    arbitrarily bursty — R-channel backpressure mid-frame is harmless.

    CSRs (7 words — SAME footprint as the simple-mode block it replaces, so the DT
    `dma-tx` window and every downstream CSR address stay put; roles mirror RX):
      base[64] | mask[32] | wr_ptr[32] RW | rd_ptr[32] RO | enable[1] | sent[32] RO
    """
    def __init__(self, bus, max_frame_bytes=4096, burst_beats=16):
        self.bus    = bus               # axi.AXIInterface(data_width=64), byte-addressed
        self.source = source = stream.Endpoint([("data", 64), ("keep", 8)])

        self.base   = CSRStorage(64, description="Ring base address (bytes, 8-aligned).")
        self.mask   = CSRStorage(32, description="Ring size-1 (size = power of two).")
        self.wr_ptr = CSRStorage(32, description="SW write pointer (frames queued up to here).")
        self.rd_ptr = CSRStatus(32,  description="HW read pointer (consumed up to here).")
        self.enable = CSRStorage(1,  description="Ring enable.")
        self.sent   = CSRStatus(32,  description="Frames streamed to the datapath.")

        # # #

        rd    = Signal(32)              # HW consumption pointer (== rd_ptr CSR)
        nsent = Signal(32)
        self.comb += [
            self.rd_ptr.status.eq(rd),
            self.sent.status.eq(nsent),
        ]

        frame_bytes = Signal(16)        # exact payload bytes (from the header)
        frame_beats = Signal(11)        # ceil(bytes/8)
        rbeat       = Signal(12)        # payload beats already streamed on R
        rlast_keep  = Signal(8)
        self.comb += [
            frame_beats.eq((frame_bytes + 7)[3:]),
            # last-beat byte mask from the exact length (0 -> all 8 valid)
            rlast_keep.eq(Mux(frame_bytes[:3] == 0, 0xFF,
                              (1 << frame_bytes[:3]) - 1)),
        ]

        # burst geometry over the PAYLOAD region. Same TIMING NOTE as the writer: the
        # geometry cone runs off REGISTERED off_r/rem_r (updated incrementally per
        # burst) and each burst's address/length is registered in PREP before AR.
        off_r  = Signal(32)             # ring byte offset of the next payload beat
        rem_r  = Signal(12)             # payload beats not yet requested
        blen_r = Signal(12)             # burst length, registered in PREP
        addr_r = Signal(32)             # burst address, registered in PREP
        bcnt   = Signal(12)             # R beats received in the current burst
        cur_addr = Signal(32)
        to_wrap  = Signal(30)
        to_4k    = Signal(10)
        blen_a   = Signal(12)
        blen_b   = Signal(12)
        blen     = Signal(12)
        self.comb += [
            cur_addr.eq(self.base.storage[:32] + off_r),
            to_wrap.eq((self.mask.storage + 1 - off_r) >> 3),
            to_4k.eq((4096 - (cur_addr & 0xFFF)) >> 3),
            blen_a.eq(Mux(rem_r > burst_beats, burst_beats, rem_r)),
            blen_b.eq(Mux(blen_a > to_wrap, to_wrap, blen_a)),
            blen.eq(Mux(blen_b > to_4k, to_4k, blen_b)),
        ]

        hdr_addr = Signal(32)
        self.comb += hdr_addr.eq(self.base.storage[:32] + rd)

        self.comb += [
            self.bus.ar.size.eq(3),     # 8 bytes/beat
            self.bus.ar.burst.eq(1),    # INCR
        ]

        fb_new = Signal(11)             # ceil(len/8) of the header being parsed
        self.comb += fb_new.eq((self.bus.r.data[:16] + 7)[3:])

        self.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            If(self.enable.storage & (self.wr_ptr.storage != rd),
                NextValue(rbeat, 0),
                NextState("HDR_AR"),
            )
        )
        fsm.act("HDR_AR",
            self.bus.ar.valid.eq(1),
            self.bus.ar.addr.eq(hdr_addr),
            self.bus.ar.len.eq(0),      # single-beat header read
            If(self.bus.ar.ready,
                NextState("HDR_R"),
            )
        )
        fsm.act("HDR_R",
            self.bus.r.ready.eq(1),
            If(self.bus.r.valid,
                NextValue(frame_bytes, self.bus.r.data[:16]),
                NextValue(rem_r, fb_new),
                NextValue(off_r, (rd + 8) & self.mask.storage),
                # len==0 / oversized can only be a software bug: resync, don't stream garbage
                If((self.bus.r.data[:16] == 0) | (self.bus.r.data[:16] > max_frame_bytes),
                    NextValue(rd, self.wr_ptr.storage & self.mask.storage),
                    NextState("IDLE"),
                ).Else(
                    NextState("PREP"),
                )
            )
        )
        fsm.act("PREP",                 # register this burst's geometry
            NextValue(blen_r, blen),
            NextValue(addr_r, cur_addr),
            NextState("PAY_AR"),
        )
        fsm.act("PAY_AR",
            self.bus.ar.valid.eq(1),
            self.bus.ar.addr.eq(addr_r),
            self.bus.ar.len.eq(blen_r - 1),
            If(self.bus.ar.ready,
                NextValue(bcnt, 0),
                NextValue(off_r, (off_r + (blen_r << 3)) & self.mask.storage),
                NextValue(rem_r, rem_r - blen_r),
                NextState("PAY_R"),
            )
        )
        fsm.act("PAY_R",
            source.valid.eq(self.bus.r.valid),
            source.data.eq(self.bus.r.data),
            source.last.eq(rbeat == frame_beats - 1),
            source.keep.eq(Mux(rbeat == frame_beats - 1, rlast_keep, 0xFF)),
            self.bus.r.ready.eq(source.ready),
            If(self.bus.r.valid & self.bus.r.ready,
                NextValue(rbeat, rbeat + 1),
                NextValue(bcnt, bcnt + 1),
                If(rbeat == frame_beats - 1,            # whole frame streamed
                    NextValue(rd, (rd + 8 + (frame_beats << 3)) & self.mask.storage),
                    NextValue(nsent, nsent + 1),
                    NextState("IDLE"),
                ).Elif(bcnt == blen_r - 1,               # burst fully streamed, more to go
                    NextState("PREP"),
                )
            )
        )


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
        # TX: memory -> datapath. RingDMAReader (see its docstring) — a native AXI
        # burst master like the RX writer: software queues frames in a DRAM ring and
        # writes ONE CSR per frame; the per-frame base/length/enable+DONE dance (and
        # the ~21 MB/s per-beat wishbone ceiling) are gone. Same 7-word CSR footprint,
        # so the DT `dma-tx` window and all later CSR addresses stay put.
        self.tx = RingDMAReader(axi.AXIInterface(data_width=data_width, address_width=32,
                                                 id_width=4))
        dma_bus.add_master("milan_dma_tx", master=self.tx.bus)
        # RX: datapath -> circular DRAM ring (RingDMAWriter — see its docstring; replaces
        # the single-shot writer whose re-arm-per-frame protocol corrupted RX under load).
        # Same 7-word CSR footprint, so the DT `dma-rx` window and all later CSRs stay put.
        # NATIVE AXI master (not wishbone): the NaxRiscv coherent dma_bus is full AXI4,
        # and burst writes amortize the per-transaction coherency round trip that capped
        # the wishbone adapter at ~21 MB/s (< the 125 MB/s wire — HW-measured, see the
        # RingDMAWriter docstring). The dma_bus handler is standard "axi", so this master
        # connects through AXIInterconnectShared with bursts intact.
        self.rx = RingDMAWriter(axi.AXIInterface(data_width=data_width, address_width=32,
                                                 id_width=4))
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
            # TX: reader.source (sys) -> datapath TX endpoint. The ring reader carries
            # the exact last-beat byte mask (from the header's byte length), so wire
            # frames are no longer padded to 8 B — the MAC glue turns keep into last_be.
            tx_dp.sys.valid.eq(self.tx.source.valid), tx_dp.sys.data.eq(self.tx.source.data),
            tx_dp.sys.last.eq(self.tx.source.last),   tx_dp.sys.keep.eq(self.tx.source.keep),
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


# Debug / pipeline telemetry ----------------------------------------------------------------------

class MilanDebug(LiteXModule):
    """Memory-mapped observability for the whole TX+RX AXIS pipeline — the numbers a HW
    developer wants to localise where a frame is lost or where it queues up.

    At each pipeline stage it counts, free-running (reset via `reset`):
      * `*_frames` — completed frames (valid & ready & last). A frame present at stage N
        but missing at N+1 pinpoints the loss.
      * `*_beats`  — beats transferred (valid & ready). frames→size, beats→throughput.
      * `*_stalls` — cycles the stage was back-pressured (valid & ~ready). The bottleneck
        stage is the one with high stalls upstream of it.

    Stages (see the pipeline both ways):
      TX:  dma_out → dp_out → core_in → [LiteEth] → tx_wire (GMII)
      RX:  rx_wire (GMII) → [LiteEth] → core_out → dp_in → dma_in

    `tx_wire`/`rx_wire` count frames on the GMII pins (eth_tx/eth_rx domains, brought to
    sys with a BusSynchronizer) — the answer to "did it actually reach the wire?".

    `*_inflight_acc` accumulate Σ(in-flight) each cycle across the black-box datapath
    (in-flight = frames_in − frames_out). By Little's law: **avg occupancy = acc/cycles**
    and **avg latency (wait time) = acc/frames** — the average FIFO depth and the average
    time a frame spends crossing the datapath. `cycles` is the free-running normaliser.

    **Coherent capture.** All counters run live; writing `capture` latches EVERY counter
    into a shadow at the same clock edge, and the CSRs read the shadow. So software does:
    one write to `capture`, then read the whole set — a consistent snapshot, not values
    still moving between reads. `reset` zeroes the live counters.

    **Extensible.** The probe primitives are public methods — `sys_probe`, `wire_probe`,
    `match_probe`, `ethertype_probe`, `inflight_acc` (all auto-`snap`'d and CSR-mapped).
    Add a new observable in one line, either inline below or via the `extra(dbg)` hook,
    e.g. count gPTP frames (done here), PTP-event frames, a VLAN/PCP, a dst-MAC match, a
    drop point, another FIFO's occupancy … The gPTP TX/RX counters below are the worked
    example of `ethertype_probe`.

    **Cross-platform (LiteX vs Zynq).** This class is the **LiteX** binding — it uses
    LiteX for the LiteX-specific things: LiteX `CSRStatus` registers, `BusSynchronizer`
    for the CDC, and taps on the LiteX edges (the `WishboneDMAReader/Writer` and the
    `LiteEthPHYGMII` wire). The *shared* observables — everything at the `milan_datapath`
    AXIS boundary (tx_dp/rx_dp) and inside it — are the same on Zynq; the cross-platform
    home for those is the shared `milan_datapath.sv` counters exposed through the shared
    `milan_csr` block (0x9000_0000 on LiteX, 0x43c0_0000 on Zynq), so the Zynq wrapper
    gets them for free and only re-binds its own edges (axi_dma, its MAC). Keep new
    *datapath-internal* probes in the SV/`milan_csr` path; keep *edge/SoC-fabric* probes
    (DMA-to-memory, MAC-to-wire) in the per-platform wrapper like this one."""
    def __init__(self, dma, mac, extra=None):
        self.reset   = CSRStorage(1, description="write 1 to zero all live counters")
        self.capture = CSRStorage(1, description="write 1 to LATCH a coherent snapshot of every counter, then read them")
        self._rst = self.reset.storage
        self._cap = self.capture.re               # 1-cycle pulse on write → latch all shadows together

        cyc = Signal(64)
        self.sync += If(self._rst, cyc.eq(0)).Else(cyc.eq(cyc + 1))
        self._snap(cyc, 64, "cycles", "free-running sys cycles at capture — normaliser")

        # --- standard TX/RX stage probes (frames / beats / stalls) ---
        tx_dma = self.sys_probe("tx_dma",  dma.tx.source,   "TX: DMA read -> AXIS")
        tx_dp  = self.sys_probe("tx_dp",   mac.dbg_tx_dp,   "TX: datapath -> MAC")
        self.sys_probe("tx_core", mac.core.sink,   "TX: -> LiteEth core")
        self.sys_probe("rx_core", mac.core.source, "RX: LiteEth core ->")
        rx_dp  = self.sys_probe("rx_dp",   mac.dbg_rx_dp,   "RX: datapath -> AXIS")
        rx_dma = self.sys_probe("rx_dma",  dma.rx.sink,     "RX: -> DMA write")

        # --- wire-level GMII frame counts (eth_tx/eth_rx) ---
        phy_tx = getattr(mac.phy, "sink", None)   or getattr(getattr(mac.phy, "tx", None), "sink", None)
        phy_rx = getattr(mac.phy, "source", None) or getattr(getattr(mac.phy, "rx", None), "source", None)
        self.wire_probe("tx_wire", phy_tx, "eth_tx", "TX: frames onto the GMII wire")
        self.wire_probe("rx_wire", phy_rx, "eth_rx", "RX: frames off the GMII wire")

        # --- datapath occupancy / latency (Little's law) ---
        self.inflight_acc("tx_datapath", tx_dma, tx_dp, "TX datapath Σ in-flight/cycle (avg occ=acc/cycles, avg wait=acc/tx_dp_frames)")
        self.inflight_acc("rx_datapath", rx_dp, rx_dma, "RX datapath Σ in-flight/cycle (avg occ=acc/cycles, avg wait=acc/rx_dma_frames)")

        # --- EXAMPLE filtered probes: gPTP (802.1AS, EtherType 0x88F7) TX + RX ---
        self.ethertype_probe("tx_gptp", mac.dbg_tx_dp, 0x88F7, "TX gPTP (0x88F7) frames")
        self.ethertype_probe("rx_gptp", mac.dbg_rx_dp, 0x88F7, "RX gPTP (0x88F7) frames")

        # --- user extension hook: extra(dbg) may add any further probes ---
        if extra is not None:
            extra(self)

    # ---- probe primitives (public → extensible) --------------------------------------------
    def _snap(self, live, width, name, desc):
        """Latch `live` into a shadow on `capture` and expose it as a CSR."""
        sh = Signal(width)
        self.sync += If(self._cap, sh.eq(live))
        cs = CSRStatus(width, name=name, description=desc)
        setattr(self, name, cs)
        self.comb += cs.status.eq(sh)

    def sys_probe(self, name, ep, desc):
        """frames / beats / stalls at a sys-domain AXIS endpoint. Returns the frame counter."""
        frames, beats, stalls = Signal(32), Signal(32), Signal(32)
        self.sync += If(self._rst, frames.eq(0), beats.eq(0), stalls.eq(0)).Else(
            If(ep.valid & ep.ready & ep.last, frames.eq(frames + 1)),
            If(ep.valid & ep.ready,           beats.eq(beats + 1)),
            If(ep.valid & ~ep.ready,          stalls.eq(stalls + 1)),
        )
        self._snap(frames, 32, f"{name}_frames", f"{desc} — completed frames")
        self._snap(beats,  32, f"{name}_beats",  f"{desc} — beats (valid&ready)")
        self._snap(stalls, 32, f"{name}_stalls", f"{desc} — back-pressure cycles")
        return frames

    def wire_probe(self, name, ep, cd, desc):
        """Frame count at an endpoint in clock domain `cd`, brought to sys and captured."""
        if ep is None:
            return
        fr = Signal(32)
        getattr(self.sync, cd).__iadd__(If(ep.valid & ep.ready & ep.last, fr.eq(fr + 1)))
        bs = BusSynchronizer(32, cd, "sys"); setattr(self, f"{name}_bs", bs)
        self.comb += bs.i.eq(fr)
        self._snap(bs.o, 32, f"{name}_frames", desc)

    def match_probe(self, name, ep, match, desc):
        """Count only frames for which `match` (held over the frame) is asserted at `last`."""
        frames = Signal(32)
        self.sync += If(self._rst, frames.eq(0)).Elif(
            ep.valid & ep.ready & ep.last & match, frames.eq(frames + 1))
        self._snap(frames, 32, f"{name}_frames", desc)

    def ethertype_probe(self, name, ep, etype, desc):
        """Count frames whose (untagged) EtherType == `etype`. `ep` must carry `.data`
        (>= 64-bit): byte 12/13 = the EtherType land in beat 1 (bytes 8..15). VLAN-tagged
        frames carry it 4 bytes later — extend here if you need the tagged case."""
        # beat 1 = frame bytes 8..15; EtherType = frame bytes 12,13 = word bytes 4,5 =
        # data[32:40], data[40:48]. et = byte12<<8 | byte13 -> 0x88F7 for gPTP.
        beat, et = Signal(4), Signal(16)
        self.sync += If(ep.valid & ep.ready,
            If(ep.last, beat.eq(0)).Else(beat.eq(beat + 1)),
            If(beat == 1, et.eq(Cat(ep.data[40:48], ep.data[32:40]))),  # [7:0]=byte13, [15:8]=byte12
        )
        self.match_probe(name, ep, et == etype, desc)

    def inflight_acc(self, name, cin, cout, desc):
        """Σ(cin−cout) per cycle across a segment: avg occupancy = acc/cycles, avg wait = acc/frames."""
        acc, inflight = Signal(64), Signal(16)
        self.comb += inflight.eq(cin - cout)
        self.sync += If(self._rst, acc.eq(0)).Else(acc.eq(acc + inflight))
        self._snap(acc, 64, f"{name}_inflight_acc", desc)


# SoC ----------------------------------------------------------------------------------------------

class MilanSoC(SoCCore):
    def __init__(self, platform, sys_clk_freq, xlen=64, cpu_count=1,
                 with_milan=True, with_mac=False, with_dma=False, with_dram=False,
                 with_spiflash=False, flashboot="kernel", gtx_tx_invert=False,
                 main_ram_size=0x8000, milan_clk_freq=None, coherent_dma=False,
                 rgmii_tx_delay=2e-9, rgmii_rx_delay=2e-9, l2_bytes=None, with_fpu=False,
                 extra_scala_args=None, cpu="naxriscv",
                 **kwargs):
        # ---- RISC-V core(s), MMU, Linux-capable. Two cores are supported, selected by
        #      `cpu`: NaxRiscv (out-of-order, high IPC, ~100 MHz on this -2 Artix) or
        #      VexiiRiscv (in-order, higher fmax + smaller — the AVB-switch direction,
        #      see AVB_SWITCH_DIRECTION.md "CPU budget"). BOTH expose a coherent AXI
        #      `dma_bus` (soc.dma_bus) that the Milan DMA masters attach to identically
        #      (MilanDMA reads getattr(soc, "dma_bus", soc.bus)), and BOTH map csr @
        #      0xf000_0000 / clint @ 0xf001_0000 / plic @ 0xf0c0_0000 — so the datapath
        #      and the ring DMA port over with no address changes.
        if cpu == "vexiiriscv":
            from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
            _vex_parser = argparse.ArgumentParser()
            VexiiRiscv.args_fill(_vex_parser)
            _vex_args, _ = _vex_parser.parse_known_args([])
            # cpu_variant is a SoCCore-level arg (not in the CPU parser) — set it here.
            # "linux" = rv64imasu + sv39 MMU + L1$ + BTB/RAS/gshare (no C, no FPU);
            # "debian" additionally enables C + F + D. We use "linux" for the smallest,
            # highest-fmax Linux core (matches our no-C/no-FPU kernel); the --xlen=64 in
            # vexii-args makes it RV64 (the linux variant otherwise defaults to RV32).
            _vex_args.cpu_variant = "linux"
            _vex_args.cpu_count   = cpu_count
            _vex_args.with_dma    = coherent_dma          # coherent AXI dma_bus
            _vex_args.l2_bytes    = int(l2_bytes) if l2_bytes else 0
            vexii_extra = " ".join(extra_scala_args) if extra_scala_args else ""
            _vex_args.vexii_args  = ("--xlen=64 " + vexii_extra).strip()
            VexiiRiscv.args_read(_vex_args)
            kwargs["cpu_type"]    = "vexiiriscv"
            kwargs["cpu_variant"] = "linux"
            kwargs["cpu_count"]   = cpu_count
        else:
            # Populate NaxRiscv's class config exactly as the CLI path does: fill a parser
            # with its own args, take the defaults, override xlen/cpu-count, then args_read
            # (this sets xlen/data_width/gcc_triple/l2/netlist-cache/update-repo/… for us).
            from litex.soc.cores.cpu.naxriscv import NaxRiscv
            _nax_parser = argparse.ArgumentParser()
            NaxRiscv.args_fill(_nax_parser)
            _nax_args, _ = _nax_parser.parse_known_args([])
            _nax_args.xlen      = xlen
            _nax_args.cpu_count = cpu_count
            # Cache-coherent DMA: NaxRiscv then exposes a snooping `dma_bus` (soc.dma_bus)
            # that the Milan DMA masters attach to, so CPU writes and DMA reads share one
            # coherent view of DRAM (see MilanDMA). Without it the DMA reads stale DRAM.
            _nax_args.with_coherent_dma = coherent_dma
            # IPC knob I1 (AVB_SWITCH_DIRECTION.md): the shared L2 is BRAM and its size is
            # a pure config choice — a bigger L2 keeps the ring buffers + stack working set
            # out of DDR3 (each miss pays the full DRAM round trip on this 100 MHz core).
            if l2_bytes:
                _nax_args.l2_bytes = int(l2_bytes)
            # Hardware FPU. TWO things must happen and LiteX's --with-fpu only does the
            # first: (1) with_fpu sets the TOOLCHAIN arch/abi to rv64imafd / lp64d; (2) the
            # actual FP hardware is a NaxRiscv Scala-config option (gen.scala `arg("rvf")`
            # / `arg("rvd")`), enabled via --scala-args — WITHOUT this the softcore has NO
            # FPU even though the toolchain is hard-float (HW-confirmed 2026-07-05: misa
            # reported rv64ima and a CONFIG_FPU kernel hung on FP init). scala_args ARE in
            # the netlist hash, so this regenerates a distinct FPU netlist.
            _nax_args.with_fpu = with_fpu
            _nax_args.scala_args = list(_nax_args.scala_args or [])
            if with_fpu:
                _nax_args.scala_args += ["rvf=true,rvd=true"]
            if extra_scala_args:
                _nax_args.scala_args += list(extra_scala_args)
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

        # ---- QSPI config flash (memory-mapped) + Linux flash-boot manifest ----
        # Maps the on-board N25Q128 (16 MB) into the CPU address space so the BIOS can
        # copy boot images straight from flash into DRAM (~10 MB/s quad) instead of the
        # ~4-min 1.5 Mbaud serial upload. `flashboot` selects which images live in flash
        # (see FLASHBOOT_MANIFESTS); the emitted MILAN_FLASHBOOT_* constants drive the
        # `linux_flashboot` BIOS method (sw/litex/patches/0001-milan-linux-flashboot.patch).
        if with_spiflash:
            from litespi.modules import N25Q128A13
            from litespi.opcodes import SpiNorFlashOpCodes as SpiCodes
            # Quad read (0x6B, 3-byte addr → whole 16 MB); mode="4x" drives all four DQ so
            # WP#/HOLD# are never floating. Micron 0x6B needs no quad-enable bit.
            self.add_spi_flash(mode="4x", module=N25Q128A13(SpiCodes.READ_1_1_4),
                               with_master=True)
            self._add_flashboot_constants(flashboot)

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
                                          gtx_tx_invert=gtx_tx_invert,
                                          rgmii_tx_delay=rgmii_tx_delay,
                                          rgmii_rx_delay=rgmii_rx_delay)
                dp_ports.update(self.milan_mac.dp_ports)
            # Pipeline telemetry (memory-mapped): frame/beat/stall counts at every TX+RX
            # AXIS stage + GMII wire counts + datapath occupancy/latency + gPTP counters,
            # all coherently snapshot-latched by one `capture` write. Needs both engines.
            if with_dma and with_mac:
                self.milan_tlm = MilanDebug(self.milan_dma, self.milan_mac)
            self.milan = MilanNIC(platform, axil, dma_mac_ports=dp_ports or None,
                                  milan_cd=milan_cd)
            self.irq.add("milan", use_loc_if_exists=True)  # 4 lines -> CPU via EventManager

    def _add_flashboot_constants(self, manifest_name):
        """Emit the MILAN_FLASHBOOT_* BIOS constants for the chosen flash manifest.

        `linux_flashboot` (the patched BIOS boot method) reads, for each image in the
        manifest, `MILAN_FLASHBOOT_<IMG>_OFFSET/_ADDR` and copies it from the memory-mapped
        flash (`SPIFLASH_BASE + OFFSET`) into DRAM. If the manifest is *complete* (holds the
        whole boot set) it also emits `MILAN_FLASHBOOT_COMPLETE`, so the BIOS boots OpenSBI
        straight from flash with no serial upload; otherwise it pre-loads what it has and
        falls through to serialboot for the rest. The constants are inert (#defines nobody
        reads) unless the BIOS patch is applied — so building with --with-spiflash is safe
        either way. The layout is stored for deploy.sh in `_flashboot_layout` (written to
        <build>/flashboot_layout.json by main()), keeping gateware and flashing in lock-step.
        """
        images = FLASHBOOT_MANIFESTS[manifest_name]
        self._flashboot_layout = {"manifest": manifest_name, "entry": FLASHBOOT_ENTRY,
                                  "complete": images == FLASHBOOT_MANIFESTS["full"],
                                  "images": []}
        if not images:
            return
        for name in images:
            e = FLASHBOOT_LAYOUT[name]
            self.add_constant(f"MILAN_FLASHBOOT_{name.upper()}_OFFSET", e["offset"])
            self.add_constant(f"MILAN_FLASHBOOT_{name.upper()}_ADDR",   e["addr"])
            self._flashboot_layout["images"].append(
                {"name": name, "offset": e["offset"], "addr": e["addr"]})
        self.add_constant("MILAN_FLASHBOOT_ENTRY", FLASHBOOT_ENTRY)
        if self._flashboot_layout["complete"]:
            self.add_constant("MILAN_FLASHBOOT_COMPLETE")  # zero-upload full boot


# Build --------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Milan single-core RISC-V Linux SoC")
    ap.add_argument("--xlen", default=64, type=int, choices=[32, 64],
                    help="NaxRiscv width (64 = RV64GC/sv39 default; 32 = RV32/sv32)")
    ap.add_argument("--cpu-count",    default=1, type=int, help="number of cores (this config: 1)")
    ap.add_argument("--cpu",          default="naxriscv", choices=["naxriscv","vexiiriscv"], help="soft CPU (vexiiriscv = higher fmax, smaller — AVB-switch direction)")
    ap.add_argument("--with-fpu",     action="store_true", help="hardware FP unit (rv64imafd / lp64d)")
    ap.add_argument("--scala-args",   action="append", default=[], help="extra NaxRiscv scala args, e.g. alu-count=1,decode-count=1 (append)")
    ap.add_argument("--sys-clk-freq", default=100e6, type=float)
    ap.add_argument("--l2-bytes", default=None, type=float,
                    help="NaxRiscv shared-L2 size in bytes (default 128 KiB; IPC knob I1).")
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
    ap.add_argument("--with-spiflash", action="store_true",
                    help="memory-map the on-board N25Q128 QSPI flash (16 MB) so the BIOS can "
                         "flash-boot Linux images instead of the ~4-min serial upload (§QSPI). "
                         "Included by --all-blocks.")
    ap.add_argument("--flashboot", default="kernel", choices=["none", "kernel", "full"],
                    help="which boot images live in flash (needs --with-spiflash): 'kernel' "
                         "(default) pre-loads the 14 MB kernel from flash and serial-uploads "
                         "the rest (~60%% faster); 'full' flash-boots everything with zero "
                         "upload (only fits with a slimmed <6.5 MB kernel — see "
                         "docs/QSPI_FLASHBOOT.md); 'none' maps the flash but adds no boot method.")
    ap.add_argument("--all-blocks", "--full", dest="all_blocks", action="store_true",
                    help="enable ALL fabric blocks: NIC + DMA + MAC + DDR3 (= --with-dma "
                         "--with-mac --with-dram). This means 'every block instantiated', NOT "
                         "a complete/validated NIC — MDIO/PHY mgmt, the kl-eth driver, DMA "
                         "scatter-gather, and on-hardware traffic (M-A3..M-A5) are still open. "
                         "(--full is a legacy alias for this flag.)")
    ap.add_argument("--gtx-tx-invert", action="store_true",
                    help="forward GMII gtx_clk 180° out of phase with TXD so the PHY samples "
                         "mid-bit — the fix for the marginal GMII-TX setup/hold at the RTL8211E "
                         "(docs/kl-eth-tx-debug §GMII-TX). Default off = edge-aligned (upstream).")
    ap.add_argument("--rgmii-tx-delay", default=2e-9, type=float,
                    help="RGMII MAC-side TX clock delay, seconds (default 2e-9).")
    ap.add_argument("--rgmii-rx-delay", default=0e-9, type=float,
                    help="RGMII MAC-side RX IDELAY, seconds (default 0 — the AX7101 PHY uses "
                         "RX-clock inversion, not IDELAY, to centre sampling; see milan_rgmii.py).")
    ap.add_argument("--uart-baudrate", default=115200, type=int,
                    help="console UART baud (default 115200; the AX7101 factory demo uses 9600)")
    ap.add_argument("--build", action="store_true", help="run vendor P&R (needs Artix-7 in Vivado)")
    ap.add_argument("--load",  action="store_true", help="program the board over JTAG (openFPGALoader -c ft232)")
    ap.add_argument("--vivado-max-threads", type=int, default=min(os.cpu_count() or 1, 32),
                    help="max Vivado synth/place/route threads (set_param general.maxThreads; Vivado caps at 32)")
    ap.add_argument("--timing-opt", action="store_true",
                    help="aggressive Vivado place/route/phys-opt directives to squeeze out "
                         "the last ns of setup slack (slower P&R; use when WNS is marginally "
                         "negative, e.g. the 100 MHz --full CBS path)")
    builder_args(ap)
    args = ap.parse_args()

    platform = alinx_ax7101.Platform()
    soc = MilanSoC(platform, int(args.sys_clk_freq), xlen=args.xlen,
                   cpu_count=args.cpu_count, cpu=args.cpu, with_milan=not args.no_milan,
                   with_mac=args.with_mac or args.all_blocks,
                   with_dma=args.with_dma or args.all_blocks,
                   with_dram=args.with_dram or args.all_blocks,
                   with_spiflash=args.with_spiflash or args.all_blocks,
                   flashboot=args.flashboot,
                   gtx_tx_invert=args.gtx_tx_invert,
                   main_ram_size=args.main_ram_size,
                   milan_clk_freq=args.milan_clk_freq, l2_bytes=args.l2_bytes,
                   with_fpu=args.with_fpu, extra_scala_args=args.scala_args,
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
    # Use as many CPU cores as Vivado allows for synth/place/route (`set_param
    # general.maxThreads N`). Vivado caps this at 32 regardless of host cores, so
    # request min(cores, 32) — the rest of the box is idle during a single P&R run.
    if args.vivado_max_threads:
        build_kwargs["vivado_max_threads"] = args.vivado_max_threads
    builder.build(run=args.build, **build_kwargs)  # run=False => elaborate + export gateware, no Vivado
    # Persist the flash-boot layout so deploy.sh writes the exact same offsets the BIOS
    # was compiled with (single source of truth — see FLASHBOOT_LAYOUT / deploy.sh flash-images).
    if getattr(soc, "_flashboot_layout", None):
        layout_path = os.path.join(builder.output_dir, "flashboot_layout.json")
        with open(layout_path, "w") as f:
            json.dump(soc._flashboot_layout, f, indent=2)
        print(f"[milan] flash-boot layout ({args.flashboot}) -> {layout_path}")
    if args.load:
        prog = platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))


if __name__ == "__main__":
    main()
