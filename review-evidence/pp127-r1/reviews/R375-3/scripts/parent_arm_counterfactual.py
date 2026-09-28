#!/usr/bin/env python3
"""Evaluate the parent evidence inventory's own arm rules for tb/srp_top only.

Imports the unmodified parent functions (measure_test_evidence.py at parent dev
c0723222) and applies them to this head's tb/srp_top Makefile and mutants.py,
with the processor entries as committed (run_suites.sh + hdl.yml) and with the
new hdl.yml campaign step removed. No parent bank is run.
usage: parent_arm_counterfactual.py <parent-scripts-dir> <processor-tree>
"""
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import measure_test_evidence as m  # noqa: E402

tree = Path(sys.argv[2])
makefile = (tree / "tb/srp_top/Makefile").read_text()
scripts = {"mutants.py": (tree / "tb/srp_top/mutants.py").read_text()}
runner = (tree / "scripts/run_suites.sh").read_text()
hdl = (tree / ".github/workflows/hdl.yml").read_text()
hdl_without = hdl.replace("          make -C tb/srp_top mutants\n", "")
assert hdl_without != hdl


def goals(entries: list[str]) -> set[str]:
    """Goals reaching protocol-processor/tb/srp_top from the given entry texts."""
    out: set[str] = set()
    for text in entries:
        for directory, targets in m.make_invocations(text):
            if directory is not None and ("$" in directory or directory.strip("/") == "tb/srp_top"):
                out |= set(targets) or {""}
    return out


for label, entries in (("committed entries (run_suites.sh + hdl.yml)", [runner, hdl]),
                       ("hdl.yml campaign step removed", [runner, hdl_without]),
                       ("run_suites.sh only", [runner])):
    g = goals(entries)
    print(f"{label}: goals={sorted(g)} arms={m.arms(makefile, g, scripts)}")
