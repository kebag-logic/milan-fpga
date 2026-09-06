#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The CPU memory port crosses from the CPU clock into the LiteDRAM clock (#359).

`milan_soc.cross_cpu_memory_ports` is the shipping hook. These checks build it
on a stand-in CPU object shaped like LiteX's VexiiRiscv (a `cpu_clk` attribute,
`memory_buses`, an `add_memory_buses` method that appends an AXI port) and
grade three things:

  1. SHAPE. With `cpu_clk` present, after `add_memory_buses` the port LiteDRAM
     would read is a `sys`-domain AXI interface, distinct from the CPU's own
     port, with the same data width, address width, id width and AXI version;
     the crossing is a LiteX `AXIClockDomainCrossing` between the two. Without
     `cpu_clk`, or with `cd_from == cd_to`, nothing is touched.
  2. TRANSPORT. Through the hook's real output, every AXI channel (aw, w, b,
     ar, r) carries 24 random payloads exactly - order, IDs and LAST intact -
     between a 50 MHz-shaped source and a 100 MHz-shaped sink, and the other
     way, under a backpressuring consumer.
  3. NEGATIVE CONTROL. The same channels connected directly across the same
     unequal clocks - the shape the SoC shipped before #359 - lose or
     duplicate beats, so the transport arm is not vacuous; an equal-clock
     direct connection is the stimulus/scoreboard control.

The transport and control arms follow the workstation-local diagnostic
published on #358; the checker here reads the shipping hook rather than a
copy of its logic.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Generator
from pathlib import Path
from random import Random

from migen import Cat, ClockDomain, Module, Signal, run_simulation

from litex.soc.interconnect import axi

sys.path.insert(0, str(Path(__file__).resolve().parent))
import milan_soc  # noqa: E402

CHANNELS = ("aw", "w", "b", "ar", "r")
FORWARD = {"aw", "w", "ar"}


class StandInCpu(Module):
    """What the hook needs from LiteX's VexiiRiscv: a clock attribute, the
    memory-bus list and the method LiteX calls from add_sdram."""

    def __init__(self, with_cpu_clk: bool) -> None:
        """A CPU with or without its own clock; no ports until LiteX asks."""
        self.memory_buses: list = []
        self.native_ports: list = []     # what the generator made, before any hook
        if with_cpu_clk:
            self.cpu_clk = Signal()

    def add_memory_buses(self, address_width: int, data_width: int) -> None:
        """The generator's port exactly as LiteX's VexiiRiscv makes it: clocked
        by cpu_clk in the netlist, yet carrying the DEFAULT clock_domain label
        ("sys"). A hook that believed the label would cross nothing."""
        port = axi.AXIInterface(data_width=data_width, address_width=address_width,
                                id_width=8, version="axi4")
        self.native_ports.append(port)
        self.memory_buses.append(port)


class Harness(Module):
    """A stand-in CPU with the hook installed, or connected directly."""

    def __init__(self, crossing: bool) -> None:
        """Two clock domains, one stand-in CPU, its LiteDRAM-facing port."""
        self.clock_domains.cd_milan = ClockDomain("milan")
        self.clock_domains.cd_sys = ClockDomain("sys")
        self.submodules.cpu = StandInCpu(with_cpu_clk=True)
        if crossing:
            milan_soc.cross_cpu_memory_ports(self.cpu, cd_from="milan", cd_to="sys")
        self.cpu.add_memory_buses(address_width=32, data_width=256)
        self.dram = self.cpu.memory_buses[0]        # what LiteDRAM would connect to
        self.cpu_port = self.cpu.native_ports[0]    # what the CPU netlist drives


def contents(endpoint: object, channel: str) -> Cat:
    """Every AXI wire of one channel endpoint as one vector (w and r carry last)."""
    fields = [endpoint.payload.raw_bits(), endpoint.param.raw_bits()]
    if channel in ("w", "r"):
        fields.append(endpoint.last)
    return Cat(*fields)


def check(problems: list[str], ok: bool, what: str) -> None:
    """Record one graded fact."""
    print(f"  [{'ok  ' if ok else 'FAIL'}] {what}")
    if not ok:
        problems.append(what)


def shape_arms(problems: list[str]) -> None:
    """Arm 1: what the hook does to the port list, and when it does nothing."""
    cpu = StandInCpu(with_cpu_clk=True)
    milan_soc.cross_cpu_memory_ports(cpu, cd_from="milan", cd_to="sys")
    cpu.add_memory_buses(address_width=32, data_width=256)
    port = cpu.memory_buses[0]
    check(problems, len(cpu.memory_buses) == 1, "one memory bus is handed to LiteDRAM")
    check(problems, port.clock_domain == "sys", "the LiteDRAM-facing port is in the sys domain")
    # migen publishes `cpu.submodules.name = obj` as `cpu.name` as well
    cdc = getattr(cpu, "memory_port_cdc0", None)
    check(problems, isinstance(cdc, axi.AXIClockDomainCrossing),
          "an AXIClockDomainCrossing sits behind the port")
    check(problems, (port.data_width, port.address_width, port.id_width, port.version)
          == (256, 32, 8, "axi4"), "the port keeps the CPU port's data, address, id widths and version")
    plain = StandInCpu(with_cpu_clk=False)
    milan_soc.cross_cpu_memory_ports(plain, cd_from="milan", cd_to="sys")
    plain.add_memory_buses(address_width=32, data_width=256)
    check(problems, plain.memory_buses[0] is plain.native_ports[0]
          and not hasattr(plain, "memory_port_cdc0"),
          "a CPU without cpu_clk is left alone")
    check(problems, cpu.native_ports[0].clock_domain == "sys" and port is not cpu.native_ports[0],
          "a CPU port carrying LiteX's default sys label is still crossed (the label is not the fact)")
    same = StandInCpu(with_cpu_clk=True)
    milan_soc.cross_cpu_memory_ports(same, cd_from="sys", cd_to="sys")
    same.add_memory_buses(address_width=32, data_width=256)
    check(problems, not hasattr(same, "memory_port_cdc0"),
          "cd_from == cd_to installs nothing (the simulation SoCs' shape)")


def transport(crossing: bool, periods: tuple[int, int], channel: str) -> bool:
    """Push 24 random beats over one channel; True when the sink saw exactly them."""
    dut = Harness(crossing)
    forward = channel in FORWARD
    # Without the hook the CPU's own port IS the LiteDRAM port (the pre-#359
    # shape): a milan-clocked driver and a sys-clocked consumer on one set of
    # wires. With it the two ends are the two sides of the crossing.
    source_if, sink_if = (dut.cpu_port, dut.dram) if forward else (dut.dram, dut.cpu_port)
    source, sink = getattr(source_if, channel), getattr(sink_if, channel)
    source_domain, sink_domain = ("milan", "sys") if forward else ("sys", "milan")
    source_data, sink_data = contents(source, channel), contents(sink, channel)
    rng = Random(359)
    expected = [rng.getrandbits(len(source_data)) for _ in range(24)]
    observed: list[int] = []
    sent: list[int] = []

    def produce() -> Generator[None, None, None]:
        """Offer every expected beat in order, holding valid until ready."""
        for _ in range(8):
            yield
        for word in expected:
            yield source_data.eq(word)
            yield source.valid.eq(1)
            for _ in range(250):
                yield
                if (yield source.ready):
                    sent.append(word)
                    break
            else:
                raise AssertionError("source stalled")
            yield source.valid.eq(0)
            yield

    def consume() -> Generator[None, None, None]:
        """Take beats under a periodic backpressure pattern and record them."""
        for cycle in range(1000):
            yield sink.ready.eq(cycle % 11 not in (3, 4, 5, 6))
            yield
            if (yield sink.valid) and (yield sink.ready):
                observed.append((yield sink_data))

    generators = defaultdict(list)
    generators[source_domain].append(produce())
    generators[sink_domain].append(consume())
    run_simulation(dut, dict(generators), clocks={"milan": periods[0], "sys": periods[1]})
    if sent != expected:
        raise AssertionError(f"{channel}: the source did not send every beat")
    return observed == expected


def transport_arms(problems: list[str]) -> None:
    """Arms 2 and 3: exact delivery through the hook, loss without it."""
    for name in CHANNELS:
        check(problems, transport(False, (10, 10), name),
              f"equal-clock direct connection carries {name} exactly (stimulus control)")
    lost = 0
    for periods in ((20, 10), (30, 14), (10, 20)):
        for name in CHANNELS:
            check(problems, transport(True, periods, name),
                  f"through the hook, {name} is exact at periods {periods}")
            lost += not transport(False, periods, name)
    check(problems, lost > 0,
          f"the pre-#359 direct connection loses or duplicates beats across unequal clocks ({lost} of 15 arms)")


def main() -> int:
    """Every arm; exit 1 naming each failure."""
    problems: list[str] = []
    print("test_cpu_memory_port_cdc: the CPU memory port crosses into the LiteDRAM clock (#359)")
    shape_arms(problems)
    transport_arms(problems)
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    print(f"test_cpu_memory_port_cdc: {len(problems)} failure(s)")
    # the aggregate reads this line as the verdict, beside the exit status
    print(f"RESULT: {'PASS' if not problems else 'FAIL'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
