#!/usr/bin/env python3
"""Scratch probe for AS6's new quiet-window check (not part of the tree).

It plants one listener defect: UNBIND_RX in SETTLED_RSV_OK also runs A5, so the
unbound sink sends one PROBE_TX right after its UNBIND_RX_RESPONSE; T-ACMP-CMD
then expires in UNBOUND, an impossible (inert) cell, so nothing else follows.
The same defect is graded by the round-1 bench and by the new one, each with the
driver's own judge().

Usage: python3 as6_probe.py --driver TREE --old OLD_TREE --new NEW_TREE --output DIR
"""

import argparse
import importlib.util
import json
from pathlib import Path


def load(root: Path):
    """Import the driver (its judge and suite table) from a tree."""
    spec = importlib.util.spec_from_file_location("acmp_mutants", root / "tb/pp_top/acmp_mutants.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--driver", type=Path, required=True)
    parser.add_argument("--old", type=Path, required=True)
    parser.add_argument("--new", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    am = load(args.driver.resolve())
    edits = (("hdl/acmp/rom/gen_ltn_rom.py", '"UNB/A1 A11 A8 A9 A10 A7"]),',
              '"UNB/A1 A11 A8 A9 A10 A7 A5"]),'),)
    new_check = "AS6: no ACMP frame from the UNBIND_RX_RESPONSE to the GET_RX_STATE"
    records = []
    for tag, root in (("round1-a9ce0fa", args.old), ("round2", args.new)):
        r = am.judge(f"probe-unbind-then-probe@{tag}", am.PP_TOP, edits, (new_check,),
                     (root.resolve(), out, "verilator", 3600.0))
        records.append(r)
        print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "build_rc", "run_rc",
                                                "completed", "missing", "failing_checks")}))
    for tag, root in (("round1-a9ce0fa", args.old), ("round2", args.new)):
        r = am.judge(f"probe-golden@{tag}", am.PP_TOP, (), (), (root.resolve(), out, "verilator",
                                                                3600.0))
        records.append(r)
        print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "failing_checks")}))
    (out / "as6_probe_results.json").write_text(json.dumps(records, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
