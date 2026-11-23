#!/usr/bin/env python3
"""aecp_suite_arms.py TREE BUILD_DIR: of the firmware gate's suites phase (test_ctrl_firmware.py --shard 0/4), the part
that compiles test_aecp.cpp: aecp_arms.all_arms, on a tree built as the gate's main() builds it (Tree, stack pin,
cut_reuse), reported by the gate's own ctrl_arms.report. First the gate's own shard-inventory self-check
(test_ctrl_firmware_shards.run_cases), which prints the live invocation count and each shard's size. Exit 0 when the
inventory passes and every AECP arm passes."""
import sys
from pathlib import Path

test = Path(sys.argv[1]).resolve() / 'sw/firmware/ctrl/test'
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(test))
import test_ctrl_firmware as gate  # noqa: E402
from test_ctrl_firmware_shards import run_cases  # noqa: E402

run_cases(gate)
print(f"toolchain: {gate.fw_gtest.toolchain()}", flush=True)
try:
    tree = gate.Tree(gate.CTRL, out / "checkout", out / "reuse", gate.fw_gtest.Build(jobs=4))
    print(f"tsn-c-stack at {gate.stack_pin()}", flush=True)
    gate.cut_reuse(tree.reuse)
    failed = gate.ctrl_arms.report(gate.aecp_arms.all_arms(tree))
except gate.Refusal as exc:
    print(f"REFUSED: {exc}")
    sys.exit(2)
print(f"aecp suite arms: {gate.verdict(failed)}")
sys.exit(1 if failed else 0)
