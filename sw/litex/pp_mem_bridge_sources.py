#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""The PARSED half of the protocol-processor memory-bridge evidence.

`test_pp_mem_bridge.py` makes five claims about the two main-memory bridges.
Three of them are simulated - they build migen FSMs and drive them - and two
are PARSED: milan_soc.py's own AST is read and required to have the shape the
simulation stands for, and the processor's RTL is read for the watchdog the
race in claim 4 is measured against. Those two need no migen, no simulator and
no LiteX, so they live here, and the simulation half imports them.

Splitting on that line is not filing: it means the structural evidence can be
run, and reviewed, on a machine that cannot build a SoC - and it keeps the two
kinds of claim from sharing helpers, which is how a "parsed" check quietly
starts believing a model.

THE TALLY LIVES HERE for the same reason it was a module-level dict before:
one run prints ONE verdict over both halves, so both halves must count into the
same object. `test_pp_mem_bridge.py` imports `TALLY` and `check` from here and
mutates that dict; nothing rebinds it.

Every path in this module is a `pathlib.Path`.
"""

import ast
import re
from pathlib import Path

#: This directory (sw/litex), the SoC source beside it, and the pinned
#: processor's top level two levels up. Paths, never strings: the only things
#: done with them here are `read_text()` and printing one in a failure detail.
HERE = Path(__file__).resolve().parent
MILAN_SOC = HERE / "milan_soc.py"
# the protocol processor is the AUTHORITY on its own watchdog: read the
# parameter out of its RTL rather than believing milan_soc.py's mirror of it
PP_TOP_SV = (HERE.parents[1] / "protocol-processor" / "hdl" / "top"
             / "protocol_processor_top.sv")

#: The running tally. A dict the arms MUTATE, never rebind, so `check` does
#: not have to reach up and re-declare this module's own counters - and the
#: final verdict below reads the same object every arm wrote to.
TALLY = {"checks": 0, "fails": 0}


def check(name: str, cond: object, detail: str = "") -> None:
    """Grade one claim into the module-level tally. `cond` is read for truth
    only, and `detail` is printed just when it fails - a failure that does not
    say what it saw costs the next reader the run."""
    TALLY["checks"] += 1
    if cond:
        print(f"  [ok]   {name}")
    else:
        TALLY["fails"] += 1
        print(f"  [FAIL] {name} {detail}")


def proc_watchdog_from_rtl() -> int | None:
    """DESC_MEM_TMO_CYC_P, read from the processor's own RTL.

    The authority is the submodule, not milan_soc.py's mirror of it. Bumping
    the parameter in the .sv and forgetting the mirror would otherwise widen
    the processor's budget silently - which is harmless - or NARROW it, which
    hands the race to the processor and voids the design intent with nothing
    to see.
    """
    src = PP_TOP_SV.read_text()
    m = re.search(r"parameter\s+int\s+unsigned\s+DESC_MEM_TMO_CYC_P\s*=\s*"
                  r"(\d+)", src)
    return int(m.group(1)) if m else None


def test_counter_wiring() -> None:
    """The observer must be wired to the REAL bridges, and to BOTH of them.

    Parsed, not grepped. Everything above builds its own wiring, so a perfectly
    correct block connected to the wrong signals - or to one face only - would
    pass every behavioural check and still read 0 on the board.
    """
    tree = ast.parse(MILAN_SOC.read_text())
    calls = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "_PPMemDiag"]
    check("milan_soc.py instantiates _PPMemDiag", len(calls) == 1,
          f"found {len(calls)}")
    if not calls:
        return
    faces = {}
    for face in (calls[0].args[0].elts if calls[0].args
                 and isinstance(calls[0].args[0], (ast.List, ast.Tuple))
                 else []):
        if isinstance(face, ast.Tuple) and isinstance(face.elts[0], ast.Constant):
            faces[face.elts[0].value] = {n.id for n in ast.walk(face)
                                         if isinstance(n, ast.Name)}
    # ORDER IS ABI: `stat` packs two live bits per face in this order, and the
    # register map publishes those bit positions. Swapping the two faces would
    # keep every counter correct and silently rename the flags.
    check("both memory bridges are observed, descriptor face first",
          list(faces) == ["desc", "resp"], f"faces: {list(faces)}")
    # The bus objects the FSMs actually drive, the flags they actually set.
    for face, want in (("desc", {"_dwb", "_dpsn", "_dpsn_set"}),
                       ("resp", {"_rwb", "_rpsn", "_rpsn_set"})):
        check(f"the {face} face watches that bridge's own bus, poison flag "
              "and watchdog pulse",
              want <= faces.get(face, set()),
              f"wired to {sorted(faces.get(face, set()))}, want {sorted(want)}")

    # The bank's ADDRESS is part of the ABI the register map publishes, and
    # LiteX allocates the lowest free page: unpinned, this bank lands on
    # sdram's page and pushes the LiteSPI bank - a write path to the boot
    # flash - out from under every consumer that names it.
    pinned = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr == "add" and n.args
              and isinstance(n.args[0], ast.Constant) and n.args[0].value == "ppmem"]
    check("the ppmem CSR bank is pinned to a fixed location",
          bool(pinned) and any(k.arg == "n" for c in pinned for k in c.keywords),
          "an unpinned bank moves sdram and spiflash the next time a module "
          "is added ahead of it")


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

    The loaded value only has to NAME the flag, not be it: since 2026-08-14
    IDLE loads `_dpsn | ~_mem_rdy`, because a request that arrives before the
    BIOS has finished with the DDR3 is answered `err` without a bus cycle at
    all. Requiring a bare name here would grade the expression's shape, which
    is not the claim.
    """
    out = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "NextValue" and len(node.args) == 2
                and isinstance(node.args[0], ast.Name)
                and any(isinstance(n, ast.Name) and n.id.endswith("psn")
                        for n in ast.walk(node.args[1]))):
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


def test_structural() -> None:
    """Every bus state of the REAL FSMs must have a non-`ack` exit.

    Parsed, not grepped: a comment about watchdogs must not be able to satisfy
    this. For each bus state we require a NextState reached from a test that is
    NOT the `ack` test - which is what "leaves the state only on ack" means -
    and we require it to name the state's timeout counter.
    """
    src = MILAN_SOC.read_text()
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
