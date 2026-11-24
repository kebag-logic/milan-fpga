import sys, tempfile
from pathlib import Path
sys.path.insert(0, '/data-2/milan/lanes/cicd-1/scripts')
import test_suite_cancellation as h, suite_preflight_controls as c
from owned_process import OwnedProcesses
which = sys.argv[1]
with tempfile.TemporaryDirectory() as d, OwnedProcesses():
    try:
        getattr(c, which)(h, Path(d), **({"fail": True} if which == "preflight_only" else {}))
    except AssertionError as e:
        print("CONTROL FAILED (mutant caught):", str(e)[:150]); sys.exit(0)
print("CONTROL PASSED (mutant survived)"); sys.exit(1)
