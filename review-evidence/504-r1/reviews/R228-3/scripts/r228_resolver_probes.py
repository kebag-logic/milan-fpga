#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R228-3 reviewer-owned literal-assembly probes of the RV32 store resolver.

Usage: r228_resolver_probes.py <tree> [<out.json>]

Imports sw/builder/test_builder.py from <tree> and drives rv32_run() on
hand-written assembly. Each probe states the SOUND answer; the script
records what the resolver reported and whether it matched. Nothing is
compiled and no file in <tree> is written.

"stale" probes park an address outside the window, rewrite the parked
word, reload it and store through it. The sound answer is an UNPLACED
final store. "kept" probes are the whole-word positive arms.
"""

import json
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
sys.path.insert(0, str(tree / "scripts"))
import test_builder as tb  # noqa: E402

OUTSIDE = 0x8000_1000
CSR_BASE = 0x9000_0000          # read back from the gate's own footprint note
FRAME = ("\taddi sp,sp,-48\n\tsw ra,44(sp)\n\tsw s0,40(sp)\n"
         "\taddi s0,sp,48\n"
         f"\tli a5,{tb._rv32_s32(OUTSIDE)}\n")
STATIC = FRAME + "\tlla a3,probe_static\n"
TAIL = "\tli a2,1\n\tsw a2,0(a4)\n"


def run(body):
    """Store addresses the resolver reports for one function body."""
    result = tb.rv32_run(tb.rv32_functions(f"probe:\n{body}\tret\n")["probe"], {})
    return [address for _at, (address, _v) in result["stores"]]


def show(value):
    """JSON-friendly rendering of one reported address."""
    return f"0x{value:08x}" if isinstance(value, int) else repr(value)


def last_is_unplaced(reported):
    return bool(reported) and isinstance(reported[-1], tb.Rv32Where) and \
        reported[-1].kind == "unplaced"


results = []


def record(group, label, body, reported, sound, expectation):
    results.append({"group": group, "label": label, "body": body,
                    "reported": [show(r) for r in reported],
                    "expected": expectation, "sound": bool(sound)})


# ---- stale-word rewrites: every one must leave the final store unplaced
stale = (
    ("frame: sb at the slot's LAST byte (+3)",
     FRAME + "\tsw a5,-20(s0)\n\tsb zero,-17(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: sb at +1", FRAME + "\tsw a5,-20(s0)\n\tsb zero,-19(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: sb at +2", FRAME + "\tsw a5,-20(s0)\n\tsb zero,-18(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: sh at +2 (upper half)",
     FRAME + "\tsw a5,-20(s0)\n\tsh zero,-18(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: misaligned sw from below (-22)",
     FRAME + "\tsw a5,-20(s0)\n\tsw zero,-22(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: misaligned sw from above (-18)",
     FRAME + "\tsw a5,-20(s0)\n\tsw zero,-18(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: fsd at the slot's own offset",
     FRAME + "\tsw a5,-20(s0)\n\tfsd fa5,-20(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: fsd over the NEXT slot (-16) from -20",
     FRAME + "\tsw a5,-16(s0)\n\tfsd fa5,-20(s0)\n\tlw a4,-16(s0)\n"),
    ("frame: fsq from -32 covering -20",
     FRAME + "\tsw a5,-20(s0)\n\tfsq fa5,-32(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: fsh at +2", FRAME + "\tsw a5,-20(s0)\n\tfsh fa5,-18(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: amoswap via a pointer (stack base)",
     FRAME + "\tsw a5,-20(s0)\n\taddi a3,s0,-20\n\tli a2,7\n"
     "\tamoswap.w t0,a2,0(a3)\n\tlw a4,-20(s0)\n"),
    ("frame: sc.w at the slot through s0",
     FRAME + "\tsw a5,-20(s0)\n\tsc.w t0,a5,0(s0)\n\tlw a4,0(s0)\n"),
    ("frame: sb through a pointer to the slot",
     FRAME + "\tsw a5,-20(s0)\n\taddi a3,s0,-17\n\tsb zero,0(a3)\n\tlw a4,-20(s0)\n"),
    ("frame: sw through a pointer formed from sp",
     FRAME + "\tsw a5,-20(s0)\n\taddi a3,sp,28\n\tsw zero,0(a3)\n\tlw a4,-20(s0)\n"),
    ("frame: sw through a stack pointer parked in another slot",
     FRAME + "\tsw a5,-20(s0)\n\taddi a3,s0,-20\n\tsw a3,-24(s0)\n"
     "\tlw a3,-24(s0)\n\tsw zero,0(a3)\n\tlw a4,-20(s0)\n"),
    ("static: sb at byte 3", STATIC + "\tsw a5,0(a3)\n\tsb zero,3(a3)\n\tlw a4,0(a3)\n"),
    ("static: sh at +2", STATIC + "\tsw a5,0(a3)\n\tsh zero,2(a3)\n\tlw a4,0(a3)\n"),
    ("static: fsd from -4 covering word 0",
     STATIC + "\tsw a5,0(a3)\n\tfsd fa5,-4(a3)\n\tlw a4,0(a3)\n"),
    ("static: misaligned sw at +2", STATIC + "\tsw a5,0(a3)\n\tsw zero,2(a3)\n\tlw a4,0(a3)\n"),
    ("static: amoxor", STATIC + "\tsw a5,0(a3)\n\tamoxor.w t0,a5,0(a3)\n\tlw a4,0(a3)\n"),
    ("static: amomaxu.w.aqrl", STATIC + "\tsw a5,0(a3)\n\tamomaxu.w.aqrl t0,a5,0(a3)\n\tlw a4,0(a3)\n"),
    ("static: sc.w.aqrl", STATIC + "\tsw a5,0(a3)\n\tsc.w.aqrl t0,a5,0(a3)\n\tlw a4,0(a3)\n"),
    ("static: unclassified memory writer (cbo.zero) over it",
     STATIC + "\tsw a5,0(a3)\n\tcbo.zero (a3)\n\tlw a4,0(a3)\n"),
    ("static: a store through an unresolved pointer",
     STATIC + "\tsw a5,0(a3)\n\tlw a1,0(a0)\n\tsw zero,0(a1)\n\tlw a4,0(a3)\n"),
    ("static: a call between", STATIC + "\tsw a5,0(a3)\n\tcall helper\n"
     "\tlla a3,probe_static\n\tlw a4,0(a3)\n"),
    ("atomic: rd receives old memory (amoswap rd=a4)",
     FRAME + "\tli a4,0\n\tlla a3,probe_static\n\tamoswap.w a4,a5,0(a3)\n"),
    ("atomic: unreadable amo operand clears rd",
     FRAME + "\tmv a4,a5\n\tamoor.w a4,a5,probe_static\n"),
)
for label, body in stale:
    reported = run(body + TAIL)
    record("stale", label, body, reported, last_is_unplaced(reported),
           "final store unplaced")

# ---- pre-existing reads the page documents as NOT observed/limited
limits = (
    ("frame: lbu from the slot reads the whole modelled word",
     FRAME + "\tsw a5,-20(s0)\n\tlbu a4,-20(s0)\n"),
    ("frame: lhu from the slot reads the whole modelled word",
     FRAME + "\tsw a5,-20(s0)\n\tlhu a4,-20(s0)\n"),
    ("frame: sp-keyed store aliasing an s0-keyed slot (-20(s0) == 28(sp))",
     FRAME + "\tsw a5,-20(s0)\n\tsw zero,28(sp)\n\tlw a4,-20(s0)\n"),
    ("frame: slot survives a call that was handed its address",
     FRAME + "\tsw a5,-20(s0)\n\taddi a0,s0,-20\n\tcall helper\n\tlw a4,-20(s0)\n"),
    ("frame: slot survives a store through a resolved number",
     FRAME + "\tsw a5,-20(s0)\n\tli a3,0x10000\n\tsw zero,0(a3)\n\tlw a4,-20(s0)\n"),
)
for label, body in limits:
    reported = run(body + TAIL)
    record("documented-limit", label, body, reported, last_is_unplaced(reported),
           "sound answer would be unplaced; page states this is not modelled")

# ---- positive arms: whole-word stores must keep exactly their word
kept = (
    ("frame: sw keeps", FRAME + "\tsw a5,-20(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: sw at -16 survives sb at -20 (disjoint)",
     FRAME + "\tsw a5,-16(s0)\n\tsb zero,-20(s0)\n\tlw a4,-16(s0)\n"),
    ("frame: sw at -20 survives sh at -22 (disjoint below)",
     FRAME + "\tsw a5,-20(s0)\n\tsh zero,-22(s0)\n\tlw a4,-20(s0)\n"),
    ("frame: sw at -20 survives sw at -24 (adjacent)",
     FRAME + "\tsw a5,-20(s0)\n\tsw zero,-24(s0)\n\tlw a4,-20(s0)\n"),
    ("static: amoswap.w.aqrl keeps rs2",
     STATIC + "\tamoswap.w.aqrl t0,a5,0(a3)\n\tlw a4,0(a3)\n"),
    ("static: word 4 survives sb at word 0",
     STATIC + "\tsw a5,4(a3)\n\tsb zero,3(a3)\n\tlw a4,4(a3)\n"),
)
for label, body in kept:
    reported = run(body + TAIL)
    record("kept", label, body, reported, reported[-1:] == [OUTSIDE],
           f"final store placed at 0x{OUTSIDE:08x}")

# ---- class and footprint probes near both window edges and 32-bit wrap
footprint = (
    ("fsq straddling into the window from -12",
     f"\tli a4,{tb._rv32_s32(CSR_BASE - 12)}\n\tfsq fa5,0(a4)\n",
     [CSR_BASE - 12, CSR_BASE - 8, CSR_BASE - 4, CSR_BASE]),
    ("misaligned fsw from -1", f"\tli a4,{tb._rv32_s32(CSR_BASE - 1)}\n\tfsw fa5,0(a4)\n",
     [CSR_BASE - 1, CSR_BASE]),
    ("sh straddling from -1", f"\tli a4,{tb._rv32_s32(CSR_BASE - 1)}\n\tsh a5,0(a4)\n",
     [CSR_BASE - 1, CSR_BASE]),
    ("fsd wrapping at 2^32", "\tli a4,-4\n\tfsd fa5,0(a4)\n", [0xFFFF_FFFC, 0]),
    ("negative displacement", f"\tli a4,{tb._rv32_s32(CSR_BASE + 8)}\n\tfsd fa5,-12(a4)\n",
     [CSR_BASE - 4, CSR_BASE]),
)
for label, body, words in footprint:
    reported = run(body)
    record("footprint", label, body, reported, reported == words,
           [show(w) for w in words])

# ---- the branch-refinement mirror must stop at every memory writer
mirror_range = tb.Rv32Range(0x4000_0000, 0x4000_0000 + 63 + 3)


def mirror(between):
    return run("\taddi sp,sp,-32\n\tsw s0,28(sp)\n\taddi s0,sp,32\n"
               "\tlw a4,0(a1)\n\tsw a4,-20(s0)\n\tlw a4,-20(s0)\n"
               f"{between}\tli a5,64\n\tbltu a4,a5,.L3\n\tj .L9\n"
               f".L3:\n\tlw a3,-20(s0)\n\tli a2,{tb._rv32_s32(mirror_range.lo)}\n"
               "\tadd a3,a2,a3\n\tsw zero,0(a3)\n.L9:\n")


record("mirror", "positive: nothing between", "", mirror(""),
       mirror("")[-1:] == [mirror_range], repr(mirror_range))
for label, between in (("sb over the slot", "\tsb zero,-20(s0)\n"),
                       ("sw to another slot", "\tsw zero,-24(s0)\n"),
                       ("fsd over the slot", "\tfsd fa5,-24(s0)\n"),
                       ("sc.w through a pointer", "\taddi a3,s0,-20\n\tsc.w t0,a5,0(a3)\n"),
                       ("cbo.zero through a pointer", "\taddi a3,s0,-20\n\tcbo.zero (a3)\n"),
                       ("a call", "\tcall helper\n")):
    reported = mirror(between)
    record("mirror", f"stop: {label}", between, reported,
           last_is_unplaced(reported), "final store unplaced")
record("mirror", "no stop: an ALU op between", "\tli a2,5\n",
       mirror("\tli a2,5\n"), mirror("\tli a2,5\n")[-1:] == [mirror_range],
       repr(mirror_range))

# ---- loads must never be reported as stores
for insn in ("flh fa5,0(a4)", "flq fa5,0(a4)", "lr.w.aq a3,(a4)", "lhu a3,2(a4)"):
    reported = run(f"\tli a4,{tb._rv32_s32(CSR_BASE)}\n\t{insn}\n")
    record("load", insn, insn, reported, reported == [], "no store")

sound = sum(r["sound"] for r in results if r["group"] != "documented-limit")
total = sum(1 for r in results if r["group"] != "documented-limit")
limit_open = [r["label"] for r in results
              if r["group"] == "documented-limit" and not r["sound"]]
summary = {"tree": "<tree>", "sound": sound, "total": total,
           "unsound": [r["label"] for r in results
                       if r["group"] != "documented-limit" and not r["sound"]],
           "documented_limits_unsound": limit_open, "results": results}
text = json.dumps(summary, indent=1)
if len(sys.argv) > 2:
    Path(sys.argv[2]).write_text(text + "\n")
print(f"R228 resolver probes: {sound}/{total} sound; unsound: {summary['unsound']}")
print(f"documented limits still unsound (expected): {limit_open}")
sys.exit(0 if sound == total else 1)
