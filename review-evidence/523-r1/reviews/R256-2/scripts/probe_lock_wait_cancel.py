#!/usr/bin/env python3
"""Reviewer probe: sweep A holds the tree lock at a command handshake; sweep B
queues with --wait on the same lock; TERM/INT B's entry process. B must exit
128+sig promptly without running a suite, and A's processes (foreign to B)
must keep their identities and complete normally after release.

Usage: probe_lock_wait_cancel.py REPO_COPY OUT_JSON
"""
import json, os, signal, subprocess, sys, time
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
sys.path.insert(0, str(repo / "scripts"))
os.chdir(repo)
import tempfile
from owned_process import OwnedProcesses
from test_suite_cancellation import fixture, start
from process_test_support import Probe, identity

def case(parent, signum):
    root, a = fixture(parent, f"lockwait-{signal.Signals(signum).name}")
    a.env["PROBE_MODE"] = "orphan"  # prints a tally after release, so A can exit 0
    start(a)
    data = a.ready()
    held = {str(p): identity(p) for p in (a.process.pid, data["pid"], data["child"])}
    b = Probe(root, f"queued-{signal.Signals(signum).name}")
    b.env = dict(a.env, PROBE_CONTROL=str(b.control), TMPDIR=str(b.control), PROBE_MODE="pass")
    (b.control / "bin").mkdir()
    (b.control / "bin/make").write_bytes((a.control / "bin/make").read_bytes()); (b.control / "bin/make").chmod(0o755)
    (b.control / "real_tally.py").write_bytes((a.control / "real_tally.py").read_bytes())
    (b.control / "real_selector.py").write_bytes((a.control / "real_selector.py").read_bytes())
    b.env["PATH"] = str(b.control / "bin") + os.pathsep + os.environ["PATH"]
    b.start(["bash", str(root / "scripts/run_all_suites.sh"), str(root / "logs-b"), "--wait"])
    # Observable boundary: a `flock 9` process descended from B's entry process.
    def descends(pid, ancestor):
        while pid > 1:
            if pid == ancestor:
                return True
            try:
                pid = int(Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[1])
            except (OSError, ValueError):
                return False
        return False
    deadline = time.monotonic() + 20
    waiting = False
    while time.monotonic() < deadline and not waiting:
        for entry in Path("/proc").iterdir():
            if entry.name.isdecimal():
                try:
                    argv = (entry / "cmdline").read_bytes().split(b"\0")[:2]
                except OSError:
                    continue
                if argv == [b"flock", b"9"] and descends(int(entry.name), b.process.pid):
                    waiting = True
        time.sleep(0.05)
    started = time.monotonic()
    b.signal(signum)
    b_status = b.process.wait(timeout=15)
    b_seconds = round(time.monotonic() - started, 2)
    b_log = b.log()
    still = {pid: identity(int(pid)) for pid in held}
    foreign_ok = all(still[p] is not None and still[p][0] == held[p][0] and still[p][1] != "Z" for p in held)
    (a.control / "release").write_text("release A\n")
    a_status = a.process.wait(timeout=30)
    return dict(signal=signal.Signals(signum).name, b_blocked_in_flock=waiting, b_exit=b_status,
                b_seconds=b_seconds, b_ran_suite=(root / "logs-b" / "alpha.log").exists(),
                b_cancelled_line="CANCELLED:" in b_log, b_summary="\nsuites:" in b_log,
                holder_identities_unchanged=foreign_ok, holder_exit_after_release=a_status,
                holder_completed="\nsuites:" in a.log())

def main():
    rows = []
    with tempfile.TemporaryDirectory(prefix="lockwait-", dir=os.environ.get("TMPDIR")) as scratch:
        with OwnedProcesses():
            for signum in (signal.SIGTERM, signal.SIGINT):
                rows.append(case(Path(scratch), signum))
    out.write_text(json.dumps(rows, indent=2) + "\n")
    for r in rows:
        print(json.dumps(r))
    ok = all(r["b_blocked_in_flock"] and r["b_exit"] == 128 + signal.Signals[r["signal"]] and not r["b_ran_suite"]
             and not r["b_summary"] and r["holder_identities_unchanged"] and r["holder_exit_after_release"] == 0 for r in rows)
    print("LOCK-WAIT CANCELLATION " + ("OK" if ok else "UNEXPECTED"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
