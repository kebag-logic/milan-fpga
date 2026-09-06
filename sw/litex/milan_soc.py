#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Configurable RISC-V SoC with the Milan TSN NIC. The product profile is a
# cacheless RV32 VexiiRiscv running the Milan bare-metal control firmware.
#
#   ./milan_soc.py                         # NIC (CSR only); elaborate + export gateware
#   ./milan_soc.py --full                  # complete fabric endpoint + MAC/PHY + DDR3
#   ./milan_soc.py --with-mac              # attach the board MAC/PHY boundary
#   ./milan_soc.py --no-milan              # bare SoC (bring-up smoke; self-contained)
#   ./milan_soc.py --software-profile baremetal --cpu vexiiriscv --xlen 32 \
#       --with-spiflash --flashboot baremetal
#   ./milan_soc.py --full --build          # + run Vivado P&R -> bitstream (needs Artix-7)
#   ./milan_soc.py --full --build --load   # + program the board
#
# The Artix-7 (xc7a100t) bitstream needs Vivado with Artix-7 device support. This
# box only has Spartan-7 installed, so `--build` P&R is blocked here; gateware
# EXPORT (the default, run=False) works with no vendor tools. The CPU⇄CSR path is
# proven by the rerunnable softcore integration sim: sw/litex/milan_sim.py ->
# the BIOS reads ID="MILN" (M-A2). The old captured bring-up logs were retired
# with #259 and remain available in Git history.

import os
import re
import sys
import subprocess
import json
import argparse
import binascii
from pathlib import Path

from gptp_owner_contract import GPTP_OWNER_CODES
from qspi_owner_transition import aem_image_binding, bitstream_binding

from migen import (ClockDomain, ClockDomainsRenamer, ClockSignal, ResetSignal,
                   Instance, Signal, Mux, If, Cat, C, Array, FSM, NextValue,
                   NextState, Memory, Module, Record)
from migen.genlib.cdc import MultiReg
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.gen import LiteXModule
from litex.soc.interconnect import stream

from litex.build.io import DDROutput

from litex.soc.cores.clock import S7PLL, S7MMCM
from litex.soc.interconnect import axi
from litex.soc.interconnect.csr import CSRStorage, CSRStatus, CSRField
from litex.gen.genlib.cdc import BusSynchronizer
from litex.soc.integration.soc_core import SoCCore
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import Builder, builder_args, builder_argdict

# THIS FILE'S TWO ROOTS, as `Path`s, derived once. Every path below is a
# `Path`; a `str()` marks the boundary where one leaves for something that
# takes text - a migen `Instance` parameter, a LiteX platform/source list, a
# `sys.path` entry or a JSON field - and there are no others.
SOC_DIR = Path(__file__).parent                 # sw/litex/
REPO_ROOT = SOC_DIR.parent.parent               # milan-fpga/

# Local platform (not in upstream litex_boards).
sys.path.insert(0, str(SOC_DIR / "platforms"))
import alinx_ax7101
import board_audio_routing

# The Milan CSR window. The register OFFSETS (0x000..0x700) match docs/reference/REGISTER_MAP.md;
# only the BASE is CPU-specific: on the supported LiteX CPU maps an MMIO peripheral
# must live in the IO region (>= 0x8000_0000, uncached), so we map it at 0x9000_0000. The Zynq
# alternate integration used 0x43C0_0000. Firmware and gateware must share this base.
MILAN_CSR_BASE = 0x9000_0000
MILAN_CSR_SIZE = 0x0001_0000  # 64 KB

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
#   user     raw bare-metal records: entity/group names, channel maps, mixer
#            state, and the rotating compressed CTF fault log. There is no
#            filesystem or target-OS mount associated with this region.
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
    "user":    {"offset": 0xF0_0000, "size": 0x10_0000},   # 1 MiB raw records
}


def flash_map() -> list[tuple[str, int, int, str]]:
    """Every slot on the device, ordered by offset: [(name, offset, size, kind)].

    The single reader of both dicts.  `kind` is "image" for anything the BIOS
    or deploy.sh transfers and "reserved" for the writable slots.
    """
    rows = [(n, e["offset"], e["size"], "image")
            for n, e in FLASHBOOT_LAYOUT.items()]
    rows += [(n, e["offset"], e["size"], "reserved")
             for n, e in FLASHBOOT_RESERVED.items()]
    return sorted(rows, key=lambda r: r[1])


def check_flash_map() -> list[str]:
    """Return a list of problems with the flash map; empty means consistent.

    Erase-block alignment is not cosmetic: a writable region that starts or ends
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

    `milan_datapath` is the vendor-neutral fabric endpoint: a real,
    Verilator+Yosys-verified module (tb/verilator/milan_dp, syn/yosys). It exposes:
      * an AXI4-Lite CSR slave (milan_csr control plane)  -  wired here to the CPU bus;
      * a MAC-facing AXIS pair + MAC cfg/status  -  the §A.7 MAC (LiteEth `LiteEthMAC`
        or Forencich `eth_mac_1g_rgmii_fifo` + RGMII PHY) attaches here (stubbed);
      * protocol-processor descriptor/response memory faces bridged by the SoC.

    This makes the SoC instantiate real RTL with no target-OS data-plane boundary.
    The fabric AAF/CRF/gPTP/protocol sources and the MAC are the complete product
    packet path; the CPU remains a control-plane owner over CSRs and the two
    protocol-processor memory regions.
    """
    def __init__(self, platform, axil, board_ports=None, milan_cd="sys",
                 desc_base=None, resp_base=None,
                 milan_clk_hz=100_000_000, num_streams=1,
                 audio_if_slots=0, talker_wire_chans=2, audio_if_master=False,
                 audio_if_i2s_pair=False, gptp_plane=None,
                 loopback_lane=False,
                 render_lpf=True, optional_blocks=None,
                 entity_gen_dir=None):
        # AECP IDENTIFY control level (Milan FR-MGT-01) - wired to a board LED
        # by the SoC so a controller's "identify" visibly blinks the device.
        self.identify = Signal()
        add_milan_datapath(self, platform, axil, desc_base=desc_base,
                           resp_base=resp_base,
                           extra_ports=dict(board_ports or {}, o_o_identify=self.identify),
                           milan_cd=milan_cd,
                           milan_clk_hz=milan_clk_hz, num_streams=num_streams,
                           audio_if_slots=audio_if_slots,
                           talker_wire_chans=talker_wire_chans,
                           audio_if_master=audio_if_master,
                           audio_if_i2s_pair=audio_if_i2s_pair,
                           gptp_plane=gptp_plane,
                           loopback_lane=loopback_lane,
                           render_lpf=render_lpf, optional_blocks=optional_blocks,
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
    spec = importlib.util.spec_from_file_location(
        "pp_srcs", REPO_ROOT / "scripts" / "pp_srcs.py")
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
    # shadow/substitution wrapper and the block-vs-per-source MAAP adapter,
    # and the saved-state backing store the shadow instantiates behind the
    # processor's NVM device face (docs/design/SAVED_STATE_FASTCONNECT.md).
    "hdl/milan/KL_pp_shadow.sv", "hdl/milan/KL_pp_maap_shim.sv",
    "hdl/milan/KL_nvm_backend.sv",
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
    "third_party/verilog-axis/rtl/axis_fifo.v",
    "third_party/verilog-axis/rtl/axis_arb_mux.v", "third_party/verilog-axis/rtl/arbiter.v",
    "third_party/verilog-axis/rtl/priority_encoder.v",
    # the 802.1Q classifier/queue/CBS chain (hdl/ieee8021q/ts/*) and the
    # ptp_ts_top record stampers are NOT datapath sources any more: the
    # retired transmit path that fed them is gone (#259) and milan_datapath no longer
    # instantiates them. They keep their unit suites and Yosys tops.
    "hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv", "hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv",
    "hdl/common/cdc_pulse.sv", "hdl/common/cdc_handshake.sv",
    "hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv",
    "hdl/ieee8021q/filtering/tcam.sv", "hdl/ieee8021q/filtering/rx_mac_filter.sv",
    "hdl/common/tx_ifg_gasket.sv", "hdl/ieee1722/aaf/KL_pcm_lpf.sv",
    "hdl/common/KL_link_guard.sv",
    # ADP TX arbitration survives the scenario-B substitution: the advertiser
    # itself is the processor's KL_adp_engine now, but the two-source TX merge
    # in front of the MAC is still this module.
    "hdl/ieee17221/adp/adp_tx_arbiter.sv",
    # AVTP AAF talker (MVP: Pmod I2S2 on pmoda -> class-A stream, fabric-only)
    "hdl/ieee1722/aaf/aaf_talker_i2s.sv", "hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv",
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
    "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv", "hdl/ieee1722/avtp/KL_talker_diag_ctx.sv",
    "hdl/ieee1722/avtp/KL_media_clock_restart.sv",
    "hdl/ieee1722/aaf/KL_pcm_route.sv",
    "hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv", "hdl/ieee1722/aaf/KL_tdm_capture.sv",
    "hdl/ieee1722/aaf/KL_tdm_capture_master.sv", "hdl/ieee1722/aaf/KL_pair_blend.sv",
    "hdl/ieee1722/aaf/KL_pair_zero_fill.sv", "hdl/ieee1722/aaf/KL_tdm_render.sv",
    "hdl/ieee1722/aaf/KL_chan_map_render.sv", "hdl/ieee1722/aaf/KL_chan_map_capture.sv",
    "hdl/ieee1722/aaf/KL_aaf_packetizer.sv", "hdl/ieee1722/crf/KL_crf_rx.sv",
    "hdl/ieee1722/crf/KL_crf_tx.sv", "hdl/ieee1722/maap/KL_maap.sv",
    "hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv", "hdl/ieee1722/aaf/KL_aaf_packetizer.sv",
    "hdl/ieee1722/crf/KL_crf_rx.sv", "hdl/ieee1722/crf/KL_crf_tx.sv",
    "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv", "hdl/ieee1722/crf/KL_media_nco.sv",
    "hdl/ieee1722/crf/KL_media_grid_align.sv", "hdl/ieee1722/maap/KL_maap.sv",
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
    svh = REPO_ROOT / "hdl" / "common" / "eth_event_counter" / \
        "ethernet_events.svh"
    body = svh.read_text()
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


def _board_audio_ports(platform):
    """Bind the fabric audio interfaces directly to board pads.

    Audio is a fabric function, not a side effect of a packet-memory engine.
    Keeping this binding beside `add_milan_datapath` makes that ownership
    explicit and lets the product omit a general packet interface.
    Returns `(instance_ports, i2s_capture_pads)`; the latter is used only to
    decide whether the Arty TDM/I2S blend is physically routed.
    """
    i2s_pads = None
    i2s_dac_pads = None
    try:
        connectors = platform.constraint_manager.connector_manager.connector_table
    except AttributeError:
        connectors = {}

    if "pmoda" in connectors:
        try:
            from litex_boards.platforms.digilent_arty import i2s_pmod_io
            platform.add_extension(i2s_pmod_io("pmoda"))
            rx = platform.request("i2s_rx")
            rx_mclk = platform.request("i2s_rx_mclk")
            tx = platform.request("i2s_tx")
            tx_mclk = platform.request("i2s_tx_mclk")
            i2s_pads = (rx_mclk, rx.clk, rx.sync, rx.rx)
            i2s_dac_pads = (tx_mclk, tx.clk, tx.sync, tx.tx)
        except Exception:
            # Board variants may expose the connector without the complete
            # I2S resource. An absent interface is represented by the explicit
            # structural-zero input below and is caught by the routing gate.
            i2s_pads = None
            i2s_dac_pads = None

    # The Arty TDM8-master header lives on pmodb. This declaration is also the
    # routing oracle consumed by board_audio_routing.py.
    if "pmodb" in connectors:
        platform.add_extension(_arty_serial_io("tdm", "pmodb"))

    ports = dict(
        o_i2s_dac_mclk_o=(i2s_dac_pads[0] if i2s_dac_pads else Signal()),
        o_i2s_dac_sclk_o=(i2s_dac_pads[1] if i2s_dac_pads else Signal()),
        o_i2s_dac_lrck_o=(i2s_dac_pads[2] if i2s_dac_pads else Signal()),
        o_i2s_dac_sdin_o=(i2s_dac_pads[3] if i2s_dac_pads else Signal()),
        o_i2s_mclk_o=(i2s_pads[0] if i2s_pads else Signal()),
        o_i2s_sclk_o=(i2s_pads[1] if i2s_pads else Signal()),
        o_i2s_lrck_o=(i2s_pads[2] if i2s_pads else Signal()),
        i_i2s_sdout_i=(i2s_pads[3] if i2s_pads else 0),
    )
    return ports, i2s_pads


def add_milan_datapath(host: Module, platform: object,
                       axil: axi.AXILiteInterface,
                       extra_ports: dict[str, object] | None = None,
                       milan_cd: str = "sys",
                       desc_base: int | None = None,
                       resp_base: int | None = None,
                       milan_clk_hz: float = 100_000_000,
                       num_streams: int = 1,
                       audio_if_slots: int = 0,
                       talker_wire_chans: int = 2,
                       audio_if_master: bool = False,
                       audio_if_i2s_pair: bool = False,
                       gptp_plane: bool | None = None,
                       loopback_lane: bool = False,
                       render_lpf: bool = True,
                       optional_blocks: dict[str, bool] | None = None,
                       entity_gen_dir: str | None = None) -> None:
    """Instantiate `milan_datapath` and add its RTL sources  -  the single place the
    wrapper is wired, reused by the board SoC (`MilanNIC`) and the sim SoC
    (`milan_sim.py`). `axil` is the AXI-Lite CSR slave. `extra_ports`
    overrides/adds Instance ports to attach the board MAC and audio pads. The
    datapath exposes AXI-Lite control, protocol memory, MAC AXIS and physical
    audio boundaries. Instance ports for RTL signals already named `i_*`/`o_*`
    get the doubled migen prefix (e.g. milan port
    `i_i_mac_speed`, `o_o_irq_csr`)  -  that is correct, not a typo."""
    # Run the datapath in `milan_cd`. When that is not `sys`, cross the CPU's
    # AXI-Lite CSR bus (sys) into `milan_cd` with an async-FIFO CDC  -  so the dense
    # datapath logic leaves the sys (100 MHz) timing budget while the CPU/DDR3 stay
    # fast. `milan_cd == "sys"` (the default, and what the sim uses) keeps the old
    # single-clock direct wiring. The MAC AXIS boundary is likewise crossed by
    # its own stream CDC in MilanMAC when `milan_cd != "sys"`.
    if milan_cd != "sys":
        csr_axil = axi.AXILiteInterface(data_width=32, address_width=32)
        host.submodules.milan_axil_cdc = axi.AXILiteClockDomainCrossing(
            axil, csr_axil, cd_from="sys", cd_to=milan_cd)
    else:
        csr_axil = axil
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
        # The bare-metal firmware polls the CSR state it owns. The aggregate
        # diagnostic interrupt has no CPU event-manager ABI in this product.
        o_o_irq_csr = Signal(),
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
    # TALKER_WIRE_CHANS_P (item 00): the channels_per_frame the framer emits.
    # Passed only above the default, so the
    # shipping build's Instance and generated top .v stay byte-identical.
    # milan_datapath REFUSES at elaboration any width the front-end selected by
    # audio_if_slots cannot feed - that guard is what makes this a fabric fact
    # and not one more declaration.
    # milan-fpga/ root - used by the source list AND the processor ROM path
    base = REPO_ROOT
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
    # THE ACMP TRANSITION ROM IS NOT OPTIONAL. protocol_processor_top - which
    # milan_datapath now instantiates unconditionally through KL_pp_shadow -
    # $readmemh's its listener transition ROM by the RELATIVE name
    # "ltn_rom.hex", and Vivado resolves that against ITS OWN run directory,
    # not against the source file. Every build therefore generates the image
    # and hands over an ABSOLUTE path, so the bitstream cannot depend on where
    # vivado was launched from and cannot silently elaborate an all-zero ROM
    # (which is a listener that answers nothing).
    rom = base / "configs" / "generated" / "ltn_rom.hex"
    gen = base / "protocol-processor" / "hdl" / "acmp" / "rom" / "gen_ltn_rom.py"
    rom.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(gen), "-o", str(rom)], check=True)
    # A `str`: this is a Verilog string parameter on the Instance below, and a
    # PurePath would render into the emitted .v as a repr, not as a path.
    dp_params["p_PP_TROM_HEX_P"] = str(rom)

    # THE AECP uCPU MICROCODE IMAGE, same relative-$readmemh contract as the
    # ACMP ROM above and the same failure mode if it is not handed over as an
    # absolute path: an all-zero microcode store is an AECP engine that
    # answers nothing, which looks exactly like the pre-uCPU build.
    uc = base / "configs" / "generated" / "ucode.hex"
    ucgen = base / "protocol-processor" / "hdl" / "aecp" / "ucode" / "gen_ucode.py"
    subprocess.run([sys.executable, str(ucgen), "-o", str(uc)], check=True)
    dp_params["p_PP_UCODE_HEX_P"] = str(uc)          # Instance parameter: text

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
    if loopback_lane:
        # task #65 rx -> talker LOOPBACK bucket. The SV parameter is
        # LOOPBACK_P. Passed only when asked for, so a build that does not
        # ask emits a byte-identical top .v. It buys the entity's declared
        # loopback AUDIO_CLUSTERs their actual source; it costs +2303 LUT /
        # +1542 FF OOC at the 8x8 shape, which is why the shipping config
        # leaves it off and points its power-on map at silence.
        dp_params["p_LOOPBACK_P"] = 1
    if audio_if_master and int(audio_if_slots):
        # AUDIO_IF_MASTER_P / AUDIO_IF_CLK_HZ_P (item 4): the TDM bus ROLE and
        # the clock the master divides. Passed
        # passed ONLY when asked for, so a build that does not ask emits a
        # byte-identical top .v - and the SAME TRAP applies: the names below
        # must match the SV parameter declarations CHARACTER FOR CHARACTER
        # (`AUDIO_IF_MASTER_P`, `AUDIO_IF_CLK_HZ_P` in hdl/milan/
        # milan_datapath.sv), because LiteX does not diagnose a parameter the
        # module does not have - it silently drops it.
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
    # There is no CBS instance mask any more: milan_datapath stopped
    # instantiating the 802.1Q classifier/queue/CBS chain when the retired-target
    # TX that fed it left (#259), so the 2026-07-28 area lever has nothing to
    # prune and CBS_QUEUES_MASK_P is not a parameter of the module.
    # =======================================================================
    #  AECP DESCRIPTOR-IMAGE READ BRIDGE  (protocol-processor 07 §3.3)
    # =======================================================================
    # The processor's descriptor store fetches the entity model from main
    # memory. This is that master, bridged to a LiteX wishbone READ master on
    # the CPU's dedicated fabric-memory port and extended across a burst of
    # 64-bit words.
    #
    # CONTRACT (the submodule's): ONE outstanding request, held until ready;
    # responses IN ORDER; `beats` is 64-bit beats, >= 1, max 128; `rsp_last`
    # marks the final beat; `rsp_ready` is tied 1 by the processor, it always
    # sinks. A beat carries its LOWEST byte address in bits [63:56] - 1722.1
    # wire order, i.e. BIG-ENDIAN, a byte-reverse of the little-endian words
    # the bus returns.
    #
    # THE ERROR ARM IS NOT OPTIONAL: LiteX's wishbone2axi asserts `err`
    # TOGETHER WITH `ack` in its error state, so `If(ack, ...)` alone accepts a
    # FAILED read and latches whatever `dat_r` held. This master has an error
    # output: `desc_mem_rsp_err` aborts the burst and the store degrades that
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
    # (see `descmem` in the SoC body).
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

    # The THIRD main-memory master: KL_nvm_backend's, behind the processor's
    # NVM device face inside KL_pp_shadow (docs/design/SAVED_STATE_FASTCONNECT.md
    # section 8). The persisted record image lives in the reserved ppmem window
    # and the backend reads and writes it one 64-bit lane at a time, with the
    # SAME contract as the response face above: single-beat reads (it only
    # ever asks for one), real `rsp_ready` backpressure, one outstanding
    # 8-byte-aligned write whose zero-strobe bytes must not be modified, and a
    # one-cycle `wr_done` commit pulse strictly after `wr_ready`. Same CDC
    # shape, same reasons, a separate face because it is a separate
    # one-transaction client and the bus is the arbiter.
    nvm_req_valid = Signal();      nvm_req_ready = Signal()
    nvm_req_addr  = Signal(32);    nvm_req_beats = Signal(9)
    nvm_rsp_valid = Signal();      nvm_rsp_ready = Signal()
    nvm_rsp_data  = Signal(64)
    nvm_rsp_last  = Signal();      nvm_rsp_err   = Signal()
    nvm_wr_valid  = Signal();      nvm_wr_ready  = Signal()
    nvm_wr_addr   = Signal(32);    nvm_wr_data   = Signal(64)
    nvm_wr_strb   = Signal(8)
    nvm_wr_done   = Signal();      nvm_wr_err    = Signal()

    n_req = _axis_dp_cdc(host, "nvmmem_req_cdc",
                         [("addr", 32), ("beats", 9)], milan_cd,
                         to_datapath=False)
    n_rsp = _axis_dp_cdc(host, "nvmmem_rsp_cdc",
                         [("data", 64), ("blast", 1), ("err", 1)], milan_cd,
                         to_datapath=True)
    n_wr  = _axis_dp_cdc(host, "nvmmem_wr_cdc",
                         [("addr", 32), ("data", 64), ("strb", 8)], milan_cd,
                         to_datapath=False)
    n_wd  = _axis_dp_cdc(host, "nvmmem_wd_cdc",
                         [("err", 1)], milan_cd, to_datapath=True)
    host.comb += [
        n_req.dp.valid.eq(nvm_req_valid), n_req.dp.addr.eq(nvm_req_addr),
        n_req.dp.beats.eq(nvm_req_beats), nvm_req_ready.eq(n_req.dp.ready),
        nvm_rsp_valid.eq(n_rsp.dp.valid), nvm_rsp_data.eq(n_rsp.dp.data),
        nvm_rsp_last.eq(n_rsp.dp.blast),  nvm_rsp_err.eq(n_rsp.dp.err),
        n_rsp.dp.ready.eq(nvm_rsp_ready),
        n_wr.dp.valid.eq(nvm_wr_valid),   n_wr.dp.addr.eq(nvm_wr_addr),
        n_wr.dp.data.eq(nvm_wr_data),     n_wr.dp.strb.eq(nvm_wr_strb),
        nvm_wr_ready.eq(n_wr.dp.ready),
        n_wd.dp.ready.eq(1),
        nvm_wr_done.eq(n_wd.dp.valid), nvm_wr_err.eq(n_wd.dp.err),
    ]
    host.nvmmem_req_sys = n_req.sys
    host.nvmmem_rsp_sys = n_rsp.sys
    host.nvmmem_wr_sys  = n_wr.sys
    host.nvmmem_wd_sys  = n_wd.sys

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
        o_o_nvm_mem_req_valid  = nvm_req_valid,
        i_i_nvm_mem_req_ready  = nvm_req_ready,
        o_o_nvm_mem_req_addr   = nvm_req_addr,
        o_o_nvm_mem_req_beats  = nvm_req_beats,
        i_i_nvm_mem_rsp_valid  = nvm_rsp_valid,
        o_o_nvm_mem_rsp_ready  = nvm_rsp_ready,
        i_i_nvm_mem_rsp_data   = nvm_rsp_data,
        i_i_nvm_mem_rsp_last   = nvm_rsp_last,
        i_i_nvm_mem_rsp_err    = nvm_rsp_err,
        o_o_nvm_mem_wr_valid   = nvm_wr_valid,
        i_i_nvm_mem_wr_ready   = nvm_wr_ready,
        o_o_nvm_mem_wr_addr    = nvm_wr_addr,
        o_o_nvm_mem_wr_data    = nvm_wr_data,
        o_o_nvm_mem_wr_strb    = nvm_wr_strb,
        i_i_nvm_mem_wr_done    = nvm_wr_done,
        i_i_nvm_mem_wr_err     = nvm_wr_err,
    )

    host.specials += Instance("milan_datapath", **dp_params, **ports)
    # CBS slope timing: no XDC exception needed since the sequential slope
    # engine (credit_based_shaper.sv slope_engine, 2026-07-11). The old per-
    # cycle combinational constant-divide cones (~9.3K LUTs over 4 queues,
    # partly attributed to milan_csr by cross-boundary optimization) needed
    # set_multicycle_path 4 on the config->slope_r capture; the engine's
    # 1-bit-per-cycle divider paths close timing natively.
    # RTL sources for elaboration / P&R. Curated list (NOT add_source_dir) so the
    # Same file set the tb/verilator/milan_dp + syn/yosys checks use.
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
        platform.add_verilog_include_path(str(Path(entity_gen_dir) / "gen"))
    for inc in ("hdl/common", "hdl/ieee8021q/ts", "hdl/ieee8021as/ptp_timestamp",
                "hdl/ieee17221/adp", "hdl/common/csr", "hdl/common/eth_event_counter",
                "hdl/ieee1722/avtp"):
        platform.add_verilog_include_path(str(base / inc))
    for f in _MILAN_DATAPATH_SOURCES:
        platform.add_source(str(base / f))


# AXIS clock-domain crossing (protocol-memory/MAC boundaries) -------------------------------------

class _AxisDP:
    """Pair of stream endpoints for one AXIS lane crossing the datapath boundary:
    `.dp` is bound to the `milan_datapath` Instance, `.sys` to the SoC-side
    protocol-memory bridge or MAC."""
    def __init__(self, dp, sys):
        self.dp  = dp
        self.sys = sys

#: Async-FIFO depth of every AXIS datapath crossing, in beats. It was a
#: `depth=16` parameter of `_axis_dp_cdc` that not one of its eight call sites
#: ever passed - a knob nobody turns is a constant with a longer signature, and
#: this file has enough of those. Named here so the eight crossings still say
#: the same number in one place.
_AXIS_CDC_DEPTH = 16


def _axis_dp_cdc(host, name, layout, milan_cd, to_datapath, rename=None):
    """Cross one AXIS lane between the sys domain (memory bridge / MAC core) and the
    datapath's `milan_cd` domain with an async-FIFO `stream.ClockDomainCrossing`
    boundary, `_AXIS_CDC_DEPTH` beats deep. `to_datapath=True` is a sys->milan_cd
    lane; False is milan_cd->sys. When `milan_cd == "sys"` there is no
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
        cdc = stream.ClockDomainCrossing(layout, cd_from="sys", cd_to=milan_cd,
                                         depth=_AXIS_CDC_DEPTH, buffered=True)
        if rename: cdc = ClockDomainsRenamer(rename)(cdc)
        setattr(host, name, cdc)                           # LiteXModule auto-submodule
        return _AxisDP(dp=cdc.source, sys=cdc.sink)
    # milan_cd -> sys
    cdc = stream.ClockDomainCrossing(layout, cd_from=milan_cd, cd_to="sys",
                                     depth=_AXIS_CDC_DEPTH, buffered=True)
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
    it as `MilanNIC(..., board_ports=mac.dp_ports)`.

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
            # MAC preamble errors (TROUBLESHOOTING Section 17; the retired bench log
            # remains in Git history under #259). LiteEthPHYGMII is the right PHY.
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
        # the whole sys side (core + tx FIFO) in reset. The fabric guard now
        # owns both reset halves and performs a clean eth re-init without
        # touching the Milan datapath.
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
        # matched pointers without an external reset writer; the fabric guard
        # owns the eth-side reset too.
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
        # cycle), while a fabric source may pause mid-frame -> a single `valid` bubble
        # becomes a tx_en glitch -> the PHY emits a
        # fragment the peer NIC discards WITHOUT counting (total silence). Sim-reproduced
        # (starved source -> 6 bubbles/frame) and sim-fixed by this FIFO: it releases a
        # frame downstream only once COMPLETELY buffered, so the drain is always gapless.
        # 512 x 8 B = 4 KB >= 2 max-size frames; 8 frame slots.
        # (Full LiteEthMAC has SRAM buffering for exactly this reason; we drive the bare
        # core, so we provide the gapless drain FIFO here.)
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
                                    # is a structural requirement of this boundary).
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
        # back into its MAC-RX stream (bypassing the LiteEth core + PHY) so the complete
        # fabric packet path can be verified with no wire rig. Both are AXIS keep-masks
        # here, so no last_be conversion is needed on the loop path.
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

        # ---- PHY/MAC link status (MAC_STATUS 0x110 / REQ-MAC-03) --------------------
        # WHY A CSR AND NOT A WIRE: LiteEth's GMII/MII PHY wrappers expose NO link,
        # speed or duplex output. `LiteEthPHYGMII`/`LiteEthPHYMII` carry the TX/RX
        # datapaths, the CRG, and - only when the board routes mdc/mdio - a
        # `LiteEthPHYMDIO`, which is a SOFTWARE BIT-BANG register pair (mdc / mdio_w
        # {oe,w} / mdio_r), NOT an autoneg-result register. There is no hardware MDIO
        # master anywhere in the SoC, so the negotiated state only ever exists where
        # the MDIO transactions happen: through the `phy` register window at
        # 0xf000_3800. A fabric MDIO poller would be new
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
            # levers inside the datapath; the CSR remains the control boundary
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
    hypotheses. These two bridges had no direct bus-level diagnostics.

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
    the `PBK_RAILS` rails follow). 16 bits, not 32, because
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
            "`issued` is 0). Bit 4 observes LiteDRAM only: the dedicated CPU "
            "memory port itself publishes no readiness signal here, "
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


#: The masters on the dedicated fabric-memory port, and the number the
#: arbitration floor below is derived from: the descriptor reader, the AECP
#: response-buffer reader/writer and, since #70's backend landed, the
#: saved-state record-image reader/writer (KL_nvm_backend through
#: KL_pp_shadow). test_pp_boot_bus_freeze.py models the port with the same
#: list, in the same insertion order.
PP_MEM_MASTERS = ("milan_desc_mem", "milan_resp_mem", "milan_nvm_mem")


def pp_mem_bus_worst_cycles(sys_clk_hz: float) -> int:
    """Conservative arbitration floor for the protocol-memory masters.

    Only the masters named in PP_MEM_MASTERS share this dedicated
    fabric-memory port, each with one outstanding single-beat access. A
    requester can therefore wait for at most one access of EACH peer before
    its own: two, now that the record-image master is the third. The 45-cycle
    term is the measured memory-port round trip; a peer's access adds one data
    beat. `sys_clk_hz` remains in the signature because the timeout API is
    clock-pair based, but there is no longer a frame-time term.
    """
    del sys_clk_hz
    mem_cycles = 45
    peers = len(PP_MEM_MASTERS) - 1
    return peers * (mem_cycles + 1) + mem_cycles


def pp_mem_timeout_cycles(sys_clk_hz: float, milan_clk_hz: float,
                          proc_tmo_cyc: int = PP_PROC_MEM_TMO_CYC,
                          share: tuple[int, int] = PP_MEM_TMO_SHARE) -> int:
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
    # spuriously under peer-bridge load and every AECP command would answer wrongly.
    worst = pp_mem_bus_worst_cycles(sys_clk_hz)
    if cyc <= worst:
        raise RuntimeError(
            f"the protocol-processor memory-bridge watchdog ({cyc} sys cycles) "
            f"is inside the worst-case memory-port wait ({worst} sys cycles at "
            f"{sys_clk_hz/1e6:g} MHz): a healthy bus would time out. "
            f"milan_clk {milan_clk_hz/1e6:g} MHz is too fast against sys")
    return cyc


def pp_mem_gate(m: Module, dfi_sel: Signal) -> Signal:
    """`mem_rdy`: the DFI has been handed BACK to the LiteDRAM controller.

    A LEVEL, and it is READ from LiteDRAM rather than restated: the BIOS takes
    the DFI away from the controller to level the DDR3 ("Switching SDRAM to
    software control") and hands it back when it is done. `sel` RESETS TO 1
    (litedram/dfii.py DFIInjector, `reset=0b1  # Defaults to HW control.`), so
    hardware control on its own is not evidence that the BIOS ever ran. The
    1 -> 0 -> 1 edge is, and only that edge opens this gate.

    WHAT IT OBSERVES IS ONE HOP, and the label has to say so: that the BIOS got
    past `sdram_init`. It does not observe the CPU's dedicated memory port,
    which is the block that took the AR and never answered it (see the bridge below),
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


def pp_desc_bridge(m: Module, req: Record, rsp: Record, wb: object,
                   mem_rdy: Signal | C, tmo: int, sel_mask: int, addr_sh: int) -> tuple[FSM, Signal, Signal]:
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
    # the flag can clear. On a generic SoC bus the Arbiter gates every
    # slave->master signal on the grant
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
    # watched in EVERY state and not from the bus state's own arm, because on the
    # dedicated memory attachment each master owns its converter (SoCBusHandler.add_master adapts
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


def pp_rw_bridge(m: Module, faces: tuple[Record, Record, Record, Record],
                 wb: object, mem_rdy: Signal | C, tmo: int,
                 geom: tuple[int, int]) -> tuple[FSM, Signal, Signal]:
    """A READ+WRITE main-memory bridge: one wishbone master, one FSM.

    `faces` are the processor-side sys-domain endpoints in the order
    (read request, read response, write, write done); `wb` the master this
    drives, `mem_rdy` the DFI handover gate, `tmo` the watchdog in sys cycles
    and `geom` the `(sel_mask, addr_shift)` pair of the 64-bit lane. Returns
    `(fsm, poisoned, poison_set)` exactly like `pp_desc_bridge`.

    THESE ARE THE RESPONSE-BUFFER BRIDGE'S ARMS, for the saved-state backing
    store's face (KL_nvm_backend through KL_pp_shadow, design page section 8):
    the same contract to the letter - one outstanding single-beat write whose
    strobe rides ONE 64-bit wishbone cycle as `sel` so a zero-strobe byte is
    never modified, an entirely empty strobe skipped rather than issued, the
    write offered first when both are pending, `rsp.ready` as real
    backpressure, the error arm that reads `err` beside `ack`, the watchdog and
    the poison flag (see `pp_desc_bridge` for why a poisoned master keeps
    driving the bus). The response bridge itself stays inline in `MilanSoC`,
    where the waiting bitstreams were exported from; moving it here is a
    follow-up that owes the same netlist-identical export diff the descriptor
    bridge's move produced.
    """
    rq, rs, rw, rd = faces
    sel_mask, addr_sh = geom
    _ra = Signal(32); _rl = Signal(9)
    _rdat = Signal(64); _re = Signal()
    _wa = Signal(32); _wd = Signal(64); _ws = Signal(8); _werr = Signal()
    _rto = Signal(max=tmo + 1)
    _psn = Signal(); _psn_set = Signal()
    m.sync += If(_psn_set, _psn.eq(1)
              ).Elif(_psn & (wb.ack | wb.err), _psn.eq(0))
    fsm = FSM(reset_state="IDLE")
    fsm.act("IDLE",
        rw.ready.eq(1),
        rq.ready.eq(~rw.valid),
        NextValue(_rto, 0),
        If(rw.valid,
            NextValue(_wa, rw.addr), NextValue(_wd, rw.data),
            NextValue(_ws, rw.strb),
            NextValue(_werr, _psn | ~mem_rdy),
            If(mem_rdy, NextState("WR")).Else(NextState("WDONE"))
        ).Elif(rq.valid,
            NextValue(_ra, rq.addr), NextValue(_rl, rq.beats),
            NextValue(_re, _psn | ~mem_rdy),
            If(mem_rdy, NextState("RD")).Else(NextState("REMIT"))))
    fsm.act("WR",
        If(_ws == 0,
            NextState("WDONE")     # no byte enabled: nothing to write
        ).Else(
            wb.cyc.eq(1), wb.stb.eq(1), wb.we.eq(1),
            wb.sel.eq(_ws), wb.adr.eq(_wa[addr_sh:]),
            wb.dat_w.eq(Cat(_wd[56:64], _wd[48:56], _wd[40:48], _wd[32:40],
                            _wd[24:32], _wd[16:24], _wd[8:16],  _wd[0:8])),
            NextValue(_rto, _rto + 1),
            If(wb.ack,
                NextValue(_rto, 0),
                If(wb.err, NextValue(_werr, 1)),
                NextState("WDONE")
            ).Elif(_rto == tmo,
                NextValue(_rto, 0), NextValue(_werr, 1),
                _psn_set.eq(1), NextState("WDONE"))))
    # one cycle here = the one-cycle commit pulse, strictly after `wr_ready`
    fsm.act("WDONE",
        rd.valid.eq(1), rd.err.eq(_werr),
        If(rd.ready, NextState("IDLE")))
    fsm.act("RD",
        wb.cyc.eq(1), wb.stb.eq(1), wb.sel.eq(sel_mask),
        wb.adr.eq(_ra[addr_sh:]),
        NextValue(_rto, _rto + 1),
        If(wb.ack,
            NextValue(_rto, 0),
            If(wb.err, NextValue(_re, 1)
            ).Else(NextValue(_rdat, wb.dat_r)),
            NextState("REMIT")
        ).Elif(_rto == tmo,
            NextValue(_rto, 0), NextValue(_re, 1),
            _psn_set.eq(1), NextState("REMIT")))
    fsm.act("REMIT",
        rs.valid.eq(1), rs.err.eq(_re),
        rs.blast.eq((_rl == 1) | _re),
        rs.data.eq(Cat(_rdat[56:64], _rdat[48:56], _rdat[40:48], _rdat[32:40],
                       _rdat[24:32], _rdat[16:24], _rdat[8:16],  _rdat[0:8])),
        If(rs.ready,
            If(_re | (_rl == 1), NextState("IDLE")
            ).Else(NextValue(_ra, _ra + 8), NextValue(_rl, _rl - 1),
                   NextValue(_rto, 0), NextState("RD"))))
    return fsm, _psn, _psn_set


# SoC ----------------------------------------------------------------------------------------------

class MilanSoC(SoCCore):
    def __init__(self, platform, sys_clk_freq, xlen=64, cpu_count=1,
                 with_milan=True, with_mac=False, with_dram=False,
                 with_spiflash=False, flashboot="none", gtx_tx_invert=False,
                 main_ram_size=0x8000, milan_clk_freq=None,
                 rgmii_tx_delay=2e-9, rgmii_rx_delay=2e-9, l2_bytes=None, with_fpu=False,
                 extra_scala_args=None, cpu="naxriscv",
                 board="ax7101", eth_phy_index=0,
                 num_streams=1, audio_if_slots=0, talker_wire_chans=2,
                 audio_if_master=False,
                 loopback_lane=False,
                 bus_standard="wishbone",
                 software_profile="baremetal",
                 gptp_plane=None,
                 render_lpf=True, optional_blocks=None,
                 entity_gen_dir=None, **kwargs):
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
        # ---- RISC-V core(s). Two cores are understood by the integration, although
        #      the product gate below accepts only cacheless RV32 VexiiRiscv. The
        #      processor descriptor/response bridges need the core's dedicated
        #      fabric-memory attachment whenever the Milan endpoint is present;
        #      it is a structural part of those two protocol faces.
        if cpu == "vexiiriscv":
            from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
            _vex_parser = argparse.ArgumentParser()
            VexiiRiscv.args_fill(_vex_parser)
            _vex_args, _ = _vex_parser.parse_known_args([])
            # cpu_variant is a SoCCore-level argument (not in the CPU parser).
            _vex_args.cpu_variant = "baremetal"
            _vex_args.cpu_count   = cpu_count
            _vex_args.with_dma    = bool(with_milan)
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
            # The protocol processor's two memory faces require the same dedicated
            # attachment on this developer-only CPU shape.
            _nax_args.with_coherent_dma = bool(with_milan)
            # The optional shared L2 is BRAM and its size is a pure config
            # choice: a bigger L2 keeps the bare-metal protocol/application
            # working set out of DDR3 (each miss pays the full DRAM round trip
            # on this 100 MHz core).
            if l2_bytes:
                _nax_args.l2_bytes = int(l2_bytes)
            # Hardware FPU. TWO things must happen and LiteX's --with-fpu only does the
            # first: (1) with_fpu sets the TOOLCHAIN arch/abi to rv64imafd / lp64d; (2) the
            # actual FP hardware is a NaxRiscv Scala-config option (gen.scala `arg("rvf")`
            # / `arg("rvd")`), enabled via --scala-args  -  WITHOUT this the softcore has NO
            # FPU even though the toolchain is hard-float (HW-confirmed 2026-07-05: misa
            # reported rv64ima and an FPU-enabled runtime hung during FP init). scala_args ARE in
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
        # This bus carries no packet payload: with VexiiRiscv the CPU reaches DRAM on
        # its own 256-bit AXI4 mBus and the protocol-processor memory masters use the
        # dedicated 64-bit attachment. The slaves here are rom / sram / spiflash /
        # milan_csr / csr.
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
            # is a silent configuration defect: the build
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
            milan_cd = "milan" if milan_clk_freq else "sys"
            dp_ports, i2s_pads = _board_audio_ports(platform)
            if with_mac:
                self.milan_mac = MilanMAC(platform, data_width=64, milan_cd=milan_cd,
                                          gtx_tx_invert=gtx_tx_invert,
                                          phy_index=eth_phy_index,
                                          phy_model=("mii" if board == "arty" else "gmii"),
                                          rgmii_tx_delay=rgmii_tx_delay,
                                          rgmii_rx_delay=rgmii_rx_delay)
                dp_ports.update(self.milan_mac.dp_ports)
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
            # The direct board-audio binding above publishes whether the I2S
            # Pmod is physically present; a padless board gets structural
            # silence, while the Arty can blend it with the TDM master.
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
                    # the TDM MCLK - override the I2S-Pmod binding.
                    o_i2s_mclk_o  = (self.tdm_pads.mclk if self.tdm_pads
                                     else Signal()),
                )
                if self.tdm_pads is not None and i2s_pads is not None:
                    # HANDOVER 8.3b blend (the Arty): BOTH front-ends are
                    # real, so the override above is itself overridden -
                    # o_i2s_mclk_o goes BACK to the Pmod I2S2 (pmoda:4, D13,
                    # the CS5343 - the pin that must not move) and the TDM
                    # header gets the master's mclk on its OWN pad. The
                    # datapath blends the pair streams (KL_pair_blend, I2S =
                    # pair slot 0).
                    dp_ports["o_i2s_mclk_o"] = i2s_pads[0]
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
            # The platform shape reserves the processor window and this binding
            # checks that the whole reservation lies inside main memory. A base
            # derived independently here could silently diverge from the loader.
            _ram = self.bus.regions["main_ram"]
            _shape = _platform_shape(entity_gen_dir)
            _desc_base  = int(_shape["pp_mem"]["phys"], 16)
            _PP_WINDOW  = int(_shape["pp_mem"]["bytes"], 16)
            # Refuse rather than build a bitstream that writes outside memory.
            if _desc_base < _ram.origin or (
                    _desc_base + _PP_WINDOW) > (_ram.origin + _ram.size):
                raise RuntimeError(
                    f"the protocol processor's window "
                    f"0x{_desc_base:08x}+0x{_PP_WINDOW:x} is not inside "
                    f"main_ram 0x{_ram.origin:08x}+0x{_ram.size:x}")
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
            # - forty-five times the largest shape in the tree. Both bases are
            # derived from one reserved window, so moving it moves both together.
            _resp_base = _desc_base + _PP_WINDOW - 0x1000
            # Published for the manifest that ships with the image. The loader
            # must not restate this address: it is compiled into the gateware,
            # so a loader that guesses it writes the model somewhere the store
            # will never look and the entity stays silent with no error.
            self._pp_windows = {"desc_base": _desc_base,
                                "resp_base": _resp_base,
                                "window_bytes": _PP_WINDOW}
            self.milan = MilanNIC(platform, axil, board_ports=dp_ports or None,
                                  desc_base=_desc_base, resp_base=_resp_base,
                                  milan_cd=milan_cd,
                                  milan_clk_hz=int(milan_clk_freq or sys_clk_freq),
                                  num_streams=int(num_streams),
                                  audio_if_slots=int(audio_if_slots),
                                  talker_wire_chans=int(talker_wire_chans),
                                  audio_if_master=bool(audio_if_master),
                                  # 8.3b blend: on only when the board routes
                                  # BOTH the I2S Pmod and a tdm header (the
                                  # same directly-bound I2S pad tuple the mclk
                                  # rebind used; a padless board never blends)
                                  audio_if_i2s_pair=(self.tdm_pads is not None
                                                     and i2s_pads is not None),
                                  # Preserve None so add_milan_datapath catches
                                  # a severed ownership carrier.
                                  gptp_plane=gptp_plane,
                                  loopback_lane=bool(loopback_lane),
                                  render_lpf=bool(render_lpf),
                                  optional_blocks=optional_blocks,
                                  entity_gen_dir=entity_gen_dir)
            # ===============================================================
            #  AECP DESCRIPTOR-IMAGE READ BRIDGE (protocol-processor 07 §3.3)
            # ===============================================================
            # The processor fetches its entity image through a read-only,
            # 64-bit Wishbone master on the CPU core dedicated memory port.
            # The response-buffer bridge below is the only peer on that port.
            # Both faces propagate bus errors, bound no-progress with a
            # watchdog, and keep a timed-out transaction poisoned until the
            # answer still owed by AXI is collected.
            #
            # The processor contract is one outstanding request, in-order
            # responses, a 9-bit 64-bit-beat count, and big-endian byte lanes.
            # LiteX reports an error with ack, so every ack arm checks err before
            # accepting data. The DFI handover gate prevents either master from
            # issuing while the BIOS owns DDR3 training.
            from litex.soc.interconnect import wishbone as _wb
            import math as _math
            _pp_dw   = 64                      # the processor's memory lane
            _pp_selm = 2**(_pp_dw // 8) - 1
            _pp_adrw = 32 - int(_math.log2(_pp_dw // 8))
            _pp_sh   = int(_math.log2(_pp_dw // 8))
            # Derive a watchdog below the processor per-beat ceiling and above
            # one complete arbitration lap of the PP_MEM_MASTERS. The
            # three-master floor is 137 sys cycles (two peer accesses of 46
            # plus the requester's own 45).
            _pp_tmo = pp_mem_timeout_cycles(sys_clk_freq,
                                            milan_clk_freq or sys_clk_freq)
            # Hold all three masters off while the BIOS owns the LiteDRAM DFI.
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
            _mem_bus = getattr(self, "dma_bus", self.bus)
            _mem_bus.add_master("milan_desc_mem", master=_dwb)

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
            _mem_bus.add_master("milan_resp_mem", master=_rwb)

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
            #  SAVED-STATE RECORD IMAGE READ+WRITE BRIDGE (design page 8)
            # ===============================================================
            # The THIRD master: KL_nvm_backend's, through KL_pp_shadow. The
            # record image sits in the reserved ppmem window between the
            # descriptor image and the response buffer, and the firmware that
            # owns the flash names it to the backend through PP_NVM_SEL/DATA
            # (0x934/0x938); until it does, the backend issues NOTHING on this
            # master and the processor's NVM port sees blank flash. The arms
            # are the response bridge's, in `pp_rw_bridge`: same lane, same
            # strobe rule, same watchdog and poison flag, same DFI gate.
            # ITS EVIDENCE IS THE BACKEND'S OWN: a refused or failed access
            # reaches the processor as `dev_err` and the firmware as
            # PP_NVM_STAT, so this face is not added to the `ppmem` observer
            # below, whose published bit layout is two faces wide.
            self.nvmmem_wb = _nwb = _wb.Interface(data_width=_pp_dw,
                                                  adr_width=_pp_adrw,
                                                  addressing="word")
            _mem_bus.add_master("milan_nvm_mem", master=_nwb)
            self.nvmmem_fsm, _npsn, _npsn_set = pp_rw_bridge(
                self, (self.milan.nvmmem_req_sys, self.milan.nvmmem_rsp_sys,
                       self.milan.nvmmem_wr_sys, self.milan.nvmmem_wd_sys),
                _nwb, _mem_rdy, _pp_tmo, (_pp_selm, _pp_sh))

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

#: REPO_ROOT and SOC_DIR are derived once, beside the imports at the top of
#: this file - `_pp_sources()` runs while `_MILAN_DATAPATH_SOURCES` is being
#: built, long before this point, so the roots cannot live down here.


def _builder_out(entity_gen_dir, name):
    """A file in the end-station builder's output for this config.

    The RTL include dir and the builder's output dir are two faces of ONE
    config, named alike by endstation_builder.py.
    """
    if not entity_gen_dir:
        raise RuntimeError(
            "this build needs its end-station config: pass --entity-gen-dir "
            "(build.sh does, for every named config)")
    cfg = Path(entity_gen_dir).name
    path = REPO_ROOT / "sw" / "builder" / "out" / cfg / name
    if not path.exists():
        raise RuntimeError(
            f"config '{cfg}' has no {name} ({path}). Run the end-station "
            f"builder for this config first")
    # A `str`, named as a boundary: one caller feeds this straight to a migen
    # Instance parameter (p_GPTP_UCODE_HEX_P) and another puts it in a JSON
    # manifest, and neither accepts a PurePath.
    return str(path)


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


def build_desc_image(entity_gen_dir: str | None) -> tuple[bytes, str, str]:
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

    sys.path.insert(0, str(REPO_ROOT / "avdecc"))
    sys.path.insert(0, str(REPO_ROOT / "protocol-processor" / "hdl" /
                           "aecp" / "desc"))
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


def main() -> None:
    """The gateware generator: resolve the build shape from the command line,
    elaborate the SoC, and - before Vivado is asked for anything - build the
    descriptor image and bind every flash artifact it will be shipped with.
    """
    ap = argparse.ArgumentParser(description="Milan RISC-V fabric-control SoC")
    ap.add_argument("--xlen", default=32, type=int, choices=[32, 64],
                    help="CPU register width, honoured by BOTH --cpu choices "
                         "(the bare-metal product profile requires RV32 without an MMU)")
    ap.add_argument("--cpu-count",    default=1, type=int, help="number of cores (this config: 1)")
    ap.add_argument("--cpu",          default="vexiiriscv",
                    choices=["naxriscv","vexiiriscv"],
                    help="soft CPU (the product profile uses vexiiriscv)")
    ap.add_argument("--software-profile", default="baremetal",
                    choices=("baremetal",),
                    help="firmware shape; the product uses the cacheless RV32I "
                         "M-mode Vexii core and Milan UART/CSR firmware")
    ap.add_argument("--with-fpu",     action="store_true", help="hardware FP unit (rv64imafd / lp64d)")
    ap.add_argument("--scala-args",   action="append", default=[],
                    help="extra NaxRiscv scala args, e.g. "
                         "alu-count=1,decode-count=1 (append)")
    ap.add_argument("--sys-clk-freq", default=100e6, type=float)
    ap.add_argument("--board", default="ax7101", choices=["ax7101", "arty"],
                    help="target board: ax7101 (Alinx, 1G GMII, QSPI flashboot) or "
                         "arty (Digilent Arty A7-100: 100M MII DP83848, serial boot, "
                         "second Milan node for AVDECC interop).")
    ap.add_argument("--l2-bytes", default=None, type=float,
                    help="shared-L2 size in bytes (the cacheless RV32I product recipes state 0)")
    ap.add_argument("--milan-clk-freq", default=None, type=float,
                    help="run the Milan datapath in its own slower clock domain (Hz, e.g. "
                         "50e6), async-FIFO CDC'd to sys on the AXI-Lite CSR bus and the "
                         "MAC AXIS boundary  -  lifts the dense datapath off the 100 MHz "
                         "sys critical path (it still exceeds 1 GbE). Works with --full.")
    ap.add_argument("--num-streams", default=1, type=int,
                    help="NxN dataplane width (docs/fpga/FPGA_DESIGN.md section 2): AAF stream "
                         "contexts per shared engine (milan_datapath N_STREAMS). The "
                         "builder emits this from the config's streams section; default "
                         "1 = today's bit-compatible single-stream shape.")
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
    ap.add_argument("--no-datapath-probes", action="store_true",
                    help="AREA LEVER: prune the APRB (0x8B4-0x8C4) and PBK "
                         "(0x8C8-0x8D0) probe groups - closed-finding "
                         "diagnostics; the range reads 0 on a pruned build "
                         "(the LTAP precedent). Default off => probes PRESENT.")
    ap.add_argument("--no-rx-mac-filter", action="store_true",
                    help="AREA LEVER: prune rx_mac_filter + its TCAM. The RX stream "
                         "becomes a straight wire to the fabric observers, which is bit-exactly "
                         "what the filter does with promisc=1 - so this is legal only "
                         "when the port is meant to be PROMISCUOUS. The TCAM_* CSR window still accepts writes and "
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
    ap.add_argument("--with-dram", action="store_true",
                    help="512 MB DDR3 via LiteDRAM (A7DDRPHY + MT41J256M16)")
    ap.add_argument("--bus-standard", default="wishbone", choices=["wishbone", "axi-lite"],
                    help="main SoC bus standard. 'axi-lite' makes the control path AXI end "
                         "to end and deletes the two round-trip bridges LiteX inserts when "
                         "the default 'wishbone' sits between the CPU's AXI-Lite pBus and "
                         "the AXI-Lite milan_csr window (OOC: 106 + 150 LUT, minus 18 for "
                         "AXILite2CSR over Wishbone2CSR). Carries no packet payload.")
    ap.add_argument("--with-spiflash", action="store_true",
                    help="memory-map the on-board N25Q128 QSPI flash (16 MB) so the BIOS can "
                         "load the bare-metal AEM image. "
                         "Included by --full.")
    ap.add_argument("--flashboot", default="none",
                    choices=["none", "baremetal"],
                    help="which artifacts live in flash (needs --with-spiflash or --full): "
                         "'baremetal' stores the raw AEM image beside the bitstream; 'none' "
                         "(default) maps the flash but adds no boot method.")
    ap.add_argument("--full", action="store_true",
                    help="enable the complete fabric endpoint + MAC/PHY + DDR3 "
                         "(= --with-mac --with-dram). Physical two-board traffic "
                         "acceptance remains a separate bench obligation.")
    ap.add_argument("--eth-port", default="e1", choices=["e1", "e2"],
                    help="AX7101 PHY port: e1 (default) or e2 — the e1-GMII-RX "
                         "hardware-fault fallback (2026-07-22); both are 8-bit GMII")
    ap.add_argument("--gtx-tx-invert", action="store_true",
                    help="forward GMII gtx_clk 180° out of phase with TXD so the PHY samples "
                         "mid-bit - the GMII-TX setup/hold correction for the RTL8211E. "
                         "Default off = edge-aligned.")
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
                         "is set via --sys-clk-freq.")
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
                   with_mac=args.with_mac or args.full,
                   with_dram=args.with_dram or args.full,
                   with_spiflash=args.with_spiflash or args.full,
                   flashboot=args.flashboot,
                   gtx_tx_invert=args.gtx_tx_invert,
                   main_ram_size=args.main_ram_size,
                   milan_clk_freq=args.milan_clk_freq, l2_bytes=args.l2_bytes,
                   num_streams=args.num_streams,
                   gptp_plane=args.fabric_gptp,
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
                   entity_gen_dir=args.entity_gen_dir,
                   audio_if_slots={"i2s_philips": 0, "tdm8": 8, "tdm16": 16,
                                   "tdm32": 32}[args.audio_interface],
                   talker_wire_chans=int(args.talker_wire_chans),
                   audio_if_master=bool(args.audio_interface_master),
                   eth_phy_index=(1 if args.eth_port == "e2" else 0),
                   with_fpu=args.with_fpu, extra_scala_args=args.scala_args,
                   software_profile=args.software_profile,
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
        # clock is raised separately via --sys-clk-freq.)
        soc.platform.add_platform_command("set_multicycle_path 2 -setup -through [get_nets sys_rst]")
        soc.platform.add_platform_command("set_multicycle_path 1 -hold  -through [get_nets sys_rst]")
    builder = Builder(soc, **builder_argdict(args))
    if args.software_profile == "baremetal":
        fw_dir = str(REPO_ROOT / "sw" / "firmware" / "milan_baremetal")
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
    _out_dir = Path(builder.output_dir)
    if _desc_blob is not None:
        _img_path = _out_dir / "aem_desc.bin"
        _img_path.write_bytes(_desc_blob)
        _aem_binding = aem_image_binding(_img_path)
        _man = {
            "desc_base": soc._pp_windows["desc_base"],
            "resp_base": soc._pp_windows["resp_base"],
            "window_bytes": soc._pp_windows["window_bytes"],
            "image": "aem_desc.bin",
            "image_bytes": len(_desc_blob),
            # `str`, and it has to be: this dict is json.dump-ed below.
            # `_builder_out` built the overlay path under REPO_ROOT, so the
            # relative walk is always downwards and never needs a `..`.
            "overlay": str(Path(_desc_overlay).relative_to(REPO_ROOT)),
        }
        with open(_out_dir / "aem_desc.json", "w") as f:
            json.dump(_man, f, indent=2)
        with open(_out_dir / "aem_desc.map", "w") as f:
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
            if not Path(bit_path).is_file():
                raise RuntimeError(
                    f"Vivado build produced no bitstream for layout binding: {bit_path}")
            soc._flashboot_layout.update(bitstream_binding(bit_path))
        layout_path = _out_dir / "flashboot_layout.json"
        with open(layout_path, "w") as f:
            json.dump(soc._flashboot_layout, f, indent=2)
        print(f"[milan] flash-boot layout ({args.flashboot}) -> {layout_path}")
    if args.load:
        prog = platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))


if __name__ == "__main__":
    main()
