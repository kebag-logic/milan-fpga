#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""The AAF playback DDR3 fetch bridge must not accept a FAILED read.

THE DEFECT (found 2026-08-11, present in the flashed bitstream). LiteX's
wishbone2axi does not signal a bus error by withholding `ack` - it asserts
`ack` AND `err` in the SAME cycle. Verified in the shipping build's own
generated netlist, gateware/alinx_ax7101.v:

    10713:  2'd3: begin
    10714:      milandma_interface2_adapted_interface_ack = 1'd1;
    10715:      milandma_interface2_adapted_interface_err = 1'd1;

while the bridge FSM tested only `ack`:

    22287:  if (milandma_aafpb_wb_ack) begin
    22288:      milandma_pb_data_l_fsm_next_value1 = milandma_aafpb_wb_dat_r;

and `milandma_aafpb_wb_err` occurred exactly TWICE in the whole file - its
declaration and its assign. ZERO consumers. So a DRAM/interconnect read error
latched an UNDEFINED 64-bit word and handed it to KL_pcm_tx as a valid PCM
sample, in a hard-real-time audio path, with nothing to observe it by.

WHY SILENCE AND NOT A STALL. Refusing to answer would hang KL_pcm_tx: it waits
for the word it asked for (KL_pcm_tx.sv:84 - "any latency" means any, not
never). Digital silence keeps the media grid running and makes the damage
bounded, deterministic and - via the _pb_bus_err CSR - visible.

WHAT THIS FILE PROVES, in two independent ways so neither can pass vacuously:
  1. BEHAVIOURAL. Two FSMs are built in the same run - the pre-fix shape
     (ack-only) and the shipping shape (ack + err arm) - and driven by the
     SAME errored-read stimulus. The pre-fix one must forward the poison word
     and count nothing; the fixed one must forward zero and count one. If the
     fix were inert both would agree and the test fails.
  2. STRUCTURAL. milan_soc.py is parsed and the real READ state is required to
     carry an `err` test and a saturating counter, so the behavioural model
     above cannot drift away from the code it stands for.
"""

import ast
import os
import sys

from migen import *

HERE = os.path.dirname(os.path.abspath(__file__))
MILAN_SOC = os.path.join(HERE, "milan_soc.py")

POISON = 0xDEADBEEFCAFEF00D      # what a failed read leaves on dat_r
GOOD   = 0x0123456789ABCDEF

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


class Bridge(Module):
    """The playback fetch bridge, in both shapes.

    `err_arm=False` reproduces the pre-fix FSM exactly as it stood in the
    flashed netlist; `err_arm=True` is the shipping shape. Everything else -
    the IDLE/READ/RESP structure, the latch, the handshakes - is identical, so
    the ONLY variable between the two runs is the arm under test.
    """

    def __init__(self, err_arm):
        self.req_valid = Signal()
        self.req_addr = Signal(32)
        self.wb_ack = Signal()
        self.wb_err = Signal()
        self.wb_dat_r = Signal(64)
        self.resp_valid = Signal()
        self.resp_data = Signal(64)
        self.err_cnt = Signal(32)

        data_l = Signal(64)
        addr_l = Signal(32)
        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            If(self.req_valid, NextValue(addr_l, self.req_addr), NextState("READ")))
        if err_arm:
            fsm.act("READ",
                If(self.wb_ack,
                    If(self.wb_err,
                        NextValue(data_l, 0),
                        If(self.err_cnt != 2**32 - 1,
                           NextValue(self.err_cnt, self.err_cnt + 1)),
                    ).Else(
                        NextValue(data_l, self.wb_dat_r),
                    ),
                    NextState("RESP")))
        else:
            fsm.act("READ",
                If(self.wb_ack, NextValue(data_l, self.wb_dat_r), NextState("RESP")))
        fsm.act("RESP",
            self.resp_valid.eq(1), NextState("IDLE"))
        self.comb += self.resp_data.eq(data_l)


def drive(dut, errored):
    """One request; the slave answers with ack, and with err when `errored`."""
    seen = []

    def stim():
        yield dut.req_valid.eq(1)
        yield
        yield dut.req_valid.eq(0)
        # slave responds a few cycles later, ack and err TOGETHER
        for _ in range(3):
            yield
        yield dut.wb_ack.eq(1)
        yield dut.wb_err.eq(1 if errored else 0)
        yield dut.wb_dat_r.eq(POISON if errored else GOOD)
        yield
        yield dut.wb_ack.eq(0)
        yield dut.wb_err.eq(0)
        for _ in range(6):
            if (yield dut.resp_valid):
                seen.append((yield dut.resp_data))
            yield
        seen.append((yield dut.err_cnt))

    run_simulation(dut, stim())
    return seen


def test_behavioural():
    """The errored read must not reach KL_pcm_tx, and must be counted."""
    pre = drive(Bridge(err_arm=False), errored=True)
    fix = drive(Bridge(err_arm=True), errored=True)
    ok = drive(Bridge(err_arm=True), errored=False)

    pre_words, pre_cnt = pre[:-1], pre[-1]
    fix_words, fix_cnt = fix[:-1], fix[-1]
    ok_words, ok_cnt = ok[:-1], ok[-1]

    # the pre-fix shape is the DEFECT - if this does not reproduce, the test is
    # not exercising the path and every result below is meaningless
    check("pre-fix FSM forwards the poison word (the defect reproduces)",
          POISON in pre_words, f"got {[hex(w) for w in pre_words]}")
    check("pre-fix FSM counts nothing", pre_cnt == 0, f"got {pre_cnt}")

    # the fix
    check("fixed FSM never forwards the poison word",
          POISON not in fix_words, f"got {[hex(w) for w in fix_words]}")
    check("fixed FSM substitutes digital silence",
          fix_words and all(w == 0 for w in fix_words),
          f"got {[hex(w) for w in fix_words]}")
    check("fixed FSM counts the error exactly once", fix_cnt == 1, f"got {fix_cnt}")

    # and it must not fire on a clean read, or the counter is worthless
    check("clean read still delivers its data", GOOD in ok_words,
          f"got {[hex(w) for w in ok_words]}")
    check("clean read counts no error", ok_cnt == 0, f"got {ok_cnt}")

    # the two shapes MUST disagree, or the arm is inert
    check("the err arm changes behaviour (the fix is not a no-op)",
          pre_words != fix_words or pre_cnt != fix_cnt)


def test_structural():
    """The real milan_soc.py READ state must carry the arm and the counter.

    Parsed, not grepped: a comment mentioning `err` must not be able to satisfy
    this. We locate the fsm.act("READ", ...) call and require an attribute load
    of `.err` and a saturating increment inside its argument tree.
    """
    tree = ast.parse(open(MILAN_SOC).read())
    read_acts = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "act"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and node.args[0].value == "READ"):
            read_acts.append(node)
    check("milan_soc.py has an fsm.act(\"READ\", ...)", len(read_acts) >= 1,
          f"found {len(read_acts)}")
    if not read_acts:
        return

    hit_err = hit_sat = False
    for act in read_acts:
        attrs = {n.attr for n in ast.walk(act) if isinstance(n, ast.Attribute)}
        if "err" in attrs and "ack" in attrs:
            hit_err = True
            # The saturating guard: a bare +1 wraps to zero and would read as
            # "no errors ever happened".
            # NOT "is there a ** in here" - the line above is
            # `sel.eq(2**nb - 1)`, so that test passes on ANY version of this
            # FSM and proved to be a tautology when mutation-tested. Require
            # instead that the counter is COMPARED against something, i.e.
            # that the increment is guarded by a test naming the counter.
            for n in ast.walk(act):
                if (isinstance(n, ast.Compare)
                        and isinstance(n.left, ast.Name)
                        and n.left.id.endswith("err_cnt")):
                    hit_sat = True
    check("the READ state tests wb.err alongside wb.ack", hit_err,
          "an ack-only test accepts a FAILED read")
    check("the error counter saturates rather than wrapping", hit_sat,
          "a wrapping counter reads as 0 after 2**32 errors")

    src = open(MILAN_SOC).read()
    check("a CSR exposes the count (_pb_bus_err)", "_pb_bus_err" in src)


if __name__ == "__main__":
    print("test_behavioural:")
    test_behavioural()
    print("test_structural:")
    test_structural()
    print(f"\ntest_pb_bus_err: {checks} checks: {checks - fails} PASS, {fails} FAIL")
    print("RESULT:", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)
