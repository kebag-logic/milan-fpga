#
# LiteX platform for the Alinx AX7101 (Xilinx Artix-7 XC7A100T-2FGG484I).
# Part of the Milan fully-FPGA SoC (sw/litex/milan_soc.py). Not in upstream
# litex_boards, so we ship it locally.
#
# Pin assignments are PORTED FROM THE OFFICIAL ALINX AX7101 CONSTRAINTS
# (github.com/alinxalinx/AX7101): the LED/clock/reset + UART example XDCs, the
# rgmii_ethernet example XDC (4× RTL8211E PHYs — the Milan NIC uses ports e1/e2),
# and the DDR3 MIG UCF (512 MB MT41J256M16, parsed into the `ddram` group). See
# docs/integration/BOARD_PORTING_AX7101.md for the porting method + sources.
#
# SPDX-License-Identifier: (GPL-2.0 OR MIT)

from litex.build.generic_platform import Pins, Subsignal, IOStandard, Misc
from litex.build.xilinx import Xilinx7SeriesPlatform
from litex.build.openfpgaloader import OpenFPGALoader

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # 200 MHz differential system clock (siT9102) + active-low reset key (bank 34).
    ("clk200", 0,
        Subsignal("p", Pins("R4"), IOStandard("DIFF_SSTL15")),
        Subsignal("n", Pins("T4"), IOStandard("DIFF_SSTL15")),
    ),
    ("cpu_reset_n", 0, Pins("T6"), IOStandard("LVCMOS15")),

    # USB-UART console (CP2102 -> /dev/ttyUSB console).
    ("serial", 0,
        Subsignal("tx", Pins("AB15"), IOStandard("LVCMOS33")),
        Subsignal("rx", Pins("AA15"), IOStandard("LVCMOS33")),
    ),

    # User LEDs.
    ("user_led", 0, Pins("E17"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("F16"), IOStandard("LVCMOS33")),

    # GMII PHY0 = the AX7101 "e1" RTL8211E (the Milan NIC first port). The board wires
    # the RTL8211E in **GMII** mode — 8-bit SDR, separate RX_DV/RX_ER, gtx+rx+tx clocks
    # (per the Alinx SRC/15_ethernet_test top: `input [7:0] e_rxd`, e_rxdv, e_rxer,
    # `assign e_gtxc=e_rxc`). NOT RGMII: a 4-bit-DDR RGMII read of this 8-bit-SDR bus
    # corrupts every byte (hardware-confirmed: 100% MAC preamble errors).
    ("eth_clocks", 0,
        Subsignal("rx",  Pins("K18")),   # e1_rxc  (PHY->FPGA 125 MHz)
        Subsignal("gtx", Pins("G21")),   # e1_gtxc (FPGA->PHY 125 MHz, 1G TX)
        Subsignal("tx",  Pins("K21")),   # e1_txc  (MII 25 MHz, 10/100)
        IOStandard("LVCMOS33"),
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("G20"), IOStandard("LVCMOS33")),   # e1_reset
        Subsignal("rx_dv",   Pins("M22"), IOStandard("LVCMOS33")),   # e1_rxdv
        Subsignal("rx_er",   Pins("N18"), IOStandard("LVCMOS33")),   # e1_rxer
        Subsignal("rx_data", Pins("N22 H18 H17 M21 L21 N20 M20 N19"),
                  IOStandard("LVCMOS33")),                            # e1_rxd[0:7]
        Subsignal("tx_en",   Pins("G22"), IOStandard("LVCMOS33")),   # e1_txen
        Subsignal("tx_data", Pins("D22 H20 H22 J22 K22 L19 K19 L20"),
                  IOStandard("LVCMOS33")),                            # e1_txd[0:7]
        # PHY management (2026-07-22): e1_mdc = J17 (every
        # vendor example XDC), e1_mdio = L16 (EX SCH: E1_MDIO = B15_L23_P;
        # CORE SCH: B15_L23_P = ball L16/IO_L23P_T3_FOE_B_15). NB the EX
        # schematic's pdftotext pairs labels ONE ROW BELOW their nets — the
        # first read gave K16/B15_L23_N, which is really E2_TXD1 (silicon:
        # pull-up line, drives fine, no PHY ever answered); anchors RXD5=
        # B15_L18_P=N20 / RXD6=B15_L18_N=M20 pin the offset against the
        # vendor XDC. liteeth's GMII PHY auto-adds the LiteEthPHYMDIO
        # bitbang CSRs when mdc is present.
        Subsignal("mdc",  Pins("J17"), IOStandard("LVCMOS33")),
        Subsignal("mdio", Pins("L16"), IOStandard("LVCMOS33"), Misc("PULLUP TRUE")),
    ),
    # GMII PHY1 = the AX7101 "e2" RTL8211E — the e1-fault fallback port
    # (2026-07-22: e1's GMII-RX died in hardware, cold-soak-proven). The
    # vendor 4-port example wires e2 EXACTLY like e1: 8-bit bus, separate
    # rxdv/rxer, gtxc — i.e. GMII, not RGMII (all pins from the vendor
    # propImpl XDC). e2_mdio = AB22 (EX SCH: E2_MDIO = B14_L10_N; CORE:
    # B14_L10_N = AB22 — anchor-verified on the same row as E2_MDC =
    # B14_L10_P = AB21, which the vendor XDC confirms).
    ("eth_clocks", 1,
        Subsignal("rx",  Pins("J20")),   # e2_rxc
        Subsignal("gtx", Pins("M16")),   # e2_gtxc
        Subsignal("tx",  Pins("T14")),   # e2_txc (MII 10/100)
        IOStandard("LVCMOS33"),
    ),
    ("eth", 1,
        Subsignal("rst_n",   Pins("L14"), IOStandard("LVCMOS33")),   # e2_reset
        Subsignal("rx_dv",   Pins("L13"), IOStandard("LVCMOS33")),   # e2_rxdv
        Subsignal("rx_er",   Pins("G13"), IOStandard("LVCMOS33")),   # e2_rxer
        Subsignal("rx_data", Pins("M13 K14 K13 J14 H14 H15 J15 H13"),
                  IOStandard("LVCMOS33")),                            # e2_rxd[0:7]
        Subsignal("tx_en",   Pins("M15"), IOStandard("LVCMOS33")),   # e2_txen
        Subsignal("tx_data", Pins("L15 K16 W15 W16 V17 W17 U15 V15"),
                  IOStandard("LVCMOS33")),                            # e2_txd[0:7]
        Subsignal("mdc",  Pins("AB21"), IOStandard("LVCMOS33")),
        Subsignal("mdio", Pins("AB22"), IOStandard("LVCMOS33"), Misc("PULLUP TRUE")),
    ),

    # QSPI configuration flash = Micron N25Q128 (128 Mbit / 16 MB), confirmed from the
    # Alinx AX7101 repo (DATASHEET/QSPI FLASH/N25Q128.pdf). The FPGA boots its bitstream
    # from here in master-SPI x4 mode; after configuration the LiteSPI core re-drives it
    # (litespi module `N25Q128A13`, quad read 0x6B, 3-byte address → the whole 16 MB is
    # reachable). Pins are the Xilinx dedicated config pins for the FGG484 package (BANK14
    # data + FCS_B, BANK0 CCLK) — cross-checked against three independent xc7a*t-fgg484
    # LiteX boards (myir_myc_j7a100t, alchitry_pt_v2, numato_mimas_a7):
    #   cs_n = T19 (FCS_B) ; dq = P22 R22 P21 R21 (D00_MOSI D01_DIN D02/WP# D03/HOLD#).
    # CCLK is NOT a fabric pin: LiteSPI drives it through the STARTUPE2/USRCCLKO primitive
    # (litespi/clkgen.py), so no `clk` subsignal is listed. mode="4x" drives all four DQ,
    # so WP#/HOLD# are never left floating (which Vivado's default UNUSEDPIN=PULLDOWN would
    # otherwise pull low and freeze the chip).
    ("spiflash4x", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("dq",   Pins("P22 R22 P21 R21")),
        IOStandard("LVCMOS33"),
    ),
    # 1x fallback (single-lane 0x03 read) — same pads; use if quad ever misbehaves.
    ("spiflash", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("mosi", Pins("P22")),
        Subsignal("miso", Pins("R22")),
        Subsignal("wp",   Pins("P21")),
        Subsignal("hold", Pins("R21")),
        IOStandard("LVCMOS33"),
    ),

    # item-4 TDM audio header on J11 — the AAF talker's capture front-end when
    # the build is the TDM bus MASTER (milan_soc.py --audio-interface-master ->
    # milan_datapath AUDIO_IF_MASTER_P -> KL_tdm_capture_master). WHY THIS
    # EXISTS: the AX7101 has `_connectors = []`, so there is no pmoda, so
    # `i2s_pads = None` and `i_i2s_sdout_i = 0` — its capture front-end clocked
    # in a constant zero and produced ONE pair of digital SILENCE, which is the
    # 2-channel frame a Milan-validated listener received where 8 were promised
    # (silicon 2026-07-27, UNSUPPORTED_FORMAT on 296,294 of 296,294 frames).
    #
    # THE HEADER.  J11, "FPGA 40 PIN External IO", HEADER 20x2/M — the ONLY
    # 40-pin expansion header on the board (SCH/AX7101_EX_SCH.pdf; a grep for
    # `HEADER 20x2` over the whole EX schematic returns exactly one).  Odd pins
    # are EX_IO1_kN, even pins EX_IO1_kP, k = 1..17, each through a 33 R series
    # resistor (RN1..RN9) between the FPGA net and the header pin — source-
    # series termination, which is what a 49.152 MHz bclk wants; keep the
    # ribbon short.  All of J11 is on banks 15/16, and AC7100_CORE_SCH.pdf's
    # power page groups VCCO_13/14/15/16 under +3.3V VCCIO (VCCO_34/35, the
    # DDR3 banks above, are the +1.5V ones), so LVCMOS33 — which is also what
    # every vendor XDC constrains these pins to.
    #
    # THE PINS.  Deliberately the block the VENDOR ITSELF uses for audio: the
    # WM8731 codec example, SRC/08_audio_record_play/.../audio_record_play.xdc,
    # puts its I2S bus on exactly these five balls, all bank 16, contiguous on
    # J11 pins 3-8.  Choosing them means a stock Alinx WM8731 daughterboard
    # plugs straight in, and it means every pin here is vendor-proven at this
    # IOSTANDARD rather than inferred:
    #
    #   ball  J11  vendor net (evidence)                       role here
    #   B22    3   clk_out, SRC/03_pll_test/.../pll.xdc:17     mclk  (out)
    #              under the header comment "J11PIN3" — the
    #              absolute pin-number anchor for the whole
    #              connector, and the one J11 pin the vendor
    #              demonstrates as an ODDR-forwarded CLOCK OUT
    #              (pll_test.v:56,63-73).  Also wm8731_scl.
    #   B20    6   wm8731_bclk   (audio_record_play.xdc:33)    bclk  (out)
    #   F20    7   wm8731_adcdat (audio_record_play.xdc:34)    din   (in)
    #   F19    8   wm8731_daclrc (audio_record_play.xdc:35)    fsync (out)
    #   A20    5   wm8731_dacdat (audio_record_play.xdc:32)    dout  (out)
    #
    # The ball<->J11-pin order is confirmed three ways: SRC/06_3_an070_lcd_test
    # and SRC/06_2_an430_lcd_test both list the identical ball sequence under
    # "on AX7101 J11" for two DIFFERENT LCD modules, and every odd J11 pin
    # lands on the _N half of a diff pair and every even pin on the _P half,
    # unbroken across all 17 pairs.  Ball<->bank came from AC7100_CORE_SCH.pdf
    # (NOT the EX schematic, whose pdftotext pairs labels one row below their
    # nets — the trap recorded on e1_mdio above); the CORE sheet was validated
    # against five facts already proven on this board (e1_mdio=L16,
    # e2_mdc/mdio=AB21/AB22, e1_rxd5/6=N20/M20, QSPI_CS=T19) before being
    # trusted.  Zero collisions with any ball already claimed in this file.
    #
    # NONE of the five is clock-capable, and that is correct: MRCC/SRCC only
    # matters for a pin feeding a BUFG/MMCM, and all three clocks here are
    # OUTPUTS.  If an external word clock is ever fed IN, move that signal to
    # the bank-16 SRCC pair D19/E19 (J11 23/24) or the MRCC pair C19/C18
    # (J11 31/32).
    ("tdm", 0,
        Subsignal("mclk",  Pins("B22")),   # J11.3
        Subsignal("dout",  Pins("A20")),   # J11.5  fabric -> codec (render)
        Subsignal("bclk",  Pins("B20")),   # J11.6
        Subsignal("din",   Pins("F20")),   # J11.7  codec -> fabric (capture)
        Subsignal("fsync", Pins("F19")),   # J11.8
        #! MEDIA-GRID TEST POINT (J11.9, ball J16 - free, and the next pin
        #! along from fsync so a two-channel probe reaches both on one clip).
        #!
        #! WHY IT EXISTS. On the TDM8-master shape fsync above is derived from
        #! clk_audio (24,575,738.53 Hz / 512 = 47,999.4893 Hz, i.e. -10.64 ppm
        #! by construction), while the AAF packet grid is media_tick_p off the
        #! 100 MHz milan clock. Those are DIFFERENT CLOCKS about 10.6 ppm
        #! apart, and until now nothing on the board could observe the second
        #! one - no CSR carries it and no capture shows it. Bringing it out
        #! beside fsync makes the difference a scope or frequency counter can
        #! read directly, with no peer device in the loop.
        #!
        #! SEMANTICS: it TOGGLES on every media sample tick, so it is a clean
        #! 50%-duty square at fs/2 = 24 kHz, not a 48 kHz pulse train. Multiply
        #! by two, or just compare its edges against fsync.
        Subsignal("lrclk", Pins("J16")),   # J11.9
        IOStandard("LVCMOS33"),
    ),

    # DDR3 — 512 MB (2× MT41J256M16, 32-bit). Parsed from the AX7101 MIG UCF (ddr3.ucf).
    ("ddram", 0,
        Subsignal("a", Pins("AA4 AB2 AA5 AB5 AB1 U3 W1 T1 V2 U2 Y1 W2 Y2 U1 V3"), IOStandard("SSTL15")),
        Subsignal("ba", Pins("AA3 Y3 Y4"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("V4"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("W4"), IOStandard("SSTL15")),
        Subsignal("we_n", Pins("AA1"), IOStandard("SSTL15")),
        Subsignal("cs_n", Pins("AB3"), IOStandard("SSTL15")),
        Subsignal("dm", Pins("D2 G2 M2 M5"), IOStandard("SSTL15")),
        Subsignal("dq", Pins(
            "C2 G1 A1 F3 B2 F1 B1 E2 H3 G3 H2 H5 J1 J5 K1 H4 "
            "L4 M3 L3 J6 K3 K6 J4 L5 P1 N4 R1 N2 M6 N5 P6 P2"), IOStandard("SSTL15")),
        Subsignal("dqs_p", Pins("E1 K2 M1 P5"), IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n", Pins("D1 J2 L1 P4"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p", Pins("R3"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("R2"), IOStandard("DIFF_SSTL15")),
        Subsignal("cke", Pins("T5"), IOStandard("SSTL15")),
        Subsignal("odt", Pins("U5"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("W6"), IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
    ),
]

_connectors = []

# Platform -----------------------------------------------------------------------------------------

class Platform(Xilinx7SeriesPlatform):
    default_clk_name   = "clk200"
    default_clk_period = 1e9 / 200e6

    def __init__(self, toolchain="vivado"):
        # XC7A100T-2FGG484I: Artix-7, FGG484 package, speed grade -2.
        Xilinx7SeriesPlatform.__init__(self, "xc7a100t-fgg484-2", _io, _connectors,
                                       toolchain=toolchain)
        self.toolchain.bitstream_commands = [
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "set_property CONFIG_MODE SPIx4 [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 50 [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
        ]

    def create_programmer(self):
        # AX7101 JTAG = onboard Digilent FT232H (USB 0403:6014). Verified on hardware:
        # `openFPGALoader -c ft232 --detect` reads IDCODE = xc7a100t. `--load` SRAM-loads
        # the bitstream over JTAG.
        return OpenFPGALoader(cable="ft232")

    def do_finalize(self, fragment):
        Xilinx7SeriesPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk200", loose=True), 1e9 / 200e6)
        # NOTE: the GMII TX IOB-packing constraint lives in MilanMAC (milan_soc.py), which
        # emits it only when the MAC/pads exist. It must be plain `set_property` lines: XDC
        # does NOT execute TCL control flow, so an `if {...}` guard here is silently skipped
        # (hardware-diagnosed: the "guarded" constraint left the TX FFs in fabric at X14).
