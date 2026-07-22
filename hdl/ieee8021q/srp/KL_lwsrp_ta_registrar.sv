/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_ta_registrar.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP, AVnu Milan v1.2 §5.6)
//
//  Description : Listener-side registrar for the TalkerAdvertise and
//                TalkerFailed attributes covering the ACMP listener's BOUND
//                stream_id (the walker's second match context).
//
//                Same registrar dynamics as the talker-side Listener
//                registrar: {NEW, JOININ, JOINMT, IN} register and reload
//                the 600 ms leave timer; {LV, LeaveAll} arm it; expiry
//                deregisters. The registered level INCLUDES the LV/leave
//                window (the pipewire reference treats IN and LV alike —
//                the transient recovers on the next JoinIn).
//
//                ta_registered_o drives the ACMP listener's TK_REGISTERED/
//                TK_UNREGISTERED events and selects Listener Ready (vs
//                Ready-Failed) in the applicant. ta_failed_o mirrors the
//                TalkerFailed attribute (SRP_REGISTERING_FAILED reporting +
//                the settled reservation-lost transition).
//---------------------------------------------------------------------------//

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_ta_registrar (
    input  wire        clk_i,
    input  wire        rst_n,
    input  wire        enable_i,          //! binding valid (ACMP listener)
    input  wire        tick_1khz_i,

    // ---- walker events (second match context) ---------------------------
    input  wire        leaveall_p_i,
    input  wire        l_tadv_p_i,
    input  wire        l_tfail_p_i,
    input  wire [2:0]  l_evt_i,
    input  wire [7:0]  l_tfail_code_i,
    input  wire [11:0] tk_vlan_i,         //! walker Talker-attr captures
    input  wire [31:0] tk_acclat_i,
    input  wire [63:0] tk_bridge_i,

    // ---- registration state ----------------------------------------------
    output reg         ta_registered_o,
    output reg         ta_failed_o,
    output reg  [7:0]  ta_fail_code_o,
    //! Milan GET_STREAM_INFO fields from the registered Talker attribute
    output reg  [11:0] ta_vlan_o,
    output reg  [31:0] ta_acclat_o,
    output reg  [63:0] ta_fail_bridge_o
);

  //! leave downcounters (ms); 0 = disarmed
  reg [9:0] ta_leave_r, tf_leave_r;

  wire w_join_evt = (l_evt_i == MRP_EVT_NEW_C)    || (l_evt_i == MRP_EVT_JOININ_C) ||
                    (l_evt_i == MRP_EVT_JOINMT_C) || (l_evt_i == MRP_EVT_IN_C);
  wire w_lv_evt   = (l_evt_i == MRP_EVT_LV_C);

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      ta_registered_o <= 1'b0;
      ta_failed_o     <= 1'b0;
      ta_fail_code_o  <= 8'h00;
      ta_vlan_o       <= 12'h0;
      ta_acclat_o     <= 32'h0;
      ta_fail_bridge_o<= 64'h0;
      ta_leave_r      <= 10'd0;
      tf_leave_r      <= 10'd0;
    end else if (!enable_i) begin
      // binding dropped: forget everything
      ta_registered_o <= 1'b0;
      ta_failed_o     <= 1'b0;
      ta_leave_r      <= 10'd0;
      tf_leave_r      <= 10'd0;
    end else begin
      // leave expiry
      if (tick_1khz_i && ta_leave_r != 10'd0) begin
        ta_leave_r <= ta_leave_r - 10'd1;
        if (ta_leave_r == 10'd1) ta_registered_o <= 1'b0;
      end
      if (tick_1khz_i && tf_leave_r != 10'd0) begin
        tf_leave_r <= tf_leave_r - 10'd1;
        if (tf_leave_r == 10'd1) ta_failed_o <= 1'b0;
      end

      // LeaveAll arms the leave window on whatever is registered
      if (leaveall_p_i) begin
        if (ta_registered_o && ta_leave_r == 10'd0)
          ta_leave_r <= 10'(LEAVE_TIME_MS_C);
        if (ta_failed_o && tf_leave_r == 10'd0)
          tf_leave_r <= 10'(LEAVE_TIME_MS_C);
      end

      if (l_tadv_p_i) begin
        if (w_join_evt) begin
          ta_registered_o <= 1'b1;
          ta_vlan_o       <= tk_vlan_i;
          ta_acclat_o     <= tk_acclat_i;
          ta_leave_r      <= 10'd0;      // reload: disarm the leave window
        end else if (w_lv_evt && ta_registered_o) begin
          ta_leave_r <= 10'(LEAVE_TIME_MS_C);
        end
      end
      if (l_tfail_p_i) begin
        if (w_join_evt) begin
          ta_failed_o      <= 1'b1;
          ta_fail_code_o   <= l_tfail_code_i;
          ta_vlan_o        <= tk_vlan_i;
          ta_acclat_o      <= tk_acclat_i;
          ta_fail_bridge_o <= tk_bridge_i;
          tf_leave_r       <= 10'd0;
        end else if (w_lv_evt && ta_failed_o) begin
          tf_leave_r <= 10'(LEAVE_TIME_MS_C);
        end
      end
    end
  end

endmodule

`default_nettype wire
