"""Re-run the unchanged published fixture builders against production."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
checkout = Path(sys.argv[1]).resolve()
checker = checkout / "scripts/check_merge_containment.py"
sys.path.insert(0, str(checker.parent))
import check_merge_containment as mc
import merge_containment_replay as proof
from merge_containment_selftest_scratch import quiet_git

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def components(mod, branch):
    paths = proof._retained_at_tip(branch, "main", mc._git)
    return dict(G_shape=proof._redundant_merge_shape(branch, "main", mc._git),
                H_replay=mc._linear_patches_contained(branch, "main")[0],
                T_retained=not paths, T_detail=paths)

saved = sys.argv
sys.argv = ["fixtures.py", str(root / "baseline/check_merge_containment.py"),
            str(checker), str(root / "public-fixtures"), str(root / "receipts/public-matrix.json")]
fixtures = load("published_fixtures", root / "public/scripts/fixtures.py")
sys.argv = saved
fixtures.components = components  # Adapter only for the production helper interface.
with quiet_git():
    result = fixtures.main()
record = json.loads((root / "receipts/public-matrix.json").read_text())
original = json.loads((root / "public/rawlogs/fixture-matrix.json").read_text())
assert len(record["rows"]) == len(original["rows"]) == 31
for actual, public in zip(record["rows"], original["rows"]):
    assert (actual["branch_head"], actual["base_tip"]) == (public["branch_head"], public["base_tip"])
print("All 31 public head/tip object pairs reproduce exactly.")
sys.exit(result)
