#!/usr/bin/env python3
"""Run test_ctrl_firmware.py unchanged, logging every `git ... rev-parse --show-toplevel`
that ctrl_arms.lwsrp_pin issues whose answer would refuse: return code, stdout, stderr,
cwd and the GIT_* environment.

Usage (from the candidate clone): python3 trace_lwsrp_pin.py <clone> <test_ctrl_firmware args...>
"""
import os
import runpy
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
test_dir = clone / "sw/firmware/ctrl/test"
sys.path[:0] = [str(test_dir), str(clone / "sw/firmware/gtest")]
import ctrl_arms  # noqa: E402

real_run = ctrl_arms.run


def traced(argv, cwd=None):
    res = real_run(argv, cwd)
    if list(argv[:1]) == ["git"] and "--show-toplevel" in argv:
        target = Path(argv[argv.index("-C") + 1]).resolve()
        if res.returncode or Path(res.stdout.strip()).resolve() != target:
            env = {k: v for k, v in os.environ.items() if k.startswith("GIT")}
            print(f"TRACE git refusal: argv={argv} rc={res.returncode} stdout={res.stdout!r} "
                  f"stderr={res.stderr!r} cwd={cwd} process_cwd={os.getcwd()} env={env}", flush=True)
    return res


ctrl_arms.run = traced
sys.argv = [str(test_dir / "test_ctrl_firmware.py"), *sys.argv[2:]]
runpy.run_path(sys.argv[0], run_name="__main__")
