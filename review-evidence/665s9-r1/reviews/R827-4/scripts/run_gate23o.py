"""Run builder gate 23o (test_placement_recipe) alone on the checkout in the
current directory, and list the path labels build() writes for one config.

    cd <checkout> && python3 -B /path/to/run_gate23o.py
Exit 0 when the gate passes, 1 when it fails.
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw" / "builder"))
spec = importlib.util.spec_from_file_location("test_builder", ROOT / "sw" / "builder" / "test_builder.py")
tb = importlib.util.module_from_spec(spec)
sys.modules["test_builder"] = tb
spec.loader.exec_module(tb)
eb = tb.eb
print("labels gate 23o compares:", ", ".join(tb.RECIPE_SHAPE_ARTIFACTS))
with tempfile.TemporaryDirectory() as tmp:
    for placement in (None, "split"):
        kw = {"placement": placement} if placement else {}
        r = eb.build(str(tb.CONFIGS["ax7101_1x1_tdm8"]), str(Path(tmp) / str(placement)), **kw)
        held = [lbl for lbl in tb.RECIPE_SHAPE_ARTIFACTS if lbl in r["paths"]]
        absent = [lbl for lbl in tb.RECIPE_SHAPE_ARTIFACTS if lbl not in r["paths"]]
        print(f"ax7101_1x1_tdm8 placement={placement or 'all-fabric'}: labels written {sorted(r['paths'])}")
        print(f"  gate labels present: {len(held)}; absent: {absent}")
try:
    tb.test_placement_recipe()
except AssertionError as exc:
    print(f"GATE 23o FAILED: {exc}")
    sys.exit(1)
print("GATE 23o PASSED")
