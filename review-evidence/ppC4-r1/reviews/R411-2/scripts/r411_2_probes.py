#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probes for R411-2 on the AS6 quiet-window check of tb/pp_top.

Each probe is one exact edit to hdl/acmp/rom/gen_ltn_rom.py (the listener's
F05.3 ROM), planted by the tree's own tb/pp_top/acmp_mutants.py judge() in an
isolated copy; the tree itself is never touched.

  P1 unbind_then_probe_A5   UNBIND_RX in SETTLED_RSV_OK also runs A5: a fresh
                            PROBE_TX leaves AFTER the UNBIND_RX_RESPONSE (A5 is
                            last in the listener's canonical action order).
  P2 unbind_then_probe_A13  UNBIND_RX in SETTLED_RSV_OK also runs A13: the
                            duplicate PROBE_TX leaves BEFORE the response (A13
                            precedes A7 in the canonical order).

`--bench-next` adds a scratch bench edit to every copy (and to the golden):
AS6 reads the UNBIND_RX_RESPONSE as the next ACMP frame (wait_any) instead
of skipping to it (wait_acmp), so a frame emitted before it is graded.

`--named` grades P1 on the round-2 check alone; without it a probe is KILLED
when any check fails (checks=()), and every failing check is recorded.

Usage: python3 r411_2_probes.py --tree TREE --tag TAG --output DIR
                                --verilator V [--only P1 P2] [--golden]
                                [--named] [--bench-next] [--suite pp_top|acmp_listener]

A copy whose edits are only the bench edit (--golden --bench-next) is judged
by judge()'s mutant rule, so its PASS reads as SURVIVED with run_rc 0 and no
failing check.
"""

import argparse
import importlib.util
import json
from pathlib import Path

ROM = "hdl/acmp/rom/gen_ltn_rom.py"
SOK_UNBIND = '"UNB/A1 A11 A8 A9 A10 A7"]),'
NEW_CHECK = "AS6: no ACMP frame from the UNBIND_RX_RESPONSE to the GET_RX_STATE"
BENCH = "tb/pp_top/sim_main.cpp"
BENCH_OLD = ("                       0, 0, 0x4815, 0, 0));\n"
             "    auto u = wait_acmp(9, 0x4815, 400);\n")
BENCH_NEW = ("                       0, 0, 0x4815, 0, 0));\n"
             "    auto u = h2.wait_any(h2.q_acmp, 400);\n")
PROBES = {
    "P1": ("unbind_then_probe_A5", '"UNB/A1 A11 A8 A9 A10 A7 A5"]),'),
    "P2": ("unbind_then_probe_A13", '"UNB/A1 A11 A8 A9 A10 A13 A7"]),'),
}


def load(root: Path):
    """Import the mutation driver (its judge and suite table) from a tree."""
    spec = importlib.util.spec_from_file_location("acmp_mutants",
                                                  root / "tb/pp_top/acmp_mutants.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verilator", required=True)
    parser.add_argument("--only", nargs="*", default=sorted(PROBES))
    parser.add_argument("--named", action="store_true")
    parser.add_argument("--golden", action="store_true")
    parser.add_argument("--bench-next", action="store_true")
    parser.add_argument("--suite", choices=("pp_top", "acmp_listener"), default="pp_top")
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    root = args.tree.resolve()
    am = load(root)
    work = (root, out, args.verilator)
    suite = am.PP_TOP if args.suite == "pp_top" else am.ACMP_LISTENER
    records = []
    bench = ((BENCH, BENCH_OLD, BENCH_NEW),) if args.bench_next else ()
    sfx = "-benchnext" if args.bench_next else ""
    if args.golden:
        records.append(am.judge(f"golden{sfx}-{args.suite}@{args.tag}", suite, bench, (), work))
    for key in args.only:
        name, new = PROBES[key]
        checks = (NEW_CHECK,) if args.named else ()
        label = f"{key}-{name}{'-named' if args.named else ''}{sfx}-{args.suite}@{args.tag}"
        records.append(am.judge(label, suite, ((ROM, SOK_UNBIND, new),) + bench,
                                checks, work))
    for r in records:
        print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "build_rc", "run_rc",
                                                "completed", "missing", "failing_checks")}))
    name = f"results-{args.suite}-{args.tag}{'-named' if args.named else ''}{sfx}.json"
    (out / name).write_text(json.dumps(records, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
