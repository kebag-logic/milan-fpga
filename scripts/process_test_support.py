#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable handshake fixtures for the two production verification drivers."""

import concurrent.futures
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace

import owned_process

PROC = Path("/proc")
ROOT = Path(__file__).resolve().parent.parent
#: Bounds a hang, never a property under test (#833). One real mutation driver took
#: up to 15.1 s under load, beside host stalls of up to 7.96 s. This is four times
#: that driver. On the owner's clock in scripts/owned_process.py, a true survivor's
#: deadline is 14 s into cleanup (GRACE + KILL_ALL + REAP). After a resume, every
#: remaining descendant's deadline is 20 s after the resume (TRAP + REAP), including
#: one the trap started. That resume comes before 14 s: under 34 s. A listing that
#: dies inside every census waits REAP more: under 44 s. The run fails in the first
#: census pass at or past the deadline, at most 0.5 s of owner clock later. Wall
#: time runs ahead of the owner's clock only while a pass takes longer than 0.5 s.
#: With the driver's 15.1 s on top that is 49.6 s, or 59.6 s for the listing: both
#: inside this bound while passes stay within 0.5 s.
FINISH_SECONDS = 60

# A command publishes readiness only after its detached, stubborn child has
# installed both handlers. The release file, never a delay, controls progress.
WORKER = r'''
import hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
if sys.argv[1:] == ["child"]:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    (control / "child-ready").write_text(str(os.getpid()))
    while True:
        time.sleep(0.02)
child = subprocess.Popen([sys.executable, __file__, "child"], start_new_session=True)
deadline = time.monotonic() + 10
while not (control / "child-ready").exists():
    assert time.monotonic() < deadline, "child handshake missing"
    time.sleep(0.01)
data = {"pid": os.getpid(), "child": child.pid, "cwd": str(Path.cwd())}
if (control / "mutation.json").exists():
    catalog = json.loads((control / "mutation.json").read_text())
    root = Path.cwd().parents[2]
    data["mutations"] = [row["name"] for row in catalog
                         if hashlib.sha256((root / row["path"]).read_bytes()).hexdigest() == row["hash"]]
    data["private"] = str(root)
    # Write copied inputs of both required dependencies, including modes. A
    # link back to the caller would corrupt the independently measured snapshot.
    for name in json.loads((control / "private-writes.json").read_text()):
        target = root / name
        target.write_text("private dependency write\n")
        target.chmod(0o700)
(control / "ready.tmp").write_text(json.dumps(data))
(control / "ready.tmp").replace(control / "ready.json")
print("PARTIAL: owned command reached handshake", flush=True)
while not (control / "release").exists():
    time.sleep(0.02)
'''


#: Loaded through PYTHONPATH by a production entry point under test. It removes
#: one process facility, as on a host that lacks it, before that entry runs.
FACILITY_SITE = r'''
import ctypes, os, signal
mode = os.environ.get("PROBE_FACILITY")
if mode == "no-prctl":
    class _NoPrctl:
        """A C library without prctl, as on a host that lacks it."""
    ctypes.CDLL = lambda *args, **kwargs: _NoPrctl()
elif mode == "prctl-fails":
    class _FailingPrctl:
        """A prctl that refuses every option."""
        @staticmethod
        def prctl(*args):
            return -1
    ctypes.CDLL = lambda *args, **kwargs: _FailingPrctl()
elif mode == "no-pidfd-open":
    del os.pidfd_open
elif mode == "no-pidfd-signal":
    del signal.pidfd_send_signal
'''
FACILITY_MODES = ("no-prctl", "prctl-fails", "no-pidfd-open", "no-pidfd-signal")


def git(root: Path, *args: str) -> bytes:
    """Run fixture-only Git without caller Git redirection or index refresh.

    Only standard output is returned: a Git warning is never fixture data.
    """
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    return subprocess.run(["git", "--no-optional-locks", "-C", str(root), *args],
                          env=env, capture_output=True, check=True).stdout


def commit(root: Path) -> None:
    """Commit only a disposable fixture tree."""
    git(root, "add", "-A")
    git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-qm", "Disposable verification fixture")


def install(root: Path, relative: str) -> None:
    """Copy a production file into a disposable fixture without links."""
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, target)


def write(path: Path, text: str, executable: bool = False) -> None:
    """Create one fixture input with explicit permissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    path.chmod(0o755 if executable else 0o644)


def identity(pid: int) -> tuple[str, str] | None:
    """Observe start time and state independently of the production census."""
    try:
        fields = (PROC / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()
        return fields[19], fields[0]
    except (FileNotFoundError, ProcessLookupError):
        return None


def parent(pid: int) -> int | None:
    """Observe the current parent of a process, or None once it is gone."""
    try:
        return int((PROC / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()[1])
    except (FileNotFoundError, ProcessLookupError):
        return None


def running(pid: int, start: str) -> bool:
    """Is this exact identity still executing (neither gone nor a zombie)?"""
    current = identity(pid)
    return current is not None and current[0] == start and current[1] != "Z"


def eventually(condition: Callable[[], bool], seconds: float, what: str) -> None:
    """Wait for an observable condition; the deadline only bounds a failure."""
    deadline = time.monotonic() + seconds
    while not condition():
        assert time.monotonic() < deadline, what
        time.sleep(0.02)


def snapshot(root: Path) -> dict:
    """Record tracked bytes, kinds, full modes and index, recursively at pins."""
    indexed = git(root, "ls-files", "--stage", "-z")
    result = {"index": indexed.hex(), "files": {}}
    for row in indexed.split(b"\0"):
        if not row:
            continue
        metadata, raw_name = row.split(b"\t", 1)
        name = os.fsdecode(raw_name)
        path = root / name
        if metadata.startswith(b"160000"):
            # A gitlink with no checkout of its own would otherwise read the
            # superproject again; record that state instead.
            result["files"][name] = snapshot(path) if (path / ".git").exists() else ["no checkout"]
            continue
        if not path.exists() and not path.is_symlink():
            result["files"][name] = ["absent"]
            continue
        info = path.lstat()
        data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
        result["files"][name] = [info.st_mode, hashlib.sha256(data).hexdigest()]
    return result


class Probe:
    """Run a driver in its own session and retain its original transcripts."""

    def __init__(self, root: Path, label: str) -> None:
        self.root = root
        self.label = label
        self.control = root.parent / (label + "-control")
        self.control.mkdir()
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_")}
        self.env.update(PROBE_CONTROL=str(self.control), PYTHONDONTWRITEBYTECODE="1",
                        TMPDIR=str(self.control))
        write(self.control / "worker.py", WORKER)
        self.process = None

    def start(self, argv: list[str], cwd: Path | None = None) -> None:
        """Launch a production driver; keep output even if its assertion fails."""
        with (self.control / "driver.log").open("wb") as output:
            self.process = subprocess.Popen(argv, cwd=cwd or self.root, env=self.env,
                                            start_new_session=True, stdout=output,
                                            stderr=subprocess.STDOUT)

    def ready(self) -> dict:
        """Wait for a published boundary, refusing premature driver exit."""
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            path = self.control / "ready.json"
            if path.exists():
                data = json.loads(path.read_text())
                data["identities"] = {str(pid): identity(pid)
                                      for pid in (data["pid"], data["child"])}
                assert all(data["identities"].values()), data
                return data
            assert self.process.poll() is None, self.log()
            time.sleep(0.01)
        raise AssertionError(f"{self.label}: missing boundary: {self.log()}")

    def signal(self, signum: int) -> None:
        """Signal the unreaped driver through a stable identity handle."""
        fd = os.pidfd_open(self.process.pid)
        try:
            signal.pidfd_send_signal(fd, signum)
        finally:
            os.close(fd)

    def finish(self) -> tuple[int, str]:
        """Read the exact exit and transcript after bounded driver completion."""
        status = self.process.wait(timeout=FINISH_SECONDS)
        self._retain(dict(raw_exit=status))
        return status, self.log()

    def log(self) -> str:
        """Return the unfiltered driver transcript."""
        return (self.control / "driver.log").read_text()

    def save(self, evidence: dict) -> None:
        """Print attributable identities; optionally retain every raw fixture log."""
        print(self.label + ": " + json.dumps(evidence, sort_keys=True), flush=True)
        self._retain(evidence)

    def _retain(self, evidence):
        destination = self.env.get("VERIFICATION_TEST_LOGS")
        if destination:
            target = Path(destination) / self.label
            target.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.control / "driver.log", target / "driver.log")
            (target / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
            logs = self.root / "logs"
            if logs.exists():
                shutil.copytree(logs, target / "suite-logs", dirs_exist_ok=True)


def assert_reaped(data: dict) -> None:
    """Require gone identities, rejecting both live and unreaped zombie state."""
    for pid, previous in data["identities"].items():
        current = identity(int(pid))
        assert current is None or current[0] != previous[0], (pid, previous, current)


#: A tick of the starved owner's clock: about a microsecond, and exact in binary, as every time on that clock is.
TICK = 2.0 ** -20
#: The resume-timing matrix's classes of census pass, each at its earliest and its latest pass.
RESUME_MATRIX = (("first-pass", 0), ("second-pass", TICK), ("last in-grace", 2 - TICK), ("first past-grace", 2),
                 ("second past-grace", 2 + TICK), ("last-pass", 14 - TICK))


def window(resume: float, windowed: tuple[str, ...] = ("shell", "trap command")) -> list[tuple]:
    """What a shell resumed then is sent, as stated, with what shares its window, and when the run fails."""
    return [*[(0, "SIGTERM", "child")][:resume > 0], *[(2, "SIGKILL", "child")][:resume > 2],
            (resume, "SIGCONT", "shell"), *[(resume + 10, "SIGKILL", name) for name in windowed],
            *[(resume + 20, "SIGKILL", name) for name in windowed], (resume + 20, "verdict")]


def starved_cleanup(owner: owned_process.OwnedProcesses, listing: Callable[[float], dict], names: dict,
                    stated: list[tuple], reaped: Callable[[float], set] = lambda _clock: set()) -> list[tuple]:
    """Run one cleanup over a listing on a starved owner's clock; return each signal and the verdict by that clock.

    A pass longer than the cap, half a second, counts as the cap, whether it took a tick more or an hour. One
    shorter counts its own length: the clock lands a tick short of each time in `stated`, then on it, so the
    pass before each stated time is a tick early. Only what `reaped` returns is ever collected. A verdict
    that does not report a real process's wall time since its first SIGKILL adds that time to the events.
    """
    now, clock, events, killed = [0.0], [0.0], [], {}

    def pause(_seconds: float) -> None:
        """One pass's pause, whatever it asks for."""
        due = min((event[0] for event in stated if event[0] > clock[0]), default=clock[0] + 1.0)
        slow = 3600.0 if int(clock[0] * 2) % 2 else 0.5 + TICK
        step = max(due - TICK - clock[0], TICK) if due - clock[0] <= 0.5 else slow
        now[0] += step
        clock[0] += min(step, 0.5)

    def census() -> dict:
        """List what the listing lists at this time."""
        assert clock[0] < 100, "cleanup never reached a verdict on the owner's clock"
        return listing(clock[0])

    def send(pid: int, _start: str, signum: int) -> bool:
        """Note the signal and its time; no process receives it."""
        events.append((clock[0], signal.Signals(signum).name, names[pid]))
        if signum == signal.SIGKILL:
            killed.setdefault(pid, now[0])
        return True
    real = owned_process.time
    owned_process.time = SimpleNamespace(monotonic=lambda: now[0], sleep=pause)
    owner._descendants, owner._reap, owner._send = census, lambda: reaped(clock[0]), send
    owner._signal = lambda _fd, signum: events.append((clock[0], signal.Signals(signum).name, "shell"))
    try:
        owner._cleanup()
        events.append((clock[0], "no verdict"))
    except RuntimeError as exc:
        events.append((clock[0], "verdict"))
        ages = [f"sent SIGKILL {now[0] - at:.2f} s ago" for pid, at in killed.items()
                if pid == os.getpid() and pid in listing(clock[0])]
        events += [("not in the report", age) for age in ages if age not in str(exc)]
    finally:
        owned_process.time = real
        del owner._descendants, owner._reap, owner._send, owner._signal
    return events


#: Every published mutant of scripts/owned_process.py for #833, so that the next
#: one has a home. Each breaks a row of the cleanup table in docs/testing/TESTING.md,
#: which names it in that row, and names the owner control that must fail under it,
#: with words of that failure; or names none, with why it breaks no row.
#: Its edits follow, and each must match the product exactly once.
MUTANTS: dict[str, tuple] = {
    "none": (None, "the product as it stands; every control passes"),
    "cleanup-does-nothing": ("owner_reparented", "re-parented descendant was treated as new and never got SIGTERM",
        ("        started = last = time.monotonic()\n",
         "        return\n        started = last = time.monotonic()\n")),
    "identity-start-holds-parent": ("owner_reparented", "re-parented descendant was treated as new and never"
                                                        " got SIGTERM",
        ("return None if fields is None else (int(fields[1]), fields[19])",
         "return None if fields is None else (int(fields[1]), fields[1] + ':' + fields[19])")),
    "identity-keys-hold-parent": ("owner_reparented", "re-parented descendant was treated as new and never"
                                                      " got SIGTERM",
        ("initial = {(pid, start): parent for pid, (parent, start) in owned.items()}",
         "initial = {(pid, start, parent): parent for pid, (parent, start) in owned.items()}"),
        ("first = {pid: parent for (pid, _start), parent in initial.items()}",
         "first = {pid: parent for (pid, _start, _p), parent in initial.items()}"),
        ("if (pid, start) not in initial:\n                        continue",
         "if (pid, start, _parent) not in initial:\n                        continue"),
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start, _parent) not in initial and resumed is not None:"),
        ("if key not in notified and self._send(pid, start, signum):",
         "if key not in notified and _identity(pid) == (_parent, start) and self._send(pid, start, signum):")),
    "identity-first-census-holds-parent": ("owner_reparented", "re-parented descendant was treated as new"
                                                               " and never got SIGTERM",
        ("initial = {(pid, start): parent for pid, (parent, start) in owned.items()}",
         "initial = {(pid, start, parent): parent for pid, (parent, start) in owned.items()}")),
    "identity-includes-parent": ("owner_reparented", "re-parented descendant was treated as new and never"
                                                     " got SIGTERM",
        ("                    if (pid, start) not in initial:\n                        continue",
         "                    if initial.get((pid, start)) != _parent:\n                        continue"),
        ("                key = (pid, start, signum)\n",
         "                if _identity(pid) != (_parent, start):\n                    continue\n"
         "                key = (pid, start, signum)\n")),
    "identity-checks-parent-before-send": ("owner_reparented", "re-parented descendant was treated as new"
                                                               " and never got SIGTERM",
        ("            for pid, (_parent, start) in owned.items():\n                # A notified shell",
         "            for pid, (_parent, start) in owned.items():\n"
         "                if _identity(pid) != (_parent, start):\n                    continue\n"
         "                if signum != signal.SIGKILL and initial.get((pid, start)) != _parent:\n"
         "                    continue\n                # A notified shell")),
    "sigterm-checks-parent": (None, "equivalent: the first pass sends SIGTERM to every descendant of the"
                                    " first census under the parent that census read, so this refuses only a"
                                    " SIGTERM already sent",
        ("                    if (pid, start) not in initial:\n                        continue",
         "                    if initial.get((pid, start)) != _parent:\n                        continue")),
    "send-checks-parent": ("owner_reparented", "SIGTERM waited for a later census",
        ("                key = (pid, start, signum)\n",
         "                if _identity(pid) != (_parent, start):\n                    continue\n"
         "                key = (pid, start, signum)\n")),
    "no-start-recheck": ("owner_reused_identity", "a census entry whose process was replaced was signalled",
        ("            if identity is None or identity[1] != start:\n", "            if identity is None:\n")),
    "no-reap-after-census": ("owner_late_exit", "CLEANUP FAILED: owned descendants remain",
        ("reaped = self._reap()", "reaped = set()")),
    "owned-is-census": ("owner_late_exit", "CLEANUP FAILED: owned descendants remain",
        ("owned = {pid: entry for pid, entry in census.items() if pid not in reaped}", "owned = dict(census)")),
    "deadline-wall-clock": ("owner_stall", "the stall was charged in full",
        ("clock += min(now - last, MAX_PASS_SECONDS)", "clock += now - last")),
    "pass-cap-1s": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("MAX_PASS_SECONDS = 0.5\n", "MAX_PASS_SECONDS = 1.0\n")),
    "pass-cap-1.5s": ("owner_stall", "the stall was charged in full",
        ("MAX_PASS_SECONDS = 0.5", "MAX_PASS_SECONDS = 1.5")),
    "pass-cap-5s": ("owner_stall", "the stall was charged in full",
        ("MAX_PASS_SECONDS = 0.5", "MAX_PASS_SECONDS = 5.0")),
    "windows-2s": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("TRAP_SECONDS = 10.0", "TRAP_SECONDS = 2.0"),
        ("REAP_SECONDS = 10.0", "REAP_SECONDS = 2.0")),
    "reap-window-2s": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("REAP_SECONDS = 10.0", "REAP_SECONDS = 2.0")),
    "no-shell-window": ("owner_shell_window", "the shell was killed in the pass that resumed it, before its trap",
        ("                kill_all = max(kill_all, clock + TRAP_SECONDS)\n", "")),
    "no-shell-window-kept": ("owner_shell_window", "the shell was killed in the pass that resumed it, before"
                                                   " its trap",
        ("kill_all = max(kill_all, clock + TRAP_SECONDS)", "kill_all = kill_all")),
    "no-shell-window-pass": ("owner_shell_window", "the shell was killed in the pass that resumed it, before"
                                                   " its trap",
        ("kill_all = max(kill_all, clock + TRAP_SECONDS)", "pass")),
    "no-trap-window": ("owner_shell_window", "the shell was killed in the pass that resumed it, before its trap",
        ("kill_all = max(kill_all, clock + TRAP_SECONDS)", "kill_all = max(kill_all, clock)")),
    "root-killed-unresumed": ("owner_shell_window", "the shell was killed in the pass that resumed it,"
                                                    " before its trap",
        ("(resumed is None or clock < kill_all)", "clock < kill_all")),
    "shell-killed-when-resumed": ("owner_shell_window", "the shell was killed in the pass that resumed it,"
                                                        " before its trap",
        ("(resumed is None or clock < kill_all):", "resumed is None:")),
    "shell-window-one-pass": ("owner_stated_seconds", "a late resume's stated seconds were not kept",
        ("(resumed is None or clock < kill_all):", "(resumed is None or clock <= resumed):")),
    "shell-window-1s": ("owner_shell_window", "the resumed shell was killed inside its own window, with no"
                                              " child to spare it",
        ("(resumed is None or clock < kill_all):", "(resumed is None or clock < resumed + 1.0):")),
    "trap-commands-no-window": ("owner_shell_window", "the resumed shell's trap command was killed inside"
                                                      " the shell's window",
        ("                    if (pid, start) not in initial and resumed is not None:\n"
         "                        continue\n",
         "")),
    "trap-commands-never-spared": ("owner_shell_window", "the resumed shell's trap command was killed inside"
                                                         " the shell's window",
        ("if (pid, start) not in initial and resumed is not None:", "if False:")),
    "trap-commands-1s": ("owner_stated_seconds", "a late resume's stated seconds were not kept",
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and clock < resumed + 1.0:")),
    "resume-collected-shell": ("owner_late_cancel", "a cancel after the shell was collected resumed it",
        ("resumed is None and root_pid in owned and not (live - {root_pid}):",
         "resumed is None and not (live - {root_pid}):")),
    "window-without-resume": ("owner_late_cancel", "cleanup never reached a verdict after a late cancel",
        ("resumed is None and root_pid in owned and not (live - {root_pid}):",
         "resumed is None and not (live - {root_pid}):"),
        ("                self._signal(self.root_fd, signal.SIGCONT)\n",
         "                if root_pid in owned:\n                    self._signal(self.root_fd, signal.SIGCONT)\n")),
    "rearm-without-sigcont": ("owner_late_cancel", "cleanup never reached a verdict after a late cancel",
        ("resumed is None and root_pid in owned and not (live - {root_pid}):",
         "resumed is None and not (live - {root_pid}):"),
        ("self._signal(self.root_fd, signal.SIGCONT)\n", "pass\n")),
    "resume-while-listed": ("owner_late_cancel", "a cancel after the shell was collected resumed it",
        ("resumed is None and root_pid in owned and not (live - {root_pid}):",
         "resumed is None and root_pid in census and not (live - {root_pid}):")),
    "no-kill-before-raise": ("owner_survivor", "stopped shell left behind",
        ("                for pid, (_parent, start) in owned.items():\n"
         "                    self._send(pid, start, signal.SIGKILL)\n",
         "")),
    "no-kill-before-raise-empty": ("owner_survivor", "stopped shell left behind",
        ("for pid, (_parent, start) in owned.items():\n                    self._send(pid, start, signal.SIGKILL)",
         "for pid, (_parent, start) in ():\n                    self._send(pid, start, signal.SIGKILL)")),
    "kill-before-fail-spares-shell": ("owner_survivor", "stopped shell left behind",
        ("                for pid, (_parent, start) in owned.items():\n"
         "                    self._send(pid, start, signal.SIGKILL)\n",
         "                for pid, (_parent, start) in owned.items():\n"
         "                    if self.process is None or pid != self.process.pid:\n"
         "                        self._send(pid, start, signal.SIGKILL)\n")),
    "endless-unbounded": ("owner_vanishing", "cleanup never reached a verdict",
        ("(owned or clock >= limit + REAP_SECONDS)", "owned")),
    "survivor-never-fails": ("owner_survivor", "a survivor never failed the run",
        ("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):", "if False:")),
    "survivor-never-fails-guarded": ("owner_survivor", "a survivor never failed the run",
        ("if clock >= limit and (owned", "if False and (owned")),
    "trust-sigkill": ("owner_survivor", "a survivor never failed the run",
        ("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):",
         "if clock >= limit and (any(p not in killed and (self.process is None or p != self.process.pid) for"
         " p in owned) or not owned and clock >= limit + REAP_SECONDS):")),
    "killed-counts-as-gone": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("owned = {pid: entry for pid, entry in census.items() if pid not in reaped}",
         "owned = {pid: entry for pid, entry in census.items() if pid not in reaped and pid not in killed}")),
    "report-without-state": ("owner_report", "('state S'",
        ("state {fields[0]} wchan", "wchan")),
    "report-without-wchan": ("owner_report", "('wchan '",
        ("wchan {wchan} parent", "parent")),
    "report-without-state-or-wchan": ("owner_report", "('state S'",
        ("state {fields[0]} wchan {wchan} ", "")),
    "grace-1s": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("GRACE_SECONDS = 2.0", "GRACE_SECONDS = 1.0")),
    "return-with-zombies": ("owner_late_exit", "cleanup returned with an owned child unreaped",
        ("            if not census:\n                return\n",
         "            if not [pid for pid in census if _live(pid)]:\n                return\n")),
    "vanishing-waits-no-more": ("owner_late_exit", "CLEANUP FAILED: owned descendants remain",
        ("(owned or clock >= limit + REAP_SECONDS)", "(owned or clock >= limit)")),
    "resume-with-one-live": ("owner_stated_seconds", "a late resume's stated seconds were not kept",
        ("and not (live - {root_pid}):", "and len(live - {root_pid}) <= 1:")),
    "clock-always-cap": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("clock += min(now - last, MAX_PASS_SECONDS)", "clock += MAX_PASS_SECONDS")),
    "killed-not-recorded": ("owner_survivor", "('sent SIGKILL '",
        ("                        killed.setdefault(pid, time.monotonic())\n", "                        pass\n")),
    "no-sigcont-after-send": (None, "breaks no row: SIGCONT after each signal is on the table's not-pinned list",
        ("            self._signal(fd, signal.SIGCONT)\n            return True\n", "            return True\n")),
    "sigterm-to-new": ("owner_stated_seconds", "a first-pass resume's stated seconds were not kept",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    pass\n                elif")),
    "no-leaf-first": (None, "breaks no row: a first-census parent's extra second after grace is on the table's"
                            " not-pinned list",
        ("if clock < deadline + 1.0 and pid in initial.values():", "if False:")),
    "signal-by-number": ("owner_reused_identity", "a census entry was signalled by its number",
        ("            self._signal(fd, signum)\n            self._signal(fd, signal.SIGCONT)\n",
         "            os.kill(pid, signum)\n            os.kill(pid, signal.SIGCONT)\n")),
    "parent-spared-past-kill-all": ("owner_stated_seconds", "a stubborn parent's stated seconds were not kept",
        ("                elif clock < kill_all:\n",
         "                elif clock < kill_all or any(parent == pid and child in live"
         " for child, (parent, _start) in owned.items()):\n")),
    "parents-killed-at-grace": ("owner_stated_seconds", "a stubborn parent's stated seconds were not kept",
        ("                    if clock < deadline + 1.0 and pid in initial.values():\n"
         "                        continue\n"
         "                    if any(parent == pid and child in live for child, (parent, _start) in owned.items()):\n"
         "                        continue\n",
         "")),
    "vanishing-waits-30s-more": ("owner_stated_seconds", "a vanishing listing's stated seconds were not kept",
        ("(owned or clock >= limit + REAP_SECONDS)", "(owned or clock >= limit + 3 * REAP_SECONDS)")),
    "report-without-current-parent": ("owner_report", "the report's current parent is not its own field",
        ("parent {fields[1]} ", "")),
    "report-age-in-ticks": ("owner_report", "the report's age is not the process's own",
        ("int(fields[19]) / os.sysconf('SC_CLK_TCK')", "int(fields[19])")),
    "check-before-open": ("owner_reused_identity", "a census entry was signalled by its number",
        ("        try:\n            fd = os.pidfd_open(pid)\n"
         "        except ProcessLookupError:\n            return False\n"
         "        try:\n            identity = _identity(pid)\n"
         "            if identity is None or identity[1] != start:\n                return False\n",
         "        identity = _identity(pid)\n"
         "        if identity is None or identity[1] != start:\n            return False\n"
         "        try:\n            fd = os.pidfd_open(pid)\n"
         "        except ProcessLookupError:\n            return False\n"
         "        try:\n")),
    "no-sigterm": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    continue\n                elif")),
    "kill-all-a-pass-late": ("owner_stated_seconds", "a stubborn parent's stated seconds were not kept",
        ("                elif clock < kill_all:\n", "                elif clock <= kill_all:\n")),
    "verdict-past-deadline": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):",
         "if clock > limit and (owned or clock >= limit + REAP_SECONDS):")),
    "resume-only-when-alone": ("owner_stated_seconds", "a late resume's stated seconds were not kept",
        ("and not (live - {root_pid}):", "and not (set(owned) - {root_pid}):")),
    "trap-window-from-grace": ("owner_stated_seconds", "a late resume's stated seconds were not kept",
        ("kill_all = max(kill_all, clock + TRAP_SECONDS)", "kill_all = max(kill_all, deadline + TRAP_SECONDS)")),
    "shell-spared-only-while-stopped": ("owner_shell_window", "the shell was killed in the pass that resumed it,"
                                                              " before its trap",
        ("(resumed is None or clock < kill_all)", "(resumed is None or (_stat(pid) or ['T'])[0] == 'T')")),
    "trap-commands-until-grace": ("owner_shell_window", "the resumed shell's trap command was killed inside the"
                                                        " shell's window",
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and clock < deadline + 1.0:")),
    "cap-on-total": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("clock += min(now - last, MAX_PASS_SECONDS)", "clock = min(clock + now - last, MAX_PASS_SECONDS * passes)")),
    "first-pass-full-cap": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("        started = last = time.monotonic()\n",
         "        started = time.monotonic()\n        last = started - MAX_PASS_SECONDS\n")),
    "vanishing-waits-from-grace": ("owner_stated_seconds", "a vanishing listing's stated seconds were not kept",
        ("(owned or clock >= limit + REAP_SECONDS)", "(owned or clock >= deadline + 2 * REAP_SECONDS)")),
    "verdict-counts-census": ("owner_late_exit", "CLEANUP FAILED: owned descendants remain",
        ("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):",
         "if clock >= limit and (census or clock >= limit + REAP_SECONDS):")),
    "sigterm-needs-live-parent": ("owner_reparented", "SIGTERM waited for a later census",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial or not _live(_parent):\n                        continue\n"
         "                elif")),
    "resume-unless-reaped-now": ("owner_late_cancel", "a cancel after the shell was collected resumed it",
        ("resumed is None and root_pid in owned and not (live - {root_pid}):",
         "resumed is None and root_pid not in reaped and not (live - {root_pid}):")),
    "verdict-kills-only-the-killed": ("owner_survivor", "stopped shell left behind",
        ("                for pid, (_parent, start) in owned.items():\n"
         "                    self._send(pid, start, signal.SIGKILL)\n",
         "                for pid, (_parent, start) in owned.items():\n"
         "                    if pid in killed:\n"
         "                        self._send(pid, start, signal.SIGKILL)\n")),
    "report-parent-is-first-parent": ("owner_report", "the report's current parent is not its own field",
        ("parent {fields[1]} ", "parent {first_parent} ")),
    "sigkill-by-number": ("owner_reused_identity", "a census entry was signalled by its number",
        ("            self._signal(fd, signum)\n            self._signal(fd, signal.SIGCONT)\n",
         "            if signum == signal.SIGKILL:\n                os.kill(pid, signum)\n"
         "            else:\n                self._signal(fd, signum)\n"
         "            self._signal(fd, signal.SIGCONT)\n")),
    "sigcont-by-number": ("owner_reused_identity", "a census entry was signalled by its number",
        ("            self._signal(fd, signum)\n            self._signal(fd, signal.SIGCONT)\n",
         "            self._signal(fd, signum)\n            os.kill(pid, signal.SIGCONT)\n")),
    "resume-not-before-grace": ("owner_stated_seconds", "a first-pass resume's stated seconds were not kept",
        ("and root_pid in owned and not (live - {root_pid}):",
         "and root_pid in owned and not (live - {root_pid}) and clock >= deadline:")),
    "resume-not-first-pass": ("owner_stated_seconds", "a first-pass resume's stated seconds were not kept",
        ("and root_pid in owned and not (live - {root_pid}):",
         "and root_pid in owned and not (live - {root_pid}) and passes > 1:")),
    "sigterm-trap-commands": ("owner_stated_seconds", "a first-pass resume's stated seconds were not kept",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial and resumed is None:\n                        continue\n"
         "                elif")),
    "sigterm-to-new-before-resume": ("owner_stated_seconds", "a new descendant's stated seconds were not kept",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial and resumed is not None:\n"
         "                        continue\n                elif")),
    "sigcont-by-number-after-kill": ("owner_reused_identity", "a census entry was signalled by its number",
        ("            self._signal(fd, signum)\n            self._signal(fd, signal.SIGCONT)\n",
         "            self._signal(fd, signum)\n"
         "            if signum == signal.SIGKILL:\n                os.kill(pid, signal.SIGCONT)\n"
         "            else:\n                self._signal(fd, signal.SIGCONT)\n")),
    "recheck-spares-sigkill": ("owner_reused_identity", "a census entry whose process was replaced was signalled",
        ("            if identity is None or identity[1] != start:\n",
         "            if identity is None or identity[1] != start and signum != signal.SIGKILL:\n")),
    "grace-a-tick-short": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("GRACE_SECONDS = 2.0", "GRACE_SECONDS = 2.0 - 2 ** -19")),
    "kill-all-a-tick-early": ("owner_stated_seconds", "a stubborn parent's stated seconds were not kept",
        ("                elif clock < kill_all:\n", "                elif clock < kill_all - 2 ** -19:\n")),
    "verdict-a-tick-early": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("limit = kill_all + REAP_SECONDS\n", "limit = kill_all + REAP_SECONDS - 2 ** -19\n")),
    "verdict-waits-for-resume": ("owner_stated_seconds", "cleanup never reached a verdict on the owner's clock",
        ("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):",
         "if clock >= limit and (resumed is not None or not self.root_notified) and (owned or"
         " clock >= limit + REAP_SECONDS):")),
    "no-resume-before-verdict": ("owner_stated_seconds", "a last-pass resume's stated seconds were not kept",
        ("and root_pid in owned and not (live - {root_pid}):",
         "and root_pid in owned and not (live - {root_pid}) and clock + MAX_PASS_SECONDS < kill_all + REAP_SECONDS:")),
    "trap-window-a-tick-short": ("owner_stated_seconds", "a late resume's stated seconds were not kept",
        ("TRAP_SECONDS = 10.0", "TRAP_SECONDS = 10.0 - 2 ** -19")),
    "no-window-inside-grace": ("owner_stated_seconds", "a first-pass resume's stated seconds were not kept",
        ("kill_all = max(kill_all, clock + TRAP_SECONDS)",
         "kill_all = max(kill_all, clock + TRAP_SECONDS) if clock >= deadline else kill_all")),
    "trap-commands-spared-only-past-grace": ("owner_stated_seconds", "a first-pass resume's stated seconds were"
                                                                     " not kept",
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and resumed >= deadline:")),
    "cap-lifted-past-a-minute": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("clock += min(now - last, MAX_PASS_SECONDS)",
         "clock += min(now - last, MAX_PASS_SECONDS) if now - last < 60 else now - last")),
    "tick-passes-count-nothing": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("clock += min(now - last, MAX_PASS_SECONDS)",
         "clock += min(now - last, MAX_PASS_SECONDS) if now - last >= 0.001 else 0")),
    "vanishing-verdict-ignores-resume": ("owner_stated_seconds", "a resumed vanishing listing's stated seconds were"
                                                                 " not kept",
        ("(owned or clock >= limit + REAP_SECONDS)",
         "(owned or clock >= GRACE_SECONDS + KILL_ALL_SECONDS + 2 * REAP_SECONDS)")),
    "no-reap-after-first-census": ("owner_late_exit", "CLEANUP FAILED: owned descendants remain",
        ("reaped = self._reap()", "reaped = self._reap() if passes > 1 else set()")),
    "sigterm-rechecks-parent": ("owner_reparented", "SIGTERM waited for a later census",
        ("                key = (pid, start, signum)\n",
         "                if signum == signal.SIGTERM and _identity(pid) != (_parent, start):\n"
         "                    continue\n                key = (pid, start, signum)\n")),
    "resume-collected-shell-past-grace": ("owner_late_cancel", "a cancel after the shell was collected resumed it",
        ("resumed is None and root_pid in owned and not (live - {root_pid}):",
         "resumed is None and (root_pid in owned or clock >= deadline) and not (live - {root_pid}):")),
    "verdict-sends-sigterm": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("self._send(pid, start, signal.SIGKILL)", "self._send(pid, start, signal.SIGTERM)")),
    "killed-ago-from-start": ("owner_stated_seconds", "not in the report",
        ("now - killed[pid] if pid in killed else None", "now - started if pid in killed else None")),
    "return-before-confirm": ("owner_vanishing", "an endless listing did not fail the run",
        ("            owned = {pid: entry for pid, entry in census.items() if pid not in reaped}\n",
         "            owned = {pid: entry for pid, entry in census.items() if pid not in reaped}\n"
         "            if not owned:\n                return\n")),
    "check-before-open-for-sigkill": ("owner_reused_identity", "a census entry was signalled by its number",
        ("        try:\n            fd = os.pidfd_open(pid)\n"
         "        except ProcessLookupError:\n            return False\n"
         "        try:\n            identity = _identity(pid)\n",
         "        early = _identity(pid) if signum == signal.SIGKILL else None\n"
         "        try:\n            fd = os.pidfd_open(pid)\n"
         "        except ProcessLookupError:\n            return False\n"
         "        try:\n            identity = early or _identity(pid)\n")),
    "no-resume-later-in-grace": ("owner_stated_seconds", "an in-grace resume's stated seconds were not kept",
        ("and root_pid in owned and not (live - {root_pid}):",
         "and root_pid in owned and not (live - {root_pid}) and not (passes > 1 and clock < deadline):")),
    "sigterm-trap-command-unless-first-pass-resume": ("owner_stated_seconds", "an in-grace resume's stated seconds"
                                                                              " were not kept",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial and (resumed is None or resumed == 0.0):\n"
         "                        continue\n                elif")),
    "sigterm-trap-command-after-later-grace-resume": ("owner_stated_seconds", "an in-grace resume's stated seconds"
                                                                              " were not kept",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial and not (resumed is not None and resumed > 0):\n"
         "                        continue\n                elif")),
    "trap-window-not-later-in-grace": ("owner_stated_seconds", "an in-grace resume's stated seconds were not kept",
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and (resumed == 0.0 or resumed >= deadline):")),
    "sigterm-to-new-while-shell-stopped": ("owner_stated_seconds", "a new descendant beside a stopped shell's stated"
                                                                   " seconds were not kept",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial and (resumed is not None or not self.root_notified):\n"
         "                        continue\n                elif")),
    "sigterm-to-new-after-1s": ("owner_stated_seconds", "a first-pass resume's stated seconds were not kept",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial and clock < 1.0:\n"
         "                        continue\n                elif")),
    "no-window-later-in-grace": ("owner_stated_seconds", "an in-grace resume's stated seconds were not kept",
        ("kill_all = max(kill_all, clock + TRAP_SECONDS)",
         "kill_all = max(kill_all, clock + TRAP_SECONDS) if clock >= deadline or passes == 1 else kill_all")),
    "lone-first-pass-shell-needs-a-child": ("owner_stated_seconds", "a lone first-pass resume's stated seconds were"
                                                                    " not kept",
        ("resumed = clock\n", "resumed, edge = clock, passes == 1\n"),
        ("(resumed is None or clock < kill_all):",
         "(resumed is None or clock < kill_all and (clock == resumed or not edge"
         " or any(parent == pid for _child, (parent, _start) in owned.items()))):")),
    "first-pass-trap-command-sigtermed": ("owner_stated_seconds", "a first-pass resume's stated seconds were not kept",
        ("resumed = clock\n", "resumed, edge = clock, passes == 1\n"),
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial and not (resumed is not None and edge):\n"
         "                        continue\n                elif")),
    "lone-second-pass-shell-needs-a-child": ("owner_stated_seconds", "a lone second-pass resume's stated seconds"
                                                                     " were not kept",
        ("resumed = clock\n", "resumed, edge = clock, passes == 2\n"),
        ("(resumed is None or clock < kill_all):",
         "(resumed is None or clock < kill_all and (clock == resumed or not edge"
         " or any(parent == pid for _child, (parent, _start) in owned.items()))):")),
    "second-pass-trap-command-sigtermed": ("owner_stated_seconds", "a second-pass resume and its trap command's"
                                                                   " stated seconds were not kept",
        ("resumed = clock\n", "resumed, edge = clock, passes == 2\n"),
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial and not (resumed is not None and edge):\n"
         "                        continue\n                elif")),
    "lone-last-in-grace-shell-needs-a-child": ("owner_stated_seconds", "a lone last in-grace resume's stated"
                                                                       " seconds were not kept",
        ("resumed = clock\n", "resumed, edge = clock, deadline - MAX_PASS_SECONDS <= clock < deadline\n"),
        ("(resumed is None or clock < kill_all):",
         "(resumed is None or clock < kill_all and (clock == resumed or not edge"
         " or any(parent == pid for _child, (parent, _start) in owned.items()))):")),
    "last-in-grace-trap-command-unspared": ("owner_stated_seconds", "a last in-grace resume and its trap command's"
                                                                    " stated seconds were not kept",
        ("resumed = clock\n", "resumed, edge = clock, deadline - MAX_PASS_SECONDS <= clock < deadline\n"),
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and not edge:")),
    "lone-first-past-grace-shell-needs-a-child": ("owner_stated_seconds", "a lone first past-grace resume's stated"
                                                                          " seconds were not kept",
        ("passes = 0\n", "passes = late = 0\n"),
        ("            last = now\n", "            last = now\n            late += clock >= deadline\n"),
        ("resumed = clock\n", "resumed, edge = clock, late == 1\n"),
        ("(resumed is None or clock < kill_all):",
         "(resumed is None or clock < kill_all and (clock == resumed or not edge"
         " or any(parent == pid for _child, (parent, _start) in owned.items()))):")),
    "first-past-grace-trap-command-unspared": ("owner_stated_seconds", "a first past-grace resume and its trap"
                                                                       " command's stated seconds were not kept",
        ("passes = 0\n", "passes = late = 0\n"),
        ("            last = now\n", "            last = now\n            late += clock >= deadline\n"),
        ("resumed = clock\n", "resumed, edge = clock, late == 1\n"),
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and not edge:")),
    "lone-second-past-grace-shell-needs-a-child": ("owner_stated_seconds", "a lone second past-grace resume's"
                                                                           " stated seconds were not kept",
        ("passes = 0\n", "passes = late = 0\n"),
        ("            last = now\n", "            last = now\n            late += clock >= deadline\n"),
        ("resumed = clock\n", "resumed, edge = clock, late == 2\n"),
        ("(resumed is None or clock < kill_all):",
         "(resumed is None or clock < kill_all and (clock == resumed or not edge"
         " or any(parent == pid for _child, (parent, _start) in owned.items()))):")),
    "second-past-grace-trap-command-unspared": ("owner_stated_seconds", "a second past-grace resume and its trap"
                                                                        " command's stated seconds were not kept",
        ("passes = 0\n", "passes = late = 0\n"),
        ("            last = now\n", "            last = now\n            late += clock >= deadline\n"),
        ("resumed = clock\n", "resumed, edge = clock, late == 2\n"),
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and not edge:")),
    "lone-last-pass-shell-needs-a-child": ("owner_stated_seconds", "a lone last-pass resume's stated seconds were"
                                                                   " not kept",
        ("resumed = clock\n", "resumed, edge = clock, clock + MAX_PASS_SECONDS >= kill_all + REAP_SECONDS\n"),
        ("(resumed is None or clock < kill_all):",
         "(resumed is None or clock < kill_all and (clock == resumed or not edge"
         " or any(parent == pid for _child, (parent, _start) in owned.items()))):")),
    "last-pass-trap-command-spared-only-if-listed-at-resume": ("owner_stated_seconds", "a last-pass resume and its"
                                                                                       " trap command's stated"
                                                                                       " seconds were not kept",
        ("resumed = clock\n",
         "resumed, edge = clock, set(owned) if clock + MAX_PASS_SECONDS >= kill_all + REAP_SECONDS else None\n"),
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and (edge is None or pid in edge):")),
}


def mutant_tree(scratch: Path, name: str) -> Path:
    """Copy scripts/ under scratch with one mutant applied to owned_process.py."""
    root = scratch / name
    shutil.copytree(ROOT / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = root / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in MUTANTS[name][2:]:
        assert text.count(old) == 1, f"mutant {name} no longer applies: {old!r}"
        text = text.replace(old, new)
    product.write_text(text)
    return root


def run_mutant(root: Path, control: str | None) -> tuple[int | None, float, str]:
    """Run one owner control, or the whole test, from a mutant tree; None is a run cut at its bound."""
    argv = [sys.executable, "-B", str(root / "scripts/test_suite_cancellation.py")]
    argv += ["--control", control] if control else []
    env = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
    began = time.monotonic()
    # A file, not a pipe: what a mutant leaks must not hold the run open.
    with tempfile.TemporaryFile() as output:
        try:
            status = subprocess.run(argv, cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=output,
                                    stderr=subprocess.STDOUT, timeout=150 if control else 400,
                                    start_new_session=True).returncode
        except subprocess.TimeoutExpired:
            status = None
        output.seek(0)
        return status, time.monotonic() - began, output.read().decode(errors="replace")


def mutation_campaign(controls: tuple[str, ...], names: list[str], matrix: bool, jobs: int) -> int:
    """Each mutant must fail its control with its words, and `none` must pass.

    The caller owns every process a mutant leaves behind. With `matrix`, every
    mutant also runs against every control and the whole test, for the table.
    """
    unknown = sorted(set(names) - set(MUTANTS))
    assert not unknown, f"no such mutant: {unknown}"
    names = ["none", *(name for name in names or MUTANTS if name != "none")]
    runs = []
    for name in names:
        control = MUTANTS[name][0]
        if matrix:
            runs += [(name, target) for target in (*controls, None)]
        elif name == "none":
            runs += [(name, target) for target in controls]
        elif control:
            runs.append((name, control))
    # A launcher that ignores SIGHUP hands that on to every run, and the whole test's HUP
    # stops need it at its default. A handler is reset at exec, so with one the runs get
    # the default, while this process still outlives a hangup as its launcher meant.
    hangup_ignored = signal.getsignal(signal.SIGHUP) == signal.SIG_IGN
    if hangup_ignored:
        signal.signal(signal.SIGHUP, lambda _signum, _frame: None)
    try:
        with tempfile.TemporaryDirectory(prefix="owned-process-mutants-") as scratch:
            trees = {name: mutant_tree(Path(scratch), name) for name in names}
            with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
                results = dict(zip(runs, pool.map(lambda run: run_mutant(trees[run[0]], run[1]), runs)))
    finally:
        if hangup_ignored:
            signal.signal(signal.SIGHUP, signal.SIG_IGN)
    for (name, target), (status, seconds, output) in results.items():
        lines = [line for line in output.splitlines() if line.strip()]
        verdict = "cut" if status is None else "red" if status else "green"
        print(f"{name} / {target or 'whole'}: {verdict} rc {status} {seconds:.1f} s: "
              f"{lines[-1][:300] if lines else ''}", flush=True)
    wrong = [f"none / {target or 'whole'}" for (name, target), (status, _s, _o) in results.items()
             if name == "none" and status != 0]
    for name in names[1:]:
        control, words = MUTANTS[name][:2]
        if control:
            status, _seconds, output = results[(name, control)]
            if not status or words not in output:
                wrong.append(f"{name} / {control}: expected to fail with {words!r}")
    print(f"owned-process mutants: {'FAIL' if wrong else 'PASS'} ({len(names) - 1} mutants, "
          f"{sum(bool(MUTANTS[name][0]) for name in names[1:])} with a control that must fail)", flush=True)
    for line in wrong:
        print("  " + line, flush=True)
    return 1 if wrong else 0
