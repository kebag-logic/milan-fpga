"""Run only builder gate 23h and its missing-patch control at a candidate checkout.
Usage: python3 gate23h.py SOURCE  (MILAN_LITEX_PYTHON may name the LiteX interpreter)"""
import sys, time
from pathlib import Path
src = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(src / "sw/builder"))
t0 = time.time()
import test_builder as t
for fn in (t.test_toolchain_patches_are_applied, t.test_toolchain_patch_gate_bites):
    fn()
    print(f"RAN {fn.__name__} ok", flush=True)
print(f"gate23h: PASS ({time.time()-t0:.1f}s)")
