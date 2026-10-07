#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check GMII capture against its pre-patch synchronous-reset contract.

The oracle follows pad samples, not the implementation's internal signals.
Every byte is sampled with both valid levels and both reset levels. Reset
also changes between edges, including at the last-byte boundary. A reset
mask using the live reset instead of its sampled value must fail here.
"""

from collections.abc import Generator
import argparse
from pathlib import Path

from migen import ClockDomain, Instance, Module, Record, Signal
from migen.fhdl import verilog
from migen.sim import run_simulation
from liteeth.phy.gmii import LiteEthPHYGMIIRX


class CaptureBench(Module):
    """Expose a controllable reset and the product's actual RX capture."""

    def __init__(self, reset_before_d: bool = False) -> None:
        self.clock_domains.cd_sys = ClockDomain("sys")
        self.pads = Record([("rx_dv", 1), ("rx_data", 8), ("rx_er", 1)])
        self.reset = Signal()
        self.comb += self.cd_sys.rst.eq(self.reset)
        capture_pads = self.pads
        if reset_before_d:
            capture_pads = Record([("rx_dv", 1), ("rx_data", 8)])
            # Preserve the planted LUTs: synthesis must not repair this
            # negative control by absorbing them into reset pins.
            for pad, masked in [(self.pads.rx_dv, capture_pads.rx_dv),
                                *zip(self.pads.rx_data, capture_pads.rx_data)]:
                self.specials += Instance("LUT2", p_INIT=2,
                    i_I0=pad, i_I1=self.reset, o_O=masked,
                    attr={"dont_touch"})
        self.submodules.rx = LiteEthPHYGMIIRX(capture_pads)


def check_capture() -> int:
    """Compare visible outputs before and after each sampling edge."""
    dut = CaptureBench()
    checked = 0

    def stimulus() -> Generator:
        """Exercise pad, reset and ready changes between sample edges."""
        nonlocal checked
        previous_valid = 0
        previous_data = 0
        # The simulator applies drives after an edge. Before the following
        # sample updates, only last may respond to the new pad-valid level.
        for value in range(256):
            for valid in (0, 1):
                for reset in (0, 1):
                    yield dut.pads.rx_dv.eq(valid)
                    yield dut.pads.rx_data.eq(value)
                    yield dut.pads.rx_er.eq(value & 1)
                    yield dut.reset.eq(reset)
                    yield dut.rx.source.ready.eq(value & 1)
                    yield
                    expected_valid = valid if not reset else 0
                    expected_data = value if not reset else 0
                    got = ((yield dut.rx.source.valid),
                           (yield dut.rx.source.data),
                           (yield dut.rx.source.last))
                    expected = (previous_valid, previous_data,
                                (1 - valid) & previous_valid)
                    assert got == expected, (value, valid, reset, got, expected)
                    checked += 1
                    previous_valid = expected_valid
                    previous_data = expected_data
        yield
        assert (yield dut.rx.source.valid) == previous_valid
        assert (yield dut.rx.source.data) == previous_data
        checked += 1

    run_simulation(dut, stimulus())
    return checked


def emit_capture(directory: Path) -> None:
    """Generate the actual capture and a reset-before-D placement control."""
    directory.mkdir(parents=True, exist_ok=True)
    for defect in (False, True):
        # Plant reset before capture through the production receiver.
        # Both fixtures are generated, with no hand-edited output HDL.
        dut = CaptureBench(reset_before_d=defect)
        ports = {dut.cd_sys.clk, dut.reset, dut.pads.rx_dv, dut.pads.rx_data,
                 dut.rx.source.valid, dut.rx.source.data, dut.rx.source.last}
        converted = verilog.convert(dut, ios=ports, name="gmii_capture")
        name = "reset_before_d" if defect else "capture"
        converted.write(str(directory / f"{name}.v"))


def main() -> None:
    """Fail the process on a sample mismatch."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-dir", type=Path)
    args = parser.parse_args()
    checked = check_capture()
    if args.emit_dir is not None:
        emit_capture(args.emit_dir)
    print(f"RESULT: PASS ({checked} GMII capture comparisons)")


if __name__ == "__main__":
    main()
