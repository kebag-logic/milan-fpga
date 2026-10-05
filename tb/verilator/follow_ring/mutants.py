#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""follow_ring's mutation arm: each planted defect must fail its named check.

  mutants.py [--mdir DIR] [--jobs N]

The #645 ruling's three planted controls, on the settle recentre that
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
OVERSHOOT: the loopback ring's recentre aims one event past the depth (9 at
  a PDU end). It holds three pops where the shipped one holds two, so the
  next PDU finds the queue full and drops an event about a PDU after the
  decision. The ring then sits back inside (2, 3] ticks, so centring passes:
  only grading that drop as after the settle recentre, from the end of the
  PDU the ring decided on, catches it.

Exit 0 = every mutant built and was killed by its named check.
"""

import argparse
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATAPATH = HERE / "../../../hdl/milan/milan_datapath.sv"
CAPTURE = HERE / "../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv"

B8 = ["--case", "b8", "--dwell-s", "1.0", "--set-phase", "0.0", "--hold-s", "16"]
PULLIN = ["--case", "pullin", "--latency-us", "210.42", "--after-s", "1.5"]

#: (name, wrapper define or None, [(shipped text, planted text)] in the datapath,
#:  [(shipped text, planted text)] in the capture crossbar, leg, the check that must fail)
MUTANTS = (
    ("NO-SETTLE", None,
     [("          settle_recentre_p_r <= 1'b1;\n", "          settle_recentre_p_r <= 1'b0;\n")], [],
     PULLIN, "[PULLIN] the render stage is on its law after the settle recentre"),
    ("RENDER-ONLY", "FR_MUT_RENDER_ONLY", [], [],
     B8, "[B8] the loopback ring is centred after the settle recentre (margin in (2, 3] ticks)"),
    ("EARLY", None,
     [("  wire settle_steady_w = follow_sel_r\n", "  wire settle_steady_w = 1'b0\n"),
      ("  wire [SETTLE_RUN_W_C-1:0] settle_need_w = follow_sel_r\n",
       "  wire [SETTLE_RUN_W_C-1:0] settle_need_w = 1'b0\n")], [],
     B8, "[B8] the render stage is on its law after the settle recentre"),
    ("W1", "FR_MUT_W1", [], [],
     ["--case", "b8", "--dwell-s", "1.0", "--set-phase", "0.0", "--hold-s", "12", "--switch-hold-s", "9"],
     "[SW] AAF to CRF: the switch moved the loopback margin less than 0.1 tick before its settle"),
    ("OVERSHOOT", None, [],
     [("  localparam int unsigned LB_LEFT_C    = LB_TARGET_C - 6;\n",
       "  localparam int unsigned LB_LEFT_C    = LB_TARGET_C - 5;\n")],
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


def run_one(mdir_root: Path, name: str, define: str | None, edits: list[tuple[str, str]],
            cmap_edits: list[tuple[str, str]], leg: list[str], check: str) -> tuple[str, bool, str]:
    """Build one mutant through the suite's own recipe and run its leg."""
    mdir = mdir_root / name.lower()
    mdir.mkdir(parents=True, exist_ok=True)
    make = ["make", "-s", "--no-print-directory", "-C", str(HERE), "build", f"MDIR={mdir}"]
    if define:
        make.append(f"MUT_DEFS=+define+{define}")
    for src, todo, var in ((DATAPATH, edits, "DP_SRC"), (CAPTURE, cmap_edits, "CMAP_SRC")):
        if todo:
            planted = mdir / f"{src.stem}_planted.sv"
            why = plant(src, todo, planted)
            if why:
                return name, False, f"not planted: {why}"
            make.append(f"{var}={planted}")
    build = subprocess.run(make, capture_output=True, text=True, check=False)
    if build.returncode != 0:
        return name, False, f"did not build (rc {build.returncode})\n{build.stdout[-2000:]}{build.stderr[-2000:]}"
    run = subprocess.run([str(mdir / "Vfollow_ring"), *leg], capture_output=True, text=True, check=False)
    killed = run.returncode != 0 and f"[FAIL] {check}" in run.stdout
    return name, killed, run.stdout


def main() -> int:
    """Run every mutant on a pool and require each one's named failure."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mdir", type=Path, default=HERE / "obj_mut")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    survivors = 0
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futs = {pool.submit(run_one, a.mdir, *m): m for m in MUTANTS}
        for fut in cf.as_completed(futs):
            name, killed, out = fut.result()
            check = futs[fut][5]
            print(f"[MUTANT] {name}: {'caught' if killed else 'SURVIVED'} by \"{check}\"", flush=True)
            if not killed:
                print(out)
                survivors += 1
    print(f"follow_ring mutants: {len(MUTANTS) - survivors}/{len(MUTANTS)} caught")
    return 0 if survivors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
