#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer mutation probes against the guard suite and the product-top suite.

Each mutant is a single textual edit applied to a private copy of the exact-head
tree extracted by 00_extract_and_suites.sh.  Product sources in the review clone
are never touched.  A mutant counts as KILLED only when the simulation completes
and prints at least one FAIL line with a nonzero checks-failed tally; a build
failure is reported as BUILD-ERROR, never as a kill.
"""
import argparse
import re
import shutil
import subprocess
from pathlib import Path

GUARD = "hdl/aecp/KL_aecp_desc_mem_guard.sv"
TOP = "hdl/top/protocol_processor_top.sv"
WRAP = "tb/desc_mem_guard/wrap.sv"

MUTANTS = {
    # guard: request faces
    "G1-valid-hold-only-removed": (GUARD, "assign m_req_valid_o = s_req_valid_i && !owed_r;",
                                   "assign m_req_valid_o = s_req_valid_i;", "desc_mem_guard"),
    "G2-ready-hold-only-removed": (GUARD, "assign s_req_ready_o = m_req_ready_i && !owed_r;",
                                   "assign s_req_ready_o = m_req_ready_i;", "desc_mem_guard"),
    # guard: debt clear conditions
    "G3-err-not-terminal": (GUARD, "&& (m_rsp_last_i || m_rsp_err_i)) begin",
                            "&& m_rsp_last_i) begin", "desc_mem_guard"),
    "G4-clear-ignores-ready": (GUARD, "end else if (m_rsp_valid_i && m_rsp_ready_o",
                               "end else if (m_rsp_valid_i", "desc_mem_guard"),
    "G5-clear-ignores-valid": (GUARD, "end else if (m_rsp_valid_i && m_rsp_ready_o",
                               "end else if (m_rsp_ready_o", "desc_mem_guard"),
    "G6-set-ignores-ready": (GUARD, "end else if (m_req_valid_o && m_req_ready_i) begin",
                             "end else if (m_req_valid_o) begin", "desc_mem_guard"),
    "G7-debt-port-tied-0": (GUARD, "assign debt_o = owed_r;", "assign debt_o = 1'b0;",
                            "desc_mem_guard"),
    "G8-never-owed": (GUARD, "      owed_r <= 1'b1;", "      owed_r <= 1'b0;", "desc_mem_guard"),
    # seam: guard reset follows the store-only reset (violates hard-reset-only)
    "W1-guard-reset-follows-store": (WRAP, "KL_aecp_desc_mem_guard u_guard (\n      .clk_i(clk_i), .rst_n(rst_n),",
                                     "KL_aecp_desc_mem_guard u_guard (\n      .clk_i(clk_i), .rst_n(rst_n && store_rst_n),",
                                     "desc_mem_guard"),
    # product top: same mutants seen through the wire-level bench
    "T1-top-hold-removed": (GUARD, None, None, "pp_top"),
    "T2-top-debt-port-tied-0": (GUARD, "assign debt_o = owed_r;", "assign debt_o = 1'b0;", "pp_top"),
}


def apply(tree: Path, name: str) -> None:
    """Apply one mutant in place in a private tree; refuse unless the anchor is unique."""
    path, old, new, _ = MUTANTS[name]
    target = tree / path
    text = target.read_text()
    if old is None:  # both request holds, as the author's control does
        if text.count(" && !owed_r") != 2:
            raise SystemExit(f"{name}: anchor count mismatch")
        target.write_text(text.replace(" && !owed_r", ""))
        return
    if text.count(old) != 1:
        raise SystemExit(f"{name}: anchor count {text.count(old)} != 1")
    target.write_text(text.replace(old, new))


def run(tree: Path, suite: str, verilator: str, log: Path) -> tuple[int, str]:
    """Build and run one suite on 8 cores; return make rc and the classification."""
    cmd = ["taskset", "-c", "0-7", "make", "-C", str(tree / "tb" / suite), f"VERILATOR={verilator}"]
    with log.open("w") as out:
        rc = subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT, timeout=3600).returncode
    text = log.read_text()
    tally = [int(t) for t in re.findall(r"^\d+ checks: \d+ PASS, (\d+) FAIL", text, re.M)]
    # the product-top bench prints one "N checks, M failures" line per build
    tally += [int(t) for t in re.findall(r"^\[build [^\]]*\] \d+ checks, (\d+) failures", text, re.M)]
    fails = [ln for ln in text.splitlines() if ln.startswith("FAIL")]
    if not tally:
        return rc, "BUILD-ERROR-OR-CRASH"
    nfail = sum(tally)
    return rc, ("KILLED" if nfail and fails else "SURVIVED") + f" ({nfail} FAIL; first: {fails[0] if fails else '-'})"


def main() -> int:
    """Run every mutant, or the ones named on the command line, and write a summary."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    head = a.packet / "scratch" / "head"
    rec = a.packet / "receipts" / "mutants"
    rec.mkdir(parents=True, exist_ok=True)
    for name in a.names or list(MUTANTS):
        suite = MUTANTS[name][3]
        tree = a.packet / "scratch" / "mut" / name
        shutil.rmtree(tree, ignore_errors=True)
        shutil.copytree(head, tree, ignore=shutil.ignore_patterns("obj_dir", "obj_*"))
        apply(tree, name)
        diff = subprocess.run(["diff", "-ru", str(head / "hdl"), str(tree / "hdl")],
                              capture_output=True, text=True).stdout
        diff += subprocess.run(["diff", "-u", str(head / WRAP), str(tree / WRAP)],
                               capture_output=True, text=True).stdout
        (rec / f"{name}.diff").write_text(diff.replace(str(a.packet), "$PACKET"))
        rc, verdict = run(tree, suite, a.verilator, rec / f"{name}.log")
        line = f"{name} suite={suite} make_rc={rc} {verdict}"
        print(line, flush=True)
        with (rec / "SUMMARY.txt").open("a") as s:
            s.write(line + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
