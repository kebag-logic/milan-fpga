#
# LiteX platform for the Alinx AX7101 (Xilinx Artix-7 xc7a100t).
# Part of the Milan fully-FPGA SoC (sw/litex/milan_soc.py). Not in upstream
# litex_boards, so we ship it locally. Pin assignments follow the AX7101 user
# manual; they matter for place-&-route (Vivado) but not for gateware export.
#
# SPDX-License-Identifier: (GPL-2.0 OR MIT)

from litex.build.generic_platform import Pins, Subsignal, IOStandard
from litex.build.xilinx import Xilinx7SeriesPlatform
from litex.build.openocd import OpenOCD

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # 200 MHz differential system clock + active-low reset button (AX7101 bank 34).
    ("clk200", 0,
        Subsignal("p", Pins("R4"), IOStandard("DIFF_SSTL15")),
        Subsignal("n", Pins("T4"), IOStandard("DIFF_SSTL15")),
    ),
    ("cpu_reset_n", 0, Pins("T6"), IOStandard("LVCMOS15")),

    # USB-UART (CP210x) console.
    ("serial", 0,
        Subsignal("tx", Pins("N15"), IOStandard("LVCMOS33")),
        Subsignal("rx", Pins("P20"), IOStandard("LVCMOS33")),
    ),

    # User LEDs (boot / heartbeat indicators).
    ("user_led", 0, Pins("B13"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("C13"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("D14"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("D15"), IOStandard("LVCMOS33")),

    # RGMII PHY0 (the Milan NIC port) — RTL8211 @ MDIO addr 1.
    ("eth_clocks", 0,
        Subsignal("tx", Pins("E18")),
        Subsignal("rx", Pins("B17")),
        IOStandard("LVCMOS33"),
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("D16"), IOStandard("LVCMOS33")),
        Subsignal("mdio",    Pins("B15"), IOStandard("LVCMOS33")),
        Subsignal("mdc",     Pins("B16"), IOStandard("LVCMOS33")),
        Subsignal("rx_ctl",  Pins("A15"), IOStandard("LVCMOS33")),
        Subsignal("rx_data", Pins("A16 B18 C18 C19"), IOStandard("LVCMOS33")),
        Subsignal("tx_ctl",  Pins("F18"), IOStandard("LVCMOS33")),
        Subsignal("tx_data", Pins("C20 D20 A19 A18"), IOStandard("LVCMOS33")),
    ),
    # RGMII PHY1 (second Milan port).
    ("eth_clocks", 1,
        Subsignal("tx", Pins("A14")),
        Subsignal("rx", Pins("E19")),
        IOStandard("LVCMOS33"),
    ),
    ("eth", 1,
        Subsignal("rst_n",   Pins("B22"), IOStandard("LVCMOS33")),
        Subsignal("mdio",    Pins("C22"), IOStandard("LVCMOS33")),
        Subsignal("mdc",     Pins("F20"), IOStandard("LVCMOS33")),
        Subsignal("rx_ctl",  Pins("F19"), IOStandard("LVCMOS33")),
        Subsignal("rx_data", Pins("A20 B20 D19 C17"), IOStandard("LVCMOS33")),
        Subsignal("tx_ctl",  Pins("D17"), IOStandard("LVCMOS33")),
        Subsignal("tx_data", Pins("E17 C14 C15 A13"), IOStandard("LVCMOS33")),
    ),
]

_connectors = []

# Platform -----------------------------------------------------------------------------------------

class Platform(Xilinx7SeriesPlatform):
    default_clk_name   = "clk200"
    default_clk_period = 1e9 / 200e6

    def __init__(self, toolchain="vivado"):
        Xilinx7SeriesPlatform.__init__(self, "xc7a100t-fgg484-2", _io, _connectors,
                                       toolchain=toolchain)

    def create_programmer(self):
        return OpenOCD("openocd_xc7_ft2232.cfg", "bscan_spi_xc7a100t.bit")

    def do_finalize(self, fragment):
        Xilinx7SeriesPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk200", loose=True), 1e9 / 200e6)
