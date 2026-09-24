#!/usr/bin/env python3
"""R294 reviewer-owned extra GSI mutants (disposable copies only).

Usage: extra_mutants.py <source-tree> <scratch-dir> <output-dir> <verilator>
Each mutant edits one exact site in a private copy, builds the pp_top
`gsi-build` target and runs `--gsi-internal-only`. A mutant is KILLED when
the build succeeds and the run completes with rc 1 and at least one FAIL
line; SURVIVED when the run passes. Build failures are reported, not scored.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
SRP = "hdl/srp/KL_srp_listener_fsm.sv"
MUTANTS = [
    # (name, file, old, new, expected-count, intent)
    ("srp-failure-strobe-removed", SRP,
     "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w)\n"
     "                      || (rx_is_failed_w\n",
     "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w)\n"
     "                      || (1'b0 && rx_is_failed_w\n", 1,
     "changed FailureInformation no longer strobes registration"),
    ("sel4-integrator-byte", TOP,
     "4'd4: aecp_gsi_data_w = {gsi_data_i[63:16], gsi_fail_code_r, 8'd0};",
     "4'd4: aecp_gsi_data_w = gsi_data_i;", 1,
     "selector-4 failure-code byte back on the integrator path"),
    ("notify-every-write", TOP,
     "(lstn_gsi_status_r[lstn_recwr_sink_w] != lstn_gsi_status_w);",
     "1'b1;", 1,
     "status notification without the committed-change compare"),
    ("live-unsampled-fields", TOP,
     "4'd5: aecp_gsi_data_w = gsi_fail_bridge_r;",
     "4'd5: aecp_gsi_data_w = srp_snk_fail_bridge_w[SINK_IDX_W_C'(gsi_desc_index_o)];",
     1, "bridge read live at the selector-5 beat instead of the selector-0 sample"),
    ("index-guard-removed", TOP,
     "if (32'(gsi_desc_index_o) < N_STREAM_IN_P) begin\n        gsi_fail_code_r",
     "if (1'b1) begin\n        gsi_fail_code_r", 1,
     "descriptor index no longer range-checked before narrowing"),
]


def sh(cmd, cwd, log):
    with open(log, "w") as out:
        return subprocess.run(cmd, cwd=cwd, stdout=out, stderr=subprocess.STDOUT,
                              timeout=3600).returncode


def main() -> int:
    src, scratch, output, verilator = map(Path, sys.argv[1:5])
    output.mkdir(parents=True, exist_ok=True)
    results = []
    for name, rel, old, new, count, intent in MUTANTS:
        tree = scratch / ("xm-" + name)
        shutil.rmtree(tree, ignore_errors=True)
        for d in ("hdl", "tb/common", "tb/pp_top"):
            shutil.copytree(src / d, tree / d,
                            ignore=shutil.ignore_patterns("obj*", "*.hex"))
        path = tree / rel
        text = path.read_text()
        if text.count(old) != count:
            raise SystemExit(f"{name}: expected {count} site(s), found {text.count(old)}")
        path.write_text(text.replace(old, new))
        bench = tree / "tb/pp_top"
        brc = sh(["make", "gsi-build", "VERILATOR=" + str(verilator)], bench,
                 output / (name + "-build.log"))
        rrc = None
        fails = []
        if brc == 0:
            log = output / (name + "-run.log")
            rrc = sh(["./obj_dir/Vpp_top_sim", "--gsi-internal-only"], bench, log)
            t = log.read_text()
            fails = [l for l in t.splitlines() if l.startswith("FAIL: ")]
            complete = "[build default," in t
        verdict = ("BUILD-FAIL" if brc != 0 else
                   "KILLED" if (rrc == 1 and fails and complete) else
                   "SURVIVED" if (rrc == 0 and complete) else "INCONCLUSIVE")
        r = {"mutant": name, "intent": intent, "build_rc": brc, "run_rc": rrc,
             "verdict": verdict, "first_failures": fails[:4]}
        print(json.dumps(r), flush=True)
        results.append(r)
        shutil.rmtree(tree / "tb/pp_top/obj_dir", ignore_errors=True)
    (output / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
