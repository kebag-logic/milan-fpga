#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_fanout_plant.py SOURCE OUT - the parser with the defect #948 found, for twin-fanout-plants.

The planted copy hands each PDU to the highest matching table entry alone, as the parser did before #948, so
twin_split.cpp --fanout must fail on the first of two inputs bound to one stream. The one line it replaces must
appear exactly once, or the plant refuses: a plant that changes nothing proves nothing.
"""
import sys
from pathlib import Path

LINE = "          match_vec_o      <= match_vec;\n"
PLANT = "          match_vec_o      <= N_STREAMS'(1) << match_idx;\n"


def main() -> int:
    """Write the planted copy; 1 when the line is not there exactly once."""
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    text = Path(sys.argv[1]).read_text()
    if text.count(LINE) != 1:
        print(f"twin_fanout_plant: the line appears {text.count(LINE)} time(s) in {sys.argv[1]}, expected 1",
              file=sys.stderr)
        return 1
    Path(sys.argv[2]).write_text(text.replace(LINE, PLANT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
