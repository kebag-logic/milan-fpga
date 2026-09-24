#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned mutants, round 2, for the processor-owned GET_STREAM_INFO
fields and their notification triggers.

Usage: r295_mutants2.py --src <clean extracted tree> --work <scratch dir>
                        --out <receipt dir> --verilator <path>
                        [--only a,b] [--jobs N]
Each mutant copies hdl/ and tb/ from --src into its own tree, applies one
exact edit (the edit count is asserted) and runs one bench:
  gi     tb/pp_top default build, --gsi-internal-only
  full   tb/pp_top default build, whole default suite
  lsm    tb/acmp_listener  make run
  srpfsm tb/srp_stream_fsms make run
  srptop tb/srp_top make run
Only a completed simulation counts; a build failure is reported INCOMPLETE.
Round-1 mutants whose site is unchanged are carried over verbatim; sites the
round removed by design are re-expressed on the new code and named -r2.
"""
import argparse, json, shutil, subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
SRP = "hdl/srp/KL_srp_listener_fsm.sv"
LSM = "hdl/acmp/KL_pp_acmp_listener.sv"
MUTANTS = [
    # name, file, old, new, count, mode
    ("golden-gi", TOP, "", "", 0, "gi"),
    ("golden-full", TOP, "", "", 0, "full"),
    # --- round-1 reviewer mutants, sites unchanged, edits verbatim ---------
    ("sink-index-guard-removed", TOP,
     "if (32'(gsi_desc_index_o) < N_STREAM_IN_P) begin", "if (1'b1) begin", 1, "gi"),
    ("status-compare-removed", TOP,
     "(lstn_gsi_status_r[lstn_recwr_sink_w] != lstn_gsi_status_w);", "1'b1;", 1, "gi"),
    ("desc-type-ignored", TOP,
     "&& (gsi_desc_type_o == 16'h0005);", "&& 1'b1;", 1, "full"),
    # --- round-1 site removed by design, re-expressed ----------------------
    ("srp-failure-change-strobe-removed-r2", SRP,
     "ind_fchg_w[s] = fchg_cand_w[s] && rx_registering_w && rx_is_failed_w\n"
     "                   && fchg_diff_w;",
     "ind_fchg_w[s] = 1'b0;", 1, "gi"),
    # --- round-2 reviewer mutants on the new code --------------------------
    ("fail-chg-not-routed-to-notify", TOP,
     "|| srp_evt_tk_fail_chg_w[k];", ";", 1, "gi"),
    ("strt-term-not-routed-to-notify", TOP,
     "&& lstn_act_strt_chg_w && !lstn_act_strt_cmd_chg_w)",
     "&& 1'b0)", 1, "gi"),
    ("status-compare-wrong-sink", TOP,
     "(lstn_gsi_status_r[lstn_recwr_sink_w] != lstn_gsi_status_w);",
     "(lstn_gsi_status_r[0] != lstn_gsi_status_w);", 1, "gi"),
    ("bridge-gate-reads-sink0-state", TOP,
     "if (srp_tk_reg_state_w[gsi_sink_w] == 2'd2) begin",
     "if (srp_tk_reg_state_w[0] == 2'd2) begin", 1, "gi"),
    ("status-view-reads-sink0", TOP,
     "gsi_status_w = lstn_gsi_status_r[gsi_sink_w];",
     "gsi_status_w = lstn_gsi_status_r[0];", 1, "gi"),
    ("fchg-lv-excluded", SRP,
     "fchg_cand_w[s] = reg_rx_hit_w[s] && (reg_r[s] != R_MT_C) && rtype_r[s];",
     "fchg_cand_w[s] = reg_rx_hit_w[s] && (reg_r[s] == R_IN_C) && rtype_r[s];",
     1, "srpfsm"),
    ("fchg-compare-sink0", SRP,
     "fchg_ix_w  = SNK_W_C'(s);", "fchg_ix_w  = '0;", 1, "srpfsm"),
    ("fchg-compare-sink0-gi", SRP,
     "fchg_ix_w  = SNK_W_C'(s);", "fchg_ix_w  = '0;", 1, "gi"),
    ("strt-bound-before-removed", LSM,
     "act_strt_chg_o <= cellmut_r && bnd_was_r && rec_r.f_bound\n",
     "act_strt_chg_o <= cellmut_r && rec_r.f_bound\n", 1, "lsm"),
    ("strt-bound-before-removed-gi", LSM,
     "act_strt_chg_o <= cellmut_r && bnd_was_r && rec_r.f_bound\n",
     "act_strt_chg_o <= cellmut_r && rec_r.f_bound\n", 1, "gi"),
    ("fchg-recoupled-into-reg-srpfsm", SRP,
     "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w));",
     "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w)"
     " || ind_fchg_w[s]);", 1, "srpfsm"),
    ("fchg-recoupled-into-reg-srptop", SRP,
     "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w));",
     "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w)"
     " || ind_fchg_w[s]);", 1, "srptop"),
]

BENCH = {"gi": "tb/pp_top", "full": "tb/pp_top", "lsm": "tb/acmp_listener",
         "srpfsm": "tb/srp_stream_fsms", "srptop": "tb/srp_top"}


def sh(cmd, cwd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                              check=False, timeout=7200).returncode


def one(a, m):
    name, fn, old, new, count, mode = m
    tree = a.work / name
    shutil.rmtree(tree, ignore_errors=True)
    for d in ("hdl", "tb/common", BENCH[mode]):
        shutil.copytree(a.src / d, tree / d,
                        ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
    if old:
        p = tree / fn
        s = p.read_text()
        if s.count(old) != count:
            raise SystemExit(f"{name}: expected {count} edit sites, found {s.count(old)}")
        p.write_text(s.replace(old, new))
    bench = tree / BENCH[mode]
    log = a.out / f"{name}-run.log"
    if mode in ("gi", "full"):
        brc = sh(["make", "gsi-build", "VERILATOR=" + a.verilator], bench,
                 a.out / f"{name}-build.log")
        if brc != 0:
            return {"mutant": name, "mode": mode, "verdict": "INCOMPLETE",
                    "build_rc": brc}
        args = ["./obj_dir/Vpp_top_sim"] + (["--gsi-internal-only"] if mode == "gi" else [])
        rrc = sh(args, bench, log)
        text = log.read_text()
        tally = [l for l in text.splitlines() if l.startswith("[build default")]
    else:
        rrc = sh(["make", "run", "VERILATOR=" + a.verilator], bench, log)
        text = log.read_text()
        tally = [l for l in text.splitlines() if " checks: " in l and " PASS, " in l]
    fails = [l for l in text.splitlines() if l.startswith("FAIL")]
    return {"mutant": name, "mode": mode, "run_rc": rrc, "tally": tally,
            "first_failures": fails[:6], "n_fail_lines": len(fails),
            "verdict": ("KILLED" if rrc != 0 and (tally or fails) else
                        "SURVIVED" if rrc == 0 and tally else "INCOMPLETE")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    todo = [m for m in MUTANTS if not a.only or m[0] in a.only.split(",")]
    with ThreadPoolExecutor(max_workers=min(a.jobs, 8)) as ex:
        results = list(ex.map(lambda m: one(a, m), todo))
    for r in results:
        print(json.dumps(r), flush=True)
    (a.out / "results.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
