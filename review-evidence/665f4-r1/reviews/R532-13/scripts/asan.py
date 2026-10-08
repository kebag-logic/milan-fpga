"""R532-13: AddressSanitizer build of the SRP/composition suites at IF=1 and IF=2. Usage: <repo> <lwsrp> <out>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, LWSRP, OUT
from ctrl_build import CTRL, Tree
import srp_arms, fw_gtest
build = fw_gtest.Build(jobs=4, address_sanitizer=True)
rc = 0
for n in (1, 2):
    for suite in ("srp_mbx.cpp", "srp_rx_retry.cpp", "srp_app.cpp", "test_acmp_mbx.cpp",
                  "srp_latency.cpp", "srp_walk.cpp", "srp_debug.cpp"):
        out = OUT / "build"
        r = srp_arms.arm_srp(Tree(CTRL, out, out / "reuse", build), LWSRP, n,
                             debug=suite == "srp_debug.cpp", test=suite)
        (OUT / f"asan-{suite}-if{n}.log").write_text(r.log)
        print(f"asan {suite} IF={n}: rc={r.rc}", flush=True)
        rc |= r.rc
print(f"asan: {'FAIL' if rc else 'PASS'}")
sys.exit(1 if rc else 0)
