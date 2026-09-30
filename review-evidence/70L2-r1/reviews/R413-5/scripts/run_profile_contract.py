#!/usr/bin/env python3
"""Run test_builder.test_baremetal_profile_contract() from <tree> alone.

usage: run_profile_contract.py <tree>
Exit 0 when the function returns, or when the stop sentinel planted by
plant_stop.py fires (printed as STOPPED-AFTER-VERDICT-BREAKS with the counts);
exit 1 with GATE-REFUSED: <message> on an AssertionError.
"""
import sys, time
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
sys.dont_write_bytecode = True
import test_builder as tb  # noqa: E402
t0 = time.time()
try:
    tb.test_baremetal_profile_contract()
except AssertionError as exc:
    print(f"GATE-REFUSED: {exc}")
    print(f"elapsed={time.time()-t0:.0f}s")
    sys.exit(1)
except Exception as exc:  # the stop sentinel, or a crash
    if type(exc).__name__ == "R413StopAfterBreaks":
        print(f"STOPPED-AFTER-VERDICT-BREAKS {exc}")
        print(f"elapsed={time.time()-t0:.0f}s")
        sys.exit(0)
    print(f"CRASH: {type(exc).__name__}: {exc}")
    sys.exit(2)
print("PROFILE-CONTRACT RETURNED")
print(f"elapsed={time.time()-t0:.0f}s")
