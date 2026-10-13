#!/usr/bin/env python3
"""Reviewer probe: run the #726 parent fixture with an extra disposable plant.

Usage: probe_counters.py <repo> <probe> <shape> <work> [frames-only]

The head's stream_counters.py is imported unchanged; only its plant() is
wrapped so one additional source replacement is staged in <work>. The probe
reports the named [FAIL] groups of the clean-variant run instead of raising.
No file in <repo> is written.
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
probe, shape, work = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4]).resolve()
condition = sys.argv[5] if len(sys.argv) > 5 else "uncertain"
sys.path.insert(0, str(repo / "tb/verilator/milan_dp"))
import stream_counters as sc  # noqa: E402

AAF = "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
CRF = "hdl/ieee1722/crf/KL_crf_rx.sv"
TX = "hdl/ieee1722/avtp/KL_talker_diag_ctx.sv"
NOTIFY = "protocol-processor/hdl/aecp/KL_aecp_notify.sv"
DP = "hdl/milan/milan_datapath.sv"

PLANTS = {
    # restore the c6bd08c6 healthy-path guards in the AAF engine only
    "aaf-guard": [(AAF, "if (iv_seen_r[iv_s_w] != '0)",
                   "if ((iv_seen_r[iv_s_w] & ~(12'b1 << C_FRX_C)) != '0)"),
                  (AAF, "            dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r <= monst_next_w;",
                   "            if (!cur_w.tv || lock_now_w ||\n"
                   "                (seq_mm_w && lost_w >= 8'(INTERRUPT_MIN_LOST_C)))\n"
                   "              dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r <= monst_next_w;")],
    # restore the healthy FRAMES_RX exclusion in the CRF engine only
    "crf-guard": [(CRF, "        pdu_count_o <= pdu_count_o + 32'd1;\n        dirty_p_o <= 1'b1;",
                   "        pdu_count_o <= pdu_count_o + 32'd1;")],
    # AAF FRAMES_RX publishes +1 per interval instead of the packet batch
    "aaf-rx-interval": [(AAF, "? 32'(frx_add_r) : 32'd1);", "? 32'd1 : 32'd1);")],
    # AAF bind wipe keeps the previous era's unpublished packet batch
    "aaf-acc-bind": [(AAF, "          iv_pend_r[s] <= 1'b0;\n          frx_acc_r[s] <= {31'd0, iv_set_w[s][C_FRX_C]};",
                      "          iv_pend_r[s] <= 1'b0;")],
    # talker start drops a PDU completing in the start cycle
    "tx-start-drop": [(TX, "ftx_r[c]    <= {31'd0, ev_f_w[c]};", "ftx_r[c]    <= '0;")],
    # processor scheduler waits 1600 ms instead of 1000 ms after the stamp
    "sched-1600": [(NOTIFY, "((now_ms_i - ctr_last_r[c]) >= 32'd1000)",
                    "((now_ms_i - ctr_last_r[c]) >= 32'd1600)")],
    "sched-2000": [(NOTIFY, "((now_ms_i - ctr_last_r[c]) >= 32'd1000)",
                    "((now_ms_i - ctr_last_r[c]) >= 32'd2000)")],
    # parent control egress holds the first processor frame after 100 quiet
    # protocol ms for 900 protocol ms (1000 cycles per ms in this fixture),
    # only while the CRF talker is enabled (the measurement window)
    "egress-stall": [
        (DP, "  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH), .TO_LOG2_P(15)) ctl_tx_mux (",
         "  logic [31:0] r726_hold_r, r726_quiet_r; logic r726_busy_r; wire r726_ready_w;\n"
         "  always_ff @(posedge axis_clk) begin\n"
         "    if (!axis_resetn) begin r726_hold_r <= '0; r726_quiet_r <= '0; r726_busy_r <= 1'b0; end\n"
         "    else begin\n"
         "      if (pp_tx_tvalid_w && pp_tx_tready_w && pp_tx_tlast_w) r726_quiet_r <= '0;\n"
         "      else if (r726_quiet_r != 32'hFFFFFFFF) r726_quiet_r <= r726_quiet_r + 1;\n"
         "      if (pp_tx_tvalid_w && !r726_busy_r) begin\n"
         "        if (!cfg_crft_en || r726_quiet_r < 32'd100000 || r726_hold_r >= 32'd900000) begin\n"
         "          r726_busy_r <= 1'b1; r726_hold_r <= '0; end\n"
         "        else r726_hold_r <= r726_hold_r + 1;\n"
         "      end\n"
         "      if (r726_busy_r && pp_tx_tvalid_w && pp_tx_tready_w && pp_tx_tlast_w) r726_busy_r <= 1'b0;\n"
         "    end\n"
         "  end\n"
         "  assign pp_tx_tready_w = r726_ready_w & r726_busy_r;\n"
         "  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH), .TO_LOG2_P(15)) ctl_tx_mux ("),
        (DP, "    .s_data_tvalid(pp_tx_tvalid_w), .s_data_tlast (pp_tx_tlast_w),\n"
             "    .s_data_tready(pp_tx_tready_w),",
         "    .s_data_tvalid(pp_tx_tvalid_w & r726_busy_r), .s_data_tlast (pp_tx_tlast_w),\n"
         "    .s_data_tready(r726_ready_w),"),
    ],
}

orig_plant = sc.plant


def plant(variant, w, output_condition):
    paths = orig_plant("clean", w, output_condition)
    for rel, old, new in PLANTS[probe]:
        src = Path(paths.get(str(repo / rel), str(repo / rel)))
        text = src.read_text()
        if text.count(old) != 1:
            raise SystemExit(f"anchor count {text.count(old)} for {probe}: {old!r}")
        dest = w / ("probe_" + Path(rel).name)
        dest.write_text(text.replace(old, new))
        paths[str(repo / rel)] = str(dest)
    return paths


sc.plant = plant
try:
    sc.run(shape, "clean", work, sc.os.environ.get("VERILATOR", "verilator"), condition)
    verdict = "ESCAPED (clean run passed)"
except RuntimeError as exc:
    verdict = f"DETECTED/FAILED: {str(exc)[:300]}"
log = (work / "run.log")
groups = {}
if log.exists():
    for line in log.read_text().splitlines():
        if "[FAIL]" in line:
            tag = line.split("[726 ")[1].split("]")[0] if "[726 " in line else "other"
            groups[tag] = groups.get(tag, 0) + 1
print(f"PROBE {probe} shape={shape} condition={condition}: {verdict}")
print(f"PROBE {probe} failing groups: {groups}")
