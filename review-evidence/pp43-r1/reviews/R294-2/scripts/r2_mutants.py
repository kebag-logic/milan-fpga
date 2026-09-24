#!/usr/bin/env python3
"""R294 round-2 reviewer mutants (disposable copies only).

Usage: r2_mutants.py <source-tree> <scratch-dir> <output-dir> <verilator> [name ...]

Part A re-applies the round-1 R294 mutant list (scripts/extra_mutants.py)
BYTE FOR BYTE: each entry whose exact site still exists is run unchanged; an
entry whose site is gone is reported SITE-GONE and not scored.
Part B are this reviewer's own re-expressions of the gone sites and new
round-2 mutants. Each mutant edits one exact site in a private copy and is
scored on every bench listed for it:
  gi     tb/pp_top  `make gsi-build` then `Vpp_top_sim --gsi-internal-only`
  fsm    tb/srp_stream_fsms  `make`
  srptop tb/srp_top  `make`
  lstn   tb/acmp_listener  `make`
  full   tb/pp_top  `make` (default + fixture builds, every section)
KILLED = build ok, run completed, rc != 0 with >= 1 FAIL line.
SURVIVED = build ok, run completed with 0 failures. Build failures are not
scored.
"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOP = "hdl/top/protocol_processor_top.sv"
SRP = "hdl/srp/KL_srp_listener_fsm.sv"
LSTN = "hdl/acmp/KL_pp_acmp_listener.sv"

# (name, file, old, new, count, benches, intent)
OWN = [
    # -- re-expressions of round-1 sites that are gone at this head --------
    ("r2-srp-failure-notify-dropped-at-top", TOP,
     "          || srp_evt_tk_fail_chg_w[k];",
     "          || 1'b0;", 1, ["gi"],
     "re-expression of srp-failure-strobe-removed: the changed "
     "FailureInformation no longer reaches the notification OR"),
    ("r2-sel4-integrator-byte", TOP,
     "4'd4: aecp_gsi_data_w = {gsi_data_i[63:16], gsi_fail_code_w, 8'd0};",
     "4'd4: aecp_gsi_data_w = gsi_data_i;", 1, ["gi"],
     "re-expression of sel4-integrator-byte on the live code"),
    ("r2-index-guard-removed", TOP,
     "if (32'(gsi_desc_index_o) < N_STREAM_IN_P) begin",
     "if (1'b1) begin", 1, ["gi"],
     "re-expression of index-guard-removed on the live reads"),
    ("r2-index-guard-after-narrowing", TOP,
     "if (32'(gsi_desc_index_o) < N_STREAM_IN_P) begin",
     "if (32'(gsi_sink_w) < N_STREAM_IN_P) begin", 1, ["gi"],
     "guard compares the NARROWED sink index (aliasing survives it)"),
    ("r2-index-guard-off-by-one", TOP,
     "if (32'(gsi_desc_index_o) < N_STREAM_IN_P) begin",
     "if (32'(gsi_desc_index_o) <= N_STREAM_IN_P) begin", 1, ["gi"],
     "boundary: index N_STREAM_IN_P admitted and aliased onto sink 0"),
    # -- round-2 specific ----------------------------------------------------
    ("r2-fchg-code-compare-only", SRP,
     "    fchg_diff_w = (fcode_r[fchg_ix_w] != evt_failure_code_i)\n"
     "               || (fsysid_r[fchg_ix_w] != evt_failure_system_id_i);",
     "    fchg_diff_w = (fcode_r[fchg_ix_w] != evt_failure_code_i);", 1,
     ["gi", "fsm", "srptop"], "a bridge-only FailureInformation change is missed"),
    ("r2-fchg-bridge-compare-only", SRP,
     "    fchg_diff_w = (fcode_r[fchg_ix_w] != evt_failure_code_i)\n"
     "               || (fsysid_r[fchg_ix_w] != evt_failure_system_id_i);",
     "    fchg_diff_w = (fsysid_r[fchg_ix_w] != evt_failure_system_id_i);", 1,
     ["gi", "fsm", "srptop"], "a code-only FailureInformation change is missed"),
    ("r2-fchg-lowest-candidate-only", SRP,
     "      ind_fchg_w[s] = fchg_cand_w[s] && rx_registering_w && rx_is_failed_w",
     "      ind_fchg_w[s] = fchg_cand_w[s] && (fchg_ix_w == SNK_W_C'(s))"
     " && rx_registering_w && rx_is_failed_w", 1,
     ["gi", "fsm"], "only the compared sink of a shared stream is strobed"),
    ("r2-fchg-candidate-includes-mt", SRP,
     "      fchg_cand_w[s] = reg_rx_hit_w[s] && (reg_r[s] != R_MT_C) && rtype_r[s];",
     "      fchg_cand_w[s] = reg_rx_hit_w[s] && rtype_r[s];", 1,
     ["gi", "fsm"], "an MT (unregistered) sink can be the compared candidate"),
    ("r2-fail-code-ungated", SRP,
     "      msrp_fail_code_o[s]   = (tk_reg_state_o[s] == 2'd2) ? fcode_r[s] : 8'd0;",
     "      msrp_fail_code_o[s]   = fcode_r[s];", 1,
     ["gi", "fsm", "srptop"], "failure code no longer gated to FAILED"),
    ("r2-bridge-gate-other-sink", TOP,
     "if (srp_tk_reg_state_w[gsi_sink_w] == 2'd2) begin",
     "if (srp_tk_reg_state_w[0] == 2'd2) begin", 1, ["gi"],
     "bridge gated on sink 0's registration instead of the addressed sink's"),
    ("r2-internal-honours-external-wait", TOP,
     "assign aecp_gsi_wait_w = !gsi_internal_w && gsi_wait_i;",
     "assign aecp_gsi_wait_w = gsi_wait_i;", 1, ["gi"],
     "internal selectors 5/7 honour the integrator's HOLD"),
    ("r2-internal-req-leaks", TOP,
     "assign gsi_req_o = aecp_gsi_req_w && !gsi_internal_w;",
     "assign gsi_req_o = aecp_gsi_req_w;", 1, ["gi"],
     "internal selectors still raise the external request"),
    ("r2-status-view-stale-on-write", TOP,
     "        lstn_gsi_status_r[lstn_recwr_sink_w] <= lstn_gsi_status_w;\n",
     "        if (lstn_gsi_status_r[lstn_recwr_sink_w] == 8'd0)\n"
     "          lstn_gsi_status_r[lstn_recwr_sink_w] <= lstn_gsi_status_w;\n",
     1, ["gi"], "status view keeps its first non-zero value"),
    ("r2-strt-chg-bound-before-removed", LSTN,
     "          act_strt_chg_o <= cellmut_r && bnd_was_r && rec_r.f_bound\n",
     "          act_strt_chg_o <= cellmut_r && rec_r.f_bound\n", 1,
     ["gi", "lstn"], "undefined->started on a fresh bind raises the trigger"),
    ("r2-strt-chg-trigger-dropped-at-top", TOP,
     "           && lstn_act_strt_chg_w && !lstn_act_strt_cmd_chg_w)",
     "           && 1'b0)", 1, ["gi"],
     "the listener's started/stopped pulse no longer reaches the OR"),
    ("r2-desc-type-ignored", TOP,
     "assign gsi_input_w = (gsi_kind_o == 2'd0)\n"
     "                        && (gsi_desc_type_o == 16'h0005);",
     "assign gsi_input_w = (gsi_kind_o == 2'd0);", 1, ["full"],
     "STREAM_OUTPUT selectors 4/5/7 intercepted as if they were inputs"),
]


def load_round1():
    spec = importlib.util.spec_from_file_location("r1", HERE / "extra_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [(n, f, o, w, c, ["gi"], i) for (n, f, o, w, c, i) in mod.MUTANTS]


def sh(cmd, cwd, log):
    with open(log, "w") as out:
        return subprocess.run(cmd, cwd=cwd, stdout=out, stderr=subprocess.STDOUT,
                              timeout=3600).returncode


BENCH = {
    "gi": ("tb/pp_top", [["make", "gsi-build"]],
           ["./obj_dir/Vpp_top_sim", "--gsi-internal-only"]),
    "fsm": ("tb/srp_stream_fsms", [], ["make"]),
    "srptop": ("tb/srp_top", [], ["make"]),
    "lstn": ("tb/acmp_listener", [], ["make"]),
    "full": ("tb/pp_top", [], ["make"]),
}


def score(tree, bench, out, tag, verilator):
    sub, builds, runcmd = BENCH[bench]
    d = tree / sub
    shutil.rmtree(d / "obj_dir", ignore_errors=True)
    brc = 0
    for b in builds:
        brc = sh(b + ["VERILATOR=" + str(verilator)], d, out / f"{tag}-{bench}-build.log")
        if brc:
            return {"bench": bench, "build_rc": brc, "run_rc": None,
                    "verdict": "BUILD-FAIL", "first_failures": []}
    cmd = runcmd + (["VERILATOR=" + str(verilator)] if runcmd[0] == "make" else [])
    log = out / f"{tag}-{bench}-run.log"
    rrc = sh(cmd, d, log)
    t = log.read_text(errors="replace")
    fails = [l for l in t.splitlines() if l.startswith("FAIL")]
    complete = bool(re.search(r"\d+ checks[,:]", t))
    if runcmd[0] == "make" and not complete:
        verdict = "BUILD-FAIL"
    elif complete and rrc != 0 and fails:
        verdict = "KILLED"
    elif complete and rrc == 0 and not fails:
        verdict = "SURVIVED"
    else:
        verdict = "INCONCLUSIVE"
    shutil.rmtree(d / "obj_dir", ignore_errors=True)
    return {"bench": bench, "build_rc": brc, "run_rc": rrc, "verdict": verdict,
            "first_failures": fails[:4]}


def main() -> int:
    src, scratch, output, verilator = map(Path, sys.argv[1:5])
    only = set(sys.argv[5:])
    output.mkdir(parents=True, exist_ok=True)
    plan = [("A", m) for m in load_round1()] + [("B", m) for m in OWN]
    results = []
    for part, (name, rel, old, new, count, benches, intent) in plan:
        if only and name not in only:
            continue
        found = (src / rel).read_text().count(old)
        r = {"part": part, "mutant": name, "file": rel, "intent": intent,
             "sites_found": found}
        if found != count:
            r["verdict"] = "SITE-GONE"
            print(json.dumps(r), flush=True)
            results.append(r)
            continue
        tree = scratch / ("r2m-" + name)
        shutil.rmtree(tree, ignore_errors=True)
        for d in ["hdl", "tb/common"] + [BENCH[b][0] for b in benches]:
            shutil.copytree(src / d, tree / d,
                            ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
        p = tree / rel
        p.write_text(p.read_text().replace(old, new))
        r["benches"] = [score(tree, b, output, name, verilator) for b in benches]
        r["verdict"] = ("KILLED" if any(b["verdict"] == "KILLED" for b in r["benches"])
                        else "SURVIVED" if all(b["verdict"] == "SURVIVED" for b in r["benches"])
                        else "MIXED/INCONCLUSIVE")
        print(json.dumps(r), flush=True)
        results.append(r)
        shutil.rmtree(tree, ignore_errors=True)
    (output / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
