#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Production sweep cancellation, using disposable known-boundary commands."""

import json
import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

from owned_process import OwnedProcesses
from process_test_support import Probe, assert_reaped, identity, install, write

DRIVER = "scripts/run_all_suites.sh"

MAKE = r'''#!/usr/bin/env python3
import os, subprocess, sys
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
suite = Path(sys.argv[sys.argv.index("-C") + 1]).name
if suite == "omega":
    (control / "next-suite").write_text("omega executed\n")
    print("1 checks: 1 PASS, 0 FAIL", flush=True)
    raise SystemExit(0)
mode = os.environ.get("PROBE_MODE", "pass")
print("PARTIAL: alpha entered", flush=True)
if mode == "command":
    raise SystemExit(subprocess.call([sys.executable, str(control / "worker.py")]))
if mode == "orphan":
    subprocess.run([sys.executable, str(control / "worker.py")], check=True)
if mode == "timeout":
    # timeout must terminate the real command. Readiness proves it started;
    # there is deliberately no release and no completed suite tally.
    (control / "timeout-started").write_text("alpha started\n")
    signal_file = control / "never-release"
    import time
    while not signal_file.exists():
        time.sleep(0.01)
if mode in ("fail", "masked"):
    print("1 checks: 0 PASS, 1 FAIL", flush=True)
    raise SystemExit(0 if mode == "masked" else 1)
print("1 checks: 1 PASS, 0 FAIL", flush=True)
'''

TALLY = r'''
import os, runpy, subprocess, sys
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
mode = os.environ.get("PROBE_MODE", "pass")
if ((mode == "preflight" and "--selftest" in sys.argv) or
    (mode == "transition" and "--verdict" in sys.argv and sys.argv[-1].endswith("alpha.log"))):
    raise SystemExit(subprocess.call([sys.executable, str(control / "worker.py")]))
if "--selftest" in sys.argv:
    raise SystemExit(0)
runpy.run_path(str(control / "real_tally.py"), run_name="__main__")
'''

SELECTOR = r'''
import os, runpy, subprocess, sys
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
if os.environ.get("PROBE_MODE") == "selection" and "--selftest" not in sys.argv:
    raise SystemExit(subprocess.call([sys.executable, str(control / "worker.py")]))
runpy.run_path(str(control / "real_selector.py"), run_name="__main__")
'''


def fixture(parent: Path, label: str) -> tuple[Path, Probe]:
    """Keep real driver, selector and tally; replace only expensive commands."""
    root = parent / (label + " input [523]")
    root.mkdir()
    for relative in (DRIVER, "scripts/owned_process.py"):
        install(root, relative)
    probe = Probe(root, label)
    source = Path(__file__).resolve().parent
    write(probe.control / "real_tally.py", (source / "suite_tally.py").read_text())
    write(probe.control / "real_selector.py", (source / "suite_shards.py").read_text())
    write(root / "scripts/suite_tally.py", TALLY)
    write(root / "scripts/suite_shards.py", SELECTOR)
    for name in ("check_merge_containment", "check_results_fresh", "xvlog_gate",
                 "check_merge_review_integrity"):
        write(root / f"scripts/{name}.py", "print('bounded prerequisite fixture')\n")
    # The recursive test call is replaced only IN THIS disposable fixture.
    # Its marker and forced-red arm prove normal entry-point ownership.
    write(root / "scripts/test_suite_cancellation.py",
          'import os\nfrom pathlib import Path\n'
          'Path(os.environ["PROBE_CONTROL"], "owner-ran").write_text("owned\\n")\n'
          'raise SystemExit(1 if os.environ.get("PROBE_OWNER_FAIL") else 0)\n')
    write(root / "syn/yosys/check_list_hermetic.sh", "#!/usr/bin/env bash\nexit 0\n", executable=True)
    for name in ("alpha", "omega"):
        write(root / f"tb/verilator/{name}/Makefile", "all:\n\t@echo fixture\n")
    write(probe.control / "bin/make", MAKE, executable=True)
    probe.env["PATH"] = str(probe.control / "bin") + os.pathsep + os.environ["PATH"]
    probe.env.pop("SUITE_TIMEOUT", None)
    probe.env.pop("SUITE_SWEEP_LOCK", None)
    return root, probe


def start(probe: Probe) -> None:
    """Start the normal production entry point with attributable log paths."""
    probe.start(["bash", str(probe.root / DRIVER), str(probe.root / "logs")])


def ordinary(parent: Path, mode: str) -> None:
    """Normal failures continue; masked verdict and deadline remain distinct."""
    root, probe = fixture(parent, mode)
    probe.env["PROBE_MODE"] = mode
    if mode == "timeout":
        probe.env["SUITE_TIMEOUT"] = "0.5"
    start(probe)
    status, output = probe.finish()
    expected = {"pass": 0, "fail": 1, "masked": 1, "timeout": 92}[mode]
    assert status == expected, output
    assert (probe.control / "next-suite").exists() and "PASS     omega" in output, output
    assert (probe.control / "owner-ran").exists(), "normal sweep did not own cancellation tests"
    if mode == "timeout":
        assert (probe.control / "timeout-started").exists(), output
        assert "TIMEOUT  alpha" in output and "UNKNOWN" in output and "PASS     alpha" not in output, output
    elif mode in ("fail", "masked"):
        assert "FAIL     alpha" in output and "PASS     alpha" not in output, output
    if mode == "masked":
        assert "masked verdict" in output, output
    assert "suites: 2" in output, output
    assert not (root / ".run_all_suites.lock.owner").exists()
    probe.save(dict(exit=status, mode=mode, next_suite=True, owner_ran=True))


def cancellation(parent: Path, phase: str, signum: int, unsafe: bool = False) -> None:
    """Latch at selection/preflight/command/transition; reject a later suite."""
    label = ("unsafe-" if unsafe else "cancel-") + phase + "-" + signal.Signals(signum).name
    root, probe = fixture(parent, label)
    probe.env["PROBE_MODE"] = phase
    write(root / "logs/omega.log", "OLD COMPLETED RUN\n")
    write(root / "logs/preflight/old.log", "OLD PREFLIGHT\n")
    if unsafe:
        path = root / DRIVER
        text = path.read_text()
        begin = text.index("# A separate owner adopts")
        end = text.index("WAIT=0", begin)
        text = text[:begin] + text[end:]
        assert "trap cleanup EXIT\n" in text
        path.write_text(text.replace("trap cleanup EXIT\n", "trap cleanup EXIT INT TERM\n"))
    # This sibling is deliberately foreign to the production driver's subtree.
    foreign = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], start_new_session=True)
    foreign_identity = identity(foreign.pid)
    try:
        start(probe)
        data = probe.ready()
        probe.signal(signum)
        if unsafe:
            # Original sweep waited on timeout; reproduce the recorded stop of
            # that owned command too. The handshake identifies this child.
            fd = os.pidfd_open(data["pid"])
            try:
                signal.pidfd_send_signal(fd, signal.SIGTERM)
            finally:
                os.close(fd)
        status, output = probe.finish()
        next_suite = (probe.control / "next-suite").exists()
        assert next_suite == unsafe, output
        if not unsafe:
            assert status == 128 + signum, output
            assert "\nsuites:" not in output and "PASS     omega" not in output, output
            assert "CANCELLED:" in output, output
            assert_reaped(data)
            assert not (root / ".run_all_suites.lock.owner").exists(), "lock owner survived"
        else:
            assert "PASS     omega" in output and "\nsuites:" in output, output
        if phase in ("command", "transition"):
            assert "PARTIAL: alpha entered" in (root / "logs/alpha.log").read_text()
        if phase == "preflight":
            assert "PARTIAL: owned command" in (root / "logs/preflight/suite_tally.log").read_text()
            assert not (root / "logs/omega.log").exists(), "stale suite log survived"
            assert not (root / "logs/preflight/old.log").exists(), "stale prerequisite log survived"
        current = identity(foreign.pid)
        assert foreign.poll() is None and current is not None, "foreign process exited"
        assert current[0] == foreign_identity[0] and current[1] != "Z", "foreign identity changed"
        probe.save(dict(exit=status, phase=phase, handshake=data, next_suite=next_suite,
                        foreign_untouched=True, unsafe_control_detected=unsafe))
    finally:
        foreign.terminate()
        foreign.wait(timeout=3)


def ownership_refusal(parent: Path) -> None:
    """A failing cancellation test must stop the normal sweep in preflight."""
    root, probe = fixture(parent, "owner-refusal")
    probe.env["PROBE_OWNER_FAIL"] = "1"
    start(probe)
    status, output = probe.finish()
    assert status == 2 and "ABORTING: sweep cancellation controls failed" in output, output
    assert (probe.control / "owner-ran").exists() and not (root / "logs/alpha.log").exists()
    probe.save(dict(exit=status, owner_refusal=True, suite_started=False))


def normal_orphan(parent: Path) -> None:
    """Normal completion also reaps an adopted, detached stubborn descendant."""
    _root, probe = fixture(parent, "normal-orphan")
    probe.env["PROBE_MODE"] = "orphan"
    start(probe)
    data = probe.ready()
    write(probe.control / "release", "command may complete\n")
    status, output = probe.finish()
    assert status == 0 and "PASS     omega" in output, output
    assert_reaped(data)
    probe.save(dict(exit=status, normal_cleanup=True, handshake=data))


def relative_output(parent: Path) -> None:
    """Prerequisite directory changes must preserve a relative caller outdir."""
    root, probe = fixture(parent, "relative-output")
    probe.start(["bash", str(root / DRIVER), str(Path(root.name) / "logs")], cwd=parent)
    status, output = probe.finish()
    assert status == 0 and "PASS     omega" in output, output
    assert (root / "logs/preflight/check_merge_containment.log").is_file()
    probe.save(dict(exit=status, relative_output=True))


def main() -> int:
    """Exercise production orchestration with no compiler or RTL substitution claim."""
    with tempfile.TemporaryDirectory(prefix="suite-cancellation-") as scratch:
        parent = Path(scratch)
        with OwnedProcesses():
            for mode in ("pass", "fail", "masked", "timeout"):
                ordinary(parent, mode)
            ownership_refusal(parent)
            normal_orphan(parent)
            relative_output(parent)
            for phase in ("selection", "preflight", "command", "transition"):
                for signum in (signal.SIGINT, signal.SIGTERM):
                    cancellation(parent, phase, signum)
            with OwnedProcesses():
                cancellation(parent, "command", signal.SIGTERM, unsafe=True)
    print("suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, "
          "partial logs, next-suite sentinel, ordinary/masked/timeout, unsafe negative control)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
