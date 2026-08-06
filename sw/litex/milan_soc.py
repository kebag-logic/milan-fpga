#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Configurable single-core RISC-V SoC that BOOTS Linux with the Milan TSN NIC and
# its driver  -  the fully-FPGA target from docs/integration/FULLY_FPGA_RISCV_MIGRATION.md. One
# NaxRiscv core (MMU, Linux-capable) + clock/reset + UART + integrated RAM, with the
# Milan datapath as a memory-mapped peripheral (CSR @ 0x9000_0000 + IRQs), and  - 
# with --full  -  the AXIS<->memory DMA (§A.6) and the 1G MAC + RGMII PHY (§A.7).
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
import re
import sys
import json
import argparse

from migen import ClockDomain, ClockDomainsRenamer, ClockSignal, ResetSignal, Instance, Signal, Mux, If, Cat, C, Array, FSM, NextValue, NextState, Memory
from migen.genlib.cdc import MultiReg
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.gen import LiteXModule
from litex.soc.interconnect import stream

from litex.build.io import DDROutput

from litex.soc.cores.clock import S7PLL, S7MMCM
from litex.soc.interconnect import axi
from litex.soc.interconnect.csr import CSRStorage, CSRStatus, CSRField
from litex.gen.genlib.cdc import BusSynchronizer
from litex.soc.interconnect.csr_eventmanager import EventManager, EventSourceLevel
from litex.soc.integration.soc_core import SoCCore
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import Builder, builder_args, builder_argdict

# Local platform (not in upstream litex_boards).
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "platforms"))
import alinx_ax7101
import board_audio_routing

# The Milan CSR window. The register OFFSETS (0x000..0x700) match docs/reference/REGISTER_MAP.md;
# only the BASE is host-specific: on this NaxRiscv SoC an MMIO peripheral must live in
# the CPU IO region (>= 0x8000_0000, uncached), so we map it at 0x9000_0000. The Zynq
# build used 0x43C0_0000. The device-tree `reg` base must match the host (see sw/README).
MILAN_CSR_BASE = 0x9000_0000
MILAN_CSR_SIZE = 0x0001_0000  # 64 KB

# On-chip BRAM PCM ring MMIO window (--pcm-ring bram). Uncached IO region just
# above the CSR window; the CPU mmaps this to read received PCM straight out of
# the dual-port BRAM (no DRAM ring, no DMA writer => the datapath's sink.ready is
# constant 1, so mf52 SHED + I6 are structurally impossible). The pcm CSR block
# (base/length/stride/enable/sel/offset) is UNCHANGED - the driver ABI is
# identical; only `base` now reads this window instead of a DRAM address. 32 KB
# = 64b x 4096 = 8 RAMB36 (mf53e has 36 free); the CSR `length` may program a
# smaller live sub-ring. DT: the pcm-ring reg node's base becomes 0x9010_0000.
MILAN_PCM_BRAM_BASE = 0x9010_0000
MILAN_PCM_BRAM_SIZE = 0x0000_8000  # 32 KB, power of two

# ---- item-4 audio-interface family: the TDM frame's arithmetic ----------------------------------
# A TDM slot is 32 bit clocks wide whatever the sample word inside it is - the
# configs' `word_length_bits: 24` means "24-in-32", which is what
# milan_datapath's AIF_WORD_BITS_C = 32 elaborates. The frame rate IS the
# sample rate, so bclk = SLOTS x 32 x fs and a bus MASTER, which toggles a
# divider to make bclk, needs a clock at 2 x that. These two constants are the
# only place that arithmetic is written on the Python side; milan_datapath
# re-derives it in SV and REFUSES any clock that is not an exact multiple, so
# the two cannot silently disagree.
AUDIO_IF_WORD_BITS = 32
AUDIO_IF_FS_HZ     = 48000

# ---- QSPI flash boot ("gain time"  -  skip the ~4-min serial image upload) -------------------------
# The AX7101 flash is a Micron N25Q128 = 16 MB (confirmed from the Alinx repo datasheet).
# The Linux boot images total ~23 MB (14 MB kernel Image + 8.7 MB rootfs.cpio.gz + 0.26 MB
# OpenSBI + 3 KB dtb), so they do NOT all fit in 16 MB at once. Two supported layouts:
#
#   "kernel" (DEFAULT)  -  flash only the big, static 14 MB kernel; the BIOS pre-loads it
#       from flash into DRAM, then serialboot uploads only OpenSBI+dtb+rootfs (~9 MB).
#       Cuts the per-boot upload ~60 %. The bitstream is JTAG-loaded (not in flash).
#   "full"  -  flash every image and boot with ZERO serial upload. Only fits once the
#       kernel is slimmed below ~6.5 MB (see docs/integration/QSPI_FLASHBOOT.md).
#
# Offsets are relative to the SPIFLASH region base (resolved at run time from SPIFLASH_BASE);
# each image is written as a LiteX FBI (little-endian [length][crc32][data], via crcfbigen).
# DRAM targets match the OpenSBI fw_jump map (kernel 0x4000_0000, dtb 0x40ef_0000, OpenSBI
# 0x40f0_0000 = entry with a0=hartid/a1=0, rootfs/initrd 0x4100_0000). deploy.sh writes the
# generated <build>/flashboot_layout.json so gateware + flashing never drift.
FLASHBOOT_ENTRY = 0x40F0_0000  # OpenSBI fw_jump entry
# Flash offsets (64 KB-aligned, 16 MB device) and their DRAM targets. The kernel always
# lives at offset 0. The opensbi/dtb/rootfs offsets only apply to the "full" (zero-upload)
# manifest and assume a SLIM kernel ≤ 5.5 MB (0x58_0000)  -  the *un*-slimmed 14 MB kernel
# does not leave room for the 8.7 MB rootfs in 16 MB, which is exactly why "full" requires
# slimming (docs/integration/QSPI_FLASHBOOT.md). In the default "kernel" manifest only the kernel is
# flashed, so its 14 MB span (0..0xE0_0000) is free to use these otherwise-unused offsets.
FLASHBOOT_LAYOUT = {
    #  name       flash_offset      dram_addr        budget (v2 QSPI-boot layout)
    # v3 (2026-07-12): QSPI-booted BITSTREAM at 0x0 (compressed, config-read;
    # flashed via `deploy.sh flash`, never fbi-wrapped) + XZ KERNEL: the slot
    # holds the kernel build's own Image.xz (MEASURED 2.52 MB, xz -9
    # --check=crc32) and the BIOS decompresses it with the vendored
    # xz_embedded (patch 0003; staged at kernel_addr+24 MB, 64 KB arena at
    # +28 MB, byte-identical decode host-proven). Budgets: bit ~2.0-2.3 MiB
    # Image.xz 2.52 MB in 3; fw_jump 261 KB in 384 KiB; rootfs
    # gets 8.5 MiB (5.6 actual — 2.9 MiB slack).
    # BIOS copies only the manifest images; the bitstream is config-read.
    "bitstream": {"offset": 0x00_0000, "addr": 0x0,          "size": 0x40_0000},
    "kernel":  {"offset": 0x40_0000, "addr": 0x4000_0000, "size": 0x30_0000},
    "opensbi": {"offset": 0x70_0000, "addr": 0x40F0_0000, "size": 0x06_0000},
    "dtb":     {"offset": 0x76_0000, "addr": 0x40EF_0000, "size": 0x02_0000},
    # v4 (2026-07-26): rootfs SHRUNK 8.5 -> 6.375 MiB to make room for the two
    # writable slots below. Measured rootfs.cpio.xz was 5.6 MiB then.
    # v5 (2026-07-28): rootfs 6.375 -> 7.375 MiB, taken back from `user`
    # (2 -> 1 MiB) because the 0x0019 image measured 8.6 MiB xz'd - the
    # PipeWire/ALSA stack plus the fast-connect tooling outgrew v4's slot -
    # and the same round prunes perf + fputest + the no-consumer libraries
    # (fpga/buildroot commit trail) to land back under this budget WITH slack.
    # ONLY the rootfs ceiling and the two reserved slots move: the four boot
    # image offsets are untouched, so a bitstream built against v4 boots the
    # same flash. `deploy.sh flash-images` prints each image's size next
    # to its budget before writing anything - READ THAT LINE, it is the
    # pre-flash check that the rootfs still fits (SAVED_STATE_FASTCONNECT.md
    # section 11 gate G0). See the OPEN ITEM note under FLASHBOOT_RESERVED.
    "rootfs":  {"offset": 0x78_0000, "addr": 0x4100_0000, "size": 0x76_0000},
}
FLASHBOOT_MANIFESTS = {
    "none":   [],
    "kernel": ["kernel"],                              # partial: pre-load kernel, serial rest
    "full":   ["opensbi", "dtb", "kernel", "rootfs"],  # zero-upload (needs a slim kernel)
}

# Writable slots. NOT boot images: the BIOS never copies them, deploy.sh never
# writes them, and `build.sh flash` / `deploy.sh flash-images` MUST NOT erase
# them on a reflash - a gateware update that silently wipes saved bindings and
# fault logs is worse than not having them, because the entity then comes back
# unbound *sometimes*.  They are declared here so that the flash map has ONE
# source of truth (docs/design/SAVED_STATE_FASTCONNECT.md section 5) and so that
# sw/dts/gen_mtd_partitions.py can derive the kernel's `fixed-partitions` node
# from it instead of a second hand-maintained copy.
#
#   journal  2 x 64 KiB erase blocks = slot A / slot B, RAW (no filesystem):
#            "a torn write cannot damage the other slot" is then a property of
#            the flash geometry, not a promise from a log-structured fs, and the
#            slot is readable before any mount.
#   user     jffs2, mounted at /user: entity/group names, channel maps, mixer
#            state, and /user/log - the rotating xz CTF fault log
#            (docs/design/TRACE_LOGGING.md).
#
# OPEN ITEM (deliberately not fixed here - deploy.sh is not this change's file):
# deploy.sh derives each image's ceiling from the NEXT image offset in
# flashboot_layout.json, and the reserved slots are exported under a separate
# "reserved" key that it does not read.  So its printed rootfs budget is still
# 16 MiB - 0x78_0000 and an oversized rootfs would be accepted and would
# overwrite `journal`/`user`.  The one-line fix is for do_flash_images() to
# prefer an image's own `budget` field (now exported below) over the
# next-offset computation.  Until then the rootfs `size` above is the number to
# check by hand.
FLASH_SIZE        = 0x100_0000   # 16 MiB (N25Q128A13 / S25FL128S)
FLASH_ERASE_BLOCK = 0x1_0000     # 64 KiB - the unit of erase, and of slot alignment
FLASHBOOT_RESERVED = {
    # v5 (2026-07-28): both slots slid up 1 MiB when the rootfs ceiling grew
    # (see the v5 note above); `user` paid, 2 -> 1 MiB. 1 MiB = 16 erase
    # blocks - jffs2 wants >= 5 free for GC, so the fault log rotates sooner
    # but the filesystem stays comfortable. Nothing had ever been flashed at
    # the v4 offsets (the journal/user map ships FOR THE FIRST TIME with
    # 0x0019), so there is no migration - but any board that DOES someday
    # move across maps loses its saved bindings and starts clean, which the
    # fabric's CRC/shape verification turns into "no restore", never a
    # half-restore.
    "journal": {"offset": 0xEE_0000, "size": 0x02_0000},   # 128 KiB, raw A/B
    "user":    {"offset": 0xF0_0000, "size": 0x10_0000},   # 1 MiB, jffs2 -> /user
}


def flash_map():
    """Every slot on the device, ordered by offset: [(name, offset, size, kind)].

    The single reader of both dicts.  `kind` is "image" for anything the BIOS
    or deploy.sh transfers and "reserved" for the writable slots.
    """
    rows = [(n, e["offset"], e["size"], "image")
            for n, e in FLASHBOOT_LAYOUT.items()]
    rows += [(n, e["offset"], e["size"], "reserved")
             for n, e in FLASHBOOT_RESERVED.items()]
    return sorted(rows, key=lambda r: r[1])


def check_flash_map():
    """Return a list of problems with the flash map; empty means consistent.

    Erase-block alignment is not cosmetic: an mtd partition that starts or ends
    mid-block cannot be erased without destroying its neighbour, which would
    turn "write the journal" into "corrupt the rootfs".
    """
    problems, prev_end, prev_name = [], 0, None
    for name, off, size, _kind in flash_map():
        if size <= 0:
            problems.append(f"{name}: non-positive size {size}")
        if off % FLASH_ERASE_BLOCK:
            problems.append(f"{name}: offset 0x{off:X} is not erase-block aligned")
        if size % FLASH_ERASE_BLOCK:
            problems.append(f"{name}: size 0x{size:X} is not an erase-block multiple")
        if off < prev_end:
            problems.append(f"{name} @0x{off:X} overlaps {prev_name} "
                            f"(ends 0x{prev_end:X})")
        if off + size > FLASH_SIZE:
            problems.append(f"{name}: ends 0x{off + size:X}, past the "
                            f"0x{FLASH_SIZE:X} device")
        prev_end, prev_name = off + size, name
    return problems


# CRG ----------------------------------------------------------------------------------------------

class _CRG(LiteXModule):
    """Clock/reset: PLL the 200 MHz board clock down to the system clock.

    With `with_dram`, also produces the DDR3 PHY clocks (`sys4x`, `sys4x_dqs`); with
    `with_dram` or `with_eth`, the 200 MHz `idelay` reference + IDELAYCTRL that both
    the Artix-7 DDR3 PHY (A7DDRPHY) and the RGMII PHY (LiteEth s7rgmii) need for their
    IODELAY calibration."""
    def __init__(self, platform, sys_clk_freq, with_dram=False, with_eth=False,
                 milan_clk_freq=None, board="ax7101", audio_tdm_hz=None):
        self.cd_sys = ClockDomain()

        # Board clocking: AX7101 = 200 MHz differential + active-low reset button,
        # speedgrade -2. Arty A7-100 = 100 MHz single-ended + cpu_reset button,
        # speedgrade -1, and the DP83848 MII PHY needs a 25 MHz reference OUT
        # (eth_ref_clk pin -> PHY X1), produced below when with_eth.
        if board == "arty":
            clkin, clkin_freq = platform.request("clk100"), 100e6
            self.pll = pll = S7PLL(speedgrade=-1)
        else:
            clkin, clkin_freq = platform.request("clk200"), 200e6
            self.pll = pll = S7PLL(speedgrade=-2)
        rst_n = platform.request("cpu_reset_n")
        self.comb += pll.reset.eq(~rst_n)
        pll.register_clkin(clkin, clkin_freq)
        pll.create_clkout(self.cd_sys, sys_clk_freq)
        platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin)

        if board == "arty" and with_eth:
            self.cd_eth_ref = ClockDomain(reset_less=True)
            pll.create_clkout(self.cd_eth_ref, 25e6)
            self.comb += platform.request("eth_ref_clk").eq(ClockSignal("eth_ref"))

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

            # CLEAN audio clock (07-18): the CS4344 needs a ~ps-jitter MCLK -
            # the fractional-N divider's +-1-cycle edge jitter measured
            # THD+N -4.5 dB analog. The I2S serializer divides MCLK
            # /2 /8 /512 in clean registers. Rate mismatch vs the talker's
            # 48 kHz = counted slips (USER internal-clock rule) until the
            # CRF servo below pulls it in.
            #
            # MMCM-DRP media-clock servo plan (2026-07-22, roadmap item 6):
            # the audio MMCM is now the ACTUATOR of the CRF media-clock
            # servo (hdl/ieee1722/crf/KL_mmcm_drp_servo.sv). The fine,
            # glitch-free knob is the MMCME2 dynamic fine phase shift
            # (UG472: steps of 1/(56*F_VCO), PSDONE after exactly 12 PSCLK
            # cycles, round-robin wrap = a sustained step rate is a
            # permanent frequency trim), and UG472 forbids fractional
            # divide in fine-PS mode. So the audio clock is INTEGER-ONLY,
            # produced deterministically in two stages (best single-stage
            # integer ratio from 100 MHz is 43/175 = -186 ppm, beyond the
            # PS slew budget; two stages reach -10.6 ppm):
            #   pre-PLL : 100 MHz /2 x23      -> VCO 1150 MHz, /37 -> 31.081081 MHz
            #   MMCM    : 31.081081 /1 x34    -> VCO 1056.7568 MHz (DS181 -1:
            #             600-1200), /43      -> 24.575739 MHz = 24.576 MHz - 10.6 ppm
            # PS step = 1/(56*1056.76 MHz) = 16.9 ps; PSCLK = 200 MHz idelay
            # (DS181 MMCM_FMAX_PSCLK 450 MHz at -1) -> sustained-slew ceiling
            # (200e6/13)*16.9ps = 260 ppm, covering base 10.6 + talker 100 ppm
            # with >2x margin. DRP DCLK = the milan clock (DS181 FDCK <= 200 MHz).
            # Both boards run the same 100 MHz-referenced plan (Arty: clk100
            # pad - a second load on the pad is fine, silicon-proven mf14-17;
            # AX: cascade from the buffered sys clock - a second IBUFDS on the
            # clk200 pads is Place 30-475 unplaceable, AX13 2026-07-18).
            # BANDWIDTH=LOW on the MMCM filters the cascade jitter (UG472
            # "Jitter Filter"); bench THD+N re-check is on the bring-up list.
            #
            # ITEM-4 TDM MASTER PLAN (2026-07-28, `audio_tdm_hz`). A TDM bus
            # MASTER generates its own bit clock, and bclk = SLOTS x 32 x fs:
            #   TDM8  x 32 @ 48k -> 12.288 MHz -> clk_tdm 24.576 MHz
            #   TDM16 x 32 @ 48k -> 24.576 MHz -> clk_tdm 49.152 MHz
            #   TDM32 x 32 @ 48k -> 49.152 MHz -> clk_tdm 98.304 MHz
            # (the master toggles a divider, so its clock is 2 x bclk). The
            # 24.576 MHz cd_audio CANNOT be re-rated to reach those: it is
            # 24.576 MHz BY CONTRACT - KL_crf_tx divides it /512 for the 48 kHz
            # CRF event, KL_i2s_playback /2 /8 /512 for the DAC, and
            # KL_mmcm_drp_servo measures it. So the master gets its OWN MMCM
            # OUTPUT off the SAME VCO, and the two-stage integer chain is
            # re-derived so one VCO serves both:
            #   pre-PLL : 100 MHz /2 x23      -> VCO 1150 MHz (UNCHANGED),
            #             /67                 -> 17.164179 MHz  (was /37)
            #   MMCM    : 17.164179 /1 x63    -> VCO 1081.3433 MHz (600-1200 ok)
            #             CLKOUT0 /44         -> 24.575984 MHz = -0.66 ppm
            #             CLKOUT1 /44,/22,/11 -> 24.576 / 49.152 / 98.304 MHz
            # The audio clock gets BETTER, not worse: -0.66 ppm against the
            # -10.64 ppm of the default plan, because 44 divides the new VCO
            # where 43 (odd) could never yield an integer 2x or 4x sibling.
            # PS step = 1/(56*1081.34 MHz) = 16.51 ps (was 16.90), so the
            # sustained-slew ceiling is (200e6/13)*16.51ps = 254 ppm (was 260)
            # - still base 0.66 + talker 100 ppm with >2x margin. CLKOUT1 also
            # carries USE_FINE_PS so the servo trims BOTH outputs together
            # (UG472: the phase shift applies to every CLKOUTx that asks for
            # it); a capture clock the media-clock servo could not reach would
            # be a talker that ignores its own recovered media clock.
            #
            # DEFAULT (audio_tdm_hz None) KEEPS PLAN A BIT-FOR-BIT: this is a
            # clocking change, and a clocking change that happened merely
            # because a parameter now exists would move every bench number
            # measured through the DAC (-72.7 dB analog loop, THD+N) on builds
            # that never asked for a TDM master.
            self.cd_audio = ClockDomain()
            audio_in = clkin if board == "arty" else ClockSignal("sys")
            audio_src_hz = clkin_freq if board == "arty" else sys_clk_freq
            if audio_tdm_hz is None:
                pre_div, mmcm_mult, audio_div = 37, 34.0, 43.0   # PLAN A
            else:
                pre_div, mmcm_mult, audio_div = 67, 63.0, 44.0   # PLAN B
                _vco2 = audio_src_hz * 23 / 2 / pre_div * mmcm_mult
                tdm_div = round(_vco2 / audio_tdm_hz)
                if abs(_vco2 / tdm_div - audio_tdm_hz) / audio_tdm_hz > 20e-6:
                    raise ValueError(
                        f"_CRG: audio_tdm_hz={audio_tdm_hz} is not an integer "
                        f"divide of the audio MMCM VCO {_vco2/1e6:.6f} MHz "
                        f"(nearest /{tdm_div} = {_vco2/tdm_div/1e6:.6f} MHz). "
                        f"The TDM master's frame rate would not be 48 kHz. "
                        f"Supported: 24.576e6 (TDM8), 49.152e6 (TDM16), "
                        f"98.304e6 (TDM32), all x 32-bit slots at 48 kHz.")
                self.cd_audio_tdm = ClockDomain()
            pll_audio_fb  = Signal()
            audio_ref_raw = Signal()
            audio_ref     = Signal()
            self.specials += Instance("PLLE2_ADV", name="pll_audio_pre",
                p_STARTUP_WAIT="FALSE", p_BANDWIDTH="OPTIMIZED",
                p_REF_JITTER1=0.01, p_CLKIN1_PERIOD=1e9/clkin_freq if board == "arty" else 1e9/sys_clk_freq,
                p_DIVCLK_DIVIDE=2, p_CLKFBOUT_MULT=23,   # PFD 50 MHz, VCO 1150 MHz
                p_CLKOUT0_DIVIDE=pre_div, p_CLKOUT0_PHASE=0.0,  # 31.081081 / 17.164179 MHz
                i_CLKIN1=audio_in, i_RST=~rst_n, i_PWRDWN=0,
                i_CLKFBIN=pll_audio_fb, o_CLKFBOUT=pll_audio_fb,
                o_CLKOUT0=audio_ref_raw,
            )
            self.specials += Instance("BUFG", i_I=audio_ref_raw, o_O=audio_ref)
            # KL_mmcm_drp_servo <-> MMCME2_ADV wiring (through milan_datapath)
            self.audio_drp_addr   = Signal(7)
            self.audio_drp_en     = Signal()
            self.audio_drp_we     = Signal()
            self.audio_drp_di     = Signal(16)
            self.audio_drp_do     = Signal(16)
            self.audio_drp_rdy    = Signal()
            self.audio_mmcm_rst   = Signal()
            self.audio_mmcm_locked= Signal()
            self.audio_ps_en      = Signal()
            self.audio_ps_incdec  = Signal()
            self.audio_ps_done    = Signal()
            self.audio_ps_clk     = ClockSignal("idelay") if (with_dram or with_eth) else ClockSignal("sys")
            mmcm_audio_fb  = Signal()
            audio_mclk_raw = Signal()
            mmcm_ports = dict(
                p_STARTUP_WAIT="FALSE", p_BANDWIDTH="LOW",
                p_REF_JITTER1=0.01,
                p_CLKIN1_PERIOD=1e9/(audio_src_hz*23/(2*pre_div)),
                p_DIVCLK_DIVIDE=1, p_CLKFBOUT_MULT_F=mmcm_mult,
                p_CLKOUT0_DIVIDE_F=audio_div, p_CLKOUT0_PHASE=0.0,
                p_CLKOUT0_USE_FINE_PS="TRUE",               # UG472 dynamic fine PS
                i_CLKIN1=audio_ref, i_RST=self.audio_mmcm_rst, i_PWRDWN=0,
                i_CLKFBIN=mmcm_audio_fb, o_CLKFBOUT=mmcm_audio_fb,
                o_CLKOUT0=audio_mclk_raw, o_LOCKED=self.audio_mmcm_locked,
                # DRP port (DCLK = milan clock; XAPP888 sequencing in the servo)
                i_DCLK=ClockSignal("milan"), i_DADDR=self.audio_drp_addr,
                i_DEN=self.audio_drp_en, i_DWE=self.audio_drp_we,
                i_DI=self.audio_drp_di, o_DO=self.audio_drp_do,
                o_DRDY=self.audio_drp_rdy,
                # dynamic fine phase shift port (UG472)
                i_PSCLK=self.audio_ps_clk, i_PSEN=self.audio_ps_en,
                i_PSINCDEC=self.audio_ps_incdec, o_PSDONE=self.audio_ps_done,
            )
            audio_tdm_raw = Signal()
            if audio_tdm_hz is not None:
                # CLKOUT1 = the item-4 TDM MASTER serial-domain clock. FINE_PS
                # on as well so the media-clock servo trims the capture bit
                # clock and the DAC clock TOGETHER - they are the same media
                # clock seen at two rates, and a capture front-end the servo
                # cannot reach would free-run against the stream it feeds.
                mmcm_ports.update(p_CLKOUT1_DIVIDE=tdm_div, p_CLKOUT1_PHASE=0.0,
                                  p_CLKOUT1_USE_FINE_PS="TRUE",
                                  o_CLKOUT1=audio_tdm_raw)
            self.specials += Instance("MMCME2_ADV", name="mmcm_audio",
                                      **mmcm_ports)
            self.specials += Instance("BUFG", i_I=audio_mclk_raw, o_O=self.cd_audio.clk)
            # audio-domain reset while the MMCM is unlocked (incl. during a
            # servo DRP repair - the clock-outage sequencing class shared
            # with the link-guard GMII CDC reinit)
            self.specials += AsyncResetSynchronizer(self.cd_audio, ~self.audio_mmcm_locked)
            platform.add_false_path_constraints(self.cd_sys.clk,   self.cd_audio.clk)
            platform.add_false_path_constraints(self.cd_milan.clk, self.cd_audio.clk)
            if audio_tdm_hz is not None:
                self.specials += Instance("BUFG", i_I=audio_tdm_raw,
                                          o_O=self.cd_audio_tdm.clk)
                self.specials += AsyncResetSynchronizer(
                    self.cd_audio_tdm, ~self.audio_mmcm_locked)
                platform.add_false_path_constraints(self.cd_sys.clk,
                                                    self.cd_audio_tdm.clk)
                platform.add_false_path_constraints(self.cd_milan.clk,
                                                    self.cd_audio_tdm.clk)
                platform.add_false_path_constraints(self.cd_audio.clk,
                                                    self.cd_audio_tdm.clk)

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
    and minus the MAC)  -  a real, Verilator+Yosys-verified module (tb/verilator/
    milan_dp, syn/yosys). It exposes:
      * an AXI4-Lite CSR slave (milan_csr control plane)  -  wired here to the CPU bus;
      * three DMA AXIS ports (tx from DRAM / rx to DRAM / ts to DRAM)  -  the §A.6 DMA
        engine attaches here (stubbed idle for now);
      * a MAC-facing AXIS pair + MAC cfg/status  -  the §A.7 MAC (LiteEth `LiteEthMAC`
        or Forencich `eth_mac_1g_rgmii_fifo` + RGMII PHY) attaches here (stubbed);
      * `o_irq_csr` (link/PTP/RMON aggregate)  -  routed to the PLIC below.

    This makes the SoC instantiate REAL RTL (no black box). The DMA + MAC attach are
    the next migration steps (§A.6/§A.7); until then their AXIS ports are tied idle,
    which still elaborates and exports gateware and keeps the CPU⇄CSR path live
    (proven end-to-end in tb/verilator/milan_dp: CPU reads ID="MILN", M-A2).
    """
    def __init__(self, platform, axil, dma_mac_ports=None, milan_cd="sys", rx_irq=None,
                 rx1_irq=None, milan_clk_hz=100_000_000, num_streams=1,
                 audio_if_slots=0, talker_wire_chans=2, audio_if_master=False,
                 audio_if_i2s_pair=False, aaf_playback=False, aaf_pb_streams=1,
                 loopback_lane=False,
                 render_lpf=True, optional_blocks=None,
                 cbs_queues_mask=None, entity_gen_dir=None):
        # Interrupts, level-triggered, CPU-facing via the SoC IRQ handler. Four lines
        # match the DT/driver (tx/rx/ts-dma + csr); tx/ts come from the §A.6 DMA engine
        # (held 0 until attached); csr is driven by the datapath.
        self.submodules.ev = ev = EventManager()
        ev.tx  = EventSourceLevel()
        ev.rx  = EventSourceLevel()
        ev.ts  = EventSourceLevel()
        ev.csr = EventSourceLevel()
        ev.finalize()
        # ev.rx = RX-completion interrupt: level-high while the RX ring is non-empty
        # (RingDMAWriter.non_empty, sys domain  -  same as ev, no CDC), so the driver delivers
        # on arrival (interrupt-driven NAPI) instead of the hrtimer poll. 0 when no DMA.
        # ev.tx is unused by the DMA reader (TX has no completion IRQ  -  the driver
        # reaps in NAPI), so the RX fan-out reuses it as RX-queue-1's completion line.
        self.comb += [ev.tx.trigger.eq(rx1_irq if rx1_irq is not None else 0),
                      ev.rx.trigger.eq(rx_irq if rx_irq is not None else 0),
                      ev.ts.trigger.eq(0)]
        # AECP IDENTIFY control level (Milan FR-MGT-01) - wired to a board LED
        # by the SoC so a controller's "identify" visibly blinks the device.
        self.identify = Signal()
        add_milan_datapath(self, platform, axil, ev.csr.trigger,
                           extra_ports=dict(dma_mac_ports or {}, o_o_identify=self.identify),
                           milan_cd=milan_cd,
                           milan_clk_hz=milan_clk_hz, num_streams=num_streams,
                           audio_if_slots=audio_if_slots,
                           talker_wire_chans=talker_wire_chans,
                           audio_if_master=audio_if_master,
                           audio_if_i2s_pair=audio_if_i2s_pair,
                           aaf_playback=aaf_playback, aaf_pb_streams=aaf_pb_streams,
                           loopback_lane=loopback_lane,
                           render_lpf=render_lpf, optional_blocks=optional_blocks,
                           cbs_queues_mask=cbs_queues_mask,
                           entity_gen_dir=entity_gen_dir)


# The milan_datapath source set (ordered: packages first). Mirrors the milan_dp
# Verilator Makefile and the syn/yosys entry  -  the single source of truth for what
# the §A.9 wrapper is built from.
_MILAN_DATAPATH_SOURCES = [
    "hdl/common/ethernet_packet_pkg.sv", "hdl/common/axi_stream_if.sv", "hdl/ieee17221/adp/adp_pkg.sv",
    "third_party/verilog-axis/rtl/axis_fifo.v", "third_party/verilog-axis/rtl/axis_demux.v",
    "third_party/verilog-axis/rtl/axis_arb_mux.v", "third_party/verilog-axis/rtl/arbiter.v",
    "third_party/verilog-axis/rtl/priority_encoder.v",
    "hdl/ieee8021q/ts/traffic_class_map.sv", "hdl/ieee8021q/ts/traffic_classifier.sv",
    "hdl/ieee8021q/ts/credit_based_shaper.sv", "hdl/ieee8021q/ts/traffic_shaping_core.sv",
    "hdl/ieee8021q/ts/traffic_queues.sv", "hdl/ieee8021q/ts/traffic_controller_802_1q.sv",
    "hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv", "hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv",
    "hdl/common/cdc_pulse.sv", "hdl/common/cdc_handshake.sv", "hdl/common/axis_mux_rr_2in_1out.sv",
    "hdl/ieee8021as/ptp_timestamp/ptp_ts_core.sv", "hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv",
    "hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv",
    "hdl/ieee8021q/filtering/tcam.sv", "hdl/ieee8021q/filtering/rx_mac_filter.sv", "hdl/common/tx_ifg_gasket.sv", "hdl/ieee1722/aaf/KL_pcm_lpf.sv",
    "hdl/common/KL_link_guard.sv",
    "hdl/ieee17221/adp/adp_advertiser.sv", "hdl/ieee17221/adp/adp_tx_arbiter.sv",
    # AECP/AEM listener (IEEE 1722.1 / Milan v1.2). Order: pkg, then leaf
    # modules, then KL_aecp_top. The store/accessor read the generated ROM
    # include hdl/ieee17221/aecp/gen/aecp_aem_rom.svh (avdecc/gen_aem_store.py).
    "hdl/ieee17221/aecp/aecp_pkg.sv",
    "hdl/ieee17221/aecp/KL_aecp_packet_validator.sv", "hdl/ieee17221/aecp/KL_aecp_common_parser.sv",
    "hdl/ieee17221/aecp/KL_aecp_l0_state.sv", "hdl/ieee17221/aecp/KL_aecp_timers.sv",
    "hdl/ieee17221/aecp/KL_aecp_accessor.sv", "hdl/ieee17221/aecp/KL_aecp_aem_store.sv",
    "hdl/ieee17221/aecp/KL_aem_patch.sv",
    "hdl/ieee17221/aecp/KL_aecp_aem_dyn_mux.sv", "hdl/ieee17221/aecp/KL_aecp_response_builder.sv",
    "hdl/ieee17221/aecp/KL_aecp_ingress.sv", "hdl/ieee17221/aecp/KL_aecp_top.sv",
    # ACMP N-context engine + compatibility wrappers (Milan v1.2 §5.5)
    "hdl/ieee17221/acmp/acmp_pkg.sv",
    "hdl/ieee17221/acmp/KL_acmp_tlkr_ctx.sv", "hdl/ieee17221/acmp/KL_acmp_responder.sv",
    "hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv", "hdl/ieee17221/acmp/KL_acmp_listener.sv",
    # lwSRP engine (802.1Q MSRP/MVRP, Milan v1.2 §5.6). Order: pkg first.
    "hdl/ieee8021q/srp/lwsrp_pkg.sv", "hdl/ieee8021q/srp/KL_lwsrp_timers.sv",
    "hdl/ieee8021q/srp/KL_lwsrp_tx.sv", "hdl/ieee8021q/srp/KL_lwsrp_ingress.sv",
    "hdl/ieee8021q/srp/KL_lwsrp_walker.sv", "hdl/ieee8021q/srp/KL_lwsrp_registrar.sv", "hdl/ieee8021q/srp/KL_lwsrp_ta_registrar.sv",
    "hdl/ieee8021q/srp/KL_lwsrp_ctx.sv", "hdl/ieee8021q/srp/KL_lwsrp_ctx_tx.sv",
    "hdl/ieee8021q/srp/KL_lwsrp_rx.sv", "hdl/ieee8021q/srp/KL_lwsrp_bw_gate.sv",
    "hdl/ieee8021q/srp/KL_lwsrp_top.sv",
    # AVTP AAF talker (MVP: Pmod I2S2 on pmoda -> class-A stream, fabric-only)
    "hdl/ieee1722/aaf/aaf_talker_i2s.sv", "hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv",
    "hdl/ieee1722/aaf/KL_pcm_ring_bram.sv",   # --pcm-ring bram: shed-proof on-chip PCM ring
    "hdl/ieee1722/aaf/KL_i2s_playback.sv", "hdl/ieee1722/aaf/KL_tone_gen.sv",
    # item-7 playback: picks the DAC source AND its pace (render crossbar vs
    # the legacy RX tap). Instantiated by milan_datapath - a missing entry
    # here is invisible to Verilator and to yosys (both carry their own file
    # lists) and only surfaces as a Vivado "module not found" at synthesis.
    "hdl/ieee1722/aaf/KL_i2s_feed_mux.sv",
    "hdl/ieee1722/aaf/KL_aaf_latency_taps.sv",   # item-11: per-stage AAF latency taps (LTAP CSR group 0x870)
    "hdl/ieee1722/aaf/KL_media_adv.sv", "hdl/common/cdc_pair_fifo.sv",
    "hdl/ieee1722/avtp/avtp_subtype_pkg.sv", "hdl/ieee1722/avtp/avtp_stream_parser.sv",
    "hdl/ieee1722/avtp/KL_stream_table.sv",
    "hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv",
    "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv", "hdl/ieee1722/avtp/KL_talker_diag_ctx.sv", "hdl/ieee1722/avtp/KL_media_clock_restart.sv", "hdl/ieee17221/aecp/KL_persist_journal.sv",
    "hdl/ieee1722/aaf/KL_pcm_route.sv",
    "hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv", "hdl/ieee1722/aaf/KL_tdm_capture.sv", "hdl/ieee1722/aaf/KL_tdm_capture_master.sv", "hdl/ieee1722/aaf/KL_pair_blend.sv", "hdl/ieee1722/aaf/KL_pair_zero_fill.sv", "hdl/ieee1722/aaf/KL_tdm_render.sv", "hdl/ieee1722/aaf/KL_chan_map_render.sv", "hdl/ieee1722/aaf/KL_chan_map_capture.sv", "hdl/ieee1722/aaf/KL_aaf_packetizer.sv", "hdl/ieee1722/crf/KL_crf_rx.sv", "hdl/ieee1722/crf/KL_crf_tx.sv", "hdl/ieee1722/maap/KL_maap.sv",
    "hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv", "hdl/ieee1722/aaf/KL_aaf_packetizer.sv", "hdl/ieee1722/crf/KL_crf_rx.sv", "hdl/ieee1722/crf/KL_crf_tx.sv", "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv", "hdl/ieee1722/maap/KL_maap.sv",
    "hdl/common/eth_event_counter/ethernet_events.sv", "hdl/common/eth_event_counter/event_counter.sv",
    # RMON pulse synthesiser at the SoC's MAC boundary (MilanMAC instantiates it;
    # listed here because add_milan_datapath is the one place RTL sources are
    # registered, and the STAT window is meaningless without it)
    "hdl/common/eth_event_counter/KL_mac_rmon_events.sv",
    "hdl/common/csr/milan_csr.sv", "hdl/milan/milan_datapath.sv",
]


def _eth_event_lanes():
    """Number of RMON lanes, READ OUT OF `ethernet_events.svh` instead of being
    duplicated here as a `9`.

    This is the lane's own lesson applied to itself. A hardcoded width would be
    the LiteX silent-no-op class one level up: add a lane to the enum and the
    migen `Signal` stays 9 bits, so the tenth lane's pulse and its capability
    bit are dropped on the floor with nothing failing anywhere - the same shape
    as the tie that killed RMON in the first place. Parsing the single source of
    truth costs three lines and cannot drift."""
    svh = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "hdl", "common", "eth_event_counter",
        "ethernet_events.svh")
    with open(svh) as f:
        body = f.read()
    m = re.search(r"typedef\s+enum\s+int\s*\{(.*?)\}", body, re.S)
    assert m, f"{svh}: ethernet_events_t enum not found"
    names = [n.split("=")[0].strip()
             for n in re.sub(r"//.*", "", m.group(1)).split(",")]
    names = [n for n in names if n]
    assert names[-1] == "_ETH_EVENT_COUNTER", \
        f"{svh}: enum must end with the _ETH_EVENT_COUNTER terminator"
    return len(names) - 1          # the terminator is the count, not a lane


#! docs/design/AREA_BUDGET.md tier-1 optional blocks: SoC keyword -> the
#! milan_datapath parameter that prunes it. EVERY ONE DEFAULTS TO PRESENT
#! (True); the parameter is passed to the Instance ONLY when the block is
#! pruned, so a default build's generated top .v is byte-identical to the
#! shipping one and no existing bitstream changes by these keywords existing.
#! Order is the AREA_BUDGET tier-1 table order (largest first).
MILAN_OPTIONAL_BLOCKS = {
    "media_clock_servo": "MCSERVO_P",   # KL_mmcm_drp_servo
    "latency_taps":      "LTAP_P",      # KL_aaf_latency_taps
    "maap":              "MAAP_P",      # KL_maap
    "i2s_playback":      "I2SPB_P",     # KL_i2s_playback
    "rx_mac_filter":     "RXFILT_P",    # rx_mac_filter + tcam
    "render_lpf":        "LPF_P",       # KL_pcm_lpf (banked lever, lane S)
    "datapath_probes":   "DPROBES_P",   # APRB + PBK probe groups (0x8B4-0x8D0)
}


def _arty_serial_io(name, pmod):
    """HANDOVER 8.3b: the Arty TDM8 MASTER header, as an add_extension resource.

    Placed on pmodb - a HIGH-SPEED Pmod (straight to the FPGA, no 200 R series
    resistors, unlike JC/JD), which is what a continuously-toggling 12.288 MHz
    bclk wants. Pin order is the Pmod's own top row 1-4 plus bottom-row pin 7:

        pmodb:0  E15  mclk   (out, 12.288 MHz = clk/2, codec master clock)
        pmodb:1  E16  bclk   (out, 12.288 MHz = 8 slots x 32 bit x 48 kHz)
        pmodb:2  D15  fsync  (out, 48.000 kHz, 1-bclk pulse)
        pmodb:3  C15  din    (in,  TDM serial data, MSB first)
        pmodb:4  J17  dout   (out, KL_tdm_render serial out)

    pmoda is UNTOUCHED: the Pmod I2S2 keeps all eight pins and the CS5343
    MCLK stays on pmoda:4 (D13) - the blend (milan_datapath
    AUDIO_IF_I2S_PAIR_P -> KL_pair_blend) runs BOTH front-ends, I2S as pair
    slot 0 ("channels 1/2 stay the I2S Pmod", USER 2026-07-28).

    The parameterization is deliberate: the add_extension CALL LINE names the
    resource ("tdm") and the connector ("pmodb") as string literals, which is
    exactly what sw/litex/platforms/board_audio_routing.py reads as the
    routing oracle - one line, and every routing answer flips with no edit
    there."""
    from litex.build.generic_platform import Subsignal, Pins, IOStandard
    return [(name, 0,
             Subsignal("mclk",  Pins(f"{pmod}:0")),
             Subsignal("bclk",  Pins(f"{pmod}:1")),
             Subsignal("fsync", Pins(f"{pmod}:2")),
             Subsignal("din",   Pins(f"{pmod}:3")),
             Subsignal("dout",  Pins(f"{pmod}:4")),
             IOStandard("LVCMOS33"))]


def add_milan_datapath(host, platform, axil, o_irq_csr, extra_ports=None, milan_cd="sys",
                       milan_clk_hz=100_000_000, num_streams=1, audio_if_slots=0,
                       talker_wire_chans=2, audio_if_master=False,
                       audio_if_i2s_pair=False,
                       aaf_playback=False, aaf_pb_streams=1, loopback_lane=False,
                       render_lpf=True,
                       optional_blocks=None, cbs_queues_mask=None,
                       entity_gen_dir=None):
    """Instantiate `milan_datapath` and add its RTL sources  -  the single place the
    wrapper is wired, reused by the board SoC (`MilanNIC`) and the sim SoC
    (`milan_sim.py`). `axil` is the AXI-Lite CSR slave; `o_irq_csr` gets the datapath
    interrupt. `extra_ports` overrides/adds Instance ports to attach the DMA (§A.6)
    and MAC (§A.7) at the exposed AXIS boundary  -  without it, those ports are tied
    idle (still elaborates; keeps the CPU⇄CSR path live). Instance ports for RTL
    signals already named `i_*`/`o_*` get the doubled migen prefix (e.g. milan port
    `i_i_mac_speed`, `o_o_irq_csr`)  -  that is correct, not a typo."""
    # Run the datapath in `milan_cd`. When that is not `sys`, cross the CPU's
    # AXI-Lite CSR bus (sys) into `milan_cd` with an async-FIFO CDC  -  so the dense
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
        # clocks / reset  -  the whole datapath runs in `milan_cd`
        i_axis_clk    = ClockSignal(milan_cd),  i_axis_resetn = ~ResetSignal(milan_cd),
        i_clk_audio_i = ClockSignal("audio"),
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
        # TX/RX/TS DMA AXIS  -  §A.6 engine attaches here (idle stub)
        i_s_axis_tx_tdata = 0, i_s_axis_tx_tkeep = 0, i_s_axis_tx_tvalid = 0,
        i_s_axis_tx_tlast = 0,
        i_m_axis_rx_tready = 0, i_m_axis_ts_tready = 0,
        # MAC-facing AXIS  -  §A.7 MAC attaches here (idle stub)
        i_m_axis_mac_tx_tready = 0,
        i_s_axis_mac_rx_tdata = 0, i_s_axis_mac_rx_tkeep = 0,
        i_s_axis_mac_rx_tvalid = 0, i_s_axis_mac_rx_tlast = 0,
        # MAC status (from the external MAC; constants until §A.7). RMON: this is
        # the NO-MAC-ATTACHED stub (CSR-only / sim elaboration), so there is no
        # boundary to derive events from - and that is now SAID rather than
        # implied: the zeroed capability mask below publishes "every lane
        # structurally silent" at CSR 0x204, except the two good-frame lanes
        # milan_datapath derives itself and forces supported. MilanMAC overrides
        # BOTH ties with the live KL_mac_rmon_events vector + mask.
        i_i_mac_speed = 0b10, i_i_link_up = 1, i_i_full_duplex = 1, i_i_mac_events = 0,
        i_i_mac_events_cap = 0,
        # no PHY in the stub: static toggles keep the link guard unarmed/inert
        i_i_ethrx_tgl = 0, i_i_ethtx_tgl = 0, i_i_ethact_tgl = 0,
        # TDM bus, SLAVE role (item-4 front-end family): only sampled when
        # AUDIO_IF_SLOTS_P > 0 AND AUDIO_IF_MASTER_P == 0. These stay tied to
        # 0 - which is precisely why a SLAVE TDM build yields no pairs at all
        # and why the MASTER role exists: it generates bclk/fsync itself
        # (o_tdm_bclk_o / o_tdm_fsync_o, added below only for a master build,
        # so this dict - and the generated top .v - is unchanged otherwise).
        # i_tdm_data_i is overridden from the platform's TDM pads by the board
        # SoC via extra_ports; a master build with it still 0 captures digital
        # SILENCE at the right frame width, exactly as the pmoda-less AX7101
        # I2S front-end does today.
        i_tdm_bclk_i = 0, i_tdm_fsync_i = 0, i_tdm_data_i = 0,
        # chmap follow-up 4: KL_tdm_render serial out is EXPORTED (tdm_dout_o);
        # open here - the same TDM-header platform extension that provides
        # bclk/fsync claims it (extra_ports), no RTL change needed then.
        o_tdm_dout_o = Signal(),
        # audio-MMCM servo boundary: inert ties (servo idles unless
        # clock_source == 2; locked=1 keeps a future VERIFY from hanging).
        # The board SoC overrides these with the real MMCME2_ADV wiring
        # (_CRG audio_* bundle) via extra_ports.
        i_i_ps_clk = ClockSignal(milan_cd),
        i_i_mmcm_drp_do = 0, i_i_mmcm_drp_rdy = 0,
        i_i_mmcm_locked = 1, i_i_mmcm_ps_done = 0,
        # P12: the 0x800 window's LCTX/TCTX/ACMP-tbl engine boundary moved
        # INSIDE milan_datapath (wired to the live monitor_ctx/packetizer/
        # acmp engines) - the P11 inert ties are gone with the ports.
        # interrupt (csr aggregate; DMA-done IRQs come from §A.6). CDC'd to sys above.
        o_o_irq_csr = irq_port,
    )
    if extra_ports:
        ports.update(extra_ports)
    # MILAN_CLK_FREQ_HZ drives the ADP/ACMP 1 s tick divider and the AECP
    # 1 kHz lock timer. NEVER omitted again: silicon 2026-07-14 - the RTL
    # default (100 MHz) on the Arty's 50 MHz datapath made the tick 2 s,
    # stretching the ADP re-advertise to 62 s (the validity horizon) and the
    # Milan probe window to ~30 s. The adpfix RTL fix was correct but this
    # parameter never reached it.
    # N_STREAMS: NxN dataplane width (docs/NXN_ARCHITECTURE.md P0). The builder
    # emits --num-streams in soc_params for the 4x4/8x8 shapes; default 1 =
    # today's bit-compatible single-stream build.
    # AUDIO_IF_SLOTS_P: item-4 audio-interface family front-end generate
    # select (0 = stereo I2S default, 8/16/32 = KL_tdm_capture TDM slave).
    # The builder emits --audio-interface for the tdm kinds; default 0 keeps
    # the shipping I2S build bit-identical.
    # AAF_PLAYBACK_P (item-7): passed ONLY when --aaf-playback is on, so the
    # default build's Instance (and generated top .v) is byte-identical - the
    # SV default AAF_PLAYBACK_P=0 prunes the KL_pcm_tx generate.
    # TALKER_WIRE_CHANS_P (item 00): the channels_per_frame the framer emits.
    # Passed ONLY above the default, on the AAF_PLAYBACK_P discipline, so the
    # shipping build's Instance and generated top .v stay byte-identical.
    # milan_datapath REFUSES at elaboration any width the front-end selected by
    # audio_if_slots cannot feed - that guard is what makes this a fabric fact
    # and not one more declaration.
    dp_params = dict(p_MILAN_CLK_FREQ_HZ=int(milan_clk_hz),
                     p_N_STREAMS=int(num_streams),
                     p_AUDIO_IF_SLOTS_P=int(audio_if_slots))
    if int(talker_wire_chans) != 2:
        dp_params["p_TALKER_WIRE_CHANS_P"] = int(talker_wire_chans)
    if aaf_playback:
        # param NAME must match the SV declaration exactly - a mismatched
        # LiteX Instance param silently no-ops (latent find 2026-07-25:
        # this line passed p_AAF_PLAYBACK for weeks and pruned nothing in,
        # because the RTL parameter is AAF_PLAYBACK_P)
        dp_params["p_AAF_PLAYBACK_P"] = 1
        # task #31 START-SMALL: how many host playback rings KL_pcm_tx
        # serves. ONE value drives BOTH the datapath parameter and the
        # MilanDMA pb CSR sizing (the derive-never-mirror rule); ship
        # default 1 - the full-N engine OOC'd 2216 LUT at 8x8x8, the one-
        # ring shape is ~1/8th of that and the 64ch chmap already places
        # its pairs on any talker's wire slots.
        dp_params["p_AAF_PB_STREAMS_P"] = int(aaf_pb_streams)
    if loopback_lane:
        # task #65 rx -> talker LOOPBACK bucket. SAME DISCIPLINE as
        # AAF_PLAYBACK_P above, and the same name trap: the SV parameter is
        # LOOPBACK_P. Passed only when asked for, so a build that does not
        # ask emits a byte-identical top .v. It buys the entity's declared
        # loopback AUDIO_CLUSTERs their actual source; it costs +2303 LUT /
        # +1542 FF OOC at the 8x8 shape, which is why the shipping config
        # leaves it off and points its power-on map at the host pool.
        dp_params["p_LOOPBACK_P"] = 1
    if audio_if_master and int(audio_if_slots):
        # AUDIO_IF_MASTER_P / AUDIO_IF_CLK_HZ_P (item 4): the TDM bus ROLE and
        # the clock the master divides. SAME DISCIPLINE as AAF_PLAYBACK_P -
        # passed ONLY when asked for, so a build that does not ask emits a
        # byte-identical top .v - and the SAME TRAP applies: the names below
        # must match the SV parameter declarations CHARACTER FOR CHARACTER
        # (`AUDIO_IF_MASTER_P`, `AUDIO_IF_CLK_HZ_P` in hdl/milan/
        # milan_datapath.sv), because LiteX does not diagnose a parameter the
        # module does not have - it silently drops it, which is how
        # p_AAF_PLAYBACK pruned nothing for weeks.
        dp_params["p_AUDIO_IF_MASTER_P"] = 1
        dp_params["p_AUDIO_IF_CLK_HZ_P"] = (2 * int(audio_if_slots)
                                            * AUDIO_IF_WORD_BITS
                                            * AUDIO_IF_FS_HZ)
        if audio_if_i2s_pair:
            # HANDOVER 8.3b blend: keep the stereo I2S front-end alive beside
            # the TDM master (KL_pair_blend, I2S = pair slot 0). Passed ONLY
            # when the board routes BOTH pad sets - same byte-identical
            # discipline, same character-for-character name rule as above.
            dp_params["p_AUDIO_IF_I2S_PAIR_P"] = 1
    # LPF_P: BANKED AREA LEVER (docs/NXN_ARCHITECTURE.md 6.2). Passed ONLY when
    # the filter is pruned, so the default build's Instance - and the generated
    # top .v - stay byte-identical; the SV default LPF_P=1 keeps KL_pcm_lpf.
    # Pruning it makes the render tap behave exactly like LPF_CTRL[0]=0 does
    # today, and costs the -72.7 dB analog loop record its bitstream (that
    # number was measured THROUGH the filter): re-measure before quoting it.
    # It is now ONE ROW of the general tier-1 table below.
    #
    # docs/design/AREA_BUDGET.md tier-1 prunes. `optional_blocks` is a
    # {keyword: bool} map over MILAN_OPTIONAL_BLOCKS; a MISSING key means
    # PRESENT, and only a False value emits a parameter. `render_lpf` is the
    # older single-purpose keyword for the same block and still works - it is
    # folded in here so the two cannot disagree (either says "prune" -> prune).
    blocks = dict.fromkeys(MILAN_OPTIONAL_BLOCKS, True)
    blocks["render_lpf"] = bool(render_lpf)
    for k, v in (optional_blocks or {}).items():
        if k not in MILAN_OPTIONAL_BLOCKS:
            raise ValueError(f"unknown milan_datapath optional block '{k}' "
                             f"(known: {sorted(MILAN_OPTIONAL_BLOCKS)})")
        blocks[k] = blocks[k] and bool(v)
    for k, param in MILAN_OPTIONAL_BLOCKS.items():
        if not blocks[k]:
            dp_params[f"p_{param}"] = 0
    # CBS instance mask (2026-07-28 area lever, traffic_shaping_core has the
    # contract). Passed ONLY when it actually prunes - None or all-ones emits
    # a byte-identical top .v (the AAF_PLAYBACK_P discipline), and the name
    # must match the SV declaration CHARACTER FOR CHARACTER (the silent-drop
    # trap above).
    if cbs_queues_mask is not None and int(cbs_queues_mask) != (1 << 5) - 1:
        dp_params["p_CBS_QUEUES_MASK_P"] = int(cbs_queues_mask)
    host.specials += Instance("milan_datapath", **dp_params, **ports)
    # CBS slope timing: no XDC exception needed since the sequential slope
    # engine (credit_based_shaper.sv slope_engine, 2026-07-11). The old per-
    # cycle combinational constant-divide cones (~9.3K LUTs over 4 queues,
    # partly attributed to milan_csr by cross-boundary optimization) needed
    # set_multicycle_path 4 on the config->slope_r capture; the engine's
    # 1-bit-per-cycle divider paths close timing natively.
    # RTL sources for elaboration / P&R. Curated list (NOT add_source_dir) so the
    # Zynq-only milan_top.sv / milan_dma_wrapper.v are excluded from the fabric build
    #  -  same file set the tb/verilator/milan_dp + syn/yosys checks use.
    # abspath: normalize a literal "./" in __file__ (e.g. `python ./milan_sim.py` on
    # 3.14 keeps it) — an un-normalized "." component silently eats one dirname level.
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # milan-fpga/
    # Include dirs for the ``include ...`` files (ethernet_packet_pkg.sv, *.svh).
    # Vivado auto-searches source dirs; Verilator (the sim backend) needs -I.
    # PER-CONFIG entity definition (USER 2026-07-28: both boards' 3-seed
    # sweeps run CONCURRENTLY): when set, the generated entity svh
    # (gen/adp_shape_defaults.svh + aecp_aem_rom.svh) resolves from THIS
    # config's own configs/generated/<cfg>/ copy instead of the single
    # tracked hdl/ one - two boards can then build from one tree at the same
    # time with no svh-ownership handoff. Prepended so it WINS the include
    # search; the tracked dirs below stay as the fallback for every other
    # include.
    if entity_gen_dir:
        platform.add_verilog_include_path(entity_gen_dir)
        platform.add_verilog_include_path(os.path.join(entity_gen_dir, "gen"))
    for inc in ("hdl/common", "hdl/ieee8021q/ts", "hdl/ieee8021as/ptp_timestamp",
                "hdl/ieee17221/adp", "hdl/common/csr", "hdl/common/eth_event_counter",
                "hdl/ieee17221/aecp", "hdl/ieee17221/aecp/gen", "hdl/ieee1722/avtp"):
        platform.add_verilog_include_path(os.path.join(base, inc))
    srcs = list(_MILAN_DATAPATH_SOURCES)
    if aaf_playback:
        # item-7: the host-PCM-ring AAF talker source (only referenced when the
        # AAF_PLAYBACK_P generate is live, so the default source list is unchanged).
        srcs.append("hdl/ieee1722/aaf/KL_pcm_tx.sv")
    for f in srcs:
        platform.add_source(os.path.join(base, f))


# AXIS clock-domain crossing (DMA/MAC boundary) ---------------------------------------------------

class _AxisDP:
    """Pair of stream endpoints for one AXIS lane crossing the datapath boundary:
    `.dp` is bound to the `milan_datapath` Instance, `.sys` to the sys-domain DMA/MAC."""
    def __init__(self, dp, sys):
        self.dp  = dp
        self.sys = sys

def _axis_dp_cdc(host, name, layout, milan_cd, to_datapath, depth=16, rename=None):
    """Cross one AXIS lane between the sys domain (DMA engine / MAC core) and the
    datapath's `milan_cd` domain with an async-FIFO `stream.ClockDomainCrossing`
    (the "use a FIFO to compensate the timing" boundary). `to_datapath=True` is a
    sys->milan_cd lane (memory->TX, MAC-RX->datapath); False is milan_cd->sys
    (datapath->RX/TS memory, datapath->MAC-TX). When `milan_cd == "sys"` there is no
    crossing: `.dp` and `.sys` are the same endpoint (direct wire)."""
    if milan_cd == "sys":
        ep = stream.Endpoint(layout)
        return _AxisDP(dp=ep, sys=ep)
    # buffered=True (AsyncFIFOBuffered) re-registers dout in the read domain:
    # the BRAM CLK->Q cone otherwise fans straight into the datapath consumers
    # (AX33 x3-seed violator, storage cell = mac_rx_cdc). +1 cycle on a
    # handshaked stream = transparent.
    # `rename` maps the CDC's internal clock domains onto shadow domains whose
    # resets are EXTENDED (the 07-29 wedge lesson: these FIFOs sat outside
    # every recovery reset - LINK_CTRL[1] reinit reset the MAC core + tx_sf
    # around a possibly-corrupt crossing it could not touch). Both sides must
    # rename TOGETHER: resetting one side of an async FIFO skews the gray
    # pointers past the depth invariant and can MANUFACTURE the permanent-full
    # state it is meant to clear.
    if to_datapath:                                        # sys -> milan_cd
        cdc = stream.ClockDomainCrossing(layout, cd_from="sys", cd_to=milan_cd, depth=depth, buffered=True)
        if rename: cdc = ClockDomainsRenamer(rename)(cdc)
        setattr(host, name, cdc)                           # LiteXModule auto-submodule
        return _AxisDP(dp=cdc.source, sys=cdc.sink)
    cdc = stream.ClockDomainCrossing(layout, cd_from=milan_cd, cd_to="sys", depth=depth, buffered=True)  # milan_cd -> sys
    if rename: cdc = ClockDomainsRenamer(rename)(cdc)
    setattr(host, name, cdc)
    return _AxisDP(dp=cdc.sink, sys=cdc.source)


# MAC (§A.7) ---------------------------------------------------------------------------------------

class MilanMAC(LiteXModule):
    """The 1G MAC + RGMII PHY (§A.7), attached at the milan_datapath MAC-facing AXIS
    boundary. Uses LiteEth's `LiteEthPHYGMII` (the AX7101 e1 port is GMII-wired) + `LiteEthMACCore`
    (preamble/CRC/padding, PHY-width conversion) and a thin stream↔AXIS adapter, so
    the Milan datapath owns *all* packet processing (classify/CBS/PTP/filter/ADP) and
    the MAC core just does L1/framing.

    `dp_ports` is the dict of `milan_datapath` Instance ports this MAC drives  -  pass
    it as `MilanNIC(..., dma_mac_ports=mac.dp_ports)`.

    NOTE (board-gated): the exact `last_be`↔`tkeep` byte-enable mapping and the
    link/speed status (MDIO) are wired to sensible values for elaboration; they are
    validated on hardware (there is no RGMII PHY to exercise in sim). See
    docs/integration/FULLY_FPGA_RISCV_MIGRATION.md §A.7 and the protocol/test matrix."""
    def __init__(self, platform, data_width=64, phy_index=0, milan_cd="sys",
                 gtx_tx_invert=False, phy_model="gmii", **_rgmii):
        from liteeth.phy.gmii import LiteEthPHYGMII
        from liteeth.mac.core import LiteEthMACCore
        from liteeth.common import eth_phy_description
        from litex.soc.interconnect.packet import PacketFIFO

        clk_pads = platform.request("eth_clocks", phy_index)
        pads     = platform.request("eth",        phy_index)
        # Sequenced eth-side reset request from the datapath's KL_link_guard (o_eth_rst),
        # created UP-FRONT (before the PHY is built) so it can be threaded into BOTH the
        # PHY CRG (ext_reset -> re-inits the PHY TX register stage + gtx forward in
        # cd_eth_tx/cd_eth_rx) and, further down, the MAC core's ETH-side CDC halves.
        # The guard drops it mid-settle, strictly BEFORE reinit, so release order stays
        # eth-first-then-sys (AX42: 2026-07-23).
        self.eth_rst = Signal()  # driven from the datapath's link guard (o_eth_rst)
        self.eth_guard = Signal()  # ETH GUARD state (CSR 0x7D8, USER 08-06)
        # phy_model="mii": Arty A7 DP83848 (10/100, MII 4-bit). The MAC core
        # handles the PHY-width conversion, so everything downstream of
        # self.phy (store-and-forward FIFO, last_be conversion, CDC, loopback)
        # is identical; the gtx invert does not apply. The IOB pad-locking
        # DOES apply — the 2026-07-29 Arty TX wedge was this exact class:
        # zero IOB/output constraints on the MII pads left the TX launch FFs
        # to placement luck, the 0x001A-era trees shifted global placement,
        # and four consecutive seeds (asl/eppo x m0019q/m001a) lost the
        # clock-to-pad lottery the older pk seed had been winning — TX died
        # minutes after boot as the die warmed through the marginal window
        # while RX stayed perfect. Same commands as the GMII branch below.
        if phy_model == "mii":
            from liteeth.phy.mii import LiteEthPHYMII
            self.phy = LiteEthPHYMII(clk_pads, pads, with_hw_init_reset=True)
        else:
            # The AX7101 RTL8211E is strapped for **GMII** (8-bit SDR), per the Alinx
            # example top (`input [7:0] e_rxd`, separate rxdv/rxer, gtx=rxc). An RGMII
            # (4-bit DDR) read of this bus corrupts every byte  -  hardware-confirmed as 100%
            # MAC preamble errors (evidence/hw_ma3_*). LiteEthPHYGMII is the right PHY.
            # (`**_rgmii` absorbs the now-unused --rgmii-*-delay knobs for API compat.)
            self.phy  = LiteEthPHYGMII(clk_pads, pads, with_hw_init_reset=True,
                                       tx_clk_invert=gtx_tx_invert,
                                       # AX42: thread the guard's eth_rst into the PHY CRG so a
                                       # link bounce that stops RXC (and with it the eth_tx domain,
                                       # which GMII forwards off RXC) re-inits the PHY TX register
                                       # stage + gtx clock-forward on recovery - not just the MAC
                                       # CDC halves. Same signal, so the eth-first-then-sys release
                                       # ordering is preserved. (MII/Arty PHY: TX_CLK is separate,
                                       # so the eth_tx domain does not die on an RXC drop - N/A.)
                                       ext_reset=self.eth_rst)

        # PHY pad launch/capture timing is otherwise UNCONSTRAINED, so the placer
        # may put the tx_data/tx_en launch FFs anywhere: measured on AX silicon,
        # FFs at SLICE_X1 (next to the IO column, data-vs-gtx skew ~1-2 ns) TX
        # 10/10 frames; FFs at SLICE_X14 (~4-6 ns skew) TX 0/10 - outside the
        # RTL8211E sampling window (~(0,6) ns @ 8 ns). The Arty MII path hit the
        # SAME class 2026-07-29 (four consecutive seeds TX-dead minutes after
        # boot, thermal drift through the marginal window) because these
        # commands used to live in the GMII-only branch. Pack the launch AND
        # capture FFs into the IOB on EVERY phy_model so clock-to-out/setup is
        # pad-locked on every build. Plain set_property lines only - XDC does
        # not execute TCL `if` guards (verified: a guarded version was silently
        # skipped and the FFs stayed in fabric). RX side per AX36: adding IOBs
        # near the RX bank shifted IO-adjacent placement and killed RX on both
        # seeds until the capture FFs were pad-locked too.
        platform.add_platform_command(
            "set_property IOB TRUE [get_ports {{eth%d_tx_data[*]}}]" % phy_index)
        platform.add_platform_command(
            "set_property IOB TRUE [get_ports eth%d_tx_en]" % phy_index)
        # RX capture pad-lock is GMII-ONLY: LiteEthPHYMII's RX inputs feed
        # more than one consumer, so forcing the capture FF into the ILOGIC
        # trips DRC PDRC-158 (routing-mux contention, m001b: ILOGICE2.DINV
        # two arcs -> bitgen refused). MII RX sampling has been clean on
        # every seed including all four TX-wedged ones - it does not need
        # the force; GMII does (AX36) and packs legally.
        if phy_model != "mii":
            platform.add_platform_command(
                "set_property IOB TRUE [get_ports {{eth%d_rx_data[*]}}]" % phy_index)
            platform.add_platform_command(
                "set_property IOB TRUE [get_ports eth%d_rx_dv]" % phy_index)
            platform.add_platform_command(
                "set_property IOB TRUE [get_ports eth%d_rx_er]" % phy_index)

        # The PHY clock domains were UNTIMED in every bitstream ever shipped:
        # the emitted XDC held exactly ONE create_clock (the board oscillator),
        # so every path clocked by eth_rx/eth_tx - 328 endpoints on the Arty,
        # check_timing "no_clock" - got no setup OR hold analysis and no hold
        # fixing, making the MAC edge a per-seed placement lottery that the
        # sweep's "STA-clean" gate could not see (2026-07-29 adversarial
        # review). MII: the DP83848 drives BOTH pad clocks at 25 MHz. GMII:
        # the RTL8211E drives RXC at 125 MHz and liteeth forwards the TX
        # domain off the same clock (gtx = rxc), so the one constraint
        # propagates to both. Each PHY clock is its own asynchronous group:
        # the crossings into sys/milan are gray-coded AsyncFIFOs whose
        # synchronizers LiteX already false-paths, and without the group
        # Vivado would time those crossings as same-PLL related paths.
        eth_clk_groups = ["eth_clocks%d_rx" % phy_index]
        if phy_model == "mii":
            platform.add_period_constraint(clk_pads.rx, 1e9/25e6)
            platform.add_period_constraint(clk_pads.tx, 1e9/25e6)
            eth_clk_groups.append("eth_clocks%d_tx" % phy_index)
        else:
            platform.add_period_constraint(clk_pads.rx, 1e9/125e6)
        # MUST go through additional_xdc_commands, NOT add_platform_command:
        # platform commands are emitted in list order and the create_clock
        # lines are only appended at finalize() - a construction-time
        # set_clock_groups would land BEFORE its create_clock in the XDC,
        # resolve an empty clock list, and silently never apply, leaving the
        # newly-timed eth clocks RELATED to sys (Opus verify D2: the worst of
        # both worlds - every gray-coded crossing timed as a same-PLL path).
        # additional_xdc_commands is emitted in its own section after the
        # clock + false-path sections (vivado.py build_io_constraints).
        #
        # USER 2026-08-06 (the t522-eppo placement-lottery postmortem): a
        # blanket `set_clock_groups -asynchronous` FALSE-PATHS every eth
        # crossing, so the gray-pointer/synchronizer skew into sys+milan was
        # bounded by nothing but placement luck - the eppo seed shipped a
        # bitstream whose kernel-bound RX/ARP died as the die warmed while
        # the fabric plane stayed healthy. GMII boards now get BOUNDED
        # crossings instead: hold analysis is meaningless across async
        # domains (false_path -hold), and setup becomes a real 8 ns
        # datapath-only budget (min of the two periods) that every seed
        # must MEET - the lottery becomes an STA failure the sweep gate can
        # see. MII (arty, retired) keeps the legacy groups.
        if phy_model == "mii":
            for eth_clk_pad in eth_clk_groups:
                platform.toolchain.additional_xdc_commands.add(
                    "set_clock_groups -asynchronous -group "
                    "[get_clocks -of_objects [get_ports %s]]" % eth_clk_pad)
        else:
            eth_ck = ("[get_clocks -of_objects [get_ports %s]]"
                      % eth_clk_groups[0])
            # LiteX templates additional_xdc_commands through str.format -
            # literal TCL braces must be doubled or they parse as format keys
            part_cks = "[get_clocks {{crg_clkout0 crg_clkout1}}]"
            for a, b in ((eth_ck, part_cks), (part_cks, eth_ck)):
                platform.toolchain.additional_xdc_commands.add(
                    "set_false_path -hold -from %s -to %s" % (a, b))
                platform.toolchain.additional_xdc_commands.add(
                    "set_max_delay -datapath_only -from %s -to %s 8.000"
                    % (a, b))
            # the audio/idelay clocks have no real eth crossings - keep them
            # formally asynchronous so nothing accidental gets timed as
            # PLL-related
            platform.toolchain.additional_xdc_commands.add(
                "set_clock_groups -asynchronous -group %s -group "
                "[get_clocks {{crg_audio_ref_raw crg_audio_mclk_raw "
                "crg_pll_audio_fb crg_clkout2 crg_clkout3 crg_clkout4}}]"
                % eth_ck)

        # MAC-path supervised reset (link-bounce wedge, 2026-07-19): the eth
        # clock domains reset via phy_crg_reset, but the core's SYS-side CDC
        # halves kept their pointers = permanent desync after a link bounce
        # (silicon: TX or RX wedges until a gateware reload). `reinit` holds
        # the whole sys side (core + tx FIFO) in reset; the recovery daemon
        # strobes phy_crg_reset + reinit together for a clean eth re-init
        # WITHOUT touching the Milan datapath.
        self.reinit = Signal()   # driven from the datapath's link guard | LINK_CTRL[1]
        self.cd_macsys = ClockDomain()
        self.comb += self.cd_macsys.clk.eq(ClockSignal("sys"))
        # `reinit` comes from the milan_cd-clocked datapath Instance and
        # sys<->milan is false-pathed, so a plain comb OR into rst releases
        # UNTIMED w.r.t. sys - different macsys FFs could leave reset on
        # different sys edges (Opus verify D9). Async assert + sys-synchronous
        # release, same discipline the macdp side below gets.
        self.specials += AsyncResetSynchronizer(
            self.cd_macsys, ResetSignal("sys") | self.reinit)
        # Link-guard liveness toggles (KL_link_guard, 2026-07-21): plain
        # divide-by-2 FFs in each PHY-provided clock domain plus one flip per
        # received frame. The datapath's guard samples them as async data,
        # declares a clock dead after 41 us without a transition, and then
        # auto-sequences the reinit strobe (hold through the outage + ~21 ms
        # clean-clock settle) - the hardware version of the linkmon recovery.
        # reset_less: the toggles OBSERVE the raw clocks, so they must sit outside
        # every reset cone the guard itself drives. With plain FFs the AX42 ext_reset
        # thread (eth_rst -> PHY CRG -> cd_eth_tx/rx domain resets) froze the toggles
        # whenever the guard asserted eth_rst: both_alive dropped 41 us into SETTLE,
        # the FSM fell back to HOLD with eth_rst still high, and the guard deadlocked
        # holding MAC+PHY in reset forever (silicon 2026-07-24: every cold boot with
        # an autoneg RXC bounce, and every manual LINK_CTRL[1] reinit, wire-dead).
        self.ethrx_tgl  = Signal(reset_less=True)
        self.ethtx_tgl  = Signal(reset_less=True)
        self.ethact_tgl = Signal(reset_less=True)
        self.sync.eth_rx += self.ethrx_tgl.eq(~self.ethrx_tgl)
        self.sync.eth_tx += self.ethtx_tgl.eq(~self.ethtx_tgl)
        self.sync.eth_rx += If(self.phy.source.valid & self.phy.source.last,
                               self.ethact_tgl.eq(~self.ethact_tgl))
        # Sequenced eth-side CDC reset (gaps 5 RTL fix, 2026-07-22): the guard's
        # `eth_rst` re-initializes the MAC core's ETH-side CDC halves in hardware.
        # The MAC's eth domains are derived copies (maceth_tx/maceth_rx) whose reset
        # is the PHY domain reset OR the guard request, async-asserted / sync-released
        # per eth clock (AsyncResetSynchronizer: asserts even while the eth clock is
        # stopped, releases only on a running clock). The guard drops eth_rst
        # mid-settle - strictly BEFORE `reinit` - so both CDC halves restart from
        # matched pointers with zero software involvement (previously only the
        # daemon's phy_crg_reset strobe covered the eth side).
        # (AsyncResetSynchronizer comes from the module-level import: a local
        # re-import here made the name function-local and blew up the EARLIER
        # macsys use with UnboundLocalError - Python scoping, m001d launch.)
        # self.eth_rst is created up-front (near the eth pads request) so it can also be
        # threaded into the PHY CRG (ext_reset); here it additionally re-inits the MAC
        # core's ETH-side CDC halves.
        self.cd_maceth_tx = ClockDomain()
        self.cd_maceth_rx = ClockDomain()
        self.comb += [
            self.cd_maceth_tx.clk.eq(ClockSignal("eth_tx")),
            self.cd_maceth_rx.clk.eq(ClockSignal("eth_rx")),
        ]
        self.specials += [
            AsyncResetSynchronizer(self.cd_maceth_tx,
                                   ResetSignal("eth_tx") | self.eth_rst),
            AsyncResetSynchronizer(self.cd_maceth_rx,
                                   ResetSignal("eth_rx") | self.eth_rst),
        ]
        self.core = ClockDomainsRenamer({"sys":    "macsys",
                                         "eth_tx": "maceth_tx",
                                         "eth_rx": "maceth_rx"})(
                        LiteEthMACCore(phy=self.phy, dw=data_width,
                                       with_preamble_crc=True, with_padding=True))
        # Store-and-forward TX packet FIFO (HW-root-caused 2026-07-04): the bare MACCore is
        # CUT-THROUGH and GMII has no mid-frame flow control (`tx_en = sink.valid` cycle by
        # cycle), while our DMA/datapath source can drop below 1 Gbps mid-frame (Wishbone
        # wait states) -> a single `valid` bubble becomes a tx_en glitch -> the PHY emits a
        # fragment the peer NIC discards WITHOUT counting (total silence). Sim-reproduced
        # (starved source -> 6 bubbles/frame) and sim-fixed by this FIFO: it releases a
        # frame downstream only once COMPLETELY buffered, so the drain is always gapless.
        # 512 x 8 B = 4 KB >= 2 max-size frames; 8 frame slots.
        # (Full LiteEthMAC has SRAM buffering for exactly this reason; we drive the bare
        # core, so we provide it here. docs/findings/kl-eth-tx-debug.md #Second bug.)
        self.tx_sf = ClockDomainsRenamer({"sys": "macsys"})(
                         PacketFIFO(eth_phy_description(data_width),
                                    # 512 x 8 B = 4 KB >= 2 max frames (the
                                    # original sizing); 1024 put the BRAM's
                                    # ADDR[9] pointer cone on the AX critical
                                    # path (AX31/32: storage_32 CLKARDCLK->
                                    # ADDRARDADDR[9] -0.25 ns, 8 seeds missed)
                                    payload_depth=512, param_depth=8,
                                    # buffered => migen SyncFIFOBuffered, whose
                                    # read port is SYNCHRONOUS. The default
                                    # fwft SyncFIFO reads the storage
                                    # ASYNCHRONOUSLY, and an async read can
                                    # only be distributed RAM: this one array
                                    # (512 x 82) was 784 of the board's 1,070
                                    # RAMD64E, i.e. ~196 SLICEMs whose LUTs
                                    # cannot LUT-combine - single biggest
                                    # packing consumer on the board, and the
                                    # reason 4 place directives all missed by
                                    # 22..53 slices. Sync read => BRAM: MEASURED
                                    # -784 LUTRAM (-1,051 slice LUTs) for +1.5
                                    # tiles, AlternateRoutability synth. See
                                    # docs/design/AREA_BUDGET.md 2026-08-03.
                                    # Costs ONE cycle of latency and nothing
                                    # else: SyncFIFOBuffered pre-fetches, so a
                                    # drain still runs 1 beat/cycle with no
                                    # bubble - the gapless-drain property this
                                    # FIFO exists to provide is preserved (and
                                    # is pinned by test_tx_sf_gapless.py).
                                    buffered=True))
        self.comb += self.tx_sf.source.connect(self.core.sink)

        nb = data_width // 8
        L  = [("data", data_width), ("keep", nb)]
        # The datapath-facing endpoints are in `milan_cd`; the MAC core is in sys.
        # When they differ, an async-FIFO stream CDC bridges each direction (`keep`
        # carries the last-beat byte-enable). `_axis_dp_cdc` returns the endpoint the
        # datapath binds to, wiring the CDC (or a direct pass-through) to `sys_ep`.
        # Both MAC crossings live in shadow domains so LINK_CTRL[1]'s reinit
        # resets THEM TOO (07-29 wedge class: a corrupt/stuck crossing at this
        # exact boundary was unreachable by every recovery path). macsys
        # already carries `sys.rst | reinit`; macdp is the same extension of
        # the datapath-side domain, with reinit crossed in async-assert /
        # sync-release. Both sides of each FIFO reset together - see
        # `_axis_dp_cdc` for why one-sided reset is worse than none.
        # LOAD-BEARING INVARIANT: the two sides release a few cycles APART
        # (each synchronizes release into its own clock). That skew is safe
        # ONLY because reinit is held ~21 ms (KL_link_guard SETTLE) with both
        # clocks running, so the reset_less gray-pointer MultiRegs converge
        # to 0 long before EITHER side releases; a future "fast reinit" of a
        # few cycles would reintroduce pointer desync - keep the hold long.
        if milan_cd != "sys":
            self.cd_macdp = ClockDomain()
            self.comb += self.cd_macdp.clk.eq(ClockSignal(milan_cd))
            self.specials += AsyncResetSynchronizer(
                self.cd_macdp, ResetSignal(milan_cd) | self.reinit)
            mac_cdc_rename = {"sys": "macsys", milan_cd: "macdp"}
        else:
            mac_cdc_rename = None
        tx_dp = _axis_dp_cdc(self, "mac_tx_cdc", L, milan_cd, to_datapath=False,
                             rename=mac_cdc_rename)  # dp -> MAC
        rx_dp = _axis_dp_cdc(self, "mac_rx_cdc", L, milan_cd, to_datapath=True,
                             rename=mac_cdc_rename)  # MAC -> dp
        # Debug/telemetry taps (sys side): datapath->MAC-TX out and MAC-RX->datapath in.
        # `MilanDebug` also taps self.core.sink/source (LiteEth in/out) and
        # self.phy.sink/source (GMII wire, eth_tx/eth_rx).
        self.dbg_tx_dp = tx_dp.sys
        self.dbg_rx_dp = rx_dp.sys
        # LiteEth's `last_be` is NOT an AXIS keep mask  -  it is a **one-hot pointer to the
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
            # the last beat  -  it must be 0 on every non-last beat. LiteEth's TX last-BE
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

        # (i2s pads are requested at the DMA/datapath layer - the block that
        # lived here could never run: `soc` is not in this scope and the old
        # try/except only ever swallowed its own NameError)
        self.i2s_pads = None
        self.i2s_dac_pads = None

        # ---- PHY/MAC link status (MAC_STATUS 0x110 / REQ-MAC-03) --------------------
        # WHY A CSR AND NOT A WIRE: LiteEth's GMII/MII PHY wrappers expose NO link,
        # speed or duplex output. `LiteEthPHYGMII`/`LiteEthPHYMII` carry the TX/RX
        # datapaths, the CRG, and - only when the board routes mdc/mdio - a
        # `LiteEthPHYMDIO`, which is a SOFTWARE BIT-BANG register pair (mdc / mdio_w
        # {oe,w} / mdio_r), NOT an autoneg-result register. There is no hardware MDIO
        # master anywhere in the SoC, so the negotiated state only ever exists where
        # the MDIO transactions happen: in software (kl-eth's phylib/ethtool path,
        # `phy` reg window 0xf000_3800). A fabric MDIO poller would be new
        # SystemVerilog, i.e. a different lane - see docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md.
        #
        # Before this register the three datapath status inputs were CONSTANTS
        # (`i_link_up = 1`, `i_full_duplex = 1`, `i_mac_speed` = a per-board build-time
        # guess). That is the RMON tie-off class (2026-07-22: `i_mac_events = 0` made a
        # fully-tested counter block dead in silicon): MAC_STATUS[0] could never report
        # link-down, and REQ-MAC-03's `o_mac_is_1g = mac_ctrl[5] ? mac_ctrl[4] :
        # (i_speed == 2'd2)` derived "1 Gb/s" from a build-time constant - so the lwSRP
        # bandwidth gate's 750 Mb/s admission limit was pinned by the bitstream, not by
        # the link. Reset values REPRODUCE the old constants exactly, so a build whose
        # software never writes this register behaves bit-identically to before; the
        # difference is that software CAN now publish the truth.
        self.link_status = CSRStorage(fields=[
            CSRField("link_up", size=1, offset=0, reset=1,
                     description="PHY link is up (MAC_STATUS[0]). Software-published "
                                 "from the MDIO autoneg result; reset 1 = the "
                                 "pre-2026-07-26 hardwired constant."),
            CSRField("speed", size=2, offset=1,
                     reset=(0b01 if phy_model == "mii" else 0b10),
                     description="Negotiated speed (MAC_STATUS[2:1]): 0=10, 1=100, "
                                 "2=1000 Mb/s. Feeds milan_csr i_speed, hence "
                                 "o_mac_is_1g (REQ-MAC-03) unless MAC_CTRL[5] "
                                 "manual-override is set. Reset = the board's PHY "
                                 "wiring (mii -> 100, gmii -> 1000)."),
            CSRField("full_duplex", size=1, offset=3, reset=1,
                     description="Full-duplex indication (MAC_STATUS[3])."),
        ], description="PHY/MAC link status published by software (MDIO). See "
                       "MAC_STATUS 0x110 in docs/reference/REGISTER_MAP.md.")
        # The register lives in `sys`; the datapath samples in `milan_cd`. `speed` is
        # already 2-FF synchronised inside milan_datapath (`mac_speed_cdc`), so it goes
        # across raw - exactly as the constant did. The two single-bit lanes are NOT
        # synchronised in the RTL (link_up feeds eff_link/cnt_link combinationally and
        # full_duplex feeds the CSR read mux), so they get the standard 2-FF treatment
        # here. Same MultiReg idiom add_milan_datapath() uses for the CSR IRQ.
        # NAME the two signals explicitly: migen derives wire names from the assignment
        # frame, and a tuple assignment (`a, b = Signal(), Signal()`) leaves one of them
        # with a degenerate name in the generated .v (`wire milanmac;` - verified).
        link_up_cd     = Signal(name="link_up_cd")
        full_duplex_cd = Signal(name="full_duplex_cd")
        self.specials += [
            MultiReg(self.link_status.fields.link_up,     link_up_cd,     odomain=milan_cd),
            MultiReg(self.link_status.fields.full_duplex, full_duplex_cd, odomain=milan_cd),
        ]

        # ---- RMON event pulses (STAT window 0x210..0x230 / STATS_CAP 0x204) -------
        # THE FIX for "RMON reads zero on both boards" (root-caused 2026-07-22,
        # re-confirmed on silicon 2026-07-26): `ethernet_events` + `event_counter`
        # were unit-tested, wired into milan_csr and documented in REGISTER_MAP,
        # and every lane still read 0 forever, because this glue tied
        # `i_mac_events` to the literal 0. LiteEth genuinely exposes no
        # Forencich-style event pulses - but it is NOT silent either, and nothing
        # existed to turn what it DOES expose into pulses. `KL_mac_rmon_events`
        # (hdl/common/eth_event_counter) is that block, deliberately RTL rather
        # than more migen glue: glue is what tied the port off, and glue has no
        # testbench. It derives, at this MAC boundary:
        #   * TX/RX good frames  <- the frame AXIS handshakes (accepted tlast)
        #   * RX_FIFO_BAD_FRAME  <- LiteEth's per-frame `error` field, which the
        #                           CRC32 checker sets on FCS failure and the
        #                           padding checker sets on an undersize runt.
        #                           NOTE this is a real finding of its own: the
        #                           datapath consumes `core.source` WITHOUT that
        #                           flag, so bad frames were being handed to the
        #                           classifier as if good; they are now at least
        #                           counted.
        #   * RX_ERROR_BAD_FCS   <- LiteEth's `crc_errors` counter (CRC32Checker)
        #   * RX_ERROR_BAD_FRAME <- LiteEth's `preamble_errors` counter
        # TX_ERROR_UNDERFLOW / TX_FIFO_OVERFLOW / TX_FIFO_BAD_FRAME /
        # RX_FIFO_OVERFLOW have NO source at this boundary and are NOT faked from
        # AXIS backpressure - they stay 0 and say so through `cap_o` (0x204), so
        # software can tell "structurally silent" from "nothing went wrong".
        # The counters live in `milan_cd`; the MAC boundary is `macsys`, so the
        # module owns the crossing (one cdc_pulse per lane, per-frame rates).
        n_lane         = _eth_event_lanes()
        mac_events     = Signal(n_lane, name="mac_rmon_events")
        mac_events_cap = Signal(n_lane, name="mac_rmon_cap")
        rx_bad_frame   = Signal(name="mac_rmon_rx_err")
        self.comb += rx_bad_frame.eq(self.core.source.error != 0)
        # `rx_datapath` only owns these two counters when the core was built with
        # preamble/CRC checking; parameterise the module off the same fact so the
        # capability mask can never over-claim (getattr, not a bare attribute:
        # a with_preamble_crc=False core has no such CSRs at all).
        rx_dp_stage  = self.core.rx_datapath
        fcs_cnt      = getattr(rx_dp_stage, "crc_errors",      None)
        align_cnt    = getattr(rx_dp_stage, "preamble_errors", None)
        self.specials += Instance("KL_mac_rmon_events",
            p_HAS_FCS_CHECK_P   = 1 if fcs_cnt   is not None else 0,
            p_HAS_ALIGN_CHECK_P = 1 if align_cnt is not None else 0,
            # the per-frame `error` field only ever gets set by the checker
            # stages; no checkers, no flag - so gate the claim on the same fact
            # rather than asserting it. Under-claiming is the safe direction:
            # an unclaimed lane reads as "not supported", never as "all clean".
            p_HAS_RX_ERR_FLAG_P = 1 if fcs_cnt is not None else 0,
            i_mac_clk_i       = ClockSignal("macsys"),
            i_mac_rst_n       = ~ResetSignal("macsys"),
            i_attached_i      = 1,        # a real MAC drives this boundary
            i_mac_tx_tvalid_i = self.core.sink.valid,
            i_mac_tx_tready_i = self.core.sink.ready,
            i_mac_tx_tlast_i  = self.core.sink.last,
            i_mac_rx_tvalid_i = self.core.source.valid,
            i_mac_rx_tready_i = self.core.source.ready,
            i_mac_rx_tlast_i  = self.core.source.last,
            i_mac_rx_err_i    = rx_bad_frame,
            i_fcs_err_cnt_i   = fcs_cnt.status   if fcs_cnt   is not None else 0,
            i_align_err_cnt_i = align_cnt.status if align_cnt is not None else 0,
            i_dp_clk_i        = ClockSignal(milan_cd),
            i_dp_rst_n        = ~ResetSignal(milan_cd),
            o_events_o        = mac_events,
            o_cap_o           = mac_events_cap,
        )

        self.dp_ports = dict(
            o_o_mac_reinit      = self.reinit,
            o_o_eth_rst         = self.eth_rst,
            # ETH GUARD (USER 08-06): exported for future SoC-side gating of
            # the LiteEth phy_crg_reset chain (v2); v1 guards the milan-csr
            # levers inside the datapath and statd respects the CSR
            o_o_eth_guard       = self.eth_guard,
            o_m_axis_mac_tx_tdata  = tx_dp.dp.data,  o_m_axis_mac_tx_tkeep = tx_dp.dp.keep,
            o_m_axis_mac_tx_tvalid = tx_dp.dp.valid, o_m_axis_mac_tx_tlast = tx_dp.dp.last,
            i_m_axis_mac_tx_tready = tx_dp.dp.ready,
            i_s_axis_mac_rx_tdata  = rx_dp.dp.data,  i_s_axis_mac_rx_tkeep = rx_dp.dp.keep,
            i_s_axis_mac_rx_tvalid = rx_dp.dp.valid, i_s_axis_mac_rx_tlast = rx_dp.dp.last,
            o_s_axis_mac_rx_tready = rx_dp.dp.ready,
            # MAC status: from the `link_status` CSR above (software-published MDIO
            # autoneg result), NOT constants - see the block comment there for why a
            # CSR is the only honest source on a LiteEth GMII/MII PHY.
            # RMON: real pulses from KL_mac_rmon_events above (this line was
            # `i_i_mac_events = 0` until 2026-07-26 - the tie that made a
            # fully-tested counter block dead in silicon). `cap` tells software
            # which of the nine lanes those pulses actually cover.
            i_i_mac_speed = self.link_status.fields.speed,
            i_i_link_up = link_up_cd, i_i_full_duplex = full_duplex_cd,
            i_i_mac_events = mac_events,
            i_i_mac_events_cap = mac_events_cap,
            i_i_ethrx_tgl = self.ethrx_tgl, i_i_ethtx_tgl = self.ethtx_tgl,
            i_i_ethact_tgl = self.ethact_tgl,
        )


# DMA (§A.6) ---------------------------------------------------------------------------------------


class RingDMAWriter(LiteXModule):
    """Pipeline reference: docs/fpga/PIPELINE_STAGES.md (stages R3-R5: slots, pages,
    CQ/BD publication, every knob with measured effects) and
    docs/RX_PERF_TUNING_MAP.drawio. STRICT driver pairings live there too.

    AXIS-frame -> circular-DRAM-ring **AXI burst** DMA writer (RX upgrade v2, 2026-07-04).

    v1 (wishbone) taught two HW lessons, both measured on silicon via the pipeline
    telemetry (rx_dma: 18 stall-cycles/beat @ 50 MHz):
      1. one classic-Wishbone write per 8-byte beat costs the full coherent-bus round
         trip (~38 sys cycles) -> ~21 MB/s sustained drain vs the 125 MB/s wire. Every
         frame longer than the ~70-beat upstream elasticity (LiteEth RX CDC + datapath
         FIFOs) overflowed MID-FRAME: the GMII side cannot stall the wire, so beats  - 
         including `last`  -  vanished silently and frames merged (ping -s 600 fine,
         -s 800 dead, 100% loss).
      2. any transient sink backpressure reaches LiteEth. The DMA must be ALWAYS READY.

    v2 therefore:
      * ingress = store-and-forward frame FIFO with whole-frame drop-when-full:
        `sink.ready` is CONSTANT 1, so upstream can never overflow/corrupt. The drop
        decision is taken at frame start (reserving one max frame); dropped frames
        bump `dropped`. Frames longer than `max_frame_beats` are truncated (cannot
        happen from the MAC; safety only).
      * drain = native AXI4 burst master on the NaxRiscv coherent dma_bus (the port
        is full AXI4  -  the wishbone adapter was the bottleneck, not the CPU). The
        frame length is known up front, so the header streams FIRST in the same
        burst sequence; bursts are <= `burst_beats` beats, split at the ring-wrap
        and 4 KB boundaries; `wr_ptr` only advances after the LAST B response, so
        software still never observes a partial frame.
      * ring full -> the buffered frame is discarded from the FIFO, `dropped`++.

    Ring protocol (BYTES, 8-aligned, wrap via `mask`)  -  UNCHANGED from v1, driver-ABI
    compatible: frame slot = 8-byte header + payload padded to 8 B; header word =
    {rsvd[31:0], seq[15:0], length[15:0]} (length = padded payload bytes); frames may
    wrap the ring end (software splits the copy).

    CSRs (7 words, same footprint/order as v1 and as the simple-mode block before it  - 
    the DT `dma-rx` window and every downstream CSR address stay put):
      base[64] | mask[32] | wr_ptr[32] RO | rd_ptr[32] RW | enable[1] | dropped[32] RO
    """
    def __init__(self, bus, max_frame_beats=512, fifo_beats=2048, burst_beats=16,
                 n_slots=4, cq_depth=8, hs_capable=True, hs_page_bytes=4096,
                 legacy_ring=True, rsc_capable=True):
        # hs_page_bytes (hsq10): posted-page size the hs page-crossing arithmetic
        # assumes  -  MUST match the driver's page-pool order (STRICT pairing, kl-eth
        # hsplit12 `hs_pgsz`). 16384 quadruples the posted-pool burst absorbency
        # (60 pages: 240KB->960KB/queue = the legacy 0-drop regime) at the cost of
        # coarser page granularity. Power of two; only three sites use it (the
        # crossing compare + the two mod-page slices).
        # legacy_ring (AREA-70 byte-ring fold, 2026-07-11): False elaborates OUT
        # the byte-ring datapath (the bd_base==0 fallback ABI)  -  every shape mux
        # hardwires to the BD arm and the ring dispatch/commit arms are not
        # generated. bd_mode remains the runtime ARMING gate: unarmed + enabled
        # = frames back up the drop-FIFO (counted ingress drops), NEVER a DMA
        # write via base.storage/addr 0 (the lethal-pairing lesson applied to
        # old bd=0 drivers on folded gateware). See docs/fpga/PIPELINE_STAGES.md.
        # rsc_capable (rxq2-sans-RSC fold, 2026-08-01): False elaborates OUT the
        # RSC coalescing engine - the header-capture regfile + eth/IP/TCP parse,
        # the n_slots aggregate state with its MATCH/DISPATCH pipeline and
        # timers, ACK-run merging, the append rotator and every header-split
        # state - keeping the plain single-frame BD path, which is ALSO the
        # runtime rsc_en=0 path: drivers see a supported mode where every BD is
        # a v1 single (the path all non-TCP traffic takes today) and coalescing
        # simply never arms. Every RSC/hs CSR KEEPS its offset (the driver bakes
        # them in): the storages stay, nothing reads them; status CSRs read 0.
        # The 2-queue steering front-end is outside this class and untouched.
        assert hs_page_bytes & (hs_page_bytes - 1) == 0
        assert hs_page_bytes <= 32768   # v3 w0[31:16] carries the page fill length
        PGB = hs_page_bytes.bit_length() - 1
        self.bus  = bus                 # axi.AXIInterface(data_width=64), byte-addressed
        self.sink = sink = stream.Endpoint([("data", 64), ("keep", 8)])

        self.base    = CSRStorage(64, description="Ring base address (bytes, 8-aligned).")
        self.mask    = CSRStorage(32, description="Ring size-1 (size = power of two).")
        self.wr_ptr  = CSRStatus(32,  description="HW write pointer (committed frames).")
        self.rd_ptr  = CSRStorage(32, description="SW read pointer (consumed up to here).")
        self.enable  = CSRStorage(1,  description="Ring enable.")
        self.dropped = CSRStatus(32,  description="Whole frames dropped (ingress/ring full).")
        # Pointer-writeback shadow (perf, 2026-07-05): after each frame commit the engine
        # DMA-writes {dropped[63:32], wr_ptr[31:0]} to this coherent 8-byte address, so the
        # driver detects new frames by reading the shadow FROM CACHE instead of stalling the
        # in-order CPU on an MMIO wr_ptr/dropped CSR read every poll (the measured hot-path
        # cost  -  backing the poll off 200us->4ms alone gave +32% RX). 0 = writeback off.
        self.status  = CSRStorage(64, description="Coherent addr of the {dropped,wr_ptr} writeback shadow (0=off).")
        # RX-path telemetry (2026-07-05): make the interrupt/CPPI behaviour observable  - 
        # `frames` = HW-committed frame count (vs the driver's rx_packets shows SW keeping up);
        # `occ_hi` = ring occupancy high-water in bytes (near 0 => latency-bound / starving,
        # near `mask` => driver too slow / filling); `irqs` = empty->non-empty edges (~one per
        # IRQ batch, so frames/irqs = batching factor). Also exposes `non_empty` for ev.rx.
        self.frames  = CSRStatus(32, description="RX frames committed (HW delivered).")
        self.occ_hi  = CSRStatus(32, description="Ring occupancy high-water (bytes used, max seen).")
        self.irqs    = CSRStatus(32, description="ev.rx rising edges (empty->non-empty; ~one per IRQ batch).")
        # ---- BD (buffer-descriptor) mode  -  CPPI-style zero-copy RX (P2/P4, 2026-07-05) ----
        # Instead of the byte-ring, the driver POSTS per-frame buffers (write the 8-aligned
        # phys addr to `post`; 64-deep FIFO) and the engine DMA-writes each frame's payload
        # STRAIGHT into the next posted buffer (no ring, no header, no driver memcpy), then
        # DMA-writes a 16 B completion BD {magic,seq,len,csum | buf_addr} into a coherent
        # DRAM BD ring. The driver detects frames by reading the BD from CACHED memory (one
        # coherent read)  -  no wr_ptr MMIO, no DRAM header read, no 35 us/1500 B copy (the
        # two measured per-frame costs, LATENCY_INVESTIGATION §4-6). No posted buffer when a
        # frame arrives => whole-frame drop (`dropped`++)  -  the always-ready invariant holds.
        # bd_base==0 (reset) = BD mode off => the legacy byte-ring path is bit-identical.
        # In BD mode the existing ring CSRs are REUSED for the BD ring: `mask` = BD-ring
        # bytes-1 (entries*16-1), `wr_ptr` = HW BD write offset, `rd_ptr` = SW consumed-BD
        # offset  -  so `non_empty` (ev.rx), occupancy telemetry and the IRQ path all work
        # unchanged; `base` is unused. BD (16 B, 2 beats, little-endian):
        #   word0 = {drops[15:0], csum[15:0], len_bytes[15:0], seq[7:0], magic 0xBD}
        #   word1 = posted buffer phys addr (debug/robustness; consumption order == post order)
        #   len_bytes = the TRUE frame byte length (gPTP RX-pad fix: single-frame BDs
        #   subtract the last beat's invalid bytes; RSC aggregates were always parse-
        #   derived). The DMA itself still moves whole 8-byte beats - only the report
        #   changed, so old drivers (which size the skb from len) need no change and
        #   the kl-eth PTP-trim becomes a no-op on this gateware.
        self.post    = CSRStorage(32, description="Write a posted RX buffer phys addr (8-aligned, >= max frame). FIFO of 64.")
        self.bd_base = CSRStorage(64, description="Completion-BD ring base (coherent, 16 B/entry, 16-aligned). 0 = BD mode off.")
        self.posted  = CSRStatus(8,   description="Posted buffers currently queued (telemetry).")

        # # #

        drops   = Signal(32)
        seq     = Signal(16)
        wr      = Signal(32)            # committed ring write offset (== wr_ptr CSR)
        # ---- M1 telemetry (CAMPAIGN_500_PLAN): WHY aggregates close + coalesce ratio.
        # Counted at the close-ARMING sites (psh / seg-cap / idle-timeout / parked-
        # newcomer|mack); v2_segs accumulates each closed aggregate's segment count so
        # Σsegs/v2_cnt = the measured coalescing factor. Snapped by MilanDebug.
        close_psh  = Signal(32)
        close_cap  = Signal(32)
        close_tout = Signal(32)
        close_park = Signal(32)
        close_age  = Signal(32)         # lifetime cap closes (multi-slot HOL bound)
        close_prs  = Signal(32)         # CQ pressure closes (head-of-line open slot)
        v2_cnt     = Signal(32)
        v2_segs    = Signal(32)
        self.dbg_close_psh, self.dbg_close_cap = close_psh, close_cap
        self.dbg_close_tout, self.dbg_close_park = close_tout, close_park
        self.dbg_close_age, self.dbg_close_prs = close_age, close_prs
        self.dbg_v2_cnt, self.dbg_v2_segs = v2_cnt, v2_segs
        frames  = Signal(32)           # committed frame counter (telemetry)
        occ_hi  = Signal(32)           # occupancy high-water (telemetry)
        irq_cnt = Signal(32)           # non_empty rising edges (telemetry)
        ne_prev = Signal()
        self.non_empty = Signal()      # -> ev.rx.trigger (level RX-completion interrupt)
        self.comb += [
            self.wr_ptr.status.eq(wr),
            self.dropped.status.eq(drops),
            self.frames.status.eq(frames),
            self.occ_hi.status.eq(occ_hi),
            self.irqs.status.eq(irq_cnt),
            self.non_empty.eq(wr != self.rd_ptr.storage),
        ]
        self.sync += [
            ne_prev.eq(self.non_empty),
            If(~self.enable.storage, irq_cnt.eq(0)).Elif(self.non_empty & ~ne_prev,
                                                         irq_cnt.eq(irq_cnt + 1)),
        ]

        # ---- ingress: always-ready store-and-forward, whole-frame drop ----------------
        self.data_fifo = data_fifo = stream.SyncFIFO([("data", 64)], depth=fifo_beats, buffered=True)
        # `pad` (gPTP RX-pad fix, GPTP_RXPAD_ROOTCAUSE.md): invalid bytes of the frame's
        # LAST beat (0-7, from the ingress `keep`), so BD completions can report the TRUE
        # byte length. 0 when the upstream drives no keep (sim harnesses) = old behavior.
        self.len_fifo  = len_fifo  = stream.SyncFIFO([("beats", 11), ("csum", 16), ("pad", 3)], depth=64)

        # ---- BD mode: posted-buffer FIFO + completion-BD state -------------------------
        bd_mode = Signal()
        self.post_fifo = post_fifo = stream.SyncFIFO([("addr", 32)], depth=64)
        buf_addr_r = Signal(32)         # posted buffer being filled (registered at pop)
        wb_beat    = Signal()           # 0 = BD word0 (meta), 1 = word1 (buf addr)
        post_pop = Signal()             # FSM pops the next posted buffer this cycle
        # ---- RSC phase A (HW_GRO_RSC.md): capture the first 9 beats into a register
        # file and parse eth/IPv4/TCP fields. Phase A is OBSERVE-ONLY (frames still
        # stream unchanged as single-frame BDs); rsc_dbg exposes the parse for sims.
        self.rsc_en = CSRStorage(1, description="RSC parse enable (phase A: observe-only).")
        # capability gate (rxq2-sans-RSC fold): the runtime enable, forced to a
        # constant 0 when the engine is not elaborated - derived from the one
        # elaboration param, never mirrored (same shape trick as hs below).
        rsc_on = self.rsc_en.storage if rsc_capable else C(0)
        hdr_reg  = Array([Signal(64) for _ in range(9)])
        hdr_cnt  = Signal(4)
        hdr_take = Signal(4)            # beats to capture = min(total_beats, 9)
        fbeat    = Signal(12)           # frame-beat index for the regfile replay
        in_hdrr  = Signal()
        def _b(idx):                    # frame byte idx as an 8-bit slice of the regfile
            return hdr_reg[idx >> 3][8*(idx & 7):8*(idx & 7)+8]
        p_eth_ip  = Signal()
        p_ihl5    = Signal()
        p_tcp     = Signal()
        p_nofrag  = Signal()
        p_flags   = Signal(8)
        p_doff    = Signal(4)
        p_eligible = Signal()
        p_seq     = Signal(32)
        p_totlen  = Signal(16)
        self.comb += [
            p_eth_ip.eq((_b(12) == 0x08) & (_b(13) == 0x00)),
            p_ihl5.eq(_b(14) == 0x45),
            p_tcp.eq(_b(23) == 6),
            p_nofrag.eq(((_b(20) & 0x3F) == 0) & (_b(21) == 0)),
            p_flags.eq(_b(47)),
            p_doff.eq(_b(46)[4:8]),
            p_seq.eq(Cat(_b(41), _b(40), _b(39), _b(38))),
            p_totlen.eq(Cat(_b(17), _b(16))),
            # data segment, flags subset {ACK(0x10), PSH(0x08)}, sane doff
            p_eligible.eq((hdr_take >= 7) & p_eth_ip & p_ihl5 & p_tcp & p_nofrag &
                          ((p_flags & 0xE7) == 0) & (p_flags[4]) &
                          (p_doff >= 5) &
                          (p_totlen > (20 + Cat(C(0, 2), p_doff)))),
        ]
        p_ack   = Signal(32)
        p_win   = Signal(16)
        p_plen  = Signal(16)            # exact TCP payload bytes (from ip.tot_len)
        p_soff  = Signal(8)             # payload start byte in the frame = 34 + doff*4
        p_srcip = Signal(32)
        p_dstip = Signal(32)
        p_ports = Signal(32)
        self.comb += [
            p_ack.eq(Cat(_b(45), _b(44), _b(43), _b(42))),
            p_win.eq(Cat(_b(49), _b(48))),
            p_plen.eq(p_totlen - 20 - Cat(C(0, 2), p_doff)),
            p_soff.eq(34 + Cat(C(0, 2), p_doff)),
            p_srcip.eq(Cat(_b(26), _b(27), _b(28), _b(29))),
            p_dstip.eq(Cat(_b(30), _b(31), _b(32), _b(33))),
            p_ports.eq(Cat(_b(34), _b(35), _b(36), _b(37))),
        ]
        # ---- RSC phase C (R2, 2026-07-09): N-slot aggregate state + pop-ordered CQ ----
        # n_slots concurrent aggregates kill the park tax (a different-flow newcomer no
        # longer closes the open aggregate  -  it takes its own slot). Correctness rests on
        # the completion queue below: BDs become VISIBLE strictly in posted-buffer pop
        # order, so the driver's blind FIFO pairing (RX_OVERLOAD_WEDGE.md invariant)
        # holds by construction  -  v2 BDs still carry no address, driver ABI unchanged.
        NS = n_slots
        assert NS >= 1 and (NS & (NS - 1)) == 0, "n_slots must be a power of two (victim wrap)"
        s_open  = Array(Signal(name=f"s_open{i}")       for i in range(NS))
        s_srcip = Array(Signal(32, name=f"s_srcip{i}")  for i in range(NS))
        s_dstip = Array(Signal(32, name=f"s_dstip{i}")  for i in range(NS))
        s_ports = Array(Signal(32, name=f"s_ports{i}")  for i in range(NS))
        s_doff  = Array(Signal(4,  name=f"s_doff{i}")   for i in range(NS))
        s_eseq  = Array(Signal(32, name=f"s_eseq{i}")   for i in range(NS))
        s_off   = Array(Signal(16, name=f"s_off{i}")    for i in range(NS))
        s_buf   = Array(Signal(32, name=f"s_buf{i}")    for i in range(NS))
        s_segs  = Array(Signal(8,  name=f"s_segs{i}")   for i in range(NS))
        s_mss   = Array(Signal(16, name=f"s_mss{i}")    for i in range(NS))
        s_ack   = Array(Signal(32, name=f"s_ack{i}")    for i in range(NS))
        s_win   = Array(Signal(16, name=f"s_win{i}")    for i in range(NS))
        s_psh   = Array(Signal(name=f"s_psh{i}")        for i in range(NS))
        s_idle  = Array(Signal(24, name=f"s_idle{i}")   for i in range(NS))
        s_age   = Array(Signal(24, name=f"s_age{i}")    for i in range(NS))
        s_cq    = Array(Signal(max=cq_depth, name=f"s_cq{i}") for i in range(NS))  # CQ index: MUST track cq_depth (4-bit relic broke CQD=32: closes stamped done on entry&0xF, head starved)
        self.rsc_bufsz = CSRStorage(16, reset=2048, description="RSC aggregate buffer bytes (driver posts this size).")
        self.rsc_tout  = CSRStorage(24, reset=5000, description="RSC aggregate idle-close timeout (milan_clk cycles; 5000 = 100 us @ 50 MHz).")
        # slot selection combs
        slot_hit  = Signal(NS)          # per-slot: open & same flow & in-seq & fits
        agg_match = Signal()
        hit_idx   = Signal(max=max(NS, 2))
        free_any  = Signal()
        free_idx  = Signal(max=max(NS, 2))
        exp_any   = Signal()
        exp_idx   = Signal(max=max(NS, 2))
        exp_age   = Signal()            # exp_idx expired by lifetime (vs idle)
        victim    = Signal(max=max(NS, 2))  # round-robin park victim when all slots busy
        slot_sel  = Signal(max=max(NS, 2))  # slot the in-flight frame operates on
        sel_off   = Signal(16)
        sel_buf   = Signal(32)
        slot_touch_sel = Signal()       # comb strobe from WAIT_B: reset slot_sel's idle timer
        self.comb += [slot_hit[i].eq(s_open[i] & p_eligible &
                                     (p_srcip == s_srcip[i]) & (p_dstip == s_dstip[i]) &
                                     (p_ports == s_ports[i]) & (p_doff == s_doff[i]) &
                                     (p_seq == s_eseq[i]) &
                                     ((s_off[i] + p_plen) <= self.rsc_bufsz.storage))
                      for i in range(NS)]
        # same flow but NOT appendable (seq gap / buffer full): the stale aggregate can
        # never extend  -  close it immediately (v1 park semantics) instead of leaking a
        # second slot for the flow and stranding the first until its idle timeout.
        slot_flow = Signal(NS)
        flow_any  = Signal()
        flow_idx  = Signal(max=max(NS, 2))
        self.comb += [slot_flow[i].eq(s_open[i] & p_eligible & ~slot_hit[i] &
                                      (p_srcip == s_srcip[i]) & (p_dstip == s_dstip[i]) &
                                      (p_ports == s_ports[i]))
                      for i in range(NS)]
        self.comb += flow_any.eq(slot_flow != 0)
        _fl = flow_idx.eq(0)
        for i in reversed(range(NS)):
            _fl = If(slot_flow[i], flow_idx.eq(i)).Else(_fl)
        self.comb += _fl
        self.comb += [
            agg_match.eq(slot_hit != 0),
            free_any.eq(Cat(*[s_open[i] for i in range(NS)]) != (2**NS - 1)),
            sel_off.eq(s_off[hit_idx]),
            sel_buf.eq(s_buf[hit_idx]),
        ]
        _hi = hit_idx.eq(0)
        _fi = free_idx.eq(0)
        for i in reversed(range(NS)):
            _hi = If(slot_hit[i], hit_idx.eq(i)).Else(_hi)
            _fi = If(~s_open[i], free_idx.eq(i)).Else(_fi)
        self.comb += [_hi, _fi]
        # MATCH pipeline stage (timing): the wide per-slot compares + priority encodes
        # + slot-field muxes fed DISPATCH's branch select as one cone (physopt named
        # agg_match/state_reg among the -1.2ns violators). A 1-cycle MATCH state
        # registers them; DISPATCH consumes registers only. Slot state cannot change
        # between MATCH and DISPATCH (the FSM is sequential), and every re-dispatch
        # path re-enters through MATCH so freshly-freed slots are re-evaluated.
        m_hit      = Signal()
        m_hit_idx  = Signal(max=max(NS, 2))
        m_free_any = Signal()
        m_free_idx = Signal(max=max(NS, 2))
        m_flow_any = Signal()
        m_flow_idx = Signal(max=max(NS, 2))
        m_sel_off  = Signal(16)
        m_sel_buf  = Signal(32)
        # per-slot timers: idle (touch-reset) + lifetime age (never reset while open).
        # Idle close keeps latency bounded when a flow stops; the age cap bounds the CQ
        # head-of-line hold a slow-trickle flow could otherwise stretch to ~segcap*tout.
        # agemax_v aliases the rsc_agemax CSR declared AFTER acks_merged (CSR offsets of
        # every pre-existing register must not move  -  the driver bakes them in).
        agemax_v = Signal(24)
        s_exp = Signal(NS)
        s_expage = Signal(NS)
        if rsc_capable:                 # folded: timers undriven => s_exp stays 0
            for i in range(NS):
                self.sync += [
                    If(~s_open[i] | (slot_touch_sel & (slot_sel == i)),
                        s_idle[i].eq(0),
                    ).Elif(s_idle[i] < self.rsc_tout.storage,
                        s_idle[i].eq(s_idle[i] + 1),
                    ),
                    If(~s_open[i],
                        s_age[i].eq(0),
                    ).Elif(s_age[i] < agemax_v,
                        s_age[i].eq(s_age[i] + 1),
                    ),
                ]
                self.comb += [
                    s_expage[i].eq(s_open[i] & (s_age[i] >= agemax_v)),
                    s_exp[i].eq((s_open[i] & (s_idle[i] >= self.rsc_tout.storage)) | s_expage[i]),
                ]
        self.comb += exp_any.eq(s_exp != 0)
        _ei = [exp_idx.eq(0), exp_age.eq(s_expage[0])]
        for i in reversed(range(NS)):
            _ei = If(s_exp[i], exp_idx.eq(i), exp_age.eq(s_expage[i])).Else(_ei)
        self.comb += _ei
        # ---- completion queue: BD visibility in pop order (depth power of 2) ----------
        CQD = cq_depth
        CQB = CQD.bit_length() - 1      # index bits (depth must be a power of two)
        assert (1 << CQB) == CQD
        # CQ word storage in distributed LUTRAM (2026-07-10 slice diet, for 2-queue hs):
        # as Array(Signal(64))×CQD these were 4 Kb of FFs plus a CQD-way write demux at
        # EVERY fill site and a CQD-way read mux at the drain  -  the writer's single
        # biggest slice consumer (hsq6 placed at 96.8% slices). One 128-bit Memory with
        # a sync-write + async-read port (RAM32M) is cycle-exact equivalent: the write
        # lands on the clock edge (= NextValue), the async read feeds the drain comb.
        # Every fill site writes w0|w1 to ONE index per cycle (FSM states are exclusive,
        # CQ_FILL's pv3/meta passes sequential), so a single write port suffices. An
        # entry being filled has done=0 so the drain never reads the address being
        # written in the same cycle. done/hs flags and head/tail stay FFs.
        cq_mem = Memory(128, CQD)
        cq_wp  = cq_mem.get_port(write_capable=True)
        cq_rp  = cq_mem.get_port(async_read=True)
        self.specials += cq_mem, cq_wp, cq_rp

        def cq_write(idx, w0, w1):
            """comb strobe inside an fsm.act branch: sync write, visible next cycle"""
            return [cq_wp.we.eq(1), cq_wp.adr.eq(idx), cq_wp.dat_w.eq(Cat(w0, w1))]
        cq_done = Array(Signal(name=f"cq_done{i}")    for i in range(CQD))
        cq_head = Signal(CQB + 1)       # extra bit: full/empty disambiguation
        cq_tail = Signal(CQB + 1)
        cq_level = Signal(CQB + 1)
        cq_room  = Signal()             # a pop may allocate an entry
        cq_drain = Signal()             # head entry ready to write back
        cq_nhead = Signal(CQB + 1)
        cq_more  = Signal()             # after head retires, next is ready too
        head_open_hit = Signal()        # CQ head entry belongs to a still-open slot
        head_slot     = Signal(max=max(NS, 2))
        self.comb += [
            cq_level.eq(cq_tail - cq_head),
            cq_room.eq(cq_level < (CQD - 1)),
            cq_drain.eq((cq_level != 0) & cq_done[cq_head[:CQB]]),
            cq_nhead.eq(cq_head + 1),
            cq_more.eq((cq_tail != cq_nhead) & cq_done[cq_nhead[:CQB]]),
            cq_rp.adr.eq(cq_head[:CQB]),   # drain only ever reads the head
        ]
        # (hsplit14: metas allocate at CLOSE and pages are done-at-completion, so
        # the only undone head an open slot can own is its PAGE entry  -  s_cq-only
        # matching is complete again; the hsq9 meta-term came and went with the
        # meta-first ordering.)
        cq_pressure = Signal()
        # DRAM BD-ring flow control (2026-07-10): the drain used to write BDs whenever
        # the CQ head was done, so under a reap gap the HW LAPPED the driver's rd and
        # overwrote unread BDs (seq skew of exactly `entries`  -  detected+resynced at 64
        # entries = the -P4 "RX BD desync" storms; silently poisonous at 256 where the
        # 8-bit seq aliases). wr may never catch rd: wr+16==rd IS full (the driver-side
        # "posted max 63" comment is this same rule from the other side). Stalling the
        # drain backs pressure into the CQ, so overload becomes counted ingress drops  - 
        # never corruption. bd_room2 pre-checks the slot AFTER this one for the WB_B
        # drain-chain, where wr has already advanced by 16 in the same cycle.
        bd_room  = Signal()
        bd_room2 = Signal()
        self.comb += [
            bd_room.eq(((wr + 16) & self.mask.storage) != self.rd_ptr.storage),
            bd_room2.eq(((wr + 32) & self.mask.storage) != self.rd_ptr.storage),
        ]
        # sim-introspection aliases (zero hardware: attribute refs only)
        self.dbg_cq_head, self.dbg_cq_tail, self.dbg_cq_done = cq_head, cq_tail, cq_done
        self.dbg_head_open_hit = head_open_hit
        self.dbg_s_open, self.dbg_s_cq = s_open, s_cq
        self.dbg_cq_level = cq_level
        cq_tail1 = Signal(CQB)          # (tail+1) as a plain Signal: Migen array WRITES
        self.comb += cq_tail1.eq((cq_tail + 1)[:CQB])   # need non-computed indices
        cur_cq = Signal(CQB)            # CQ entry allocated by the in-flight pop
        def cq_alloc():
            """allocate the tail CQ entry for a buffer pop (call at post_pop sites)"""
            return [NextValue(cur_cq, cq_tail[:CQB]),
                    NextValue(cq_done[cq_tail[:CQB]], 0),
                    NextValue(cq_tail, cq_tail + 1)]
        # single-level comb hops for each close site's CQ index: cq_w0[s_cq[k]] would
        # nest one Array proxy inside another (k is a Signal)  -  resolve s_cq[k] into a
        # plain Signal first so every Array index stays single-level.
        cq_of_exp  = Signal(CQB)
        cq_of_head = Signal(CQB)
        cq_of_vic  = Signal(CQB)
        cq_of_mflow = Signal(CQB)
        cq_of_sel  = Signal(CQB)
        self.comb += [
            cq_of_exp.eq(s_cq[exp_idx]),
            cq_of_head.eq(s_cq[head_slot]),
            cq_of_vic.eq(s_cq[victim]),
            cq_of_mflow.eq(s_cq[m_flow_idx]),
            cq_of_sel.eq(s_cq[slot_sel]),
        ]
        # v2-close staging (timing): the close cone {slot-field mux(k) + adders -> 64b
        # Cat -> CQ-entry demux(cqi)} failed 100 MHz as one cycle (route WNS -1.2, all
        # violators cq_w1*). stage_close() registers the finished meta + target index;
        # the 1-cycle CQ_FILL state then does the short reg->demux write. Closes are
        # per-aggregate (rare), so the extra cycle is noise.
        meta_w0  = Signal(64)
        meta_w1  = Signal(64)
        meta_cqi = Signal(CQB)
        cqf_ret_match = Signal()        # CQ_FILL exit: 1 = re-dispatch (MATCH), 0 = IDLE
        def stage_close(k, cqi, mcqi, ret_match, extra_segs=0):  # mcqi: dead since hsplit14
            """stage slot k's close: legacy = one v2 BD into `cqi` (the open-pop entry);
            header-split = last-page v3 into `cqi` (w1 = current page) + v2 meta into
            `mcqi` (hs layout: len = payload+hdrlen, tag = k, hdr_idx). CQ_FILL commits
            next cycle(s). seq/drops are patched at drain (WB_W)."""
            hdrlen = 34 + Cat(C(0, 2), s_doff[k])          # 14 + 20 + 4*doff (ihl=5)
            k2 = Signal(2)
            self.comb += k2.eq(k)                          # slot tag, width-forced
            return [If(hs,
                        NextValue(meta_w0,
                            Cat(C(0xBD, 8), C(0, 8), (s_off[k] + hdrlen)[:16], s_mss[k],
                                C(0, 6), k2, C(1, 1), s_psh[k], C(0, 1), s_hidx[k])),
                        NextValue(pv3_cqi, cqi),
                        NextValue(pv3_addr, s_buf[k]),
                        NextValue(pv3_tag, k2),
                        NextValue(pv3_hidx, s_hidx[k]),
                        NextValue(pv3_fill, Mux(s_off[k][:PGB] == 0,
                                                hs_page_bytes, s_off[k][:PGB])),
                        NextValue(pv3_pend, 1),
                    ).Else(
                        NextValue(meta_w0,
                            Cat(C(0xBD, 8), C(0, 8), s_off[k], s_mss[k], C(0, 8),
                                Cat(C(1, 1), s_psh[k], C(0, 6)))),
                        NextValue(pv3_pend, 0),
                        NextValue(meta_cqi, cqi),
                    ),
                    # hsplit14 (hs only): the meta allocates AT CLOSE (drains LAST,
                    # after every page v3  -  pages become visible as they complete).
                    # Callers gate on cq_room. Legacy v2s keep their popped entry.
                    If(hs,
                        NextValue(meta_cqi, cq_tail[:CQB]),
                    NextValue(cq_done[cq_tail[:CQB]], 0),
                    NextValue(cq_tail, cq_tail + 1)
                    ),
                    NextValue(meta_w1,
                        Cat(s_ack[k], s_win[k], s_segs[k], Cat(C(0, 2), s_doff[k]), C(0, 2))),
                    NextValue(cqf_ret_match, ret_match),
                    NextValue(s_open[k], 0),
                    NextValue(v2_cnt, v2_cnt + 1),
                    NextValue(v2_segs, v2_segs + s_segs[k] + extra_segs),
                    NextState("CQ_FILL")]
        # append-path registers (set at DISPATCH  -  keeps cones off the data path)
        ap_append = Signal()            # this frame appends payload-only
        ap_arm    = Signal()            # this frame opens an aggregate at WAIT_B
        ap_p      = Signal(3)           # byte rotate = (s_lane - r_lane) mod 8
        ap_pass   = Signal()            # p == 0 passthrough
        ap_head   = Signal(8)           # first-beat wstrb
        ap_tail   = Signal(8)           # last-beat wstrb
        ap_inrem  = Signal(12)          # input beats still to consume
        ap_flush  = Signal(2)           # trailing pad beats to sink after payload
        ap_carry  = Signal(64)
        ap_prime  = Signal()            # s>r regime: preload one beat into carry
        ap_first  = Signal()            # next W beat is the append's first (head strb)
        self.rsc_dbg = CSRStatus(32, description="RSC parse of the last captured frame: "
                                 "{eligible, doff[3:0], flags[7:0], totlen[15:0]}.")
        # ---- RSC ACK-run merging (2026-07-06): coalesce runs of PURE ACKs ----------
        # A mergeable ACK (flags==ACK only, no payload, doff 5 or the Linux
        # timestamp-only option layout 01 01 08 0A) lives ENTIRELY in hdr_reg
        # (<= 9 beats incl. 60 B pad). One pending slot: a same-flow successor
        # REPLACES it (TCP acks are cumulative  -  the stale one carries nothing);
        # a different flow / idle timeout flushes it as a NORMAL v1 single-frame
        # BD (zero driver change). SACK ACKs (other option layouts) never match
        # the predicate and pass through untouched, preserving loss recovery.
        # Cuts the dominant RX cost of a TX-heavy workload: the per-ACK driver
        # build+GRO (~90 us/ACK at 115 Mbit/s was ~40% of the NAPI hart).
        p_mack = Signal()
        self.comb += p_mack.eq(
            p_eth_ip & p_ihl5 & p_tcp & p_nofrag &
            (p_flags == 0x10) & (p_plen == 0) &
            ((p_doff == 5) | ((p_doff == 8) & (_b(54) == 1) & (_b(55) == 1) &
                              (_b(56) == 8) & (_b(57) == 10))))
        ack_open  = Signal()
        ack_srcip = Signal(32)
        ack_dstip = Signal(32)
        ack_ports = Signal(32)
        ack_hdr   = Array([Signal(64) for _ in range(9)])
        ack_beats = Signal(11)          # captured frame beats (BD len = beats*8 - pad)
        ack_pad   = Signal(3)           # captured frame's last-beat pad
        ack_csum  = Signal(16)
        ack_wb    = Signal()            # W stage streams from ack_hdr (flush in flight)
        ack_ret   = Signal()            # after the flush WB: 1 = re-DISPATCH newcomer
        nc_pad    = Signal(3)           # parked newcomer's last-beat pad
        nc_beats  = Signal(11)          # parked newcomer's geometry (the flush reuses
        nc_csum   = Signal(16)          # frame_beats/frame_csum; restore at WB_B)
        ack_match = Signal()
        self.acks_merged = CSRStatus(32, description="Pure ACKs absorbed by ACK-run merging (telemetry).")
        ack_timer = Signal(24)
        ack_touch = Signal()
        ack_expired = Signal()
        self.comb += [
            ack_match.eq(ack_open & (p_srcip == ack_srcip) &
                         (p_dstip == ack_dstip) & (p_ports == ack_ports)),
            ack_expired.eq(ack_open & (ack_timer >= self.rsc_tout.storage)),
        ]
        ack_merged = Signal(32)
        self.comb += self.acks_merged.status.eq(ack_merged)
        # R2 geometry knobs  -  declared LAST so every pre-existing CSR keeps its offset
        # (the driver hardcodes them). segcap replaces the v1 `agg_segs == 15` constant;
        # agemax bounds an open slot's total lifetime (CQ head-of-line + delivery bound).
        self.rsc_segcap = CSRStorage(8, reset=15, description="RSC aggregate segment cap (close after this many merged segments).")
        self.rsc_agemax = CSRStorage(24, reset=200000, description="RSC aggregate lifetime cap in cycles (2 ms @ 100 MHz); bounds CQ head-of-line hold.")
        self.comb += agemax_v.eq(self.rsc_agemax.storage)
        # R-3 header-split (HEADER_SPLIT_DESIGN.md): payload at offset 0 of order-0
        # 4 KB posted pages + opener headers to a side ring -> every full frag is
        # tcp_zerocopy_receive-mappable. hs_en=0 (reset) keeps all paths bit-exact.
        self.hs_en = CSRStorage(1, description="Header-split mode (driver must post 4 KB pages + set hs_hdr_base).")
        self.hs_hdr_base = CSRStorage(64, description="Header ring base (32 x 128 B, coherent). Opener header lands at slot v2.w0[63:59].")
        hs = Signal()
        # hs_capable=False (2nd queue) forces hs=0 so synthesis prunes the header-split
        # datapath + HS_* states  -  the CSRs stay (map-stable) but the area is gone,
        # relieving the datapath congestion that the full 2-queue hs build hit (mac_cam
        # WNS -0.105). q0-only hs is the first-silicon proof vehicle.
        self.comb += hs.eq(C(1 if hs_capable else 0) & self.hs_en.storage &
                           bd_mode & rsc_on)
        hdr_ctr = Signal(5)             # free-running header-slot allocator (32 slots:
                                        # outstanding v2s are BD-ring/pool bounded < 32)
        hw_cnt  = Signal(4)             # header-write beat counter (fbeat stays for payload)
        s_hidx  = Array(Signal(5,  name=f"s_hidx{i}") for i in range(NS))   # header slot
        cq_hs   = Signal(CQD)           # per-entry hs-drop6-layout flag (bit-vector: the
                                        # packed 1-bit Array miscompiled under FSM NextValue)
        pv3_cqi  = Signal(CQB)          # staged last-page v3 fill (closes emit v3 + meta)
        pv3_addr = Signal(32)
        pv3_pend = Signal()
        pv3_tag  = Signal(2)
        pv3_hidx = Signal(5)            # hsplit14: v3 carries hdr_idx (early header bind)
        pv3_fill = Signal(16)           # hsplit14: bytes in THIS page (last page: partial)
        drops6   = Signal(6)            # saturating drops for hs BDs ([53:48])
        self.comb += drops6.eq(Mux(drops > 63, 63, drops[:6]))
        slot_tag2 = Signal(2)
        self.comb += slot_tag2.eq(slot_sel)
        self.dbg_pv3_pend, self.dbg_pv3_cqi, self.dbg_meta_cqi = pv3_pend, pv3_cqi, meta_cqi
        # CQ head-of-line detector: an open slot blocks the head via its current
        # PAGE entry (s_cq). Pressure force-closes it; the close allocates its meta
        # at the tail (hsplit14 ordering: pages drain as they complete, meta last).
        _hs = [head_open_hit.eq(0), head_slot.eq(0)]
        for i in reversed(range(NS)):
            _hs = If(s_open[i] & (s_cq[i] == cq_head[:CQB]) & (cq_level != 0),
                     head_open_hit.eq(1), head_slot.eq(i)).Else(_hs)
        self.comb += _hs
        self.comb += cq_pressure.eq((cq_level >= (CQD - 2)) & head_open_hit)
        cur_hidx = Signal(5)
        hs_cross = Signal()             # this frame swapped pages (update s_cq/s_buf)
        ap_needswap = Signal()          # append starts exactly on a page boundary
        cqf_disc    = Signal()          # CQ_FILL exits to DISCARD (famine mid-frame)
        self.comb += [        ]
        if rsc_capable:                 # folded: ack_timer/rsc_dbg undriven (0)
            self.sync += [
                If(~ack_open | ack_touch,
                    ack_timer.eq(0),
                ).Elif(~ack_expired,
                    ack_timer.eq(ack_timer + 1),
                ),
            ]
            self.sync += If(hdr_cnt == hdr_take,
                self.rsc_dbg.status.eq(Cat(p_totlen, p_flags, p_doff, p_eligible)))
        self.comb += in_hdrr.eq(bd_mode & rsc_on &
                                (ack_wb | (fbeat < hdr_cnt)))
        # bd_mode REGISTERED (2026-07-29): the 64-bit bd_base != 0 compare was
        # computed combinationally from the CSR storage and fanned into every
        # dispatch site - the AX csfix build's worst path ran bd_base_storage
        # -> the rx1 data_fifo readable cone at -0.948 (19 levels, 72% route).
        # bd_base is written ONCE at driver init, so arming one cycle later
        # is invisible; the flop kills the compare from every timing path.
        self.sync += bd_mode.eq(self.bd_base.storage != 0)
        self.comb += [
            post_fifo.sink.valid.eq(self.post.re),    # one push per CSR write
        ]
        # SHAPE-vs-GATE split for the fold: bd_shape selects datapath shape (a
        # constant 1 when the byte-ring is folded out => the ring arms of every
        # mux die at synthesis); bd_mode stays the runtime arming gate at every
        # dispatch site in both modes.
        bd_shape = bd_mode if legacy_ring else C(1)
        self.comb += [
            post_fifo.sink.addr.eq(self.post.storage),
            self.posted.status.eq(post_fifo.level),
            # DRAIN the posted-buffer FIFO while the ring is disabled: buffers posted by a
            # previous driver load would otherwise SURVIVE a reload and desync the FIFO<->
            # driver pairing by their count  -  the HW then fills freed memory and every BD
            # pairs with the wrong buffer (silicon bug 2026-07-05: reload -> 100% garbage RX).
            post_fifo.source.ready.eq(post_pop | ~self.enable.storage),
        ]

        in_frame = Signal()             # mid-frame (first beat already seen)
        in_drop  = Signal()             # this frame is being swallowed
        in_beats = Signal(11)           # beats stored for the current frame

        # TIMING (build_ring6): the checksum adders may not load the upstream CDC
        # FIFO's BRAM output directly (BRAM clk-to-out + adder cone missed 100 MHz by
        # -0.36 ns), so the stream is registered once at entry  -  free, because
        # sink.ready is CONSTANT 1 (no handshake to pipeline)  -  and the end-of-frame
        # FOLD runs one cycle AFTER the last beat (delayed length push).
        s_valid = Signal()
        s_data  = Signal(64)
        s_last  = Signal()
        s_keep  = Signal(8)
        self.sync += [
            s_valid.eq(sink.valid),
            s_data.eq(sink.data),
            s_last.eq(sink.last),
            s_keep.eq(sink.keep),
        ]
        self.comb += sink.ready.eq(1)   # THE invariant: upstream is never backpressured

        # RX checksum offload (CHECKSUM_COMPLETE): ones-complement sum of ALL stored
        # bytes (16-bit LE lanes, exactly what the RISC-V kernel's csum_partial computes
        # over the same memory), accumulated as beats stream in and delivered to
        # software in the frame header's spare bits  -  the kernel then skips its own
        # per-byte checksum pass. Invalid last-beat lanes ARE summed on purpose: the
        # padded bytes land in the skb too, so the sum matches the skb contents
        # (pskb_trim_rcsum subtracts trimmed bytes itself).
        # INVARIANT (gPTP RX-pad fix): pad lanes are ZERO on this pipeline (LiteEth
        # converter zero-fills; observed on silicon both PHY paths), so a BD skb built
        # to the TRUE length still matches this sum. If a future ingress can deliver
        # nonzero pad lanes, mask `lanes` by s_keep here (costs one LUT layer in the
        # timing-critical csum cone - that is why it is not done unconditionally).
        lanes    = Signal(18)           # this beat's four 16-bit lanes, summed
        acc      = Signal(30)           # frame accumulator (512 beats max fits easily)
        acc_fin  = Signal(30)           # final acc, registered at end-of-frame
        fold_a   = Signal(17)
        csum16   = Signal(16)

        pend       = Signal()           # a length+csum push is due (1 cycle after last)
        pend_beats = Signal(11)
        pend_pad   = Signal(3)          # last-beat invalid bytes (from registered keep)
        keep_pop   = Signal(4)          # popcount of the (registered) last-beat keep
        last_pad   = Signal(3)

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
            # keep==0 = upstream drives no byte mask (unit sims): report pad 0, i.e.
            # the padded length - exactly the pre-fix behavior. Real ingress always
            # drives keep (0xFF mid-frame, last_be-derived mask on last).
            keep_pop.eq(sum([s_keep[i] for i in range(8)])),
            last_pad.eq(Mux(keep_pop == 0, 0, 8 - keep_pop)),
            len_fifo.sink.valid.eq(pend),
            len_fifo.sink.beats.eq(pend_beats),
            len_fifo.sink.csum.eq(csum16),
            len_fifo.sink.pad.eq(pend_pad),
        ]
        self.sync += [
            # a pending push completes in one cycle (the len FIFO can never be full
            # here: the frame-start drop decision reserved the slot); a new end-of-
            # frame in the same cycle just re-loads pend  -  the old push has completed.
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
                        # truncated frame: the stored tail is not the wire tail - report
                        # the full padded length (safety path, cannot happen from the MAC)
                        pend_pad.eq(Mux(in_beats != max_frame_beats, last_pad, 0)),
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
        # address/length before AW. Costs 1-2 cycles per <=16-beat burst  -  noise.
        frame_beats = Signal(11)        # payload beats of the frame being written
        pad_r       = Signal(3)         # its last-beat pad (BD len reports beats*8 - pad)
        total_beats = Signal(12)        # + header (registered in IDLE)
        wcnt        = Signal(9)         # W beats sent in the current burst
        disc        = Signal(11)        # beats left to discard (ring full)
        outstanding = Signal(6)         # AW issued minus B received
        off_r       = Signal(32)        # ring byte offset of the next beat to issue
        rem_r       = Signal(12)        # beats (incl. header) not yet issued
        blen_r      = Signal(10)        # burst length, registered in PREP
        blen_m1     = Signal(10)        # blen_r - 1, registered beside it (the same
                                        # per-beat-cone hoist as the reader's)
        rem_z       = Signal()          # rem_r == 0 as of this burst's AW-accept
        burst_last  = Signal()          # wcnt == blen_m1
        addr_r      = Signal(32)        # burst address, registered in PREP
        hdr_sent    = Signal()
        frame_csum  = Signal(16)        # ones-complement sum for CHECKSUM_COMPLETE

        # ring-fit check for the WHOLE frame (header+payload+8 spare so wr never == rd
        # when full)  -  evaluated in CHECK from registered frame_beats.
        used, free, need = Signal(32), Signal(33), Signal(15)
        no_fit = Signal()
        self.comb += [
            used.eq((wr - self.rd_ptr.storage) & self.mask.storage),
            free.eq(self.mask.storage + 1 - used),
            need.eq(((frame_beats + 1) << 3) + 8),
            no_fit.eq(free < need),
        ]
        # telemetry high-water, reset when the ring is disabled (driver re-init clears the
        # stale `wr-rd` spike a reload would otherwise latch  -  occ_hi is now per-session).
        self.sync += If(~self.enable.storage, occ_hi.eq(0)).Elif(used > occ_hi, occ_hi.eq(used))

        # burst geometry from the REGISTERED off_r/rem_r (registered again in PREP)
        cur_addr = Signal(32)
        to_wrap  = Signal(30)           # beats to the ring end
        to_4k    = Signal(10)           # beats to the next 4 KB boundary
        blen_a   = Signal(12)
        blen_b   = Signal(12)
        blen     = Signal(12)
        self.comb += [
            # BD mode: the write target is the posted buffer (linear, never wraps  -  cap the
            # wrap term above the max frame). Ring mode: base+offset with ring-wrap splits.
            cur_addr.eq(Mux(bd_shape, buf_addr_r + off_r,
                                      self.base.storage[:32] + off_r)),
            to_wrap.eq(Mux(bd_shape, max_frame_beats + 1,
                                     (self.mask.storage + 1 - off_r) >> 3)),
            to_4k.eq((4096 - (cur_addr & 0xFFF)) >> 3),
            blen_a.eq(Mux(rem_r > burst_beats, burst_beats, rem_r)),
            blen_b.eq(Mux(blen_a > to_wrap, to_wrap, blen_a)),
            blen.eq(Mux(blen_b > to_4k, to_4k, blen_b)),
        ]

        # W beat 0 of the whole frame is the header (length known up front); commit  -
        # wr_ptr/seq  -  still waits for the last B, so software never sees a partial frame.
        # NOTE (measured 2026-07-11): pinning is_hdr low in folded builds was
        # tried and made the OOC writer BIGGER (5739 -> 6653 LUTs; the constant
        # broke the W-mux sharing pattern and Vivado restructured worse). Leave
        # the runtime term; synthesis already shares it.
        is_hdr    = Signal()
        len_bytes = Signal(16)          # PADDED length: byte-ring header ABI (rd advance
                                        # = 8+len, len&7==0 check) - never changes
        bd_len    = Signal(16)          # TRUE length: single-frame BD w0 (gPTP fix; the
                                        # driver sizes the skb from it, ring/geometry
                                        # never touch it - aggregates are parse-derived)
        self.comb += [
            is_hdr.eq(~hdr_sent),
            len_bytes.eq(frame_beats << 3),
            bd_len.eq((frame_beats << 3) - pad_r),
        ]

        aw_fire = Signal()
        self.comb += [
            aw_fire.eq(self.bus.aw.valid & self.bus.aw.ready),
            self.bus.b.ready.eq(1),
        ]
        self.sync += outstanding.eq(outstanding + aw_fire - self.bus.b.valid)

        def ack_capture():
            """latch the just-parsed pure ACK (fully in hdr_reg) into the pending slot"""
            return ([NextValue(ack_hdr[i], hdr_reg[i]) for i in range(9)] +
                    [NextValue(ack_beats, frame_beats),
                     NextValue(ack_pad, pad_r),
                     NextValue(ack_csum, frame_csum),
                     NextValue(ack_srcip, p_srcip), NextValue(ack_dstip, p_dstip),
                     NextValue(ack_ports, p_ports),
                     NextValue(ack_open, 1),
                     ack_touch.eq(1)])

        def ack_flush(ret):
            """emit the pending ACK as a normal v1 single BD (via ACK_POP);
            ret=1 re-DISPATCHes the frame parked in hdr_reg afterwards"""
            return [
                NextValue(nc_beats, frame_beats),
                NextValue(nc_pad, pad_r),
                NextValue(nc_csum, frame_csum),
                NextValue(frame_beats, ack_beats),
                NextValue(pad_r, ack_pad),
                NextValue(total_beats, ack_beats),
                NextValue(frame_csum, ack_csum),
                NextValue(rem_r, ack_beats),
                NextValue(rem_z, ack_beats == 0),
                NextValue(off_r, 0),
                NextValue(hdr_sent, 1),
                NextValue(fbeat, 0),
                NextValue(ap_append, 0),
                NextValue(ap_arm, 0),
                NextValue(ack_wb, 1),
                NextValue(ack_ret, ret),
                NextValue(ack_open, 0),
                NextState("ACK_POP"),
            ]

        self.fsm = fsm = FSM(reset_state="IDLE")
        # IDLE dispatch, built incrementally so the byte-ring arm is generated
        # only when legacy_ring elaborates the fallback path (AREA-70 fold),
        # and the RSC arms only when rsc_capable elaborates the engine.
        idle_disp = (
            # While the ring is disabled, hold wr/seq/frames at 0 so a driver re-init (which
            # toggles enable) starts a truly-empty ring  -  no stale mid-ring `wr` for the fresh
            # rd=0 to read as ~full (the occ_hi reload artifact), and per-session `frames`.
            If(~self.enable.storage,
                NextValue(wr, 0), NextValue(seq, 0), NextValue(frames, 0),
                *([NextValue(s_open[i], 0) for i in range(NS)] +
                  [NextValue(cq_done[i], 0) for i in range(CQD)] +
                  [NextValue(cq_hs, 0)] +
                  [NextValue(cq_head, 0), NextValue(cq_tail, 0), NextValue(victim, 0),
                   NextValue(pv3_pend, 0), NextValue(cqf_disc, 0), NextValue(hs_cross, 0)]),
                NextValue(ack_open, 0), NextValue(ack_wb, 0),
                NextValue(ack_merged, 0),
            ).Elif(bd_mode & cq_drain & bd_room,
                # pop-ordered BD visibility: write back every ready head entry first
                # (bd_room: never lap the driver's rd  -  stall here, not corrupt there)
                NextState("WB_AW"),
            )
        )
        if rsc_capable:
            idle_disp = idle_disp.Elif(bd_mode & exp_any & cq_room,
                # RSC: close an idle-expired (or lifetime-capped) slot; its BD becomes
                # drainable and the (possibly blocked) CQ head advances. 1-cycle action.
                If(exp_age,
                    NextValue(close_age, close_age + 1),
                ).Else(
                    NextValue(close_tout, close_tout + 1),
                ),
                *stage_close(exp_idx, cq_of_exp, 0, 0),
            ).Elif(bd_mode & cq_pressure & cq_room,
                # CQ backpressure: the head entry's slot is still open while the queue
                # fills behind it  -  force-close it so completions keep flowing.
                NextValue(close_prs, close_prs + 1),
                *stage_close(head_slot, cq_of_head, 0, 0),
            )
        if rsc_capable:
            # RSC gateware: head beats detour through the parse regfile; the
            # posted-buffer pop is decided at DISPATCH.
            bd_disp = If(rsc_on,
                NextValue(hdr_cnt, 0),
                NextValue(fbeat, 0),
                NextValue(hdr_take, Mux(len_fifo.source.beats > 9, 9,
                                        len_fifo.source.beats)),
                NextState("HDR_CAP"),        # buffer pop decided at DISPATCH
            ).Elif(post_fifo.source.valid & cq_room,
                post_pop.eq(1),
                *cq_alloc(),
                NextValue(buf_addr_r, post_fifo.source.addr),
                NextState("PREP"),
            ).Else(                                          # no buffer/CQ room -> drop
                NextValue(disc, len_fifo.source.beats),
                NextState("DISCARD"),
            )
        else:
            # folded: every frame is a plain single v1 BD (the runtime rsc_en=0
            # dispatch, made the only shape)
            bd_disp = If(post_fifo.source.valid & cq_room,
                post_pop.eq(1),
                *cq_alloc(),
                NextValue(buf_addr_r, post_fifo.source.addr),
                NextState("PREP"),
            ).Else(                                          # no buffer/CQ room -> drop
                NextValue(disc, len_fifo.source.beats),
                NextState("DISCARD"),
            )
        idle_disp = idle_disp.Elif(len_fifo.source.valid & bd_mode,
            # BD/zero-copy mode: payload -> the next POSTED buffer, meta -> a BD.
            len_fifo.source.ready.eq(1),
            NextValue(frame_beats, len_fifo.source.beats),
            NextValue(pad_r, len_fifo.source.pad),
            NextValue(total_beats, len_fifo.source.beats),   # no header beat
            NextValue(frame_csum, len_fifo.source.csum),
            NextValue(rem_r, len_fifo.source.beats),
            NextValue(rem_z, len_fifo.source.beats == 0),
            NextValue(off_r, 0),
            NextValue(hdr_sent, 1),                          # suppress the header
            bd_disp,
        )
        if rsc_capable:
            idle_disp = idle_disp.Elif(bd_mode & ack_expired & cq_room,
                # ACK-run idle-timeout  -  deliver the latest pending ACK. The historical
                # ~agg_open gate (RX-wedge fix, 2026-07-08) is GONE: the completion
                # queue serializes BD visibility to pop order by construction, so the
                # flush may pop while aggregates are open  -  its BD simply waits its
                # turn behind theirs (bounded by rsc_tout/rsc_agemax).
                *ack_flush(ret=0)
            )
        if legacy_ring:
            # byte-ring dispatch (the bd_base==0 fallback ABI): frame -> ring
            # header slot + wrapped payload. Folded builds do NOT generate this
            # arm  -  unarmed-but-enabled backs up the drop-FIFO (counted ingress
            # drops), never a write through base.storage.
            idle_disp = idle_disp.Elif(len_fifo.source.valid,
                len_fifo.source.ready.eq(1),        # frame is fully buffered by now
                NextValue(frame_beats, len_fifo.source.beats),
                NextValue(pad_r, 0),                # ring header stays PADDED (ABI)
                NextValue(total_beats, len_fifo.source.beats + 1),
                NextValue(frame_csum, len_fifo.source.csum),
                NextValue(rem_r, len_fifo.source.beats + 1),
                NextValue(rem_z, 0),
                NextValue(off_r, wr),               # header slot first
                NextValue(hdr_sent, 0),
                NextState("CHECK"),
            )
        fsm.act("IDLE", idle_disp)
        # RSC-only states: elaborated only when the engine exists. For capable
        # builds act_rsc IS fsm.act (bit-identical elaboration); folded builds
        # discard the constructed statement trees, so none of these states or
        # their NextState targets are ever created (stage_close's k2 staging
        # comb is the one construction side effect - a dangling wire nothing
        # reads, swept at synthesis).
        act_rsc = fsm.act if rsc_capable else (lambda name, *stmts: None)
        act_rsc("HDR_CAP",              # RSC: consume the head beats into the regfile
            data_fifo.source.ready.eq(1),
            If(data_fifo.source.valid,
                NextValue(hdr_reg[hdr_cnt], data_fifo.source.data),
                NextValue(hdr_cnt, hdr_cnt + 1),
                If(hdr_cnt == hdr_take - 1,
                    NextState("MATCH"),
                )
            )
        )
        # DISPATCH: decide append / close-first / fresh-open / plain single
        s_lane  = Signal(3)
        r_lane  = Signal(3)
        ap_outb = Signal(12)            # output beats for the append
        self.comb += [
            s_lane.eq(p_soff[:3]),
            r_lane.eq(m_sel_off[:3]),   # matched slot's fill point (registered at MATCH)
            ap_outb.eq((r_lane + p_plen + 7)[3:]),
        ]
        tl_lane   = Signal(3)
        self.comb += tl_lane.eq((m_sel_off + p_plen - 1)[:3])

        act_rsc("MATCH",          # register the slot-selection cones (timing stage)
            NextValue(m_hit, agg_match),
            NextValue(m_hit_idx, hit_idx),
            NextValue(m_free_any, free_any),
            NextValue(m_free_idx, free_idx),
            NextValue(m_flow_any, flow_any),
            NextValue(m_flow_idx, flow_idx),
            NextValue(m_sel_off, sel_off),
            NextValue(m_sel_buf, sel_buf),
            NextState("DISPATCH"),
        )
        act_rsc("DISPATCH",
            If(rsc_on & p_mack,
                # pure-ACK run: replace-in-place (cumulative ack), open, or flush
                # the other flow's pending ACK (newcomer re-dispatches). The flush may
                # run with aggregates open  -  the CQ keeps BD order == pop order.
                # NOTE: the frame is FULLY inside hdr_reg (beats <= 9), so absorbing
                # it consumes nothing from data_fifo  -  the disc=0 rule.
                If(ack_match | ~ack_open,
                    *(ack_capture() +
                      [If(ack_match, NextValue(ack_merged, ack_merged + 1)),
                       NextState("IDLE")])
                ).Elif(cq_room,
                    *ack_flush(ret=1)
                ).Else(
                    # CQ full (extreme corner): flushing would need an entry we don't
                    # have, and staying here would deadlock (drain runs from IDLE).
                    # A stale pure ACK is droppable  -  the wire could have lost it  - 
                    # so the newcomer replaces it and the old one counts as dropped.
                    *(ack_capture() + [NextValue(drops, drops + 1), NextState("IDLE")])
                )
            ).Elif(m_hit,
                # payload-only append into the matched slot's buffer
                NextValue(ap_append, 1),
                NextValue(ap_arm, 0),
                NextValue(slot_sel, m_hit_idx),
                NextValue(ap_p, s_lane - r_lane),
                NextValue(ap_pass, s_lane == r_lane),
                NextValue(ap_prime, s_lane > r_lane),
                NextValue(ap_first, 1),
                NextValue(ap_head, 0xFF & (0xFF << r_lane)),
                NextValue(ap_tail, (0x1FF & ((2 << tl_lane) - 1))[:8]),
                NextValue(ap_inrem, (s_lane + p_plen + 7)[3:]),
                NextValue(fbeat, p_soff[3:]),
                NextValue(rem_r, ap_outb),
                NextValue(rem_z, ap_outb == 0),
                NextValue(off_r, Mux(hs, Cat(C(0, 3), m_sel_off[3:PGB]),
                                         Cat(C(0, 3), m_sel_off[3:]))),
                NextValue(ap_needswap, hs & (m_sel_off[:PGB] == 0)),
                NextValue(hs_cross, 0),
                NextValue(buf_addr_r, m_sel_buf),
                NextState("APRIME"),
            ).Elif(m_flow_any & cq_room,
                # same-flow seq-gap / buffer-full: close that slot now (frame stays
                # parked in hdr_reg and re-dispatches into a fresh aggregate)
                NextValue(close_park, close_park + 1),          # M1 telemetry
                *stage_close(m_flow_idx, cq_of_mflow, 0, 1),
            ).Elif(p_eligible & rsc_on & ~m_free_any & cq_room,
                # all slots busy: park-close the round-robin victim (1-cycle CQ fill),
                # then this frame re-dispatches into the freed slot. This is the only
                # interleave park left  -  expect it rare (slots >= concurrent flows).
                NextValue(close_park, close_park + 1),          # M1 telemetry
                NextValue(victim, victim + 1),
                *stage_close(victim, cq_of_vic, 0, 1),
            ).Elif(hs & p_eligible & ~p_flags[3] & post_fifo.source.valid &
                   (cq_level < (CQD - 2)),
                # header-split opener: TWO CQ entries (meta first = drains first,
                # then this page), header slot, payload written at page offset 0
                # through the append rotator (s_lane = soff&7 -> r_lane = 0).
                post_pop.eq(1),
                NextValue(cur_cq, cq_tail[:CQB]),
                NextValue(cq_done[cq_tail[:CQB]], 0),
                NextValue(cq_tail, cq_tail + 1),
                NextValue(cur_hidx, hdr_ctr),
                NextValue(hdr_ctr, hdr_ctr + 1),
                NextValue(buf_addr_r, post_fifo.source.addr),
                NextValue(ap_append, 1),            # W-path in append/rotate mode
                NextValue(ap_arm, 1),               # WAIT_B arms the slot
                NextValue(slot_sel, m_free_idx),
                NextValue(ap_p, s_lane),            # r_lane = 0
                NextValue(ap_pass, s_lane == 0),
                NextValue(ap_prime, s_lane > 0),
                NextValue(ap_first, 1),
                NextValue(ap_head, 0xFF),
                NextValue(ap_tail, (0x1FF & ((2 << (p_plen - 1)[:3]) - 1))[:8]),
                NextValue(ap_inrem, (s_lane + p_plen + 7)[3:]),
                NextValue(fbeat, p_soff[3:]),
                NextValue(rem_r, (p_plen + 7)[3:]),
                NextValue(rem_z, (p_plen + 7)[3:] == 0),
                NextValue(off_r, 0),
                NextValue(hs_cross, 0),
                NextValue(hw_cnt, 0),
                NextState("HS_HAW"),
            ).Elif(post_fifo.source.valid & cq_room,
                post_pop.eq(1),
                *cq_alloc(),
                NextValue(buf_addr_r, post_fifo.source.addr),
                NextValue(ap_append, 0),
                NextValue(ap_arm, p_eligible),      # open an aggregate at WAIT_B
                NextValue(slot_sel, m_free_idx),
                NextValue(ap_first, 0),
                NextState("PREP"),
            ).Else(
                # no free buffer -> drop. A frame with beats <= hdr_take lives ENTIRELY
                # in hdr_reg  -  data_fifo holds none of it, so entering DISCARD with
                # disc=0 would eat 2047 beats of FOLLOWING frames (11-bit wrap) and
                # permanently desync len/data FIFOs (the -P4 RX wedge, 2026-07-06).
                If(frame_beats == hdr_take,
                    NextValue(drops, drops + 1),
                    NextState("IDLE"),
                ).Else(
                    NextValue(disc, frame_beats - hdr_take),
                    NextState("DISCARD"),
                )
            )
        )
        act_rsc("CQ_FILL",         # commit staged BDs (reg -> demux only). hs closes
            If(pv3_pend,               # take two passes: last-page v3, then the meta.
                *cq_write(pv3_cqi,
                    Cat(C(0xBD, 8), C(0, 8), pv3_fill, C(0, 16), C(0, 6),
                        pv3_tag, C(1, 1), C(0, 1), C(1, 1), pv3_hidx),
                    pv3_addr),
                NextValue(cq_done[pv3_cqi], 1),
                NextValue(cq_hs, (cq_hs & ~(C(1, CQD) << pv3_cqi)) | (C(1, 1) << pv3_cqi)),
                NextValue(pv3_pend, 0),
            ).Else(
                *cq_write(meta_cqi, meta_w0, meta_w1),
                NextValue(cq_done[meta_cqi], 1),
                NextValue(cq_hs, (cq_hs & ~(C(1, CQD) << meta_cqi)) | (hs << meta_cqi)),
                If(cqf_disc & (disc != 0),
                    NextValue(cqf_disc, 0),
                    NextState("DISCARD"),
                ).Elif(cqf_ret_match,
                    NextValue(cqf_disc, 0),
                    NextState("MATCH"),
                ).Else(
                    NextValue(cqf_disc, 0),
                    NextState("IDLE"),
                )
            )
        )
        act_rsc("ACK_POP",              # pending-ACK flush: needs a posted buffer
            If(post_fifo.source.valid,
                post_pop.eq(1),
                *cq_alloc(),            # callers guarantee cq_room
                NextValue(buf_addr_r, post_fifo.source.addr),
                NextState("PREP"),
            ).Else(                     # no buffer -> the pending ACK drops whole
                NextValue(drops, drops + 1),
                NextValue(ack_wb, 0),
                If(ack_ret,
                    NextValue(frame_beats, nc_beats),   # restore parked newcomer
                    NextValue(pad_r, nc_pad),
                    NextValue(frame_csum, nc_csum),
                    NextState("MATCH"),
                ).Else(
                    NextState("IDLE"),
                )
            )
        )
        act_rsc("APRIME",
            If(ap_prime,                             # consume ONE source beat into carry
                If(in_hdrr,
                    NextValue(ap_carry, hdr_reg[fbeat[:4]]),
                    NextValue(fbeat, fbeat + 1),
                    NextValue(ap_inrem, ap_inrem - 1),
                    NextState("PREP"),
                ).Elif(data_fifo.source.valid,
                    data_fifo.source.ready.eq(1),
                    NextValue(ap_carry, data_fifo.source.data),
                    NextValue(fbeat, fbeat + 1),
                    NextValue(ap_inrem, ap_inrem - 1),
                    NextState("PREP"),
                )
            ).Else(
                NextState("PREP"),
            )
        )
        if legacy_ring:
            # ring-only admission state (reached solely from the byte-ring
            # dispatch arm above; not generated in folded builds)
            fsm.act("CHECK",
                If(~self.enable.storage | no_fit,
                    NextValue(disc, frame_beats),
                    NextState("DISCARD"),
                ).Else(
                    NextState("PREP"),
                )
            )
        if rsc_capable:
            fsm.act("PREP",                         # register this burst's geometry
                If(hs & ap_append & ((off_r == hs_page_bytes) | ap_needswap),
                    NextState("HS_PGSWAP"),         # page full: v3 + JIT next-page pop
                ).Else(
                    NextValue(blen_r, blen),
                    NextValue(blen_m1, blen - 1),
                    NextValue(addr_r, cur_addr),
                    NextState("AW"),
                )
            )
        else:
            # folded: no hs page swaps (hs is a constant 0) - PREP is pure geometry
            fsm.act("PREP",                         # register this burst's geometry
                NextValue(blen_r, blen),
                NextValue(blen_m1, blen - 1),
                NextValue(addr_r, cur_addr),
                NextState("AW"),
            )
        act_rsc("HS_HAW",           # header-split opener: header -> ring slot
            self.bus.aw.valid.eq(1),
            self.bus.aw.addr.eq(self.hs_hdr_base.storage[:32] + Cat(C(0, 7), cur_hidx)),
            self.bus.aw.len.eq(hdr_take - 1),
            self.bus.aw.size.eq(3),
            self.bus.aw.burst.eq(1),
            If(self.bus.aw.ready,
                NextState("HS_HW"),
            )
        )
        act_rsc("HS_HW",
            self.bus.w.valid.eq(1),
            self.bus.w.data.eq(hdr_reg[hw_cnt]),
            self.bus.w.strb.eq(2**len(self.bus.w.strb) - 1),
            self.bus.w.last.eq(hw_cnt == hdr_take - 1),
            If(self.bus.w.ready,
                NextValue(hw_cnt, hw_cnt + 1),
                If(hw_cnt == hdr_take - 1,
                    NextState("APRIME"),    # payload via the rotator (B's tracked
                )                           # by `outstanding`; WAIT_B syncs all)
            )
        )
        act_rsc("HS_PGSWAP",
            # the CURRENT page is complete: emit its v3 (reg->demux, shallow) and swap
            # to a freshly-popped page. Famine here = close the aggregate with what is
            # fully written (s_off excludes the in-flight frame) and discard its rest.
            # v3 target = the SLOT'S registered page entry (cq_of_sel), NOT cur_cq:
            # cur_cq is a global last-pop register  -  another slot's open/crossing pops
            # between this slot's crossings under interleave, so cur_cq points at the
            # wrong entry and this slot's real page entry stays done=0 forever => the
            # CQ head jams = the multi-flow hs livelock (task #13, sim c5681 fsm=DISCARD).
            *cq_write(cq_of_sel,
                Cat(C(0xBD, 8), C(0, 8), C(hs_page_bytes, 16), C(0, 16), C(0, 6),
                    slot_tag2, C(1, 1), C(0, 1), C(1, 1), s_hidx[slot_sel]),
                buf_addr_r),
            NextValue(cq_done[cq_of_sel], 1),
            NextValue(cq_hs, (cq_hs & ~(C(1, CQD) << cq_of_sel)) | (C(1, 1) << cq_of_sel)),
            NextValue(ap_needswap, 0),
            If(post_fifo.source.valid & cq_room,
                post_pop.eq(1),
                NextValue(cur_cq, cq_tail[:CQB]),
                NextValue(cq_done[cq_tail[:CQB]], 0),
                NextValue(cq_tail, cq_tail + 1),
                NextValue(buf_addr_r, post_fifo.source.addr),
                NextValue(off_r, 0),
                NextValue(hs_cross, 1),
                NextState("PREP"),
            ).Else(
                # famine: stage the meta close (v3 for THIS page just filled above  - 
                # it is the aggregate's last), drop the in-flight frame's tail.
                NextValue(meta_w0,
                    Cat(C(0xBD, 8), C(0, 8),
                        (s_off[slot_sel] + 34 + Cat(C(0, 2), s_doff[slot_sel]))[:16],
                        s_mss[slot_sel], C(0, 6), slot_tag2, C(1, 1),
                        s_psh[slot_sel], C(0, 1), s_hidx[slot_sel])),
                NextValue(meta_w1,
                    Cat(s_ack[slot_sel], s_win[slot_sel], s_segs[slot_sel],
                        Cat(C(0, 2), s_doff[slot_sel]), C(0, 2))),
                NextValue(meta_cqi, cq_tail[:CQB]),
                NextValue(cq_done[cq_tail[:CQB]], 0),
                NextValue(cq_tail, cq_tail + 1),
                NextValue(pv3_pend, 0),
                NextValue(cqf_ret_match, 0),
                NextValue(cqf_disc, 1),
                NextValue(disc, frame_beats - Mux(fbeat > hdr_cnt, fbeat, hdr_cnt)),
                NextValue(s_open[slot_sel], 0),
                NextValue(v2_cnt, v2_cnt + 1),
                NextValue(v2_segs, v2_segs + s_segs[slot_sel]),
                NextValue(close_park, close_park + 1),
                NextValue(drops, drops + 1),
                NextState("CQ_FILL"),
            )
        )
        fsm.act("AW",
            self.bus.aw.valid.eq(1),
            self.bus.aw.addr.eq(addr_r),
            self.bus.aw.len.eq(blen_m1),
            self.bus.aw.size.eq(3),                 # 8 bytes/beat
            self.bus.aw.burst.eq(1),                # INCR
            If(self.bus.aw.ready,
                NextValue(wcnt, 0),
                # BD mode: off_r is a LINEAR offset into the posted buffer  -  masking it with
                # the (BD-ring!) mask wrapped it at ring-size bytes and overwrote the frame
                # head (silicon bug 2026-07-05: >1 KB frames corrupt, ping fine, TCP dead).
                NextValue(off_r, Mux(bd_shape, off_r + (blen_r << 3),
                                     (off_r + (blen_r << 3)) & self.mask.storage)),
                NextValue(rem_r, rem_r - blen_r),
                NextValue(rem_z, rem_r == blen_r),
                NextState("W"),
            )
        )
        raw_beat = Signal(64)           # current source beat (regfile / FIFO / drain-0)
        ap_out   = Signal(64)           # realigned append beat
        ap_srcv  = Signal()             # source valid for this beat
        ap_last  = Signal()             # final beat of the whole append
        self.comb += [
            raw_beat.eq(Mux(ap_inrem == 0, 0,
                        Mux(in_hdrr, hdr_reg[fbeat[:4]], data_fifo.source.data))),
            ap_srcv.eq((ap_inrem == 0) | in_hdrr | data_fifo.source.valid),
            ap_out.eq(Mux(ap_pass, raw_beat,
                      (Cat(ap_carry, raw_beat) >> Cat(C(0, 3), ap_p))[:64])),
            burst_last.eq(wcnt == blen_m1),
            ap_last.eq(rem_z & burst_last),
        ]
        fsm.act("W",
            self.bus.w.valid.eq(Mux(ap_append, ap_srcv,
                                    is_hdr | in_hdrr | data_fifo.source.valid)),
            self.bus.w.data.eq(Mux(is_hdr,
                Cat(len_bytes, seq, frame_csum, Signal(16)),     # {0, csum, seq, len}
                Mux(ap_append, ap_out,
                    Mux(in_hdrr, Mux(ack_wb, ack_hdr[fbeat[:4]],
                                     hdr_reg[fbeat[:4]]),
                        data_fifo.source.data)))),
            self.bus.w.strb.eq(Mux(ap_append,
                                   Mux(ap_first, ap_head, 0xFF) &
                                   Mux(ap_last, ap_tail, 0xFF),
                                   2**len(self.bus.w.strb) - 1)),
            self.bus.w.last.eq(burst_last),
            If(self.bus.w.valid & self.bus.w.ready,
                data_fifo.source.ready.eq(~is_hdr & ~in_hdrr &
                                          (~ap_append | (ap_inrem != 0))),
                NextValue(hdr_sent, 1),
                NextValue(wcnt, wcnt + 1),
                If(ap_append,
                    NextValue(ap_first, 0),
                    NextValue(ap_carry, raw_beat),
                    If(ap_inrem != 0,
                        NextValue(fbeat, fbeat + 1),
                        NextValue(ap_inrem, ap_inrem - 1),
                    )
                ).Elif(~is_hdr,
                    NextValue(fbeat, fbeat + 1),
                ),
                If(self.bus.w.last,
                    If(rem_z,                       # updated at AW: post-burst remaining
                        NextState("WAIT_B"),
                    ).Else(
                        NextState("PREP"),
                    )
                )
            )
        )
        # WAIT_B dispatch, built incrementally: folded builds keep only the
        # plain single-BD commit arm (+ the legacy/quiesce Else).
        if rsc_capable:
            wb_disp = If(bd_mode & ap_arm & ~p_flags[3],
                    # RSC: first frame parked  -  slot_sel opens, BD deferred to close.
                    # hs mode: s_off counts PAYLOAD only (headers live in the side
                    # ring at s_hidx; the meta CQ entry pre-allocated at dispatch).
                    NextValue(s_open[slot_sel], 1),
                    NextValue(s_srcip[slot_sel], p_srcip), NextValue(s_dstip[slot_sel], p_dstip),
                    NextValue(s_ports[slot_sel], p_ports), NextValue(s_doff[slot_sel], p_doff),
                    NextValue(s_eseq[slot_sel], p_seq + p_plen),
                    NextValue(s_off[slot_sel], Mux(hs, p_plen, 14 + p_totlen)),
                    NextValue(s_buf[slot_sel], buf_addr_r),
                    NextValue(s_segs[slot_sel], 1), NextValue(s_mss[slot_sel], p_plen),
                    NextValue(s_ack[slot_sel], p_ack), NextValue(s_win[slot_sel], p_win),
                    NextValue(s_psh[slot_sel], 0),
                    NextValue(s_cq[slot_sel], cur_cq),   # page entry (hs) / only entry
                    NextValue(s_hidx[slot_sel], cur_hidx),
                    NextValue(ap_arm, 0),
                    NextValue(ap_append, 0),
                    NextState("IDLE"),
                ).Elif(bd_mode & ap_append,
                    # RSC: payload appended  -  update slot_sel, maybe close
                    slot_touch_sel.eq(1),                # reset the slot's idle timer
                    NextValue(ap_append, 0),
                    If(p_flags[3] | (s_segs[slot_sel] == self.rsc_segcap.storage),
                        # close with THIS frame folded in  -  staged via CQ_FILL (timing).
                        # hs: last-page v3 (the page this frame ended on) + hs meta.
                        If(hs,
                            NextValue(meta_w0,
                                Cat(C(0xBD, 8), C(0, 8),
                                    (s_off[slot_sel] + p_plen + 34 +
                                     Cat(C(0, 2), s_doff[slot_sel]))[:16],
                                    s_mss[slot_sel], C(0, 6), slot_tag2, C(1, 1),
                                    s_psh[slot_sel] | p_flags[3], C(0, 1),
                                    s_hidx[slot_sel])),
                            NextValue(pv3_cqi, Mux(hs_cross, cur_cq, cq_of_sel)),
                            NextValue(pv3_addr, buf_addr_r),
                            NextValue(pv3_tag, slot_tag2),
                            NextValue(pv3_pend, 1),
                            NextValue(pv3_hidx, s_hidx[slot_sel]),
                            NextValue(pv3_fill,
                                Mux((s_off[slot_sel] + p_plen)[:PGB] == 0,
                                    hs_page_bytes,
                                    (s_off[slot_sel] + p_plen)[:PGB])),
                            NextValue(meta_cqi, cq_tail[:CQB]),
                            NextValue(cq_done[cq_tail[:CQB]], 0),
                            NextValue(cq_tail, cq_tail + 1),
                        ).Else(
                            NextValue(meta_w0,
                                Cat(C(0xBD, 8), C(0, 8), (s_off[slot_sel] + p_plen)[:16],
                                    s_mss[slot_sel], C(0, 8),
                                    Cat(C(1, 1), s_psh[slot_sel] | p_flags[3], C(0, 6)))),
                            NextValue(pv3_pend, 0),
                            NextValue(meta_cqi, cq_of_sel),
                        ),
                        NextValue(meta_w1,
                            Cat(p_ack, p_win, (s_segs[slot_sel] + 1)[:8],
                                Cat(C(0, 2), s_doff[slot_sel]), C(0, 2))),
                        NextValue(cqf_ret_match, 0),
                        NextValue(s_open[slot_sel], 0),
                        # M1 telemetry: s_segs is pre-increment here → final = +1
                        If(p_flags[3],
                            NextValue(close_psh, close_psh + 1),
                        ).Else(
                            NextValue(close_cap, close_cap + 1),
                        ),
                        NextValue(v2_cnt, v2_cnt + 1),
                        NextValue(v2_segs, v2_segs + s_segs[slot_sel] + 1),
                        NextState("CQ_FILL"),
                    ).Else(
                        NextValue(s_off[slot_sel], s_off[slot_sel] + p_plen),
                        NextValue(s_eseq[slot_sel], s_eseq[slot_sel] + p_plen),
                        NextValue(s_segs[slot_sel], s_segs[slot_sel] + 1),
                        NextValue(s_ack[slot_sel], p_ack), NextValue(s_win[slot_sel], p_win),
                        NextValue(s_psh[slot_sel], s_psh[slot_sel] | p_flags[3]),
                        NextValue(s_buf[slot_sel], buf_addr_r),   # page may have swapped
                        If(hs_cross,
                            NextValue(s_cq[slot_sel], cur_cq),
                        ),
                        NextState("IDLE"),
                    )
                ).Elif(bd_mode,
                    # plain single (incl. arm+PSH: eligible-but-pushed -> v1 BD):
                    # fill this pop's CQ entry; seq/drops patched at drain
                    NextValue(ap_arm, 0),
                    *cq_write(cur_cq,
                        Cat(C(0xBD, 8), C(0, 8), bd_len, frame_csum, C(0, 16)),
                        buf_addr_r),
                    NextValue(cq_done[cur_cq], 1),
                    If(ack_wb,
                        # pending-ACK flush payload done; restore a parked newcomer
                        NextValue(ack_wb, 0),
                        If(ack_ret,
                            NextValue(frame_beats, nc_beats),
                            NextValue(pad_r, nc_pad),
                            NextValue(frame_csum, nc_csum),
                            NextState("MATCH"),
                        ).Else(
                            NextState("IDLE"),
                        )
                    ).Else(
                        NextState("IDLE"),
                    )
                )
        else:
            wb_disp = If(bd_mode,
                # plain single v1 BD - the folded build's only BD commit arm
                *cq_write(cur_cq,
                    Cat(C(0xBD, 8), C(0, 8), bd_len, frame_csum, C(0, 16)),
                    buf_addr_r),
                NextValue(cq_done[cur_cq], 1),
                NextState("IDLE"),
            )
        wb_disp = wb_disp.Else(
                    # legacy: byte-ring frame commit (wr advance + optional shadow
                    # writeback). Folded: quiesce  -  reachable only if bd_base is
                    # cleared mid-frame (drivers never do; enable-toggle re-inits);
                    # drop the in-flight frame's commit rather than write anywhere.
                    *([NextValue(wr, (wr + (total_beats << 3)) & self.mask.storage),
                       NextValue(seq, seq + 1),
                       NextValue(frames, frames + 1),   # telemetry: HW-committed frames
                       If(self.status.storage != 0,
                           NextState("WB_AW"),
                       ).Else(
                           NextState("IDLE"),
                       )] if legacy_ring else [NextState("IDLE")])
        )
        fsm.act("WAIT_B", If(outstanding == 0, wb_disp))
        # ---- writeback: ring mode = one 8-byte {dropped, wr_ptr} shadow write (poll from
        # cache, not MMIO); BD mode = the 16-byte completion BD (meta + buf addr) to
        # bd_base+wr. Either way the write happens only AFTER the payload's last B response,
        # so software never observes a frame before its data is globally visible.
        fsm.act("WB_AW",
            self.bus.aw.valid.eq(1),
            self.bus.aw.addr.eq(Mux(bd_shape, self.bd_base.storage[:32] + wr,
                                              self.status.storage[:32])),
            self.bus.aw.len.eq(Mux(bd_shape, 1, 0)),  # BD = 2 beats, shadow = 1
            self.bus.aw.size.eq(3),                   # 8 bytes/beat
            self.bus.aw.burst.eq(1),
            If(self.bus.aw.ready, NextValue(wb_beat, 0), NextState("WB_W")),
        )
        fsm.act("WB_W",
            self.bus.w.valid.eq(1),
            # BD mode: drain the CQ head entry  -  BDs hit memory strictly in posted-
            # buffer pop order (the wedge invariant, now by queue construction). The
            # live `seq`/`drops` fields are OR-patched here so BD sequence numbers
            # reflect WRITE order and drops stay 8-bit at [55:48] ([63:56] belongs to
            # the v2 marker/flags  -  the drops/bit-56 alias, 2026-07-08, stays fixed).
            self.bus.w.data.eq(Mux(bd_shape,
                Mux(wb_beat, cq_rp.dat_r[64:],
                             cq_rp.dat_r[:64] | (seq[:8] << 8) |
                             Mux((cq_hs >> cq_head[:CQB])[0],
                                 (drops6 << 48),          # hs BDs: 6-bit at [53:48]
                                 (drops[:8] << 48))),     # legacy: 8-bit at [55:48]
                Cat(wr, drops))),                     # ring-mode shadow {drops, wr}
            self.bus.w.strb.eq(2**len(self.bus.w.strb) - 1),
            self.bus.w.last.eq(~bd_shape | wb_beat),
            If(self.bus.w.valid & self.bus.w.ready,
                NextValue(wb_beat, 1),
                If(~bd_shape | wb_beat, NextState("WB_B")),
            )
        )
        fsm.act("WB_B",
            If(self.bus.b.valid,
                If(bd_shape,                          # commit: BD slot consumed, frame live
                    NextValue(wr, (wr + 16) & self.mask.storage),
                    NextValue(seq, seq + 1),
                    NextValue(frames, frames + 1),
                    NextValue(cq_done[cq_head[:CQB]], 0),   # retire: clear done+hs so
                    NextValue(cq_hs, cq_hs & ~(C(1, CQD) << cq_head[:CQB])),  # reuse=legacy
                    NextValue(cq_head, cq_head + 1),
                    If(cq_more & bd_room2,            # drain every ready successor now
                        NextState("WB_AW"),           # (room for the slot AFTER the wr
                    ).Else(                           # bump this cycle commits)
                        NextState("IDLE"),
                    )
                ).Else(
                    NextState("IDLE"),
                )
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

        # Phase-0: expose the live AW-outstanding count for MilanDebug.outstanding_hi_probe
        #  -  the write-side depth the AXIInterconnectShared actually grants is the pre-build
        # proxy for the read-side depth TX prefetch would need.
        self.dbg_outstanding = Signal(6)
        self.comb += self.dbg_outstanding.eq(outstanding)
        # sim-only probe of the W-stage source mux (R2 bring-up)
        self.dbg_w = Signal(64)
        self.comb += self.dbg_w.eq(Cat(wcnt, blen_r, rem_r[:10], ap_inrem, fbeat[:8],
                                       hdr_cnt, self.bus.w.valid, self.bus.w.ready,
                                       ap_srcv, in_hdrr, ap_append, ap_prime))


class RingDMAReader(LiteXModule):
    """Circular-DRAM-ring -> AXIS-frame **AXI burst** DMA reader (TX upgrade, 2026-07-04).

    Mirror image of RingDMAWriter, replacing the simple-mode WishboneDMAReader whose
    protocol capped TX two ways (both silicon-measured):
      * one classic-Wishbone read per beat = the full coherent-bus round trip per 8 B
        (same ~38 sys-cycles as the RX writer measured) -> ~21 MB/s = ~170 Mbit/s wire
        ceiling (masked so far by the latency-bound stack, but it also throttles ACK
        egress and thereby PEER->FPGA TCP);
      * one frame in flight with a base/length/enable CSR dance + a DONE wait per
        frame -> the driver poll cadence sat in the TX hot path.

    With the ring, software memcpys a frame into the ring, writes ONE CSR (wr_ptr)
    and returns; hardware walks rd -> wr at burst speed. ~40 MTU frames queue in a
    64 KB ring, so the NIC streams back-to-back while the CPU prepares the next.

    Ring protocol (BYTES, 8-aligned, wrap via `mask`)  -  same slot format as RX:
      * frame slot = 8-byte header + payload padded to 8 B;
      * header word = {rsvd[47:0], length[15:0]}, length = EXACT payload bytes  -  the
        last AXIS beat carries the true byte mask in `keep` (the MAC glue converts it
        to LiteEth's one-hot last_be), so wire frames are no longer 8-padded;
      * frames may wrap the ring end (bursts split there; software splits its memcpy);
      * a nonsense header (len 0 or > max_frame_bytes) can only mean a software bug:
        hardware resyncs rd := wr and drops the ring content rather than streaming
        garbage to the MAC.

    Downstream elasticity: MilanMAC's store-and-forward PacketFIFO (the TX starvation
    fix) launches a frame onto GMII only when fully buffered, so this reader may be
    arbitrarily bursty  -  R-channel backpressure mid-frame is harmless.

    CSRs (7 words  -  SAME footprint as the simple-mode block it replaces, so the DT
    `dma-tx` window and every downstream CSR address stay put; roles mirror RX):
      base[64] | mask[32] | wr_ptr[32] RW | rd_ptr[32] RO | enable[1] | sent[32] RO
    """
    def __init__(self, bus, max_frame_bytes=4096, burst_beats=64,
                 legacy_ring=True):
        # legacy_ring: as in RingDMAWriter (AREA-70 byte-ring fold). The reader
        # side is read-only, so folded builds simply hardwire the BD shape; a
        # doorbell with bd_base==0 parses low DRAM as BDs and lands in the
        # existing bad-BD resync (len 0/oversized -> BD_FLUSH), never a write.
        # burst_beats 16->64 (2026-07-07): the reader is SERIAL (PAY_AR issues one AR,
        # PAY_R streams it, then the next AR) so every burst pays the full coherent-DMA
        # read latency (~140 cyc) unhidden. With HW-TSO's csum pre-pass reading each
        # segment twice, 16-beat bursts left the reader ~45% idle waiting on reads and
        # capped TX at 186 (silicon-profiled: tx_dma 52% stall + 45% idle, datapath NOT
        # the limit). 64-beat bursts (512 B, well under the 4 KB split) amortize the
        # latency ~3x/burst. Still capped by to_4k/to_wrap in the blen chain, so any
        # frame/ring geometry stays correct.
        self.bus    = bus               # axi.AXIInterface(data_width=64), byte-addressed
        self.source = source = stream.Endpoint([("data", 64), ("keep", 8)])

        self.base   = CSRStorage(64, description="Ring base address (bytes, 8-aligned).")
        self.mask   = CSRStorage(32, description="Ring size-1 (size = power of two).")
        self.wr_ptr = CSRStorage(32, description="SW write pointer (frames queued up to here).")
        self.rd_ptr = CSRStatus(32,  description="HW read pointer (consumed up to here).")
        self.enable = CSRStorage(1,  description="Ring enable.")
        self.sent   = CSRStatus(32,  description="Frames streamed to the datapath.")
        # ---- TX BD (descriptor) mode  -  P5 zero-copy TX (2026-07-06) -------------------
        # xmit stage timers measured skb_copy_and_csum_dev at ~166 us/frame: the CPU's
        # SERIAL cold-DRAM reads (no MLP) are the cost, while this engine's 16-beat bursts
        # hide the same latency. So in BD mode software writes 16-byte descriptors instead
        # of copying payload: the engine reads each segment STRAIGHT from skb memory.
        #   BD w0 (LE): addr[31:0] | len[15:0]<<32 | flags[15:0]<<48; flags bit0 = EOF.
        #   w1: reserved (v2: csum_start/csum_off for HW checksum insert).
        # CSR reuse (same trick as RX BD): mask = BD-ring bytes-1, wr_ptr = SW BD tail
        # (doorbell), rd_ptr = HW consumed-BD offset. DRIVER CONTRACT: every segment addr
        # is 8-aligned; non-EOF segments have len%8 == 0 (no inter-segment byte shifter);
        # the EOF segment's exact len drives the last-beat keep. bd_base==0 = ring mode.
        self.bd_base = CSRStorage(64, description="TX BD ring base (16 B/entry, coherent). 0 = byte-ring mode.")

        # # #

        rd    = Signal(32)              # HW consumption pointer (internal; may rewind)
        rd_pub = Signal(32)             # PUBLISHED rd (== rd_ptr CSR): frame ends only
        nsent = Signal(32)
        bd_mode  = Signal()
        seg_addr = Signal(32)           # current segment base (BD mode; MAY be unaligned)
        seg_eof  = Signal()             # this segment ends the frame
        # v2 byte-offset realignment (2026-07-06): Ethernet's 14-byte header makes
        # skb->data =2 mod 8 essentially always, so true zero-copy TX must read from
        # UNALIGNED addresses. The engine reads aligned beats from addr&~7 and realigns
        # through a one-beat carry: out = carry>>8o | in<<(64-8o); ceil((o+len)/8) input
        # beats produce ceil(len/8) outputs (+ at most one DRAIN beat from the carry).
        seg_off  = Signal(3)            # byte offset within the first beat
        sh_lo    = Signal(6)            # 8*seg_off, registered at BD parse
        carry    = Signal(64)
        carry_v  = Signal()
        obeat    = Signal(12)           # OUTPUT beats emitted (drives last/keep)
        self.comb += [
            self.rd_ptr.status.eq(rd_pub),   # pre-pass rd excursions stay hidden
            self.sent.status.eq(nsent),
            bd_mode.eq(self.bd_base.storage != 0),
        ]
        # SHAPE constant for the byte-ring fold (see RingDMAWriter): every ring
        # arm below dies at synthesis when the fallback is elaborated out.
        bd_shape = bd_mode if legacy_ring else C(1)
        # v2b HW checksum-insert (2026-07-07): BD w1 = {en[63], csum_off[31:16],
        # csum_start[15:0]} (frame-relative bytes). The engine burst-reads the region
        # [start, seg_len) FIRST, accumulates the 16-bit ones-complement sum (the stack
        # pre-seeds the csum field with the pseudo-header sum, exactly as for software
        # checksum_help), folds, then streams the frame with the folded sum muxed into
        # the csum_off beat. Offsets are even so both bytes sit in one beat.
        cs_en    = Signal()
        cs_start = Signal(16)
        cs_off   = Signal(16)
        cs_acc   = Signal(32)
        cs_init  = Signal(32)           # registered TSO P seed for the current segment
        cs_seed  = Signal(32)           # comb: what cs_clr loads (default 0; TSO drives cs_init)
        cs_val   = Signal(16)           # folded, ready to patch
        cs_lanes = Signal(18)
        cs_fold1 = Signal(17)
        cs_pass  = Signal()             # 1 = silent checksum pre-pass through PAY/DRAIN
        # cs-across-BDs (2026-07-06): the pre-pass walks the WHOLE BD chain (the
        # accumulator survives seg_finish), then rewinds the BD ring to the chain's
        # first BD and re-walks it for real. cs fields latch ONLY from the first BD's
        # w1; rd_pub shields the driver from the pre-pass rd excursion (reap would
        # otherwise free skbs the real pass still reads).
        rd_c     = Signal(32)           # BD-ring offset of the chain's first BD
        cs_done  = Signal()             # pre-pass finished: real pass in flight
        chain_first = Signal()          # next parsed BD is the chain's first
        # pipelined accumulate (2026-07-07): the keep-decode+mask+lane-add+32b-accumulate
        # cone was the design's critical path (21 levels; -0.065 with the 2nd hart).
        # Stage 1 registers the beat's lane sum; stage 2 adds it. Sum identical; the
        # trailing add completes during PREP, one cycle before any consumer.
        cs_take  = Signal()             # comb strobe: pre-pass beat accepted this cycle
        cs_clr   = Signal()             # comb strobe: new BD parsed  -  reset accumulator
        cs_lanes_r = Signal(18)
        cs_lv    = Signal()
        cs_sel_lo = Signal(8)           # one-hot byte select for csum low byte (REGISTERED
        cs_sel_hi = Signal(8)           # at parse  -  keeps comparators out of the data cone)
        # checksum datapath: byte-mask the candidate output beat by its keep, sum as
        # 16-bit LE lanes (same convention as the RX offload the kernel already accepts)
        cs_beat  = Signal(64)           # the would-be output beat during the pre-pass
        cs_keep  = Signal(8)
        cs_masked = Signal(64)
        # stage-0 registers (2026-07-29): the keep-decode reached the lane
        # adder COMBINATIONALLY - blen_r -> last-beat keep -> 64-bit mask ->
        # adder tree -> cs_lanes_r was the worst path on BOTH boards' m0019h
        # builds (arty -0.099 over exactly the cs_lanes_r[13..17] fan after
        # two recovery passes; AX -1.079 systemic). Registering {beat, keep,
        # take} first cuts blen_r out of the arithmetic cone; the sum is
        # IDENTICAL one cycle later. Ordering is safe by construction:
        # cs_clr fires at CHAIN start only, and a chain begins with a BD
        # fetch (a DRAM read, tens of cycles after the previous chain's last
        # take), so the deeper pipe always drains first - and cs_clr kills
        # the in-flight stages anyway, which can only hold already-consumed
        # data from the previous chain.
        cs_beat_q = Signal(64)
        cs_keep_q = Signal(8)
        cs_tk_q   = Signal()
        self.comb += [
            cs_masked.eq(Cat(*[Mux(cs_keep_q[i], cs_beat_q[8*i:8*i+8], 0) for i in range(8)])),
            cs_lanes.eq(cs_masked[0:16] + cs_masked[16:32] +
                        cs_masked[32:48] + cs_masked[48:64]),
            cs_fold1.eq(cs_acc[:16] + cs_acc[16:]),
            cs_val.eq(~(cs_fold1[:16] + cs_fold1[16])),
        ]
        self.sync += [
            cs_beat_q.eq(cs_beat),
            cs_keep_q.eq(cs_keep),
            cs_tk_q.eq(cs_take),
            If(cs_tk_q,
                cs_lanes_r.eq(cs_lanes),
                cs_lv.eq(1),
            ).Else(
                cs_lv.eq(0),
            ),
            If(cs_lv, cs_acc.eq(cs_acc + cs_lanes_r)),
            # TSO seeds the accumulator with the driver's pseudo-header sum P so the
            # folded result IS the TCP checksum; non-TSO paths seed 0 (cs_seed is a
            # comb default-0, driven only by the TSO pre-pass entry).
            If(cs_clr, cs_acc.eq(cs_seed), cs_lv.eq(0), cs_tk_q.eq(0)),
        ]
        # patch mux for the real pass: replace the 2 checksum bytes in their beat
        patch_hit = Signal()
        # realigned data path (pure comb from carry + live r.data)
        shifted = Signal(64)
        self.comb += shifted.eq((carry >> sh_lo) |
                                Mux(sh_lo == 0, 0, self.bus.r.data << (64 - sh_lo)))

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
        blen_m1 = Signal(12)            # blen_r - 1, registered BESIDE it: the runtime
                                        # 12-bit decrement used to sit inside the
                                        # per-beat in_last cone (5 of 15 logic levels,
                                        # 4.65 ns of an 11.95 ns path - m001d analysis)
        rem_z   = Signal()              # rem_r == 0 as of this burst's AR-accept
        burst_last = Signal()           # bcnt == blen_m1: the only per-beat term
        addr_r = Signal(32)             # burst address, registered in PREP
        bcnt   = Signal(12)             # R beats received in the current burst
        cur_addr = Signal(32)
        to_wrap  = Signal(30)
        to_4k    = Signal(10)
        blen_a   = Signal(12)
        blen_b   = Signal(12)
        blen     = Signal(12)
        self.comb += [
            # BD mode: segment reads are LINEAR from skb memory (no ring wrap  -  cap the
            # wrap term above any segment). Ring mode: base+offset with wrap splits.
            cur_addr.eq(Mux(bd_shape, Cat(C(0, 3), seg_addr[3:]) + off_r,
                                      self.base.storage[:32] + off_r)),
            to_wrap.eq(Mux(bd_shape, 1024,
                                     (self.mask.storage + 1 - off_r) >> 3)),
            to_4k.eq((4096 - (cur_addr & 0xFFF)) >> 3),
            blen_a.eq(Mux(rem_r > burst_beats, burst_beats, rem_r)),
            blen_b.eq(Mux(blen_a > to_wrap, to_wrap, blen_a)),
            blen.eq(Mux(blen_b > to_4k, to_4k, blen_b)),
        ]

        hdr_addr = Signal(32)
        self.comb += hdr_addr.eq(Mux(bd_shape, self.bd_base.storage[:32] + rd,
                                               self.base.storage[:32] + rd))

        self.comb += [
            self.bus.ar.size.eq(3),     # 8 bytes/beat
            self.bus.ar.burst.eq(1),    # INCR
        ]

        fb_new = Signal(11)             # ceil(len/8) of the header being parsed
        self.comb += fb_new.eq((self.bus.r.data[:16] + 7)[3:])

        # ---- cross-BD continuity assembly (TX>=200 step 1) ----
        # A holds 0-14 pending OUTPUT bytes across the BD chain of one frame; each R
        # beat inserts its valid bytes at A[aocc]; a full 8 emits. No %8 contract.
        A_reg   = Signal(120)
        aocc    = Signal(4)
        first_in = Signal()
        f_first = Signal(4)
        f_tail  = Signal(4)
        v_in    = Signal(4)
        in_last = Signal()
        raw_al  = Signal(64)
        raw_msk = Signal(64)
        m_first = Signal(8)             # byte-valid masks, REGISTERED at BD parse
        m_tail  = Signal(8)             # (the 65-bit variable-shift mask was -4.4 WNS)
        msk8    = Signal(8)
        ins_sh  = Signal(120)
        a_nxt   = Signal(120)
        occ_nxt = Signal(5)
        emit_now = Signal()
        eof_done = Signal()
        self.comb += [
            burst_last.eq(bcnt == blen_m1),
            in_last.eq(rem_z & burst_last),
            v_in.eq(Mux(first_in, f_first, Mux(in_last, f_tail, 8))),
            raw_al.eq(Mux(first_in, self.bus.r.data >> sh_lo, self.bus.r.data)),
            # CRITICAL: mask to the v_in VALID bytes  -  unmasked tail garbage ORs into
            # A_reg, survives frames, and corrupts every later frame's first bytes
            # (silicon-only: sim memory beyond segments reads 0; real DRAM does not).
            # Masks are REGISTERED per segment; per-beat cone = one byte-select level.
            msk8.eq(Mux(first_in, m_first, Mux(in_last, m_tail, 0xFF))),
            raw_msk.eq(Cat(*[Mux(msk8[i], raw_al[8*i:8*i+8], 0) for i in range(8)])),
            ins_sh.eq(raw_msk << Cat(C(0, 3), aocc[:3])),
            a_nxt.eq(A_reg | ins_sh),
            occ_nxt.eq(aocc + v_in),
            emit_now.eq(occ_nxt >= 8),
            eof_done.eq(in_last & seg_eof),
        ]
        bd_beat2 = Signal()             # BD reads are 2 beats: w0 parsed, w1 skipped

        # ---- HW header-generation TSO (TX>=200 step 3, 2026-07-07) -------------
        # ONE descriptor pair + the frag payload BDs describe a whole gso super-skb;
        # the ENGINE loops the segments: per segment it synthesizes a template window
        # (re-read from the arena) + payload windows sliced from the frag BDs, streams
        # them through the UNCHANGED continuity/csum machinery, and patches the per-
        # segment header fields at CONSTANT frame offsets (driver guards eth+ihl5:
        # tot_len@16 ipck@24 [last seg only, driver-precomputed], seq@38 flags@47
        # [k>0], tcp.check@50 via the existing cs machinery with cs_acc SEEDED to a
        # driver-provided pseudo-header sum P  -  the pre-pass sums the PATCHED beats,
        # so seq/flag drift self-accounts). IP id stays fixed (DF set  -  RFC-legal).
        # Descriptor ABI (2 ring entries, TSO flag = w0 bit 49):
        #   e0.w0 = tmpl_addr | hlen<<32 | TSO49    e0.w1 = mss | pay<<16 |
        #           fmid<<32 | flast<<40
        #   e1.w0 = P_full | P_last<<32             e1.w1 = tot_len_last |
        #           ipck_last<<16 | seq0<<32
        tso_on      = Signal()          # segment loop active
        tso_pend    = Signal()          # descriptor e0.w1 parse pending
        tso_tmpl    = Signal(32)        # template address (arena, any alignment)
        tso_hlen    = Signal(8)         # header bytes (54..94)
        tso_mss     = Signal(14)
        tso_payrem  = Signal(17)        # payload bytes not yet COMMITTED
        tso_fmid    = Signal(8)         # flags byte, mid segments (driver-precomputed)
        tso_flast   = Signal(8)         # flags byte, last segment
        tso_pfull   = Signal(32)        # cs_acc seed, full-mss segments
        tso_plast   = Signal(32)        # cs_acc seed, last segment
        tso_lenlast = Signal(16)        # ip.tot_len, last segment (logical u16)
        tso_cklast  = Signal(16)        # ip.check,  last segment (logical u16)
        tso_seq     = Signal(32)        # THIS segment's tcp.seq (logical u32)
        tso_k0      = Signal()          # first segment (template streams unpatched)
        tso_last    = Signal()          # last segment
        tso_chunk   = Signal(14)        # this segment's payload bytes
        tso_wleft   = Signal(14)        # window walk: chunk bytes not yet windowed
        pbd_v       = Signal()          # a payload BD is loaded
        pbd_addr    = Signal(32)
        pbd_len     = Signal(16)
        pbd_cons    = Signal(16)        # bytes of the loaded BD consumed
        anc_rd      = Signal(32)        # segment-start rewind anchors (pre-pass
        anc_cons    = Signal(16)        #  re-walks the same windows, then rewinds)
        tbd_beat    = Signal()          # payload-BD read beat toggle
        twin_addr   = Signal(32)
        t_avail     = Signal(16)
        twin_take   = Signal(16)
        twin_eof    = Signal()
        self.comb += [
            twin_addr.eq(pbd_addr + pbd_cons),
            t_avail.eq(pbd_len - pbd_cons),
            twin_take.eq(Mux(t_avail < tso_wleft, t_avail, tso_wleft)),
            twin_eof.eq(twin_take == tso_wleft),
        ]
        # per-segment field patches on the assembled OUTPUT beats  -  all offsets are
        # constants (rbeat==N compares only), one 2-3 deep byte mux on top of a_nxt;
        # the check field itself is the existing cs patch (cs_off=50) downstream.
        t_nxt  = Signal(64)
        tp_b2  = Signal()
        tp_b3  = Signal()
        tp_b4  = Signal()
        tp_b5  = Signal()
        self.comb += [
            tp_b2.eq(tso_on & tso_last & (rbeat == 2)),
            tp_b3.eq(tso_on & tso_last & (rbeat == 3)),
            tp_b4.eq(tso_on & ~tso_k0 & (rbeat == 4)),
            tp_b5.eq(tso_on & ~tso_k0 & (rbeat == 5)),
            t_nxt.eq(Cat(
                Mux(tp_b2, tso_lenlast[8:16],
                    Mux(tp_b3, tso_cklast[8:16],
                        Mux(tp_b5, tso_seq[8:16], a_nxt[0:8]))),
                Mux(tp_b2, tso_lenlast[0:8],
                    Mux(tp_b3, tso_cklast[0:8],
                        Mux(tp_b5, tso_seq[0:8], a_nxt[8:16]))),
                a_nxt[16:24], a_nxt[24:32], a_nxt[32:40], a_nxt[40:48],
                Mux(tp_b4, tso_seq[24:32], a_nxt[48:56]),
                Mux(tp_b4, tso_seq[16:24],
                    Mux(tp_b5, Mux(tso_last, tso_flast, tso_fmid),
                        a_nxt[56:64])))),
        ]

        def window_setup(addr, ln, eof):
            """program the streaming machinery for one (addr,len,eof) window  - 
            the register set the BD parse fills, fed from TSO registers instead"""
            a3 = addr[:3]
            return [
                NextValue(frame_bytes, ln),
                NextValue(rem_r, (ln + a3 + 7)[3:]),
                NextValue(rem_z, (ln + a3 + 7)[3:] == 0),
                NextValue(seg_addr, addr),
                NextValue(seg_off, a3),
                NextValue(sh_lo, Cat(C(0, 3), a3)),
                NextValue(carry_v, 0),
                NextValue(obeat, 0),
                NextValue(first_in, 1),
                NextValue(f_first, Mux(ln < (8 - a3), ln[:4], 8 - a3)),
                NextValue(f_tail, ((a3 + ln - 1) & 0x7) + 1),
                NextValue(m_first,
                          ((C(1, 9) << Mux(ln < (8 - a3), ln[:4], 8 - a3)) - 1)[:8]),
                NextValue(m_tail, ((C(1, 9) << (((a3 + ln - 1) & 0x7) + 1)) - 1)[:8]),
                NextValue(seg_eof, eof),
                NextValue(off_r, 0),
            ]

        def tso_rewind():
            """end of a segment's silent pre-pass: rewind the payload cursor and
            re-walk the same windows for real (mirrors cs_restart for chains)"""
            return [
                NextValue(cs_pass, 0),
                NextValue(rd, anc_rd),
                NextValue(pbd_v, 0),        # pbd regs may hold a LATER BD: re-fetch
                NextValue(pbd_cons, anc_cons),
                NextState("TSO_TGO"),
            ]

        self.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            If(~self.enable.storage,
                NextValue(rd, 0),       # reload hygiene (mirror of the RX post-FIFO drain)
                NextValue(rd_pub, 0),
                NextValue(tso_on, 0),
                NextValue(tso_pend, 0),
            ).Elif(self.wr_ptr.storage != rd,
                NextValue(rbeat, 0),
                NextValue(bd_beat2, 0),
                NextValue(rd_c, rd),    # chain anchor for the csum-restart rewind
                NextValue(cs_done, 0),
                NextValue(chain_first, 1),
                NextState("HDR_AR"),
            )
        )
        fsm.act("HDR_AR",
            self.bus.ar.valid.eq(1),
            self.bus.ar.addr.eq(hdr_addr),
            self.bus.ar.len.eq(Mux(bd_shape, 1, 0)),  # BD = 2 beats, ring header = 1
            If(self.bus.ar.ready,
                NextState("HDR_R"),
            )
        )
        fsm.act("HDR_R",
            self.bus.r.ready.eq(1),
            If(self.bus.r.valid,
                If(bd_shape & bd_beat2,
                    If(tso_pend,
                        # TSO descriptor e0.w1: {flast[47:40], fmid[39:32],
                        # pay_total[31:16], mss[13:0]}
                        NextValue(tso_pend, 0),
                        NextValue(tso_mss, self.bus.r.data[:14]),
                        NextValue(tso_payrem, self.bus.r.data[16:32]),
                        NextValue(tso_fmid, self.bus.r.data[32:40]),
                        NextValue(tso_flast, self.bus.r.data[40:48]),
                        NextValue(rd, (rd + 16) & self.mask.storage),
                        If((self.bus.r.data[:14] == 0) |
                           (self.bus.r.data[16:32] == 0),
                            NextValue(rd, self.wr_ptr.storage & self.mask.storage),
                            NextValue(rd_pub, self.wr_ptr.storage & self.mask.storage),
                            NextState("IDLE"),
                        ).Else(
                            NextState("TSO_EXT_AR"),
                        )
                    ).Else(
                        # second BD word: {en[63], csum_off[31:16], csum_start[15:0]}.
                        # cs state latches ONLY from the chain's FIRST BD, and only on
                        # the pre-pass entry (~cs_done)  -  mid-chain w1s are ignored and
                        # the post-rewind re-parse must not restart the pre-pass.
                        If(chain_first & ~cs_done,
                            NextValue(cs_en,    self.bus.r.data[63]),
                            NextValue(cs_start, self.bus.r.data[:16]),
                            NextValue(cs_off,   self.bus.r.data[16:32]),
                            NextValue(cs_sel_lo, Mux(self.bus.r.data[63],
                                                     1 << self.bus.r.data[16:19], 0)),
                            NextValue(cs_sel_hi, Mux(self.bus.r.data[63],
                                                     2 << self.bus.r.data[16:19], 0)),
                            cs_clr.eq(1),
                            NextValue(cs_pass, self.bus.r.data[63]),
                        ),
                        NextValue(chain_first, 0),
                        NextState("PREP"),
                    )
                ).Elif(bd_shape & self.bus.r.data[49],
                    # TSO descriptor e0.w0: {TSO=1<<49, hlen[39:32], tmpl_addr[31:0]}
                    NextValue(tso_tmpl, self.bus.r.data[:32]),
                    NextValue(tso_hlen, self.bus.r.data[32:40]),
                    NextValue(tso_pend, 1),
                    NextValue(bd_beat2, 1),
                    If((self.bus.r.data[32:40] < 54) | (self.bus.r.data[32:40] > 94),
                        # malformed template: resync like any bad BD
                        NextValue(tso_pend, 0),
                        NextValue(rd, self.wr_ptr.storage & self.mask.storage),
                        NextValue(rd_pub, self.wr_ptr.storage & self.mask.storage),
                        NextState("BD_FLUSH"),
                    )
                ).Else(
                    NextValue(frame_bytes, Mux(bd_shape, self.bus.r.data[32:48],
                                                         self.bus.r.data[:16])),
                    # input beats = ceil((off + len)/8); output beats = ceil(len/8)
                    NextValue(rem_r, Mux(bd_shape,
                        (self.bus.r.data[32:48] + self.bus.r.data[:3] + 7)[3:], fb_new)),
                    NextValue(rem_z, Mux(bd_shape,
                        (self.bus.r.data[32:48] + self.bus.r.data[:3] + 7)[3:], fb_new) == 0),
                    NextValue(seg_addr, self.bus.r.data[:32]),
                    NextValue(seg_off, self.bus.r.data[:3]),
                    NextValue(sh_lo, Cat(C(0, 3), self.bus.r.data[:3])),
                    NextValue(carry_v, 0),
                    NextValue(obeat, 0),
                    # continuity (TX>=200 step 1): per-segment byte-valid counts for the
                    # assembly shifter; f_first covers tiny one-beat segments too
                    NextValue(first_in, 1),
                    NextValue(f_first, Mux(
                        self.bus.r.data[32:48] < (8 - self.bus.r.data[:3]),
                        self.bus.r.data[32:36],
                        8 - self.bus.r.data[:3])),
                    NextValue(f_tail, ((self.bus.r.data[:3] +
                                        self.bus.r.data[32:48] - 1) & 0x7) + 1),
                    NextValue(m_first, ((C(1, 9) << Mux(
                        self.bus.r.data[32:48] < (8 - self.bus.r.data[:3]),
                        self.bus.r.data[32:36],
                        8 - self.bus.r.data[:3])) - 1)[:8]),
                    NextValue(m_tail, ((C(1, 9) << (((self.bus.r.data[:3] +
                        self.bus.r.data[32:48] - 1) & 0x7) + 1)) - 1)[:8]),
                    NextValue(seg_eof, self.bus.r.data[48]),
                    NextValue(off_r, Mux(bd_shape, 0, (rd + 8) & self.mask.storage)),
                    NextValue(bd_beat2, 1),
                    # len==0 / oversized can only be a software bug: resync, don't stream garbage
                    If(bd_shape,
                        If((self.bus.r.data[32:48] == 0) |
                           (self.bus.r.data[32:48] > max_frame_bytes),
                            NextValue(rd, self.wr_ptr.storage & self.mask.storage),
                            NextValue(rd_pub, self.wr_ptr.storage & self.mask.storage),
                            NextValue(bd_beat2, 1),      # still drain the 2nd beat
                            NextState("BD_FLUSH"),
                        )
                    ).Elif((self.bus.r.data[:16] == 0) | (self.bus.r.data[:16] > max_frame_bytes),
                        NextValue(rd, self.wr_ptr.storage & self.mask.storage),
                        NextValue(rd_pub, self.wr_ptr.storage & self.mask.storage),
                        NextState("IDLE"),
                    ).Else(
                        NextState("PREP"),
                    )
                )
            )
        )
        fsm.act("BD_FLUSH",             # bad BD: eat the second beat, then resync'd IDLE
            self.bus.r.ready.eq(1),
            If(self.bus.r.valid, NextState("IDLE")),
        )
        fsm.act("PREP",                 # register this burst's geometry
            NextValue(blen_r, blen),
            NextValue(blen_m1, blen - 1),
            NextValue(addr_r, cur_addr),
            NextState("PAY_AR"),
        )
        fsm.act("PAY_AR",
            self.bus.ar.valid.eq(1),
            self.bus.ar.addr.eq(addr_r),
            self.bus.ar.len.eq(blen_m1),
            If(self.bus.ar.ready,
                NextValue(bcnt, 0),
                # BD mode: LINEAR segment offset  -  masking with the (BD-ring!) mask would
                # wrap the read at ring-size bytes (the same class of bug the RX BD mode
                # shipped with; its 1520 B content test is the template for test_tx_bd).
                NextValue(off_r, Mux(bd_shape, off_r + (blen_r << 3),
                                     (off_r + (blen_r << 3)) & self.mask.storage)),
                NextValue(rem_r, rem_r - blen_r),
                NextValue(rem_z, rem_r == blen_r),
                NextState("PAY_R"),
            )
        )
        # segment-finish micro-sequence, shared by aligned / realigned / drain exits
        def seg_finish():
            return [
                If(bd_shape,
                    NextValue(rd, (rd + 16) & self.mask.storage),  # consume the BD
                    # rbeat is FRAME-relative across the chain (patch_here indexes
                    # the assembled output); IDLE re-zeroes it per frame.
                    NextValue(bd_beat2, 0),
                    If(seg_eof,
                        NextValue(nsent, nsent + 1),
                        # publish rd only at committed frame ends  -  the csum
                        # pre-pass advances rd through the chain and REWINDS;
                        # exposing that excursion would let the driver reap
                        # skbs the real pass still reads.
                        NextValue(rd_pub, (rd + 16) & self.mask.storage),
                        NextState("IDLE"),
                    ).Else(
                        NextState("HDR_AR"),            # next segment of the same frame
                    )
                ).Else(
                    NextValue(rd, (rd + 8 + (frame_beats << 3)) & self.mask.storage),
                    NextValue(rd_pub, (rd + 8 + (frame_beats << 3)) & self.mask.storage),
                    NextValue(nsent, nsent + 1),
                    NextState("IDLE"),
                )
            ]

        def cs_patched(base):
            """base beat with the folded checksum muxed in  -  REGISTERED one-hot selects
            (cs_sel_lo/hi), so the cone is one 2-level per-byte mux, no comparators
            (the +0.039 flake fix: this mux sits in the datapath even with csum off)."""
            byts = []
            for i in range(8):
                byts.append(Mux(cs_sel_lo[i], cs_val[:8],
                            Mux(cs_sel_hi[i], cs_val[8:16],
                                base[8*i:8*i+8])))
            return Cat(*byts)

        def cs_restart():
            """end of the silent pre-pass: fold is combinational; rerun for real.
            cs-across-BDs: rewind the BD ring to the chain's first BD and re-walk
            the whole chain through HDR_AR (per-BD geometry reloads on re-parse;
            cs_done blocks a second pre-pass). Ring mode rewinds trivially (rd
            never moved). The accumulator's trailing pipeline add completes during
            HDR_AR/HDR_R, well before the first patched beat."""
            return [
                NextValue(cs_pass, 0),
                NextValue(cs_done, 1),
                NextValue(chain_first, 1),
                NextValue(rd, rd_c),
                NextValue(rbeat, 0),
                NextValue(bd_beat2, 0),
                NextValue(carry_v, 0),
                NextValue(A_reg, 0),
                NextValue(aocc, 0),
                NextValue(first_in, 1),
                NextState("HDR_AR"),
            ]

        pay_last = Signal()             # this output beat is the segment's final one
        patch_here = Signal()           # csum bytes live in THIS output beat
        self.comb += [
            pay_last.eq(rbeat == frame_beats - 1),
            patch_here.eq(cs_en & ~cs_pass & (rbeat == cs_off[3:])),
        ]

        fsm.act("PAY_R",
            If(~bd_shape,
                # aligned path: input beats == output beats (bit-identical to pre-v2)
                # (byte-ring only  -  dead-folds out of legacy_ring=False builds)
                source.valid.eq(self.bus.r.valid & ~cs_pass),
                source.data.eq(Mux(patch_here, cs_patched(self.bus.r.data),
                                   self.bus.r.data)),
                source.last.eq(pay_last & (~bd_shape | seg_eof)),
                source.keep.eq(Mux(pay_last, rlast_keep, 0xFF)),
                self.bus.r.ready.eq(source.ready | cs_pass),
                cs_beat.eq(self.bus.r.data),
                cs_keep.eq(Mux(pay_last, rlast_keep, 0xFF)),
                If(self.bus.r.valid & self.bus.r.ready,
                    cs_take.eq(cs_pass),
                    NextValue(rbeat, rbeat + 1),
                    NextValue(bcnt, bcnt + 1),
                    If(rbeat == frame_beats - 1,
                        If(cs_pass, *cs_restart()).Else(*seg_finish())
                    ).Elif(burst_last,
                        NextState("PREP"),
                    )
                )
            ).Else(
                # assembly path: insert v_in bytes at A[aocc]; emit on >=8. Continuity:
                # A/aocc persist across non-EOF segments (no drain mid-frame).
                source.valid.eq(self.bus.r.valid & emit_now & ~cs_pass),
                source.data.eq(Mux(patch_here, cs_patched(t_nxt), t_nxt)),
                source.last.eq(eof_done & (occ_nxt == 8)),
                source.keep.eq(0xFF),
                self.bus.r.ready.eq(~emit_now | source.ready | cs_pass),
                # cs taps the FIELD-PATCHED stream: the pre-pass then sums exactly
                # what the real pass emits, so per-segment seq/flag drift lands in
                # the checksum automatically (the check field itself streams as the
                # template's zeros during accumulation).
                cs_beat.eq(t_nxt),
                cs_keep.eq(0xFF),
                If(self.bus.r.valid & self.bus.r.ready,
                    cs_take.eq(cs_pass & emit_now),
                    NextValue(first_in, 0),
                    NextValue(bcnt, bcnt + 1),
                    If(emit_now,
                        NextValue(A_reg, a_nxt[64:]),
                        NextValue(aocc, occ_nxt - 8),
                        NextValue(rbeat, rbeat + 1),
                    ).Else(
                        NextValue(A_reg, a_nxt),
                        NextValue(aocc, occ_nxt),
                    ),
                    If(eof_done,
                        If(occ_nxt == 8,                # frame ends beat-aligned
                            NextValue(A_reg, 0),
                            NextValue(aocc, 0),
                            If(cs_pass,
                                If(tso_on,
                                    *tso_rewind()
                                ).Else(
                                    *cs_restart()
                                )
                            ).Elif(tso_on,              # segment committed
                                NextState("TSO_COMMIT"),
                            ).Else(
                                *seg_finish()
                            )
                        ).Else(
                            NextState("DRAIN"),         # residual bytes flush
                        )
                    ).Elif(in_last,                     # non-EOF: A/aocc carry over
                        If(tso_on,
                            NextState("TSO_WIN"),       # next synthesized window
                        ).Else(
                            *seg_finish()
                        )
                    ).Elif(burst_last,
                        NextState("PREP"),
                    )
                )
            )
        )
        drain_keep = Signal(8)
        self.comb += drain_keep.eq((1 << aocc[:3]) - 1)
        fsm.act("DRAIN",                                # assembly residual flush (EOF)
            source.valid.eq(~cs_pass),
            source.data.eq(Mux(patch_here, cs_patched(A_reg[:64]), A_reg[:64])),
            source.last.eq(1),
            source.keep.eq(drain_keep),
            cs_beat.eq(A_reg[:64]),
            cs_keep.eq(drain_keep),
            If(cs_pass,
                cs_take.eq(1),
                NextValue(A_reg, 0),
                NextValue(aocc, 0),
                If(tso_on,
                    *tso_rewind()
                ).Else(
                    *cs_restart()
                )
            ).Elif(source.ready,
                NextValue(A_reg, 0),
                NextValue(aocc, 0),
                If(tso_on,
                    NextState("TSO_COMMIT"),
                ).Else(
                    *seg_finish()
                )
            )
        )

        # ---- HW-TSO sequencer -------------------------------------------------
        fsm.act("TSO_EXT_AR",           # fetch descriptor entry 2
            self.bus.ar.valid.eq(1),
            self.bus.ar.addr.eq(self.bd_base.storage[:32] + rd),
            self.bus.ar.len.eq(1),
            If(self.bus.ar.ready,
                NextValue(tbd_beat, 0),
                NextState("TSO_EXT_R"),
            )
        )
        fsm.act("TSO_EXT_R",
            self.bus.r.ready.eq(1),
            If(self.bus.r.valid,
                If(~tbd_beat,
                    # e1.w0 = {P_last[63:32], P_full[31:0]}
                    NextValue(tso_pfull, self.bus.r.data[:32]),
                    NextValue(tso_plast, self.bus.r.data[32:64]),
                    NextValue(tbd_beat, 1),
                ).Else(
                    # e1.w1 = {seq0[63:32], ipck_last[31:16], tot_len_last[15:0]}
                    NextValue(tso_lenlast, self.bus.r.data[:16]),
                    NextValue(tso_cklast, self.bus.r.data[16:32]),
                    NextValue(tso_seq, self.bus.r.data[32:64]),
                    NextValue(rd, (rd + 16) & self.mask.storage),
                    NextValue(tso_on, 1),
                    NextValue(tso_k0, 1),
                    NextValue(pbd_v, 0),
                    NextValue(pbd_cons, 0),
                    NextState("TSO_SEG"),
                )
            )
        )
        fsm.act("TSO_SEG",              # per-segment setup + rewind anchors
            NextValue(tso_chunk, Mux(tso_payrem > tso_mss, tso_mss,
                                     tso_payrem[:14])),
            NextValue(tso_last, tso_payrem <= tso_mss),
            NextValue(cs_init, Mux(tso_payrem <= tso_mss, tso_plast, tso_pfull)),
            NextValue(cs_en, 1),
            NextValue(cs_off, 50),      # tcp.check, frame-relative (ihl=5 contract)
            NextValue(cs_sel_lo, 1 << 2),
            NextValue(cs_sel_hi, 1 << 3),
            NextValue(cs_pass, 1),
            NextValue(anc_rd, rd),
            NextValue(anc_cons, pbd_cons),
            NextState("TSO_TGO"),
        )
        fsm.act("TSO_TGO",              # start a pass: template window first
            If(cs_pass, cs_clr.eq(1), cs_seed.eq(cs_init)),
            NextValue(tso_wleft, tso_chunk),
            NextValue(A_reg, 0),
            NextValue(aocc, 0),
            NextValue(rbeat, 0),
            *window_setup(tso_tmpl, tso_hlen, C(0, 1)),
            NextState("PREP"),
        )
        fsm.act("TSO_WIN",              # next payload window of this segment
            If(~pbd_v,
                NextState("TSO_BD_AR"),
            ).Else(
                NextValue(tso_wleft, tso_wleft - twin_take),
                NextValue(pbd_cons, pbd_cons + twin_take),
                If(pbd_cons + twin_take == pbd_len,   # BD exhausted: consume it
                    NextValue(rd, (rd + 16) & self.mask.storage),
                    NextValue(pbd_v, 0),
                    NextValue(pbd_cons, 0),
                ),
                *window_setup(twin_addr, twin_take, twin_eof),
                NextState("PREP"),
            )
        )
        fsm.act("TSO_BD_AR",            # fetch the next payload BD
            self.bus.ar.valid.eq(1),
            self.bus.ar.addr.eq(self.bd_base.storage[:32] + rd),
            self.bus.ar.len.eq(1),
            If(self.bus.ar.ready,
                NextValue(tbd_beat, 0),
                NextState("TSO_BD_R"),
            )
        )
        fsm.act("TSO_BD_R",
            self.bus.r.ready.eq(1),
            If(self.bus.r.valid,
                If(~tbd_beat,
                    NextValue(pbd_addr, self.bus.r.data[:32]),
                    NextValue(pbd_len, self.bus.r.data[32:48]),
                    NextValue(tbd_beat, 1),
                    If(self.bus.r.data[32:48] == 0,   # garbage BD: resync
                        NextValue(tso_on, 0),
                        NextValue(rd, self.wr_ptr.storage & self.mask.storage),
                        NextValue(rd_pub, self.wr_ptr.storage & self.mask.storage),
                        NextState("BD_FLUSH"),
                    )
                ).Else(                                # drain w1 (ignored)
                    NextValue(pbd_v, 1),
                    NextState("TSO_WIN"),
                )
            )
        )
        fsm.act("TSO_COMMIT",           # real pass of one segment finished
            NextValue(tso_payrem, tso_payrem - tso_chunk),
            NextValue(tso_seq, tso_seq + tso_chunk),
            NextValue(tso_k0, 0),
            NextValue(nsent, nsent + 1),
            If(tso_payrem == tso_chunk,               # that was the last segment
                # publish ONLY here: earlier segments still re-read the TEMPLATE
                # (descriptor entry 0's arena slot)  -  a mid-frame publish would
                # let the driver recycle it under the engine.
                NextValue(rd_pub, rd),
                NextValue(tso_on, 0),
                NextValue(cs_en, 0),
                NextState("IDLE"),
            ).Else(
                NextState("TSO_SEG"),
            )
        )

        # ---- Phase-0 observability taps (read-only comb; no functional effect) --------
        # Exposed for MilanDebug's reader probes (rd_latency_probe / rd_produce_probe) so
        # they can attribute, each sys cycle, WHY the reader is or isn't feeding `source`.
        # All sys-domain (the reader is a sys master) → the probes need no CDC.
        self.dbg_cs_pass = Signal()     # 1 = silent csum/TSO pre-pass (source suppressed)
        self.dbg_reading = Signal()     # in a state that awaits/consumes an R beat
        self.dbg_idle    = Signal()     # IDLE: no work queued (rd == wr)
        # M1 telemetry: TX ring/BD occupancy (bytes queued by SW, unconsumed by HW  - 
        # "is the CPU keeping the ring fed") + doorbell strobe (wr_ptr CSR writes,
        # for the frames-per-doorbell batching factor). Tracked/snapped in MilanDebug.
        self.dbg_occ      = Signal(32)
        self.dbg_doorbell = Signal()
        self.comb += [
            self.dbg_cs_pass.eq(cs_pass),
            self.dbg_reading.eq(fsm.ongoing("HDR_R") | fsm.ongoing("PAY_R") |
                                fsm.ongoing("TSO_EXT_R") | fsm.ongoing("TSO_BD_R") |
                                fsm.ongoing("BD_FLUSH")),
            self.dbg_idle.eq(fsm.ongoing("IDLE")),
            self.dbg_occ.eq((self.wr_ptr.storage - rd_pub) & self.mask.storage),
            self.dbg_doorbell.eq(self.wr_ptr.re),
        ]


class RxSteer(LiteXModule):
    """2-way RX steering front-end: gPTP gets its OWN queue, everything else shares q0.

    USER directive (2026-07-26, the 802.1Q-ordered egress round): "one [ingress queue]
    dedicated to gPTP, one for everything else".

      q1  frames whose DMAC is the 802.1AS reserved multicast 01-80-C2-00-00-0E
          AND whose (inner) EtherType is 0x88F7  -  i.e. exactly the gPTP test
          `hdl/ieee8021q/ts/traffic_class_map.sv` applies on egress with
          CLS_CTRL[1] set (REQ-CLS-07). One detector, one rule, both directions.
      q0  everything else.

    WHAT THIS REPLACES AND WHAT IT COSTS. Until this commit the block was a TCP
    4-tuple flow hash built for THROUGHPUT: it split one MTU-1500 RX stream into
    two flow-consistent queues so two TCP flows' ACK/recv processing ran on two
    harts, breaking the single-NAPI ACK-processing ceiling (measured RX 223
    Mbit, see docs/findings/RX_PERF_TUNING_MAP.md). That parallel ACK split is
    GONE - bulk RX is single-NAPI again and the RX ceiling reverts to the
    one-hart number. What is bought is latency where it actually matters: PTP
    event messages no longer queue behind bulk traffic in a shared ring, and
    RX-side PTP latency is precisely what once held `asCapable` false
    (docs/findings/GPTP_RXPAD_ROOTCAUSE.md - late RX stamps, not a switch
    fault). A sync/pdelay pair is ~64-90 B at
    8-16 frames/s, so the dedicated queue is essentially never backlogged and
    its NAPI never competes with a 1500 B bulk burst.

    Per frame: buffer the head (<=3 beats = wire bytes 0..23, enough for the
    DMAC, the EtherType and one C-TAG's inner EtherType), decide, then route the
    WHOLE frame to the chosen queue. Frames never reorder within a queue.

    Downstream (both RingDMAWriter.sink) is always-ready (drop-on-full), so a small
    SyncFIFO holds `sink` (constant-ready preserved) while the head is decoded; the
    FIFO peaks ~3 beats/frame (head re-fill during replay) and never backpressures."""
    def __init__(self, depth=64):
        self.sink    = sink    = stream.Endpoint([("data", 64), ("keep", 8)])
        self.source0 = source0 = stream.Endpoint([("data", 64), ("keep", 8)])
        self.source1 = source1 = stream.Endpoint([("data", 64), ("keep", 8)])
        self.q0_frames = CSRStatus(32, description="frames steered to RX queue 0 (everything but gPTP)")
        self.q1_frames = CSRStatus(32, description="frames steered to RX queue 1 (gPTP)")
        # NAME KEPT ON PURPOSE: `hash_sel` is the third and last register of the
        # steer block and the DMA window map is pinned to its size/offset
        # (endstation_builder DMA_STEER_BYTES = 0x0C). Renaming it would move
        # nothing but would break every csr.csv-derived tool. It is now simply
        # the bypass bit it always doubled as.
        self.hash_sel  = CSRStorage(1, reset=0, description="0 = steer gPTP to q1; 1 = force all to q0 (bypass)")

        # # #
        self.fifo = fifo = stream.SyncFIFO([("data", 64), ("keep", 8)], depth=depth, buffered=True)
        self.comb += sink.connect(fifo.sink)          # sink.ready = fifo.sink.ready (~always 1)
        src = fifo.source

        NHEAD = 3                                     # beats buffered: wire bytes 0..23
        obuf_d = Array([Signal(64) for _ in range(NHEAD)])
        obuf_k = Array([Signal(8)  for _ in range(NHEAD)])
        obuf_l = Array([Signal()   for _ in range(NHEAD)])
        ocnt   = Signal(4)                            # beats collected into obuf (0..3)
        sawlast = Signal()                            # frame ended within the head
        q      = Signal()                             # latched queue for the current frame
        ridx   = Signal(4)                            # replay index
        n0 = Signal(32); n1 = Signal(32)
        self.comb += [self.q0_frames.status.eq(n0), self.q1_frames.status.eq(n1)]

        def B(beat, byte):                            # byte `byte` (0..7) of head beat `beat`
            return obuf_d[beat][8*byte:8*byte+8]
        # 802.1AS-2020 s10.5: gPTP rides the reserved multicast 01-80-C2-00-00-0E.
        # EtherType 0x88F7 ALONE is not proof of a gPTP frame (any station can mint
        # one at an arbitrary destination) - the same argument REQ-CLS-07 makes on
        # the egress side, so demand both here too. A spoofed 0x88F7 lands on q0.
        dmac_gptp = Signal(); et_ptp = Signal(); et_vlan = Signal(); vet_ptp = Signal()
        self.comb += [
            dmac_gptp.eq((B(0,0) == 0x01) & (B(0,1) == 0x80) & (B(0,2) == 0xC2) &
                         (B(0,3) == 0x00) & (B(0,4) == 0x00) & (B(0,5) == 0x0E)),
            et_ptp.eq((B(1,4) == 0x88) & (B(1,5) == 0xF7)),   # bytes 12,13 = 0x88F7
            et_vlan.eq((B(1,4) == 0x81) & (B(1,5) == 0x00)),  # bytes 12,13 = C-TAG
            vet_ptp.eq((B(2,0) == 0x88) & (B(2,1) == 0xF7)),  # bytes 16,17 after a C-TAG
        ]
        gptp = Signal()
        self.comb += gptp.eq(dmac_gptp & (et_ptp | (et_vlan & vet_ptp)))
        # decision from the (registered) head  -  evaluated when HEAD is complete.
        # `sawlast` = the frame ended inside the head; a runt that short cannot be a
        # valid gPTP PDU (the smallest, pdelay_resp_follow_up, is 60 B on the wire),
        # so it takes q0 like every other non-gPTP frame.
        qsel = Signal()
        self.comb += If(sawlast | ~gptp | self.hash_sel.storage,
                        qsel.eq(0)).Else(qsel.eq(1))

        self.submodules.fsm = fsm = FSM(reset_state="HEAD")
        fsm.act("HEAD",
            src.ready.eq(1),
            If(src.valid,
                NextValue(obuf_d[ocnt], src.data),
                NextValue(obuf_k[ocnt], src.keep),
                NextValue(obuf_l[ocnt], src.last),
                NextValue(ocnt, ocnt + 1),
                If(src.last, NextValue(sawlast, 1)),
                If(src.last | (ocnt == NHEAD - 1),      # short frame, or the 5th beat stored
                    NextState("DECODE"),                # obuf fully registered next cycle
                )
            )
        )
        fsm.act("DECODE",                               # obuf[0..ocnt-1] all visible now
            NextValue(q, qsel),
            NextValue(ridx, 0),
            NextState("REPLAY"),
        )
        # emit the buffered head (REPLAY) or the streamed tail (PASS) to the chosen queue
        for s in (source0, source1):
            self.comb += [
                s.data.eq(Mux(fsm.ongoing("PASS"), src.data, obuf_d[ridx])),
                s.keep.eq(Mux(fsm.ongoing("PASS"), src.keep, obuf_k[ridx])),
                s.last.eq(Mux(fsm.ongoing("PASS"), src.last, obuf_l[ridx])),
            ]
        fsm.act("REPLAY",
            If(q == 0, source0.valid.eq(1)).Else(source1.valid.eq(1)),
            # both writer sinks are always-ready; advance every cycle
            NextValue(ridx, ridx + 1),
            If(obuf_l[ridx],                            # head contained the whole frame
                NextValue(ocnt, 0), NextValue(sawlast, 0),
                If(q == 0, NextValue(n0, n0 + 1)).Else(NextValue(n1, n1 + 1)),
                NextState("HEAD"),
            ).Elif(ridx == ocnt - 1,                    # head drained; stream the tail
                NextState("PASS"),
            )
        )
        fsm.act("PASS",
            src.ready.eq(1),
            If(q == 0, source0.valid.eq(src.valid)).Else(source1.valid.eq(src.valid)),
            If(src.valid & src.last,
                NextValue(ocnt, 0), NextValue(sawlast, 0),
                If(q == 0, NextValue(n0, n0 + 1)).Else(NextValue(n1, n1 + 1)),
                NextState("HEAD"),
            )
        )


class _PCMRingNxN(LiteXModule):
    """NxN per-stream PCM DRAM ring writer (NXN_ARCHITECTURE.md §1.3 P3 / P12).

    Generalizes the single `WishboneDMAWriter` PCM ring with the stream index:
    a beat tagged `user = s` (the datapath's `m_axis_pcm_tuser`) lands at
    `base + s*stride + offset[s]`, where `offset[s]` is that stream's private
    write pointer wrapping at `length` (one sub-ring of `length` bytes per
    stream, sub-rings `stride` bytes apart; the consumer chases the per-stream
    offsets exactly like the flat ring's `offset` CSR). Stream 0 lands at the
    base — programming `stride = 0, length = ring bytes` with only stream 0
    routed reproduces the flat ring layout bit-for-bit.

    CSRs: base[64], length[32] (per-stream sub-ring BYTES, multiple of the bus
    word), stride[32] (BYTES between stream bases), enable, sel[4] + offset[32]
    (the selected stream's write pointer readback), cap[32] (RO geometry
    capability at +0x1c, the hs_pgsz precedent - snd-kl-milan refuses L>1
    without it). Disable clears all offsets and drops beats (the flat writer's
    disabled behavior)."""
    def __init__(self, bus, n_streams):
        from litex.soc.cores.dma import WishboneDMAWriter
        from litex.soc.interconnect import stream as _stream
        self.writer = WishboneDMAWriter(bus, endianness="big", with_csr=False)
        self.sink   = _stream.Endpoint([("data", bus.data_width), ("user", 4)])
        self._base   = CSRStorage(64, description="PCM NxN ring base address.")
        self._length = CSRStorage(32, description="per-stream sub-ring length (bytes).")
        self._stride = CSRStorage(32, description="byte distance between stream sub-ring bases.")
        self._enable = CSRStorage(description="ring writer enable (0 drops beats + clears offsets).")
        self._sel    = CSRStorage(4,  description="stream index for the offset readback.")
        self._offset = CSRStatus(32,  description="selected stream's write pointer (bytes).")
        # Geometry capability word, declared right after _offset so it lands at
        # +0x1c (LiteX maps CSRs in declaration order; the engine block ends at
        # OFFSET +0x18). Every field is the elaboration TRUTH, never policy:
        # [23:16] stride/64KiB = 0 because THIS engine has no baked stride (the
        # runtime _stride CSRStorage above is driver-programmed); [15:8] T = 0
        # because this block serves capture rings only (KL_pcm_tx playback rings
        # live behind their own pb_* CSR block, not this geometry).
        assert 1 <= n_streams <= 0xFF
        self._cap = CSRStatus(32, description="geometry capability: [31:24]=0x4D 'M', "
                              "[23:16]=stride/64KiB (0 = driver-programmed via the stride CSR), "
                              "[15:8]=T playback rings behind this block (0), "
                              "[7:0]=L capture rings (elaborated N_STREAMS).")

        # # #

        import math
        nb    = bus.data_width // 8
        shift = int(math.log2(nb))
        offsets = Array(Signal(32) for _ in range(n_streams))
        # Absolute per-stream pointers (m001d net analysis, cone C): the beat
        # address used to be base + stride*user + offsets[user] computed in
        # the beat cone - a ~40-bit carry propagation (CARRY4=10, 15-18 logic
        # levels, eppo's WNS). base/stride are init-time CSRs, so the multiply
        # and both 64-bit adds are loop-invariant: sbase[] registers them off
        # the static CSRs (stride*i with constant i is shift-add, no DSP) and
        # ptrs[] advances by nb per beat - the addr mux is all that remains.
        # offsets[] stays for the CSR readback + wrap test (ABI unchanged).
        # Ordering is enforced in hardware: ~en reloads ptrs from sbase, and
        # the driver programs base/stride before enable (it always has).
        sbase   = Array(Signal(64) for _ in range(n_streams))
        ptrs    = Array(Signal(64) for _ in range(n_streams))
        user    = Signal(4)
        sel     = Signal(4)
        addr    = Signal(64)
        en      = self._enable.storage
        # Payload register stage (2026-07-29): the sink comes straight off the
        # pcm CDC FIFO's BRAM read port, and computing base + stride*user +
        # offsets[user] combinationally from that read made
        # BRAM CLKARDCLK -> multiplier/adder chain -> writer AW the #1/#2
        # violated path on both boards' m0019j builds (arty -0.113 floor
        # after recovery, AX -0.596). One stream.Buffer re-times the whole
        # cone from registers; the PCM ring is media-paced (ms-scale), so a
        # cycle of added latency is invisible.
        from litex.soc.interconnect import stream as _stream
        self.submodules.inbuf = inbuf = _stream.Buffer(
            [("data", bus.data_width), ("user", 4)])
        self.comb += self.sink.connect(inbuf.sink)
        src = inbuf.source
        # clamp both indexes to the elaborated stream count (the datapath only
        # emits tuser < N_STREAMS; the clamp keeps a stray sel/user in range)
        self.comb += [
            user.eq(Mux(src.user >= n_streams, 0, src.user)),
            sel.eq(Mux(self._sel.storage >= n_streams, 0, self._sel.storage)),
            addr.eq(ptrs[user]),
            self.writer.sink.valid.eq(src.valid & en),
            self.writer.sink.data.eq(src.data),
            self.writer.sink.address.eq(addr[shift:]),
            src.ready.eq(self.writer.sink.ready | ~en),
            self._offset.status.eq(offsets[sel]),
            self._cap.status.eq((0x4D << 24) | int(n_streams)),
        ]
        self.sync += [
            *[sbase[i].eq(self._base.storage + self._stride.storage * i)
              for i in range(n_streams)],
            If(~en,
                *[o.eq(0) for o in offsets],
                *[p.eq(sb) for p, sb in zip(ptrs, sbase)]
            ).Elif(src.valid & src.ready,
                If(offsets[user] + nb >= self._length.storage,
                    offsets[user].eq(0),
                    ptrs[user].eq(sbase[user])
                ).Else(
                    offsets[user].eq(offsets[user] + nb),
                    ptrs[user].eq(ptrs[user] + nb)
                )
            ),
        ]


class _PCMRingBRAM(LiteXModule):
    """On-chip dual-port BRAM PCM ring (KL_pcm_ring_bram.sv) - the shed-proof
    drop-in for the WishboneDMAWriter / _PCMRingNxN DRAM ring.

    Same sink + SAME CSR block as _PCMRingNxN (base[64], length[32], stride[32],
    enable, sel[4], offset[32], cap[32] at +0x1c) so the kl-eth/PipeWire ABI is
    byte-for-byte unchanged; N=1 is byte-identical to the flat ring. The write side rides the
    pcm CDC lane and its ready is CONSTANT 1 (single-cycle BRAM write), so the
    non-stallable datapath can never be told to wait - mf52 SHED + I6 cannot
    exist. The CPU reads PCM words through a read-only wishbone slave into the
    2nd BRAM port, mapped by MilanDMA into an uncached SoCRegion at
    MILAN_PCM_BRAM_BASE (a CPU *write* to the window is unacked by design)."""
    def __init__(self, n_streams=1, ring_bytes=MILAN_PCM_BRAM_SIZE, data_width=64):
        from litex.soc.interconnect import stream as _stream
        from litex.soc.interconnect import wishbone
        import math
        adr_w = 32 - int(math.log2(data_width // 8))
        self.sink    = _stream.Endpoint([("data", data_width), ("user", 4)])
        self._base   = CSRStorage(64, description="PCM ring base = BRAM MMIO window "
                                  "(driver-programmed; gateware ignores it for intra-BRAM addressing).")
        self._length = CSRStorage(32, description="per-stream sub-ring length (bytes).")
        self._stride = CSRStorage(32, description="byte distance between stream sub-ring bases.")
        self._enable = CSRStorage(description="ring enable (0 drops beats + clears offsets).")
        self._sel    = CSRStorage(4,  description="stream index for the offset readback.")
        self._offset = CSRStatus(32,  description="selected stream's write pointer (bytes).")
        # Geometry capability at +0x1c - identical word + placement as the
        # _PCMRingNxN one (SAME-CSR-block axiom above); see that class for the
        # honesty notes on the zero stride/T fields.
        assert 1 <= n_streams <= 0xFF
        self._cap = CSRStatus(32, description="geometry capability: [31:24]=0x4D 'M', "
                              "[23:16]=stride/64KiB (0 = driver-programmed via the stride CSR), "
                              "[15:8]=T playback rings behind this block (0), "
                              "[7:0]=L capture rings (elaborated N_STREAMS).")
        # CPU read port: read-only wishbone slave into BRAM port B.
        self.bus = wishbone.Interface(data_width=data_width, adr_width=adr_w, addressing="word")

        # # #

        # `base` is a plain RW CSR the driver programs (byte-identical to the
        # _PCMRingNxN ABI); the gateware does NOT drive it. An earlier revision
        # combinationally forced `_base.storage`, DOUBLE-DRIVING the register that
        # the CSR bus already writes (a migen driver conflict). The SoC decoder
        # places the whole BRAM array at MILAN_PCM_BRAM_BASE and the driver mmaps
        # that window (from the DT reg node); the SV ignores base for addressing.
        self.specials += Instance("KL_pcm_ring_bram",
            p_DATA_W     = data_width,
            p_N_STREAMS  = n_streams,
            p_RING_BYTES = ring_bytes,
            i_clk_i      = ClockSignal("sys"),
            i_rst_n      = ~ResetSignal("sys"),
            i_wr_data_i  = self.sink.data,
            i_wr_user_i  = self.sink.user,
            i_wr_valid_i = self.sink.valid,
            o_wr_ready_o = self.sink.ready,
            i_length_i   = self._length.storage,
            i_stride_i   = self._stride.storage,
            i_enable_i   = self._enable.storage,
            i_sel_i      = self._sel.storage,
            o_offset_o   = self._offset.status,
            i_wb_adr_i   = self.bus.adr,
            i_wb_cyc_i   = self.bus.cyc,
            i_wb_stb_i   = self.bus.stb,
            o_wb_dat_o   = self.bus.dat_r,
            o_wb_ack_o   = self.bus.ack,
        )
        self.comb += self._cap.status.eq((0x4D << 24) | int(n_streams))


class MilanDMA(LiteXModule):
    """AXIS ↔ system-memory DMA (§A.6), attaching the milan_datapath TX/RX/TS DMA
    AXIS ports to the CPU's memory via three LiteX simple-mode DMA engines:

      * TX   -  `WishboneDMAReader` : memory → `s_axis_tx`  (frames to transmit)
      * RX   -  `WishboneDMAWriter` : `m_axis_rx`  → memory (received frames)
      * TS   -  `WishboneDMAWriter` : `m_axis_ts`  → memory (PTP timestamp metadata)

    Each engine is `with_csr=True`, i.e. it exposes a **simple-mode** register block
    (`base` [64], `length` [32], `enable`, `done`, `loop`, `offset`) auto-mapped in
    the SoC CSR space  -  this is the ABI the Linux driver programs (mirrors the Zynq
    axi_dma simple mode). Each engine is its own Wishbone bus master into the SoC
    interconnect (width-adapted to the main bus automatically).

    `dp_ports` is merged with the MAC's into the single `milan_datapath` Instance.

    NOTE (board-gated): this elaborates against integrated RAM here; on the board it
    targets LiteDRAM. Descriptor/scatter-gather (Option 6b, multi-queue) is a later
    upgrade  -  see docs/integration/FULLY_FPGA_RISCV_MIGRATION.md §A.6 + the protocol/test matrix."""
    def __init__(self, soc, data_width=64, milan_cd="sys", rx_queues=1, hs_page_bytes=4096,
                 legacy_ring=True, rx_fifo_beats=2048, num_streams=1, pcm_ring="dram",
                 aaf_playback=False, rx_rsc=True, talker_wire_chans=2,
                 aaf_pb_streams=1):
        # rx_fifo_beats: store-and-forward ingress FIFO depth per RX queue (BRAM:
        # 2048 beats = 16KB = 4 RAMB36). Sized in the byte-ring era; in BD/hs
        # mode burst absorbency lives in the 60x16K posted-page pool, so 1024 is
        # the staged AREA-70 diet  -  gate any change on silicon drop counters
        # (q0 0xf000303c / q1 0xf00030b0) under the P4/P8 cells, never assume.
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
        # wishbone L2  -  a different path, so CPU writes and DMA reads are NOT coherent
        # (hardware-confirmed: the DMA transmits stale DRAM). Coherent DMA closes that gap
        # so a CPU-written frame is DMA-read correctly without manual cache flushes.
        dma_bus = getattr(soc, "dma_bus", soc.bus)
        # `endianness="big"` = **no** byte-swap (with_byteswap=False): keep the Wishbone word
        # order == AXIS stream order == on-the-wire byte order. The LiteX default "little"
        # byte-swaps each word, which (with LiteEth's little-endian GMII path) reverses every
        # frame word vs memory  -  hardware-confirmed: an RX frame `ff ff ff ff ff ff 02 aa`
        # landed in memory as `aa 02 ff ff ff ff ff ff`, and TX broadcast egressed with a
        # mangled `00:02:ff:..` dst so the peer dropped it. "big" makes memory<->wire match
        # in both directions (and the internal loopback stays byte-exact, being symmetric).
        # TX: memory -> datapath. RingDMAReader (see its docstring)  -  a native AXI
        # burst master like the RX writer: software queues frames in a DRAM ring and
        # writes ONE CSR per frame; the per-frame base/length/enable+DONE dance (and
        # the ~21 MB/s per-beat wishbone ceiling) are gone. Same 7-word CSR footprint,
        # so the DT `dma-tx` window and all later CSR addresses stay put.
        self.tx = RingDMAReader(axi.AXIInterface(data_width=data_width, address_width=32,
                                                 id_width=4), legacy_ring=legacy_ring)
        dma_bus.add_master("milan_dma_tx", master=self.tx.bus)
        # RX: datapath -> circular DRAM ring (RingDMAWriter  -  see its docstring; replaces
        # the single-shot writer whose re-arm-per-frame protocol corrupted RX under load).
        # Same 7-word CSR footprint, so the DT `dma-rx` window and all later CSRs stay put.
        # NATIVE AXI master (not wishbone): the NaxRiscv coherent dma_bus is full AXI4,
        # and burst writes amortize the per-transaction coherency round trip that capped
        # the wishbone adapter at ~21 MB/s (< the 125 MB/s wire  -  HW-measured, see the
        # RingDMAWriter docstring). The dma_bus handler is standard "axi", so this master
        # connects through AXIInterconnectShared with bursts intact.
        # cq_depth=32 (was the 8 default): header-split spends 1+pages CQ entries per
        # aggregate (legacy spent 1)  -  at 8, one 20KB aggregate (6 entries) trips the
        # CQD-2 opener gate and a 39KB cwnd burst overruns mid-frame => PGSWAP no-room
        # famine => tail discard => TCP loss every burst clamped cwnd~27 (silicon
        # 2026-07-10: 138 Mbit; BUFSZ=16K config probe confirmed the model at 279).
        # 32 fits PAYCAP (meta+14 pages) plus a second aggregate with slack.
        # rx_rsc=False (rxq2-sans-RSC): both queue writers elaborate WITHOUT the
        # RSC engine; steering, BD/hs CSR maps and the plain v1 path are intact.
        self.rx = RingDMAWriter(axi.AXIInterface(data_width=data_width, address_width=32,
                                                 id_width=4), cq_depth=32,
                                hs_page_bytes=hs_page_bytes, legacy_ring=legacy_ring,
                                fifo_beats=rx_fifo_beats, rsc_capable=rx_rsc)
        dma_bus.add_master("milan_dma_rx", master=self.rx.bus)
        # RX fan-out (rx_queues=2): a steering front-end splits the single RX stream
        # into 2 queues, each its own RingDMAWriter + IRQ + NAPI. Since the 802.1Q-ordered
        # round (2026-07-26) the split is gPTP (q1) vs everything else (q0) per the
        # USER's 2-ingress-queue directive, NOT the old TCP 4-tuple flow hash - see
        # RxSteer's docstring for what that trades away (parallel ACK processing)
        # and what it buys (PTP off the bulk ring). rx1's IRQ reuses the unused
        # ev.tx line.
        if rx_queues >= 2:
            self.steer = RxSteer()
            # hsq8 (2026-07-10): rx1 goes hs-capable + CQD=32  -  the CQ LUTRAM diet +
            # --strip-probes bought the area (hsq7t proved 2q FITS at 99.4% slices,
            # hsq8p reclaimed 274 more + 4.3K FFs). CQD=32 per the hsq4 lesson (hs
            # spends 1+pages CQ entries/agg; 8 clamps cwnd ~27 => 138 Mbit). rx1's
            # CSR block already carried the inert rsc/hs registers, so this changes
            # NO addresses  -  kl-eth hsplit11 (hsplit=2) enables q1-hs; hsplit<=1
            # drivers keep q1 legacy (hs_en=0 reset => bit-exact legacy behavior).
            self.rx1 = RingDMAWriter(axi.AXIInterface(data_width=data_width,
                                                      address_width=32, id_width=4),
                                     cq_depth=32, hs_capable=True,
                                     hs_page_bytes=hs_page_bytes,
                                     legacy_ring=legacy_ring,
                                     fifo_beats=rx_fifo_beats, rsc_capable=rx_rsc)
            dma_bus.add_master("milan_dma_rx1", master=self.rx1.bus)
        self.ts = WishboneDMAWriter(mk_bus(), endianness="big", with_csr=True)
        dma_bus.add_master("milan_dma_ts", master=self.ts.bus)
        # hs page-size capability readback (hsq14 hardening): the driver's hs_pgsz
        # MUST equal the elaborated hs_page_bytes  -  a mismatch makes the writer DMA
        # gateware-page strides into smaller driver pages = kernel memory overwrite
        # (panicked 2026-07-11). Registered LAST in this bank so no existing CSR
        # address moves (csv-diff-verified additions-only). 0 on older gateware
        # (unmapped reads) => the driver treats absence as "no capability, trust
        # the operator" for backward compatibility.
        self.hs_pgsz_cap = CSRStatus(17, description="elaborated hs_page_bytes (driver pairing check)")
        self.comb += self.hs_pgsz_cap.status.eq(hs_page_bytes)
        # PCM: AAF RX depacketizer payload -> DRAM PCM ring (Milan listener media
        # path, ARCHITECTURE_HW_SW_SPLIT "DMA PCM ring from Linux first"). Same
        # recipe as the TS record ring: WishboneDMAWriter with loop=1 wraps
        # base..base+length and the `offset` CSR is the ring write pointer the
        # consumer (PipeWire) chases. Payload is full 64-bit words in wire byte
        # order (S32BE interleaved) - the depacketizer zero-pads any non-multiple
        # tail. Registered AFTER hs_pgsz_cap so no existing CSR address moves.
        # P12 (NXN §1.3): at num_streams == 1 the flat single-ring writer is
        # kept EXACTLY (same CSR block, same behavior — the N=1 byte-identity
        # axiom); num_streams > 1 swaps in the per-stream ring writer keyed by
        # the datapath's m_axis_pcm_tuser: stream s lands at base + s*stride
        # (stream 0 at the base; stride only engages for s > 0).
        if pcm_ring == "bram":
            # On-chip BRAM ring: NO DMA master (not a DMA) and NO DRAM arbitration
            # => sink.ready is constant 1, so mf52 SHED + I6 cannot occur. The read
            # port is an uncached SoCRegion at MILAN_PCM_BRAM_BASE; the pcm CSR block
            # is identical to the DRAM path so the kl-eth/PipeWire ABI is unchanged
            # (N=1 stays byte-identical to the flat ring).
            self.pcm = _PCMRingBRAM(n_streams=num_streams, ring_bytes=MILAN_PCM_BRAM_SIZE,
                                    data_width=data_width)
            soc.bus.add_slave("milan_pcm_bram", self.pcm.bus,
                              region=SoCRegion(origin=MILAN_PCM_BRAM_BASE,
                                               size=MILAN_PCM_BRAM_SIZE, cached=False))
        elif num_streams > 1:
            self.pcm = _PCMRingNxN(mk_bus(), n_streams=num_streams)
            dma_bus.add_master("milan_dma_pcm", master=self.pcm.writer.bus)
        else:
            self.pcm = WishboneDMAWriter(mk_bus(), endianness="big", with_csr=True)
            dma_bus.add_master("milan_dma_pcm", master=self.pcm.bus)

        # datapath-facing endpoints in `milan_cd`, async-FIFO CDC'd to the sys-domain
        # DMA engines when the domains differ (see _axis_dp_cdc). TX is mem->datapath;
        # RX/TS are datapath->mem.
        L = [("data", data_width), ("keep", nb)]
        tx_dp = _axis_dp_cdc(self, "dma_tx_cdc", L, milan_cd, to_datapath=True)
        rx_dp = _axis_dp_cdc(self, "dma_rx_cdc", L, milan_cd, to_datapath=False)
        ts_dp = _axis_dp_cdc(self, "dma_ts_cdc", L, milan_cd, to_datapath=False)
        # PCM lane carries the stream-index tuser through the CDC at N > 1
        # (the per-stream ring writer's key); N = 1 keeps the exact P11 lane.
        Lp = L + [("user", 4)] if num_streams > 1 else L
        # depth 128 (2026-07-23): the 16-deep lane dropped EXACTLY 1 beat in 24
        # whenever the CPU read the ring region concurrently (arecord rw path;
        # ring holes at a stable mod-24 phase, 2 kHz whole-frame artifact) -
        # the wishbone writer sustains ~23/24 of the PCM rate under DRAM
        # contention and the real-time datapath side sheds on full. 1 KB of
        # FIFO absorbs the CPU's bursty copy stalls outright.
        pcm_dp = _axis_dp_cdc(self, "dma_pcm_cdc", Lp, milan_cd, to_datapath=False, depth=128)
        # exposed for MilanDebug's TX datapath-input probe: tx_dp.dp is the milan-domain
        # endpoint feeding the datapath (traffic_controller s_axis). tx_dp.dp.ready IS
        # the traffic_controller's backpressure  -  the direct "is the datapath the TX
        # limit?" signal (stall = valid&~ready) vs "is the CPU/reader?" (starve = ~valid).
        self.tx_dp    = tx_dp
        self.milan_cd = milan_cd
        # TX: reader.source (sys) -> REGISTER STAGE -> datapath TX endpoint. The Buffer
        # cuts the reader's byte-assembly cone (blen_r -> in_last -> a_nxt -> source.data)
        # off the CDC FIFO's write-port setup path  -  the exact WNS violators of the
        # 112.5 MHz sys build (x1125: -0.226, ALL in this cone; the CPU itself closed).
        # +1 cycle of TX latency, zero protocol change; the reader RTL is untouched.
        self.tx_buf = tx_buf = stream.Buffer(L)
        self.comb += [
            # The ring reader carries the exact last-beat byte mask (from the header's
            # byte length), so wire frames are not padded to 8 B  -  the MAC glue turns
            # keep into last_be.
            self.tx.source.connect(tx_buf.sink),
            tx_dp.sys.valid.eq(tx_buf.source.valid), tx_dp.sys.data.eq(tx_buf.source.data),
            tx_dp.sys.last.eq(tx_buf.source.last),   tx_dp.sys.keep.eq(tx_buf.source.keep),
            tx_buf.source.ready.eq(tx_dp.sys.ready),
            # TS: datapath TS endpoint (sys side) -> writer.sink
            self.ts.sink.valid.eq(ts_dp.sys.valid), self.ts.sink.data.eq(ts_dp.sys.data),
            # tlast is NOT forwarded: the LiteX ctrl FSM treats sink.last as
            # end-of-transfer and (loop=1) restarts offset at 0 - with the
            # 2-beat records that made EVERY record overwrite slot 0 (the
            # phase B "offset stuck at 0" silicon finding; one record was in
            # DRAM, perfect, always at base+0). Untied, the writer runs
            # offset 0..length-1 and wraps = a true linear record ring.
            ts_dp.sys.ready.eq(self.ts.sink.ready),
            # PCM: datapath PCM endpoint (sys side) -> ring writer.sink.
            # tlast is NOT forwarded - same reason as the TS ring above: the
            # LiteX ctrl FSM restarts offset on sink.last, and PCM leaves the
            # datapath as one AXIS frame per AAF PDU.
            self.pcm.sink.valid.eq(pcm_dp.sys.valid), self.pcm.sink.data.eq(pcm_dp.sys.data),
            pcm_dp.sys.ready.eq(self.pcm.sink.ready),
        ]
        if num_streams > 1:
            # per-stream ring key: the tuser stream index rides the CDC lane
            self.comb += self.pcm.sink.user.eq(pcm_dp.sys.user)
        if rx_queues >= 2:
            # RX: datapath -> steer -> {rx.sink (q0), rx1.sink (q1)}
            self.comb += [
                self.steer.sink.valid.eq(rx_dp.sys.valid),
                self.steer.sink.data.eq(rx_dp.sys.data),
                self.steer.sink.keep.eq(rx_dp.sys.keep),
                self.steer.sink.last.eq(rx_dp.sys.last),
                rx_dp.sys.ready.eq(self.steer.sink.ready),
                self.steer.source0.connect(self.rx.sink),
                self.steer.source1.connect(self.rx1.sink),
            ]
        else:
            # RX: datapath RX endpoint (sys side) -> single writer.sink
            self.comb += [
                self.rx.sink.valid.eq(rx_dp.sys.valid), self.rx.sink.data.eq(rx_dp.sys.data),
                self.rx.sink.last.eq(rx_dp.sys.last),    rx_dp.sys.ready.eq(self.rx.sink.ready),
            ]

        # Pmod I2S2 on pmoda (AAF talker audio-in). Plumbing only: request the
        # pins where the board has them; absent (AX7101) -> talker input ties 0.
        # GATE ON THE CONNECTOR TABLE, not try/except: add_extension/request
        # succeed regardless - the missing-connector assertion only fires at
        # constraint RESOLUTION (finalization), far outside any except here
        # (the AX7101 elaboration broke on 'pmoda' 2026-07-13 because of it).
        self.i2s_pads = None
        self.i2s_dac_pads = None
        plat = soc.platform
        try:
            _has_pmoda = "pmoda" in plat.constraint_manager.connector_manager.connector_table
        except AttributeError:
            _has_pmoda = False
        if _has_pmoda:
            try:
                from litex_boards.platforms.digilent_arty import i2s_pmod_io
                plat.add_extension(i2s_pmod_io("pmoda"))
                _rx  = plat.request("i2s_rx")
                _mck = plat.request("i2s_rx_mclk")
                self.i2s_pads = (_mck, _rx.clk, _rx.sync, _rx.rx)
                # DAC (line-out) jack: zero-CPU playback of the bound stream
                _tx  = plat.request("i2s_tx")
                _tmk = plat.request("i2s_tx_mclk")
                self.i2s_dac_pads = (_tmk, _tx.clk, _tx.sync, _tx.tx)
            except Exception:
                self.i2s_pads = None
        # ---- HANDOVER 8.3b: the Arty TDM8 MASTER header on pmodb ----
        # Declared whenever the board has the connector, requested (loosely)
        # only by a master build below - same connector-table gate as pmoda.
        # This one add_extension line is what flips board_audio_routing.py's
        # routing oracle for the Arty; pmoda and the Pmod I2S2 are untouched.
        try:
            _has_pmodb = "pmodb" in plat.constraint_manager.connector_manager.connector_table
        except AttributeError:
            _has_pmodb = False
        if _has_pmodb:
            plat.add_extension(_arty_serial_io("tdm", "pmodb"))
        # ---- item-7 ALSA playback: host PCM ring -> KL_pcm_tx pair source ----
        # The TX/talker mirror of the RX depacketizer PCM ring. Software writes
        # S32BE-interleaved PCM into a DRAM ring (per-stream sub-rings at
        # base + s*stride, `length` bytes each) and bumps the per-stream wr_ptr
        # doorbell; KL_pcm_tx (inside milan_datapath, milan_cd) paces the media
        # clock, de-interleaves, and drives the AAF packetizer pair stream in
        # place of the ADC capture front-end. KL_pcm_tx OWNS the ring addressing
        # (rd_ptr/wrap), so its word-fetch port is bridged to a dumb random-
        # access wishbone READ master on the DMA bus (req/resp AXIS CDC when
        # milan_cd != sys). Control/status are a small CSR block in the milan_dma
        # group. All gated on --aaf-playback: off => none of this exists, so the
        # default build is byte-identical.
        pb_ports = {}
        if aaf_playback:
            shift = int(math.log2(nb))
            ns    = int(num_streams)
            wch   = int(talker_wire_chans)
            # task #31 START-SMALL: the pb CSR block is sized by the SERVED
            # ring count (the same value add_milan_datapath passes as
            # p_AAF_PB_STREAMS_P - one writer, both sides derived), not by
            # N_STREAMS: the boundary ports stay N_STREAMS-wide and the
            # unserved tail is constant zero (swept in synthesis).
            pbs   = max(1, min(int(aaf_pb_streams), ns))
            # Geometry capability word FIRST in the block (the +0x1c capture
            # precedent, self-identifying): the driver reads pb-dma +0x00 and
            # refuses a window whose magic/shape disagrees with its DT. Every
            # field is elaboration TRUTH: [31:24]=0x4D 'M', [23:16]=wire
            # channels per stream (TALKER_WIRE_CHANS_P - the ring's frame is
            # chans/2 x 8-byte pair words), [15:8]=T playback rings SERVED
            # (aaf_pb_streams), [7:0]=L capture rings behind this
            # block (0 - the capture geometry lives at pcm-dma +0x1c).
            assert 1 <= pbs <= 0xFF and 2 <= wch <= 0xFF
            self._pb_cap = CSRStatus(32, description="playback geometry capability: "
                                     "[31:24]=0x4D 'M', [23:16]=wire chans/stream, "
                                     "[15:8]=T playback rings (elaborated), [7:0]=0.")
            self.comb += self._pb_cap.status.eq((0x4D << 24) | (wch << 16) | (pbs << 8))
            self._pb_enable      = CSRStorage(description="AAF playback master enable (KL_pcm_tx pair source).")
            self._pb_silence     = CSRStorage(description="underrun policy: 0 repeat-last, 1 digital silence.")
            self._pb_ring_base   = CSRStorage(64, description="playback PCM ring base (stream 0 sub-ring, bytes).")
            self._pb_ring_len    = CSRStorage(32, description="per-stream sub-ring length (bytes, multiple of 8).")
            self._pb_ring_stride = CSRStorage(32, description="bytes between stream sub-ring bases.")
            self._pb_stream_en   = CSRStorage(pbs, description="per-stream ring-read gate (bit s).")
            self._pb_playing     = CSRStatus(description="KL_pcm_tx is walking a sample tick.")
            # per-stream vectors packed 32/16b each in one wide CSR (spanning
            # ceil(width/32) sub-words; stream s is bits [s*w +: w]). wr_ptr is
            # the host doorbell; rd_ptr/under/over are the KL_pcm_tx status.
            self._pb_wr_ptr = CSRStorage(pbs*32, description="per-stream host write pointers (32b each, absolute bytes).")
            self._pb_rd_ptr = CSRStatus(pbs*32,  description="per-stream consumed pointers (32b each, absolute bytes).")
            self._pb_under  = CSRStatus(pbs*16,  description="per-stream underrun counts (16b each).")
            self._pb_over   = CSRStatus(pbs*16,  description="per-stream overrun counts (16b each).")
            # served-slice <-> N_STREAMS-wide boundary pads
            pb_sen_full = Signal(ns)
            pb_wr_full  = Signal(ns*32)
            self.comb += [pb_sen_full[:pbs].eq(self._pb_stream_en.storage),
                          pb_wr_full[:pbs*32].eq(self._pb_wr_ptr.storage)]
            # CDC control sys<->milan_cd. Multi-bit -> BusSynchronizer (coherent
            # word); 1-bit -> MultiReg. The wr_ptr doorbell tolerates the resync
            # latency (KL_pcm_tx only reads it to gauge fill); a credit handshake
            # is the silicon follow-up.
            def _in(name, sig):
                if milan_cd == "sys":
                    return sig
                if len(sig) == 1:
                    d = Signal(); self.specials += MultiReg(sig, d, odomain=milan_cd); return d
                bs = BusSynchronizer(len(sig), "sys", milan_cd); setattr(self, name, bs)
                self.comb += bs.i.eq(sig); return bs.o
            def _out(name, width):
                dp = Signal(width)
                if milan_cd == "sys":
                    return dp, dp
                if width == 1:
                    o = Signal(); self.specials += MultiReg(dp, o); return dp, o
                bs = BusSynchronizer(width, milan_cd, "sys"); setattr(self, name, bs)
                self.comb += bs.i.eq(dp); return dp, bs.o
            pb_rd_dp, pb_rd_s = _out("aafpb_bs_rd", ns*32)
            pb_un_dp, pb_un_s = _out("aafpb_bs_un", ns*16)
            pb_ov_dp, pb_ov_s = _out("aafpb_bs_ov", ns*16)
            pb_pl_dp, pb_pl_s = _out("aafpb_bs_pl", 1)
            self.comb += [self._pb_rd_ptr.status.eq(pb_rd_s[:pbs*32]),
                          self._pb_under.status.eq(pb_un_s[:pbs*16]),
                          self._pb_over.status.eq(pb_ov_s[:pbs*16]),
                          self._pb_playing.status.eq(pb_pl_s)]
            # word-fetch bridge: KL_pcm_tx mem port <-> wishbone READ master.
            pb_mem_addr  = Signal(32)      # milan_cd (datapath out)
            pb_mem_rd    = Signal()        # milan_cd
            pb_mem_data  = Signal(64)      # milan_cd (datapath in)
            pb_mem_valid = Signal()        # milan_cd
            req  = _axis_dp_cdc(self, "aafpb_req_cdc",  [("addr", 32)], milan_cd, to_datapath=False)
            resp = _axis_dp_cdc(self, "aafpb_resp_cdc", [("data", 64)], milan_cd, to_datapath=True)
            self.comb += [
                req.dp.valid.eq(pb_mem_rd), req.dp.addr.eq(pb_mem_addr),
                pb_mem_data.eq(resp.dp.data), pb_mem_valid.eq(resp.dp.valid),
                resp.dp.ready.eq(1),       # KL_pcm_tx latches its awaited word
            ]
            self.aafpb_wb = wishbone.Interface(data_width=data_width, adr_width=adr_w, addressing="word")
            dma_bus.add_master("milan_aaf_pb", master=self.aafpb_wb)
            pb_addr_l = Signal(32); pb_data_l = Signal(data_width)
            self.aafpb_fsm = fsm = FSM(reset_state="IDLE")
            fsm.act("IDLE",
                req.sys.ready.eq(1),
                If(req.sys.valid, NextValue(pb_addr_l, req.sys.addr), NextState("READ")))
            fsm.act("READ",
                self.aafpb_wb.cyc.eq(1), self.aafpb_wb.stb.eq(1),
                self.aafpb_wb.adr.eq(pb_addr_l[shift:]), self.aafpb_wb.sel.eq(2**nb - 1),
                If(self.aafpb_wb.ack, NextValue(pb_data_l, self.aafpb_wb.dat_r), NextState("RESP")))
            fsm.act("RESP",
                resp.sys.valid.eq(1), resp.sys.data.eq(pb_data_l),
                If(resp.sys.ready, NextState("IDLE")))
            pb_ports = dict(
                i_pb_enable_i           = _in("aafpb_bs_en",  self._pb_enable.storage),
                i_pb_underrun_silence_i = _in("aafpb_bs_sil", self._pb_silence.storage),
                i_pb_stream_en_i        = _in("aafpb_bs_sen", pb_sen_full),
                i_pb_ring_base_i        = _in("aafpb_bs_base", self._pb_ring_base.storage),
                i_pb_ring_len_i         = _in("aafpb_bs_len",  self._pb_ring_len.storage),
                i_pb_ring_stride_i      = _in("aafpb_bs_str",  self._pb_ring_stride.storage),
                i_pb_wr_ptr_i           = _in("aafpb_bs_wr",   pb_wr_full),
                i_pb_mem_data_i         = pb_mem_data,
                i_pb_mem_valid_i        = pb_mem_valid,
                o_pb_mem_addr_o         = pb_mem_addr,
                o_pb_mem_rd_o           = pb_mem_rd,
                o_pb_rd_ptr_o           = pb_rd_dp,
                o_pb_underrun_o         = pb_un_dp,
                o_pb_overrun_o          = pb_ov_dp,
                o_pb_playing_o          = pb_pl_dp,
            )
        self.dp_ports = dict(
            # TX: reader.source (mem data) -> datapath s_axis_tx
            i_s_axis_tx_tdata  = tx_dp.dp.data,  i_s_axis_tx_tkeep = tx_dp.dp.keep,
            i_s_axis_tx_tvalid = tx_dp.dp.valid, i_s_axis_tx_tlast = tx_dp.dp.last,
            o_s_axis_tx_tready = tx_dp.dp.ready,
            # RX: datapath m_axis_rx -> writer.sink
            o_m_axis_rx_tdata  = rx_dp.dp.data,  o_m_axis_rx_tvalid = rx_dp.dp.valid,
            o_m_axis_rx_tlast  = rx_dp.dp.last,  i_m_axis_rx_tready = rx_dp.dp.ready,
            # TS: datapath m_axis_ts -> writer.sink
            o_i2s_dac_mclk_o = self.i2s_dac_pads[0] if self.i2s_dac_pads else Signal(),
            o_i2s_dac_sclk_o = self.i2s_dac_pads[1] if self.i2s_dac_pads else Signal(),
            o_i2s_dac_lrck_o = self.i2s_dac_pads[2] if self.i2s_dac_pads else Signal(),
            o_i2s_dac_sdin_o = self.i2s_dac_pads[3] if self.i2s_dac_pads else Signal(),
            o_i2s_mclk_o = self.i2s_pads[0] if self.i2s_pads else Signal(),
            o_i2s_sclk_o = self.i2s_pads[1] if self.i2s_pads else Signal(),
            o_i2s_lrck_o = self.i2s_pads[2] if self.i2s_pads else Signal(),
            i_i2s_sdout_i = self.i2s_pads[3] if self.i2s_pads else 0,
            o_m_axis_ts_tdata  = ts_dp.dp.data,  o_m_axis_ts_tvalid = ts_dp.dp.valid,
            o_m_axis_ts_tlast  = ts_dp.dp.last,  i_m_axis_ts_tready = ts_dp.dp.ready,
            # PCM: datapath m_axis_pcm -> PCM ring writer.sink. tuser = stream
            # index (NXN §1.3 P12: ring base + s*stride key); at N=1 the tag
            # is constant 0 and lands in an unconnected sink (flat ring).
            o_m_axis_pcm_tdata  = pcm_dp.dp.data,  o_m_axis_pcm_tkeep = pcm_dp.dp.keep,
            o_m_axis_pcm_tvalid = pcm_dp.dp.valid,
            o_m_axis_pcm_tlast  = pcm_dp.dp.last,  i_m_axis_pcm_tready = pcm_dp.dp.ready,
            o_m_axis_pcm_tuser  = (pcm_dp.dp.user if num_streams > 1 else Signal(4)),
            # item-7 ALSA playback ports (empty dict unless --aaf-playback)
            **pb_ports,
        )


# Debug / pipeline telemetry ----------------------------------------------------------------------

class MilanDebug(LiteXModule):
    """Memory-mapped observability for the whole TX+RX AXIS pipeline  -  the numbers a HW
    developer wants to localise where a frame is lost or where it queues up.

    At each pipeline stage it counts, free-running (reset via `reset`):
      * `*_frames`  -  completed frames (valid & ready & last). A frame present at stage N
        but missing at N+1 pinpoints the loss.
      * `*_beats`   -  beats transferred (valid & ready). frames→size, beats→throughput.
      * `*_stalls`  -  cycles the stage was back-pressured (valid & ~ready). The bottleneck
        stage is the one with high stalls upstream of it.

    Stages (see the pipeline both ways):
      TX:  dma_out → dp_out → core_in → [LiteEth] → tx_wire (GMII)
      RX:  rx_wire (GMII) → [LiteEth] → core_out → dp_in → dma_in

    `tx_wire`/`rx_wire` count frames on the GMII pins (eth_tx/eth_rx domains, brought to
    sys with a BusSynchronizer)  -  the answer to "did it actually reach the wire?".

    `*_inflight_acc` accumulate Σ(in-flight) each cycle across the black-box datapath
    (in-flight = frames_in − frames_out). By Little's law: **avg occupancy = acc/cycles**
    and **avg latency (wait time) = acc/frames**  -  the average FIFO depth and the average
    time a frame spends crossing the datapath. `cycles` is the free-running normaliser.

    **Coherent capture.** All counters run live; writing `capture` latches EVERY counter
    into a shadow at the same clock edge, and the CSRs read the shadow. So software does:
    one write to `capture`, then read the whole set  -  a consistent snapshot, not values
    still moving between reads. `reset` zeroes the live counters.

    **Extensible.** The probe primitives are public methods  -  `sys_probe`, `wire_probe`,
    `match_probe`, `ethertype_probe`, `inflight_acc` (all auto-`snap`'d and CSR-mapped).
    Add a new observable in one line, either inline below or via the `extra(dbg)` hook,
    e.g. count gPTP frames (done here), PTP-event frames, a VLAN/PCP, a dst-MAC match, a
    drop point, another FIFO's occupancy … The gPTP TX/RX counters below are the worked
    example of `ethertype_probe`.

    **Cross-platform (LiteX vs Zynq).** This class is the **LiteX** binding  -  it uses
    LiteX for the LiteX-specific things: LiteX `CSRStatus` registers, `BusSynchronizer`
    for the CDC, and taps on the LiteX edges (the `WishboneDMAReader/Writer` and the
    `LiteEthPHYGMII` wire). The *shared* observables  -  everything at the `milan_datapath`
    AXIS boundary (tx_dp/rx_dp) and inside it  -  are the same on Zynq; the cross-platform
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
        self._snap(cyc, 64, "cycles", "free-running sys cycles at capture  -  normaliser")

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

        # --- TX datapath INPUT (milan domain): is the datapath the TX limit? -----------
        # Counts, in the DATAPATH clock domain, the handshake at tx_dp.dp (feeding the
        # traffic_controller s_axis). busy = beats accepted; stall = data offered but
        # the datapath back-pressures (datapath-internally-limited); starve = no data
        # (reader/CPU can't feed it). High stall -> the 50 MHz datapath IS the cap;
        # high starve -> the CPU/reader is, and the datapath has headroom.
        self.dp_in_probe("txdp_in", getattr(dma, "tx_dp", None),
                         getattr(dma, "milan_cd", "sys"),
                         "TX datapath input (traffic_controller s_axis)")

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
        self._snap(frames, 32, f"{name}_frames", f"{desc}  -  completed frames")
        self._snap(beats,  32, f"{name}_beats",  f"{desc}  -  beats (valid&ready)")
        self._snap(stalls, 32, f"{name}_stalls", f"{desc}  -  back-pressure cycles")
        return frames

    def dp_in_probe(self, name, ep, cd, desc):
        """busy/stall/starve/cyc at a datapath-input endpoint in domain `cd`, to sys.

        Free-running (like wire_probe); the reader takes a delta between two captures.
        stall (valid & ~ready) = the datapath back-pressures = datapath-limited;
        starve (~valid)        = no data offered        = reader/CPU-limited."""
        ep = getattr(ep, "dp", ep) if ep is not None else None
        if ep is None:
            return
        busy, stall, starve, cyc = (Signal(32) for _ in range(4))
        counts = [
            cyc.eq(cyc + 1),
            If(ep.valid & ep.ready,  busy.eq(busy + 1)),
            If(ep.valid & ~ep.ready, stall.eq(stall + 1)),
            If(~ep.valid,            starve.eq(starve + 1)),
        ]
        pairs = ((busy, "busy"), (stall, "stall"), (starve, "starve"), (cyc, "cyc"))
        if cd == "sys":                       # same domain: no CDC needed
            self.sync += counts
            for sig, tag in pairs:
                self._snap(sig, 32, f"{name}_{tag}", f"{desc}  -  {tag}")
            return
        getattr(self.sync, cd).__iadd__(counts)
        for sig, tag in pairs:                # cross the datapath domain to sys
            bs = BusSynchronizer(32, cd, "sys"); setattr(self, f"{name}_{tag}_bs", bs)
            self.comb += bs.i.eq(sig)
            self._snap(bs.o, 32, f"{name}_{tag}", f"{desc}  -  {tag}")

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
        frames carry it 4 bytes later  -  extend here if you need the tagged case."""
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

    # ---- Phase-0 reader probes (TX_READER_PREFETCH_PLAN.md Appendix A) ------------------
    # All sys-domain (the RingDMAReader/Writer are sys masters) → no CDC. Reset-based, like
    # sys_probe: pulse `reset`, run the load, pulse `capture`, read a coherent snapshot.
    def rd_latency_probe(self, name, rdr, desc):
        """AR-accepted -> first-R-beat round-trip latency. Mean L = acc/n cyc (×1000/f_MHz
        ns); payload-only split (ar.len>=8) excludes header/BD/shadow reads. Phase-0 tool:
        the single (waiting,lat) pair is exact ONLY while the reader is single-outstanding  - 
        which is the gateware Phase-0 runs on (see plan A.1)."""
        bus = rdr.bus
        ar_fire = Signal()
        self.comb += ar_fire.eq(bus.ar.valid & bus.ar.ready)
        waiting = Signal(); lat = Signal(16); is_pay = Signal()
        acc = Signal(48); n = Signal(32); mx = Signal(16)
        pacc = Signal(48); pn = Signal(32)
        self.sync += If(self._rst,
            acc.eq(0), n.eq(0), mx.eq(0), pacc.eq(0), pn.eq(0), waiting.eq(0), lat.eq(0),
        ).Else(
            If(waiting,
                If(bus.r.valid,                     # first R beat of this burst: record
                    waiting.eq(0),
                    acc.eq(acc + lat), n.eq(n + 1),
                    If(lat > mx, mx.eq(lat)),
                    If(is_pay, pacc.eq(pacc + lat), pn.eq(pn + 1)),
                ).Else(
                    lat.eq(lat + 1),
                )
            ).Elif(ar_fire,                         # start timing (single-outstanding: safe)
                waiting.eq(1), lat.eq(0), is_pay.eq(bus.ar.len >= 8),
            ),
        )
        for sig, w, tag, d in ((acc, 48, "acc", "sum AR->firstR cyc, all reads"),
                               (n,   32, "n",   "read count"),
                               (mx,  16, "max", "worst-case latency cyc"),
                               (pacc, 48, "pacc", "sum cyc, payload bursts len>=8"),
                               (pn,  32, "pn",  "payload-burst count")):
            self._snap(sig, w, f"{name}_{tag}", f"{desc} - {d}")

    def rd_produce_probe(self, name, rdr, desc):
        """Partition every sys cycle by WHY the reader is/ isn't feeding `source`. Splits the
        silent pre-pass into read-blocked (PREFETCHABLE) vs summing-beats (STRUCTURAL double-
        read)  -  the number that decides whether prefetch alone can reach 200. Books balance:
        busy+stall+pre_wait+pre_busy+rd_wait+idle+setup == cyc."""
        src, bus = rdr.source, rdr.bus
        prod = Signal(); stall = Signal(); nov = Signal(); rwait = Signal()
        self.comb += [
            prod.eq(src.valid & src.ready),
            stall.eq(src.valid & ~src.ready),
            nov.eq(~src.valid),
            rwait.eq(rdr.dbg_reading & ~bus.r.valid),
        ]
        busy = Signal(32); st = Signal(32); cyc = Signal(32)
        pre_wait = Signal(32); pre_busy = Signal(32); rd_wait = Signal(32)
        idle = Signal(32); setup = Signal(32)
        self.sync += If(self._rst,
            busy.eq(0), st.eq(0), cyc.eq(0), pre_wait.eq(0), pre_busy.eq(0),
            rd_wait.eq(0), idle.eq(0), setup.eq(0),
        ).Else(
            cyc.eq(cyc + 1),
            If(prod,  busy.eq(busy + 1)),
            If(stall, st.eq(st + 1)),
            If(nov,                                 # not producing → why? (priority order)
                If(rdr.dbg_cs_pass & rwait, pre_wait.eq(pre_wait + 1)
                ).Elif(rdr.dbg_cs_pass,     pre_busy.eq(pre_busy + 1)
                ).Elif(rwait,               rd_wait.eq(rd_wait + 1)
                ).Elif(rdr.dbg_idle,        idle.eq(idle + 1)
                ).Else(                     setup.eq(setup + 1)),
            ),
        )
        for sig, tag, d in ((busy, "busy", "producing valid&ready"),
                            (st, "stall", "source back-pressured by datapath"),
                            (pre_wait, "pre_wait", "pre-pass read-blocked PREFETCHABLE"),
                            (pre_busy, "pre_busy", "pre-pass summing beats STRUCTURAL"),
                            (rd_wait, "rd_wait", "real-pass read-blocked PREFETCHABLE"),
                            (idle, "idle", "IDLE ring-empty CPU/driver-bound"),
                            (setup, "setup", "AR-issue/PREP/header setup"),
                            (cyc, "cyc", "total cycles (normaliser)")):
            self._snap(sig, 32, f"{name}_{tag}", f"{desc} - {d}")

    def outstanding_hi_probe(self, name, wtr, desc):
        """Max AW-in-flight high-water on a RingDMAWriter  -  the read-depth proxy (same
        AXIInterconnectShared). ≥4 ⇒ read prefetch depth almost certainly available; ≤2 ⇒
        interconnect/L2 serializing (defer prefetch). Read after RX load."""
        hi = Signal(6)
        self.sync += If(self._rst, hi.eq(0)).Elif(wtr.dbg_outstanding > hi,
                                                  hi.eq(wtr.dbg_outstanding))
        self._snap(hi, 6, f"{name}_hi", f"{desc} - max AW in flight")

    # ---- M1 probes (CAMPAIGN_500_PLAN §M1) ----------------------------------------------
    def hiwater_probe(self, name, sig, width, desc):
        """Track max(sig) since `reset` and snap it (e.g. TX ring occupancy)."""
        hi = Signal(width)
        self.sync += If(self._rst, hi.eq(0)).Elif(sig > hi, hi.eq(sig))
        self._snap(hi, width, f"{name}_hi", desc)

    def pulse_count_probe(self, name, strobe, desc):
        """Count 1-cycle strobes since `reset` (e.g. TX doorbells = wr_ptr writes)."""
        n = Signal(32)
        self.sync += If(self._rst, n.eq(0)).Elif(strobe, n.eq(n + 1))
        self._snap(n, 32, name, desc)


# SoC ----------------------------------------------------------------------------------------------

class MilanSoC(SoCCore):
    def __init__(self, platform, sys_clk_freq, xlen=64, cpu_count=1,
                 with_milan=True, with_mac=False, with_dma=False, with_dram=False,
                 with_spiflash=False, flashboot="kernel", gtx_tx_invert=False,
                 main_ram_size=0x8000, milan_clk_freq=None, coherent_dma=False,
                 rgmii_tx_delay=2e-9, rgmii_rx_delay=2e-9, l2_bytes=None, with_fpu=False,
                 extra_scala_args=None, cpu="naxriscv", rx_queues=1, rx_rsc=True,
                 strip_probes=False, hs_page_bytes=4096, legacy_ring=False,
                 rx_fifo_beats=2048, board="ax7101", eth_phy_index=0,
                 num_streams=1, audio_if_slots=0, talker_wire_chans=2,
                 audio_if_master=False,
                 pcm_ring="dram", aaf_playback=False, aaf_pb_streams=1,
                 loopback_lane=False,
                 bus_standard="wishbone",
                 render_lpf=True, optional_blocks=None,
                 cbs_queues_mask=None, entity_gen_dir=None, **kwargs):
        # ---- RISC-V core(s), MMU, Linux-capable. Two cores are supported, selected by
        #      `cpu`: NaxRiscv (out-of-order, high IPC, ~100 MHz on this -2 Artix) or
        #      VexiiRiscv (in-order, higher fmax + smaller  -  the AVB-switch direction,
        #      see AVB_SWITCH_DIRECTION.md "CPU budget"). BOTH expose a coherent AXI
        #      `dma_bus` (soc.dma_bus) that the Milan DMA masters attach to identically
        #      (MilanDMA reads getattr(soc, "dma_bus", soc.bus)), and BOTH map csr @
        #      0xf000_0000 / clint @ 0xf001_0000 / plic @ 0xf0c0_0000  -  so the datapath
        #      and the ring DMA port over with no address changes.
        if cpu == "vexiiriscv":
            from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
            _vex_parser = argparse.ArgumentParser()
            VexiiRiscv.args_fill(_vex_parser)
            _vex_args, _ = _vex_parser.parse_known_args([])
            # cpu_variant is a SoCCore-level arg (not in the CPU parser)  -  set it here.
            # "linux" = rv{XLEN}imasu + MMU + L1$ + BTB/RAS/gshare (no C, no FPU);
            # "debian" additionally enables C + F + D. We use "linux" for the smallest,
            # highest-fmax Linux core (matches our no-C/no-FPU kernel); the --xlen in
            # vexii-args picks RV32 (sv32 MMU) or RV64 (sv39). The VexiiRiscv "linux"
            # variant itself defaults to RV32, so the width MUST be stated explicitly.
            _vex_args.cpu_variant = "linux"
            _vex_args.cpu_count   = cpu_count
            _vex_args.with_dma    = coherent_dma          # coherent AXI dma_bus
            _vex_args.l2_bytes    = int(l2_bytes) if l2_bytes else 0
            vexii_extra = " ".join(extra_scala_args) if extra_scala_args else ""
            # --xlen is a REAL knob on this path, not a NaxRiscv-only one. It used to be
            # hardcoded to 64 here, so `--cpu vexiiriscv --xlen 32` was accepted and
            # silently built an RV64 core  -  the same "flag that does nothing" defect the
            # --audio-interface-master check below refuses outright. Thread it through.
            _vex_args.vexii_args  = (f"--xlen={int(xlen)} " + vexii_extra).strip()
            # NEVER pull the pinned VexiiRiscv/SpinalHDL repos at build time:
            # the wrapper's `git checkout dev && git pull` dies the moment
            # upstream dev touches the locally-patched Soc.scala (2026-07-23:
            # upstream moved and killed 4 sweep launches on a clean bench).
            # The build is hash-pinned - updating is a deliberate manual step.
            _vex_args.update_repo = "no"
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
            # a pure config choice  -  a bigger L2 keeps the ring buffers + stack working set
            # out of DDR3 (each miss pays the full DRAM round trip on this 100 MHz core).
            if l2_bytes:
                _nax_args.l2_bytes = int(l2_bytes)
            # Hardware FPU. TWO things must happen and LiteX's --with-fpu only does the
            # first: (1) with_fpu sets the TOOLCHAIN arch/abi to rv64imafd / lp64d; (2) the
            # actual FP hardware is a NaxRiscv Scala-config option (gen.scala `arg("rvf")`
            # / `arg("rvd")`), enabled via --scala-args  -  WITHOUT this the softcore has NO
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

        # MAIN SoC BUS STANDARD. LiteX defaults this to "wishbone", and because we never
        # stated it, the control path ran AXI-Lite -> Wishbone -> AXI-Lite: the CPU pBus is
        # an AXILiteInterface and the milan_csr window at 0x9000_0000 is an AXILiteInterface,
        # with a Wishbone bus wedged between them purely by omission (build 0x0021 litex.log
        # lines 43 and 81: "cpu_bus0 Bus adapted from AXI-Lite 32-bit to Wishbone 32-bit" and
        # the same for milan_csr). Saying "axi-lite" deletes BOTH round-trip bridges - OOC
        # measured 106 LUT (AXILite2Wishbone) + 150 LUT (Wishbone2AXILite) on xc7a100t - and
        # turns the CSR bridge from Wishbone2CSR (48 LUT) into AXILite2CSR (66 LUT), +18.
        # This bus carries NO bulk traffic: with VexiiRiscv the CPU reaches DRAM on its own
        # 256-bit AXI4 mBus and the DMA masters live on the separate 64-bit AXI dma_bus, so
        # the only slaves here are rom / sram / spiflash / milan_csr / csr.
        kwargs.setdefault("bus_standard", bus_standard)

        # DERIVE the ident from the core that was actually selected. It used to say
        # "NaxRiscv" unconditionally, so every --cpu vexiiriscv build advertised the
        # wrong core over the BIOS banner and the ident CSR that bench operators read.
        _cpu_human = {"vexiiriscv": "VexiiRiscv", "naxriscv": "NaxRiscv"}[cpu]
        SoCCore.__init__(self, platform, sys_clk_freq,
                         ident=f"Milan TSN SoC - {_cpu_human} RV{xlen} {cpu_count}-core",
                         **kwargs)

        # item-4 TDM MASTER: the front-end generates the bus, so it needs a
        # clock at 2 x bclk = 2 x SLOTS x 32 x 48 kHz. Only a master build asks
        # for one, and only then does _CRG switch to the re-derived two-stage
        # plan (see its comment) - so every existing build's MMCM, and every
        # bench number measured through it, is untouched.
        if audio_if_master and not int(audio_if_slots):
            # REFUSE, do not ignore. A flag that is accepted and does nothing
            # is the p_AAF_PLAYBACK defect wearing a different hat: the build
            # succeeds, the argv records the intent, and the gateware is the
            # one you did not ask for. The stereo I2S front-end is already its
            # own clock master, so there is no coherent thing to do here.
            raise ValueError(
                "--audio-interface-master needs --audio-interface tdm8|tdm16|"
                "tdm32: the TDM bus role is only meaningful when a TDM "
                "front-end is elaborated (the I2S capture front-end is "
                "already an I2S clock master). milan_datapath refuses the "
                "same combination at elaboration.")
        audio_tdm_hz = (2 * int(audio_if_slots) * AUDIO_IF_WORD_BITS
                        * AUDIO_IF_FS_HZ) if (audio_if_master and
                                              int(audio_if_slots)) else None
        # HANDOVER 8.3b: a TDM8 master's serial clock is 24.576 MHz - the
        # audio MMCM's own contract rate. Reuse cd_audio directly: no CLKOUT1,
        # no cd_audio_tdm, no new closure surface, and plan A (with its
        # bench-measured DAC numbers) stays selected. Only TDM16/TDM32 need
        # the second output and plan B. The datapath still sees
        # AUDIO_IF_CLK_HZ_P = 24576000 and derives BCLK_HALF_P = 1 -> a
        # 12.288 MHz bclk, exactly.
        if audio_tdm_hz == 24_576_000:
            audio_tdm_hz = None
        self.crg = _CRG(platform, sys_clk_freq, with_dram=with_dram, with_eth=with_mac,
                        milan_clk_freq=milan_clk_freq, board=board,
                        audio_tdm_hz=audio_tdm_hz)

        # ---- DDR3 (LiteDRAM, A7DDRPHY)  -  migration §A.3. AX7101 = MT41J256M16
        # (512 MB, 2x16); Arty A7-100 = MT41K128M16 (256 MB, 1x16). ----
        if with_dram:
            from litedram.phy import s7ddrphy
            from litedram.modules import MT41J256M16, MT41K128M16
            self.ddrphy = s7ddrphy.A7DDRPHY(platform.request("ddram"),
                memtype        = "DDR3",
                nphases        = 4,
                sys_clk_freq   = sys_clk_freq,
                iodelay_clk_freq = 200e6)
            dram_module = (MT41K128M16 if board == "arty" else MT41J256M16)
            self.add_sdram("sdram",
                phy    = self.ddrphy,
                module = dram_module(sys_clk_freq, "1:4"),
                l2_cache_size = 8192)

        # ---- QSPI config flash (memory-mapped) + Linux flash-boot manifest ----
        # Maps the on-board N25Q128 (16 MB) into the CPU address space so the BIOS can
        # copy boot images straight from flash into DRAM (~10 MB/s quad) instead of the
        # ~4-min 1.5 Mbaud serial upload. `flashboot` selects which images live in flash
        # (see FLASHBOOT_MANIFESTS); the emitted MILAN_FLASHBOOT_* constants drive the
        # `linux_flashboot` BIOS method (sw/litex/patches/0001-milan-linux-flashboot.patch).
        if with_spiflash:
            from litespi.modules import N25Q128A13, S25FL128S
            from litespi.opcodes import SpiNorFlashOpCodes as SpiCodes
            # Arty A7-100: S25FL128S (16 MB, same geometry class as the N25Q128).
            # Same Alinx flashboot model: the flash holds the LINUX IMAGES with
            # the kernel at offset 0 (FLASHBOOT_LAYOUT transfers verbatim: slim
            # kernel + rootfs.cpio.xz + opensbi + dtb = 14 MB of 16), which is
            # MUTUALLY EXCLUSIVE with a bitstream in flash - flashing images
            # sacrifices the QSPI self-config; gateware is JTAG-SRAM loaded,
            # exactly like the AX7101. Same timing-robust single-lane recipe
            # (see the AX7101 rationale below); litespi's S25FL128S table only
            # lists plain READ_1_1_1 (0x03) on one lane - valid to 50 MHz on
            # this chip, and our effective SCK at sys 83.333 MHz is ~20.8 MHz.
            flash_module = (S25FL128S(SpiCodes.READ_1_1_1) if board == "arty"
                            else N25Q128A13(SpiCodes.READ_1_1_1_FAST))
            # Quad read (0x6B, 3-byte addr → whole 16 MB); mode="4x" drives all four DQ so
            # WP#/HOLD# are never floating. Micron 0x6B needs no quad-enable bit.
            # SINGLE-LANE fast read (0x0B, 1-1-1) + 25 MHz clock cap. At sys=112.5 MHz the
            # 4x QUAD read (0x6B) CRC-failed QSPI flashboot NON-DETERMINISTICALLY even after
            # the SCK cap (silicon 2026-07-08: got=685383e7 then 2eac15ab, expected constant)
            #  -  the sys-domain sampling of the four DQ lanes is marginal at the faster clock.
            # 1x drops 3 of the 4 DQ timing paths (only MISO), the most timing-robust MMAP
            # read; at 25 MHz SCK the sampling window is huge vs a 112.5 MHz sys. Flashboot
            # reads a few MB → still <1 s. Correct at ANY sys clock; 100 MHz builds unaffected.
            # 12.5 MHz requested => ~25 MHz effective SPI read clk (was 50 MHz at the
            # 25e6 request): doubles the sampling margin. build_hsq0's placement made
            # 50 MHz reads corrupt (CRC differs per read); r2slots was borderline-OK.
            self.add_spi_flash(mode="1x", module=flash_module,
                               clk_freq=int(12.5e6), with_master=True)
            # The BIOS boot-time auto-calibration (liblitespi spiflash_freq_init) re-tunes the
            # divisor UP from this default as long as a short CRC test block reads stably  -  on
            # this board it locked div=2 (50 MHz) and the marginality only shows on MB-scale
            # reads (silicon 2026-07-10: opensbi+dtb copied fine, then the kernel FBI length
            # word read as garbage). The divisor the gateware was built for is the one with
            # margin; skip the calibration so it actually holds.
            self.add_constant("SPIFLASH_SKIP_FREQ_INIT")
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
            # item-7: playback needs the DMA (the PCM-ring read master lives in
            # MilanDMA); silently no-op it without --with-dma/--full.
            aaf_pb = bool(aaf_playback) and with_dma
            if aaf_playback and not with_dma:
                print("[milan] --aaf-playback ignored without --with-dma/--full")
            if with_dma:
                self.milan_dma = MilanDMA(self, data_width=64, milan_cd=milan_cd,
                                          rx_queues=rx_queues, rx_rsc=rx_rsc,
                                          hs_page_bytes=hs_page_bytes,
                                          legacy_ring=legacy_ring,
                                          rx_fifo_beats=rx_fifo_beats,
                                          num_streams=int(num_streams),
                                          pcm_ring=pcm_ring, aaf_playback=aaf_pb,
                                          talker_wire_chans=int(talker_wire_chans),
                                          aaf_pb_streams=int(aaf_pb_streams))
                dp_ports.update(self.milan_dma.dp_ports)
            if with_mac:
                self.milan_mac = MilanMAC(platform, data_width=64, milan_cd=milan_cd,
                                          gtx_tx_invert=gtx_tx_invert,
                                          phy_index=eth_phy_index,
                                          phy_model=("mii" if board == "arty" else "gmii"),
                                          rgmii_tx_delay=rgmii_tx_delay,
                                          rgmii_rx_delay=rgmii_rx_delay)
                dp_ports.update(self.milan_mac.dp_ports)
            # Pipeline telemetry (memory-mapped): frame/beat/stall counts at every TX+RX
            # AXIS stage + GMII wire counts + datapath occupancy/latency + gPTP counters,
            # all coherently snapshot-latched by one `capture` write. Needs both engines.
            # --strip-probes drops the whole block (area-70 lever #2: every counter is
            # 32 FFs + a capture shadow + increment logic  -  thousands of LUTs across
            # ~40 probes). The kl-eth driver probes tlm presence and tolerates absence
            # ("optional (absent on minimal gateware)"); dev/forensics builds keep it.
            if with_dma and with_mac and not strip_probes:
                # Phase-0 reader instrumentation (TX_READER_PREFETCH_PLAN.md App. A): measure
                # L, the starve breakdown, and the outstanding-depth proxy BEFORE any prefetch
                # RTL. Added via MilanDebug's extra hook so it's one closure, trivially dropped.
                def _phase0(dbg):
                    dbg.rd_latency_probe("txrd_lat", self.milan_dma.tx,
                                         "TX reader AR->firstR latency")
                    dbg.rd_produce_probe("txrd", self.milan_dma.tx,
                                         "TX reader produce/starve breakdown")
                    dbg.outstanding_hi_probe("rxw_out", self.milan_dma.rx,
                                             "RX writer outstanding")
                    if hasattr(self.milan_dma, "rx1"):
                        dbg.outstanding_hi_probe("rx1w_out", self.milan_dma.rx1,
                                                 "RX1 writer outstanding")
                    # ---- M1 (CAMPAIGN_500_PLAN): the probes the >500 phases gate on ----
                    # RSC close reasons + coalesce ratio (free-running; read as deltas)
                    for tag, sig, d in (
                        ("rsc_close_psh",  self.milan_dma.rx.dbg_close_psh,  "aggregate closes: PSH"),
                        ("rsc_close_cap",  self.milan_dma.rx.dbg_close_cap,  "aggregate closes: seg-cap 16"),
                        ("rsc_close_tout", self.milan_dma.rx.dbg_close_tout, "aggregate closes: idle timeout"),
                        ("rsc_close_park", self.milan_dma.rx.dbg_close_park, "aggregate closes: parked newcomer/mack"),
                        ("rsc_v2_cnt",     self.milan_dma.rx.dbg_v2_cnt,     "v2 aggregate BDs written"),
                        ("rsc_v2_segs",    self.milan_dma.rx.dbg_v2_segs,    "sum of segs over v2 BDs (ratio = segs/cnt)"),
                    ):
                        dbg._snap(sig, 32, tag, f"{d} (q0, free-running)")
                    # TX-side CPU-feed evidence: ring occupancy high-water + doorbells
                    dbg.hiwater_probe("txring_occ", self.milan_dma.tx.dbg_occ, 32,
                                      "TX ring/BD bytes queued-unconsumed, max since reset")
                    dbg.pulse_count_probe("tx_doorbells", self.milan_dma.tx.dbg_doorbell,
                                          "TX wr_ptr CSR writes (frames/doorbell = batching)")
                    # RX queue-1 stage probe + steer output stalls (fan-out attribution)
                    if hasattr(self.milan_dma, "rx1"):
                        dbg.sys_probe("rx1_dma", self.milan_dma.rx1.sink,
                                      "RX q1: steer -> DMA write")
                    if hasattr(self.milan_dma, "steer"):
                        dbg.sys_probe("steer0", self.milan_dma.steer.source0,
                                      "RxSteer q0 output")
                        dbg.sys_probe("steer1", self.milan_dma.steer.source1,
                                      "RxSteer q1 output")
                    # R2 multi-slot RSC: the two new close reasons (appended LAST so
                    # every earlier probe keeps its snapshot address)
                    for tag, sig, d in (
                        ("rsc_close_age", self.milan_dma.rx.dbg_close_age,
                         "aggregate closes: lifetime cap (rsc_agemax)"),
                        ("rsc_close_prs", self.milan_dma.rx.dbg_close_prs,
                         "aggregate closes: CQ pressure (head-of-line)"),
                    ):
                        dbg._snap(sig, 32, tag, f"{d} (q0, free-running)")
                self.milan_tlm = MilanDebug(self.milan_dma, self.milan_mac, extra=_phase0)
            # audio-MMCM servo boundary: the real MMCME2_ADV DRP/PS wiring
            # (KL_mmcm_drp_servo inside milan_datapath <-> _CRG mmcm_audio)
            if hasattr(self.crg, "audio_mmcm_rst"):
                mmcm_ports = dict(
                    i_i_ps_clk         = self.crg.audio_ps_clk,
                    o_o_mmcm_drp_addr  = self.crg.audio_drp_addr,
                    o_o_mmcm_drp_en    = self.crg.audio_drp_en,
                    o_o_mmcm_drp_we    = self.crg.audio_drp_we,
                    o_o_mmcm_drp_di    = self.crg.audio_drp_di,
                    i_i_mmcm_drp_do    = self.crg.audio_drp_do,
                    i_i_mmcm_drp_rdy   = self.crg.audio_drp_rdy,
                    o_o_mmcm_rst       = self.crg.audio_mmcm_rst,
                    i_i_mmcm_locked    = self.crg.audio_mmcm_locked,
                    o_o_mmcm_ps_en     = self.crg.audio_ps_en,
                    o_o_mmcm_ps_incdec = self.crg.audio_ps_incdec,
                    i_i_mmcm_ps_done   = self.crg.audio_ps_done,
                )
                dp_ports = dict(dp_ports or {}, **mmcm_ports)
            # ---- item-4 TDM MASTER: the header, and the clock that drives it ----
            # THE WHOLE POINT OF THE MASTER ROLE. A SLAVE build leaves
            # i_tdm_bclk_i/i_tdm_fsync_i at 0 (see add_milan_datapath), so its
            # fsync never toggles, KL_tdm_capture yields no pairs and every
            # talker built on it emits NO FRAME AT ALL - which is why
            # endstation_builder.interface_is_placeholder() withholds
            # --audio-interface for a slave. A MASTER drives them itself, so
            # the front-end is real the moment the clock exists; the PADS then
            # decide whether it captures audio or digital silence, exactly the
            # distinction check_wire_accountability.py draws for the AX7101's
            # pmoda-less I2S front-end (i_i2s_sdout_i = 0 -> one pair of
            # silence, still one FED pair).
            self.tdm_pads = None
            # The I2S pads belong to MilanDMA (it requests the Pmod I2S2);
            # the SoC has none of its own. getattr, not self.i2s_pads: a
            # migen Module raises AttributeError for names never assigned,
            # and on a board with NO i2s front-end (the AX7101 tdm32 master
            # build) nothing assigns one - the first elaboration of that
            # path died exactly here on 2026-07-28. Hoisted above the master
            # branch because the blend kwarg below reads it on EVERY build.
            _dma_i2s = getattr(getattr(self, "milan_dma", None),
                               "i2s_pads", None)
            if audio_if_master and int(audio_if_slots):
                # `loose=True` returns None when the platform declares no
                # `tdm` resource (the Arty today) instead of raising, so a
                # board without the header still elaborates - the same
                # tolerance i2s_pads has, and NOT a try/except: an absent pin
                # only asserts at constraint RESOLUTION, far outside any
                # except here (the AX7101 'pmoda' elaboration break,
                # 2026-07-13).
                self.tdm_pads = platform.request("tdm", loose=True)
                dp_ports.update(
                    # TDM8 divides the audio clock itself (no cd_audio_tdm -
                    # see the audio_tdm_hz note above); TDM16/32 get the
                    # dedicated MMCM output
                    i_clk_tdm_i   = ClockSignal("audio_tdm" if audio_tdm_hz
                                                else "audio"),
                    o_tdm_bclk_o  = (self.tdm_pads.bclk if self.tdm_pads
                                     else Signal()),
                    o_tdm_fsync_o = (self.tdm_pads.fsync if self.tdm_pads
                                     else Signal()),
                    i_tdm_data_i  = (self.tdm_pads.din if self.tdm_pads else 0),
                    o_tdm_dout_o  = (self.tdm_pads.dout if self.tdm_pads
                                     else Signal()),
                    # milan_datapath routes the TDM master's MCLK out of
                    # i2s_mclk_o (one pin serves both front-ends; a TDM build
                    # parks i2s_sclk/lrck), so on a master build that pin IS
                    # the TDM MCLK - override MilanDMA's I2S-Pmod binding.
                    o_i2s_mclk_o  = (self.tdm_pads.mclk if self.tdm_pads
                                     else Signal()),
                )
                if self.tdm_pads is not None and _dma_i2s is not None:
                    # HANDOVER 8.3b blend (the Arty): BOTH front-ends are
                    # real, so the override above is itself overridden -
                    # o_i2s_mclk_o goes BACK to the Pmod I2S2 (pmoda:4, D13,
                    # the CS5343 - the pin that must not move) and the TDM
                    # header gets the master's mclk on its OWN pad. The
                    # datapath blends the pair streams (KL_pair_blend, I2S =
                    # pair slot 0).
                    dp_ports["o_i2s_mclk_o"] = _dma_i2s[0]
                    dp_ports["o_tdm_mclk_o"] = self.tdm_pads.mclk
                if self.tdm_pads is None:
                    print("[milan] --audio-interface-master: no `tdm` pads on "
                          "this platform - bclk/fsync/dout float and the "
                          "capture front-end frames DIGITAL SILENCE at the "
                          "declared width")
            self.milan = MilanNIC(platform, axil, dma_mac_ports=dp_ports or None,
                                  milan_cd=milan_cd,
                                  rx_irq=self.milan_dma.rx.non_empty if with_dma else None,
                                  rx1_irq=(self.milan_dma.rx1.non_empty
                                           if (with_dma and rx_queues >= 2) else None),
                                  milan_clk_hz=int(milan_clk_freq or sys_clk_freq),
                                  num_streams=int(num_streams),
                                  audio_if_slots=int(audio_if_slots),
                                  talker_wire_chans=int(talker_wire_chans),
                                  audio_if_master=bool(audio_if_master),
                                  # 8.3b blend: on only when the board routes
                                  # BOTH the I2S Pmod and a tdm header (the
                                  # same _dma_i2s the mclk rebind used - the
                                  # pads are MilanDMA's, and a padless board
                                  # never assigns them)
                                  audio_if_i2s_pair=(self.tdm_pads is not None
                                                     and _dma_i2s is not None),
                                  aaf_playback=aaf_pb,
                                  aaf_pb_streams=int(aaf_pb_streams),
                                  loopback_lane=bool(loopback_lane),
                                  render_lpf=bool(render_lpf),
                                  optional_blocks=optional_blocks,
                                  cbs_queues_mask=cbs_queues_mask,
                                  entity_gen_dir=entity_gen_dir)
            self.irq.add("milan", use_loc_if_exists=True)  # 4 lines -> CPU via EventManager
            # Milan IDENTIFY -> board LED (controllers blink it to locate the
            # device). Skipped quietly on platforms without user_led pads.
            try:
                self.comb += platform.request("user_led", 0).eq(self.milan.identify)
            except Exception:
                print("[milan] no user_led pad - IDENTIFY LED not wired")

    def _add_flashboot_constants(self, manifest_name):
        """Emit the MILAN_FLASHBOOT_* BIOS constants for the chosen flash manifest.

        `linux_flashboot` (the patched BIOS boot method) reads, for each image in the
        manifest, `MILAN_FLASHBOOT_<IMG>_OFFSET/_ADDR` and copies it from the memory-mapped
        flash (`SPIFLASH_BASE + OFFSET`) into DRAM. If the manifest is *complete* (holds the
        whole boot set) it also emits `MILAN_FLASHBOOT_COMPLETE`, so the BIOS boots OpenSBI
        straight from flash with no serial upload; otherwise it pre-loads what it has and
        falls through to serialboot for the rest. The constants are inert (#defines nobody
        reads) unless the BIOS patch is applied  -  so building with --with-spiflash is safe
        either way. The layout is stored for deploy.sh in `_flashboot_layout` (written to
        <build>/flashboot_layout.json by main()), keeping gateware and flashing in lock-step.
        """
        # A build must never emit a flash map that cannot be erased safely.
        problems = check_flash_map()
        if problems:
            raise ValueError("FLASHBOOT flash map is inconsistent:\n  " +
                             "\n  ".join(problems))

        images = FLASHBOOT_MANIFESTS[manifest_name]
        self._flashboot_layout = {"manifest": manifest_name, "entry": FLASHBOOT_ENTRY,
                                  "complete": images == FLASHBOOT_MANIFESTS["full"],
                                  "flash_size": FLASH_SIZE,
                                  "erase_block": FLASH_ERASE_BLOCK,
                                  "images": [],
                                  # deploy.sh does not read this key; it is here
                                  # so the writable slots are visible to anything
                                  # that consumes the layout json (see the OPEN
                                  # ITEM note at FLASHBOOT_RESERVED).
                                  "reserved": [
                                      {"name": n, "offset": e["offset"],
                                       "size": e["size"]}
                                      for n, e in sorted(
                                          FLASHBOOT_RESERVED.items(),
                                          key=lambda kv: kv[1]["offset"])]}
        # The writable slots exist independently of the boot manifest, so their
        # constants are emitted even for manifest "none": a daemon looking for
        # /user or the journal must not have to know how the box was booted.
        for name, e in FLASHBOOT_RESERVED.items():
            self.add_constant(f"MILAN_FLASH_{name.upper()}_OFFSET", e["offset"])
            self.add_constant(f"MILAN_FLASH_{name.upper()}_SIZE",   e["size"])
        if not images:
            return
        # the gateware slot is not a BIOS-copied image, but deploy.sh needs it
        # in the json for slot ceilings + `flash` targeting
        eb = FLASHBOOT_LAYOUT["bitstream"]
        self._flashboot_layout["images"].append(
            {"name": "bitstream", "offset": eb["offset"], "addr": eb["addr"],
             "budget": eb["size"]})
        for name in images:
            e = FLASHBOOT_LAYOUT[name]
            self.add_constant(f"MILAN_FLASHBOOT_{name.upper()}_OFFSET", e["offset"])
            self.add_constant(f"MILAN_FLASHBOOT_{name.upper()}_ADDR",   e["addr"])
            self.add_constant(f"MILAN_FLASHBOOT_{name.upper()}_SIZE",   e["size"])
            self._flashboot_layout["images"].append(
                {"name": name, "offset": e["offset"], "addr": e["addr"],
                 "budget": e["size"]})
        self.add_constant("MILAN_FLASHBOOT_ENTRY", FLASHBOOT_ENTRY)
        if self._flashboot_layout["complete"]:
            self.add_constant("MILAN_FLASHBOOT_COMPLETE")  # zero-upload full boot


# Build --------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Milan single-core RISC-V Linux SoC")
    ap.add_argument("--xlen", default=64, type=int, choices=[32, 64],
                    help="CPU register width, honoured by BOTH --cpu choices "
                         "(64 = RV64/sv39 default; 32 = RV32/sv32)")
    ap.add_argument("--cpu-count",    default=1, type=int, help="number of cores (this config: 1)")
    ap.add_argument("--cpu",          default="naxriscv", choices=["naxriscv","vexiiriscv"], help="soft CPU (vexiiriscv = higher fmax, smaller  -  AVB-switch direction)")
    ap.add_argument("--with-fpu",     action="store_true", help="hardware FP unit (rv64imafd / lp64d)")
    ap.add_argument("--scala-args",   action="append", default=[], help="extra NaxRiscv scala args, e.g. alu-count=1,decode-count=1 (append)")
    ap.add_argument("--sys-clk-freq", default=100e6, type=float)
    ap.add_argument("--rx-queues", default=1, type=int,
                    help="RX DMA queues (2 = flow-steered fan-out for parallel ACK/recv on 2 harts)")
    ap.add_argument("--no-rx-rsc", action="store_true",
                    help="AREA LEVER (rxq2-sans-RSC): elaborate OUT the RSC "
                         "coalescing engine from EVERY RX queue writer - header "
                         "parse regfile, 4-slot aggregate state, ACK-run merge, "
                         "append rotator, header-split states - while KEEPING "
                         "the 2-queue steering front-end (the D7 gPTP fix) and "
                         "the whole CSR map (RSC/hs registers stay, inert). "
                         "Every BD is then a v1 single frame, the path all "
                         "non-TCP traffic takes today, so a deployed kl-eth "
                         "(rsc=1 default) runs unmodified: coalescing simply "
                         "never kicks in and SW GRO takes over (expect the "
                         "pre-RSC ~43 Mbit/s TCP RX regime; AVTP/gPTP/UDP are "
                         "unaffected). Default off => engine PRESENT, build "
                         "byte-identical.")
    ap.add_argument("--hs-page-bytes", default=4096, type=lambda x: int(x, 0),
                    help="posted-page size the hs crossing arithmetic assumes (power of 2; "
                         "16384 = 4x burst absorbency, pairs STRICTLY with kl-eth hsplit12 "
                         "hs_pgsz=16384)")
    ap.add_argument("--strip-probes", action="store_true",
                    help="drop the MilanDebug telemetry block (tlm CSRs @0xf0004000+ incl. "
                         "Phase-0/M1 probes)  -  the area-70 ship-build diet; kl-eth handles "
                         "the absence. Keep probes on dev/forensics builds.")
    ap.add_argument("--board", default="ax7101", choices=["ax7101", "arty"],
                    help="target board: ax7101 (Alinx, 1G GMII, QSPI flashboot) or "
                         "arty (Digilent Arty A7-100: 100M MII DP83848, serial boot, "
                         "second Milan node for AVDECC interop).")
    ap.add_argument("--rx-fifo-beats", default=2048, type=float,
                    help="store-and-forward ingress FIFO depth per RX queue, beats "
                         "(2048 = 16KB = 4 RAMB36/queue). AREA-70 staged diet: 1024; "
                         "gate on silicon drop counters under the P4/P8 cells.")
    ap.add_argument("--legacy-ring", action="store_true",
                    help="elaborate the legacy byte-ring DMA fallback (bd_base==0 ABI) back "
                         "in. DEFAULT IS FOLDED OUT (AREA-70): shape muxes hardwire to the "
                         "BD arm and the ring dispatch/commit arms are not generated; an "
                         "unarmed engine parks (counted drops), never DMA via base/addr 0. "
                         "Only the kl-eth bd=0 A/B forensics lever needs this flag.")
    ap.add_argument("--l2-bytes", default=None, type=float,
                    help="NaxRiscv shared-L2 size in bytes (default 128 KiB; IPC knob I1).")
    ap.add_argument("--milan-clk-freq", default=None, type=float,
                    help="run the Milan datapath in its own slower clock domain (Hz, e.g. "
                         "50e6), async-FIFO CDC'd to sys on the AXI-Lite CSR bus and the "
                         "DMA/MAC AXIS boundary  -  lifts the dense datapath off the 100 MHz "
                         "sys critical path (it still exceeds 1 GbE). Works with --full.")
    ap.add_argument("--num-streams", default=1, type=int,
                    help="NxN dataplane width (docs/NXN_ARCHITECTURE.md P0): AAF stream "
                         "contexts per shared engine (milan_datapath N_STREAMS). The "
                         "builder emits this from the config's streams section; default "
                         "1 = today's bit-compatible single-stream shape.")
    ap.add_argument("--pcm-ring", default="dram", choices=("dram", "bram"),
                    help="Milan listener PCM ring backend. 'dram' (default) = the LiteDRAM "
                         "WishboneDMAWriter ring (unchanged). 'bram' = the on-chip dual-port "
                         "BRAM ring (KL_pcm_ring_bram): single-cycle writes, sink.ready "
                         "constant 1, so no beat can ever be shed (kills mf52 SHED + I6 at "
                         "root). CPU mmaps MILAN_PCM_BRAM_BASE (0x9010_0000); the pcm CSR ABI "
                         "is unchanged. ~8 RAMB36.")
    ap.add_argument("--no-render-lpf", action="store_true",
                    help="AREA LEVER (banked, docs/NXN_ARCHITECTURE.md 6.2): prune "
                         "KL_pcm_lpf, the 2nd-order Butterworth on the DAC render tap. "
                         "Vivado place report of the shipping 8x8 bitstream prices it at "
                         "428 LUT / 756 FF / 0 DSP. The pruned datapath behaves exactly "
                         "like a shipped one with LPF_CTRL[0]=0 (raw AXIS to the DAC), so "
                         "no digital acceptance surface moves - but the analog loop THD+N "
                         "record was measured THROUGH the filter and must be re-measured "
                         "before it is quoted against a pruned bitstream. Default off "
                         "=> filter PRESENT, build byte-identical.")
    # ---- docs/design/AREA_BUDGET.md tier-1 optional-block prunes ----
    # One --no-<block> flag per row of MILAN_OPTIONAL_BLOCKS. EVERY ONE
    # DEFAULTS OFF, i.e. the block is PRESENT and the generated top is
    # byte-identical to today's; the flag only exists so a deployment that
    # cannot use a block can say so and get the LUTs back. Figures are yosys
    # ESTIMATES from syn/yosys/ooc.sh on the 8x8 ship shape (measured
    # 2026-07-27), not placement results.
    ap.add_argument("--no-media-clock-servo", action="store_true",
                    help="AREA LEVER: prune KL_mmcm_drp_servo (the audio-MMCM "
                         "media-clock actuator). Legal ONLY when the media clock is "
                         "INTERNAL - the servo is what disciplines the MMCM to a "
                         "recovered CRF or input-stream clock, so a pruned build "
                         "cannot slave to a remote grandmaster's media clock at all. "
                         "A_MCSRV_STAT 0x8F8 then reads 0 STRUCTURALLY. Default off "
                         "=> servo PRESENT.")
    ap.add_argument("--no-latency-taps", action="store_true",
                    help="AREA LEVER: prune KL_aaf_latency_taps. Pure instrumentation "
                         "- nothing in the media path reads a tap - so no acceptance "
                         "surface moves, but the whole LTAP CSR window 0x870-0x8B0 "
                         "reads 0 and every number in docs/AAF_LATENCY_TAPS.md becomes "
                         "unreproducible on the resulting bitstream. Default off "
                         "=> taps PRESENT.")
    ap.add_argument("--no-maap", action="store_true",
                    help="AREA LEVER: prune KL_maap (IEEE 1722 Annex B dynamic stream "
                         "DMAC allocation). Legal when stream destination addresses are "
                         "STATICALLY provisioned (AAF_DMAC / the builder's "
                         "srp.stream_dmac_base). MAAP_CTRL.en becomes effectively "
                         "reserved: setting it would pin AAF admission shut, because "
                         "the claim can never complete. Default off => MAAP PRESENT.")
    ap.add_argument("--no-i2s-playback", action="store_true",
                    help="AREA LEVER: prune KL_i2s_playback (the DAC serializer + its "
                         "rate servo). For a board with no DAC: the four i2s_dac_* pins "
                         "park at 0 and the I2SPB CSR group reads 0. Also stops "
                         "i2spb_converged, so an EXTERNAL media clock never reports "
                         "converged (consistent - there is no render device to "
                         "converge). Default off => playback PRESENT.")
    ap.add_argument("--entity-gen-dir", default=None,
                    help="resolve the generated entity definition "
                         "(gen/adp_shape_defaults.svh + aecp_aem_rom.svh) from "
                         "this directory (a configs/generated/<cfg>/ tree) "
                         "instead of the tracked hdl/ copy - lets both boards' "
                         "sweeps build CONCURRENTLY from one tree with no "
                         "svh-ownership handoff")
    ap.add_argument("--cbs-queues-mask", type=lambda x: int(x, 0), default=None,
                    help="AREA LEVER: which egress queues get a credit_based_shaper "
                         "INSTANCE (bit i = queue i). A masked-out queue is strict-"
                         "priority only - bit-identical to a built CBS whose runtime "
                         "cbs_shaped_i is 0, which is how every non-SR queue runs "
                         "today; its cbs_* CSR words stay and read back as written. "
                         "The builder derives this from srp.class_queue (the SR "
                         "classes keep CBS). Default None = all queues, the "
                         "pre-2026-07-28 build, byte-identical.")
    ap.add_argument("--no-datapath-probes", action="store_true",
                    help="AREA LEVER: prune the APRB (0x8B4-0x8C4) and PBK "
                         "(0x8C8-0x8D0) probe groups - closed-finding "
                         "diagnostics; the range reads 0 on a pruned build "
                         "(the LTAP precedent). Default off => probes PRESENT.")
    ap.add_argument("--no-rx-mac-filter", action="store_true",
                    help="AREA LEVER: prune rx_mac_filter + its TCAM. The RX stream "
                         "becomes a straight wire to the DMA port, which is bit-exactly "
                         "what the filter does with promisc=1 - so this is legal only "
                         "when the port is meant to be PROMISCUOUS or filtering is done "
                         "in software. The TCAM_* CSR window still accepts writes and "
                         "nothing reads them. Default off => filter PRESENT.")
    ap.add_argument("--aaf-playback", action="store_true",
                    help="item-7 ALSA playback: wire KL_pcm_tx (host PCM ring -> AAF "
                         "talker pair source) into milan_datapath, the TX mirror of the RX "
                         "PCM ring. Software writes S32BE PCM to a DRAM ring + bumps a wr_ptr "
                         "doorbell; while PB_CTRL.enable is set KL_pcm_tx feeds the packetizer "
                         "in place of the ADC front-end. Needs --with-dma/--full. Default off "
                         "=> byte-identical build.")
    ap.add_argument("--aaf-playback-streams", type=int, default=1,
                    help="task #31 START-SMALL: how many host playback RINGS "
                         "KL_pcm_tx serves (1..num-streams). One 8ch ring already "
                         "reaches every wire channel through the 64ch chmap; the "
                         "full-N engine OOC'd 2216 LUT at 8x8x8. Drives BOTH "
                         "AAF_PB_STREAMS_P and the pb CSR sizing (one value, two "
                         "consumers - never restated). Only with --aaf-playback.")
    ap.add_argument("--loopback-lane", action="store_true",
                    help="task #65: wire KL_chan_map_capture's rx -> talker LOOPBACK "
                         "bucket (SRC_LOOP = 5) to the depacketizer payload clone, so a "
                         "talker slot naming a loopback AUDIO_CLUSTER really carries that "
                         "RECEIVED channel pair. This is what makes the entity's declared "
                         "loopback clusters true; without it they select silence. NOT free: "
                         "+2303 LUT / +1542 FF OOC at the 8x8 shape (32 pair holds x 48 b "
                         "that cannot be LUTRAM - the bank takes a reset and two writes per "
                         "beat). Default off => no parameter passed, so the top .v is "
                         "byte-identical. The endstation config "
                         "declares it (cluster_mapping.fabric.loopback_lane) so the AEM's "
                         "power-on map and this flag can never disagree.")
    ap.add_argument("--audio-interface", default="i2s_philips",
                    choices=("i2s_philips", "tdm8", "tdm16", "tdm32"),
                    help="item-4 audio-interface family: capture front-end generate "
                         "select (milan_datapath AUDIO_IF_SLOTS_P). i2s_philips (default) "
                         "= the stereo I2S master front-end, bit-identical to the shipping "
                         "build; tdmN = the KL_tdm_capture N-slot TDM slave (the builder "
                         "emits this from audio_interface.kind).")
    ap.add_argument("--audio-interface-master", action="store_true",
                    help="item-4: be the TDM bus MASTER (milan_datapath "
                         "AUDIO_IF_MASTER_P -> KL_tdm_capture_master). The "
                         "fabric GENERATES bclk/fsync instead of waiting for a "
                         "codec to drive them, which is the difference between "
                         "a declared interface and one the wire-accountability "
                         "gate can count: with --audio-interface tdmN alone the "
                         "SLAVE's fsync never toggles (the SoC ties it to 0) so "
                         "the front-end yields no pairs and every talker is "
                         "silent. Needs --audio-interface tdmN. Adds a second "
                         "audio MMCM output at 2 x SLOTS x 32 x 48 kHz "
                         "(TDM8 24.576 / TDM16 49.152 / TDM32 98.304 MHz) and "
                         "re-derives the two-stage integer clock plan so one "
                         "VCO serves it and the 24.576 MHz CRF/DAC clock; the "
                         "audio clock's error IMPROVES from -10.6 to -0.66 ppm. "
                         "Default off => byte-identical build.")
    ap.add_argument("--talker-wire-chans", default=2, type=int,
                    help="item-00 WIRE CHANNEL CONSTANT: channels_per_frame the AAF "
                         "framer emits per talker (milan_datapath TALKER_WIRE_CHANS_P, "
                         "even 2..8). This is what the fabric PUTS ON THE WIRE, not what "
                         "the entity advertises - milan_datapath refuses at elaboration "
                         "any width the capture front-end selected by --audio-interface "
                         "cannot feed, so raising it requires raising the framer (roadmap "
                         "item 5). Default 2 = today's stereo framer, byte-identical.")
    ap.add_argument("--main-ram-size", default=0x8000, type=lambda x: int(x, 0),
                    help="integrated main RAM size (bytes)")
    ap.add_argument("--no-milan", action="store_true", help="bare SoC, no NIC (bring-up smoke test)")
    ap.add_argument("--with-mac", action="store_true",
                    help="attach the 1G MAC + RGMII PHY (§A.7) at the datapath MAC boundary")
    ap.add_argument("--with-dma", action="store_true",
                    help="attach the AXIS<->memory DMA engines (§A.6) with simple-mode CSRs")
    ap.add_argument("--with-dram", action="store_true",
                    help="512 MB DDR3 via LiteDRAM (A7DDRPHY + MT41J256M16)  -  needed for Linux (§A.3)")
    ap.add_argument("--coherent-dma", action="store_true",
                    help="cache-coherent DMA (NaxRiscv snooping dma_bus; needed for correct DMA content without manual cache flushes)")
    ap.add_argument("--bus-standard", default="wishbone", choices=["wishbone", "axi-lite"],
                    help="main SoC bus standard. 'axi-lite' makes the control path AXI end "
                         "to end and deletes the two round-trip bridges LiteX inserts when "
                         "the default 'wishbone' sits between the CPU's AXI-Lite pBus and "
                         "the AXI-Lite milan_csr window (OOC: 106 + 150 LUT, minus 18 for "
                         "AXILite2CSR over Wishbone2CSR). Carries no DRAM or DMA traffic.")
    ap.add_argument("--with-spiflash", action="store_true",
                    help="memory-map the on-board N25Q128 QSPI flash (16 MB) so the BIOS can "
                         "flash-boot Linux images instead of the ~4-min serial upload (§QSPI). "
                         "Included by --all-blocks.")
    ap.add_argument("--flashboot", default="kernel", choices=["none", "kernel", "full"],
                    help="which boot images live in flash (needs --with-spiflash): 'kernel' "
                         "(default) pre-loads the 14 MB kernel from flash and serial-uploads "
                         "the rest (~60%% faster); 'full' flash-boots everything with zero "
                         "upload (only fits with a slimmed <6.5 MB kernel  -  see "
                         "docs/integration/QSPI_FLASHBOOT.md); 'none' maps the flash but adds no boot method.")
    ap.add_argument("--all-blocks", "--full", dest="all_blocks", action="store_true",
                    help="enable ALL fabric blocks: NIC + DMA + MAC + DDR3 (= --with-dma "
                         "--with-mac --with-dram). This means 'every block instantiated', NOT "
                         "a complete/validated NIC  -  MDIO/PHY mgmt, the kl-eth driver, DMA "
                         "scatter-gather, and on-hardware traffic (M-A3..M-A5) are still open. "
                         "(--full is a legacy alias for this flag.)")
    ap.add_argument("--eth-port", default="e1", choices=["e1", "e2"],
                    help="AX7101 PHY port: e1 (default) or e2 — the e1-GMII-RX "
                         "hardware-fault fallback (2026-07-22); both are 8-bit GMII")
    ap.add_argument("--gtx-tx-invert", action="store_true",
                    help="forward GMII gtx_clk 180° out of phase with TXD so the PHY samples "
                         "mid-bit  -  the fix for the marginal GMII-TX setup/hold at the RTL8211E "
                         "(docs/kl-eth-tx-debug §GMII-TX). Default off = edge-aligned (upstream).")
    ap.add_argument("--rgmii-tx-delay", default=2e-9, type=float,
                    help="RGMII MAC-side TX clock delay, seconds (default 2e-9).")
    ap.add_argument("--rgmii-rx-delay", default=0e-9, type=float,
                    help="RGMII MAC-side RX IDELAY, seconds (default 0  -  the AX7101 PHY uses "
                         "RX-clock inversion, not IDELAY, to centre sampling; see milan_rgmii.py).")
    ap.add_argument("--uart-baudrate", default=115200, type=int,
                    help="console UART baud (default 115200; the AX7101 factory demo uses 9600)")
    ap.add_argument("--build", action="store_true", help="run vendor P&R (needs Artix-7 in Vivado)")
    ap.add_argument("--load",  action="store_true", help="program the board over JTAG (openFPGALoader -c ft232)")
    ap.add_argument("--vivado-max-threads", type=int, default=min(os.cpu_count() or 1, 32),
                    help="max Vivado synth/place/route threads (set_param general.maxThreads; Vivado caps at 32)")
    ap.add_argument("--place-directive", default=None,
                    help="override the Vivado place directive (e.g. AltSpreadLogic_high "
                         "to relieve congestion on a route-dominated critical path).")
    ap.add_argument("--synth-directive", default=None,
                    help="override the Vivado synth_design directive (e.g. "
                         "AreaOptimized_high for the AREA-70 density flow).")
    ap.add_argument("--opt-directive", default=None,
                    help="override the Vivado opt_design directive (e.g. ExploreArea).")
    ap.add_argument("--route-directive", default=None,
                    help="override the Vivado route_design directive (e.g. "
                         "AlternateCLBRouting when routing dies on node overlaps "
                         "at high fill; --timing-opt alone pins AggressiveExplore).")
    ap.add_argument("--area-flow", action="store_true",
                    help="AREA-70 density flow: synth AreaOptimized_high + opt "
                         "ExploreArea + a second opt_design -control_set_merge "
                         "-merge_equivalent_drivers pass before placement. The slice "
                         "binder is packing density, not LUT count (cbse_spr: 71.2 "
                         "percent LUTs but 94.85 percent slices at 75 percent fill).")
    ap.add_argument("--timing-opt", action="store_true",
                    help="aggressive Vivado place/route/phys-opt directives to squeeze out "
                         "the last ns of setup slack (slower P&R; use when WNS is marginally "
                         "negative, e.g. the 100 MHz --full CBS path)")
    ap.add_argument("--floorplan", action="store_true",
                    help="attempt to attack the 100 MHz critical path (sys_rst, fanout ~3900, "
                         "8.9 ns route, 0 logic levels) for a higher sys clock. NOTE: reset "
                         "replication does NOT work here  -  Vivado protects the reset control set "
                         "(DONT_TOUCH on the synchronizer clock), so the RTL max_fanout attr this "
                         "sets AND the forced phys_opt both leave sys_rst at fo~3969. The real fix "
                         "is a multicycle/false-path on the reset, not this flag; the clock itself "
                         "is set via --sys-clk-freq. See docs/findings/LATENCY_INVESTIGATION.md §8.")
    builder_args(ap)
    args = ap.parse_args()

    # ---- L1 BINDING REFUSAL: the board must ROUTE the front-end it is asked
    #      for. BEFORE the platform is built, so an unbackable request is a
    #      BUILD FAILURE and never a bitstream.
    #
    #      `--audio-interface tdmN` selects a capture front-end in
    #      milan_datapath; whether that front-end reaches a pin is a property of
    #      the BOARD. On a board with no `tdm` resource the request (a) drives
    #      bclk/fsync/dout into unconnected Signal()s and reads tdm_data_i = 0 -
    #      digital SILENCE at the declared width - and (b) rebinds o_i2s_mclk_o
    #      off the I2S front-end's pad, which on the Arty is pmoda:4 (D13), the
    #      CS5343 MCLK and the only working audio input the board has. Both used
    #      to be a printed warning; a warning is not enough
    #      (docs/testing/methodology.md R5 - a structural zero is not a
    #      measurement). `getattr` for the master flag so this composes with the
    #      trees that do and do not yet have it.
    board_audio_routing.assert_front_end_routed(
        args.board, args.audio_interface,
        audio_if_master=getattr(args, "audio_interface_master", False))

    if args.board == "arty":
        # Digilent Arty A7-100: same xc7a100t die (csg324-1), 100 MHz clkin,
        # MT41K128M16 DDR3, DP83848 MII 10/100 PHY, FT2232 = JTAG+UART on one
        # cable. Second Milan node for AVDECC/Milan interop (100M CBS point).
        from litex_boards.platforms import digilent_arty
        platform = digilent_arty.Platform(variant="a7-100", toolchain="vivado")
    else:
        platform = alinx_ax7101.Platform()
    # QSPI-bootable bitstreams (user directive 2026-07-12): compress (a 100t
    # frame is 3.65 MiB raw — the 16 MiB flash only fits it compressed) and
    # pin the SPI config settings the ARTY's flash part supports. ARTY ONLY:
    # the AX7101 platform pins CONFIG_MODE SPIx4, and a later SPI_BUSWIDTH 1
    # contradicts it - bitgen hard-errors (Designutils 20-1856; killed the
    # whole 2026-07-13 AX sweep). The AX bitstream is JTAG-SRAM per policy,
    # so it keeps its platform's proven settings untouched.
    if args.board == "arty":
        platform.toolchain.bitstream_commands += [
            "set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 1 [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]",
        ]
        # The litex-boards Arty platform hardcodes a SPIX4 write_cfgmem in
        # additional_commands; against our x1 bitstream (the PROVEN boot
        # config above) Vivado hard-errors AT THE VERY END of an otherwise
        # complete run (Writecfgmem 68-20 - it cost the m0019h arty seeds
        # their exit status AFTER their bitstreams were already written).
        # Override to the matching x1 interface so the .bin exists and the
        # flow exits 0.
        platform.toolchain.additional_commands = [
            "write_cfgmem -force -format bin -interface spix1 -size 16 "
            "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin",
        ]
        # The LiteX arty platform ships SPI_BUSWIDTH 4 + a spix4 write_cfgmem;
        # our x1 override above wins the property fight, and Vivado then
        # refuses the platform's spix4 cfgmem against an x1 bitfile
        # (Writecfgmem 68-20 - killed both finished arty m0019h seeds AFTER
        # their bitstreams succeeded, 2026-07-28). One decision, both halves:
        # the .bin is generated x1 to match the x1 bitfile.
        platform.toolchain.additional_commands = [
            "write_cfgmem -force -format bin -interface spix1 -size 16 "
            "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin"]
    soc = MilanSoC(platform, int(args.sys_clk_freq), xlen=args.xlen,
                   cpu_count=args.cpu_count, cpu=args.cpu, with_milan=not args.no_milan,
                   board=args.board, bus_standard=args.bus_standard,
                   with_mac=args.with_mac or args.all_blocks,
                   with_dma=args.with_dma or args.all_blocks,
                   with_dram=args.with_dram or args.all_blocks,
                   with_spiflash=args.with_spiflash or args.all_blocks,
                   flashboot=args.flashboot,
                   gtx_tx_invert=args.gtx_tx_invert,
                   main_ram_size=args.main_ram_size,
                   milan_clk_freq=args.milan_clk_freq, l2_bytes=args.l2_bytes,
                   num_streams=args.num_streams,
                   pcm_ring=args.pcm_ring,
                   aaf_playback=args.aaf_playback,
                   aaf_pb_streams=args.aaf_playback_streams,
                   loopback_lane=args.loopback_lane,
                   render_lpf=not args.no_render_lpf,
                   # tier-1 optional blocks: a key is emitted only when the
                   # flag is set, and False is the ONLY value that prunes.
                   optional_blocks={
                       "media_clock_servo": not args.no_media_clock_servo,
                       "latency_taps":      not args.no_latency_taps,
                       "maap":              not args.no_maap,
                       "i2s_playback":      not args.no_i2s_playback,
                       "rx_mac_filter":     not args.no_rx_mac_filter,
                       "datapath_probes":   not args.no_datapath_probes,
                   },
                   cbs_queues_mask=args.cbs_queues_mask,
                   entity_gen_dir=args.entity_gen_dir,
                   audio_if_slots={"i2s_philips": 0, "tdm8": 8, "tdm16": 16,
                                   "tdm32": 32}[args.audio_interface],
                   talker_wire_chans=int(args.talker_wire_chans),
                   audio_if_master=bool(args.audio_interface_master),
                   rx_queues=args.rx_queues, rx_rsc=not args.no_rx_rsc,
                   strip_probes=args.strip_probes,
                   legacy_ring=args.legacy_ring,
                   rx_fifo_beats=int(args.rx_fifo_beats),
                   eth_phy_index=(1 if args.eth_port == "e2" else 0),
                   hs_page_bytes=args.hs_page_bytes,
                   with_fpu=args.with_fpu, extra_scala_args=args.scala_args,
                   coherent_dma=args.coherent_dma,
                   rgmii_tx_delay=args.rgmii_tx_delay,
                   rgmii_rx_delay=args.rgmii_rx_delay,
                   uart_baudrate=args.uart_baudrate)
    if args.floorplan:
        # The 100 MHz critical path is the sys reset (fanout ~3900, 8.9 ns of PURE route,
        # 0 logic levels), which also caps the clock. The obvious fix is to REPLICATE the
        # reset into compact local copies  -  but on this design that PROVED IMPOSSIBLE: all
        # three replication methods FAILED to fracture `sys_rst` (each left it at fo~3969,
        # 8.9 ns route, the +0.043 ns path):
        #   1. post-synth XDC set_property MAX_FANOUT,
        #   2. the RTL (* max_fanout = 100 *) attribute set below (applied at synthesis), and
        #   3. phys_opt_design -force_replication_on_nets (the -force variant, below).
        # Root cause: Vivado protects the reset CONTROL SET because the reset synchronizer's
        # clock carries a DONT_TOUCH  -  no lever (XDC / RTL attr / forced phys_opt) will touch
        # it. THE WORKING FIX (this flag): declare the reset a MULTICYCLE path. `sys_rst` is
        # async-assert / sync-deassert (AsyncResetSynchronizer) and HELD for many cycles at
        # boot / soc_ctrl reset, so its synchronous-deassertion arc need NOT close in one cycle
        #  -  a 1-cycle skew in reset RELEASE is harmless (all flops are still held reset for the
        # surrounding cycles, and the deassertion is already synchronised at the source). Giving
        # the arc 2 cycles (-setup 2 / -hold 1) lets the ~8.9 ns fanout-3969 route arrive within
        # 20 ns, so the reset stops being a timing constraint DETERMINISTICALLY (not placer
        # luck)  -  the same pattern LiteX already uses for the CBS slope path above. (The sys
        # clock is raised separately via --sys-clk-freq; the 112.5 MHz fp builds are in
        # docs/findings/LATENCY_INVESTIGATION.md §8.)
        soc.platform.add_platform_command("set_multicycle_path 2 -setup -through [get_nets sys_rst]")
        soc.platform.add_platform_command("set_multicycle_path 1 -hold  -through [get_nets sys_rst]")
    builder = Builder(soc, **builder_argdict(args))
    # Aggressive timing closure (opt-in): enables the post-place phys_opt pass
    # (off by default in LiteX) and steps place/route/phys-opt up to their
    # timing-focused directives  -  enough to close the marginal CBS setup path at
    # 100 MHz without further RTL pipelining.
    build_kwargs = dict(
        vivado_place_directive               = "ExtraTimingOpt",
        vivado_post_place_phys_opt_directive = "AggressiveExplore",
        # route Explore -> AggressiveExplore (m001d net analysis): at ~100%
        # slice occupancy every m001d seed lost 0.32-0.77 ns between the
        # placement ESTIMATE (+0.05..-0.02) and the routed result - the
        # router, not the placer, needed the top-effort rung.
        vivado_route_directive               = "AggressiveExplore",
        vivado_post_route_phys_opt_directive = "AggressiveExplore",
    ) if args.timing_opt else {}
    if args.place_directive:
        build_kwargs["vivado_place_directive"] = args.place_directive
    if args.synth_directive:
        build_kwargs["vivado_synth_directive"] = args.synth_directive
    if args.opt_directive:
        build_kwargs["vivado_opt_directive"] = args.opt_directive
    if args.route_directive:
        build_kwargs["vivado_route_directive"] = args.route_directive
    if args.area_flow:
        build_kwargs.setdefault("vivado_synth_directive", "AreaOptimized_high")
        build_kwargs.setdefault("vivado_opt_directive", "ExploreArea")
        # second, merge-focused opt pass right before placement (the flow's own
        # opt_design already ran): folds equivalent CE/reset drivers so FFs pack
        # denser into slices (control_sets.rpt suggestion)
        soc.platform.toolchain.pre_placement_commands.append(
            "opt_design -control_set_merge -merge_equivalent_drivers")
    # Use as many CPU cores as Vivado allows for synth/place/route (`set_param
    # general.maxThreads N`). Vivado caps this at 32 regardless of host cores, so
    # request min(cores, 32)  -  the rest of the box is idle during a single P&R run.
    if args.vivado_max_threads:
        build_kwargs["vivado_max_threads"] = args.vivado_max_threads
    builder.build(run=args.build, **build_kwargs)  # run=False => elaborate + export gateware, no Vivado
    # Persist the flash-boot layout so deploy.sh writes the exact same offsets the BIOS
    # was compiled with (single source of truth  -  see FLASHBOOT_LAYOUT / deploy.sh flash-images).
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
