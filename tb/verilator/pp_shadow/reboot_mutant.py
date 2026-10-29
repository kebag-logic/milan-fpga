#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require section [RB] to fail on a datapath whose reset ignores REBOOT (#787).

The control builds this suite's base leg twice and runs section [RB] alone
(`--reboot-only`): once from the committed sources, which must pass, and once
with a private copy of milan_datapath.sv in which KL_reboot_ctrl never sees
the processor's request. That copy must fail [RB]'s named check, the PHY hold
two clocks after the request. Mutant logs stay in the private directory.

Exit 0 = the clean control passed and the mutant was caught by its check;
1 = otherwise.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = (ROOT / "hdl" / "milan" / "milan_datapath.sv").resolve()
CONNECTED = "      .reboot_req_i (pp_reboot_req_w),\n"
IGNORED = "      .reboot_req_i (pp_reboot_req_w & 1'b0),\n"
NAMED = "[FAIL] RB the PHY hold rises two clocks after the REBOOT request"


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
    """The clean control, then the mutant; 0 when the mutant was caught."""
    original = SOURCE.read_text()
    if original.count(CONNECTED) != 1:
        print("REFUSED: the request connection anchor changed")
        return 1
    with tempfile.TemporaryDirectory(prefix="pp-reboot-") as temporary:
        directory = Path(temporary)
        status, text = run_leg(directory, "control")
        if status != 0 or "RESULT: PASS" not in text:
            print(f"FAIL: the clean control did not pass [RB] (exit {status})")
            return 1
        print("clean control: [RB] PASS")
        mutant = directory / "hdl" / "milan" / SOURCE.name
        mutant.parent.mkdir(parents=True)
        mutant.write_text(original.replace(CONNECTED, IGNORED))
        listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"],
                                 cwd=HERE, check=True, capture_output=True, text=True)
        sources = [(HERE / path).resolve() for path in listing.stdout.split()]
        if sources.count(SOURCE) != 1:
            print("REFUSED: expected exactly one shipping datapath source")
            return 1
        sources = [mutant if path == SOURCE else path for path in sources]
        status, text = run_leg(directory, "request-ignored", sources)
        caught = status != 0 and "RESULT: FAIL" in text and NAMED in text
        failing = sum(1 for line in text.splitlines() if line.lstrip().startswith("[FAIL]"))
        if SOURCE.read_text() != original:
            print("FAIL: the shipping source changed during the mutation")
            return 1
        if not caught:
            print(f"FAIL: request-ignored SURVIVED (exit {status})")
            return 1
        print(f"request-ignored: KILLED by its named check, {failing} failing checks")
        print(f"  named check: {NAMED[len('[FAIL] '):]}")
    print("PASS: the reset that ignores the REBOOT request is caught by [RB]; "
          "clean control passes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
