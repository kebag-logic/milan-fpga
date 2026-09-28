#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the capture_coherence suite: prove its assertions can fail.

Why this exists. `sim_main.cpp` asserts that every AAF column the talker
emits carries one TDM frame, that every walk reads exactly the frame its tick
takes, that columns step by one frame or by one slip at a beat crossing,
that the junction counters count each walk's slips, and that under CRF no
lock phase repeats or skips a frame. A harness whose assertions never fail is
indistinguishable from one that asserts nothing, and the first mutant below
is the law the #451 bench measured: the walk reading per-pair latest-sample
holds, as the crossbar did at ce550952.

So the real RTL is mutated, one defect at a time, and the SAME harness is
run against each mutant through its suite's own Makefile recipe, so the flag
set is stated once. Eight legs:
  junction  a crossbar mutant through `make build` (CMAP_SRC, MDIR) against
            the junction harness, `--quick`;
  band      a mutant of the wrapper's grid-aligner binding (WRAP_SRC) - the
            round-2 guard: marker, delayed tick, keep-off - against the
            junction harness's placed true-plan band, `--band`;
  band50    a datapath mutant through the junction's `make build` (DP_SRC):
            the wrapper binds milan_datapath's own keep-off declaration
            (mga_keepoff.py), so a mutated keep-off meets the junction's
            placed +/-50 ppm bands, `--band50` - the value the true-plan band
            cannot see;
  fine      a media NCO mutant (NCO_SRC) against the junction's sub-cycle
            sweep at -50 ppm, `--fine`: where the aligner's trim updates land
            on the NCO's terminal count;
  dp        a datapath mutant through `make dp-build` (DP_SRC, DP_MDIR)
            against the milan_datapath leg's fixed scenarios, `--quick`: the
            only leg that sees the frame length milan_datapath hands the
            crossbar;
  dp-band   a datapath mutant against that leg's placed band, `--band`: the
            only leg that sees milan_datapath's own aligner binding;
  chmap     a crossbar mutant through tb/verilator/chmap_capture's `make
            build` (CMAP_SRC, MDIR): the only harness that elaborates the
            one-pair TDM frame of the I2S-capture shapes, and that queues a
            tick behind a running walk;
  nco       a media NCO mutant through tb/verilator/media_nco's `make build`
            (NCO_SRC, MDIR): the grid alone, its trim moved on every cycle
            around the terminal count.
Every mutant must make the harness FAIL by its OWN verdict (a `[FAIL]` line
or a tally with failures, read by scripts/suite_tally.py) AND the failure
must be the check the mutant names: a run that fails some other check proves
nothing about that one. Each leg's unmutated build must still PASS the same
run. A crash or an abort is not a catch. Each pattern is REQUIRED to appear
exactly once, so a refactor that moves the code fails here instead of
silently skipping a mutant.

`--quick` leaves out the junction's whole true-plan beat (whose phases the
+/-1000 ppm sweeps cross in 3,200 frames each) and every placed sweep;
`--band` runs the true plan's placed band alone; `--band50` the +/-50 ppm
bands every 32 cycles; `--fine` the -50 ppm sub-cycle sweep. Each leg's clean
control runs the same way as its mutants, so a mutant is graded against
exactly the scenarios its control passed.

What bounds a livelocking mutant. This driver sets no host-time deadline on a
run (rule 8's wall-clock ratchet, scripts/test_evidence.budget item 4). The
harnesses are cycle-bounded by construction: each scenario runs until it has
decoded its columns or until a cycle guard fixed from its frame count, and no
loop waits on a DUT output without that guard. The host-time bound is the
sweep's: scripts/run_all_suites.sh runs this suite's `make` under its
per-suite guard and reports a kill as TIMEOUT, an UNKNOWN result (exit 92),
never a pass or a fail. The SIGTERM handler in main() turns that kill into an
exit that removes the temporary directory and the harness's process group.

Usage: python3 mutants.py      (run from tb/verilator/capture_coherence)
Exit 0 = every mutant was caught and every clean build still passes.
"""

import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHMAP = HERE / "../chmap_capture"
MEDIA_NCO = HERE / "../media_nco"
CROSSBAR = HERE / "../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv"
DATAPATH = HERE / "../../../hdl/milan/milan_datapath.sv"
NCO = HERE / "../../../hdl/ieee1722/crf/KL_media_nco.sv"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

TORN = "[A] AAF columns mixing two TDM frames"
MISCOUNT = "[C] walks whose repeat or skip the junction counters did not count"
LOCK_SLIP = "[C] slips while the CRF lock held"

#: each leg's recipe: the suite directory, the build target, its source and
#: objdir overrides, the file its mutants plant defects in, the executable it
#: leaves and the arguments the harness runs with
LEGS = {
    "junction": (HERE, "build", "CMAP_SRC", "MDIR", CROSSBAR, "Vcoherence_sim", ("--quick",)),
    "band": (HERE, "build", "WRAP_SRC", "MDIR", HERE / "coherence_wrap.sv", "Vcoherence_sim", ("--band",)),
    "band50": (HERE, "build", "DP_SRC", "MDIR", DATAPATH, "Vcoherence_sim", ("--band50",)),
    "fine": (HERE, "build", "NCO_SRC", "MDIR", NCO, "Vcoherence_sim", ("--fine",)),
    "dp": (HERE, "dp-build", "DP_SRC", "DP_MDIR", DATAPATH, "Vcoherence_dp", ("--quick",)),
    "dp-band": (HERE, "dp-build", "DP_SRC", "DP_MDIR", DATAPATH, "Vcoherence_dp", ("--band",)),
    "chmap": (CHMAP, "build", "CMAP_SRC", "MDIR", CROSSBAR, "Vchmap_wrap", ()),
    "nco": (MEDIA_NCO, "build", "NCO_SRC", "MDIR", NCO, "Vmedia_nco_sim", ()),
}

#: the wrapper's aligner binding and milan_datapath's, as rounds 2 and 3
#: write them
WRAP_KEEPOFF = ("    .FS_HZ_P            (FS_HZ_C),\n    .LOCK_KEEPOFF_CYC_P (MGA_KEEPOFF_CYC_C)",
                "    .FS_HZ_P            (FS_HZ_C)")
WRAP_TICK = ("    .tick_i (tick_q_r),", "    .tick_i (tick_w),")
WRAP_MARKER = ("    .frame_ev_i (cap_pv_w && (32'(cap_slot_w) == TDM_SLOTS_P / 2 - 1)),",
               "    .frame_ev_i (cap_pv_w && (cap_slot_w == 4'd0)),")
#: the crossbar's snapshot instant and the NCO's terminal compare (#617
#: rounds 2 and 3)
SNAP = "  wire tdm_snap_w = (st_r == CM_IDLE_S) && (tick_pend_r ? tick_late_r : tick_i);"
NCO_EQ = (("    else if (32'(cnt_r) >= end_w) begin", "    else if (32'(cnt_r) == end_w) begin"),)

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
     "[W] walks older than the frame their tick takes"),
    ("junction", "the stage is never written (only the closing pair reaches the frame)",
     (("      if (tdm_stage_w) tdm_stage_r[tdm_pair_slot_i[TDMPW_C-1:0]] <= tdm_pair_w;",
       "      if (1'b0) tdm_stage_r[tdm_pair_slot_i[TDMPW_C-1:0]] <= tdm_pair_w;"),),
     #: no column ever carries its own tags, so the harness never goes live
     #: and the vacuity guard is the check that must refuse the run
     "[V] every requested column was decoded"),
    ("junction", "the walk ignores the coincidence law: a close on the tick cycle always waits",
     (("  wire         tdm_snap_take_w = tdm_snap_w && tdm_close_w && !tdm_frame_pend_r;",
       "  wire         tdm_snap_take_w = 1'b0;"),),
     (MISCOUNT, "[W] walks older than the frame their tick takes")),
    ("junction", "the walk snapshot back on the pre-walk's last cycle (the round-1 instant)",
     (("  wire tdm_snap_w = (st_r == CM_IDLE_S) && (tick_pend_r ? tick_late_r : tick_i);",
       "  wire tdm_snap_w = (st_r == CM_POP_S) && (32'(pop_idx_r) == LB_PAIRS_C);"),),
     "[W] walks newer than the frame their tick takes"),
    ("junction", "the junction counters keyed on the slot-0 write against the tick (the round-1 law)",
     (("      unique case ({tdm_close_w, tdm_snap_w})",
       "      unique case ({tdm_pair_valid_i && (tdm_pair_slot_i == 4'd0), tick_i})"),),
     MISCOUNT),
    ("band", "the round-1 aligner binding: slot-0 marker, the tick itself, the 1/128-sample keep-off",
     (WRAP_MARKER, WRAP_TICK, WRAP_KEEPOFF),
     LOCK_SLIP),
    ("band", "the aligner's keep-off back to its 1/128-sample default",
     (WRAP_KEEPOFF,),
     LOCK_SLIP),
    ("band", "the aligner sees the tick itself, one cycle before the walk's crossing",
     (WRAP_TICK,),
     "[C] CRF slips net zero"),
    ("dp", "milan_datapath tells the crossbar a one-pair TDM frame",
     (("  localparam int CMAP_TDM_FRAME_PAIRS_C = (AIF_PAIRS_C < CMAP_TDM_SLOTS_C / 2)\n"
       "                                        ? AIF_PAIRS_C : CMAP_TDM_SLOTS_C / 2;",
       "  localparam int CMAP_TDM_FRAME_PAIRS_C = 1;"),),
     TORN),
    ("dp-band", "milan_datapath's round-1 aligner binding: slot-0 marker, the tick itself, the default keep-off",
     (("    .FS_HZ_P            (48_000),\n    .LOCK_KEEPOFF_CYC_P (MGA_KEEPOFF_CYC_C)",
       "    .FS_HZ_P            (48_000)"),
      ("    .frame_ev_i (aafcap_pv_w &&\n"
       "                 (32'(aafcap_slot_w) == CMAP_TDM_FRAME_PAIRS_C - 1)),\n"
       "    .tick_i     (media_tick_q_r),",
       "    .frame_ev_i (aafcap_pv_w && (aafcap_slot_w == 4'd0)),\n"
       "    .tick_i     (media_tick_p),")),
     LOCK_SLIP),
    ("chmap", "RM7: a tick queued behind a running walk takes no snapshot when its walk starts",
     ((SNAP, "  wire tdm_snap_w = (st_r == CM_IDLE_S) && !tick_pend_r && tick_i;"),),
     "Q: col 2 pair 0 L is frame 4"),
    ("chmap", "RM8: a queued tick snapshots at the tick itself, reloading the walk still running",
     ((SNAP, "  wire tdm_snap_w = tick_i;"),),
     ("Q: col 1 pair 2 L is frame 2", "Q: col 2 pair 0 L is frame 4")),
    ("band50", "RM5: milan_datapath's keep-off halved to 128 cycles, under the 200-cycle proportional "
               "equilibrium a 50 ppm rate forces on a pulled engagement",
     (("                                            ? MGA_SAMPLE_CYC_C / 4 : 256;",
       "                                            ? MGA_SAMPLE_CYC_C / 4 : 128;"),),
     LOCK_SLIP),
    ("nco", "the terminal compare back to == (377d1ac3): a trim lowering the end under the count is missed",
     NCO_EQ,
     "update landing at old end +0: one tick, in a period the old or the new trim sets"),
    ("fine", "the terminal compare back to == (377d1ac3), under the aligner's trim updates",
     NCO_EQ,
     "[C] CRF slips net zero"),
    ("chmap", "the frame closes on the bucket's last pair whatever the frame length",
     (("(32'(tdm_pair_slot_i) == TDM_FRAME_PAIRS_P - 1);",
       "(32'(tdm_pair_slot_i) == N_TDM_PAIRS_C - 1);"),
      ("(t == int'(TDM_FRAME_PAIRS_P) - 1) ? tdm_pair_w",
       "(t == int'(N_TDM_PAIRS_C) - 1) ? tdm_pair_w")),
     "F1: col 0 carries its own pair-0 frame (L)"),
]


def build(leg: str, rtl_path: Path, workdir: Path, tag: str) -> Path | None:
    """Build `leg`'s harness against `rtl_path` through the suite's own recipe."""
    suite, target, src_var, mdir_var, _, exe_name, _ = LEGS[leg]
    mdir = workdir / f"obj_{tag}"
    out = subprocess.run(
        ["make", "-s", "-C", str(suite), target, f"{src_var}={rtl_path}", f"{mdir_var}={mdir}"],
        capture_output=True, text=True, check=False)
    exe = mdir / exe_name
    if out.returncode != 0 or not exe.is_file():
        return None
    return exe


def run_harness(leg: str, exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one harness run, from its suite directory (the datapath
    leg's processor reads its ROM images by relative name), waited for with no
    host deadline: the harness is cycle-bounded (module docstring). The harness
    is its own session, so the sweep's kill reaches it only through the
    SIGTERM handler in main(), whose exit runs the kill below."""
    suite, *_, args = LEGS[leg]
    proc = subprocess.Popen([str(exe), *args], cwd=suite, stdout=subprocess.PIPE,
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
    rtl = LEGS[leg][4]
    src = rtl.read_text()
    mutated = mutate(src, edits)
    if mutated is None:
        counts = [src.count(p) for p, _ in edits]
        print(f"[FAIL] mutation {name!r}: its pattern(s) appear {counts} "
              f"time(s), expected exactly 1 each. The RTL moved and this "
              f"mutant is no longer mutating anything - fix the pattern, "
              f"do not delete the arm.")
        return False
    tag = "".join(c if c.isalnum() else "_" for c in f"{leg}_{name}")[:60]
    mpath = work / tag / rtl.name
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
        print(f"[PASS] mutant caught ({leg}): {name} - breaks {shown}")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED ({leg}): {name}. The harness does not prove {shown}.")
    else:
        print(f"[FAIL] mutant ({leg}) {name!r} {answer}")
    return False


def clean_control(leg: str, work: Path) -> bool:
    """The unmutated source through `leg`'s recipe must pass its harness."""
    rtl = LEGS[leg][4]
    clean = work / f"clean_{leg}" / rtl.name
    clean.parent.mkdir()
    clean.write_text(rtl.read_text())
    exe = build(leg, clean, work, f"clean_{leg}")
    answer = verdict(*run_harness(leg, exe)) if exe else "did not compile"
    if answer == "pass":
        print(f"[PASS] the unmutated source still passes the {leg} harness")
        return True
    print(f"[FAIL] the unmutated source does NOT pass the {leg} harness ({answer}) - "
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
