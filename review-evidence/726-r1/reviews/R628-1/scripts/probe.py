#!/usr/bin/env python3
"""Reviewer fault probes for #726 (disposable; never touches the clone).

Usage: probe.py <tree> <scratch> <probe-name>
Copies <tree> (an exact-head copy) to <scratch>/probe-<name>, applies one
exact-once source replacement, and prints the probe's diff. The caller then
runs the stock fixture from the probe copy. Each plant must match its anchor
exactly once, so a moved anchor is an error rather than a silent no-op.
"""
import shutil
import subprocess
import sys
from pathlib import Path

TX = "hdl/ieee1722/avtp/KL_talker_diag_ctx.sv"
RX = "hdl/ieee1722/crf/KL_crf_rx.sv"
AAF = "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
DP = "hdl/milan/milan_datapath.sv"

PLANTS = {
    # FRAMES_TX saturates instead of wrapping at 32 bits
    "tx-saturate": [(TX, "ftx_r[c] <= ftx_r[c] + 32'd1;",
                     "if (ftx_r[c] != 32'hFFFFFFFF) ftx_r[c] <= ftx_r[c] + 32'd1;")],
    # CRF FRAMES_RX also resets on bound -> not bound (forbidden by 5.3.8.10)
    "crf-unbind-reset": [(RX, "      if (w_bind_fall_w && locked_o) begin",
                          "      if (w_bind_fall_w) pdu_count_o <= '0;\n"
                          "      if (w_bind_fall_w && locked_o) begin")],
    # the CRF output's PDU strobe never reaches the talker counters
    "crf-tx-lost": [(DP, "    .frame_p_i   (aaf_frame_p_w | tkd_crf_p_w),\n"
                         "    .frame_idx_i (aaf_frame_p_w ? aaf_frame_idx_w : 4'(N_STREAMS)),\n"
                         "    //! Match",
                     "    .frame_p_i   (aaf_frame_p_w),\n"
                     "    .frame_idx_i (aaf_frame_p_w ? aaf_frame_idx_w : 4'(N_STREAMS)),\n"
                     "    //! Match")],
    # healthy CRF FRAMES_RX advances no longer mark the CRF input dirty
    "crf-rx-nodirty": [(RX, "        pdu_count_o <= pdu_count_o + 32'd1;\n        dirty_p_o <= 1'b1;",
                        "        pdu_count_o <= pdu_count_o + 32'd1;")],
    # AAF inputs: restore both pre-#726 healthy-update exclusions only
    "aaf-rx-nodirty": [
        (AAF, "            if (iv_seen_r[iv_s_w] != '0)",
              "            if ((iv_seen_r[iv_s_w] & ~(12'b1 << C_FRX_C)) != '0)"),
        (AAF, "            dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r",
              "            if (!cur_w.tv || lock_now_w ||\n"
              "                (seq_mm_w && lost_w >= 8'(INTERRUPT_MIN_LOST_C)))\n"
              "              dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r")],
    # healthy transmitted PDUs no longer mark the Stream Output dirty
    "tx-nodirty": [(TX, "          ftx_r[c] <= ftx_r[c] + 32'd1;\n          dirty_p_o[c] <= 1'b1;",
                    "          ftx_r[c] <= ftx_r[c] + 32'd1;")],
    # a PDU in the exact start cycle is dropped from the new run
    "tx-start-coincident": [(TX, "ftx_r[c]    <= {31'd0, ev_f_w[c]};", "ftx_r[c]    <= '0;")],
    # control: the talker counters see tu clear (a locked PHC), per-PDU dirty intact
    "tu0": [(DP, "    .tu_i        (aaf_frame_p_w ? aaf_frame_tu_w : crft_tu_last_w),",
             "    .tu_i        (1'b0),")],
    # tu clear AND healthy transmitted PDUs no longer mark the output dirty
    "tx-nodirty-tu0": [(TX, "          ftx_r[c] <= ftx_r[c] + 32'd1;\n          dirty_p_o[c] <= 1'b1;",
                        "          ftx_r[c] <= ftx_r[c] + 32'd1;"),
                       (DP, "    .tu_i        (aaf_frame_p_w ? aaf_frame_tu_w : crft_tu_last_w),",
                        "    .tu_i        (1'b0),")],
}


def main():
    tree, scratch, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    dest = scratch / f"probe-{name}"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(tree, dest, symlinks=True,
                    ignore=shutil.ignore_patterns("obj_*", "obj_dir"))
    for rel, old, new in PLANTS[name]:
        p = dest / rel
        text = p.read_text()
        if text.count(old) != 1:
            raise SystemExit(f"{name}: anchor occurs {text.count(old)} times in {rel}")
        p.write_text(text.replace(old, new))
    print(subprocess.run(["git", "diff", "--stat"], cwd=dest, text=True,
                         capture_output=True).stdout)
    print(dest)


if __name__ == "__main__":
    main()
