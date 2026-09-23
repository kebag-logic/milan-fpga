#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer-owned RV32 resolver controls (R227-2, issue #504 / PR #521).

Loads the resolver from a given checkout's sw/builder/test_builder.py and
runs literal-assembly probes written independently of the PR's own
controls. Each probe states the SOUND answer; a probe PASSES when the
resolver gives it. Probes are grouped:

  F1-*  the store-class root cause answered by the correction round;
  X-*   pre-existing lattice behaviour outside #504's scope, reported
        so it can be classified (run on the base as well as the head).

Usage: resolver_controls.py <checkout-root> [--json]
Exit status: 0 when every F1-* probe passes, 1 otherwise. X-* probes are
reported but never change the exit status.
"""

import importlib.util
import json
import re
import sys
from pathlib import Path


def load(root: Path):
    """Import the checkout's test_builder module under a unique name."""
    path = root / "sw/builder/test_builder.py"
    name = "tb_" + re.sub(r"\W", "_", str(root))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    soc = (root / "sw/litex/milan_soc.py").read_text()
    base = int(re.search(r"(?m)^MILAN_CSR_BASE\s*=\s*(0x[0-9A-Fa-f_]+)",
                         soc).group(1).replace("_", ""), 16)
    size = int(re.search(r"(?m)^MILAN_CSR_SIZE\s*=\s*(0x[0-9A-Fa-f_]+)",
                         soc).group(1).replace("_", ""), 16)
    return module, base, size


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    tb, W, SIZE = load(root)
    s32 = tb._rv32_s32
    OUT = 0x8000_1000  # an address outside the window the census would accept

    def stores(body: str) -> list:
        run = tb.rv32_run(tb.rv32_functions(f"probe:\n{body}\tret\n")["probe"], {})
        return [address for _at, (address, _v) in run["stores"]]

    def in_window(address) -> bool:
        if isinstance(address, int):
            return W <= address < W + SIZE
        return isinstance(address, tb.Rv32Range) and \
            address.hi >= W and address.lo < W + SIZE

    def kind(address) -> str:
        return address.kind if isinstance(address, tb.Rv32Where) else \
            type(address).__name__

    def refused(reported: list) -> bool:
        """What the census would refuse: a window hit, or any store it
        cannot place (everything except int/range/stack/sym)."""
        return any(in_window(a) or (isinstance(a, tb.Rv32Where) and
                                    a.kind not in ("stack", "sym"))
                   for a in reported)

    results = []

    def check(pid: str, ok: bool, detail) -> None:
        results.append({"id": pid, "pass": bool(ok), "detail": repr(detail)})

    li = lambda reg, value: f"\tli {reg},{s32(value)}\n"
    frame = "\taddi sp,sp,-32\n\tsw s0,28(sp)\n\taddi s0,sp,32\n"

    # ---- F1: every store class is reported at every word it writes ----
    exact = [
        ("F1-fsw-t1", li("t1", W) + "\tfsw fa0,4(t1)\n", [W + 4]),
        ("F1-fsd-neg-disp", li("a2", W + 8) + "\tfsd fs1,-8(a2)\n", [W, W + 4]),
        ("F1-fsd-misaligned", li("a2", W) + "\tfsd ft0,6(a2)\n",
         [W + 6, W + 8, W + 12]),
        ("F1-fsh", li("a3", W) + "\tfsh ft1,2(a3)\n", [W + 2]),
        ("F1-fsq-ending-in-window", li("a3", W - 12) + "\tfsq ft2,0(a3)\n",
         [W - 12, W - 8, W - 4, W]),
        ("F1-sh-straddle-below", li("a4", W) + "\tsh a5,-1(a4)\n", [W - 1, W]),
        ("F1-fsd-ends-below-window", li("a4", W - 8) + "\tfsd fa1,0(a4)\n",
         [W - 8, W - 4]),
        ("F1-fsd-misaligned-touches", li("a4", W - 7) + "\tfsd fa1,0(a4)\n",
         [W - 7, W - 4, W]),
        ("F1-sb-below-window", li("a4", W - 1) + "\tsb a5,0(a4)\n", [W - 1]),
    ]
    for amo in ("amoswap", "amoadd", "amoxor", "amoand", "amoor", "amomin",
                "amomax", "amominu", "amomaxu", "sc"):
        for order in ("", ".aq", ".rl", ".aqrl"):
            exact.append((f"F1-{amo}.w{order}",
                          li("a3", W) + f"\t{amo}.w{order} t0,t2,(a3)\n", [W]))
    for pid, body, want in exact:
        got = stores(body)
        check(pid, got == want, got)
    # boundary exactness: stores that end below the window are NOT hits
    bodies = {pid: body for pid, body, _want in exact}
    for pid in ("F1-fsd-ends-below-window", "F1-sb-below-window"):
        got = stores(bodies[pid])
        check(pid + "-not-hit", not any(in_window(a) for a in got), got)

    # loads are not stores, and their integer destination is forgotten
    got = stores(li("a3", W) + "\tflw ft0,0(a3)\n\tfld ft1,8(a3)\n"
                 "\tflh ft2,0(a3)\n\tflq ft3,0(a3)\n\tlr.w t0,(a3)\n"
                 "\tlr.w.aq t1,0(a3)\n\tlh t2,0(a3)\n\tlbu t3,0(a3)\n")
    check("F1-loads-report-none", got == [], got)
    got = stores(li("t0", OUT) + li("a3", 0x4000_0000) +
                 "\tlr.w.aqrl t0,0(a3)\n\tsw zero,0(t0)\n")
    check("F1-lr-dest-forgotten", refused(got) and OUT not in got, got)

    # the class fail-closed default
    for insn in ("c.fsw fa5,0(a4)", "c.fsd fa5,0(a4)", "c.sw a5,0(a4)",
                 "sd a4,0(a4)", "cbo.zero (a4)", "cbo.zero 0(a4)",
                 "vse32.v v1,(a4)", "vsse32.v v1,(a4),a5",
                 "amocas.w a3,a5,0(a4)", "amoswap.b a3,a5,0(a4)",
                 "amoadd.h a3,a5,0(a4)", "ssamoswap.w a3,a5,(a4)",
                 "prefetch.w 0(a4)"):
        got = stores(li("a4", 0x4000_0000) + f"\t{insn}\n")
        check(f"F1-unclassified[{insn}]",
              len(got) == 1 and kind(got[0]) == "unclassified", got)
    for insn in ("fsw fa5,sym,t0", "fsd fa5,sym,t0", "amoswap.w a5,0(a4)",
                 "sc.w a5,a4"):
        got = stores(li("a4", W) + f"\t{insn}\n")
        check(f"F1-unreadable[{insn}]",
              len(got) == 1 and kind(got[0]) == "unreadable", got)

    # atomic rd is forgotten; only amoswap carries its rs2 as the value
    for amo in ("amoadd.w", "amoor.w", "sc.w", "amoswap.w"):
        got = stores(li("a5", OUT) + li("a4", 0x4000_0000) +
                     f"\t{amo} a5,a6,0(a4)\n\tsw zero,0(a5)\n")
        check(f"F1-rd-forgotten[{amo}]", refused(got[1:]), got)
    got = stores(frame + li("a5", OUT) + "\tamoswap.w t0,a5,-20(s0)\n"
                 "\tlw a2,-20(s0)\n\tsw zero,0(a2)\n")
    check("F1-amoswap-value-carried", got[-1:] == [OUT], got)
    for amo in ("amoadd.w", "sc.w", "amoor.w"):
        got = stores(frame + li("a5", OUT) + "\tsw a5,-20(s0)\n"
                     f"\t{amo} t0,a5,-20(s0)\n\tlw a2,-20(s0)\n\tsw zero,0(a2)\n")
        check(f"F1-amo-slot-forgotten[{amo}]", refused(got), got)
    for insn in ("fsw fa5,-20(s0)", "fsd fa5,-24(s0)", "fsh fa5,-18(s0)",
                 "fsq fa5,-32(s0)"):
        got = stores(frame + li("a5", OUT) + "\tsw a5,-20(s0)\n"
                     f"\t{insn}\n\tlw a2,-20(s0)\n\tsw zero,0(a2)\n")
        check(f"F1-fp-slot-forgotten[{insn}]", refused(got), got)
    got = stores(frame + li("a5", OUT) + "\tlla a3,obj\n\tsw a5,4(a3)\n"
                 "\tfsd fa5,0(a3)\n\tlw a2,4(a3)\n\tsw zero,0(a2)\n")
    check("F1-sym-fsd-overlap-forgotten", refused(got[-1:]), got)
    got = stores(frame + li("a5", OUT) + "\tlla a3,obj\n\tsw a5,0(a3)\n"
                 "\tamoadd.w t0,a6,0(a3)\n\tlw a2,0(a3)\n\tsw zero,0(a2)\n")
    check("F1-sym-amo-forgotten", refused(got[-1:]), got)

    # ranged stores cover their whole footprint
    def ranged(base: int, store: str) -> list:
        return stores(
            frame + li("a4", base) + "\tsw a4,-24(s0)\n\tsw zero,-20(s0)\n"
            "\tj .L2\n.L3:\n\tlw a4,-24(s0)\n\tlw a5,-20(s0)\n\tadd a5,a4,a5\n"
            f"\t{store}\n\tlw a5,-20(s0)\n\taddi a5,a5,1\n\tsw a5,-20(s0)\n"
            ".L2:\n\tlw a4,-20(s0)\n\tli a5,64\n\tbltu a4,a5,.L3\n"
            "\tlw s0,28(sp)\n\taddi sp,sp,32\n")
    for store, width in (("sw zero,0(a5)", 4), ("fsd fa5,0(a5)", 8),
                         ("amoswap.w t0,zero,0(a5)", 4), ("fsw fa5,0(a5)", 4)):
        got = ranged(W - 64, store)
        check(f"F1-range-footprint[{store}]",
              any(in_window(a) for a in got) or refused(got), got)
    got = ranged(W - 64 - 8, "fsd fa5,0(a5)")
    check("F1-range-below-not-hit", not any(in_window(a) for a in got), got)

    # branch refinement may not mirror a slot a non-integer store rewrote
    for insn in ("fsw fa5,-20(s0)", "amoadd.w t0,a6,-20(s0)",
                 "fsd fa5,-24(s0)"):
        got = stores(
            frame + "\tlw a5,0(a1)\n\tsw a5,-20(s0)\n\tlw a4,-20(s0)\n"
            f"\t{insn}\n\tli a5,64\n\tbltu a4,a5,.L3\n\tj .L9\n"
            ".L3:\n\tlw a3,-20(s0)\n" + li("a2", 0x4000_0000) +
            "\tadd a3,a2,a3\n\tsw zero,0(a3)\n.L9:\n")
        check(f"F1-mirror-stopped[{insn}]", refused(got), got)

    # ---- X: pre-existing lattice behaviour, classified on base and head --
    got = stores(frame + li("a5", OUT) + "\tsw a5,-20(s0)\n"
                 "\taddi a4,s0,-20\n" + li("a3", W) +
                 "\tsw a3,0(a4)\n\tlw a2,-20(s0)\n\tli a1,1\n\tsw a1,0(a2)\n")
    check("X-stack-alias-overwrites-slot", refused(got[-1:]), got)
    got = stores(frame + li("a5", 0x1_0000) + "\tsw a5,-20(s0)\n"
                 "\tlhu a4,-20(s0)\n" + li("a3", W + 0x600) +
                 "\tadd a4,a4,a3\n\tsw zero,0(a4)\n")
    check("X-subword-slot-load", refused(got), got)
    got = stores(frame + li("a5", W + 0x600) + "\tsw a5,-20(s0)\n" +
                 li("a4", 0x8000_0000 | ((W + 0x600) & 0xFF)) +
                 "\tsb a4,-20(s0)\n\tlw a2,-20(s0)\n\tsw zero,0(a2)\n")
    check("X-subword-slot-store", refused(got), got)

    f1 = [r for r in results if r["id"].startswith("F1-")]
    xs = [r for r in results if r["id"].startswith("X-")]
    if "--json" in sys.argv:
        print(json.dumps(results, indent=1))
    for r in results:
        print(("PASS " if r["pass"] else "FAIL ") + r["id"] + "  " +
              r["detail"][:160])
    print(f"SUMMARY root={root.name} F1 {sum(r['pass'] for r in f1)}/{len(f1)} "
          f"X {sum(r['pass'] for r in xs)}/{len(xs)}")
    return 0 if all(r["pass"] for r in f1) else 1


if __name__ == "__main__":
    sys.exit(main())
