#!/usr/bin/env python3
"""R227-4 supplementary literal-assembly probes, outside the delta.

Usage: extra_probes.py <sw/builder dir of a tree copy>

Runs the resolver exactly as the gate's own `rv32_probe` helper does
(rv32_functions + rv32_run over one `probe:` body, no data) and prints the
store addresses each body reports. Each body parks 0x80001000 in a modelled
word, rewrites that word, reloads it and stores through it; a final store
placed at 2147487744 (0x80001000) is a stale read-back, `unplaced` is sound.
"""

import json
import sys

sys.path.insert(0, sys.argv[1])
import test_builder as tb  # noqa: E402

OUTSIDE = 0x8000_1000
FRAME = ("\taddi sp,sp,-32\n\tsw s0,28(sp)\n\taddi s0,sp,32\n"
         f"\tli a5,{tb._rv32_s32(OUTSIDE)}\n")
STATIC = FRAME + "\tlla a3,probe_static\n"
TAIL = "\tli a2,1\n\tsw a2,0(a4)\n"

BODIES = {
    # HIGH boundary of _rv32_forget_overlap: a misaligned store whose LAST
    # byte is the parked word's FIRST byte.
    "high-frame-sh-ending-on-slot":
        FRAME + "\tsw a5,-20(s0)\n\tsh zero,-21(s0)\n\tlw a4,-20(s0)\n",
    "high-static-sw-ending-on-word":
        STATIC + "\tsw a5,4(a3)\n\taddi a2,a3,1\n\tsw zero,0(a2)\n"
        "\tlw a4,4(a3)\n",
    # ... and one byte short of it (must keep the word).
    "high-frame-sh-one-short":
        FRAME + "\tsw a5,-20(s0)\n\tsh zero,-22(s0)\n\tlw a4,-20(s0)\n",
    # The compiled spelling measured in receipts/align_static_probe.s.txt:
    # GCC folds `(char *)&g + 1` into `lla a5,g+1`.
    "addend-spelling-misaligned-static":
        STATIC + "\tsw a5,4(a3)\n\tlla a2,probe_static+1\n\tsw zero,0(a2)\n"
        "\tlw a4,4(a3)\n",
    "addend-spelling-whole-word-static":
        STATIC + "\tsw a5,4(a3)\n\tlla a2,probe_static+4\n\tsw zero,0(a2)\n"
        "\tlw a4,4(a3)\n",
}


def reported(body: str) -> list[str]:
    """The store addresses the resolver reports, as the gate's helper."""
    run = tb.rv32_run(tb.rv32_functions(f"probe:\n{body}\tret\n")["probe"], {})
    return [repr(address) for _at, (address, _v) in run["stores"]]


for label, body in BODIES.items():
    print(json.dumps({"probe": label, "stores": reported(body + TAIL)}))
