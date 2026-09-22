/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_srp_vlan.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/10 §6.2 F10.3 per-VID refcounted MVRP
//                 membership, Milan §4.3.2 join-before-streaming,
//                 Milan Table 5.3 frozen declaring VID)
//
//  Description : The single MVRP participant: one FSM over a small
//                refcounted per-VID membership table. Users (talker and
//                listener stream FSMs) register with THEIR OWN stream VID —
//                the first user of a VID declares it (New, then JoinIn on
//                the join/periodic cadence), later users of the same VID
//                only increment the count, and the LAST user leaving emits
//                Lv. Because the table is keyed by the VID each user
//                brought, a Domain default-VID change never moves an
//                existing membership: a declaring talker's VID stays frozen
//                until its last user deregisters (Milan Table 5.3 /
//                §4.3.2), and across the F05.12 withdraw -> re-declare flow
//                two VIDs are briefly live — the steady state is one.
//                LeaveAll or periodic ticks re-join EVERY VID that still
//                has users (F10.3).
//
//  Decision    : the design decision that matters — the membership store
//                follows the KL_pp_timer_service split: {vid, refcount}
//                lives in a 1W1R sync-read RAM walked one entry per cycle
//                (lookup is a serial scan — membership ops are protocol-
//                rate, never wire-rate), while the per-entry ACTIVE bits
//                live in a flop vector so scan qualification and the
//                re-join walk never need a second RAM port or a flop
//                mirror behind a wide read mux.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_srp_vlan #(
    //! membership table entries; steady state is ONE live VID and a Domain
    //! VID change adds one more (10 §6.2) — 4 leaves margin for overlap
    parameter int unsigned N_VIDS_P   = 4,
    //! refcount width: must hold P-N-STREAM-IN + P-N-STREAM-OUT users
    parameter int unsigned REFCNT_W_P = 5
) (
    input  wire         clk_i,            //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,            //! synchronous active-low reset

    // ---- user registration face (stream FSMs not yet landed) -------------
    input  wire         user_valid_i,     //! op offered, held until ready
    input  wire         user_join_i,      //! 1 = join user_vid_i, 0 = leave it
    input  wire  [11:0] user_vid_i,       //! the USER'S stream VID (frozen-VID key)
    output logic        user_ready_o,     //! op accepted this cycle
    output logic        user_err_o,       //! strobe: join with a full table / leave of an unknown VID

    // ---- MVRP participant cadence (timer expiries via the event router) ---
    input  wire         periodic_tick_i,  //! T-MRP-PERIODIC: re-join every held VID
    input  wire         leaveall_tick_i,  //! MVRP LeaveAll cycle: re-join every held VID

    // ---- declaration events toward KL_srp_encoder -------------------------
    output logic        vlan_ev_valid_o,  //! event pending, held until ready
    output logic [2:0]  vlan_ev_event_o,  //! attribute event (0 New, 1 JoinIn, 5 Lv)
    output logic [15:0] vlan_ev_vid_o,    //! MVRP FirstValue (VID)
    input  wire         vlan_ev_ready_i,  //! encoder accepts the event

    // ---- observability ----------------------------------------------------
    output logic [N_VIDS_P-1:0] vid_active_o //! per-entry membership-live bits
);

  localparam int unsigned IDX_W_C  = (N_VIDS_P > 1) ? $clog2(N_VIDS_P) : 1;
  localparam int unsigned ENT_W_C  = 12 + REFCNT_W_P;   // {vid, refcount}
  localparam logic [REFCNT_W_P-1:0] CNT_ONE_C = REFCNT_W_P'(1);
  localparam logic [REFCNT_W_P-1:0] CNT_MAX_C = '1;

  localparam logic [2:0] EV_NEW_C    = 3'd0;
  localparam logic [2:0] EV_JOININ_C = 3'd1;
  localparam logic [2:0] EV_LV_C     = 3'd5;

  // ----------------------------------------------------- membership store
  // {vid, refcount} in a 1W1R sync-read RAM; ACTIVE bits in flops (banner)
  logic [ENT_W_C-1:0] tbl_r [0:N_VIDS_P-1];
  logic [ENT_W_C-1:0] tbl_q_r;
  logic [N_VIDS_P-1:0] active_r;

  logic [IDX_W_C-1:0] rd_addr_w;
  logic               tbl_we_w;
  logic [IDX_W_C-1:0] tbl_wix_w;
  logic [ENT_W_C-1:0] tbl_wdat_w;

  always_ff @(posedge clk_i) begin : tbl_write
    if (tbl_we_w) tbl_r[tbl_wix_w] <= tbl_wdat_w;
  end

  always_ff @(posedge clk_i) begin : tbl_read
    tbl_q_r <= tbl_r[rd_addr_w];
  end

  // ------------------------------------------------------------ FSM state
  typedef enum logic [3:0] {
    V_IDLE  = 4'd0,   // accept a user op or start a re-join walk
    V_SCAN  = 4'd1,   // serial lookup of the op's VID (+ first free slot)
    V_APPLY = 4'd2,   // refcount update / allocate / retire
    V_EV    = 4'd3,   // push New or Lv toward the encoder
    R_SEL   = 4'd4,   // re-join walk: find the next ACTIVE entry
    R_RD    = 4'd5,   // issue its RAM read
    R_CAP   = 4'd6,   // capture the VID
    R_EV    = 4'd7    // push JoinIn toward the encoder
  } vlan_st_e;

  vlan_st_e            st_r;
  logic                op_join_r;
  logic [11:0]         op_vid_r;
  logic [IDX_W_C-1:0]  scan_ix_r;      // address being issued
  logic [IDX_W_C-1:0]  chk_ix_r;       // address whose data is in tbl_q_r
  logic                chk_v_r;
  logic                found_v_r;
  logic [IDX_W_C-1:0]  found_ix_r;
  logic [REFCNT_W_P-1:0] found_cnt_r;
  logic                free_v_r;
  logic [IDX_W_C-1:0]  free_ix_r;
  logic [IDX_W_C-1:0]  ridx_r;         // re-join walk index
  logic                rejoin_pend_r;
  logic [2:0]          ev_code_r;
  logic [15:0]         ev_vid_r;

  logic [11:0]           q_vid_w;
  logic [REFCNT_W_P-1:0] q_cnt_w;
  logic                  scan_done_w;

  assign {q_vid_w, q_cnt_w} = tbl_q_r;
  assign scan_done_w = chk_v_r && (chk_ix_r == IDX_W_C'(N_VIDS_P - 1));

  assign rd_addr_w = (st_r == V_SCAN) ? scan_ix_r : ridx_r;

  // ----------------------------------------------------- table write mux
  always_comb begin : tbl_wmux
    tbl_we_w   = 1'b0;
    tbl_wix_w  = '0;
    tbl_wdat_w = '0;
    if (st_r == V_APPLY) begin
      if (op_join_r && found_v_r) begin
        // another user of a live VID: count up, no wire action (F10.3)
        tbl_we_w   = 1'b1;
        tbl_wix_w  = found_ix_r;
        tbl_wdat_w = {op_vid_r, (found_cnt_r == CNT_MAX_C)
                                ? CNT_MAX_C
                                : found_cnt_r + CNT_ONE_C};
      end else if (op_join_r && free_v_r) begin
        // first user of a VID: allocate and declare it
        tbl_we_w   = 1'b1;
        tbl_wix_w  = free_ix_r;
        tbl_wdat_w = {op_vid_r, CNT_ONE_C};
      end else if (!op_join_r && found_v_r && (found_cnt_r != CNT_ONE_C)) begin
        tbl_we_w   = 1'b1;
        tbl_wix_w  = found_ix_r;
        tbl_wdat_w = {op_vid_r, found_cnt_r - CNT_ONE_C};
      end
    end
  end

  // -------------------------------------------------------------- main SM
  always_ff @(posedge clk_i) begin : vlan_sm
    if (!rst_n) begin
      st_r          <= V_IDLE;
      active_r      <= '0;
      op_join_r     <= 1'b0;
      op_vid_r      <= 12'd0;
      scan_ix_r     <= '0;
      chk_ix_r      <= '0;
      chk_v_r       <= 1'b0;
      found_v_r     <= 1'b0;
      found_ix_r    <= '0;
      found_cnt_r   <= '0;
      free_v_r      <= 1'b0;
      free_ix_r     <= '0;
      ridx_r        <= '0;
      rejoin_pend_r <= 1'b0;
      ev_code_r     <= 3'd0;
      ev_vid_r      <= 16'd0;
      user_err_o    <= 1'b0;
    end else begin
      user_err_o <= 1'b0;
      if (periodic_tick_i || leaveall_tick_i) rejoin_pend_r <= 1'b1;

      unique case (st_r)
        V_IDLE: begin
          chk_v_r <= 1'b0;
          if (user_valid_i) begin
            op_join_r   <= user_join_i;
            op_vid_r    <= user_vid_i;
            scan_ix_r   <= '0;
            found_v_r   <= 1'b0;
            free_v_r    <= 1'b0;
            st_r        <= V_SCAN;
          end else if (rejoin_pend_r) begin
            rejoin_pend_r <= 1'b0;
            if (active_r != '0) begin
              ridx_r <= '0;
              st_r   <= R_SEL;
            end
          end
        end
        V_SCAN: begin
          // issue addr scan_ix; data for chk_ix lands in tbl_q_r
          chk_ix_r <= scan_ix_r;
          chk_v_r  <= 1'b1;
          if (scan_ix_r != IDX_W_C'(N_VIDS_P - 1)) begin
            scan_ix_r <= scan_ix_r + IDX_W_C'(1);
          end
          if (chk_v_r) begin
            if (active_r[chk_ix_r] && (q_vid_w == op_vid_r)) begin
              found_v_r   <= 1'b1;
              found_ix_r  <= chk_ix_r;
              found_cnt_r <= q_cnt_w;
            end
            if (!active_r[chk_ix_r] && !free_v_r) begin
              free_v_r  <= 1'b1;
              free_ix_r <= chk_ix_r;
            end
          end
          if (scan_done_w) st_r <= V_APPLY;
        end
        V_APPLY: begin
          if (op_join_r) begin
            if (found_v_r) begin
              st_r <= V_IDLE;                      // count up, silent
            end else if (free_v_r) begin
              active_r[free_ix_r] <= 1'b1;
              ev_code_r <= EV_NEW_C;               // New, then JoinIn on cadence
              ev_vid_r  <= {4'd0, op_vid_r};
              st_r      <= V_EV;
            end else begin
              user_err_o <= 1'b1;                  // table full
              st_r       <= V_IDLE;
            end
          end else begin
            if (found_v_r && (found_cnt_r == CNT_ONE_C)) begin
              active_r[found_ix_r] <= 1'b0;
              ev_code_r <= EV_LV_C;                // last user gone: Lv (F10.3)
              ev_vid_r  <= {4'd0, op_vid_r};
              st_r      <= V_EV;
            end else if (found_v_r) begin
              st_r <= V_IDLE;                      // count down, silent
            end else begin
              user_err_o <= 1'b1;                  // unknown VID
              st_r       <= V_IDLE;
            end
          end
        end
        V_EV: begin
          if (vlan_ev_ready_i) st_r <= V_IDLE;
        end
        R_SEL: begin
          if (active_r[ridx_r]) begin
            st_r <= R_RD;
          end else if (ridx_r == IDX_W_C'(N_VIDS_P - 1)) begin
            st_r <= V_IDLE;
          end else begin
            ridx_r <= ridx_r + IDX_W_C'(1);
          end
        end
        R_RD: begin
          st_r <= R_CAP;                           // sync read lands next cycle
        end
        R_CAP: begin
          ev_code_r <= EV_JOININ_C;                // re-join every held VID
          ev_vid_r  <= {4'd0, q_vid_w};
          st_r      <= R_EV;
        end
        R_EV: begin
          if (vlan_ev_ready_i) begin
            if (ridx_r == IDX_W_C'(N_VIDS_P - 1)) begin
              st_r <= V_IDLE;
            end else begin
              ridx_r <= ridx_r + IDX_W_C'(1);
              st_r   <= R_SEL;
            end
          end
        end
        default: st_r <= V_IDLE;
      endcase
    end
  end

  // -------------------------------------------------------------- outputs
  assign user_ready_o    = (st_r == V_IDLE);
  assign vlan_ev_valid_o = (st_r == V_EV) || (st_r == R_EV);
  assign vlan_ev_event_o = ev_code_r;
  assign vlan_ev_vid_o   = ev_vid_r;
  assign vid_active_o    = active_r;

endmodule : KL_srp_vlan
`default_nettype wire
