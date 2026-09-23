#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probes for the #387 gmstep leg (disposable, never committed).

Each variant plants at most one defect into a PRIVATE copy of one source (the
datapath, the clock-validity block or the render stage), optionally on top of
the proposed datapath edit, and builds the leg through the tree's own
`make gmstep` recipe with DP_SRC / CLKV_SRC / RSP_SRC / GMSTEP_MDIR overridden.
Nothing inside the tree is edited. The verdict of each variant is the leg's own
exit status and its printed [FAIL] lines.

Usage: gmstep_probes.py --tree <copy of the head> --work <scratch dir>
                        --edited <patched datapath> --only <name>[,<name>...]
       VERILATOR=<wrapper> in the environment; --jobs caps concurrent legs and
       --vjobs the Verilator build jobs of each (jobs * vjobs <= 8).
"""

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
from pathlib import Path

DP_STEP_TO_CLKV = "                   ? gptp_step_we_w : cfg_ptp_cmd_adjust),"
DP_TALKER_GATE = "assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;"
DP_RENDER_HEAD = "       gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load\n       | src_recentre_p_r;"
DP_RENDER_EDIT = "       media_rebase_p_w | src_recentre_p_r;"
DP_RESTART_EDIT = "                       | media_rebase_p_w;\n"
DP_DISC = "    .fabric_disc_p_i  (gptp_pub_disc_w),"
DP_STEP_SIGN = "                               ? gptp_step_w             : cfg_ptp_offset;"
CLKV_HOLD = "  parameter int unsigned HOLD_QTICK_P = 2,"
CLKV_TU = "  assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w;\n"
RSP_SNAP = ("                rptr_r[s]    <= snap_rptr_w;\n"
            "                prefill_r[s] <= 1'b0;\n")

# name: (base datapath, source, anchor, replacement, what the reviewer expects)
VARIANTS = {
    # ---- at the exact head -------------------------------------------------
    "H0-clean-head": ("head", None, None, None, "fail: exactly the 3 named checks"),
    "H1-tu-stops-talker": ("head", "datapath", DP_TALKER_GATE,
                           DP_TALKER_GATE.replace(";", " & ~clkv_tu_w;"),
                           "licence arms fail"),
    "H2-clkv-ignores-step": ("head", "datapath", DP_STEP_TO_CLKV,
                             DP_STEP_TO_CLKV.replace("gptp_step_we_w", "1'b0          "),
                             "tu holdover-after-step arm fails"),
    "H3-render-ignores-step": ("head", "datapath", DP_RENDER_HEAD,
                               "       gm_recentre_p_r | cfg_ptp_cmd_load\n       | src_recentre_p_r;",
                               "render count 2 -> 1: the count arm PASSES at head"),
    "H4-render-ignores-identity": ("head", "datapath", DP_RENDER_HEAD,
                                   "       eff_ptp_adjust_w | cfg_ptp_cmd_load\n       | src_recentre_p_r;",
                                   "render count 2 -> 1"),
    "H5-no-commit-disc-to-clkv": ("head", "datapath", DP_DISC,
                                  "    .fabric_disc_p_i  (1'b0),",
                                  "observe whether tu-at-identity still holds"),
    "H6-step-sign-inverted": ("head", "datapath", DP_STEP_SIGN,
                              "                               ? (64'd0 - gptp_step_w)   : cfg_ptp_offset;",
                              "step-count / step-size arms fail"),
    "H7-holdover-one-qtick": ("head", "clkv", CLKV_HOLD, CLKV_HOLD.replace("= 2", "= 1"),
                              "tu held-at-least arm fails"),
    "H8-holdover-four-qticks": ("head", "clkv", CLKV_HOLD, CLKV_HOLD.replace("= 2", "= 4"),
                                "tu cleared-within-bound arm fails"),
    "H9-stream-input-counters-dead": ("head", "datapath",
                                      "  wire ctr_sin_w = (ctrq_type_r == DESC_STREAM_INPUT_C)\n"
                                      "                && (ctrq_index_r < 16'(N_STREAMS));",
                                      "  wire ctr_sin_w = 1'b0;",
                                      "observe whether 'listener stays locked' still passes"),
    # ---- on the proposed datapath edit (not in this PR) --------------------
    "E0-clean-edited": ("edited", None, None, None, "pass 40/40"),
    "E1-tu-late-4-cycles": ("edited", "clkv", CLKV_TU,
                            "  logic [3:0] tu_late_r;\n"
                            "  always_ff @(posedge clk_i) begin : p_tu_late\n"
                            "    tu_late_r <= {tu_late_r[2:0], (~sync_ok_w) | hold_w | disc_p_w};\n"
                            "  end : p_tu_late\n"
                            "  assign ts_uncertain_o = tu_late_r[3];\n",
                            "tu-at-identity arm fails"),
    "E2-render-ignores-step": ("edited", "datapath", DP_RENDER_EDIT,
                               "       src_recentre_p_r;", "render count arm fails (0)"),
    "E3-render-identity-too": ("edited", "datapath", DP_RENDER_EDIT,
                               "       gm_recentre_p_r | media_rebase_p_w | src_recentre_p_r;",
                               "render count arm fails (2)"),
    "E4-no-restart-on-step": ("edited", "datapath", DP_RESTART_EDIT, "                       ;\n",
                              "mr and MEDIA_RESET arms fail"),
    "E5-restart-on-identity-too": ("edited", "datapath", DP_RESTART_EDIT,
                                   "                       | media_rebase_p_w | gm_recentre_p_r;\n",
                                   "mr exactly-once / MEDIA_RESET exactly-one arms fail"),
    "E6-snap-off-setpoint": ("edited", "stage", RSP_SNAP,
                             "                rptr_r[s]    <= prefill_r[s] ? snap_rptr_w : snap_rptr_w - 1'b1;\n"
                             "                prefill_r[s] <= 1'b0;\n",
                             "fill-constant arm fails"),
    "E7-holdover-one-qtick": ("edited", "clkv", CLKV_HOLD, CLKV_HOLD.replace("= 2", "= 1"),
                              "tu held-at-least arm fails"),
    # the re-base keyed to the grandmaster-identity change instead of the step
    "E8-identity-keyed-rebase": ("edited", "datapath",
                                 "  wire media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load;",
                                 "  wire media_rebase_p_w = gm_recentre_p_r | cfg_ptp_cmd_load;",
                                 "a counted-event arm should fail; does it?"),
    # the AAF packetizer silenced for good once tu clears after the change;
    # the admission gate itself is untouched
    "E9-talker-silent-after-event": ("edited", "datapath", [
        ("  wire [N_STREAMS-1:0] aaf_stream_en_raw_w /* verilator public_flat_rd */;",
         "  logic probe_armed_r, probe_stop_r, probe_tu_q_r;\n"
         "  wire [N_STREAMS-1:0] aaf_stream_en_raw_w /* verilator public_flat_rd */;"),
        ("    .stream_en_i (aaf_stream_en_w),",
         "    .stream_en_i (aaf_stream_en_w & ~{N_STREAMS{probe_stop_r}}),"),
        ("  end : g_gm_recentre\n",
         "  end : g_gm_recentre\n"
         "  always_ff @(posedge axis_clk) begin : g_probe_stop\n"
         "    if (!axis_resetn) begin\n"
         "      probe_armed_r <= 1'b0; probe_stop_r <= 1'b0; probe_tu_q_r <= 1'b1;\n"
         "    end else begin\n"
         "      probe_tu_q_r <= clkv_tu_w;\n"
         "      if (gm_recentre_p_r) probe_armed_r <= 1'b1;\n"
         "      if (probe_armed_r && probe_tu_q_r && !clkv_tu_w) probe_stop_r <= 1'b1;\n"
         "    end\n"
         "  end : g_probe_stop\n"),
    ], None, "a licence arm should fail; does it?"),
}


def run_variant(name, tree, work, sources, vjobs):
    base, source, anchor, replacement, expect = VARIANTS[name]
    chosen = dict(sources)
    chosen["datapath"] = sources["edited"] if base == "edited" else sources["datapath"]
    record = {"name": name, "base": base, "expect": expect}
    if source is not None:
        text = chosen[source].read_text(encoding="utf-8")
        edits = anchor if isinstance(anchor, list) else [(anchor, replacement)]
        record["anchor_count"] = [text.count(a) for a, _ in edits]
        if any(text.count(a) != 1 for a, _ in edits):
            record["verdict"] = "ANCHOR-NOT-UNIQUE"
            return record
        for a, r in edits:
            text = text.replace(a, r, 1)
        planted = work / f"{name}_{chosen[source].name}"
        planted.write_text(text, encoding="utf-8")
        chosen[source] = planted
    mdir = f"obj_probe_{name}"
    command = ["make", "-C", str(tree / "tb/verilator/milan_dp"), "gmstep",
               f"GMSTEP_MDIR={mdir}", f"DP_SRC={chosen['datapath']}",
               f"CLKV_SRC={chosen['clkv']}", f"RSP_SRC={chosen['stage']}",
               f"VERILATOR={os.environ['VERILATOR']}", f"VERILATOR_JOBS={vjobs}"]
    done = subprocess.run(command, capture_output=True, text=True, check=False,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    log = done.stdout + done.stderr
    (work / f"{name}.log").write_text(log, encoding="utf-8")
    record["exit"] = done.returncode
    record["summary"] = [line for line in log.splitlines() if line.startswith("== gmstep:")]
    record["failed"] = [line.split("[FAIL]", 1)[1].split(" got=")[0].strip()
                        for line in log.splitlines() if "[FAIL]" in line]
    record["render_line"] = [line for line in log.splitlines() if line.startswith("RENDER:")]
    record["event_line"] = [line for line in log.splitlines() if line.startswith(("EVENT:", "TU:"))]
    record["verdict"] = "RAN" if record["summary"] else "NO-VERDICT (build or crash)"
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--edited", type=Path, required=True)
    parser.add_argument("--only", required=True)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--vjobs", type=int, default=2)
    args = parser.parse_args()
    if args.jobs * args.vjobs > 8:
        sys.exit("jobs * vjobs must not exceed 8")
    tree = args.tree.resolve()
    args.work.mkdir(parents=True, exist_ok=True)
    sources = {
        "datapath": tree / "hdl/milan/milan_datapath.sv",
        "edited": args.edited.resolve(),
        "clkv": tree / "hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv",
        "stage": tree / "hdl/ieee1722/aaf/KL_render_setpoint.sv",
    }
    names = args.only.split(",")
    for name in names:
        if name not in VARIANTS:
            sys.exit(f"unknown variant {name}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda n: run_variant(n, tree, args.work.resolve(), sources,
                                                      args.vjobs), names))
    for record in results:
        print(json.dumps(record))
    return 0


if __name__ == "__main__":
    sys.exit(main())
