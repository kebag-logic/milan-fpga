#!/usr/bin/env python3
"""R528-3 reviewer probes for PR #687 at 8b78a8fd (merge-sensitive plants).

Usage: r528_3_probes.py CLONE SCRATCH [PROBE ...]

Every source plant is written into a disposable copy of sw/firmware/ctrl
(ctrl_mutants.plant), never into CLONE. Harness plants are applied by
monkeypatching the imported driver modules in this process only. Each probe
prints its expected and observed verdicts; rc is 0 only when every probe
behaved as expected.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
SCRATCH = Path(sys.argv[2]).resolve()
sys.path[:0] = [str(CLONE / "sw/firmware/ctrl/test"), str(CLONE / "sw/firmware/gtest")]

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import fw_rv32  # noqa: E402
from ctrl_build import Outcome, Refusal, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

M = ctrl_mutants.Mutant
BUILD = fw_gtest.Build(jobs=4)

ARMS = {"maap": ctrl_arms.arm_maap, "maap_debug": ctrl_arms.arm_maap_debug,
        "maap_if2": ctrl_arms.arm_maap_if2, "rv32": lambda t: ctrl_arms.arm_rv32(t, True)}

ASSERT_INC = "#ifndef NDEBUG\n#include <assert.h>\n#endif\n"
ASSERT_USE = "#ifndef NDEBUG\n\t\tassert(!m->in_call);\n#endif\n"

# name -> (mutant, {arm: expected rc (0 pass, 1 fail)}, needle that a failing arm must print or "")
SOURCE = {
    # Revert 8b78a8fd's include guard: the hosted header must be refused by the freestanding RV32 build.
    "p1-unconditional-assert-include": (
        M("p1", "maap/maap.c", ASSERT_INC, "#include <assert.h>\n", "rv32", "", "does not build for RV32I"),
        {"rv32": 1, "maap": 0, "maap_debug": 0}, "does not build for RV32I"),
    # Revert all of 8b78a8fd.
    "p2-revert-8b78a8fd": (
        M("p2", "maap/maap.c", ASSERT_INC, "#include <assert.h>\n", "rv32", "", "does not build for RV32I"),
        {"rv32": 1, "maap": 0, "maap_debug": 0}, "does not build for RV32I"),
    # Flip the assertion guard: the debug build no longer asserts; the expected-abort test must fail.
    "p3-assert-only-in-release": (
        M("p3", "maap/maap.c", ASSERT_USE, "#ifdef NDEBUG\n\t\tassert(!m->in_call);\n#endif\n",
          "maap_debug", "", ""),
        # The include stays debug-only, so release builds no longer compile: every arm reports the defect.
        {"maap_debug": 1, "maap": 2, "rv32": 1}, ""),
    # Assertion dropped entirely, still in a debug-only block.
    "p4-assert-removed": (
        M("p4", "maap/maap.c", ASSERT_USE, "#ifndef NDEBUG\n\t\t(void)0;\n#endif\n", "maap_debug", "", ""),
        {"maap_debug": 1, "maap": 0}, ""),
    # Stray runtime dependency in MAAP core objects (memmove is not a named interface).
    "p5-maap-core-memmove": (
        M("p5", "maap/maap.c", "memcpy(m->queue[i], m->queue[i + 1u], MAAP_FRAME_BYTES);",
          "__builtin_memmove(m->queue[i], m->queue[i + 1u], MAAP_FRAME_BYTES);", "rv32", "", "x"),
        {"rv32": 1, "maap": 0}, "symbols outside the C library"),
    # Stray runtime dependency in the MAAP mailbox adapter object.
    "p6-maap-mbx-heap": (
        M("p6", "maap/maap_mbx.c", "memset(m, 0, sizeof *m);",
          "memset(m, 0, sizeof *m);\n\t{ void *volatile heap = __builtin_malloc(1); (void)heap; }", "rv32", "", "x"),
        {"rv32": 1}, "symbols outside the C library"),
    # An undeclared-interface dependency in the MAAP CSR object.
    "p7-maap-csr-puts": (
        M("p7", "maap/maap_csr.c", "memset(c, 0, sizeof *c);",
          "memset(c, 0, sizeof *c);\n\t{ extern int puts(const char *); (void)puts(\"x\"); }", "rv32", "", "x"),
        {"rv32": 1}, "puts"),
    # R528-2-S1 variant of my own: a bounce re-probes the previous allocation instead of drawing.
    "p8-bounce-reuses-previous-base": (
        M("p8", "maap/maap.c", "\t\t\t\trestart(m); // Table B.7 PortOperational! in every state",
          "\t\t\t\tif (m->base != 0u) { stop_timer(m); m->queued = 0; m->state = MAAP_INITIAL; "
          "reserve(m, m->base); } else { restart(m); }", "maap", "", ""),
        {"maap": 1}, "MaapCore.LinkBounceDrawsAfterSuppliedRange"),
    # The assigned control, replayed by the reviewer.
    "p9-r2-saved-range-never-consumed": (
        M("p9", "maap/maap.c", "m->preferred = 0;", "/* saved preference retained */;", "maap", "", ""),
        {"maap": 1}, "link bounce draws after consuming supplied range"),
}


def run_arms(tree: Tree, expect: dict[str, int], needle: str) -> bool:
    ok = True
    for arm, want in expect.items():
        try:
            out = ARMS[arm](tree)
        except Refusal as exc:
            out = Outcome(arm, 2, f"refused: {exc}")
        fails = [ln.strip() for ln in out.log.splitlines() if "[FAIL]" in ln]
        got = 0 if out.rc == 0 else (2 if out.rc == 2 and want == 2 else 1)
        hit = (not needle) or want == 0 or any(needle in ln for ln in out.log.splitlines())
        good = got == want and hit
        ok &= good
        print(f"  arm {arm}: rc={out.rc} expected={'FAIL' if want else 'PASS'} "
              f"{'needle-ok' if hit else 'NEEDLE-MISSING:' + needle} -> {'as expected' if good else 'UNEXPECTED'}")
        for ln in fails[:4]:
            print(f"    {ln[:240]}")
        if out.rc == 2:
            print(f"    {out.log[:400]}")
    return ok


def compiler_selection() -> bool:
    """CTRL_RV32_CC (documented by maap/README.md:155) versus MILAN_RV32_CC after the merge."""
    saved = {k: os.environ.pop(k, None) for k in ("CTRL_RV32_CC", "MILAN_RV32_CC")}
    try:
        base = fw_rv32.compiler()
        os.environ["CTRL_RV32_CC"] = "riscv64-elf-gcc"
        legacy = fw_rv32.compiler()
        del os.environ["CTRL_RV32_CC"]
        os.environ["MILAN_RV32_CC"] = "riscv64-elf-gcc"
        current = fw_rv32.compiler()
    finally:
        for k, v in saved.items():
            os.environ.pop(k, None)
            if v is not None:
                os.environ[k] = v
    print(f"  default compiler: {base}")
    print(f"  CTRL_RV32_CC=riscv64-elf-gcc selects: {legacy}")
    print(f"  MILAN_RV32_CC=riscv64-elf-gcc selects: {current}")
    ignored = legacy == base and current != base
    print(f"  CTRL_RV32_CC ignored after the merge: {ignored}")
    return True


def harness_no_ndebug(reuse: Path) -> bool:
    """RV32 arm without -DNDEBUG: the debug configuration of maap.c on the target headers."""
    saved = ctrl_arms.RV32_FLAGS
    ctrl_arms.RV32_FLAGS = tuple(f for f in saved if f != "-DNDEBUG")
    try:
        tree = Tree(ctrl_arms.CTRL, SCRATCH / "h1" / "build", reuse, BUILD)
        return run_arms(tree, {"rv32": 1}, "does not build for RV32I")
    finally:
        ctrl_arms.RV32_FLAGS = saved


def baseline(reuse: Path, which: str) -> bool:
    """The unplanted head on the probed arms, with one compiler choice."""
    if which == "elf":
        os.environ["MILAN_RV32_CC"] = "riscv64-elf-gcc"
    try:
        tree = Tree(ctrl_arms.CTRL, SCRATCH / f"base-{which}" / "build", reuse, BUILD)
        return run_arms(tree, {"rv32": 0, "maap": 0, "maap_debug": 0, "maap_if2": 0}, "")
    finally:
        os.environ.pop("MILAN_RV32_CC", None)


def main() -> int:
    wanted = sys.argv[3:] or ["baseline-sdk", "baseline-elf", "compiler", "h1-no-ndebug", *SOURCE]
    SCRATCH.mkdir(parents=True, exist_ok=True)
    reuse = cut_reuse(SCRATCH / "reuse") and SCRATCH / "reuse"
    print(f"toolchain: {fw_gtest.toolchain()}")
    bad = []
    for name in wanted:
        print(f"== probe {name}")
        if name == "baseline-sdk":
            ok = baseline(reuse, "sdk")
        elif name == "baseline-elf":
            ok = baseline(reuse, "elf")
        elif name == "compiler":
            ok = compiler_selection()
        elif name == "h1-no-ndebug":
            ok = harness_no_ndebug(reuse)
        else:
            mutant, expect, needle = SOURCE[name]
            if name == "p2-revert-8b78a8fd":
                mutant = M("p2", "maap/maap.c", ASSERT_INC, "#include <assert.h>\n", "rv32", "", "")
            copy = ctrl_mutants.plant(mutant, SCRATCH / "plants")
            if name == "p2-revert-8b78a8fd":
                target = copy / "maap/maap.c"
                text = target.read_text()
                assert text.count(ASSERT_USE) == 1
                target.write_text(text.replace(ASSERT_USE, "\t\tassert(!m->in_call);\n"))
            tree = Tree(copy, SCRATCH / "plants" / mutant.name / "build", reuse, BUILD)
            ok = run_arms(tree, expect, needle)
        print(f"== probe {name}: {'AS EXPECTED' if ok else 'UNEXPECTED'}")
        if not ok:
            bad.append(name)
    print(f"probes: {len(wanted) - len(bad)} of {len(wanted)} as expected{'; unexpected: ' + ', '.join(bad) if bad else ''}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
