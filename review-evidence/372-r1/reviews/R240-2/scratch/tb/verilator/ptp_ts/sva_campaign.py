#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Detection campaign for the checker bound to axis_mux_rr_2in_1out (#372).

Why this exists. An assertion that has never been seen to fail cannot be told
apart from one that cannot fail (Rule 8, docs/development/CODE_QUALITY.md).
The suite's positive leg, `make mux-sva`, shows the checker is bound, enabled
and exercised. This script shows that every property it claims fails, by its
own name, on a defect it exists for, and that the check deciding "detected"
itself fails once the checker is disabled or unbound.

Six kinds of row, each graded on its own:

  clean       the suite's own two builds, run exactly as a mutant is run: they
              must pass with no assertion failing.
  stimulus    a clean build with one source rule broken on purpose
              (+stimulus_fault=): the named u_s<N>_stimulus property must stop
              the run.
  mutant      a scratch copy of the product mux with one span rewritten
              (MUTATIONS). It must build, and the named property must be among
              the assertions failing at the first failing edge.
  scoreboard  one rewrite that no property covers (round-robin order): the
              harness's own scoreboard must fail, and no assertion may.
  elaboration the checker built at a TDATA width that is not whole bytes:
              gen_guard_tdata_width must refuse it with its own message. The
              clean rows are its legal counterpart.
  coverage    the clean mux with its checker unable to vouch for it: built
              with --no-assert, with a mistyped bind target (pinned Verilator
              5.050 builds both without a word), with s0 and s1 swapped in the
              bind, and run on one scenario that never stalls the output. The
              harness must refuse each positive run by its own scope or
              witness check, no assertion firing, and every stimulus fault
              must be injected and go UNDETECTED: the detection check has to
              fail here, or it could pass without the checker.

"Detected" means all of: the build succeeded; the fault was injected (stimulus
rows); the harness exited 3, its assertion stop; and an `Assertion failed in
<path>` line names the expected property. A compile failure, a crash, a
watchdog, a usage error or a scoreboard verdict is not a detection. Runs raise
+verilator+error+limit+ so every assertion failing at the first failing edge
is reported before the harness stops at that edge. The harness bounds every
run in DUT cycles, so nothing here needs a wall clock.

Expected failures stay out of the suite log. Every build and run log is kept
under obj_dir_sva_campaign/<row>/, and this script prints one verdict line per
row and the tally. A row that did NOT behave as required prints [FAIL].

Usage: python3 sva_campaign.py [--verilator PATH] [--only ROW] [--list]
Exit 0 when every row behaved as required, 1 when one did not, 2 on bad usage.
"""

import argparse
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
#: The product module, read and rewritten only into scratch copies under WORK.
DUT = (HERE / "../../../hdl/common/axis_mux_rr_2in_1out.sv").resolve()
BIND = (HERE / "../../common/sva/axis_mux_rr_2in_1out_bind.sv").resolve()
WORK = HERE / "obj_dir_sva_campaign"
CHECKER = "TOP.axis_mux_rr_2in_1out.u_sva"
EXIT_ASSERTION_STOP = 3
ERROR_LIMIT = "+verilator+error+limit+1000"
FAILED_LINE = re.compile(r"Assertion failed in ([\w.$]+):")
INJECTED = "stimulus fault injected"
SCOPE_REFUSAL = "is elaborated with its assertions"

sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import FAIL_MARKER  # noqa: E402


class Mutation(NamedTuple):
    """One rewrite of the product mux and the verdict it must draw."""

    name: str
    width: int
    pattern: str
    replacement: str
    scenario: str
    expect: str
    why: str


#: One row per claimed DUT property, plus one row for the scoreboard (`expect`
#: empty). Each `pattern` must appear in the pristine mux EXACTLY ONCE, or the
#: row fails instead of quietly mutating nothing.
MUTATIONS = (
    Mutation("tvalid_waits_for_tready", 64,
             "m_tvalid = s0_tvalid;", "m_tvalid = s0_tvalid && m_tready;",
             "backpressure_mid_packet", "forwarding_laws.ai_tvalid_forwarded",
             "the defect the mux's own comment records: TVALID made to wait for TREADY"),
    Mutation("tdata_hidden_while_stalled", 8,
             "m_tdata  = s1_tdata;", "m_tdata  = s1_tdata & {TDATA_WIDTH{m_tready}};",
             "backpressure_mid_packet", "u_m_dut.ap_tdata_stable_until_handshake",
             "the output TDATA is gated by TREADY, so it moves while stalled"),
    Mutation("tkeep_hidden_while_stalled", 64,
             "m_tkeep  = s0_tkeep;", "m_tkeep  = s0_tkeep & {(TDATA_WIDTH/8){m_tready}};",
             "backpressure_mid_packet", "u_m_dut.ap_tkeep_stable_until_handshake",
             "the output TKEEP is gated by TREADY, so it moves while stalled"),
    Mutation("tlast_hidden_while_stalled", 8,
             "m_tlast  = s1_tlast;", "m_tlast  = s1_tlast && m_tready;",
             "backpressure_last_beat", "u_m_dut.ap_tlast_stable_until_handshake",
             "the output TLAST is gated by TREADY, so it rises only at the handshake"),
    Mutation("released_while_tlast_stalled", 64,
             "if (s0_tvalid && s0_tlast && m_tready)", "if (s0_tvalid && s0_tlast)",
             "backpressure_last_beat", "u_m_dut.ap_tvalid_held_until_handshake",
             "s0 gives up the output on a TLAST beat the sink has not taken"),
    Mutation("released_before_tlast_s0", 8,
             "if (s0_tvalid && s0_tlast && m_tready)", "if (s0_tvalid && m_tready)",
             "multi_beats", "ap_owner_held_until_tlast_handshake",
             "s0 gives up the output after any beat, not after its TLAST beat"),
    Mutation("released_before_tlast_s1", 64,
             "if (s1_tvalid && s1_tlast && m_tready)", "if (s1_tvalid && m_tready)",
             "multi_beats", "ap_owner_held_until_tlast_handshake",
             "s1 gives up the output after any beat, not after its TLAST beat"),
    Mutation("kept_after_tlast", 8,
             "if (s1_tvalid && s1_tlast && m_tready)\n          next_state = IDLE;",
             "if (s1_tvalid && s1_tlast && m_tready)\n          next_state = STREAM_1;",
             "single_beats", "ap_owner_released_after_tlast",
             "s1 keeps the output after its TLAST beat"),
    Mutation("reset_ignored", 64,
             "if (!rst_n)\n      state <= IDLE;", "if (1'b0)\n      state <= IDLE;",
             "reset_while_stalled", "ap_reset_releases_owner",
             "the state register ignores reset, so an owner survives it"),
    Mutation("illegal_state_reached", 64,
             "if (!last_served) begin\n          if (s1_tvalid)\n            next_state = STREAM_1;",
             "if (!last_served) begin\n          if (s1_tvalid)\n            next_state = state_t'(2'b11);",
             "single_beats", "ap_state_legal",
             "a grant decodes to the encoding no state name owns"),
    Mutation("granted_without_request", 8,
             "if (!last_served) begin\n          if (s1_tvalid)",
             "if (!last_served) begin\n          if (1'b1)",
             "single_beats", "ap_grant_only_to_requester",
             "the arbiter grants s1 whether or not it offers a beat"),
    Mutation("both_sources_ready", 64,
             "assign s1_tready = (state == STREAM_1) && m_tready;",
             "assign s1_tready = (state != IDLE) && m_tready;",
             "single_beats", "forwarding_laws.ai_grants_mutually_exclusive",
             "s1 also sees TREADY while s0 owns the output"),
    Mutation("ready_ignores_sink", 8,
             "assign s0_tready = (state == STREAM_0) && m_tready;",
             "assign s0_tready = (state == STREAM_0);",
             "backpressure_mid_packet", "forwarding_laws.ai_ready_only_for_owner_and_ready_sink",
             "s0 sees TREADY while the sink is stalling the output"),
    Mutation("tkeep_from_other_source", 64,
             "m_tkeep  = s1_tkeep;", "m_tkeep  = s0_tkeep;",
             "multi_beats", "forwarding_laws.ai_payload_forwarded_on_transfer",
             "an s1 beat leaves with s0's TKEEP"),
    Mutation("round_robin_inverted", 8,
             "last_served <= (state == STREAM_0) ? 1'b0 : 1'b1;",
             "last_served <= (state == STREAM_0) ? 1'b1 : 1'b0;",
             "simultaneous_offers", "",
             "the arbiter prefers the source it just served; no property claims fairness, "
             "so the scoreboard must catch it"),
)

#: The four source rules, the +stimulus_fault= that breaks each, and the scenario
#: whose first stall of each port is an arbitration wait, so the fault is not
#: forwarded to m and only the stimulus property can fire.
STIMULUS_FAULTS = (
    ("drop_tvalid", "ap_tvalid_held_until_handshake"),
    ("flip_tdata", "ap_tdata_stable_until_handshake"),
    ("flip_tkeep", "ap_tkeep_stable_until_handshake"),
    ("flip_tlast", "ap_tlast_stable_until_handshake"),
)
FAULT_SCENARIO = "single_beats"
SCOREBOARD_FAILURE = "alternate packet by packet"
#: A shape the checker must refuse at elaboration, and the message it must say.
GUARD_WIDTH = 12
GUARD_MESSAGE = (f"axis_stream_source_sva: TDATA_WIDTH_P={GUARD_WIDTH} is not a whole, "
                 "non-zero number of bytes")
GUARD_ROW = f"elaboration-tdata_width_{GUARD_WIDTH}"


class CoverageControl(NamedTuple):
    """The CLEAN mux, built or run so that its checker cannot vouch for it:
    absent, disabled, wired to the wrong port, or never exercised."""

    name: str
    width: int
    rebuild: bool
    assert_flag: str
    bind_rewrites: tuple[tuple[str, str, int], ...]
    run_plusargs: tuple[str, ...]
    refusal: str
    with_faults: bool
    why: str


#: (pattern, replacement, occurrences): mirror s0 and s1 in the bind, the
#: connections and the ownership flags alike, so every law still holds and
#: only the per-port witness counts can tell the checker is miswired.
SWAP_PORTS = (
    ("(s0_", "(sX_", 5), ("(s1_", "(s0_", 5), ("(sX_", "(s1_", 5),
    ("(state == STREAM_0)", "(state == STREAM_X)", 1),
    ("(state == STREAM_1)", "(state == STREAM_0)", 1),
    ("(state == STREAM_X)", "(state == STREAM_1)", 1),
)

COVERAGE_CONTROLS = (
    CoverageControl("assertions_disabled", 64, True, "--no-assert", (), (), SCOPE_REFUSAL, True,
                    "--no-assert compiles every assertion, and every witness with it, out of a bound checker"),
    CoverageControl("bind_target_mistyped", 8, True, "--assert",
                    (("bind axis_mux_rr_2in_1out ", "bind axis_mux_rr_2in_1out_mistyped ", 1),), (),
                    SCOPE_REFUSAL, True,
                    "a bind naming a module that does not exist binds nothing, and 5.050 builds it silently"),
    CoverageControl("bind_ports_swapped", 64, True, "--assert", SWAP_PORTS, (),
                    f"witness {CHECKER}.u_s0_stimulus.", True,
                    "a checker wired to the wrong ports still sees legal traffic; only the witness "
                    "counts the harness takes from the ports can tell"),
    CoverageControl("unused_path", 8, False, "--assert", (), ("+scenario=single_beats", "+grade_witnesses"),
                    f"witness {CHECKER}.u_m_dut.", False,
                    "single_beats never stalls the output, so every u_m_dut property passes vacuously"),
)


class Shape(NamedTuple):
    """Everything `make mux-sva-build` is told about one build."""

    width: int
    dut: Path
    bind: Path
    assert_flag: str


class Verdict(NamedTuple):
    """Whether a row behaved as required, and the evidence line for it."""

    ok: bool
    text: str


#: Which rows to run, by name; a row that is not wanted does no work at all.
Wanted = Callable[[str], bool]


def clean_binary(width: int) -> Path:
    """The suite's own build at `width`, made by `make mux-sva`."""
    return HERE / f"obj_dir_mux_sva_w{width}" / "Vmux_sva"


def build(row: Path, shape: Shape, verilator: str) -> Path | None:
    """Build `shape` through the Makefile's one recipe; the binary, or None.

    The build log stays in `row`. A build that fails is reported by the row
    as a build failure, never as a detection.
    """
    obj = row / "obj"
    command = ["make", "--no-print-directory", "-C", str(HERE), "mux-sva-build",
               f"VERILATOR={verilator}", f"MUX_SVA_WIDTH={shape.width}", f"MUX_SVA_OBJ={obj}",
               f"MUX_SVA_DUT={shape.dut}", f"MUX_SVA_BIND={shape.bind}",
               f"MUX_SVA_ASSERT={shape.assert_flag}"]
    with (row / "build.log").open("w") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
    binary = obj / "Vmux_sva"
    return binary if result.returncode == 0 and binary.is_file() else None


def run_harness(binary: Path, log_path: Path, plusargs: list[str]) -> tuple[int, str]:
    """(exit status, log text) of one harness run; the log stays at `log_path`."""
    with log_path.open("w") as log:
        result = subprocess.run([str(binary), *plusargs], stdout=log, stderr=subprocess.STDOUT,
                                check=False)
    return result.returncode, log_path.read_text(errors="replace")


def fired(text: str) -> list[str]:
    """The distinct assertion paths a run reported failing, in order."""
    paths: list[str] = []
    for match in FAILED_LINE.finditer(text):
        if match.group(1) not in paths:
            paths.append(match.group(1))
    return paths


def fail_lines(text: str) -> list[str]:
    """The harness's own failed checks, found with the sweep's [FAIL] marker
    and quoted without it, so this script's log carries no [FAIL] of its own
    for a failure the row expected."""
    return [FAIL_MARKER.sub("", line).strip() for line in text.splitlines() if FAIL_MARKER.match(line)]


def detection(status: int, text: str, expect: str) -> Verdict:
    """Did the named property stop this run? The one rule every row uses."""
    paths = fired(text)
    target = f"{CHECKER}.{expect}"
    if status != EXIT_ASSERTION_STOP:
        return Verdict(False, f"exit {status}, not the assertion stop {EXIT_ASSERTION_STOP}; "
                              f"properties named: {', '.join(paths) or 'none'}")
    if target not in paths:
        return Verdict(False, f"stopped, but by {', '.join(paths) or 'nothing named'}")
    others = [path.removeprefix(CHECKER + ".") for path in paths if path != target]
    also = f"; the same edge also failed {', '.join(others)}" if others else ""
    return Verdict(True, f"stopped by {expect}{also}")


def row_dir(name: str) -> Path:
    """A fresh directory for one row's logs and scratch sources."""
    path = WORK / name
    path.mkdir(parents=True)
    return path


def clean_rows(wanted: Wanted) -> Iterator[tuple[str, Verdict]]:
    """The suite's own builds must pass when run the way mutants are run."""
    for width in (8, 64):
        name = f"clean-w{width}"
        if not wanted(name):
            continue
        binary = clean_binary(width)
        if not binary.is_file():
            yield name, Verdict(False, f"{binary.name} is missing; `make mux-sva` builds it")
            continue
        status, text = run_harness(binary, row_dir(name) / "run.log", [ERROR_LIMIT])
        ok = status == 0 and not fired(text) and not fail_lines(text)
        yield name, Verdict(ok, "passes, no property fails" if ok
                            else f"exit {status}, failing: {fired(text) or fail_lines(text)[:1]}")


def stimulus_rows(wanted: Wanted) -> Iterator[tuple[str, Verdict]]:
    """Each source rule, broken on each port at each width, must be named."""
    for width in (8, 64):
        binary = clean_binary(width)
        for port in (0, 1):
            for fault, rule in STIMULUS_FAULTS:
                name = f"stimulus-s{port}_{fault}-w{width}"
                if not wanted(name):
                    continue
                if not binary.is_file():
                    yield name, Verdict(False, f"{binary.name} is missing; `make mux-sva` builds it")
                    continue
                status, text = run_harness(binary, row_dir(name) / "run.log",
                                           [ERROR_LIMIT, f"+scenario={FAULT_SCENARIO}",
                                            f"+stimulus_fault=s{port}_{fault}"])
                verdict = detection(status, text, f"u_s{port}_stimulus.{rule}")
                if INJECTED not in text:
                    verdict = Verdict(False, "the fault was never injected")
                yield name, verdict


def mutant_source(row: Path, pristine: str, mutation: Mutation) -> Path | None:
    """Write the mutated scratch copy; None when the pattern is not unique."""
    if pristine.count(mutation.pattern) != 1:
        return None
    scratch = row / DUT.name
    scratch.write_text(pristine.replace(mutation.pattern, mutation.replacement))
    return scratch


def scoreboard_verdict(status: int, text: str) -> Verdict:
    """The scoreboard row: the harness's own verdict, and no property."""
    if fired(text):
        return Verdict(False, f"a property fired ({', '.join(fired(text))}); this row is the scoreboard's")
    caught = [line for line in fail_lines(text) if SCOREBOARD_FAILURE in line]
    if status != 1 or not caught:
        return Verdict(False, f"exit {status} without the scoreboard's '{SCOREBOARD_FAILURE}' failure")
    return Verdict(True, f"no property fails; the scoreboard's check does: {caught[0]}")


def mutation_row_name(mutation: Mutation) -> str:
    """A mutant row, or the scoreboard row when no property is expected."""
    kind = "mutant" if mutation.expect else "scoreboard"
    return f"{kind}-{mutation.name}-w{mutation.width}"


def mutant_rows(verilator: str, wanted: Wanted) -> Iterator[tuple[str, Verdict]]:
    """Each DUT property must name the mutant written against it."""
    pristine = DUT.read_text()
    for mutation in MUTATIONS:
        name = mutation_row_name(mutation)
        if not wanted(name):
            continue
        row = row_dir(name)
        source = mutant_source(row, pristine, mutation)
        if source is None:
            yield name, Verdict(False, f"its pattern appears {pristine.count(mutation.pattern)} times, "
                                       "not once: the mux moved, so fix the pattern, not the row")
            continue
        binary = build(row, Shape(mutation.width, source, BIND, "--assert"), verilator)
        if binary is None:
            yield name, Verdict(False, "did not build: a compile failure is not a detection")
            continue
        status, text = run_harness(binary, row / "run.log",
                                   [ERROR_LIMIT, f"+scenario={mutation.scenario}"])
        yield name, (detection(status, text, mutation.expect) if mutation.expect
                     else scoreboard_verdict(status, text))


def guard_rows(verilator: str, wanted: Wanted) -> Iterator[tuple[str, Verdict]]:
    """The checker's elaboration guard must refuse a width that is not whole
    bytes, by its own diagnostic rather than by some other build failure."""
    if not wanted(GUARD_ROW):
        return
    row = row_dir(GUARD_ROW)
    binary = build(row, Shape(GUARD_WIDTH, DUT, BIND, "--assert"), verilator)
    log = (row / "build.log").read_text(errors="replace")
    if binary is not None:
        yield GUARD_ROW, Verdict(False, "it built: the checker accepted a width that is not whole bytes")
    elif GUARD_MESSAGE not in log:
        yield GUARD_ROW, Verdict(False, "the build failed, but not with gen_guard_tdata_width's message")
    else:
        yield GUARD_ROW, Verdict(True, f"refused at elaboration by its own message: '{GUARD_MESSAGE}'")


def coverage_binary(row: Path, control: CoverageControl, verilator: str) -> Path | None:
    """The binary `control` runs: the clean build, or the clean mux rebuilt
    the way the control loses its checker. None when it cannot be made, or
    when a bind rewrite no longer matches exactly as often as it should."""
    if not control.rebuild:
        binary = clean_binary(control.width)
        return binary if binary.is_file() else None
    bind = BIND
    if control.bind_rewrites:
        text = BIND.read_text()
        for pattern, replacement, occurrences in control.bind_rewrites:
            if text.count(pattern) != occurrences:
                return None
            text = text.replace(pattern, replacement)
        bind = row / BIND.name
        bind.write_text(text)
    return build(row, Shape(control.width, DUT, bind, control.assert_flag), verilator)


def coverage_names(control: CoverageControl) -> list[str]:
    """The control's own row, then one row per stimulus fault run on it."""
    name = f"coverage-{control.name}-w{control.width}"
    if not control.with_faults:
        return [name]
    return [name] + [f"{name}-s{port}_{fault}" for port in (0, 1) for fault, _rule in STIMULUS_FAULTS]


def refusal_verdict(control: CoverageControl, status: int, text: str) -> Verdict:
    """The control's positive run must fail on the harness's own check, the
    one the control is about, with no assertion firing."""
    refused = [line for line in fail_lines(text) if control.refusal in line]
    if fired(text):
        return Verdict(False, f"a property fired ({', '.join(fired(text))}); the refusal must be the harness's")
    if status != 1 or not refused:
        return Verdict(False, f"exit {status} and no '{control.refusal}' failure: lost coverage went unnoticed")
    how = "rebuilt" if control.rebuild else "the clean build"
    return Verdict(True, f"{how}; the harness refuses the run, failing '{refused[0]}'")


def coverage_rows(verilator: str, wanted: Wanted) -> Iterator[tuple[str, Verdict]]:
    """Without the checker in force, the harness must refuse to pass and the
    detection check must fail for every injected fault."""
    for control in COVERAGE_CONTROLS:
        if not any(wanted(row_name) for row_name in coverage_names(control)):
            continue
        name = coverage_names(control)[0]
        row = row_dir(name)
        binary = coverage_binary(row, control, verilator)
        if binary is None:
            yield name, Verdict(False, "could not be built or found; the control must run to show anything")
            continue
        status, text = run_harness(binary, row / "run.log", list(control.run_plusargs))
        yield name, refusal_verdict(control, status, text)
        if not control.with_faults:
            continue
        for port in (0, 1):
            for fault, rule in STIMULUS_FAULTS:
                fault_name = f"{name}-s{port}_{fault}"
                status, text = run_harness(binary, row / f"run-s{port}_{fault}.log",
                                           [ERROR_LIMIT, f"+scenario={FAULT_SCENARIO}",
                                            f"+stimulus_fault=s{port}_{fault}"])
                verdict = detection(status, text, f"u_s{port}_stimulus.{rule}")
                if INJECTED not in text:
                    yield fault_name, Verdict(False, "the fault was never injected, so its "
                                                     "non-detection shows nothing")
                elif verdict.ok:
                    yield fault_name, Verdict(False, f"DETECTED without the checker: {verdict.text}")
                else:
                    yield fault_name, Verdict(True, f"injected, not detected ({verdict.text}): "
                                                    "the detection check fails, as it must")


def tool_identity(verilator: str) -> str:
    """The first line `verilator --version` prints, for the log."""
    result = subprocess.run([verilator, "--version"], capture_output=True, text=True, check=False)
    lines = result.stdout.strip().splitlines()
    return lines[0] if result.returncode == 0 and lines else f"`{verilator} --version` failed"


def all_rows(verilator: str, wanted: Wanted) -> Iterator[tuple[str, Verdict]]:
    """Every wanted row, in the order the module docstring describes them.
    A coverage control yields its fault rows too; the caller filters them."""
    yield from clean_rows(wanted)
    yield from stimulus_rows(wanted)
    yield from mutant_rows(verilator, wanted)
    yield from guard_rows(verilator, wanted)
    yield from coverage_rows(verilator, wanted)


def row_names() -> list[str]:
    """Every row name, for --list, without building or running anything."""
    names = [f"clean-w{width}" for width in (8, 64)]
    names += [f"stimulus-s{port}_{fault}-w{width}" for width in (8, 64) for port in (0, 1)
              for fault, _rule in STIMULUS_FAULTS]
    names += [mutation_row_name(mutation) for mutation in MUTATIONS]
    names.append(GUARD_ROW)
    for control in COVERAGE_CONTROLS:
        names += coverage_names(control)
    return names


def row_notes() -> dict[str, str]:
    """Why each mutant and control row exists, keyed by row name, for --list."""
    notes = {mutation_row_name(mutation): mutation.why for mutation in MUTATIONS}
    notes[GUARD_ROW] = "gen_guard_tdata_width must refuse a TDATA width that is not whole bytes"
    notes.update({coverage_names(control)[0]: control.why for control in COVERAGE_CONTROLS})
    return notes


def main() -> int:
    """Run the campaign and print one verdict per row and the tally."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verilator", default="verilator", help="the Verilator the suite builds with")
    parser.add_argument("--only", help="run the rows whose name starts with this prefix")
    parser.add_argument("--list", action="store_true", help="print the row names and exit")
    args = parser.parse_args()
    if args.list:
        notes = row_notes()
        for name in row_names():
            print(f"{name}: {notes[name]}" if name in notes else name)
        return 0
    if args.only and not any(name.startswith(args.only) for name in row_names()):
        print(f"no row starts with {args.only!r}; --list prints them", file=sys.stderr)
        return 2
    shutil.rmtree(WORK, ignore_errors=True)
    WORK.mkdir()
    print(f"sva campaign: {tool_identity(args.verilator)}; raw logs in {WORK.relative_to(HERE)}/")
    def wanted(name: str) -> bool:
        """Every row, or the rows --only names by prefix."""
        return not args.only or name.startswith(args.only)

    checks = failures = 0
    for name, verdict in all_rows(args.verilator, wanted):
        if not wanted(name):
            continue
        checks += 1
        failures += 0 if verdict.ok else 1
        print(f"  [{'PASS' if verdict.ok else 'FAIL'}] {name}: {verdict.text}")
    print(f"== ptp_ts sva campaign: checks: {checks}   failures: {failures} ==")
    return 1 if failures or not checks else 0


if __name__ == "__main__":
    sys.exit(main())
