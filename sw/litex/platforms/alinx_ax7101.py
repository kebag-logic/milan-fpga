#
# LiteX platform for the Alinx AX7101 (Xilinx Artix-7 XC7A100T-2FGG484I).
# Part of the Milan fully-FPGA SoC (sw/litex/milan_soc.py). Not in upstream
# litex_boards, so we ship it locally.
#
# Pin assignments are PORTED FROM THE OFFICIAL ALINX AX7101 CONSTRAINTS
# (github.com/alinxalinx/AX7101): the LED/clock/reset + UART example XDCs, the
# rgmii_ethernet example XDC (4× RTL8211E PHYs — the Milan NIC uses ports e1/e2),
# and the DDR3 MIG UCF (512 MB MT41J256M16, parsed into the `ddram` group). See
# docs/BOARD_PORTING_AX7101.md for the porting method + sources.
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

    # RGMII PHY0 = the AX7101 "e1" RTL8211E (the Milan NIC first port).
    ("eth_clocks", 0,
        Subsignal("tx", Pins("G21")),   # e1_gtxc (FPGA->PHY 125 MHz)
        Subsignal("rx", Pins("K18")),   # e1_rxc  (PHY->FPGA)
        IOStandard("LVCMOS33"),
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("G20"), IOStandard("LVCMOS33")),   # e1_reset
        # PHY management: e1_mdc = J17; the MDIO *data* pin is not in the Alinx GMII
        # example XDC (take it from SCH/AX7101_EX_SCH.pdf). Left unwired for now — the
        # RGMII data path works on the PHY power-on straps; MDIO management is §A.7.
        # Subsignal("mdc", Pins("J17"), IOStandard("LVCMOS33")),
        # Subsignal("mdio", Pins("<from schematic>"), IOStandard("LVCMOS33")),
        Subsignal("rx_ctl",  Pins("M22"), IOStandard("LVCMOS33")),   # e1_rxdv
        Subsignal("rx_data", Pins("N22 H18 H17 M21"), IOStandard("LVCMOS33")),  # e1_rxd[0:3]
        Subsignal("tx_ctl",  Pins("G22"), IOStandard("LVCMOS33")),   # e1_txen
        Subsignal("tx_data", Pins("D22 H20 H22 J22"), IOStandard("LVCMOS33")),  # e1_txd[0:3]
    ),
    # RGMII PHY1 = the AX7101 "e2" RTL8211E (the Milan NIC second port).
    ("eth_clocks", 1,
        Subsignal("tx", Pins("M16")),   # e2_gtxc
        Subsignal("rx", Pins("J20")),   # e2_rxc
        IOStandard("LVCMOS33"),
    ),
    ("eth", 1,
        Subsignal("rst_n",   Pins("L14"), IOStandard("LVCMOS33")),   # e2_reset
        # PHY management: e2_mdc = AB21; MDIO data pin from SCH (see PHY0 note above).
        # Subsignal("mdc", Pins("AB21"), IOStandard("LVCMOS33")),
        Subsignal("rx_ctl",  Pins("L13"), IOStandard("LVCMOS33")),   # e2_rxdv
        Subsignal("rx_data", Pins("M13 K14 K13 J14"), IOStandard("LVCMOS33")),  # e2_rxd[0:3]
        Subsignal("tx_ctl",  Pins("M15"), IOStandard("LVCMOS33")),   # e2_txen
        Subsignal("tx_data", Pins("L15 K16 W15 W16"), IOStandard("LVCMOS33")),  # e2_txd[0:3]
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
