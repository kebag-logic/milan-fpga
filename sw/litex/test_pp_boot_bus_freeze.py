#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""One abandoned descriptor read must not kill the shared dma_bus for good.

THE DEFECT, measured on flashed silicon 2026-08-14 and reproduced below.
`KL_aecp_desc_store` resets to S_HDR_REQ (KL_aecp_desc_store.sv:449), so it is
the one master on this bus that TRANSACTS OUT OF RESET: it asks for the entity
model at FPGA CONFIGURATION TIME. (Not "the only master without a software
enable" - `milan_resp_mem` has no enable either, it just resets to R_FILL,
KL_aecp_resp_buf.sv:353, which does not transact.) The board's own counters
name the boot probe exactly:

    fresh boot, no AECP traffic:  ppmem_desc_req   0x00010000   1 issued
                                  ppmem_desc_fault 0x00000001   1 timed out
    after 3 enumeration rounds:                    16 issued, 0 acked,
                                                   0 errored, 16 timed out

WHY THAT ACCESS WAS NEVER ANSWERED IS UNIDENTIFIED, and this file does not
supply a mechanism for it. See `pp_mem_gate` in milan_soc.py for the two that
were written down and refuted (LiteDRAM answers reads at configuration, with
garbage; an unloaded address answers too, and garbage fails the store's header
check as fault 1 = FAULT_MAGIC_C, not the fault 8 = FAULT_TIMEOUT_C measured).
What IS established is the consequence, and that is what is simulated here.

WHO NEVER ANSWERED IS NOT THE DDR3. `dma_bus` has EXACTLY ONE SLAVE and it is
the CPU: "Interconnect: AXIInterconnectShared (8 <-> 1)" (litex.log:103 of the
flashed build) and the slave's AR lands on
`milansoc_milansoc_vexiiriscv_dma_bus_ar_valid` (alinx_ax7101.v:12288). The
block that accepted the AR and never returned R is the VexiiRiscv coherent-DMA
slave port and its coherency hub; main memory is two hops further on. The name
matters because it is where the next debugger looks.

What made a lost access FATAL is that the bridge's watchdog releases the
WISHBONE cycle and nothing else: the AXI transaction it already became cannot
be retracted. LiteX's Wishbone2AXILite samples `stb & cyc` in IDLE alone
(axi_lite_to_wishbone.py:166), so it stays parked in READ and forwards nothing
ever again, and the arbiter's `rd_lock` still counts the accepted AR, so

    rr_read.ce = ~(ar.valid | r.valid) & rd_lock.ready     axi_full.py:1188

(`ready` is that counter's own alias for `empty`, same file:1113) is 0 for the
life of the bitstream. The READ half of dma_bus is then dead for EVERY master
on it. The receipt from the board, same session as the counters:

    milan_dma_tx_enable  1          the ring engine is armed
    milan_dma_tx_wr_ptr  0x760      Linux has queued descriptors
    milan_dma_tx_rd_ptr  0          the engine has fetched NOTHING
    milan_dma_tx_sent    0
    STAT_TX_GOOD (0x9000021c) 0     the MAC transmitted 0 frames in 1,800 s

Linux could not put one packet on the wire all session (both pings 100% loss),
while RX - whose ring writers are WRITE masters, on the write grant - carried
3,795 frames. AVDECC still answered because those responses are built in the
fabric and injected post-shaper, never through this bus.

WHAT THE GAP ACTUALLY WAS, because the first version of this banner overstated
it. It claimed every prior bridge sim put ONE master on a memory model that WAS
the bus. That is true of `test_pp_mem_bridge.py` and `test_pb_bus_err.py` and
false as a statement about the suite: `test_dma_bus_faults.py`, tracked in this
directory, already puts THREE masters (`B_REQS`) on the real
`AXIArbiter`/`AXIDecoder`/`AXITimeout` composition and characterises this exact
freeze as its defect B - reported XFAIL, because the defect is LiteX's and not
ours. The interconnect's behaviour was already on record. The real gap is
narrower: NOTHING DROVE OUR BRIDGE ACROSS A WINDOW IN WHICH MEMORY COULD NOT
ANSWER, so nothing graded what the protocol processor does to that bus at boot.
This file is that experiment:

  * the bus is a real `SoCBusHandler` in "axi" mode, so the real `add_master`
    addressing conversion, the real `Wishbone2AXI` (Wishbone2AXILite +
    AXILite2AXI) and the real `AXIInterconnectShared` (AXIArbiter + AXIDecoder
    + AXITimeout) are all in the path, at the flashed build's widths;
  * ALL EIGHT masters are attached, in the SAME ORDER milan_soc.py attaches
    them and with the same standard each one has, so the grant indices are the
    silicon ones - `milan_desc_mem` is 6 and `milan_resp_mem` is 7, which the
    flashed netlist confirms (`socbushandler1_rr_read_grant == 3'd6` selects
    `axiinterface0`, the descriptor bridge's AXI port);
  * the bridge is milan_soc.py's OWN `pp_desc_bridge` and the gate is its own
    `pp_mem_gate`, imported, not modelled. A replica cannot fail against a gate
    that is present and ineffective, which is exactly the defect a test of a
    gate has to be able to see;
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
it is: LiteDRAM itself (no DFI beyond the one `sel` bit, no PHY, no refresh),
the VexiiRiscv coherent DMA port and its L2 - which is the block that actually
failed to answer - the milan_cd <-> sys CDC in front of both bridges, and
timing closure. AND THE WINDOW IS ASSUMED, not derived: the dead window here
ends at the DFI handover because that is where the gate opens, so this file
proves the gate covers the window it was built for. If the real trigger outlives
the handover, every check below still passes and the board still freezes; the
board's own `stat[4]` is what settles that, not this file.

THE FIVE CLAIMS:
  1. CONTROL. A healthy memory with all eight masters loaded: the bridge is
     answered, timed_out stays 0. Nothing below means anything without it - and
     it is also the experiment that RETIRES contention as a cause, which the
     board round had already argued from `img_valid` latching.
  2. THE DEFECT. The PRE-FIX bridge - the shipping arms with the gate tied 1,
     which is the flashed shape - must still freeze the read half after its
     boot probe is lost. That keeps the defect on record and proves claim 3 is
     measuring something.
  3. THE FIX, driven and not parsed: milan_soc.py's own bridge and gate, with
     the DFI `sel` sequence a boot performs. No bus cycle while the gate is
     shut; a real burst, completed, once it opens.
  4. THE CLAIMS CAN FAIL. The same predicates, applied to two mutants: the gate
     tied 1 (present, ineffective) and the gate tied 0 (present, never opens).
     Each must be caught, and the second must degrade honestly rather than
     deadlock. A test that cannot name what would falsify it is not a test.
  5. STRUCTURAL. The wiring the simulation cannot see: that MilanSoC feeds that
     gate to that bridge, to the response bridge, and to the observer.

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
#: The same word as the PROCESSOR must see it. A beat carries its lowest byte
#: address in bits [63:56] - 1722.1 wire order, big-endian - and the bus words
#: are little-endian, so the bridge byte-reverses. Checking the payload and not
#: just `err` is what makes "the access completed" a measurement.
WORD_BE = int.from_bytes(WORD.to_bytes(8, "little"), "big")

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
    """The real SoC module: the bridge, the gate and the counters are ITS code."""
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

class DmaBus(Module):
    """`dma_bus` as milan_soc.py builds it: eight masters, one AXI slave.

    Widths are the flashed build's - 64-bit data, 32-bit byte-addressed AXI,
    word-addressed 64-bit wishbone masters, id_width 4 on the native ones, one
    slave covering the whole space. Nothing here models the interconnect:
    `SoCBusHandler.finalize()` builds it, so this cannot agree with a bug the
    real one does not have.

    THE SLAVE STANDS FOR THE CPU's coherent-DMA port, not for DDR3: on the
    board that one slave is `milansoc_milansoc_vexiiriscv_dma_bus_*`. Main
    memory is behind it, through the coherency hub and the L2, neither of which
    is modelled here.
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
#  the device under test: milan_soc.py's own bridge, on that bus
# ---------------------------------------------------------------------------

#: The three gate shapes this file drives. "real" is the shipping wiring;
#: "open" is the flashed pre-fix shape AND the mutant the fix must not be
#: mistaken for; "shut" is a gate that is present and never opens.
GATE_REAL = "real"
GATE_OPEN = "open"
GATE_SHUT = "shut"


class Session(Module):
    """The bus, milan_soc.py's bridge on grant index 6, and the REAL counters.

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
        self.submodules.bus = self.bus = DmaBus()
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

def run(gate, healthy, cycles=CYCLES, boot_probe=True, load=True):
    """One session. `gate` picks the shape, `healthy` the memory.

    Timeline, in the board's order: the store probes at reset; the BIOS takes
    the DFI to software control at `SW_AT` and hands it back at `HAND_AT`; the
    memory answers from cycle 0 when `healthy`, from `HAND_AT` otherwise; the
    ring engines and the playback fetch start at the handover, since nothing on
    the board reads main memory before the driver is up; a locate re-arms the
    header probe at `LOCATE_AT`; and one more read stands in for Linux's first
    transmit. The load STOPS 300 cycles before the snapshot so the bus can
    drain: a read legitimately in flight would otherwise read as a freeze.
    """
    dut = Session(gate)
    p = dut.bus.port
    quiet = 300
    busy = max(0, cycles - HAND_AT - quiet)
    alive_at = 0 if healthy else HAND_AT

    gens = [memory(dut.bus, cycles, alive_at)()]
    if load:
        gens += [
            axi_burst_reader(p["milan_dma_tx"], 0x40001000, 16, busy,
                             start=HAND_AT)(),
            axi_writer(p["milan_dma_rx"], 0x40010000, busy, start=HAND_AT)(),
            axi_writer(p["milan_dma_rx1"], 0x40020000, busy, start=HAND_AT)(),
            wb_reader(p["milan_aaf_pb"], 0x4FE00000, busy, start=HAND_AT)(),
        ]

    def dfi():
        """The one DFI bit the gate reads: 1 at configuration, 0 for the
        BIOS's software-control window, 1 again when `sdram_init` is done."""
        for _ in range(SW_AT):
            yield
        yield dut.sel.eq(0)
        for _ in range(HAND_AT - SW_AT):
            yield
        yield dut.sel.eq(1)
        for _ in range(cycles - HAND_AT):
            yield
    gens.append(dfi())

    def processor():
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

    beats = []

    def collector():
        """Every response beat the processor would see, with its cycle."""
        for t in range(cycles):
            if (yield dut.rsp.valid):
                beats.append({"t": t, "err": (yield dut.rsp.err),
                              "data": (yield dut.rsp.data),
                              "blast": (yield dut.rsp.blast)})
            yield

    watch = {"first_cyc": None, "first_rdy": None, "cyc_dead": 0,
             "alive_at": alive_at}

    def monitor():
        """WAS THE BUS TOUCHED WHILE THE MEMORY COULD NOT ANSWER.

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

    # Linux's first transmit, as a plain read on a master that had nothing to
    # do with the protocol processor, issued long after the handover
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

    gens += [processor(), collector(), monitor(), tx_gen(), probe()]
    run_simulation(dut, gens)
    boot = [b for b in beats if b["t"] < LOCATE_AT]
    late = [b for b in beats if b["t"] >= LOCATE_AT]
    return {"boot": boot, "late": late, "tx": tx, "arb": snap, **watch}


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


def session(gate, healthy):
    key = (gate, healthy)
    if key not in _RUNS:
        _RUNS[key] = run(gate, healthy)
    return _RUNS[key]


# ---------------------------------------------------------------------------
#  the predicates, shared between the fix and the mutants
# ---------------------------------------------------------------------------

def grade(r):
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
            bool(r["tx"]) and r["tx"][0] == ("ack", WORD),
        "the arbiter is free and nothing is outstanding":
            a.get("ce") == 1 and a.get("rd_lock") == 0,
    }


# ---------------------------------------------------------------------------
#  claims
# ---------------------------------------------------------------------------

def test_control_loaded_bus():
    """A healthy memory, all eight masters loaded, 1,424 ns per miss.

    This is also the experiment that retires CONTENTION as a cause: the bridge
    shares the bus with two ring writers, a 16-beat burst reader and the
    playback fetch, and is still answered inside its watchdog.
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
          r["tx"] and r["tx"][0] == ("ack", WORD), f"got {r['tx']}")
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


def test_pre_fix_shape_freezes_the_read_half():
    """THE DEFECT, kept on record. The flashed shape puts its boot probe on a
    bus that cannot answer it, and the read half never recovers - for masters
    that had nothing to do with the protocol processor."""
    r = session(GATE_OPEN, False)
    a = r["arb"]
    check("pre-fix: the boot probe is reported err (the watchdog fired)",
          len(r["boot"]) == 1 and r["boot"][0]["err"] == 1,
          f"got {r['boot']}, {_fmt(r)}")
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
          len(r["late"]) == 1 and r["late"][0]["err"] == 1,
          f"got {r['late']} - Wishbone2AXILite is parked in READ and never "
          "samples stb & cyc again")


def test_shipping_shape_survives_its_boot_probe():
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


def test_the_claims_can_fail():
    """THE MUTANTS. A gate has two ways to be wrong and both must be caught.

    MUTANT 1, `_mem_rdy` tied 1: the gate is present, named in every arm, and
    ineffective. This is also the shape that was flashed, so it is not a
    hypothetical. MUTANT 2, tied 0: present, never opens. The second must
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


def test_gate_derivation():
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

    def gen():
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


def test_structural():
    """THE WIRING, which the simulation above cannot see.

    This file builds `pp_mem_gate` and `pp_desc_bridge` itself, so it would
    pass against a SoC that called neither. These checks are what tie the two
    together, and they are parsed rather than grepped so a comment naming a
    signal cannot satisfy them.
    """
    src = open(MILAN_SOC).read()
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
    print("test_the_claims_can_fail:")
    test_the_claims_can_fail()
    print("test_gate_derivation:")
    test_gate_derivation()
    print("test_structural:")
    test_structural()
    print(f"\ntest_pp_boot_bus_freeze: {checks} checks: "
          f"{checks - fails} PASS, {fails} FAIL")
    print("RESULT:", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)
