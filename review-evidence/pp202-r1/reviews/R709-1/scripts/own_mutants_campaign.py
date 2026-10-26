#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer (R709-1) mutants graded by the repository's own suites, through the
repository's own judge in tb/pp_top/acmp_mutants.py (same isolation and verdict
rules). The tree passed as --root is copied, never modified.

Usage: python3 -I own_mutants_campaign.py --root TREE --output DIR --verilator V [--jobs N]
"""
import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", default="verilator")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("acmp_mutants", a.root / "tb/pp_top/acmp_mutants.py")
    am = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(am)
    talker = "hdl/acmp/KL_acmp_talker.sv"
    upper = ((talker, "        {cfg_stream_id_i[g*64+16 +: 48],\n", "        {cfg_stream_id_i[16 +: 48],\n"),)
    pp_acmp = am.Suite("tb/pp_top", ("make", "gsi-build"), ("./obj_dir/Vpp_top_sim", "--acmp-only"))
    mutants = [
        am.Mutant("own_pub_upper_slot0", am.ACMP_TALKER, upper, ()),
        am.Mutant("own_pub_upper_slot0", am.PP_TOP_MAAP, upper, ()),
        am.Mutant("own_pub_upper_slot0", pp_acmp, upper, ()),
    ]
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = (a.root.resolve(), out, a.verilator)
    suites = {(m.suite.directory, m.suite.run): m.suite for m in mutants}
    records = [am.judge(am.golden_label(s), s, (), (), work) for _, s in sorted(suites.items())]
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        futs = [pool.submit(am.judge, am.label_of(m), m.suite, m.edits, m.checks, work) for m in mutants]
        for f in concurrent.futures.as_completed(futs):
            records.append(f.result())
    for r in records:
        print(json.dumps({"mutant": r["mutant"], "verdict": r["verdict"], "run_rc": r.get("run_rc"),
                          "completed": r.get("completed"), "failing": len(r.get("failing_checks", [])),
                          "first_failing": r.get("failing_checks", [])[:4]}))
    (out / "results.json").write_text(json.dumps(records, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
