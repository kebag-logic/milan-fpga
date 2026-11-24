#!/usr/bin/env python3
"""Run tb/verilator/gptp_shadow/mutants.py's own main() on the named controls.
Usage: campaign_slice.py REPO NAME...

The driver's private input copy, detection rule and tally are its own; only
the population is narrowed to the named controls.
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
names = sys.argv[2:]
sys.path.insert(0, str(repo / "tb" / "verilator" / "gptp_shadow"))
sys.argv = [sys.argv[0]]
import mutants  # noqa: E402

whole = list(mutants.MUTATIONS)
print("population:", len(whole), [row[0] for row in whole], flush=True)
mutants.MUTATIONS[:] = [row for row in whole if row[0] in names]
assert len(mutants.MUTATIONS) == len(names), names
sys.exit(mutants.main())
