#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The defect controls the closed loop owns.

WHY THIS EXISTS. A green suite and a suite that cannot go red look the same
from the outside. Each control below plants ONE defect the design is
supposed to refuse, requires this suite to notice, and restores the exact
source afterwards - verified, not assumed. A control that leaves the suite
green is a finding about the suite.

WHAT IS HERE AND WHAT IS NOT. Only the defects that need the SHIPPING MAC
and the two real seams to show up: the observation point itself, the number
of register stages between the launch and the capture, and the measured
cycle distance that refuses a fragmented frame. The ledger's ownership,
recovery and PHC-history controls live with the plane-slice suite, which
carries them at a fraction of the build cost.

Each control names the check it must break, and the run prints whether that
check really failed rather than only that something did.

Usage:
    python3 mutants.py            # every control
    python3 mutants.py --list     # name them and change nothing

Exit 0 = every control was caught and every source restored; 1 = a control
was not caught, or a file was left modified; 2 = the tree was not clean to
start with, which is a refusal rather than a mutation of unknown work.
"""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
PLANE = REPO / "hdl" / "ieee8021as" / "gptp_plane"
WRAP = HERE / "gptp_txts_wrap.sv"

#: The record carries the EXPECTED distance instead of the one the observer
#: measured, which is how a fragmented frame earns a plausible timestamp instead
#: of an abort. Both shapes carry this control: a whole frame measures 45 clocks
#: on GMII and 90 on MII, so a refusal read against the wrong one cannot fail.
DELTA_FORCED_OLD = (
    "                        oidx_r, gen_r, type_r, seq_r, delta_r,\n"
    "                        (delta_r != TXTS_DELTA_W_P'"
    "(TXTS_DELTA_EXP_P))};")
DELTA_FORCED_NEW = (
    "                        oidx_r, gen_r, type_r, seq_r,\n"
    "                        TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P),\n"
    "                        1'b0};  // MUTATION: forced, not measured")

#: The 10/100 shape's controls (issue #829), each run on the MII build. The first
#: is the fault itself: the observer reads one octet per clock, the delimiter
#: check fails on the held preamble, no record ever comes and the engine waits
#: for one.
MII_MUTATIONS = [
    (
        "mii_observer_ignores_ready",
        PLANE / "KL_gptp_gmii_launch.sv",
        "        if (gmii_tready_i) begin\n",
        "        if (1'b1) begin  // MUTATION: one octet per clock\n",
        "launch: an isolated exchange completes",
    ),
    (
        "mii_first_symbol_term_dropped",
        PLANE / "KL_gptp_txret.sv",
        "(TXTS_DELTA_EXP_P + OBS_LAT_E_CYC_P + ETH_CYC_PER_OCTET_P - 1) * ETH_TICK_NS_P",
        "(TXTS_DELTA_EXP_P + OBS_LAT_E_CYC_P) * ETH_TICK_NS_P  // MUTATION",
        "bias: the mean error is within 1.754 ns of zero",
    ),
    (
        "mii_transmit_tick_left_at_gmii",
        WRAP,
        "      .ETH_TICK_NS_P (ETH_TICK_NS_P),\n",
        "      .ETH_TICK_NS_P (8),  // MUTATION\n",
        "launch: every reconstruction is inside the published bound",
    ),
    (
        "mii_history_guard_left_at_the_gmii_floor",
        PLANE / "KL_gptp_txret.sv",
        "(RECON_NEED_CYC_C > RECON_GUARD_CYC_P) ? RECON_NEED_CYC_C : RECON_GUARD_CYC_P;",
        "RECON_GUARD_CYC_P;  // MUTATION",
        "phc window: that frame's own result is an explicit loss",
    ),
    (
        "mii_delta_forced_not_measured",
        PLANE / "KL_gptp_gmii_launch.sv",
        DELTA_FORCED_OLD,
        DELTA_FORCED_NEW,
        "fragment: the observer refused it, by measurement",
    ),
]

#: (name, file, old text, new text, the check this must break)
MUTATIONS = [
    (
        "observer_disconnected",
        WRAP,
        "assign obs_valid_w = phy_sink_v_o & ~obs_bubble_i;",
        "assign obs_valid_w = 1'b0;  // MUTATION",
        "launch: every isolated frame was graded",
    ),
    (
        "observer_shifted_one_transmit_cycle",
        WRAP,
        "  assign obs_valid_w = phy_sink_v_o & ~obs_bubble_i;",
        "  logic mut_v_r;\n"
        "  logic [7:0] mut_d_r;\n"
        "  always_ff @(posedge eth_clk_i) begin\n"
        "    mut_v_r <= phy_sink_v_o & ~obs_bubble_i;\n"
        "    mut_d_r <= phy_sink_d_o;\n"
        "  end\n"
        "  assign obs_valid_w = mut_v_r;  // MUTATION: one cycle late",
        "bias: the mean error is within one nanosecond of zero",
    ),
    (
        "observer_latency_term_dropped",
        PLANE / "KL_gptp_txret.sv",
        "parameter int unsigned OBS_LAT_E_CYC_P  = 2,",
        "parameter int unsigned OBS_LAT_E_CYC_P  = 1,",
        "bias: the mean error is within one nanosecond of zero",
    ),
    (
        "crossing_latency_term_dropped",
        PLANE / "KL_gptp_txret.sv",
        "parameter int unsigned CDC_LAT_D_CYC_P  = 2,",
        "parameter int unsigned CDC_LAT_D_CYC_P  = 1,",
        "bias: the mean error is within one nanosecond of zero",
    ),
    (
        "mean_sampling_phase_term_dropped",
        PLANE / "KL_gptp_txret.sv",
        "    + CDC_LAT_D_CYC_P * DP_TICK_NS_P\n    + DP_TICK_NS_P / 2;",
        "    + CDC_LAT_D_CYC_P * DP_TICK_NS_P;  // MUTATION",
        "bias: the mean error is within one nanosecond of zero",
    ),
    (
        "delta_forced_not_measured",
        PLANE / "KL_gptp_gmii_launch.sv",
        DELTA_FORCED_OLD,
        DELTA_FORCED_NEW,
        "fragment: the observer refused it, by measurement",
    ),
]


def tracked_clean(path: Path) -> bool:
    """Is `path` TRACKED and unmodified?

    Both halves matter. `git diff --quiet` says nothing about a file Git
    does not know, and `git checkout --` cannot restore one: the first
    version of this driver mutated an untracked wrapper and left the defect
    in the tree. An untracked file is refused rather than mutated.
    """
    known = subprocess.run(["git", "ls-files", "--error-unmatch", str(path)],
                           cwd=REPO, check=False, capture_output=True)
    if known.returncode != 0:
        return False
    done = subprocess.run(["git", "diff", "--quiet", "--", str(path)],
                          cwd=REPO, check=False)
    return done.returncode == 0


def restore(path: Path) -> None:
    """Put the file back exactly as Git has it. The caller re-checks."""
    subprocess.run(["git", "checkout", "--", str(path)], cwd=REPO, check=True)


def run_suite(target: str) -> str:
    """Build and run the suite's target, returning its whole output."""
    done = subprocess.run(["make", "-s", target], cwd=HERE, check=False,
                          capture_output=True, text=True)
    return done.stdout + done.stderr


def apply_control(path: Path, old: str, new: str) -> bool:
    """Plant one defect. False when its anchor is no longer in the source,
    which is a finding about this file and not a passing control."""
    text = path.read_text(encoding="utf-8")
    if old not in text:
        return False
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def main() -> int:
    """Run every control, or list them."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true",
                        help="name the controls and change nothing")
    args = parser.parse_args()

    controls = ([("run", *control) for control in MUTATIONS] +
                [("run-mii", *control) for control in MII_MUTATIONS])
    if args.list:
        for _target, name, path, _old, _new, expect in controls:
            print(f"{name:40s} {path.relative_to(REPO)}  -> {expect}")
        return 0

    for _target, _name, path, _old, _new, _expect in controls:
        if not tracked_clean(path):
            print(f"REFUSED: {path.relative_to(REPO)} is untracked or "
                  f"already modified; a control must not mutate work in "
                  f"progress and must be able to restore what it mutated",
                  file=sys.stderr)
            return 2

    failures = 0
    for target, name, path, old, new, expect in controls:
        if not apply_control(path, old, new):
            print(f"[FAIL] {name}: its anchor is no longer in "
                  f"{path.relative_to(REPO)}")
            failures += 1
            continue
        output = run_suite(target)
        restore(path)
        if not tracked_clean(path):
            print(f"[FAIL] {name}: {path.relative_to(REPO)} was not restored")
            failures += 1
            continue
        caught = "RESULT: FAIL" in output
        named = expect in output and "[FAIL] " + expect in output
        if caught and named:
            print(f"[ ok ] {name}: caught by \"{expect}\"")
        elif caught:
            print(f"[ ok ] {name}: caught, though not by \"{expect}\"")
        else:
            print(f"[FAIL] {name}: the suite stayed green")
            failures += 1

    print(f"controls: {len(controls)}   failures: {failures}")
    print(f"RESULT: {'PASS' if failures == 0 else 'FAIL'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
