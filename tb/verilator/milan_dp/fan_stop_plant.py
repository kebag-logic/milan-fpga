#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""fan_stop_plant.py SOURCE OUT PLANT - a datapath whose stop gate is not per input, for fan-stop-plants.

Milan v1.2 5.3.8.7 stops a Stream Input, not a stream: when one of the inputs bound to a talker stream is
stopped, the others go on receiving every PDU. The datapath gates the depacketizer's verdict mask input by input
(#948). Each plant replaces that gate with one that is not, so sim_nxn.cpp's [FAN] STOP legs must fail:

  shared     a stopped input among a PDU's accepting inputs discards the PDU for all of them
  one-index  the accept pulse's one-index stop (the last accepting input's) gates every input's share

The one line it replaces must appear exactly once, or the plant refuses: a plant that changes nothing proves
nothing.
"""
import sys
from pathlib import Path

LINE = "      avtprx_done_mask_w & ~acmpl_stopped_v_w[N_STREAMS-1:0];\n"
PLANTS = {
    "shared": "      avtprx_done_mask_w &\n"
              "      ~{N_STREAMS{|(avtprx_done_mask_w & acmpl_stopped_v_w[N_STREAMS-1:0])}};\n",
    "one-index": "      avtprx_done_mask_w & ~{N_STREAMS{avtprx_stopped_w}};\n",
}


def main() -> int:
    """Write the planted copy; 1 when the line is not there exactly once or the plant is unknown."""
    if len(sys.argv) != 4 or sys.argv[3] not in PLANTS:
        print(__doc__, file=sys.stderr)
        return 2
    text = Path(sys.argv[1]).read_text()
    if text.count(LINE) != 1:
        print(f"fan_stop_plant: the line appears {text.count(LINE)} time(s) in {sys.argv[1]}, expected 1",
              file=sys.stderr)
        return 1
    Path(sys.argv[2]).write_text(text.replace(LINE, PLANTS[sys.argv[3]]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
