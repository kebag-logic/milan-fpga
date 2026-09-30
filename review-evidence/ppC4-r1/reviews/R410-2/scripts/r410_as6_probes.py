#!/usr/bin/env python3
"""R410-2 reviewer probes of AS6's round-2 quiet-window grading (tb/pp_top).

Each probe plants one listener transition-ROM defect with the exact-edit and
judge() machinery of the tree's own tb/pp_top/acmp_mutants.py (imported from
--driver), and grades it against the round-1 bench (--old) and the round-2
bench (--new). A golden of each bench runs first.

  P2 unbind_emits_getrx_answer: UNBIND_RX in SETTLED_RSV_OK also runs A16, so
     the unbound sink emits one extra ACMP frame after its UNBIND_RX_RESPONSE
     (not a probe; a GET_RX_STATE_RESPONSE-type frame for the unbind's seq).
  P4 getrx_unbound_also_probes: GET_RX_STATE in UNBOUND also runs A5, so a
     PROBE_TX leaves beside the GET_RX_STATE_RESPONSE.
  With --strict (round-2 bench only): the same bench with one scratch edit,
  AS6 reading its UNBIND_RX_RESPONSE as the next ACMP frame (wait_any) rather
  than skipping non-matching frames; a golden of that bench and P2 on it.

Usage: r410_as6_probes.py --driver TREE --old TREE --new TREE --output DIR
       --verilator V [--jobs N] [--strict]
"""
import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path

ROM = "hdl/acmp/rom/gen_ltn_rom.py"
PROBES = {
    "P2_unbind_emits_getrx_answer": (
        ((ROM, '"UNB/A1 A11 A8 A9 A10 A7"]),', '"UNB/A1 A11 A8 A9 A10 A7 A16"]),'),),
        ("AS6: no ACMP frame from the UNBIND_RX_RESPONSE to the GET_RX_STATE",)),
    "P4_getrx_unbound_also_probes": (
        ((ROM, '("GETRX", ["UNB/A16",', '("GETRX", ["UNB/A5 A16",'),),
        ("AS6: GET_RX_STATE unbound",)),
}

BENCH = "tb/pp_top/sim_main.cpp"
STRICT = ((BENCH, "auto u = wait_acmp(9, 0x4815, 400);", "auto u = h2.wait_any(h2.q_acmp, 400);"),)
STRICT_JOBS = {
    "strict_golden": (STRICT, ()),
    "P2_unbind_emits_getrx_answer+strict": (
        PROBES["P2_unbind_emits_getrx_answer"][0] + STRICT,
        ("AS6: UNBIND_RX_RESPONSE SUCCESS byte-exact",)),
}


def load(root: Path):
    spec = importlib.util.spec_from_file_location("acmp_mutants", root / "tb/pp_top/acmp_mutants.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ap = argparse.ArgumentParser()
    for a in ("--driver", "--old", "--new", "--output"):
        ap.add_argument(a, type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    am = load(args.driver.resolve())
    benches = (("round1-a9ce0fa", args.old.resolve()), ("round2-616cbdf", args.new.resolve()))
    if args.strict:
        jobs = [(f"{name}@{benches[1][0]}", edits, checks, benches[1][1])
                for name, (edits, checks) in STRICT_JOBS.items()]
    else:
        jobs = [(f"golden@{tag}", (), (), root) for tag, root in benches]
        jobs += [(f"{name}@{tag}", edits, checks, root)
                 for name, (edits, checks) in PROBES.items() for tag, root in benches]
    records = []
    with concurrent.futures.ThreadPoolExecutor(max(1, args.jobs)) as pool:
        futs = [pool.submit(am.judge, label, am.PP_TOP, edits, checks,
                            (root, out, args.verilator)) for label, edits, checks, root in jobs]
        for f in futs:
            r = f.result()
            records.append(r)
            print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "run_rc", "completed",
                                                    "missing", "failing_checks")}), flush=True)
    (out / ("results-strict.json" if args.strict else "results.json")).write_text(json.dumps(records, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
