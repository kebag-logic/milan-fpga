#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R390-5 probe: the owned half of "an abort names its own manager's READ only".

Disposable, reviewer-owned. In an isolated copy (the tree's own d3_mutants.judge),
it adds one check, R5P, to tb/acmp_nvm: manager 1 (synthetic, request low) holds
its abort from the strobe of each of the binding walk's READs to that READ's end,
so the abort is present while manager 0 OWNS the READ, not only in its issue cycle
(N11b). The check requires the walk to complete as saved with no drain, and that
the abort was really present in owned cycles (non-vacuity).

Runs three copies: probe on the head's arbiter (must PASS), probe plus
r5_owned_cross_m0_only (must fail R5P), and the unmodified-harness mutant for
reference (survives at the head, the reported gap).

Usage: python3 r5_owned_cross_probe.py --tree CLONE --output DIR --verilator V
"""

import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path

SIM = "tb/acmp_nvm/sim_main.cpp"

HARNESS = (
    (SIM, "  bool m1_abort_on_m0 = false;\n",
     "  bool m1_abort_on_m0 = false;\n"
     "  bool m1_abort_m0_owned = false;   // R5P: held through manager 0's READ\n"
     "  bool m0_rd_live = false;\n"
     "  int m1_abort_m0_owned_cyc = 0;\n"),
    (SIM, "                    || (m1_abort_on_m0 && d->mgr_req_o && !d->mgr_we_o);\n",
     "                    || (m1_abort_on_m0 && d->mgr_req_o && !d->mgr_we_o)\n"
     "                    || (m1_abort_m0_owned && ((d->mgr_req_o && !d->mgr_we_o) || m0_rd_live));\n"),
    (SIM, "    if (d->arb_req_o && d->mgr_req_o && !d->mgr_we_o) {\n      ++m0_rd_issues;\n",
     "    if (m0_rd_live && d->m1_abort_i) ++m1_abort_m0_owned_cyc;\n"
     "    if (d->mgr_done_o || d->mgr_err_o) m0_rd_live = false;\n"
     "    if (d->arb_req_o && d->mgr_req_o && !d->mgr_we_o) {\n      m0_rd_live = true;\n"
     "      ++m0_rd_issues;\n"),
    (SIM, "    m1_abort_hold = false; m1_abort_on_m0 = false;\n",
     "    m1_abort_hold = false; m1_abort_on_m0 = false;\n"
     "    m1_abort_m0_owned = false; m0_rd_live = false; m1_abort_m0_owned_cyc = 0;\n"),
    (SIM, "  {\n    const char* tag = \"N11c a manager-1 READ abandoned in its issue cycle after a WRITE\";\n",
     "  {\n"
     "    const char* tag = \"R5P manager 1's abort held through each of the walk's READs\";\n"
     "    l_seed({{0, L_B0}, {L_LAST, L_B7}});\n"
     "    reset();\n"
     "    m1_abort_m0_owned = true;\n"
     "    go();\n"
     "    l_finish();\n"
     "    m1_abort_m0_owned = false;\n"
     "    std::string why;\n"
     "    std::string nvm;\n"
     "    const bool walk = l_walk_ok(why) && !d->restore_fail_o && d->restore_cause_o == 0;\n"
     "    const bool kept = l_nvm_untouched(nvm);\n"
     "    CHECK(walk && kept && m0_rd_issues == N_SINKS && m1_abort_m0_owned_cyc > N_SINKS\n"
     "              && drain_on < 0 && drain_leaks == 0 && aborts == 0,\n"
     "          \"%s: abort present in %d owned cycles over %d READs, none drained (from %ld), \"\n"
     "          \"the walk completes as saved: %s %s\", tag, m1_abort_m0_owned_cyc, m0_rd_issues,\n"
     "          drain_on, why.c_str(), nvm.c_str());\n"
     "  }\n"
     "  {\n    const char* tag = \"N11c a manager-1 READ abandoned in its issue cycle after a WRITE\";\n"),
)


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
    extra = importlib.util.spec_from_file_location(
        "r5x", Path(__file__).with_name("r5_extra_mutants.py"))
    r5x = importlib.util.module_from_spec(extra)
    extra.loader.exec_module(r5x)
    owned = r5x.edits(d3)["r5_owned_cross_m0_only"]
    work = (tree, output, args.verilator)
    runs = (
        ("probe-head", HARNESS, ()),
        ("probe+r5_owned_cross_m0_only", HARNESS + owned,
         ("R5P manager 1's abort held through each of the walk's READs",)),
        ("tree-harness+r5_owned_cross_m0_only", owned, ("__any__",)),
    )
    records = []
    with concurrent.futures.ThreadPoolExecutor(3) as pool:
        futures = [pool.submit(d3.judge, n, d3.ACMP_NVM, e, c, work) for n, e, c in runs]
        for f in concurrent.futures.as_completed(futures):
            r = f.result()
            records.append(r)
            print(json.dumps({"run": r["mutant"], "verdict": r.get("verdict"),
                              "run_rc": r.get("run_rc"), "completed": r.get("completed"),
                              "missing": r.get("missing"),
                              "failing": [x[:200] for x in r.get("failing_checks", [])]}),
                  flush=True)
    records.sort(key=lambda r: r["mutant"])
    (output / "results.json").write_text(json.dumps(records, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
