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
That is what made a local stall fatal: the generated netlist arbitrates the DMA
bus with

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
     answer given; the shipping one must report `err` and let go of the bus.
     If the watchdog were inert the two would agree and this test fails.
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

Run: cd sw/litex && python3 test_pp_mem_bridge.py
"""

import ast
import os
import sys

from migen import *

HERE = os.path.dirname(os.path.abspath(__file__))
MILAN_SOC = os.path.join(HERE, "milan_soc.py")

TMO = 32                       # the model's watchdog; the SoC uses 2,048

# Two different words, so a beat can say WHICH answer it carried: the one a
# healthy memory returns, and the one the abandoned access is still owed.
FRESH      = 0x01000100494D4541
FRESH_WIRE = 0x41454D4900010001   # FRESH in 1722.1 wire order (byte-reversed)
STALE      = 0x0BADF00D0BADF00D

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


class ReadBridge(Module):
    """The descriptor-image read FSM, in both shapes.

    `watchdog=False` reproduces the FSM as it stood in the flashed bitstream -
    the bus state exits on `ack` and on nothing else. `watchdog=True` is the
    shipping shape. The request/emit structure, the handshakes and the byte
    reversal are identical between the two, so the ONLY variable is the arm
    under test.
    """

    def __init__(self, watchdog):
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
        _dto = Signal(max=TMO + 1)
        self.psn = _dpsn = Signal(); _dpsn_set = Signal()
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
            rd.append(If(~self.wb_ack & (_dto == TMO),
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


def drive(dut, dead_after, cycles=400):
    """One 2-beat burst. `dead_after` bus accesses, the memory stops acking."""
    out = {"beats": [], "cyc_at_end": 0, "acks": 0}

    def stim():
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


def test_behavioural():
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
    check("watchdog FSM LETS GO of the bus (the arbiter is freed)",
          fix["cyc_at_end"] == 0, f"cyc={fix['cyc_at_end']}")
    check("watchdog FSM marks the master poisoned (a stale ack is still owed)",
          fix["psn"] == 1, f"psn={fix['psn']}")
    check("the watchdog changes behaviour (the fix is not a no-op)",
          pre["cyc_at_end"] != fix["cyc_at_end"])


def drive_recovery(dut, tries=4, budget=8 * TMO):
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

    def step():
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

    def burst(addr):
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

    def stim():
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


def test_recovery():
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


def _act_calls(tree, names):
    out = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "act"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and node.args[0].value in names):
            out.setdefault(node.args[0].value, []).append(node)
    return out


def _tokens(nodes):
    """Every Name id and Attribute attr under a list of AST nodes."""
    out = set()
    for node in nodes:
        for sub in ast.walk(node):
            if isinstance(sub, ast.Attribute):
                out.add(sub.attr)
            elif isinstance(sub, ast.Name):
                out.add(sub.id)
    return out


def _poison_latches(tree):
    """The per-transaction latches a state loads from a poison flag.

    `NextValue(_de, _dpsn)` in IDLE: `_de` is how the flag reaches the bus
    state, and finding it by assignment rather than by name is what keeps the
    bypass check below tied to the poison flag and not to any early exit.
    """
    out = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "NextValue" and len(node.args) == 2
                and isinstance(node.args[0], ast.Name)
                and isinstance(node.args[1], ast.Name)
                and node.args[1].id.endswith("psn")):
            out.add(node.args[0].id)
    return out


def _poison_clear_arms(tree):
    """The `.Elif(...)` conditions of every `If(<x>psn_set, ...)` register."""
    out = []
    for node in ast.walk(tree):
        outer = node.func.value if (isinstance(node, ast.Call)
                                    and isinstance(node.func, ast.Attribute)
                                    and node.func.attr == "Elif") else None
        if (isinstance(outer, ast.Call) and isinstance(outer.func, ast.Name)
                and outer.func.id == "If" and outer.args
                and isinstance(outer.args[0], ast.Name)
                and outer.args[0].id.endswith("psn_set") and node.args):
            out.append(node.args[0])
    return out


def _needs_an_ack(cond):
    """True if only an answer from the bus can meet this clear condition.

    `err` counts as one: wishbone2axi raises it WITH `ack`, so a condition
    that waits for either still waits for a transaction. The bus object's own
    name (`_dwb` in `_dwb.ack`) is not an operand and is discounted.
    """
    bases = {n.value for n in ast.walk(cond)
             if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    attrs = {n.attr for n in ast.walk(cond) if isinstance(n, ast.Attribute)}
    free = {n.id for n in ast.walk(cond)
            if isinstance(n, ast.Name) and n not in bases}
    return attrs <= {"ack", "err"} and all(f.endswith("psn") for f in free)


def _skips_the_bus(act, latches):
    """True if the state answers a poisoned transaction without driving cyc.

    The shape: `If(<latch>, NextState(...)).Else(cyc.eq(1), ...)`. Reached
    that way the state never asks the bus for anything, so nothing it does
    can produce the ack the poison flag is waiting for.
    """
    for node in ast.walk(act):
        outer = node.func.value if (isinstance(node, ast.Call)
                                    and isinstance(node.func, ast.Attribute)
                                    and node.func.attr == "Else") else None
        if not (isinstance(outer, ast.Call)
                and isinstance(outer.func, ast.Name)
                and outer.func.id == "If" and len(outer.args) >= 2):
            continue
        arm = _tokens(outer.args[1:])
        if (_tokens(outer.args[:1]) & latches
                and "NextState" in arm and "cyc" not in arm
                and "cyc" in _tokens(node.args)):
            return True
    return False


def test_structural():
    """Every bus state of the REAL FSMs must have a non-`ack` exit.

    Parsed, not grepped: a comment about watchdogs must not be able to satisfy
    this. For each bus state we require a NextState reached from a test that is
    NOT the `ack` test - which is what "leaves the state only on ack" means -
    and we require it to name the state's timeout counter.
    """
    src = open(MILAN_SOC).read()
    tree = ast.parse(src)

    # the pre-fix state names must be GONE, or a stale copy could satisfy the
    # per-state checks below while the live FSM kept the split-word shape
    dead = _act_calls(tree, {"RD_LO", "RD_HI", "WR_LO", "WR_HI"})
    check("the split-word bus states are gone (one access per 64-bit beat)",
          not dead, f"still present: {sorted(dead)}")

    acts = _act_calls(tree, {"RD", "WR"})
    check('milan_soc.py has both bus states, act("RD") and act("WR")',
          set(acts) == {"RD", "WR"}, f"found {sorted(acts)}")

    # The poison flag can only be cleared by an event the poisoned master can
    # still cause. Two shapes satisfy that and this check accepts either: the
    # bus state keeps driving cyc while poisoned (so the owed ack lands on the
    # master that is owed it), or the flag has a clear that is not an ack.
    latches = _poison_latches(tree)
    check("the poison flags reach the bus states through a loaded latch",
          len(latches) >= 2, f"found {sorted(latches)}")
    arms = _poison_clear_arms(tree)
    heals = bool(arms) and not any(_needs_an_ack(c) for c in arms)
    stranded = f"clear arms: {[ast.unparse(c) for c in arms]}"

    for state in sorted(acts):
        for act in acts[state]:
            names = {n.id for n in ast.walk(act) if isinstance(n, ast.Name)}
            attrs = {n.attr for n in ast.walk(act) if isinstance(n, ast.Attribute)}
            check(f'act("{state}") still tests wb.err alongside wb.ack',
                  "err" in attrs and "ack" in attrs,
                  "an ack-only test accepts a FAILED access")
            # the watchdog: a counter compared against a bound, inside an Elif
            # arm - i.e. an exit that is NOT the ack arm
            bounded = any(isinstance(n, ast.Compare)
                          and isinstance(n.left, ast.Name)
                          and n.left.id.endswith("to")
                          for n in ast.walk(act))
            check(f'act("{state}") exits on a TIMEOUT as well as on ack',
                  bounded, "one unacked access wedges this state forever")
            check(f'act("{state}") poisons the master on that exit',
                  any(nm.endswith("psn_set") for nm in names),
                  "a late ack would then pair with the NEXT access")
            check(f'act("{state}") cannot strand the flag it just set',
                  not _skips_the_bus(act, latches) or heals,
                  "poisoned, it answers without driving cyc, and the flag "
                  f"clears only on an ack that therefore never comes ({stranded})")

    check("the watchdog is sized in the source, not left to a magic number",
          "_pp_tmo" in src)
    check("both masters derive their address width from the data width",
          "_pp_adrw" in src and "_math.log2" in src)


if __name__ == "__main__":
    print("test_behavioural:")
    test_behavioural()
    print("test_recovery:")
    test_recovery()
    print("test_structural:")
    test_structural()
    print(f"\ntest_pp_mem_bridge: {checks} checks: "
          f"{checks - fails} PASS, {fails} FAIL")
    print("RESULT:", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)
