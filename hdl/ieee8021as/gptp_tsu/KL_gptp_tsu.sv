/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_gptp_tsu.sv
  Description : THE TIMESTAMP UNIT of one gPTP port, for gPTP in firmware
                (#884, #665 F6; the owner's decision of 2026-11-21 on #872:
                the fabric gPTP plane is removed, the hardware timestamps and
                the PHC stay in fabric). It times every IEEE 802.1AS event
                message (messageType 0 to 3) the port receives or launches
                and hands each result, a measurement or a counted loss, to
                the firmware as one record, keyed by direction, messageType
                and sequenceId, through a FIFO the mailbox drains into its
                TIMESTAMP events (contract 2.5). It runs no protocol.

                THE ONE DECISION THAT MATTERS: both stamp points and every
                correction are the fabric plane's, unchanged, so the digital
                bound docs/design/GPTP_PLANE.md publishes (+/-11.2 ns on GMII)
                still holds:
                  ingress  the PHC on the edge the frame's first beat is
                           accepted at the receive tap (KL_gptp_shadow's
                           ts_arr_r), less INGRESS_LAT_NS_P
                  egress   the PHC registered on the edge a launch record of
                           KL_gptp_gmii_launch lands (KL_gptp_txret's
                           cap_phc_r), less the derived digital correction,
                           plus EGRESS_LAT_NS_P, valid only when the record
                           is whole (no abort, the expected cycle distance)
                           and the PHC's trajectory was inside the model for
                           the whole reconstructed window (txret's history
                           guard and addend envelope, carried over)
                What leaves with the plane is the ledger that paired launches
                with the engine's frames by position: the firmware pairs a
                record with its own frame by messageType and sequenceId, so
                the unit keeps the observer sealed at one generation and
                reports a record of another generation as a loss.
  Spec refs   : IEEE Std 802.1AS-2020 11.3.9 (the message timestamp point),
                11.4.2 (event messages), 8.4.3 (ingress and egress latency);
                docs/design/GPTP_PLANE.md; docs/design/GPTP_SOFTWARE.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//
`default_nettype none

module KL_gptp_tsu #(
    parameter int unsigned TDATA_WIDTH_P       = 64,
    //! the record FIFO, entries (a power of two)
    parameter int unsigned FIFO_DEPTH_P        = 8,
    //! the egress reconstruction's terms: KL_gptp_txret's, by the same names
    parameter int unsigned ETH_TICK_NS_P       = 8,
    parameter int unsigned ETH_CYC_PER_OCTET_P = 1,
    parameter int unsigned DP_TICK_NS_P        = 20,
    parameter int unsigned OBS_LAT_E_CYC_P     = 2,
    parameter int unsigned CDC_LAT_D_CYC_P     = 2,
    parameter int unsigned TXTS_DELTA_EXP_P    = 45,
    parameter int unsigned TXTS_DELTA_W_P      = 8,
    parameter int unsigned TXTS_OIDX_W_P       = 12,
    parameter int unsigned TXTS_GEN_W_P        = 4,
    parameter int unsigned RECON_GUARD_CYC_P   = 64,
    parameter int unsigned RECON_REL_PPM_P     = 200,
    parameter int unsigned PHC_CLK_HZ_P        = 50_000_000,
    parameter int unsigned SEAL_RETRY_CYC_P    = 256,
    //! the board's latency corrections (issue #358), applied here only
    parameter int unsigned INGRESS_LAT_NS_P    = 0,
    parameter int unsigned EGRESS_LAT_NS_P     = 0
) (
    input  wire                       clk_i,    //! the datapath's clock, the PHC's
    input  wire                       rst_n,    //! synchronous active-low reset
    //! ---- the receive tap (input only, qualified on the handshake)
    input  wire [TDATA_WIDTH_P-1:0]   rx_tdata_i,
    input  wire [TDATA_WIDTH_P/8-1:0] rx_tkeep_i,
    input  wire                       rx_tvalid_i,
    input  wire                       rx_tready_i,
    input  wire                       rx_tlast_i,
    //! ---- the live PHC and the counter's own effective controls (txret's)
    input  wire [63:0]                phc_ns_i,
    input  wire                       phc_en_eff_i,
    input  wire [31:0]                phc_incr_eff_ns_i,
    input  wire signed [31:0]         phc_adj_eff_ns_i,
    input  wire                       phc_load_eff_i,
    input  wire                       phc_adjust_eff_i,
    //! ---- the launch observer's records, already in this domain
    input  wire                       rec_valid_i,
    input  wire                       rec_kind_i,   //! 0 = frame, 1 = echo
    input  wire [TXTS_OIDX_W_P-1:0]   rec_oidx_i,   //! the observer's position, unused: records are keyed
    input  wire [TXTS_GEN_W_P-1:0]    rec_gen_i,    //! the generation the observer adopted
    input  wire [3:0]                 rec_type_i,   //! the frame's messageType
    input  wire [15:0]                rec_seq_i,    //! the frame's sequenceId
    input  wire [TXTS_DELTA_W_P-1:0]  rec_delta_i,  //! the observer's measured distance, against TXTS_DELTA_EXP_P
    input  wire                       rec_abort_i,  //! the launch was aborted: no measurement
    //! ---- the seal offered to the observer
    output logic                      seal_req_o,
    output logic [TXTS_GEN_W_P-1:0]   seal_gen_o,
    input  wire                       seal_ack_i,
    //! ---- the records: {EGRESS, OK, MSG_TYPE, SEQUENCE_ID, STAMP}, STAMP lowest, the PHC's 64-bit time
    output logic                      ts_valid_o,
    output logic [85:0]               ts_data_o,
    input  wire                       ts_take_p_i,
    //! ---- counters, wrapping
    output logic [15:0]               dbg_drop_o,    //! records the FIFO could not hold
    output logic [15:0]               dbg_lost_o     //! egress records with no measurement
);

  // ---- derived constants: KL_gptp_txret's, by its derivation -------------
  localparam int unsigned TXTS_CORR_NS_C =
      (TXTS_DELTA_EXP_P + OBS_LAT_E_CYC_P + ETH_CYC_PER_OCTET_P - 1) * ETH_TICK_NS_P
    + CDC_LAT_D_CYC_P * DP_TICK_NS_P
    + DP_TICK_NS_P / 2;
  localparam longint signed TXTS_NET_NS_C = longint'(TXTS_CORR_NS_C) - longint'(EGRESS_LAT_NS_P);
  localparam int unsigned RECON_NEED_CYC_C = TXTS_CORR_NS_C / DP_TICK_NS_P + 15;
  localparam int unsigned RECON_GUARD_CYC_C =
      (RECON_NEED_CYC_C > RECON_GUARD_CYC_P) ? RECON_NEED_CYC_C : RECON_GUARD_CYC_P;
  localparam int unsigned GDW_C = $clog2(RECON_GUARD_CYC_C + 1);
  localparam logic [31:0] PHC_INCR_NOM_C = 32'(DP_TICK_NS_P << 24);
  localparam longint unsigned PHC_ADJ_MAX_C =
      (longint'(RECON_REL_PPM_P) * (longint'(1) << 24) * 1000
       + longint'(PHC_CLK_HZ_P) / 2) / longint'(PHC_CLK_HZ_P);
  localparam int unsigned PW_C  = $clog2(FIFO_DEPTH_P);
  localparam int unsigned SRT_C = $clog2(SEAL_RETRY_CYC_P + 1);
  //! the generation this unit seals the observer into; never 0
  localparam logic [TXTS_GEN_W_P-1:0] GEN_C = TXTS_GEN_W_P'(1);

  if (TDATA_WIDTH_P != 64) begin : g_width_check
    $error("KL_gptp_tsu: TDATA_WIDTH_P must be 64 (the tap's lane arithmetic), got %0d", TDATA_WIDTH_P);
  end
  if ((FIFO_DEPTH_P & (FIFO_DEPTH_P - 1)) != 0 || FIFO_DEPTH_P < 2) begin : g_depth_check
    $error("KL_gptp_tsu: FIFO_DEPTH_P must be a power of two of at least 2, got %0d", FIFO_DEPTH_P);
  end

  localparam logic [47:0] DA_GPTP_C = 48'h01_80_C2_00_00_0E;   //! IEEE 802.1AS-2020 Table 11-3
  localparam logic [15:0] ET_GPTP_C = 16'h88F7;

  // ======================================================================= //
  //  Ingress: the first accepted beat's PHC, the key from beats 1 and 5    //
  // ======================================================================= //
  logic beat_w;
  assign beat_w = rx_tvalid_i & rx_tready_i;
  //! beat 0 lanes 0-5 the destination; beat 1 lanes 4-5 the EtherType and
  //! lane 6 the PTP header's first octet (majorSdoId | messageType); beat 5
  //! lanes 4-5 the sequenceId (frame octets 44 and 45)
  logic [2:0]  rx_beat_r;     //! beats of this frame accepted so far, saturating at 6
  logic        rx_cand_r;     //! still a gPTP event message
  logic [3:0]  rx_type_r;
  logic [63:0] rx_ts_r;
  logic        rx_push_w;
  logic [15:0] rx_seq_w;
  logic [47:0] da_w;
  assign da_w = {rx_tdata_i[7:0], rx_tdata_i[15:8], rx_tdata_i[23:16],
                 rx_tdata_i[31:24], rx_tdata_i[39:32], rx_tdata_i[47:40]};
  assign rx_seq_w  = {rx_tdata_i[39:32], rx_tdata_i[47:40]};
  assign rx_push_w = beat_w && rx_cand_r && (rx_beat_r == 3'd5) && (&rx_tkeep_i[5:4]);

  always_ff @(posedge clk_i) begin : rx_tap
    if (!rst_n) begin
      rx_beat_r <= '0;
      rx_cand_r <= 1'b0;
      rx_type_r <= '0;
      rx_ts_r   <= '0;
    end else if (beat_w) begin
      if (rx_beat_r == 3'd0) begin
        //! THE INGRESS STAMP POINT: the plane's, on this same edge
        rx_ts_r   <= phc_ns_i - 64'(INGRESS_LAT_NS_P);
        rx_cand_r <= (da_w == DA_GPTP_C) && !rx_tlast_i;
      end else if (rx_beat_r == 3'd1) begin
        rx_type_r <= rx_tdata_i[51:48];
        rx_cand_r <= rx_cand_r && ({rx_tdata_i[39:32], rx_tdata_i[47:40]} == ET_GPTP_C)
                     && (rx_tdata_i[55:52] == 4'h1) && (rx_tdata_i[51:50] == 2'b00) && !rx_tlast_i;
      end else if (rx_beat_r == 3'd5) begin
        rx_cand_r <= 1'b0;
      end
      rx_beat_r <= rx_tlast_i ? 3'd0 : ((rx_beat_r == 3'd6) ? 3'd6 : rx_beat_r + 3'd1);
    end
  end : rx_tap

  // ======================================================================= //
  //  Egress: the PHC history guard and the capture (KL_gptp_txret's)       //
  // ======================================================================= //
  logic signed [31:0] adj_eff_w;
  logic [31:0]        adj_abs_w;
  logic               elig_now_w, phc_chg_w;
  logic [GDW_C-1:0]   phc_dirty_r;
  logic               phc_en_d_r;
  logic [31:0]        phc_incr_d_r;
  logic signed [31:0] phc_adj_d_r;
  assign adj_eff_w  = phc_adj_eff_ns_i;
  assign adj_abs_w  = adj_eff_w[31] ? unsigned'(-adj_eff_w) : unsigned'(adj_eff_w);
  assign elig_now_w = phc_en_eff_i && (phc_incr_eff_ns_i == PHC_INCR_NOM_C)
                   && (longint'(adj_abs_w) <= PHC_ADJ_MAX_C);
  assign phc_chg_w  = (phc_en_eff_i != phc_en_d_r) || (phc_incr_eff_ns_i != phc_incr_d_r)
                   || (phc_adj_eff_ns_i != phc_adj_d_r) || phc_load_eff_i || phc_adjust_eff_i;
  always_ff @(posedge clk_i) begin : phc_history
    if (!rst_n) begin
      phc_dirty_r  <= GDW_C'(RECON_GUARD_CYC_C);
      phc_en_d_r   <= 1'b0;
      phc_incr_d_r <= 32'd0;
      phc_adj_d_r  <= 32'sd0;
    end else begin
      phc_en_d_r   <= phc_en_eff_i;
      phc_incr_d_r <= phc_incr_eff_ns_i;
      phc_adj_d_r  <= phc_adj_eff_ns_i;
      if (!elig_now_w || phc_chg_w) phc_dirty_r <= GDW_C'(RECON_GUARD_CYC_C);
      else if (|phc_dirty_r)        phc_dirty_r <= phc_dirty_r - GDW_C'(1);
    end
  end : phc_history

  logic                      cap_v_r, cap_kind_r, cap_abort_r, cap_elig_r;
  logic [TXTS_GEN_W_P-1:0]   cap_gen_r;
  logic [3:0]                cap_type_r;
  logic [15:0]               cap_seq_r;
  logic [TXTS_DELTA_W_P-1:0] cap_delta_r;
  logic [63:0]               cap_phc_r;
  always_ff @(posedge clk_i) begin : capture
    if (!rst_n) begin
      cap_v_r     <= 1'b0;
      cap_kind_r  <= 1'b0;
      cap_abort_r <= 1'b0;
      cap_elig_r  <= 1'b0;
      cap_gen_r   <= '0;
      cap_type_r  <= '0;
      cap_seq_r   <= '0;
      cap_delta_r <= '0;
      cap_phc_r   <= '0;
    end else begin
      cap_v_r <= rec_valid_i;
      if (rec_valid_i) begin
        //! THE EGRESS CAPTURE POINT: txret's, on this same edge
        cap_elig_r  <= (phc_dirty_r == GDW_C'(0));
        cap_kind_r  <= rec_kind_i;
        cap_gen_r   <= rec_gen_i;
        cap_type_r  <= rec_type_i;
        cap_seq_r   <= rec_seq_i;
        cap_delta_r <= rec_delta_i;
        cap_abort_r <= rec_abort_i;
        cap_phc_r   <= phc_ns_i;
      end
    end
  end : capture

  //! the seal: offered until the observer echoes this unit's generation
  logic             echo_ok_r;
  logic [SRT_C-1:0] seal_tmr_r;
  wire  frame_w = cap_v_r & ~cap_kind_r;
  wire  echo_w  = cap_v_r &  cap_kind_r;
  wire  gen_ok_w = echo_ok_r && (cap_gen_r == GEN_C);
  always_ff @(posedge clk_i) begin : seal
    if (!rst_n) begin
      echo_ok_r  <= 1'b0;
      seal_req_o <= 1'b0;
      seal_tmr_r <= '0;
    end else begin
      if (echo_w && cap_gen_r == GEN_C) echo_ok_r <= 1'b1;
      //! a frame of another generation means the observer was reset: seal again
      if (frame_w && cap_gen_r != GEN_C) echo_ok_r <= 1'b0;
      if (!echo_ok_r) begin
        if (seal_tmr_r == SRT_C'(SEAL_RETRY_CYC_P)) begin
          seal_tmr_r <= '0;
          seal_req_o <= ~seal_req_o;
        end else begin
          seal_tmr_r <= seal_tmr_r + SRT_C'(1);
        end
      end else begin
        seal_req_o <= 1'b0;
        seal_tmr_r <= '0;
      end
    end
  end : seal
  assign seal_gen_o = GEN_C;

  //! an egress record: a whole frame of this generation, inside the model,
  //! is a measurement; every other event-message frame is a counted loss
  logic tx_event_w, tx_ok_w;
  assign tx_event_w = frame_w && (cap_type_r[3:2] == 2'b00);
  assign tx_ok_w    = gen_ok_w && !cap_abort_r && cap_elig_r
                   && (cap_delta_r == TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P));

  // ======================================================================= //
  //  The record FIFO                                                        //
  // ======================================================================= //
  logic [85:0] fifo_r [FIFO_DEPTH_P];
  logic [PW_C:0] wp_r, rp_r;
  logic          full_w, push_w, pop_w;
  logic [85:0]   push_rec_w;
  assign full_w = (wp_r - rp_r) == (PW_C+1)'(FIFO_DEPTH_P);
  //! an egress record and an ingress record never land on one edge in
  //! practice (a launch record is two clocks of a frame the tap is not
  //! seeing), but if they do, egress goes first and ingress next cycle
  logic        rx_hold_r;
  logic [85:0] rx_rec_r;
  always_comb begin : pick
    push_w     = 1'b0;
    push_rec_w = '0;
    if (tx_event_w) begin
      push_w     = 1'b1;
      push_rec_w = {1'b1, tx_ok_w, cap_type_r, cap_seq_r,
                    tx_ok_w ? (cap_phc_r - 64'(TXTS_NET_NS_C)) : 64'd0};
    end else if (rx_hold_r) begin
      push_w     = 1'b1;
      push_rec_w = rx_rec_r;
    end else if (rx_push_w) begin
      push_w     = 1'b1;
      push_rec_w = {1'b0, 1'b1, rx_type_r, rx_seq_w, rx_ts_r};
    end
  end : pick
  assign pop_w = ts_take_p_i && ts_valid_o;

  always_ff @(posedge clk_i) begin : fifo
    if (!rst_n) begin
      wp_r       <= '0;
      rp_r       <= '0;
      rx_hold_r  <= 1'b0;
      rx_rec_r   <= '0;
      dbg_drop_o <= '0;
      dbg_lost_o <= '0;
    end else begin
      rx_hold_r <= 1'b0;
      if (tx_event_w && (rx_hold_r || rx_push_w)) begin
        rx_hold_r <= 1'b1;
        rx_rec_r  <= rx_hold_r ? rx_rec_r : {1'b0, 1'b1, rx_type_r, rx_seq_w, rx_ts_r};
      end
      if (push_w) begin
        if (full_w && !pop_w) begin
          dbg_drop_o <= dbg_drop_o + 16'd1;
        end else begin
          fifo_r[wp_r[PW_C-1:0]] <= push_rec_w;
          wp_r <= wp_r + (PW_C+1)'(1);
        end
      end
      if (pop_w) rp_r <= rp_r + (PW_C+1)'(1);
      if (tx_event_w && !tx_ok_w) dbg_lost_o <= dbg_lost_o + 16'd1;
    end
  end : fifo
  assign ts_valid_o = wp_r != rp_r;
  assign ts_data_o  = fifo_r[rp_r[PW_C-1:0]];

  //! the observer's index, the seal's delivery report and the frame octets
  //! past the key are not read: identity is the key, not the position
  logic unused_w;
  assign unused_w = ^{rec_oidx_i, seal_ack_i, rx_tkeep_i[7:6], rx_tkeep_i[3:0]};

endmodule

`default_nettype wire
