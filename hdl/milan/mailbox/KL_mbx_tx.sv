/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_mbx_tx.sv
//  Project     : Milan FPGA Platform (packet mailbox, #665 lane F0)
//
//  Description : The TX merge: reads one record at a time out of the TX
//                rings, round-robin over the channels whose TX_HEAD has
//                moved past TX_TAIL, and streams its frame one byte per
//                accepted cycle with the frame's interface and channel.
//                A record is checked before a byte leaves: KIND is a TX
//                frame, LEN is 14 to the channel's max_frame_bytes, IF names
//                an elaborated interface, the reserved word is zero and the
//                whole record lies below TX_HEAD. A refused record counts in
//                TX_ERR and flushes the ring to TX_HEAD, because a record
//                whose length cannot be trusted leaves no next record to
//                find. TX_TAIL moves past a record only after its last byte
//                is taken, so the core reuses the space only once the frame
//                has left.
//
//                The one decision that matters: one record at a time, one
//                read port. A channel's frame is never interleaved with
//                another's, which is what lets the fabric's TX path treat
//                each record as one frame.
//---------------------------------------------------------------------------//

`default_nettype none

module KL_mbx_tx
  import KL_mbx_pkg::*;
(
  input  wire                         clk_i,            //! the mailbox clock
  input  wire                         rst_n,            //! synchronous active-low reset

  input  wire  [MBX_N_CH_C*16-1:0]    tx_head_words_i,  //! TX_HEAD per channel, words the core committed
  output logic [MBX_N_CH_C*16-1:0]    tx_tail_words_o,  //! TX_TAIL per channel, words consumed here
  output logic [MBX_N_CH_C*16-1:0]    tx_err_cnt_o,     //! TX_ERR per channel, saturating
  output logic                        err_p_o,          //! one-cycle pulse: TX_ERR moved

  output logic                        rd_en_o,          //! read one TX ring word
  output logic [MBX_CH_W_C-1:0]       rd_ch_o,          //! the ring's channel
  output logic [MBX_RING_AW_C-1:0]    rd_addr_o,        //! word index inside that ring
  input  wire  [31:0]                 rd_data_i,        //! the word, one cycle after rd_en_o

  output logic                        tx_valid_o,       //! a frame byte is offered
  input  wire                         tx_ready_i,       //! the byte is taken this cycle
  output logic [7:0]                  tx_data_o,        //! the byte, wire order
  output logic                        tx_last_o,        //! the byte is the frame's last
  output logic [MBX_IF_W_C-1:0]       tx_if_o,          //! interface to send on, held for the frame
  output logic [MBX_CH_W_C-1:0]       tx_ch_o           //! channel the frame came from, held for the frame
);

  typedef enum logic [2:0] {IDLE_S, W0_S, W1_S, LOAD_S, OUT_S, ERR_S, DONE_S} state_t;

  state_t                 st_r;
  logic [MBX_CH_W_C-1:0]  ch_r;        //! channel being served
  logic [MBX_CH_W_C-1:0]  last_ch_r;   //! channel served last (round-robin origin)
  logic [31:0]            w0_r;        //! header word 0 of the record
  logic [15:0]            left_r;      //! bytes still to send
  logic [8:0]             widx_r;      //! payload word being sent
  logic [31:0]            pw_r;        //! that payload word
  logic [1:0]             lane_r;      //! byte lane of pw_r on the wire
  logic [15:0]            tail_r [MBX_N_CH_C];
  logic [15:0]            err_r  [MBX_N_CH_C];

  // ---- the channel to serve next ------------------------------------------------
  logic                  pick_w;
  logic [MBX_CH_W_C-1:0] pick_ch_w;
  always_comb begin : arbiter
    pick_w    = 1'b0;
    pick_ch_w = '0;
    for (int k = 1; k <= int'(MBX_N_CH_C); k++) begin
      int unsigned c;
      c = (int'(last_ch_r) + k) % int'(MBX_N_CH_C);
      if (!pick_w && tx_head_words_i[16*c +: 16] != tail_r[c]) begin
        pick_w    = 1'b1;
        pick_ch_w = MBX_CH_W_C'(c);
      end
    end
  end : arbiter

  // ---- the served ring --------------------------------------------------------------
  logic [15:0] ring_words_w;
  logic [15:0] occ_w;
  logic [15:0] len_w;
  logic [15:0] rec_words_w;
  logic        w0_ok_w;
  always_comb begin : record_check
    ring_words_w = 16'(MBX_CH_TX_WORDS_TBL_C[ch_r]);
    occ_w        = tx_head_words_i[16*ch_r +: 16] - tail_r[ch_r];
    len_w        = 16'(w0_r >> MBX_TXREC_W0_LEN_LSB_C);
    rec_words_w  = 16'(MBX_TX_HDR_WORDS_C) + ((len_w + 16'd3) >> 2);
    w0_ok_w      = (((w0_r >> MBX_TXREC_W0_KIND_LSB_C) & ((32'd1 << MBX_TXREC_W0_KIND_WIDTH_C) - 32'd1))
                    == MBX_TX_KIND_C)
                   && (((w0_r >> MBX_TXREC_W0_IF_LSB_C) & ((32'd1 << MBX_TXREC_W0_IF_WIDTH_C) - 32'd1))
                       < MBX_N_IF_C)
                   && len_w >= 16'd14 && 32'(len_w) <= MBX_CH_MAX_FRAME_BYTES_TBL_C[ch_r]
                   && occ_w <= ring_words_w && rec_words_w <= occ_w;
  end : record_check

  // ---- reads ---------------------------------------------------------------------
  always_comb begin : ring_read
    rd_en_o   = 1'b0;
    rd_ch_o   = ch_r;
    rd_addr_o = '0;
    unique case (st_r)
      IDLE_S: begin
        rd_en_o   = pick_w;
        rd_ch_o   = pick_ch_w;
        rd_addr_o = MBX_RING_AW_C'(tail_r[pick_ch_w] & (16'(MBX_CH_TX_WORDS_TBL_C[pick_ch_w]) - 16'd1));
      end
      W0_S: begin
        rd_en_o   = 1'b1;
        rd_addr_o = MBX_RING_AW_C'((tail_r[ch_r] + 16'd1) & (ring_words_w - 16'd1));
      end
      W1_S: begin
        rd_en_o   = 1'b1;
        rd_addr_o = MBX_RING_AW_C'((tail_r[ch_r] + 16'(MBX_TX_HDR_WORDS_C)) & (ring_words_w - 16'd1));
      end
      OUT_S: begin
        rd_en_o   = tx_ready_i && lane_r == 2'd3 && left_r > 16'd1;
        rd_addr_o = MBX_RING_AW_C'((tail_r[ch_r] + 16'(MBX_TX_HDR_WORDS_C) + 16'(widx_r) + 16'd1)
                                   & (ring_words_w - 16'd1));
      end
      default: ;
    endcase
  end : ring_read

  assign tx_valid_o = (st_r == OUT_S);
  assign tx_data_o  = pw_r[8*lane_r +: 8];
  assign tx_last_o  = (st_r == OUT_S) && (left_r == 16'd1);
  assign tx_ch_o    = ch_r;
  assign tx_if_o    = MBX_IF_W_C'(w0_r >> MBX_TXREC_W0_IF_LSB_C);
  assign err_p_o    = (st_r == ERR_S);

  always_ff @(posedge clk_i) begin : fsm
    if (!rst_n) begin
      st_r      <= IDLE_S;
      ch_r      <= '0;
      last_ch_r <= MBX_CH_W_C'(MBX_N_CH_C - 1);
      w0_r      <= '0;
      left_r    <= '0;
      widx_r    <= '0;
      pw_r      <= '0;
      lane_r    <= '0;
      for (int c = 0; c < int'(MBX_N_CH_C); c++) begin
        tail_r[c] <= '0;
        err_r[c]  <= '0;
      end
    end else begin
      unique case (st_r)
        IDLE_S: if (pick_w) begin
          ch_r <= pick_ch_w;
          st_r <= W0_S;
        end
        W0_S: begin
          w0_r <= rd_data_i;
          st_r <= W1_S;
        end
        W1_S: begin
          // the reserved word must be zero and word 0 must hold
          if (w0_ok_w && rd_data_i == 32'd0) begin
            left_r <= len_w;
            widx_r <= '0;
            st_r   <= LOAD_S;
          end else begin
            st_r <= ERR_S;
          end
        end
        LOAD_S: begin
          pw_r   <= rd_data_i;
          lane_r <= '0;
          st_r   <= OUT_S;
        end
        OUT_S: if (tx_ready_i) begin
          left_r <= left_r - 16'd1;
          lane_r <= lane_r + 2'd1;
          if (left_r == 16'd1) begin
            st_r <= DONE_S;
          end else if (lane_r == 2'd3) begin
            widx_r <= widx_r + 9'd1;
            st_r   <= LOAD_S;
          end
        end
        ERR_S: begin
          tail_r[ch_r] <= tx_head_words_i[16*ch_r +: 16];
          if (err_r[ch_r] != 16'hFFFF) err_r[ch_r] <= err_r[ch_r] + 16'd1;
          last_ch_r <= ch_r;
          st_r      <= IDLE_S;
        end
        DONE_S: begin
          tail_r[ch_r] <= tail_r[ch_r] + rec_words_w;
          last_ch_r    <= ch_r;
          st_r         <= IDLE_S;
        end
        default: st_r <= IDLE_S;
      endcase
    end
  end : fsm

  always_comb begin : publish
    for (int c = 0; c < int'(MBX_N_CH_C); c++) begin
      tx_tail_words_o[16*c +: 16] = tail_r[c];
      tx_err_cnt_o[16*c +: 16]    = err_r[c];
    end
  end : publish

endmodule : KL_mbx_tx

`default_nettype wire
