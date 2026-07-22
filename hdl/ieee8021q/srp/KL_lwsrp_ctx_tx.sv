/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_ctx_tx.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : SHARED applicant serializer for the extra context rows
//                (table rows 1..N-1; row 0 keeps the proven KL_lwsrp_tx
//                template path byte-for-byte). One byte-serial engine walks
//                the context table and emits ONE MSRP MRPDU per declare
//                batch, packing every declared attribute into it
//                (802.1Q §35.2 encoding):
//
//                  [eth 14 B][ver 0]
//                  [TalkerAdvertise msg: hdr(4) + one single-value vector
//                   (28 B) per talker row + EndMark]        (if any)
//                  [Listener msg: hdr(4) + one single-value vector (12 B)
//                   per listener row + EndMark]             (if any)
//                  [message-list EndMark][pad to 60]
//
//                AttributeListLength = nRows*vector + 2, byte-exact per the
//                pipewire contract; vectors are NumberOfValues = 1 like the
//                row-0 applicant (bridges aggregate, endpoints need not).
//                Event selection per row mirrors mrp.c: NEW on the first TX
//                after provisioning, JOININ on refresh, LV on withdraw; the
//                Listener four-pack follows the row's TA registration
//                (Ready / AskingFailed).
//
//                Row records stream out of the context table's single RAM
//                read port (2-cycle prefetch per talker row); tvalid gaps
//                mid-frame are AXIS-legal and absorbed by the low-rate
//                control merge. The frame masks are LATCHED at frame start
//                and handed back on tx_done_o so KL_lwsrp_ctx clears
//                exactly what went on the wire (a provisioning write racing
//                the frame is never half-forgotten).
//---------------------------------------------------------------------------//

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_ctx_tx #(
  parameter int unsigned EXT_LANES_P = 1
)(
    input  wire        clk_i,
    input  wire        rst_n,
    input  wire        enable_i,          //! lwSRP engine enable (CSR)

    // ---- shared identity -------------------------------------------------
    input  wire [47:0] station_mac_i,     //! [47:40] = first wire byte
    input  wire [11:0] vid_i,             //! SR VID (DataFrameParams)

    // ---- context table hookup (KL_lwsrp_ctx) -----------------------------
    input  wire [EXT_LANES_P-1:0]    row_valid_i,
    input  wire [EXT_LANES_P-1:0]    row_dir_i,   //! 0 talker, 1 listener
    input  wire [EXT_LANES_P-1:0]    row_fresh_i,
    input  wire [EXT_LANES_P-1:0]    row_lv_i,
    input  wire [EXT_LANES_P-1:0]    row_ready_i,
    input  wire [EXT_LANES_P*64-1:0] row_sid_i,
    input  wire                      tx_go_i,
    output reg                       tx_done_o,   //! one-cycle, frame sent
    output reg  [EXT_LANES_P-1:0]    tx_fresh_o,  //! latched batch masks
    output reg  [EXT_LANES_P-1:0]    tx_lv_o,
    //! record RAM read port (sync, 1-cycle):
    //! {dmac[119:72], prio_rank[71:64], max_frame[63:48],
    //!  interval[47:32], latency[31:0]}
    output wire [3:0]                rec_addr_o,
    input  wire [119:0]              rec_data_i,

    // ---- AXI4-Stream master (little lane; -> the top-level frame mux) ----
    output logic [63:0] m_axis_tdata,
    output logic [7:0]  m_axis_tkeep,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  wire         m_axis_tready,

    output reg  [15:0]  tx_count_o         //! extra-context MRPDUs sent
);

  localparam int unsigned PAD_LEN_C   = 60;
  localparam int unsigned GAP_CYC_C   = 8;
  localparam int unsigned TVEC_LEN_C  = 28;  //! vech2 + FV25 + evt1
  localparam int unsigned LVEC_LEN_C  = 12;  //! vech2 + FV8 + evt1 + par1

  // -----------------------------------------------------------------------
  // Row helpers
  // -----------------------------------------------------------------------
  function automatic [4:0] popcnt(input [EXT_LANES_P-1:0] m);
    popcnt = '0;
    for (int i = 0; i < int'(EXT_LANES_P); i++) popcnt += 5'(m[i]);
  endfunction

  //! lowest set row with index >= from; 4'hF = none
  function automatic [3:0] find_row(input [EXT_LANES_P-1:0] m,
                                    input [3:0] from);
    find_row = 4'hF;
    for (int i = int'(EXT_LANES_P) - 1; i >= 0; i--)
      if (m[i] && (4'(i) >= from)) find_row = 4'(i);
  endfunction

  // -----------------------------------------------------------------------
  // Frame batch latches
  // -----------------------------------------------------------------------
  reg [EXT_LANES_P-1:0] t_mask_r, l_mask_r, ready_q_r;
  reg [4:0]             nt_r, nl_r;
  reg [9:0]             frame_len_r;

  wire [EXT_LANES_P-1:0] incl_w = row_valid_i | row_lv_i;

  // -----------------------------------------------------------------------
  // Serializer FSM
  // -----------------------------------------------------------------------
  typedef enum logic [2:0] {
    C_IDLE_S, C_LATCH_S, C_LOAD1_S, C_LOAD2_S, C_RUN_S, C_FLUSH_S, C_GAP_S
  } cst_t;
  typedef enum logic [3:0] {
    S_HDR_E, S_TMH_E, S_TVEC_E, S_TEND_E, S_LMH_E, S_LVEC_E, S_LEND_E,
    S_MLE_E, S_PAD_E
  } sec_t;

  cst_t       st_r;
  sec_t       sec_r;
  reg [4:0]   off_r;          //! byte offset inside the section
  reg [3:0]   row_r;          //! current table row
  reg         loaded_r;       //! rec_q_r holds row_r's record
  reg [119:0] rec_q_r;
  reg [9:0]   fb_cnt_r;       //! frame byte counter
  reg [63:0]  beat_r;
  reg [2:0]   bidx_r;         //! byte lane inside the beat
  reg         last_beat_r;
  reg [3:0]   gap_r;

  assign rec_addr_o = row_r;

  //! per-row three-packed event octet (single value: e0*36)
  function automatic [7:0] row_evt(input [3:0] row);
    if (row_lv_i[row] || tx_lv_o[row])      row_evt = 8'(MRP_EVT_LV_C) * 8'd36;
    else if (tx_fresh_o[row])               row_evt = 8'(MRP_EVT_NEW_C) * 8'd36;
    else                                    row_evt = 8'(MRP_EVT_JOININ_C) * 8'd36;
  endfunction

  //! current frame byte (combinational over latched state + rec_q_r)
  logic [7:0] byte_w;
  always_comb begin
    logic [15:0] listlen;
    byte_w = 8'h00;
    unique case (sec_r)
      S_HDR_E: begin
        unique case (off_r)
          5'd0:  byte_w = MSRP_MCAST_MAC_C[47:40];
          5'd1:  byte_w = MSRP_MCAST_MAC_C[39:32];
          5'd2:  byte_w = MSRP_MCAST_MAC_C[31:24];
          5'd3:  byte_w = MSRP_MCAST_MAC_C[23:16];
          5'd4:  byte_w = MSRP_MCAST_MAC_C[15:8];
          5'd5:  byte_w = MSRP_MCAST_MAC_C[7:0];
          5'd6:  byte_w = station_mac_i[47:40];
          5'd7:  byte_w = station_mac_i[39:32];
          5'd8:  byte_w = station_mac_i[31:24];
          5'd9:  byte_w = station_mac_i[23:16];
          5'd10: byte_w = station_mac_i[15:8];
          5'd11: byte_w = station_mac_i[7:0];
          5'd12: byte_w = MSRP_ETHERTYPE_C[15:8];
          5'd13: byte_w = MSRP_ETHERTYPE_C[7:0];
          default: byte_w = MRP_PROTO_VER_C;
        endcase
      end
      S_TMH_E: begin
        listlen = 16'(nt_r) * 16'(TVEC_LEN_C) + 16'd2;
        unique case (off_r)
          5'd0: byte_w = MSRP_ATTR_TALKER_ADV_C;
          5'd1: byte_w = MSRP_LEN_TALKER_ADV_C;
          5'd2: byte_w = listlen[15:8];
          default: byte_w = listlen[7:0];
        endcase
      end
      S_TVEC_E: begin
        unique case (off_r)
          5'd0:  byte_w = 8'h00;                       // vech hi (no LeaveAll)
          5'd1:  byte_w = 8'h01;                       // NumberOfValues = 1
          5'd2, 5'd3, 5'd4, 5'd5, 5'd6, 5'd7, 5'd8, 5'd9:
                 byte_w = row_sid_i[64*row_r + 8*(4'd9 - off_r[3:0]) +: 8];
          5'd10: byte_w = rec_q_r[119:112];            // DataFrameParams DMAC
          5'd11: byte_w = rec_q_r[111:104];
          5'd12: byte_w = rec_q_r[103:96];
          5'd13: byte_w = rec_q_r[95:88];
          5'd14: byte_w = rec_q_r[87:80];
          5'd15: byte_w = rec_q_r[79:72];
          5'd16: byte_w = {4'h0, vid_i[11:8]};
          5'd17: byte_w = vid_i[7:0];
          5'd18: byte_w = rec_q_r[63:56];              // TSpec MaxFrameSize
          5'd19: byte_w = rec_q_r[55:48];
          5'd20: byte_w = rec_q_r[47:40];              // MaxIntervalFrames
          5'd21: byte_w = rec_q_r[39:32];
          5'd22: byte_w = rec_q_r[71:64];              // PriorityAndRank
          5'd23: byte_w = rec_q_r[31:24];              // AccumulatedLatency
          5'd24: byte_w = rec_q_r[23:16];
          5'd25: byte_w = rec_q_r[15:8];
          5'd26: byte_w = rec_q_r[7:0];
          default: byte_w = row_evt(row_r);
        endcase
      end
      S_LMH_E: begin
        listlen = 16'(nl_r) * 16'(LVEC_LEN_C) + 16'd2;
        unique case (off_r)
          5'd0: byte_w = MSRP_ATTR_LISTENER_C;
          5'd1: byte_w = MSRP_LEN_LISTENER_C;
          5'd2: byte_w = listlen[15:8];
          default: byte_w = listlen[7:0];
        endcase
      end
      S_LVEC_E: begin
        unique case (off_r)
          5'd0:  byte_w = 8'h00;
          5'd1:  byte_w = 8'h01;
          5'd2, 5'd3, 5'd4, 5'd5, 5'd6, 5'd7, 5'd8, 5'd9:
                 byte_w = row_sid_i[64*row_r + 8*(4'd9 - off_r[3:0]) +: 8];
          5'd10: byte_w = row_evt(row_r);
          default:                                     // four-packed decl
                 byte_w = {ready_q_r[row_r] ? LSTN_DECL_READY_C
                                            : LSTN_DECL_ASKING_FAIL_C,
                           6'b000000};
        endcase
      end
      //! S_TEND / S_LEND / S_MLE / S_PAD are all zeros
      default: byte_w = 8'h00;
    endcase
  end

  //! section byte counts
  wire [4:0] sec_len_w = (sec_r == S_HDR_E)  ? 5'd15
                       : (sec_r == S_TMH_E)  ? 5'd4
                       : (sec_r == S_TVEC_E) ? 5'(TVEC_LEN_C)
                       : (sec_r == S_LMH_E)  ? 5'd4
                       : (sec_r == S_LVEC_E) ? 5'(LVEC_LEN_C)
                       : 5'd2;               //! TEND/LEND/MLE (PAD unused)
  wire sec_end_w   = (sec_r != S_PAD_E) && (off_r == sec_len_w - 5'd1);
  wire frame_end_w = (fb_cnt_r == frame_len_r - 10'd1);

  // AXIS beat presentation
  always_comb begin
    m_axis_tvalid = (st_r == C_FLUSH_S);
    m_axis_tdata  = beat_r;
    m_axis_tlast  = (st_r == C_FLUSH_S) && last_beat_r;
    m_axis_tkeep  = (st_r == C_FLUSH_S)
                  ? 8'((16'd1 << (16'(bidx_r) + 16'd1)) - 16'd1)
                  : 8'h00;
  end

  always_ff @(posedge clk_i or negedge rst_n) begin : ctx_tx_S
    sec_t nsec;
    logic [3:0] nrow;
    logic       need_load;
    if (!rst_n) begin
      st_r <= C_IDLE_S; sec_r <= S_HDR_E; off_r <= '0; row_r <= '0;
      loaded_r <= 1'b0; rec_q_r <= '0; fb_cnt_r <= '0;
      beat_r <= '0; bidx_r <= '0; last_beat_r <= 1'b0; gap_r <= '0;
      t_mask_r <= '0; l_mask_r <= '0; ready_q_r <= '0;
      nt_r <= '0; nl_r <= '0; frame_len_r <= 10'(PAD_LEN_C);
      tx_done_o <= 1'b0; tx_fresh_o <= '0; tx_lv_o <= '0;
      tx_count_o <= 16'd0;
    end else begin
      tx_done_o <= 1'b0;

      unique case (st_r)
        C_IDLE_S: begin
          if (tx_go_i && (incl_w != '0)) begin
            t_mask_r   <= incl_w & ~row_dir_i;
            l_mask_r   <= incl_w & row_dir_i;
            tx_fresh_o <= row_fresh_i & incl_w;
            tx_lv_o    <= row_lv_i;
            ready_q_r  <= row_ready_i;
            st_r       <= C_LATCH_S;
          end
        end

        C_LATCH_S: begin : latch_b
          logic [9:0] core;
          nt_r <= popcnt(t_mask_r);
          nl_r <= popcnt(l_mask_r);
          core = 10'd17                                     // hdr+ver+MLE
               + ((t_mask_r != '0)
                  ? 10'd6 + 10'(popcnt(t_mask_r)) * 10'(TVEC_LEN_C) : 10'd0)
               + ((l_mask_r != '0)
                  ? 10'd6 + 10'(popcnt(l_mask_r)) * 10'(LVEC_LEN_C) : 10'd0);
          frame_len_r <= (core < 10'(PAD_LEN_C)) ? 10'(PAD_LEN_C) : core;
          sec_r <= S_HDR_E; off_r <= '0; fb_cnt_r <= '0; bidx_r <= '0;
          row_r <= '0; loaded_r <= 1'b0; last_beat_r <= 1'b0;
          st_r <= C_RUN_S;
        end

        //! record prefetch: address settles (C_LOAD1), RAM output registers
        //! (C_LOAD2 captures it) — the table's one read port, 2 cycles/row
        C_LOAD1_S: st_r <= C_LOAD2_S;
        C_LOAD2_S: begin
          rec_q_r  <= rec_data_i;
          loaded_r <= 1'b1;
          st_r     <= C_RUN_S;
        end

        C_RUN_S: begin
          if ((sec_r == S_TVEC_E) && !loaded_r) begin
            st_r <= C_LOAD1_S;
          end else begin
            // ---- emit one byte into the beat ----
            beat_r[8*bidx_r +: 8] <= byte_w;
            fb_cnt_r <= fb_cnt_r + 10'd1;

            // ---- cursor advance ----
            nsec = sec_r; nrow = row_r; need_load = 1'b0;
            if (sec_end_w) begin
              off_r <= '0;
              unique case (sec_r)
                S_HDR_E: begin
                  if (t_mask_r != '0) begin
                    nsec = S_TMH_E;
                  end else if (l_mask_r != '0) begin
                    nsec = S_LMH_E;
                  end else begin
                    nsec = S_MLE_E;   // unreachable: batch never empty
                  end
                end
                S_TMH_E: begin
                  nsec = S_TVEC_E;
                  nrow = find_row(t_mask_r, 4'd0);
                  need_load = 1'b1;
                end
                S_TVEC_E: begin
                  nrow = find_row(t_mask_r, row_r + 4'd1);
                  if (nrow != 4'hF) begin
                    nsec = S_TVEC_E; need_load = 1'b1;
                  end else begin
                    nsec = S_TEND_E; nrow = row_r;
                  end
                end
                S_TEND_E: nsec = (l_mask_r != '0) ? S_LMH_E : S_MLE_E;
                S_LMH_E: begin
                  nsec = S_LVEC_E;
                  nrow = find_row(l_mask_r, 4'd0);
                end
                S_LVEC_E: begin
                  nrow = find_row(l_mask_r, row_r + 4'd1);
                  if (nrow != 4'hF) nsec = S_LVEC_E;
                  else begin nsec = S_LEND_E; nrow = row_r; end
                end
                S_LEND_E: nsec = S_MLE_E;
                S_MLE_E:  nsec = S_PAD_E;
                default:  nsec = S_PAD_E;
              endcase
              sec_r    <= nsec;
              row_r    <= (nrow == 4'hF) ? row_r : nrow;
              loaded_r <= !need_load && loaded_r;
            end else begin
              off_r <= off_r + 5'd1;
            end

            // ---- beat boundary / frame end ----
            if ((bidx_r == 3'd7) || frame_end_w) begin
              last_beat_r <= frame_end_w;
              st_r        <= C_FLUSH_S;
            end else begin
              bidx_r <= bidx_r + 3'd1;
            end
          end
        end

        C_FLUSH_S: begin
          if (m_axis_tready) begin
            bidx_r <= '0;
            beat_r <= '0;
            if (last_beat_r) begin
              tx_done_o  <= 1'b1;
              tx_count_o <= tx_count_o + 16'd1;
              gap_r      <= 4'(GAP_CYC_C - 1);
              st_r       <= C_GAP_S;
            end else begin
              st_r <= C_RUN_S;
            end
          end
        end

        C_GAP_S: begin
          gap_r <= gap_r - 4'd1;
          if (gap_r == '0) begin
            tx_fresh_o <= '0;
            tx_lv_o    <= '0;
            st_r       <= C_IDLE_S;
          end
        end

        default: st_r <= C_IDLE_S;
      endcase

      if (!enable_i && st_r == C_IDLE_S) begin
        tx_fresh_o <= '0; tx_lv_o <= '0;
      end
    end
  end

endmodule

`default_nettype wire
