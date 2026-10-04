#!/usr/bin/env python3
"""R463-2: plant the prior external review's (R463-1) published arm-port controls in the head.

usage: aq_prior_r463_1.py --trees DIR --extract R463_1_SCRIPTS/armq_lockstep/extract.py
                          --work DIR --out DIR [--jobs N]

R463-1's MUTANTS table is imported unchanged and each edit planted once, exact-match,
in protocol_processor_top.sv of a head copy; each run is `--arm-queue-only`. Every
control must fail; `probe_head_unreset` (an equivalence probe) must pass. Reuses
aq_matrix.py's helpers; same environment.
"""
import argparse
import concurrent.futures
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aq_matrix  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trees", type=Path, required=True)
    ap.add_argument("--extract", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    args.r462 = None
    args.out.mkdir(parents=True, exist_ok=True)
    args.work.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("r463_1_extract", args.extract)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    jobs = [{"name": f"r463_1_{n}", "kind": "plant", "hdl": "head", "tb": "head", "edit": e,
             "expect": "pass" if n.startswith("probe_") else "fail"}
            for n, e in mod.MUTANTS.items()]
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda j: aq_matrix.run_job(j, args), jobs))
    ok = True
    for r in results:
        r["as_expected"] = (r["rc"] != 0) == (r["expect"] == "fail")
        ok &= r["as_expected"]
        print(f"{r['name']:<32} rc={r['rc']:<5} expect={r['expect']:<4} "
              f"{'OK' if r['as_expected'] else 'UNEXPECTED'}")
    (args.out / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    print("ALL AS EXPECTED" if ok else "SOME UNEXPECTED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
