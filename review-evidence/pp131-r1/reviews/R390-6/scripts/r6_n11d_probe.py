#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R390-6 probe: N11d's readings, its non-vacuity, and its reach.

Disposable, reviewer-owned. Uses the tree's own tb/pp_top/d3_mutants.judge to
build isolated copies of tb/acmp_nvm. Every copy carries one print-only edit
(R6PRINT) that prints N11d's monitor counts after its CHECK, so the golden's
readings (owned cycles, cycles with manager 1's abort, READs, the fewest owned
cycles before a READ's end, issue cycles with the abort) are visible.

Runs:
  print-head             the print only (must pass 360 of 360)
  cross_own_byte         manager 0's owned term also takes manager 1's abort,
                         but only while a byte is in hand (p_rvalid_i)
  cross_own_nobyte       ...only while no byte is in hand
  h_no_abort_at_end      harness edit: manager 1's abort is withheld in the
                         cycle the port ends the READ (N11d's equality must fail)
  h_abort_in_issue_too   harness edit: N11d also presents the abort in each
                         READ's issue cycle (N11d's 0-of-8 must fail)
The arbiter edits must fail N11d; the harness edits must fail N11d on the
head's arbiter (the check's non-vacuity terms are live).

Usage: python3 r6_n11d_probe.py --tree CLONE --output DIR --verilator V
"""

import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path

SIM = "tb/acmp_nvm/sim_main.cpp"
ARB = "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv"
N11D = "N11d manager 1's abort held while manager 0 owns each of the walk's READs"

PRINT = (
    (SIM, "          nvm.c_str());\n  }\n}\n\nint Harness::report() {\n",
     "          nvm.c_str());\n"
     "    printf(\"R6PRINT N11d owned_cyc=%d with_m1_abort=%d reads_ended=%d span_min=%d \"\n"
     "           \"issues=%d issues_with_m1_abort=%d drain_on=%ld aborts=%d leaks=%d\\n\",\n"
     "           m0_own_cyc, m0_own_cyc_m1_abort, m0_own_rds, m0_own_span_min,\n"
     "           m0_rd_issues, m0_rd_issues_m1_abort, drain_on, aborts, drain_leaks);\n"
     "  }\n}\n\nint Harness::report() {\n"),
)


def arm(d3, a0_own):
    return ((ARB, d3.ARMS,
             "  assign arm0_w = (iss0_w && !m0_we_i && m0_abort_i)\n"
             f"                  || ((own_r == O_M0) && !we_r && ({a0_own}));\n"
             "  assign arm1_w = (iss1_w && !m1_we_i && m1_abort_i)\n"
             "                  || ((own_r == O_M1) && !we_r && m1_abort_i);\n"),)


H_END = ((SIM, "                    || (m1_abort_over_m0 && m0_rd_own)\n",
          "                    || (m1_abort_over_m0 && m0_rd_own && !d->arb_end_o)\n"),)
H_ISSUE = ((SIM, "    m1_abort_over_m0 = true;\n    go();\n",
            "    m1_abort_over_m0 = true;\n    m1_abort_on_m0 = true;\n    go();\n"),)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verilator", default="verilator")
    args = parser.parse_args()
    tree = args.tree.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("d3_mutants", tree / "tb/pp_top/d3_mutants.py")
    d3 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d3)
    runs = (
        ("print-head", PRINT, ()),
        ("cross_own_byte", PRINT + arm(d3, "m0_abort_i || (m1_abort_i && p_rvalid_i)"), (N11D,)),
        ("cross_own_nobyte", PRINT + arm(d3, "m0_abort_i || (m1_abort_i && !p_rvalid_i)"), (N11D,)),
        ("h_no_abort_at_end", PRINT + H_END, (N11D,)),
        ("h_abort_in_issue_too", PRINT + H_ISSUE, (N11D,)),
    )
    records = []
    with concurrent.futures.ThreadPoolExecutor(5) as pool:
        futures = [pool.submit(d3.judge, n, d3.ACMP_NVM, e, c, (tree, output, args.verilator))
                   for n, e, c in runs]
        for f in concurrent.futures.as_completed(futures):
            r = f.result()
            log = (output / f"{r['mutant']}.log").read_text(errors="replace")
            r["print"] = [l for l in log.splitlines() if l.startswith("R6PRINT")]
            r["tally"] = [l for l in log.splitlines() if " checks: " in l]
            records.append(r)
    records.sort(key=lambda r: r["mutant"])
    for r in records:
        # the print-only copy is judged as a mutant by the driver (edits are
        # non-empty), so its PASS reads as "SURVIVED" with run_rc 0
        verdict = ("PASS" if r["mutant"] == "print-head" and r.get("run_rc") == 0
                   and not r.get("failing_checks") else r.get("verdict"))
        print(json.dumps({"run": r["mutant"], "verdict": verdict, "run_rc": r.get("run_rc"),
                          "tally": r["tally"], "print": r["print"],
                          "failing": [x[:160] for x in r.get("failing_checks", [])]}), flush=True)
    (output / "results.json").write_text(json.dumps(records, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
