#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""The shared dma_bus must not lie to a master, and must not starve one.

KNOWN-FAIL BANNER. This file is a CHARACTERISATION suite and it is RED today,
deliberately. Both defects it grades are open in LiteX (`a1e1c36`), not in this
repo's RTL, and `/home/alex/litex-milan` is read-only to this round. Every red
check prints as [XFAIL] and is named again in the summary; an [XFAIL] that
turns [XPASS] means the defect was fixed upstream and this banner is due for
retirement. That is the same convention `tb/verilator/hostplane` carried from
2026-07-25 until the fix landed on 2026-07-26.

THE SHAPE OF THE MISS THIS FILE ANSWERS. The bus-fault sims next door
(`test_pb_bus_err.py`, `test_pp_mem_bridge.py`) grade what OUR masters do when
the bus misbehaves. Nothing graded the bus itself, so two defects in the
interconnect every one of those masters sits on were never anybody's test.

DEFECT A, THE ARLEN BUG. `AXITimeout` (axi_full.py:1047-1103) gives up after
`timeout_cycles` and its read arm answers with ONE beat carrying `r.last`,
whatever ARLEN said:

    axi_full.py:1096   master.r.valid.eq(~master.ar.valid),
    axi_full.py:1097   master.r.last.eq(1),
    axi_full.py:1098   master.r.resp.eq(RESP_SLVERR),
    axi_full.py:1099   master.r.data.eq(2**len(master.r.data) - 1),

and in the flashed netlist, on the dma_bus handler, exactly that:

    alinx_ax7101.v:12326   socbushandler1_r_last = 1'd1;
    alinx_ax7101.v:12327   socbushandler1_r_payload_resp = 2'd2;
    alinx_ax7101.v:12328   socbushandler1_r_payload_data = 64'hffffffffffffffff;

(build_ax7101_eto_ppbus; `socbushandler1` is the dma_bus, its slave port being
`milansoc_milansoc_vexiiriscv_dma_bus_*`, and `socbushandler1_rr_read_request`
is 8 bits wide, so eight masters share it.) The ring engines read in INCR
bursts - `ar.len` is driven at milan_soc.py:3674, 3795, 3985 and 4054, up to
`burst_beats` = 16 - so a timeout mid-burst tells such a master its burst
finished after one beat. AXI4 (IHI0022 A3.4.1) is not ambiguous here: a read
burst delivers ARLEN+1 transfers and RLAST marks the last of THOSE. Rated a
silent-corruption path: the master is not stalled, it is told a lie it cannot
detect, and the slave may still be holding beats it will deliver later.

DEFECT B, THE ARBITER FREEZE, and this is the one that took the SoC down on
2026-08-13. `AXIArbiter` advances its read grant only when nothing is
outstanding:

    axi_full.py:1188  self.rr_read.ce.eq(~(target.ar.valid | target.r.valid) & rd_lock.ready)
    alinx_ax7101.v:12196  assign socbushandler1_rr_read_ce =
                              ((~(socbushandler1_ar_valid | socbushandler1_r_valid))
                               & socbushandler1_rd_lock_empty);

and responses are steered by GRANT INDEX, never by AXI ID: in the slave->master
loop (axi_full.py:1158-1166) only `valid`/`ready` are qualified by the grant,
while `r.data`, `r.resp`, `r.last` and `r.id` are broadcast to every master. So
the arbiter cannot let a second master's read overtake a first one, and one
master with an accepted-but-unanswered read freezes the READ half for ALL eight
masters. The board's receipt: descriptor-store fault 8 (FAULT_TIMEOUT), response
buffer fault 1 (FAULT_WTMO), image invalid, every AECP command
ENTITY_MISBEHAVING - while `dbg_lane_wr = 2` proved the write half was still
alive, because the write half has its own grant.

WHAT THIS FILE PROVES, and why the red checks are the DUT's fault and not the
harness's:
  * The DUT is the REAL LiteX code. `SharedBus` composes the real `AXIArbiter`,
    `AXIDecoder` and `AXITimeout` in the real order; `test_provenance` pins that
    composition against `AXIInterconnectShared` itself and against the
    `SoCBusHandler` table that picks it for an "axi" bus. No model of the
    interconnect exists here to agree with its bugs.
  * Every failing claim has a CONTROL that passes on the same DUT, the same
    masters and the same slave, with exactly one variable moved. A5 counts the
    beats of a burst that is answered normally, so the beat counting is proved
    live by a green check before A3/A4 use it. B1 runs the identical three-master
    stimulus with master 0's answer prompt, so B3/B4 differ from a passing run by
    the answer delay alone.
  * The slave model completes different AXI IDs OUT OF ORDER, which AXI4 permits
    (IHI0022 A5.3), and B2 proves it does so through this interconnect. Without
    that, an in-order slave would starve the other masters by itself and the
    freeze could be blamed on the model.
  * `_TimeoutBeatCounted` is a candidate fix for defect A's arm, run against the
    same stimulus, so "the requirement is unsatisfiable" is not available as an
    explanation. It is not a model of the DUT: the expectation it is graded
    against comes from AXI4, not from LiteX.

Run: cd sw/litex && python3 test_dma_bus_faults.py   (LiteX venv interpreter)
"""

import ast
import inspect
import os
import sys

from migen import *

from litex.gen.genlib.misc import WaitTimer
from litex.soc.integration import soc as soc_mod
from litex.soc.interconnect.axi import (
    AXSIZE,
    BURST_INCR,
    RESP_SLVERR,
    AXIArbiter,
    AXIDecoder,
    AXIInterconnectShared,
    AXIInterface,
    AXITimeout,
)

DW   = 64        # the dma_bus data width on this board
AWD  = 32
IDW  = 4
SZ   = AXSIZE[DW // 8]
MASK = 2**DW - 1

# The arm is the same one at any size, and 1,000,000 cycles (10 ms at 100 MHz,
# the SoC's default) is not simulable. Every case that must NOT time out is
# checked against this SHORT value, which makes those checks stronger: 24
# cycles is an eighth of the stall in the B cases and the arm still cannot see
# it.
TMO  = 24
ALEN = 3         # a 4-beat INCR burst: the whole point is ARLEN > 0
SLOW = 300       # master 0's answer delay in the freeze case
# The three-master stimulus is 12 beats and three handshakes, so 60 cycles is
# five times what it needs and a fifth of SLOW. The bound is on the CONTROL,
# where every answer is 2 cycles away: it is what makes B1 fail if the control
# is ever handed the freeze case's delays by accident.
SOON = 60

fails  = 0       # unexpected failures: the harness or this repo
xfails = 0       # requirements that are red today: the open LiteX defects
xpass  = 0       # a requirement that went green: retire the banner
checks = 0


def check(name, cond, detail=""):
    """A claim that must hold today."""
    global fails, checks
    checks += 1
    if cond:
        print(f"  [ok]   {name}")
    else:
        fails += 1
        print(f"  [FAIL] {name} {detail}")


def req(name, cond, detail=""):
    """A REQUIREMENT that an open defect breaks. Red today, green when fixed."""
    global xfails, xpass, checks
    checks += 1
    if cond:
        xpass += 1
        print(f"  [XPASS] {name}  <- the defect appears FIXED; retire the banner")
    else:
        xfails += 1
        print(f"  [XFAIL] {name} {detail}")


# --- the DUT ------------------------------------------------------------------

class SharedBus(Module):
    """The dma_bus interconnect, built from the real LiteX parts in real order.

    ORDER IS LOAD-BEARING. Migen lowers the whole design's combinational
    statements into one block, so the timeout's RESPOND arm overrides the
    decoder's slave-driven `ar.ready`/`r.valid` - visible in the flashed
    netlist at alinx_ax7101.v:12317-12328, where the decoder's assignments are
    emitted first and the FSM's case arm re-assigns the same nets. Building the
    three by hand (rather than calling AXIInterconnectShared) is only so the
    timeout can be substituted; test_provenance pins this against the real
    class so the hand build cannot drift.
    """

    def __init__(self, n_masters, timeout_cycles=TMO, timeout_cls=AXITimeout):
        self.masters = [AXIInterface(data_width=DW, address_width=AWD, id_width=IDW)
                        for _ in range(n_masters)]
        self.slave  = AXIInterface(data_width=DW, address_width=AWD, id_width=IDW)
        self.shared = AXIInterface(data_width=DW, address_width=AWD, id_width=IDW)
        self.submodules.arbiter = AXIArbiter(self.masters, self.shared)
        self.submodules.decoder = AXIDecoder(self.shared, [(lambda a: 1, self.slave)])
        self.submodules.timeout = timeout_cls(self.shared, timeout_cycles)


class _TimeoutBeatCounted(Module):
    """A candidate fix for the read arm of AXITimeout. Read half only.

    Here so that "no timeout arm could satisfy A3/A4" is not available as an
    explanation for the red checks. The expectation it is graded against is
    AXI4 IHI0022 A3.4.1 - ARLEN+1 transfers, RLAST on the last of them - not
    anything read out of LiteX. The write arm is untouched by these cases and
    is deliberately not modelled: no case here drives a write channel.
    """

    def __init__(self, master, cycles):
        self.error = Signal()
        rd_error   = Signal()
        self.comb += self.error.eq(rd_error)

        left = Signal(len(master.ar.len))
        rid  = Signal(len(master.r.id))
        self.submodules.rd_timer = rd_timer = WaitTimer(cycles)
        self.submodules.rd_fsm = fsm = FSM(reset_state="WAIT")
        fsm.act("WAIT",
            rd_timer.wait.eq(master.ar.valid & ~master.ar.ready),
            If(rd_timer.done & rd_timer.wait,
                rd_error.eq(1),
                NextState("RESPOND")))
        fsm.act("RESPOND",
            master.ar.ready.eq(master.ar.valid),
            # ARLEN is only knowable at the accept, so it is latched there and
            # counted out; the original arm never looks at it at all.
            If(master.ar.valid,
                NextValue(left, master.ar.len),
                NextValue(rid,  master.ar.id)),
            master.r.valid.eq(~master.ar.valid),
            master.r.id.eq(rid),
            master.r.last.eq(left == 0),
            master.r.resp.eq(RESP_SLVERR),
            master.r.data.eq(2**len(master.r.data) - 1),
            If(master.r.valid & master.r.ready,
                If(left == 0,
                    NextState("WAIT")
                ).Else(
                    NextValue(left, left - 1))))


# --- stimulus -----------------------------------------------------------------
#
# ONE CYCLE DISCIPLINE, shared by every generator below: after `yield; t += 1`
# a read sees cycle `t` and a write is what the design sees in cycle `t + 1`.
# The A6 case calibrates one generator against another and is off by one
# without it.

def word(addr, n):
    """The slave's data, derived from the address it was asked for.

    A beat can therefore never be mistaken for another transaction's, which is
    the whole assertion in A6.
    """
    return ((addr << 8) | n) & MASK


def ar_driver(bus, mid, reqs, rec, cycles):
    """Issue each request in turn on one master's AR channel.

    A request is (addr, arlen, after_bursts, arid): it is presented once
    `after_bursts` bursts have completed on this master's R channel, which is
    how A6 issues its second read only after the first was declared finished.
    `ar.valid` is held until `ar.ready` (AXI4 A3.1.2: a VALID may not be
    retracted before its READY).
    """
    t = 0
    yield bus.r.ready.eq(1)          # a burst master keeps its R channel drained
    for (addr, arlen, after, arid) in reqs:
        while t < cycles and len([b for b in rec["beats"] if b["last"]]) < after:
            yield
            t += 1
        yield bus.ar.addr.eq(addr)
        yield bus.ar.len.eq(arlen)
        yield bus.ar.size.eq(SZ)
        yield bus.ar.burst.eq(BURST_INCR)
        yield bus.ar.id.eq(arid if arid is not None else mid)
        yield bus.ar.valid.eq(1)
        while t < cycles:
            yield
            t += 1
            if (yield bus.ar.ready):
                rec["ar_ack"].append(t)
                break
        yield bus.ar.valid.eq(0)
    while t < cycles:
        yield
        t += 1


def r_collector(bus, rec, cycles):
    """Record every beat this master is shown, with the cycle it arrived in.

    Independent of AR state on purpose: a real burst master holds `r.ready` and
    consumes whatever the interconnect presents. A collector that only listened
    while it believed a read was outstanding would step over exactly the beats
    A6 is about.
    """
    t = 0
    while t < cycles:
        yield
        t += 1
        if (yield bus.r.valid) and (yield bus.r.ready):
            rec["beats"].append({
                "t":    t,
                "data": (yield bus.r.data),
                "resp": (yield bus.r.resp),
                "last": (yield bus.r.last),
                "id":   (yield bus.r.id),
            })


def slave_gen(bus, cfg, rec, cycles):
    """An AXI4 read slave that may complete different IDs OUT OF ORDER.

    AXI4 permits it (IHI0022 A5.3: no ordering is guaranteed between
    transactions of different IDs) and this file needs it. A slave that could
    only answer in order would starve the other masters by itself, and the
    freeze in B3/B4 could be blamed on the model instead of on the arbiter.
    B2 proves the capability is real through this interconnect.

    cfg["ar_from"]  cycle from which AR is accepted at all (None: never)
    cfg["delay"]    per-ARID answer delay in cycles, key "_" is the default
    cfg["depth"]    how many accepted-but-unanswered reads it will hold
    """
    t = 0
    q = []            # accepted, not yet being answered
    live = None       # the burst currently on the R channel
    while t < cycles:
        yield
        t += 1
        # --- observe cycle t
        if (yield bus.ar.valid) and (yield bus.ar.ready):
            e = {"id": (yield bus.ar.id), "addr": (yield bus.ar.addr),
                 "len": (yield bus.ar.len), "at": t, "n": 0}
            e["due"] = t + cfg["delay"].get(e["id"], cfg["delay"]["_"])
            q.append(e)
            rec["accepted"].append((t, e["addr"], e["id"]))
        if live is not None and (yield bus.r.valid) and (yield bus.r.ready):
            live["n"] += 1
            if live["n"] > live["len"]:
                rec["answered"].append((t, live["addr"], live["id"]))
                live = None
        if live is None:
            due = [e for e in q if e["due"] <= t]
            if due:
                live = due[0]
                q.remove(live)
        # --- present cycle t+1
        room  = (len(q) + (0 if live is None else 1)) < cfg.get("depth", 4)
        allow = cfg["ar_from"] is not None and (t + 1) >= cfg["ar_from"]
        yield bus.ar.ready.eq(1 if (room and allow) else 0)
        if live is None:
            yield bus.r.valid.eq(0)
        else:
            yield bus.r.valid.eq(1)
            yield bus.r.data.eq(word(live["addr"], live["n"]))
            yield bus.r.id.eq(live["id"])
            yield bus.r.resp.eq(0)
            yield bus.r.last.eq(1 if live["n"] == live["len"] else 0)


def run(reqs, slave_cfg, timeout_cls=AXITimeout, cycles=520):
    """One case: len(reqs) masters on one shared bus, one slave."""
    dut  = SharedBus(len(reqs), TMO, timeout_cls)
    recs = [{"beats": [], "ar_ack": []} for _ in reqs]
    srec = {"accepted": [], "answered": []}
    gens = [slave_gen(dut.slave, slave_cfg, srec, cycles)]
    for i, m in enumerate(dut.masters):
        gens.append(ar_driver(m, i, reqs[i], recs[i], cycles))
        gens.append(r_collector(m, recs[i], cycles))
    run_simulation(dut, gens)
    return recs, srec


def bursts(rec):
    """Split one master's beats into transactions, at every beat carrying last."""
    out, cur = [], []
    for b in rec["beats"]:
        cur.append(b)
        if b["last"]:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)          # an unterminated tail is a finding, not a burst
    return out


# --- defect A: the timeout answers a burst with one beat ----------------------

def test_defect_a():
    """A timed-out burst read must not be declared finished after one beat."""
    # A5, THE CONTROL, first: the same master, the same 4-beat burst, a slave
    # that answers. Everything A3/A4 assert is counted here on a passing run,
    # so a red A3/A4 cannot be the beat counting being wrong.
    ok, _ = run(reqs=[[(0x1000, ALEN, 0, None)]],
                slave_cfg={"ar_from": 1, "delay": {"_": 2}})
    ok_b = bursts(ok[0])
    check("A5 control: an answered 4-beat burst delivers 4 beats",
          len(ok_b) == 1 and len(ok_b[0]) == ALEN + 1,
          f"got {[len(b) for b in ok_b]}")
    check("A5 control: RLAST marks the 4th beat and no earlier one",
          len(ok_b) == 1 and [b["last"] for b in ok_b[0]] == [0, 0, 0, 1],
          f"got {[b['last'] for b in ok_b[0]] if ok_b else None}")
    check("A5 control: the beats are the slave's own words for that address",
          len(ok_b) == 1 and [b["data"] for b in ok_b[0]]
          == [word(0x1000, n) for n in range(ALEN + 1)],
          f"got {[hex(b['data']) for b in ok_b[0]] if ok_b else None}")

    # THE DEFECT: the slave never accepts the AR, so the timeout answers.
    stall = {"ar_from": None, "delay": {"_": 2}}
    bad, srec = run(reqs=[[(0x1000, ALEN, 0, None)]], slave_cfg=stall)

    # the premise. Without these the case is not exercising the arm at all
    check("A1 the slave never accepted the AR, so the read timeout answered it",
          srec["accepted"] == [] and bad[0]["ar_ack"],
          f"slave saw {srec['accepted']}, master ar_ack {bad[0]['ar_ack']}")
    check("A2 the injected beat is SLVERR with all-ones data (the netlist's shape)",
          bad[0]["beats"] and bad[0]["beats"][0]["resp"] == RESP_SLVERR
          and bad[0]["beats"][0]["data"] == MASK,
          f"got {bad[0]['beats'][:1]}")

    # the requirement, from AXI4 IHI0022 A3.4.1
    req("A3 a timed-out 4-beat read is answered with 4 beats",
        len(bad[0]["beats"]) == ALEN + 1,
        f"got {len(bad[0]['beats'])} beat(s) for ARLEN={ALEN}")
    req("A4 RLAST is not asserted before the 4th beat of that burst",
        len(bad[0]["beats"]) >= ALEN + 1
        and [b["last"] for b in bad[0]["beats"][:ALEN + 1]] == [0, 0, 0, 1],
        f"got last={[b['last'] for b in bad[0]['beats']]}")

    # and the same stimulus against a beat-counting arm, so the requirement is
    # demonstrably satisfiable on this DUT and this harness
    fix, _ = run(reqs=[[(0x1000, ALEN, 0, None)]], slave_cfg=stall,
                 timeout_cls=_TimeoutBeatCounted)
    check("A7 a beat-counting arm answers the same read with 4 SLVERR beats",
          len(fix[0]["beats"]) == ALEN + 1
          and all(b["resp"] == RESP_SLVERR for b in fix[0]["beats"])
          and [b["last"] for b in fix[0]["beats"]] == [0, 0, 0, 1],
          f"got {[(hex(b['data']), b['resp'], b['last']) for b in fix[0]['beats']]}")
    check("A7 the arm is not a no-op: it disagrees with the shipping one",
          len(fix[0]["beats"]) != len(bad[0]["beats"]))


def test_defect_a_abandoned():
    """A6. The timed-out AR the SLAVE also took: whose beats are those?

    The timeout accepts the AR on the master's behalf (`ar.ready.eq(ar.valid)`)
    without any way to withdraw it from the slave, and AXI4 forbids retracting
    a VALID before its READY, so in the cycle the arm fires a slave that
    asserts `ar.ready` takes the same command. Its beats then arrive after the
    master was told the burst was over, and are collected as the NEXT read's
    data. Calibrated rather than guessed: run one probe to find the cycle the
    arm accepts in, then hand the slave that cycle.
    """
    probe, _ = run(reqs=[[(0x1000, ALEN, 0, None)]],
                   slave_cfg={"ar_from": None, "delay": {"_": 2}})
    check("A6 setup: the probe run found the cycle the timeout arm accepts in",
          bool(probe[0]["ar_ack"]), "the arm never fired; A6 below is vacuous")
    if not probe[0]["ar_ack"]:
        return
    t_arm = probe[0]["ar_ack"][0]

    # read 2 is issued only once read 1 has been declared finished
    recs, srec = run(reqs=[[(0x1000, ALEN, 0, None), (0x2000, ALEN, 1, None)]],
                     slave_cfg={"ar_from": t_arm, "delay": {"_": 6}})
    got = bursts(recs[0])
    accepted = [a for a in srec["accepted"] if a[1] == 0x1000]

    check("A6 the slave took the same AR in the cycle the arm answered it",
          bool(accepted) and accepted[0][0] == t_arm,
          f"arm at {t_arm}, slave accepted {srec['accepted']}")
    check("A6 the slave then delivered that abandoned burst",
          any(a[1] == 0x1000 for a in srec["answered"]),
          f"answered {srec['answered']}")

    # the requirement: read 2 gets read 2's data
    second = got[1] if len(got) > 1 else []
    req("A6 the read after a timed-out one collects its OWN data",
        bool(second) and second[0]["data"] == word(0x2000, 0),
        f"first beat of read 2 = {hex(second[0]['data']) if second else None}, "
        f"expected {hex(word(0x2000, 0))}")

    # ... and the beat-counting arm does NOT close this one: the abandoned
    # command is a separate defect from the RLAST one, and a fix for A3/A4
    # alone still leaves the master reading another transaction's beats.
    fixed, _ = run(reqs=[[(0x1000, ALEN, 0, None), (0x2000, ALEN, 1, None)]],
                   slave_cfg={"ar_from": t_arm, "delay": {"_": 6}},
                   timeout_cls=_TimeoutBeatCounted)
    fx = bursts(fixed[0])
    check("A6 the beat-counting arm does not close this: the AR is still abandoned",
          len(fx) > 1 and fx[1][0]["data"] != word(0x2000, 0),
          "if this now passes, A6's fix landed too and the note above is stale")


# --- defect B: one stalled master freezes the read half -----------------------

B_REQS = [[(0x1000 * (i + 1), ALEN, 0, None)] for i in range(3)]


def test_defect_b():
    """Three masters, one slow answer. The other two must still make progress."""
    # B1, THE CONTROL: identical stimulus, master 0 answered promptly. The only
    # variable between this and the freeze below is that one delay.
    ctl, _ = run(reqs=B_REQS, slave_cfg={"ar_from": 1, "delay": {"_": 2}})
    for i in range(3):
        b = bursts(ctl[i])
        check(f"B1 control: master {i} completes its 4-beat read promptly",
              len(b) == 1 and len(b[0]) == ALEN + 1 and b[0][-1]["t"] < SOON
              and [x["data"] for x in b[0]]
              == [word(0x1000 * (i + 1), n) for n in range(ALEN + 1)],
              f"got {[[hex(x['data']) for x in bb] for bb in b]} "
              f"at {[x['t'] for x in ctl[i]['beats']]}")

    # B2, THE CONTROL FOR THE COMPARISON B4/B5 MAKE: a slow read does not have
    # to block a fast one on this DUT, this slave and this harness - as long as
    # both belong to the master that HOLDS THE GRANT. One master, two reads,
    # the second answered first. That is what narrows B4/B5 to the arbiter.
    ooo, _ = run(reqs=[[(0x1000, ALEN, 0, 5), (0x2000, ALEN, 0, 6)]],
                 slave_cfg={"ar_from": 1, "delay": {"_": 2, 5: 60, 6: 2}})
    ob = bursts(ooo[0])
    check("B2 the slave answers a later ID first, and the ID reaches the master",
          len(ob) >= 1 and ob[0][0]["id"] == 6
          and ob[0][0]["data"] == word(0x2000, 0),
          f"first burst id={ob[0][0]['id'] if ob else None} "
          f"data={hex(ob[0][0]['data']) if ob else None}")
    slow_first = [b["t"] for b in ooo[0]["beats"] if b["id"] == 5]
    check("B2 the fast read completes before the slow one is answered",
          len(ob) >= 1 and ob[0][0]["id"] == 6 and slow_first
          and ob[0][-1]["t"] < slow_first[0],
          f"fast read ends at {ob[0][-1]['t'] if ob else None}, "
          f"slow read starts at {slow_first[0] if slow_first else None}")

    # THE DEFECT: master 0's read is accepted and answered only after 300
    # cycles. Masters 1 and 2 want 4 beats each from the same slave, which has
    # had their answers ready since cycle 3.
    frz, srec = run(reqs=B_REQS,
                    slave_cfg={"ar_from": 1, "delay": {"_": 2, 0: SLOW}})
    m0 = bursts(frz[0])
    t0 = m0[0][0]["t"] if m0 else None      # when master 0 was finally answered

    # the premise
    check("B3 setup: the slave accepted master 0's read and held it",
          any(a[1] == 0x1000 for a in srec["accepted"]) and t0 is not None
          and t0 > SLOW,
          f"accepted {srec['accepted']}, master 0 first beat at {t0}")
    check("B3 setup: the read timeout cannot see this at an eighth of the stall",
          not any(b["resp"] == RESP_SLVERR for r in frz for b in r["beats"]),
          "a SLVERR beat means the timeout fired and the case is not the freeze")

    # the requirement
    for i in (1, 2):
        b = bursts(frz[i])
        done = b and len(b[0]) == ALEN + 1
        req(f"B{3 + i} master {i} completes its read before master 0 is answered",
            done and b[0][-1]["t"] < t0,
            f"master {i} beats at "
            f"{[x['t'] for x in frz[i]['beats']] or 'none'}, master 0 at {t0}")
    req("B6 the slave is shown the other masters' addresses while master 0 waits",
        any(a[0] < t0 and a[1] in (0x2000, 0x3000) for a in srec["accepted"]),
        f"the slave saw only {[(a[0], hex(a[1])) for a in srec['accepted']]}")


# --- provenance ---------------------------------------------------------------

def test_provenance():
    """Pin WHAT was characterised, so an upgrade cannot silence this file.

    None of the checks above build `AXIInterconnectShared` itself (the timeout
    has to be substitutable), and none of them would notice if LiteX moved the
    dma_bus onto a different interconnect. These three do.
    """
    src = inspect.getsourcefile(AXITimeout)
    print(f"  [--]   DUT source: {src}")
    check("the arbiter and the timeout come from one axi_full.py",
          os.path.basename(src) == "axi_full.py"
          and inspect.getsourcefile(AXIArbiter) == src,
          f"timeout {src}, arbiter {inspect.getsourcefile(AXIArbiter)}")

    ic = AXIInterconnectShared(
        masters = [AXIInterface(data_width=DW, address_width=AWD, id_width=IDW)],
        slaves  = [(lambda a: 1, AXIInterface(data_width=DW, address_width=AWD,
                                              id_width=IDW))],
        timeout_cycles = TMO)
    shape = [(n, m.__class__) for n, m in ic._submodules]
    check("SharedBus stands for AXIInterconnectShared: same parts, same order",
          [c for _, c in shape] == [AXIArbiter, AXIDecoder, AXITimeout],
          f"got {[(n, c.__name__) for n, c in shape]}")

    # and that this is what a SoC's "axi" bus with several masters gets. Parsed,
    # not grepped: a comment naming the class must not be able to satisfy it.
    tree = ast.parse(open(inspect.getsourcefile(soc_mod)).read())
    picked = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Subscript)):
            continue
        if not (node.targets and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "interconnect_shared_cls"):
            continue
        d = node.value.value
        if isinstance(d, ast.Dict):
            for k, v in zip(d.keys, d.values):
                if isinstance(k, ast.Constant) and k.value == "axi" \
                        and isinstance(v, ast.Attribute):
                    picked.add(v.attr)
    check("a SoC 'axi' bus with several masters gets AXIInterconnectShared",
          picked == {"AXIInterconnectShared"}, f"soc.py picks {picked or 'nothing'}")


if __name__ == "__main__":
    print("test_defect_a (the ARLEN bug):")
    test_defect_a()
    print("test_defect_a_abandoned (the AR the timeout could not withdraw):")
    test_defect_a_abandoned()
    print("test_defect_b (the arbiter freeze):")
    test_defect_b()
    print("test_provenance:")
    test_provenance()

    total = fails + xfails
    print(f"\ntest_dma_bus_faults: {checks} checks: {checks - total} PASS, "
          f"{total} FAIL")
    if xfails:
        print(f"  of those, {xfails} are the KNOWN-FAIL characterisation "
              f"checks: open LiteX defects A (RLAST vs ARLEN) and B (the "
              f"arbiter freeze). See the banner at the top of this file.")
    if xpass:
        print(f"  {xpass} requirement(s) went green: an open defect looks "
              f"FIXED. Re-read the banner and retire it.")
    if fails:
        print(f"  {fails} UNEXPECTED failure(s): those are ours, not LiteX's.")
    print("RESULT:", "FAIL" if total else "PASS")
    sys.exit(1 if total else 0)
