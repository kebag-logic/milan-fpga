#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Failure-sensitive arms for sim_pool.py, the #517 leg runner, on real processes.

Every arm starts the real runner as a process, in a fresh directory, against
fake legs: small executables that write known bytes, record what they saw in
a ledger, and can be held on a FIFO until the arm releases them. The arms
decide from those records and from the runner's own output and exit status;
nothing here reads the host's clock (rule 8's wall-clock ratchet), so an arm
that needs two legs alive at once holds one leg until the other has run.

What the arms hold, and why each one is here:

* both worker counts run every leg exactly once, with argv, directory,
  environment, input, session and signal state the recipe line gave it, and
  replay the same transcript;
* every byte a leg writes, on stdout or stderr and past any pipe size, is
  replayed in recipe order behind the recipe's banner and command line, and a
  leg that finishes first still prints second;
* at most two legs are ever alive, whatever MAKEFLAGS says, and two really
  are; one worker means one;
* a worker count other than 1 or 2 is refused before anything starts;
* a leg that exits non-zero, dies by a signal or cannot be started fails the
  run, stops any further start, and is named; the legs already running
  finish; a leg that exits 0 while printing [FAIL] still reaches
  scripts/suite_tally.py's verdict unmasked;
* SIGTERM, SIGINT and SIGHUP kill every running leg and everything it spawned,
  reap them, replay the partial output with the leg and the signal named, name
  the legs never started, and end the runner by the same signal; a leg that
  exits by itself leaves nothing it spawned behind; an interrupt the runner
  inherited as ignored stays ignored;
* MILAN_COUNTER_FRAME_OUT, set or empty, selects one leg at a time in recipe
  order, the dump file ends with the last writer's bytes, and an empty name
  fails at the first writer as the sequential recipe did;
* the runner's own lines add no check and no failure to the suite's tally;
* the Makefile hands the runner the ten legs of the recipe, in the recipe's
  order and with its banners, at two workers unless SIM_JOBS says one.

A runner that never has two legs alive leaves the two arms that need two
waiting rather than passing: ending that wait is the person's or the per-suite
wall clock's, as render_mutants.py documents for a livelocking mutant.
Over-concurrency is checked by every leg as it starts and by the arm while it
holds legs; a runner that launched an extra leg would have to stall for longer
than a leg takes to start, at every such check, to go unseen. Linux only: the
arms read /proc and wait on pidfds.

Usage: python3 tb/verilator/milan_dp/test_sim_pool.py
Exit 0 = every arm held.
"""

import contextlib
import ctypes
import json
import os
import select
import shlex
import signal
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterator
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "sim_pool.py"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import FAIL_MARKER, log_reports_failure, scan  # noqa: E402

#: the ten ordinary legs and their banners exactly as the recipe ran them at
#: dev 483a133e, before #517: the frozen inventory the Makefile must hand over
LEGACY_LEGS = (
    (None, "./obj_dir/Vmilan_dp_sim"),
    ("---- Milan 5.4.5 notifications, TIMED on the compressed processor timebase ----",
     "./obj_notify/Vmilan_dp_notify"),
    (None, "./obj_nxn/Vmilan_dp_nxn"),
    ("---- the DIVERGENT shape: input row 1 declares the 96 kHz base ----",
     "./obj_nxndv/Vmilan_dp_nxndv"),
    (None, "./obj_nxn8/Vmilan_dp_nxn8"),
    ("---- the shipping Arty shape: 4 streams x 4 wire channels ----",
     "./obj_nxn4c/Vmilan_dp_nxn4c"),
    ("---- LPF_P=0 (pruned render tap, the ax7101 shipping shape) ----",
     "./obj_nolpf/Vmilan_dp_nolpf"),
    ("---- all six tier-1 blocks pruned ----", "./obj_prune/Vmilan_dp_prune"),
    ("---- THE SHIPPING ALINX SHAPE: 1 stream x 8 wire channels, TDM8 master ----",
     "./obj_ax1x1/Vmilan_dp_ax1x1"),
    ("---- the same shape at the TRUE clk_audio ratio (391/1591) ----",
     "./obj_aclk/Vmilan_dp_aclk"),
)

#: the fake leg every arm runs; a leg's executable imports it with its config
FAKE_LEG = r'''
import fcntl, json, os, resource, signal, subprocess, sys

FRAME_VAR = "MILAN_COUNTER_FRAME_OUT"


def record(path, **fields):
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, (json.dumps(fields) + "\n").encode())
    finally:
        os.close(fd)


def live_children(ppid):
    """Children of `ppid` that are not zombies, read from /proc."""
    alive = 0
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            with open("/proc/" + entry + "/stat", "rb") as fh:
                raw = fh.read()
        except OSError:
            continue
        fields = raw[raw.rfind(b")") + 2:].split()
        if int(fields[1]) == ppid and fields[0] != b"Z":
            alive += 1
    return alive


def status(name):
    with open("/proc/self/status") as fh:
        for line in fh:
            if line.startswith(name + ":"):
                return line.split()[1]
    return None


def hold(path):
    """Block until the arm writes a byte or lets go of the FIFO."""
    fd = os.open(path, os.O_RDONLY)
    try:
        os.read(fd, 1)
    finally:
        os.close(fd)


def write_chunks(chunks):
    for stream, text in chunks:
        os.write(1 if stream == "out" else 2, text.encode("latin-1"))


def main(cfg):
    name = cfg["name"]
    ppid = os.getppid()
    siblings = live_children(ppid)
    descendant = None
    if cfg.get("descendant_hold"):
        ready_read, ready_write = os.pipe()
        code = ("import os, sys, json\n"
                "os.write(int(sys.argv[3]), b'r')\n"
                "os.close(int(sys.argv[3]))\n"
                "fd = os.open(sys.argv[1], os.O_RDONLY)\n"
                "os.read(fd, 1)\n"
                "out = os.open(sys.argv[2], os.O_WRONLY | os.O_APPEND)\n"
                "os.write(out, (json.dumps({'event': 'survived', 'pid': os.getpid()})"
                " + chr(10)).encode())\n")
        descendant = subprocess.Popen([sys.executable, "-S", "-c", code,
                                       cfg["descendant_hold"], cfg["ledger"], str(ready_write)],
                                      pass_fds=(ready_write,),
                                      start_new_session=cfg.get("descendant_session", False)).pid
        os.close(ready_write)
        assert os.read(ready_read, 1) == b'r'
        os.close(ready_read)
    environ = dict(os.environ)
    record(cfg["ledger"], event="start", leg=name, pid=os.getpid(), ppid=ppid,
           argv=sys.argv, cwd=os.getcwd(), stdin=os.readlink("/proc/self/fd/0"),
           sid=os.getsid(0), pgid=os.getpgid(0), siblings=siblings,
           sigblk=status("SigBlk"), sigign=status("SigIgn"), environ=environ,
           descendant=descendant)
    shared = None
    if cfg.get("shared"):
        shared = os.open(cfg["shared"], os.O_WRONLY | os.O_CREAT, 0o644)
        try:
            fcntl.flock(shared, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            record(cfg["ledger"], event="contention", leg=name)
            cfg["exit"] = 4
    write_chunks(cfg.get("out", []))
    fd = os.open(cfg["announce"], os.O_WRONLY)
    os.write(fd, (json.dumps({"leg": name, "pid": os.getpid(), "holds": bool(cfg.get("hold")),
                              "descendant": descendant}) + "\n").encode())
    os.close(fd)
    if cfg.get("hold"):
        hold(cfg["hold"])
        record(cfg["ledger"], event="survived" if cfg.get("killed") else "released",
               leg=name, pid=os.getpid())
    if cfg.get("dump") and FRAME_VAR in os.environ:
        try:
            with open(os.environ[FRAME_VAR], "wb") as dump:
                dump.write(name.encode())
        except OSError:
            write_chunks([["out", "  [FAIL] optional reference frame dump\n"]])
            record(cfg["ledger"], event="end", leg=name)
            sys.exit(1)
    write_chunks(cfg.get("after", []))
    record(cfg["ledger"], event="end", leg=name)
    if cfg.get("crash"):
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        os.kill(os.getpid(), getattr(signal, cfg["crash"]))
    sys.exit(cfg.get("exit", 0))
'''


class Scenario:
    """One directory, its fake legs, the FIFOs that hold them, and a runner."""

    def __init__(self, root: Path) -> None:
        """Lay out the ledger, the announcement FIFO and the fake leg module."""
        self.dir = root
        self.ledger = root / "ledger.jsonl"
        self.ledger.touch()
        self.announce = root / "announce.fifo"
        os.mkfifo(self.announce)
        #! Held read-write, so a leg never blocks opening it and a read here
        #! never sees end-of-file between two legs.
        self.announce_fd = os.open(self.announce, os.O_RDWR)
        self.announcements = os.fdopen(os.dup(self.announce_fd), "rb", buffering=0)
        (root / "fake_leg.py").write_text(FAKE_LEG)
        self.holds: dict[str, int] = {}
        self.pidfds: dict[int, int] = {}
        self.runner: subprocess.Popen | None = None
        self.stdout_path = root / "runner.out"
        self.stderr_path = root / "runner.err"

    def hold_fifo(self, name: str) -> str:
        """A FIFO a leg or descendant blocks on until `release(name)`."""
        path = self.dir / f"hold-{name}.fifo"
        os.mkfifo(path)
        self.holds[name] = os.open(path, os.O_RDWR)
        return str(path)

    def leg(self, name: str, **cfg: object) -> str:
        """Write one fake leg executable, ./obj_<name>/V<name>, and return that path."""
        cfg.update(name=name, ledger=str(self.ledger), announce=str(self.announce))
        exe_dir = self.dir / f"obj_{name}"
        exe_dir.mkdir()
        exe = exe_dir / f"V{name}"
        exe.write_text(f"#!{sys.executable} -S\nimport sys\n"
                       f"sys.path.insert(0, {str(self.dir)!r})\n"
                       f"import fake_leg\nfake_leg.main({cfg!r})\n")
        exe.chmod(0o755)
        return f"./obj_{name}/V{name}"

    def start(self, args: list[str], env: dict[str, str],
              ignore: tuple[signal.Signals, ...] = ()) -> None:
        """Start the runner here, stdout and stderr to files so it never blocks,
        with every interrupt at its default unless `ignore` names it, and
        nothing blocked: the state make hands a recipe line."""

        def signal_state() -> None:
            """Runs in the runner's process before it execs."""
            for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
                signal.signal(sig, signal.SIG_IGN if sig in ignore else signal.SIG_DFL)
            signal.pthread_sigmask(signal.SIG_SETMASK, set())

        with self.stdout_path.open("wb") as out, self.stderr_path.open("wb") as err:
            self.runner = subprocess.Popen(
                [sys.executable, str(RUNNER), *args], cwd=self.dir, env=env,
                stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                preexec_fn=signal_state)

    def next_start(self) -> dict:
        """Block until the next leg announces itself. A pidfd is kept on the
        leg when it holds, and on its descendant, which always holds: both are
        then certainly alive, so the pid cannot have been reused."""
        news = json.loads(self.announcements.readline())
        alive = [news["descendant"]] if news["descendant"] is not None else []
        if news["holds"]:
            alive.append(news["pid"])
        for pid in alive:
            self.pidfds[pid] = os.pidfd_open(pid)
        return news

    def release(self, name: str) -> None:
        """Let one held leg or descendant carry on."""
        os.write(self.holds[name], b"g")

    def runner_children(self) -> int:
        """The runner's children that are alive now, read from /proc."""
        alive = 0
        for entry in os.listdir("/proc"):
            if not entry.isdigit():
                continue
            with contextlib.suppress(OSError):
                raw = Path(f"/proc/{entry}/stat").read_bytes()
                fields = raw[raw.rfind(b")") + 2:].split()
                if int(fields[1]) == self.runner.pid and fields[0] != b"Z":
                    alive += 1
        return alive

    def wait_exit(self, pid: int) -> None:
        """Block until process `pid` (announced earlier) has ended."""
        poller = select.poll()
        poller.register(self.pidfds[pid], select.POLLIN)
        poller.poll()

    def finish(self) -> int:
        """Wait for the runner, let every hold go, wait out every announced
        process, and return the runner's status."""
        status = self.runner.wait()
        # A pidfd gets POLLHUP only after the process is reaped. POLLIN
        # alone accepts zombies, and releasing a leaked child before checking
        # would let it exit by itself and hide the cleanup defect.
        for pid, pidfd in self.pidfds.items():
            poller = select.poll()
            poller.register(pidfd, select.POLLIN | select.POLLHUP)
            events = poller.poll(0)
            assert events and events[0][1] & select.POLLHUP, f"owned PID {pid} survived or was not reaped"
        for fd in self.holds.values():
            os.close(fd)
        self.holds.clear()
        for pid in list(self.pidfds):
            self.wait_exit(pid)
        return status

    def events(self, kind: str | None = None) -> list[dict]:
        """The ledger, optionally only one kind of event."""
        rows = [json.loads(line) for line in self.ledger.read_text().splitlines()]
        return [row for row in rows if kind is None or row["event"] == kind]

    def stdout(self) -> bytes:
        """What the runner printed on stdout."""
        return self.stdout_path.read_bytes()

    def stderr(self) -> str:
        """What the runner printed on stderr."""
        return self.stderr_path.read_text()

    def close(self) -> None:
        """Leave nothing running, whatever an arm did or failed to do."""
        if self.runner is not None and self.runner.poll() is None:
            self.runner.kill()
            self.runner.wait()
        for pidfd in self.pidfds.values():
            with contextlib.suppress(OSError):
                signal.pidfd_send_signal(pidfd, signal.SIGKILL)
        # The test process is also a subreaper, solely for failed fixtures.
        # Assertions run before this cleanup, so this cannot give a broken
        # runner credit for killing or reaping its own descendants.
        while True:
            children = Path(f"/proc/self/task/{os.getpid()}/children").read_text().split()
            if not children:
                break
            for child in children:
                os.kill(int(child), signal.SIGKILL)
            for child in children:
                os.waitpid(int(child), 0)
        for fd in list(self.holds.values()) + list(self.pidfds.values()):
            with contextlib.suppress(OSError):
                os.close(fd)
        self.announcements.close()
        os.close(self.announce_fd)


@contextlib.contextmanager
def scenario() -> Iterator[Scenario]:
    """A Scenario in a fresh directory, torn down however the arm ends."""
    assert ctypes.CDLL(None).prctl(36, 1, 0, 0, 0) == 0, "cannot adopt failed fixture descendants"
    with tempfile.TemporaryDirectory(prefix="sim-pool-test-") as root:
        case = Scenario(Path(root))
        try:
            yield case
        finally:
            case.close()


def transcript(*parts: tuple[str | None, str, str]) -> bytes:
    """What the recipe printed for each (banner, command, leg bytes) in order."""
    text = ""
    for banner, command, body in parts:
        if banner is not None:
            text += banner + "\n"
        text += command + "\n" + body
    return text.encode("latin-1")


def big_body(tag: str) -> list[list[str]]:
    """Output past any pipe size, stdout and stderr interleaved, and a final
    line with no newline: what a leg's capture must keep byte for byte."""
    chunks = []
    for block in range(24):
        line = f"{tag} block {block:02d} " + "x" * 400 + "\n"
        chunks.append(["out", line * 32])
        chunks.append(["err", f"{tag} stderr after block {block:02d}\n"])
    chunks.append(["out", f"{tag}: checks: 7   failures: 0\n\x00\xff\x80{tag} tail without newline"])
    return chunks


def body_text(chunks: list[list[str]]) -> str:
    """The bytes a list of chunks puts in one shared capture, in write order."""
    return "".join(text for _stream, text in chunks)


def run_to_end(case: Scenario, args: list[str], env: dict[str, str]) -> int:
    """Start the runner on legs that never hold, and wait for everything."""
    case.start(args, env)
    return case.finish()


def clean_env(**extra: str) -> dict[str, str]:
    """This process's environment without any frame-dump or make state, plus `extra`."""
    env = {key: value for key, value in os.environ.items()
           if key not in ("MILAN_COUNTER_FRAME_OUT", "MAKEFLAGS", "MFLAGS", "MAKELEVEL")}
    env.update(extra)
    return env


def sigmask_bits(*signals: signal.Signals) -> int:
    """The /proc status mask with the bits of `signals` set."""
    return sum(1 << (int(sig) - 1) for sig in signals)


def arm_both_worker_counts_run_each_leg_once_as_the_recipe_did() -> None:
    """argv, directory, environment, input, session and signal mask are the
    recipe's, each leg runs once, and one worker and two replay the same."""
    seen = {}
    for jobs in ("1", "2"):
        with scenario() as case:
            env = clean_env(SIM_POOL_ARM="identity")
            legs = [case.leg(f"L{k}", out=[["out", f"L{k} ran\n"], ["err", f"L{k} err\n"]])
                    for k in range(1, 5)]
            args = [f"--jobs={jobs}", legs[0], "--banner", "---- b2 ----", legs[1],
                    legs[2], "--banner", "---- b4 ----", legs[3]]
            assert run_to_end(case, args, env) == 0, case.stderr()
            starts = case.events("start")
            assert sorted(row["leg"] for row in starts) == ["L1", "L2", "L3", "L4"], starts
            for row, exe in zip(sorted(starts, key=lambda r: r["leg"]), legs):
                assert row["argv"] == [exe], row["argv"]
                assert Path(row["cwd"]) == case.dir.resolve(), row["cwd"]
                assert row["environ"] == env, "the leg's environment is not the runner's"
                assert row["stdin"] == "/dev/null", row["stdin"]
                assert row["sid"] == row["pid"] == row["pgid"], "not its own session"
                assert int(row["sigblk"], 16) == 0, f"leg inherited blocked {row['sigblk']}"
                interrupts = sigmask_bits(signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
                assert int(row["sigign"], 16) & interrupts == 0, row["sigign"]
            want = transcript((None, legs[0], "L1 ran\nL1 err\n"),
                              ("---- b2 ----", legs[1], "L2 ran\nL2 err\n"),
                              (None, legs[2], "L3 ran\nL3 err\n"),
                              ("---- b4 ----", legs[3], "L4 ran\nL4 err\n"))
            assert case.stdout() == want, case.stdout()
            assert case.stderr() == "", case.stderr()
            logs = sorted(p.name for p in (case.dir / "obj_legs").iterdir())
            assert logs == ["01-VL1.log", "02-VL2.log", "03-VL3.log", "04-VL4.log"], logs
            seen[jobs] = (case.stdout(), [(r["leg"], r["argv"]) for r in
                                          sorted(starts, key=lambda r: r["leg"])])
    assert seen["1"] == seen["2"], "one worker and two did not replay the same"


def arm_every_byte_is_replayed_in_recipe_order() -> None:
    """Past any pipe size, stdout and stderr interleaved, an unterminated last
    line: each capture is replayed whole, in recipe order, and kept on disk."""
    with scenario() as case:
        bodies = {name: big_body(name) for name in ("L1", "L2", "L3")}
        legs = {name: case.leg(name, out=chunks) for name, chunks in bodies.items()}
        banner = "---- after an unterminated line ----"
        args = ["--jobs=2", legs["L1"], "--banner", banner, legs["L2"], legs["L3"]]
        assert run_to_end(case, args, clean_env()) == 0, case.stderr()
        want = transcript((None, legs["L1"], body_text(bodies["L1"])),
                          (banner, legs["L2"], body_text(bodies["L2"])),
                          (None, legs["L3"], body_text(bodies["L3"])))
        assert len(want) > 3 * 65536, "the fixture no longer exceeds a pipe"
        assert case.stdout() == want, "a capture was not replayed byte for byte"
        for position, name in enumerate(("L1", "L2", "L3"), start=1):
            kept = (case.dir / "obj_legs" / f"{position:02d}-V{name}.log").read_bytes()
            assert kept == body_text(bodies[name]).encode("latin-1"), name


def arm_a_leg_that_finishes_first_still_prints_second() -> None:
    """Two legs alive at once and the second finished first: the replay keeps
    the recipe's order, and the ledger shows the completion order did not."""
    with scenario() as case:
        first = case.leg("L1", out=[["out", "L1 before\n"]], after=[["out", "L1 after\n"]],
                         hold=case.hold_fifo("L1"))
        second = case.leg("L2", out=[["out", "L2 whole\n"]], hold=case.hold_fifo("L2"))
        case.start(["--jobs=2", first, second], clean_env())
        pids = {news["leg"]: news["pid"] for news in (case.next_start(), case.next_start())}
        case.release("L2")
        case.wait_exit(pids["L2"])
        case.release("L1")
        assert case.finish() == 0, case.stderr()
        assert [row["leg"] for row in case.events("end")] == ["L2", "L1"]
        started = {row["leg"]: row for row in case.events("start")}
        assert started["L2"]["siblings"] == 2, "L2 did not start beside a live L1"
        assert case.stdout() == transcript((None, first, "L1 before\nL1 after\n"),
                                           (None, second, "L2 whole\n")), case.stdout()


def hold_protocol(case: Scenario, total: int, ceiling: int) -> list[int]:
    """Release held legs oldest first, one at a time. Before each release every
    leg that may be alive has announced itself; the runner's live children are
    counted then, and returned, one count per release."""
    held: list[dict] = []
    counts = []
    for released in range(total):
        while len(held) < min(ceiling, total - released):
            held.append(case.next_start())
        counts.append(case.runner_children())
        oldest = held.pop(0)
        case.release(oldest["leg"])
        case.wait_exit(oldest["pid"])
    return counts


def arm_never_more_than_two_legs_alive() -> None:
    """Whatever MAKEFLAGS says, two legs at most and two in fact, and one
    worker means one: counted by each leg as it starts and while legs are held."""
    for extra, makeflags, ceiling in (([], "-j8 --jobserver-auth=fifo:/nonexistent", 2),
                                      (["--jobs=2"], "-j16", 2),
                                      (["--jobs=1"], "-j8", 1)):
        with scenario() as case:
            legs = [case.leg(f"L{k}", hold=case.hold_fifo(f"L{k}")) for k in range(1, 7)]
            env = clean_env(MAKEFLAGS=makeflags, MFLAGS=makeflags.split()[0], MAKELEVEL="1")
            case.start([*extra, *legs], env)
            counts = hold_protocol(case, len(legs), ceiling)
            assert case.finish() == 0, case.stderr()
            starts = case.events("start")
            assert sorted(row["leg"] for row in starts) == [f"L{k}" for k in range(1, 7)]
            if ceiling == 1:
                assert [row["leg"] for row in starts] == [f"L{k}" for k in range(1, 7)]
            beside = max(row["siblings"] for row in starts)
            assert beside <= ceiling, f"{extra} {makeflags}: {beside} legs alive at a start"
            want = [ceiling] * (len(legs) - ceiling + 1) + list(range(ceiling - 1, 0, -1))
            assert counts == want, f"{extra} {makeflags}: alive while held {counts}"


def arm_shared_group_is_exclusive_ordered_and_allows_independent_overlap() -> None:
    """Five writers hold one shared file; independent work fills the second
    slot even past blocked writers. Every command runs once, in group order."""
    with scenario() as case:
        shared = str(case.dir / "shared-header")
        groups = [case.leg(f"G{k}", shared=shared, hold=case.hold_fifo(f"G{k}"),
                           out=[["out", f"G{k} output\n"]]) for k in range(1, 6)]
        independent = [case.leg(f"I{k}", hold=case.hold_fifo(f"I{k}"),
                                out=[["out", f"I{k} output\n"]]) for k in range(1, 6)]
        args = [independent[0]]
        for leg in groups:
            args += ["--exclusive", leg]
        args += independent[1:]
        case.start(args, clean_env(MAKEFLAGS="-j8"))
        first = [case.next_start(), case.next_start()]
        assert {r["leg"] for r in first} == {"I1", "G1"}, first
        for k in range(1, 6):
            assert case.runner_children() == 2, "total child bound or independent overlap lost"
            case.release(f"I{k}")
            if k < 5:
                news = case.next_start()
                assert not case.events("contention"), "shared-state contention between grouped writers"
                assert news["leg"] == f"I{k+1}", news
        case.wait_exit(next(r["pid"] for r in first if r["leg"] == "I1"))
        for k in range(1, 6):
            case.release(f"G{k}")
            if k < 5:
                news = case.next_start()
                assert news["leg"] == f"G{k+1}", "exclusive group relative order changed"
        assert case.finish() == 0, case.stderr()
        assert not case.events("contention"), "shared-state contention between grouped writers"
        starts = case.events("start")
        assert sorted(r["leg"] for r in starts) == sorted([f"{c}{k}" for c in "GI" for k in range(1, 6)])
        assert max(r["siblings"] for r in starts) == 2, "total two-child ceiling changed"
        assert [r["leg"] for r in starts if r["leg"].startswith("G")] == [f"G{k}" for k in range(1, 6)]
        ordered = [independent[0], *groups, *independent[1:]]
        assert case.stdout() == transcript(*[(None, exe, Path(exe).name[1:] + " output\n")
                                             for exe in ordered]), "ordered output lost"


def arm_skipped_group_members_do_not_hide_later_logs() -> None:
    """A failure or interrupt with an unstarted grouped leg must still publish
    the complete or partial log of independent work that bypassed it."""
    for interrupt in (False, True):
        with scenario() as case:
            g1 = case.leg("G1", hold=case.hold_fifo("G1"), out=[["out", "group output\n"]])
            g2 = case.leg("G2")
            later = case.leg("I1", hold=case.hold_fifo("I1"), exit=3,
                             out=[["err", "independent output\n"]])
            case.start(["--exclusive", g1, "--exclusive", g2, later], clean_env())
            started = {r["leg"]: r for r in (case.next_start(), case.next_start())}
            assert set(started) == {"G1", "I1"}, started
            if interrupt:
                case.runner.send_signal(signal.SIGTERM)
            else:
                case.release("I1")
                case.wait_exit(started["I1"]["pid"])
                case.release("G1")
            assert case.finish() == (-signal.SIGTERM if interrupt else 1), case.stderr()
            text = case.stdout()
            assert text.count(b"independent output\n") == 1, text
            assert text.index(b"group output") < text.index(g2.encode()) < text.index(later.encode()), text
            assert (g2 + " was not started").encode() in text, text
            assert (later + " was not started").encode() not in text, text
            assert (case.dir / "obj_legs/03-VI1.log").read_bytes() == b"independent output\n"


def arm_worker_counts_other_than_one_or_two_are_refused() -> None:
    """Refused with status 2 and the reason, before a leg starts or a log exists."""
    for value in ("0", "3", "8", "-1", "", "two", "02", " 2", "2.0", "+2", "1 "):
        with scenario() as case:
            leg = case.leg("L1")
            assert run_to_end(case, [f"--jobs={value}", leg], clean_env()) == 2, value
            reason = f"--jobs must be 1 or 2 (the #517 ceiling), not {value!r}"
            assert reason in case.stderr(), case.stderr()
            assert case.stdout() == b"" and case.events() == [], value
            assert not (case.dir / "obj_legs").exists(), value
    with scenario() as case:
        leg = case.leg("L1")
        assert run_to_end(case, ["--jobs", "2", leg], clean_env()) == 2
        assert "unknown option '--jobs'" in case.stderr(), case.stderr()
        assert case.events() == []


def failure_notes(failed: str, how: str, unstarted: list[str]) -> bytes:
    """The lines the runner adds after a failed leg, in the order it adds them."""
    lines = [f"sim_pool: {failed} {how}"]
    lines += [f"sim_pool: {leg} was not started after a child failure" for leg in unstarted]
    lines.append(f"sim_pool: first leg in recipe order that did not pass: {failed}")
    return ("\n".join(lines) + "\n").encode()


def arm_a_failing_leg_fails_the_run_and_stops_later_starts() -> None:
    """A non-zero exit fails the run and is named; nothing starts after it has
    been seen; a leg already running finishes and is replayed whole."""
    with scenario() as case:
        l1 = case.leg("L1", out=[["out", "L1 before\n"]], after=[["out", "L1 after\n"]],
                      hold=case.hold_fifo("L1"))
        l2 = case.leg("L2", out=[["out", "L2 says why\n"]], hold=case.hold_fifo("L2"), exit=3)
        l3, l4 = case.leg("L3"), case.leg("L4")
        case.start(["--jobs=2", l1, l2, "--banner", "---- b3 ----", l3, l4], clean_env())
        pids = {news["leg"]: news["pid"] for news in (case.next_start(), case.next_start())}
        case.release("L2")
        case.wait_exit(pids["L2"])
        case.release("L1")
        assert case.finish() == 1, case.stderr()
        assert sorted(row["leg"] for row in case.events("start")) == ["L1", "L2"]
        want = (transcript((None, l1, "L1 before\nL1 after\n"), (None, l2, "L2 says why\n"))
                + failure_notes(l2, "exited with status 3", [l3, l4]))
        assert case.stdout() == want, case.stdout()
    with scenario() as case:
        l1, l3 = case.leg("L1", out=[["out", "L1 ran\n"]]), case.leg("L3")
        l2 = case.leg("L2", out=[["out", "L2 says why\n"]], exit=1)
        assert run_to_end(case, ["--jobs=1", l1, l2, l3], clean_env()) == 1
        assert [row["leg"] for row in case.events("start")] == ["L1", "L2"]
        want = (transcript((None, l1, "L1 ran\n"), (None, l2, "L2 says why\n"))
                + failure_notes(l2, "exited with status 1", [l3]))
        assert case.stdout() == want, case.stdout()


def arm_a_leg_killed_by_a_signal_fails_the_run() -> None:
    """A crash is a failure, named by its signal, however much the leg printed."""
    for crash in ("SIGSEGV", "SIGABRT"):
        with scenario() as case:
            l1, l3 = case.leg("L1", out=[["out", "fine\n"]]), case.leg("L3")
            l2 = case.leg("L2", out=[["out", "checks: 9   failures: 0\n"]], crash=crash)
            assert run_to_end(case, ["--jobs=1", l1, l2, l3], clean_env()) == 1, crash
            want = (transcript((None, l1, "fine\n"), (None, l2, "checks: 9   failures: 0\n"))
                    + failure_notes(l2, f"was killed by {crash}", [l3]))
            assert case.stdout() == want, case.stdout()


def arm_a_leg_that_cannot_start_fails_the_run() -> None:
    """A missing or non-executable leg is a failure, named with the reason,
    and stops every later start; the leg already running still finishes."""
    with scenario() as case:
        l1 = case.leg("L1", out=[["out", "L1 ran\n"]], hold=case.hold_fifo("L1"))
        l3 = case.leg("L3")
        gone = "./obj_gone/Vgone"
        case.start(["--jobs=2", l1, gone, l3], clean_env())
        case.release(case.next_start()["leg"])
        assert case.finish() == 1, case.stderr()
        why = f"could not be started: [Errno 2] No such file or directory: '{gone}'"
        want = transcript((None, l1, "L1 ran\n"), (None, gone, "")) + failure_notes(gone, why, [l3])
        assert case.stdout() == want, case.stdout()
        assert [row["leg"] for row in case.events("start")] == ["L1"]
    with scenario() as case:
        stuck = case.dir / "obj_stuck" / "Vstuck"
        stuck.parent.mkdir()
        stuck.write_text("#!/bin/sh\nexit 0\n")
        assert run_to_end(case, ["--jobs=1", "./obj_stuck/Vstuck"], clean_env()) == 1
        assert b"could not be started: [Errno 13] Permission denied" in case.stdout()


def arm_a_leg_that_prints_fail_and_exits_0_is_not_masked() -> None:
    """The runner passes a leg by its exit status only, and replays the [FAIL]
    line unchanged, so the sweep's own verdict still refuses the suite."""
    with scenario() as case:
        leg = case.leg("L1", out=[["out", "  [FAIL] a check that only logs\n"
                                          "checks: 3   failures: 1\n"]])
        assert run_to_end(case, ["--jobs=2", leg], clean_env()) == 0
        text = case.stdout().decode()
        assert log_reports_failure(text)[1], "the replay hid a masked verdict"
        assert "sim_pool:" not in text, text


def arm_an_interrupt_kills_every_leg_and_what_it_spawned() -> None:
    """SIGTERM, SIGINT, SIGHUP: every running leg and its descendant is killed
    and nothing it spawned carries on; the partial output is replayed under
    the leg with the signal named; the unstarted legs are named; the runner
    ends by the same signal."""
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        with scenario() as case:
            legs = [case.leg(name, out=[["out", f"{name} partial\n"], ["err", f"{name} err\n"]],
                             hold=case.hold_fifo(name), killed=True,
                             descendant_hold=case.hold_fifo(f"{name}-child"),
                             descendant_session=name == "L2")
                    for name in ("L1", "L2")]
            later = [case.leg("L3"), case.leg("L4")]
            case.start(["--jobs=2", legs[0], "--banner", "---- b2 ----", legs[1], *later],
                       clean_env())
            case.next_start()
            case.next_start()
            case.runner.send_signal(sig)
            status = case.finish()
            assert status == -sig, f"{sig.name}: the runner ended with {status}"
            assert case.events("survived") == [], f"{sig.name}: {case.events('survived')}"
            killed = f"was killed by this runner on {sig.name}; its output above is incomplete"
            want = (transcript((None, legs[0], "L1 partial\nL1 err\n"))
                    + f"sim_pool: {legs[0]} {killed}\n".encode()
                    + transcript(("---- b2 ----", legs[1], "L2 partial\nL2 err\n"))
                    + f"sim_pool: {legs[1]} {killed}\n".encode()
                    + "".join(f"sim_pool: {leg} was not started before {sig.name}\n"
                              for leg in later).encode())
            assert case.stdout() == want, case.stdout()
            kept = (case.dir / "obj_legs" / "01-VL1.log").read_bytes()
            assert kept == b"L1 partial\nL1 err\n", kept


def arm_a_leg_that_exits_leaves_nothing_it_spawned() -> None:
    """A leg that exits 0 with a descendant still running: the descendant dies
    with it, before the next leg, and the run still passes."""
    with scenario() as case:
        l1 = case.leg("L1", out=[["out", "L1 spawned and left\n"]], hold=case.hold_fifo("L1"),
                      descendant_hold=case.hold_fifo("L1-child"))
        l2 = case.leg("L2", out=[["out", "L2 ran\n"]])
        case.start(["--jobs=1", l1, l2], clean_env())
        case.release(case.next_start()["leg"])
        assert case.finish() == 0, case.stderr()
        assert case.events("survived") == [], case.events("survived")
        assert case.stdout() == transcript((None, l1, "L1 spawned and left\n"),
                                           (None, l2, "L2 ran\n")), case.stdout()


def arm_an_interrupt_inherited_as_ignored_stays_ignored() -> None:
    """Started with SIGHUP ignored, the runner neither acts on one nor gives
    it back to the legs: they finish and keep the inherited ignore."""
    with scenario() as case:
        legs = [case.leg(name, out=[["out", f"{name} ran\n"]], hold=case.hold_fifo(name))
                for name in ("L1", "L2")]
        case.start(["--jobs=2", *legs], clean_env(), ignore=(signal.SIGHUP,))
        case.next_start()
        case.next_start()
        case.runner.send_signal(signal.SIGHUP)
        case.release("L1")
        case.release("L2")
        assert case.finish() == 0, case.stderr()
        assert case.stdout() == transcript((None, legs[0], "L1 ran\n"),
                                           (None, legs[1], "L2 ran\n")), case.stdout()
        for row in case.events("start"):
            assert int(row["sigign"], 16) & sigmask_bits(signal.SIGHUP), row["sigign"]


FRAME_NOTE = (b"sim_pool: MILAN_COUNTER_FRAME_OUT is set, so the legs run one at a "
              b"time in recipe order\n")


def arm_the_frame_dump_variable_runs_one_leg_at_a_time() -> None:
    """MILAN_COUNTER_FRAME_OUT present, even empty, beats --jobs=2: one leg at
    a time in recipe order, the file ends with the last writer's bytes, and an
    empty name fails at the first writer and starts nothing after it."""
    with scenario() as case:
        dump = case.dir / "frame.bin"
        legs = [case.leg(f"L{k}", out=[["out", f"L{k} ran\n"]], hold=case.hold_fifo(f"L{k}"),
                         dump=k % 2 == 0) for k in range(1, 5)]
        case.start(["--jobs=2", legs[0], "--exclusive", legs[1], "--exclusive", legs[2], legs[3]],
                   clean_env(MILAN_COUNTER_FRAME_OUT=str(dump)))
        counts = hold_protocol(case, len(legs), 1)
        assert case.finish() == 0, case.stderr()
        assert counts == [1, 1, 1, 1], counts
        starts = case.events("start")
        assert [(row["leg"], row["siblings"]) for row in starts] == [
            ("L1", 1), ("L2", 1), ("L3", 1), ("L4", 1)], starts
        assert dump.read_bytes() == b"L4", dump.read_bytes()
        want = FRAME_NOTE + transcript(*[(None, leg, f"L{k} ran\n")
                                         for k, leg in enumerate(legs, start=1)])
        assert case.stdout() == want, case.stdout()
    with scenario() as case:
        l1 = case.leg("L1", out=[["out", "L1 ran\n"]], hold=case.hold_fifo("L1"))
        l2 = case.leg("L2", out=[["out", "L2 ran\n"]], dump=True)
        l3 = case.leg("L3", dump=True)
        case.start(["--jobs=2", "--exclusive", l1, "--exclusive", l2, l3],
                   clean_env(MILAN_COUNTER_FRAME_OUT=""))
        case.next_start()
        assert case.runner_children() == 1, "a second leg started beside L1"
        case.release("L1")
        assert case.finish() == 1, case.stderr()
        assert [(row["leg"], row["siblings"]) for row in case.events("start")] == [
            ("L1", 1), ("L2", 1)]
        want = (FRAME_NOTE + transcript((None, l1, "L1 ran\n"),
                                        (None, l2, "L2 ran\n  [FAIL] optional reference frame dump\n"))
                + failure_notes(l2, "exited with status 1", [l3]))
        assert case.stdout() == want, case.stdout()


def runner_lines(text: str) -> list[str]:
    """The lines the runner wrote itself."""
    return [line for line in text.splitlines() if line.startswith("sim_pool:")]


def arm_the_runner_adds_no_check_and_no_failure() -> None:
    """On the failing, unstartable, interrupted and frame-dump paths, the
    tally of the replayed output is exactly the legs' own, and no line of the
    runner's is a tally shape or a [FAIL] marker."""
    lines = []
    with scenario() as case:
        l1 = case.leg("L1", out=[["out", "checks: 5   failures: 0\n"]])
        l2 = case.leg("L2", out=[["out", "checks: 2   failures: 1\n"]], exit=1)
        assert run_to_end(case, ["--jobs=1", l1, l2, case.leg("L3")], clean_env()) == 1
        checks, failures, _matched, unparsed, _skipped = scan(case.stdout().decode())
        assert (checks, failures, unparsed) == (7, 1, []), (checks, failures, unparsed)
        lines += runner_lines(case.stdout().decode())
    with scenario() as case:
        l1 = case.leg("L1", out=[["out", "checks: 4   failures: 0\n"]])
        assert run_to_end(case, ["--jobs=2", l1, "./obj_gone/Vgone", case.leg("L3")],
                          clean_env()) == 1
        assert scan(case.stdout().decode())[:2] == (4, 0)
        lines += runner_lines(case.stdout().decode())
    with scenario() as case:
        l1 = case.leg("L1", out=[["out", "checks: 6   failures: 0\n"]],
                      hold=case.hold_fifo("L1"), killed=True)
        case.start(["--jobs=2", l1, case.leg("L2")],
                   clean_env(MILAN_COUNTER_FRAME_OUT=str(case.dir / "f.bin")))
        case.next_start()
        case.runner.send_signal(signal.SIGTERM)
        assert case.finish() == -signal.SIGTERM
        assert scan(case.stdout().decode())[:2] == (6, 0)
        lines += runner_lines(case.stdout().decode())
    kinds = ("exited with status", "was not started after", "first leg in recipe order",
             "could not be started", "killed by this runner", "was not started before",
             "MILAN_COUNTER_FRAME_OUT is set")
    for kind in kinds:
        assert any(kind in line for line in lines), f"no runner line says {kind!r}"
    for line in lines:
        _checks, _failures, matched, unparsed, _skipped = scan(line)
        assert matched == [] and unparsed == [], f"a runner line tallies: {line}"
        assert FAIL_MARKER.match(line) is None, f"a runner line is a [FAIL] marker: {line}"


def logical_lines(text: str) -> list[str]:
    """`make -n` output with each continued command joined onto one line."""
    return text.replace("\\\n", " ").splitlines()


def arm_the_makefile_hands_the_runner_the_recipes_ten_legs() -> None:
    """`make -n run`: the runner gets exactly the recipe's ten legs, in its
    order and with its banners, two workers unless SIM_JOBS=1 and whatever
    -j says, after the ten builds and before render_mutants.py, on a line
    whose errors make does not ignore."""
    expected: list[str] = []
    for banner, exe in LEGACY_LEGS:
        if banner is not None:
            expected += ["--banner", banner]
        if exe.split("/")[1] in {"obj_notify", "obj_nxn", "obj_nxndv", "obj_nxn8", "obj_nxn4c"}:
            expected.append("--exclusive")
        expected.append(exe)
    for extra, jobs in (([], "2"), (["SIM_JOBS=1"], "1"), (["-j8"], "2")):
        dry = subprocess.run(["make", "-n", "-C", str(HERE), "run", *extra],
                             env=clean_env(), capture_output=True, text=True, check=False)
        assert dry.returncode == 0, dry.stderr
        lines = logical_lines(dry.stdout)
        runner_at = [k for k, line in enumerate(lines) if "sim_pool.py" in line]
        assert len(runner_at) == 1, runner_at
        words = shlex.split(lines[runner_at[0]])
        assert words == ["exec", "python3", "sim_pool.py", f"--jobs={jobs}", *expected], words
        built = [k for k, line in enumerate(lines)
                 for _banner, exe in LEGACY_LEGS if line.endswith(f"-o {Path(exe).name}")]
        assert len(built) == len(LEGACY_LEGS), f"{extra}: {len(built)} of the ten builds"
        assert max(built) < runner_at[0] < lines.index("python3 render_mutants.py"), extra
    recipe = [line for line in (HERE / "Makefile").read_text().splitlines()
              if "sim_pool.py" in line and line.startswith("\t")]
    assert len(recipe) == 1, recipe
    prefix = recipe[0][:recipe[0].index("exec")]
    assert set(prefix) <= {"\t", "@"}, f"the runner's recipe line ignores errors: {prefix!r}"


ARMS = (
    arm_both_worker_counts_run_each_leg_once_as_the_recipe_did,
    arm_every_byte_is_replayed_in_recipe_order,
    arm_a_leg_that_finishes_first_still_prints_second,
    arm_never_more_than_two_legs_alive,
    arm_shared_group_is_exclusive_ordered_and_allows_independent_overlap,
    arm_skipped_group_members_do_not_hide_later_logs,
    arm_worker_counts_other_than_one_or_two_are_refused,
    arm_a_failing_leg_fails_the_run_and_stops_later_starts,
    arm_a_leg_killed_by_a_signal_fails_the_run,
    arm_a_leg_that_cannot_start_fails_the_run,
    arm_a_leg_that_prints_fail_and_exits_0_is_not_masked,
    arm_an_interrupt_kills_every_leg_and_what_it_spawned,
    arm_a_leg_that_exits_leaves_nothing_it_spawned,
    arm_an_interrupt_inherited_as_ignored_stays_ignored,
    arm_the_frame_dump_variable_runs_one_leg_at_a_time,
    arm_the_runner_adds_no_check_and_no_failure,
    arm_the_makefile_hands_the_runner_the_recipes_ten_legs,
)


def main() -> int:
    """Run every arm; 1 if any of them failed."""
    if not hasattr(os, "pidfd_open") or not Path("/proc/self/stat").is_file():
        print("[FAIL] these arms need Linux /proc and os.pidfd_open; nothing was run")
        return 1
    passes = fails = 0
    for arm in ARMS:
        try:
            arm()
        except Exception as finding:
            #! Every arm reports, including one that broke rather than
            #! asserted: a traceback out of the first arm would leave the
            #! rest of the list unrun and unreported.
            fails += 1
            print(f"[FAIL] {arm.__name__}: {type(finding).__name__}: {finding}")
        else:
            passes += 1
            print(f"[PASS] {arm.__name__}")
    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
