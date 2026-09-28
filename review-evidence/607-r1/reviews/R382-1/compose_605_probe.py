#!/usr/bin/env python3
"""Resolve the #615 x #605 conflicts two ways and run both lanes' focused tests.
Usage: compose_605_probe.py <merged-worktree> <platform-conflict-copy> <test_builder-conflict-copy> <litex-python>"""
import re, subprocess, sys
from pathlib import Path
work, ax, tb, py = Path(sys.argv[1]), Path(sys.argv[2]).read_text(), Path(sys.argv[3]).read_text(), sys.argv[4]
HUNK = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)
# test_builder: keep both test functions and both list entries.
def tb_fix(m):
    ours, theirs = m.group(1), m.group(2)
    if "def test_" in ours:
        return ours + "\n" + theirs
    return theirs.replace("test_declaration_contracts, test_all_configs_build",
                          "test_declaration_contracts, test_clock_crossing_constraints, test_all_configs_build")
(work / "sw/builder/test_builder.py").write_text(HUNK.sub(tb_fix, tb))
for order in ("swap-before-605-hooks", "605-hooks-before-swap"):
    def ax_fix(m):
        ours, theirs = m.group(1), m.group(2)
        if "import" in ours:
            return ours + theirs
        return ours + theirs if order.startswith("swap") else theirs + ours
    (work / "sw/litex/platforms/alinx_ax7101.py").write_text(HUNK.sub(ax_fix, ax))
    a = subprocess.run([py, "-B", "sw/builder/test_clock_constraints.py"], cwd=work, capture_output=True, text=True)
    b = subprocess.run([py, "-B", "-c", "from test_timing_grade import *\n"
                        f"test_timing_grade_contract(); test_platform_hooks({py!r}); test_pll_grade({py!r})"],
                       cwd=work / "sw/builder", capture_output=True, text=True)
    tail = lambda r: (r.stdout + r.stderr).strip().splitlines()[-1][:160] if (r.stdout + r.stderr).strip() else ""
    print(f"{order}: #607 test rc={a.returncode} | #395 tests rc={b.returncode} :: {tail(b)}")
