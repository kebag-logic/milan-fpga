#!/usr/bin/env python3
"""reviewer_srp_wide.py - plant rv-talker-decl-before-the-joins (see
reviewer_fw_plants.py) and run WHOLE SRP suites on it (filter Srp.*), printing
every [FAIL] line: does any existing test observe a TALKER_DECL that names
sources a failed creation never declared?
Usage: python3 -B reviewer_srp_wide.py <tree> <build-root> <lwsrp>"""
import shutil
import sys
from pathlib import Path
tree, root, lwsrp = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(tree / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
import srp_mutants  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from srp_arms import arm_srp  # noqa: E402
OLD = "    uint32_t declared = 0;\n"
NEW = OLD + "    (void)mbx_pub_talker_decl(i->index,(1u<<CTRL_SRP_SOURCES)-1u);\n"
for plant in (False, True):
    out = root / ("wide-planted" if plant else "wide-control")
    src = out / "ctrl"
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    t = src / "srp/srp_mbx.c"
    s = t.read_text()
    assert s.count(OLD) == 1
    if plant:
        t.write_text(s.replace(OLD, NEW))
    for ifs in (1, 2):
        for suite in ("srp_mbx.cpp", "srp_app.cpp", "srp_rx_retry.cpp"):
            r = arm_srp(Tree(src, out / "build", out / "reuse", fw_gtest.Build(jobs=4)), lwsrp, ifs,
                        test=(suite, "*"))
            fails = [ln.strip() for ln in r.log.splitlines() if "[FAIL]" in ln]
            tally = [ln.strip() for ln in r.log.splitlines() if "checks:" in ln][-1:]
            print(f"{'planted' if plant else 'control'} if{ifs} {suite}: rc {r.rc}, {len(fails)} [FAIL] {tally}")
            for f in fails[:5]:
                print("    " + f[:220])
