#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Verilator simulation of the Milan SoC. NOTE: this sim still uses the historical
# NaxRiscv core, whereas the published board Linux results use VexiiRiscv (RV64IMA;
# note deploy.sh still builds the naxriscv CLI default) — the CSR/mem-map
# and `milan_datapath` wiring are identical across the two, so M-A2 proven here holds.
# `milan_datapath` is attached as an AXI4-Lite CSR slave at 0x9000_0000, running
# the real LiteX BIOS. This is the board-independent proof of migration milestone
# **M-A2** — "CPU reaches milan_csr and reads ID='MILN'" — on the actual softcore
# (not just a Verilator RTL harness): boot to the BIOS prompt and `mem_read` the ID.
#
#   ./milan_sim.py                       # build + boot the sim (interactive BIOS)
#   ./milan_sim.py --non-interactive     # scripted boot-check (reads the ID)
#
# It reuses litex_sim's proven sim plumbing (SimSoC + sim Platform + serial2console)
# and milan_soc.add_milan_datapath() (the same wrapper wiring as the board SoC).
#
# XLEN: **RV32 is the default focus** — the board shape is RV32 VexiiRiscv (area;
# HANDOVER_0801 §1) and the sim core has always defaulted to `--xlen=32`. RV64 stays
# supported but is not primary: pass `--xlen=64` explicitly.
#
# Verilator multithreading: OFF by default (that is the proven M-A2 path). Opt in per
# run with VERILATOR_THREADS / VERILATOR_JOBS — see _verilator_build_kwargs() below and
# docs/testing/VIRTUAL_E2E_HOWTO.md §6.

import os
import sys
import argparse

from migen import Signal, ClockDomain, ClockSignal, ResetSignal

from litex.soc.interconnect import axi
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import Builder
from litex.build.sim.config import SimConfig

# Reuse the real sim SoC and the shared datapath wiring.
from litex.tools.litex_sim import SimSoC
sys.path.insert(0, os.path.dirname(__file__))
from milan_soc import (MILAN_CSR_BASE, MILAN_CSR_SIZE, add_milan_datapath,
                       _platform_shape)

#: The end-station config the sim borrows its window GEOMETRY from. Only the
#: geometry: see `_pp_windows_for_sim` for why the board's physical base cannot
#: come with it.
DEFAULT_CFG = "endstation_ax7101_1x1_tdm8"


def _pp_windows_for_sim(main_ram_origin, main_ram_size, cfg):
    """The protocol processor's two main-memory bases, for THIS SoC's memory.

    THE SIZE IS THE CONFIG'S, THE ADDRESS CANNOT BE. `milan_soc.py` reads both
    out of the config's platform shape because the board's DRAM reservation and
    the gateware's compiled-in base must be one declaration or they corrupt
    each other. That argument does not reach here: the sim's `main_ram` is an
    integrated on-chip SRAM a few megabytes wide, and the config's base
    (0x7F700000, the top of a 1 GiB DDR3) is not inside it - a build that took
    it verbatim would fail the containment check `milan_soc.py` applies, which
    is exactly the check that must not be weakened. So the WINDOW SIZE and the
    response buffer's offset rule are shared, and the window is placed at the
    top of whatever main memory this SoC actually has.

    Stated plainly because it bounds what this simulator can prove: the
    addresses here are the sim's, not the board's.
    """
    window = int(_platform_shape(cfg)["pp_mem"]["bytes"], 16)
    if window > main_ram_size:
        raise RuntimeError(
            f"the sim's main_ram (0x{main_ram_size:x}) is smaller than the "
            f"protocol processor's window (0x{window:x}): raise "
            f"--main-ram-size")
    desc_base = main_ram_origin + main_ram_size - window
    # same rule as the board: the buffer is the LAST 4 KiB of the same window,
    # the image grows up from the foot, and the two cannot meet
    return desc_base, desc_base + window - 0x1000


class MilanSimSoC(SimSoC):
    """SimSoC + the Milan TSN datapath as an AXI4-Lite CSR slave at 0x9000_0000."""
    def __init__(self, entity_gen_dir=DEFAULT_CFG, **kwargs):
        SimSoC.__init__(self, **kwargs)

        # AXI-Lite CSR window in the CPU IO region (uncached MMIO).
        axil = axi.AXILiteInterface(data_width=32, address_width=32)
        self.bus.add_slave("milan_csr", axil,
            region=SoCRegion(origin=MILAN_CSR_BASE, size=MILAN_CSR_SIZE, cached=False))

        # The datapath grew a dedicated audio clock input (board: 24.576 MHz MMCM,
        # cd_audio in the CRG). The sim has no MMCM and M-A2 only exercises the CSR
        # path, so the audio domain just has to resolve: drive it from sys.
        self.cd_audio = ClockDomain()
        self.comb += [
            self.cd_audio.clk.eq(ClockSignal("sys")),
            self.cd_audio.rst.eq(ResetSignal("sys")),
        ]

        # Instantiate the real wrapper (DMA/MAC ports idle — only the CSR path matters
        # for M-A2) and add its RTL so Verilator compiles it into the sim model.
        #
        # THE TWO BASES ARE NOT OPTIONAL and this file had not run since they
        # stopped being: `add_milan_datapath` RAISES rather than defaulting,
        # because the protocol processor's own placeholder base is not
        # guaranteed to be memory on any SoC that instantiates it, and a WRITE
        # master pointed at the wrong place corrupts whatever it lands on. So
        # the sim computes them from ITS memory map, the way the board SoC
        # computes them from its own.
        ram = self.bus.regions["main_ram"]
        desc_base, resp_base = _pp_windows_for_sim(ram.origin, ram.size,
                                                   entity_gen_dir)
        irq_csr = Signal()
        add_milan_datapath(self, self.platform, axil, irq_csr,
                           desc_base=desc_base, resp_base=resp_base,
                           entity_gen_dir=entity_gen_dir)

        # Fast, deterministic boot to the prompt (this sim exists to read one register).
        self.add_config("BIOS_NO_DELAYS")     # no countdowns
        self.add_config("BIOS_NO_MEMTEST")    # skip mem test/speed (slow at sim 1 MHz)


def _verilator_build_kwargs():
    """Verilator multithreading hook — the LiteX sim toolchain's own, no monkey-patch.

    `Builder.build(**kw)` forwards to `SimVerilatorToolchain.build()`, which accepts
    `threads=` and `jobs=` and turns them into `THREADS=` / `JOBS=` for
    litex/build/sim/core/Makefile:
        THREADS=N  ->  `verilator ... --threads N`   (emitted only when N > 1)
        JOBS=N     ->  `make -j$(JOBS)` of the generated model
    Nothing else in the flow reads them, so an unset env == today's build byte-for-byte.

    Defaults are deliberately the PROVEN M-A2 path (single-threaded model, unbounded
    `make -j`). Opt in per run:
        VERILATOR_THREADS=auto   -> max(2, min(nproc, 8))
        VERILATOR_THREADS=<int>  -> exact count (1 or unset = off)
        VERILATOR_JOBS=<int>     -> bound the C++ compile fan-out
    `auto` caps at 8 on purpose: `--threads` partitions the *design*, and this SoC has
    nowhere near nproc-way (128-way here) parallelism — over-threading costs more in
    barrier sync than it buys. See docs/testing/VIRTUAL_E2E_HOWTO.md §6.
    """
    kwargs = {}
    threads = os.environ.get("VERILATOR_THREADS", "").strip()
    if threads:
        n = max(2, min(os.cpu_count() or 2, 8)) if threads == "auto" else int(threads)
        if n > 1:
            kwargs["threads"] = n
    jobs = os.environ.get("VERILATOR_JOBS", "").strip()
    if jobs:
        kwargs["jobs"] = int(jobs)
    return kwargs


def main():
    ap = argparse.ArgumentParser(description="Milan SoC Verilator simulation (M-A2 proof)")
    ap.add_argument("--xlen", default=32, type=int, choices=[32, 64],
                    help="NaxRiscv width (default 32 — matches the RV32 board shape, "
                         "and a smaller/faster Verilator model; 64 = supported, not primary)")
    ap.add_argument("--non-interactive", action="store_true",
                    help="run without a BIOS console (won't read mem; for CI elaboration)")
    ap.add_argument("--output-dir", default="build_milan_sim")
    ap.add_argument("--entity-gen-dir", default=DEFAULT_CFG,
                    help="end-station config the protocol processor's window "
                         "GEOMETRY comes from (its base is this SoC's, see "
                         "_pp_windows_for_sim)")
    # Main RAM has to hold the processor's window (1 MiB at every shape in the
    # tree) on top of what the BIOS needs, so it is no longer the 64 KiB that
    # predates the descriptor store moving to main memory.
    ap.add_argument("--main-ram-size", default=0x200000, type=lambda s: int(s, 0),
                    help="integrated main_ram bytes (default 0x200000)")
    args = ap.parse_args()

    # NaxRiscv config, exactly like the board target.
    from litex.soc.cores.cpu.naxriscv import NaxRiscv
    _p = argparse.ArgumentParser(); NaxRiscv.args_fill(_p)
    _na, _ = _p.parse_known_args([]); _na.xlen = args.xlen; _na.cpu_count = 1
    NaxRiscv.args_read(_na)

    soc = MilanSimSoC(
        entity_gen_dir = args.entity_gen_dir,
        cpu_type    = "naxriscv",
        cpu_variant = "standard",
        uart_name   = "sim",
        integrated_rom_size      = 0x20000,
        integrated_main_ram_size = args.main_ram_size,
    )

    sim_config = SimConfig()
    sim_config.add_clocker("sys_clk", freq_hz=int(1e6))
    sim_config.add_module("serial2console", "serial")

    # csr.csv beside the build, not beside the source: a relative name lands in
    # whatever directory the sim happened to be launched from, and sw/litex is
    # the usual one.
    builder = Builder(soc, output_dir=args.output_dir,
                      csr_csv=os.path.join(args.output_dir, "csr.csv"))
    builder.build(sim_config=sim_config, interactive=not args.non_interactive,
                  **_verilator_build_kwargs())


if __name__ == "__main__":
    main()
