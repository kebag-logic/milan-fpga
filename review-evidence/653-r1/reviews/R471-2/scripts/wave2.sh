#!/bin/bash
# Wave 2: the timed notify leg ([UNB]) on planted copies, full logs kept.
# M1..M5 re-plant unb_mutants.py's five defects by hand (its own text) so each
# failure set can be read in full; P1 is this review's own AAF probe; BASECRF
# is the leg on the base KL_crf_rx file (the dev trace column).
. "$(dirname "$0")/env.sh"
leg() {  # leg NAME: build and run the notify leg in copy NAME
  run "leg_$1" make -C "$SCR/$1/tb/verilator/milan_dp" notify VERILATOR="$VERILATOR" VERILATOR_JOBS=3
}
CRF=hdl/ieee1722/crf/KL_crf_rx.sv
PPT=protocol-processor/hdl/top/protocol_processor_top.sv
AAF=hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv
pl() { python3 "$PKT/scripts/plant.py" "$SCR/$1/$2" "$3" "$4"; }
mkcopy m1; pl m1 $PPT "  assign arb_req_w[LANE_ACMP_C]     = laneq_acmp_cnt_r != 4'd0;" "  logic [12:0] acmp_hold_cyc_r;
  always_ff @(posedge clk_i) begin : acmp_hold
    if (!rst_n || (laneq_acmp_cnt_r == 4'd0)) acmp_hold_cyc_r <= 13'd6000;
    else if (acmp_hold_cyc_r != 13'd0)        acmp_hold_cyc_r <= acmp_hold_cyc_r - 13'd1;
  end
  assign arb_req_w[LANE_ACMP_C]     = (laneq_acmp_cnt_r != 4'd0)
                                    && (acmp_hold_cyc_r == 13'd0);" && leg m1
mkcopy m2; pl m2 $CRF "      if (w_bind_fall_w && locked_o) begin
" "      if (1'b0) begin
" && leg m2
mkcopy m3; pl m3 $CRF "      if (w_bind_fall_w && locked_o) begin
        locked_o       <= 1'b0;
" "      if (w_bind_fall_w && locked_o) begin
" && leg m3
mkcopy m4; pl m4 $CRF "      if (w_bind_fall_w && locked_o) begin
" "      if (w_bind_fall_w && locked_o) begin
        cnt_intr_o     <= cnt_intr_o + 32'd1;
" && leg m4
mkcopy m5; pl m5 $CRF "        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;
        dirty_p_o      <= 1'b1;
      end

      //! not-bound" "        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;
      end

      //! not-bound" && leg m5
mkcopy p1; pl p1 $AAF "        if (bind_fall_i[s] && locked_sh_r[s]) sil_pend_r[s] <= 1'b1;" "        // P1: AAF bind-fall unlock removed" && leg p1
mkcopy basecrf; git -C "$CLONE" show $BASE_SHA:$CRF > "$SCR/basecrf/$CRF" && leg basecrf
wait
