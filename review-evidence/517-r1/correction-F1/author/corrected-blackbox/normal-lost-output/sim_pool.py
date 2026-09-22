#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run milan_dp's ordinary simulation legs at most two at a time (#517).

    python3 sim_pool.py [--jobs=1|2] [--exclusive] [--banner TEXT] EXE ...

The `run` recipe builds every model first and used to run ten of them one
after another. Each is a finished executable that takes no argument. The five sim_nxn
legs rewrite repository-relative shape headers as well as private images.
Mark each with --exclusive: only one member of this shared group runs at a
time, in recipe order. Independent legs may bypass a waiting group member.
At most JOBS legs are alive at once: 2 by default, 1 for sequential replay.
Each leg writes stdout and stderr into one capture file of its own, the way
scripts/run_all_suites.sh writes a suite into one log, and the captures are
replayed in the recipe's order: the banner the recipe echoed, the command
line make echoed, then the leg's bytes unchanged. A leg is replayed as soon
as it and every leg before it have finished, so the log reads as the
sequential recipe's did, leg by leg, whichever leg finished first.

The bound is this argument and nothing else. MAKEFLAGS and `make -j` are never
read, and any value but 1 or 2 is refused before a leg starts: two is the #517
decision for the four-core hosted worker, not a tuning knob.

MILAN_COUNTER_FRAME_OUT, when it is in the environment at all (empty
included), makes every sim_nxn leg that reaches [CTRS-OUT] rewrite the one
file it names, so the legs then run one at a time in recipe order and that
file ends with the last writer's bytes, as it always did.

A leg passes only by exiting 0. A non-zero exit, a signal, or an executable
that cannot be started fails the run (exit 1). After the first failure no leg
is started; the ones already running finish and are replayed, and make stops
at this recipe line, so render_mutants.py never runs.

Every leg is its own session and process group, reading /dev/null. Linux
subreaper adoption retains orphaned descendants, including new sessions.
SIGINT,
SIGTERM and SIGHUP - scripts/run_all_suites.sh's per-suite wall clock sends
SIGTERM - kill every running leg's whole group with SIGKILL, then kill and
reap adopted descendants as well as direct children. Every started leg is
then recorded with what it had written in obj_legs/replay.log; each
unfinished or unstarted leg is named. Available stdout receives that ordered
transcript, but cancellation never waits for a blocked consumer. This process
ends by the same signal. SIGKILL rather than SIGTERM because none of the ten legs handles a
signal, so both end a leg the same way, and SIGKILL needs no grace period, so
this runner reads no host clock (rule 8's wall-clock ratchet,
scripts/test_evidence.budget item 4). A leg that exits by itself has its
group killed too, before it is reaped, so nothing it spawned outlives it and
its group id cannot have been reused.

The captures stay in obj_legs/NN-<executable>.log, so a run killed before it
could replay still leaves each leg's output under the leg's own name. The
ordered transcript is also kept in obj_legs/replay.log. Nonblocking stdout
writes preserve a byte cursor; cancellation interrupts capacity waits, then
cleanup precedes a final attempt to write only immediately available bytes.
The output retry interval is not a simulation deadline or a test verdict. Every
line this runner adds starts with `sim_pool:` and matches no tally shape
scripts/suite_tally.py reads: it adds no check and no verdict of its own.
"""

import ctypes
import os
import shutil
import signal
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

USAGE = "usage: sim_pool.py [--jobs=1|2] [--exclusive] [--banner TEXT] EXE ..."

#: the #517 ceiling: at most two legs alive at once
MAX_JOBS = 2
#: the only values --jobs accepts, spelled exactly
JOB_VALUES = tuple(str(jobs) for jobs in range(1, MAX_JOBS + 1))
#: present at all, it names one file every dumping sim_nxn leg rewrites
FRAME_DUMP_VAR = "MILAN_COUNTER_FRAME_OUT"
#: where each leg's capture is kept, relative to the suite directory
LOG_DIR = Path("obj_legs")
#: the signals that end the pool early
INTERRUPTS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)


def adopt_descendants() -> None:
    """Linux subreaper: orphaned grandchildren stay ours to kill and reap.

    Process groups reach the normal generator subprocesses. Adoption also
    covers descendants that start another session, and avoids leaving zombies
    for the host's init process. Refuse before launch if this is unavailable.
    """
    if not sys.platform.startswith("linux"):
        raise OSError("sim_pool requires Linux child-subreaper support")
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code))


def reap_adopted(running: list["Leg"]) -> None:
    """Kill and reap orphans, including their subsequently adopted children.

    This single-threaded runner owns every PID here and nobody else waits
    for them, so none can be reused before our waitpid. Active ordinary legs
    stay in the pool; their attached descendants are still their responsibility.
    """
    active = {leg.proc.pid for leg in running}
    children = Path(f"/proc/self/task/{os.getpid()}/children")
    while True:
        adopted = set(map(int, children.read_text().split())) - active
        if not adopted:
            return
        for pid in adopted:
            os.kill(pid, signal.SIGKILL)
        for pid in adopted:
            os.waitpid(pid, 0)


class UsageError(Exception):
    """A command line this runner refuses before any leg starts."""


@dataclass
class Leg:
    """One ordinary leg: its place in the recipe, what it runs, how it ended."""

    position: int
    exe: str
    banner: str | None
    exclusive: bool = False
    proc: subprocess.Popen | None = None
    #: why the executable could not be started, when it could not
    error: str | None = None
    #: the interrupt this runner killed the leg for, when it did
    stopped_by: signal.Signals | None = None
    done: bool = False

    @property
    def log(self) -> Path:
        """This leg's capture: its recipe position, then its executable's name."""
        return LOG_DIR / f"{self.position:02d}-{Path(self.exe).name}.log"

    def passed(self) -> bool:
        """Did the leg run to an exit status of 0?"""
        return self.proc is not None and self.proc.returncode == 0


def parse_args(argv: list[str]) -> tuple[int, list[Leg]]:
    """(jobs, legs in recipe order), or UsageError before anything runs."""
    jobs = str(MAX_JOBS)
    legs: list[Leg] = []
    banner = None
    exclusive = False
    args = iter(argv)
    for arg in args:
        if arg.startswith("--jobs="):
            jobs = arg.removeprefix("--jobs=")
        elif arg == "--exclusive":
            exclusive = True
        elif arg == "--banner":
            banner = next(args, None)
            if banner is None:
                raise UsageError("--banner needs the line to print")
        elif arg.startswith("-"):
            raise UsageError(f"unknown option {arg!r}")
        else:
            legs.append(Leg(len(legs) + 1, arg, banner, exclusive))
            banner = None
            exclusive = False
    if jobs not in JOB_VALUES:
        raise UsageError(f"--jobs must be 1 or 2 (the #517 ceiling), not {jobs!r}")
    if banner is not None or exclusive:
        raise UsageError("the last --banner or --exclusive has no leg after it")
    if not legs:
        raise UsageError("no leg to run")
    if len({leg.exe for leg in legs}) != len(legs):
        raise UsageError("a leg is listed twice; each runs exactly once")
    return int(jobs), legs


def signal_name(signo: int) -> str:
    """SIGSEGV for 11, or the bare number for a signal Python cannot name."""
    try:
        return signal.Signals(signo).name
    except ValueError:
        return f"signal {signo}"


def write_line(out: BinaryIO, text: str) -> None:
    """One line of text, in the stream the legs are replayed to."""
    out.write(text.encode() + b"\n")


def ends_mid_line(path: Path) -> bool:
    """Is the last byte of a non-empty capture something other than a newline?"""
    with path.open("rb") as capture:
        if capture.seek(0, os.SEEK_END) == 0:
            return False
        capture.seek(-1, os.SEEK_END)
        return capture.read(1) != b"\n"


def outcome(leg: Leg) -> str | None:
    """What ended a leg that did not pass, as one line; None for a pass."""
    if leg.error is not None:
        return f"{leg.exe} could not be started: {leg.error}"
    code = leg.proc.returncode
    if leg.stopped_by is not None:
        return (f"{leg.exe} was killed by this runner on {leg.stopped_by.name}; "
                f"its output above is incomplete")
    if code < 0:
        return f"{leg.exe} was killed by {signal_name(-code)}"
    if code:
        return f"{leg.exe} exited with status {code}"
    return None


def kill_group(leg: Leg) -> None:
    """SIGKILL the leg's process group. Called only while the leg itself is
    unreaped, so the group id is still the leg's and cannot name a stranger."""
    try:
        os.killpg(leg.proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


class ReplayInterrupted(Exception):
    """An output-capacity wait received a watched cancellation signal."""

    def __init__(self, signo: int) -> None:
        self.signo = signal.Signals(signo)
        super().__init__(self.signo.name)


class Replay:
    """Deliver a disk transcript without blocking cancellation or losing position.

    Only this owner writes stdout. Restore its shared descriptor flags before
    any launch or exit. There is no buffered stdout write or exit-time flush.
    The disk transcript remains complete even when cancellation stops delivery.
    """

    def __init__(self, transcript: BinaryIO, fd: int,
                 watched: set[signal.Signals]) -> None:
        self.transcript = transcript
        self.fd = fd
        self.interrupts = watched & set(INTERRUPTS)
        self.position = 0

    def wait_interrupt(self, seconds: float) -> None:
        """Wait only for output retry or cancellation, never for a test verdict."""
        pending = signal.sigtimedwait(self.interrupts, seconds)
        if pending is not None:
            raise ReplayInterrupted(pending.si_signo)

    def drain(self, *, wait: bool = True) -> None:
        """Deliver in order; after cleanup, wait=False never awaits the reader."""
        self.transcript.flush()
        blocking = os.get_blocking(self.fd)
        os.set_blocking(self.fd, False)
        try:
            while True:
                if wait:
                    self.wait_interrupt(0)
                data = os.pread(self.transcript.fileno(), 65536, self.position)
                if not data:
                    return
                try:
                    written = os.write(self.fd, data)
                except BlockingIOError:
                    if not wait:
                        return
                    self.wait_interrupt(0.05)
                    continue
                except BrokenPipeError:
                    if not wait:
                        return
                    raise
                self.position += written
        finally:
            os.set_blocking(self.fd, blocking)


class Pool:
    """The legs, the bound, and the replay position, for one run."""

    def __init__(self, legs: list[Leg], jobs: int, out: BinaryIO) -> None:
        """Nothing starts here; `run` starts the legs."""
        self.legs = legs
        self.jobs = jobs
        self.out = out
        self.replayed = 0
        self.mid_line = False
        self.failed = False
        self.child_mask: set[signal.Signals] = set()

    def launch(self, leg: Leg) -> None:
        """Start one leg as the recipe line did: its path alone as argv, this
        directory, this environment; plus its own session, /dev/null for
        input, and its capture for stdout and stderr together."""
        mask = self.child_mask

        def restore_mask() -> None:
            """The leg gets the signal mask this runner was started with."""
            signal.pthread_sigmask(signal.SIG_SETMASK, mask)

        with leg.log.open("wb") as capture:
            try:
                leg.proc = subprocess.Popen(
                    [leg.exe], stdin=subprocess.DEVNULL, stdout=capture,
                    stderr=subprocess.STDOUT, start_new_session=True,
                    preexec_fn=restore_mask)
            except (OSError, subprocess.SubprocessError) as exc:
                leg.error = str(exc)
                leg.done = True
                self.failed = True

    def reap_exited(self, running: list[Leg]) -> None:
        """Retire every running leg that has exited: kill what it left in its
        group while it is still unreaped, then reap it."""
        for leg in list(running):
            state = os.waitid(os.P_PID, leg.proc.pid,
                              os.WEXITED | os.WNOHANG | os.WNOWAIT)
            if state is None:
                continue
            kill_group(leg)
            leg.proc.wait()
            leg.done = True
            running.remove(leg)
            self.failed = self.failed or leg.proc.returncode != 0
        reap_adopted(running)

    def stop(self, running: list[Leg], signo: signal.Signals | None) -> None:
        """Kill every running leg's group, then reap every leg. A leg this
        kill ended is marked as stopped; one that had already exited by
        itself keeps its own status."""
        self.reap_exited(running)
        for leg in running:
            kill_group(leg)
        for leg in running:
            leg.proc.wait()
            leg.done = True
            if leg.proc.returncode == -signal.SIGKILL:
                leg.stopped_by = signo
        running.clear()
        reap_adopted(running)

    def note(self, text: str) -> None:
        """One line of this runner's own, always on a line of its own. A leg's
        bytes are replayed as they are, so the recipe's next banner or command
        line still follows a leg's unterminated last line as make's did."""
        if self.mid_line:
            self.out.write(b"\n")
        write_line(self.out, f"sim_pool: {text}")
        self.mid_line = False

    def replay_ready(self) -> None:
        """Replay each finished leg whose predecessors have all been replayed."""
        while self.replayed < len(self.legs) and self.legs[self.replayed].done:
            leg = self.legs[self.replayed]
            if leg.banner is not None:
                write_line(self.out, leg.banner)
            write_line(self.out, leg.exe)
            with leg.log.open("rb") as capture:
                capture.read()
            self.mid_line = ends_mid_line(leg.log)
            ended = outcome(leg)
            if ended is not None:
                self.note(ended)
            self.out.flush()
            self.replayed += 1

    def run(self, watched: set[signal.Signals], replay: Replay) -> signal.Signals | None:
        """Run eligible legs, at most `jobs` alive, replaying in recipe order as
        they finish. Returns the interrupt that ended the run early, or None.
        The watched signals stay blocked from here on and are taken with
        sigwait, so no handler can run in the middle of a launch."""
        self.child_mask = signal.pthread_sigmask(signal.SIG_BLOCK, watched)
        pending = list(self.legs)
        running: list[Leg] = []
        interrupt = None
        try:
            while pending or running:
                while pending and len(running) < self.jobs and not self.failed:
                    group_busy = any(leg.exclusive for leg in running)
                    eligible = next((leg for leg in pending
                                     if not leg.exclusive or not group_busy), None)
                    if eligible is None:
                        break
                    pending.remove(eligible)
                    leg = eligible
                    self.launch(leg)
                    if leg.proc is not None:
                        running.append(leg)
                if not running:
                    break
                signo = signal.sigwait(watched)
                if signo != signal.SIGCHLD:
                    interrupt = signal.Signals(signo)
                    break
                self.reap_exited(running)
                self.replay_ready()
                replay.drain()
        except ReplayInterrupted as exc:
            interrupt = exc.signo
        finally:
            #! Normally empty. Non-empty on an interrupt, and on an exception
            #! out of this loop, which must not leave a leg running either.
            self.stop(running, interrupt)
        self.replay_ready()
        return interrupt

    def report_unstarted(self, interrupt: signal.Signals | None) -> None:
        """Name every leg that never started, and why none did."""
        why = (f"before {interrupt.name}" if interrupt is not None
               else "after a child failure")
        while self.replayed < len(self.legs):
            leg = self.legs[self.replayed]
            if leg.done:
                # Independent legs may have run past an unstarted group member.
                self.replay_ready()
            else:
                self.note(f"{leg.exe} was not started {why}")
                self.replayed += 1
        first = next((leg for leg in self.legs if leg.done and not leg.passed()),
                     None)
        if interrupt is None and first is not None:
            self.note(f"first leg in recipe order that did not pass: {first.exe}")
        self.out.flush()


def end_by(signo: int) -> int:
    """End this process by `signo`, as an uncaught signal would have."""
    signal.signal(signo, signal.SIG_DFL)
    os.kill(os.getpid(), signo)
    signal.pthread_sigmask(signal.SIG_UNBLOCK, {signo})
    return 128 + signo


def main(argv: list[str]) -> int:
    """Run the legs; 0 when every one exited 0, 1 when any did not, 2 on usage."""
    try:
        jobs, legs = parse_args(argv)
    except UsageError as exc:
        print(f"sim_pool: {exc}\n{USAGE}", file=sys.stderr)
        return 2
    frame_dump = FRAME_DUMP_VAR in os.environ
    #! An ignored interrupt stays ignored, as it was for the recipe's legs. A
    #! blocked signal is never discarded, so watching one would turn it back on.
    watched = {signal.SIGCHLD}
    watched.update(sig for sig in INTERRUPTS if signal.getsignal(sig) != signal.SIG_IGN)
    signal.signal(signal.SIGCHLD, signal.SIG_DFL)
    adopt_descendants()
    LOG_DIR.mkdir(exist_ok=True)
    for stale in LOG_DIR.glob("*.log"):
        stale.unlink()
    with (LOG_DIR / "replay.log").open("w+b") as transcript:
        replay = Replay(transcript, sys.stdout.fileno(), watched)
        pool = Pool(legs, 1 if frame_dump else jobs, transcript)
        if frame_dump:
            pool.note(f"{FRAME_DUMP_VAR} is set, so the legs run one at a time in "
                      f"recipe order")
        interrupt = pool.run(watched, replay)
        passed = all(leg.passed() for leg in legs)
        if interrupt is not None or not passed:
            pool.report_unstarted(interrupt)
        try:
            replay.drain(wait=interrupt is None)
        except ReplayInterrupted as exc:
            # All owned processes have already been reaped by Pool.run.
            interrupt = exc.signo
        if interrupt is not None:
            return end_by(interrupt)

    #! A signal that arrived after the last leg ended is still an interrupt.
    late = signal.sigpending() & set(INTERRUPTS)
    if late:
        return end_by(min(late))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
