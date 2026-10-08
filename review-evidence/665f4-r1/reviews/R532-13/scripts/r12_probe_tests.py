"""R532-13: the original R532-12 probe header, appended to a disposable copy of
srp_feedback.hpp, run unmodified at IF=1 and IF=2. Usage: <repo> <lwsrp> <out> <header>"""
import sys, os, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, LWSRP, OUT
from pathlib import Path
from ctrl_build import CTRL, Tree
import srp_arms, fw_gtest
src = OUT / "probe-ctrl"
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
p = src / "test/srp_feedback.hpp"
p.write_bytes(p.read_bytes() + b"\n" + Path(sys.argv[4]).read_bytes())
srp_arms.HERE = src / "test"
rc = 0
for n in (1, 2):
    r = srp_arms.arm_srp(Tree(src, OUT / f"b{n}", OUT / f"reuse{n}", fw_gtest.Build(jobs=4)), LWSRP, n,
                         test=("test_acmp_mbx.cpp", "SrpFeedback.*"))
    (OUT / f"r12-probe-tests-if{n}.log").write_text(r.log)
    print(r.log, flush=True)
    rc |= r.rc
print(f"r12 probe tests: {'FAIL' if rc else 'PASS'}")
sys.exit(1 if rc else 0)
