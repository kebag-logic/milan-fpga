#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""One abandoned descriptor read must not kill the shared dma_bus for good.

THE DEFECT, measured on flashed silicon 2026-08-14 and reproduced below.
`KL_aecp_desc_store` starts in S_HDR_REQ out of reset (KL_aecp_desc_store.sv
:449), so the descriptor bridge asks DDR3 for the entity model at FPGA
CONFIGURATION TIME - before the BIOS has run `sdram_init`, and before software
has put an image at that address. The board's own counters name it exactly:

    fresh boot, no AECP traffic:  ppmem_desc_req   0x00010000   1 issued
                                  ppmem_desc_fault 0x00000001   1 timed out
    after 3 enumeration rounds:                    16 issued, 0 acked,
                                                   0 errored, 16 timed out

What made a lost access FATAL is that the bridge's watchdog releases the
WISHBONE cycle and nothing else: the AXI transaction it already became cannot
be retracted. LiteX's Wishbone2AXILite samples `stb & cyc` in IDLE alone
(axi_lite_to_wishbone.py:166), so it stays parked in READ and forwards nothing
ever again, and the arbiter's `rd_lock` still counts the accepted AR, so

    rr_read.ce = ~(ar.valid | r.valid) & rd_lock.empty      axi_full.py:1188

is 0 for the life of the bitstream. The READ half of dma_bus is then dead for
EVERY master on it. The receipt from the board, same session as the counters:

    milan_dma_tx_enable  1          the ring engine is armed
    milan_dma_tx_wr_ptr  0x760      Linux has queued descriptors
    milan_dma_tx_rd_ptr  0          the engine has fetched NOTHING
    milan_dma_tx_sent    0
    STAT_TX_GOOD (0x9000021c) 0     the MAC transmitted 0 frames in 1,800 s

Linux could not put one packet on the wire all session (both pings 100% loss),
while RX - whose ring writers are WRITE masters, on the write grant - carried
3,795 frames. AVDECC still answered because those responses are built in the
fabric and injected post-shaper, never through this bus.

WHY NO EXISTING TEST CAUGHT IT, and it is the shape of the miss that matters:
every bridge sim we had put ONE master on a memory model that WAS the bus. A
master alone on a bus transacts perfectly and passes forever. So this file
puts the real interconnect and the real neighbours in the simulation:

  * the bus is a real `SoCBusHandler` in "axi" mode, so the real `add_master`
    addressing conversion, the real `Wishbone2AXI` (Wishbone2AXILite +
    AXILite2AXI) and the real `AXIInterconnectShared` (AXIArbiter + AXIDecoder
    + AXITimeout) are all in the path, at the flashed build's widths;
  * ALL EIGHT masters are attached, in the SAME ORDER milan_soc.py attaches
    them and with the same standard each one has, so the grant indices are the
    silicon ones - `milan_desc_mem` is 6 and `milan_resp_mem` is 7, which the
    flashed netlist confirms (`socbushandler1_rr_read_grant == 3'd6` selects
    `axiinterface0`, the descriptor bridge's AXI port);
  * the other masters are DRIVEN, hard enough that the arbiter has to rotate,
    because an idle bus is the case that already passed;
  * the memory answers after a real latency, not in one cycle: the reference
    SoC's own measured miss, 1,424 ns = 142 cycles at 100 MHz, and the bridge
    watchdog `milan_soc.pp_mem_timeout_cycles` derives against it. Both are
    divided by `SIM_SCALE` so a session finishes in seconds; the RATIO, which
    is what every claim rests on, is untouched, and `test_control_loaded_bus`
    is the check that would go red if the scaling flattered the watchdog;
  * and the four counters are the REAL `_PPMemDiag` imported out of
    milan_soc.py, so the printed issued/acked/errored/timed_out is directly
    comparable to the board's 16 / 0 / 0 / 16.

WHAT THE MEMORY MODEL DOES IN THE DEAD WINDOW, and why it is the honest shape.
It ACCEPTS the AR and never answers it. That is not a choice: `AXITimeout`'s
read arm only watches `ar.valid & ~ar.ready` (axi_full.py:1092), its budget on
this bus is 1,000,000 cycles = 10 ms (flashed netlist:
`socbushandler1_rd_timer_count = 20'd1000000`), and the board's freeze outlived
it by five orders of magnitude - so the AR was taken and the data never came. A
model that refused the AR instead would let AXITimeout rescue the bus and the
defect would not reproduce.

WHAT THIS SIMULATION DOES NOT MODEL, stated so a pass is not read as more than
it is: LiteDRAM itself (no DFI, no software-control window, no refresh), the
VexiiRiscv coherent DMA port and its L2, the milan_cd <-> sys CDC in front of
both bridges, and timing closure. A defect living in any of those would not
appear here. What it DOES model is the interconnect this defect propagates
through, and that is where the permanence comes from.

THE FOUR CLAIMS:
  1. CONTROL. A healthy memory with all eight masters loaded: the descriptor
     bridge is answered, timed_out stays 0. Nothing below means anything
     without it - and it is also the experiment that RETIRES contention as a
     cause, which the board round had already argued from `img_valid`
     latching.
  2. THE DEFECT. The PRE-FIX bridge - watchdog, no gate, the flashed shape -
     must still freeze the read half after its boot probe is lost. That keeps
     the defect on record and proves claim 3 is measuring something.
  3. THE FIX. The bridge built in the shape milan_soc.py ACTUALLY DESCRIBES,
     read out of the source: the TX ring reader must survive its boot probe.
     Before the gate landed, that shape was the pre-fix one and this was RED.
  4. STRUCTURAL. The gate is in milan_soc.py, on BOTH bridges, derived from
     the LiteDRAM DFI handover rather than restated.

Run: cd sw/litex && python3 test_pp_boot_bus_freeze.py
"""

import ast
import os
import sys

from migen import *

from litex.soc.integration.soc import SoCBusHandler, SoCRegion
from litex.soc.interconnect import wishbone, axi

HERE = os.path.dirname(os.path.abspath(__file__))
MILAN_SOC = os.path.join(HERE, "milan_soc.py")

#: `dma_bus`'s master table in INSERTION order, with the bus standard each one
#: presents, because the grant index IS the insertion index. Taken from the
#: add_master calls in milan_soc.py and confirmed by the flashed build's log
#: ("milan_desc_mem added as Bus Master" is the seventh of eight).
MASTERS = [
    ("milan_dma_tx",   "axi"),   # 0  TX ring reader - Linux transmits through it
    ("milan_dma_rx",   "axi"),   # 1  RX ring writer
    ("milan_dma_rx1",  "axi"),   # 2  RX ring writer, queue 1
    ("milan_dma_ts",   "wb"),    # 3  timestamp writer
    ("milan_dma_pcm",  "wb"),    # 4  PCM capture ring writer
    ("milan_aaf_pb",   "wb"),    # 5  AAF playback fetch - the proven-good reader
    ("milan_desc_mem", "wb"),    # 6  descriptor image read bridge
    ("milan_resp_mem", "wb"),    # 7  AECP response buffer read+write bridge
]
TX_RING  = 0
AAF_PB   = 5
DESC_MEM = 6

#: The reference SoC's measured miss latency to main memory, 1,424 ns, in sys
#: cycles at 100 MHz. The same measurement `pp_mem_bus_worst_cycles` is built
#: on, so the bus this simulation presents is not a faster one than the
#: watchdog was sized against.
MEM_LATENCY_REAL = 142
SYS_HZ           = 100e6

#: EVERYTHING IN TIME IS SCALED BY THIS, watchdog and memory latency together,
#: and the ratio between them is what the claims actually rest on. migen's
#: simulator runs this eight-master interconnect at about 55 cycles/second, so
#: the shipping 3,072-cycle watchdog would put every session in the minutes and
#: the suite would stop being run. `test_control_loaded_bus` is what proves the
#: scale is not cheating: a loaded, healthy bus must show timed_out = 0, which
#: a watchdog scaled tighter than the bus it watches could not deliver.
SIM_SCALE   = 8
MEM_LATENCY = max(1, MEM_LATENCY_REAL // SIM_SCALE)

WORD = 0x01000100494D4541          # what a healthy memory returns

fails = 0
checks = 0


def check(name, cond, detail=""):
    global fails, checks
    checks += 1
    if cond:
        print(f"  [ok]   {name}")
    else:
        fails += 1
        print(f"  [FAIL] {name} {detail}")


def _milan_soc():
    """The real SoC module: the counters and the watchdog are ITS code."""
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import milan_soc
    return milan_soc


#: The bridge watchdog the SoC derives for the shipping AX shape (sys and milan
#: both 100 MHz), read from milan_soc.py rather than restated - a magic number
#: here would let this file grade a budget the build does not use - then scaled
#: with the memory latency so the pair keeps its ratio.
TMO_REAL = _milan_soc().pp_mem_timeout_cycles(SYS_HZ, SYS_HZ)
TMO      = max(8, TMO_REAL // SIM_SCALE)


# ---------------------------------------------------------------------------
#  the bus: LiteX's own, not a model of it
# ---------------------------------------------------------------------------

class DmaBus(Module):
    """`dma_bus` as milan_soc.py builds it: eight masters, one AXI slave.

    Widths are the flashed build's - 64-bit data, 32-bit byte-addressed AXI,
    word-addressed 64-bit wishbone masters, id_width 4 on the native ones, one
    slave covering the whole space. Nothing here models the interconnect:
    `SoCBusHandler.finalize()` builds it, so this cannot agree with a bug the
    real one does not have.
    """

    def __init__(self):
        self.submodules.h = h = SoCBusHandler(
            name          = "SoCDMABusHandler",
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

    def arbiter(self):
        return dict(self.h._submodules)["_interconnect"].arbiter


# ---------------------------------------------------------------------------
#  the descriptor bridge, in both shapes
# ---------------------------------------------------------------------------

class DescBridge(Module):
    """milan_soc.py's `descmem_fsm`, with the memory-ready gate optional.

    `gate=False` is the flashed shape: IDLE takes the request and goes straight
    to the bus state whatever main memory is doing. `gate=True` is the shipping
    shape: a request that arrives before main memory can end a transaction is
    ANSWERED `err` and never becomes a bus cycle. The watchdog, the poison flag
    and the emit arm are identical between the two, so the only variable is the
    gate.

    It is a REPLICA, not the SoC's own FSM - `descmem_fsm` is built inline in
    `MilanSoC.__init__` around a `milan_datapath` blackbox and cannot be
    instantiated on its own. `test_structural` below and
    `test_pp_mem_bridge.test_structural` both parse milan_soc.py so the replica
    cannot drift from what the build generates.
    """

    def __init__(self, wb, gate, tmo=TMO):
        self.req_valid = Signal()
        self.req_addr  = Signal(32)
        self.req_beats = Signal(9)
        self.rsp_valid = Signal()
        self.rsp_err   = Signal()
        self.mem_rdy   = Signal(reset=1)
        self.psn = psn = Signal()
        self.psn_set = psn_set = Signal()

        _da = Signal(32); _dl = Signal(9); _dd = Signal(64); _de = Signal()
        _dto = Signal(max=tmo + 1)
        self.sync += If(psn_set, psn.eq(1)
                     ).Elif(psn & (wb.ack | wb.err), psn.eq(0))

        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        start = [NextValue(_da, self.req_addr), NextValue(_dl, self.req_beats),
                 NextValue(_dto, 0)]
        if gate:
            fsm.act("IDLE",
                If(self.req_valid, *start,
                    NextValue(_de, psn | ~self.mem_rdy),
                    If(self.mem_rdy, NextState("RD")).Else(NextState("EMIT"))))
        else:
            fsm.act("IDLE",
                If(self.req_valid, *start,
                    NextValue(_de, psn), NextState("RD")))
        fsm.act("RD",
            wb.cyc.eq(1), wb.stb.eq(1), wb.sel.eq(0xFF), wb.adr.eq(_da[3:]),
            NextValue(_dto, _dto + 1),
            If(wb.ack,
                NextValue(_dto, 0),
                If(wb.err, NextValue(_de, 1)).Else(NextValue(_dd, wb.dat_r)),
                NextState("EMIT")
            ).Elif(_dto == tmo,
                NextValue(_dto, 0), NextValue(_de, 1),
                psn_set.eq(1), NextState("EMIT")))
        fsm.act("EMIT",
            self.rsp_valid.eq(1), self.rsp_err.eq(_de),
            If(_de | (_dl == 1), NextState("IDLE")
            ).Else(NextValue(_da, _da + 8), NextValue(_dl, _dl - 1),
                   NextValue(_dto, 0), NextState("RD")))


class Session(Module):
    """The bus, the bridge on grant index 6, and the REAL counter block."""

    def __init__(self, gate):
        self.submodules.bus = self.bus = DmaBus()
        wb = self.bus.port["milan_desc_mem"]
        self.submodules.br = self.br = DescBridge(wb, gate)
        self.submodules.diag = self.diag = _milan_soc()._PPMemDiag(
            [("desc", wb, self.br.psn, self.br.psn_set)])


def counters(dut):
    """The two CSR words, decoded the way the register map documents them."""
    req = yield dut.diag.desc_req.status
    flt = yield dut.diag.desc_fault.status
    return {"issued": (req >> 16) & 0xFFFF, "acked": req & 0xFFFF,
            "errored": (flt >> 16) & 0xFFFF, "timed_out": flt & 0xFFFF}


# ---------------------------------------------------------------------------
#  the memory, and the neighbours that load the bus
# ---------------------------------------------------------------------------

def memory(dut, cycles, alive_at=0, latency=MEM_LATENCY):
    """Main memory: `latency` cycles, ARLEN+1 beats, writes answered on B.

    Before `alive_at` a read COMMAND IS ACCEPTED AND SWALLOWED - see the banner
    for why that, and not a refused AR, is the shape the board proves.
    """
    s = dut.slave

    def gen():
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

def axi_burst_reader(iface, addr, beats, cycles, start=0, out=None):
    """A ring engine: back-to-back INCR read bursts, R beats always taken."""
    def gen():
        yield iface.r.ready.eq(1)
        yield iface.ar.addr.eq(addr)
        yield iface.ar.len.eq(beats - 1)
        yield iface.ar.size.eq(3)
        yield iface.ar.burst.eq(1)
        for _ in range(start):
            yield
        got = beats
        for _ in range(cycles):
            if got >= beats:
                yield iface.ar.valid.eq(1)
            if (yield iface.ar.valid) and (yield iface.ar.ready):
                yield iface.ar.valid.eq(0)
                got = 0
            if (yield iface.r.valid) and (yield iface.r.ready):
                got += 1
                if out is not None:
                    out.append((yield iface.r.data))
            yield
        yield iface.ar.valid.eq(0)
    return gen


def axi_writer(iface, addr, cycles, start=0):
    """A ring writer: single-beat writes, to load the WRITE grant."""
    def gen():
        yield iface.aw.addr.eq(addr)
        yield iface.aw.len.eq(0)
        yield iface.aw.size.eq(3)
        yield iface.aw.burst.eq(1)
        yield iface.w.last.eq(1)
        yield iface.w.strb.eq(0xFF)
        yield iface.b.ready.eq(1)
        for _ in range(start):
            yield
        yield iface.aw.valid.eq(1)
        yield iface.w.valid.eq(1)
        aw = w = False
        for _ in range(cycles):
            if (yield iface.aw.valid) and (yield iface.aw.ready):
                yield iface.aw.valid.eq(0)
                aw = True
            if (yield iface.w.valid) and (yield iface.w.ready):
                yield iface.w.valid.eq(0)
                w = True
            if aw and w and (yield iface.b.valid):
                yield iface.aw.valid.eq(1)
                yield iface.w.valid.eq(1)
                aw = w = False
            yield
        yield iface.aw.valid.eq(0)
        yield iface.w.valid.eq(0)
    return gen


def wb_reader(wb, addr, cycles, start=0, out=None):
    """A wishbone read master hammering the bus (`milan_aaf_pb`'s shape)."""
    def gen():
        yield wb.adr.eq(addr >> 3)
        yield wb.sel.eq(0xFF)
        yield wb.we.eq(0)
        for _ in range(start):
            yield
        yield wb.cyc.eq(1)
        yield wb.stb.eq(1)
        for _ in range(cycles):
            if (yield wb.ack) or (yield wb.err):
                if out is not None:
                    out.append((yield wb.dat_r))
                yield wb.cyc.eq(0)
                yield wb.stb.eq(0)
                yield
                yield wb.cyc.eq(1)
                yield wb.stb.eq(1)
            yield
        yield wb.cyc.eq(0)
        yield wb.stb.eq(0)
    return gen


def wb_one_read(wb, addr, budget, start=0):
    """One wishbone read, abandoned after `budget` cycles."""
    out = []

    def gen():
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


def idle(n):
    def gen():
        for _ in range(n):
            yield
    return gen


# ---------------------------------------------------------------------------
#  the session
# ---------------------------------------------------------------------------

def run(gate, alive_at, cycles, boot_probe=True, load=True):
    """One session with every master present, and loaded unless `load` is off.

    Timeline, in the board's order: the store probes at reset; main memory
    starts answering at `alive_at` (the BIOS finishing `sdram_init`, which is
    also when `mem_rdy` rises - the gate is not clairvoyant, it is exactly the
    DFI handover); the ring engines and the playback fetch start there too,
    since nothing on the board reads DRAM before the driver is up; a locate
    re-arms the header probe; and one more read stands in for Linux's first
    transmit. The load STOPS 300 cycles before the snapshot so the bus can
    drain: a read legitimately in flight would otherwise read as a freeze.
    """
    dut = Session(gate)
    p = dut.bus.port
    quiet = 300
    busy = max(0, cycles - alive_at - quiet)

    gens = [memory(dut.bus, cycles, alive_at)()]
    if load:
        gens += [
            axi_burst_reader(p["milan_dma_tx"], 0x40001000, 16, busy,
                             start=alive_at)(),
            axi_writer(p["milan_dma_rx"], 0x40010000, busy, start=alive_at)(),
            axi_writer(p["milan_dma_rx1"], 0x40020000, busy, start=alive_at)(),
            wb_reader(p["milan_aaf_pb"], 0x4FE00000, busy, start=alive_at)(),
        ]

    def dram():
        """`mem_rdy`: main memory can end a transaction, never before."""
        yield dut.br.mem_rdy.eq(0)
        for _ in range(alive_at):
            yield
        yield dut.br.mem_rdy.eq(1)
    gens.append(dram())

    boot = {}
    late = {}

    # The locate is scheduled on the ABSOLUTE clock, not relative to the boot
    # answer: the two shapes answer that probe whole watchdogs apart (the
    # gated one answers at once, the flashed one after `TMO`), and a relative
    # schedule would put the locate before `alive_at` in one shape and after
    # it in the other, which would compare two different experiments.
    locate_at = alive_at + 400

    def processor():
        t = 0
        if boot_probe:
            # the boot walk: KL_aecp_desc_store is in S_HDR_REQ out of reset
            yield dut.br.req_addr.eq(0x7F700000)
            yield dut.br.req_beats.eq(4)
            yield dut.br.req_valid.eq(1)
            yield
            t += 1
            yield dut.br.req_valid.eq(0)
            while t < locate_at and "err" not in boot:
                if (yield dut.br.rsp_valid):
                    boot["err"] = (yield dut.br.rsp_err)
                yield
                t += 1
        # a locate re-arms the header probe long after the BIOS is done
        while t < locate_at:
            yield
            t += 1
        yield dut.br.req_addr.eq(0x7F700000)
        yield dut.br.req_beats.eq(1)
        yield dut.br.req_valid.eq(1)
        yield
        yield dut.br.req_valid.eq(0)
        for _ in range(TMO + 200):
            if (yield dut.br.rsp_valid):
                late["err"] = (yield dut.br.rsp_err)
                break
            yield

    # Linux's first transmit, as a plain read on a master that had nothing to
    # do with the protocol processor, issued long after main memory is healthy
    tx_gen, tx = wb_one_read(p["milan_dma_ts"], 0x40001000, 600,
                             start=cycles - 700)
    snap = {}

    def probe():
        yield from idle(cycles - 20)()
        a = dut.bus.arbiter()
        snap["rd_lock"] = (yield a.rd_lock.counter)
        snap["grant"] = (yield a.rr_read.grant)
        snap["ce"] = (yield a.rr_read.ce)
        snap.update((yield from counters(dut)))

    gens += [processor(), tx_gen(), probe()]
    run_simulation(dut, gens)
    return {"boot": boot, "late": late, "tx": tx, "arb": snap}


def _fmt(r):
    a = r["arb"]
    return (f"issued {a.get('issued')} / acked {a.get('acked')} / errored "
            f"{a.get('errored')} / timed_out {a.get('timed_out')}; "
            f"grant {a.get('grant')} ce {a.get('ce')} rd_lock "
            f"{a.get('rd_lock')}")


# ---------------------------------------------------------------------------
#  the source: which shape is actually built
# ---------------------------------------------------------------------------

def _idle_arms():
    """The IDLE arm of each bridge FSM in milan_soc.py, as an AST."""
    tree = ast.parse(open(MILAN_SOC).read())
    out = {}
    for n in ast.walk(tree):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "act" and n.args
                and isinstance(n.args[0], ast.Constant)
                and n.args[0].value == "IDLE"
                and isinstance(n.func.value, ast.Name)
                and n.func.value.id in ("_dfsm", "_rfsm")):
            out[n.func.value.id] = n
    return out


def shipping_gate():
    """True when milan_soc.py's descriptor bridge consults the gate in IDLE."""
    arm = _idle_arms().get("_dfsm")
    if arm is None:
        return False
    return "_mem_rdy" in {n.id for n in ast.walk(arm) if isinstance(n, ast.Name)}


# ---------------------------------------------------------------------------
#  claims
# ---------------------------------------------------------------------------

def test_control_loaded_bus():
    """A healthy memory, all eight masters loaded, 1,424 ns per miss.

    This is also the experiment that retires CONTENTION as a cause: the bridge
    shares the bus with two ring writers, a 16-beat burst reader and the
    playback fetch, and is still answered inside its watchdog.
    """
    for gate in (False, True):
        tag = "gated" if gate else "pre-fix"
        r = run(gate=gate, alive_at=0, cycles=1800)
        a = r["arb"]
        check(f"loaded healthy bus ({tag}): the boot probe is answered",
              r["boot"].get("err") == 0, f"got {r['boot']}, {_fmt(r)}")
        check(f"loaded healthy bus ({tag}): the later locate is answered",
              r["late"].get("err") == 0, f"got {r['late']}, {_fmt(r)}")
        check(f"loaded healthy bus ({tag}): another master reads too",
              r["tx"] and r["tx"][0] == ("ack", WORD), f"got {r['tx']}")
        check(f"loaded healthy bus ({tag}): the bridge was ACKED, not timed out",
              a.get("acked", 0) >= 4 and a.get("timed_out") == 0, _fmt(r))
        check(f"loaded healthy bus ({tag}): every access it issued was answered",
              a.get("issued") == a.get("acked"), _fmt(r))
        check(f"loaded healthy bus ({tag}): the arbiter still rotates",
              a.get("ce") == 1 or a.get("rd_lock") == 0, _fmt(r))


def test_pre_fix_shape_freezes_the_read_half():
    """THE DEFECT, kept on record. The flashed shape puts its boot probe on a
    bus that cannot answer it, and the read half never recovers - for masters
    that had nothing to do with the protocol processor."""
    r = run(gate=False, alive_at=TMO + 200, cycles=TMO + 2000)
    a = r["arb"]
    check("pre-fix: the boot probe is reported err (the watchdog fired)",
          r["boot"].get("err") == 1, f"got {r['boot']}, {_fmt(r)}")
    check("pre-fix: the counters read like the board - issued, none acked",
          a.get("issued", 0) >= 1 and a.get("acked") == 0
          and a.get("errored") == 0 and a.get("timed_out") == a.get("issued"),
          f"{_fmt(r)} - the board reads 16 / 0 / 0 / 16")
    check("pre-fix: another master is STARVED after it",
          r["tx"] and r["tx"][0][0] == "tmo",
          f"got {r['tx']}, {_fmt(r)} - if this passes the freeze stopped "
          "reproducing and the claim below is measuring nothing")
    check("pre-fix: the read grant is frozen on the descriptor bridge",
          a.get("ce") == 0 and a.get("grant") == DESC_MEM, _fmt(r))
    check("pre-fix: an AR is outstanding that will never see r.last",
          a.get("rd_lock") == 1, _fmt(r))
    check("pre-fix: the bridge cannot transact again either",
          r["late"].get("err") == 1,
          f"got {r['late']} - Wishbone2AXILite is parked in READ and never "
          "samples stb & cyc again")


def test_shipping_shape_survives_its_boot_probe():
    """THE FIX. Built in the shape milan_soc.py actually describes."""
    gate = shipping_gate()
    check("the shipping descriptor bridge consults a memory-ready gate", gate,
          "milan_soc.py's _dfsm IDLE arm goes to the bus state unconditionally")
    r = run(gate=gate, alive_at=TMO + 200, cycles=TMO + 2000)
    a = r["arb"]
    check("shipping: the boot probe is answered err WITHOUT a bus cycle",
          r["boot"].get("err") == 1, f"got {r['boot']}, {_fmt(r)}")
    check("shipping: nothing was issued while memory could not answer",
          a.get("timed_out") == 0, f"{_fmt(r)}")
    check("shipping: another master is answered once memory is healthy",
          r["tx"] and r["tx"][0] == ("ack", WORD),
          f"got {r['tx']}, {_fmt(r)} - on silicon this reads tx_rd_ptr=0, "
          "tx_sent=0, STAT_TX_GOOD=0 with the ring armed")
    check("shipping: the descriptor bridge transacts on the later locate",
          r["late"].get("err") == 0 and a.get("acked", 0) >= 1, f"{_fmt(r)}")
    check("shipping: the arbiter is free and nothing is outstanding",
          a.get("ce") == 1 and a.get("rd_lock") == 0, _fmt(r))


def test_structural():
    """The gate has to be IN milan_soc.py, on BOTH bridges, and derived from
    LiteDRAM rather than restated - a model of it would pass against a design
    that never grew one."""
    src = open(MILAN_SOC).read()
    check("the gate is derived from the LiteDRAM DFI handover, not restated",
          "dfii._control.fields.sel" in src,
          "a constant or a CSR poke would be a second source of truth")
    check("hardware control ALONE is not taken as proof (sel resets to 1)",
          "_sw_seen" in src,
          "the 1 -> 0 -> 1 edge is what proves the DDR3 was initialised")
    arms = _idle_arms()
    check("both bridge FSMs have an IDLE arm to gate", len(arms) == 2,
          f"found {sorted(arms)}")
    for who, arm in sorted(arms.items()):
        names = {n.id for n in ast.walk(arm) if isinstance(n, ast.Name)}
        check(f"{who} IDLE consults the memory-ready gate", "_mem_rdy" in names,
              "this FSM can still start a transaction main memory cannot end")
    check("the gate is published so the board can read it back",
          "mem_rdy=_mem_rdy" in src,
          "issued == 0 stays ambiguous between held-off and never-asked")
    check("the grant table above is the SoC's, in insertion order",
          all(src.index(f'add_master("{a}"') < src.index(f'add_master("{b}"')
              for (a, _), (b, _) in zip(MASTERS[3:-1], MASTERS[4:])),
          "the wishbone masters are not attached in the order this file assumes")


if __name__ == "__main__":
    print("test_control_loaded_bus:")
    test_control_loaded_bus()
    print("test_pre_fix_shape_freezes_the_read_half:")
    test_pre_fix_shape_freezes_the_read_half()
    print("test_shipping_shape_survives_its_boot_probe:")
    test_shipping_shape_survives_its_boot_probe()
    print("test_structural:")
    test_structural()
    print(f"\ntest_pp_boot_bus_freeze: {checks} checks: "
          f"{checks - fails} PASS, {fails} FAIL")
    print("RESULT:", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)
