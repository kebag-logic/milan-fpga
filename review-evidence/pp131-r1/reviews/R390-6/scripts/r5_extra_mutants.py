#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned arbiter controls for processor PR #132 round 5 (R390-5).

Imports the tree's own tb/pp_top/d3_mutants.py (its plant/copy/judge machinery,
unchanged) and plants reviewer edits of KL_pp_nvm_mgr_arb's drain-arm terms in
isolated copies. Each edit is run against tb/acmp_nvm and tb/pp_top (--d3-only).
A mutant a suite does not kill is reported SURVIVED there; that is the data point,
not an error.

Usage: python3 r5_extra_mutants.py --tree CLONE --output DIR --verilator V [--jobs N]
       [--only NAME ...] [--suites acmp_nvm pp_top pp_top_full]
"""

import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path


def load_driver(tree: Path):
    """Load the tree's mutation driver as a module, without running it."""
    spec = importlib.util.spec_from_file_location("d3_mutants", tree / "tb/pp_top/d3_mutants.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def edits(d3):
    """The reviewer edits, each replacing the head's four drain-arm lines."""
    arms = d3.ARMS

    def arm(a0_iss, a0_own, a1_iss, a1_own):
        return (("hdl/packet_engine/KL_pp_nvm_mgr_arb.sv", arms,
                 f"  assign arm0_w = (iss0_w && !m0_we_i && ({a0_iss}))\n"
                 f"                  || ((own_r == O_M0) && !we_r && ({a0_own}));\n"
                 f"  assign arm1_w = (iss1_w && !m1_we_i && ({a1_iss}))\n"
                 f"                  || ((own_r == O_M1) && !we_r && ({a1_own}));\n"),)

    m0, m1, both = "m0_abort_i", "m1_abort_i", "m0_abort_i || m1_abort_i"
    return {
        # the author's stated by-construction gap: manager 0's abort arms the
        # drain of manager 1's READ in manager 1's issue cycle
        "r5_issue_cross_m1_only": arm(m0, m0, both, m1),
        # the other half of the issue-cycle cross rule (N11b's target)
        "r5_issue_cross_m0_only": arm(both, m0, m1, m1),
        # the OWNED half of the cross rule: manager 1's abort while manager 0
        # owns its READ drains manager 0's READ
        "r5_owned_cross_m0_only": arm(m0, both, m1, m1),
        # manager 0's abort while manager 1 owns its READ drains it
        "r5_owned_cross_m1_only": arm(m0, m0, m1, both),
        # both owned terms take either abort
        "r5_owned_cross_both": arm(m0, both, m1, both),
        # sanity: the head's own text re-planted (must PASS like the golden)
        "r5_identity": arm(m0, m0, m1, m1),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verilator", default="verilator")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--only", nargs="*", default=None)
    parser.add_argument("--suites", nargs="*", default=["acmp_nvm", "pp_top"])
    args = parser.parse_args()
    tree = args.tree.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    d3 = load_driver(tree)
    suites = {"acmp_nvm": d3.ACMP_NVM, "pp_top": d3.PP_TOP,
              # the whole pp_top suite, every section, not only --d3-only
              "pp_top_full": d3.Suite("tb/pp_top", (), ("make", "run"))}
    table = edits(d3)
    names = args.only or list(table)
    work = (tree, output, args.verilator)
    jobs = []
    for sname in args.suites:
        jobs.append(("golden-" + sname, suites[sname], ()))
        for name in names:
            jobs.append((f"{name}@{sname}", suites[sname], table[name]))
    records = []
    with concurrent.futures.ThreadPoolExecutor(max(1, args.jobs)) as pool:
        futures = [pool.submit(d3.judge, n, s, e, ("__any_failure__",) if e else (), work)
                   for n, s, e in jobs]
        for future in concurrent.futures.as_completed(futures):
            r = future.result()
            fails = r.get("failing_checks", [])
            # a reviewer control has no named check: report whether the suite
            # completed and failed anything at all
            r["reviewer_verdict"] = ("PASS" if r["mutant"].startswith("golden-")
                                     and r.get("verdict") == "PASS" else
                                     "BROKEN" if r["mutant"].startswith("golden-") else
                                     "INCOMPLETE" if not r.get("completed") else
                                     "KILLED" if (r.get("run_rc") not in (0, None) and fails)
                                     else "SURVIVED")
            records.append(r)
            print(json.dumps({"mutant": r["mutant"], "verdict": r["reviewer_verdict"],
                              "run_rc": r.get("run_rc"), "failing": len(fails),
                              "first": fails[:3]}), flush=True)
    records.sort(key=lambda r: r["mutant"])
    (output / "results.json").write_text(json.dumps(records, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
