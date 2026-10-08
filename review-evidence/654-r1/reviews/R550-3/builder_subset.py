"""Run the builder-bank arms this composition can affect, at the current checkout.

Arms: the PR's registered refusal bank (test_soc_option_refusals) and the
predecessor-touched toolchain patch gate 23h with its negative control. Any
recorded skip is a failure here: this subset exists to prove these arms ran.
Run with the LiteX interpreter from the repository root: python -I <this>.
"""
import os
import sys
from pathlib import Path

repo = Path.cwd()
sys.path.insert(0, str(repo / "sw/builder"))
os.chdir(repo / "sw/builder")
import test_builder as tb  # noqa: E402

arms = (tb.test_soc_option_refusals,
        tb.test_toolchain_patches_are_applied,
        tb.test_toolchain_patch_gate_bites)
for fn in arms:
    print(f"== {fn.__name__}", flush=True)
    fn()
    print(f"== {fn.__name__} returned", flush=True)
if tb.SKIPPED:
    print(f"SKIPPED arms: {tb.SKIPPED}")
    sys.exit(1)
print(f"builder subset: {len(arms)}/{len(arms)} arms ran, no skip recorded")
