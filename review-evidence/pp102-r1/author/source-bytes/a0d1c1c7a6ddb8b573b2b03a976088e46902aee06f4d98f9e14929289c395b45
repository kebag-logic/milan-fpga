#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Listener transition-ROM image generator for KL_pp_acmp_listener
(docs/architecture/05 §6.3, figure F05.3).

Emits 128 lines of 8 hex digits (32-bit entries = P-ACMP-TROM-W), addressed
{event[3:0], state[2:0]}: 14 events x 8 states = 112 used cells, 16 padding
rows. ONE profile column — Milan. The plain-IEEE column is ABSENT:
P-EN-PLAIN-IEEE-PROFILE = 0 is the F01.5 default and a product decision; a
plain-IEEE build would generate a second image, never patch this one.

THE TABLE BELOW MIRRORS F05.3 ROW-BY-ROW AND CELL-BY-CELL; every emitted
line carries its F05.3 cell text so drift against the doc is reviewable
line-by-line. The independent check is tb/acmp_listener/sim_main.cpp, whose
C++ matrix model is transcribed from the same doc table WITHOUT this file:
the two transcriptions must agree through the DUT's behavior (MTXW).

Entry encoding (hdl/acmp/pp_acmp_pkg.sv):
    [2:0]  next_state          [19:3] A1..A17 action bitmap (bit i-1 = Ai)
    [20]   VALID (0 = em-dash) [21]   IGN ('ign' / 'note only': inert)
    [22]   COND_TK (dagger cells: the ROM carries the tk arm {next, A12};
           the executor swaps to {PWA, A17} when the record's tk_disc = 0)
    [31:23] 0
"""
import argparse

# F05.3 column key order = lsm_state_e codes (pp_acmp_pkg.sv)
STATES = ["UNB", "PWA", "PWD", "PWR", "PW2", "PWT", "SNR", "SOK"]
ST = {name: i for i, name in enumerate(STATES)}

DASH = "-"    # F05.3 em-dash: impossible cell
IGN = "ign"   # F05.3 'ign' / 'note only': no effect

# --------------------------------------------------------------------------
# F05.3 — Full matrix (Milan Table 5.30 + §5.5.3.5.1-.48), row by row.
# Cell grammar: 'NEXT/A1 A2 ...' | '-' | 'ign' | 'cond[/A8]' where 'cond' is
# the dagger cell 'tk? PWD/A12 : PWA/A17' (the optional '/A8' runs first).
# Every row below carries the doc's cell text as written in F05.3.
# --------------------------------------------------------------------------
MATRIX = [
    # F05.3 row 1: BIND_RX same talker+source
    #   UNB: — (impossible: nothing bound to equal, 05 §6.3 cell note)
    ("BIND_SAME", ["-",
                   "PWA/A1 A6 A3", "PWD/A1 A6 A3", "PWR/A1 A6 A3",
                   "PW2/A1 A6 A3", "PWT/A1 A6 A3", "SNR/A1 A6 A3",
                   "SOK/A1 A6 A3"]),
    # F05.3 row 2: BIND_RX new/different source
    ("BIND_NEW", ["PWR/A1 A2 A3 A4 A5",
                  "PWR/A1 A11 A9 A2 A3 A4 A5",
                  "PWR/A1 A11 A9 A2 A3 A4 A5",
                  "PWR/A1 A11 A9 A2 A3 A4 A5",
                  "PWR/A1 A11 A9 A2 A3 A4 A5",
                  "PWR/A1 A11 A9 A2 A3 A4 A5",
                  "PWR/A1 A11 A8 A9 A2 A3 A4 A5",
                  "PWR/A1 A11 A8 A9 A2 A3 A4 A5"]),
    # F05.3 row 3: UNBIND_RX
    ("UNBIND", ["UNB/A1 A7",
                "UNB/A1 A11 A9 A10 A7",
                "UNB/A1 A11 A9 A10 A7",
                "UNB/A1 A11 A9 A10 A7",
                "UNB/A1 A11 A9 A10 A7",
                "UNB/A1 A11 A9 A10 A7",
                "UNB/A1 A11 A8 A9 A10 A7",
                "UNB/A1 A11 A8 A9 A10 A7"]),
    # F05.3 row 4: GET_RX_STATE (always answered, state kept — F05.14)
    ("GETRX", ["UNB/A16", "PWA/A16", "PWD/A16", "PWR/A16",
               "PW2/A16", "PWT/A16", "SNR/A16", "SOK/A16"]),
    # F05.3 row 5: PROBE_RESP status = SUCCESS
    ("PROBE_OK", ["ign", "ign", "ign",
                  "SNR/A11 A15", "SNR/A11 A15",
                  "ign", "ign", "ign"]),
    # F05.3 row 6: PROBE_RESP status != SUCCESS (A14 captures the status)
    ("PROBE_FAIL", ["ign", "ign", "ign",
                    "PWT/A11 A14", "PWT/A11 A14",
                    "ign", "ign", "ign"]),
    # F05.3 row 7: T-ACMP-DELAY expiry
    ("TMR_DELAY", ["-", "-", "PWR/A5", "-", "-", "-", "-", "-"]),
    # F05.3 row 8: T-ACMP-CMD expiry (PWR: exact duplicate; PW2: A14(=7))
    ("TMR_CMD", ["-", "-", "-", "PW2/A13", "PWT/A14", "-", "-", "-"]),
    # F05.3 row 9: T-ACMP-RETRY expiry — dagger: tk? PWD/A12 : PWA/A17
    ("TMR_RETRY", ["-", "-", "-", "-", "-", "cond", "-", "-"]),
    # F05.3 row 10: T-ACMP-NOTK expiry — dagger: A8; tk? PWD/A12 : PWA/A17
    ("TMR_NOTK", ["-", "-", "-", "-", "-", "-", "cond/A8", "-"]),
    # F05.3 row 11: EVT_TK_DISCOVERED ('ign (note)' cells: the tk_disc
    #   bookkeeping flag still tracks the discovery SM — VALID gates it)
    ("TK_DISC", ["-", "PWD/A12", "ign", "ign", "ign", "ign", "ign", "ign"]),
    # F05.3 row 12: EVT_TK_DEPARTED (SNR/SOK: note only — reservation kept,
    #   Milan §5.5.3.5.41/.47)
    ("TK_DEP", ["-", "-",
                "PWA/A11 A17", "PWA/A11 A17", "PWA/A11 A17", "PWA/A11 A17",
                "ign", "ign"]),
    # F05.3 row 13: EVT_TK_REGISTERED — ONLY SNR. The SOK column is the
    #   documented reference-implementation bug (Table 5.30 'x'): a
    #   TalkerFailed rise in RSV_OK takes NO invented arc.
    ("TK_REG", ["-", "-", "-", "-", "-", "-", "SOK/A11", "-"]),
    # F05.3 row 14: EVT_TK_UNREGISTERED — dagger: A8; tk? PWD/A12 : PWA/A17
    ("TK_UNREG", ["-", "-", "-", "-", "-", "-", "-", "cond/A8"]),
]

# Entry encoding constants — MUST match pp_acmp_pkg.sv
ACT_LSB, VALID_B, IGN_B, COND_B = 3, 20, 21, 22


def encode(cell: str, state_ix: int) -> int:
    """One F05.3 cell -> one 32-bit ROM entry."""
    if cell == DASH:
        return 0                                    # VALID = 0: impossible
    if cell == IGN:
        return (1 << VALID_B) | (1 << IGN_B) | state_ix
    if cell.startswith("cond"):
        acts = 1 << (ACT_LSB + 12 - 1)              # the tk arm carries A12
        if cell == "cond/A8":
            acts |= 1 << (ACT_LSB + 8 - 1)
        elif cell != "cond":
            raise ValueError(cell)
        return (1 << VALID_B) | (1 << COND_B) | acts | ST["PWD"]
    nxt, alist = cell.split("/")
    acts = 0
    for tok in alist.split():
        assert tok.startswith("A"), cell
        n = int(tok[1:])
        assert 1 <= n <= 17, cell
        acts |= 1 << (ACT_LSB + n - 1)
    return (1 << VALID_B) | acts | ST[nxt]


def main() -> None:
    """Write the ROM image the CLI names: one line per F05.3 cell, each
    carrying the doc's cell text, then the unused-event-code padding."""
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="ltn_rom.hex")
    args = ap.parse_args()

    lines = []
    for evt_ix, (row, cells) in enumerate(MATRIX):
        assert len(cells) == 8, row
        for st_ix, cell in enumerate(cells):
            addr = (evt_ix << 3) | st_ix
            lines.append(f"{encode(cell, st_ix):08X} "
                         f"// [{addr:3d}] F05.3 {row} x {STATES[st_ix]}: {cell}")
    for addr in range(len(lines), 128):
        lines.append(f"{0:08X} // [{addr:3d}] pad (event codes 14/15 unused)")

    with open(args.out, "w") as f:
        f.write("// generated by gen_ltn_rom.py — the F05.3 Milan column; "
                "do not edit\n")
        f.write("\n".join(lines) + "\n")
    print(f"wrote {args.out}: 128 x 32 b, 112 F05.3 cells")


if __name__ == "__main__":
    main()
