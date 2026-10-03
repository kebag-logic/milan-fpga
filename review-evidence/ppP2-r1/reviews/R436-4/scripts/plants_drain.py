#!/usr/bin/env python3
"""R436-3 plants in the owed READ's drain bound (KL_pp_nvm_port.sv), each an
exact single-occurrence edit. `plants_drain.py list` prints names;
`plants_drain.py apply NAME RTL` edits RTL in place (refuses if the anchor is
not found exactly once)."""
import sys
from pathlib import Path

L_RHCOLL = "  assign left_w  = (state_r == S_RHCOLL) ? (HDR_LEN_C - 16'(hidx_r))"
L_RPPUMP = "                 : (state_r == S_RPPUMP) ? (plen_r - bcnt_r)"
L_OTHER  = "                 : dev_len_o;"
DEC      = "    else if (drain_w && dev_rvalid_i) owed_left_r <= owed_left_r - 16'd1;"
DECL     = "  logic       [15:0] owed_left_r;   // ...as many as it still owes"
RREADY   = "                      || drain_w;                      // the owed READ's drain"

PLANTS = {
    # header read abandoned in S_RHCOLL: owes its whole 8, bytes moved ignored
    "Z1": [(L_RHCOLL, "  assign left_w  = (state_r == S_RHCOLL) ? HDR_LEN_C")],
    # payload read abandoned in S_RPPUMP: owes its whole length
    "Z2": [(L_RPPUMP, "                 : (state_r == S_RPPUMP) ? plen_r")],
    # a READ whose bytes all moved (S_RHWAIT / S_RPWAIT) still owes 8
    "Z3": [(L_OTHER, "                 : ((state_r == S_RHWAIT) || (state_r == S_RPWAIT)) ? 16'd8 : dev_len_o;")],
    # a READ request withdrawn and granted late owes nothing (underdrain)
    "Z4": [(L_OTHER, "                 : 16'd0;")],
    "Z5": [(L_RPPUMP, "                 : (state_r == S_RPPUMP) ? (plen_r - bcnt_r + 16'd1)")],
    "Z6": [(L_RPPUMP, "                 : (state_r == S_RPPUMP) ? (plen_r - bcnt_r - 16'd1)")],
    "Z7": [(L_RHCOLL, "  assign left_w  = (state_r == S_RHCOLL) ? (HDR_LEN_C - 16'(hidx_r) - 16'd1)")],
    "Z8": [(L_RHCOLL, "  assign left_w  = (state_r == S_RHCOLL) ? (HDR_LEN_C - 16'(hidx_r) + 16'd1)")],
    # the count decremented on any byte while owed: wraps past zero
    "Z9": [(DEC, "    else if (owed_r && dev_rvalid_i)  owed_left_r <= owed_left_r - 16'd1;")],
    # the count 8 bits wide: a READ owing 256 or more is under-drained
    "Z10": [(DECL, "  logic        [7:0] owed_left_r;   // ...as many as it still owes")],
    # rready unbounded, the count kept
    "Z11": [(RREADY, "                      || (owed_r && owed_rd_r);        // the owed READ's drain")],
    # a late-granted READ request owes one byte fewer than its length
    # Z10 spelled lint-clean (Z10 itself fails elab_bounds.sh's -Wall on width)
    "Z10b": [(DECL, "  logic        [7:0] owed_left_r;   // ...as many as it still owes"),
             ("    else if (dl_w && !owed_r)         owed_left_r <= left_w;",
              "    else if (dl_w && !owed_r)         owed_left_r <= left_w[7:0];"),
             (DEC, "    else if (drain_w && dev_rvalid_i) owed_left_r <= owed_left_r - 8'd1;"),
             ("  assign drain_w = owed_r && owed_rd_r && (owed_left_r != 16'd0);",
              "  assign drain_w = owed_r && owed_rd_r && (owed_left_r != 8'd0);")],
    "Z12": [(L_OTHER, "                 : (dev_len_o - 16'd1);")],
}

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
