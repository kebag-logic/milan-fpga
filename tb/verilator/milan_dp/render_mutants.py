#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #386 render law in milan_dp: prove the checks can fail.

sim_aclk.cpp asserts, on the elaborated shipping shape, that every accepted
PDU's first event renders SETPOINT media ticks after its accept, that a PHC
step recentres the fill once (from a short queue and from a long one), and
that a clock-source change under the running stream recentres it once the
grid has settled. Issue #386's acceptance asks for the negative controls by
name: a deliberately wrong prefill must fail the law check, and a disabled
recentre must fail the recentre check; the round-5 review added the recentre
that counts but does not snap, and the clock-source trigger. So the real
KL_render_setpoint, or the real milan_datapath, is mutated, one defect at a
time, and the SAME leg is rebuilt through the Makefile's own recipe (`make
aclk-build` with RSP_SRC or DP_SRC, and ACLK_MDIR, overridden) and run in
the short mode that holds the check: `--render-only` for the stage's
defects, `--live-only` for the datapath's trigger. Each mutant must make the
leg FAIL by its OWN verdict (a `[FAIL]` line or a tally with failures, read
by scripts/suite_tally.py), and the named check must be among the failures;
a crash or an abort is not a catch. The positive control is the clean leg
the sweep just ran (obj_aclk): it is re-run here in both short modes so the
verdicts come from the same binary shape.

What bounds a livelocking mutant. This driver sets no host-time deadline
on a run (rule 8's wall-clock ratchet, scripts/test_evidence.budget item
4). Both short legs of sim_aclk.cpp are cycle-bounded by construction, not
by a cap constant: each steps a fixed count out of reset, binds listener 0
through fixed step loops and an AXI4-Lite BFM whose every handshake gives
up after kAxiGuardCycles (2048 cycles), injects each frame through inject()
(at most 1500 cycles), and runs its windows through run_fed (a fixed cycle
target each; the feed's slot-boundary wait is bounded by the PDU period);
no loop on either path waits on a DUT output without a cycle bound, so a
leg ends at the same cycle whatever the mutated gateware does. The
host-time bound is the sweep's: scripts/run_all_suites.sh runs this suite's
`make` (whose `run` recipe ends with `python3 render_mutants.py`) under its
per-suite guard, suite_timeout = 3600 s (decision 5820240308), and reports a kill as TIMEOUT, an
UNKNOWN result (exit 92), never a pass or a fail. The SIGTERM handler in
main() turns that kill into an exit that removes the temporary directory
and the leg's own process group. Run by hand, outside the sweep, nothing
but the cycle bound limits a run.

What the RENDER-PHASE records are, and are not (#445). Around each build and
each short-mode run this driver already makes, it prints one flushed JSON
line naming the case, the phase, a sequence number and an offset in seconds
from one origin taken when the run starts, so a reader can tell which case
and phase a kill landed in and how long the completed phases took. Five of
six results and no phase timing is what left the last case unattributable.
The clock is monotonic and read for observation only: it is injected, no
argument, status, wait, tally or printed verdict depends on it, and this
driver still sets no host-time deadline on a run (rule 8's wall-clock
ratchet, scripts/test_evidence.budget item 4). A phase with a start and no
end is incomplete and earns no result; a reading the clock would not give,
and a record that cannot be written, are gaps in the diagnostic - a null
where a number would have been, never a changed outcome. The records carry
no path, no environment and no child output, and their wording matches none
of the tally shapes scripts/suite_tally.py reads, so they add no check and
no verdict. README.md documents the fields and the limits.

Usage: python3 render_mutants.py      (run from tb/verilator/milan_dp)
Exit 0 = every mutant was caught and the clean leg still passes.
"""

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from pathlib import Path
from typing import TextIO

HERE = Path(__file__).resolve().parent
STAGE_RTL = HERE / "../../../hdl/ieee1722/aaf/KL_render_setpoint.sv"
DP_RTL = HERE / "../../../hdl/milan/milan_datapath.sv"
CLEAN_EXE = HERE / "obj_aclk/Vmilan_dp_aclk"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the two sources a mutant may plant into: (path, the Makefile override)
SOURCES = {
    "stage": (STAGE_RTL, "RSP_SRC"),
    "datapath": (DP_RTL, "DP_SRC"),
}

#: (name, source, pattern, replacement, the leg's short mode, the check this
#: defect must break)
MUTATIONS = [
    ("prefill target three events high", "stage",
     "localparam int unsigned TARGET_C = SETPOINT_EVT_P + PDU_EVENTS_P;",
     "localparam int unsigned TARGET_C = SETPOINT_EVT_P + PDU_EVENTS_P + 3;",
     "--render-only",
     "RENDER-INT: every PDU's first event inside the law band"),
    ("recentre pulse ignored", "stage",
     "if (recentre_p_i && !prefill_r[s]) pend_r[s] <= 1'b1;",
     "if (1'b0 && !prefill_r[s]) pend_r[s] <= 1'b1;",
     "--render-only",
     "RENDER-RC-INT: the recentre restored the law (fill at accept = setpoint) (late)"),
    ("recentre counted and cleared but not snapped", "stage",
     "              if (enough_w) begin\n"
     "                rptr_r[s]    <= snap_rptr_w;\n"
     "                prefill_r[s] <= 1'b0;\n"
     "                pend_r[s]    <= 1'b0;\n",
     "              if (enough_w) begin\n"
     "                rptr_r[s]    <= prefill_r[s] ? snap_rptr_w : rptr_r[s];\n"
     "                prefill_r[s] <= 1'b0;\n"
     "                pend_r[s]    <= 1'b0;\n",
     "--render-only",
     "RENDER-RC-INT: the recentre restored the law (fill at accept = setpoint) (early)"),
    ("clock-source trigger dropped from the recentre set", "datapath",
     "       | src_recentre_p_r;",
     "       | 1'b0;",
     "--live-only",
     "RENDER-LIVE-CRF: the fill at accept is the setpoint for every PDU"),
]


#: the marker every observation record carries. Deliberately not a word
#: scripts/suite_tally.py counts: these lines are neither a tally shape nor a
#: [FAIL] marker, so a record can neither add a check nor forge a verdict.
PHASE_MARKER = "RENDER-PHASE"


class PhaseLog:
    """#445's observation of WHEN this driver's phases ran. Nothing else.

    One flushed line per event, around the build and run calls below. Each
    record carries `seq`, which advances even when the write fails, so a lost
    record leaves a visible gap instead of a shorter plausible log; and `t_s`,
    seconds since the origin taken at construction, so durations are
    comparable inside one run and mean nothing across runs.

    The instrument may not decide anything, and does not: it adds no check, no
    tally and no verdict, changes no argument, status, exit or printed line,
    and waits for nothing. A phase is closed only by `end`; one left open is
    incomplete and earns no pass and no caught mutation. The clock is injected
    so the fixtures step it by hand rather than reading the host's.

    Nothing here may raise. Reading the clock is as much a part of the
    telemetry as writing the record, so a clock that fails - at the origin,
    around a call, or under the kill - costs a timing and nothing else: the
    reading is recorded as null, never as a plausible number, and the call's
    own result, its verdict, the tally, exit 143 and the cleanup are whatever
    they would have been with no instrument at all. `SystemExit` is not an
    `Exception` and still leaves through here, so the SIGTERM path is intact.

    `_active` names the call that is running now, and only that: `start` arms
    it once its record is out, `end` disarms it before writing the record that
    closes the phase. So a phase whose `end` a reader can see is never also
    reported active and incomplete by a kill, and a kill between the two is
    the idle it really is.
    """

    def __init__(self, stream: TextIO | None = None,
                 clock: Callable[[], float] = time.monotonic) -> None:
        """Take the origin every later record counts from, and state it once."""
        self._stream = sys.stdout if stream is None else stream
        self._clock = clock
        self._origin: float | None = None
        try:
            self._origin = clock()
        except Exception:
            #! An origin nobody could take leaves every later offset null,
            #! which is a run with its phase order recorded and no durations.
            pass
        self._seq = 0
        #: (case, phase, mode, offset) of the phase now running, or None
        self._active: tuple[str, str, str | None, float | None] | None = None
        #: offset of the last state change, so a gap between phases is timed
        self._since: float | None = 0.0
        self._emit("origin", None if self._origin is None else 0.0,
                   clock="monotonic", unit="s")

    def _now(self) -> float | None:
        """Seconds since the origin, to the millisecond, or None if this
        telemetry reading cannot be taken: taking it and working it out are as
        much a part of the instrument as writing the record, so a clock that
        raises, and an origin that was never taken, both give a gap rather
        than a number nobody measured."""
        try:
            return round(self._clock() - self._origin, 3)
        except Exception:
            return None

    @staticmethod
    def _span(began: float | None, at: float | None) -> float | None:
        """Seconds between two readings, or None when either side is missing:
        a gap is reported as a gap, not as a duration."""
        return None if began is None or at is None else round(at - began, 3)

    def _emit(self, event: str, at: float | None, **fields: object) -> None:
        """Write one record and flush it, so no buffer can hide the last one."""
        self._seq += 1
        try:
            record = {"seq": self._seq, "event": event, "t_s": at}
            record.update(fields)
            self._stream.write(f"{PHASE_MARKER} {json.dumps(record)}\n")
            self._stream.flush()
        except Exception:
            #! Telemetry never rewrites an outcome. A record that cannot be
            #! serialised or written is a gap in the diagnostic, not a changed
            #! verdict, status or exit, and there is nowhere left to report it.
            #! The SIGTERM path still leaves through here: SystemExit is not an
            #! Exception.
            pass

    def baseline(self, selected: str) -> None:
        """Record which unmutated executable the positive controls got: the one
        the sweep already built, or this driver's own fallback build."""
        self._emit("baseline", self._now(), case="control", selected=selected)

    def start(self, case: str, phase: str, mode: str | None = None) -> None:
        """Open one phase of one case, BEFORE the existing call is made."""
        at = self._now()
        self._emit("start", at, case=case, phase=phase, mode=mode,
                   idle_s=self._span(self._since, at))
        self._active = (case, phase, mode, at)
        self._since = at

    def end(self, status: object, **fields: object) -> None:
        """Close the phase `start` opened, with what the existing call returned.

        The phase stops being the running one BEFORE its record is written: a
        kill that lands on this record finds the driver idle, which is what it
        is once the call has returned, and can no longer call a phase a reader
        has already seen ended both complete and incomplete."""
        at = self._now()
        case, phase, mode, began = self._active or (None, None, None, at)
        self._active = None
        self._since = at
        self._emit("end", at, case=case, phase=phase, mode=mode,
                   elapsed_s=self._span(began, at), status=status, **fields)

    def interrupted(self) -> None:
        """Record the state a kill landed in: the case and phase that was
        running and is now incomplete, or the gap between two phases."""
        at = self._now()
        if self._active is None:
            self._emit("interrupted", at, state="idle", case=None, phase=None,
                       mode=None, idle_s=self._span(self._since, at))
            return
        case, phase, mode, began = self._active
        self._emit("interrupted", at, state="active", case=case, phase=phase,
                   mode=mode, elapsed_s=self._span(began, at), incomplete=True)

    def finished(self) -> None:
        """Record that the phase sequence ended, so a truncated log is not
        mistaken for a complete one."""
        at = self._now()
        idle = self._active is None
        self._emit("end-of-run", at, state="idle" if idle else "active",
                   idle_s=self._span(self._since, at) if idle else None)


def build(override: str, rtl_path: Path, mdir: Path,
          observed: Callable[[int], None] | None = None) -> Path | None:
    """Build the leg against `rtl_path` through the suite's own recipe.

    `observed`, when a caller passes one, is handed the recipe's own exit
    status: this helper does see it (#445 asks for the returned status where
    one exists), and the pass/fail decision below, the command, the capture
    and the returned executable-or-nothing are the ones it always had."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "aclk-build", f"{override}={rtl_path}",
         f"ACLK_MDIR={mdir}"],
        capture_output=True, text=True)
    if observed is not None:
        observed(out.returncode)
    exe = mdir / "Vmilan_dp_aclk"
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def timed_build(log: PhaseLog, case: str, override: str, rtl_path: Path,
                mdir: Path) -> Path | None:
    """One build() call, framed by a phase record pair. No try/finally: a call
    that does not return leaves its phase open, which is what incomplete means.
    The record keeps both halves of the answer, because a recipe that returns 0
    without leaving a leg and a recipe that returns 2 are different failures:
    `returncode` is the recipe's own exit status, and `status` stays what
    build() returned, an executable (`built`) or nothing (`no-executable`).
    A recipe whose status was never observed records `returncode` null."""
    log.start(case, "build")
    seen: list[int] = []
    exe = build(override, rtl_path, mdir, seen.append)
    log.end("built" if exe else "no-executable",
            returncode=seen[-1] if seen else None)
    return exe


def run_leg(exe: Path, mode: str) -> tuple[int, str]:
    """(rc, stdout) of one short-mode run, waited for with no host deadline:
    the leg is cycle-bounded (module docstring). The leg is its own session,
    so the sweep's kill reaches it only through the SIGTERM handler in
    main(), whose exit runs the kill below."""
    proc = subprocess.Popen([str(exe), mode], cwd=str(HERE),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, start_new_session=True)
    try:
        out, _ = proc.communicate()
        return proc.returncode, out
    finally:
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait()


def timed_leg(log: PhaseLog, case: str, exe: Path, mode: str) -> tuple[int, str]:
    """One run_leg() call, framed by a phase record pair. The captured output
    is handed back untouched, and only the status the child returned is
    recorded: no part of the child's log enters a record."""
    log.start(case, "simulation", mode)
    rc, out = run_leg(exe, mode)
    log.end(rc)
    return rc, out


def verdict(rc: int, out: str, must_fail: str | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        if must_fail and not any(line.strip().startswith("[FAIL]") and must_fail in line
                                 for line in out.splitlines()):
            return f"failed, but not the named check ({must_fail!r})"
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def main(log: PhaseLog | None = None) -> int:
    """Run the positive controls and every mutant; 1 if any mutant survived."""
    log = PhaseLog() if log is None else log

    def on_sigterm(*_: object) -> None:
        """Name the case and phase the sweep's kill landed in, then exit and
        clean up exactly as this handler always did."""
        log.interrupted()
        sys.exit(143)

    sources = {key: path.read_text() for key, (path, _) in SOURCES.items()}
    passes = fails = 0
    signal.signal(signal.SIGTERM, on_sigterm)
    with tempfile.TemporaryDirectory(prefix="render-mutants-") as td:
        work = Path(td)
        reused = CLEAN_EXE.is_file()
        log.baseline("prebuilt" if reused else "fallback-build")
        exe = CLEAN_EXE if reused else timed_build(
            log, "control", "RSP_SRC", STAGE_RTL, work / "obj_clean")
        for mode in sorted({m[4] for m in MUTATIONS}):
            answer = (verdict(*timed_leg(log, "control", exe, mode), None)
                      if exe else "did not compile")
            if answer == "pass":
                passes += 1
                print(f"[PASS] the unmutated gateware still passes the render-law leg ({mode})")
            else:
                fails += 1
                print(f"[FAIL] the unmutated gateware does NOT pass ({mode}: {answer}) - "
                      f"every mutant result in that mode is meaningless")
        for name, source, pattern, replacement, mode, breaks in MUTATIONS:
            src = sources[source]
            path, override = SOURCES[source]
            if src.count(pattern) != 1:
                fails += 1
                print(f"[FAIL] mutation {name!r}: its pattern appears "
                      f"{src.count(pattern)} time(s) in {path.name}, expected exactly 1. "
                      f"The RTL moved and this mutant is no longer mutating "
                      f"anything - fix the pattern, do not delete the arm.")
                continue
            tag = name.replace(" ", "_").replace("-", "_")
            mpath = work / f"{path.stem}_{tag}.sv"
            mpath.write_text(src.replace(pattern, replacement))
            exe = timed_build(log, tag, override, mpath, work / f"obj_{tag}")
            if exe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant that "
                      f"cannot build proves nothing about the leg")
                continue
            answer = verdict(*timed_leg(log, tag, exe, mode), breaks)
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught ({mode}): {name} - breaks \"{breaks}\"")
            elif answer == "pass":
                fails += 1
                print(f"[FAIL] mutant SURVIVED: {name}. The leg does not "
                      f"prove \"{breaks}\".")
            else:
                fails += 1
                print(f"[FAIL] mutant {name!r} {answer}")
    log.finished()
    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
