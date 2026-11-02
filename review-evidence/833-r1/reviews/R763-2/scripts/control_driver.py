#!/usr/bin/env python3
"""usage: control_driver.py <scripts_dir> <control> [production]

Run one owner control of scripts/test_suite_cancellation.py, imported from
<scripts_dir> (a possibly mutated copy), inside the same outer owner that the
preflight's main() provides. "production" keeps every cleanup stage at the
product's constants for that control."""
import contextlib, sys, tempfile, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import owned_process, test_suite_cancellation as t
if len(sys.argv) > 3 and sys.argv[3] == "production":
    t.stages = lambda **_s: contextlib.nullcontext()
control = getattr(t, sys.argv[2])
began = time.monotonic()
with tempfile.TemporaryDirectory(prefix="r763-2-ctl-") as scratch:
    with owned_process.OwnedProcesses():
        if sys.argv[2] == "owner_vanishing":
            control()
        else:
            control(Path(scratch))
print(f"CONTROL {sys.argv[2]} PASS in {time.monotonic() - began:.2f} s", flush=True)
