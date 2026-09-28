#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the capture_coherence suite: prove its assertions can fail.

Why this exists. `sim_main.cpp` asserts that every AAF column the talker
emits carries one TDM frame, that every walk reads the newest frame complete
at its tick and none completed after its first inject, and that columns step
by one frame or by one slip at a beat crossing. A harness whose assertions
never fail is indistinguishable from one that asserts nothing, and the first
mutant below is the law the #451 bench measured: the walk reading per-pair
latest-sample holds, as the crossbar did at ce550952.

So the real RTL is mutated, one defect at a time, and the SAME harness is
run against each mutant through the suite's own Makefile recipe, so the flag
set is stated once: a crossbar mutant through `make build` (CMAP_SRC and MDIR
overridden) against the junction harness, and a datapath mutant through
`make dp-build` (DP_SRC and DP_MDIR overridden) against the milan_datapath
leg, which is the only leg that can see the frame length milan_datapath hands
the crossbar. Every mutant must make the harness FAIL by its OWN verdict (a `[FAIL]`
line or a tally with failures, read by scripts/suite_tally.py) AND the
failure must be the check the mutant names: a run that fails some other check
proves nothing about that one. The unmutated build must still PASS. A crash
or an abort is not a catch. Each pattern is REQUIRED to appear exactly once,
so a refactor that moves the code fails here instead of silently skipping a
mutant.

The junction harness runs with `--quick`: every scenario but the true plan's
whole beat, whose phases the +/-1000 ppm sweeps cross in 3,200 frames each.
Each leg's clean control runs the same way as its mutants, so a mutant is
graded against exactly the scenarios its control passed.

What bounds a livelocking mutant. This driver sets no host-time deadline on a
run (rule 8's wall-clock ratchet, scripts/test_evidence.budget item 4). The
harness is cycle-bounded by construction: each scenario runs until it has
decoded its columns or until a cycle guard fixed from its frame count, and no
loop waits on a DUT output without that guard. The host-time bound is the
sweep's: scripts/run_all_suites.sh runs this suite's `make` under its
per-suite guard and reports a kill as TIMEOUT, an UNKNOWN result (exit 92),
never a pass or a fail. The SIGTERM handler in main() turns that kill into an
exit that removes the temporary directory and the harness's process group.

Usage: python3 mutants.py      (run from tb/verilator/capture_coherence)
Exit 0 = every mutant was caught and the clean build still passes.
"""

import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
#: the file each leg's mutants plant their defects in
RTL = {
    "junction": HERE / "../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv",
    "dp": HERE / "../../../hdl/milan/milan_datapath.sv",
}
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

TORN = "[A] AAF columns mixing two TDM frames"

#: (leg, name, ((pattern, replacement), ...), the check(s) this defect must
#: break, spelled as the harness prints them)
MUTATIONS = [
    ("junction", "the walk reads the per-pair stage (the ce550952 latest-sample law)",
     (("                               ? tdm_walk_r[idx_f[TDMPW_C-1:0]] : 48'd0;",
       "                               ? tdm_stage_r[idx_f[TDMPW_C-1:0]] : 48'd0;"),),
     (TORN, "[W] walks reading two TDM frames")),
    ("junction", "no walk snapshot: the walk reads the frame bank live",
     (("                               ? tdm_walk_r[idx_f[TDMPW_C-1:0]] : 48'd0;",
       "                               ? tdm_frame_r[idx_f[TDMPW_C-1:0]] : 48'd0;"),),
     TORN),
    ("junction", "the frame is closed by its first pair",
     (("(32'(tdm_pair_slot_i) == TDM_FRAME_PAIRS_P - 1);",
       "(32'(tdm_pair_slot_i) == 0);"),
      ("(t == int'(TDM_FRAME_PAIRS_P) - 1) ? tdm_pair_w",
       "(t == 0) ? tdm_pair_w")),
     TORN),
    ("junction", "the frame is published whole but one pair late (at the next frame's first pair)",
     (("(32'(tdm_pair_slot_i) == TDM_FRAME_PAIRS_P - 1);",
       "(32'(tdm_pair_slot_i) == 0);"),
      ("(t == int'(TDM_FRAME_PAIRS_P) - 1) ? tdm_pair_w",
       "1'b0 ? tdm_pair_w")),
     "[W] walks older than the newest frame closed by the tick"),
    ("junction", "the stage is never written (only the closing pair reaches the frame)",
     (("      if (tdm_stage_w) tdm_stage_r[tdm_pair_slot_i[TDMPW_C-1:0]] <= tdm_pair_w;",
       "      if (1'b0) tdm_stage_r[tdm_pair_slot_i[TDMPW_C-1:0]] <= tdm_pair_w;"),),
     #: no column ever carries its own tags, so the harness never goes live
     #: and the vacuity guard is the check that must refuse the run
     "[V] every requested column was decoded"),
    ("dp", "milan_datapath tells the crossbar a one-pair TDM frame",
     (("  localparam int CMAP_TDM_FRAME_PAIRS_C = (AIF_PAIRS_C < CMAP_TDM_SLOTS_C / 2)\n"
       "                                        ? AIF_PAIRS_C : CMAP_TDM_SLOTS_C / 2;",
       "  localparam int CMAP_TDM_FRAME_PAIRS_C = 1;"),),
     TORN),
]

#: each leg's recipe: the build target, its source and objdir overrides, the
#: executable it leaves and the arguments the harness runs with
LEGS = {
    "junction": ("build", "CMAP_SRC", "MDIR", "Vcoherence_sim", ("--quick",)),
    "dp": ("dp-build", "DP_SRC", "DP_MDIR", "Vcoherence_dp", ()),
}


def build(leg: str, rtl_path: Path, workdir: Path, tag: str) -> Path | None:
    """Build `leg`'s harness against `rtl_path` through the suite's own recipe."""
    target, src_var, mdir_var, exe_name, _ = LEGS[leg]
    mdir = workdir / f"obj_{tag}"
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), target, f"{src_var}={rtl_path}", f"{mdir_var}={mdir}"],
        capture_output=True, text=True, check=False)
    exe = mdir / exe_name
    if out.returncode != 0 or not exe.is_file():
        return None
    return exe


def run_harness(leg: str, exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one harness run, from the suite directory (the datapath
    leg's processor reads its ROM images by relative name), waited for with no
    host deadline: the harness is cycle-bounded (module docstring). The harness
    is its own session, so the sweep's kill reaches it only through the
    SIGTERM handler in main(), whose exit runs the kill below."""
    proc = subprocess.Popen([str(exe), *LEGS[leg][4]], cwd=HERE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, start_new_session=True)
    try:
        out, _ = proc.communicate()
        return proc.returncode, out
    finally:
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait()


def named_checks(breaks: str | tuple[str, ...]) -> tuple[str, ...]:
    """The check name(s) a mutant must break, as a tuple."""
    return (breaks,) if isinstance(breaks, str) else breaks


def verdict(rc: int, out: str, must_fail: tuple[str, ...] = ()) -> str:
    """How the harness answered: 'pass', 'caught', or why it is not evidence.

    A harness failure is a catch only when every check the mutant NAMES is
    among the reported failures.
    """
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        lines = [line.strip() for line in out.splitlines()
                 if line.strip().startswith("[FAIL]")]
        missing = [w for w in must_fail
                   if not any(w in line for line in lines)]
        if missing:
            return ("failed, but not the named check(s) "
                    f"{', '.join(repr(w) for w in missing)}")
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def mutate(src: str, edits: tuple[tuple[str, str], ...]) -> str | None:
    """The source with every edit applied, or None if any pattern is not unique."""
    for pattern, replacement in edits:
        if src.count(pattern) != 1:
            return None
        src = src.replace(pattern, replacement)
    return src


def grade_mutant(leg: str, work: Path, name: str, edits: tuple[tuple[str, str], ...],
                 breaks: str | tuple[str, ...]) -> bool:
    """Build and run one mutant; True when it was caught by its named check(s)."""
    src = RTL[leg].read_text()
    mutated = mutate(src, edits)
    if mutated is None:
        counts = [src.count(p) for p, _ in edits]
        print(f"[FAIL] mutation {name!r}: its pattern(s) appear {counts} "
              f"time(s), expected exactly 1 each. The RTL moved and this "
              f"mutant is no longer mutating anything - fix the pattern, "
              f"do not delete the arm.")
        return False
    tag = "".join(c if c.isalnum() else "_" for c in name)[:60]
    mpath = work / tag / RTL[leg].name
    mpath.parent.mkdir()
    mpath.write_text(mutated)
    exe = build(leg, mpath, work, tag)
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that "
              f"cannot build proves nothing about the harness")
        return False
    wanted = named_checks(breaks)
    shown = " and ".join(f'"{w}"' for w in wanted)
    answer = verdict(*run_harness(leg, exe), wanted)
    if answer == "caught":
        print(f"[PASS] mutant caught: {name} - breaks {shown}")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The harness does not prove {shown}.")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def clean_control(leg: str, work: Path) -> bool:
    """The unmutated RTL through `leg`'s recipe must pass its harness."""
    clean = work / f"clean_{leg}" / RTL[leg].name
    clean.parent.mkdir()
    clean.write_text(RTL[leg].read_text())
    exe = build(leg, clean, work, f"clean_{leg}")
    answer = verdict(*run_harness(leg, exe)) if exe else "did not compile"
    if answer == "pass":
        print(f"[PASS] the unmutated RTL still passes the {leg} harness")
        return True
    print(f"[FAIL] the unmutated RTL does NOT pass the {leg} harness ({answer}) - "
          f"every {leg} mutant result is meaningless")
    return False


def main() -> int:
    """Run each leg's positive control and every mutant; 1 if any mutant survived."""
    passes = fails = 0
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    with tempfile.TemporaryDirectory(prefix="capture-coherence-mutants-") as td:
        work = Path(td)
        for leg in LEGS:
            if clean_control(leg, work):
                passes += 1
            else:
                fails += 1
        for leg, name, edits, breaks in MUTATIONS:
            if grade_mutant(leg, work, name, edits, breaks):
                passes += 1
            else:
                fails += 1
    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
