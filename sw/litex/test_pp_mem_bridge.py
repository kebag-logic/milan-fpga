#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""The protocol processor's two main-memory bridges must survive a dead bus.

THE DEFECT (measured on flashed silicon 2026-08-13). Every AECP command came
back ENTITY_MISBEHAVING because neither main-memory master completed a
transaction. The processor's snapshot window named both faults:

    word 34 = 0x0000F150   image INVALID, descriptor-store fault 8
    word 35 = 0x00230002   35 responses voided, 2 lane writes committed
    word 36 = 0x00000001   response-buffer fault 1

  fault 8 = FAULT_TIMEOUT_C (KL_aecp_desc_store.sv:198)
  fault 1 = FAULT_WTMO_C    (KL_aecp_resp_buf.sv:180)

Both are TIMEOUTS, and that is the whole diagnosis. LiteX's wishbone2axi
answers a FAILED access with `err` AND `ack` in the same cycle - the error arm
these FSMs already had would have produced NO_SUCH_DESCRIPTOR, which is not
what the board reported. A timeout means the access was never acked at all, and
every bus state left ONLY on `ack`:

    _dfsm.act("RD_LO", ..., If(_dwb.ack, ...))     # and nothing else

so one unanswered access parked the FSM there permanently, holding `cyc`/`stb`.
That is what made a local stall fatal: the generated netlist arbitrates the
dedicated protocol-memory port with

    socbushandler1_rr_read_ce = ~(ar_valid | r_valid) & rd_lock_empty

i.e. it re-arbitrates only when NOTHING is outstanding, so one wedged master
freezes the read half for every master on that bus. `dbg_lane_wr = 2` is the
receipt that the masters themselves transact: the write half stayed alive long
enough to commit two lanes, and stopped when the response's read-back went out
on the frozen read half and parked the response FSM in ITS read state.

WHAT THIS FILE PROVES, in two independent ways so neither can pass vacuously:
  1. BEHAVIOURAL. Both FSM shapes are built in the same run - the pre-fix one
     (ack-only) and the shipping one (ack + watchdog) - and driven by the SAME
     dead-bus stimulus. The pre-fix one must still be holding cyc/stb with no
     answer given; the shipping one must report `err` and end the wishbone
     cycle. If the watchdog were inert the two would agree and this test fails.
     THE SCOPE IS THE WISHBONE FACE ONLY, and the 2026-08-14 board round is the
     receipt for saying so: the memory model here IS the bus, so ending the
     cycle looks like releasing the bus, and on the real chain it is not. The
     AXI transaction the converter already launched cannot be retracted, so the
     shared read grant freezes behind it and takes the peer bridge
     with it. That claim needs the real LiteX arbiter in the simulation, and
     `test_pp_boot_bus_freeze.py` is where it is graded.
  2. RECOVERY, and it is a SEPARATE claim from the watchdog's. Letting go of
     the bus is worth nothing if the master can never take it again. The dead
     bus is brought BACK - with the answer the bridge abandoned still owed by
     the memory - and the same bridge, with no reset and nothing poked, has to
     transact again. That is the poison flag's own documented contract, from
     the descriptor bridge's comment in milan_soc.py: poisoned, the bus state
     still drives cyc/stb, "and that is the only way the flag can clear".
  3. STRUCTURAL. milan_soc.py is parsed and every bus state of both real FSMs
     is required to carry a non-`ack` exit, so the model above cannot drift
     away from the code it stands for, and to be unable to strand its own
     poison flag.
  4. PRECEDENCE, which is the invariant the whole design intent rests on and
     which nothing guarded until 2026-08-13: the bridge's watchdog must expire
     STRICTLY BEFORE the processor's own per-beat watchdog
     (DESC_MEM_TMO_CYC_P), or the submodule records "no progress" where the
     truth is a failed bus and the bridge's report is never the one that
     lands. The two counters are in DIFFERENT CLOCK DOMAINS, so this is a race
     in TIME and not a comparison of two integers - a bare cycle constant
     satisfies it only by accident of the clock pair the build happens to use.
  5. DIAGNOSABLE, and that is a claim about the INSTRUMENT, not about the fix.
     Failing safely where nothing can see it is what cost the week: on the
     board, "the bridge never issued a read" and "the bridge issued one and was
     never answered" both read as img_valid = 0 and ENTITY_MISBEHAVING, and
     they have completely different causes. The counters that separate them are
     the REAL `_PPMemDiag` imported out of milan_soc.py - not a copy of it -
     driven by the model bridge above and graded against what the MEMORY MODEL
     itself served, never against the DUT's own arithmetic.

Run: cd sw/litex && python3 test_pp_mem_bridge.py
"""

import importlib.util
import sys
from collections.abc import Callable, Generator
from typing import Any

from migen import *

# The parsed half of this evidence, and the tally both halves count into.
# Every path named below is a Path and it is defined there: this file
# builds none of its own.
from pp_mem_bridge_sources import (
    HERE,
    PP_TOP_SV,
    TALLY,
    check,
    proc_watchdog_from_rtl,
    test_counter_wiring,
    test_structural,
)

TMO = 32                       # the model's watchdog; the SoC derives its own

#: One response beat as the EMIT state presents it: (data, err, blast).
Beat = tuple[int, int, int]

#: What a migen stimulus process is: it yields signal reads and `.eq()` writes
#: to the simulator and is sent back whatever a read resolved to, so neither
#: side of the exchange has one type.
Stim = Generator[Any, Any, None]

# Two different words, so a beat can say WHICH answer it carried: the one a
# healthy memory returns, and the one the abandoned access is still owed.
FRESH      = 0x01000100494D4541
FRESH_WIRE = 0x41454D4900010001   # FRESH in 1722.1 wire order (byte-reversed)
STALE      = 0x0BADF00D0BADF00D


class ReadBridge(Module):
    """The descriptor-image read FSM, in both shapes.

    `watchdog=False` reproduces the FSM as it stood in the flashed bitstream -
    the bus state exits on `ack` and on nothing else. `watchdog=True` is the
    shipping shape. The request/emit structure, the handshakes and the byte
    reversal are identical between the two, so the ONLY variable is the arm
    under test.
    """

    def __init__(self, watchdog, tmo=TMO):
        self.req_valid = Signal()
        self.req_addr  = Signal(32)
        self.req_beats = Signal(9)
        self.rsp_valid = Signal()
        self.rsp_err   = Signal()
        self.rsp_blast = Signal()
        self.rsp_data  = Signal(64)
        self.wb_cyc = Signal(); self.wb_stb = Signal()
        self.wb_ack = Signal(); self.wb_err = Signal()
        self.wb_adr = Signal(29); self.wb_dat_r = Signal(64)

        _da = Signal(32); _dl = Signal(9); _dd = Signal(64); _de = Signal()
        _dto = Signal(max=tmo + 1)
        # `psn_set` is exposed because it is the watchdog-fire pulse the real
        # observer counts (milan_soc.py wires the same signal into _PPMemDiag);
        # on the pre-fix shape below nothing drives it, which is the truth.
        self.psn = _dpsn = Signal(); self.psn_set = _dpsn_set = Signal()
        self.sync += If(_dpsn_set, _dpsn.eq(1)
                     ).Elif(_dpsn & (self.wb_ack | self.wb_err), _dpsn.eq(0))
        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            If(self.req_valid,
                NextValue(_da, self.req_addr), NextValue(_dl, self.req_beats),
                NextValue(_de, _dpsn if watchdog else 0), NextValue(_dto, 0),
                NextState("RD")))
        rd = [
            self.wb_cyc.eq(1), self.wb_stb.eq(1), self.wb_adr.eq(_da[3:]),
            NextValue(_dto, _dto + 1),
            If(self.wb_ack,
                NextValue(_dto, 0),
                If(self.wb_err, NextValue(_de, 1)
                ).Else(NextValue(_dd, self.wb_dat_r)),
                NextState("EMIT")),
        ]
        if watchdog:
            # POISONED, THE BUS IS STILL DRIVEN. `_de` marks the transaction
            # `err` so the answer it collects is discarded, and driving cyc/stb
            # is what lets that answer reach the master it is owed to.
            rd.append(If(~self.wb_ack & (_dto == tmo),
                NextValue(_dto, 0), NextValue(_de, 1),
                _dpsn_set.eq(1), NextState("EMIT")))
        fsm.act("RD", *rd)
        fsm.act("EMIT",
            self.rsp_valid.eq(1), self.rsp_err.eq(_de),
            self.rsp_blast.eq((_dl == 1) | _de),
            self.rsp_data.eq(Cat(_dd[56:64], _dd[48:56], _dd[40:48],
                                 _dd[32:40], _dd[24:32], _dd[16:24],
                                 _dd[8:16], _dd[0:8])),
            If(_de | (_dl == 1), NextState("IDLE")
            ).Else(NextValue(_da, _da + 8), NextValue(_dl, _dl - 1),
                   NextValue(_dto, 0), NextState("RD")))


def drive(dut: ReadBridge, dead_after: int,
          cycles: int = 400) -> dict[str, list[Beat] | int]:
    """One 2-beat burst. `dead_after` bus accesses, the memory stops acking."""
    out = {"beats": [], "cyc_at_end": 0, "acks": 0}

    def stim() -> Stim:
        """The memory: it answers the first `dead_after` accesses and then goes
        silent, while every beat the bridge emits is collected as it appears."""
        yield dut.req_addr.eq(0x7F700000)
        yield dut.req_beats.eq(2)
        yield dut.req_valid.eq(1)
        yield
        yield dut.req_valid.eq(0)
        served = 0
        for _ in range(cycles):
            if (yield dut.wb_cyc) and (yield dut.wb_stb):
                if served < dead_after:
                    served += 1
                    out["acks"] += 1
                    yield dut.wb_ack.eq(1)
                    yield dut.wb_dat_r.eq(0x0100010049_4D4541)
                    yield
                    yield dut.wb_ack.eq(0)
                    continue
            if (yield dut.rsp_valid):
                out["beats"].append(((yield dut.rsp_data),
                                     (yield dut.rsp_err),
                                     (yield dut.rsp_blast)))
            yield
        out["cyc_at_end"] = (yield dut.wb_cyc)
        out["psn"] = (yield dut.psn)

    run_simulation(dut, stim())
    return out


def test_behavioural() -> None:
    """Claim 1: the watchdog is free on a healthy bus and decisive on a dead
    one. Both FSM shapes take the same stimulus, so an inert watchdog shows up
    as the two agreeing rather than as a check nobody wrote."""
    # a healthy bus: both shapes must be identical, or the watchdog is not
    # free and the fix costs correctness on the path that already worked
    pre_ok = drive(ReadBridge(False), dead_after=99)
    fix_ok = drive(ReadBridge(True),  dead_after=99)
    check("healthy bus: the burst delivers 2 beats", len(fix_ok["beats"]) >= 2,
          f"got {len(fix_ok['beats'])}")
    check("healthy bus: no beat carries err",
          all(b[1] == 0 for b in fix_ok["beats"]))
    check("healthy bus: the beat is the wire-order byte reversal",
          fix_ok["beats"] and fix_ok["beats"][0][0] == 0x41454D4900010001,
          f"got {hex(fix_ok['beats'][0][0]) if fix_ok['beats'] else None}")
    check("healthy bus: the watchdog changes NOTHING that worked",
          [b[:2] for b in pre_ok["beats"]] == [b[:2] for b in fix_ok["beats"]],
          f"{pre_ok['beats']} vs {fix_ok['beats']}")

    # the defect: the memory answers the first access and then goes silent
    pre = drive(ReadBridge(False), dead_after=1)
    fix = drive(ReadBridge(True),  dead_after=1)

    check("pre-fix FSM gives NO answer to the unacked access",
          len(pre["beats"]) == 0 or all(b[1] == 0 for b in pre["beats"])
          and len(pre["beats"]) < 2,
          f"got {pre['beats']}")
    check("pre-fix FSM is STILL holding the bus at the end (the wedge)",
          pre["cyc_at_end"] == 1, f"cyc={pre['cyc_at_end']}")

    check("watchdog FSM answers the unacked access", len(fix["beats"]) >= 1,
          f"got {fix['beats']}")
    check("watchdog FSM reports it as err", any(b[1] == 1 for b in fix["beats"]))
    check("watchdog FSM ends the burst on that beat",
          any(b[1] == 1 and b[2] == 1 for b in fix["beats"]))
    # NOT "the arbiter is freed", and the 2026-08-14 board round is why the
    # name changed: this model's memory IS the bus, so ending the wishbone
    # cycle looks like releasing it. On the real chain it is not - the AXI
    # transaction the converter already launched cannot be retracted, and the
    # shared read grant stays frozen behind it. That claim needs the real
    # arbiter in the simulation and lives in test_pp_boot_bus_freeze.py.
    check("watchdog FSM ends the WISHBONE cycle it abandoned",
          fix["cyc_at_end"] == 0, f"cyc={fix['cyc_at_end']}")
    check("watchdog FSM marks the master poisoned (a stale ack is still owed)",
          fix["psn"] == 1, f"psn={fix['psn']}")
    check("the watchdog changes behaviour (the fix is not a no-op)",
          pre["cyc_at_end"] != fix["cyc_at_end"])


def drive_recovery(dut: ReadBridge, tries: int = 4, budget: int = 8 * TMO
                   ) -> dict[str, list[Beat] | list[list[Beat]] | int]:
    """A dead bus, then a HEALTHY one, with no reset anywhere in between.

    THE MEMORY MODEL OBEYS ONE RULE and the test means nothing without it:
    `ack` reaches a master ONLY while that master is driving cyc/stb. That is
    what the interconnect does - litex/soc/interconnect/wishbone.py's Arbiter
    gates every slave->master signal as `dest.eq(source & (rr.grant == i))`
    and drives `rr.request` from the masters' own `cyc` - so an answer that
    arrives after a master has let go is delivered to whoever holds the bus
    then, never to the master that abandoned it. A model free to ack an idle
    master would clear the poison flag by magic and prove nothing.

    The abandoned access is modelled as an answer the memory still OWES: the
    first access it serves after coming back carries the OLD access's data
    (STALE), which is the exact hazard the poison flag exists to cover.
    """
    out = {"dead": [], "later": [], "acc": 0,
           "psn_dead": 0, "cyc_dead": 0, "psn_end": 0}
    st = {"alive": False, "owed": False, "acc": 0}
    beats = []

    def step() -> Stim:
        """One simulation cycle of the memory: collect any beat, retire an ack
        it already gave, and answer at most one access per cycle."""
        # EMIT is one cycle wide and this face has no backpressure, so a beat
        # not sampled here is a beat lost
        if (yield dut.rsp_valid):
            beats.append(((yield dut.rsp_data), (yield dut.rsp_err),
                          (yield dut.rsp_blast)))
        if (yield dut.wb_ack):
            yield dut.wb_ack.eq(0)          # one ack per access, never two
        elif st["alive"] and (yield dut.wb_cyc) and (yield dut.wb_stb):
            st["acc"] += 1
            yield dut.wb_dat_r.eq(STALE if st["owed"] else FRESH)
            yield dut.wb_ack.eq(1)
            st["owed"] = False
        yield

    def burst(addr: int) -> Generator[Any, Any, list[Beat]]:
        """One 2-beat request at `addr`, run until its blast beat or `budget`
        cycles, and the beats it produced."""
        del beats[:]
        yield dut.req_addr.eq(addr)
        yield dut.req_beats.eq(2)
        yield dut.req_valid.eq(1)
        yield from step()
        yield dut.req_valid.eq(0)
        for _ in range(budget):
            yield from step()
            if beats and beats[-1][2]:      # blast: the burst is answered
                break
        for _ in range(2):                  # let the FSM settle back in IDLE
            yield from step()
        return list(beats)

    def stim() -> Stim:
        """Dead bus, then a live one that still owes the abandoned answer, with
        no reset and nothing poked into the bridge in between."""
        # 1. the memory stops answering
        out["dead"] = yield from burst(0x7F700000)
        out["psn_dead"] = (yield dut.psn)
        out["cyc_dead"] = (yield dut.wb_cyc)
        # 2. the bus comes back, and it still owes the abandoned answer.
        #    Nothing else changes: no reset, no poke into the bridge.
        st.update(alive=True, owed=True, acc=0)
        # 3. the bridge has to come back on its own
        for n in range(tries):
            out["later"].append((yield from burst(0x7F700000 + 64 * (n + 1))))
        out["acc"] = st["acc"]
        out["psn_end"] = (yield dut.psn)

    run_simulation(dut, stim())
    return out


def test_recovery() -> None:
    """The poison flag has to be able to clear, and only the bus can clear it.

    A master that answers `err` without asserting cyc/stb is asking the bus
    for nothing, so no ack can reach it (see drive_recovery for why the model
    may not hand one to an idle master), so a flag whose only clear is an ack
    stays set for the life of the bitstream. The processor then sees every
    descriptor read fail forever after ONE slow access, which is not a stall
    the board can be talked out of: it is a reset.
    """
    r = drive_recovery(ReadBridge(True))

    # the premise. Without a real timeout there is nothing to recover FROM
    check("dead bus: the burst is answered with err (the timeout reports)",
          bool(r["dead"]) and any(b[1] == 1 for b in r["dead"]),
          f"got {r['dead']}")
    check("dead bus: the master ends up poisoned and off the bus",
          r["psn_dead"] == 1 and r["cyc_dead"] == 0,
          f"psn={r['psn_dead']} cyc={r['cyc_dead']}")

    # the contract
    check("recovered bus: the bridge asks the bus for something again",
          r["acc"] > 0,
          f"no cyc/stb in {len(r['later'])} later bursts: the master never "
          "transacts again, so the ack that would clear its poison flag can "
          "never arrive")
    check("recovered bus: the poison flag clears, with no reset",
          r["psn_end"] == 0, f"psn={r['psn_end']}")
    last = r["later"][-1]
    check("recovered bus: a later burst completes, 2 beats and no err",
          len(last) == 2 and all(b[1] == 0 for b in last), f"got {last}")
    check("recovered bus: the completed burst carries the fresh word, not the "
          "abandoned one",
          bool(last) and all(b[0] == FRESH_WIRE for b in last),
          f"got {[hex(b[0]) for b in last]}")


# ---------------------------------------------------------------------------
#  4. PRECEDENCE
# ---------------------------------------------------------------------------
# Every shape this tree actually builds. The pair matters, not either value:
# the bridge counts sys cycles and the processor counts milan_clk cycles, so
# the relation is a race in TIME and a build that changes one clock can invert
# it. ax7101 from sweep.sh:41 (--milan-clk-freq 100e6, --sys-clk-freq default
# 100e6); arty from sweep.sh:40; the 112.5 MHz floorplan build is the shape the
# perf campaign closed timing on and is kept here because it is the one pair in
# the tree's history where the two clocks DIFFER on the AX.
SHAPES = [
    ("ax7101 shipping", 100e6,    100e6),
    ("arty shipping",    83.333e6, 50e6),
    ("ax7101 fp 112.5", 112.5e6,  100e6),
]


def proc_deadline_cycles(proc_tmo: int, sys_hz: float, milan_hz: float) -> int:
    """The sys cycle on which the PROCESSOR's watchdog expires.

    Independent arithmetic, from the submodule's semantics and not from
    milan_soc.py: KL_aecp_desc_store.sv:500 adds one every milan_clk cycle in
    which a request of its own is outstanding and no beat has arrived, and
    :495 clears it on a beat. So it fires after `proc_tmo` milan_clk periods,
    i.e. at the first sys cycle c with c/sys_hz >= proc_tmo/milan_hz.
    """
    return -(-proc_tmo * int(sys_hz) // int(milan_hz))


def race(tmo: int, proc_deadline: int) -> int | None:
    """Run the shipping bridge into a bus that never answers; report both fires.

    The processor's counter STARTS EARLIER than the bridge's - on `mreq_valid_r`
    (KL_aecp_desc_store.sv:500), before the request has crossed the CDC into the
    sys domain - so it is started here at cycle 0 while the bridge's starts when
    its FSM first drives the bus, which is what the hardware does and is the
    pessimistic direction for the claim under test.
    """
    out = {"bridge": None}

    def stim() -> Stim:
        """A bus that never answers, run one cycle past the processor's
        deadline so a bridge that reports too late reads as a loss."""
        yield dut.req_addr.eq(0x7F700000)
        yield dut.req_beats.eq(2)
        yield dut.req_valid.eq(1)
        yield
        yield dut.req_valid.eq(0)
        # one cycle past the processor's deadline: if the bridge has not
        # reported by then it has LOST the race, and the run must not stop
        # early or a loss would read as a pass
        for c in range(1, proc_deadline + 2):
            if out["bridge"] is None and (yield dut.rsp_valid) and (yield dut.rsp_err):
                out["bridge"] = c
            yield

    dut = ReadBridge(True, tmo=tmo)
    run_simulation(dut, stim())
    return out["bridge"]


def test_precedence() -> None:
    """The bridge must report BEFORE the processor gives up. Nothing guarded it.

    Three claims, and they fail for different reasons on purpose:
      * the mirror of DESC_MEM_TMO_CYC_P still matches the processor's RTL;
      * for every shape the tree builds, the derived watchdog expires strictly
        earlier IN NANOSECONDS, with the margin stated rather than assumed;
      * and it expires later than the worst-case protocol-memory wait, so a
        healthy bus under peer-bridge load is not timed out. A watchdog can only fail in those two
        directions and this pins both ends of it.
    """
    sys.path.insert(0, str(HERE))
    import milan_soc

    rtl = proc_watchdog_from_rtl()
    check("the processor's DESC_MEM_TMO_CYC_P is readable from its own RTL",
          rtl is not None, f"not found in {PP_TOP_SV}")
    check("milan_soc.py's mirror of it has not drifted",
          rtl == milan_soc.PP_PROC_MEM_TMO_CYC,
          f"RTL says {rtl}, milan_soc.py says {milan_soc.PP_PROC_MEM_TMO_CYC}")
    proc_tmo = rtl or milan_soc.PP_PROC_MEM_TMO_CYC

    for name, sys_hz, milan_hz in SHAPES:
        tmo   = milan_soc.pp_mem_timeout_cycles(sys_hz, milan_hz)
        worst = milan_soc.pp_mem_bus_worst_cycles(sys_hz)
        # in nanoseconds, because the two counters do not share a clock
        bridge_ns = tmo * 1e9 / sys_hz
        proc_ns   = proc_tmo * 1e9 / milan_hz
        check(f"{name}: the bridge watchdog expires before the processor's "
              f"({bridge_ns:.0f} ns vs {proc_ns:.0f} ns)",
              bridge_ns < proc_ns,
              "the processor's per-beat watchdog wins the race, so it records "
              "no-progress where the truth is a failed bus")
        check(f"{name}: the bridge leaves the processor real headroom",
              proc_ns - bridge_ns >= proc_ns / 8,
              f"only {proc_ns - bridge_ns:.1f} ns of the processor's budget "
              "is left for the response CDC and its own reaction")
        check(f"{name}: the watchdog clears the worst-case memory-port wait "
              f"({tmo} vs {worst} sys cycles)",
              tmo > worst,
              "a healthy bus under peer-bridge load would time out spuriously")

        # ... and the same claim as a RACE, not as arithmetic. The bridge model
        # runs at the REAL derived timeout into a bus that never answers.
        deadline = proc_deadline_cycles(proc_tmo, sys_hz, milan_hz)
        fired = race(tmo, deadline)
        check(f"{name}: on a dead bus the bridge's err beat lands first "
              f"(cycle {fired} of {deadline})",
              fired is not None and fired < deadline,
              f"bridge fired at {fired}, processor deadline {deadline}")

    # THE GUARD ITSELF. A clock pair whose derived watchdog falls inside the
    # current bus-wait floor (137 cycles with the three masters of
    # PP_MEM_MASTERS) must be REFUSED at elaboration, not built. At sys=100 MHz
    # the 3/4 processor budget crosses that floor above about 2.2 GHz.
    for sys_hz, milan_hz in ((100e6, 3.4e9), (100e6, 4.0e9)):
        try:
            got = milan_soc.pp_mem_timeout_cycles(sys_hz, milan_hz)
        except RuntimeError:
            got = None
        check(f"a build with milan {milan_hz/1e6:g} MHz against sys "
              f"{sys_hz/1e6:g} MHz is refused, not silently narrowed",
              got is None, f"elaboration returned {got}")


# ---------------------------------------------------------------------------
#  5. DIAGNOSABLE  -  the counters
# ---------------------------------------------------------------------------
# Everything below drives the REAL `_PPMemDiag` out of milan_soc.py. A model of
# the counters would prove only that two copies of the same idea agree, and the
# claim being made is about the register a person reads at 3am.


class _BusFace:
    """The four wishbone fields the observer reads, presented off loose signals.

    `_PPMemDiag` takes the bridges' `wishbone.Interface`; the model bridge above
    drives individual signals. This adapts them and adds NO behaviour: an
    observer that starts reading a fifth field raises AttributeError here rather
    than passing quietly on a stale adapter.
    """

    def __init__(self, cyc, stb, ack, err):
        self.cyc, self.stb, self.ack, self.err = cyc, stb, ack, err


def _milan_soc():
    """The real SoC module: the counters under test are ITS code, not a copy."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import milan_soc
    return milan_soc


class Counted(Module):
    """The shipping read bridge with the real observer watching its bus."""

    def __init__(self):
        self.submodules.br = br = ReadBridge(True)
        self.submodules.diag = _milan_soc()._PPMemDiag(
            [("desc", _BusFace(br.wb_cyc, br.wb_stb, br.wb_ack, br.wb_err),
              br.psn, br.psn_set)])


def _snap(dut):
    """The three CSR words, decoded the way the register map documents them."""
    req = yield dut.diag.desc_req.status
    flt = yield dut.diag.desc_fault.status
    st  = yield dut.diag.stat.status
    return {"issued": req >> 16, "acked": req & 0xFFFF,
            "errored": flt >> 16, "timed_out": flt & 0xFFFF,
            "poisoned": st & 1, "on_bus": (st >> 1) & 1, "tag": st >> 24}


def counted_run(policy: Callable[[int], str], cycles: int, peek: int | None = None,
                beats: int = 2,
                request: bool = True) -> dict[str, int | dict[str, int] | None]:
    """One burst against a memory whose behaviour `policy(n)` decides.

    `policy` returns "ack", "err" or "hang" for the n-th access the memory is
    offered. The memory model keeps its OWN tally of what it served, and that
    tally - not the DUT's registers, and not a re-implementation of them - is
    what the counters are graded against.

    `peek` snapshots the counters at that cycle, which is how the case with no
    other symptom (issued, never answered, watchdog not yet expired) is caught
    while it still exists.
    """
    dut = Counted()
    out = {"served": 0, "sv_ack": 0, "sv_err": 0, "peek": None, "end": None}

    def stim() -> Stim:
        """Drive the burst if one was asked for, then serve the memory by
        `policy` and keep the tally of what it actually served."""
        if request:
            yield dut.br.req_addr.eq(0x7F700000)
            yield dut.br.req_beats.eq(beats)
            yield dut.br.req_valid.eq(1)
            yield
            yield dut.br.req_valid.eq(0)
        n = 0
        for c in range(cycles):
            if (yield dut.br.wb_ack):
                yield dut.br.wb_ack.eq(0)      # one ack per access, never two
                yield dut.br.wb_err.eq(0)
            elif (yield dut.br.wb_cyc) and (yield dut.br.wb_stb):
                what = policy(n)
                if what != "hang":
                    n += 1
                    out["served"] += 1
                    yield dut.br.wb_dat_r.eq(FRESH)
                    yield dut.br.wb_ack.eq(1)
                    if what == "err":
                        out["sv_err"] += 1
                        yield dut.br.wb_err.eq(1)   # LiteX raises err WITH ack
                    else:
                        out["sv_ack"] += 1
            if peek is not None and c == peek:
                out["peek"] = yield from _snap(dut)
            yield
        out["end"] = yield from _snap(dut)

    run_simulation(dut, stim())
    return out


def test_counters() -> None:
    """Each counter counts the thing it claims, and the two causes separate."""
    # ---- a healthy burst: every access answered ---------------------------
    ok = counted_run(lambda n: "ack", cycles=60)
    e = ok["end"]
    check("healthy bus: ISSUED equals the accesses the memory saw",
          e["issued"] == ok["served"] == 2,
          f"issued {e['issued']}, memory served {ok['served']}")
    check("healthy bus: ACKED equals the accesses the memory acked",
          e["acked"] == ok["sv_ack"] == 2, f"acked {e['acked']}")
    check("healthy bus: no fault is counted",
          (e["errored"], e["timed_out"], e["poisoned"]) == (0, 0, 0), f"{e}")

    # ---- an errored answer: ack and err in the same cycle ------------------
    er = counted_run(lambda n: "err", cycles=60)
    e = er["end"]
    check("errored answer: ERRORED counts it",
          e["errored"] == er["sv_err"] == 1, f"errored {e['errored']}")
    check("errored answer: it is NOT counted as acked", e["acked"] == 0,
          f"acked {e['acked']} (an ack-only test would count a failed access)")
    check("errored answer: the watchdog did not fire", e["timed_out"] == 0)

    # ---- THE DISCRIMINATOR -------------------------------------------------
    # A memory that takes the request and never answers. Peeked INSIDE the
    # watchdog window, this is the reading that did not exist on 2026-08-13.
    hung = counted_run(lambda n: "hang", cycles=4 * TMO, peek=TMO // 2)
    mid, e = hung["peek"], hung["end"]
    check("unanswered access, watchdog still running: ISSUED > 0",
          mid["issued"] == 1, f"issued {mid['issued']}")
    check("unanswered access, watchdog still running: ACKED == 0",
          mid["acked"] == 0, f"acked {mid['acked']}")
    check("unanswered access, watchdog still running: no fault counted YET "
          "(so the reading is 'outstanding', not 'failed')",
          (mid["errored"], mid["timed_out"]) == (0, 0), f"{mid}")
    check("unanswered access: the live flag says it is ON THE BUS right now",
          mid["on_bus"] == 1, f"stat {mid}")
    check("the hung access is counted ONCE, not once per held cycle",
          e["issued"] == 1,
          f"issued {e['issued']} after {4 * TMO} cycles of held cyc/stb")
    check("after the watchdog: TIMED OUT counts it", e["timed_out"] == 1,
          f"timed_out {e['timed_out']}")
    check("after the watchdog: it is not miscounted as an err answer",
          e["errored"] == 0, f"errored {e['errored']}")
    check("after the watchdog: POISONED is live and set, and the bus is let go",
          (e["poisoned"], e["on_bus"]) == (1, 0), f"stat {e}")

    # the other cause of the same board symptom
    idle = counted_run(lambda n: "ack", cycles=60, request=False)
    i = idle["end"]
    check("never issued: every counter reads 0",
          (i["issued"], i["acked"], i["errored"], i["timed_out"]) == (0, 0, 0, 0),
          f"{i}")
    check("never issued: the block still identifies itself, so 0 is a "
          "MEASUREMENT and not an absent register",
          i["tag"] == 0x5B, f"tag 0x{i['tag']:02x}")
    # ...and the whole point: the two are different readings
    check("'never issued' and 'issued, never answered' are DISTINGUISHABLE",
          (i["issued"], i["on_bus"]) != (mid["issued"], mid["on_bus"]),
          f"idle {i} vs unanswered {mid}")

    # ---- the memory dies mid-burst, which is what the board did ------------
    half = counted_run(lambda n: "ack" if n < 1 else "hang", cycles=4 * TMO)
    e = half["end"]
    check("bus dies mid-burst: ISSUED counts both accesses",
          e["issued"] == 2, f"issued {e['issued']}")
    check("bus dies mid-burst: ACKED counts only the one that was answered",
          e["acked"] == half["sv_ack"] == 1, f"acked {e['acked']}")
    check("bus dies mid-burst: TIMED OUT counts the one that was not",
          e["timed_out"] == 1, f"timed_out {e['timed_out']}")


class Bare(Module):
    """The observer with no bridge at all: every input driven by the test."""

    def __init__(self):
        self.cyc = Signal(); self.stb = Signal()
        self.ack = Signal(); self.err = Signal()
        self.psn = Signal(); self.pset = Signal()
        self.submodules.diag = _milan_soc()._PPMemDiag(
            [("desc", _BusFace(self.cyc, self.stb, self.ack, self.err),
              self.psn, self.pset)])


def test_counter_gating() -> None:
    """An answer that lands while this master is asking for nothing is NOT ours.

    Each memory client owns its converter, so
    the answer owed to an access the watchdog abandoned can arrive after the FSM
    has let go of the bus (which is why milan_soc.py watches the poison flag's
    clear in EVERY state, not from the bus state's arm). Counting that as an ACK
    would make `issued - acked` - the arithmetic the whole block is read by -
    report an outstanding access as settled.
    """
    dut = Bare()
    seen = {}

    def stim() -> Stim:
        """Answer a master that is asking for nothing, then let it ask and be
        answered, snapshotting the counters after each."""
        yield dut.ack.eq(1)               # the bus answers, nobody is asking
        for _ in range(4):
            yield
        yield dut.err.eq(1)
        for _ in range(4):
            yield
        yield dut.ack.eq(0)
        yield dut.err.eq(0)
        yield
        seen["stray"] = yield from _snap(dut)
        yield dut.cyc.eq(1)               # now this master asks, and is answered
        yield dut.stb.eq(1)
        yield
        yield dut.ack.eq(1)
        yield
        yield dut.ack.eq(0)
        yield dut.cyc.eq(0)
        yield dut.stb.eq(0)
        yield
        yield
        seen["own"] = yield from _snap(dut)

    run_simulation(dut, stim())
    s, o = seen["stray"], seen["own"]
    check("an ack with this master off the bus counts nothing",
          (s["issued"], s["acked"], s["errored"]) == (0, 0, 0), f"{s}")
    check("its own access is still counted, issued and acked",
          (o["issued"], o["acked"]) == (1, 1), f"{o}")


def test_counter_saturation() -> None:
    """0xFFFF means "at least this many". A wrap would read as almost none.

    Driven on the bare observer: 65,600 events is far past the counter's range
    and a wrapping counter would land near 64. The watchdog-fire input is used
    because it is a plain pulse, so the count is exactly the number of cycles
    the stimulus asserts it - an expectation this test owns rather than infers.
    """
    dut = Bare()
    seen = {}

    def stim() -> Stim:
        """Hold the watchdog-fire pulse for 65,600 cycles, reading the count
        once just short of the range and once well past it."""
        yield dut.pset.eq(1)
        for c in range(2**16 + 64):
            if c == 2**16 - 3:            # still short of the range
                seen["before"] = (yield from _snap(dut))["timed_out"]
            yield
        seen["after"] = (yield from _snap(dut))["timed_out"]

    run_simulation(dut, stim())
    check("the counter reaches its full range (not truncated early)",
          seen["before"] == 2**16 - 4, f"got {seen['before']}")
    check("past the range it SATURATES at 0xFFFF rather than wrapping",
          seen["after"] == 0xFFFF,
          f"got {seen['after']} - a wrapped counter reads as 'almost none'")


class TwoFaced(Module):
    """The observer as milan_soc.py really builds it: BOTH bridges, no FSM.

    Everything else in this file drives ONE face, so nothing else can see the
    second one at all: a block that summed both bridges into one set of counters,
    or that packed the response face's live bits at the wrong offset, would pass
    every check above and still misdirect the person reading it at 3am - to the
    descriptor bridge when the response bridge is the one that died.
    """

    def __init__(self):
        self.f = []
        faces = []
        for tag in ("desc", "resp"):
            sig = {n: Signal() for n in
                   ("cyc", "stb", "ack", "err", "psn", "pset")}
            self.f.append(sig)
            faces.append((tag, _BusFace(sig["cyc"], sig["stb"],
                                        sig["ack"], sig["err"]),
                          sig["psn"], sig["pset"]))
        self.submodules.diag = _milan_soc()._PPMemDiag(faces)


def _snap2(dut):
    """Both faces, decoded at the offsets and bit positions the map publishes.

    `resp` is read out of ITS OWN registers (+0x08 / +0x0C) and out of stat bits
    2 and 3, which is the claim under test - not re-derived from the desc face.
    """
    dreq = yield dut.diag.desc_req.status
    dflt = yield dut.diag.desc_fault.status
    rreq = yield dut.diag.resp_req.status
    rflt = yield dut.diag.resp_fault.status
    st = yield dut.diag.stat.status

    def face(req: int, flt: int, psn_bit: int, on_bit: int) -> dict[str, int]:
        """One bridge's reading, taken from ITS registers and ITS stat bits."""
        return {"issued": req >> 16, "acked": req & 0xFFFF,
                "errored": flt >> 16, "timed_out": flt & 0xFFFF,
                "poisoned": (st >> psn_bit) & 1, "on_bus": (st >> on_bit) & 1}

    return {"desc": face(dreq, dflt, 0, 1), "resp": face(rreq, rflt, 2, 3),
            "tag": st >> 24}


def test_two_faces() -> None:
    """Each bridge is counted SEPARATELY, and at the documented bit positions.

    The register map's whole promise is that a reading names WHICH bridge is
    stuck. Drive one face and the other must stay at rest, in both directions:
    the descriptor bridge's traffic must not appear in `resp_req`, and the
    response bridge's poison must not light `stat[0]`.
    """
    dut = TwoFaced()
    seen = {}

    def one(i: int) -> Stim:
        """One issued-and-acked access plus one watchdog fire, on face `i`."""
        yield dut.f[i]["cyc"].eq(1)
        yield dut.f[i]["stb"].eq(1)
        yield
        yield dut.f[i]["ack"].eq(1)
        yield
        yield dut.f[i]["ack"].eq(0)
        yield dut.f[i]["cyc"].eq(0)
        yield dut.f[i]["stb"].eq(0)
        yield
        yield dut.f[i]["pset"].eq(1)     # the watchdog fires
        yield dut.f[i]["psn"].eq(1)      # and the master is poisoned
        yield
        yield dut.f[i]["pset"].eq(0)
        yield
        yield

    def hold(i: int) -> Generator[Any, Any, int]:
        """Park face `i` on the bus and read `stat` WHILE it is still there.

        `one()` above lets go of cyc/stb before it snapshots, so every reading
        it takes has both live on-bus bits at 0 - which means it cannot see them
        transposed. Measured 2026-08-13: swapping stat[1] with stat[3] left all
        87 checks green while the verdict table's "which face is still holding
        cyc/stb" row named the wrong bridge, i.e. it misdirects at exactly the
        moment the bank exists for. The poison bits latch and are covered; these
        two are combinational on cyc&stb and only exist mid-access.
        """
        yield dut.f[i]["cyc"].eq(1)
        yield dut.f[i]["stb"].eq(1)
        yield
        yield
        st = yield dut.diag.stat.status
        yield dut.f[i]["cyc"].eq(0)
        yield dut.f[i]["stb"].eq(0)
        yield
        return st

    def stim() -> Stim:
        """Exercise each face alone, then park each on the bus in turn so the
        live on-bus bits are read while they can actually be set."""
        yield from one(0)                # the DESCRIPTOR bridge only
        seen["desc_only"] = yield from _snap2(dut)
        yield dut.f[0]["psn"].eq(0)      # its debt is settled
        yield
        yield from one(1)                # now the RESPONSE bridge only
        seen["resp_too"] = yield from _snap2(dut)
        seen["d_live"] = yield from hold(0)
        seen["r_live"] = yield from hold(1)

    run_simulation(dut, stim())
    d, r = seen["desc_only"], seen["resp_too"]
    check("descriptor traffic lands in the DESCRIPTOR counters",
          (d["desc"]["issued"], d["desc"]["acked"], d["desc"]["timed_out"])
          == (1, 1, 1), f"desc {d['desc']}")
    check("and not one count of it reaches the RESPONSE counters",
          (d["resp"]["issued"], d["resp"]["acked"], d["resp"]["errored"],
           d["resp"]["timed_out"]) == (0, 0, 0, 0),
          f"resp {d['resp']} - the two bridges share a counter")
    check("the descriptor poison flag is stat[0], and stat[2] stays clear",
          (d["desc"]["poisoned"], d["resp"]["poisoned"]) == (1, 0),
          f"desc {d['desc']['poisoned']} resp {d['resp']['poisoned']}")
    check("the response bridge is counted in ITS OWN registers",
          (r["resp"]["issued"], r["resp"]["acked"], r["resp"]["timed_out"])
          == (1, 1, 1), f"resp {r['resp']}")
    check("and the descriptor counters do not move while it runs",
          (r["desc"]["issued"], r["desc"]["acked"], r["desc"]["timed_out"])
          == (1, 1, 1), f"desc {r['desc']} - it was 1/1/1 before resp ran")
    check("the response poison flag is stat[2], the position the map publishes",
          (r["resp"]["poisoned"], r["desc"]["poisoned"]) == (1, 0),
          f"stat resp {r['resp']['poisoned']} desc {r['desc']['poisoned']}")
    check("the tag survives two faces (it is not overwritten by the flags)",
          r["tag"] == 0x5B, f"tag 0x{r['tag']:02x}")
    dl, rl = seen["d_live"], seen["r_live"]
    check("mid-access, the DESCRIPTOR bridge lights stat[1] and not stat[3]",
          ((dl >> 1) & 1, (dl >> 3) & 1) == (1, 0),
          f"stat 0x{dl:08x} - the live on-bus bits are transposed, so the "
          "verdict table's outstanding-right-now row names the wrong bridge")
    check("mid-access, the RESPONSE bridge lights stat[3] and not stat[1]",
          ((rl >> 1) & 1, (rl >> 3) & 1) == (0, 1),
          f"stat 0x{rl:08x} - the live on-bus bits are transposed, so the "
          "verdict table's outstanding-right-now row names the wrong bridge")


if __name__ == "__main__":
    print("test_behavioural:")
    test_behavioural()
    print("test_recovery:")
    test_recovery()
    print("test_precedence:")
    test_precedence()
    print("test_counters:")
    test_counters()
    print("test_counter_gating:")
    test_counter_gating()
    print("test_counter_saturation:")
    test_counter_saturation()
    print("test_two_faces:")
    test_two_faces()
    print("test_counter_wiring:")
    test_counter_wiring()
    print("test_structural:")
    test_structural()
    checks, fails = TALLY["checks"], TALLY["fails"]
    print(f"\ntest_pp_mem_bridge: {checks} checks: "
          f"{checks - fails} PASS, {fails} FAIL")
    print("RESULT:", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)
