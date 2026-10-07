#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""follow_ring's mutation arm: each planted defect must fail its named check.

  mutants.py [--mdir DIR] [--jobs N]

The #645 ruling's planted controls, on the settle recentre that
milan_datapath ships (dp_glue.py copies it, so each is a planted COPY of
milan_datapath.sv the build reads through DP_SRC, never an edit of a tracked
file), the stage-1 W1 arm, and one on the loopback ring's own recentre (a
planted COPY of KL_chan_map_capture.sv through CMAP_SRC):

NO-SETTLE: the settle recentre never pulses. An INTERNAL pull-in under a
  running stream then keeps its shift (#647): the pull-in leg at a feed phase
  the pull moves off the law must fail the law after the settle.
RENDER-ONLY: the settle recentre reaches the render stage but not the
  loopback ring (a define on the wrapper's one restated binding). After the
  INTERNAL-to-AAF set at phase 0.0 the frequency-only servo leaves the ring
  about half a tick from its empty edge, so it must fail centring.
EARLY: under following the settle waits for the aligner's band, as at
  INTERNAL, and not for 8 LOCKED windows: it fires 43 ms after the set, before
  the servo's pull-in walks 1.4 ticks, so the render stage must leave its law.
W1: a switch between two followed sources passes servo IDLE (the design's
  rejected W1, MEDIA_CLOCK_FOLLOWING.md "Switching sources"), so the trim
  restarts from the bare MMCM plan and the DUT reads 5.92 ppm fast while the
  servo re-acquires: the AAF-to-CRF switch must move the ring's phase by more
  than W2's tenth of a tick before its settle recentre.
OVERSHOOT: the loopback ring's recentre aims one event past the depth (17
  at a PDU end). It holds eleven pops where the shipped one holds five, so
  a later PDU finds the queue full. Grading from the decision PDU's end
  catches the resulting drop without granting a post-decision grace period.

NO-ARM: remove excursion arming under a running INTERNAL stream. The fine
  hold (two samples plus 3/64 sample) crosses a gradable render-law boundary
  while its peak error remains below the former four-band threshold.
SINGLE-DROP: replace the full-side correction with one drop. The ten-event
  pre-PDU fill must then fail the LRC wire expectation for five drops.
HELD-DUP: count every held pop as a loopback dup. The declared holds must
  then fail the LRC case for a walk before a pair's first commit, the LRC
  counter check and the span checks' counter check.
STARVED-HELD-DUP: count a held pop as a dup only where the pair is still
  empty (R474-2 F1). Only the LRC case for a walk before a pair's first
  commit reaches that state, so it and the LRC counter check must fail.
NO-RECOVERY: let the excursion arm while recovering. The three-quantum hold
  then causes two actions, one from the aligner's own recovery swing.
HIGH-ARM: raise the arm above the one-quantum pull's +9-cycle peak. Its
  gradable render-law boundary is missed.
QUIET-ARM: set the quiet band to zero. Quantisation noise then arms a
  pending correction in an undisturbed running stream.

Exit 0 = every mutant built and was killed by its named check.
"""

import argparse
import concurrent.futures as cf
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATAPATH = HERE / "../../../hdl/milan/milan_datapath.sv"
CAPTURE = HERE / "../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv"

B8 = ["--case", "b8", "--dwell-s", "1.0", "--set-phase", "0.0", "--hold-s", "16"]
SMALL_PULLIN = ["--case", "pullin", "--hold-us", "42.64", "--latency-us", "204.4", "--after-s", "1.5"]
PULLIN = ["--case", "pullin", "--latency-us", "210.42", "--after-s", "1.5"]

#: (name, wrapper define or None, [(shipped text, planted text)] in the datapath,
#:  [(shipped text, planted text)] in the capture crossbar, leg, the check or
#:  checks that must all fail)
Plant = list[tuple[str, str]]
Mutant = tuple[str, str | None, Plant, Plant, list[str], str | tuple[str, ...]]
#: built and run through chmap_capture's recipe, not follow_ring's
CAPTURE_SUITE = {"SINGLE-DROP", "HELD-DUP", "STARVED-HELD-DUP"}
POP_DUP = "&& q_fed_r[pop_pair_w] && (pop_cnt_w == '0) && !pop_hold_w;"
EARLY_HOLD = "LRC: that held walk on a still-empty pair counts no dup"
LRC_DUPS = "LRC: no recentre moved the dup counter"
MUTANTS: tuple[Mutant, ...] = (
    ("NO-ARM", None,
     [("                      (settle_exc_w && !settle_pend_r && !settle_recover_r);\n",
       "                      1'b0;\n")], [],
     SMALL_PULLIN, "[PULLIN] the render stage is on its law after the settle recentre"),
    ("NO-RECOVERY", None,
     [("                      (settle_exc_w && !settle_pend_r && !settle_recover_r);\n",
       "                      (settle_exc_w && !settle_pend_r);\n")], [],
     SMALL_PULLIN,
     "[PULLIN] exactly one settle recentre from the transient to the hold's end"),
    ("HIGH-ARM", None,
     [("  localparam int unsigned SETTLE_EXC_ERR_C   = 2;\n",
       "  localparam int unsigned SETTLE_EXC_ERR_C   = 10;\n")], [],
     ["--case", "pullin", "--hold-us", "41.9921875", "--latency-us", "204.0", "--after-s", "1.5"],
     "[PULLIN] the render stage is on its law after the settle recentre"),
    ("QUIET-ARM", None,
     [("  localparam int unsigned SETTLE_EXC_ERR_C   = 2;\n",
       "  localparam int unsigned SETTLE_EXC_ERR_C   = 0;\n")], [],
     ["--case", "pullin", "--hold-us", "0", "--latency-us", "204.4", "--after-s", "1.5"],
     "[STEADY] INTERNAL without a hold has no pending settle"),
    ("SINGLE-DROP", None, [],
     [("? LB_DROPW_C'(32'(rc_left_w) - LB_LEFT_C) : '0;",
       "? LB_DROPW_C'(1) : '0;")], [],
     "LRC: ten left drops five excess events on both pairs"),
    ("HELD-DUP", None, [],
     [(POP_DUP, "&& q_fed_r[pop_pair_w] && ((pop_cnt_w == '0) || pop_hold_w);")], [],
     (EARLY_HOLD, LRC_DUPS, "SPAN: no action counted as a duplicate")),
    ("STARVED-HELD-DUP", None, [],
     [(POP_DUP, "&& q_fed_r[pop_pair_w] && (pop_cnt_w == '0);")], [],
     (EARLY_HOLD, LRC_DUPS)),
    ("NO-SETTLE", None,
     [("          settle_recentre_p_r <= 1'b1;\n", "          settle_recentre_p_r <= 1'b0;\n")], [],
     PULLIN, "[PULLIN] the render stage is on its law after the settle recentre"),
    ("RENDER-ONLY", "FR_MUT_RENDER_ONLY", [], [],
     B8, "[B8] the loopback ring is centred after the settle recentre (margin in (5, 6] ticks)"),
    ("EARLY", None,
     [("  wire settle_steady_w = follow_sel_r\n", "  wire settle_steady_w = 1'b0\n"),
      ("  wire [SETTLE_RUN_W_C-1:0] settle_need_w = follow_sel_r\n",
       "  wire [SETTLE_RUN_W_C-1:0] settle_need_w = 1'b0\n")], [],
     B8, "[B8] the render stage is on its law after the settle recentre"),
    ("W1", "FR_MUT_W1", [], [],
     ["--case", "b8", "--dwell-s", "1.0", "--set-phase", "0.0", "--hold-s", "12", "--switch-hold-s", "9"],
     "[SW] AAF to CRF: the switch moved the loopback margin less than 0.1 tick before its settle"),
    ("OVERSHOOT", None, [],
     [("  localparam int unsigned LB_TARGET_C  = (LB_QDEPTH_C + 6) / 2;\n",
       "  localparam int unsigned LB_TARGET_C  = LB_QDEPTH_C + 1;\n")],
     B8, "[B8] no loopback slip after the settle recentre"),
)


def plant(src: Path, edits: list[tuple[str, str]], out: Path) -> str | None:
    """Write `src` with each edit applied once; the reason if one cannot be."""
    text = src.read_text()
    for old, new in edits:
        if text.count(old) != 1:
            return f"the shipped text {old.strip()!r} is not exactly one line of {src.name}"
        text = text.replace(old, new)
    out.write_text(text)
    return None


def run_one(mdir_root: Path, mutant: Mutant) -> tuple[str, bool, str]:
    """Build one mutant through the suite's own recipe and run its leg."""
    name, define, edits, cmap_edits, leg, check = mutant
    mdir = mdir_root / name.lower()
    mdir.mkdir(parents=True, exist_ok=True)
    suite = HERE.parent / "chmap_capture" if name in CAPTURE_SUITE else HERE
    make = ["make", "-j16", "-s", "--no-print-directory", "-C", str(suite), "build",
            "VERILATOR_JOBS=16", f"MDIR={mdir}"]
    if name in {"NO-ARM", "NO-RECOVERY", "HIGH-ARM", "QUIET-ARM"}:
        make += ["CLK_HZ=25000000", "FRAME_DIV=64"]
    if define:
        make.append(f"MUT_DEFS=+define+{define}")
    for src, todo, var in ((DATAPATH, edits, "DP_SRC"), (CAPTURE, cmap_edits, "CMAP_SRC")):
        if todo:
            planted = mdir / f"{src.stem}_planted.sv"
            why = plant(src, todo, planted)
            if why:
                return name, False, f"not planted: {why}"
            make.append(f"{var}={planted}")
    (mdir / "build.command.json").write_text(json.dumps(make) + "\n")
    build = subprocess.run(make, capture_output=True, text=True, check=False)
    (mdir / "build.log").write_text(build.stdout + build.stderr)
    (mdir / "build.rc").write_text(f"{build.returncode}\n")
    if build.returncode != 0:
        return name, False, f"did not build (rc {build.returncode})\n{build.stdout[-2000:]}{build.stderr[-2000:]}"
    executable = "Vchmap_wrap" if name in CAPTURE_SUITE else "Vfollow_ring"
    argv = [str(mdir / executable), *leg]
    (mdir / "run.command.json").write_text(json.dumps(argv) + "\n")
    run = subprocess.run(argv, capture_output=True, text=True, check=False)
    (mdir / "run.log").write_text(run.stdout + run.stderr)
    (mdir / "run.rc").write_text(f"{run.returncode}\n")
    checks = (check,) if isinstance(check, str) else check
    killed = run.returncode != 0 and all(f"[FAIL] {c}" in run.stdout for c in checks)
    return name, killed, run.stdout


def main() -> int:
    """Run every mutant on a pool and require each one's named failure."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mdir", type=Path, default=HERE / "obj_mut")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--select", nargs="+", choices=[m[0] for m in MUTANTS])
    a = ap.parse_args()
    survivors = 0
    selected = [m for m in MUTANTS if not a.select or m[0] in a.select]
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futs = {pool.submit(run_one, a.mdir, m): m for m in selected}
        for fut in cf.as_completed(futs):
            name, killed, out = fut.result()
            check = futs[fut][5]
            named = check if isinstance(check, str) else "\" and \"".join(check)
            print(f"[MUTANT] {name}: {'caught' if killed else 'SURVIVED'} by \"{named}\"", flush=True)
            if not killed:
                print(out)
                survivors += 1
    print(f"follow_ring mutants: {len(selected) - survivors}/{len(selected)} caught")
    return 0 if survivors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
