/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_mbx_evt.sv
//  Project     : Milan FPGA Platform (packet mailbox, #665 lane F0)
//
//  Description : The fabric timers and the event poster. The core arms a
//                timer slot with an absolute NOW_MS deadline and a tag of
//                its own (TMR_CMD); a scanner visits one slot per cycle and
//                marks an armed slot whose deadline has passed as expired.
//                The poster writes four-word records into the event ring:
//                a link level change, a grandmaster change the gPTP plane
//                published, each expired timer with the tag of the arm it
//                belongs to, and, while TICK_CTL.EN is set, the centisecond
//                tick count the firmware's timer port (lwSRP's
//                shlan_timer_tick) is driven by. Since contract 2.3 (#665,
//                ruling 6410169666) it also posts the datapath's face events:
//                a live audio-map write, an AVB_INFO or AS_PATH change, each
//                with the count since its last record, and a served
//                descriptor's counter change, one pending bit per descriptor
//                (Milan v1.2 Table 5.22). Fixed priority: link, then
//                grandmaster, then the lowest expired slot, then the tick,
//                then the map write, AVB_INFO, AS_PATH, and last the lowest
//                pending descriptor of the lowest interface.
//
//                The one decision that matters: every source is COALESCED.
//                A source holds at most one unposted record and posts its
//                state at posting time, and the poster writes only when four
//                words are free. So the ring can never overflow and drop the
//                last state of anything (an EVT_TAIL more than the ring
//                behind EVT_HEAD, or ahead of it, which only a wrong host
//                counter writes, leaves no free word: nothing posts until
//                the tail is back in range, as on the receive rings): a link that flaps twice before its
//                record is posted posts its current level once, and a timer
//                re-armed before its expiry was posted posts nothing for the
//                old arm, and ticks counted while their record waits are
//                posted as one record carrying the count. An expiry already
//                in the ring when its slot is re-armed or cancelled stays
//                there with its old tag, and the core discards it by that
//                tag. A descriptor whose counters move again before its
//                record is posted posts once, and one posted in the current
//                holdoff epoch of NOW_MS (CTRCHG_HOLDOFF_MS, the Table 5.22
//                second) waits pending for the next, so counters that move
//                with every frame cost one record per descriptor per epoch.
//---------------------------------------------------------------------------//

`default_nettype none

module KL_mbx_evt
  import KL_mbx_pkg::*;
(
  input  wire                           clk_i,              //! the mailbox clock
  input  wire                           rst_n,              //! synchronous active-low reset
  input  wire                           ms_tick_p_i,        //! one-cycle pulse per elapsed millisecond (NOW_MS)
  input  wire  [31:0]                   now_ms_i,           //! NOW_MS
  input  wire                           tick_en_i,          //! TICK_CTL.EN: count and post centisecond ticks

  input  wire                           tmr_cmd_p_i,        //! one-cycle pulse: TMR_CMD was written
  input  wire  [7:0]                    tmr_slot_i,         //! TMR_CMD.SLOT
  input  wire  [15:0]                   tmr_tag_i,          //! TMR_CMD.TAG
  input  wire  [1:0]                    tmr_op_i,           //! TMR_CMD.OP
  input  wire  [31:0]                   tmr_deadline_ms_i,  //! TMR_DEADLINE, the arm's absolute deadline
  output logic                          tmr_bad_p_o,        //! one-cycle pulse: the command named no slot or no op

  input  wire  [MBX_N_IF_C-1:0]         link_up_i,          //! link level per interface
  input  wire  [MBX_N_IF_C-1:0]         gm_change_p_i,      //! one-cycle pulse per interface: a grandmaster change
  input  wire  [MBX_N_IF_C*64-1:0]      gm_id_i,            //! gptp_grandmaster_id per interface
  input  wire  [MBX_N_IF_C*8-1:0]       gptp_domain_i,      //! gptp_domain_number per interface

  input  wire  [MBX_N_IF_C-1:0]         ctr_chg_p_i,        //! one-cycle pulse per interface: a served descriptor's counters moved
  input  wire  [MBX_N_IF_C*16-1:0]      ctr_chg_type_i,     //! its descriptor_type, valid with ctr_chg_p_i
  input  wire  [MBX_N_IF_C*16-1:0]      ctr_chg_index_i,    //! its descriptor_index, valid with ctr_chg_p_i
  input  wire  [MBX_N_IF_C-1:0]         avb_chg_p_i,        //! one-cycle pulse per interface: a served GET_AVB_INFO word changed
  input  wire  [MBX_N_IF_C-1:0]         asp_chg_p_i,        //! one-cycle pulse per interface: the served AS_PATH sequence changed
  input  wire  [MBX_N_IF_C-1:0]         amap_wr_p_i,        //! one-cycle pulse per interface: an edit's commit changed the live map

  input  wire  [15:0]                   evt_tail_words_i,   //! EVT_TAIL, words the core consumed
  output logic [15:0]                   evt_head_words_o,   //! EVT_HEAD, words posted here

  output logic                          wr_en_o,            //! write one event ring word
  output logic [$clog2(MBX_EVT_WORDS_C)-1:0] wr_addr_o,     //! word index inside the event ring
  output logic [31:0]                   wr_data_o           //! the word
);

  localparam int unsigned NT_C = MBX_N_TIMERS_C;
  localparam int unsigned SW_C = (NT_C > 1) ? $clog2(NT_C) : 1;   //! scanner index width
  localparam int unsigned NP_C = MBX_CTRCHG_N_PEND_C;              //! counter-change pending bits per interface
  localparam int unsigned PW_C = $clog2(NP_C);                     //! a pending bit's index width

  // ---- the timer bank -------------------------------------------------------------
  logic [NT_C-1:0] armed_r;
  logic [NT_C-1:0] pend_r;
  logic [15:0]     tag_r [NT_C];
  logic [31:0]     dl_r  [NT_C];
  logic [SW_C-1:0] scan_r;

  logic cmd_ok_w;
  assign cmd_ok_w    = tmr_cmd_p_i && (32'(tmr_slot_i) < NT_C)
                       && (32'(tmr_op_i) == MBX_TMR_OP_ARM_C || 32'(tmr_op_i) == MBX_TMR_OP_CANCEL_C);
  assign tmr_bad_p_o = tmr_cmd_p_i && !cmd_ok_w;

  // ---- the poster's choice -----------------------------------------------------------
  typedef enum logic [2:0] {SRC_LINK_S, SRC_GM_S, SRC_TIMER_S, SRC_TICK_S, SRC_AMAP_S, SRC_AVB_S, SRC_ASP_S,
                            SRC_CTR_S} src_t;

  logic [MBX_N_IF_C-1:0] posted_up_r;   //! the link level the last LINK record carried
  logic [MBX_N_IF_C-1:0] gm_pend_r;     //! a grandmaster change not yet posted
  logic [15:0]           head_r;
  logic [15:0]           seq_r;
  logic [1:0]            k_r;           //! record word being written
  logic                  busy_r;        //! a record is being written
  logic [31:0]           rec_r [4];
  logic [7:0]            tick_div_r;    //! milliseconds counted toward the next tick
  logic [15:0]           tick_cnt_r;    //! ticks counted and not yet posted, saturating
  logic [15:0]           amap_cnt_r [MBX_N_IF_C];   //! live map writes not yet posted, saturating
  logic [15:0]           avb_cnt_r  [MBX_N_IF_C];   //! AVB_INFO changes not yet posted, saturating
  logic [15:0]           asp_cnt_r  [MBX_N_IF_C];   //! AS_PATH changes not yet posted, saturating
  logic [NP_C-1:0]       ctr_pend_r [MBX_N_IF_C];   //! descriptors whose counters moved, not yet posted
  logic [NP_C-1:0]       ctr_seen_r [MBX_N_IF_C];   //! descriptors posted in this holdoff epoch
  logic [15:0]           ctr_epoch_r;   //! NOW_MS milliseconds into the holdoff epoch

  //! the pending bit a counter change names: its descriptor's, or ALL for a
  //! descriptor no family keeps a bit for
  function automatic logic [NP_C-1:0] ctr_bit_f(input logic [15:0] dtype, input logic [15:0] index);
    logic [NP_C-1:0] b;
    b = '0;
    b[MBX_CTRCHG_ALL_BIT_C] = 1'b1;
    for (int f = 0; f < int'(MBX_CTRCHG_N_SRC_C); f++) begin
      if (32'(dtype) == MBX_CTRCHG_TYPE_TBL_C[f] && 32'(index) < MBX_CTRCHG_COUNT_TBL_C[f]) begin
        b = '0;
        b[PW_C'(MBX_CTRCHG_FIRST_TBL_C[f] + 32'(index))] = 1'b1;
      end
    end
    return b;
  endfunction : ctr_bit_f

  logic tick_p_w;   //! a tick completes this cycle
  assign tick_p_w = tick_en_i && ms_tick_p_i && (32'(tick_div_r) + 32'd1 >= MBX_TICK_MS_C);

  logic        any_w;
  src_t        src_w;
  logic [MBX_IF_W_C-1:0] src_if_w;
  logic [SW_C-1:0] src_slot_w;
  logic [PW_C-1:0] src_bit_w;   //! the counter-change pending bit posted
  logic [15:0] used_w;   //! words posted and not released (a bad EVT_TAIL makes it exceed the ring)
  logic [15:0] free_w;
  always_comb begin : choose
    any_w      = 1'b0;
    src_w      = SRC_LINK_S;
    src_if_w   = '0;
    src_slot_w = '0;
    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
      if (!any_w && link_up_i[i] != posted_up_r[i]) begin
        any_w    = 1'b1;
        src_w    = SRC_LINK_S;
        src_if_w = MBX_IF_W_C'(i);
      end
    end
    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
      if (!any_w && gm_pend_r[i]) begin
        any_w    = 1'b1;
        src_w    = SRC_GM_S;
        src_if_w = MBX_IF_W_C'(i);
      end
    end
    for (int s = 0; s < int'(NT_C); s++) begin
      if (!any_w && pend_r[s]) begin
        any_w      = 1'b1;
        src_w      = SRC_TIMER_S;
        src_slot_w = SW_C'(s);
      end
    end
    if (!any_w && tick_cnt_r != 16'd0) begin
      any_w = 1'b1;
      src_w = SRC_TICK_S;
    end
    src_bit_w = '0;
    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
      if (!any_w && amap_cnt_r[i] != 16'd0) begin
        any_w    = 1'b1;
        src_w    = SRC_AMAP_S;
        src_if_w = MBX_IF_W_C'(i);
      end
    end
    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
      if (!any_w && avb_cnt_r[i] != 16'd0) begin
        any_w    = 1'b1;
        src_w    = SRC_AVB_S;
        src_if_w = MBX_IF_W_C'(i);
      end
    end
    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
      if (!any_w && asp_cnt_r[i] != 16'd0) begin
        any_w    = 1'b1;
        src_w    = SRC_ASP_S;
        src_if_w = MBX_IF_W_C'(i);
      end
    end
    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
      for (int b = 0; b < int'(NP_C); b++) begin
        if (!any_w && ctr_pend_r[i][b] && !ctr_seen_r[i][b]) begin
          any_w     = 1'b1;
          src_w     = SRC_CTR_S;
          src_if_w  = MBX_IF_W_C'(i);
          src_bit_w = PW_C'(b);
        end
      end
    end
    used_w = head_r - evt_tail_words_i;
    free_w = (used_w > 16'(MBX_EVT_WORDS_C)) ? 16'd0 : 16'(MBX_EVT_WORDS_C) - used_w;
  end : choose

  logic start_w;
  assign start_w = !busy_r && any_w && free_w >= 16'(MBX_EV_WORDS_C);

  // the record the chosen source posts
  logic [31:0] w0_w;
  logic [31:0] w1_w;
  logic [31:0] w2_w;
  logic [31:0] w3_w;
  always_comb begin : record
    logic [31:0] etype;
    logic [31:0] dtype;
    logic [31:0] dindex;
    etype = (src_w == SRC_LINK_S)  ? MBX_EV_TYPE_LINK_C
          : (src_w == SRC_GM_S)    ? MBX_EV_TYPE_GM_C
          : (src_w == SRC_TIMER_S) ? MBX_EV_TYPE_TIMER_C
          : (src_w == SRC_TICK_S)  ? MBX_EV_TYPE_TICK_C
          : (src_w == SRC_AMAP_S)  ? MBX_EV_TYPE_AMAP_LIVE_WRITE_C
          : (src_w == SRC_AVB_S)   ? MBX_EV_TYPE_AVB_INFO_CHANGED_C
          : (src_w == SRC_ASP_S)   ? MBX_EV_TYPE_AS_PATH_CHANGED_C : MBX_EV_TYPE_COUNTERS_CHANGED_C;
    // the descriptor a counter-change bit stands for; ALL names none
    dtype  = '0;
    dindex = '0;
    for (int f = 0; f < int'(MBX_CTRCHG_N_SRC_C); f++) begin
      if (32'(src_bit_w) >= MBX_CTRCHG_FIRST_TBL_C[f]
          && 32'(src_bit_w) < MBX_CTRCHG_FIRST_TBL_C[f] + MBX_CTRCHG_COUNT_TBL_C[f]) begin
        dtype  = MBX_CTRCHG_TYPE_TBL_C[f];
        dindex = 32'(src_bit_w) - MBX_CTRCHG_FIRST_TBL_C[f];
      end
    end
    w0_w = (etype << MBX_EVREC_W0_TYPE_LSB_C) | (32'(src_if_w) << MBX_EVREC_W0_IF_LSB_C)
         | (32'(seq_r) << MBX_EVREC_W0_SEQ_LSB_C);
    unique case (src_w)
      SRC_LINK_S: begin
        w1_w = 32'(link_up_i[src_if_w]) << MBX_EV_LINK_W1_UP_LSB_C;
        w2_w = '0;
        w3_w = now_ms_i << MBX_EV_LINK_W3_NOW_MS_LSB_C;
      end
      SRC_GM_S: begin
        w1_w = gm_id_i[64*src_if_w +: 32] << MBX_EV_GM_W1_ID_LO_LSB_C;
        w2_w = gm_id_i[64*src_if_w + 32 +: 32] << MBX_EV_GM_W2_ID_HI_LSB_C;
        w3_w = 32'(gptp_domain_i[8*src_if_w +: 8]) << MBX_EV_GM_W3_DOMAIN_LSB_C;
      end
      SRC_TIMER_S: begin
        w1_w = (32'(tag_r[src_slot_w]) << MBX_EV_TIMER_W1_TAG_LSB_C)
             | (32'(src_slot_w) << MBX_EV_TIMER_W1_SLOT_LSB_C);
        w2_w = dl_r[src_slot_w] << MBX_EV_TIMER_W2_DEADLINE_MS_LSB_C;
        w3_w = now_ms_i << MBX_EV_TIMER_W3_NOW_MS_LSB_C;
      end
      SRC_TICK_S: begin
        w1_w = 32'(tick_cnt_r) << MBX_EV_TICK_W1_COUNT_LSB_C;
        w2_w = '0;
        w3_w = now_ms_i << MBX_EV_TICK_W3_NOW_MS_LSB_C;
      end
      SRC_AMAP_S: begin
        w1_w = 32'(amap_cnt_r[src_if_w]) << MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_LSB_C;
        w2_w = '0;
        w3_w = now_ms_i << MBX_EV_AMAP_LIVE_WRITE_W3_NOW_MS_LSB_C;
      end
      SRC_AVB_S: begin
        w1_w = 32'(avb_cnt_r[src_if_w]) << MBX_EV_AVB_INFO_CHANGED_W1_COUNT_LSB_C;
        w2_w = '0;
        w3_w = now_ms_i << MBX_EV_AVB_INFO_CHANGED_W3_NOW_MS_LSB_C;
      end
      SRC_ASP_S: begin
        w1_w = 32'(asp_cnt_r[src_if_w]) << MBX_EV_AS_PATH_CHANGED_W1_COUNT_LSB_C;
        w2_w = '0;
        w3_w = now_ms_i << MBX_EV_AS_PATH_CHANGED_W3_NOW_MS_LSB_C;
      end
      default: begin
        w1_w = mbx_place_f(dtype, MBX_EV_COUNTERS_CHANGED_W1_TYPE_LSB_C, MBX_EV_COUNTERS_CHANGED_W1_TYPE_WIDTH_C)
             | mbx_place_f(dindex, MBX_EV_COUNTERS_CHANGED_W1_INDEX_LSB_C, MBX_EV_COUNTERS_CHANGED_W1_INDEX_WIDTH_C);
        w2_w = mbx_place_f(32'(32'(src_bit_w) == MBX_CTRCHG_ALL_BIT_C), MBX_EV_COUNTERS_CHANGED_W2_ALL_LSB_C,
                           MBX_EV_COUNTERS_CHANGED_W2_ALL_WIDTH_C);
        w3_w = now_ms_i << MBX_EV_COUNTERS_CHANGED_W3_NOW_MS_LSB_C;
      end
    endcase
  end : record

  always_ff @(posedge clk_i) begin : timers
    if (!rst_n) begin
      armed_r <= '0;
      pend_r  <= '0;
      scan_r  <= '0;
      for (int s = 0; s < int'(NT_C); s++) begin
        tag_r[s] <= '0;
        dl_r[s]  <= '0;
      end
    end else begin
      scan_r <= (32'(scan_r) == NT_C - 1) ? '0 : scan_r + SW_C'(1);
      if (armed_r[scan_r] && $signed(now_ms_i - dl_r[scan_r]) >= 0) begin
        armed_r[scan_r] <= 1'b0;
        pend_r[scan_r]  <= 1'b1;
      end
      if (start_w && src_w == SRC_TIMER_S) pend_r[src_slot_w] <= 1'b0;
      // a command on a slot wins over its own scan and post in the same cycle
      if (cmd_ok_w) begin
        armed_r[SW_C'(tmr_slot_i)] <= (32'(tmr_op_i) == MBX_TMR_OP_ARM_C);
        pend_r[SW_C'(tmr_slot_i)]  <= 1'b0;
        if (32'(tmr_op_i) == MBX_TMR_OP_ARM_C) begin
          tag_r[SW_C'(tmr_slot_i)] <= tmr_tag_i;
          dl_r[SW_C'(tmr_slot_i)]  <= tmr_deadline_ms_i;
        end
      end
    end
  end : timers

  // the counter-change sources' next state: a change in the posting cycle stays
  // pending, and a post in the cycle the epoch ends counts in the next epoch
  logic            ctr_roll_w;   //! the holdoff epoch ends this cycle
  logic [NP_C-1:0] ctr_pend_n_w [MBX_N_IF_C];
  logic [NP_C-1:0] ctr_seen_n_w [MBX_N_IF_C];
  assign ctr_roll_w = ms_tick_p_i && (32'(ctr_epoch_r) + 32'd1 >= MBX_CTRCHG_HOLDOFF_MS_C);
  always_comb begin : ctr_next
    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
      ctr_pend_n_w[i] = ctr_pend_r[i];
      ctr_seen_n_w[i] = ctr_roll_w ? '0 : ctr_seen_r[i];
      if (start_w && src_w == SRC_CTR_S && src_if_w == MBX_IF_W_C'(i)) begin
        ctr_pend_n_w[i][src_bit_w] = 1'b0;
        ctr_seen_n_w[i][src_bit_w] = 1'b1;
      end
      if (ctr_chg_p_i[i])
        ctr_pend_n_w[i] = ctr_pend_n_w[i] | ctr_bit_f(ctr_chg_type_i[16*i +: 16], ctr_chg_index_i[16*i +: 16]);
    end
  end : ctr_next

  always_ff @(posedge clk_i) begin : poster
    if (!rst_n) begin
      posted_up_r <= '0;
      gm_pend_r   <= '0;
      head_r      <= '0;
      seq_r       <= '0;
      k_r         <= '0;
      busy_r      <= 1'b0;
      tick_div_r  <= '0;
      tick_cnt_r  <= '0;
      ctr_epoch_r <= '0;
      for (int k = 0; k < 4; k++) rec_r[k] <= '0;
      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
        amap_cnt_r[i] <= '0;
        avb_cnt_r[i]  <= '0;
        asp_cnt_r[i]  <= '0;
        ctr_pend_r[i] <= '0;
        ctr_seen_r[i] <= '0;
      end
    end else begin
      // the face events: a pulse in the posting cycle counts toward the next record
      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
        if (start_w && src_w == SRC_AMAP_S && src_if_w == MBX_IF_W_C'(i)) amap_cnt_r[i] <= 16'(amap_wr_p_i[i]);
        else if (amap_wr_p_i[i] && amap_cnt_r[i] != 16'hFFFF) amap_cnt_r[i] <= amap_cnt_r[i] + 16'd1;
        if (start_w && src_w == SRC_AVB_S && src_if_w == MBX_IF_W_C'(i)) avb_cnt_r[i] <= 16'(avb_chg_p_i[i]);
        else if (avb_chg_p_i[i] && avb_cnt_r[i] != 16'hFFFF) avb_cnt_r[i] <= avb_cnt_r[i] + 16'd1;
        if (start_w && src_w == SRC_ASP_S && src_if_w == MBX_IF_W_C'(i)) asp_cnt_r[i] <= 16'(asp_chg_p_i[i]);
        else if (asp_chg_p_i[i] && asp_cnt_r[i] != 16'hFFFF) asp_cnt_r[i] <= asp_cnt_r[i] + 16'd1;
        ctr_pend_r[i] <= ctr_pend_n_w[i];
        ctr_seen_r[i] <= ctr_seen_n_w[i];
      end
      if (ms_tick_p_i) ctr_epoch_r <= ctr_roll_w ? '0 : ctr_epoch_r + 16'd1;
      // the tick: a disabled tick holds nothing; a tick in the posting cycle
      // counts toward the next record
      if (!tick_en_i) begin
        tick_div_r <= '0;
        tick_cnt_r <= '0;
      end else begin
        if (ms_tick_p_i) tick_div_r <= tick_p_w ? 8'd0 : tick_div_r + 8'd1;
        if (start_w && src_w == SRC_TICK_S) tick_cnt_r <= 16'(tick_p_w);
        else if (tick_p_w && tick_cnt_r != 16'hFFFF) tick_cnt_r <= tick_cnt_r + 16'd1;
      end
      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin
        if (gm_change_p_i[i]) gm_pend_r[i] <= 1'b1;
        else if (start_w && src_w == SRC_GM_S && src_if_w == MBX_IF_W_C'(i)) gm_pend_r[i] <= 1'b0;
      end
      if (start_w) begin
        if (src_w == SRC_LINK_S) posted_up_r[src_if_w] <= link_up_i[src_if_w];
        rec_r[0] <= w0_w;
        rec_r[1] <= w1_w;
        rec_r[2] <= w2_w;
        rec_r[3] <= w3_w;
        k_r      <= '0;
        busy_r   <= 1'b1;
      end else if (busy_r) begin
        k_r <= k_r + 2'd1;
        if (k_r == 2'd3) begin
          busy_r <= 1'b0;
          head_r <= head_r + 16'(MBX_EV_WORDS_C);
          seq_r  <= seq_r + 16'd1;
        end
      end
    end
  end : poster

  assign wr_en_o          = busy_r;
  assign wr_addr_o        = $clog2(MBX_EVT_WORDS_C)'((head_r + 16'(k_r)) & (16'(MBX_EVT_WORDS_C) - 16'd1));
  assign wr_data_o        = rec_r[k_r];
  assign evt_head_words_o = head_r;

endmodule : KL_mbx_evt

`default_nettype wire
