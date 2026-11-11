#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require section [DR] to fail on each planted defect of the tap's drop count (#854).

Two controls build this suite's base leg and run section [DR] alone
(`--drops-only`) from the committed sources, and both must pass: the base leg
as the suite builds it, and the base leg with rx_mac_filter pruned
(`RXFILT=0`, RXFILT_P = 0), the one build where a one-beat runt reaches the
tap. Then each arm is built in its leg with a private copy of one source
carrying the arm's plant, and must fail [DR] on the arm's named check:

  count-removed          the drop count never moves
  count-from-tready      the count read from the FIFO's tready, which a FIFO
                         that drops when full never lowers
  counts-refused         every FIFO overflow counted, a refused frame's too
  misses-second-beat     a frame the tap keeps at its second beat not counted
  wraps                  the count wraps instead of saturating at 255
  diag-tied-off          the count never reaches PP_DIAG[15:8]
  misses-oversize        a frame lost for being longer than the FIFO not
                         counted (a frame over 512 words ends uncounted)
  counts-runts           a runt the full FIFO turns away counted; RXFILT=0
                         leg, since the filter drops every runt in the other

Mutant logs stay in the private directory. Exit 0 = both clean controls passed
and every arm was caught by its named check; 1 = otherwise.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SHADOW = (ROOT / "hdl" / "milan" / "KL_pp_shadow.sv").resolve()
DATAPATH = (ROOT / "hdl" / "milan" / "milan_datapath.sv").resolve()

COUNTS = "[FAIL] DR a burst past the FIFO loses frames and counts them"

#: the arm's leg: the base leg as the suite builds it, or with the filter pruned
BASE, PRUNED = "1", "0"

#: (name, source, old text, new text, the named check this must break, RXFILT)
ARMS = [
    ("count-removed", SHADOW,
     "      if (drop_evt_w & (rx_drops_o != 8'hFF)) rx_drops_o <= rx_drops_o + 8'd1;\n",
     "      if (drop_evt_w & (rx_drops_o != 8'hFF) & 1'b0) rx_drops_o <= rx_drops_o + 8'd1;\n",
     COUNTS, BASE),
    ("count-from-tready", SHADOW,
     "  assign drop_evt_w = ff_overflow_w & last_kept_r;\n",
     "  assign drop_evt_w = (fw_valid_w & ~fw_ready_w) | (ff_overflow_w & last_kept_r & 1'b0);\n",
     COUNTS, BASE),
    ("counts-refused", SHADOW,
     "  assign drop_evt_w = ff_overflow_w & last_kept_r;\n",
     "  assign drop_evt_w = ff_overflow_w | (last_kept_r & 1'b0);\n",
     "[FAIL] DR ...and are not counted: the kept frames lost equal the count", BASE),
    ("misses-second-beat", SHADOW,
     "      last_kept_r <= (fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w);\n",
     "      last_kept_r <= (fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w && 1'b0);\n",
     "[FAIL] DR the burst's lost frames equal the drop count", BASE),
    ("wraps", SHADOW,
     "      if (drop_evt_w & (rx_drops_o != 8'hFF)) rx_drops_o <= rx_drops_o + 8'd1;\n",
     "      if (drop_evt_w) rx_drops_o <= rx_drops_o + 8'd1;\n",
     "[FAIL] DR the count saturates at 255", BASE),
    ("diag-tied-off", DATAPATH,
     "    .i_pp_rx_drops      (pp_rx_drops_w),\n",
     "    .i_pp_rx_drops      (pp_rx_drops_w & 8'd0),\n",
     COUNTS, BASE),
    ("misses-oversize", SHADOW,
     "  assign drop_evt_w = ff_overflow_w & last_kept_r;\n",
     "  logic [9:0] mut_beats_r;\n"
     "  logic       mut_long_r;\n"
     "  always_ff @(posedge clk_i or negedge rst_n) begin\n"
     "    if (!rst_n) begin\n"
     "      mut_beats_r <= 10'd0;\n"
     "      mut_long_r  <= 1'b0;\n"
     "    end else if (fw_valid_w && fw_ready_w) begin\n"
     "      mut_beats_r <= fw_last_w ? 10'd0 : mut_beats_r + {9'd0, mut_beats_r != 10'h3FF};\n"
     "      if (fw_last_w) mut_long_r <= mut_beats_r >= 10'd512;\n"
     "    end\n"
     "  end\n"
     "  assign drop_evt_w = ff_overflow_w & last_kept_r & ~mut_long_r;\n",
     "[FAIL] DR the frame longer than the FIFO is counted", BASE),
    ("counts-runts", SHADOW,
     "      last_kept_r <= (fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w);\n",
     "      last_kept_r <= (fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w) || (fw_S == FW_HEAD0);\n",
     "[FAIL] DR ...and runts are not counted: the kept frames lost equal the count", PRUNED),
]


def run_leg(directory: Path, label: str, rxfilt: str, sources: list[Path] | None = None) -> tuple[int, str]:
    """Build the base leg, the filter as `rxfilt` says, into its own directory and run [DR] alone."""
    build = directory / label
    command = ["make", "--no-print-directory", "build-base", f"BUILD_DIR={build}", f"RXFILT={rxfilt}"]
    if sources is not None:
        command.append("DP_SRCS=" + " ".join(str(path) for path in sources))
    log_path = directory / f"{label}.log"
    with log_path.open("w") as log:
        made = subprocess.run(command, cwd=HERE, stdout=log,
                              stderr=subprocess.STDOUT, check=False)
        if made.returncode != 0:
            return made.returncode, log_path.read_text()
        ran = subprocess.run([str(build / "Vpp_shadow_sim"), "--drops-only"], cwd=HERE,
                             stdout=log, stderr=subprocess.STDOUT, check=False)
    return ran.returncode, log_path.read_text()


def main() -> int:
    """The two clean controls, then every arm; 0 when each arm was caught."""
    originals = {path: path.read_text() for path in (SHADOW, DATAPATH)}
    for name, source, old, _new, _check, _leg in ARMS:
        if originals[source].count(old) != 1:
            print(f"REFUSED: {name}: its anchor occurs {originals[source].count(old)} times")
            return 1
    #: read the list as the Makefile does: under an outer `make -C` an
    #: inherited MAKEFLAGS prints directory lines into it
    quiet = {key: value for key, value in os.environ.items() if key not in ("MAKEFLAGS", "MFLAGS")}
    listing = subprocess.run(["make", "-s", "--no-print-directory", "-C", "../milan_dp", "print-srcs"],
                             cwd=HERE, check=True, capture_output=True, text=True, env=quiet)
    sources = [(HERE / path).resolve() for path in listing.stdout.split()]
    for path in originals:
        if sources.count(path) != 1:
            print(f"REFUSED: expected exactly one {path.name} in the datapath source list")
            return 1
    missed = []
    with tempfile.TemporaryDirectory(prefix="pp-drops-") as temporary:
        directory = Path(temporary)
        for leg, label in ((BASE, "control"), (PRUNED, "control-rxfilt0")):
            status, text = run_leg(directory, label, leg)
            if status != 0 or "RESULT: PASS" not in text:
                print(f"FAIL: the clean control (RXFILT={leg}) did not pass [DR] (exit {status})")
                return 1
            print(f"clean control (RXFILT={leg}): [DR] PASS")
        for name, source, old, new, check, leg in ARMS:
            mutant = directory / name / "hdl" / "milan" / source.name
            mutant.parent.mkdir(parents=True)
            mutant.write_text(originals[source].replace(old, new))
            planted = [mutant if path == source else path for path in sources]
            status, text = run_leg(directory, name, leg, planted)
            failing = sum(1 for line in text.splitlines()
                          if line.lstrip().startswith("[FAIL]"))
            caught = status != 0 and "RESULT: FAIL" in text and any(
                line.lstrip().startswith(check) for line in text.splitlines())
            if caught:
                print(f"{name} (RXFILT={leg}): KILLED by its named check, {failing} failing checks")
                print(f"  named check: {check[len('[FAIL] '):]}")
            else:
                reason = "it built nothing to grade" if "RESULT:" not in text else \
                         "its named check passed"
                print(f"{name} (RXFILT={leg}): SURVIVED, {reason} (exit {status})")
                missed.append(name)
    for path, text in originals.items():
        if path.read_text() != text:
            print(f"FAIL: {path.name} changed during the mutation")
            return 1
    print(f"== pp_shadow drops mutants: arms: {len(ARMS)}   survived: {len(missed)} ==")
    if missed:
        print("RESULT: FAIL (" + ", ".join(missed) + ")")
        return 1
    print(f"PASS: [DR] catches every arm ({len(ARMS)} of {len(ARMS)}); both clean controls pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
