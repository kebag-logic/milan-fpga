#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
bringup.py — start Vivado and bring up the Milan TSN NIC project on a chosen
FPGA device.

This is the human-friendly entry point. It:
  1. finds the Vivado install and sources its settings,
  2. lets you pick the target device (--part),
  3. launches Vivado (GUI by default) running bringup.tcl, which creates the
     project, adds the RTL, builds the milan_dma block design, and sets
     milan_top as the top.

Examples
--------
    # open the project in the Vivado GUI on the board's Zynq-7000 device
    ./bringup.py

    # a different device, GUI
    ./bringup.py --part xc7z010clg400-1

    # headless (no GUI), e.g. on a build server
    ./bringup.py --batch

    # bring up just the RTL (no Zynq PS7 block design) on any installed part
    ./bringup.py --part xc7s100fgga484-1 --no-bd
"""

from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Directory of this script (= <repo>/bd) and the Tcl it drives.
BD_DIR = Path(__file__).resolve().parent
BRINGUP_TCL = BD_DIR / "bringup.tcl"

# The board's target device. Change this default, or pass --part.
DEFAULT_PART = "xc7z020clg400-1"


def find_vivado_settings(explicit: str | None) -> Path:
    """Locate a Vivado settings64.sh (sourced to put `vivado` on PATH)."""
    if explicit:
        p = Path(explicit)
        if not p.is_file():
            sys.exit(f"error: --vivado-settings '{p}' does not exist")
        return p

    # If `vivado` is already on PATH, no settings file is needed.
    if shutil.which("vivado"):
        return Path()  # empty -> "already on PATH"

    # Otherwise pick the newest install under the usual roots.
    candidates: list[str] = []
    for root in ("/opt/Xilinx", "/tools/Xilinx", os.path.expanduser("~/Xilinx")):
        candidates += glob.glob(f"{root}/*/Vivado/settings64.sh")
    if not candidates:
        sys.exit(
            "error: could not find Vivado. Put `vivado` on PATH, or pass "
            "--vivado-settings /opt/Xilinx/<ver>/Vivado/settings64.sh"
        )
    newest = sorted(candidates)[-1]  # lexical sort ~ version order (…/2026.1/…)
    return Path(newest)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Start Vivado and bring up the Milan TSN project.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--part", default=DEFAULT_PART,
                    help="FPGA device (full Vivado part name)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--gui", dest="gui", action="store_true", default=True,
                      help="open the Vivado GUI (default)")
    mode.add_argument("--batch", dest="gui", action="store_false",
                      help="run headless (no GUI)")
    bd = ap.add_mutually_exclusive_group()
    bd.add_argument("--with-bd", dest="with_bd", action="store_const", const=1,
                    help="force building the milan_dma block design")
    bd.add_argument("--no-bd", dest="with_bd", action="store_const", const=0,
                    help="RTL only, skip the Zynq PS7 block design")
    ap.add_argument("--vivado-settings", default=None,
                    help="path to a specific Vivado settings64.sh")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the command that would run, then exit")
    args = ap.parse_args()

    if not BRINGUP_TCL.is_file():
        sys.exit(f"error: {BRINGUP_TCL} not found next to this script")

    # with_bd: default = auto (Zynq-7000 -> yes, else no); bringup.tcl decides
    # when we don't pass it, so only forward it if the user was explicit.
    settings = find_vivado_settings(args.vivado_settings)
    vmode = "gui" if args.gui else "batch"

    # Build the `vivado ... -tclargs <part> [with_bd]` invocation.
    tclargs = [args.part]
    if args.with_bd is not None:
        tclargs.append(str(args.with_bd))
    vivado_cmd = (
        f"vivado -mode {vmode} -notrace "
        f"-source {shq(str(BRINGUP_TCL))} -tclargs {' '.join(shq(a) for a in tclargs)}"
    )

    # Source the settings (if any) in the same shell, then run Vivado.
    if settings and str(settings):
        shell_cmd = f"source {shq(str(settings))} && {vivado_cmd}"
    else:
        shell_cmd = vivado_cmd  # vivado already on PATH

    print(f"# device (part) : {args.part}")
    print(f"# mode          : {vmode}")
    print(f"# vivado        : {'(PATH)' if not str(settings) else settings}")
    print(f"# tcl           : {BRINGUP_TCL}")
    print(f"# command        : {shell_cmd}")
    if args.dry_run:
        return 0

    # Run from bd/ so build outputs land under bd/build/.
    return subprocess.call(["bash", "-lc", shell_cmd], cwd=str(BD_DIR))


def shq(s: str) -> str:
    """Minimal shell-quote (paths here are simple, but be safe)."""
    if s and all(c.isalnum() or c in "-._/=:" for c in s):
        return s
    return "'" + s.replace("'", "'\\''") + "'"


if __name__ == "__main__":
    raise SystemExit(main())
