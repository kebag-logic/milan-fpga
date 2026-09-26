#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""F1: cancellation must finish while the stdout consumer stays blocked.

Run directly and through the unchanged actual Makefile, with inert build and
prerequisite executables. These are host orchestration controls, not RTL checks.
Hold both legs until their pidfds are owned; release the first and saturate
stdout. Large binary copies and a small final flush are separate cases.
Only after runner exit and owned-process reaping may the reader drain.
The two-second pidfd observation bounds cancellation, not simulation behavior.
An outer command guard handles broken fixture setup as UNKNOWN, never PASS.
--output preserves every fixture, capture and result in a new directory.
"""

import argparse
import array
import contextlib
import ctypes
import fcntl
import json
import os
import select
import signal
import subprocess
import sys
import tempfile
import termios
from dataclasses import dataclass
from pathlib import Path

from test_sim_pool import HERE, LEGACY_LEGS, Scenario, clean_env, transcript



@dataclass(frozen=True)
class Control:
    """One wiring/output boundary and its signal/race variant."""

    recipe: bool
    flush: bool
    signo: signal.Signals | None
    race: str


def events(fd: int, milliseconds: int = 0) -> list:
    """Observe exit/reaping without changing process state."""
    poller = select.poll()
    poller.register(fd, select.POLLIN | select.POLLHUP)
    return poller.poll(milliseconds)


def reaped(observed: list) -> bool:
    """POLLIN alone includes an unreaped zombie; require POLLHUP."""
    return bool(observed and observed[0][1] & select.POLLHUP)


def queued(fd: int) -> int:
    """Bytes pending in the pipe; this observation never consumes them."""
    count = array.array("i", [0])
    fcntl.ioctl(fd, termios.FIONREAD, count)
    return count[0]


def prepare(case: Scenario, recipe: bool, body: str) -> tuple[list[str], list]:
    """Use the original two held fixtures at the recipe's original paths."""
    commands = []
    selected = list(LEGACY_LEGS) if recipe else [(None, "./obj_L1/VL1"),
                                                (None, "./obj_L2/VL2")]
    for index, (_banner, exe) in enumerate(selected):
        name = f"L{index + 1}"
        cfg = {"out": [["out", body if index == 0 else f"{name} partial\n"]]}
        if index < 2:
            cfg["hold"] = case.hold_fifo(name)
        if index == 1:
            cfg.update(descendant_hold=case.hold_fifo("descendant"), descendant_session=True)
        original = case.leg(name, **cfg)
        if original != exe:
            target = case.dir / exe
            target.parent.mkdir(exist_ok=True)
            (case.dir / original).replace(target)
        commands.append(exe)
    (case.dir / "sim_pool.py").write_bytes((HERE / "sim_pool.py").read_bytes())
    if not recipe:
        return [sys.executable, "sim_pool.py", "--jobs=2", *commands], selected
    (case.dir / "Makefile").write_bytes((HERE / "Makefile").read_bytes())
    for path in ("compiler", "obj_gptp/Vmilan_dp_gptp", "obj_gptplat/Vmilan_dp_gptplat",
                 "obj_gmstep/Vmilan_dp_gmstep"):
        exe = case.dir / path
        exe.parent.mkdir(exist_ok=True)
        exe.write_text("#!/bin/sh\nexit 0\n")
        exe.chmod(0o755)
    (case.dir / "render_mutants.py").write_text(
        "from pathlib import Path\nPath('render-ran').touch()\n")
    (case.dir / "gmstep_mutants.py").write_text(
        "from pathlib import Path\nPath('gmstep-controls-ran').touch()\n")
    argv = ["make", "-s", "--no-print-directory", "-f", "Makefile", "run",
            f"CURDIR={HERE}", f"VERILATOR={case.dir}/compiler", "VERILATOR_JOBS=8"]
    # Query expanded prerequisites from the actual recipe, rather than keep
    # a second generated-input inventory. All three prerequisite legs execute.
    # CRFLIC_BUILD also adds a target-specific .SHELLSTATUS assignment.
    # That database row is a variable, not the run prerequisite list.
    database = subprocess.run(["make", "-np", "-C", str(HERE), "run"],
                              env=clean_env(), capture_output=True, text=True, check=True)
    prerequisites = next(line.split()[1:] for line in database.stdout.splitlines()
                         if line.startswith("run:") and ":=" not in line)
    for name in prerequisites:
        if name not in ("gptp", "gptp-lat", "gmstep"):
            argv += ["-o", name]
    argv += ["-o", "gmstep-build"]
    return argv, selected


def check_delivery(case: Scenario, selected: list, body: str, prefix: bytes,
                   output: bytes, control: Control) -> dict:
    """Judge binary output against independent fixture bytes and legacy order."""
    recipe, sig, race = control.recipe, control.signo, control.race
    disk = (case.dir / "obj_legs/replay.log").read_bytes()
    for index, (_banner, exe) in enumerate(selected[:2]):
        expected = (body if index == 0 else "L2 partial\n").encode("latin-1")
        assert (case.dir / "obj_legs" / f"{index + 1:02d}-{Path(exe).name}.log").read_bytes() == expected
        assert disk.count(expected) == 1, "capture omitted or duplicated on disk"
    if sig is None:
        expected = transcript(*[(banner, exe, body if index == 0 else f"L{index + 1} partial\n")
                                for index, (banner, exe) in enumerate(selected)])
        assert disk == expected, "legacy binary transcript changed"
        suffix = (b"---- #386 render law: the same leg against mutated setpoint stages and datapath ----\n"
                  b"---- #387 GM step re-base: the gmstep leg against the acceptance's controls ----\n"
                  if recipe else b"")
        assert output == prefix + expected + suffix, "pipe output lost/duplicated/reordered bytes"
        assert (case.dir / "render-ran").exists() == recipe
        assert (case.dir / "gmstep-controls-ran").exists() == recipe
    else:
        assert (prefix + disk).startswith(output), "partial delivery is not a transcript prefix"
        assert len(output) == len(prefix), "consumer drained before cancellation assertions"
        if race != "child-exit":
            assert f"on {sig.name}".encode() in disk, "partial capture lacks signal attribution"
        if recipe:
            assert b"was not started before" in disk, "unstarted legs not attributed"
    return dict(accepted=True, exit=case.runner.returncode, captured_bytes=len(disk),
                delivered_bytes=len(output))


def cancel_blocked(case: Scenario, control: Control, read_fd: int,
                   write_fd: int, runner_fd: int, row: dict) -> None:
    """Require shutdown and owned reaping before permitting any consumer drain."""
    recipe, sig, race = control.recipe, control.signo, control.race
    if recipe:
        os.killpg(case.runner.pid, sig)
    else:
        case.runner.send_signal(sig)
    if race == "repeated":
        for _ in range(8):
            with contextlib.suppress(ProcessLookupError):
                signal.pidfd_send_signal(runner_fd, sig)
    runner_events = events(runner_fd, 2000)
    owned = {pid: events(fd) for pid, fd in case.pidfds.items()}
    row.update(signal=sig.name, recipe=recipe, race=race,
               runner_events=runner_events, owned_events=owned,
               queued_after=queued(read_fd),
               descriptor_restored=os.get_blocking(write_fd))
    (case.dir / "before-drain.json").write_text(json.dumps(row, indent=2) + "\n")
    assert runner_events, "runner did not shut down while stdout stayed blocked"
    assert all(reaped(value) for value in owned.values()), "owned processes not reaped"
    assert row["descriptor_restored"], "shared stdout flags were not restored"
    # Reap make/the direct runner before any stdout read.
    parent_fd = os.pidfd_open(case.runner.pid)
    try:
        assert events(parent_fd, 2000), "recipe did not end before consumer drain"
    finally:
        os.close(parent_fd)
    assert case.runner.wait() == -sig, "original cancellation status was lost"
    assert not (case.dir / "render-ran").exists(), "render ran after cancellation"
    assert not (case.dir / "gmstep-controls-ran").exists(), "GM-step controls ran after cancellation"


def exercise(root: Path, recipe: bool, flush: bool, sig: signal.Signals | None,
             race: str) -> dict:
    """Retain verdict observations before either drain or fallback cleanup."""
    root.mkdir()
    control = Control(recipe, flush, sig, race)
    case = Scenario(root)
    read_fd, write_fd = os.pipe()
    runner_fd = None
    row = {}
    try:
        capacity = fcntl.fcntl(write_fd, fcntl.F_SETPIPE_SZ, 4096)
        body = "first binary\x00\xff\x80" + ("x" * 262144 if not flush else "") + "\n"
        argv, selected = prepare(case, recipe, body)

        def signal_state() -> None:
            """Give the cancellation fixture its own interrupt preconditions."""
            for signo in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
                signal.signal(signo, signal.SIG_DFL)
            signal.pthread_sigmask(signal.SIG_SETMASK, set())

        with case.stderr_path.open("wb") as err:
            case.runner = subprocess.Popen(argv, cwd=root, env=clean_env(MAKEFLAGS="-j8"),
                                           stdout=write_fd, stderr=err, start_new_session=True,
                                           preexec_fn=signal_state)
        news = [case.next_start(), case.next_start()]
        starts = {entry["leg"]: entry for entry in news}
        # Both writers announced their start records and are now held.
        # Save the PID before release; later appends can leave a partial line.
        runner_pid = next(entry["ppid"] for entry in case.events("start"))
        runner_fd = os.pidfd_open(runner_pid)
        prefix = b"======================================================================\n" if recipe else b""
        # Fill capacity after make's pre-run echo. A large nonblocking write
        # can lack capacity even before FIONREAD reaches the nominal maximum.
        # Fully saturating first gives both implementations the same handshake.
        os.set_blocking(write_fd, False)
        try:
            while True:
                os.write(write_fd, b"P")
                prefix += b"P"
        except BlockingIOError:
            pass
        finally:
            os.set_blocking(write_fd, True)
        case.release("L1")
        first_fd = case.pidfds[starts["L1"]["pid"]]
        while not reaped(events(first_fd)) or queued(read_fd) != capacity:
            assert case.runner.poll() is None, "exited before blocked-output handshake"
            # A readiness retry, with no clock-derived test result.
            signal.sigtimedwait(set(), 0.005)
        if race == "child-exit":
            case.release("L2")
        row.update(argv=argv, runner_pid=runner_pid, flush=flush,
                   queued_before=queued(read_fd))
        if sig is not None:
            cancel_blocked(case, control, read_fd, write_fd, runner_fd, row)
        else:
            case.release("L2")
        # Draining is a positive output control, never a cancellation prerequisite.
        os.close(write_fd)
        write_fd = -1
        with os.fdopen(read_fd, "rb") as reader:
            read_fd = -1
            output = reader.read()
        (root / "stdout-after-drain").write_bytes(output)
        if sig is None:
            assert case.finish() == 0, case.stderr()
        row.update(check_delivery(case, selected, body, prefix, output, control))
        return row
    finally:
        (root / "result.json").write_text(json.dumps(row, indent=2) + "\n")
        case.close()
        for fd in (read_fd, write_fd, runner_fd):
            if fd is not None and fd >= 0:
                os.close(fd)


def run(root: Path) -> int:
    """Exercise both wiring paths and both output boundaries independently."""
    assert ctypes.CDLL(None).prctl(36, 1, 0, 0, 0) == 0
    failures = 0
    for recipe in (False, True):
        for flush in (False, True):
            controls = [(sig, race) for sig in (signal.SIGINT, signal.SIGTERM)
                        for race in ("active", "repeated", "child-exit")]
            controls.append((None, "drain"))
            for sig, race in controls:
                name = (f"{'make' if recipe else 'direct'}-{'flush' if flush else 'copy'}-"
                        f"{sig.name if sig else 'normal'}-{race}")
                try:
                    exercise(root / name, recipe, flush, sig, race)
                except Exception as exc:
                    failures += 1
                    print(f"[FAIL] {name}: {type(exc).__name__}: {exc}", flush=True)
                else:
                    print(f"[PASS] {name}", flush=True)
    print(f"28 backpressure controls: {28 - failures} PASS, {failures} FAIL")
    return int(bool(failures))


def main() -> int:
    """Optionally retain the disposable fixtures and raw observations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is not None:
        args.output.mkdir(parents=True, exist_ok=False)
        return run(args.output.resolve())
    with tempfile.TemporaryDirectory(prefix="sim-pool-backpressure-") as directory:
        return run(Path(directory))


if __name__ == "__main__":
    sys.exit(main())
