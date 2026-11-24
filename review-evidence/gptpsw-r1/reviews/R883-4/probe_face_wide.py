#!/usr/bin/env python3
"""Reviewer probe: the unmasked AS_CAPABLE defect in aecp_face.c (the datapath's bit 0 kept under software gPTP)
against every AECP face/app/debug test at one and two interfaces and the platform boot at one and two interfaces.
usage: probe_face_wide.py <checkout> <work-dir>   (the checkout is copied, never written)"""
import shutil
import sys
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
import aecp_arms, plat_arms, fw_gtest  # noqa: E401,E402
from ctrl_build import CTRL, ROOT, STACK, Tree  # noqa: E402

OLD = "(uint8_t)((out->flags & ~1u) | (as_capable ? 1u : 0u));"
NEW = "(uint8_t)(out->flags | (as_capable ? 1u : 0u));"
src = work / "ctrl"
shutil.rmtree(work, ignore_errors=True)
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__"))
shutil.copytree(CTRL.parent / "ctrl_nvm", work / "ctrl_nvm", ignore=shutil.ignore_patterns("test", "__pycache__"))
f = src / "aecp/aecp_face.c"
t = f.read_text()
assert t.count(OLD) == 1
f.write_text(t.replace(OLD, NEW))
tree = Tree(src, work / "build", work / "reuse", fw_gtest.Build(jobs=4), STACK.resolve())
cfg = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
runs = {
    "app-if1": lambda: aecp_arms.core_arm(tree, cfg, 1, "app"),
    "app-if2": lambda: aecp_arms.core_arm(tree, cfg, 2, "app"),
    "debug-if2": lambda: aecp_arms.core_arm(tree, cfg, 2, "debug"),
    "platboot1": lambda: plat_arms.arm_platboot(tree, 1),
    "platboot2": lambda: plat_arms.arm_platboot(tree, 2),
}
for name, fn in runs.items():
    out = fn()
    (work / f"{name}.log").write_text(out.log)
    fails = [ln.strip() for ln in out.log.splitlines() if "[FAIL]" in ln or "[  FAILED  ]" in ln]
    print(f"{name}: rc={out.rc} failures={len(fails)} first={fails[0] if fails else '-'}", flush=True)
