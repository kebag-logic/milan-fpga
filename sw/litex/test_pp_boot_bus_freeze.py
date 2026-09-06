#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""The protocol-processor memory gate must contain an unanswered boot read.

The bare-metal endpoint has two memory clients: the descriptor-image reader
and the AECP response-buffer bridge.  Both share the CPU core memory attachment.
This test instantiates the real LiteX interconnect plus milan_soc.py's bridge,
gate, watchdog, and diagnostic counters.  It proves that no request reaches an
unavailable memory window, that both clients recover after handover, and that
the always-open and never-open gate mutants are rejected.

The memory model deliberately accepts and drops reads during its dead window.
That is the failure mode which permanently locks LiteX's read arbiter if the
gate is bypassed.  Timing is scaled uniformly to keep the simulation short.

Run: cd sw/litex && python3 test_pp_boot_bus_freeze.py
"""

import ast
import sys
from collections.abc import Callable, Generator
from pathlib import Path

from migen import *

from litex.soc.integration.soc import SoCBusHandler, SoCRegion
from litex.soc.interconnect import wishbone, axi

HERE = Path(__file__).resolve().parent
MILAN_SOC = HERE / "milan_soc.py"

#: Protocol-memory masters in the same insertion order used by milan_soc.py.
#: The grant index is the insertion index.
MASTERS = [
    ("milan_desc_mem", "wb"),    # 0  descriptor-image read bridge
    ("milan_resp_mem", "wb"),    # 1  AECP response-buffer bridge
    ("milan_nvm_mem", "wb"),     # 2  saved-state record-image bridge (#70)
]
DESC_MEM = 0

#: The reference SoC's measured miss latency to main memory, 1,424 ns, in sys
#: cycles at 100 MHz. The same measurement `pp_mem_bus_worst_cycles` is built
#: on, so the bus this simulation presents is not a faster one than the
#: watchdog was sized against.
MEM_LATENCY_REAL = 142
SYS_HZ           = 100e6

#: EVERYTHING IN TIME IS SCALED BY THIS, watchdog and memory latency together,
#: and the ratio between them is what the claims actually rest on. migen's
#: the unscaled watchdog would put every session in the minutes and
#: the suite would stop being run. `test_control_loaded_bus` is what proves the
#: scale is not cheating: a loaded, healthy bus must show timed_out = 0, which
#: a watchdog scaled tighter than the bus it watches could not deliver.
SIM_SCALE   = 8
MEM_LATENCY = max(1, MEM_LATENCY_REAL // SIM_SCALE)

WORD = 0x01000100494D4541          # what a healthy memory returns
#: The same word as the PROCESSOR must see it. A beat carries its lowest byte
#: address in bits [63:56] - 1722.1 wire order, big-endian - and the bus words
#: are little-endian, so the bridge byte-reverses. Checking the payload and not
#: just `err` is what makes "the access completed" a measurement.
WORD_BE = int.from_bytes(WORD.to_bytes(8, "little"), "big")

#: The tally `check()` accumulates into: ONE module-level container it MUTATES,
#: rather than two names it had to declare `global` to rebind. The summary at
#: the bottom of the file reads the same object, so the count printed and the
#: count exited on cannot come apart.
TALLY = {"checks": 0, "fails": 0}

#: What migen's simulator drives: a generator that yields signals and
#: statements and is sent back the values it reads. Spelled once so the
#: stimulus factories below can say what they hand `run_simulation`.
SimGen = Generator[object, object, None]


def check(name: str, cond: object, detail: str = "") -> None:
    """Score one claim into TALLY, and say which one on the spot.

    `cond` is judged for truth, not for being a bool: several claims read a
    list that is empty exactly when the bus froze, and a `bool()` here would
    hide which of the two it was from the printed detail.
    """
    TALLY["checks"] += 1
    if cond:
        print(f"  [ok]   {name}")
    else:
        TALLY["fails"] += 1
        print(f"  [FAIL] {name} {detail}")


def _milan_soc():
    """The real SoC module: the bridge, the gate and the counters are ITS code."""
    # sys.path entries are strings; a Path here would never compare equal to
    # one already present and would be re-inserted on every call.
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import milan_soc
    return milan_soc


#: The bridge watchdog the SoC derives for the shipping AX shape (sys and milan
#: both 100 MHz), read from milan_soc.py rather than restated - a magic number
#: here would let this file grade a budget the build does not use - then scaled
#: with the memory latency so the pair keeps its ratio.
TMO_REAL = _milan_soc().pp_mem_timeout_cycles(SYS_HZ, SYS_HZ)
TMO      = max(8, TMO_REAL // SIM_SCALE)

#: THE TIMELINE EVERY SESSION SHARES, so the five runs differ in the gate and
#: in the memory alone. `sel` drops when the BIOS enters `sdram_init`'s
#: software-control window and rises when it hands the DFI back; the handover
#: is put a whole watchdog past the boot probe so the pre-fix shape has time to
#: time out INSIDE the dead window, which is the board's reading.
SW_AT   = 200
HAND_AT = TMO + 200
CYCLES  = TMO + 2000
#: The locate is scheduled on the ABSOLUTE clock, not relative to the boot
#: answer: the shapes answer that probe whole watchdogs apart, and a relative
#: schedule would put the locate before the handover in one shape and after it
#: in the other, which would compare two different experiments.
LOCATE_AT = HAND_AT + 400


# ---------------------------------------------------------------------------
#  the bus: LiteX's own, not a model of it
# ---------------------------------------------------------------------------

class PPMemBus(Module):
    """The protocol-memory attachment: two Wishbone masters, one AXI slave.

    Widths are the flashed build's - 64-bit data, 32-bit byte-addressed AXI,
    word-addressed 64-bit Wishbone masters and one
    slave covering the whole space. Nothing here models the interconnect:
    `SoCBusHandler.finalize()` builds it, so this cannot agree with a bug the
    real one does not have.

    The slave stands for the CPU core's dedicated memory attachment. Main
    memory is behind it; the core-side cache/interconnect is not modelled here.
    """

    def __init__(self):
        self.submodules.h = h = SoCBusHandler(
            name          = "SoCPPMemBusHandler",
            standard      = "axi",
            data_width    = 64,
            address_width = 32,
            bursting      = True,
        )
        self.port = {}
        for name, std in MASTERS:
            if std == "axi":
                m = axi.AXIInterface(data_width=64, address_width=32,
                                     id_width=4)
            else:
                m = wishbone.Interface(data_width=64, adr_width=29,
                                       addressing="word")
            h.add_master(name, master=m)
            self.port[name] = m
        self.slave = axi.AXIInterface(data_width=64, address_width=32,
                                      id_width=h.get_axi_id_width())
        h.add_slave(name="dma", slave=self.slave,
                    region=SoCRegion(origin=0x00000000, size=2**32))

    def arbiter(self) -> Module:
        """The read arbiter LiteX built, so a freeze can be read off it.

        Reached through the handler's own submodules rather than kept as a
        name here: the interconnect is `SoCBusHandler.finalize()`'s, and a
        second reference to it would be a second thing to keep current.
        """
        return dict(self.h._submodules)["_interconnect"].arbiter


# ---------------------------------------------------------------------------
#  the device under test: milan_soc.py's own bridge, on that bus
# ---------------------------------------------------------------------------

#: The three gate shapes this file drives. "real" is the shipping wiring;
#: "open" is the flashed pre-fix shape AND the mutant the fix must not be
#: mistaken for; "shut" is a gate that is present and never opens.
GATE_REAL = "real"
GATE_OPEN = "open"
GATE_SHUT = "shut"


class Session(Module):
    """The bus, milan_soc.py's bridge on grant index 0, and the real counters.

    THE BRIDGE IS NOT A REPLICA. `pp_desc_bridge` and `pp_mem_gate` are
    imported out of milan_soc.py and built here, so a change to either is
    graded by what it DOES. The only thing this class supplies is what the SoC
    supplies: the request and response faces (records the datapath's CDC drives
    on silicon), the wishbone master, the watchdog budget, and - in the two
    mutant shapes - a different gate.

    `mem_rdy` is a Signal in all three shapes, wrapping the gate rather than
    replacing it, only so one monitor can read it whatever the shape is.
    """

    def __init__(self, gate, tmo=TMO):
        soc = _milan_soc()
        self.submodules.bus = self.bus = PPMemBus()
        wb = self.bus.port["milan_desc_mem"]

        self.req = Record([("valid", 1), ("ready", 1),
                           ("addr", 32), ("beats", 9)])
        self.rsp = Record([("valid", 1), ("ready", 1), ("data", 64),
                           ("blast", 1), ("err", 1)])
        # the processor's `rsp_ready` is tied 1: it always sinks its own beats
        self.comb += self.rsp.ready.eq(1)

        # `sel` RESETS TO 1 because LiteDRAM's does (litedram/dfii.py
        # DFIInjector: `reset=0b1  # Defaults to HW control.`). A gate that
        # took hardware control alone as proof would be open at cycle 0.
        self.sel     = Signal(reset=1)
        self.mem_rdy = Signal()
        if gate == GATE_REAL:
            self.comb += self.mem_rdy.eq(soc.pp_mem_gate(self, self.sel))
        elif gate == GATE_OPEN:
            self.comb += self.mem_rdy.eq(1)
        else:
            self.comb += self.mem_rdy.eq(0)

        fsm, self.psn, self.psn_set = soc.pp_desc_bridge(
            self, self.req, self.rsp, wb, self.mem_rdy, tmo,
            0xFF,    # sel mask: the whole 64-bit lane, `_pp_selm`
            3)       # address shift: byte address -> 64-bit word, `_pp_sh`
        self.submodules.fsm = fsm
        self.submodules.diag = self.diag = soc._PPMemDiag(
            [("desc", wb, self.psn, self.psn_set)], mem_rdy=self.mem_rdy)


def counters(dut: Session) -> Generator[object, object, dict[str, int]]:
    """The two CSR words, decoded the way the register map documents them."""
    req = yield dut.diag.desc_req.status
    flt = yield dut.diag.desc_fault.status
    return {"issued": (req >> 16) & 0xFFFF, "acked": req & 0xFFFF,
            "errored": (flt >> 16) & 0xFFFF, "timed_out": flt & 0xFFFF}


# ---------------------------------------------------------------------------
#  the memory, and the neighbours that load the bus
# ---------------------------------------------------------------------------

def memory(dut: PPMemBus, cycles: int, alive_at: int = 0,
           latency: int = MEM_LATENCY) -> Callable[[], SimGen]:
    """Main memory: `latency` cycles, ARLEN+1 beats, writes answered on B.

    Before `alive_at` a read COMMAND IS ACCEPTED AND SWALLOWED - see the banner
    for why that, and not a refused AR, is the shape the board proves.
    """
    s = dut.slave

    def gen() -> SimGen:
        """Accept AR/AW every cycle; answer only what arrived after `alive_at`."""
        rq = []          # [ready_cycle, beats_left]
        wq = []          # ready_cycle
        yield s.ar.ready.eq(1)
        yield s.aw.ready.eq(1)
        yield s.w.ready.eq(1)
        for cyc in range(cycles):
            if (yield s.ar.valid) and (yield s.ar.ready):
                if cyc >= alive_at:
                    rq.append([cyc + latency, (yield s.ar.len) + 1])
            if (yield s.aw.valid) and (yield s.aw.ready):
                wq.append(cyc + latency)

            fire_b = (yield s.b.valid) and (yield s.b.ready)
            if fire_b or not (yield s.b.valid):
                if wq and wq[0] <= cyc:
                    wq.pop(0)
                    yield s.b.valid.eq(1)
                    yield s.b.resp.eq(0)
                else:
                    yield s.b.valid.eq(0)

            fire_r = (yield s.r.valid) and (yield s.r.ready)
            if fire_r:
                rq[0][1] -= 1
                if rq[0][1] == 0:
                    rq.pop(0)
            if fire_r or not (yield s.r.valid):
                if rq and rq[0][0] <= cyc:
                    yield s.r.valid.eq(1)
                    yield s.r.data.eq(WORD)
                    yield s.r.resp.eq(0)
                    yield s.r.last.eq(1 if rq[0][1] == 1 else 0)
                else:
                    yield s.r.valid.eq(0)
            yield
    return gen


# EVERY GENERATOR BELOW IS A BOUNDED PER-CYCLE STATE MACHINE, and that is a
# requirement of the thing being tested rather than a style choice: the failure
# under study is a bus that STOPS ANSWERING, so any stimulus written as
# "wait until the beat arrives" hangs the simulator instead of failing the
# check. `run_simulation` ends when every generator has, so one unbounded wait
# turns a red test into a test that never finishes.

def wb_repeat_reads(wb: wishbone.Interface, addr: int, cycles: int,
                    start: int = 0) -> Callable[[], SimGen]:
    """Repeated response-buffer reads that load the retained read arbiter."""
    def gen() -> SimGen:
        """One read after another for `cycles`, each released on ack or err."""
        for _ in range(start):
            yield
        yield wb.adr.eq(addr >> 3)
        yield wb.sel.eq(0xFF)
        yield wb.we.eq(0)
        active = False
        for _ in range(cycles):
            if not active:
                yield wb.cyc.eq(1)
                yield wb.stb.eq(1)
                active = True
            yield
            if active and ((yield wb.ack) or (yield wb.err)):
                yield wb.cyc.eq(0)
                yield wb.stb.eq(0)
                active = False
                # Make the transaction boundary visible to Wishbone2AXI and
                # give the shared read arbiter a cycle in which to rotate.
                yield
        yield wb.cyc.eq(0)
        yield wb.stb.eq(0)
    return gen


def wb_one_read(wb: wishbone.Interface, addr: int, budget: int, start: int = 0
                ) -> tuple[Callable[[], SimGen], list[tuple[str, int | None]]]:
    """One wishbone read, abandoned after `budget` cycles.

    The list comes back with the generator and is filled while it runs: one
    ("ack", word) if the bus answered, one ("tmo", None) if it never did.
    """
    out = []

    def gen() -> SimGen:
        """Hold cyc & stb until the read is answered or the budget is spent."""
        for _ in range(start):
            yield
        yield wb.adr.eq(addr >> 3)
        yield wb.sel.eq(0xFF)
        yield wb.we.eq(0)
        yield wb.cyc.eq(1)
        yield wb.stb.eq(1)
        done = False
        for _ in range(budget):
            yield
            if not done and (yield wb.ack):
                out.append(("ack", (yield wb.dat_r)))
                yield wb.cyc.eq(0)
                yield wb.stb.eq(0)
                done = True
        if not done:
            yield wb.cyc.eq(0)
            yield wb.stb.eq(0)
            yield
            out.append(("tmo", None))
    return gen, out


def idle(n: int) -> Callable[[], SimGen]:
    """`n` cycles of nothing - a bounded wait, never a wait-until.

    Every generator in this file is bounded on purpose: the defect under
    study is a bus that stops answering, and a wait-until would hang the
    simulator instead of failing a check.
    """
    def gen() -> SimGen:
        """Advance `n` cycles and stop."""
        for _ in range(n):
            yield
    return gen


# ---------------------------------------------------------------------------
#  the session
# ---------------------------------------------------------------------------

def _dfi_handover(dut, cycles):
    """The one DFI bit the gate reads: 1 at configuration, 0 for the BIOS's
    software-control window, 1 again when `sdram_init` is done."""
    for _ in range(SW_AT):
        yield
    yield dut.sel.eq(0)
    for _ in range(HAND_AT - SW_AT):
        yield
    yield dut.sel.eq(1)
    for _ in range(cycles - HAND_AT):
        yield


def _processor(dut, cycles, boot_probe):
    """The store's two requests, each offered until the bridge takes it."""
    t = 0
    if boot_probe:
        # the boot walk: KL_aecp_desc_store resets INTO S_HDR_REQ
        yield dut.req.addr.eq(0x7F700000)
        yield dut.req.beats.eq(4)
        yield dut.req.valid.eq(1)
        yield
        t += 1
        while t < LOCATE_AT and not (yield dut.req.ready):
            yield
            t += 1
        yield dut.req.valid.eq(0)
    while t < LOCATE_AT:
        yield
        t += 1
    # a locate re-arms the header probe long after the BIOS is done
    yield dut.req.addr.eq(0x7F700000)
    yield dut.req.beats.eq(4)
    yield dut.req.valid.eq(1)
    yield
    t += 1
    while t < cycles - 20 and not (yield dut.req.ready):
        yield
        t += 1
    yield dut.req.valid.eq(0)
    while t < cycles - 20:
        yield
        t += 1


def _collector(dut, cycles, beats):
    """Every response beat the processor would see, with its cycle, into `beats`."""
    for t in range(cycles):
        if (yield dut.rsp.valid):
            beats.append({"t": t, "err": (yield dut.rsp.err),
                          "data": (yield dut.rsp.data),
                          "blast": (yield dut.rsp.blast)})
        yield


def _monitor(dut, cycles, alive_at, watch):
    """WAS THE BUS TOUCHED WHILE THE MEMORY COULD NOT ANSWER, recorded in `watch`.

    MEASURED AGAINST THE EXPERIMENT'S CLOCK, never against `mem_rdy`: a
    gate tied to 1 asserts it is ready throughout, so a window defined by
    the gate's own opinion is empty exactly when the gate is broken, and
    the check passes for the mutant it exists to catch. `alive_at` is the
    objective fact - the cycle the memory model starts answering.
    """
    for t in range(cycles):
        on  = (yield dut.bus.port["milan_desc_mem"].cyc) \
            and (yield dut.bus.port["milan_desc_mem"].stb)
        if (yield dut.mem_rdy) and watch["first_rdy"] is None:
            watch["first_rdy"] = t
        if on:
            if watch["first_cyc"] is None:
                watch["first_cyc"] = t
            if t < alive_at:
                watch["cyc_dead"] += 1
        yield


def _arbiter_probe(dut, cycles, snap):
    """The arbiter and counter reading taken 20 cycles from the end, into `snap`."""
    yield from idle(cycles - 20)()
    a = dut.bus.arbiter()
    snap["rd_lock"] = (yield a.rd_lock.counter)
    snap["grant"] = (yield a.rr_read.grant)
    snap["ce"] = (yield a.rr_read.ce)
    snap.update((yield from counters(dut)))


def run(gate: str, healthy: bool, cycles: int = CYCLES, boot_probe: bool = True,
        load: bool = True) -> dict[str, object]:
    """One session. `gate` picks the shape, `healthy` the memory.

    Timeline, in the board's order: the store probes at reset; the BIOS takes
    the DFI to software control at `SW_AT` and hands it back at `HAND_AT`; the
    memory answers from cycle 0 when `healthy`, from `HAND_AT` otherwise; the
    response-buffer traffic starts at the handover; a locate re-arms the
    header probe at `LOCATE_AT`; and one more read stands in for firmware's first
    transmit. The load STOPS 300 cycles before the snapshot so the bus can
    drain: a read legitimately in flight would otherwise read as a freeze.
    """
    dut = Session(gate)
    p = dut.bus.port
    quiet = 800
    busy = max(0, cycles - HAND_AT - quiet)
    alive_at = 0 if healthy else HAND_AT

    gens = [memory(dut.bus, cycles, alive_at)()]
    if load:
        gens.append(wb_repeat_reads(p["milan_resp_mem"], 0x40001000, busy,
                                    start=HAND_AT)())
    gens.append(_dfi_handover(dut, cycles))

    beats = []
    watch = {"first_cyc": None, "first_rdy": None, "cyc_dead": 0,
             "alive_at": alive_at}
    snap = {}

    # The other processor bridge performs one plain read long after handover.
    # It is independent of the descriptor bridge and proves a lost descriptor
    # access wedges every read-capable master, not only its originator.
    other_gen, other = wb_one_read(p["milan_resp_mem"], 0x40001000, 600,
                                   start=cycles - 700)

    gens += [_processor(dut, cycles, boot_probe),
             _collector(dut, cycles, beats),
             _monitor(dut, cycles, alive_at, watch),
             other_gen(),
             _arbiter_probe(dut, cycles, snap)]
    run_simulation(dut, gens)
    boot = [b for b in beats if b["t"] < LOCATE_AT]
    late = [b for b in beats if b["t"] >= LOCATE_AT]
    return {"boot": boot, "late": late, "other": other, "arb": snap, **watch}


def _fmt(r):
    a = r["arb"]
    return (f"issued {a.get('issued')} / acked {a.get('acked')} / errored "
            f"{a.get('errored')} / timed_out {a.get('timed_out')}; "
            f"grant {a.get('grant')} ce {a.get('ce')} rd_lock "
            f"{a.get('rd_lock')}; first cyc {r['first_cyc']} first rdy "
            f"{r['first_rdy']} memory alive at {r['alive_at']} "
            f"cycles-on-a-dead-memory {r['cyc_dead']}")


#: Sessions are expensive (about 45 s each on this interconnect), and three of
#: the claims below read the same two runs, so they are built once.
_RUNS = {}


def session(gate: str, healthy: bool) -> dict[str, object]:
    """The run for one (gate, memory) pair, built at most once.

    Three claims read the same two runs and a session costs about 45 s, so
    they share one result rather than each paying for its own.
    """
    key = (gate, healthy)
    if key not in _RUNS:
        _RUNS[key] = run(gate, healthy)
    return _RUNS[key]


# ---------------------------------------------------------------------------
#  the predicates, shared between the fix and the mutants
# ---------------------------------------------------------------------------

def grade(r: dict[str, object]) -> dict[str, bool]:
    """The shipping claims as booleans, so a MUTANT is graded by exactly the
    predicates the fix is graded by. A claim only one of them is applied to is
    a claim nobody has shown can fail."""
    a = r["arb"]
    boot, late = r["boot"], r["late"]
    return {
        "no bus cycle while the memory cannot answer":
            r["cyc_dead"] == 0
            and (r["first_cyc"] is None or r["first_cyc"] >= r["alive_at"]),
        "the boot probe is ANSWERED, and answered err":
            len(boot) == 1 and boot[0]["err"] == 1 and boot[0]["blast"] == 1,
        "answered at once, not after a watchdog":
            bool(boot) and boot[0]["t"] < TMO,
        "the later locate COMPLETES, all four beats, no err":
            len(late) == 4 and not any(b["err"] for b in late)
            and all(b["data"] == WORD_BE for b in late)
            and [b["blast"] for b in late] == [0, 0, 0, 1],
        "nothing timed out":
            a.get("timed_out") == 0 and a.get("issued") == a.get("acked"),
        "another master is answered too":
            bool(r["other"]) and r["other"][0] == ("ack", WORD),
        "the arbiter is free and nothing is outstanding":
            a.get("ce") == 1 and a.get("rd_lock") == 0,
    }


# ---------------------------------------------------------------------------
#  claims
# ---------------------------------------------------------------------------

def test_control_loaded_bus() -> None:
    """A healthy memory, every read-capable path exercised, 1,424 ns per miss.

    The response-buffer bridge loads the same read arbiter, and the descriptor
    bridge is still answered inside its watchdog.
    """
    r = session(GATE_OPEN, True)
    a = r["arb"]
    check("loaded healthy bus: the boot probe is answered",
          len(r["boot"]) == 4 and not any(b["err"] for b in r["boot"]),
          f"got {r['boot']}, {_fmt(r)}")
    check("loaded healthy bus: the later locate is answered",
          len(r["late"]) == 4 and not any(b["err"] for b in r["late"]),
          f"got {r['late']}, {_fmt(r)}")
    check("loaded healthy bus: another master reads too",
          r["other"] and r["other"][0] == ("ack", WORD), f"got {r['other']}")
    check("loaded healthy bus: the bridge was ACKED, not timed out",
          a.get("acked", 0) >= 4 and a.get("timed_out") == 0, _fmt(r))
    check("loaded healthy bus: every access it issued was answered",
          a.get("issued") == a.get("acked"), _fmt(r))
    check("loaded healthy bus: the arbiter still rotates",
          a.get("ce") == 1 or a.get("rd_lock") == 0, _fmt(r))

    # AND WHAT THE GATE COSTS, on that same healthy bus: the boot probe is
    # refused although the memory would have answered it. That is the price of
    # a gate that is not clairvoyant, it is bounded (the store re-probes on the
    # next locate, KL_aecp_desc_store.sv:794), and it is stated here rather
    # than left for the board to discover.
    g = session(GATE_REAL, True)
    # Written None-safe on purpose: a gate that never opens leaves both cycles
    # unset, and a test that raises TypeError there reports a defect as a
    # crash. Every predicate in this file has to survive the shapes it grades.
    check("the gate's COST is one refused boot probe on a healthy bus",
          len(g["boot"]) == 1 and g["boot"][0]["err"] == 1
          and g["first_rdy"] is not None
          and (g["first_cyc"] is None or g["first_cyc"] >= g["first_rdy"]),
          f"got {g['boot']}, {_fmt(g)}")
    check("and nothing after the handover pays it",
          len(g["late"]) == 4 and not any(b["err"] for b in g["late"])
          and g["arb"].get("timed_out") == 0, f"got {g['late']}, {_fmt(g)}")


def test_pre_fix_shape_freezes_the_read_half() -> None:
    """The ungated shape loses its boot probe and never recovers the read half."""
    r = session(GATE_OPEN, False)
    a = r["arb"]
    check("pre-fix: the boot probe is reported err (the watchdog fired)",
          len(r["boot"]) == 1 and r["boot"][0]["err"] == 1,
          f"got {r['boot']}, {_fmt(r)}")
    check("pre-fix: the counters read like the board - issued, none acked",
          a.get("issued", 0) >= 1 and a.get("acked") == 0
          and a.get("errored") == 0 and a.get("timed_out") == a.get("issued"),
          _fmt(r))
    check("pre-fix: another master is STARVED after it",
          r["other"] and r["other"][0][0] == "tmo",
          f"got {r['other']}, {_fmt(r)} - if this passes the freeze stopped "
          "reproducing and the claim below is measuring nothing")
    check("pre-fix: the read grant is frozen on the descriptor bridge",
          a.get("ce") == 0 and a.get("grant") == DESC_MEM, _fmt(r))
    check("pre-fix: an AR is outstanding that will never see r.last",
          a.get("rd_lock") == 1, _fmt(r))
    check("pre-fix: the bridge cannot transact again either",
          len(r["late"]) == 1 and r["late"][0]["err"] == 1,
          f"got {r['late']} - Wishbone2AXILite is parked in READ and never "
          "samples stb & cyc again")


def test_shipping_shape_survives_its_boot_probe() -> None:
    """THE FIX. milan_soc.py's own bridge and gate, DRIVEN.

    The gate is `pp_mem_gate` fed the `sel` sequence a boot performs, and the
    bridge is `pp_desc_bridge`: nothing here is a model of either, so a gate
    that is present and ineffective fails these checks (test_the_claims_can_fail
    is the proof of that, not a claim about it).
    """
    r = session(GATE_REAL, False)
    verdict = grade(r)
    for name, ok in verdict.items():
        check(f"shipping: {name}", ok, _fmt(r))
    check("shipping: the gate opened at the DFI handover and not before",
          r["first_rdy"] is not None and r["first_rdy"] >= HAND_AT,
          f"first rdy {r['first_rdy']}, handover at {HAND_AT} - a gate that "
          "opens on hardware control alone is open at cycle 0")


def test_the_claims_can_fail() -> None:
    """THE MUTANTS. A gate has two ways to be wrong and both must be caught.

    MUTANT 1, `_mem_rdy` tied 1: the gate is present, named in every arm, and
    ineffective. MUTANT 2, tied 0: present, never opens. The second must
    DEGRADE HONESTLY - answer every request `err` on the spot - and not
    deadlock behind a request nobody will take.
    """
    m1 = grade(session(GATE_OPEN, False))
    check("mutant `mem_rdy = 1` is CAUGHT: it drives a bus that cannot answer",
          not m1["no bus cycle while the memory cannot answer"],
          "the ineffective gate is indistinguishable from the fix, so this "
          "file grades spelling and not behaviour")
    caught1 = [k for k, ok in m1.items() if not ok]
    check("mutant `mem_rdy = 1` fails the completion claims as well",
          "the later locate COMPLETES, all four beats, no err" in caught1
          and "another master is answered too" in caught1,
          f"only {caught1} went red")

    m2 = grade(session(GATE_SHUT, False))
    check("mutant `mem_rdy = 0` is CAUGHT: the access never completes",
          not m2["the later locate COMPLETES, all four beats, no err"],
          "a gate that never opens would pass for the fix")
    check("mutant `mem_rdy = 0` degrades HONESTLY: every request is answered",
          m2["the boot probe is ANSWERED, and answered err"]
          and m2["answered at once, not after a watchdog"],
          "a shut gate must answer err on the spot, never stall the request "
          "until the processor's own 4,096-cycle watchdog notices")
    check("mutant `mem_rdy = 0` does not take the bus down with it",
          m2["another master is answered too"]
          and m2["the arbiter is free and nothing is outstanding"],
          "a refused request must not touch the bus at all")


def test_gate_derivation() -> None:
    """`pp_mem_gate` alone: the 1 -> 0 -> 1 edge, and nothing less.

    Cheap and separate from the bus runs above, because it is the one claim
    that is about the DERIVATION rather than about the bridge: `sel` resets to
    1, so a gate built on the level alone is open at cycle 0 and the whole fix
    is a no-op.
    """
    class Gate(Module):
        def __init__(self):
            self.sel = Signal(reset=1)
            self.rdy = Signal()
            self.comb += self.rdy.eq(_milan_soc().pp_mem_gate(self, self.sel))

    dut = Gate()
    seen = {}

    def gen() -> SimGen:
        """Drive `sel` 1 -> 0 -> 1 and read the gate at each of the four moments."""
        yield
        seen["at_config"] = (yield dut.rdy)
        yield dut.sel.eq(0)
        yield
        yield
        seen["in_sw_window"] = (yield dut.rdy)
        yield dut.sel.eq(1)
        yield
        yield
        seen["after_handover"] = (yield dut.rdy)
        for _ in range(20):
            yield
        seen["stays_open"] = (yield dut.rdy)
    run_simulation(dut, [gen()])
    check("hardware control at configuration does NOT open the gate",
          seen.get("at_config") == 0,
          f"got {seen} - `sel` resets to 1, so this is the whole point")
    check("the software-control window keeps it shut",
          seen.get("in_sw_window") == 0, f"got {seen}")
    check("the handover opens it", seen.get("after_handover") == 1,
          f"got {seen}")
    check("and it stays open (a level, not a pulse)",
          seen.get("stays_open") == 1, f"got {seen}")


def test_structural() -> None:
    """THE WIRING, which the simulation above cannot see.

    This file builds `pp_mem_gate` and `pp_desc_bridge` itself, so it would
    pass against a SoC that called neither. These checks are what tie the two
    together, and they are parsed rather than grepped so a comment naming a
    signal cannot satisfy them.
    """
    src = MILAN_SOC.read_text()
    tree = ast.parse(src)

    calls = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            calls.setdefault(n.func.id, []).append(n)

    gate_calls = calls.get("pp_mem_gate", [])
    check("MilanSoC builds the gate with pp_mem_gate", len(gate_calls) == 1,
          f"found {len(gate_calls)}")
    check("the gate is derived from the LiteDRAM DFI handover, not restated",
          bool(gate_calls) and "dfii._control.fields.sel"
          in ast.unparse(gate_calls[0]),
          "a constant or a CSR poke would be a second source of truth")
    check("hardware control ALONE is not taken as proof (sel resets to 1)",
          "_sw_seen" in src,
          "the 1 -> 0 -> 1 edge is what proves the BIOS ran sdram_init")

    br = calls.get("pp_desc_bridge", [])
    check("MilanSoC builds the descriptor bridge with pp_desc_bridge",
          len(br) == 1, f"found {len(br)}")
    check("and hands it THAT gate",
          bool(br) and "_mem_rdy" in {n.id for n in ast.walk(br[0])
                                      if isinstance(n, ast.Name)},
          "the bridge this file drives is not the one the SoC builds")

    # the response bridge is inline (it does not transact out of reset, so it
    # is not simulated here) and must still consult the same gate
    rfsm = [n for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == "act" and n.args
            and isinstance(n.args[0], ast.Constant) and n.args[0].value == "IDLE"
            and isinstance(n.func.value, ast.Name)
            and n.func.value.id == "_rfsm"]
    check("the response bridge's IDLE arm consults the gate too",
          len(rfsm) == 1 and "_mem_rdy" in {n.id for n in ast.walk(rfsm[0])
                                            if isinstance(n, ast.Name)},
          "that FSM can still start a transaction the memory may not end")
    check("the gate is published for firmware diagnostics",
          "mem_rdy=_mem_rdy" in src,
          "issued == 0 stays ambiguous between held-off and never-asked")
    check("the grant table above is the SoC's, in insertion order",
          all(src.index(f'add_master("{a}"') < src.index(f'add_master("{b}"')
              for (a, _), (b, _) in zip(MASTERS, MASTERS[1:])),
          "the wishbone masters are not attached in the order this file assumes")


if __name__ == "__main__":
    print("test_control_loaded_bus:")
    test_control_loaded_bus()
    print("test_pre_fix_shape_freezes_the_read_half:")
    test_pre_fix_shape_freezes_the_read_half()
    print("test_shipping_shape_survives_its_boot_probe:")
    test_shipping_shape_survives_its_boot_probe()
    print("test_the_claims_can_fail:")
    test_the_claims_can_fail()
    print("test_gate_derivation:")
    test_gate_derivation()
    print("test_structural:")
    test_structural()
    print(f"\ntest_pp_boot_bus_freeze: {TALLY['checks']} checks: "
          f"{TALLY['checks'] - TALLY['fails']} PASS, {TALLY['fails']} FAIL")
    print("RESULT:", "FAIL" if TALLY["fails"] else "PASS")
    sys.exit(1 if TALLY["fails"] else 0)
