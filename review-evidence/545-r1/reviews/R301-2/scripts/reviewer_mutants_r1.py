#!/usr/bin/env python3
"""Reviewer mutation probes for the #545 servo change (exact head sources).

Each mutant is one textual edit of KL_mmcm_drp_servo.sv, built into its own
scratch directory with the repository Makefile, then graded by the named
harness mode. A mutant is KILLED when the harness exits 1 with RESULT: FAIL;
SURVIVED when it exits 0. Build failures are reported, never counted as kills.
"""
import concurrent.futures as cf
import os
import subprocess
import sys
from pathlib import Path

PKT = Path(os.environ.get("PKT", "$REVIEWS/545-r301-2-packet"))
TREE = PKT / "scratch/tree"          # created by servo_suite.sh (git archive of the head)
MS = TREE / "tb/verilator/mmcm_servo"
RTL = TREE / "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
VER = os.environ.get("VERILATOR", "$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator")
WORK = PKT / "scratch/rmut"

# name, anchor, replacement, harness ("unit" | "phc:+arg")
MUTANTS = [
    ("coincident_step_double_counted",
     "slew_window_w && !step_hit_w;", "slew_window_w;", "unit"),
    ("boundary_reseed_removed",
     "            win_slew_r  <= phc_slew_q_r;\n", "", "phc:+slew_control"),
    ("boundary_sample_ignored_by_pi",
     "                           && !slew_window_w\n", "                           && !win_slew_r\n", "phc:+slew_suite"),
    ("count_every_cycle",
     "  wire slew_hit_w = tick_p_w && win_valid_r &&\n                    (tick_cnt_r == (WIN_LOG2_P+1)'(WIN_TICKS_C - 1)) &&\n",
     "  wire slew_hit_w = win_valid_r &&\n", "phc:+slew_control"),
    ("guard_streak_not_reset_by_slew",
     "        if (slew_hit_w) disc_run_r <= '0;\n", "", "phc:+slew_suite"),
    ("guard_streak_not_reset_by_slew_unit",
     "        if (slew_hit_w) disc_run_r <= '0;\n", "", "unit"),
    ("open_seed_removed",
     "            win_slew_r <= phc_slew_q_r;\n", "", "phc:+slew_suite"),
    ("sticky_clear_removed",
     "      if (!win_valid_r) win_slew_r <= 1'b0;\n      else if (phc_slew_q_r) win_slew_r <= 1'b1;\n",
     "      if (phc_slew_q_r) win_slew_r <= 1'b1;\n", "phc:+slew_suite"),
]


def run(m):
    name, anchor, repl, harness = m
    src = RTL.read_text()
    if src.count(anchor) != 1:
        return name, "ANCHOR", f"anchor count {src.count(anchor)}"
    d = WORK / name
    d.mkdir(parents=True, exist_ok=True)
    rtl = d / "KL_mmcm_drp_servo.sv"
    rtl.write_text(src.replace(anchor, repl))
    if harness == "unit":
        tgt, var, exe, args = "unit-build", "UNIT_MDIR", "Vservo_sim", []
    else:
        tgt, var, exe, args = "phc_step_build", "PHC_MDIR", "Vphc_step", [harness.split(":", 1)[1]]
    b = subprocess.run(["make", "-s", "--no-print-directory", "-C", str(MS), tgt,
                        f"SERVO_RTL={rtl}", f"{var}={d / 'obj'}", f"VERILATOR={VER}"],
                       capture_output=True, text=True)
    (d / "build.log").write_text(b.stdout + b.stderr)
    if b.returncode:
        return name, "BUILD-FAIL", ""
    r = subprocess.run([str(d / "obj" / exe)] + args, capture_output=True, text=True, timeout=1500)
    out = r.stdout + r.stderr
    (d / "run.log").write_text(out)
    fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l or "FAIL]" in l][:6]
    verdict = "KILLED" if (r.returncode == 1 and "RESULT: FAIL" in out) else (
        "SURVIVED" if r.returncode == 0 else f"rc={r.returncode}")
    return name, verdict, f"harness={harness}; " + " | ".join(fails)


def main():
    sel = [m for m in MUTANTS if len(sys.argv) < 2 or m[0] in sys.argv[1:]]
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for name, verdict, detail in ex.map(run, sel):
            print(f"{verdict:10s} {name}: {detail}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
