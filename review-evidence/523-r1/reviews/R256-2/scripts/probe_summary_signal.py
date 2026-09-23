#!/usr/bin/env python3
"""Reviewer probe: signal the sweep entry while summarise() runs its final
tally (handshake: the tally command itself reaches the fixture worker).
Records the exit status and which summary lines were already printed.

Usage: probe_summary_signal.py REPO_COPY OUT_JSON
"""
import json, os, signal, sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
sys.path.insert(0, str(repo / "scripts"))
os.chdir(repo)
import tempfile
from owned_process import OwnedProcesses
from test_suite_cancellation import fixture, start
from process_test_support import assert_reaped, write

TALLY = r'''
import os, runpy, subprocess, sys
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
if "--quiet" in sys.argv:
    raise SystemExit(subprocess.call([sys.executable, str(control / "worker.py")]))
if "--selftest" in sys.argv:
    raise SystemExit(0)
runpy.run_path(str(control / "real_tally.py"), run_name="__main__")
'''

rows = []
with tempfile.TemporaryDirectory(prefix="summary-", dir=os.environ.get("TMPDIR")) as scratch:
    with OwnedProcesses():
        for signum in (signal.SIGINT, signal.SIGTERM):
            root, probe = fixture(Path(scratch), "summary-" + signal.Signals(signum).name)
            write(root / "scripts/suite_tally.py", TALLY)
            probe.env["PROBE_MODE"] = "pass"
            start(probe)
            data = probe.ready()
            probe.signal(signum)
            status, output = probe.finish()
            assert_reaped(data)
            rows.append(dict(signal=signal.Signals(signum).name, exit=status,
                             printed_suite_verdicts=[l for l in output.splitlines() if l.startswith(("PASS ", "FAIL "))],
                             printed_summary_lines=[l for l in output.splitlines() if l.startswith(("suites:", "----", "logs:"))],
                             cancelled_lines=[l for l in output.splitlines() if l.startswith(("CANCELLED", "partial logs"))]))
out.write_text(json.dumps(rows, indent=2) + "\n")
for r in rows:
    print(json.dumps(r))
