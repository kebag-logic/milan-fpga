#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Configurable single-core RISC-V SoC that BOOTS Linux with the Milan TSN NIC and
# its driver — the fully-FPGA target from docs/FULLY_FPGA_RISCV_MIGRATION.md,
# reduced to the smallest bootable config: ONE NaxRiscv core + DDR + UART + the
# Milan datapath as a memory-mapped peripheral (CSR @ 0x43C0_0000 + DMA + IRQs).
#
#   ./milan_soc.py --build                 # build the bitstream (needs Vivado + AX7101 part)
#   ./milan_soc.py --build --load          # + program the board
#   ./milan_soc.py --xlen 32               # RV32 fallback (default RV64GC)
#   ./milan_soc.py --no-milan              # bare SoC (bring-up smoke test, no NIC)
#
# Prereqs: LiteX (enjoy-digital/litex) + a platform for the Alinx AX7101
# (litex_boards or a local platform), the Milan RTL (../../hdl), the vendored
# verilog-axis (../../third_party) and verilog-ethernet (the MAC). This script is
# the *configuration*; the actual build needs that toolchain + the board.

import argparse

from migen import *

from litex.gen import LiteXModule
from litex.soc.integration.soc_core import SoCCore
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import Builder, builder_args, builder_argdict
from litex.soc.interconnect import axi
from litex.soc.interconnect.csr import AutoCSR

# The Milan CSR window (must match docs/REGISTER_MAP.md and the driver DT `reg`).
MILAN_CSR_BASE = 0x43c0_0000
MILAN_CSR_SIZE = 0x0001_0000  # 64 KB


class MilanNIC(LiteXModule, AutoCSR):
    """The Milan TSN datapath (milan_top / milan_datapath) wired into the SoC.

    Exposes: an AXI4-Lite slave (the milan_csr control plane), the RGMII pins to
    the PHY, and four interrupt lines routed to the CPU's interrupt controller.
    The RTL is added as external Verilog; here we only build the bus/IRQ glue.
    """
    def __init__(self, platform, pads, axil, irq_lines):
        self.platform = platform
        # AXI4-Lite -> milan_csr (low 16 bits decoded = register offset).
        self.specials += Instance("milan_datapath",   # PS-less wrapper (migration §A.9)
            # ---- clocks / reset ----
            i_axis_clk    = ClockSignal("sys"),
            i_axis_resetn = ~ResetSignal("sys"),
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
            # ---- RGMII to PHY0 ----
            i_rgmii_rx_clk = pads.rx_clk, i_rgmii_rxd = pads.rxd, i_rgmii_rx_ctl = pads.rx_ctl,
            o_rgmii_tx_clk = pads.tx_clk, o_rgmii_txd = pads.txd, o_rgmii_tx_ctl = pads.tx_ctl,
            o_mdc = pads.mdc, io_mdio = pads.mdio,
            # ---- interrupts: tx-dma, rx-dma, ts-dma, csr ----
            o_irq_tx = irq_lines[0], o_irq_rx = irq_lines[1],
            o_irq_ts = irq_lines[2], o_irq_csr = irq_lines[3],
            # MAC synthesis target: GENERIC/SIM off-Xilinx, XILINX on the Artix build
            p_MAC_TARGET = "XILINX",
        )
        # Add the RTL. `milan_datapath` = milan_top minus the Zynq PS wrapper.
        # (Provide it, plus the vendored cores + the verilog-ethernet MAC.)
        # platform.add_source_dir("../../hdl")
        # platform.add_source_dir("../../third_party/verilog-axis/rtl")


class MilanSoC(SoCCore):
    def __init__(self, platform, sys_clk_freq, xlen=64, cpu_count=1,
                 with_milan=True, **kwargs):
        # ---- ONE RISC-V core, MMU, Linux-capable (NaxRiscv RV64GC / RV32 fallback) ----
        kwargs["cpu_type"]     = "naxriscv"
        kwargs["cpu_variant"]  = "linux"        # MMU + supervisor
        kwargs["cpu_count"]    = cpu_count       # a single core (this config)
        SoCCore.__init__(self, platform, sys_clk_freq,
                         ident=f"Milan TSN SoC (NaxRiscv RV{xlen}, {cpu_count} core)",
                         **kwargs)
        # NaxRiscv width is selected via the CPU's --xlen; forwarded by the caller.

        if with_milan:
            # AXI-Lite bridge from the CPU bus to the Milan CSR window.
            axil = axi.AXILiteInterface(data_width=32, address_width=32)
            self.bus.add_slave("milan_csr", axil,
                               region=SoCRegion(origin=MILAN_CSR_BASE, size=MILAN_CSR_SIZE,
                                                cached=False))
            # Four interrupt lines -> the CPU interrupt controller (PLIC).
            irq = [Signal(name=n) for n in ("irq_tx", "irq_rx", "irq_ts", "irq_csr")]
            pads = platform.request("eth", 0)   # RGMII PHY0 on the AX7101
            self.milan = MilanNIC(platform, pads, axil, irq)
            for i, name in enumerate(("milan_tx", "milan_rx", "milan_ts", "milan_csr_irq")):
                self.irq.add(name, use_loc_if_exists=True)  # allocate PLIC sources
                self.comb += self.irq.pending(name).eq(irq[i]) if hasattr(self.irq, "pending") else []


def main():
    ap = argparse.ArgumentParser(description="Milan single-core RISC-V Linux SoC")
    ap.add_argument("--xlen", default=64, type=int, choices=[32, 64],
                    help="NaxRiscv width (64 = RV64GC default; 32 = RV32 fallback)")
    ap.add_argument("--cpu-count", default=1, type=int, help="number of cores (this config: 1)")
    ap.add_argument("--sys-clk-freq", default=100e6, type=float)
    ap.add_argument("--no-milan", action="store_true", help="bare SoC, no NIC (bring-up smoke test)")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--load",  action="store_true")
    builder_args(ap)
    args = ap.parse_args()

    # Board platform: the Alinx AX7101 (xc7a100t). Use a litex_boards platform or a
    # local one (see sw/README.md). Kept import-local so --help works without it.
    from litex_boards.platforms import alinx_ax7101 as board   # or a local platform
    platform = board.Platform()

    soc = MilanSoC(platform, args.sys_clk_freq, xlen=args.xlen,
                   cpu_count=args.cpu_count, with_milan=not args.no_milan)
    builder = Builder(soc, **builder_argdict(args))
    builder.build(run=args.build)
    if args.load:
        prog = platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))


if __name__ == "__main__":
    main()
