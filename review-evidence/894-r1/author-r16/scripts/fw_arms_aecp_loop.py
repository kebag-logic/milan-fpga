#!/usr/bin/env python3
"""The firmware unit gate's AECP and loop arms alone, as test_ctrl_firmware.py's suites phase runs them: the compiled
service bounds (ctrl_service_bounds.arm_service_bounds, which holds the loop's stated figures at compile time), the
port and event loop (ctrl_arms.arm_port, test_port_loop.cpp) and every AECP arm (aecp_arms.all_arms). Each arm's
verdict through ctrl_arms.report, as the gate prints it. Run from the tree's top with the RV32 SDK on PATH.
usage: fw_arms_aecp_loop.py [JOBS]"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path('sw/firmware/ctrl/test').resolve()))
import test_ctrl_firmware as t  # noqa: E402


def main(argv):
    jobs = int(argv[1]) if len(argv) > 1 else 4
    print(f"toolchain: {t.fw_gtest.toolchain()}")
    with tempfile.TemporaryDirectory(prefix='ctrl-fw-arms-') as tmp:
        out = Path(tmp)
        tree = t.Tree(t.CTRL, out / 'checkout', out / 'reuse', t.fw_gtest.Build(jobs=jobs))
        print(f"tsn-c-stack at {t.stack_pin()}")
        t.cut_reuse(tree.reuse)
        outcomes = [t.ctrl_arms.arm_service_bounds(tree), t.ctrl_arms.arm_port(tree), *t.aecp_arms.all_arms(tree)]
        failed = t.ctrl_arms.report(outcomes)
    print(f"arms: {', '.join(o.arm for o in outcomes)}")
    print(f"AECP and loop arms: {'FAIL' if failed else 'PASS'} ({len(outcomes)} arms)")
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
