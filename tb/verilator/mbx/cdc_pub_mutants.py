#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""cdc_pub_mutants.py - planted defects the gPTP publication crossing's bench must catch (#884, REQ-PTP-07).

Each arm copies the crossing (KL_mbx_cdc.sv) and the sources the bench builds with it to a scratch directory,
writes ONE defect into the copy (a substitution that must occur exactly once), builds tb_cdc_pub.sv against the
copy with the Makefile's own recipe (read through `make print-cdc-pub-vflags`, never restated here), runs it, and
requires the run to fail with a `[FAIL]` line holding the arm's words. The unmodified crossing is the positive
control (`make run-cdc-pub`, which `make cdc-pub-mutants` runs first). The tree is never written.

Usage:
    python3 tb/verilator/mbx/cdc_pub_mutants.py [--jobs N] [--keep DIR]

Exit 0 = every arm caught by its words; 1 = an arm escaped or did not build; 2 = a fixture did not apply.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MBX = ROOT / "hdl" / "milan" / "mailbox"
#: the bench's sources, in the Makefile's order (CDC_PUB_RTL), the crossing among them
SOURCES = (MBX / "KL_mbx_pkg.sv", ROOT / "hdl" / "common" / "cdc_handshake.sv",
           ROOT / "hdl" / "common" / "cdc_pulse.sv", MBX / "KL_mbx_cdc_window.sv", MBX / "KL_mbx_cdc.sv")


@dataclass(frozen=True)
class Arm:
    """One planted defect in KL_mbx_cdc.sv and the words its [FAIL] line must hold."""

    name: str
    old: str
    new: str
    needle: str


ARMS = (
    # the defect #966's first review found: the crossing takes the live words when it is free, not the commit
    Arm("live-words-crossed", ".src_in(gptp_bank_r)", ".src_in(m_pub_gptp_i)",
        "not a commit newer than the last it took"),
    # a bank that follows the live words each cycle is no bank: an update begun after a commit reaches it
    Arm("bank-follows-the-live-words", "      if (gptp_commit_w) gptp_bank_r <= m_pub_gptp_i;\n",
        "      gptp_bank_r <= m_pub_gptp_i;\n", "not a commit newer than the last it took"),
    # the latch taking precedence over a commit on its own edge loses that commit
    Arm("commit-on-the-latch-edge-lost",
        "      if (gptp_commit_w) gptp_dirty_r <= 1'b1;\n      else if (gptp_latch_w) gptp_dirty_r <= 1'b0;\n",
        "      if (gptp_latch_w) gptp_dirty_r <= 1'b0;\n      else if (gptp_commit_w) gptp_dirty_r <= 1'b1;\n",
        "a commit on the edge the crossing takes the one before: the last commit landed"),
    # a commit owed after the crossing took it is sent again: the same snapshot lands twice
    Arm("taken-commit-still-owed", "      else if (gptp_latch_w) gptp_dirty_r <= 1'b0;\n", "",
        "not a commit newer than the last it took"),
    # a commit while one crosses, left waiting for a GEN move that already happened
    Arm("commit-in-flight-dropped", "      end else if (gptp_dirty_r) begin\n",
        "      end else if (gptp_dirty_r && gptp_commit_w) begin\n",
        "the last commit landed"),
)


def vflags() -> list[str]:
    """The Makefile's recipe for the crossing's bench, one argument a line."""
    out = subprocess.run(["make", "-s", "--no-print-directory", "-C", str(HERE), "print-cdc-pub-vflags"],
                         check=True, capture_output=True, text=True).stdout
    return [line for line in out.splitlines() if line]


def run_arm(arm: Arm, root: Path, flags: list[str]) -> tuple[str, str]:
    """Plant, build and run one arm; returns (verdict, detail)."""
    work = root / arm.name
    rtl = work / "rtl"
    rtl.mkdir(parents=True)
    copies = []
    for src in SOURCES:
        shutil.copy(src, rtl / src.name)
        copies.append(rtl / src.name)
    target = rtl / "KL_mbx_cdc.sv"
    text = target.read_text()
    if text.count(arm.old) != 1:
        return "FIXTURE", f"the substitution occurs {text.count(arm.old)} times"
    target.write_text(text.replace(arm.old, arm.new))
    build = subprocess.run([*flags, "--Mdir", str(work / "obj"), *map(str, copies), str(HERE / "tb_cdc_pub.sv"),
                            "-o", "Vtb_cdc_pub"], cwd=HERE, capture_output=True, text=True)
    if build.returncode != 0:
        return "BUILD", build.stderr[-400:]
    run = subprocess.run([str(work / "obj" / "Vtb_cdc_pub")], capture_output=True, text=True)
    failed = [line for line in run.stdout.splitlines() if "[FAIL]" in line]
    if run.returncode != 0 and any(arm.needle in line for line in failed):
        return "caught", arm.needle
    return "ESCAPED", f"rc {run.returncode}; {failed[:2]}"


def main() -> int:
    """Every arm, in parallel; one line each, then the tally."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--keep", type=Path, help="keep the scratch builds here")
    args = parser.parse_args()
    flags = vflags()
    with tempfile.TemporaryDirectory(prefix="mbx-cdc-pub-mutants-") as tmp:
        root = args.keep or Path(tmp)
        root.mkdir(parents=True, exist_ok=True)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(lambda arm: (arm, *run_arm(arm, root, flags)), ARMS))
    fixture = any(verdict == "FIXTURE" for _, verdict, _ in results)
    for arm, verdict, detail in results:
        print(f"  [{'ok' if verdict == 'caught' else verdict}] {arm.name}: {detail}")
    caught = sum(verdict == "caught" for _, verdict, _ in results)
    print(f"mbx gPTP publication crossing mutants: {caught} of {len(ARMS)} caught")
    if fixture:
        return 2
    return 0 if caught == len(ARMS) else 1


if __name__ == "__main__":
    sys.exit(main())
