#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Configurable RISC-V SoC with the Milan TSN NIC. The product profile is a
# cacheless RV32 VexiiRiscv running the Milan bare-metal control firmware.
#
#   ./milan_soc.py                         # NIC (CSR only); elaborate + export gateware
#   ./milan_soc.py --full                  # FULL FPGA solution: NIC + DMA + MAC + PHY
#   ./milan_soc.py --with-dma / --with-mac # attach just one boundary
#   ./milan_soc.py --no-milan              # bare SoC (bring-up smoke; self-contained)
#   ./milan_soc.py --software-profile baremetal --cpu vexiiriscv --xlen 32 \
#       --with-spiflash --flashboot baremetal
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
import subprocess
import json
import argparse
import binascii

from gptp_owner_contract import GPTP_OWNER_CODES
from qspi_owner_transition import aem_image_binding, bitstream_binding

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
# only the BASE is CPU-specific: on this NaxRiscv SoC an MMIO peripheral must live in
# the CPU IO region (>= 0x8000_0000, uncached), so we map it at 0x9000_0000. The Zynq
# alternate integration used 0x43C0_0000. Firmware and gateware must share this base.
MILAN_CSR_BASE = 0x9000_0000
MILAN_CSR_SIZE = 0x0001_0000  # 64 KB

# On-chip BRAM PCM ring MMIO window (--pcm-ring bram). Uncached IO region just
# above the CSR window; the CPU mmaps this to read received PCM straight out of
# the dual-port BRAM (no DRAM ring, no DMA writer => the datapath's sink.ready is
# constant 1, so mf52 SHED + I6 are structurally impossible). The pcm CSR block
# (base/length/stride/enable/sel/offset) is UNCHANGED - the driver ABI is
# identical; only `base` now reads this window instead of a DRAM address. 32 KB
# = 64b x 4096 = 8 RAMB36 (mf53e has 36 free); the CSR `length` may program a
# smaller live sub-ring.
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

# ---- QSPI flash boot -------------------------------------------------------
# The 16 MiB product map contains the self-configuring bitstream, the raw AEM
# descriptor image, and two persistent writable regions. Offsets are relative
# to the memory-mapped flash base and are erase-block aligned. The generated
# flashboot_layout.json binds deployment to this exact map.
FLASHBOOT_LAYOUT = {
    "bitstream": {"offset": 0x00_0000, "addr": 0x0,          "size": 0x40_0000},
    "aem":       {"offset": 0x40_0000, "addr": 0x0,          "size": 0x01_0000},
}
FLASHBOOT_MANIFESTS = {
    "none": [],
    "baremetal": ["aem"],
}
FLASHBOOT_AEM = FLASHBOOT_LAYOUT["aem"]

# Writable slots. NOT boot images: the BIOS never copies them, deploy.sh never
# writes them, and `build.sh flash` / `deploy.sh flash-pair` MUST NOT erase
# them on a reflash - a gateware update that silently wipes saved bindings and
# fault logs is worse than not having them, because the entity then comes back
# unbound *sometimes*.  They are declared here so that the flash map has ONE
# source of truth (docs/design/SAVED_STATE_FASTCONNECT.md section 5) and so that
# sw/litex/flash_map.py can serve every other consumer of the map from it
# instead of a second hand-maintained copy.
#
#   journal  2 x 64 KiB erase blocks = slot A / slot B, RAW (no filesystem):
#            "a torn write cannot damage the other slot" is then a property of
#            the flash geometry, not a promise from a log-structured fs, and the
#            slot is readable before any mount.
#   user     application records: entity/group names, channel maps, mixer
#            state, and the rotating compressed CTF fault log.
#
# deploy.sh treats every image budget and every reserved-slot boundary as a
# hard ceiling before writing. That protects these writable ranges from an
# oversized artifact and bounds the AEM write to its 64 KiB slot.
FLASH_SIZE        = 0x100_0000   # 16 MiB (N25Q128A13 / S25FL128S)
FLASH_ERASE_BLOCK = 0x1_0000     # 64 KiB - the unit of erase, and of slot alignment
FLASHBOOT_RESERVED = {
    # Keep these stable across product revisions: moving them intentionally
    # starts with empty persistence and requires an explicit migration plan.
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
    turn "write the journal" into "corrupt the adjacent slot".
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
        # margin=0 on every create_clkout below. LiteX defaults margin=1e-2:
        # each clkout is a REQUEST with a +-10000 ppm acceptance window (the
        # "(+-10000.00ppm)" S7PLL log line) and the solver takes the FIRST
        # in-window integer divider, not the closest. t532 forensics (08-08):
        # the window never actually bit on these requests - VCO 1600 divides
        # 100/400/200 exactly - but a request the VCO could not divide exactly
        # would be accepted up to 1 % off while every cycle-counted constant
        # elaborated from the REQUESTED Hz (the PHC's 10.0 ns nominal
        # PTP_INCR, the /48000 media-tick Bresenhams, CBS slopes, QTICK)
        # kept assuming the request: a silent 1 %-class detune of timestamps
        # and pacing. margin=0 = exact division or a loud elaboration error.
        pll.create_clkout(self.cd_sys, sys_clk_freq, margin=0)
        platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin)

        if board == "arty" and with_eth:
            self.cd_eth_ref = ClockDomain(reset_less=True)
            pll.create_clkout(self.cd_eth_ref, 25e6, margin=0)
            self.comb += platform.request("eth_ref_clk").eq(ClockSignal("eth_ref"))

        if milan_clk_freq:
            # Separate, slower clock for the Milan TSN datapath (rx_filter/CAM/CBS/
            # classifier/PTP/csr). That block is dense and was the sys (100 MHz)
            # critical path, but it only has to keep up with 1 GbE: a 64-bit datapath
            # at >=50 MHz is >3 Gb/s, so running it below sys costs no throughput while
            # lifting its logic off the 100 MHz timing budget entirely. The CPU + DDR3
            # stay at sys; the CSR (AXI-Lite) crosses via AXILiteClockDomainCrossing.
            self.cd_milan = ClockDomain()
            # margin=0 (see CRG note above): the Milan datapath's entire time
            # base is CYCLE arithmetic on MILAN_CLK_FREQ_HZ - the PHC advances
            # a nominal 10.0 ns per edge and the AAF/media grids are /48000
            # Bresenhams of the same constant - so the synthesized frequency
            # must BE the requested one, never merely "within 1 %".
            pll.create_clkout(self.cd_milan, milan_clk_freq, margin=0)
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
            # The audio clocks are deliberately NOT create_clkout products, so
            # the margin=0 rule above does not apply here: 24.576 MHz has NO
            # exact integer solution from a 100 MHz reference. The explicit
            # two-stage chain below lands at a KNOWN, by-construction error -
            # PLAN A 24,575,738.53 Hz = -10.64 ppm, PLAN B 24,575,983.70 Hz =
            # -0.66 ppm - both inside Milan 7.4's +-50 ppm media-clock budget
            # even before the KL_mmcm_drp_servo fine-PS trim (~260 ppm
            # authority) pulls them onto the recovered media clock. Do not
            # "fix" these toward exactness: the values below ARE the
            # achievable optima and they are silicon-proven.
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
            pll.create_clkout(self.cd_sys4x,     4 * sys_clk_freq, margin=0)
            pll.create_clkout(self.cd_sys4x_dqs, 4 * sys_clk_freq, phase=90, margin=0)

        if with_dram or with_eth:
            # 200 MHz IDELAY reference + controller (DDR3 PHY + RGMII PHY IODELAYs).
            from litex.soc.cores.clock import S7IDELAYCTRL
            self.cd_idelay = ClockDomain()
            pll.create_clkout(self.cd_idelay, 200e6, margin=0)
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
                 desc_base=None, resp_base=None,
                 rx1_irq=None, milan_clk_hz=100_000_000, num_streams=1,
                 audio_if_slots=0, talker_wire_chans=2, audio_if_master=False,
                 audio_if_i2s_pair=False, gptp_plane=None, sound_card=False,
                 aaf_playback=False, aaf_pb_streams=1,
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
        add_milan_datapath(self, platform, axil, ev.csr.trigger, desc_base=desc_base,
                           resp_base=resp_base,
                           extra_ports=dict(dma_mac_ports or {}, o_o_identify=self.identify),
                           milan_cd=milan_cd,
                           milan_clk_hz=milan_clk_hz, num_streams=num_streams,
                           audio_if_slots=audio_if_slots,
                           talker_wire_chans=talker_wire_chans,
                           audio_if_master=audio_if_master,
                           audio_if_i2s_pair=audio_if_i2s_pair,
                           gptp_plane=gptp_plane,
                           sound_card=sound_card,
                           aaf_playback=aaf_playback, aaf_pb_streams=aaf_pb_streams,
                           loopback_lane=loopback_lane,
                           render_lpf=render_lpf, optional_blocks=optional_blocks,
                           cbs_queues_mask=cbs_queues_mask,
                           entity_gen_dir=entity_gen_dir)


# The milan_datapath source set (ordered: packages first) for the §A.9 wrapper.
# It used to say it mirrored the milan_dp Verilator Makefile and the syn/yosys
# entry, calling those the single source of truth while each of them said the
# same of another: nothing held the authority and every copy drifted together.
#
# THE PROTOCOL PROCESSOR IS PART OF THE DATAPATH NOW (scenario B, 2026-08-13).
# milan_datapath instantiates KL_pp_shadow UNCONDITIONALLY - there is no
# PP_PLANE_P any more - so the submodule's files are datapath files, not an
# opt-in extra. They come FIRST because their packages must be declared before
# the modules that import them, which scripts/pp_srcs.py guarantees by reading
# each file for a `package` declaration rather than trusting a name. Paths are
# repo-root relative like every other entry here (add_source joins them onto
# `base`). This comment used to call tb/verilator/milan_dp/Makefile the
# authoritative list; that file said the same of nothing, so the authority was
# circular and the instruction to copy it is what recreated the drift.
def _pp_sources():
    """Submodule design sources, derived from the tree by scripts/pp_srcs.py."""
    import importlib.util
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    spec = importlib.util.spec_from_file_location(
        "pp_srcs", os.path.join(root, "scripts", "pp_srcs.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.pp_sources()


_MILAN_DATAPATH_SOURCES = [
    # The submodule half is DERIVED from the tree; see scripts/pp_srcs.py.
    # This list used to name tb/verilator/milan_dp/Makefile as authoritative
    # while that file named none, so the authority was circular and all four
    # copies went stale together the moment the submodule pin moved.
    *_pp_sources(),
    # the two consumer-side wrappers that bind it into this datapath: the
    # shadow/substitution wrapper and the block-vs-per-source MAAP adapter.
    "hdl/milan/KL_pp_shadow.sv", "hdl/milan/KL_pp_maap_shim.sv",
    # the gPTP plane (#114): milan_datapath instantiates KL_gptp_shadow and
    # KL_gptp_txstamp under GPTP_PLANE_EN_P (product default ON), so Vivado must see
    # the wrappers and the gptp-processor engine they wrap. No copy of this
    # list is authoritative - not this one, and not GPTP_SRCS in the milan_dp
    # Verilator Makefile, which this comment once called so: the RTL is, and
    # scripts/check_rtl_source_lists.py checks every copy against the engine
    # files the datapath really reaches. The package first, its importers after.
    "gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv", "gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv",
    "gptp-processor/hdl/wire/KL_gptp_rx_parser.sv", "gptp-processor/hdl/wire/KL_gptp_tx_slot.sv",
    "gptp-processor/hdl/common/KL_gptp_timer.sv", "gptp-processor/hdl/top/KL_gptp_engine.sv",
    "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv",
    "hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv",
    "hdl/common/ethernet_packet_pkg.sv", "hdl/common/axi_stream_if.sv",
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
    # ADP TX arbitration survives the scenario-B substitution: the advertiser
    # itself is the processor's KL_adp_engine now, but the two-source TX merge
    # in front of the MAC is still this module.
    "hdl/ieee17221/adp/adp_tx_arbiter.sv",
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
    "hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv",  # item-11: observation-point adapter + LTAP CSR word order
    "hdl/ieee1722/aaf/KL_media_adv.sv", "hdl/common/cdc_pair_fifo.sv",
    "hdl/ieee1722/avtp/avtp_subtype_pkg.sv", "hdl/ieee1722/avtp/avtp_stream_parser.sv",
    "hdl/ieee1722/avtp/KL_stream_table.sv",
    "hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv",
    "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv", "hdl/ieee1722/avtp/KL_talker_diag_ctx.sv", "hdl/ieee1722/avtp/KL_media_clock_restart.sv",
    "hdl/ieee1722/aaf/KL_pcm_route.sv",
    "hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv", "hdl/ieee1722/aaf/KL_tdm_capture.sv", "hdl/ieee1722/aaf/KL_tdm_capture_master.sv", "hdl/ieee1722/aaf/KL_pair_blend.sv", "hdl/ieee1722/aaf/KL_pair_zero_fill.sv", "hdl/ieee1722/aaf/KL_tdm_render.sv", "hdl/ieee1722/aaf/KL_chan_map_render.sv", "hdl/ieee1722/aaf/KL_chan_map_capture.sv", "hdl/ieee1722/aaf/KL_aaf_packetizer.sv", "hdl/ieee1722/crf/KL_crf_rx.sv", "hdl/ieee1722/crf/KL_crf_tx.sv", "hdl/ieee1722/maap/KL_maap.sv",
    "hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv", "hdl/ieee1722/aaf/KL_aaf_packetizer.sv", "hdl/ieee1722/crf/KL_crf_rx.sv", "hdl/ieee1722/crf/KL_crf_tx.sv", "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv", "hdl/ieee1722/crf/KL_media_nco.sv", "hdl/ieee1722/maap/KL_maap.sv",
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

    This five-signal TDM header deliberately has no `lrclk` subsignal.  The
    AX7101 J11 `lrclk` is an optional media-grid observation point, not part
    of the TDM bus; MilanSoC leaves that output internal on boards without it.

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
                       desc_base=None, resp_base=None,
                       milan_clk_hz=100_000_000, num_streams=1, audio_if_slots=0,
                       talker_wire_chans=2, audio_if_master=False,
                       audio_if_i2s_pair=False,
                       gptp_plane=None,
                       sound_card=False, aaf_playback=False, aaf_pb_streams=1,
                       loopback_lane=False,
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
        # media-grid test point: left open unless the board has a J11 header
        o_media_lrclk_o = Signal(),
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
    # N_STREAMS: NxN dataplane width (docs/fpga/FPGA_DESIGN.md section 2). The builder
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
    # milan-fpga/ root - used by the source list AND the processor ROM path
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # milan-fpga/
    # Ownership is a per-build fact.  Raising here catches a caller which
    # stopped forwarding the resolved value; bool(None) would silently choose
    # the option-off plane even though the RTL product default is on.
    if gptp_plane is None:
        raise RuntimeError(
            "add_milan_datapath needs gptp_plane=: resolve the PHC owner and "
            "pass gptp_plane=True or gptp_plane=False")
    dp_params = dict(p_MILAN_CLK_FREQ_HZ=int(milan_clk_hz),
                     p_N_STREAMS=int(num_streams),
                     p_AUDIO_IF_SLOTS_P=int(audio_if_slots),
                     # Always pass the option: an explicit legacy build must
                     # override milan_datapath's product-default 1.
                     p_GPTP_PLANE_EN_P=int(bool(gptp_plane)))
    if gptp_plane:
        # #116 product-default fabric build. The builder generates this image from
        # the SAME end-station YAML as the AEM: station MAC, gPTP priority1 and
        # Milan clock are therefore facts of one config, not parallel CLI
        # literals. Pass an absolute path because Vivado's run directory is
        # not the repository and a relative $readmemh silently yields zero ROM.
        dp_params["p_GPTP_UCODE_HEX_P"] = _builder_out(
            entity_gen_dir, "gptp_ucode.hex")
    if sound_card:
        dp_params["p_SOUND_CARD_P"] = 1
    # THE ACMP TRANSITION ROM IS NOT OPTIONAL. protocol_processor_top - which
    # milan_datapath now instantiates unconditionally through KL_pp_shadow -
    # $readmemh's its listener transition ROM by the RELATIVE name
    # "ltn_rom.hex", and Vivado resolves that against ITS OWN run directory,
    # not against the source file. Every build therefore generates the image
    # and hands over an ABSOLUTE path, so the bitstream cannot depend on where
    # vivado was launched from and cannot silently elaborate an all-zero ROM
    # (which is a listener that answers nothing).
    rom = os.path.join(base, "configs", "generated", "ltn_rom.hex")
    gen = os.path.join(base, "protocol-processor", "hdl", "acmp", "rom",
                       "gen_ltn_rom.py")
    os.makedirs(os.path.dirname(rom), exist_ok=True)
    subprocess.run([sys.executable, gen, "-o", rom], check=True)
    dp_params["p_PP_TROM_HEX_P"] = rom

    # THE AECP uCPU MICROCODE IMAGE, same relative-$readmemh contract as the
    # ACMP ROM above and the same failure mode if it is not handed over as an
    # absolute path: an all-zero microcode store is an AECP engine that
    # answers nothing, which looks exactly like the pre-uCPU build.
    uc = os.path.join(base, "configs", "generated", "ucode.hex")
    ucgen = os.path.join(base, "protocol-processor", "hdl", "aecp", "ucode",
                         "gen_ucode.py")
    subprocess.run([sys.executable, ucgen, "-o", uc], check=True)
    dp_params["p_PP_UCODE_HEX_P"] = uc

    # WHERE THE ENTITY MODEL LIVES. The processor's descriptor store fetches
    # the AEM image from MAIN MEMORY over a read-only master, at a base that is
    # COMPILE-TIME by its design - there is no base register, so software
    # cannot point it somewhere wrong at runtime. On this SoC that memory is
    # DDR3, so the base must be a real address inside the SoC's main_ram
    # region that software reserves and loads before enabling the entity.
    #
    # DERIVED, NEVER MIRRORED: taken from the SoC's own memory map rather than
    # restated as a literal, because a copied base is a base that diverges the
    # first time the map moves. The offset is the top 1 MiB of main memory,
    # which the product memory map reserves.
    # RAISE rather than fall back. The processor's default base (0x2000_0000)
    # is ITS repository's placeholder and is not guaranteed to be memory on
    # this SoC; letting it stand would give the store a base that reads as
    # "image not loaded" forever - indistinguishable from a software bug, and
    # found on a board instead of here. The SoC computes it (only the SoC
    # knows its memory map) and hands it down.
    if desc_base is None:
        raise RuntimeError(
            "milan_datapath: the protocol processor's descriptor store needs a "
            "main-memory base to fetch the entity model from. Pass desc_base=.")
    assert desc_base % 8 == 0, "DESC_BASE_P must be 8-byte aligned"
    dp_params["p_PP_DESC_BASE_P"] = desc_base

    # WHERE THE AECP RESPONSE BUFFER LIVES. Second window, same rule, one extra
    # obligation: the processor WRITES this one. Held as fabric flops the buffer
    # measured 5,079 FF / 3,495 LUT and it was those flops that failed placement
    # on a die whose block RAM was 100% used - so it is main memory here too,
    # and the region must be the processor's alone. RAISE rather than fall back
    # for exactly the DESC_BASE_P reason above, and one worse: the submodule's
    # placeholder default (0x2010_0000) is not guaranteed to be memory on this
    # SoC, and a WRITE master pointed at the wrong place corrupts whatever it
    # lands on instead of merely reading zeros.
    if resp_base is None:
        raise RuntimeError(
            "milan_datapath: the protocol processor's AECP response buffer "
            "needs a main-memory region of its own. Pass resp_base=.")
    assert resp_base % 8 == 0, "RESP_BASE_P must be 8-byte aligned"
    dp_params["p_PP_RESP_BASE_P"] = resp_base
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
    # LPF_P: BANKED AREA LEVER (docs/design/AREA_BUDGET.md). Passed ONLY when
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
    # =======================================================================
    #  AECP DESCRIPTOR-IMAGE READ BRIDGE  (protocol-processor 07 §3.3)
    # =======================================================================
    # The processor's descriptor store fetches the entity model from main
    # memory. This is that master, bridged to a LiteX wishbone READ master on
    # the DMA bus - the same shape as the AAF playback word-fetch bridge above
    # (`milan_aaf_pb`), extended from one word to a BURST.
    #
    # CONTRACT (the submodule's): ONE outstanding request, held until ready;
    # responses IN ORDER; `beats` is 64-bit beats, >= 1, max 128; `rsp_last`
    # marks the final beat; `rsp_ready` is tied 1 by the processor, it always
    # sinks. A beat carries its LOWEST byte address in bits [63:56] - 1722.1
    # wire order, i.e. BIG-ENDIAN, a byte-reverse of the little-endian words
    # the bus returns.
    #
    # THE ERROR ARM IS NOT OPTIONAL, and this is the second time this exact
    # trap has been paid for on this bus: LiteX's wishbone2axi asserts `err`
    # TOGETHER WITH `ack` in its error state, so `If(ack, ...)` alone accepts a
    # FAILED read and latches whatever `dat_r` held. The audio path had to
    # substitute silence because KL_pcm_tx has no error input. THIS master has
    # one: `desc_mem_rsp_err` aborts the burst and the store degrades that
    # locate to NO_SUCH_DESCRIPTOR. So the error is PROPAGATED, never masked -
    # a corrupt descriptor is never served as though it were good.
    desc_req_valid = Signal();     desc_req_ready = Signal()
    desc_req_addr  = Signal(32);   desc_req_beats = Signal(9)
    desc_rsp_valid = Signal();     desc_rsp_ready = Signal()
    desc_rsp_data  = Signal(64)
    desc_rsp_last  = Signal();     desc_rsp_err   = Signal()

    d_req = _axis_dp_cdc(host, "descmem_req_cdc",
                         [("addr", 32), ("beats", 9)], milan_cd,
                         to_datapath=False)
    d_rsp = _axis_dp_cdc(host, "descmem_rsp_cdc",
                         [("data", 64), ("blast", 1), ("err", 1)], milan_cd,
                         to_datapath=True)
    host.comb += [
        d_req.dp.valid.eq(desc_req_valid), d_req.dp.addr.eq(desc_req_addr),
        d_req.dp.beats.eq(desc_req_beats), desc_req_ready.eq(d_req.dp.ready),
        desc_rsp_valid.eq(d_rsp.dp.valid), desc_rsp_data.eq(d_rsp.dp.data),
        desc_rsp_last.eq(d_rsp.dp.blast),  desc_rsp_err.eq(d_rsp.dp.err),
        d_rsp.dp.ready.eq(1),   # the processor's rsp_ready is tied 1
    ]
    # THE BUS MASTER LIVES AT THE SoC, not here: this is a LiteXModule and has
    # no bus. Publish the sys-domain endpoints and let the SoC bridge them
    # (see `descmem` in the SoC body) - the same split MilanDMA already uses.
    host.descmem_req_sys = d_req.sys
    host.descmem_rsp_sys = d_rsp.sys

    ports.update(
        o_o_desc_mem_req_valid = desc_req_valid,
        i_i_desc_mem_req_ready = desc_req_ready,
        o_o_desc_mem_req_addr  = desc_req_addr,
        o_o_desc_mem_req_beats = desc_req_beats,
        i_i_desc_mem_rsp_valid = desc_rsp_valid,
        o_o_desc_mem_rsp_ready = desc_rsp_ready,
        i_i_desc_mem_rsp_data  = desc_rsp_data,
        i_i_desc_mem_rsp_last  = desc_rsp_last,
        i_i_desc_mem_rsp_err   = desc_rsp_err,
    )

    # =======================================================================
    #  AECP RESPONSE-BUFFER READ+WRITE BRIDGE  (protocol-processor 03 §7)
    # =======================================================================
    # The SECOND main-memory master, and the one that made this bitstream
    # placeable: the AECP response buffer used to be 5,079 flip-flops of fabric
    # state inside KL_aecp_engine, on a die whose 135 block-RAM tiles were 100%
    # spoken for. It is a REGION now, and this is its bridge.
    #
    # NOT MERGED WITH THE DESCRIPTOR FACE ABOVE, on the submodule's explicit
    # contract: both masters are watchdog-bounded with one outstanding
    # transaction each, and one shared channel would need an arbiter whose
    # grant has to be released correctly on every timeout arm of both. The
    # SoC's memory system already arbitrates, so they stay two faces.
    #
    # THREE CONTRACT DIFFERENCES from `desc_mem_*`, all of them this bridge's
    # obligation (protocol_processor_top.sv's port banner is the authority):
    #   * `rsp_ready` is REAL backpressure - it is NOT tied 1 here. The buffer
    #     takes a beat only once the frame builder spent the previous one, so
    #     the response endpoint's `ready` comes FROM the datapath and the CDC
    #     FIFO holds the beat until it is taken.
    #   * the write channel is ONE outstanding SINGLE-BEAT write: 8-byte
    #     aligned address, big-endian lane (byte addr+n = data[63-8n -: 8]),
    #     `strb` bit n enabling byte n, and A ZERO-STROBE BYTE MUST NOT BE
    #     MODIFIED - which is why the bus side splits the lane into two 32-bit
    #     wishbone cycles carrying HALF THE STROBE EACH as `sel`, and skips a
    #     half whose strobe is empty rather than issuing a sel=0 cycle.
    #   * `wr_done` is a ONE-CYCLE COMMIT PULSE. It is generated as
    #     `valid & ready` on a CDC endpoint whose `ready` is tied 1, so exactly
    #     one token = exactly one cycle, and it necessarily lands STRICTLY
    #     AFTER `wr_ready` (this is the acknowledged bridge, not the posted
    #     one) - which is also the only shape KL_aecp_resp_buf's R_FLUSH arm
    #     accepts, since it sets `wbusy_r` on the ready and only then looks for
    #     the done.
    # Ordering ("a read accepted after a write reported done observes that
    # write") is free: one wishbone master, one FSM, strictly serialised.
    resp_req_valid = Signal();     resp_req_ready = Signal()
    resp_req_addr  = Signal(32);   resp_req_beats = Signal(9)
    resp_rsp_valid = Signal();     resp_rsp_ready = Signal()
    resp_rsp_data  = Signal(64)
    resp_rsp_last  = Signal();     resp_rsp_err   = Signal()
    resp_wr_valid  = Signal();     resp_wr_ready  = Signal()
    resp_wr_addr   = Signal(32);   resp_wr_data   = Signal(64)
    resp_wr_strb   = Signal(8)
    resp_wr_done   = Signal();     resp_wr_err    = Signal()

    r_req = _axis_dp_cdc(host, "respmem_req_cdc",
                         [("addr", 32), ("beats", 9)], milan_cd,
                         to_datapath=False)
    r_rsp = _axis_dp_cdc(host, "respmem_rsp_cdc",
                         [("data", 64), ("blast", 1), ("err", 1)], milan_cd,
                         to_datapath=True)
    r_wr  = _axis_dp_cdc(host, "respmem_wr_cdc",
                         [("addr", 32), ("data", 64), ("strb", 8)], milan_cd,
                         to_datapath=False)
    r_wd  = _axis_dp_cdc(host, "respmem_wd_cdc",
                         [("err", 1)], milan_cd, to_datapath=True)
    host.comb += [
        r_req.dp.valid.eq(resp_req_valid), r_req.dp.addr.eq(resp_req_addr),
        r_req.dp.beats.eq(resp_req_beats), resp_req_ready.eq(r_req.dp.ready),
        resp_rsp_valid.eq(r_rsp.dp.valid), resp_rsp_data.eq(r_rsp.dp.data),
        resp_rsp_last.eq(r_rsp.dp.blast),  resp_rsp_err.eq(r_rsp.dp.err),
        # REAL backpressure - the one place this face differs from descmem's
        r_rsp.dp.ready.eq(resp_rsp_ready),
        r_wr.dp.valid.eq(resp_wr_valid),   r_wr.dp.addr.eq(resp_wr_addr),
        r_wr.dp.data.eq(resp_wr_data),     r_wr.dp.strb.eq(resp_wr_strb),
        resp_wr_ready.eq(r_wr.dp.ready),
        # one token in flight by contract, `ready` tied 1 -> `valid` is high
        # for exactly one cycle: the commit pulse the buffer waits for
        r_wd.dp.ready.eq(1),
        resp_wr_done.eq(r_wd.dp.valid), resp_wr_err.eq(r_wd.dp.err),
    ]
    host.respmem_req_sys = r_req.sys
    host.respmem_rsp_sys = r_rsp.sys
    host.respmem_wr_sys  = r_wr.sys
    host.respmem_wd_sys  = r_wd.sys

    ports.update(
        o_o_resp_mem_req_valid = resp_req_valid,
        i_i_resp_mem_req_ready = resp_req_ready,
        o_o_resp_mem_req_addr  = resp_req_addr,
        o_o_resp_mem_req_beats = resp_req_beats,
        i_i_resp_mem_rsp_valid = resp_rsp_valid,
        o_o_resp_mem_rsp_ready = resp_rsp_ready,
        i_i_resp_mem_rsp_data  = resp_rsp_data,
        i_i_resp_mem_rsp_last  = resp_rsp_last,
        i_i_resp_mem_rsp_err   = resp_rsp_err,
        o_o_resp_mem_wr_valid  = resp_wr_valid,
        i_i_resp_mem_wr_ready  = resp_wr_ready,
        o_o_resp_mem_wr_addr   = resp_wr_addr,
        o_o_resp_mem_wr_data   = resp_wr_data,
        o_o_resp_mem_wr_strb   = resp_wr_strb,
        i_i_resp_mem_wr_done   = resp_wr_done,
        i_i_resp_mem_wr_err    = resp_wr_err,
    )

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
    # (base is hoisted above dp_params: the transition-ROM path needs it too)
    # Include dirs for the ``include ...`` files (ethernet_packet_pkg.sv, *.svh).
    # Vivado auto-searches source dirs; Verilator (the sim backend) needs -I.
    # PER-CONFIG entity definition (USER 2026-07-28: both boards' 3-seed
    # sweeps run CONCURRENTLY): when set, the generated entity svh
    # (gen/adp_shape_defaults.svh) resolves from THIS config's own
    # configs/generated/<cfg>/ copy instead of the single tracked hdl/ one -
    # two boards can then build from one tree at the same time with no
    # svh-ownership handoff. Prepended so it WINS the include search; the
    # tracked dirs below stay as the fallback for every other include.
    if entity_gen_dir:
        platform.add_verilog_include_path(entity_gen_dir)
        platform.add_verilog_include_path(os.path.join(entity_gen_dir, "gen"))
    for inc in ("hdl/common", "hdl/ieee8021q/ts", "hdl/ieee8021as/ptp_timestamp",
                "hdl/ieee17221/adp", "hdl/common/csr", "hdl/common/eth_event_counter",
                "hdl/ieee1722/avtp"):
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
        # bitstream whose CPU-bound RX/ARP died as the die warmed while
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

        # QUASI-STATIC CLASS RELAXATION (USER 2026-08-15: constrain by CLASS,
        # never by per-endpoint analysis). Registers tagged
        # (* quasi_static = "yes" *) in the RTL (the tagging rules live at the
        # tag site in milan_csr.sv) are boot-written levels whose whole
        # fan-out cone is legitimately multi-cycle: one rule here prunes
        # every tagged cone from the single-cycle graph, and a register
        # tagged in any FUTURE round inherits the relaxation with no XDC
        # edit. Guarded so a build with zero tagged cells (or a synthesis
        # that dropped the attribute) degrades to full-strictness rather
        # than a Tcl error - the constraint can only ever RELAX known-safe
        # paths, never mask an untagged one. Hold 3 accompanies setup 4 per
        # the standard multicycle pairing, so hold analysis does not move to
        # the wrong capture edge. (Doubled braces: LiteX templates these
        # lines through str.format.)
        platform.toolchain.additional_xdc_commands.add(
            "set qs_cells [get_cells -hierarchical -quiet "
            "-filter {{quasi_static == \"yes\"}}]")
        platform.toolchain.additional_xdc_commands.add(
            "if {{[llength $qs_cells] > 0}} {{ "
            "set_multicycle_path 4 -setup -from $qs_cells ; "
            "set_multicycle_path 3 -hold  -from $qs_cells }}")

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
        # SystemVerilog, i.e. a different lane - see docs/testing/MILAN_V12_AUDIT_2026-08-16.md.
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
    docs/findings/PERFORMANCE_GOAL.md. Historical driver pairings are archived.

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
        # ---- M1 telemetry (docs/findings/PERFORMANCE_GOAL.md): closure + coalesce ratio.
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
        # ---- RSC phase A (docs/fpga/PIPELINE_STAGES.md): capture nine beats into a register
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
        # order, so the driver's blind FIFO pairing (docs/fpga/PIPELINE_STAGES.md)
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
        # A mergeable ACK (flags==ACK only, no payload, doff 5 or the common
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
    Mbit, see docs/findings/PERFORMANCE_GOAL.md). That parallel ACK split is
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
    """NxN per-stream PCM DRAM ring writer (docs/fpga/FPGA_DESIGN.md section 2).

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
    enable, sel[4], offset[32], cap[32] at +0x1c) so the ring ABI is
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
    the SoC CSR space  -  this is the firmware-visible ABI
    axi_dma simple mode). Each engine is its own Wishbone bus master into the SoC
    interconnect (width-adapted to the main bus automatically).

    `dp_ports` is merged with the MAC's into the single `milan_datapath` Instance.

    NOTE (board-gated): this elaborates against integrated RAM here; on the board it
    targets LiteDRAM. Descriptor/scatter-gather (Option 6b, multi-queue) is a later
    upgrade  -  see docs/integration/FULLY_FPGA_RISCV_MIGRATION.md §A.6 + the protocol/test matrix."""
    def __init__(self, soc, data_width=64, milan_cd="sys", rx_queues=1, hs_page_bytes=4096,
                 legacy_ring=True, rx_fifo_beats=2048, num_streams=1, pcm_ring="dram",
                 sound_card=False, aaf_playback=False, rx_rsc=True, talker_wire_chans=2,
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

        # Attach the DMA masters to the CPU's dedicated DMA port when it exists.
        # NaxRiscv --with-coherent-dma exposes a snooping port; the cacheless
        # bare-metal Vexii profile exposes the same attachment without coherence
        # hardware because there are no CPU caches. Otherwise use the plain SoC bus.
        # Without the coherent port, a cached NaxRiscv
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
        # path. Same
        # recipe as the TS record ring: WishboneDMAWriter with loop=1 wraps
        # base..base+length and the `offset` CSR is the ring write pointer the
        # consumer chases. Payload is full 64-bit words in wire byte
        # order (S32BE interleaved) - the depacketizer zero-pads any non-multiple
        # tail. Registered AFTER hs_pgsz_cap so no existing CSR address moves.
        # P12 (NXN §1.3): at num_streams == 1 the flat single-ring writer is
        # kept EXACTLY (same CSR block, same behavior — the N=1 byte-identity
        # axiom); num_streams > 1 swaps in the per-stream ring writer keyed by
        # the datapath's m_axis_pcm_tuser: stream s lands at base + s*stride
        # (stream 0 at the base; stride only engages for s > 0).
        if sound_card and pcm_ring == "bram":
            # On-chip BRAM ring: NO DMA master (not a DMA) and NO DRAM arbitration
            # => sink.ready is constant 1, so mf52 SHED + I6 cannot occur. The read
            # port is an uncached SoCRegion at MILAN_PCM_BRAM_BASE; the pcm CSR block
            # is identical to the DRAM path so the ring ABI is unchanged
            # (N=1 stays byte-identical to the flat ring).
            self.pcm = _PCMRingBRAM(n_streams=num_streams, ring_bytes=MILAN_PCM_BRAM_SIZE,
                                    data_width=data_width)
            soc.bus.add_slave("milan_pcm_bram", self.pcm.bus,
                              region=SoCRegion(origin=MILAN_PCM_BRAM_BASE,
                                               size=MILAN_PCM_BRAM_SIZE, cached=False))
        elif sound_card and num_streams > 1:
            self.pcm = _PCMRingNxN(mk_bus(), n_streams=num_streams)
            dma_bus.add_master("milan_dma_pcm", master=self.pcm.writer.bus)
        elif sound_card:
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
        pcm_dp = (_axis_dp_cdc(self, "dma_pcm_cdc", Lp, milan_cd,
                               to_datapath=False, depth=128)
                  if sound_card else None)
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
        ]
        if sound_card:
            # PCM: datapath PCM endpoint (sys side) -> ring writer.sink.
            # tlast is NOT forwarded - same reason as the TS ring above: the
            # LiteX ctrl FSM restarts offset on sink.last, and PCM leaves the
            # datapath as one AXIS frame per AAF PDU.
            self.comb += [
                self.pcm.sink.valid.eq(pcm_dp.sys.valid),
                self.pcm.sink.data.eq(pcm_dp.sys.data),
                pcm_dp.sys.ready.eq(self.pcm.sink.ready),
            ]
        if sound_card and num_streams > 1:
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
        # ---- optional PCM playback ring -> KL_pcm_tx pair source ----
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
        if sound_card and aaf_playback:
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
            # BUS ERRORS on the DDR3 fetch path. NOT a duplicate of under/over:
            # those two are ring-flow faults the FSM can see, this one is the
            # INTERCONNECT failing a read. It was invisible until 2026-08-11 -
            # see the err arm in the READ state below for why it silently
            # corrupted audio. Saturating, not wrapping: a count that rolls to
            # zero reads as "no errors", and this must never lie.
            self._pb_bus_err = CSRStatus(32, description="DDR3/interconnect read errors on the playback fetch path (saturating). Nonzero = fetched samples were replaced with digital silence; the audio is not bit-exact.")
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
            # THE ERROR ARM (2026-08-11). Wishbone's `err` is not an alternative
            # to `ack` on this path - LiteX's wishbone2axi asserts BOTH in its
            # error state, so a bare `If(ack, ...)` accepts a FAILED read and
            # latches whatever dat_r happens to hold. Verified in the flashed
            # build's own netlist (gateware/alinx_ax7101.v): the error state
            # drives `..._ack = 1'd1; ..._err = 1'd1;` together, the FSM tests
            # `if (milandma_aafpb_wb_ack)` alone, and `milandma_aafpb_wb_err`
            # occurs exactly twice in the whole file - its declaration and its
            # assign. ZERO consumers. An undefined 64-bit word therefore went
            # into KL_pcm_tx as a valid PCM sample, in a hard-real-time audio
            # path, with nothing to observe it by.
            # The substitution is DIGITAL SILENCE rather than a stall: refusing
            # to answer would hang KL_pcm_tx, which waits for the word it asked
            # for (KL_pcm_tx.sv:84 "any latency" means any, not never). Silence
            # keeps the grid running and makes the damage bounded, deterministic
            # and - via _pb_bus_err - visible.
            pb_err_cnt = Signal(32)
            self.comb += self._pb_bus_err.status.eq(pb_err_cnt)
            fsm.act("READ",
                self.aafpb_wb.cyc.eq(1), self.aafpb_wb.stb.eq(1),
                self.aafpb_wb.adr.eq(pb_addr_l[shift:]), self.aafpb_wb.sel.eq(2**nb - 1),
                If(self.aafpb_wb.ack,
                    If(self.aafpb_wb.err,
                        NextValue(pb_data_l, 0),
                        # saturate: 0xFFFFFFFF is "at least this many", never 0
                        If(pb_err_cnt != 2**32 - 1,
                           NextValue(pb_err_cnt, pb_err_cnt + 1)),
                    ).Else(
                        NextValue(pb_data_l, self.aafpb_wb.dat_r),
                    ),
                    NextState("RESP")))
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
        pcm_ports = dict(
            o_m_axis_pcm_tdata=Signal(64), o_m_axis_pcm_tkeep=Signal(8),
            o_m_axis_pcm_tvalid=Signal(), o_m_axis_pcm_tlast=Signal(),
            o_m_axis_pcm_tuser=Signal(4), i_m_axis_pcm_tready=1,
        )
        if sound_card:
            pcm_ports = dict(
                o_m_axis_pcm_tdata=pcm_dp.dp.data,
                o_m_axis_pcm_tkeep=pcm_dp.dp.keep,
                o_m_axis_pcm_tvalid=pcm_dp.dp.valid,
                o_m_axis_pcm_tlast=pcm_dp.dp.last,
                i_m_axis_pcm_tready=pcm_dp.dp.ready,
                o_m_axis_pcm_tuser=(pcm_dp.dp.user if num_streams > 1 else Signal(4)),
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
            # PCM: the optional host-facing capture ring. With sound_card=0
            # all outputs terminate here and ready is tied high; the media
            # render/loopback paths remain inside milan_datapath.
            **pcm_ports,
            # Optional playback ports (empty unless the internal feature is enabled)
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

    # ---- Phase-0 reader probes (docs/fpga/PIPELINE_STAGES.md) ---------------------------
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

    # ---- M1 probes (docs/findings/PERFORMANCE_GOAL.md) ----------------------------------
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


class _PPMemDiag(LiteXModule):
    """Bus-level diagnosis for the protocol processor's two main-memory bridges.

    WHY THIS EXISTS. On 2026-08-13 the flashed entity answered every AECP
    command with ENTITY_MISBEHAVING because neither main-memory master
    completed a transaction. The processor's own snapshot named the symptom
    (descriptor-store fault 8 = FAULT_TIMEOUT, response-buffer fault 1 =
    FAULT_WTMO, image invalid) and no register anywhere separated the two
    causes that produce it: a bridge that NEVER ASKED the bus, and a bridge
    that asked and was never answered. Those have nothing in common - the
    first is a dead request path inside the fabric, the second is the bus -
    and telling them apart from the board took a week and several wrong
    hypotheses. `milan_aaf_pb` had `_pb_bus_err` and was diagnosable in one
    read; these two had nothing.

    THE DISCRIMINATOR, which is the whole point of the block:

        issued == 0, stat[4] == 0        the bridge is HELD OFF the bus: the
                                         BIOS has not handed the DFI back to
                                         the LiteDRAM controller yet. Expected
                                         between FPGA configuration and the end
                                         of `sdram_init`
        issued == 0, stat[4] == 1        the bridge never asked. Look at the
                                         processor's request face, not the bus
        issued > acked+errored+timed_out  it asked and is UNANSWERED right now
                                         (`stat` names which face still holds
                                         the bus)
        timed_out > 0                    it asked, the watchdog gave up, and
                                         the master is poisoned until the
                                         memory pays its debt

    SATURATING at 65,535, the project convention: a wrapped counter reads as a
    small number and lies, and 0xFFFF means "at least that many" (the same rule
    `_pb_bus_err` and the `PBK_RAILS` rails follow). 16 bits, not 32, because
    area is the binding constraint at 99.88% slice occupancy and a control-path
    fault that has happened 65,535 times needs no more resolution than that.

    PURE OBSERVER. Everything below is derived from signals the bridges already
    drive; no FSM arm changed, so the counters cannot alter the behaviour they
    are there to measure (`syn/yosys/check_tap_purity.sh`'s rule).
    """

    #: Liveness tag in `stat[31:24]`, the same 0x5B the fabric publishes in
    #: A_PP_STAT. Without it "every counter reads 0" is ambiguous between a
    #: bitstream built before these counters existed and a bridge nothing has
    #: ever asked for anything, which is exactly the confusion this block is
    #: here to end.
    TAG_C = 0x5B

    def __init__(self, faces, mem_rdy=None):
        """`faces` = [(name, wishbone, poison flag, watchdog-fire pulse), ...].

        `mem_rdy` is the gate that keeps both bridges off the bus until the
        BIOS has finished with the DDR3 (see `pp_mem_gate`). Without it
        published, `issued` = 0 stays ambiguous between the two things it now
        means - a dead request path inside the fabric, and a bridge
        deliberately holding back - which is the same ambiguity this block
        exists to end.
        """
        flags = []
        for name, wb, psn, tmo_pulse in faces:
            iss  = Signal(16)
            ackd = Signal(16)
            errd = Signal(16)
            tmod = Signal(16)
            on   = Signal()      # this master is asking the bus this cycle
            on_q = Signal()
            self.comb += on.eq(wb.cyc & wb.stb)
            self.sync += on_q.eq(on)
            # ISSUED counts the START of an access, not the cycles it is held.
            # Both FSMs hold cyc/stb until the access ends and pass through a
            # non-bus state (EMIT / WDONE / IDLE) before the next one, so every
            # access is ONE contiguous run of cyc&stb and its rising edge is
            # the request. Counting cycles instead would report one request per
            # held cycle - a whole watchdog's worth of them for the single
            # access that hangs, the reading this register exists to prevent.
            #
            # ACKED and ERRORED are gated on `on` because LiteX's
            # Wishbone2AXILite raises `err` WITH `ack` (axi_lite_to_wishbone.py
            # ERROR state), so the two are one event with two outcomes, and
            # because an answer owed to an abandoned access can land while this
            # master is asking for nothing at all.
            #
            # TIMED OUT is the watchdog-fire pulse, which is the ONLY thing
            # that sets either poison flag (the `_dto == _pp_tmo` arms below
            # are its only writers), so this counts watchdog fires and not
            # poison state.
            for cnt, ev in ((iss,  on & ~on_q),
                            (ackd, on & wb.ack & ~wb.err),
                            (errd, on & wb.ack & wb.err),
                            (tmod, tmo_pulse)):
                self.sync += If(ev & (cnt != 2**16 - 1), cnt.eq(cnt + 1))
            req = CSRStatus(32, name=f"{name}_req", description=(
                f"{name} bridge bus requests (saturating at 0xFFFF): "
                "[31:16] accesses ISSUED (rising edge of cyc&stb, one per "
                "access), [15:0] accesses the bus ACKED without err. "
                "ISSUED = 0 means this bridge never asked; ISSUED > ACKED + "
                "the two fault counts means an access is outstanding."))
            flt = CSRStatus(32, name=f"{name}_fault", description=(
                f"{name} bridge bus faults (saturating at 0xFFFF): "
                "[31:16] accesses the bus answered with err (ack AND err "
                "together, the LiteX shape), [15:0] accesses the watchdog "
                "abandoned with no answer at all (its budget is derived per "
                "build: see pp_mem_timeout_cycles)."))
            setattr(self, f"{name}_req", req)
            setattr(self, f"{name}_fault", flt)
            self.comb += [req.status.eq(Cat(ackd, iss)),
                          flt.status.eq(Cat(tmod, errd))]
            # Live, not counted: what the bridge is doing AT THIS INSTANT.
            # Two bits per face, in `faces` order: the register map publishes
            # bit positions, so the order is ABI and the caller owns it.
            flags += [psn, on]
        # THE GATE IS APPENDED, so it lands at bit 2 * len(faces) and every bit
        # already published keeps its position. With the two faces this SoC
        # builds that is BIT 4, and the generated netlist is the check rather
        # than this sentence: `status = ({mem_rdy, on1, rpsn, on0, dpsn} |
        # 31'h5b000000)` (alinx_ax7101.v:25786, build_ax7101_eppo_dfigate),
        # i.e. [0] desc poisoned, [1] desc cyc&stb, [2] resp poisoned, [3] resp
        # cyc&stb, [4] the gate. A THIRD FACE WOULD MOVE THE GATE to bit 6,
        # which is why the register map documents bit 4 against the two-face
        # shape and not as a fixed address.
        flags += [C(1, 1) if mem_rdy is None else mem_rdy]
        assert len(flags) <= 24, "the live flags would run into the 0x5B tag"
        self.stat = CSRStatus(32, description=(
            "protocol-processor memory-bridge live state: [0] descriptor "
            "bridge POISONED (a timed-out access is still owed an answer; the "
            "next answer it collects is discarded), [1] descriptor bridge is "
            "driving cyc/stb right now, [2] response bridge poisoned, [3] "
            "response bridge driving cyc/stb, [4] the LiteDRAM DFI handover "
            "has been seen, i.e. the BIOS got past sdram_init (0 = both "
            "bridges answer err without touching the bus, which is why "
            "`issued` is 0). Bit 4 observes LiteDRAM only: the dma_bus slave "
            "is the CPU's coherent-DMA port and nothing here watches it, "
            "[31:24] = 0x5B liveness tag "
            "(a build without these counters reads 0 here)."))
        self.comb += self.stat.status.eq(Cat(*flags) | (self.TAG_C << 24))


# Protocol-processor memory-bridge watchdog ---------------------------------------------------------

#: The PROCESSOR's own no-progress watchdog on each main-memory face, in
#: milan_clk cycles, per BEAT: `DESC_MEM_TMO_CYC_P`
#: (protocol-processor/hdl/top/protocol_processor_top.sv:113), consumed as
#: `MEM_TIMEOUT_CYC_P` by KL_aecp_desc_store.sv:304 and KL_aecp_resp_buf.sv:243.
#: Mirrored here because a Python elaboration cannot read a SystemVerilog
#: parameter; `test_pp_mem_bridge.py` reads the .sv and fails if the two drift
#: apart, which is the only reason mirroring it is allowed at all.
PP_PROC_MEM_TMO_CYC = 4096

#: Share of the processor's budget the BRIDGE is allowed to spend before it
#: reports. Three quarters: the cost of reporting LATE is bounded (the bus is
#: already dead and the timeout does not release it - see below), while the cost
#: of reporting EARLY is a wrong answer on a healthy bus, so the trade favours
#: spending as much of the budget as the ceiling allows.
PP_MEM_TMO_SHARE = (3, 4)


def pp_mem_bus_worst_cycles(sys_clk_hz):
    """Worst case, in sys cycles, from a bridge entering its bus state to `ack`.

    THE COUNTER STARTS ON ENTRY TO THE BUS STATE, so it measures ARBITRATION
    WAIT plus memory latency, not memory latency alone. The arithmetic, from the
    LiteX arbiter and from what the other masters on `dma_bus` actually do:

      * the arbiter re-arbitrates only on
        ``rr_read.ce = ~(ar.valid | r.valid) & rd_lock.ready``
        (litex/soc/interconnect/axi/axi_full.py:1188; `ready` is that counter's
        own alias for `empty`, same file:1113, and `empty` is the spelling the
        generated netlist carries, `socbushandler1_rd_lock_empty`). `r.valid`
        there is the SLAVE's, so the grant is held for as long as the granted
        master leaves a read beat UNACCEPTED - the term the old 2,048 left out
        entirely;

      * eight masters share the bus but only SIX ever assert `ar.valid`: the ts
        and pcm rings are WishboneDMAWriters with `we` tied 1 (netlist:
        `assign milandma_interface0_we = 1'd1`), so they never contend for the
        READ channel at all;

      * the lap is ONE lap, not a livelock: migen's SP_CE round-robin moves the
        grant to the first requester in i+1..i+n-1 order, so each of the other
        five is granted AT MOST ONCE before this master;

      * and the lap is DOMINATED by the TX ring reader, not by memory. Its
        `r.ready` is the TX datapath's backpressure (RingDMAReader's PAY_R:
        `self.bus.r.ready.eq(source.ready | cs_pass)`) behind a 16-deep CDC
        FIFO (`_axis_dp_cdc` default depth), and what stalls the
        datapath is the per-frame TX grant (CBS shaper + MAC store-and-forward),
        i.e. a FRAME time and not a memory time. Silicon measured that
        backpressure at 39% of the reader's cycles.

    `MEM` below is the SILICON-measured round trip on THIS bus: L_pay = 45
    cycles = 450 ns (docs/findings/PERFORMANCE_GOAL.md:155). It is NOT the 1,424
    ns the old comment cited: that is a CPU-side random DRAM miss, half of it a
    713 ns sv39 page-table walk no DMA master ever pays.

    WHY THE COUNTER CANNOT JUST STOP WHILE IT WAITS FOR THE GRANT, which is the
    first idea anyone has on reading the above, and it is dead: the master
    cannot SEE arbitration. Its face is Wishbone (cyc, stb, we, adr, dat_w, sel
    out; ack, dat_r, err back) and not one of those carries a grant, so from the
    bridge FSM "queued behind five masters" and "granted, memory is slow" are
    the same silence. The only signal that separates them is `_cmd_done` inside
    LiteX's Wishbone2AXILite, set when `ar` is accepted and therefore meaning
    exactly "granted, now waiting for data" - and it is a plain local `Signal()`
    (axi_lite_to_wishbone.py:159), never bound to the converter object, so
    nothing outside that FSM can reference it without patching vendored LiteX.
    The wait is ONE indivisible number. Budgeting for all of it, which is what
    this function does, is the only honest option rather than the cheapest one.

    Conservative by construction: it prices every optional master (both RX
    queues, the AAF playback fetch) whether or not this build elaborates them.
    """
    MEM   = 45                                  # AR -> first R, measured
    # one maximum-size frame on the wire, 1,522 bytes + preamble/SFD + IFG
    FRAME = -(-(1522 + 8 + 12) * 8 * int(sys_clk_hz) // 1000000000)
    return (FRAME + MEM + 64          # TX ring reader: grant wait + 64 beats
            + 2 * (MEM + 2)           # 2 RX ring writers: BD reads, <=2 beats
            + (MEM + 1)               # AAF playback fetch: 1 beat
            + (MEM + 1)               # the other processor bridge: 1 beat
            + MEM)                    # our own access, once granted


def pp_mem_timeout_cycles(sys_clk_hz, milan_clk_hz,
                          proc_tmo_cyc=PP_PROC_MEM_TMO_CYC,
                          share=PP_MEM_TMO_SHARE):
    """The bridge watchdog in sys cycles. Derived, because the RELATION is what
    the design depends on and a bare number only satisfies it by accident.

    THE CEILING. The bridge must report BEFORE the processor's own per-beat
    watchdog or the submodule records silence where the truth is a failed bus.
    The two counters run in DIFFERENT CLOCK DOMAINS - the bridge FSM in sys, the
    processor in milan_cd - so "first" is a comparison in TIME, and cycle counts
    alone do not settle it. A fixed 2,048 held at the shipping AX shape only
    because milan and sys are both 100 MHz there; it was generous on the Arty
    shape (milan 50, sys 83.333) and it INVERTS on any build with milan faster
    than sys, silently, with nothing to catch it.

    The processor is also AHEAD: its counter starts on `mreq_valid_r`
    (KL_aecp_desc_store.sv:500), before the request has crossed the CDC into the
    sys domain, while `_dto` starts when this FSM enters its bus state. The
    quarter of the budget left unspent covers that skew several thousand times
    over.

    WHAT THE TIMEOUT DOES NOT BUY, so nobody re-derives this on a false premise:
    it does not release the AXI read channel. LiteX's Wishbone2AXILite holds
    `ar.valid` in its READ state with no `cyc` term at all
    (axi_lite_to_wishbone.py:223), so dropping cyc/stb abandons the access at the
    WISHBONE layer only. What it buys is that the PROCESSOR gets an answer and
    this FSM re-arms - which is why reporting late is cheap and reporting early
    is not.
    """
    num, den = share
    cyc = int(proc_tmo_cyc * num * int(sys_clk_hz) // (den * int(milan_clk_hz)))
    # Strictly first IN TIME. Belt and braces on the truncation above, and the
    # one check that must never be relaxed: without it the processor's watchdog
    # wins the race and the fault it records is "no progress", not "the bus".
    if cyc * int(milan_clk_hz) >= proc_tmo_cyc * int(sys_clk_hz):
        raise RuntimeError(
            f"the protocol-processor memory-bridge watchdog ({cyc} sys cycles "
            f"at {sys_clk_hz/1e6:g} MHz) does not expire before the "
            f"processor's own {proc_tmo_cyc}-cycle per-beat watchdog at "
            f"{milan_clk_hz/1e6:g} MHz: the bridge would not report first")
    # And it must still clear the bus. A clock pair that cannot satisfy both
    # ends is a REFUSAL, not a number to round up: every access would time out
    # spuriously under TX load and every AECP command would answer wrongly.
    worst = pp_mem_bus_worst_cycles(sys_clk_hz)
    if cyc <= worst:
        raise RuntimeError(
            f"the protocol-processor memory-bridge watchdog ({cyc} sys cycles) "
            f"is inside the worst-case dma_bus wait ({worst} sys cycles at "
            f"{sys_clk_hz/1e6:g} MHz): a healthy bus would time out. "
            f"milan_clk {milan_clk_hz/1e6:g} MHz is too fast against sys")
    return cyc


def pp_mem_gate(m, dfi_sel):
    """`mem_rdy`: the DFI has been handed BACK to the LiteDRAM controller.

    A LEVEL, and it is READ from LiteDRAM rather than restated: the BIOS takes
    the DFI away from the controller to level the DDR3 ("Switching SDRAM to
    software control") and hands it back when it is done. `sel` RESETS TO 1
    (litedram/dfii.py DFIInjector, `reset=0b1  # Defaults to HW control.`), so
    hardware control on its own is not evidence that the BIOS ever ran. The
    1 -> 0 -> 1 edge is, and only that edge opens this gate.

    WHAT IT OBSERVES IS ONE HOP, and the label has to say so: that the BIOS got
    past `sdram_init`. It does not observe the CPU's coherent-DMA port, which
    is the block that took the AR and never answered it (see the bridge below),
    and it cannot - nothing on that path publishes a ready. What defends the
    gate is WHERE IT SITS IN TIME, not what it measures.

    Factored out of `MilanSoC.__init__` so `test_pp_boot_bus_freeze.py` drives
    THIS expression and not a copy of it: a copy passes against a gate wired to
    a constant, which is the failure that test was written to catch.
    """
    _sw_seen = Signal()
    _mem_rdy = Signal()
    m.sync += If(~dfi_sel, _sw_seen.eq(1))
    m.comb += _mem_rdy.eq(_sw_seen & dfi_sel)
    return _mem_rdy


def pp_desc_bridge(m, req, rsp, wb, mem_rdy, tmo, sel_mask, addr_sh):
    """The descriptor-image read bridge: one wishbone READ master, one FSM.

    `req`/`rsp` are the processor's sys-domain request and response faces, `wb`
    the master this drives, `mem_rdy` the gate above, `tmo` the watchdog in sys
    cycles. Returns `(fsm, poisoned, poison_set)`; the caller owns the
    attribute the FSM is named by and the observer that reads the two flags.

    A FUNCTION AND NOT AN INLINE BLOCK because the behaviour has to be
    simulable: `MilanSoC` cannot be elaborated in a migen simulation (it wraps
    a `milan_datapath` blackbox on a Vivado platform), so before this was
    factored out the boot-freeze simulation drove a REPLICA of these arms and
    graded the shipping shape by parsing this file for the identifier
    `_mem_rdy`. That grades spelling. `test_pp_boot_bus_freeze.py` now builds
    what is below, on the real LiteX interconnect, and fails against a gate
    that is present and ineffective.

    THE ARMS THEMSELVES ARE UNCHANGED by the move, and the check that says so
    is a gateware export (`--output-dir`, no `--build`) diffed against the
    export of the tree the waiting bitstreams were built from: identical RTL,
    to the character, comments and the CPU blackbox hash aside. Keep it that
    way - a refactor here that moves a signal name reshapes the netlist, and
    the bitstreams stop corresponding to the source.
    """
    _da = Signal(32); _dl = Signal(9)
    _dd = Signal(64); _de = Signal()
    _dto = Signal(max=tmo + 1)
    # A timed-out access is ABANDONED, not cancelled: AXI forbids retracting a
    # VALID before its READY, so the memory still owes one answer and delivers
    # it whenever it comes back. The master is POISONED until that answer
    # lands, and poisoned means THE NEXT ANSWER IS NOT MINE: the transaction in
    # flight is reported `err` and whatever comes back on it is discarded,
    # which is what keeps a stale word from being paired with a new address.
    #
    # POISONED, THE BUS STATE STILL DRIVES cyc/stb, and that is the only way
    # the flag can clear. Without a coherent `dma_bus` these masters land on
    # `self.bus`, whose Arbiter gates every slave->master signal on the grant
    # (wishbone.py Arbiter: `dest.eq(source & (rr.grant == i))`) and drives the
    # requests from the masters' own `cyc`, so an answer owed to a master that
    # is asking for nothing goes to whoever holds the bus instead. A master
    # that answered `err` without touching the bus could therefore never be
    # given the ack its flag waits for: every later descriptor read would fail
    # for the life of the bitstream, which is a reset and not a stall. The
    # price is one more watchdog (20.5 us) per attempt while the memory is
    # still dead, still inside the processor's own 4,096-cycle per-beat
    # watchdog.
    #
    # ONE answer can be owed, never two, so one bit counts the debt:
    # Wishbone2AXILite (axi_lite_to_wishbone.py:148) samples `stb & cyc` in
    # IDLE alone and returns there only on the AXI response, so it cannot take
    # a second access while one is outstanding - a watchdog firing again while
    # poisoned re-abandons that SAME access. `err` rides WITH `ack` on a failed
    # access (same file, ERROR state) and either settles the debt. The debt is
    # watched in EVERY state and not from the bus state's own arm, because on a
    # `dma_bus` each master owns its converter (SoCBusHandler.add_master adapts
    # per master) and that converter's `ack` is combinational on the AXI
    # response: the answer can land on a master that has already let go.
    _dpsn = Signal(); _dpsn_set = Signal()
    m.sync += If(_dpsn_set, _dpsn.eq(1)
              ).Elif(_dpsn & (wb.ack | wb.err), _dpsn.eq(0))
    _dfsm = FSM(reset_state="IDLE")
    # THE GATE IS AN ANSWER, NOT A STALL. Holding `ready` low would park the
    # request until the processor's own 4,096-cycle watchdog noticed, and would
    # report "no progress" where the truth is "the BIOS has not finished with
    # the DDR3". Taking the request and answering `err` on the spot degrades
    # the locate to NO_SUCH_DESCRIPTOR immediately, leaves `issued` at 0 - the
    # discriminator `_PPMemDiag` exists for - and never puts a transaction on a
    # bus that may not be able to end one.
    _dfsm.act("IDLE",
        req.ready.eq(1),
        If(req.valid,
            NextValue(_da, req.addr), NextValue(_dl, req.beats),
            NextValue(_de, _dpsn | ~mem_rdy), NextValue(_dto, 0),
            If(mem_rdy, NextState("RD")).Else(NextState("EMIT"))))
    _dfsm.act("RD",
        wb.cyc.eq(1), wb.stb.eq(1), wb.sel.eq(sel_mask),
        wb.adr.eq(_da[addr_sh:]),
        NextValue(_dto, _dto + 1),
        If(wb.ack,
            NextValue(_dto, 0),
            # `_de` is already set when this access is the one that collects an
            # owed answer, so the word is taken and thrown away with the beat
            # rather than reaching the processor.
            If(wb.err, NextValue(_de, 1)
            ).Else(NextValue(_dd, wb.dat_r)),
            NextState("EMIT")
        ).Elif(_dto == tmo,
            NextValue(_dto, 0), NextValue(_de, 1),
            _dpsn_set.eq(1), NextState("EMIT")))
    _dfsm.act("EMIT",
        rsp.valid.eq(1), rsp.err.eq(_de),
        rsp.blast.eq((_dl == 1) | _de),
        rsp.data.eq(Cat(_dd[56:64], _dd[48:56], _dd[40:48], _dd[32:40],
                        _dd[24:32], _dd[16:24], _dd[8:16], _dd[0:8])),
        If(rsp.ready,
            If(_de | (_dl == 1), NextState("IDLE")
            ).Else(NextValue(_da, _da + 8), NextValue(_dl, _dl - 1),
                   NextValue(_dto, 0), NextState("RD"))))
    return _dfsm, _dpsn, _dpsn_set


# SoC ----------------------------------------------------------------------------------------------

class MilanSoC(SoCCore):
    def __init__(self, platform, sys_clk_freq, xlen=64, cpu_count=1,
                 with_milan=True, with_mac=False, with_dma=False, with_dram=False,
                 with_spiflash=False, flashboot="none", gtx_tx_invert=False,
                 main_ram_size=0x8000, milan_clk_freq=None, coherent_dma=False,
                 rgmii_tx_delay=2e-9, rgmii_rx_delay=2e-9, l2_bytes=None, with_fpu=False,
                 extra_scala_args=None, cpu="naxriscv", rx_queues=1, rx_rsc=True,
                 strip_probes=False, hs_page_bytes=4096, legacy_ring=False,
                 rx_fifo_beats=2048, board="ax7101", eth_phy_index=0,
                 num_streams=1, audio_if_slots=0, talker_wire_chans=2,
                 audio_if_master=False,
                 pcm_ring="dram", sound_card=False, aaf_playback=False,
                 aaf_pb_streams=1,
                 loopback_lane=False,
                 bus_standard="wishbone",
                 software_profile="baremetal",
                 gptp_plane=None,
                 render_lpf=True, optional_blocks=None,
                 cbs_queues_mask=None, entity_gen_dir=None, **kwargs):
        self._cpu_xlen = int(xlen)
        if software_profile != "baremetal":
            raise ValueError("unsupported software profile")
        # Resolve the one PHC owner once, before it fans out into RTL, firmware
        # constants and the flash artifact contract.  `none` is a real state
        # for the documented --no-milan bare-SoC path; a missing value is not
        # allowed to masquerade as that state because old/partial layouts must
        # fail closed at deployment.
        if not with_milan:
            self._gptp_owner = "none"
        elif gptp_plane is True:
            self._gptp_owner = "fabric"
        elif gptp_plane is False:
            # Verification-only option-off elaboration: this image runs no
            # time-sync owner. Recording "none" keeps deployment tools from
            # accepting it as a product image.
            self._gptp_owner = "none"
        else:
            raise ValueError(
                "MilanSoC needs a resolved gptp_plane=True/False when the "
                "Milan datapath is present")
        # ---- RISC-V core(s). Two cores are supported, selected by
        #      `cpu`: NaxRiscv (out-of-order, high IPC, ~100 MHz on this -2 Artix) or
        #      VexiiRiscv (in-order, higher fmax + smaller  -  the AVB-switch direction,
        #      see AVB_SWITCH_DIRECTION.md "CPU budget"). Both expose an AXI
        #      `dma_bus` (soc.dma_bus) that the Milan DMA masters attach to identically;
        #      it is coherent only for cache-bearing CPU profiles
        #      (MilanDMA reads getattr(soc, "dma_bus", soc.bus)), and BOTH map csr @
        #      0xf000_0000 / clint @ 0xf001_0000 / plic @ 0xf0c0_0000  -  so the datapath
        #      and the ring DMA port over with no address changes.
        if cpu == "vexiiriscv":
            from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
            _vex_parser = argparse.ArgumentParser()
            VexiiRiscv.args_fill(_vex_parser)
            _vex_args, _ = _vex_parser.parse_known_args([])
            # cpu_variant is a SoCCore-level argument (not in the CPU parser).
            _vex_args.cpu_variant = "baremetal"
            _vex_args.cpu_count   = cpu_count
            _vex_args.with_dma    = coherent_dma          # coherent AXI dma_bus
            # The cacheless core trades latency for gates: its direct fetch/data
            # TileLink paths trade latency for gates. Clock the CPU side with the
            # already-present 50 MHz Milan domain; Vexii inserts its supported
            # CPU/LiteX CDC when --with-cpu-clk is selected.  The sys fabric and
            # audio reference stay at their silicon-proven 100 MHz recipe.
            _vex_args.with_cpu_clk = bool(milan_clk_freq)
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
            kwargs["cpu_variant"] = _vex_args.cpu_variant
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
        # BIOS ROM is always integrated. Main RAM is external LiteDRAM when
        # requested, otherwise integrated SRAM. Do not add integrated
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
                         ident=(f"Milan TSN SoC - {_cpu_human} RV{xlen} "
                                f"{cpu_count}-core {software_profile}"),
                         **kwargs)
        # Compiled into soc.h so layout_from_soch.py can reconstruct the exact
        # ownership state for sweep artifacts without consulting a launcher or
        # mutable launch state. Encoding: 0=none, 1=fabric.
        self.add_constant("MILAN_GPTP_OWNER",
                          GPTP_OWNER_CODES[self._gptp_owner])
        # The deploy preflight binds the compiled CPU width as part of the
        # bare-metal artifact identity.  Sweep layouts reconstruct this value
        # from soc.h rather than trusting a launcher.
        self.add_constant("MILAN_CPU_XLEN", self._cpu_xlen)
        self.add_config("BIOS_NO_BOOT")

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
        if hasattr(self.cpu, "cpu_clk"):
            # with_cpu_clk makes this an explicit asynchronous CPU boundary;
            # the generated Vexii wrapper retains litex_clk/reset on cd_sys.
            self.comb += self.cpu.cpu_clk.eq(ClockSignal("milan"))

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
                # The product profile is cacheless end to end.
                l2_cache_size = 0)

        # ---- QSPI config flash (memory-mapped) + selected boot manifest ----
        # Maps the on-board 16 MiB part into the CPU address space. `flashboot`
        # selects whether deployment carries the bitstream/AEM pair.
        if with_spiflash:
            from litespi.modules import N25Q128A13, S25FL128S
            from litespi.opcodes import SpiNorFlashOpCodes as SpiCodes
            # Arty A7-100: S25FL128S (16 MB, same geometry class as the N25Q128).
            # Both boards use the same timing-robust single-lane recipe.
            # The litespi S25FL128S table only
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
            # reads (silicon 2026-07-10: short probes passed, then a large-image
            # length word read as garbage). The compiled divisor is the one with
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
            aaf_pb = bool(aaf_playback) and bool(sound_card) and with_dma
            if aaf_playback and not with_dma:
                print("[milan] --aaf-playback ignored without --with-dma/--full")
            if with_dma:
                self.milan_dma = MilanDMA(self, data_width=64, milan_cd=milan_cd,
                                          rx_queues=rx_queues, rx_rsc=rx_rsc,
                                          hs_page_bytes=hs_page_bytes,
                                          legacy_ring=legacy_ring,
                                          rx_fifo_beats=rx_fifo_beats,
                                          num_streams=int(num_streams),
                                          pcm_ring=pcm_ring, sound_card=bool(sound_card),
                                          aaf_playback=aaf_pb,
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
                # Phase-0 reader instrumentation (docs/fpga/PIPELINE_STAGES.md): measure
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
                    # ---- M1 (docs/findings/PERFORMANCE_GOAL.md): campaign probes ----
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
                # `lrclk` is an AX7101-only J11 media-grid TEST POINT, not a
                # required member of a TDM resource.  The Arty Pmod header has
                # the five bus signals above and legitimately omits it, so the
                # subsignal's presence - not merely `tdm_pads` - decides
                # whether the observation output reaches a package pin.
                _media_lrclk = getattr(self.tdm_pads, "lrclk", None)
                dp_ports.update(
                    # TDM8 divides the audio clock itself (no cd_audio_tdm -
                    # see the audio_tdm_hz note above); TDM16/32 get the
                    # dedicated MMCM output
                    i_clk_tdm_i   = ClockSignal("audio_tdm" if audio_tdm_hz
                                                else "audio"),
                    o_tdm_bclk_o  = (self.tdm_pads.bclk if self.tdm_pads
                                     else Signal()),
                    o_media_lrclk_o = (_media_lrclk
                                       if _media_lrclk is not None
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
            # WHERE THE ENTITY MODEL LIVES. The processor's descriptor store
            # fetches the AEM image from main memory at a COMPILE-TIME base -
            # its design holds no base register, so software cannot point it
            # somewhere wrong at runtime. Software loads the image there before
            # enabling the entity; an unloaded (zeroed) region is caught by the
            # image header's magic/version/checksum, so it reads as "not
            # loaded" rather than as a valid empty model.
            #
            # THE BASE COMES FROM THE END-STATION CONFIG, NOT FROM THIS SoC.
            # Deriving it here as "top of main_ram" is what the previous
            # revision did, and it was WRONG in both directions: the only
            # region reserved for PCM is the ring, which this build
            # places at 0x7F800000, so the top megabyte of a 1x1 board is
            # ordinary kernel RAM - and the response buffer WRITES there. At
            # the 8x8 shape the ring is 8 MiB and swallows the top megabyte
            # outright, so the two would have shared it. A base that the DT
            # does not reserve is silent corruption: no counter reports it and
            # the entity still answers.
            #
            # So the window is READ from the config's platform shape - the same
            # value that generated the `ppmem` no-map reservation in the device
            # tree the kernel honours - and only CHECKED here.
            _ram = self.bus.regions["main_ram"]
            _shape = _platform_shape(entity_gen_dir)
            _desc_base  = int(_shape["pp_mem"]["phys"], 16)
            _PP_WINDOW  = int(_shape["pp_mem"]["bytes"], 16)
            _pcm_shape  = _shape.get("pcm")
            # Refuse rather than build a bitstream that writes where it must
            # not. Both failures are invisible on silicon: one corrupts kernel
            # memory, the other corrupts captured audio.
            if _desc_base < _ram.origin or (
                    _desc_base + _PP_WINDOW) > (_ram.origin + _ram.size):
                raise RuntimeError(
                    f"the protocol processor's window "
                    f"0x{_desc_base:08x}+0x{_PP_WINDOW:x} is not inside "
                    f"main_ram 0x{_ram.origin:08x}+0x{_ram.size:x}")
            if _pcm_shape is not None:
                _ring_phys  = int(_pcm_shape["ring_phys"], 16)
                _ring_bytes = int(_pcm_shape["ring_bytes"], 16)
                if (_desc_base + _PP_WINDOW) > _ring_phys and (
                        _ring_phys + _ring_bytes) > _desc_base:
                    raise RuntimeError(
                        f"the protocol processor's window "
                        f"0x{_desc_base:08x}+0x{_PP_WINDOW:x} overlaps the PCM "
                        f"ring 0x{_ring_phys:08x}+0x{_ring_bytes:x}")
            # ...AND WHERE THE AECP RESPONSE BUFFER LIVES. Same reserved window,
            # same derivation from the SoC's own map, one extra rule: this
            # region is WRITTEN by the processor, so it must not overlap the
            # descriptor image. It cannot, and here is the arithmetic rather
            # than the assertion:
            #   * the image starts at `_desc_base` (the FOOT of the window) and
            #     grows UPWARD. The largest one this project builds is 23,216
            #     bytes, at the 8x8 shape;
            #   * the buffer is 16 + PP_DESC_LINE_BYTES_P = 592 bytes and sits
            #     in the LAST 4 KiB of the same window, 0x100000 - 0x1000 =
            #     1,044,480 bytes above the image's first byte.
            # So the two collide only if the entity model grows past a megabyte
            # - forty-five times the largest shape in the tree - and the window
            # would run into the PCM ring first, which the check above refuses.
            # Both bases are DERIVED from the ring base and ONE window constant,
            # so moving the reserved band moves both together.
            _resp_base = _desc_base + _PP_WINDOW - 0x1000
            # Published for the manifest that ships with the image. The loader
            # must not restate this address: it is compiled into the gateware,
            # so a loader that guesses it writes the model somewhere the store
            # will never look and the entity stays silent with no error.
            self._pp_windows = {"desc_base": _desc_base,
                                "resp_base": _resp_base,
                                "window_bytes": _PP_WINDOW}
            self.milan = MilanNIC(platform, axil, dma_mac_ports=dp_ports or None,
                                  desc_base=_desc_base, resp_base=_resp_base,
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
                                  # Preserve None so add_milan_datapath catches
                                  # a severed ownership carrier.
                                  gptp_plane=gptp_plane,
                                  sound_card=bool(sound_card),
                                  aaf_playback=aaf_pb,
                                  aaf_pb_streams=int(aaf_pb_streams),
                                  loopback_lane=bool(loopback_lane),
                                  render_lpf=bool(render_lpf),
                                  optional_blocks=optional_blocks,
                                  cbs_queues_mask=cbs_queues_mask,
                                  entity_gen_dir=entity_gen_dir)
            # ===============================================================
            #  AECP DESCRIPTOR-IMAGE READ BRIDGE (protocol-processor 07 §3.3)
            # ===============================================================
            # The processor's descriptor store fetches the entity model from a
            # DDR3 ADDRESS over a read-only master. MilanNIC published the
            # sys-domain endpoints; this is the bus side, a wishbone READ
            # master on the DMA bus - the same shape as `milan_aaf_pb`,
            # extended from one word to a BURST.
            #
            # THE ROUTE IS NOT DIRECT, and every fault report below turns on
            # that: this master's ONLY slave is the CPU's coherent-DMA port
            # ("AXIInterconnectShared (8 <-> 1)"), so an unanswered access is
            # unanswered BY THE CPU's coherency hub. Main memory is two hops
            # further on. See the gate block below.
            #
            # CONTRACT: ONE outstanding request; responses IN ORDER; `beats`
            # counts 64-bit beats (>=1, max 128); `last` ends the burst. A
            # beat carries its LOWEST byte address in bits [63:56] - 1722.1
            # wire order, i.e. BIG-ENDIAN, a byte-reverse of the little-endian
            # words the bus returns.
            #
            # THE ERROR ARM IS NOT OPTIONAL, and this bus has already charged
            # for that lesson once: LiteX's wishbone2axi asserts `err`
            # TOGETHER WITH `ack`, so `If(ack, ...)` alone accepts a FAILED
            # read and latches whatever `dat_r` held. The audio path had to
            # substitute silence because KL_pcm_tx has no error input. This
            # master HAS one, so the error is PROPAGATED: the store aborts the
            # burst and degrades that locate to NO_SUCH_DESCRIPTOR. A corrupt
            # descriptor is never served as though it were good.
            #
            # NEITHER IS THE WATCHDOG, and THAT is what the 08-13 board round
            # cost. A timeout is not an error response: LiteX's wishbone2axi
            # answers a failed access with `err` AND `ack` together, so the
            # error arm above never fires for an access that is simply never
            # acked. Every bus state used to leave ONLY on `ack`, so one
            # unanswered access parked the FSM there with `cyc`/`stb` held -
            # and the dma_bus arbiter re-arbitrates only when nothing is
            # outstanding (generated netlist: `rr_read_ce = ~(ar_valid |
            # r_valid) & rd_lock_empty`), so that one access froze the READ
            # half of the bus for EVERY master on it, permanently and with
            # nothing to observe it by. Measured consequence: descriptor store
            # fault 8 = FAULT_TIMEOUT, response buffer fault 1 = FAULT_WTMO,
            # image invalid, and every AECP command answered ENTITY_MISBEHAVING
            # - while the write half stayed alive long enough to commit two
            # lanes (dbg_lane_wr = 2), which is what proves the masters
            # themselves transact and the wedge is the missing `ack`.
            #
            # WIDTH. One access per 64-bit beat, `milan_aaf_pb`'s shape and
            # the processor's own lane width, with the address width DERIVED
            # from it rather than restated. The 32-bit master this replaces
            # worked (it up-converted, and both halves of a lane reached the
            # right bytes with the right strobes) but spent two accesses and
            # an inserted converter per beat - two chances to wedge where the
            # protocol has one, and a split-strobe write arm that exists only
            # because the master was narrower than the lane.
            from litex.soc.interconnect import wishbone as _wb
            import math as _math
            _pp_dw   = 64                      # the processor's memory lane
            _pp_selm = 2**(_pp_dw // 8) - 1
            _pp_adrw = 32 - int(_math.log2(_pp_dw // 8))
            _pp_sh   = int(_math.log2(_pp_dw // 8))
            # Watchdog, in sys cycles, DERIVED from the two clocks and the
            # processor's own per-beat budget - see `pp_mem_timeout_cycles` for
            # the ceiling and `pp_mem_bus_worst_cycles` for the floor, both of
            # which this call enforces rather than asserts in prose.
            #
            # WHAT IT REPLACES AND WHY. The number was 2,048, justified against
            # "a 1,424 ns worst-case miss = 143 cycles" with the ARBITER left
            # out. The counter starts on entry to the bus state, so it measures
            # grant wait plus memory, and the grant wait is not a lap of memory
            # latencies: the dma_bus arbiter holds the grant while the granted
            # master leaves a read beat unaccepted, and the TX ring reader is
            # left unaccepted for a per-frame TX grant - 1,542 wire bytes at
            # 1 Gbit = 12.34 us = 1,234 sys cycles at 100 MHz, on its own more
            # than half of the old budget. Priced in full at the shipping AX
            # shape (sys 100 MHz):
            #     TX ring reader   1,234 + 45 + 64 = 1,343
            #     2 RX ring writers      2 x (45 + 2) = 94
            #     AAF playback fetch          45 + 1 = 46
            #     the response bridge         45 + 1 = 46
            #     our own access                       45
            #                                       = 1,574 cycles
            # 2,048 was 1.30x that. The derived value is 3,072 (30.7 us) =
            # 1.95x, and it leaves the processor 1,024 milan cycles of its own
            # budget. It is FREE: migen sizes the counter `Signal(max=n+1)`, and
            # both 2,048 and 3,072 need 12 bits, so no flop and no comparator
            # bit moves.
            #
            # It does NOT make a spurious timeout impossible - nothing under the
            # 4,096-cycle ceiling can, against a term whose scale is a frame
            # time. It makes one improbable, and `_PPMemDiag`'s `timed_out`
            # counter is what will settle the residual from the board instead of
            # from an argument.
            _pp_tmo = pp_mem_timeout_cycles(sys_clk_freq,
                                            milan_clk_freq or sys_clk_freq)
            # ---------------------------------------------------------------
            #  NO BUS ACCESS UNTIL THE BIOS HAS FINISHED WITH THE DDR3
            # ---------------------------------------------------------------
            # A TIMED-OUT ACCESS IS NOT A RELEASED BUS, and that is what the
            # watchdog above cannot do anything about. Dropping `cyc`/`stb`
            # ends the WISHBONE cycle; the AXI transaction it already became
            # cannot be retracted. LiteX's Wishbone2AXILite stays parked in its
            # READ state (it samples `stb & cyc` in IDLE alone), and the
            # arbiter's `rd_lock` still counts the accepted AR, so
            # `rr_read.ce = ~(ar.valid | r.valid) & rd_lock.ready`
            # (axi_full.py:1188; `ready` is that counter's own alias for
            # `empty`, same file:1113) is 0 for the LIFE OF THE BITSTREAM.
            # Measured in simulation against the real LiteX chain
            # (test_pp_boot_bus_freeze.py): rd_lock 1, grant 6, ce 0, another
            # master requesting and never granted. Measured on silicon
            # 2026-08-14: milan_dma_tx_rd_ptr 0, milan_dma_tx_sent 0 and
            # STAT_TX_GOOD 0 after 1,800 s with tx_enable 1 and tx_wr_ptr
            # 0x760 - the CPU transmitted NOTHING all session, because the TX
            # ring reader is a read master on this same bus.
            #
            # WHO NEVER ANSWERED IS NOT THE DDR3, and naming it wrongly sends
            # the next reader to the wrong block. `dma_bus` has EXACTLY ONE
            # SLAVE and it is the CPU: "Interconnect: AXIInterconnectShared
            # (8 <-> 1)" (litex.log:103 of the flashed build) and the slave's
            # AR lands on `milansoc_milansoc_vexiiriscv_dma_bus_ar_valid`
            # (alinx_ax7101.v:12288). What accepted that AR and never returned
            # R is the VexiiRiscv coherent-DMA slave port and its coherency
            # hub; main memory is two hops further on.
            #
            # THE TRIGGER IS UNIDENTIFIED, and this comment says so rather than
            # supplying a mechanism. What is measured: `KL_aecp_desc_store`
            # resets to S_HDR_REQ (KL_aecp_desc_store.sv:449), so it is the one
            # master here that TRANSACTS OUT OF RESET - the response buffer has
            # no software enable either, but resets to R_FILL
            # (KL_aecp_resp_buf.sv:353), which does not transact - and it asks
            # at FPGA-configuration time. The board's receipt is the fresh-boot
            # counter pair: 1 issued, 1 timed out, with no AECP traffic at all.
            # What is NOT known is why that first access was never answered.
            # Two mechanisms were written here before and BOTH ARE REFUTED:
            #   * "the DDR3 is not up yet". At configuration LiteDRAM's own
            #     controller owns the DFI (`sel` resets to 1, litedram/dfii.py
            #     DFIInjector) and `rddata_valid` is a pure latency shift of
            #     `rddata_en` with no dependence on initialisation
            #     (litedram/phy/s7ddrphy.py:510), so an uninitialised but
            #     hardware-controlled LiteDRAM ANSWERS a read, with garbage.
            #   * "nothing is loaded at 0x7F700000 yet". That answers too, and
            #     garbage fails the store's own header check as fault 1 =
            #     FAULT_MAGIC_C, not the fault 8 = FAULT_TIMEOUT_C measured.
            # The one DRAM-side window that can genuinely swallow a read is
            # `sel` = 0, the BIOS's SOFTWARE-CONTROL window, which is DURING
            # `sdram_init` and not before it. That window is inside the one
            # this gate holds shut, but no measurement ties the boot probe to
            # it, and the CPU-side path above is not covered by that reading at
            # all.
            #
            # SO THE GATE IS DEFENDED BY ITS PLACE IN TIME, not by a mechanism:
            # it opens STRICTLY LATER than every boot-window culprit that can
            # be named, which is how it covers one that cannot be. If the board
            # still reads a timed-out boot probe with `stat[4]` = 1, the cause
            # is downstream of the BIOS and this gate was the wrong fix.
            #
            # SAMPLED PER REQUEST, in IDLE, so it can never stall a burst
            # half-way: `sel` drops exactly once, inside the window where the
            # gate is already shut and no burst can be in flight, and nothing
            # in this SoC re-levels afterwards. Without DDR3 main_ram is
            # on-chip and always answerable, so the gate is a constant 1 there.
            if with_dram:
                _mem_rdy = pp_mem_gate(self,
                                       self.sdram.dfii._control.fields.sel)
            else:
                _mem_rdy = C(1)
            _dq = self.milan.descmem_req_sys
            _ds = self.milan.descmem_rsp_sys
            self.descmem_wb = _dwb = _wb.Interface(data_width=_pp_dw,
                                                   adr_width=_pp_adrw,
                                                   addressing="word")
            _dmab = getattr(self, "dma_bus", self.bus)
            _dmab.add_master("milan_desc_mem", master=_dwb)

            # The arms live in `pp_desc_bridge` above, not here, for one
            # reason: this SoC cannot be elaborated in a migen simulation, so
            # arms written inline can only ever be graded by a replica or by
            # parsing this file for an identifier. Both pass against a gate
            # wired to a constant. The export is diffed netlist-identical
            # across the move.
            self.descmem_fsm, _dpsn, _dpsn_set = pp_desc_bridge(
                self, _dq, _ds, _dwb, _mem_rdy, _pp_tmo, _pp_selm, _pp_sh)

            # ===============================================================
            #  AECP RESPONSE-BUFFER READ+WRITE BRIDGE (protocol-processor 03 §7)
            # ===============================================================
            # The bus side of the SECOND master. MilanNIC published four
            # sys-domain endpoints (read request / read response / write /
            # write-done); this is the one wishbone master and the one FSM that
            # serve all four - which is also what gives the contract's ordering
            # rule ("a read accepted after a write reported done observes that
            # write") for free, since nothing here can reorder.
            #
            # THE STROBES ARE THE POINT. `wr_strb` bit n enables byte n of the
            # big-endian lane and A ZERO-STROBE BYTE MUST NOT BE MODIFIED, so
            # the whole strobe rides ONE 64-bit wishbone cycle as `sel` (LiteX
            # forwards `sel` to AXI `wstrb` verbatim). The first lane of every
            # response has an empty low half - the uCPU's 12-byte header record
            # is dropped and the payload starts at byte 12 - which is now just
            # sel = 0xF0 rather than a skipped half-cycle; an ENTIRELY empty
            # strobe is still skipped rather than issued as a sel=0 cycle.
            #
            # THE WATCHDOG: see the descriptor bridge above for what one
            # unanswered access did to this bus. The write face is where it was
            # measured - two lanes committed (dbg_lane_wr = 2), then the
            # response's read-back went out on the frozen read half and parked
            # this FSM in its read state forever, so every later write reported
            # fault 1 = FAULT_WTMO and 35 responses were voided.
            #
            # BYTE ORDER, and it is the exact inverse of the read path above: a
            # beat carries byte `addr+n` in bits [63-8n -: 8] (1722.1 wire
            # order, big-endian), while the bus words are little-endian.
            #
            # THE ERROR ARM, for the third time on this bus: LiteX's
            # wishbone2axi asserts `err` TOGETHER WITH `ack`, so a bare
            # `If(ack, ...)` would treat a FAILED write as committed. It is
            # propagated instead - `wr_err` with the done pulse makes the buffer
            # void the response, and KL_aecp_engine answers a well-formed
            # ENTITY_MISBEHAVING rather than putting a half-written response on
            # the wire.
            _rq = self.milan.respmem_req_sys      # read request  (from datapath)
            _rs = self.milan.respmem_rsp_sys      # read response (to datapath)
            _rw = self.milan.respmem_wr_sys       # write         (from datapath)
            _rd = self.milan.respmem_wd_sys       # write done    (to datapath)
            self.respmem_wb = _rwb = _wb.Interface(data_width=_pp_dw,
                                                   adr_width=_pp_adrw,
                                                   addressing="word")
            _dmab.add_master("milan_resp_mem", master=_rwb)

            _ra = Signal(32); _rl = Signal(9)
            _rdat = Signal(64); _re = Signal()
            _wa = Signal(32); _wd = Signal(64); _ws = Signal(8); _werr = Signal()
            _rto = Signal(max=_pp_tmo + 1)
            # THE POISON FLAG: see the descriptor bridge above for why a
            # poisoned bus state keeps driving cyc/stb rather than answering
            # off the bus. On this master the poisoned access is a WRITE as
            # often as a read, and it is still issued: whether the memory
            # performs it or leaves it queued behind the answer it already
            # owes, `wr_err` rides the done pulse and the buffer voids that
            # response, so a write reported failed is never counted committed.
            _rpsn = Signal(); _rpsn_set = Signal()
            self.sync += If(_rpsn_set, _rpsn.eq(1)
                         ).Elif(_rpsn & (_rwb.ack | _rwb.err), _rpsn.eq(0))
            self.respmem_fsm = _rfsm = FSM(reset_state="IDLE")
            # The write is offered first when both are pending. Neither face can
            # be starved by that: both are single-transaction and held until
            # ready, and the buffer never has a read and a write outstanding at
            # the same time anyway (it flushes the last lane, THEN reads back).
            # `_mem_rdy`: see `pp_mem_gate` and the block above the descriptor
            # master. A write refused here rides `wr_err` with the done pulse
            # and the buffer VOIDS that response, which is the right answer - a
            # response the memory could not take must never reach the wire as
            # though it had. This face does not transact out of reset
            # (KL_aecp_resp_buf.sv:353 resets to R_FILL), so it is gated for
            # symmetry and not because it was ever measured to freeze the bus.
            _rfsm.act("IDLE",
                _rw.ready.eq(1),
                _rq.ready.eq(~_rw.valid),
                NextValue(_rto, 0),
                If(_rw.valid,
                    NextValue(_wa, _rw.addr), NextValue(_wd, _rw.data),
                    NextValue(_ws, _rw.strb),
                    NextValue(_werr, _rpsn | ~_mem_rdy),
                    If(_mem_rdy, NextState("WR")).Else(NextState("WDONE"))
                ).Elif(_rq.valid,
                    NextValue(_ra, _rq.addr), NextValue(_rl, _rq.beats),
                    NextValue(_re, _rpsn | ~_mem_rdy),
                    If(_mem_rdy, NextState("RD")).Else(NextState("REMIT"))))
            _rfsm.act("WR",
                If(_ws == 0,
                    NextState("WDONE")     # no byte enabled: nothing to write
                ).Else(
                    _rwb.cyc.eq(1), _rwb.stb.eq(1), _rwb.we.eq(1),
                    _rwb.sel.eq(_ws), _rwb.adr.eq(_wa[_pp_sh:]),
                    _rwb.dat_w.eq(Cat(_wd[56:64], _wd[48:56],
                                      _wd[40:48], _wd[32:40],
                                      _wd[24:32], _wd[16:24],
                                      _wd[8:16],  _wd[0:8])),
                    NextValue(_rto, _rto + 1),
                    If(_rwb.ack,
                        NextValue(_rto, 0),
                        If(_rwb.err, NextValue(_werr, 1)),
                        NextState("WDONE")
                    ).Elif(_rto == _pp_tmo,
                        NextValue(_rto, 0), NextValue(_werr, 1),
                        _rpsn_set.eq(1), NextState("WDONE"))))
            # ONE cycle in this state = the one-cycle commit pulse the buffer
            # waits for, and it is STRICTLY LATER than the `wr_ready` that
            # accepted the write - the acknowledged bridge, which is the shape
            # KL_aecp_resp_buf's R_FLUSH arm requires (it sets `wbusy_r` on the
            # ready and only THEN looks for the done).
            _rfsm.act("WDONE",
                _rd.valid.eq(1), _rd.err.eq(_werr),
                If(_rd.ready, NextState("IDLE")))
            _rfsm.act("RD",
                _rwb.cyc.eq(1), _rwb.stb.eq(1), _rwb.sel.eq(_pp_selm),
                _rwb.adr.eq(_ra[_pp_sh:]),
                NextValue(_rto, _rto + 1),
                If(_rwb.ack,
                    NextValue(_rto, 0),
                    If(_rwb.err, NextValue(_re, 1)
                    ).Else(NextValue(_rdat, _rwb.dat_r)),
                    NextState("REMIT")
                ).Elif(_rto == _pp_tmo,
                    NextValue(_rto, 0), NextValue(_re, 1),
                    _rpsn_set.eq(1), NextState("REMIT")))
            # `_rs.ready` is REAL backpressure here (the descriptor face ties it
            # 1): the beat is HELD until the buffer takes it.
            _rfsm.act("REMIT",
                _rs.valid.eq(1), _rs.err.eq(_re),
                _rs.blast.eq((_rl == 1) | _re),
                _rs.data.eq(Cat(_rdat[56:64], _rdat[48:56], _rdat[40:48],
                                _rdat[32:40], _rdat[24:32], _rdat[16:24],
                                _rdat[8:16],  _rdat[0:8])),
                If(_rs.ready,
                    If(_re | (_rl == 1), NextState("IDLE")
                    ).Else(NextValue(_ra, _ra + 8), NextValue(_rl, _rl - 1),
                           NextValue(_rto, 0), NextState("RD"))))

            # ===============================================================
            #  THE INSTRUMENT THE 08-13 ROUND DID NOT HAVE
            # ===============================================================
            # Both bridges above now fail SAFELY (error arm, watchdog, poison
            # flag), and a safe failure that nothing can see is still a week of
            # board time. This is the observer: it separates "never issued"
            # from "issued and never answered", which are the two causes that
            # produce the SAME symptom (fault 8 / fault 1, image invalid,
            # ENTITY_MISBEHAVING on every command) and have nothing else in
            # common.
            #
            # A NEW CSR BANK MUST NOT MOVE AN OLD ONE, and left to itself this
            # one does: LiteX hands out the LOWEST free location at the moment
            # a module is added (SoCLocHandler.alloc), and `sdram`/`spiflash`
            # are allocated later still, so the default landed on sdram's page
            # and pushed both banks up 0x800 (measured, csr.csv diff).
            # That silently invalidates firmware's fixed LiteSPI-bank address;
            # its master port at bank+0x10 is a WRITE path to the boot flash.
            # Pin this observer to the
            # LAST page of the 64 KB CSR window instead, where automatic
            # allocation (which grows upward from 0) reaches last; a future
            # bank that does collide raises SoCError rather than moving anyone.
            self.csr.add("ppmem", n=self.csr.n_locs - 1)
            self.ppmem = _PPMemDiag([("desc", _dwb, _dpsn, _dpsn_set),
                                     ("resp", _rwb, _rpsn, _rpsn_set)],
                                    mem_rdy=_mem_rdy)

            self.irq.add("milan", use_loc_if_exists=True)  # 4 lines -> CPU via EventManager
            # Milan IDENTIFY -> board LED (controllers blink it to locate the
            # device). Skipped quietly on platforms without user_led pads.
            try:
                self.comb += platform.request("user_led", 0).eq(self.milan.identify)
            except Exception:
                print("[milan] no user_led pad - IDENTIFY LED not wired")

    def _add_flashboot_constants(self, manifest_name):
        """Emit the product flash constants and deployment manifest."""
        # A build must never emit a flash map that cannot be erased safely.
        problems = check_flash_map()
        if problems:
            raise ValueError("FLASHBOOT flash map is inconsistent:\n  " +
                             "\n  ".join(problems))

        images = FLASHBOOT_MANIFESTS[manifest_name]
        self._flashboot_layout = {"manifest": manifest_name,
                                  # Deployment refuses any layout whose
                                  # compiled owner is not the fabric plane.
                                  "gptp_owner": self._gptp_owner,
                                  "cpu_xlen": self._cpu_xlen,
                                  "entry": None,
                                  "complete": False,
                                  "flash_size": FLASH_SIZE,
                                  "erase_block": FLASH_ERASE_BLOCK,
                                  "images": [],
                                  # deploy.sh includes these boundaries in its
                                  # per-image write ceilings, so a manifest can
                                  # never overwrite persistent state.
                                  "reserved": [
                                      {"name": n, "offset": e["offset"],
                                       "size": e["size"]}
                                      for n, e in sorted(
                                          FLASHBOOT_RESERVED.items(),
                                          key=lambda kv: kv[1]["offset"])]}
        # The writable slots exist independently of the boot manifest, so their
        # constants are emitted even for manifest "none": firmware can locate
        # persistent storage independently of deployment mode.
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


# Build --------------------------------------------------------------------------------------------

#: milan-fpga's root, from THIS file's location: sw/litex/milan_soc.py -> up 3.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


def _builder_out(entity_gen_dir, name):
    """A file in the end-station builder's output for this config.

    The RTL include dir and the builder's output dir are two faces of ONE
    config, named alike by endstation_builder.py.
    """
    if not entity_gen_dir:
        raise RuntimeError(
            "this build needs its end-station config: pass --entity-gen-dir "
            "(build.sh does, for every named config)")
    cfg = os.path.basename(os.path.normpath(entity_gen_dir))
    path = os.path.join(REPO_ROOT, "sw", "builder", "out", cfg, name)
    if not os.path.exists(path):
        raise RuntimeError(
            f"config '{cfg}' has no {name} ({path}). Run the end-station "
            f"builder for this config first")
    return path


def _platform_shape(entity_gen_dir):
    """The config's platform shape - the authority on the DRAM reservations.

    Read rather than re-derived: the reserved band is declared once, in the
    config and generates both the firmware map and the bases compiled into the
    gateware. A second derivation here could make them disagree; disagreement
    about a physical address is memory corruption rather than a build error.
    """
    with open(_builder_out(entity_gen_dir, "platform_shape.json"),
              encoding="utf-8") as fh:
        return json.load(fh)


def build_desc_image(entity_gen_dir):
    """The AEM descriptor image this gateware's store will fetch from DRAM.

    The processor serves READ_DESCRIPTOR out of main memory and holds no
    descriptors on-die, so a bitstream WITHOUT its image is an end-station that
    answers BAD_ARGUMENTS to every enumeration - a device that looks broken
    rather than unprovisioned. Building the image here makes it a build
    artifact of the gateware that will read it, written beside the bitstream,
    instead of a step someone has to remember.

    It is generated BEFORE Vivado runs. A model this build cannot express must
    fail in seconds, not after a forty-minute place-and-route.

    Returns (image bytes, layout report, overlay path).
    """
    # Deriving the overlay from the include dir is what stops a build
    # compiling one shape's `svh` while shipping another shape's descriptors -
    # the exact class of mismatch the entity-shape gate in build.sh exists to
    # prevent.
    overlay = _builder_out(entity_gen_dir, "aem_overlay.json")

    sys.path.insert(0, os.path.join(REPO_ROOT, "avdecc"))
    sys.path.insert(0, os.path.join(REPO_ROOT, "protocol-processor", "hdl",
                                    "aecp", "desc"))
    import gen_aem_store as _aem
    import gen_desc_image as _img
    import gen_aemi_image as _join

    with open(overlay, encoding="utf-8") as fh:
        ovl = json.load(fh)
    model = _aem.build_model(_aem.spec_from_overlay(ovl))
    # PP_DESC_LINE_BYTES_P: a descriptor longer than the store's line buffer
    # cannot be answered, and the packer is the only place that can see it
    # coming. Passed explicitly rather than defaulted so the two move together.
    blob, report = _img.build(
        _join.model_to_document(model, _join.identity_from_overlay(ovl)), 576)
    return blob, report, overlay


def main():
    ap = argparse.ArgumentParser(description="Milan RISC-V fabric-control SoC")
    ap.add_argument("--xlen", default=32, type=int, choices=[32, 64],
                    help="CPU register width, honoured by BOTH --cpu choices "
                         "(the bare-metal product profile requires RV32 without an MMU)")
    ap.add_argument("--cpu-count",    default=1, type=int, help="number of cores (this config: 1)")
    ap.add_argument("--cpu",          default="vexiiriscv", choices=["naxriscv","vexiiriscv"], help="soft CPU (the product profile uses vexiiriscv)")
    ap.add_argument("--software-profile", default="baremetal",
                    choices=("baremetal",),
                    help="firmware shape; the product uses the cacheless RV32I "
                         "M-mode Vexii core and Milan UART/CSR firmware")
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
                    help="NxN dataplane width (docs/fpga/FPGA_DESIGN.md section 2): AAF stream "
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
    gptp_group = ap.add_mutually_exclusive_group()
    gptp_group.add_argument("--fabric-gptp", dest="fabric_gptp",
                            action="store_true",
                            help="use the fabric gPTP plane (the product "
                                 "default for every Milan software profile) and the builder's "
                                 "MAC/priority/clock-specific ROM")
    gptp_group.add_argument("--no-fabric-gptp", dest="fabric_gptp",
                            action="store_false",
                            help="elaborate the option-off comparison plane. "
                                 "VERIFICATION-ONLY hardware (#259): the image "
                                 "has no gPTP owner, is not a supported "
                                 "product image, and the flash tools refuse "
                                 "its artifacts")
    # Resolve omission after parsing because --no-milan has no gPTP owner.
    ap.set_defaults(fabric_gptp=None)
    ap.add_argument("--no-render-lpf", action="store_true",
                    help="AREA LEVER (banked, docs/design/AREA_BUDGET.md): prune "
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
                         "(gen/adp_shape_defaults.svh) from "
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
    # NOTE: there is no --with-pp-plane any more. The protocol processor was a
    # shadow plane behind PP_PLANE_P for exactly one round; scenario B
    # SUBSTITUTED it for the legacy 1722.1/SRP plane, which is deleted, so
    # milan_datapath instantiates KL_pp_shadow unconditionally and every build
    # gets the processor. A flag that can only be "on" is not a flag.
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
                    help="512 MB DDR3 via LiteDRAM (A7DDRPHY + MT41J256M16)")
    ap.add_argument("--coherent-dma", action="store_true",
                    help="request a dedicated DMA port (cache-coherent for NaxRiscv; "
                         "direct and coherence-free for the cacheless bare-metal Vexii core)")
    ap.add_argument("--bus-standard", default="wishbone", choices=["wishbone", "axi-lite"],
                    help="main SoC bus standard. 'axi-lite' makes the control path AXI end "
                         "to end and deletes the two round-trip bridges LiteX inserts when "
                         "the default 'wishbone' sits between the CPU's AXI-Lite pBus and "
                         "the AXI-Lite milan_csr window (OOC: 106 + 150 LUT, minus 18 for "
                         "AXILite2CSR over Wishbone2CSR). Carries no DRAM or DMA traffic.")
    ap.add_argument("--with-spiflash", action="store_true",
                    help="memory-map the on-board N25Q128 QSPI flash (16 MB) so the BIOS can "
                         "load the bare-metal AEM image. "
                         "Included by --all-blocks.")
    ap.add_argument("--flashboot", default="none",
                    choices=["none", "baremetal"],
                    help="which artifacts live in flash (needs --with-spiflash or --all-blocks): "
                         "'baremetal' stores the raw AEM image beside the bitstream; 'none' "
                         "(default) maps the flash but adds no boot method.")
    ap.add_argument("--all-blocks", "--full", dest="all_blocks", action="store_true",
                    help="enable ALL fabric blocks: NIC + DMA + MAC + DDR3 (= --with-dma "
                         "--with-mac --with-dram). This means 'every block instantiated', NOT "
                         "a complete/validated NIC  -  MDIO/PHY management, DMA "
                         "scatter-gather, and physical traffic (M-A3..M-A5) are still open. "
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

    if args.cpu != "vexiiriscv" or args.xlen != 32 or args.cpu_count != 1:
        ap.error("--software-profile baremetal requires --cpu vexiiriscv "
                 "--xlen 32 --cpu-count 1")
    if args.with_fpu or args.l2_bytes or args.scala_args:
        ap.error("--software-profile baremetal requires no FPU, --l2-bytes 0, "
                 "and no --scala-args overrides")
    if args.fabric_gptp is None:
        args.fabric_gptp = not args.no_milan
    if args.fabric_gptp and args.no_milan:
        ap.error("--fabric-gptp requires the Milan datapath")
    if not args.fabric_gptp and not args.no_milan:
        # No refusal, one loud fact (#259): with the fabric plane off there is
        # NO gPTP owner in this image. The elaboration stays available as the
        # verification-only option-off comparison.
        print("milan_soc: --no-fabric-gptp elaborates VERIFICATION-ONLY "
              "hardware with zero gPTP owners; not a supported product image")

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
                   sound_card=False,
                   gptp_plane=args.fabric_gptp,
                   aaf_playback=False,
                   aaf_pb_streams=1,
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
                   software_profile=args.software_profile,
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
    if args.software_profile == "baremetal":
        fw_dir = os.path.join(REPO_ROOT, "sw", "firmware", "milan_baremetal")
        builder.add_software_package("libmilan_baremetal", fw_dir)
        builder.add_software_library("libmilan_baremetal", always_link=True)
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
    # Fail fast, BEFORE Vivado: a model the image cannot express is a seconds-
    # long error, not a forty-minute one.
    _desc_blob = _desc_report = _desc_overlay = None
    if getattr(soc, "_pp_windows", None):
        _desc_blob, _desc_report, _desc_overlay = build_desc_image(
            args.entity_gen_dir)
    if args.software_profile == "baremetal":
        if _desc_blob is None:
            raise RuntimeError("baremetal firmware requires the protocol-processor entity image")
        if len(_desc_blob) > FLASHBOOT_AEM["size"]:
            raise RuntimeError(
                f"entity image is {len(_desc_blob)} bytes, larger than the "
                f"{FLASHBOOT_AEM['size']}-byte baremetal flash slot")
        soc.add_constant("MILAN_AEM_FLASH_OFFSET", FLASHBOOT_AEM["offset"])
        soc.add_constant("MILAN_AEM_IMAGE_BYTES", len(_desc_blob))
        soc.add_constant("MILAN_AEM_IMAGE_CRC32",
                         binascii.crc32(_desc_blob) & 0xFFFF_FFFF)
        soc.add_constant("MILAN_AEM_DESC_BASE", soc._pp_windows["desc_base"])
        with open(_desc_overlay, encoding="utf-8") as fh:
            _baremetal_ovl = json.load(fh)
        _eid = int(_baremetal_ovl["adp"]["entity_id"], 16)
        _mid = int(_baremetal_ovl["entity"]["entity_model_id"], 16)
        _mac = bytes.fromhex(_baremetal_ovl["adp"]["mac_address"].replace(":", ""))
        _aaf_talkers = sum(s.get("kind", "aaf") == "aaf"
                           for s in _baremetal_ovl["stream_outputs"])
        with open(_builder_out(args.entity_gen_dir, "lwsrp_table.json"),
                  encoding="utf-8") as fh:
            _baremetal_srp = json.load(fh)
        soc.add_constant("MILAN_ENTITY_ID_LO", _eid & 0xFFFF_FFFF)
        soc.add_constant("MILAN_ENTITY_ID_HI", _eid >> 32)
        soc.add_constant("MILAN_MODEL_ID_LO", _mid & 0xFFFF_FFFF)
        soc.add_constant("MILAN_MODEL_ID_HI", _mid >> 32)
        soc.add_constant("MILAN_STATION_MAC_LO", int.from_bytes(_mac[:4], "little"))
        soc.add_constant("MILAN_STATION_MAC_HI", int.from_bytes(_mac[4:], "little"))
        soc.add_constant("MILAN_N_TALKERS", _aaf_talkers)
        soc.add_constant("MILAN_SR_VID",
                         int(_baremetal_srp["reset_words"]["LWSRP_VID"], 16))
        soc.add_constant("MILAN_LWSRP_CTRL_RESET",
                         int(_baremetal_srp["reset_words"]["LWSRP_CTRL"], 16))
    builder.build(run=args.build, **build_kwargs)  # run=False => elaborate + export gateware, no Vivado
    # Ship the entity model WITH the gateware that reads it, and record the
    # base it was compiled for. Bitstream and image are one deliverable: a
    # board flashed with one and loaded with the other's model enumerates the
    # wrong device, which no counter reports.
    _aem_binding = None
    if _desc_blob is not None:
        _img_path = os.path.join(builder.output_dir, "aem_desc.bin")
        with open(_img_path, "wb") as f:
            f.write(_desc_blob)
        _aem_binding = aem_image_binding(_img_path)
        _man = {
            "desc_base": soc._pp_windows["desc_base"],
            "resp_base": soc._pp_windows["resp_base"],
            "window_bytes": soc._pp_windows["window_bytes"],
            "image": "aem_desc.bin",
            "image_bytes": len(_desc_blob),
            "overlay": os.path.relpath(_desc_overlay, REPO_ROOT),
        }
        with open(os.path.join(builder.output_dir, "aem_desc.json"), "w") as f:
            json.dump(_man, f, indent=2)
        with open(os.path.join(builder.output_dir, "aem_desc.map"), "w") as f:
            f.write(_desc_report)
        print(f"[milan] entity model ({len(_desc_blob)} B) -> {_img_path} "
              f"@ 0x{soc._pp_windows['desc_base']:08x}")
    # Persist the flash-boot layout so deploy.sh writes the exact same offsets the BIOS
    # was compiled with (single source of truth  -  see FLASHBOOT_LAYOUT / deploy.sh flash-pair).
    # A runnable Vivado build also binds the JSON owner fact to the exact parsed
    # configuration payload and FPGA part.  Elaboration-only layouts deliberately
    # omit this binding and therefore cannot pass a persistent deploy check.
    if getattr(soc, "_flashboot_layout", None):
        if any(row.get("name") == "aem"
               for row in soc._flashboot_layout.get("images", [])):
            if _aem_binding is None:
                raise RuntimeError(
                    "flash layout names AEM but no generated image exists "
                    "to bind its length, CRC32, and SHA-256")
            soc._flashboot_layout.update(_aem_binding)
        if args.build:
            bit_path = builder.get_bitstream_filename(mode="sram")
            if not os.path.isfile(bit_path):
                raise RuntimeError(
                    f"Vivado build produced no bitstream for layout binding: {bit_path}")
            soc._flashboot_layout.update(bitstream_binding(bit_path))
        layout_path = os.path.join(builder.output_dir, "flashboot_layout.json")
        with open(layout_path, "w") as f:
            json.dump(soc._flashboot_layout, f, indent=2)
        print(f"[milan] flash-boot layout ({args.flashboot}) -> {layout_path}")
    if args.load:
        prog = platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))


if __name__ == "__main__":
    main()
