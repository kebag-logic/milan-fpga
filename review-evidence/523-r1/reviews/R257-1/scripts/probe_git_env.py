#!/usr/bin/env python3
"""Run the production mutation driver (or a base copy) in the production
lifecycle fixture (synthetic make, real Git) with one caller Git environment
variable set, and report exit status and whether any control ran.
Usage: probe_git_env.py <checkout> <driver-file> <outdir> NAME=VALUE|none ..."""
import json, os, shutil, sys, tempfile
from pathlib import Path
checkout, driver, outdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(checkout / "scripts")); sys.path.insert(0, str(checkout / "tb/verilator/gptp_shadow"))
from owned_process import OwnedProcesses
from process_test_support import snapshot
from test_mutant_lifecycle import fixture, DRIVER
results = {}
with tempfile.TemporaryDirectory(prefix="gitenv-", dir=os.environ.get("TMPDIR")) as scratch, OwnedProcesses():
    for spec in sys.argv[4:]:
        label = "env-" + spec.split("=")[0].lower()
        root, probe = fixture(Path(scratch), label)
        shutil.copy2(driver, root / DRIVER)
        probe.env["PROBE_MODE"] = "detect"
        if spec != "none":
            name, value = spec.split("=", 1)
            probe.env[name] = value.replace("@ROOT@", str(root))
        before = snapshot(root)
        probe.start([sys.executable, str(root / DRIVER)])
        status, output = probe.finish()
        seen = (probe.control / "seen").read_text().splitlines() if (probe.control / "seen").exists() else []
        results[spec] = dict(exit=status, controls_run=len(seen), caller_unchanged=snapshot(root) == before,
                             last_lines=[l for l in output.splitlines() if l.strip()][-2:])
outdir.mkdir(parents=True, exist_ok=True)
(outdir / "result.json").write_text(json.dumps(results, indent=1) + "\n")
for k, v in results.items(): print(f"{k:40s} exit={v['exit']} controls_run={v['controls_run']} {v['last_lines'][-1:]}")
