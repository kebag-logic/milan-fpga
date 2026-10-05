/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_mbx_tx.sv
//  Project     : Milan FPGA Platform (packet mailbox, #665 lane F0)
//
//  Description : The TX merge: reads one record at a time out of the TX
//                rings and streams its frame one byte per accepted cycle
//                with the frame's interface and channel. Records leave in
//                commit order across the channels: before each record a
//                scan reads word 1 of the oldest record of every channel
//                whose TX_HEAD has moved past TX_TAIL and keeps the one
//                whose SEQ comes first modulo 2^16. The scan starts after
//                the channel served last and keeps the first of equal SEQs,
//                so equal SEQs leave round-robin. A record is checked before
//                a byte leaves: KIND is a TX frame, LEN is 14 to the
//                channel's max_frame_bytes, IF names an elaborated
//                interface, word 1's reserved bits are zero and the whole
//                record lies below TX_HEAD. A refused record counts in
//                TX_ERR and flushes the ring to TX_HEAD, because a record
//                whose length cannot be trusted leaves no next record to
//                find. TX_TAIL moves past a record only after its last byte
//                is taken, so the core reuses the space only once the frame
//                has left.
//
//                The one decision that matters: one record at a time, one
//                read port, in commit order. A channel's frame is never
//                interleaved with another's, and a record committed after
//                another never leaves before it, so an ACMP response leaves
//                before the AECP notification committed after it, whichever
//                channel the merge served last.
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

  output logic                        rd_en_o,          //! read one transmit ring word
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

  typedef enum logic [3:0] {IDLE_S, SCAN_S, PICK_S, W0_S, W1_S, LOAD_S, OUT_S, ERR_S, DONE_S} state_t;

  localparam int unsigned KW_C = $clog2(MBX_N_CH_C + 2);   //! scan step 1 .. N_CH + 1

  state_t                 st_r;
  logic [MBX_CH_W_C-1:0]  ch_r;        //! channel being served
  logic [MBX_CH_W_C-1:0]  last_ch_r;   //! channel served last (the scan's origin)
  logic [KW_C-1:0]        scan_k_r;    //! scan step: channel last_ch_r + k is read
  logic                   scan_v_r;    //! the previous step read a word 1
  logic [MBX_CH_W_C-1:0]  scan_c_r;    //! the channel it read
  logic                   best_v_r;    //! a candidate is held
  logic [MBX_CH_W_C-1:0]  best_ch_r;   //! the candidate's channel
  logic [15:0]            best_seq_r;  //! the candidate's SEQ
  logic [31:0]            w0_r;        //! header word 0 of the record
  logic [15:0]            left_r;      //! bytes still to send
  logic [8:0]             widx_r;      //! payload word being sent
  logic [31:0]            pw_r;        //! that payload word
  logic [1:0]             lane_r;      //! byte lane of pw_r on the wire
  logic [15:0]            tail_r [MBX_N_CH_C];
  logic [15:0]            err_r  [MBX_N_CH_C];

  // ---- the channel to serve next: the earliest SEQ ----------------------------------
  logic [MBX_N_CH_C-1:0] pend_w;     //! the channel holds a committed record
  logic                  scan_rd_w;  //! this scan step reads a word 1
  logic [MBX_CH_W_C-1:0] scan_ch_w;  //! the channel this scan step reads
  logic [15:0]           seq_w;      //! the SEQ the previous step read
  logic [15:0]           dseq_w;     //! seq_w - best_seq_r, modulo 2^16
  logic                  before_w;   //! seq_w comes before the held candidate's
  always_comb begin : arbiter
    int unsigned sum;
    for (int c = 0; c < int'(MBX_N_CH_C); c++) begin
      pend_w[c] = tx_head_words_i[16*c +: 16] != tail_r[c];
    end
    sum       = int'(last_ch_r) + int'(scan_k_r);
    scan_ch_w = MBX_CH_W_C'(sum >= int'(MBX_N_CH_C) ? sum - int'(MBX_N_CH_C) : sum);
    scan_rd_w = (st_r == SCAN_S) && int'(scan_k_r) <= int'(MBX_N_CH_C) && pend_w[scan_ch_w];
    seq_w     = 16'(rd_data_i >> MBX_TXREC_W1_SEQ_LSB_C);
    dseq_w    = seq_w - best_seq_r;
    before_w  = !best_v_r || dseq_w[15];
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
      SCAN_S: begin
        rd_en_o   = scan_rd_w;
        rd_ch_o   = scan_ch_w;
        rd_addr_o = MBX_RING_AW_C'((tail_r[scan_ch_w] + 16'd1) & (16'(MBX_CH_TX_WORDS_TBL_C[scan_ch_w]) - 16'd1));
      end
      PICK_S: begin
        rd_en_o   = best_v_r && pend_w[best_ch_r];
        rd_ch_o   = best_ch_r;
        rd_addr_o = MBX_RING_AW_C'(tail_r[best_ch_r] & (16'(MBX_CH_TX_WORDS_TBL_C[best_ch_r]) - 16'd1));
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
      st_r       <= IDLE_S;
      ch_r       <= '0;
      last_ch_r  <= MBX_CH_W_C'(MBX_N_CH_C - 1);
      scan_k_r   <= '0;
      scan_v_r   <= 1'b0;
      scan_c_r   <= '0;
      best_v_r   <= 1'b0;
      best_ch_r  <= '0;
      best_seq_r <= '0;
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
        IDLE_S: if (|pend_w) begin
          scan_k_r <= KW_C'(1);
          scan_v_r <= 1'b0;
          best_v_r <= 1'b0;
          st_r     <= SCAN_S;
        end
        SCAN_S: begin
          // step k reads channel last_ch_r + k; step k + 1 compares what it read
          if (scan_v_r && before_w) begin
            best_v_r   <= 1'b1;
            best_ch_r  <= scan_c_r;
            best_seq_r <= seq_w;
          end
          scan_v_r <= scan_rd_w;
          scan_c_r <= scan_ch_w;
          scan_k_r <= scan_k_r + KW_C'(1);
          if (int'(scan_k_r) == int'(MBX_N_CH_C) + 1) st_r <= PICK_S;
        end
        PICK_S: if (best_v_r && pend_w[best_ch_r]) begin
          ch_r <= best_ch_r;
          st_r <= W0_S;
        end else begin
          st_r <= IDLE_S;
        end
        W0_S: begin
          w0_r <= rd_data_i;
          st_r <= W1_S;
        end
        W1_S: begin
          // word 1's reserved bits must be zero and word 0 must hold
          if (w0_ok_w && (rd_data_i >> MBX_TXREC_W1_RSVD_LSB_C) == 32'd0) begin
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
