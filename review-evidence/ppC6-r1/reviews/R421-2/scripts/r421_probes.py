#!/usr/bin/env python3
"""R421-2 disposable probe mutants for the identify schedule (reviewer-owned).

Reuses the lane's own driver (tb/pp_top/notify_mutants.py at the reviewed head)
for copying, planting, building, running and grading, so a probe is judged
exactly like the lane's controls: KILLED only when the build succeeds, the run
completes with its tally, exits non-zero and every named check fails.

Each probe plants into a private temporary copy; the tree given by --root is
only read.

Usage: python3 r421_probes.py --root TREE --output DIR --verilator V [--jobs N]
                             [--set probes|arms]   (arms: TREE has r421_arms.py applied)
"""
import argparse
import importlib.util
import json
from pathlib import Path
import concurrent.futures


def load(root: Path):
    spec = importlib.util.spec_from_file_location(
        "notify_mutants", root / "tb/pp_top/notify_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def probes(nm):
    M, IDENT, NTFY, TOP = nm.Mutant, nm.IDENT, nm.NTFY, nm.TOP
    return (
        # the WAIT start's gap alone (ident_next_burst_at_once drops WAIT and HOLD)
        M("p_wait_gap_dropped", IDENT, (
            (NTFY, nm.WAIT, "          I_WAIT: if (btn_q2_r) begin\n            job_r  <= 1'b1;\n"),),
          ("ID",)),
        # the HOLD start's gap alone
        M("p_hold_gap_dropped", IDENT, (
            (NTFY, nm.HOLD_GO, "            end else if (rel_r || fired_r || exp_r_w) begin\n"),),
          ("ID",)),
        # BURST deadline one tick short: due T-IDENT-BURST after the departure's ms
        M("p_burst_deadline_150", IDENT, (
            (NTFY, nm.BURST_DL,
             "    assign id_arm_deadline_w = armb_r ? now_ms_i + 32'(IDENT_BURST_MS_C)\n"),),
          ("ID",)),
        # REARM one tick short: t0 at the departure's own ms, not the next boundary
        M("p_t0_same_ms", IDENT, (
            (NTFY, nm.T0, "                t0_r    <= now_ms_i;\n"),),
          ("ID",)),
        # top: busy cleared by any eof beat even while the MAC refuses it
        M("p_busy_clear_without_ready", IDENT, (
            (TOP, "      else if (arb_tx_valid_w && arb_tx_eof_w && arb_tx_ready_w)\n",
                  "      else if (arb_tx_valid_w && arb_tx_eof_w)\n"),),
          ("ID",)),
        # top: busy cleared at the first byte the MAC takes (sof), not the last
        M("p_busy_clear_at_sof", IDENT, (
            (TOP, "      else if (arb_tx_valid_w && arb_tx_eof_w && arb_tx_ready_w)\n",
                  "      else if (arb_tx_valid_w && arb_tx_sof_w && arb_tx_ready_w)\n"),),
          ("ID",)),
    )


def arm_probes(nm):
    """With r421_arms.py applied to --root: the two probes the arms target."""
    M, IDENT, NTFY, TOP = nm.Mutant, nm.IDENT, nm.NTFY, nm.TOP
    return (
        M("a_busy_clear_without_ready", IDENT, (
            (TOP, "      else if (arb_tx_valid_w && arb_tx_eof_w && arb_tx_ready_w)\n",
                  "      else if (arb_tx_valid_w && arb_tx_eof_w)\n"),),
          ("R421a:", "R421b:")),
        M("a_wait_gap_dropped", IDENT, (
            (NTFY, nm.WAIT, "          I_WAIT: if (btn_q2_r) begin\n            job_r  <= 1'b1;\n"),),
          ("R421d:",)),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--set", choices=("probes", "arms"), default="probes")
    a = ap.parse_args()
    nm = load(a.root.resolve())
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = (a.root.resolve(), out, a.verilator)
    chosen = list(probes(nm) if a.set == "probes" else arm_probes(nm))
    records = [nm.judge(g, work) for g in nm.goldens(chosen)]
    for r in records:
        print(json.dumps({k: r[k] for k in ("mutant", "verdict")}), flush=True)
    if all(r["verdict"] == "PASS" for r in records):
        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as pool:
            for fut in concurrent.futures.as_completed([pool.submit(nm.judge, m, work) for m in chosen]):
                r = fut.result()
                records.append(r)
                print(json.dumps({"mutant": r["mutant"], "verdict": r["verdict"],
                                  "failing": [f.split(":")[0] for f in r.get("failing_checks", [])]}),
                      flush=True)
    (out / "results.json").write_text(json.dumps(records, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
