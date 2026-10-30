#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The two #814 register boundaries on the SoC's sys-domain timing paths.

Two SoC paths set the route WNS. One ran from the AXI-Lite-to-Wishbone
bridge state through the bus decoder, the flash origin offset and LiteSPI's
burst compare into the PHY's clock-generator counter (the #806 route and
earlier records). The other ran from LiteDRAM's flip-flops, the AXI
burst-to-beat counters among them, through its command arbitration, back into
the read address of a crossing FIFO's LUTRAM (two of the recipe's three
placement directives on dev 1e80128f).
`milan_soc.add_staged_spi_flash` and `milan_soc.cross_cpu_memory_ports` cut
them. This test builds each path on the real LiteX and LiteDRAM code, with the
shipping hook, and grades it three ways:

  1. STRUCTURE, read off the elaborated netlist and never off text. The
     netlist's combinational drivers are walked back from each endpoint
     register to the flip-flops that feed it through logic alone. The
     path's start flip-flops must not be among them.
  2. PLANTED UNREGISTERED PATH. The same build with the stage replaced by a
     wire must fail that check, naming the start and end flip-flops, so the
     structural arm can go red.
  3. BEHAVIOUR. Reads through the staged path return the flash image (in a
     burst, across bursts and after a gap) and take exactly the stated added
     cycles. An abandoned access never answers the next request. The DRAM
     port carries every AXI channel exactly under backpressure.

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
from litex.soc.interconnect import axi, wishbone
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
#: The stage's stated cost: one cycle to take the request, one to answer.
STAGE_CYCLES = 2
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
    """The planted unregistered path: a stage's two faces joined by wires."""

    def __init__(self, master: object, slave: object) -> None:
        """Connect the upstream face straight to the downstream face."""
        if isinstance(master, axi.AXIInterface):
            for name in ("aw", "w", "ar"):
                self.comb += getattr(master, name).connect(getattr(slave, name))
            for name in ("b", "r"):
                self.comb += getattr(slave, name).connect(getattr(master, name))
        else:
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
    """LiteDRAM-side flip-flops reaching a request crossing FIFO's LUTRAM read address.

    The request channels (aw, w, ar) cross into sys, so their FIFOs' read
    ports are the crossing's sys-clocked read ports. Returns the paths that
    reach one of those read addresses from a flip-flop of LiteDRAM's
    AXI-to-native converter or its core through logic alone, named
    `start -> end`. Then whether stage flip-flops feed every read address, and
    how many read ports were examined.
    """
    netlist = Netlist(soc.get_fragment())
    converters = find(soc, LiteDRAMAXI2Native)
    if len(converters) != 1:
        raise AssertionError(f"expected one AXI-to-native converter, found {len(converters)}")
    dram = registers(converters[0]) | registers(soc.sdram)
    stage = registers(soc.cpu.memory_port_stage0)
    ports = [special for special in soc.cpu.memory_port_cdc0._fragment.specials
             if isinstance(special, _MemoryPort) and special.we is None and special.clock.cd == "sys"]
    paths, staged = [], True
    for port in ports:
        feeders = netlist.feeding(port.adr)
        staged &= bool(feeders & stage)
        paths += [f"{netlist.name(start)} -> {netlist.name(port.adr.duid)}" for start in sorted(feeders & dram)]
    return paths, staged, len(ports)


def dram_structure(problems: list[str]) -> None:
    """Arms 1 and 2 for the DRAM path."""
    paths, staged, examined = dram_crossings(build(DramSoC))
    check(problems, examined == 3 and staged,
          f"D0 the stage feeds the read address of each request crossing FIFO ({examined} of aw, w and ar)")
    check(problems, not paths,
          "D1 no flip-flop of LiteDRAM's AXI-to-native converter or core reaches a request crossing FIFO's "
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
    stage_abandon(problems)
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
