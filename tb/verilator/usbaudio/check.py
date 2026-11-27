#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run bounded transport regressions and representative defect controls."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import time


def main() -> None:
    """Run each required baseline and representative planted defect."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--cleanup-ledger", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    args.out.mkdir(parents=True, exist_ok=True)
    ledger = args.cleanup_ledger or args.out/"cleanup.log"
    subprocess.run([sys.executable, "-B", str(here/"selection_test.py")], check=True)
    subprocess.run([sys.executable, "-B", str(here/"packing_test.py"),
                    "--out", str(args.out/"packing")], check=True)
    cases = [(name, name, []) for name in ("protocol", "reference", "media", "packet", "gpif", "levels", "epochs")]
    cases += [("storage24", "storage", ["STORAGE_BITS=24"]),
              ("storage32", "storage", ["STORAGE_BITS=32"]),
              ("duplex", "duplex", ["WINDOW_LOG2=5"])]
    suffix = "__ALL."+Path(args.engine).name+"_deplist.tmp"
    for name, test, options in cases:
        build = args.out/name
        top = "VKL_usbaudio_bridge" if test == "duplex" else "V"+test+"_tb"
        with ledger.open("a") as record:
            record.write(f"Planned generated temporary removal: {build/(top+suffix)}\n")
            record.flush()
            os.fsync(record.fileno())
        target = "build" if test == "protocol" else test+"-build"
        subprocess.run(["make", "-C", str(here), target, "MDIR="+str(build),
                        "RTL_SIMULATOR="+args.engine, "JOBS="+str(args.jobs), *options], check=True)
        subprocess.run([str(build/top), *(["1000"] if test == "duplex" else [])], check=True)
    subprocess.run([sys.executable, "-B", str(here/"transport_mutations.py"),
                    "--engine", args.engine, "--out", str(args.out/("defects-"+str(time.time_ns()))),
                    "--jobs", str(args.jobs), "--cleanup-ledger", str(ledger),
                    "--temporary-suffix", suffix, "--discard-builds",
                    "--only", "reference_count_alignment", "--only", "media_epoch_trailing",
                    "--only", "gpif_blocked_status", "--only", "packet_fence",
                    "--only", "bridge_applied_epoch", "--only", "bridge_capture_abort",
                    "--only", "bridge_status_epoch", "--only", "bridge_published_epoch",
                    "--only", "bridge_packet_fence",
                    "--only", "levels_clock_launch", "--only", "levels_playback_launch",
                    "--only", "levels_capture_launch"], check=True)
    print("PASS default audio regression: selection, protocol, references, media, packets, bus, "
          "both widths, duplex and defect controls")


if __name__ == "__main__":
    main()
