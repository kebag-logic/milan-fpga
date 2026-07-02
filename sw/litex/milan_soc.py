#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Configurable single-core RISC-V SoC that BOOTS Linux with the Milan TSN NIC and
# its driver — the fully-FPGA target from docs/FULLY_FPGA_RISCV_MIGRATION.md,
# reduced to the smallest bootable config: ONE NaxRiscv core (MMU, Linux-capable)
# + a system clock/reset + UART + integrated RAM, with the Milan datapath wired in
# as a memory-mapped peripheral (CSR @ 0x43C0_0000 + IRQs).
#
#   ./milan_soc.py                         # elaborate + export gateware (no vendor P&R)
#   ./milan_soc.py --no-milan              # bare SoC (bring-up smoke; fully self-contained)
#   ./milan_soc.py --xlen 32               # RV32 + sv32 MMU (default RV64GC + sv39)
#   ./milan_soc.py --build                 # + run Vivado P&R -> bitstream (needs Artix-7 in Vivado)
#   ./milan_soc.py --build --load          # + program the board
#
# The Artix-7 (xc7a100t) bitstream needs Vivado with Artix-7 device support. This
# box only has Spartan-7 installed, so `--build` P&R is blocked here; gateware
# EXPORT (the default, run=False) works with no vendor tools. The CPU + full flow
# are proven by the Verilator sim boot (see sw/litex/evidence/, `litex_sim`).

import os
import sys
import argparse

from migen import ClockDomain, ClockSignal, ResetSignal, Instance

from litex.gen import LiteXModule

from litex.build.io import DDROutput

from litex.soc.cores.clock import S7PLL
from litex.soc.interconnect import axi
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
    """Clock/reset: PLL the 200 MHz board clock down to the system clock."""
    def __init__(self, platform, sys_clk_freq):
        self.cd_sys = ClockDomain()

        clk200 = platform.request("clk200")
        rst_n  = platform.request("cpu_reset_n")

        self.pll = pll = S7PLL(speedgrade=-2)
        self.comb += pll.reset.eq(~rst_n)
        pll.register_clkin(clk200, 200e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq)
        platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin)


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
    def __init__(self, platform, axil):
        # Interrupts, level-triggered, CPU-facing via the SoC IRQ handler. Four lines
        # match the DT/driver (tx/rx/ts-dma + csr); tx/rx/ts come from the §A.6 DMA
        # engine (not built yet) → held 0; csr is driven by the datapath.
        self.submodules.ev = ev = EventManager()
        ev.tx  = EventSourceLevel()
        ev.rx  = EventSourceLevel()
        ev.ts  = EventSourceLevel()
        ev.csr = EventSourceLevel()
        ev.finalize()
        self.comb += [ev.tx.trigger.eq(0), ev.rx.trigger.eq(0), ev.ts.trigger.eq(0)]

        self.specials += Instance("milan_datapath",
            # ---- clocks / reset (gtx_clk = 125 MHz for MAC-RX PTP; sys for now) ----
            i_axis_clk    = ClockSignal("sys"),  i_axis_resetn = ~ResetSignal("sys"),
            i_gtx_clk     = ClockSignal("sys"),  i_gtx_resetn  = ~ResetSignal("sys"),
            # ---- AXI4-Lite CSR slave (from the CPU bus bridge) ----
            i_s_axi_awaddr  = axil.aw.addr[:16], i_s_axi_awvalid = axil.aw.valid,
            o_s_axi_awready = axil.aw.ready,
            i_s_axi_wdata   = axil.w.data,  i_s_axi_wstrb = axil.w.strb,
            i_s_axi_wvalid  = axil.w.valid, o_s_axi_wready = axil.w.ready,
            o_s_axi_bresp   = axil.b.resp,  o_s_axi_bvalid = axil.b.valid,
            i_s_axi_bready  = axil.b.ready,
            i_s_axi_araddr  = axil.ar.addr[:16], i_s_axi_arvalid = axil.ar.valid,
            o_s_axi_arready = axil.ar.ready,
            o_s_axi_rdata   = axil.r.data,  o_s_axi_rresp = axil.r.resp,
            o_s_axi_rvalid  = axil.r.valid, i_s_axi_rready = axil.r.ready,
            # ---- TX/RX/TS DMA AXIS — §A.6 engine attaches here (idle stub) ----
            i_s_axis_tx_tdata = 0, i_s_axis_tx_tkeep = 0, i_s_axis_tx_tvalid = 0,
            i_s_axis_tx_tlast = 0,
            i_m_axis_rx_tready = 0, i_m_axis_ts_tready = 0,
            # ---- MAC-facing AXIS — §A.7 MAC attaches here (idle stub) ----
            i_m_axis_mac_tx_tready = 0,
            i_s_axis_mac_rx_tdata = 0, i_s_axis_mac_rx_tkeep = 0,
            i_s_axis_mac_rx_tvalid = 0, i_s_axis_mac_rx_tlast = 0,
            # ---- MAC status (from the external MAC; constants until §A.7) ----
            i_i_mac_speed = 0b10, i_i_link_up = 1, i_i_full_duplex = 1, i_i_mac_events = 0,
            # ---- interrupt (csr aggregate; DMA-done IRQs come from §A.6) ----
            o_o_irq_csr = ev.csr.trigger,
        )
        # RTL sources for elaboration / P&R. Curated list (NOT add_source_dir) so the
        # Zynq-only milan_top.sv / milan_dma_wrapper.v are excluded from the fabric
        # build — same file set the tb/verilator/milan_dp + syn/yosys checks use.
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # milan-fpga/
        for f in _MILAN_DATAPATH_SOURCES:
            platform.add_source(os.path.join(base, f))


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


# SoC ----------------------------------------------------------------------------------------------

class MilanSoC(SoCCore):
    def __init__(self, platform, sys_clk_freq, xlen=64, cpu_count=1,
                 with_milan=True, main_ram_size=0x8000, **kwargs):
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
        NaxRiscv.args_read(_nax_args)

        kwargs["cpu_type"]    = "naxriscv"
        kwargs["cpu_variant"] = "standard"
        kwargs["cpu_count"]   = cpu_count
        # Self-contained: integrated ROM (BIOS) + main RAM, so the SoC boots without
        # external DRAM. (A board bring-up adds LiteDRAM; not needed to prove build/boot.)
        kwargs.setdefault("integrated_rom_size",      0x20000)   # BIOS lives here; reset vector
        kwargs.setdefault("integrated_main_ram_size", main_ram_size)

        SoCCore.__init__(self, platform, sys_clk_freq,
                         ident=f"Milan TSN SoC - NaxRiscv RV{xlen} {cpu_count}-core",
                         **kwargs)

        self.crg = _CRG(platform, sys_clk_freq)

        if with_milan:
            # AXI-Lite bridge from the CPU bus to the Milan CSR window.
            axil = axi.AXILiteInterface(data_width=32, address_width=32)
            self.bus.add_slave("milan_csr", axil,
                               region=SoCRegion(origin=MILAN_CSR_BASE, size=MILAN_CSR_SIZE,
                                                cached=False))
            # The MAC (§A.7) + RGMII pads attach at the MAC-facing AXIS boundary in a
            # later step; the datapath itself no longer owns the PHY pins.
            self.milan = MilanNIC(platform, axil)
            self.irq.add("milan", use_loc_if_exists=True)  # 4 lines -> CPU via EventManager


# Build --------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Milan single-core RISC-V Linux SoC")
    ap.add_argument("--xlen", default=64, type=int, choices=[32, 64],
                    help="NaxRiscv width (64 = RV64GC/sv39 default; 32 = RV32/sv32)")
    ap.add_argument("--cpu-count",    default=1, type=int, help="number of cores (this config: 1)")
    ap.add_argument("--sys-clk-freq", default=100e6, type=float)
    ap.add_argument("--main-ram-size", default=0x8000, type=lambda x: int(x, 0),
                    help="integrated main RAM size (bytes)")
    ap.add_argument("--no-milan", action="store_true", help="bare SoC, no NIC (bring-up smoke test)")
    ap.add_argument("--build", action="store_true", help="run vendor P&R (needs Artix-7 in Vivado)")
    ap.add_argument("--load",  action="store_true")
    builder_args(ap)
    args = ap.parse_args()

    platform = alinx_ax7101.Platform()
    soc = MilanSoC(platform, int(args.sys_clk_freq), xlen=args.xlen,
                   cpu_count=args.cpu_count, with_milan=not args.no_milan,
                   main_ram_size=args.main_ram_size)
    builder = Builder(soc, **builder_argdict(args))
    builder.build(run=args.build)      # run=False => elaborate + export gateware, no Vivado
    if args.load:
        prog = platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))


if __name__ == "__main__":
    main()
