#!/usr/bin/env python3
"""Reviewer-owned R300-3 mutation probe for the #545 guard-streak contract.

Same mechanism as reviewer_mutants_r2.py (anchored clause rewrite, -j 4
build through the suite Makefile, harness verdict); round-3 mutants only.

Run from an exact-head extraction of the repository:
    python3 reviewer_mutants.py <repo-root> <work-dir> <mutant-name>
Each mutant rewrites one anchored clause of KL_mmcm_drp_servo.sv into
<work-dir>, builds the named harness with at most -j 4, runs it and prints
the harness verdict and every failing check. Exit 0 means the probe ran;
the verdict (KILLED / SURVIVED / BUILD-FAIL) is on the last line.
"""

import subprocess
import sys
from pathlib import Path

# name: (anchor, replacement, harness, plusarg)
MUTANTS = {
    "clean_unit": (None, None, "unit", ""),
    "clean_slew_suite": (None, None, "phc", "+slew_suite"),
    # an odd arming cannot hide any fixed per-discard increment: +2 per discard
    "slew_discard_adds_two": (
        "if (slew_hit_w) disc_run_r <= '0;", "if (slew_hit_w) disc_run_r <= disc_run_r + 2'd2;", "unit", ""),
    # a slew discard decrements (wraps) the streak
    "slew_discard_decrements": (
        "if (slew_hit_w) disc_run_r <= '0;", "if (slew_hit_w) disc_run_r <= disc_run_r - 2'd1;", "unit", ""),
    # a slew discard handled like a #539 step: abandon the window and restart
    "slew_discard_abandons_window_unit": (
        "if (slew_hit_w) disc_run_r <= '0;", "if (slew_hit_w) begin\n          win_valid_r <= 1'b0;\n"
        "          disc_run_r  <= '0;\n        end", "unit", ""),
    "slew_discard_abandons_window_suite": (
        "if (slew_hit_w) disc_run_r <= '0;", "if (slew_hit_w) begin\n          win_valid_r <= 1'b0;\n"
        "          disc_run_r  <= '0;\n        end", "phc", "+slew_suite"),
    # only a window whose boundary sample is still slewing restarts the streak
    "slew_reset_only_while_level_high": (
        "if (slew_hit_w) disc_run_r <= '0;", "if (slew_hit_w && phc_slew_q_r) disc_run_r <= '0;", "unit", ""),
    "slew_reset_only_while_level_high_suite": (
        "if (slew_hit_w) disc_run_r <= '0;", "if (slew_hit_w && phc_slew_q_r) disc_run_r <= '0;", "phc", "+slew_suite"),
}

VFLAGS = ("--cc --exe --build -j 4 -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME "
          "-Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM "
          "-Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS \"-std=c++17 -O2 -Wall -Wextra\"")


def main() -> int:
    root, work, name = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
    verilator = sys.argv[4] if len(sys.argv) > 4 else "verilator"
    anchor, repl, harness, plus = MUTANTS[name]
    src = (root / "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv").read_text()
    if anchor is not None:
        n = src.count(anchor)
        if n != 1:
            print(f"VERDICT {name}: ANCHOR-COUNT {n}")
            return 1
        src = src.replace(anchor, repl)
    work.mkdir(parents=True, exist_ok=True)
    rtl = work / f"{name}.sv"
    rtl.write_text(src)
    mdir = work / f"obj_{name}"
    tb = root / "tb/verilator/mmcm_servo"
    target, binname, mvar = (("phc_step_build", "Vphc_step", "PHC_MDIR") if harness == "phc"
                             else ("unit-build", "Vservo_sim", "UNIT_MDIR"))
    b = subprocess.run(["make", "--no-print-directory", "-s", "-C", str(tb), target,
                        f"SERVO_RTL={rtl}", f"{mvar}={mdir}", f"VERILATOR={verilator}",
                        f"VFLAGS={VFLAGS}"], capture_output=True, text=True, check=False)
    if b.returncode:
        print(b.stdout[-3000:] + b.stderr[-3000:])
        print(f"VERDICT {name}: BUILD-FAIL")
        return 0
    cmd = [str(mdir / binname)] + ([plus] if plus else [])
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    out = r.stdout + r.stderr
    (work / f"{name}.run.log").write_text(out)
    fails = [ln.strip() for ln in out.splitlines() if "[FAIL]" in ln or "FAIL " in ln[:12]]
    for ln in fails[:20]:
        print("  " + ln)
    summary = [ln for ln in out.splitlines() if "checks" in ln and "fail" in ln.lower()]
    for ln in summary:
        print("  " + ln.strip())
    if anchor is None:
        print(f"VERDICT {name}: {'CLEAN-PASS' if r.returncode == 0 else 'CLEAN-FAIL'} rc={r.returncode}")
    else:
        print(f"VERDICT {name}: {'KILLED' if r.returncode != 0 else 'SURVIVED'} rc={r.returncode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
