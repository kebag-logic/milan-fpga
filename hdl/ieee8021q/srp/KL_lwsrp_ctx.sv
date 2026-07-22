/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_ctx.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : lwSRP attribute CONTEXT TABLE + shared registrar for the
//                extra contexts (table rows 1..N-1; row 0 stays the proven
//                legacy talker+listener pair driven by the CSR group).
//                Closes the docs/MILAN_COMPLIANCE_GAPS.md §3 single-stream
//                limit: one SHARED state machine + per-attribute context
//                storage, never per-attribute module replication — the
//                marginal cost per attribute is one walker compare lane,
//                one 120-bit record row and ~35 dynamic context bits.
//
//                A context row is ONE MSRP stream attribute:
//                  direction 0 (talker):   we declare TalkerAdvertise for
//                    row.sid; the registrar tracks the bridge's Listener
//                    attribute (Ready/AskingFailed/ReadyFailed four-pack,
//                    leave/LeaveAll aging) + the sticky TalkerFailed code
//                    (cleared by a TalkerAdvertise re-declare) — the same
//                    dynamics as KL_lwsrp_registrar row 0.
//                  direction 1 (listener): we declare the Listener attribute
//                    for row.sid (the 2nd-listener / CRF-reservation case);
//                    the registrar tracks the bridge's TalkerAdvertise /
//                    TalkerFailed with the KL_lwsrp_ta_registrar dynamics,
//                    and the declaration four-pack follows it: Ready while
//                    the TA is registered, AskingFailed otherwise (the
//                    pipewire acmp_periodic rule, as row 0 does).
//
//                Storage rules (the 0x4B LUTRAM-replica lesson,
//                MILAN_COMPLIANCE_GAPS.md §1): the record RAM has a
//                sync-only write process and ONE explicit read port (the
//                serializer and the CSR-side readback share its address);
//                per-row single-bit/dynamic state lives in flop vectors
//                because the walker/serializer need it in parallel.
//
//                Provisioning is a request/grant port (the future NxN CSR
//                lane's shape): req held high, one-cycle gnt, write applies
//                at the grant, reads snapshot record+status at the grant.
//                Row 0 is read-only here (legacy status is muxed in);
//                out-of-range rows grant but write nothing.
//
//                On engine disable the extra rows are cleared WITHOUT a
//                farewell LV PDU (the bridge ages them out over one
//                LeaveAll period); row 0 keeps its silicon-proven polite LV.
//---------------------------------------------------------------------------//

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_ctx #(
  //! total contexts incl. the legacy row 0
  parameter int unsigned N_CTX_P      = 1,
  //! extra table rows = max(1, N_CTX_P-1); MUST be passed consistently by
  //! the instantiating layer (KL_lwsrp_top) — port widths depend on it
  parameter int unsigned EXT_LANES_P  = 1
)(
    input  wire        clk_i,
    input  wire        rst_n,
    input  wire        enable_i,          //! lwSRP engine enable (CSR)
    input  wire        tick_1khz_i,       //! 1 ms strobe (KL_lwsrp_timers)
    input  wire        join_tick_i,       //! JoinTime strobe
    input  wire        leaveall_tick_i,   //! our LeaveAll turn
    input  wire        rx_leaveall_i,     //! LeaveAll registered (walker)

    // ---- provisioning request/grant port (datapath/ACMP side) -----------
    input  wire        ctx_req_i,         //! request (hold until gnt)
    input  wire        ctx_we_i,          //! 1 = write record, 0 = read
    input  wire [3:0]  ctx_idx_i,         //! row index (0 = legacy, RO)
    input  wire        ctx_valid_i,       //! record: attribute exists
    input  wire        ctx_dir_i,         //! 0 = talker, 1 = listener
    input  wire [63:0] ctx_sid_i,
    input  wire [47:0] ctx_dmac_i,        //! talker rows only
    input  wire [7:0]  ctx_prio_rank_i,   //! PriorityAndRank byte
    input  wire [15:0] ctx_max_frame_i,
    input  wire [15:0] ctx_interval_i,
    input  wire [31:0] ctx_latency_i,
    output reg         ctx_gnt_o,         //! one-cycle grant
    //! readback snapshot (held from one grant to the next)
    output reg  [63:0] ctx_rd_sid_o,
    output reg  [15:0] ctx_rd_stat_o,     //! {valid,dir,declared,reg,ready,
                                          //!  failed,decl[1:0],code[7:0]}

    // ---- legacy row-0 status (for the indexed view + status vectors) -----
    input  wire        leg_valid_i,       //! talker attribute exists
    input  wire        leg_declared_i,
    input  wire        leg_reg_i,
    input  wire        leg_ready_i,
    input  wire        leg_failed_i,
    input  wire [1:0]  leg_decl_i,
    input  wire [7:0]  leg_code_i,
    input  wire [63:0] leg_sid_i,

    // ---- walker extra-lane hookup ----------------------------------------
    output wire [EXT_LANES_P*64-1:0] lane_sid_o,
    output wire [EXT_LANES_P-1:0]    lane_en_o,
    input  wire [EXT_LANES_P-1:0]    lane_lstn_p_i,
    input  wire [EXT_LANES_P-1:0]    lane_tadv_p_i,
    input  wire [EXT_LANES_P-1:0]    lane_tfail_p_i,
    input  wire [EXT_LANES_P*3-1:0]  lane_evt_i,
    input  wire [EXT_LANES_P*2-1:0]  lane_par_i,
    input  wire [7:0]                lane_tfail_code_i,

    // ---- serializer (KL_lwsrp_ctx_tx) hookup -----------------------------
    output wire [EXT_LANES_P-1:0] row_valid_o,   //! declare on refresh
    output wire [EXT_LANES_P-1:0] row_dir_o,
    output reg  [EXT_LANES_P-1:0] row_fresh_o,   //! NEW on next TX
    output reg  [EXT_LANES_P-1:0] row_lv_o,      //! withdraw on next TX
    output wire [EXT_LANES_P-1:0] row_ready_o,   //! listener 4-pack select
    output wire [EXT_LANES_P*64-1:0] row_sid_o,
    output wire                   tx_go_o,       //! a declare batch pends
    input  wire                   tx_done_i,     //! frame out: clear latches
    input  wire [EXT_LANES_P-1:0] tx_fresh_i,    //! masks the frame carried
    input  wire [EXT_LANES_P-1:0] tx_lv_i,
    //! record RAM read port (THE one explicit read port, serializer side)
    input  wire [3:0]             rec_addr_i,
    output reg  [119:0]           rec_data_o,    //! sync read, 1-cycle

    // ---- fast-join request to the legacy applicant -----------------------
    output reg         fastjoin_p_o,      //! new listener row: LeaveAll pair

    // ---- live status vectors (bit 0 = legacy row) ------------------------
    output wire [15:0] ctx_reg_o,         //! attribute registered
    output wire [15:0] ctx_ready_o,       //! reservation-ready per direction
    output wire [15:0] ctx_failed_o       //! TalkerFailed seen
);

  localparam int unsigned LV_W_C = $clog2(LEAVE_TIME_MS_C + 1);

  // -----------------------------------------------------------------------
  // Context identity flops (walker lanes read them in parallel)
  // -----------------------------------------------------------------------
  reg [EXT_LANES_P-1:0]    valid_r, dir_r, onwire_r;
  reg [EXT_LANES_P*64-1:0] sid_r;

  assign lane_sid_o  = sid_r;
  //! keep matching while a withdraw is pending so late events settle sanely
  assign lane_en_o   = valid_r;
  assign row_valid_o = valid_r;
  assign row_dir_o   = dir_r;
  assign row_sid_o   = sid_r;

  // -----------------------------------------------------------------------
  // Record RAM: 120-bit row {dmac, prio_rank, max_frame, interval, latency}.
  // Sync-only write; ONE explicit read port whose address is muxed between
  // the serializer (priority) and the provisioning readback.
  // -----------------------------------------------------------------------
  reg [119:0] rec_ram_r [0:EXT_LANES_P-1];

  wire        svc_w     = ctx_req_i && !ctx_gnt_o;    //! service this cycle
  wire        idx_ext_w = (ctx_idx_i != 4'd0) &&
                          ({28'd0, ctx_idx_i} < N_CTX_P);
  wire [3:0]  ext_row_w = ctx_idx_i - 4'd1;
  wire        wr_en_w   = svc_w && ctx_we_i && idx_ext_w;

  always_ff @(posedge clk_i) begin : rec_ram_wr_S
    if (wr_en_w && ctx_valid_i) begin
      rec_ram_r[ext_row_w] <= {ctx_dmac_i, ctx_prio_rank_i,
                               ctx_max_frame_i, ctx_interval_i,
                               ctx_latency_i};
    end
  end

  //! the serializer owns the ONE read port outright; the provisioning
  //! readback returns flop state only (sid + status) so no address mux —
  //! and no second implicit port — can ever exist on this RAM
  always_ff @(posedge clk_i) begin : rec_ram_rd_S
    rec_data_o <=
        rec_ram_r[(rec_addr_i < 4'(EXT_LANES_P)) ? rec_addr_i : 4'd0];
  end

  // -----------------------------------------------------------------------
  // Per-row dynamic registrar state (shared update rules, parallel flops)
  // -----------------------------------------------------------------------
  reg [EXT_LANES_P-1:0]         areg_r;      //! attribute registered
  reg [EXT_LANES_P-1:0]         afail_r;     //! TalkerFailed state
  reg [EXT_LANES_P*2-1:0]       adecl_r;     //! four-packed decl (talker dir)
  reg [EXT_LANES_P*8-1:0]       acode_r;     //! failure code
  reg [EXT_LANES_P*LV_W_C-1:0]  rleave_r;    //! registration leave counter
  reg [EXT_LANES_P*LV_W_C-1:0]  fleave_r;    //! failure leave (listener dir)

  //! per-direction "ready" view
  wire [EXT_LANES_P-1:0] eready_w;
  generate
    for (genvar gr = 0; gr < int'(EXT_LANES_P); gr++) begin : g_ready
      assign eready_w[gr] = dir_r[gr]
          ? areg_r[gr]                               // listener: TA registered
          : (areg_r[gr] &&                           // talker: Ready/ReadyFail
             ((adecl_r[2*gr +: 2] == LSTN_DECL_READY_C) ||
              (adecl_r[2*gr +: 2] == LSTN_DECL_READY_FAIL_C)));
    end
  endgenerate
  assign row_ready_o = eready_w;

  //! status vectors, bit 0 = legacy; rows above N pad zero (EXT <= 15).
  //! With N_CTX_P = 1 the single lane is permanently invalid -> bit 1 = 0.
  wire [EXT_LANES_P-1:0] eused_w = valid_r;
  assign ctx_reg_o    = {15'(areg_r  & eused_w), leg_reg_i};
  assign ctx_ready_o  = {15'(eready_w & eused_w), leg_ready_i};
  assign ctx_failed_o = {15'(afail_r & eused_w), leg_failed_i};

  //! registering / leave event decodes per lane
  wire [EXT_LANES_P-1:0] jn_w, in_w, lv_w;
  generate
    for (genvar ge = 0; ge < int'(EXT_LANES_P); ge++) begin : g_evt
      wire [2:0] e = lane_evt_i[3*ge +: 3];
      assign jn_w[ge] = (e == MRP_EVT_NEW_C) || (e == MRP_EVT_JOININ_C) ||
                        (e == MRP_EVT_JOINMT_C);
      assign in_w[ge] = (e == MRP_EVT_IN_C);
      assign lv_w[ge] = (e == MRP_EVT_LV_C);
    end
  endgenerate

  always_ff @(posedge clk_i or negedge rst_n) begin : ctx_registrar_S
    if (!rst_n) begin
      areg_r <= '0; afail_r <= '0; adecl_r <= '0; acode_r <= '0;
      rleave_r <= '0; fleave_r <= '0;
    end else if (!enable_i) begin
      areg_r <= '0; afail_r <= '0; adecl_r <= '0; acode_r <= '0;
      rleave_r <= '0; fleave_r <= '0;
    end else begin
      for (int l = 0; l < int'(EXT_LANES_P); l++) begin
        if (!valid_r[l]) begin
          areg_r[l] <= 1'b0; afail_r[l] <= 1'b0;
          adecl_r[2*l +: 2] <= LSTN_DECL_IGNORE_C;
          rleave_r[LV_W_C*l +: LV_W_C] <= '0;
          fleave_r[LV_W_C*l +: LV_W_C] <= '0;
        end else begin
          // ---- leave expiry (1 kHz) ----
          if (tick_1khz_i && rleave_r[LV_W_C*l +: LV_W_C] != '0) begin
            rleave_r[LV_W_C*l +: LV_W_C] <=
                rleave_r[LV_W_C*l +: LV_W_C] - 1'b1;
            if (rleave_r[LV_W_C*l +: LV_W_C] == LV_W_C'(1)) begin
              areg_r[l] <= 1'b0;
              if (!dir_r[l]) adecl_r[2*l +: 2] <= LSTN_DECL_IGNORE_C;
            end
          end
          if (tick_1khz_i && fleave_r[LV_W_C*l +: LV_W_C] != '0) begin
            fleave_r[LV_W_C*l +: LV_W_C] <=
                fleave_r[LV_W_C*l +: LV_W_C] - 1'b1;
            if (fleave_r[LV_W_C*l +: LV_W_C] == LV_W_C'(1))
              afail_r[l] <= 1'b0;
          end
          // ---- LeaveAll arms the leave window on registered state ----
          if (rx_leaveall_i) begin
            if (areg_r[l] && rleave_r[LV_W_C*l +: LV_W_C] == '0)
              rleave_r[LV_W_C*l +: LV_W_C] <= LV_W_C'(LEAVE_TIME_MS_C);
            if (dir_r[l] && afail_r[l] && fleave_r[LV_W_C*l +: LV_W_C] == '0)
              fleave_r[LV_W_C*l +: LV_W_C] <= LV_W_C'(LEAVE_TIME_MS_C);
          end
          if (!dir_r[l]) begin
            // ---- talker direction: bridge Listener attr + sticky TF ----
            if (lane_lstn_p_i[l]) begin
              if (jn_w[l]) begin
                areg_r[l]          <= 1'b1;
                adecl_r[2*l +: 2]  <= lane_par_i[2*l +: 2];
                rleave_r[LV_W_C*l +: LV_W_C] <= '0;
              end else if (in_w[l] && areg_r[l]) begin
                adecl_r[2*l +: 2]  <= lane_par_i[2*l +: 2];
                rleave_r[LV_W_C*l +: LV_W_C] <= '0;
              end else if (lv_w[l] && areg_r[l] &&
                           rleave_r[LV_W_C*l +: LV_W_C] == '0) begin
                rleave_r[LV_W_C*l +: LV_W_C] <= LV_W_C'(LEAVE_TIME_MS_C);
              end
            end
            if (lane_tfail_p_i[l] && jn_w[l]) begin
              afail_r[l]        <= 1'b1;
              acode_r[8*l +: 8] <= lane_tfail_code_i;
            end else if (lane_tadv_p_i[l]) begin
              afail_r[l] <= 1'b0;         // bridge says we are clean again
            end
          end else begin
            // ---- listener direction: TA/TF registrar (row-0 TA rules) ----
            if (lane_tadv_p_i[l]) begin
              if (jn_w[l] || in_w[l]) begin
                areg_r[l] <= 1'b1;
                rleave_r[LV_W_C*l +: LV_W_C] <= '0;
              end else if (lv_w[l] && areg_r[l]) begin
                rleave_r[LV_W_C*l +: LV_W_C] <= LV_W_C'(LEAVE_TIME_MS_C);
              end
            end
            if (lane_tfail_p_i[l]) begin
              if (jn_w[l] || in_w[l]) begin
                afail_r[l]        <= 1'b1;
                acode_r[8*l +: 8] <= lane_tfail_code_i;
                fleave_r[LV_W_C*l +: LV_W_C] <= '0;
              end else if (lv_w[l] && afail_r[l]) begin
                fleave_r[LV_W_C*l +: LV_W_C] <= LV_W_C'(LEAVE_TIME_MS_C);
              end
            end
          end
        end
      end
    end
  end

  // -----------------------------------------------------------------------
  // Provisioning port + identity writes + declare scheduling
  // -----------------------------------------------------------------------
  reg [2:0] jdiv_r;                        //! /5 join divider (1 s refresh)
  reg       refresh_pend_r;                //! JOININ batch queued
  reg [EXT_LANES_P-1:0] ready_q_r;         //! Ready-change edge detect

  wire any_row_w = |valid_r;
  assign tx_go_o = (|row_lv_o) ||
                   (enable_i && any_row_w &&
                    (refresh_pend_r || (|row_fresh_o)));

  //! readback status mux (combinational; registered into the snapshot)
  wire [3:0]  rb_row_w   = (ext_row_w < 4'(EXT_LANES_P)) ? ext_row_w : 4'd0;
  wire        rb_leg_w   = (ctx_idx_i == 4'd0) || !idx_ext_w;
  wire [15:0] rb_stat_w  = rb_leg_w
      ? {leg_valid_i, 1'b0, leg_declared_i, leg_reg_i, leg_ready_i,
         leg_failed_i, leg_decl_i, leg_code_i}
      : {valid_r[rb_row_w], dir_r[rb_row_w],
         onwire_r[rb_row_w], areg_r[rb_row_w],
         eready_w[rb_row_w], afail_r[rb_row_w],
         adecl_r[2*rb_row_w +: 2], acode_r[8*rb_row_w +: 8]};
  wire [63:0] rb_sid_w   = rb_leg_w ? leg_sid_i
                                    : sid_r[64*rb_row_w +: 64];

  always_ff @(posedge clk_i or negedge rst_n) begin : ctx_port_S
    if (!rst_n) begin
      valid_r <= '0; dir_r <= '0; onwire_r <= '0; sid_r <= '0;
      row_fresh_o <= '0; row_lv_o <= '0;
      ctx_gnt_o <= 1'b0; ctx_rd_sid_o <= '0; ctx_rd_stat_o <= '0;
      jdiv_r <= '0; refresh_pend_r <= 1'b0; fastjoin_p_o <= 1'b0;
      ready_q_r <= '0;
    end else begin
      ctx_gnt_o    <= 1'b0;
      fastjoin_p_o <= 1'b0;

      // ---- refresh cadence: every 5th JoinTime + LeaveAll turns ----
      if (enable_i && join_tick_i)
        jdiv_r <= (jdiv_r == 3'd4) ? 3'd0 : jdiv_r + 3'd1;
      if (enable_i && any_row_w &&
          ((join_tick_i && jdiv_r == 3'd0) || rx_leaveall_i ||
           leaveall_tick_i))
        refresh_pend_r <= 1'b1;
      //! a listener row's Ready <-> AskingFailed change re-declares promptly
      //! (the row-0 acmp_periodic rule; the bridge's reservation depends on
      //! seeing the Ready four-pack)
      ready_q_r <= eready_w & valid_r & dir_r;
      if (enable_i && ((eready_w & valid_r & dir_r) != ready_q_r))
        refresh_pend_r <= 1'b1;

      // ---- serializer completion clears exactly what the frame carried ---
      if (tx_done_i) begin
        refresh_pend_r <= 1'b0;
        row_fresh_o    <= row_fresh_o & ~tx_fresh_i;
        row_lv_o       <= row_lv_o & ~tx_lv_i;
        onwire_r       <= (onwire_r | (valid_r & tx_fresh_i)) & ~tx_lv_i;
      end

      // ---- engine disable: forget the extra rows (no farewell PDU) ----
      if (!enable_i) begin
        valid_r <= '0; onwire_r <= '0;
        row_fresh_o <= '0; row_lv_o <= '0; refresh_pend_r <= 1'b0;
      end else if (svc_w) begin
        ctx_gnt_o     <= 1'b1;
        ctx_rd_stat_o <= rb_stat_w;
        ctx_rd_sid_o  <= rb_sid_w;
        if (ctx_we_i && idx_ext_w) begin
          if (ctx_valid_i) begin
            valid_r[ext_row_w] <= 1'b1;
            dir_r[ext_row_w]   <= ctx_dir_i;
            sid_r[64*ext_row_w +: 64] <= ctx_sid_i;
            row_fresh_o[ext_row_w] <=
                row_fresh_o[ext_row_w] | ~valid_r[ext_row_w];
            row_lv_o[ext_row_w] <= 1'b0;   // re-add cancels a withdraw
            //! fast join (row-0 rule): a NEW listener row must learn the
            //! bridge's steady-state TalkerAdvertise NOW, not in ~10 s
            if (ctx_dir_i && !valid_r[ext_row_w]) fastjoin_p_o <= 1'b1;
            refresh_pend_r <= 1'b1;             // update -> prompt re-declare
          end else begin
            valid_r[ext_row_w] <= 1'b0;
            //! withdraw needs one LV TX only if the attribute is on wire
            if (onwire_r[ext_row_w]) row_lv_o[ext_row_w] <= 1'b1;
            row_fresh_o[ext_row_w] <= 1'b0;
          end
        end
      end
    end
  end

endmodule

`default_nettype wire
