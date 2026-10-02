#!/usr/bin/env python3
"""R421-3 disposable probe mutants on the identify press latch (reviewer-owned).

Reuses the lane's own driver (tb/pp_top/notify_mutants.py at the reviewed head)
for copying, planting, building, running and grading. --root must be a scratch
tree with r421_3_random.py applied, so every run also executes the reviewer's
seeded random-press probe (checks R421R1..R421R5, default seed, no stalls)
after section ID's own arms. Each mutant is judged twice from one run: against
section ID's own checks (named prefix "ID") and against the probe ("R421R").

Usage: python3 r421_3_probes.py --root TREE --output DIR --verilator V [--jobs N]
"""
import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path


def load(root: Path):
    spec = importlib.util.spec_from_file_location(
        "notify_mutants", root / "tb/pp_top/notify_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


WAIT_CLR = ("              prs_r  <= 1'b0;\n              i_st_r <= I_SEND;\n"
            "            end\n          end\n          I_SEND: begin\n")
HOLD_CLR = ("              prs_r  <= 1'b0;\n              i_st_r <= I_SEND;\n"
            "            end\n          end\n          default:")
WAIT_REL = ("              ix_r   <= 2'd0;\n              rel_r  <= 1'b0;\n"
            "              prs_r  <= 1'b0;\n              i_st_r <= I_SEND;\n"
            "            end\n          end\n          I_SEND: begin\n")


def probes(nm):
    M, IDENT, NTFY = nm.Mutant, nm.IDENT, nm.NTFY
    return (
        # the HOLD start leaves a latched press set: a spurious burst later
        M("p_hold_keeps_prs", IDENT, ((NTFY, HOLD_CLR, HOLD_CLR.replace("              prs_r  <= 1'b0;\n", "", 1)),), ("ID",)),
        # the WAIT start leaves a latched press set: a burst after every latched one
        M("p_wait_keeps_prs", IDENT, ((NTFY, WAIT_CLR, WAIT_CLR.replace("              prs_r  <= 1'b0;\n", "", 1)),), ("ID",)),
        # the in-burst latch without the release qualifier: a held button latches
        M("p_burst_latch_no_rel", IDENT, ((NTFY, nm.BURST_LATCH,
           "        if (btn_q2_r && (i_st_r != I_WAIT)) prs_r <= 1'b1;\n"),), ("ID",)),
        # a stale release flag from an earlier burst survives the WAIT start
        M("p_wait_keeps_rel", IDENT, ((NTFY, WAIT_REL, WAIT_REL.replace("              rel_r  <= 1'b0;\n", "", 1)),), ("ID",)),
        # expected equivalent: WAIT latches without its gap qualifier (the
        # start's own clear wins when the gap is over)
        M("p_wait_latch_always", IDENT, ((NTFY, nm.LATCH, "            if (btn_q2_r) prs_r <= 1'b1;\n"),), ("ID",)),
        # the lane's round-3 controls, judged also by the reviewer's probe
        M("c_press_not_latched", IDENT, ((NTFY, nm.LATCH, ""),), ("ID",)),
        M("c_burst_press_not_latched", IDENT, ((NTFY, nm.BURST_LATCH, ""),), ("ID",)),
        M("c_wait_ignores_gap", IDENT, ((NTFY, nm.WAIT,
           "            if (btn_q2_r || prs_r) begin\n              job_r  <= 1'b1;\n"),), ("ID",)),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args()
    nm = load(a.root.resolve())
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = (a.root.resolve(), out, a.verilator)
    chosen = list(probes(nm))
    records = [nm.judge(g, work) for g in nm.goldens(chosen)]
    for r in records:
        print(json.dumps({k: r[k] for k in ("mutant", "verdict")}), flush=True)
    if all(r["verdict"] == "PASS" for r in records):
        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as pool:
            for fut in concurrent.futures.as_completed([pool.submit(nm.judge, m, work) for m in chosen]):
                r = fut.result()
                fails = r.get("failing_checks", [])
                ids = sorted({f.split(":")[0] for f in fails if f.startswith("ID")})
                rnd = sorted({f.split(":")[0] for f in fails if f.startswith("R421R")})
                r["section_id_failing"] = ids
                r["probe_failing"] = rnd
                records.append(r)
                print(json.dumps({"mutant": r["mutant"], "build_rc": r.get("build_rc"),
                                  "completed": r.get("completed"),
                                  "section_ID": "KILLED" if ids and r.get("completed") else "SURVIVED",
                                  "ID_failing": ids,
                                  "probe": "KILLED" if rnd and r.get("completed") else "SURVIVED",
                                  "probe_failing": rnd}), flush=True)
    (out / "results.json").write_text(json.dumps(records, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
