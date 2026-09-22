/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_srp_domain.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/10 §6.1 F10.2 Domain FSM, §3 Domain
//                 vector surfacing rule, 02 §4.1 srp contract class-C/D)
//
//  Description : The single Class A Domain participant (Milan §4.2.7.2.1).
//                Declares the default Domain {SRclassID 6, priority 3,
//                VID 2} at startup and on every LINK_UP; a received Class A
//                Domain declaration with differing parameters is ADOPTED —
//                the old declaration is withdrawn (Lv) and the adopted one
//                re-declared (New) — with a one-cycle DOMAIN_CHANGE strobe
//                and updated class-D levels {class_a_prio, class_a_vid};
//                reverts to the defaults on LINK_DOWN ONLY (F10.2: periodic
//                and LeaveAll cycles re-join, never revert). Received
//                vectors are surfaced by the 10 §3 range rule — Class A is
//                present when SRclassID_first <= 6 < SRclassID_first + NoV
//                and its priority is prio_first + (6 - SRclassID_first) —
//                so the certified two-class bridge shape (FirstValue
//                {5, 2, VID}, NumberOfValues 2) adopts correctly; equality
//                matching on FirstValue alone is a wire defect.
//
//  Decision    : the design decision that matters — Domain transmission is
//                independent of gPTP port state STRUCTURALLY: this module
//                has no gPTP input to get it wrong (Milan §4.2.7.2.1). The
//                Lv-then-New adoption pair rides a two-deep event queue
//                toward the encoder so withdrawal and re-declaration stay
//                ordered across encoder backpressure; a newer received
//                Domain simply overwrites the one-deep adoption-pending
//                latch (newest wins) and is applied when the queue drains.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_srp_domain #(
    //! default SR class A priority (Milan §4.2.7.2.1 default = 3)
    parameter logic [7:0]  DEF_PRIO_P = 8'd3,
    //! default SR class A VID (Milan §4.2.7.2.1 default = 2)
    parameter logic [15:0] DEF_VID_P  = 16'd2
) (
    input  wire         clk_i,               //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,               //! synchronous active-low reset

    input  wire         link_up_i,           //! link status level (2FF-synced upstream)

    // ---- received Domain vector (decoder not yet landed: plain ports) ----
    input  wire         rxdom_valid_i,       //! one-cycle strobe: Domain vector registered
    input  wire  [7:0]  rxdom_class_id_i,    //! FirstValue SRclassID
    input  wire  [7:0]  rxdom_prio_i,        //! FirstValue SRclassPriority
    input  wire  [15:0] rxdom_vid_i,         //! FirstValue SRclassVID (pinned across the vector)
    input  wire  [12:0] rxdom_nov_i,         //! NumberOfValues of the vector

    // ---- MSRP participant cadence (timer expiries via the event router) ---
    input  wire         periodic_tick_i,     //! T-MRP-PERIODIC: re-join the declaration
    input  wire         leaveall_tick_i,     //! MSRP LeaveAll cycle (own or received): re-declare

    // ---- declaration events toward KL_srp_encoder -------------------------
    output logic        dom_ev_valid_o,      //! event pending, held until ready
    output logic [2:0]  dom_ev_event_o,      //! attribute event (0 New, 1 JoinIn, 5 Lv)
    output logic [31:0] dom_ev_value_o,      //! Domain FirstValue {SRclassID, prio, VID}
    input  wire         dom_ev_ready_i,      //! encoder accepts the event

    // ---- class-C event (router not yet landed: strobe + payload) ----------
    output logic        evt_domain_change_o, //! one-cycle DOMAIN_CHANGE strobe

    // ---- class-D levels (F02.10) ------------------------------------------
    output logic [2:0]  class_a_prio_o,      //! operating Class A priority
    output logic [11:0] class_a_vid_o,       //! operating Class A default VID
    output logic        adopted_o            //! 0 = DEFAULTS, 1 = ADOPTED (F10.2 state)
);

  localparam logic [7:0] CLASS_A_ID_C = 8'd6;
  localparam logic [2:0] EV_NEW_C     = 3'd0;
  localparam logic [2:0] EV_JOININ_C  = 3'd1;
  localparam logic [2:0] EV_LV_C      = 3'd5;

  // ------------------------------------------------------- operating state
  logic [7:0]  decl_prio_r;
  logic [15:0] decl_vid_r;
  logic        adopted_r;
  logic        declared_r;    // a declaration is on the wire (link is up)
  logic        link_q_r;

  // two-deep ordered event queue toward the encoder
  logic        q0_valid_r, q1_valid_r;
  logic [2:0]  q0_ev_r,    q1_ev_r;
  logic [31:0] q0_val_r,   q1_val_r;

  // pending latches serviced when the queue is empty
  logic        rx_pend_v_r;
  logic [7:0]  rx_pend_prio_r;
  logic [15:0] rx_pend_vid_r;
  logic        rejoin_pend_r;

  // ------------------------------------------------------ receive surfacing
  logic        covers6_w;
  logic [7:0]  surf_prio_w;
  logic        link_rise_w, link_fall_w, q_empty_w;

  // Class A present iff SRclassID_first <= 6 < SRclassID_first + NoV (10 §3)
  assign covers6_w   = (rxdom_class_id_i <= CLASS_A_ID_C)
                    && (({6'd0, rxdom_class_id_i} + {1'b0, rxdom_nov_i})
                        > 14'd6);
  assign surf_prio_w = rxdom_prio_i + (CLASS_A_ID_C - rxdom_class_id_i);

  assign link_rise_w = link_up_i && !link_q_r;
  assign link_fall_w = !link_up_i && link_q_r;
  assign q_empty_w   = !q0_valid_r && !q1_valid_r;

  always_ff @(posedge clk_i) begin : domain_sm
    if (!rst_n) begin
      decl_prio_r         <= DEF_PRIO_P;
      decl_vid_r          <= DEF_VID_P;
      adopted_r           <= 1'b0;
      declared_r          <= 1'b0;
      link_q_r            <= 1'b0;
      q0_valid_r          <= 1'b0;
      q1_valid_r          <= 1'b0;
      q0_ev_r             <= 3'd0;
      q1_ev_r             <= 3'd0;
      q0_val_r            <= 32'd0;
      q1_val_r            <= 32'd0;
      rx_pend_v_r         <= 1'b0;
      rx_pend_prio_r      <= 8'd0;
      rx_pend_vid_r       <= 16'd0;
      rejoin_pend_r       <= 1'b0;
      evt_domain_change_o <= 1'b0;
    end else begin
      evt_domain_change_o <= 1'b0;
      link_q_r            <= link_up_i;

      // ---- queue pop toward the encoder ---------------------------------
      if (q0_valid_r && dom_ev_ready_i) begin
        q0_valid_r <= q1_valid_r;
        q0_ev_r    <= q1_ev_r;
        q0_val_r   <= q1_val_r;
        q1_valid_r <= 1'b0;
      end

      // ---- adoption / re-join request capture ---------------------------
      if (rxdom_valid_i && declared_r && covers6_w
          && ({surf_prio_w, rxdom_vid_i} != {decl_prio_r, decl_vid_r})) begin
        rx_pend_prio_r <= surf_prio_w;    // newest received Domain wins
        rx_pend_vid_r  <= rxdom_vid_i;
        rx_pend_v_r    <= 1'b1;
      end
      if ((periodic_tick_i || leaveall_tick_i) && declared_r) begin
        rejoin_pend_r <= 1'b1;
      end

      // ---- link transitions own the state (F10.2 revert rule) -----------
      if (link_fall_w) begin
        // revert to defaults on LINK_DOWN only; nothing goes on the wire
        if (adopted_r) evt_domain_change_o <= 1'b1;
        decl_prio_r   <= DEF_PRIO_P;
        decl_vid_r    <= DEF_VID_P;
        adopted_r     <= 1'b0;
        declared_r    <= 1'b0;
        q0_valid_r    <= 1'b0;
        q1_valid_r    <= 1'b0;
        rx_pend_v_r   <= 1'b0;
        rejoin_pend_r <= 1'b0;
      end else if (link_rise_w) begin
        // declare the defaults (New) — startup lands here too
        q0_valid_r <= 1'b1;
        q0_ev_r    <= EV_NEW_C;
        q0_val_r   <= {CLASS_A_ID_C, DEF_PRIO_P, DEF_VID_P};
        declared_r <= 1'b1;
      end else if (rx_pend_v_r && q_empty_w) begin
        // adopt: withdraw the old declaration, re-declare the adopted one
        q0_valid_r          <= 1'b1;
        q0_ev_r             <= EV_LV_C;
        q0_val_r            <= {CLASS_A_ID_C, decl_prio_r, decl_vid_r};
        q1_valid_r          <= 1'b1;
        q1_ev_r             <= EV_NEW_C;
        q1_val_r            <= {CLASS_A_ID_C, rx_pend_prio_r, rx_pend_vid_r};
        decl_prio_r         <= rx_pend_prio_r;
        decl_vid_r          <= rx_pend_vid_r;
        adopted_r           <= 1'b1;
        rx_pend_v_r         <= 1'b0;
        evt_domain_change_o <= 1'b1;
      end else if (rejoin_pend_r && declared_r && q_empty_w) begin
        // periodic / LeaveAll re-join of the standing declaration
        q0_valid_r    <= 1'b1;
        q0_ev_r       <= EV_JOININ_C;
        q0_val_r      <= {CLASS_A_ID_C, decl_prio_r, decl_vid_r};
        rejoin_pend_r <= 1'b0;
      end
    end
  end

  // -------------------------------------------------------------- outputs
  assign dom_ev_valid_o = q0_valid_r;
  assign dom_ev_event_o = q0_ev_r;
  assign dom_ev_value_o = q0_val_r;
  assign class_a_prio_o = decl_prio_r[2:0];
  assign class_a_vid_o  = decl_vid_r[11:0];
  assign adopted_o      = adopted_r;

endmodule : KL_srp_domain
`default_nettype wire
