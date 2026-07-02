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

from migen import ClockDomain, ClockSignal, ResetSignal, Instance, Signal, Mux

from litex.gen import LiteXModule
from litex.soc.interconnect import stream

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
    """Clock/reset: PLL the 200 MHz board clock down to the system clock.

    With `with_eth`, also produces the 200 MHz `idelay_ref` clock + IDELAYCTRL the
    Artix-7 RGMII PHY (LiteEth s7rgmii) needs for its IODELAY calibration."""
    def __init__(self, platform, sys_clk_freq, with_eth=False):
        self.cd_sys = ClockDomain()

        clk200 = platform.request("clk200")
        rst_n  = platform.request("cpu_reset_n")

        self.pll = pll = S7PLL(speedgrade=-2)
        self.comb += pll.reset.eq(~rst_n)
        pll.register_clkin(clk200, 200e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq)
        platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin)

        if with_eth:
            # 200 MHz IDELAY reference + controller for the RGMII PHY's IODELAYs.
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
    def __init__(self, platform, axil, dma_mac_ports=None):
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
        add_milan_datapath(self, platform, axil, ev.csr.trigger, extra_ports=dma_mac_ports)


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


def add_milan_datapath(host, platform, axil, o_irq_csr, extra_ports=None):
    """Instantiate `milan_datapath` and add its RTL sources — the single place the
    wrapper is wired, reused by the board SoC (`MilanNIC`) and the sim SoC
    (`milan_sim.py`). `axil` is the AXI-Lite CSR slave; `o_irq_csr` gets the datapath
    interrupt. `extra_ports` overrides/adds Instance ports to attach the DMA (§A.6)
    and MAC (§A.7) at the exposed AXIS boundary — without it, those ports are tied
    idle (still elaborates; keeps the CPU⇄CSR path live). Instance ports for RTL
    signals already named `i_*`/`o_*` get the doubled migen prefix (e.g. milan port
    `i_i_mac_speed`, `o_o_irq_csr`) — that is correct, not a typo."""
    ports = dict(
        # clocks / reset (gtx_clk = 125 MHz for MAC-RX PTP; tied to sys until §A.4b)
        i_axis_clk    = ClockSignal("sys"),  i_axis_resetn = ~ResetSignal("sys"),
        i_gtx_clk     = ClockSignal("sys"),  i_gtx_resetn  = ~ResetSignal("sys"),
        # AXI4-Lite CSR slave (from the CPU bus bridge)
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
        # interrupt (csr aggregate; DMA-done IRQs come from §A.6)
        o_o_irq_csr = o_irq_csr,
    )
    if extra_ports:
        ports.update(extra_ports)
    host.specials += Instance("milan_datapath", **ports)
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
    def __init__(self, platform, data_width=64, phy_index=0):
        from liteeth.phy.s7rgmii import LiteEthPHYRGMII
        from liteeth.mac.core    import LiteEthMACCore

        clk_pads = platform.request("eth_clocks", phy_index)
        pads     = platform.request("eth",        phy_index)
        self.phy  = LiteEthPHYRGMII(clk_pads, pads, with_hw_init_reset=True)
        self.core = LiteEthMACCore(phy=self.phy, dw=data_width,
                                   with_preamble_crc=True, with_padding=True)

        nb = data_width // 8
        # datapath -> MAC (TX)
        tx_tdata  = Signal(data_width)
        tx_tkeep  = Signal(nb)
        tx_tvalid = Signal()
        tx_tlast  = Signal()
        tx_tready = Signal()
        # MAC -> datapath (RX)
        rx_tready = Signal()
        rx_tkeep  = Signal(nb)

        self.comb += [
            # TX AXIS (datapath) -> core.sink (LiteEth stream)
            self.core.sink.valid.eq(tx_tvalid),
            self.core.sink.data.eq(tx_tdata),
            self.core.sink.last.eq(tx_tlast),
            self.core.sink.last_be.eq(tx_tkeep),   # last-byte enable ~ tkeep of last beat
            tx_tready.eq(self.core.sink.ready),
            # RX core.source -> RX AXIS (datapath); full lanes except the last beat
            self.core.source.ready.eq(rx_tready),
            rx_tkeep.eq(Mux(self.core.source.last, self.core.source.last_be, 2**nb - 1)),
        ]

        self.dp_ports = dict(
            o_m_axis_mac_tx_tdata  = tx_tdata,  o_m_axis_mac_tx_tkeep = tx_tkeep,
            o_m_axis_mac_tx_tvalid = tx_tvalid, o_m_axis_mac_tx_tlast = tx_tlast,
            i_m_axis_mac_tx_tready = tx_tready,
            i_s_axis_mac_rx_tdata  = self.core.source.data,  i_s_axis_mac_rx_tkeep = rx_tkeep,
            i_s_axis_mac_rx_tvalid = self.core.source.valid, i_s_axis_mac_rx_tlast = self.core.source.last,
            o_s_axis_mac_rx_tready = rx_tready,
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
    def __init__(self, soc, data_width=64):
        from litex.soc.cores.dma import WishboneDMAReader, WishboneDMAWriter
        from litex.soc.interconnect import wishbone
        import math
        nb      = data_width // 8
        adr_w   = 32 - int(math.log2(nb))     # word-addressed wishbone

        def mk_bus():
            return wishbone.Interface(data_width=data_width, adr_width=adr_w, addressing="word")

        # TX: memory -> datapath (reader)
        self.tx = WishboneDMAReader(mk_bus(), with_csr=True)
        soc.bus.add_master("milan_dma_tx", master=self.tx.bus)
        # RX + TS: datapath -> memory (writers)
        self.rx = WishboneDMAWriter(mk_bus(), with_csr=True)
        soc.bus.add_master("milan_dma_rx", master=self.rx.bus)
        self.ts = WishboneDMAWriter(mk_bus(), with_csr=True)
        soc.bus.add_master("milan_dma_ts", master=self.ts.bus)

        # RX/TS output signals from the datapath -> writer sinks.
        rx_tready = Signal(); ts_tready = Signal()
        rx_data = Signal(data_width); rx_valid = Signal(); rx_last = Signal()
        ts_data = Signal(data_width); ts_valid = Signal(); ts_last = Signal()
        self.comb += [
            self.rx.sink.valid.eq(rx_valid), self.rx.sink.data.eq(rx_data),
            self.rx.sink.last.eq(rx_last),   rx_tready.eq(self.rx.sink.ready),
            self.ts.sink.valid.eq(ts_valid), self.ts.sink.data.eq(ts_data),
            self.ts.sink.last.eq(ts_last),   ts_tready.eq(self.ts.sink.ready),
        ]

        self.dp_ports = dict(
            # TX: reader.source (mem data) -> datapath s_axis_tx
            i_s_axis_tx_tdata  = self.tx.source.data,  i_s_axis_tx_tkeep = 2**nb - 1,
            i_s_axis_tx_tvalid = self.tx.source.valid, i_s_axis_tx_tlast = self.tx.source.last,
            o_s_axis_tx_tready = self.tx.source.ready,
            # RX: datapath m_axis_rx -> writer.sink
            o_m_axis_rx_tdata  = rx_data,  o_m_axis_rx_tvalid = rx_valid,
            o_m_axis_rx_tlast  = rx_last,  i_m_axis_rx_tready = rx_tready,
            # TS: datapath m_axis_ts -> writer.sink
            o_m_axis_ts_tdata  = ts_data,  o_m_axis_ts_tvalid = ts_valid,
            o_m_axis_ts_tlast  = ts_last,  i_m_axis_ts_tready = ts_tready,
        )


# SoC ----------------------------------------------------------------------------------------------

class MilanSoC(SoCCore):
    def __init__(self, platform, sys_clk_freq, xlen=64, cpu_count=1,
                 with_milan=True, with_mac=False, with_dma=False, main_ram_size=0x8000, **kwargs):
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

        self.crg = _CRG(platform, sys_clk_freq, with_eth=with_mac)

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
            if with_dma:
                self.milan_dma = MilanDMA(self, data_width=64)
                dp_ports.update(self.milan_dma.dp_ports)
            if with_mac:
                self.milan_mac = MilanMAC(platform, data_width=64)
                dp_ports.update(self.milan_mac.dp_ports)
            self.milan = MilanNIC(platform, axil, dma_mac_ports=dp_ports or None)
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
    ap.add_argument("--with-mac", action="store_true",
                    help="attach the 1G MAC + RGMII PHY (§A.7) at the datapath MAC boundary")
    ap.add_argument("--with-dma", action="store_true",
                    help="attach the AXIS<->memory DMA engines (§A.6) with simple-mode CSRs")
    ap.add_argument("--full", action="store_true",
                    help="full FPGA config: NIC + DMA + MAC (equivalent to --with-dma --with-mac)")
    ap.add_argument("--build", action="store_true", help="run vendor P&R (needs Artix-7 in Vivado)")
    ap.add_argument("--load",  action="store_true")
    builder_args(ap)
    args = ap.parse_args()

    platform = alinx_ax7101.Platform()
    soc = MilanSoC(platform, int(args.sys_clk_freq), xlen=args.xlen,
                   cpu_count=args.cpu_count, with_milan=not args.no_milan,
                   with_mac=args.with_mac or args.full,
                   with_dma=args.with_dma or args.full,
                   main_ram_size=args.main_ram_size)
    builder = Builder(soc, **builder_argdict(args))
    builder.build(run=args.build)      # run=False => elaborate + export gateware, no Vivado
    if args.load:
        prog = platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))


if __name__ == "__main__":
    main()
