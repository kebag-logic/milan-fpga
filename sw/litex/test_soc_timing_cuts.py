#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The three #814 register boundaries on the SoC's sys-domain timing paths.

Three families of SoC paths set the route WNS. The flash read path ran from
the AXI-Lite-to-Wishbone bridge state through the bus decoder, the flash
origin offset, LiteSPI's burst compare and mmap FSM, then through the chip
select and command stream into the PHY's clock-generator counter (the #806
route and earlier records). The DRAM path ran from LiteDRAM's flip-flops, the
AXI burst-to-beat counters among them, through its command arbitration, back
into the read address of a crossing FIFO's LUTRAM (two of the recipe's three
placement directives on dev 1e80128f). The refresh path ran from LiteDRAM's
ZQCS timer through the refresh request into each bank machine (the shipping
directive's worst path on that dev). `MilanSoC.add_spi_flash`,
`cross_cpu_memory_ports` and `add_staged_sdram` cut them. This test builds
each path on the real LiteX, LiteSPI and LiteDRAM code, with the shipping
call, and grades it three ways:

  1. STRUCTURE, read off the elaborated netlist and never off text. The
     netlist's combinational drivers are walked back from each endpoint
     register to the flip-flops that feed it through logic alone. The
     path's start flip-flops must not be among them.
  2. PLANTED UNREGISTERED PATH. The same build with the stage replaced by
     wires (or by LiteDRAM's own refresher) must fail that check, naming the
     start and end flip-flops, so the structural arm can go red.
  3. BEHAVIOUR. Reads through the staged flash path return the image (in a
     burst, across bursts and after a gap) at exactly the stated added
     cycles, each transfer inside its chip select. LiteDRAM's native port and
     its DFI see the same traffic, the refresh one cycle later.

Run: cd sw/litex && python3 test_soc_timing_cuts.py
"""
from __future__ import annotations

import sys
from collections.abc import Generator, Iterable
from pathlib import Path

from migen import ClockDomain, Module, Signal, run_simulation
from migen.fhdl.specials import _MemoryPort
from migen.fhdl.structure import Case, If, _Assign
from migen.fhdl.tools import list_signals, list_targets

from litex.build.generic_platform import GenericPlatform
from litex.soc.integration.soc import SoCCore
from litex.soc.interconnect import axi, stream
from litedram.core.bankmachine import BankMachine
from litedram.core.refresher import Refresher
from litedram.frontend.axi import LiteDRAMAXI2Native
from litedram.modules import MT41J256M16
from litedram.phy.model import SDRAMPHYModel, get_sdram_phy_settings
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
#: LiteX's main_ram origin, the base `add_sdram` gives the AXI-to-native converter;
#: a native word is 32 bytes (256-bit port).
MAIN_RAM = 0x4000_0000


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
    """The planted unregistered path: an AXI stage's two faces joined by wires."""

    def __init__(self, master: object, slave: object) -> None:
        """Connect the upstream face straight to the downstream face."""
        for name in ("aw", "w", "ar"):
            self.comb += getattr(master, name).connect(getattr(slave, name))
        for name in ("b", "r"):
            self.comb += getattr(slave, name).connect(getattr(master, name))


class WirePHYStage(Module):
    """The planted unregistered path: `SPIPHYStage`'s faces joined to the PHY by wires."""

    def __init__(self, phy: object) -> None:
        """The stage's faces, wired straight to `phy`'s own."""
        self.phy_sink, self.phy_source, self.phy_cs = phy.sink, phy.source, phy.cs
        self.sink = stream.Endpoint(phy.sink.description)
        self.source = stream.Endpoint(phy.source.description)
        self.cs = Signal.like(phy.cs)
        self.comb += [self.sink.connect(phy.sink), phy.source.connect(self.source), phy.cs.eq(self.cs)]


# Flash -----------------------------------------------------------------------------------------------

class FlashSoC(SoCCore):
    """The SoC's flash path: an AXI-Lite master on the Wishbone bus and the shipping
    `MilanSoC.add_spi_flash`, with either the real PHY on the board's pads
    (structure) or LiteSPI's model PHY (behaviour), staged the same way."""

    mem_map = {**SoCCore.mem_map, "spiflash": FLASH_ORIGIN}
    STAGE = "SPIPHYStage"
    add_spi_flash = milan_soc.MilanSoC.add_spi_flash

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
        self.add_spi_flash(**kwargs)


def build(cls: type, *args: object, stage: type | None = None, name: str | None = None) -> Module:
    """`cls(*args)` with `stage` standing in for the shipping class `name` (default `cls.STAGE`)."""
    name = name or cls.STAGE
    shipping = getattr(milan_soc, name)
    if stage is not None:
        setattr(milan_soc, name, stage)
    try:
        return cls(*args)
    finally:
        setattr(milan_soc, name, shipping)


def faces(endpoint: object, inward: bool) -> list[Signal]:
    """A stream face's signals one way: valid and payload going in, or its ready coming back."""
    if inward:
        return [endpoint.valid, *[getattr(endpoint, field) for field, _ in endpoint.description.payload_layout]]
    return [endpoint.ready]


def flash_crossings(soc: FlashSoC) -> tuple[list[str], list[str], bool, int]:
    """The register-to-register paths that cross the stage between LiteSPI's core and its PHY.

    Returns the AXI-Lite bridge or LiteSPI core flip-flops that reach a PHY
    flip-flop through the PHY's own faces (command stream, data ready, chip
    select), and the PHY flip-flops that reach a core flip-flop through the
    stage's core faces, each through logic alone and named `start -> end`. Then
    whether only stage flip-flops drive both faces, and how many PHY
    flip-flops read the PHY faces.
    """
    netlist = Netlist(soc.get_fragment())
    bridges = find(soc.bus, axi.AXILite2Wishbone)
    if len(bridges) != 1:
        raise AssertionError(f"expected one AXI-Lite-to-Wishbone bridge, found {len(bridges)}")
    stage_module = soc.spiflash.phy.stage
    stage = registers(stage_module)
    phy = registers(soc.spiflash.phy) - stage
    core = registers(soc.spiflash) - registers(soc.spiflash.phy)
    upstream = registers(bridges[0]) | core
    into_phy = faces(stage_module.phy_sink, True) + faces(stage_module.phy_source, False) + [stage_module.phy_cs]
    into_core = faces(stage_module.source, True) + faces(stage_module.sink, False)

    def crossing(ends: set[int], face: list[Signal], starts: set[int]) -> tuple[list[str], int]:
        """Paths from `starts` to `ends` that run through `face`, and how many `ends` read it."""
        index = {signal.duid: signal for signal in face}
        paths, readers = [], 0
        for flop in sorted(ends):
            flops, wires = netlist.cone(netlist.signals[flop])
            readers += bool((flops | wires) & set(index))
            through = [index[duid] for duid in wires & set(index)]
            found = set().union(*(netlist.feeding(signal) for signal in through)) & starts
            paths += [f"{netlist.name(start)} -> {netlist.name(flop)}" for start in sorted(found)]
        return paths, readers

    forward, readers = crossing(phy, into_phy, upstream)
    backward, _ = crossing(core, into_core, phy)
    # a face signal that is a flip-flop drives itself; a combinational one, the flip-flops behind it
    drivers = set().union(*({signal.duid} if signal.duid in netlist.sync else netlist.feeding(signal)
                            for signal in into_phy + into_core))
    return forward, backward, bool(drivers) and drivers <= stage, readers


def flash_structure(problems: list[str]) -> None:
    """Arms 1 and 2 for the flash path, on the real PHY."""
    forward, backward, staged, readers = flash_crossings(build(FlashSoC, None))
    check(problems, staged and readers > 0,
          f"F0 only stage flip-flops drive the PHY's command, ready and chip select and the core's data and "
          f"ready, and {readers} PHY flip-flops read them")
    check(problems, not forward and not backward,
          "F1 no AXI-Lite bridge or LiteSPI core flip-flop reaches a PHY flip-flop, and no PHY flip-flop "
          "reaches a core flip-flop, through the stage's faces and logic alone"
          + (f": {(forward + backward)[:4]}" if forward or backward else ""))
    forward, backward, staged, _ = flash_crossings(build(FlashSoC, None, stage=WirePHYStage))
    counter = [path for path in forward if path.startswith("fsm_state") and path.endswith("_cnt")]
    check(problems, bool(counter) and bool(backward) and not staged,
          f"F2 the planted wires in place of the stage fail F0 and F1, naming the bridge into the PHY counter "
          f"({len(forward)} forward, {len(backward)} back: {counter[:2]})")


def flash_reads(stage: type | None, addresses: list[int], image: list[int]) -> tuple[list[int], list[int], list]:
    """AXI-Lite reads of `addresses` (word indices). Returns the words, each read's cycles, and
    the PHY side's chip-select edges and transfers in order."""
    soc = build(FlashSoC, image, stage=stage)
    words, cycles, events = [], [], []
    face = soc.spiflash.phy.stage

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
        events.append("end")

    def watch() -> Generator[None, None, None]:
        """The PHY side: each chip-select edge and each command it takes, and whether cs was up."""
        last = 0
        while not events or events[-1] != "end":
            cs = (yield face.phy_cs)
            if cs != last:
                events.append(("cs", cs))
                last = cs
            if (yield face.phy_sink.valid) and (yield face.phy_sink.ready):
                events.append(("tx", (yield face.phy_sink.len), (yield face.phy_sink.width), cs))
            yield

    run_simulation(soc, [master(), watch()])
    return words, cycles, [event for event in events if event != "end"]


def flash_behaviour(problems: list[str]) -> None:
    """Arm 3 for the flash path, on the model PHY."""
    image = [(0x5A00_0000 ^ (i * 0x9E37_79B1)) & 0xFFFF_FFFF for i in range(64)]
    addresses = [0, 1, 2, 3, 17, 18, 40, 9, 10, 11, 63, 62]
    words, staged, seen = flash_reads(None, addresses, image)
    big_endian = [int.from_bytes(image[i].to_bytes(4, "little"), "big") for i in addresses]
    check(problems, words in ([image[i] for i in addresses], big_endian),
          "F3 reads through the stage return the image: a burst, new bursts and after the burst timeout")
    _, wired, wired_seen = flash_reads(WirePHYStage, addresses, image)
    added = [s - w for s, w in zip(staged, wired)]
    continues = [i > 0 and a == addresses[i - 1] + 1 and addresses[i - 1] != addresses[len(addresses) // 2]
                 for i, a in enumerate(addresses)]
    expected = [2 if cont else 8 for cont in continues]
    check(problems, added == expected,
          f"F4 each flash read takes two more bus cycles in a burst and eight on a new burst (command, address, "
          f"dummy, data) through the stage (added {added}; wired {min(wired)}..{max(wired)} cycles)")
    inside = all(event[3] for event in seen if event[0] == "tx")
    check(problems, inside and seen == wired_seen and sum(event[0] == "tx" for event in seen) > 20,
          "F5 the PHY takes every command inside its chip select, with the same chip-select edges and commands "
          f"in the same order as without the stage ({sum(event[0] == 'tx' for event in seen)} commands)")

# DRAM ------------------------------------------------------------------------------------------------

class DramSoC(SoCCore):
    """The SoC's DRAM path: a stand-in CPU memory port on its own `milan` clock,
    the shipping `cross_cpu_memory_ports` hook, and the shipping `add_staged_sdram`
    call with the LiteDRAM controller on LiteDRAM's model PHY for the board's
    DDR3 part and width."""

    STAGE = "AXIReadyStage"

    def __init__(self) -> None:
        """Build it."""
        platform = GenericPlatform("xc7a100tfgg484-2", _io)
        SoCCore.__init__(self, platform, SYS_HZ, cpu_type=None, integrated_rom_size=0,
                         integrated_sram_size=0, with_uart=False, with_timer=False, with_ctrl=False)
        self.cd_milan = ClockDomain("milan")
        cpu = self.cpu
        cpu.cpu_clk = Signal()
        cpu.memory_buses = []

        def add_memory_buses(address_width: int, data_width: int) -> None:
            """The CPU's own port, as LiteX's VexiiRiscv makes it."""
            self.cpu_port = axi.AXIInterface(data_width=data_width, address_width=address_width,
                                             id_width=8, version="axi4")
            cpu.memory_buses.append(self.cpu_port)

        cpu.add_memory_buses = add_memory_buses
        milan_soc.cross_cpu_memory_ports(cpu, cd_from="milan", cd_to="sys")
        settings = get_sdram_phy_settings(memtype="DDR3", data_width=32, clk_freq=SYS_HZ)
        module = MT41J256M16(SYS_HZ, "1:4")
        milan_soc.add_staged_sdram(self, "sdram", phy=SDRAMPHYModel(module, settings=settings, clk_freq=SYS_HZ),
                                   module=module, l2_cache_size=0)


def dram_crossings(soc: DramSoC) -> tuple[list[str], bool, int]:
    """LiteDRAM-side flip-flops reaching an address crossing FIFO's LUTRAM read address.

    The address channels (aw, ar) cross into sys, so their FIFOs' read ports
    are the crossing's sys-clocked read ports whose data reach the address
    LiteDRAM's side reads. Returns the paths that reach one of those read
    addresses from a flip-flop of LiteDRAM's AXI-to-native converter or its
    core through logic alone, named `start -> end`. Then whether stage
    flip-flops feed every read address, and how many read ports were examined.
    """
    netlist = Netlist(soc.get_fragment())
    converters = find(soc, LiteDRAMAXI2Native)
    if len(converters) != 1:
        raise AssertionError(f"expected one AXI-to-native converter, found {len(converters)}")
    dram = registers(converters[0]) | registers(soc.sdram)
    stage = registers(soc.cpu.memory_port_stage0)
    dram_side = soc.cpu.memory_buses[0]
    wires = netlist.cone(dram_side.aw.addr)[1] | netlist.cone(dram_side.ar.addr)[1]
    ports = [special for special in soc.cpu.memory_port_cdc0._fragment.specials
             if isinstance(special, _MemoryPort) and special.we is None and special.clock.cd == "sys"
             and special.dat_r.duid in wires]
    paths, staged = [], True
    for port in ports:
        feeders = netlist.feeding(port.adr)
        staged &= bool(feeders & stage)
        paths += [f"{netlist.name(start)} -> {netlist.name(port.adr.duid)}" for start in sorted(feeders & dram)]
    return paths, staged, len(ports)


def dram_structure(problems: list[str]) -> None:
    """Arms 1 and 2 for the DRAM path."""
    paths, staged, examined = dram_crossings(build(DramSoC))
    check(problems, examined == 2 and staged,
          f"D0 the stage feeds the read address of each address crossing FIFO ({examined} of aw and ar)")
    check(problems, not paths,
          "D1 no flip-flop of LiteDRAM's AXI-to-native converter or core reaches an address crossing FIFO's "
          "LUTRAM read address through logic alone" + (f": {paths[:4]}" if paths else ""))
    paths, staged, _ = dram_crossings(build(DramSoC, stage=WirePassThrough))
    counter = [path for path in paths if "beat_count" in path.split(" -> ")[0]]
    check(problems, bool(counter) and not staged,
          f"D2 the planted wire in place of the stage fails D0 and D1, naming the burst-to-beat counter "
          f"({len(paths)} paths: {counter[:2]})")


def dram_traffic(stage: type | None, beats: list[tuple[int, int]]) -> tuple[list[tuple], list[int]]:
    """Write each `(address, word)` on the CPU port, then read each back. Returns every
    handshake LiteDRAM's native ports saw, with its sys cycle, and each read's milan
    cycles from the AR handshake to its R beat."""
    soc = build(DramSoC, stage=stage)
    port = soc.cpu_port
    native, cycles = [], []
    done = []

    def master() -> Generator[None, None, None]:
        """One single-beat burst at a time, every write before every read."""
        for _ in range(200):
            yield
        yield port.b.ready.eq(1)
        yield port.r.ready.eq(1)
        for address, word in beats:
            for name, value in (("addr", address), ("len", 0), ("size", 5), ("burst", 1), ("valid", 1)):
                yield getattr(port.aw, name).eq(value)
            for name, value in (("data", word), ("strb", 2**32 - 1), ("last", 1), ("valid", 1)):
                yield getattr(port.w, name).eq(value)
            aw_done = w_done = False
            while not (aw_done and w_done):
                yield
                aw_done = aw_done or bool((yield port.aw.ready))
                w_done = w_done or bool((yield port.w.ready))
                if aw_done:
                    yield port.aw.valid.eq(0)
                if w_done:
                    yield port.w.valid.eq(0)
            while not (yield port.b.valid):
                yield
            yield
        for address, _ in beats:
            for name, value in (("addr", address), ("len", 0), ("size", 5), ("burst", 1), ("valid", 1)):
                yield getattr(port.ar, name).eq(value)
            yield
            while not (yield port.ar.ready):
                yield
            yield port.ar.valid.eq(0)
            count = 0
            while not (yield port.r.valid):
                yield
                count += 1
            cycles.append(count)
            yield
        done.append(True)

    def monitor() -> Generator[None, None, None]:
        """Every native-port command and write-data handshake, in order, with its cycle."""
        cycle = 0
        while not done:
            for index, native_port in enumerate(soc.sdram.crossbar.masters):
                if (yield native_port.cmd.valid) and (yield native_port.cmd.ready):
                    native.append((cycle, index, "cmd", (yield native_port.cmd.we), (yield native_port.cmd.addr)))
                if (yield native_port.wdata.valid) and (yield native_port.wdata.ready):
                    native.append((cycle, index, "wdata", (yield native_port.wdata.data),
                                   (yield native_port.wdata.we)))
            yield
            cycle += 1

    run_simulation(soc, {"milan": [master()], "sys": [monitor()]}, clocks={"milan": 20, "sys": 10})
    return native, cycles


def dram_behaviour(problems: list[str]) -> None:
    """Arm 3 for the DRAM path: the native port's contract, and no added cycle."""
    beats = [(MAIN_RAM + 0x40, 0x1234_5678_9ABC_DEF0 << 96 | 0x55), (MAIN_RAM + 0x1000, 0xFEED_FACE << 200 | 0xAA),
             (MAIN_RAM + 0x8040, 2**255 + 7), (MAIN_RAM + 0x20, 0x0F0F_0F0F)]
    native, staged = dram_traffic(None, beats)
    words = [(address - MAIN_RAM) >> 5 for address, _ in beats]
    seen = [event[2:] for event in native]
    writes = [event for event in seen if event[0] == "wdata"]
    commands = [event for event in seen if event[0] == "cmd"]
    check(problems, commands == [("cmd", 1, word) for word in words] + [("cmd", 0, word) for word in words]
          and writes == [("wdata", data, 2**32 - 1) for _, data in beats]
          and seen[:2] == [("cmd", 1, words[0]), ("wdata", beats[0][1], 2**32 - 1)],
          "D3 LiteDRAM's native port sees each write's command, word and full mask, then each read's command, "
          "in order, at the addresses written")
    wired_native, wired = dram_traffic(WirePassThrough, beats)
    check(problems, native == wired_native and staged == wired,
          f"D4 the stage changes nothing the native port sees, cycle for cycle, and adds no cycle to a read "
          f"(staged {staged}, wired {wired} milan cycles)")

# Refresh ---------------------------------------------------------------------------------------------

def refresh_crossings(soc: DramSoC) -> tuple[list[str], bool, int]:
    """LiteDRAM refresher flip-flops reaching a bank-machine or multiplexer flip-flop
    through the refresher's `valid` or `last`.

    Returns those paths named `start -> end`, whether `valid` and `last` are
    the stage's own flip-flops, and how many controller flip-flops read them.
    The command fields leave LiteDRAM's executers from flip-flops and are not
    this path, so they are not graded here.
    """
    netlist = Netlist(soc.get_fragment())
    controller = soc.sdram.controller
    outer = controller.refresher
    inner = getattr(outer, "refresher", outer)
    refresher, stage = registers(inner), registers(outer) - registers(inner)
    machines = registers(controller.multiplexer).union(*(registers(bm) for bm in find(controller, BankMachine)))
    request = {outer.cmd.valid.duid: outer.cmd.valid, outer.cmd.last.duid: outer.cmd.last}
    paths, readers = [], 0
    for flop in sorted(machines):
        flops, wires = netlist.cone(netlist.signals[flop])
        readers += bool((flops | wires) & set(request))
        through = [request[duid] for duid in wires & set(request)]
        starts = set().union(*(netlist.feeding(signal) for signal in through)) & refresher
        paths += [f"{netlist.name(start)} -> {netlist.name(flop)}" for start in sorted(starts)]
    return paths, set(request) <= stage, readers


def refresh_structure(problems: list[str]) -> None:
    """Arms 1 and 2 for the refresh path."""
    paths, staged, readers = refresh_crossings(build(DramSoC))
    check(problems, staged and readers > 0,
          f"Z0 the refresh request is the stage's own flip-flops, and {readers} controller flip-flops read it")
    check(problems, not paths,
          "Z1 no LiteDRAM refresher flip-flop reaches a bank-machine or multiplexer flip-flop through the "
          "refresh request through logic alone" + (f": {paths[:4]}" if paths else ""))
    paths, staged, _ = refresh_crossings(build(DramSoC, stage=Refresher, name="RegisteredRefresher"))
    timer = [path for path in paths if "refreshtimer" in path.split(" -> ")[0] and "level" in path]
    check(problems, bool(timer) and not staged,
          f"Z2 LiteDRAM's own Refresher in place of the stage fails Z0 and Z1, naming a refresh timer into a "
          f"bank machine's FIFO level ({len(paths)} paths: {timer[:2]})")


def dfi_commands(stage: type | None, cycles: int) -> list[tuple[int, int, str, int]]:
    """Every command on the controller's DFI over `cycles` idle sys cycles: `(cycle, phase, name, address)`."""
    soc = build(DramSoC, stage=stage, name="RegisteredRefresher")
    names = {(0, 1, 0): "PRECHARGE", (0, 0, 1): "REFRESH", (1, 1, 0): "ZQCS"}
    seen = []

    def monitor() -> Generator[None, None, None]:
        """Decode each phase's cs/ras/cas/we every cycle."""
        for cycle in range(cycles):
            for index, phase in enumerate(soc.sdram.controller.dfi.phases):
                if not (yield phase.cs_n):
                    code = ((yield phase.ras_n), (yield phase.cas_n), (yield phase.we_n))
                    if code != (1, 1, 1):
                        seen.append((cycle, index, names.get(code, str(code)), (yield phase.address)))
            yield

    run_simulation(soc, {"sys": [monitor()]}, clocks={"milan": 20, "sys": 10})
    return seen


def refresh_behaviour(problems: list[str]) -> None:
    """Arm 3 for the refresh path: LiteDRAM's own refresh commands, each one cycle later.

    LiteDRAM issues a ZQCS only when its one-cycle ZQCS timer pulse meets the
    refresh sequencer's end, which no simulation of this length reaches; the
    ZQCS executer's commands leave the same registered fields, behind the same
    two registers.
    """
    staged = dfi_commands(None, 3200)
    plain = dfi_commands(Refresher, 3200)
    kinds = sorted({name for _, _, name, _ in staged})
    shifted = [(cycle + 1, index, name, address) for cycle, index, name, address in plain]
    check(problems, kinds == ["PRECHARGE", "REFRESH"] and len(staged) >= 6 and staged == shifted,
          f"Z3 the staged refresher issues LiteDRAM's own precharge-all and refresh commands, each exactly one "
          f"cycle later at the same spacing ({len(staged)} commands, first at {staged[0][0] if staged else None})")


def main() -> int:
    """Every arm; exit 1 naming each failure."""
    problems: list[str] = []
    print("test_soc_timing_cuts: the #814 register boundaries on the SoC's sys-domain paths")
    flash_structure(problems)
    flash_behaviour(problems)
    dram_structure(problems)
    dram_behaviour(problems)
    refresh_structure(problems)
    refresh_behaviour(problems)
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    print(f"test_soc_timing_cuts: {len(problems)} failure(s)")
    print(f"RESULT: {'PASS' if not problems else 'FAIL'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
