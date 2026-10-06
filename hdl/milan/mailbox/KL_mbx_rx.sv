/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_mbx_rx.sv
//  Project     : Milan FPGA Platform (packet mailbox, #665 lanes F0 and FC)
//
//  Description : The ingress filter and the receive ring writer. A frame arrives
//                one byte per accepted cycle. When its byte 15 arrives (or its
//                last byte, if it ends at byte 14) its full tuple picks at most
//                one channel: the destination MAC (wire bytes 0 to 5) against
//                each match tuple's address, or, for an `own` tuple, against
//                OWN_MAC of the interface the frame arrived on; the EtherType
//                (bytes 12 and 13); the AVTP subtype (byte 14) where the tuple
//                names one; and the message_type (the low nibble of byte 15, 0
//                when the frame ends at byte 14) where the tuple names some, as
//                the MAAP DEFEND to own unicast does. Every channel's
//                accept terms (the identity term: an 8-byte compare against
//                OWN_EID or zero, or a MAAP range captured for the overlap
//                test) are evaluated as the bytes pass, and the frame's words
//                are written into the picked channel's receive ring
//                speculatively, past the ring's head. At the last byte the
//                verdict is taken: a frame for no open channel, or one no
//                accept term passes, is dropped silently (it is not addressed
//                to this entity), except that a frame whose EtherType is a
//                control one (some tuple names it) and which matched no tuple
//                counts once in FILTER_MISMATCH; one that did not fit
//                max_frame_bytes or the free ring space counts in RX_DROP; one
//                the channel's token bucket refuses counts in RATE_DROP. A
//                passing frame gets its two header words written and only then
//                is the head advanced past the whole record, so the core never
//                reads a partial record. The bytes and rules are the
//                contract's (sw/mailbox/mailbox.yaml, KL_mbx_pkg).
//
//                Tagged frames, by construction: an 802.1Q tag puts its TPID
//                at bytes 12 and 13, which the contract lets no tuple name, so
//                a tagged frame matches no tuple and is of no control
//                EtherType: it reaches no channel and no counter.
//
//                The decision at byte 15 needs no drain first: bytes 0 to 15
//                are words 0 to 3, which the four-word queue holds.
//
//                The one decision that matters: a speculative word is
//                written only into space the core has released (the word
//                index stays below the free space minus the two header
//                words), so a frame that is later dropped never overwrites
//                a record the core has not read. A frame that would need
//                more space than was free while it arrived is dropped, even
//                if the core frees space before its last byte.
//---------------------------------------------------------------------------//

`default_nettype none

module KL_mbx_rx
  import KL_mbx_pkg::*;
(
  input  wire                               clk_i,            //! the mailbox clock
  input  wire                               rst_n,            //! synchronous active-low reset
  input  wire                               ms_tick_p_i,      //! one-cycle pulse per elapsed millisecond (token refill)
  input  wire  [31:0]                       now_ms_i,         //! NOW_MS, stamped into ARRIVAL_MS

  input  wire  [63:0]                       own_eid_i,        //! OWN_EID, the eq_own operand
  input  wire  [MBX_N_IF_C*48-1:0]          own_mac_i,        //! OWN_MAC per interface, an `own` tuple's destination
  input  wire  [MBX_N_CH_C-1:0]             open_i,           //! FILTER_EN.OPEN, bit c opens channel c
  input  wire  [47:0]                       maap_base_i,      //! MAAP_BASE, first address of this entity's range
  input  wire  [15:0]                       maap_count_i,     //! MAAP_COUNT, addresses in the range (0 = none)

  input  wire                               rx_valid_i,       //! a frame byte is offered
  output logic                              rx_ready_o,       //! the byte is taken this cycle
  input  wire  [7:0]                        rx_data_i,        //! the byte, wire order
  input  wire                               rx_last_i,        //! the byte is the frame's last (FCS already stripped)
  input  wire  [MBX_IF_W_C-1:0]             rx_if_i,          //! interface the frame arrived on, held for the frame

  output logic                              wr_en_o,          //! write one receive ring word
  output logic [MBX_CH_W_C-1:0]             wr_ch_o,          //! the ring's channel
  output logic [MBX_RING_AW_C-1:0]          wr_addr_o,        //! word index inside that ring
  output logic [31:0]                       wr_data_o,        //! the word

  input  wire  [MBX_N_CH_C*16-1:0]          rx_tail_words_i,  //! RX_TAIL per channel, words consumed by the core
  output logic [MBX_N_CH_C*16-1:0]          rx_head_words_o,  //! RX_HEAD per channel, words committed here
  output logic [MBX_N_CH_C*16-1:0]          rx_drop_cnt_o,    //! RX_DROP per channel, saturating
  output logic [MBX_N_CH_C*16-1:0]          rate_drop_cnt_o,  //! RATE_DROP per channel, saturating
  output logic [MBX_N_CH_C*16-1:0]          rx_pass_cnt_o,    //! RX_PASS per channel, modulo 2^16
  output logic [15:0]                       mismatch_cnt_o,   //! FILTER_MISMATCH, saturating
  output logic                              err_p_o           //! one-cycle pulse: RX_DROP, RATE_DROP or FILTER_MISMATCH moved
);

  localparam int unsigned NT_C = MBX_N_CH_C * MBX_MAX_TERMS_C;   //! accept terms, flattened
  localparam int unsigned NM_C = MBX_N_CH_C * MBX_MAX_TUPLES_C;  //! match tuples, flattened
  localparam int unsigned QD_C = 4;                              //! word queue depth
  localparam int unsigned TW_C = $clog2(NT_C);                   //! term index width

  typedef enum logic [1:0] {RECV_S, FIN_S, HDR0_S, HDR1_S} state_t;

  state_t                  st_r;
  logic [10:0]             cnt_r;          //! bytes of the frame taken so far (its length at FIN)
  logic [31:0]             wacc_r;         //! the word being assembled
  logic [1:0]              lane_r;         //! next byte lane of wacc_r
  logic [8:0]              widx_r;         //! payload words formed so far
  logic [47:0]             dst_r;          //! destination MAC, shifted in big-endian
  logic [7:0]              b12_r;          //! EtherType high byte
  logic [7:0]              b13_r;          //! EtherType low byte
  logic [7:0]              sub_r;          //! AVTP subtype, wire byte 14
  logic                    cls_done_r;     //! the channel decision is taken
  logic                    hit_r;          //! the frame classified into an open channel
  logic                    mis_r;          //! a control EtherType that matched no tuple
  logic [15:0]             mismatch_r;     //! FILTER_MISMATCH
  logic [MBX_CH_W_C-1:0]   ch_r;           //! that channel
  logic [3:0]              msg_r;          //! message_type, the low nibble of wire byte 15
  logic [MBX_IF_W_C-1:0]   if_r;           //! interface of the frame
  logic [31:0]             arrival_ms_r;   //! NOW_MS at the last byte
  logic                    overflow_r;     //! a word did not fit the free ring space
  logic                    oversize_r;     //! a word lay past max_frame_bytes
  logic [NT_C-1:0]         eqown_r;        //! term field equals OWN_EID so far
  logic [NT_C-1:0]         eqzero_r;       //! term field is zero so far
  logic [63:0]             field_r [NT_C]; //! term field bytes, shifted in big-endian

  logic [31:0]             q_data_r [QD_C];
  logic [8:0]              q_idx_r  [QD_C];
  logic [1:0]              q_rd_r;
  logic [1:0]              q_wr_r;
  logic [2:0]              q_cnt_r;

  logic [15:0]             head_r      [MBX_N_CH_C];
  logic [15:0]             drop_r      [MBX_N_CH_C];
  logic [15:0]             rate_drop_r [MBX_N_CH_C];
  logic [15:0]             pass_r      [MBX_N_CH_C];
  logic [7:0]              tokens_r    [MBX_N_CH_C];
  logic [15:0]             refill_r    [MBX_N_CH_C];

  // ---- the byte taken this cycle -------------------------------------------
  logic take_w;
  assign rx_ready_o = (st_r == RECV_S) && (q_cnt_r < 3'(QD_C));
  assign take_w     = rx_valid_i && rx_ready_o;

  // ---- the own MAC of the interface the frame arrived on ---------------------
  // An index this build has no interface for has no own MAC: no `own` tuple holds.
  logic [47:0] own_mac_w;
  logic        own_if_w;
  always_comb begin : own_mac
    own_mac_w = '0;
    own_if_w  = 1'b0;
    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
      if (int'(if_r) == i) begin
        own_mac_w = own_mac_i[48*i +: 48];
        own_if_w  = 1'b1;
      end
    end
  end : own_mac

  // ---- classification at byte 15, or at the last byte of a frame ending at 14 --
  logic                  cls_at_w;    //! the byte taken now decides the channel
  logic                  cls_hit_w;   //! a channel's tuple holds
  logic [MBX_CH_W_C-1:0] cls_ch_w;    //! that channel
  logic                  ctrl_et_w;   //! the EtherType is one some tuple names
  assign cls_at_w = (cnt_r == 11'(MBX_MSG_TYPE_BYTE_C)) || (rx_last_i && cnt_r == 11'(MBX_SUBTYPE_BYTE_C));
  always_comb begin : classify
    logic [15:0] ethertype;
    logic [7:0]  subtype;
    logic [3:0]  msg;
    ethertype = {b12_r, b13_r};
    subtype   = (cnt_r == 11'(MBX_SUBTYPE_BYTE_C)) ? rx_data_i : sub_r;
    msg       = (cnt_r == 11'(MBX_MSG_TYPE_BYTE_C)) ? rx_data_i[3:0] : 4'd0;
    cls_hit_w = 1'b0;
    cls_ch_w  = '0;
    ctrl_et_w = 1'b0;
    for (int j = 0; j < int'(NM_C); j++) begin
      logic dst_ok;
      dst_ok = (MBX_TUPLE_DST_TBL_C[j] == MBX_DST_MAC_C
                && dst_r == {16'(MBX_TUPLE_DST_HI_TBL_C[j]), MBX_TUPLE_DST_LO_TBL_C[j]})
               || (MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && own_if_w && dst_r == own_mac_w);
      if (MBX_TUPLE_DST_TBL_C[j] != MBX_DST_NONE_C && ethertype == 16'(MBX_TUPLE_ETHERTYPE_TBL_C[j]))
        ctrl_et_w = 1'b1;
      if (!cls_hit_w && dst_ok && ethertype == 16'(MBX_TUPLE_ETHERTYPE_TBL_C[j])
          && (MBX_TUPLE_HAS_SUBTYPE_TBL_C[j] == 0 || subtype == 8'(MBX_TUPLE_SUBTYPE_TBL_C[j]))
          && MBX_TUPLE_MSG_MASK_TBL_C[j][{1'b0, msg}]) begin
        cls_hit_w = 1'b1;
        cls_ch_w  = MBX_CH_W_C'(j / int'(MBX_MAX_TUPLES_C));
      end
    end
  end : classify

  // ---- free space and limits of the picked channel ---------------------------
  logic [15:0] ring_words_w;
  logic [15:0] used_w;
  logic [15:0] free_w;
  logic [9:0]  max_words_w;
  logic [15:0] tail_w;
  always_comb begin : space
    ring_words_w = 16'(MBX_CH_RX_WORDS_TBL_C[ch_r]);
    tail_w       = rx_tail_words_i[16*ch_r +: 16];
    used_w       = head_r[ch_r] - tail_w;
    free_w       = (used_w > ring_words_w) ? 16'd0 : ring_words_w - used_w;
    max_words_w  = 10'((MBX_CH_MAX_FRAME_BYTES_TBL_C[ch_r] + 3) / 4);
  end : space

  // ---- the verdict at FIN ------------------------------------------------------
  logic rule_pass_w;
  always_comb begin : verdict
    rule_pass_w = 1'b0;
    for (int t = 0; t < int'(MBX_MAX_TERMS_C); t++) begin
      logic [TW_C-1:0] j;
      logic        field_ok;
      logic        overlap;
      logic [48:0] own_end;
      logic [48:0] req_end;
      j        = TW_C'(int'(ch_r) * int'(MBX_MAX_TERMS_C) + t);
      field_ok = 32'(cnt_r) >= MBX_TERM_OFFSET_TBL_C[j] + MBX_TERM_FIELD_BYTES_C;
      own_end  = {1'b0, maap_base_i} + 49'(maap_count_i) - 49'd1;
      req_end  = {1'b0, field_r[j][63:16]} + 49'(field_r[j][15:0]) - 49'd1;
      overlap  = (field_r[j][15:0] != 16'd0) && (maap_count_i != 16'd0)
                 && ({1'b0, field_r[j][63:16]} <= own_end) && ({1'b0, maap_base_i} <= req_end);
      if (MBX_TERM_MASK_TBL_C[j][{1'b0, msg_r}]) begin
        unique case (MBX_TERM_TEST_TBL_C[j])
          MBX_TEST_ANY_C:           rule_pass_w = 1'b1;
          MBX_TEST_EQ_OWN_C:        if (field_ok && eqown_r[j]) rule_pass_w = 1'b1;
          MBX_TEST_EQ_ZERO_C:       if (field_ok && eqzero_r[j]) rule_pass_w = 1'b1;
          MBX_TEST_RANGE_OVERLAP_C: if (field_ok && overlap) rule_pass_w = 1'b1;
          default: ;
        endcase
      end
    end
  end : verdict

  // ---- queue drain: one speculative word per cycle once the channel is known ---
  logic        drain_w;
  logic        drain_fits_w;
  logic [15:0] drain_slot_w;
  assign drain_w      = cls_done_r && (q_cnt_r != 3'd0) && (st_r == RECV_S || st_r == FIN_S);
  assign drain_fits_w = (32'(q_idx_r[q_rd_r]) + 32'd2 < 32'(free_w))
                        && (10'(q_idx_r[q_rd_r]) < max_words_w);
  assign drain_slot_w = head_r[ch_r] + 16'd2 + 16'(q_idx_r[q_rd_r]);

  // ---- the ring write port -----------------------------------------------------
  always_comb begin : ring_write
    wr_en_o   = 1'b0;
    wr_ch_o   = ch_r;
    wr_addr_o = '0;
    wr_data_o = '0;
    if (drain_w && hit_r && !overflow_r && !oversize_r && drain_fits_w) begin
      wr_en_o   = 1'b1;
      wr_addr_o = MBX_RING_AW_C'(drain_slot_w & (ring_words_w - 16'd1));
      wr_data_o = q_data_r[q_rd_r];
    end else if (st_r == HDR0_S) begin
      wr_en_o   = 1'b1;
      wr_addr_o = MBX_RING_AW_C'(head_r[ch_r] & (ring_words_w - 16'd1));
      wr_data_o = (32'(cnt_r) << MBX_RXREC_W0_LEN_LSB_C)
                | (32'(if_r) << MBX_RXREC_W0_IF_LSB_C)
                | (32'(MBX_RX_KIND_C) << MBX_RXREC_W0_KIND_LSB_C);
    end else if (st_r == HDR1_S) begin
      wr_en_o   = 1'b1;
      wr_addr_o = MBX_RING_AW_C'((head_r[ch_r] + 16'd1) & (ring_words_w - 16'd1));
      wr_data_o = arrival_ms_r << MBX_RXREC_W1_ARRIVAL_MS_LSB_C;
    end
  end : ring_write

  // ---- the frame: bytes, words, terms, FSM ---------------------------------------
  logic fin_ready_w;    //! FIN with the queue drained: the verdict can be taken
  logic bad_w;          //! the frame did not fit max_frame_bytes or the free space
  logic accept_w;       //! the frame is committed: header writes follow
  logic commit_w;       //! the record's header is written this cycle (HDR1)
  logic drop_w;         //! RX_DROP moves this cycle
  logic rate_w;         //! RATE_DROP moves this cycle
  logic mis_w;          //! FILTER_MISMATCH moves this cycle
  assign fin_ready_w = (st_r == FIN_S) && (q_cnt_r == 3'd0) && cls_done_r;
  assign bad_w       = overflow_r || oversize_r || (32'(cnt_r) > MBX_CH_MAX_FRAME_BYTES_TBL_C[ch_r]);
  assign drop_w      = fin_ready_w && hit_r && rule_pass_w && bad_w;
  assign rate_w      = fin_ready_w && hit_r && rule_pass_w && !bad_w && (tokens_r[ch_r] == 8'd0);
  assign accept_w    = fin_ready_w && hit_r && rule_pass_w && !bad_w && (tokens_r[ch_r] != 8'd0);
  assign mis_w       = fin_ready_w && mis_r;
  assign commit_w    = (st_r == HDR1_S);
  assign err_p_o     = drop_w || rate_w || mis_w;

  // the word the taken byte completes or extends
  logic [31:0] word_w;
  assign word_w = wacc_r | (32'(rx_data_i) << (5'd8 * 5'(lane_r)));

  always_ff @(posedge clk_i) begin : frame_fsm
    if (!rst_n) begin
      st_r         <= RECV_S;
      cnt_r        <= '0;
      wacc_r       <= '0;
      lane_r       <= '0;
      widx_r       <= '0;
      dst_r        <= '0;
      b12_r        <= '0;
      b13_r        <= '0;
      sub_r        <= '0;
      cls_done_r   <= 1'b0;
      hit_r        <= 1'b0;
      mis_r        <= 1'b0;
      ch_r         <= '0;
      msg_r        <= '0;
      if_r         <= '0;
      arrival_ms_r <= '0;
      overflow_r   <= 1'b0;
      oversize_r   <= 1'b0;
      eqown_r      <= '1;
      eqzero_r     <= '1;
      q_rd_r       <= '0;
      q_wr_r       <= '0;
      q_cnt_r      <= '0;
      for (int j = 0; j < int'(NT_C); j++) field_r[j] <= '0;
      for (int k = 0; k < int'(QD_C); k++) begin
        q_data_r[k] <= '0;
        q_idx_r[k]  <= '0;
      end
    end else begin
      // the queue: one push per formed word, one pop per drained word
      if (drain_w) begin
        q_rd_r <= q_rd_r + 2'd1;
        if (hit_r && !drain_fits_w) begin
          if (10'(q_idx_r[q_rd_r]) >= max_words_w) oversize_r <= 1'b1;
          else overflow_r <= 1'b1;
        end
      end
      if (take_w) begin
        if (cnt_r == 11'd0) if_r <= rx_if_i;
        if (cnt_r != 11'h7FF) cnt_r <= cnt_r + 11'd1;
        // the six destination bytes from DST_BYTE (the subtraction wraps below it)
        if (32'(cnt_r) - MBX_DST_BYTE_C < 32'd6)    dst_r <= {dst_r[39:0], rx_data_i};
        if (cnt_r == 11'(MBX_ETHERTYPE_BYTE_C))     b12_r <= rx_data_i;
        if (cnt_r == 11'(MBX_ETHERTYPE_BYTE_C + 1)) b13_r <= rx_data_i;
        if (cnt_r == 11'(MBX_SUBTYPE_BYTE_C))       sub_r <= rx_data_i;
        if (cnt_r == 11'(MBX_MSG_TYPE_BYTE_C))      msg_r <= rx_data_i[3:0];
        if (cls_at_w) begin
          cls_done_r <= 1'b1;
          hit_r      <= cls_hit_w && open_i[cls_ch_w];
          ch_r       <= cls_ch_w;
          mis_r      <= ctrl_et_w && !cls_hit_w;
        end
        for (int j = 0; j < int'(NT_C); j++) begin
          if (32'(cnt_r) >= MBX_TERM_OFFSET_TBL_C[j]
              && 32'(cnt_r) < MBX_TERM_OFFSET_TBL_C[j] + MBX_TERM_FIELD_BYTES_C) begin
            if (rx_data_i != own_eid_i[8 * (7 - (32'(cnt_r) - MBX_TERM_OFFSET_TBL_C[j])) +: 8])
              eqown_r[j] <= 1'b0;
            if (rx_data_i != 8'd0) eqzero_r[j] <= 1'b0;
            field_r[j] <= {field_r[j][55:0], rx_data_i};
          end
        end
        if (lane_r == 2'd3 || rx_last_i) begin
          q_data_r[q_wr_r] <= word_w;
          q_idx_r[q_wr_r]  <= widx_r;
          q_wr_r           <= q_wr_r + 2'd1;
          widx_r           <= widx_r + 9'd1;
          wacc_r           <= '0;
          lane_r           <= '0;
        end else begin
          wacc_r <= word_w;
          lane_r <= lane_r + 2'd1;
        end
        if (rx_last_i) begin
          st_r         <= FIN_S;
          arrival_ms_r <= now_ms_i;
          // a frame shorter than the subtype byte classifies into nothing
          if (cnt_r < 11'(MBX_SUBTYPE_BYTE_C)) begin
            cls_done_r <= 1'b1;
            hit_r      <= 1'b0;
          end
        end
      end
      q_cnt_r <= q_cnt_r + 3'(take_w && (lane_r == 2'd3 || rx_last_i)) - 3'(drain_w);
      if (fin_ready_w) st_r <= accept_w ? HDR0_S : RECV_S;
      if (st_r == HDR0_S) st_r <= HDR1_S;
      if (st_r == HDR1_S) st_r <= RECV_S;
      // a new frame starts clean
      if ((fin_ready_w && !accept_w) || st_r == HDR1_S) begin
        cnt_r      <= '0;
        wacc_r     <= '0;
        lane_r     <= '0;
        widx_r     <= '0;
        cls_done_r <= 1'b0;
        hit_r      <= 1'b0;
        mis_r      <= 1'b0;
        msg_r      <= '0;
        overflow_r <= 1'b0;
        oversize_r <= 1'b0;
        eqown_r    <= '1;
        eqzero_r   <= '1;
        for (int j = 0; j < int'(NT_C); j++) field_r[j] <= '0;
      end
    end
  end : frame_fsm

  // ---- per-channel heads, counters and token buckets -------------------------------
  logic [7:0]  tokens_nx_w [MBX_N_CH_C];   //! the bucket after this cycle's refill and commit
  logic        refill_w    [MBX_N_CH_C];   //! this tick completes a refill period
  always_comb begin : buckets
    for (int c = 0; c < int'(MBX_N_CH_C); c++) begin
      logic [8:0] tokens;
      refill_w[c] = ms_tick_p_i && (32'(refill_r[c]) + 32'd1 >= MBX_CH_RATE_REFILL_MS_TBL_C[c]);
      tokens = {1'b0, tokens_r[c]};
      if (refill_w[c] && tokens < 9'(MBX_CH_RATE_BURST_TBL_C[c])) tokens = tokens + 9'd1;
      if (commit_w && ch_r == MBX_CH_W_C'(c)) tokens = tokens - 9'd1;
      tokens_nx_w[c] = tokens[7:0];
    end
  end : buckets

  always_ff @(posedge clk_i) begin : channel_state
    if (!rst_n) begin
      mismatch_r <= '0;
      for (int c = 0; c < int'(MBX_N_CH_C); c++) begin
        head_r[c]      <= '0;
        drop_r[c]      <= '0;
        rate_drop_r[c] <= '0;
        pass_r[c]      <= '0;
        tokens_r[c]    <= 8'(MBX_CH_RATE_BURST_TBL_C[c]);
        refill_r[c]    <= '0;
      end
    end else begin
      if (mis_w && mismatch_r != 16'hFFFF) mismatch_r <= mismatch_r + 16'd1;
      for (int c = 0; c < int'(MBX_N_CH_C); c++) begin
        if (refill_w[c]) refill_r[c] <= '0;
        else if (ms_tick_p_i) refill_r[c] <= refill_r[c] + 16'd1;
        if (commit_w && ch_r == MBX_CH_W_C'(c)) begin
          head_r[c] <= head_r[c] + 16'd2 + 16'(widx_r);
          pass_r[c] <= pass_r[c] + 16'd1;
        end
        tokens_r[c] <= tokens_nx_w[c];
        if (drop_w && ch_r == MBX_CH_W_C'(c) && drop_r[c] != 16'hFFFF) drop_r[c] <= drop_r[c] + 16'd1;
        if (rate_w && ch_r == MBX_CH_W_C'(c) && rate_drop_r[c] != 16'hFFFF)
          rate_drop_r[c] <= rate_drop_r[c] + 16'd1;
      end
    end
  end : channel_state

  always_comb begin : publish
    for (int c = 0; c < int'(MBX_N_CH_C); c++) begin
      rx_head_words_o[16*c +: 16] = head_r[c];
      rx_drop_cnt_o[16*c +: 16]   = drop_r[c];
      rate_drop_cnt_o[16*c +: 16] = rate_drop_r[c];
      rx_pass_cnt_o[16*c +: 16]   = pass_r[c];
    end
    mismatch_cnt_o = mismatch_r;
  end : publish

endmodule : KL_mbx_rx

`default_nettype wire
