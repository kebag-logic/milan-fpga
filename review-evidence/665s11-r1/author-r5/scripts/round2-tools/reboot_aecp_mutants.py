#!/usr/bin/env python3
"""Run only the REBOOT defects of sw/firmware/ctrl/test/aecp_mutants.py through its own campaign().

Usage: python3 -B reboot_aecp_mutants.py <checkout> <output-dir>

The driver's table-drift control runs first over the whole table, unchanged;
then DEFECTS is narrowed to the entries whose name starts with 'reboot-'. The
campaign plants into its own copy under <output-dir>/work, never the checkout.
Exit 0 when every selected defect is caught on its own words.
"""
import sys
from pathlib import Path

checkout, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
import aecp_mutants as m  # noqa: E402

m.controls()
m.DEFECTS = tuple(d for d in m.DEFECTS if d.name.startswith("reboot-"))
m.controls = lambda: None
print(f"selected {len(m.DEFECTS)} REBOOT defects: {[d.name for d in m.DEFECTS]}", flush=True)
print(f"tsn-c-stack at {m.stack_pin(m.STACK.resolve())}", flush=True)
escaped = m.campaign(output, jobs=4, stack=m.STACK.resolve())
print("RESULT:", "ESCAPED" if escaped else "ALL CAUGHT", flush=True)
sys.exit(1 if escaped else 0)
