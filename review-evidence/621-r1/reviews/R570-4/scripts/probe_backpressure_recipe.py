#!/usr/bin/env python3
"""Disposable probe (R570-4): in a SCRATCH clone whose test_sim_pool.py
LEGACY_LEGS already carries the #658 dynmap leg (probe_sim_pool_dynmap.py),
run ONE backpressure control, the actual-Makefile normal drain
(make-copy-normal-drain), so its verdict is attributable to the revision.

Usage: python3 -I probe_backpressure_recipe.py <scratch clone root> <work dir>
"""
import ctypes, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
here = root / "tb/verilator/milan_dp"
driver = (
    "import sys, signal, ctypes; sys.path.insert(0, %r)\n"
    "from pathlib import Path\n"
    "import test_sim_pool_backpressure as b\n"
    "assert ctypes.CDLL(None).prctl(36, 1, 0, 0, 0) == 0\n"
    "try:\n"
    "    b.exercise(Path(%r), True, False, None, 'drain'); print('[PASS] make-copy-normal-drain')\n"
    "except Exception as e:\n"
    "    print('[FAIL] make-copy-normal-drain:', type(e).__name__, str(e)[:300]); sys.exit(1)\n"
    % (str(here), str(work)))
sys.exit(subprocess.run([sys.executable, "-c", driver], cwd=here).returncode)
