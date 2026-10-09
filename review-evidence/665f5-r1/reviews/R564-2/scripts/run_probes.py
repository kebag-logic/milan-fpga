#!/usr/bin/env python3
"""Build exact-head AECP core suites with appended reviewer probes in a disposable copy.

Usage: run_probes.py <exact-head-tree> <packet> <set>
  set r565-1: full exact-head test_aecp.cpp + probes/r565-1_probe_cases.cpp, Core.R565*, 2 interfaces
  set r564-1: exact-head fixture (through the line before the first '#ifdef AECP_TEST_NVM'
              that follows the Core fixture) + probes/r564-1_probe_tests*.cpp, Core.P*, 1 interface
  set r564-1-full: full exact-head test_aecp.cpp + the same r564-1 probe sources, Core.P*, 1 interface
  set r564-2: full exact-head test_aecp.cpp + probes/r564-2_probes.cpp, Core.Q*, 1 and 2 interfaces
Probe sources are used unchanged; only the fixture boundary follows the head.
"""
import sys
from pathlib import Path
root, packet, which = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import aecp_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import Tree, CTRL  # noqa: E402
work = packet / "scratch" / ("probe-" + which)
work.mkdir(parents=True, exist_ok=True)
head = (root / "sw/firmware/ctrl/test/test_aecp.cpp").read_text()
probes = packet / "probes"
if which == "r564-1":
    lines = head.splitlines(keepends=True)
    cut = next(i for i, l in enumerate(lines) if i > 100 and l.startswith("#ifdef AECP_TEST_NVM"))
    text = "".join(lines[:cut]) + (probes / "r564-1_probe_tests.cpp").read_text() + (probes / "r564-1_probe_tests_p6.cpp").read_text()
    runs = [(1, "Core.P*")]
elif which == "r564-1-full":
    text = head + "\n" + (probes / "r564-1_probe_tests.cpp").read_text() + (probes / "r564-1_probe_tests_p6.cpp").read_text()
    runs = [(1, "Core.P*")]
elif which == "r565-1":
    text = head + "\n" + (probes / "r565-1_probe_cases.cpp").read_text()
    runs = [(2, "Core.R565*")]
else:
    text = head + "\n" + (probes / "r564-2_probes.cpp").read_text()
    runs = [(1, "Core.Q*"), (2, "Core.Q*")]
(work / "test_aecp.cpp").write_text(text)
# Headers the suite includes from its own directory.
for name in ("aecp_callback_inputs.hpp", "aecp_latency_policy.hpp"):
    (work / name).write_text((root / "sw/firmware/ctrl/test" / name).read_text())
aecp_arms.HERE = work
rc = 0
for interfaces, selected in runs:
    tree = Tree(CTRL, work / f"if{interfaces}", work / f"if{interfaces}" / "reuse", fw_gtest.Build(jobs=4))
    result = aecp_arms.core_arm(tree, root / "configs/endstation_ax7101_1x1_tdm8.yaml", interfaces, "core", selected)
    print(f"=== {which} interfaces={interfaces} filter={selected} rc={result.rc}")
    print(result.log)
    rc = rc or result.rc
raise SystemExit(rc)
