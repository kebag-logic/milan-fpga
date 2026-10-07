#!/usr/bin/env python3
"""Run the unchanged four reviewer tests on the previous round's core."""
from pathlib import Path
import subprocess
import sys
root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build as b
import fw_gtest
out = packet / "scratch/timer-old"
out.mkdir(parents=True)
src = out / "acmp.c"
src.write_bytes(subprocess.check_output(["git", "-C", str(root), "show", "4f6216abff01b6f859d348aaf6a71e47c5a5a2a8:sw/firmware/ctrl/acmp/acmp.c"]))
t = b.Tree(b.CTRL, out, out / "reuse", fw_gtest.Build(jobs=2))
objects = b.compile_c(t, [src], "core")
objects += fw_gtest.compile_tests(t.build, b.includes(t), [packet / "scripts/independent_timers.cpp"], out / "tests")
result = b.execute("previous-round-timers", b.link(t, "old-timers", objects))
print(result.log)
(packet / "receipts/timer-old-child.rc").write_text(str(result.rc) + "\n")
assert result.rc == 1
for expected in ("InitialImmediateSendStartsAtAcceptance", "DuplicateImmediateSendStartsAtAcceptance"):
    assert "[FAIL] ReviewerTimers." + expected in result.log
print("PASS: previous-round negative control fails the two immediate-send assertions")
