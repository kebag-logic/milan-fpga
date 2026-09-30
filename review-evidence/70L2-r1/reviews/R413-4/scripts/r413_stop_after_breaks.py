#!/usr/bin/env python3
"""Instrument a SCRATCH tree's gate 1b to stop right after its verdict
controls: the interior-byte premise, the AEM-first base (slot kept), the
forget-on-call refusal and all planted pin breaks graded.

usage: r413_stop_after_breaks.py <tree>

With R413_STOP=1 in the environment the gate prints what those controls
recorded and exits 0 there; a control that fails raises before the anchor
and run_gate1b.py prints the refusal. The rest of the gate (store-class,
CRC and later controls, none of which grades the verdict's pins) is not run.
"""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "sw/builder/test_builder.py"
text = path.read_text()
anchor = ("    #: ... and the store-class mutants measured on the resolver ALONE, so\n")
assert text.count(anchor) == 1
probe = '''    if os.environ.get("R413_STOP"):
        print("R413 verdict controls: ran=%s kept=%s refused=%d/%d "
              "interior_bytes=%s" % (
                  baseline_census_verdict["ran"], accepted.get("kept"),
                  len(verdict_pin_refused), len(verdict_pin_breaks),
                  verdict_interior_bytes), flush=True)
        raise SystemExit(0)
'''
path.write_text(text.replace(anchor, probe + anchor, 1))
print("instrumented", path)
