#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Emit the production LED attachment, including its two clock crossings."""
import sys
from pathlib import Path
from types import SimpleNamespace

from migen import ClockDomain, Module, Signal
from migen.fhdl import verilog

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "sw/litex"))
from usbnet_soc import LED_LEVELS, LedInputs, StatusLeds


class Platform:
    """Only the source list and RGB pads used by the production attachment."""

    def __init__(self) -> None:
        self.pads = [SimpleNamespace(**{c: Signal(name=f"led{n}_{c}") for c in "rgb"}) for n in range(4)]

    def add_source(self, path: str) -> None:
        """The Makefile supplies these same sources to the simulator."""
        assert Path(path).is_file()

    def request(self, name: str, index: int) -> object:
        """Expose the board's three colour channels without replacing the attachment."""
        assert name == "rgb_led"
        return self.pads[index]


def main() -> None:
    """Keep the two clocks independent and expose the status before PWM."""
    module = Module()
    module.clock_domains.cd_sys = ClockDomain("sys")
    module.clock_domains.cd_milan = ClockDomain("milan")
    levels = {name: Signal(name=name) for name in LED_LEVELS}
    link, activity, usb = (Signal(name=name) for name in ("link", "activity", "usb"))
    platform = Platform()
    module.submodules.leds = leds = StatusLeds(platform, 100000, ROOT,
                                              LedInputs(link, activity, usb, levels, "milan"))
    state = Signal(4, name="state")
    module.comb += state.eq(leds.state.fields.leds)
    ports = {link, activity, usb, state, *levels.values(),
             module.cd_sys.clk, module.cd_sys.rst, module.cd_milan.clk, module.cd_milan.rst}
    ports.update(pad for rgb in platform.pads for pad in vars(rgb).values())
    Path(sys.argv[1]).write_text(str(verilog.convert(module, ios=ports, name="led_attachment")))


if __name__ == "__main__":
    main()
