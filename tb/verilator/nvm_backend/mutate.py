#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant ONE defect into a copy of hdl/milan/KL_nvm_backend.sv for a negative control.

The Makefile builds each mutated copy with the same harness and requires the
run to FAIL. A mutation is planted by matching the shipping text exactly, so a
refactor that moves the line the control depends on stops the build loudly
("pattern hit 0 times") instead of letting the control pass against code it
no longer touches.

  alias       the output channel-map group reads the INPUT table (round 3's
              one-table-for-both-directions defect)
  stride      the output map group's base advances by a NOMINAL per-port
              stride instead of the sum of the actual input record lengths
  stale_mask  round 3's keep-the-latch stale machine: cleared only by reset,
              the published bit masked by (backed and not dirty)
  blind_read  a READ serves image bytes before the firmware validated the
              image, instead of answering blank flash

usage: mutate.py <name> <source.sv> <destination.sv>
"""
from __future__ import annotations

import sys
from pathlib import Path

MUTATIONS: dict[str, list[tuple[str, str]]] = {
    "alias": [
        ("      rec_base_w = b_mapo_w + 18'(mapo_pref_r[mapo_idx_w]);\n"
         "      rec_len_w  = 12'(mapo_len_r[mapo_idx_w]);\n",
         "      rec_base_w = b_mapo_w + 18'(mapi_pref_r[MAPI_IW_C'(mapo_idx_w)]);\n"
         "      rec_len_w  = 12'(mapi_len_r[MAPI_IW_C'(mapo_idx_w)]);\n"),
    ],
    "stride": [
        ("  assign b_mapo_w = 18'(B_MAPI_C)\n"
         "                  + 18'(mapi_pref_r[MAPI_IW_C'(N_SPORT_IN_P  - 1)])\n"
         "                  + 18'(mapi_len_r [MAPI_IW_C'(N_SPORT_IN_P  - 1)]);\n",
         "  assign b_mapo_w = 18'(B_MAPI_C) + 18'(N_SPORT_IN_P * (REC_HDR_C + 256));\n"),
    ],
    "stale_mask": [
        ("  assign stale_n_w = loss_w                    ? 1'b1\n"
         "                   : (backed_n_w & ~dirty_n_w) ? 1'b0\n"
         "                                               : stale_r;\n",
         "  assign stale_n_w = loss_w ? 1'b1 : stale_r;\n"),
        ("  assign nvm_stale_o   = stale_r;\n",
         "  assign nvm_stale_o   = stale_r & ~(backed_r & ~dirty_r);\n"),
    ],
    "blind_read": [
        ("                OP_READ_C:  st_r <= img_live_w ? S_RDFETCH : S_RDBLANK;\n",
         "                OP_READ_C:  st_r <= (img_live_w | ~img_live_w) ? S_RDFETCH : S_RDBLANK;\n"),
    ],
}


def main(argv: list[str]) -> int:
    """Write the mutated copy; a pattern that does not hit exactly once is a hard failure."""
    if len(argv) != 4 or argv[1] not in MUTATIONS:
        print(__doc__, file=sys.stderr)
        return 2
    name, source, destination = argv[1], Path(argv[2]), Path(argv[3])
    text = source.read_text(encoding="utf-8")
    for old, new in MUTATIONS[name]:
        hits = text.count(old)
        if hits != 1:
            print(f"mutate.py {name}: pattern hit {hits} times, expected exactly 1; "
                  f"the shipping text moved and this control must be re-anchored",
                  file=sys.stderr)
            return 1
        text = text.replace(old, new)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
