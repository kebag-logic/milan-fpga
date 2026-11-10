"""Run the store gate's compile-time controls alone at the shipping 1x1 shape (a quick check, not a gate)."""
import sys, tempfile
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as t, fw_gtest
with tempfile.TemporaryDirectory(prefix="controls.") as tmp:
    w = Path(tmp)
    shape = t.prepare(root / "configs" / f"{t.SELF_TEST_SHAPE}.yaml", w / "shape")
    b = fw_gtest.Build(jobs=8)
    found = []
    for f in (t.over_capacity_control, t.over_width_control, t.at_width_control, t.doctored_control):
        found += f(shape, w / f.__name__, b)
    print("\n".join(found) or "every control caught")
    sys.exit(bool(found))
