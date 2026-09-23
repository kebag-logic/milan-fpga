#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R227-3 literal-assembly probes of the RV32 resolver in a given tree.

Usage: literal_probes.py <tree> [--m15]

Imports <tree>/sw/builder/test_builder.py (bytecode writing disabled) and runs
rv32_run() over hand-written assembly, printing the store addresses it reports
as JSON. With --m15 the tree must already carry the M15 boundary mutation; the
script only labels its output. The CSR window is 0x90000000..0x9000ffff and
ADP_CTRL is 0x90000600 (both read from the gate's own run log).
"""
import json
import sys

sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path.insert(0, f"{tree}/sw/builder")
sys.path.insert(0, f"{tree}/scripts")
import test_builder as tb  # noqa: E402

FRAME = "\taddi sp,sp,-32\n\tsw s0,28(sp)\n\taddi s0,sp,32\n"
PROBES = {
    # Read-side sibling of R227-2-F1: park 0x12340600, read the low HALF at
    # the slot's own offset (real value 0x0600), OR in the window page.
    # Real store address 0x90000600 (ADP_CTRL); the lattice reads the whole
    # word and places the store at 0x92340600, outside the window.
    "halfword-read": FRAME + "\tli a5,305399296\n\tsw a5,-24(s0)\n"
                     "\tlhu a4,-24(s0)\n\tli a3,-1879048192\n\tor a4,a4,a3\n"
                     "\tli a2,1\n\tsw a2,0(a4)\n",
    # The same with a whole-word read and the low half masked: the control.
    "wholeword-read-masked": FRAME + "\tli a5,305399296\n\tsw a5,-24(s0)\n"
                             "\tlw a4,-24(s0)\n\tli a1,65535\n\tand a4,a4,a1\n"
                             "\tli a3,-1879048192\n\tor a4,a4,a3\n"
                             "\tli a2,1\n\tsw a2,0(a4)\n",
    # The same half-word read of a STATIC: only `lw` reads a static's word.
    "halfword-read-static": FRAME + "\tlla a6,probe_static\n\tli a5,305399296\n"
                            "\tsw a5,0(a6)\n\tlhu a4,0(a6)\n\tli a3,-1879048192\n"
                            "\tor a4,a4,a3\n\tli a2,1\n\tsw a2,0(a4)\n",
    # _rv32_forget_overlap() low boundary: a byte store into the TOP byte
    # (offset 3) of a parked word 0x12000600; real word becomes 0x90000600.
    "top-byte-store-frame": FRAME + "\tli a5,301991424\n\tsw a5,-24(s0)\n"
                            "\tli a4,144\n\tsb a4,-21(s0)\n\tlw a3,-24(s0)\n"
                            "\tli a2,1\n\tsw a2,0(a3)\n",
    "top-byte-store-static": FRAME + "\tlla a6,probe_static\n\tli a5,301991424\n"
                             "\tsw a5,0(a6)\n\tli a4,144\n\tsb a4,3(a6)\n"
                             "\tlw a3,0(a6)\n\tli a2,1\n\tsw a2,0(a3)\n",
}


def fmt(address):
    return f"0x{address:08x}" if isinstance(address, int) else repr(address)


def main():
    out = {"tree": tree, "label": "M15" if "--m15" in sys.argv else "as-is"}
    for name, body in PROBES.items():
        run = tb.rv32_run(tb.rv32_functions(f"probe:\n{body}\tret\n")["probe"], {})
        stores = [address for _at, (address, _v) in run["stores"]]
        last = stores[-1]
        in_window = isinstance(last, int) and 0x90000000 <= last < 0x90010000
        out[name] = {"stores": [fmt(a) for a in stores],
                     "final_store": fmt(last),
                     "final_store_judged": ("in window: refused by rule 1" if in_window
                                            else "placed outside: ACCEPTED by rule 1"
                                            if isinstance(last, int)
                                            else f"{getattr(last, 'kind', '?')}: rule 1b")}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
