#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require the historical late-mark trigger to fail both durability checks."""

from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def run_build(directory: Path, label: str,
              sources: list[Path] | None = None) -> tuple[int, str]:
    """Build and run the real command harness; retain a bounded log tail."""
    command = ["make", "run-pending",
               f"PENDING_BUILD_DIR={directory / label}"]
    if sources is not None:
        command.append("DP_SRCS=" + " ".join(str(path) for path in sources))
    log_path = directory / f"{label}.log"
    # The harness bounds waits in DUT cycles; the caller owns process limits.
    with log_path.open("w") as log:
        result = subprocess.run(command, cwd=HERE, stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    text = log_path.read_text()
    print("\n".join(text.splitlines()[-12:]))
    for line in text.splitlines():
        if "[FAIL]" in line or "[i] K" in line:
            print(line)
    return result.returncode, text


def main() -> None:
    """Require a passing clean build and both named mutant failures."""
    source = ROOT / "hdl/milan/KL_pp_shadow.sv"
    original = source.read_text()
    live = """  assign aecp_live_wr_w = aecp_name_wr_w
                        | (amap_edit_req_o && (amap_edit_phase_o == 3'd5));"""
    late = """  assign aecp_live_wr_w = aecp_nvm_stb_w
                        && ((aecp_nvm_mark_w == 8'd6)
                            || (aecp_nvm_mark_w == 8'd7));"""
    if original.count(live) != 1:
        raise SystemExit("REFUSED: live-trigger mutation anchor changed")
    with tempfile.TemporaryDirectory(prefix="pp-pending-") as temporary:
        directory = Path(temporary)
        rc, text = run_build(directory, "control")
        if rc != 0 or "RESULT: PASS" not in text:
            raise SystemExit("FAIL: clean control did not pass")
        mutant = directory / "hdl/milan/KL_pp_shadow.sv"
        mutant.parent.mkdir(parents=True)
        mutant.write_text(original.replace(live, late))
        listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"],
                                 cwd=HERE, check=True, capture_output=True, text=True)
        sources = [(HERE / path).resolve() for path in listing.stdout.split()]
        if sources.count(source) != 1:
            raise SystemExit("REFUSED: expected exactly one shipping shadow")
        sources = [mutant if path == source else path for path in sources]
        rc, text = run_build(directory, "late-mark", sources)
        required = ("[FAIL] K10 no_durable_claim_over_unsaved",
                    "[FAIL] K12 no_durable_claim_over_unsaved")
        if rc == 0 or "RESULT: FAIL" not in text or not all(s in text for s in required):
            raise SystemExit("FAIL: late-mark mutant missed a named K10/K12 failure")
        if source.read_text() != original:
            raise SystemExit("FAIL: shipping source changed during mutation")
        print("PASS: late-mark mutant killed by K10 and K12; clean control passes")


if __name__ == "__main__":
    main()
