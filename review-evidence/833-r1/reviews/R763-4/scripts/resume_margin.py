#!/usr/bin/env python3
"""Measure when owner_shell_window's shell is resumed, against the leaf-first spare's end.

usage: resume_margin.py SCRIPTS_DIR
The control stages GRACE_SECONDS=0.2, so the stubborn-leaf parent spare at
owned_process.py:325 ends at owner clock deadline + 1.0 = 1.2 s. Prints the wall
time from cleanup entry to the shell's SIGCONT (the resume) and the margin past 1.2 s.
"""
import signal, sys, tempfile, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import owned_process as op  # noqa: E402
import test_suite_cancellation as t  # noqa: E402

marks = {}
cleanup, sig = op.OwnedProcesses._cleanup, op.OwnedProcesses._signal


def timed_cleanup(self):
    marks.setdefault("cleanup", time.monotonic())
    return cleanup(self)


def timed_signal(self, fd, signum):
    if signum == signal.SIGCONT and fd == self.root_fd and "cleanup" in marks:
        marks.setdefault("resume", time.monotonic())
    return sig(fd, signum)


op.OwnedProcesses._cleanup, op.OwnedProcesses._signal = timed_cleanup, timed_signal
t.OwnedProcesses._cleanup, t.OwnedProcesses._signal = timed_cleanup, timed_signal
with tempfile.TemporaryDirectory(prefix="r763-4-margin-") as scratch:
    t.owner_shell_window(Path(scratch))
resume = marks["resume"] - marks["cleanup"]
print(f"resume {resume:.3f} s into cleanup (wall); leaf-first spare ends at 1.200 s owner clock; margin {resume - 1.2:.3f} s")
