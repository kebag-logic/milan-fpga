#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require section [RB] to fail on each planted defect of the REBOOT reset (#787).

The control builds this suite's base leg and runs section [RB] alone
(`--reboot-only`): once from the committed sources, which must pass, then
once per arm with a private copy of one source carrying the arm's plant.
Each copy must fail [RB] on the arm's named check. [RB] grades the frames
where they leave its MAC model, so the arms that let the PHY hold rise while
a frame is still in the MAC fail there, not at the datapath's port:

  request-ignored              KL_reboot_ctrl never sees the processor's request
  early-request                the request rises at the processor's acceptance,
                               before the SUCCESS response has left
  hold-on-the-request-alone    the PHY hold on the request, the shape silicon
                               ran: no egress wait at all
  egress-ignores-the-mac-fifo  the wait ends once the datapath's port is idle
  egress-without-a-bound       a MAC that never finishes keeps the hold off
  txend-unwired                the MAC's frame-end toggle is not connected

Mutant logs stay in the private directory. Exit 0 = the clean control passed
and every arm was caught by its named check; 1 = otherwise.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATAPATH = (ROOT / "hdl" / "milan" / "milan_datapath.sv").resolve()
CTRL = (ROOT / "hdl" / "milan" / "KL_reboot_ctrl.sv").resolve()

DEPARTING = ("[FAIL] RB advertising: ENTITY_DEPARTING leaves after the notification, "
             "before the PHY hold")

#: (name, source, old text, new text, the named check this must break)
ARMS = [
    ("request-ignored", DATAPATH,
     "      .reboot_req_i    (pp_reboot_req_w),\n",
     "      .reboot_req_i    (pp_reboot_req_w & 1'b0),\n",
     "[FAIL] RB advertising: the PHY hold rises"),
    ("early-request", DATAPATH,
     "      .reboot_req_i    (pp_reboot_req_w),\n",
     "      .reboot_req_i    (pp_reboot_req_w | (pp_shadow.u_pp.rbt_st_r != 3'd0)),\n",
     "[FAIL] RB advertising: the PHY hold follows the processor's REBOOT request"),
    ("hold-on-the-request-alone", CTRL,
     "            state_r <= S_EGRESS;\n            ms_r    <= '0;\n            quiet_r <= 1'b0;",
     "            state_r <= S_HOLD;\n            ms_r    <= '0;\n            hold_r  <= 1'b1;",
     DEPARTING),
    ("egress-ignores-the-mac-fifo", CTRL,
     "assign idle_w       = ~in_frame_r & (fly_r == '0);",
     "assign idle_w       = ~in_frame_r & ((fly_r == '0) | 1'b1);",
     DEPARTING),
    ("egress-without-a-bound", CTRL,
     "assign egress_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_EGRESS_MS_C));",
     "assign egress_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_EGRESS_MS_C)) & 1'b0;",
     "[FAIL] RB dead transmit clock: the PHY hold still rises"),
    ("txend-unwired", DATAPATH,
     "      .mac_txend_tgl_i (i_ethtxend_tgl),\n",
     "      .mac_txend_tgl_i (i_ethtxend_tgl & 1'b0),\n",
     "[FAIL] RB advertising: ...and at most two ticks and eight clocks after it"),
]


def run_leg(directory: Path, label: str, sources: list[Path] | None = None) -> tuple[int, str]:
    """Build the base leg into its own directory and run [RB] alone."""
    build = directory / label
    command = ["make", "--no-print-directory", "build-base", f"BUILD_DIR={build}"]
    if sources is not None:
        command.append("DP_SRCS=" + " ".join(str(path) for path in sources))
    log_path = directory / f"{label}.log"
    with log_path.open("w") as log:
        made = subprocess.run(command, cwd=HERE, stdout=log,
                              stderr=subprocess.STDOUT, check=False)
        if made.returncode != 0:
            return made.returncode, log_path.read_text()
        ran = subprocess.run([str(build / "Vpp_shadow_sim"), "--reboot-only"], cwd=HERE,
                             stdout=log, stderr=subprocess.STDOUT, check=False)
    return ran.returncode, log_path.read_text()


def main() -> int:
    """The clean control, then every arm; 0 when each arm was caught."""
    originals = {path: path.read_text() for path in (DATAPATH, CTRL)}
    for name, source, old, _new, _check in ARMS:
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
    with tempfile.TemporaryDirectory(prefix="pp-reboot-") as temporary:
        directory = Path(temporary)
        status, text = run_leg(directory, "control")
        if status != 0 or "RESULT: PASS" not in text:
            print(f"FAIL: the clean control did not pass [RB] (exit {status})")
            return 1
        print("clean control: [RB] PASS")
        for name, source, old, new, check in ARMS:
            mutant = directory / name / "hdl" / "milan" / source.name
            mutant.parent.mkdir(parents=True)
            mutant.write_text(originals[source].replace(old, new))
            planted = [mutant if path == source else path for path in sources]
            status, text = run_leg(directory, name, planted)
            failing = sum(1 for line in text.splitlines()
                          if line.lstrip().startswith("[FAIL]"))
            caught = status != 0 and "RESULT: FAIL" in text and any(
                line.lstrip().startswith(check) for line in text.splitlines())
            if caught:
                print(f"{name}: KILLED by its named check, {failing} failing checks")
                print(f"  named check: {check[len('[FAIL] '):]}")
            else:
                reason = "it built nothing to grade" if "RESULT:" not in text else \
                         "its named check passed"
                print(f"{name}: SURVIVED, {reason} (exit {status})")
                missed.append(name)
    for path, text in originals.items():
        if path.read_text() != text:
            print(f"FAIL: {path.name} changed during the mutation")
            return 1
    print(f"== pp_shadow reboot mutants: arms: {len(ARMS)}   survived: {len(missed)} ==")
    if missed:
        print("RESULT: FAIL (" + ", ".join(missed) + ")")
        return 1
    print(f"PASS: [RB] catches every arm ({len(ARMS)} of {len(ARMS)}); clean control passes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
