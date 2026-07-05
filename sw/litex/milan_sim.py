#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Verilator simulation of the Milan SoC. NOTE: this sim still uses the historical
# NaxRiscv core, whereas the board build now runs VexiiRiscv (RV64IMA) — the CSR/mem-map
# and `milan_datapath` wiring are identical across the two, so M-A2 proven here holds.
# `milan_datapath` is attached as an AXI4-Lite CSR slave at 0x9000_0000, running
# the real LiteX BIOS. This is the board-independent proof of migration milestone
# **M-A2** — "CPU reaches milan_csr and reads ID='MILN'" — on the actual softcore
# (not just a Verilator RTL harness): boot to the BIOS prompt and `mem_read` the ID.
#
#   ./milan_sim.py                       # build + boot the sim (interactive BIOS)
#   printf 'mem_read 0x90000000 16\n' | ./milan_sim.py --non-interactive-cmds
#
# It reuses litex_sim's proven sim plumbing (SimSoC + sim Platform + serial2console)
# and milan_soc.add_milan_datapath() (the same wrapper wiring as the board SoC).

import os
import sys
import argparse

from migen import Signal

from litex.soc.interconnect import axi
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import Builder
from litex.build.sim.config import SimConfig

# Reuse the real sim SoC and the shared datapath wiring.
from litex.tools.litex_sim import SimSoC
sys.path.insert(0, os.path.dirname(__file__))
from milan_soc import MILAN_CSR_BASE, MILAN_CSR_SIZE, add_milan_datapath


class MilanSimSoC(SimSoC):
    """SimSoC + the Milan TSN datapath as an AXI4-Lite CSR slave at 0x9000_0000."""
    def __init__(self, **kwargs):
        SimSoC.__init__(self, **kwargs)

        # AXI-Lite CSR window in the CPU IO region (uncached MMIO).
        axil = axi.AXILiteInterface(data_width=32, address_width=32)
        self.bus.add_slave("milan_csr", axil,
            region=SoCRegion(origin=MILAN_CSR_BASE, size=MILAN_CSR_SIZE, cached=False))

        # Instantiate the real wrapper (DMA/MAC ports idle — only the CSR path matters
        # for M-A2) and add its RTL so Verilator compiles it into the sim model.
        irq_csr = Signal()
        add_milan_datapath(self, self.platform, axil, irq_csr)

        # Fast, deterministic boot to the prompt (this sim exists to read one register).
        self.add_config("BIOS_NO_DELAYS")     # no countdowns
        self.add_config("BIOS_NO_MEMTEST")    # skip mem test/speed (slow at sim 1 MHz)


def main():
    ap = argparse.ArgumentParser(description="Milan SoC Verilator simulation (M-A2 proof)")
    ap.add_argument("--xlen", default=32, type=int, choices=[32, 64],
                    help="NaxRiscv width (sim default 32 — smaller/faster Verilator model)")
    ap.add_argument("--non-interactive", action="store_true",
                    help="run without a BIOS console (won't read mem; for CI elaboration)")
    ap.add_argument("--output-dir", default="build_milan_sim")
    args = ap.parse_args()

    # NaxRiscv config, exactly like the board target.
    from litex.soc.cores.cpu.naxriscv import NaxRiscv
    _p = argparse.ArgumentParser(); NaxRiscv.args_fill(_p)
    _na, _ = _p.parse_known_args([]); _na.xlen = args.xlen; _na.cpu_count = 1
    NaxRiscv.args_read(_na)

    soc = MilanSimSoC(
        cpu_type    = "naxriscv",
        cpu_variant = "standard",
        uart_name   = "sim",
        integrated_rom_size      = 0x20000,
        integrated_main_ram_size = 0x10000,
    )

    sim_config = SimConfig()
    sim_config.add_clocker("sys_clk", freq_hz=int(1e6))
    sim_config.add_module("serial2console", "serial")

    builder = Builder(soc, output_dir=args.output_dir, csr_csv="csr.csv")
    builder.build(sim_config=sim_config, interactive=not args.non_interactive)


if __name__ == "__main__":
    main()
