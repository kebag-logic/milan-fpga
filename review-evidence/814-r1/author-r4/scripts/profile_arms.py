#!/usr/bin/env python3
"""profile_arms.py <repo>/sw/litex <arm>...: run each named arm of test_soc_timing_cuts.py in this process,
printing its CPU seconds and the process's peak RSS after it (resource.getrusage)."""
import gc
import resource
import sys
import time

sys.path.insert(0, sys.argv[1])
import test_soc_timing_cuts as t  # noqa: E402

problems = []
for arm in sys.argv[2:]:
    cpu = time.process_time()
    getattr(t, arm)(problems)
    gc.collect()
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    with open("/proc/self/status") as status:
        rss = [line.split()[1] for line in status if line.startswith("VmRSS")][0]
    print(f"PROFILE {arm}: {time.process_time() - cpu:.0f} s CPU, peak RSS {peak:.2f} GB, now {int(rss) / 1e6:.2f} GB",
          flush=True)
print(f"RESULT: {'PASS' if not problems else 'FAIL'} {problems}")
