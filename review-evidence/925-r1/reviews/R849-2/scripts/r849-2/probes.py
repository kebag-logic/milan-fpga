#!/usr/bin/env python3
"""probes.py ROOT OUT IFS [PLANT]: copy sw/firmware/ctrl to OUT/ctrl, append probes.cpp to its srp_mbx.cpp,
optionally apply one of plants.py's EXPLORE plants by name, and run SrpTalkerKinds.R8492* at IFS interfaces.
Nothing in ROOT is written."""
from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
root, out, ifs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
plant = sys.argv[4] if len(sys.argv) > 4 else None
sys.argv = [sys.argv[0], str(root), str(out), str(ifs), "1", "none"]
spec = importlib.util.spec_from_file_location("plants", HERE / "plants.py")
plants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plants)
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402

src = out / "ctrl"
if src.exists():
    shutil.rmtree(src)
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
test = src / "test/srp_mbx.cpp"
test.write_text(test.read_text() + "\n" + (HERE / "probes.cpp").read_text())
if plant:
    name, path, old, new = next(p for p in plants.EXPLORE if p[0] == plant)
    target = src / path
    text = target.read_text()
    assert text.count(old) == 1, plant
    target.write_text(text.replace(old, new))
srp_arms.HERE = src / "test"
r = srp_arms.arm_srp(Tree(src, out / "build", out / "reuse", fw_gtest.Build(jobs=4)), root / "third_party/lwSRP",
                     ifs, test=("srp_mbx.cpp", "SrpTalkerKinds.R8492*"))
print(r.log)
print(f"probe rc={r.rc} interfaces={ifs} plant={plant}")
sys.exit(r.rc)
