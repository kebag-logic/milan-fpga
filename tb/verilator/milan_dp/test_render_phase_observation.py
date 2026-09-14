#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Pure fixtures for the #445 phase observation in render_mutants.py.

Standard library only, and nothing here starts a process, compiles anything
or reads the host's clock. The driver's two calls are stubbed with scripted
results, its clock is a fake the arms step by hand, its records go to a
recording stream, and its subprocess handle is replaced by a guard whose
every entry raises: an arm that reaches a real launch fails instead of
running one.

What the arms hold, and why each one is here:

* the records frame the calls the driver already made, in order, with one
  sequence number per record and no gap, and they name all six outcomes -
  two positive control modes and the four mutations - by a fixed label;
* the durations are the ones the fake clock was stepped by, the gaps between
  phases are accounted separately, and every record is flushed as it is
  written, so a kill cannot hide the last phase entered;
* the unmutated leg records whether the already-built executable was reused
  or the existing fallback build ran, with the fallback's frozen arguments;
* a completed build's record carries the status the recipe returned as well
  as whether a leg came out of it, and build() returns and prints as before;
* the driver prints exactly what it printed before, on the passing and on
  the failing paths, and the records add no check and no failure to what
  scripts/suite_tally.py reads out of the same log;
* a kill names the case and phase it landed in, leaves that phase without an
  end record and with no result, and still exits 143 after the temporary
  directory is removed;
* a kill delivered from the record stream, the instant a phase's end record
  is out and the driver's next statement has not run, reports the idle it is
  in and never calls that finished phase incomplete;
* a clock that refuses a reading, at the origin, around a call or under the
  kill, costs that record its number and nothing else: the child results, the
  verdicts, the tally, exit 143 and the cleanup are untouched, and no lost
  timing is made up; a call of the driver's own that raises still raises;
* the child arguments, working directory, session and process-group cleanup
  are the ones the driver always passed, and the frozen six-case inventory
  still plants the frozen replacement.

Usage: python3 tb/verilator/milan_dp/test_render_phase_observation.py
Exit 0 = every arm held.
"""

import contextlib
import io
import json
import sys
import tempfile
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import NamedTuple, TextIO

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_mutants as driver  # noqa: E402

sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure, scan  # noqa: E402

#: the two short modes, in the order the driver's positive controls run them
CONTROL_MODES = ("--live-only", "--render-only")

#: the fixed logical case label of each mutation, in table order
MUTANT_CASES = (
    "prefill_target_three_events_high",
    "recentre_pulse_ignored",
    "recentre_counted_and_cleared_but_not_snapped",
    "clock_source_trigger_dropped_from_the_recentre_set",
)

#: the frozen identity of each mutation: (name, source key, mode, named check)
MUTANT_IDENTITY = (
    ("prefill target three events high", "stage", "--render-only",
     "RENDER-INT: every PDU's first event inside the law band"),
    ("recentre pulse ignored", "stage", "--render-only",
     "RENDER-RC-INT: the recentre restored the law "
     "(fill at accept = setpoint) (late)"),
    ("recentre counted and cleared but not snapped", "stage", "--render-only",
     "RENDER-RC-INT: the recentre restored the law "
     "(fill at accept = setpoint) (early)"),
    ("clock-source trigger dropped from the recentre set", "datapath",
     "--live-only",
     "RENDER-LIVE-CRF: the fill at accept is the setpoint for every PDU"),
)

#: what the driver prints when every control passes and every mutant is caught
CAUGHT_RUN_LINES = (
    "[PASS] the unmutated gateware still passes the render-law leg "
    "(--live-only)",
    "[PASS] the unmutated gateware still passes the render-law leg "
    "(--render-only)",
    '[PASS] mutant caught (--render-only): prefill target three events high'
    ' - breaks "RENDER-INT: every PDU\'s first event inside the law band"',
    '[PASS] mutant caught (--render-only): recentre pulse ignored - breaks'
    ' "RENDER-RC-INT: the recentre restored the law'
    ' (fill at accept = setpoint) (late)"',
    '[PASS] mutant caught (--render-only): recentre counted and cleared but'
    ' not snapped - breaks "RENDER-RC-INT: the recentre restored the law'
    ' (fill at accept = setpoint) (early)"',
    '[PASS] mutant caught (--live-only): clock-source trigger dropped from'
    ' the recentre set - breaks "RENDER-LIVE-CRF: the fill at accept is the'
    ' setpoint for every PDU"',
    "",
    "6 checks: 6 PASS, 0 FAIL",
)


class FakeClock:
    """A clock the arms step by hand. It reads no host time, so a duration in
    a record is exactly the time an arm charged for that call."""

    def __init__(self, start: float = 1000.0) -> None:
        """Start at an offset no arm may assume, so only differences hold."""
        self._now = start

    def __call__(self) -> float:
        """The current reading, unchanged by being read."""
        return self._now

    def advance(self, seconds: float) -> None:
        """Charge `seconds` to whatever is running."""
        self._now += seconds


class RecordingStream:
    """A text stream that keeps every write and every flush, in order,
    optionally mirrors the text into the stream the driver prints to, and
    optionally delivers the kill to the handler main() installed once a named
    record has been written AND flushed. That last is the one moment a kill can
    land with a completed phase's record already out of the driver and the
    driver's next statement not yet run, and it needs no process and no real
    signal to reach."""

    def __init__(self, mirror: TextIO | None = None, kill_at: str = "",
                 installed: list | None = None) -> None:
        """Take an optional mirror, and the record an arm wants killed after."""
        self.events: list[tuple[str, str]] = []
        self.killed_after: dict | None = None
        self._mirror = mirror
        self._kill_at = kill_at
        self._installed = installed

    def write(self, text: str) -> int:
        """Record the text, mirror it if asked, and report it written."""
        self.events.append(("write", text))
        if self._mirror is not None:
            self._mirror.write(text)
        return len(text)

    def flush(self) -> None:
        """Record the flush, then deliver the kill if that record was the one."""
        self.events.append(("flush", ""))
        emitted = self.records()[-1]
        if (self._installed and self.killed_after is None
                and emitted["event"] == self._kill_at):
            self.killed_after = emitted
            self._installed[0][1](FakeSignal.SIGTERM, None)

    def records(self) -> list[dict]:
        """The written records, parsed, in the order they were written."""
        return [json.loads(text.split(" ", 1)[1])
                for kind, text in self.events if kind == "write"]


class UnreadableClock(FakeClock):
    """A fake clock that counts its readings and refuses the ones an arm names,
    so an arm can prove a timing nobody can take costs the diagnostic and
    nothing else. Refusing nothing, it is simply the counter."""

    def __init__(self, failing: frozenset = frozenset(),
                 fail_from: int | None = None) -> None:
        """Refuse the numbered readings, and every reading from `fail_from` on."""
        super().__init__()
        self.reads = 0
        self._failing = failing
        self._fail_from = fail_from

    def __call__(self) -> float:
        """Count this reading, then give it or refuse it as the arm asked."""
        self.reads += 1
        if self.reads in self._failing or (
                self._fail_from is not None and self.reads >= self._fail_from):
            raise OSError("the observation clock cannot be read")
        return super().__call__()


class BrokenStream:
    """A stream that cannot be written, so an arm can prove that a record
    nobody can write costs the diagnostic and nothing else."""

    def write(self, text: str) -> int:
        """Refuse the write the way a closed pipe would."""
        raise OSError("the record stream is closed")

    def flush(self) -> None:
        """Refuse the flush the same way."""
        raise OSError("the record stream is closed")


class LaunchGuard:
    """Stands in for the driver's subprocess handle: every entry raises, so an
    arm that reaches a real process launch fails instead of running one."""

    def __getattr__(self, name: str) -> object:
        """Refuse every use, naming the one that was reached."""
        raise AssertionError(
            f"fixture reached subprocess.{name}: no arm may launch a process")


class FakeSignal:
    """Stands in for the driver's signal handle: it records the handler main()
    installs instead of arming one, and carries the constants it names."""

    SIGTERM = 15
    SIGKILL = 9

    def __init__(self, installed: list) -> None:
        """Take the list the fixture reads the installed handler out of."""
        self.installed = installed

    def signal(self, number: int, handler: Callable) -> None:
        """Record the installation, arm nothing."""
        self.installed.append((number, handler))


class FakeOs:
    """Stands in for the driver's os handle: it records the process-group kill
    instead of signalling anything."""

    def __init__(self) -> None:
        """Start with nothing killed."""
        self.killed: list[tuple[int, int]] = []

    def getpgid(self, pid: int) -> int:
        """A group id distinct from the pid, so an arm can tell them apart."""
        return pid + 1000

    def killpg(self, pgid: int, number: int) -> None:
        """Record the group and signal the driver asked for."""
        self.killed.append((pgid, number))


class FakeCompleted(NamedTuple):
    """The three fields build() reads off a completed process."""

    returncode: int
    stdout: str
    stderr: str


class FakeProc:
    """The four members run_leg() uses on a child, with nothing behind them."""

    pid = 4242

    def __init__(self, status: int, output: str, running: bool = False) -> None:
        """Script the wait result and whether the child is still running."""
        self.returncode = status
        self.waited = False
        self._output = output
        self._running = running

    def communicate(self) -> tuple[str, None]:
        """The captured output, as the driver's text-mode child returns it."""
        return self._output, None

    def poll(self) -> int | None:
        """None while the scripted child is still running."""
        return None if self._running else self.returncode

    def wait(self) -> int:
        """Record that the driver waited for the killed child."""
        self.waited = True
        return self.returncode


class RecordingSubprocess:
    """Stands in for the driver's subprocess handle in the argument arms: it
    records the call and returns a scripted result, and launches nothing."""

    PIPE = "PIPE-sentinel"
    STDOUT = "STDOUT-sentinel"

    def __init__(self, result: object) -> None:
        """Take the completed process or child the scripted call returns."""
        self.calls: list[tuple[tuple, dict]] = []
        self._result = result

    def run(self, argv: list, **kwargs: object) -> object:
        """Record one build invocation and answer it."""
        self.calls.append((tuple(argv), kwargs))
        return self._result

    def Popen(self, argv: list, **kwargs: object) -> object:  # noqa: N802
        """Record one leg launch and answer it."""
        self.calls.append((tuple(argv), kwargs))
        return self._result


class BuildStep(NamedTuple):
    """One scripted build(): what it costs, whether it yields a leg, and the
    exit status the recipe itself returned."""

    seconds: float
    ok: bool = True
    returncode: int = 0


class LegStep(NamedTuple):
    """One scripted run_leg(): what it costs and what the child returned."""

    seconds: float
    status: int = 0
    output: str = ""


class Plan(NamedTuple):
    """One scripted run of the driver."""

    builds: tuple[BuildStep, ...] = ()
    legs: tuple[LegStep, ...] = ()
    prebuilt: bool = True
    sources: dict | None = None
    interrupt_at: int | None = None


class DriverRun(NamedTuple):
    """What one scripted run of the driver did."""

    status: int
    output: str
    lines: list[str]
    records: list[dict]
    stream: object
    builds: list[tuple]
    legs: list[tuple]
    handlers: list[tuple]
    work_exists: bool | None


def catch_log(check: str) -> str:
    """A child log that reports the named check as failed."""
    return f"[FAIL] {check} was not restored\n1 checks: 0 PASS, 1 FAIL\n"


def frozen_source(key: str) -> str:
    """A stand-in source for one key, carrying each frozen pattern once."""
    body = [f"// stand-in {key} source for the #445 fixtures"]
    body += [pattern for _, source, pattern, _, _, _ in driver.MUTATIONS
             if source == key]
    return "\n".join(body) + "\n"


def planted_sources(root: Path, override: dict | None) -> dict:
    """Write one stand-in source per key and return the driver's own mapping,
    with the frozen Makefile overrides kept."""
    texts = override or {key: frozen_source(key) for key in driver.SOURCES}
    mapping = {}
    for key, (path, flag) in driver.SOURCES.items():
        stand_in = root / path.name
        stand_in.write_text(texts[key])
        mapping[key] = (stand_in, flag)
    return mapping


def build_stub(clock: FakeClock, plan: Plan, calls: list) -> Callable:
    """A stand-in build(): charge the scripted time, hand the scripted recipe
    status to the recorder the wrapper passes, answer as scripted, and read
    back what was planted (a mutated copy lives beside its object dir; the
    control's fallback names the unmutated source, which is not read)."""
    def stub(flag: str, rtl_path: Path, mdir: Path,
             observed: Callable | None = None) -> Path | None:
        """Answer one framed build the way the plan's next step says to."""
        planted = rtl_path.read_text() if rtl_path.parent == mdir.parent else None
        calls.append((flag, rtl_path, mdir, planted))
        step = plan.builds[len(calls) - 1]
        clock.advance(step.seconds)
        if observed is not None:
            observed(step.returncode)
        return mdir / "Vmilan_dp_aclk" if step.ok else None
    return stub


def leg_stub(clock: FakeClock, plan: Plan, calls: list, installed: list) -> Callable:
    """A stand-in run_leg(): charge the scripted time, answer as scripted, and
    deliver the kill inside the scripted phase when the plan asks for one."""
    def stub(exe: Path, mode: str) -> tuple[int, str]:
        """Answer one framed leg the way the plan's next step says to."""
        calls.append((exe, mode))
        index = len(calls) - 1
        step = plan.legs[index]
        clock.advance(step.seconds)
        if plan.interrupt_at == index:
            installed[0][1](FakeSignal.SIGTERM, None)
        return step.status, step.output
    return stub


@contextlib.contextmanager
def stood_in(replacements: dict) -> Iterator[None]:
    """Stand in for module attributes for one arm, and restore them after."""
    saved = {name: getattr(driver, name) for name in replacements}
    try:
        for name, value in replacements.items():
            setattr(driver, name, value)
        yield
    finally:
        for name, value in saved.items():
            setattr(driver, name, value)


def run_driver(plan: Plan, mirror: bool = True, stream: object = None,
               clock: FakeClock | None = None,
               installed: list | None = None) -> DriverRun:
    """Run the driver's main() against `plan` under pure stand-ins. An arm that
    breaks the clock, or reaches the installed handler from its own stream,
    supplies its own."""
    clock = FakeClock() if clock is None else clock
    printed = io.StringIO()
    stream = RecordingStream(printed if mirror else None) if stream is None else stream
    builds: list = []
    legs: list = []
    installed = [] if installed is None else installed
    with tempfile.TemporaryDirectory(prefix="a115-fixture-") as td:
        root = Path(td)
        clean = root / "obj_aclk" / "Vmilan_dp_aclk"
        if plan.prebuilt:
            clean.parent.mkdir()
            clean.write_text("stand-in leg\n")
        replacements = {
            "SOURCES": planted_sources(root, plan.sources),
            "CLEAN_EXE": clean,
            "build": build_stub(clock, plan, builds),
            "run_leg": leg_stub(clock, plan, legs, installed),
            "subprocess": LaunchGuard(),
            "signal": FakeSignal(installed),
        }
        with stood_in(replacements), contextlib.redirect_stdout(printed):
            log = driver.PhaseLog(stream=stream, clock=clock)
            try:
                status = driver.main(log)
            except SystemExit as stop:
                status = int(stop.code or 0)
        #! the driver's own working directory, known only once it has built
        #! something into it, so an arm that asks about cleanup without one
        #! gets None and fails rather than a vacuous False.
        work = [call[2].parent for call in builds]
    output = printed.getvalue()
    lines = [line for line in output.splitlines()
             if not line.startswith(driver.PHASE_MARKER)]
    records = stream.records() if isinstance(stream, RecordingStream) else []
    return DriverRun(status, output, lines, records, stream, builds, legs,
                     installed, work[0].exists() if work else None)


def caught_plan(prebuilt: bool = True) -> Plan:
    """The run where both controls pass and all four mutants are caught."""
    legs = [LegStep(3.0), LegStep(4.0)]
    legs += [LegStep(5.0 + index, 1, catch_log(identity[3]))
             for index, identity in enumerate(MUTANT_IDENTITY)]
    builds = [BuildStep(10.0)] * (4 if prebuilt else 5)
    return Plan(builds=tuple(builds), legs=tuple(legs), prebuilt=prebuilt)


def phase_shape(records: list[dict]) -> list[tuple]:
    """(event, case, phase, mode) of every record, for an order comparison."""
    return [(rec["event"], rec.get("case"), rec.get("phase"), rec.get("mode"))
            for rec in records]


def expected_shape(prebuilt: bool) -> list[tuple]:
    """The record order one complete run owes: an origin, the baseline note,
    a start/end pair around every call the driver makes, and an end-of-run."""
    shape: list[tuple] = [("origin", None, None, None),
                          ("baseline", "control", None, None)]
    if not prebuilt:
        shape += [(event, "control", "build", None) for event in ("start", "end")]
    for mode in CONTROL_MODES:
        shape += [(event, "control", "simulation", mode)
                  for event in ("start", "end")]
    for case, identity in zip(MUTANT_CASES, MUTANT_IDENTITY):
        shape += [(event, case, "build", None) for event in ("start", "end")]
        shape += [(event, case, "simulation", identity[2])
                  for event in ("start", "end")]
    return shape + [("end-of-run", None, None, None)]


def arm_records_frame_every_call_in_order() -> None:
    """Every existing call is framed, in the order the driver makes them."""
    run = run_driver(caught_plan())
    assert run.status == 0, run.output
    assert phase_shape(run.records) == expected_shape(True), run.records
    assert [rec["seq"] for rec in run.records] == list(range(1, 24))
    assert run.records[0]["clock"] == "monotonic"
    assert run.records[0]["unit"] == "s"


def arm_all_six_outcomes_are_named() -> None:
    """The two control modes and the four mutations are each simulated once,
    under a fixed label, and no case is named twice."""
    run = run_driver(caught_plan())
    simulated = [(rec["case"], rec["mode"]) for rec in run.records
                 if rec["event"] == "start" and rec["phase"] == "simulation"]
    expected = [("control", mode) for mode in CONTROL_MODES]
    expected += [(case, identity[2])
                 for case, identity in zip(MUTANT_CASES, MUTANT_IDENTITY)]
    assert simulated == expected, simulated
    assert len(simulated) == 6, simulated
    built = [rec["case"] for rec in run.records
             if rec["event"] == "start" and rec["phase"] == "build"]
    assert built == list(MUTANT_CASES), built


def arm_durations_are_the_time_each_call_took() -> None:
    """Elapsed time is the time charged to that call, and the offsets rise."""
    plan = caught_plan()
    run = run_driver(plan)
    expected = [plan.legs[0].seconds, plan.legs[1].seconds]
    for index, step in enumerate(plan.builds):
        expected += [step.seconds, plan.legs[2 + index].seconds]
    assert [rec["elapsed_s"] for rec in run.records
            if rec["event"] == "end"] == expected, run.records
    offsets = [rec["t_s"] for rec in run.records]
    assert offsets == sorted(offsets), offsets
    assert offsets[0] == 0.0, offsets
    assert all(rec["idle_s"] == 0.0 for rec in run.records
               if rec["event"] == "start"), run.records


def arm_time_between_phases_is_accounted_separately() -> None:
    """A gap between two phases is its own number, never inside a duration."""
    clock = FakeClock()
    stream = RecordingStream()
    log = driver.PhaseLog(stream=stream, clock=clock)
    clock.advance(2.0)
    log.start("control", "simulation", "--live-only")
    clock.advance(7.0)
    log.end(0)
    clock.advance(0.5)
    log.start("control", "build")
    records = stream.records()
    assert records[1]["idle_s"] == 2.0, records
    assert records[2]["elapsed_s"] == 7.0, records
    assert records[3]["idle_s"] == 0.5, records
    log.finished()
    tail = stream.records()[-1]
    assert tail["state"] == "active" and tail["idle_s"] is None, tail


def arm_every_record_is_flushed_as_it_is_written() -> None:
    """A write is followed by a flush, so a kill cannot hide the last phase."""
    run = run_driver(caught_plan())
    events = run.stream.events
    assert events, events
    assert [kind for kind, _ in events] == ["write", "flush"] * len(run.records)
    assert all(text.endswith("\n") for kind, text in events if kind == "write")
    assert all(text.startswith(driver.PHASE_MARKER + " {")
               for kind, text in events if kind == "write")


def arm_baseline_reuse_and_fallback_are_distinguished() -> None:
    """The controls say whether the built leg was reused or rebuilt, and the
    fallback build carries the frozen arguments."""
    reused = run_driver(caught_plan())
    assert reused.records[1]["selected"] == "prebuilt", reused.records[1]
    assert [call[0] for call in reused.builds] == [
        driver.SOURCES[identity[1]][1] for identity in MUTANT_IDENTITY]
    assert len(reused.builds) == 4, reused.builds

    fell_back = run_driver(caught_plan(prebuilt=False))
    assert fell_back.records[1]["selected"] == "fallback-build", fell_back.records
    assert phase_shape(fell_back.records) == expected_shape(False)
    flag, rtl_path, _, planted = fell_back.builds[0]
    assert (flag, rtl_path) == ("RSP_SRC", driver.STAGE_RTL), fell_back.builds[0]
    assert planted is None, planted
    assert fell_back.status == 0, fell_back.output


def arm_the_frozen_replacement_is_still_what_is_planted() -> None:
    """Each mutation plants its own frozen replacement, once, into a copy."""
    run = run_driver(caught_plan())
    mutant_builds = run.builds
    assert len(mutant_builds) == len(driver.MUTATIONS), mutant_builds
    for (_, source, pattern, replacement, _, _), call in zip(driver.MUTATIONS,
                                                             mutant_builds):
        flag, rtl_path, mdir, planted = call
        original = frozen_source(source)
        assert flag == driver.SOURCES[source][1], call
        assert planted == original.replace(pattern, replacement), rtl_path
        assert planted != original, rtl_path
        assert mdir.name.startswith("obj_"), mdir


def arm_the_driver_prints_exactly_what_it_printed_before() -> None:
    """The verdict lines and the tally are the frozen ones, and diverting the
    records changes not one character of them."""
    run = run_driver(caught_plan())
    assert run.lines == list(CAUGHT_RUN_LINES), run.lines
    quiet = run_driver(caught_plan(), mirror=False)
    assert quiet.lines == run.lines, quiet.lines
    assert quiet.status == run.status
    assert driver.PHASE_MARKER not in quiet.output, quiet.output
    assert run.output.count(driver.PHASE_MARKER) == len(run.records)


def failing_plan() -> Plan:
    """The run where one control fails, one pattern has moved, one mutant will
    not build and one survives: four of the six outcomes are failures."""
    sources = {"stage": frozen_source("stage") + driver.MUTATIONS[0][2] + "\n",
               "datapath": frozen_source("datapath")}
    legs = (LegStep(1.0, 1), LegStep(2.0), LegStep(3.0),
            LegStep(4.0, 1, catch_log(MUTANT_IDENTITY[3][3])))
    return Plan(builds=(BuildStep(5.0, ok=False, returncode=2), BuildStep(6.0),
                        BuildStep(7.0)),
                legs=legs, sources=sources)


def arm_failures_are_reported_exactly_as_before() -> None:
    """A failing control, a pattern that moved, a mutant that will not build
    and a survivor read as they always did, records or no records."""
    run = run_driver(failing_plan())
    quiet = run_driver(failing_plan(), mirror=False)
    assert run.status == 1, run.output
    assert quiet.lines == run.lines, quiet.lines
    assert run.lines[-1] == "6 checks: 2 PASS, 4 FAIL", run.lines
    joined = "\n".join(run.lines)
    assert "a DUT abort is not a catch" in joined, joined
    assert "its pattern appears 2 time(s)" in joined, joined
    assert "did not compile; a mutant that cannot build proves nothing" in joined
    assert "mutant SURVIVED: recentre counted and cleared" in joined, joined
    ends = [rec for rec in run.records if rec["event"] == "end"]
    assert ends[2]["status"] == "no-executable", ends[2]
    assert ends[2]["returncode"] == 2, ends[2]
    assert ends[3]["status"] == "built", ends[3]
    assert ends[3]["returncode"] == 0, ends[3]
    assert [rec["status"] for rec in ends if rec["phase"] == "simulation"] == [
        1, 0, 0, 1], ends


def arm_a_case_with_no_call_contributes_no_record() -> None:
    """A mutation whose pattern moved builds and runs nothing, so it earns no
    phase record at all; its existing failure line is the whole report."""
    sources = {"stage": frozen_source("stage").replace(
        driver.MUTATIONS[0][2], "// the pattern moved"),
        "datapath": frozen_source("datapath")}
    legs = (LegStep(1.0), LegStep(1.0))
    legs += tuple(LegStep(1.0, 1, catch_log(identity[3]))
                  for identity in MUTANT_IDENTITY[1:])
    plan = Plan(builds=(BuildStep(1.0),) * 3, legs=legs, sources=sources)
    run = run_driver(plan)
    assert MUTANT_CASES[0] not in [rec.get("case") for rec in run.records]
    assert run.status == 1, run.output
    assert "its pattern appears 0 time(s)" in "\n".join(run.lines)
    assert run.lines[-1] == "6 checks: 5 PASS, 1 FAIL", run.lines


def arm_records_add_no_check_and_no_failure() -> None:
    """The reader that turns this log into the sweep's numbers sees exactly
    what it saw without the records: no extra tally, no unparsed line, no
    failure, in the passing and in the failing run."""
    for plan, tally in ((caught_plan(), (6, 0)), (failing_plan(), (6, 4))):
        loud = run_driver(plan)
        quiet = run_driver(plan, mirror=False)
        assert scan(loud.output) == scan(quiet.output), loud.output
        checks, failures, matched, unparsed, skipped = scan(loud.output)
        assert (checks, failures) == tally, (checks, failures)
        assert len(matched) == 1 and not unparsed and not skipped, matched
        assert log_reports_failure(loud.output) == log_reports_failure(quiet.output)
        for record_line in [line for line in loud.output.splitlines()
                            if line.startswith(driver.PHASE_MARKER)]:
            assert scan(record_line) == (0, 0, [], [], []), record_line


def arm_a_kill_names_the_phase_and_still_exits_143() -> None:
    """The kill lands inside a named case and phase, that phase is left open
    and unresolved, and the exit and the cleanup are the original ones."""
    plan = caught_plan(prebuilt=False)
    run = run_driver(plan._replace(interrupt_at=1))
    assert run.status == 143, run.output
    last = run.records[-1]
    assert last["event"] == "interrupted", run.records
    assert last["state"] == "active", last
    assert (last["case"], last["phase"], last["mode"]) == (
        "control", "simulation", "--render-only"), last
    assert last["elapsed_s"] == plan.legs[1].seconds, last
    assert last["incomplete"] is True, last
    opened = [rec for rec in run.records
              if rec["event"] == "start" and rec["mode"] == "--render-only"]
    closed = [rec for rec in run.records
              if rec["event"] == "end" and rec["mode"] == "--render-only"]
    assert len(opened) == 1 and not closed, run.records
    assert "--render-only" not in "\n".join(run.lines), run.lines
    assert run.work_exists is False, "the temporary directory outlived the kill"
    assert not [rec for rec in run.records if rec["event"] == "end-of-run"]


def arm_a_kill_between_phases_says_so() -> None:
    """Killed between two phases, the record says idle and how long for."""
    clock = FakeClock()
    stream = RecordingStream()
    log = driver.PhaseLog(stream=stream, clock=clock)
    log.start("control", "build")
    clock.advance(3.0)
    log.end("built")
    clock.advance(1.5)
    log.interrupted()
    last = stream.records()[-1]
    assert last["state"] == "idle", last
    assert last["idle_s"] == 1.5, last
    assert last["case"] is None and last["phase"] is None, last
    log.finished()
    tail = stream.records()[-1]
    assert (tail["event"], tail["state"]) == ("end-of-run", "idle"), tail


def arm_a_kill_on_a_completed_end_record_never_calls_it_active() -> None:
    """Delivered at the one boundary that could contradict the log - a phase's
    end record written and flushed, the driver's next statement not yet run -
    the kill reports the idle the driver is in, and never the phase a reader
    has just seen complete. The exit and the cleanup are the usual ones."""
    installed: list = []
    stream = RecordingStream(kill_at="end", installed=installed)
    run = run_driver(caught_plan(prebuilt=False), stream=stream,
                     installed=installed)
    assert run.status == 143, run.output
    ended = [rec for rec in run.records if rec["event"] == "end"]
    assert len(ended) == 1 and stream.killed_after == ended[0], run.records
    assert (ended[0]["case"], ended[0]["phase"]) == ("control", "build")
    assert (ended[0]["status"], ended[0]["returncode"]) == ("built", 0), ended[0]
    last = run.records[-1]
    assert (last["event"], last["state"]) == ("interrupted", "idle"), last
    assert (last["case"], last["phase"], last["mode"]) == (None, None, None)
    assert "incomplete" not in last and last["seq"] == ended[0]["seq"] + 1, last
    assert run.lines == [] and run.work_exists is False, run.lines


def arm_the_handler_is_installed_for_sigterm() -> None:
    """The driver still arms exactly one handler, on SIGTERM, and that handler
    exits 143 whenever it runs."""
    run = run_driver(caught_plan())
    assert [number for number, _ in run.handlers] == [FakeSignal.SIGTERM]
    try:
        run.handlers[0][1](FakeSignal.SIGTERM, None)
    except SystemExit as stop:
        assert stop.code == 143, stop.code
    else:
        raise AssertionError("the handler did not exit")


def arm_a_record_nobody_can_write_changes_no_outcome() -> None:
    """A record stream that refuses every write loses the diagnostic and
    nothing else: the verdicts, the tally and the exit are untouched."""
    run = run_driver(caught_plan(), stream=BrokenStream())
    assert run.status == 0, run.output
    assert run.lines == list(CAUGHT_RUN_LINES), run.lines
    assert driver.PHASE_MARKER not in run.output, run.output
    killed = run_driver(caught_plan(prebuilt=False)._replace(interrupt_at=1),
                        stream=BrokenStream())
    assert killed.status == 143, killed.output
    assert killed.work_exists is False, "the temporary directory outlived the kill"


def arm_a_clock_that_cannot_be_read_loses_only_the_timing() -> None:
    """A reading the clock refuses is a telemetry loss like a record nobody can
    write. Refused at the origin, every offset is null and the run still
    reports what it always reported. Refused at one start and at the end that
    closes it, those two records and the next gap lose their numbers, and no
    other offset, status or printed line moves. None is ever made up."""
    origin = run_driver(caught_plan(), clock=UnreadableClock(frozenset({1})))
    assert origin.status == 0 and origin.lines == list(CAUGHT_RUN_LINES)
    assert phase_shape(origin.records) == expected_shape(True), origin.records
    assert [rec["seq"] for rec in origin.records] == list(range(1, 24))
    assert all(rec["t_s"] is None for rec in origin.records), origin.records
    assert [(rec["status"], rec["elapsed_s"]) for rec in origin.records
            if rec["event"] == "end"] == [(0, None), (0, None)] + [
        ("built", None), (1, None)] * 4, origin.records

    clean = run_driver(caught_plan())
    broken = run_driver(caught_plan(), clock=UnreadableClock(frozenset({7, 8})))
    assert broken.status == 0 and broken.lines == list(CAUGHT_RUN_LINES)
    assert phase_shape(broken.records) == phase_shape(clean.records)
    assert [index for index, rec in enumerate(broken.records)
            if rec["t_s"] is None] == [6, 7], broken.records
    assert (broken.records[6]["idle_s"], broken.records[7]["elapsed_s"],
            broken.records[8]["idle_s"]) == (None, None, None), broken.records
    assert broken.records[7]["returncode"] == 0, broken.records[7]
    assert broken.records[9]["elapsed_s"] == clean.records[9]["elapsed_s"]
    kept = [(rec.get("status"), rec["t_s"]) for index, rec
            in enumerate(broken.records) if index not in (6, 7)]
    assert kept == [(rec.get("status"), rec["t_s"]) for index, rec
                    in enumerate(clean.records) if index not in (6, 7)], kept


def arm_a_clock_that_fails_under_the_kill_still_exits_143() -> None:
    """The reading the SIGTERM handler takes is telemetry too. Refused from
    that reading on, the kill still names its case and phase, still says
    incomplete, still exits 143 and still leaves the temporary directory
    removed; the two numbers are all that is gone."""
    plan = caught_plan(prebuilt=False)._replace(interrupt_at=1)
    counted = UnreadableClock()
    timed = run_driver(plan, clock=counted)
    assert timed.status == 143, timed.output
    run = run_driver(plan, clock=UnreadableClock(fail_from=counted.reads))
    assert run.status == 143, run.output
    last = run.records[-1]
    assert (last["event"], last["state"]) == ("interrupted", "active"), last
    assert (last["case"], last["phase"], last["mode"]) == (
        "control", "simulation", "--render-only"), last
    assert (last["incomplete"], last["t_s"], last["elapsed_s"]) == (
        True, None, None), last
    assert phase_shape(run.records) == phase_shape(timed.records)
    assert run.work_exists is False, "the temporary directory outlived the kill"


def angry_leg(exe: Path, mode: str) -> tuple[int, str]:
    """A stand-in run_leg() that fails the way an unrunnable leg would."""
    raise OSError("the leg could not be started")


def arm_a_real_failure_still_leaves_the_wrapper() -> None:
    """The instrument contains its own failures and not the driver's: a call
    that raises still raises, through a phase that keeps a start, no end and
    no result, which is what incomplete means."""
    stream = RecordingStream()
    log = driver.PhaseLog(stream=stream, clock=FakeClock())
    with stood_in({"run_leg": angry_leg}):
        try:
            driver.timed_leg(log, "control", Path("obj_aclk"), "--live-only")
        except OSError as failure:
            assert str(failure) == "the leg could not be started", failure
        else:
            raise AssertionError("the instrument swallowed a real failure")
    assert [rec["event"] for rec in stream.records()] == ["origin", "start"]
    log.interrupted()
    last = stream.records()[-1]
    assert (last["state"], last["incomplete"], last["case"], last["phase"]) == (
        "active", True, "control", "simulation"), last


def arm_records_carry_nothing_private() -> None:
    """No path, no environment and no child output reaches a record."""
    plan = caught_plan(prebuilt=False)
    run = run_driver(plan)
    for record in run.records:
        for key, value in record.items():
            assert not isinstance(value, Path), (key, value)
            if isinstance(value, str):
                assert "/" not in value, (key, value)
                assert "FAIL" not in value, (key, value)
    joined = json.dumps(run.records)
    assert str(driver.HERE) not in joined, joined
    assert "was not restored" not in joined, joined


def arm_the_build_command_is_unchanged_and_its_status_recorded() -> None:
    """build() still runs the suite's own recipe, with the same arguments in
    the same order, captures both streams, returns the leg or nothing and
    prints the tails of a failure. Its framed record keeps both halves of the
    answer: `returncode`, the status the recipe returned and this helper does
    see, and `status`, whether a leg came out of it."""
    #: (recipe status, leaves a leg, override, `status`, what build() prints):
    #: returning 0 with no leg, and returning 2, are the two failures `status`
    #: on its own reports identically
    cases = ((0, True, "RSP_SRC", "built", ""),
             (0, False, "DP_SRC", "no-executable", "out-tailerr-tail"),
             (2, True, "RSP_SRC", "no-executable", "out-tailerr-tail"))
    with tempfile.TemporaryDirectory(prefix="a115-fixture-") as td:
        root = Path(td)
        source = root / "stage_copy.sv"
        for index, (status, leg, override, label, tails) in enumerate(cases):
            mdir = root / f"obj_case{index}"
            mdir.mkdir()
            if leg:
                (mdir / "Vmilan_dp_aclk").write_text("stand-in leg\n")
            stream = RecordingStream()
            printed = io.StringIO()
            log = driver.PhaseLog(stream=stream, clock=FakeClock())
            recorder = RecordingSubprocess(
                FakeCompleted(status, "out-tail", "err-tail"))
            with stood_in({"subprocess": recorder}), \
                    contextlib.redirect_stdout(printed):
                exe = driver.timed_build(log, "control", override, source, mdir)
            argv, kwargs = recorder.calls[0]
            assert argv == ("make", "-s", "-C", str(driver.HERE), "aclk-build",
                            f"{override}={source}", f"ACLK_MDIR={mdir}"), argv
            assert kwargs == {"capture_output": True, "text": True}, kwargs
            assert exe == (mdir / "Vmilan_dp_aclk" if label == "built"
                           else None), (exe, label)
            assert printed.getvalue() == tails, printed.getvalue()
            record = stream.records()[-1]
            assert (record["event"], record["phase"]) == ("end", "build"), record
            assert (record["status"], record["returncode"]) == (label, status), record


def arm_the_leg_command_and_session_are_unchanged() -> None:
    """run_leg() still launches the leg with the same argument, working
    directory, captured streams and its own session, and still kills the
    process group of a child that outlives the wait."""
    exe = Path("obj_case") / "Vmilan_dp_aclk"
    finished = RecordingSubprocess(FakeProc(0, "leg log\n"))
    with stood_in({"subprocess": finished}):
        status, out = driver.run_leg(exe, "--render-only")
    argv, kwargs = finished.calls[0]
    assert argv == (str(exe), "--render-only"), argv
    assert kwargs == {"cwd": str(driver.HERE), "stdout": RecordingSubprocess.PIPE,
                      "stderr": RecordingSubprocess.STDOUT, "text": True,
                      "start_new_session": True}, kwargs
    assert (status, out) == (0, "leg log\n"), (status, out)

    child = FakeProc(-9, "", running=True)
    killer = FakeOs()
    with stood_in({"subprocess": RecordingSubprocess(child), "os": killer}):
        driver.run_leg(exe, "--live-only")
    assert killer.killed == [(FakeProc.pid + 1000, driver.signal.SIGKILL)]
    assert child.waited, "the killed child was not waited for"


def arm_the_six_case_inventory_is_frozen() -> None:
    """Four mutations, two sources, two short modes, and the named check each
    defect must break, exactly as the arm was written."""
    identity = [(name, source, mode, breaks)
                for name, source, _, _, mode, breaks in driver.MUTATIONS]
    assert identity == list(MUTANT_IDENTITY), identity
    assert sorted({m[4] for m in driver.MUTATIONS}) == sorted(CONTROL_MODES)
    assert len(driver.MUTATIONS) + len(CONTROL_MODES) == 6
    assert {key: flag for key, (_, flag) in driver.SOURCES.items()} == {
        "stage": "RSP_SRC", "datapath": "DP_SRC"}
    for _, source, pattern, replacement, _, _ in driver.MUTATIONS:
        assert source in driver.SOURCES, source
        assert pattern and replacement and pattern != replacement, pattern


def arm_the_verdict_classifier_is_unchanged() -> None:
    """Every branch of the classifier still answers what it always answered."""
    named = MUTANT_IDENTITY[0][3]
    assert driver.verdict(0, "", None) == "pass"
    assert driver.verdict(1, catch_log(named), named) == "caught"
    assert driver.verdict(1, catch_log(named), "other check").startswith(
        "failed, but not the named check")
    assert driver.verdict(0, catch_log(named), None).startswith("exited 0 but")
    assert driver.verdict(-11, "", None) == (
        "died by signal 11 with no harness verdict - a crash is not a catch")
    assert driver.verdict(3, "", None) == (
        "exited 3 with no harness verdict - a DUT abort is not a catch")


ARMS = (
    arm_records_frame_every_call_in_order,
    arm_all_six_outcomes_are_named,
    arm_durations_are_the_time_each_call_took,
    arm_time_between_phases_is_accounted_separately,
    arm_every_record_is_flushed_as_it_is_written,
    arm_baseline_reuse_and_fallback_are_distinguished,
    arm_the_frozen_replacement_is_still_what_is_planted,
    arm_the_driver_prints_exactly_what_it_printed_before,
    arm_failures_are_reported_exactly_as_before,
    arm_a_case_with_no_call_contributes_no_record,
    arm_records_add_no_check_and_no_failure,
    arm_a_kill_names_the_phase_and_still_exits_143,
    arm_a_kill_between_phases_says_so,
    arm_a_kill_on_a_completed_end_record_never_calls_it_active,
    arm_the_handler_is_installed_for_sigterm,
    arm_a_record_nobody_can_write_changes_no_outcome,
    arm_a_clock_that_cannot_be_read_loses_only_the_timing,
    arm_a_clock_that_fails_under_the_kill_still_exits_143,
    arm_a_real_failure_still_leaves_the_wrapper,
    arm_records_carry_nothing_private,
    arm_the_build_command_is_unchanged_and_its_status_recorded,
    arm_the_leg_command_and_session_are_unchanged,
    arm_the_six_case_inventory_is_frozen,
    arm_the_verdict_classifier_is_unchanged,
)


def main() -> int:
    """Run every arm; 1 if any of them failed."""
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
