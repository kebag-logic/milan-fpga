#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Own and reap verification commands, including detached build descendants.

Only the sweep and gPTP shadow campaign use this boundary. A fresh process
must enter it before starting children: adopted children then belong to that
command, never to another caller. A missing process facility is refused
before any command starts.

A command never outlives its owner. When the owner dies without cleanup
(KILL, or a fatal signal it does not handle such as HUP), a parent-death
signal kills the command it launched, so nothing that command would start
next can start. Descendants it already started may finish.
"""

import ctypes
import errno
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from types import FrameType
from typing import BinaryIO

PROC = Path("/proc")
GRACE_SECONDS = 2.0
REAP_SECONDS = 2.0
# prctl(2) options. None of them needs privilege.
PR_SET_PDEATHSIG = 1
PR_GET_PDEATHSIG = 2
PR_SET_CHILD_SUBREAPER = 36
PR_GET_CHILD_SUBREAPER = 37


class Cancelled(Exception):
    """The first handled signal is the terminal command result."""

    def __init__(self, signum: int):
        super().__init__(f"signal {signum}")
        self.signum = signum


class Unsupported(OSError):
    """A required process facility is absent on this host."""


def _prctl():
    """Resolve every facility before any state changes, or refuse by name."""
    try:
        prctl = getattr(ctypes.CDLL(None, use_errno=True), "prctl", None)
    except OSError:
        prctl = None
    missing = [name for name, present in (
        ("prctl", prctl is not None),
        ("os.pidfd_open", hasattr(os, "pidfd_open")),
        ("signal.pidfd_send_signal", hasattr(signal, "pidfd_send_signal"))) if not present]
    if missing:
        raise Unsupported("unsupported process facilities: " + ", ".join(missing))
    return prctl


def _identity(pid: int) -> tuple[int, str] | None:
    try:
        fields = (PROC / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()
        return int(fields[1]), fields[19]
    except (FileNotFoundError, ProcessLookupError):
        return None


def _live(pid: int) -> bool:
    try:
        return (PROC / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()[0] != "Z"
    except (FileNotFoundError, ProcessLookupError):
        return False


class OwnedProcesses:
    """One sequential command owner with bounded cleanup and signal latching."""

    def __init__(self) -> None:
        self.cancel_signal = 0
        self.process = None
        self.root_fd = None
        self.root_notified = False
        self.handlers = {}
        self.prctl = None
        self.owner_pid = os.getpid()
        self.previous_subreaper = ctypes.c_int()

    def __enter__(self) -> "OwnedProcesses":
        self.prctl = _prctl()
        self.owner_pid = os.getpid()
        # Probe the lifetime binding and identity handles before changing
        # adoption, so a refusal leaves this process as it found it.
        if self.prctl(PR_GET_PDEATHSIG, ctypes.byref(ctypes.c_int()), 0, 0, 0):
            raise OSError(ctypes.get_errno(), "cannot inspect command lifetime binding")
        fd = os.pidfd_open(os.getpid())
        os.close(fd)
        if self.prctl(PR_GET_CHILD_SUBREAPER, ctypes.byref(self.previous_subreaper), 0, 0, 0):
            raise OSError(ctypes.get_errno(), "cannot inspect descendant adoption")
        if self.prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0):
            raise OSError(ctypes.get_errno(), "cannot enable descendant adoption")
        for signum in (signal.SIGINT, signal.SIGTERM):
            self.handlers[signum] = signal.signal(signum, self._cancel)
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        try:
            # run() always cleans, including on error. Do not restart its
            # cleanup deadline while unwinding a failed cleanup attempt.
            # Context-only users (the fixture containment boundary) still
            # adopt and clean children launched inside their context.
            if self.process is None:
                self._cleanup()
            if exc_type is None:
                self.checkpoint()
        finally:
            for signum, handler in self.handlers.items():
                signal.signal(signum, handler)
            if self.prctl(PR_SET_CHILD_SUBREAPER, self.previous_subreaper.value, 0, 0, 0):
                raise OSError(ctypes.get_errno(), "cannot restore descendant adoption")

    def _die_with_owner(self) -> None:
        # Runs in the forked child before exec. A parent-death signal kills
        # the command when its owner dies; an orphan never starts at all.
        if self.prctl(PR_SET_PDEATHSIG, int(signal.SIGKILL), 0, 0, 0):
            raise OSError(ctypes.get_errno(), "cannot bind the command to its owner")
        if os.getppid() != self.owner_pid:
            raise OSError(errno.ESRCH, "the owner exited before the command started")

    def _cancel(self, signum: int, _frame: FrameType | None) -> None:
        if not self.cancel_signal:
            self.cancel_signal = signum
            # Notify the shell immediately, including between commands. Its
            # terminal trap must never interpret cancellation as a red suite.
            if self.root_fd is not None:
                self._signal(self.root_fd, signal.SIGSTOP)
                self._signal(self.root_fd, signum)
                self.root_notified = True

    def checkpoint(self) -> None:
        """Refuse every later command once cancellation is latched."""
        if self.cancel_signal:
            raise Cancelled(self.cancel_signal)

    @staticmethod
    def _signal(fd: int, signum: int) -> None:
        try:
            signal.pidfd_send_signal(fd, signum)
        except ProcessLookupError:
            pass

    def _descendants(self) -> dict[int, tuple[int, str]]:
        population = {}
        for entry in PROC.iterdir():
            if entry.name.isdecimal():
                pid = int(entry.name)
                identity = _identity(pid)
                if identity is not None:
                    population[pid] = identity
        owned = {os.getpid()}
        while True:
            more = {pid for pid, (parent, _start) in population.items()
                    if parent in owned} - owned
            if not more:
                return {pid: population[pid] for pid in owned if pid != os.getpid()}
            owned.update(more)

    def _reap(self) -> None:
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                return
            if not pid:
                return
            if self.process is not None and pid == self.process.pid:
                self.process.returncode = os.waitstatus_to_exitcode(status)

    def _cleanup(self) -> None:
        # Never signal a numeric PID from a stale census. Open an identity
        # handle and recheck its start time before sending any signal.
        deadline = time.monotonic() + GRACE_SECONDS
        hard_deadline = deadline + REAP_SECONDS
        notified = set()
        initial = None
        resumed = None
        while True:
            self._reap()
            owned = self._descendants()
            if not owned:
                return
            if initial is None:
                initial = set(owned.items())
            now = time.monotonic()
            if now >= hard_deadline:
                raise RuntimeError(f"CLEANUP FAILED: owned descendants remain: {owned}")
            root_pid = self.process.pid if self.process is not None else None
            live = {pid for pid in owned if _live(pid)}
            if self.root_notified and resumed is None and not (live - {root_pid}):
                # The stopped shell cannot advance the sweep while descendants
                # shut down. Resume it only when its pending terminal trap can
                # finish; it may need to reap zombies before its EXIT cleanup.
                self._signal(self.root_fd, signal.SIGCONT)
                resumed = now
            signum = signal.SIGKILL if now >= deadline else signal.SIGTERM
            for pid, identity in owned.items():
                if pid == root_pid and self.root_notified and now < hard_deadline - 0.2:
                    continue
                if signum != signal.SIGKILL:
                    # Let terminal traps run their cleanup commands during
                    # grace. New descendants still face the hard deadline.
                    if (pid, identity) not in initial:
                        continue
                elif now < hard_deadline - 0.2:
                    # Kill stubborn leaves first, so cooperative intermediate
                    # owners can reap and remove private work before exiting.
                    if now < deadline + 1.0 and any(parent == pid for _child, (parent, _start) in initial):
                        continue
                    if any(parent == pid and child in live for child, (parent, _start) in owned.items()):
                        continue
                    if (pid, identity) not in initial and resumed is not None and now < resumed + 1.0:
                        continue
                key = (pid, identity, signum)
                if key in notified:
                    continue
                try:
                    fd = os.pidfd_open(pid)
                except ProcessLookupError:
                    continue
                try:
                    if _identity(pid) == identity:
                        self._signal(fd, signum)
                        self._signal(fd, signal.SIGCONT)
                        notified.add(key)
                finally:
                    os.close(fd)
            time.sleep(0.02)

    def run(self, argv: list[str], cwd: Path | None = None, capture: bool = True,
            env: dict[str, str] | None = None, stderr: BinaryIO | None = None) -> tuple[int, str]:
        """Run one command; return its status/output only after owned cleanup.

        Captured standard error joins the output unless `stderr` receives it.
        """
        self.checkpoint()
        self.root_notified = False
        if stderr is None:
            stderr = subprocess.STDOUT if capture else None
        with tempfile.TemporaryFile() as output:
            try:
                try:
                    self.process = subprocess.Popen(
                        argv, cwd=cwd, env=env, start_new_session=True,
                        preexec_fn=self._die_with_owner,
                        stdout=output if capture else None, stderr=stderr)
                except subprocess.SubprocessError as exc:
                    raise Unsupported(f"cannot bind the command to its owner: {exc}") from exc
                self.root_fd = os.pidfd_open(self.process.pid)
                if self.cancel_signal:
                    self._signal(self.root_fd, signal.SIGSTOP)
                    self._signal(self.root_fd, self.cancel_signal)
                    self.root_notified = True
                while self.process.poll() is None:
                    self.checkpoint()
                    time.sleep(0.02)
            finally:
                try:
                    self._cleanup()
                finally:
                    if self.root_fd is not None:
                        os.close(self.root_fd)
                        self.root_fd = None
            self.checkpoint()
            output.seek(0)
            return self.process.returncode, output.read().decode("utf-8", errors="replace")


def main() -> int:
    """Supervise the sweep shell from selection through its final verdict."""
    if len(sys.argv) < 3 or sys.argv[1] != "--":
        print("usage: owned_process.py -- COMMAND [ARG ...]", file=sys.stderr)
        return 2
    try:
        with OwnedProcesses() as owner:
            status, _output = owner.run(sys.argv[2:], capture=False)
        return status if status >= 0 else 128 - status
    except Cancelled as exc:
        # The sweep shell has already said whether logs were prepared.
        print(f"CANCELLED: signal {exc.signum}; no completed sweep result", file=sys.stderr)
        return 128 + exc.signum
    except (OSError, RuntimeError) as exc:
        print(f"REFUSED: process ownership: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
