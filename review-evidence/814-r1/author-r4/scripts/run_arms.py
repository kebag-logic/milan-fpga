#!/usr/bin/env python3
"""run_arms.py <repo>/sw/litex <arm>...: run the named arm functions of test_soc_timing_cuts.py, print RESULT."""
import sys
import time

sys.path.insert(0, sys.argv[1])
import test_soc_timing_cuts as t  # noqa: E402

problems = []
for arm in sys.argv[2:]:
    start = time.time()
    getattr(t, arm)(problems)
    print(f"  ({arm}: {time.time() - start:.0f} s)")
print(f"RESULT: {'PASS' if not problems else 'FAIL'} {problems}")
sys.exit(1 if problems else 0)
