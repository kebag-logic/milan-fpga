#!/usr/bin/env python3
"""Run gate 1b (test_baremetal_profile_contract) alone on a checkout.

Usage: run_gate1b.py <checkout>
Imports sw/builder/test_builder.py without its __main__ block, runs only the
bare-metal profile contract (the gate that reads the composed builder, the
firmware page and the datapath), then prints the arms it declined.
"""
import sys, time, runpy
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.argv = [str(root / "sw/builder/test_builder.py")]
sys.path.insert(0, str(root / "sw/builder"))
t0 = time.monotonic()
mod = runpy.run_path(str(root / "sw/builder/test_builder.py"), run_name="gate1b_only")
mod["test_baremetal_profile_contract"]()
skipped = mod["SKIPPED"]
print(f"\ngate1b elapsed {time.monotonic() - t0:.1f} s")
for gate, why, kind in skipped:
    print(f"NOT RUN [{gate}] ({kind}) {why}")
print(f"GATE1B PASS, {len(skipped)} arm(s) NOT RUN")
