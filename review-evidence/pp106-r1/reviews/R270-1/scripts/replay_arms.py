#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer replay of the author's key failing arms and of the two changed
srp_top stimuli, from git objects only (disposable trees; never a fix).

Usage: replay_arms.py <donor clone> <scratch dir> <verilator dir> [ARM ...]

Each arm exports the PR head, overlays named files from another revision,
and runs the named suites through run_srp_suites.sh.
  M0-enc   : base KL_srp_encoder.sv (fbc1f715) under the head encoder suite
  RX0-dec  : KL_srp_decoder.sv of the first #106 commit (9370f8ab) under the
             head decoder suite
  RX0-top  : the first commit's receive side (decoder, both stream FSMs,
             KL_srp_top, srp_pkg) under the head srp_top suite
  STIM-old : the head RTL under the first commit's srp_top sim_main.cpp (the
             F2/F4 stimuli before the change) -- shows the stimuli had to move
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEAD = "fc155c3ca28b04c2220bf41ebea9214379210452"
BASE = "fbc1f7156d711e5b7f511da8a16d9494256b017b"
TX = "9370f8ab80231bbf1a6a833312e6b4ffbd0a4f9b"
RX_FILES = ["hdl/srp/KL_srp_decoder.sv", "hdl/srp/KL_srp_talker_fsm.sv",
            "hdl/srp/KL_srp_listener_fsm.sv", "hdl/srp/KL_srp_top.sv",
            "hdl/srp/srp_pkg.sv"]
ARMS = {
    "M0-enc": (BASE, ["hdl/srp/KL_srp_encoder.sv"], ["srp_encoder"]),
    "RX0-dec": (TX, ["hdl/srp/KL_srp_decoder.sv"], ["srp_decoder"]),
    "RX0-top": (TX, RX_FILES, ["srp_top"]),
    "STIM-old": (TX, ["tb/srp_top/sim_main.cpp"], ["srp_top"]),
}


def main():
    clone, scratch, vdir = sys.argv[1:4]
    for arm in sys.argv[4:] or list(ARMS):
        rev, files, suites = ARMS[arm]
        root = Path(scratch) / f"arm-{arm}"
        subprocess.run(["rm", "-rf", str(root)], check=True)
        root.mkdir(parents=True)
        arch = subprocess.run(["git", "-C", clone, "archive", HEAD],
                              check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(root)], input=arch, check=True)
        for f in files:
            blob = subprocess.run(["git", "-C", clone, "show", f"{rev}:{f}"],
                                  check=True, capture_output=True).stdout
            (root / f).write_bytes(blob)
        out = subprocess.run([str(HERE / "run_srp_suites.sh"), str(root), vdir, *suites],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            if not line.startswith("Verilator"):
                print(f"{arm} (overlay {rev[:8]}: {len(files)} file(s)) {line}")
        for s in suites:
            log = (root / "tb" / s / "run.log").read_text(errors="replace")
            fails = [l.strip() for l in log.splitlines()
                     if l.strip().startswith("FAIL") and "checks:" not in l]
            for l in fails[:8]:
                print(f"{arm}   {s}: {l[:150]}")
            if len(fails) > 8:
                print(f"{arm}   {s}: ... {len(fails) - 8} more FAIL lines")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
