#!/usr/bin/env python3
"""Summarize receipts/probes/<label>.<shape>.txt (one finding per line) by finding words."""
import sys
from pathlib import Path
KEYS = ("was lost on the clean reboot", "did not survive", "over the bound", "want exactly",
        "one faulty read held", "did not hold the writer", "re-attached live", "persisted something",
        "printed no boot line", "not the container it judged", "another valid container",
        "yet the boot offered", "does not name it unread", "on reads that returned different bytes",
        "generation was taken", "did not refuse the console", "named the slot on the console",
        "neither committed nor refused", "printed that it re-attached", "reloaded the window")
for f in sorted(Path(sys.argv[1]).glob("*.txt")):
    lines = [x for x in f.read_text().splitlines() if x.strip()]
    kinds = {k: sum(k in x for x in lines) for k in KEYS}
    print(f"{f.stem:<52} findings={len(lines):<4} " + ", ".join(f"'{k}': {v}" for k, v in kinds.items() if v))
