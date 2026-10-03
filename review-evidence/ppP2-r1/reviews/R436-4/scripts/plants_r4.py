#!/usr/bin/env python3
"""R436-4 reviewer plants (never proposed as the PR's code), each an exact
single-occurrence edit of KL_pp_nvm_port.sv at the exact head.
W9-W15: the owed count N bits wide, lint-clean spelling (as R436-3's Z10b at 8):
the suite's T28j owes at most 1,024, so widths 11-15 can only be caught by the
randomized harness's READ of the largest legal payload (65,527).
Y1: an abandoned command is always taken as a READ (owed_rd_r set for a WRITE).
`plants_r4.py list` | `plants_r4.py apply NAME RTL`."""
import sys
from pathlib import Path

DECL = "  logic       [15:0] owed_left_r;   // ...as many as it still owes"
LOAD = "    else if (dl_w && !owed_r)         owed_left_r <= left_w;"
DEC = "    else if (drain_w && dev_rvalid_i) owed_left_r <= owed_left_r - 16'd1;"
DRAIN = "  assign drain_w = owed_r && owed_rd_r && (owed_left_r != 16'd0);"


def width(n):
    return [(DECL, f"  logic       [{n-1}:0] owed_left_r;   // ...as many as it still owes"),
            (LOAD, f"    else if (dl_w && !owed_r)         owed_left_r <= left_w[{n-1}:0];"),
            (DEC, f"    else if (drain_w && dev_rvalid_i) owed_left_r <= owed_left_r - {n}'d1;"),
            (DRAIN, f"  assign drain_w = owed_r && owed_rd_r && (owed_left_r != {n}'d0);")]


PLANTS = {f"W{n}": width(n) for n in range(9, 16)}
PLANTS["Y1"] = [("      if (dl_w && !owed_r) owed_rd_r <= rd_st_w;",
                 "      if (dl_w && !owed_r) owed_rd_r <= 1'b1;")]


def main():
    if sys.argv[1] == "list":
        print(" ".join(PLANTS)); return 0
    name, rtl = sys.argv[2], Path(sys.argv[3])
    t = rtl.read_text()
    for old, new in PLANTS[name]:
        n = t.count(old)
        if n != 1:
            print(f"{name}: anchor found {n} times: {old!r}"); return 2
        t = t.replace(old, new)
    rtl.write_text(t)
    print(f"{name}: applied {len(PLANTS[name])} edit(s)")
    return 0


sys.exit(main())
