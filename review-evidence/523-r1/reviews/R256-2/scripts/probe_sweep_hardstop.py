#!/usr/bin/env python3
"""Reviewer probe: stop ONLY the sweep entry process with KILL or HUP at a
known command handshake, then release the command and observe whether the
sweep loop still starts the next suite and prints a completed summary.

Usage: probe_sweep_hardstop.py REPO_COPY BASE_DRIVER OUT_JSON
Reuses the head fixture from REPO_COPY/scripts/test_suite_cancellation.py.
Runs each case for the head driver and for the base driver (483a133).
"""
import json, os, signal, sys, time
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
base_driver = Path(sys.argv[2]).resolve()
out = Path(sys.argv[3])
sys.path.insert(0, str(repo / "scripts"))
os.chdir(repo)
import tempfile
from owned_process import OwnedProcesses
from test_suite_cancellation import fixture, start
from process_test_support import identity

def wait_for(pred, seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if pred():
            return True
        time.sleep(0.05)
    return False

def case(parent, driver, signum):
    label = f"{driver}-{signal.Signals(signum).name}"
    root, probe = fixture(parent, label)
    if driver == "base":
        (root / "scripts/run_all_suites.sh").write_bytes(base_driver.read_bytes())
    probe.env["PROBE_MODE"] = "command"
    start(probe)
    data = probe.ready()
    entry = probe.process.pid
    entry_comm = (Path("/proc") / str(entry) / "comm").read_text().strip()
    probe.signal(signum)
    entry_status = probe.process.wait(timeout=10)
    # The entry process is gone. Release the in-flight command as a real suite
    # would eventually finish, then look for a later suite and a summary.
    (probe.control / "release").write_text("released after entry stop\n")
    next_suite = wait_for(lambda: (probe.control / "next-suite").exists(), 20)
    wait_for(lambda: "\nlogs:" in probe.log(), 10)
    log = probe.log()
    lock_owner_left = (root / ".run_all_suites.lock.owner").exists()
    return dict(case=label, entry_process=entry_comm, entry_exit=entry_status,
                next_suite_started=next_suite,
                completed_summary="\nsuites:" in log,
                pass_omega="PASS     omega" in log,
                lock_owner_file_left=lock_owner_left,
                transcript_tail=log.splitlines()[-8:])

def main():
    results = []
    with tempfile.TemporaryDirectory(prefix="hardstop-", dir=os.environ.get("TMPDIR")) as scratch:
        parent = Path(scratch)
        # Containment only: this reviewer process adopts and later reaps any
        # survivor of the stopped entry process before the fixture is removed.
        with OwnedProcesses():
            for driver in ("head", "base"):
                for signum in (signal.SIGKILL, signal.SIGHUP):
                    results.append(case(parent, driver, signum))
    out.write_text(json.dumps(results, indent=2) + "\n")
    for r in results:
        print(json.dumps({k: v for k, v in r.items() if k != "transcript_tail"}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
