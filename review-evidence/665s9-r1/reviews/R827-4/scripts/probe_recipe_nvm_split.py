"""Probe: does builder gate 23o (test_placement_recipe) hold the split recipe's
nvm_split.json to the all-fabric build's, as it holds its other shape artifacts?

Run from a checkout of the tree under review:  python3 -B probe_recipe_nvm_split.py
No file in the checkout is edited; every change below is an in-memory patch of
one process.

  1. FACT: for every config gate 23o walks, the all-fabric build's nvm_split.json
     and the split recipe's are compared byte for byte (expected equal today).
  2. PLANT: _derive_artifacts is wrapped so that the split recipe alone writes a
     different nvm_split (its first block's count plus one), then gate 23o runs.
     If the gate stays green, it does not hold that artifact.
Exit 0 when the probe ran to completion (the verdicts are printed), 2 on error.
"""
import copy
import dataclasses
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
    sample = eb.build(str(tb.CONFIGS["ax7101_1x1_tdm8"]), str(Path(tmp) / "labels"))
    print("labels build() writes:", ", ".join(sorted(sample["paths"])))
    for name, path in tb.CONFIGS.items():
        fabric = eb.build(str(path), str(Path(tmp) / name / "fabric"))
        split = eb.build(str(path), str(Path(tmp) / name / "split"), placement="split")
        a, b = fabric["paths"].get("nvm_split"), split["paths"].get("nvm_split")
        same = a is not None and b is not None and Path(a).read_bytes() == Path(b).read_bytes()
        print(f"FACT {name}: split recipe's nvm_split.json equals the all-fabric build's: {same}")

real = eb._derive_artifacts


def planted(config_path, placement=None):
    art = real(config_path, placement)
    if placement == "split":
        changed = copy.deepcopy(art.nvm_split)
        changed["blocks"][0]["count"] += 1
        art = dataclasses.replace(art, nvm_split=changed)
    return art


eb._derive_artifacts = planted
try:
    tb.test_placement_recipe()
    print("PLANT the split recipe writes a different nvm_split.json: gate 23o PASSED (not caught)")
except AssertionError as exc:
    print(f"PLANT the split recipe writes a different nvm_split.json: gate 23o FAILED (caught): {str(exc)[:300]}")
finally:
    eb._derive_artifacts = real

# 3. FIX CHECK (in memory only): with nvm_split added to the gate's labels, the
#    unplanted gate must stay green and the plant must turn it red.
tb.RECIPE_SHAPE_ARTIFACTS = (*tb.RECIPE_SHAPE_ARTIFACTS, "nvm_split")
try:
    tb.test_placement_recipe()
    print("FIX-CHECK unplanted gate with nvm_split held: PASSED")
except AssertionError as exc:
    print(f"FIX-CHECK unplanted gate with nvm_split held: FAILED: {str(exc)[:300]}")
eb._derive_artifacts = planted
try:
    tb.test_placement_recipe()
    print("FIX-CHECK plant with nvm_split held: gate 23o PASSED (not caught)")
except AssertionError as exc:
    print(f"FIX-CHECK plant with nvm_split held: gate 23o FAILED (caught): {str(exc)[:200]}")
finally:
    eb._derive_artifacts = real
