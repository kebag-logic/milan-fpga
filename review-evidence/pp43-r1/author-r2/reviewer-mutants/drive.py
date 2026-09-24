#!/usr/bin/env python3
"""Drive a reviewer's mutant script, unchanged, over a tree whose sites moved.

usage: drive.py r294 <extra_mutants.py> <tree> <scratch> <out> <verilator>
       drive.py r295 <r295_mutants.py> <tree> <scratch> <out> <verilator> [only]

The reviewer's module is imported as published and its own main() does every
copy, edit, build, run and verdict. Only its MUTANTS list is replaced: each
published entry whose exact site still exists at <tree> is kept byte for byte;
an entry whose site is gone is reported as such, and where the mutated
behaviour still exists it is re-expressed on the new site under a name ending
in "~translated" (listed below, never mixed with the unchanged ones).
"""
import importlib.util
import json
import sys
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
SRP = "hdl/srp/KL_srp_listener_fsm.sv"

FCHG_OLD = "if (ind_fchg_w[s]) evt_tk_fail_chg_o[s]   <= 1'b1;"
FCHG_NEW = "if (1'b0) evt_tk_fail_chg_o[s]   <= 1'b1;"
GUARD_OLD = "if (32'(gsi_desc_index_o) < N_STREAM_IN_P) begin"

# name of the published entry -> (why its site is gone, translation or None)
R294 = {
    "srp-failure-strobe-removed": (
        "the FailureInformation term left ind_reg_w for its own strobe",
        (SRP, FCHG_OLD, FCHG_NEW, 1,
         "changed FailureInformation no longer strobes the notification")),
    "sel4-integrator-byte": (
        "gsi_fail_code_r (the sample) became the live gsi_fail_code_w",
        (TOP, "4'd4: aecp_gsi_data_w = {gsi_data_i[63:16], gsi_fail_code_w, 8'd0};",
         "4'd4: aecp_gsi_data_w = gsi_data_i;", 1,
         "selector-4 failure-code byte back on the integrator path")),
    "live-unsampled-fields": (
        "the selector-0 sample is removed; reading live IS the design", None),
    "index-guard-removed": (
        "the guard now precedes the live reads, not the sample registers",
        (TOP, GUARD_OLD, "if (1'b1) begin", 1,
         "descriptor index no longer range-checked before narrowing")),
}
R295 = {
    "sample-transparent": (
        "the selector-0 sample-and-hold is removed", None),
    "sample-transparent-full": (
        "the selector-0 sample-and-hold is removed", None),
    "srp-failure-change-strobe-removed": (
        "the FailureInformation term left ind_reg_w for its own strobe",
        (SRP, FCHG_OLD, FCHG_NEW, 1, "gi")),
}


def main() -> int:
    who, script, tree, scratch, out, verilator = sys.argv[1:7]
    only = sys.argv[7] if len(sys.argv) > 7 else ""
    spec = importlib.util.spec_from_file_location("reviewer", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    table = R294 if who == "r294" else R295
    keep, report = [], []
    for entry in mod.MUTANTS:
        name, rel, old = entry[0], entry[1], entry[2]
        found = (Path(tree) / rel).read_text().count(old) if old else 0
        if (not old) or found == entry[4]:
            keep.append(entry)
            report.append({"mutant": name, "site": "applies unchanged"})
            continue
        why, tr = table[name]
        report.append({"mutant": name, "site": f"gone ({found} found)",
                       "why": why, "translated": tr is not None})
        if tr is not None:
            rel2, old2, new2, count2, last = tr
            keep.append((name + "~translated", rel2, old2, new2, count2, last))
    Path(out).mkdir(parents=True, exist_ok=True)
    (Path(out) / "sites.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report), flush=True)
    mod.MUTANTS = keep
    if who == "r294":
        sys.argv = [script, tree, scratch, out, verilator]
    else:
        sys.argv = [script, "--src", tree, "--work", scratch, "--out", out,
                    "--verilator", verilator]
        if only:
            sys.argv += ["--only", only]
    rc = mod.main()
    return int(rc or 0)


if __name__ == "__main__":
    raise SystemExit(main())
