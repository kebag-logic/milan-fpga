#!/usr/bin/env python3
"""Run only the REBOOT defects of sw/firmware/ctrl/test/plat_mutants.py through ctrl_mutants.campaign().

Usage: python3 -B reboot_plat_mutants.py <checkout> <output-dir>

MUTANTS is narrowed to the entries whose name starts with 'plat-reboot-', plus
'plat-loop-before-ready' (its anchor moved in the reviewed delta). The
campaign plants into its own copy under <output-dir>, never the checkout.
Exit 0 when every selected mutant is caught by its named test on its words.
"""
import sys
from pathlib import Path

checkout, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
import ctrl_mutants as cm  # noqa: E402

keep = tuple(m for m in cm.MUTANTS if m.name.startswith("plat-reboot-") or m.name == "plat-loop-before-ready")
print(f"selected {len(keep)} mutants: {[m.name for m in keep]}", flush=True)
cm.MUTANTS = keep
cm.unnamed_tests = lambda: []
output.mkdir(parents=True, exist_ok=True)
escaped = cm.campaign(output, output / "reuse", 4)
print("RESULT:", "ESCAPED" if escaped else "ALL CAUGHT", flush=True)
sys.exit(1 if escaped else 0)
