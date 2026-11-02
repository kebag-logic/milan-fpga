#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Production sweep cancellation, using disposable known-boundary commands."""

import fcntl
import os
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import owned_process
from owned_process import Cancelled, OwnedProcesses
from process_test_support import (
    FACILITY_MODES, FACILITY_SITE, PROC, Probe, assert_reaped, eventually, identity, install,
    parent as parent_of, running, write,
)

DRIVER = "scripts/run_all_suites.sh"

#: A previous invocation's completed evidence, present in OUT before the run.
PREVIOUS = {"omega.log": "OLD COMPLETED RUN\n", "preflight/old.log": "OLD PREFLIGHT\n"}

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


def start(probe: Probe, *options: str) -> None:
    """Start the normal production entry point with attributable log paths."""
    probe.start(["bash", str(probe.root / DRIVER), str(probe.root / "logs"), *options])


def cancel_report(output: str, root: Path, signum: int, prepared: bool) -> None:
    """The sweep shell names the signal and whether OUT holds this run's logs."""
    lines = output.splitlines()
    name = signal.Signals(signum).name.removeprefix("SIG")
    # The owner's own line reads "signal N"; only the shell's trap names it.
    assert f"CANCELLED: {name}; no completed sweep result" in lines, output
    partial = [line for line in lines if line.startswith("partial logs:")]
    unprepared = "logs were not prepared for this invocation" in lines
    if prepared:
        assert partial == [f"partial logs: {root / 'logs'}"] and not unprepared, output
    else:
        assert partial == [] and unprepared, output
        for relative, text in PREVIOUS.items():
            assert (root / "logs" / relative).read_text() == text, "previous evidence changed"


def ordinary(parent: Path, mode: str) -> None:
    """Normal failures continue; masked verdict and deadline remain distinct."""
    root, probe = fixture(parent, mode)
    probe.env["PROBE_MODE"] = mode
    if mode == "timeout":
        # This deadline covers both suites, and the later one must still finish
        # within it, through a measured 7.96 s host stall (#833).
        probe.env["SUITE_TIMEOUT"] = "10"
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
    for relative, text in PREVIOUS.items():
        write(root / "logs" / relative, text)
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
            cancel_report(output, root, signum, prepared=phase != "selection")
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


def queued(entry: int) -> bool:
    """Has the sweep shell under this launched entry started its real lock wait?"""
    for comm in PROC.glob("[0-9]*/comm"):
        try:
            if comm.read_text() != "flock\n":
                continue
        except OSError:
            continue
        shell = parent_of(int(comm.parent.name))
        if shell is not None and parent_of(shell) == entry:
            return True
    return False


def lock_wait(parent: Path, signum: int) -> None:
    """Queued behind a holder, OUT still holds only the previous run's logs."""
    root, probe = fixture(parent, "cancel-lock-wait-" + signal.Signals(signum).name)
    for relative, text in PREVIOUS.items():
        write(root / "logs" / relative, text)
    # This test is the holder; the sweep's own flock call is the boundary.
    with (root / ".run_all_suites.lock").open("a") as held:
        fcntl.flock(held, fcntl.LOCK_EX)
        start(probe, "--wait")
        eventually(lambda: queued(probe.process.pid) or probe.process.poll() is not None, 15,
                   "sweep never waited for the lock")
        assert probe.process.poll() is None, probe.log()
        probe.signal(signum)
        status, output = probe.finish()
    assert status == 128 + signum and "\nsuites:" not in output, output
    cancel_report(output, root, signum, prepared=False)
    assert not (probe.control / "owner-ran").exists() and not (root / "logs/alpha.log").exists(), output
    probe.save(dict(exit=status, phase="lock-wait", previous_logs_kept=True, unprepared_reported=True))


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


def summarised(text: str) -> bool:
    """Does this transcript carry the completed sweep's summary line?"""
    return re.search(r"^suites: ", text, re.M) is not None


def sweep_shell(pid: int, entry: int) -> int:
    """The ancestor of an owned command whose parent is the launched entry."""
    while (up := parent_of(pid)) != entry:
        assert up not in (None, 0, 1), (pid, up)
        pid = up
    return pid


def lock_free(root: Path) -> bool:
    """Can a new sweep take this tree's lock right now?"""
    with (root / ".run_all_suites.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return False
        fcntl.flock(lock, fcntl.LOCK_UN)
        return True


def hard_stop(parent: Path, how: str, unsafe: bool = False) -> None:
    """A stop the owner cannot handle kills the sweep shell; nothing later starts."""
    label = ("unsafe-" if unsafe else "hard-") + how
    root, probe = fixture(parent, label)
    probe.env["PROBE_MODE"] = "orphan"
    if unsafe:
        # Restore the reviewed defect: owned commands outlive their owner.
        path = root / "scripts/owned_process.py"
        text = path.read_text()
        assert "preexec_fn=self._die_with_owner," in text
        path.write_text(text.replace("preexec_fn=self._die_with_owner,", ""))
    # Containment only: adopts whatever the stop orphans, then reaps it.
    with OwnedProcesses():
        start(probe)
        data = probe.ready()
        entry = probe.process.pid
        shell = sweep_shell(data["pid"], entry)
        shell_start = identity(shell)[0]
        if how == "HUP-group":
            os.killpg(entry, signal.SIGHUP)
        else:
            probe.signal(signal.SIGKILL if how == "KILL" else signal.SIGHUP)
        status, at_death = probe.finish()
        assert status == -(signal.SIGKILL if how == "KILL" else signal.SIGHUP), at_death
        if unsafe:
            assert running(shell, shell_start), "unsafe control: the shell did not outlive its owner"
            write(probe.control / "release", "command may complete\n")
            eventually(lambda: not running(shell, shell_start), 20, "detached sweep never finished")
        else:
            eventually(lambda: not running(shell, shell_start), 15, "sweep shell outlived its owner")
            write(probe.control / "release", "command may complete\n")
            eventually(lambda: not running(data["pid"], data["identities"][str(data["pid"])][0]), 10,
                       "in-flight command did not finish")
            eventually(lambda: lock_free(root), 10, "sweep lock still held")
        after = probe.log()[len(at_death):]
        next_suite = (probe.control / "next-suite").exists()
        if unsafe:
            assert next_suite and "PASS     omega" in after and summarised(after), after
        else:
            assert not next_suite and after == "", after
            assert "PASS     omega" not in at_death and not summarised(at_death), at_death
        lock_owner_left = (root / ".run_all_suites.lock.owner").exists()
    assert not running(shell, shell_start)
    assert_reaped(dict(data, identities={**data["identities"], str(shell): (shell_start, "R")}))
    probe.save(dict(exit=status, stop=how, sweep_shell_exited=True, next_suite=next_suite,
                    output_after_death=after, lock_owner_left=lock_owner_left,
                    unsafe_control_detected=unsafe))


def unsupported(parent: Path, mode: str) -> None:
    """A host lacking a process facility gets the documented refusal, not a traceback."""
    root, probe = fixture(parent, "facility-" + mode)
    write(probe.control / "site/sitecustomize.py", FACILITY_SITE)
    probe.env.update(PYTHONPATH=str(probe.control / "site"), PROBE_FACILITY=mode)
    start(probe)
    status, output = probe.finish()
    assert status == 2 and "REFUSED: process ownership" in output and "Traceback" not in output, output
    assert not (root / "logs").exists() and not (probe.control / "owner-ran").exists(), output
    assert not (root / ".run_all_suites.lock.owner").exists(), output
    probe.save(dict(exit=status, facility=mode, refused=True, sweep_started=False))


def relative_output(parent: Path) -> None:
    """Prerequisite directory changes must preserve a relative caller outdir."""
    root, probe = fixture(parent, "relative-output")
    probe.start(["bash", str(root / DRIVER), str(Path(root.name) / "logs")], cwd=parent)
    status, output = probe.finish()
    assert status == 0 and "PASS     omega" in output, output
    assert (root / "logs/preflight/check_merge_containment.log").is_file()
    probe.save(dict(exit=status, relative_output=True))


#: Only SIGKILL ends this one. It publishes its PID once its handlers are installed.
STUBBORN = r'''
import os, signal, sys, time
from pathlib import Path
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)
Path(sys.argv[1]).write_text(str(os.getpid()))
while True:
    time.sleep(0.02)
'''

#: Records that SIGTERM reached it, then exits, as a cooperative command does.
COOPERATIVE = r'''
import os, signal, sys, time
from pathlib import Path
def stop(_signum, _frame):
    Path(sys.argv[2]).write_text("SIGTERM")
    raise SystemExit(0)
signal.signal(signal.SIGTERM, stop)
Path(sys.argv[1]).write_text(str(os.getpid()))
while True:
    time.sleep(0.02)
'''

#: Leaves its one child running under it until something ends this parent.
PARENT = r'''
import subprocess, sys, time
subprocess.Popen([sys.executable, "-c", sys.argv[1], *sys.argv[2:]])
while True:
    time.sleep(0.02)
'''


@contextmanager
def stages(**seconds: float) -> Iterator[None]:
    """Shorten cleanup stages for a control whose result does not depend on them."""
    saved = {name: getattr(owned_process, name) for name in seconds}
    for name, value in seconds.items():
        setattr(owned_process, name, value)
    try:
        yield
    finally:
        for name, value in saved.items():
            setattr(owned_process, name, value)


def published(path: Path) -> int:
    """Wait for a child's handlers; its published PID is the handshake."""
    eventually(path.exists, 15, f"no handshake at {path}")
    eventually(lambda: path.read_text() != "", 5, f"empty handshake at {path}")
    return int(path.read_text())


def really_kill(pid: int, start: str) -> None:
    """End a control's deliberate survivor, which the owner under test could not."""
    if running(pid, start):
        os.kill(pid, signal.SIGKILL)
    eventually(lambda: not running(pid, start), 15, "deliberate survivor outlived SIGKILL")


def owner_report(parent: Path) -> None:
    """The failure message names what each remaining process is doing (#833)."""
    scratch = parent / "owner-report"
    scratch.mkdir()
    ready = scratch / "ready"
    sleeper = subprocess.Popen([sys.executable, "-c", STUBBORN, str(ready)])
    published(ready)
    eventually(lambda: identity(sleeper.pid)[1] == "S", 15, "handshake child never slept")
    asleep = owned_process._describe(sleeper.pid, os.getpid(), None)
    for field in (f"pid {sleeper.pid} (python", "state S", "wchan ", f"parent {os.getpid()}",
                  f"first parent {os.getpid()}", " age ", " start ", "not sent SIGKILL"):
        assert field in asleep, (field, asleep)
    assert "wchan  " not in asleep, asleep
    assert "new since the first census" in owned_process._describe(sleeper.pid, None, None)
    assert "(first parent 1)" in owned_process._describe(sleeper.pid, 1, None)
    sleeper.kill()
    eventually(lambda: identity(sleeper.pid)[1] == "Z", 15, "killed child never became a zombie")
    zombie = owned_process._describe(sleeper.pid, os.getpid(), 1.5)
    assert "state Z" in zombie and "sent SIGKILL 1.50 s ago" in zombie, zombie
    sleeper.wait()
    assert "exited during this report" in owned_process._describe(sleeper.pid, None, None)
    print("owner-report: " + zombie, flush=True)


def owner_reparented(parent: Path) -> None:
    """A descendant re-parented by the first SIGTERM still receives its own (#833)."""
    scratch = parent / "owner-reparented"
    scratch.mkdir()
    ready, marker = scratch / "ready", scratch / "marker"
    middle = subprocess.Popen([sys.executable, "-c", PARENT, COOPERATIVE, str(ready), str(marker)])
    child = published(ready)
    with OwnedProcesses() as owner:
        census = owner._descendants
        seen = []

        def reparenting() -> dict:
            """Exactly the recorded race: this census names a parent gone before any signal."""
            listed = census()
            if not seen:
                seen.append(True)
                middle.kill()
                eventually(lambda: parent_of(child) == os.getpid(), 15, "child was never re-parented")
            return listed
        owner._descendants = reparenting
    assert marker.exists(), "re-parented descendant was treated as new and never got SIGTERM"
    middle.wait()
    print("owner-reparented: " + str(dict(sigterm_during_grace=True)), flush=True)


def owner_late_exit(parent: Path) -> None:
    """A child that exits during the last census is collected, not failed (#833)."""
    scratch = parent / "owner-late-exit"
    scratch.mkdir()
    ready = scratch / "ready"
    child = subprocess.Popen([sys.executable, "-c", STUBBORN, str(ready)])
    published(ready)
    with stages(GRACE_SECONDS=0.0, KILL_ALL_SECONDS=0.0, REAP_SECONDS=0.4):
        with OwnedProcesses() as owner:
            census = owner._descendants

            def exiting() -> dict:
                """The slow pass measured under load: the child dies in it and the deadline passes."""
                listed = census()
                if child.pid in listed:
                    child.kill()
                    eventually(lambda: identity(child.pid)[1] == "Z", 15, "child never became a zombie")
                    time.sleep(0.45)
                return listed
            owner._descendants = exiting
    child.wait()
    print("owner-late-exit: " + str(dict(collected_at_deadline=True)), flush=True)


def owner_stall(parent: Path) -> None:
    """An owner stalled past every deadline still kills, and fails no one, first (#833)."""
    scratch = parent / "owner-stall"
    scratch.mkdir()
    ready = scratch / "ready"
    child = subprocess.Popen([sys.executable, "-c", STUBBORN, str(ready)])
    pid = published(ready)
    stalls = []
    with stages(GRACE_SECONDS=0.5, KILL_ALL_SECONDS=0.5, REAP_SECONDS=2.0):
        with OwnedProcesses() as owner:
            census = owner._descendants

            def stalling() -> dict:
                """Stall once for longer than the whole 3 s of deadlines, after SIGTERM and before SIGKILL."""
                listed = census()
                if pid in listed and len(stalls) == 1:
                    time.sleep(3.2)
                stalls.append(True)
                return listed
            owner._descendants = stalling
    assert identity(pid) is None or identity(pid)[1] == "Z", identity(pid)
    child.wait()
    print("owner-stall: " + str(dict(stalled_seconds=3.2, killed_after_stall=True)), flush=True)


def owner_shell_window(parent: Path) -> None:
    """A shell resumed past the kill time runs its trap, and what it starts, before any SIGKILL (#833)."""
    scratch = parent / "owner-shell-window"
    scratch.mkdir()
    ready, marker, command = scratch / "ready", scratch / "trap-ran", scratch / "trap-command-ran"
    # The trap's external command outlasts the 1 s such a command had before #833,
    # as the sweep's EXIT trap runs rm, so only the shell's whole window lets it finish.
    script = (f"trap 'echo trapped > \"{marker}\"; sleep 1.5 && echo ran > \"{command}\"; exit 143' TERM\n"
              f"{sys.executable} -c \"$STUBBORN\" \"{ready}\" &\nwait\n")
    env = dict(os.environ, STUBBORN=STUBBORN)
    blocked = []
    with stages(GRACE_SECONDS=0.2, KILL_ALL_SECONDS=0.2):
        try:
            with OwnedProcesses() as owner:
                send = owner._send

                def late(pid: int, start: str, signum: int) -> bool:
                    """The child dies only after the time SIGKILL reaches everything."""
                    now = time.monotonic()
                    if not blocked:
                        blocked.append(now)
                    if signum == signal.SIGKILL and pid != owner.process.pid and now < blocked[0] + 0.7:
                        return False
                    return send(pid, start, signum)
                owner._send = late

                def cancel() -> None:
                    """Cancel the owner once the child has its handlers."""
                    published(ready)
                    os.kill(os.getpid(), signal.SIGTERM)
                threading.Thread(target=cancel, daemon=True).start()
                owner.run(["bash", "-c", script], env=env)
            raise AssertionError("cancellation was not reported")
        except Cancelled:
            pass
    assert marker.exists(), "the shell was killed in the pass that resumed it, before its trap"
    assert command.exists(), "the resumed shell's trap command was killed inside the shell's window"
    print("owner-shell-window: " + str(dict(trap_ran_after_kill_time=True, trap_command_ran=True)), flush=True)


def owner_survivor(parent: Path) -> None:
    """A descendant that outlives SIGKILL fails, with its state, and leaves nothing else (#833)."""
    scratch = parent / "owner-survivor"
    scratch.mkdir()
    ready = scratch / "ready"
    # The trap keeps the shell stopped on SIGTERM; with none, the signal would end it.
    script = f"trap 'exit 143' TERM\n{sys.executable} -c \"$STUBBORN\" \"{ready}\" &\nwait\n"
    env = dict(os.environ, STUBBORN=STUBBORN)
    survivor = []
    shell_start = []
    since = time.monotonic()
    with stages(GRACE_SECONDS=0.2, KILL_ALL_SECONDS=0.2, REAP_SECONDS=0.6):
        with OwnedProcesses() as owner:
            send = owner._send

            def undying(pid: int, start: str, signum: int) -> bool:
                """What no unprivileged control can really build: SIGKILL has no effect."""
                if survivor and pid == survivor[0] and signum == signal.SIGKILL:
                    return True
                return send(pid, start, signum)
            owner._send = undying
            census = owner._descendants

            def bounded() -> dict:
                """Cleanup calls this every pass, so a run that never fails ends here, not in a hang."""
                assert time.monotonic() - since < 30, "a survivor never failed the run"
                return census()
            owner._descendants = bounded

            def cancel() -> None:
                """Cancel the owner once the survivor and its stopped-to-be shell are known."""
                survivor.append(published(ready))
                shell_start.append(identity(owner.process.pid)[0])
                os.kill(os.getpid(), signal.SIGTERM)
            threading.Thread(target=cancel, daemon=True).start()
            try:
                owner.run(["bash", "-c", script], env=env)
                raise AssertionError("a descendant survived SIGKILL and the run did not fail")
            except RuntimeError as exc:
                failure = str(exc)
            # The never-resumed shell must not stay behind this failure, stopped.
            eventually(lambda: not running(owner.process.pid, shell_start[0]), 15, "stopped shell left behind")
            owner.cancel_signal = 0
            really_kill(survivor[0], identity(survivor[0])[0])
            owner._reap()
    assert "CLEANUP FAILED: owned descendants remain" in failure, failure
    for field in (f"pid {survivor[0]} (", "state ", "wchan ", "parent ", " age ", "sent SIGKILL "):
        assert field in failure, (field, failure)
    print("owner-survivor: " + failure, flush=True)


def owner_vanishing() -> None:
    """A listing that always dies inside the census still reaches a verdict (#833)."""
    with stages(GRACE_SECONDS=0.1, KILL_ALL_SECONDS=0.1, REAP_SECONDS=0.3):
        with OwnedProcesses() as owner:
            real_census, real_reap = owner._descendants, owner._reap
            gone = 2 ** 22 + 1
            since = time.monotonic()

            def listed() -> dict:
                """List one process that cannot exist, as if it died inside every census."""
                assert time.monotonic() - since < 15, "cleanup never reached a verdict"
                return {gone: (os.getpid(), "0")}
            owner._descendants = listed
            owner._reap = lambda: {gone}
            try:
                owner._cleanup()
                raise AssertionError("an endless listing did not fail the run")
            except RuntimeError as exc:
                failure = str(exc)
            owner._descendants, owner._reap = real_census, real_reap
    assert "CLEANUP FAILED" in failure and "exited during this report" in failure, failure
    print("owner-vanishing: " + str(dict(verdict_reached=True)), flush=True)


def main() -> int:
    """Exercise production orchestration with no compiler or RTL substitution claim."""
    with tempfile.TemporaryDirectory(prefix="suite-cancellation-") as scratch:
        parent = Path(scratch)
        with OwnedProcesses():
            owner_report(parent)
            owner_reparented(parent)
            owner_late_exit(parent)
            owner_stall(parent)
            owner_shell_window(parent)
            owner_survivor(parent)
            owner_vanishing()
            for mode in ("pass", "fail", "masked", "timeout"):
                ordinary(parent, mode)
            ownership_refusal(parent)
            normal_orphan(parent)
            relative_output(parent)
            for phase in ("selection", "preflight", "command", "transition"):
                for signum in (signal.SIGINT, signal.SIGTERM):
                    cancellation(parent, phase, signum)
            for signum in (signal.SIGINT, signal.SIGTERM):
                lock_wait(parent, signum)
            with OwnedProcesses():
                cancellation(parent, "command", signal.SIGTERM, unsafe=True)
            for how in ("KILL", "HUP", "HUP-group"):
                hard_stop(parent, how)
            hard_stop(parent, "KILL", unsafe=True)
            for mode in FACILITY_MODES:
                unsupported(parent, mode)
    print("suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, "
          "partial logs, attributed cancellation reports, lock wait, next-suite sentinel, "
          "ordinary/masked/timeout, hard KILL/HUP stops, "
          "facility refusals, owner report, re-parenting, late exit, stall, shell window, survivor, "
          "unsafe negative controls)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
