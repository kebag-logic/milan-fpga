#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The #814 register boundary on the SoC's bridge-to-SPI-flash timing path.

The path decided the route WNS. It ran from the AXI-Lite-to-Wishbone bridge
state through the bus decoder, the flash origin offset and LiteSPI's burst
compare into the PHY's clock-generator counter.
`milan_soc.add_staged_spi_flash` cuts it. This test builds the path on the
real LiteX and LiteSPI code, with the shipping call, and grades it three ways:

  1. STRUCTURE, read off the elaborated netlist and never off text. The
     netlist's combinational drivers are walked back from each endpoint
     register to the flip-flops that feed it through logic alone. The
     path's start flip-flops must not be among them.
  2. PLANTED UNREGISTERED PATH. The same build with the stage replaced by a
     wire must fail that check, naming the start and end flip-flops, so the
     structural arm can go red.
  3. BEHAVIOUR. Reads through the staged path return the flash image (in a
     burst, across bursts and after a gap) and take exactly the stated added
     cycles. An abandoned access never answers the next request.

Run: cd sw/litex && python3 test_soc_timing_cuts.py
"""
from __future__ import annotations

import sys
from collections.abc import Generator, Iterable
from pathlib import Path

from migen import Module, Signal, run_simulation
from migen.fhdl.structure import Case, If, _Assign
from migen.fhdl.tools import list_signals, list_targets

from litex.build.generic_platform import GenericPlatform
from litex.soc.integration.soc import SoCCore
from litex.soc.interconnect import axi, wishbone
from litespi.modules import N25Q128A13
from litespi.opcodes import SpiNorFlashOpCodes
from litespi.phy.model import LiteSPIPHYModel

sys.path.insert(0, str(Path(__file__).resolve().parent))
import milan_soc  # noqa: E402
from platforms.alinx_ax7101 import _io  # noqa: E402

SYS_HZ = 100e6
#: The export's flash region (litex.log: "spiflash Region allocated at Origin:
#: 0x01000000, Size: 0x01000000"), origin stripped as add_spi_flash does.
FLASH_ORIGIN = 0x0100_0000
#: The stage's stated cost: one cycle to take the request, one to answer.
STAGE_CYCLES = 2


class Netlist:
    """The combinational and registered drivers of one elaborated fragment."""

    def __init__(self, fragment: object) -> None:
        """Index every assignment of `fragment` by the signal it drives."""
        self.signals: dict[int, Signal] = {}
        self.comb: dict[int, set[int]] = {}
        self.sync: dict[int, set[int]] = {}
        self._index(fragment.comb, self.comb, frozenset())
        for statements in fragment.sync.values():
            self._index(statements, self.sync, frozenset())

    def _ids(self, signals: Iterable[Signal]) -> frozenset[int]:
        """Remember each signal by its unique id."""
        for signal in signals:
            self.signals[signal.duid] = signal
        return frozenset(signal.duid for signal in signals)

    def _index(self, statements: object, drivers: dict[int, set[int]], conditions: frozenset[int]) -> None:
        """Every target an assignment drives reads its value, its index and every enclosing condition."""
        if isinstance(statements, (list, tuple)):
            for statement in statements:
                self._index(statement, drivers, conditions)
        elif isinstance(statements, _Assign):
            targets = self._ids(list_targets(statements))
            reads = conditions | self._ids(list_signals(statements.r))
            reads |= self._ids(list_signals(statements.l)) - targets
            for target in targets:
                drivers.setdefault(target, set()).update(reads)
        elif isinstance(statements, If):
            inner = conditions | self._ids(list_signals(statements.cond))
            self._index(statements.t, drivers, inner)
            self._index(statements.f, drivers, inner)
        elif isinstance(statements, Case):
            inner = conditions | self._ids(list_signals(statements.test))
            for body in statements.cases.values():
                self._index(body, drivers, inner)
        else:
            raise TypeError(f"unhandled statement {type(statements).__name__}")

    def cone(self, endpoint: Signal) -> tuple[set[int], set[int]]:
        """The flip-flops whose outputs reach `endpoint`'s input through combinational
        logic alone, and the combinational signals on the way.

        A registered endpoint is entered at its D logic, a combinational one at
        its driver. A signal driven by neither (a port, a special's output) ends
        the walk, as a flip-flop does.
        """
        start = self.sync.get(endpoint.duid, self.comb.get(endpoint.duid, set()))
        stack, seen, flops = list(start), set(), set()
        while stack:
            signal = stack.pop()
            if signal in seen:
                continue
            seen.add(signal)
            if signal in self.comb:
                stack.extend(self.comb[signal])
            elif signal in self.sync:
                flops.add(signal)
        return flops, seen - flops

    def feeding(self, endpoint: Signal) -> set[int]:
        """The flip-flops of `cone`."""
        return self.cone(endpoint)[0]

    def name(self, duid: int) -> str:
        """A signal's migen name, for the report."""
        backtrace = getattr(self.signals[duid], "backtrace", None) or [("?", None)]
        return "_".join(str(part[0]) for part in backtrace[-2:])


def registers(module: Module) -> set[int]:
    """Every flip-flop `module` and its submodules drive, after the top's fragment is built."""
    return {target.duid for statements in module._fragment.sync.values()
            for target in list_targets(statements)}


def find(module: Module, cls: type) -> list[Module]:
    """Every submodule of `module`, at any depth, that is a `cls`."""
    found = [module] if isinstance(module, cls) else []
    for _, child in module._submodules:
        found.extend(find(child, cls))
    return found


def check(problems: list[str], ok: bool, what: str) -> None:
    """Record one graded fact."""
    print(f"  [{'ok  ' if ok else 'FAIL'}] {what}")
    if not ok:
        problems.append(what)


class WirePassThrough(Module):
    """The planted unregistered path: a stage's two faces joined by wires."""

    def __init__(self, master: object, slave: object) -> None:
        """Connect the upstream face straight to the downstream face."""
        self.comb += master.connect(slave)


# Flash -----------------------------------------------------------------------------------------------

class FlashSoC(SoCCore):
    """The SoC's flash path: an AXI-Lite master on the Wishbone bus, the shipping
    `add_staged_spi_flash` call, and either the real PHY on the board's pads
    (structure) or LiteSPI's model PHY (behaviour)."""

    mem_map = {**SoCCore.mem_map, "spiflash": FLASH_ORIGIN}
    STAGE = "WishboneSlaveStage"

    def __init__(self, model_image: list[int] | None) -> None:
        """Build it; `model_image` selects the model PHY holding that image."""
        platform = GenericPlatform("xc7a100tfgg484-2", _io)
        SoCCore.__init__(self, platform, SYS_HZ, cpu_type=None, integrated_rom_size=0,
                         integrated_sram_size=0, with_uart=False, with_timer=False, with_ctrl=False)
        self.axil = axi.AXILiteInterface(data_width=32, address_width=32)
        self.bus.add_master(name="cpu_pbus", master=self.axil)
        module = N25Q128A13(SpiNorFlashOpCodes.READ_1_1_1_FAST)
        kwargs = dict(mode="1x", module=module, clk_freq=int(12.5e6), with_master=True)
        if model_image is not None:
            kwargs["phy"] = LiteSPIPHYModel(module, init=model_image)
        milan_soc.add_staged_spi_flash(self, **kwargs)


def build(cls: type, *args: object, stage: type | None = None) -> Module:
    """`cls(*args)` with `stage` standing in for the shipping stage class `cls.STAGE` names."""
    shipping = getattr(milan_soc, cls.STAGE)
    if stage is not None:
        setattr(milan_soc, cls.STAGE, stage)
    try:
        return cls(*args)
    finally:
        setattr(milan_soc, cls.STAGE, shipping)


#: The Wishbone fields a request carries to the core, and those an answer carries back.
REQUEST = ("cyc", "stb", "adr", "we", "sel", "dat_w", "cti", "bte")
ANSWER = ("ack", "err", "dat_r")


def flash_crossings(soc: FlashSoC) -> tuple[list[str], list[str], bool, int]:
    """The register-to-register paths that cross the flash slave's bus faces.

    Returns the AXI-Lite bridge flip-flops reaching a flash-core flip-flop
    through the core's Wishbone face, and the core flip-flops reaching the
    decoder's face of that slave, each through logic alone and named
    `start -> end`. Then whether only stage flip-flops feed the core face, and
    how many core flip-flops read that face.
    """
    netlist = Netlist(soc.get_fragment())
    bridges = find(soc.bus, axi.AXILite2Wishbone)
    if len(bridges) != 1:
        raise AssertionError(f"expected one AXI-Lite-to-Wishbone bridge, found {len(bridges)}")
    bridge, core = registers(bridges[0]), registers(soc.spiflash)
    stage = registers(soc.spiflash_bus_stage)
    face = {getattr(soc.spiflash.bus, field).duid: getattr(soc.spiflash.bus, field) for field in REQUEST}
    forward, readers = [], 0
    for flop in sorted(core):
        _, wires = netlist.cone(netlist.signals[flop])
        through = [face[duid] for duid in wires & set(face)]
        readers += bool(through)
        starts = set().union(*(netlist.feeding(signal) for signal in through)) & bridge
        forward += [f"{netlist.name(start)} -> {netlist.name(flop)}" for start in sorted(starts)]
    feeders = set().union(*(netlist.feeding(signal) for signal in face.values()))
    decoder = soc.bus.slaves["spiflash"]
    back = set().union(*(netlist.feeding(getattr(decoder, field)) for field in ANSWER)) & core
    backward = [f"{netlist.name(start)} -> decoder face" for start in sorted(back)]
    return forward, backward, bool(feeders) and feeders <= stage, readers


def flash_structure(problems: list[str]) -> None:
    """Arms 1 and 2 for the flash path, on the real PHY."""
    forward, backward, staged, readers = flash_crossings(build(FlashSoC, None))
    check(problems, staged and readers > 0,
          f"F0 only stage flip-flops feed the flash core's Wishbone face, and {readers} core flip-flops read it")
    check(problems, not forward and not backward,
          "F1 no AXI-Lite bridge flip-flop reaches a flash-core flip-flop through the core's bus face, and no "
          "core flip-flop reaches the decoder's face, through logic alone"
          + (f": {(forward + backward)[:4]}" if forward or backward else ""))
    forward, backward, staged, _ = flash_crossings(build(FlashSoC, None, stage=WirePassThrough))
    counter = [path for path in forward if path.endswith("_cnt")]
    check(problems, bool(counter) and bool(backward) and not staged,
          f"F2 the planted wire in place of the stage fails F0 and F1, naming the bridge into the PHY counter "
          f"({len(forward)} forward, {len(backward)} back: {counter[:2]})")


def flash_reads(stage: type | None, addresses: list[int], image: list[int]) -> tuple[list[int], list[int]]:
    """AXI-Lite reads of `addresses` (word indices); returns the words and each read's cycles."""
    soc = build(FlashSoC, image, stage=stage)
    words, cycles = [], []

    def master() -> Generator[None, None, None]:
        """One read at a time: AR, then wait for R, counting cycles from AR valid."""
        axil = soc.axil
        yield axil.r.ready.eq(1)
        for _ in range(4):
            yield
        for index in addresses:
            yield axil.ar.addr.eq(FLASH_ORIGIN + 4 * index)
            yield axil.ar.valid.eq(1)
            count = 0
            while True:
                yield
                count += 1
                if (yield axil.ar.ready):
                    break
            yield axil.ar.valid.eq(0)
            while not (yield axil.r.valid):
                yield
                count += 1
            words.append((yield axil.r.data))
            cycles.append(count)
            yield
            if index == addresses[len(addresses) // 2]:
                for _ in range(400):    # beyond LiteSPI's 256-cycle burst timeout
                    yield

    run_simulation(soc, master())
    return words, cycles


def flash_behaviour(problems: list[str]) -> None:
    """Arm 3 for the flash path, on the model PHY."""
    image = [(0x5A00_0000 ^ (i * 0x9E37_79B1)) & 0xFFFF_FFFF for i in range(64)]
    addresses = [0, 1, 2, 3, 17, 18, 40, 9, 10, 11, 63, 62]
    words, staged = flash_reads(None, addresses, image)
    big_endian = [int.from_bytes(image[i].to_bytes(4, "little"), "big") for i in addresses]
    check(problems, words in ([image[i] for i in addresses], big_endian),
          "F3 reads through the stage return the image: a burst, new bursts and after the burst timeout")
    _, wired = flash_reads(WirePassThrough, addresses, image)
    added = [s - w for s, w in zip(staged, wired)]
    check(problems, added == [STAGE_CYCLES] * len(addresses),
          f"F4 each flash read takes exactly {STAGE_CYCLES} more bus cycles through the stage "
          f"(added {sorted(set(added))}; wired {min(wired)}..{max(wired)} cycles)")


class SlowSlave(Module):
    """A Wishbone slave answering each access `delay` cycles after it starts, with a word
    derived from its address; it counts the accesses it saw begin."""

    def __init__(self, bus: object, delay: int) -> None:
        """The slave on `bus`."""
        self.started = Signal(8)
        count = Signal(8)
        active = Signal()
        self.sync += [
            If(bus.cyc & bus.stb & ~active, active.eq(1), count.eq(0), self.started.eq(self.started + 1)),
            If(active, count.eq(count + 1)),
            If(bus.ack, active.eq(0)),
        ]
        self.comb += [
            bus.ack.eq(active & (count == delay)),
            bus.dat_r.eq(0xC0DE_0000 | bus.adr[:16]),
        ]


class StageBench(Module):
    """The shipping stage alone between a scripted master and `SlowSlave`."""

    def __init__(self) -> None:
        """Both faces, the stage and the slave."""
        self.master = wishbone.Interface(data_width=32, address_width=32, addressing="word")
        core = wishbone.Interface(data_width=32, address_width=32, addressing="word")
        self.submodules.stage = milan_soc.WishboneSlaveStage(self.master, core)
        self.submodules.slave = SlowSlave(core, delay=12)


def stage_abandon(problems: list[str]) -> None:
    """Arm 3: a master that lets go mid-access is never answered, and the next request gets its own word."""
    bench = StageBench()
    seen: dict[str, object] = {"early_ack": False}

    def master() -> Generator[None, None, None]:
        """Start an access to 0x11, let go after 4 cycles, then read 0x22 at once."""
        bus = bench.master
        yield bus.adr.eq(0x11)
        yield bus.cyc.eq(1)
        yield bus.stb.eq(1)
        for _ in range(4):
            yield
            seen["early_ack"] = seen["early_ack"] or (yield bus.ack)
        yield bus.cyc.eq(0)
        yield bus.stb.eq(0)
        yield
        yield bus.adr.eq(0x22)
        yield bus.cyc.eq(1)
        yield bus.stb.eq(1)
        for cycle in range(60):
            yield
            if (yield bus.ack):
                seen["word"] = (yield bus.dat_r)
                seen["cycle"] = cycle
                break
        yield bus.cyc.eq(0)
        yield bus.stb.eq(0)
        for _ in range(4):
            yield
        seen["started"] = (yield bench.slave.started)

    run_simulation(bench, master())
    check(problems, not seen["early_ack"] and seen.get("word") == 0xC0DE_0022 and seen.get("started") == 2,
          "F5 an abandoned access finishes at the slave unanswered; the next request gets its own word "
          f"(word {seen.get('word', 0):#x}, slave accesses {seen.get('started')})")


def main() -> int:
    """Every arm; exit 1 naming each failure."""
    problems: list[str] = []
    print("test_soc_timing_cuts: the #814 register boundaries on the SoC's sys-domain paths")
    flash_structure(problems)
    flash_behaviour(problems)
    stage_abandon(problems)
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    print(f"test_soc_timing_cuts: {len(problems)} failure(s)")
    print(f"RESULT: {'PASS' if not problems else 'FAIL'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
