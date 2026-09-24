#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned extra mutants for the processor-owned GET_STREAM_INFO fields.

Usage: r295_mutants.py --src <clean extracted tree> --work <scratch dir>
                       --out <receipt dir> --verilator <path>
Each mutant copies hdl/, tb/common, tb/pp_top from --src, applies one exact
edit (the edit count is asserted), builds the default pp_top bench and runs
either the focused GI section or the whole default suite. Only a completed
simulation counts; a build failure aborts the run.
"""
import argparse, json, shutil, subprocess
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
SRP = "hdl/srp/KL_srp_listener_fsm.sv"
MUTANTS = [
    # name, file, old, new, count, mode
    ("golden-gi", TOP, "", "", 0, "gi"),
    ("sample-transparent", TOP,
     "end else if (!aecp_gsi_req_w || !gsi_input_w || (gsi_sel_o != 4'd0)) begin\n"
     "      gsi_sampled_r <= 1'b0;\n"
     "    end else if (!gsi_wait_i && !gsi_sampled_r) begin",
     "end else if (1'b0) begin\n"
     "      gsi_sampled_r <= 1'b0;\n"
     "    end else if (1'b1) begin", 1, "gi"),
    ("srp-failure-change-strobe-removed", SRP,
     "|| (rtype_r[s] != rx_is_failed_w)\n"
     "                      || (rx_is_failed_w\n"
     "                          && ((fcode_r[s] != evt_failure_code_i)\n"
     "                              || (fsysid_r[s] != evt_failure_system_id_i))));",
     "|| (rtype_r[s] != rx_is_failed_w));", 1, "gi"),
    ("sink-index-guard-removed", TOP,
     "if (32'(gsi_desc_index_o) < N_STREAM_IN_P) begin", "if (1'b1) begin", 1, "gi"),
    ("status-compare-removed", TOP,
     "(lstn_gsi_status_r[lstn_recwr_sink_w] != lstn_gsi_status_w);", "1'b1;", 1, "gi"),
    ("desc-type-ignored", TOP,
     "&& (gsi_desc_type_o == 16'h0005);", "&& 1'b1;", 1, "full"),
    ("golden-full", TOP, "", "", 0, "full"),
    ("sample-transparent-full", TOP,
     "end else if (!aecp_gsi_req_w || !gsi_input_w || (gsi_sel_o != 4'd0)) begin\n"
     "      gsi_sampled_r <= 1'b0;\n"
     "    end else if (!gsi_wait_i && !gsi_sampled_r) begin",
     "end else if (1'b0) begin\n"
     "      gsi_sampled_r <= 1'b0;\n"
     "    end else if (1'b1) begin", 1, "full"),
]


def sh(cmd, cwd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                              check=False, timeout=7200).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    results = []
    for name, fn, old, new, count, mode in MUTANTS:
        if a.only and name not in a.only.split(","):
            continue
        tree = a.work / name
        shutil.rmtree(tree, ignore_errors=True)
        for d in ("hdl", "tb/common", "tb/pp_top"):
            shutil.copytree(a.src / d, tree / d,
                            ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
        if old:
            p = tree / fn
            s = p.read_text()
            if s.count(old) != count:
                raise SystemExit(f"{name}: expected {count} edit sites, found {s.count(old)}")
            p.write_text(s.replace(old, new))
        bench = tree / "tb/pp_top"
        brc = sh(["make", "gsi-build", "VERILATOR=" + a.verilator], bench,
                 a.out / f"{name}-build.log")
        if brc != 0:
            raise SystemExit(f"{name}: build failed rc={brc}")
        args = ["./obj_dir/Vpp_top_sim"] + (["--gsi-internal-only"] if mode == "gi" else [])
        log = a.out / f"{name}-run.log"
        rrc = sh(args, bench, log)
        text = log.read_text()
        fails = [l for l in text.splitlines() if l.startswith("FAIL")]
        tally = [l for l in text.splitlines() if l.startswith("[build default")]
        r = {"mutant": name, "mode": mode, "run_rc": rrc, "tally": tally,
             "first_failures": fails[:6], "n_fail_lines": len(fails),
             "verdict": ("KILLED" if rrc != 0 and tally else
                         "SURVIVED" if rrc == 0 and tally else "INCOMPLETE")}
        print(json.dumps(r), flush=True)
        results.append(r)
    (a.out / "results.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
