#!/usr/bin/env python3
"""In a tree COPY, raise a sentinel right after gate 1b's verdict-break loop,
carrying the kept slot, the refused count and the interior bytes, so a
mutant run need not execute the rest of the profile contract.
usage: plant_stop.py <tree>"""
import sys
from pathlib import Path
path = Path(sys.argv[1]) / "sw/builder/test_builder.py"
text = path.read_text()
anchor = ("    #: ... and the store-class mutants measured on the resolver ALONE, "
          "so\n")
assert text.count(anchor) == 1, text.count(anchor)
stop = (
    "    if baseline_census_verdict[\"ran\"]:\n"
    "        class R413StopAfterBreaks(Exception):\n"
    "            pass\n"
    "        raise R413StopAfterBreaks(\n"
    "            f\"kept={accepted['kept']} \"\n"
    "            f\"refused={len(verdict_pin_refused)}/{len(verdict_pin_breaks)} \"\n"
    "            f\"interior_bytes={verdict_interior_bytes}\")\n")
path.write_text(text.replace(anchor, stop + anchor, 1))
print(f"planted stop in {path}")
