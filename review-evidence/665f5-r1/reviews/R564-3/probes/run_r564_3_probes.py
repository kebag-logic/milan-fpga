# Build the exact-head composed AECP suite with the R564-3 probes appended, optionally
# with one core plant from core_plants.py applied in a disposable copy.
# Usage: python3 -B run_r564_3_probes.py <repo-root> <output-dir> [plant-name]
from __future__ import annotations

import shutil
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
plant = sys.argv[3] if len(sys.argv) > 3 else None
here = Path(__file__).resolve().parent
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(here))
import aecp_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
import core_plants  # noqa: E402

work = out / "suite"
work.mkdir(parents=True, exist_ok=True)
head = (repo / "sw/firmware/ctrl/test/test_aecp.cpp").read_text()
(work / "test_aecp.cpp").write_text(head + "\n" + (here / "r564-3_probes.cpp").read_text())
for name in ("aecp_callback_inputs.hpp", "aecp_latency_policy.hpp"):
    shutil.copyfile(repo / "sw/firmware/ctrl/test" / name, work / name)
aecp_arms.HERE = work
src = out / "ctrl"
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
if plant:
    name, path, old, new, _ = next(p for p in core_plants.PLANTS if p[0] == plant)
    target = src / path
    text = target.read_text()
    assert text.count(old) == 1, (name, text.count(old))
    target.write_text(text.replace(old, new))
rc = 0
for interfaces in (1, 2):
    tree = Tree(src, out / f"if{interfaces}", out / f"if{interfaces}" / "reuse", fw_gtest.Build(jobs=4))
    result = aecp_arms.core_arm(tree, repo / "configs/endstation_ax7101_1x1_tdm8.yaml", interfaces, "app", "Core.S1_*:Core.S2_*")
    print(f"=== plant={plant} interfaces={interfaces} filter=Core.S1_*:Core.S2_* rc={result.rc}")
    print(result.log)
    rc = rc or result.rc
raise SystemExit(rc)
