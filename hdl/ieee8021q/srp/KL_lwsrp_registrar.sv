/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_registrar.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : lwSRP registrar — registers ONLY what gates us
//                (docs/LWSRP_FPGA_ARCHITECTURE.md §1):
//
//                LISTENER attribute for our StreamID:
//                  registering events are {New, JoinIn, JoinMt} ONLY —
//                  802.1Q-2018 Table 10-4 has no rIn! (nor rMt!) registrar
//                  row. In means "the sender holds it registered but is NOT
//                  declaring it", so an In never registers, never refreshes
//                  the stored declaration and never cancels a running leave
//                  timer: after a LeaveAll a drained listener ages out at
//                  LeaveTime no matter how many bare Ins arrive. {Lv}
//                  deregisters at once (Milan v1.2 4.2.7.2.2, which
//                  modifies ONLY the IN / rLv! cell of Table 10-4); a
//                  received LeaveAll arms the leave timer (LEAVE_TIME_MS_C)
//                  — the registration survives until the timer expires
//                  un-refreshed.
//                  The four-packed declaration is stored alongside;
//                  listener_ready_o = registered AND declaration is Ready or
//                  ReadyFailed. (DEVIATION from the pipewire reference,
//                  which activates on the three-packed transition alone and
//                  ignores the declaration — Milan-correct per the doc:
//                  AskingFailed means no listener can receive us.)
//
//                DOMAIN sanity -> srp domain boundary flag:
//                  a bridge Domain declaration for OUR SR class (class id 6)
//                  with a different priority or VID marks the port a domain
//                  boundary (domain_ok_o = 0) until a matching declaration
//                  arrives or the boundary ages out (no re-declare within
//                  DOMAIN_AGE_MS_C). Class-B domains are ignored. No Domain
//                  ever seen = Milan defaults assumed = ok.
//
//                TALKER FAILED (bridge declares our stream failed):
//                  failure code captured sticky for AECP GET_STREAM_INFO;
//                  cleared when the bridge re-declares plain TalkerAdvertise
//                  for our stream, or on engine disable.
//---------------------------------------------------------------------------//

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_registrar #(
  //! boundary age-out: two LeaveAll periods with no mismatching re-declare
  parameter int unsigned DOMAIN_AGE_MS_P = 2 * LEAVEALL_TIME_MS_C
)(
    input  wire        clk_i,
    input  wire        rst_n,
    input  wire        enable_i,          //! lwSRP engine enable (CSR)
    input  wire        tick_1khz_i,       //! 1 ms strobe (KL_lwsrp_timers)

    // ---- our domain expectation ----------------------------------------
    input  wire [11:0] vid_i,             //! the SR VID we declare

    // ---- walker event pulses --------------------------------------------
    input  wire        leaveall_p_i,
    input  wire        domain_p_i,
    input  wire [7:0]  domain_class_i,
    input  wire [7:0]  domain_prio_i,
    input  wire [15:0] domain_vid_i,
    input  wire [2:0]  domain_evt_i,
    input  wire        listener_p_i,
    input  wire [2:0]  listener_evt_i,
    input  wire [1:0]  listener_decl_i,
    input  wire        tadv_p_i,
    input  wire        tfail_p_i,
    input  wire [7:0]  tfail_code_i,
    input  wire [63:0] tk_bridge_i,          //! walker TF bridge capture

    // ---- registration state ----------------------------------------------
    output wire        listener_ready_o,     //! the AAF/bw gate condition
    output reg         listener_reg_o,       //! listener registered (any decl)
    output reg  [1:0]  listener_decl_o,      //! last four-packed declaration
    output wire        domain_ok_o,          //! !srp domain boundary
    output reg         tfail_valid_o,        //! sticky failure seen
    output reg  [7:0]  tfail_code_o,         //! last MSRP failure code
    output reg  [63:0] tfail_bridge_o        //! failing bridge_id (Milan
                                             //! GET_STREAM_INFO output side)
);

  // -----------------------------------------------------------------------
  // Listener registrar
  // -----------------------------------------------------------------------
  localparam int unsigned LV_W_C = $clog2(LEAVE_TIME_MS_C + 1);

  reg [LV_W_C-1:0] lstn_leave_r;    //! leave downcounter (0 = not running)

  //! 802.1Q-2018 Table 10-4: New/JoinIn/JoinMt are the ONLY registering
  //! events. There is no rIn! row — until 2026-08-08 an In arm refreshed
  //! the declaration AND cancelled the leave timer, so after a LeaveAll a
  //! drained listener sending bare Ins held our licence open forever.
  wire lstn_reg_evt_w  = listener_p_i && ((listener_evt_i == MRP_EVT_NEW_C)   ||
                                          (listener_evt_i == MRP_EVT_JOININ_C)||
                                          (listener_evt_i == MRP_EVT_JOINMT_C));
  wire lstn_lv_evt_w   = listener_p_i && (listener_evt_i == MRP_EVT_LV_C);

  assign listener_ready_o = listener_reg_o &&
                            ((listener_decl_o == LSTN_DECL_READY_C) ||
                             (listener_decl_o == LSTN_DECL_READY_FAIL_C));

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      listener_reg_o  <= 1'b0;
      listener_decl_o <= LSTN_DECL_IGNORE_C;
      lstn_leave_r    <= '0;
    end else if (!enable_i) begin
      listener_reg_o  <= 1'b0;
      listener_decl_o <= LSTN_DECL_IGNORE_C;
      lstn_leave_r    <= '0;
    end else begin
      if (lstn_reg_evt_w) begin
        listener_reg_o  <= 1'b1;
        listener_decl_o <= listener_decl_i;
        lstn_leave_r    <= '0;                     // cancel any pending leave
      end else if (lstn_lv_evt_w && listener_reg_o) begin
        //! MILAN 4.2.7.2.2 "Instantaneous transition from IN to MT": for the
        //! MSRP application the 802.1Q Table 10-4 transition
        //!     IN / rLv! -> (Start leavetimer) -> LV
        //! SHALL be replaced by
        //!     IN / rLv! -> (Lv) -> MT
        //! so an EXPLICIT withdrawal deregisters at once rather than ageing
        //! out. Until 2026-07-30 an rLv armed the leave timer exactly like a
        //! LeaveAll, which was tolerable only while LEAVE_TIME_MS_C was the
        //! 802.1Q 600 ms; at Milan's mandated 5 s it would have taken five
        //! seconds to notice a stream had been withdrawn - which is precisely
        //! the cost the clause's own Note says this transition exists to
        //! avoid. The leave TIMER now covers the LeaveAll path only, where
        //! waiting is the point: everyone re-declares after a LeaveAll and a
        //! registration must survive that round.
        listener_reg_o  <= 1'b0;
        listener_decl_o <= LSTN_DECL_IGNORE_C;
        lstn_leave_r    <= '0;
      end else if (leaveall_p_i && listener_reg_o &&
                   (lstn_leave_r == '0)) begin
        lstn_leave_r <= LV_W_C'(LEAVE_TIME_MS_C);  // arm the leave timer
      end else if (tick_1khz_i && (lstn_leave_r != '0)) begin
        lstn_leave_r <= lstn_leave_r - 1'b1;
        if (lstn_leave_r == LV_W_C'(1)) begin
          listener_reg_o  <= 1'b0;                 // aged out
          listener_decl_o <= LSTN_DECL_IGNORE_C;
        end
      end
    end
  end

  // -----------------------------------------------------------------------
  // Domain boundary flag
  // -----------------------------------------------------------------------
  localparam int unsigned DOM_W_C = $clog2(DOMAIN_AGE_MS_P + 1);

  reg                boundary_r;
  reg [DOM_W_C-1:0]  boundary_age_r;

  assign domain_ok_o = !boundary_r;

  wire dom_class_a_w = domain_p_i && (domain_class_i == SR_CLASS_A_ID_C) &&
                       (domain_evt_i != MRP_EVT_LV_C) &&
                       (domain_evt_i != MRP_EVT_MT_C);
  wire dom_match_w   = dom_class_a_w &&
                       (domain_prio_i == SR_CLASS_A_PRIO_C) &&
                       (domain_vid_i == {4'h0, vid_i});

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      boundary_r <= 1'b0; boundary_age_r <= '0;
    end else if (!enable_i) begin
      boundary_r <= 1'b0; boundary_age_r <= '0;
    end else begin
      if (dom_class_a_w && !dom_match_w) begin
        boundary_r     <= 1'b1;
        boundary_age_r <= DOM_W_C'(DOMAIN_AGE_MS_P);
      end else if (dom_match_w) begin
        boundary_r     <= 1'b0;
        boundary_age_r <= '0;
      end else if (tick_1khz_i && boundary_r) begin
        boundary_age_r <= boundary_age_r - 1'b1;
        if (boundary_age_r <= DOM_W_C'(1)) boundary_r <= 1'b0;
      end
    end
  end

  // -----------------------------------------------------------------------
  // TalkerFailed capture (sticky; AECP GET_STREAM_INFO exposure)
  // -----------------------------------------------------------------------
  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      tfail_valid_o <= 1'b0; tfail_code_o <= 8'h00; tfail_bridge_o <= 64'h0;
    end else if (!enable_i) begin
      tfail_valid_o <= 1'b0; tfail_code_o <= 8'h00; tfail_bridge_o <= 64'h0;
    end else if (tfail_p_i) begin
      tfail_valid_o <= 1'b1; tfail_code_o <= tfail_code_i;
      tfail_bridge_o <= tk_bridge_i;
    end else if (tadv_p_i) begin
      tfail_valid_o <= 1'b0;                 // bridge says we are clean again
    end
  end

endmodule

`default_nettype wire
