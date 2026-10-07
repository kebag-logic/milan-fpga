/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_maap.sv
  Author      : Kebag Logic

  Date        : 2026-07-17
  Description : MAAP (IEEE 1722-2016 Annex B) dynamic multicast-DMAC
                allocation - Milan-mandatory for talkers. The standard is
                the authority (#686); docs/design/MAAP_FABRIC.md carries the
                clause-by-clause contract:

                  pool 91:E0:F0:00:00:00 + 16-bit offset, size 0xFE00 (B.4);
                  ethertype 0x22F0, subtype 0xFE, maap_version 1,
                  control_data_length 16 in every frame (B.2.1). PROBE and
                  ANNOUNCE go to 91:E0:F0:00:FF:00 (Table B.10); a DEFEND
                  goes to the source MAC of the PROBE that caused it (B.2.1).

                  SM (Table B.7; IDLE = INITIAL, ANNOUNCE = DEFEND):
                  enable (Begin!) or a conflict (Restart!) draws an offset
                  and runs ReserveAddress!: the first PROBE goes at once,
                  three more follow at the probe timer (Table B.8
                  MAAP_PROBE_RETRANSMITS = 3), and the decrement to zero
                  (probeCount!) sends the first ANNOUNCE at once and enters
                  ANNOUNCE, where the address is VALID and re-announced at
                  the announce timer. Timers (B.3.4): probe strictly inside
                  500..600 ms, announce strictly inside 30..32 s.
                  RX, only for a range that conflicts (note b: the ranges
                  share an address; an empty range never conflicts):
                  PROBE while probing -> re-address; PROBE while announced
                  -> DEFEND with the overlapping sub-range (B.2.7/B.2.8);
                  DEFEND -> re-address; ANNOUNCE while probing ->
                  re-address; ANNOUNCE while announced -> compare_MAC
                  (B.3.6.4), re-address only when this station is not the
                  lower. A DEFEND is judged on its conflict_* fields, a
                  PROBE or ANNOUNCE on its requested_* fields (B.2.5-B.2.8).

                Deviations (documented in MAAP_FABRIC.md, outside #686's
                items): no compare_MAC in the rProbe!/PROBE and
                rDefend!/DEFEND cells; a DEFEND carries this station's
                range, not the PROBE's, in requested_* (B.3.6.6); a 16-bit
                station-MAC-seeded LFSR draws the offset (B.3.6.1); no
                PortOperational! input; RX parse is untagged-only (a tagged
                MAAP PDU is ignored).

                Persistence (reference load/save_state) is softcore
                provisioning: software may seed seed_offset_i +
                seed_valid_i before enable to re-probe the previously won
                block (Table B.7 note a).

  Company     : Kebag Logic
  Project     : Milan AVTP

  Notes       :
    - RX side is the standard non-intrusive monitor tap (never backpressures).
    - TX emits one 60-byte padded frame per event through the low-rate
      adp_tx_arbiter chain.
------------------------------------------------------------------------------
*/

//! MAAP (IEEE 1722-2016 Annex B) probe/defend/announce state machine
//! allocating a block of multicast destination MACs from the 91:E0:F0 pool.
//! `addr_o` / `addr_valid_o` (valid only in ANNOUNCE) feed the AAF framer's
//! DMAC mux; conflicting received PROBE/DEFEND/ANNOUNCE PDUs re-randomize the
//! block per the Table B.7 cells listed in the banner.

`default_nettype none

module KL_maap #(
  parameter int unsigned CLK_FREQ_HZ_P = 50_000_000  //! ms tick divider base
)(
  input  wire         clk_i,             //! Global clock
  input  wire         rst_n,             //! Active-low synchronous reset

  input  wire         enable_i,          //! CSR MAAP_CTRL.en (0 = engine idle)
  input  wire [7:0]   count_i,           //! block size to claim (reference: 8)
  input  wire [47:0]  station_mac_i,     //! source MAC ([47:40] = first wire byte)
  input  wire [15:0]  seed_offset_i,     //! provisioning: preferred offset
  input  wire         seed_valid_i,      //! 1 = first probe uses seed_offset_i

  //! --- monitored RX AXI-Stream (observed, never driven) ------------------
  input  wire [63:0]  rx_tdata_i,
  input  wire [7:0]   rx_tkeep_i,
  input  wire         rx_tvalid_i,
  input  wire         rx_tready_i,
  input  wire         rx_tlast_i,

  //! --- MAAP PDU out (low-rate, to the adp_tx_arbiter chain) --------------
  output logic [63:0] m_axis_tdata,
  output logic [7:0]  m_axis_tkeep,
  output logic        m_axis_tvalid,
  output logic        m_axis_tlast,
  input  wire         m_axis_tready,

  //! --- allocation result --------------------------------------------------
  output logic [47:0] addr_o,            //! allocated base DMAC (index 0)
  output logic        addr_valid_o,      //! 1 = ANNOUNCE state (claim held)

  //! --- observability (CSR 0x6D0 group) ------------------------------------
  output logic [1:0]  state_o,           //! 0 idle / 1 probe / 2 announce
  output logic [15:0] offset_o,          //! current claimed offset
  output logic [7:0]  conflicts_o,       //! re-address events (saturating)
  output logic [7:0]  defends_o          //! DEFEND frames sent (saturating)
);

  // ---- Annex B constants ---------------------------------------------------
  localparam logic [31:0] POOL_BASE_HI_C = 32'h91E0_F000;  //! bytes 0..3
  localparam logic [15:0] POOL_SIZE_C    = 16'hFE00;
  localparam logic [47:0] MAAP_DST_C     = 48'h91E0_F000_FF00;  //! Table B.10
  localparam logic [7:0]  CDL_C          = 8'd16;    //! B.2.1, every frame
  localparam logic [1:0]  MSG_PROBE_C    = 2'd1;     //! Table B.1
  localparam logic [1:0]  MSG_DEFEND_C   = 2'd2;
  localparam logic [1:0]  MSG_ANNOUNCE_C = 2'd3;
  //! the ReserveAddress! PROBE plus MAAP_PROBE_RETRANSMITS (Table B.8: 3)
  localparam int unsigned PROBE_SENDS_C  = 4;
  //! Timer draws. A load of N ms expires after more than N-1 ms and at most
  //! N ms plus a cycle, and the send then waits for any frame in flight.
  //! B.3.4.2 wants 500 < T < 600 ms: N = 518 + 0..63 keeps 17 ms at each
  //! end. B.3.4.1 wants 30 s < T < 32 s: N = 30488 + 0..1023 keeps 487 ms.
  localparam int unsigned PROBE_MIN_MS_C    = 518;
  localparam int unsigned ANNOUNCE_MIN_MS_C = 30488;

  typedef enum logic [1:0] { IDLE_S, PROBE_S, ANNOUNCE_S } mstate_t;
  mstate_t state_r;
  assign state_o = state_r;

  // ---- ms tick + LFSR ------------------------------------------------------
  localparam int unsigned TICK_DIV_C = CLK_FREQ_HZ_P / 1000;
  logic [$clog2(TICK_DIV_C)-1:0] tickdiv_r;
  logic         tick_ms_w;
  assign tick_ms_w = (tickdiv_r == '0);

  //! 16-bit Fibonacci LFSR (x^16+x^15+x^13+x^4+1), station-MAC seeded
  logic [15:0]  lfsr_r;
  wire  [15:0]  lfsr_next_w = {lfsr_r[14:0],
                               lfsr_r[15] ^ lfsr_r[14] ^ lfsr_r[12] ^ lfsr_r[3]};

  // ---- claim state ----------------------------------------------------------
  logic [15:0]  offset_r;
  logic [2:0]   probe_left_r;            //! PROBEs still to send, 4..1
  logic [15:0]  timer_ms_r;              //! counts down to the next TX event
  logic         seed_used_r;
  assign offset_o = offset_r;
  assign addr_o   = {POOL_BASE_HI_C, offset_r};
  assign addr_valid_o = (state_r == ANNOUNCE_S);

  //! bounded random offset: fold the LFSR into the pool and keep the block
  //! inside it (documented deviation from the reference's exact modulo)
  function automatic [15:0] rand_offset(input [15:0] rnd, input [7:0] cnt);
    logic [15:0] o;
    o = (rnd >= POOL_SIZE_C) ? 16'(rnd - POOL_SIZE_C) : rnd;
    if (o > 16'(POOL_SIZE_C - 16'(cnt))) o = 16'(POOL_SIZE_C - 16'(cnt));
    rand_offset = o;
  endfunction

  //! probe interval: 518 + lfsr[5:0] ms; announce: 30488 + lfsr[9:0] ms
  wire [15:0] probe_iv_w    = 16'(PROBE_MIN_MS_C)    + {10'd0, lfsr_r[5:0]};
  wire [15:0] announce_iv_w = 16'(ANNOUNCE_MIN_MS_C) + {6'd0, lfsr_r[9:0]};

  // ---- RX parse (untagged control AVTPDU, aligned lanes) --------------------
  //! frame bytes: 6..11 source MAC, 12..13 ethertype, 14 subtype,
  //! 15 msg_type[3:0], 26..31 request_start, 32..33 request_count,
  //! 34..39 conflict_start, 40..41 conflict_count. The range a PDU is judged
  //! on is captured into ONE register set: requested_* for a PROBE or
  //! ANNOUNCE, conflict_* for a DEFEND. The two sit 8 bytes apart, so they
  //! share byte lanes and the message type only picks the beat.
  wire in_acc_w = rx_tvalid_i && rx_tready_i;

  logic [2:0]   rbeat_r;
  logic         is_maap_r;
  logic [3:0]   rx_msg_r;
  logic [47:0]  rx_src_r;                //! source MAC ([47:40] = byte 6)
  logic         rx_pool_r;               //! range bytes 0..3 == pool base
  logic [15:0]  rx_start_r;              //! range offset
  logic [15:0]  rx_cnt_r;                //! range count
  logic         rx_done_p;               //! pulse: full PDU parsed

  //! byte lane accessor (little lane order: lane j = wire byte 8b+j)
  function automatic [7:0] lane(input [63:0] w, input [2:0] j);
    lane = w[8*j +: 8];
  endfunction

  //! the range sits one beat later in a DEFEND (conflict_*, B.2.7/B.2.8)
  wire       rx_defend_w = (rx_msg_r == {2'b00, MSG_DEFEND_C});
  wire [2:0] start_beat_w = rx_defend_w ? 3'd4 : 3'd3;
  wire [2:0] cnt_beat_w   = rx_defend_w ? 3'd5 : 3'd4;

  // ---- conflict math (Table B.7 note b: the ranges share an address) --------
  //! Half-open ranges with 17-bit ends, so an adjacent range is not a
  //! conflict and an empty range (count 0) never conflicts.
  wire [16:0] our_end_w = {1'b0, offset_r}   + {9'd0, count_i};
  wire [16:0] req_end_w = {1'b0, rx_start_r} + {1'b0, rx_cnt_r};
  wire        conflict_w = rx_pool_r && (rx_cnt_r != 16'd0) && (count_i != 8'd0)
                           && ({1'b0, rx_start_r} < our_end_w)
                           && ({1'b0, offset_r} < req_end_w);
  //! the overlapping sub-range a DEFEND reports (B.2.7/B.2.8)
  wire [15:0] conf_start_w = (rx_start_r > offset_r) ? rx_start_r : offset_r;
  wire [16:0] conf_end_w   = (req_end_w < our_end_w) ? req_end_w : our_end_w;
  wire [15:0] conf_cnt_w   = 16'(conf_end_w - {1'b0, conf_start_w});

  //! compare_MAC (B.3.6.4): octet-wise reversed unsigned compare, TRUE when
  //! this station's MAC is the lower; TRUE means no protocol action (note d)
  function automatic [47:0] octet_rev(input [47:0] m);
    octet_rev = {m[7:0], m[15:8], m[23:16], m[31:24], m[39:32], m[47:40]};
  endfunction
  wire mac_lower_w = octet_rev(station_mac_i) < octet_rev(rx_src_r);

  // ---- TX frame builder -----------------------------------------------------
  //! 60-byte padded frame, 8 beats, last keep 0x0F. Every per-frame field is
  //! latched at the send request, so a Restart! (or the next RX PDU) taken
  //! while a frame is on the wire cannot rewrite that frame.
  logic        tx_busy_r;
  logic [1:0]  tx_msg_r;
  logic [47:0] tx_dst_r;                 //! DEFEND only: the prober's MAC
  logic [15:0] tx_off_r;                 //! requested_start offset
  logic [15:0] tx_conf_start_r, tx_conf_cnt_r;
  logic [2:0]  tx_beat_r;

  function automatic [63:0] tx_beat(input [2:0] b);
    logic [7:0] f [0:63];
    for (int i = 0; i < 64; i++) f[i] = 8'h00;
    //! B.2.1: a DEFEND to the triggering PROBE's source, others multicast
    {f[0],f[1],f[2],f[3],f[4],f[5]} = (tx_msg_r == MSG_DEFEND_C) ? tx_dst_r
                                                                  : MAAP_DST_C;
    {f[6],f[7],f[8],f[9],f[10],f[11]} = station_mac_i;
    f[12] = 8'h22; f[13] = 8'hF0;
    f[14] = 8'hFE;                                   // subtype MAAP
    f[15] = {6'h0, tx_msg_r};                        // sv=0, ver=0, msg
    f[16] = 8'h08;                                   // maap_version=1, cdl[10:8]
    f[17] = CDL_C;                                   // control_data_length
    // stream_id bytes 18..25 = 0
    {f[26],f[27],f[28],f[29]} = POOL_BASE_HI_C;      // request_start
    f[30] = tx_off_r[15:8]; f[31] = tx_off_r[7:0];
    f[32] = 8'h00; f[33] = count_i;                  // request_count
    if (tx_msg_r == MSG_DEFEND_C) begin              // DEFEND: conflict fields
      {f[34],f[35],f[36],f[37]} = POOL_BASE_HI_C;
      f[38] = tx_conf_start_r[15:8]; f[39] = tx_conf_start_r[7:0];
      f[40] = tx_conf_cnt_r[15:8];   f[41] = tx_conf_cnt_r[7:0];
    end
    tx_beat = {f[{b,3'd7}], f[{b,3'd6}], f[{b,3'd5}], f[{b,3'd4}],
               f[{b,3'd3}], f[{b,3'd2}], f[{b,3'd1}], f[{b,3'd0}]};
  endfunction

  assign m_axis_tdata  = tx_beat(tx_beat_r);
  assign m_axis_tvalid = tx_busy_r;
  assign m_axis_tlast  = tx_busy_r && (tx_beat_r == 3'd7);
  assign m_axis_tkeep  = (tx_beat_r == 3'd7) ? 8'h0F : 8'hFF;

  // ---- protocol reactions (one parsed PDU per rx_done_p) --------------------
  //! Table B.7 rows rProbe!/rDefend!/rAnnounce!, for a conflicting range only
  wire rx_hit_w = rx_done_p && (state_r != IDLE_S) && conflict_w;
  //! INITIAL/Restart!: re-address and probe again
  wire restart_w = rx_hit_w &&
                   (((rx_msg_r == {2'b00, MSG_PROBE_C}) && (state_r == PROBE_S)) ||
                    (rx_msg_r == {2'b00, MSG_DEFEND_C}) ||
                    ((rx_msg_r == {2'b00, MSG_ANNOUNCE_C}) &&
                     ((state_r == PROBE_S) || !mac_lower_w)));
  //! sDefend; a PROBE parsed while a frame is in flight goes unanswered
  wire defend_w  = rx_hit_w && (rx_msg_r == {2'b00, MSG_PROBE_C})
                   && (state_r == ANNOUNCE_S) && !tx_busy_r;

  // ---- main SM ---------------------------------------------------------------
  //! generate_address for Begin!: the provisioning seed once (note a)
  wire [15:0] new_off_w = seed_valid_i && !seed_used_r
                          ? seed_offset_i : rand_offset(lfsr_next_w, count_i);

  always_ff @(posedge clk_i) begin : maap_sm
    if (!rst_n) begin
      state_r      <= IDLE_S;
      offset_r     <= '0;
      probe_left_r <= '0;
      timer_ms_r   <= '0;
      tickdiv_r    <= '0;
      lfsr_r       <= 16'hACE1 ^ station_mac_i[15:0]
                      ^ {station_mac_i[31:24], station_mac_i[23:16]};
      seed_used_r  <= 1'b0;
      conflicts_o  <= '0;
      defends_o    <= '0;
      tx_busy_r    <= 1'b0;
      tx_msg_r     <= '0;
      tx_dst_r     <= '0;
      tx_off_r     <= '0;
      tx_conf_start_r <= '0;
      tx_conf_cnt_r   <= '0;
      tx_beat_r    <= '0;
      rbeat_r      <= '0;
      is_maap_r    <= 1'b0;
      rx_msg_r     <= '0;
      rx_src_r     <= '0;
      rx_pool_r    <= 1'b0;
      rx_start_r   <= '0;
      rx_cnt_r     <= '0;
      rx_done_p    <= 1'b0;
    end
    else begin
      rx_done_p <= 1'b0;

      //! free-running entropy + ms tick
      lfsr_r    <= lfsr_next_w;
      tickdiv_r <= (tickdiv_r == '0) ? ($bits(tickdiv_r))'(TICK_DIV_C - 1)
                                     : tickdiv_r - 1'b1;
      if (tick_ms_w && timer_ms_r != '0) timer_ms_r <= timer_ms_r - 16'd1;

      // ---- TX beat engine ------------------------------------------------
      if (tx_busy_r && m_axis_tready) begin
        tx_beat_r <= tx_beat_r + 3'd1;
        if (tx_beat_r == 3'd7) begin
          tx_busy_r <= 1'b0;
          tx_beat_r <= '0;
        end
      end

      // ---- RX monitor tap parse ------------------------------------------
      if (in_acc_w) begin
        rbeat_r <= (rbeat_r == 3'd7) ? 3'd7 : rbeat_r + 3'd1;
        if (rbeat_r == 3'd0)
          rx_src_r[47:32] <= {lane(rx_tdata_i, 3'd6), lane(rx_tdata_i, 3'd7)};
        if (rbeat_r == 3'd1) begin
          rx_src_r[31:0] <= {lane(rx_tdata_i, 3'd0), lane(rx_tdata_i, 3'd1),
                             lane(rx_tdata_i, 3'd2), lane(rx_tdata_i, 3'd3)};
          is_maap_r <= (lane(rx_tdata_i, 3'd4) == 8'h22) &&
                       (lane(rx_tdata_i, 3'd5) == 8'hF0) &&
                       (lane(rx_tdata_i, 3'd6) == 8'hFE);
          rx_msg_r  <= lane(rx_tdata_i, 3'd7) & 8'h0F;
        end
        if (rbeat_r == start_beat_w) begin
          rx_pool_r  <= {lane(rx_tdata_i, 3'd2), lane(rx_tdata_i, 3'd3),
                         lane(rx_tdata_i, 3'd4), lane(rx_tdata_i, 3'd5)}
                        == POOL_BASE_HI_C;
          rx_start_r <= {lane(rx_tdata_i, 3'd6), lane(rx_tdata_i, 3'd7)};
        end
        if (rbeat_r == cnt_beat_w)
          rx_cnt_r <= {lane(rx_tdata_i, 3'd0), lane(rx_tdata_i, 3'd1)};
        if (rx_tlast_i) begin
          rbeat_r   <= '0;
          rx_done_p <= is_maap_r && (rbeat_r >= 3'd5) && enable_i;
          is_maap_r <= 1'b0;
        end
      end

      // ---- state walk -------------------------------------------------------
      //! One decision per cycle, in priority order: disable (Release!), a
      //! conflict Restart!, a DEFEND, then the timer's own send. A timer send
      //! deferred by any of them happens on a later cycle; the timer holds 0.
      case (state_r)
        IDLE_S : begin
          if (!enable_i) seed_used_r <= 1'b0;   //! re-arm the seed on disable
          if (enable_i) begin                   //! Begin! -> ReserveAddress!
            offset_r     <= new_off_w;
            seed_used_r  <= 1'b1;
            probe_left_r <= 3'(PROBE_SENDS_C);
            timer_ms_r   <= '0;                 //! sProbe at once
            state_r      <= PROBE_S;
          end
        end

        PROBE_S, ANNOUNCE_S : begin
          if (!enable_i) state_r <= IDLE_S;
          else if (restart_w) begin             //! Restart! -> ReserveAddress!
            offset_r     <= rand_offset(lfsr_r, count_i);
            probe_left_r <= 3'(PROBE_SENDS_C);
            timer_ms_r   <= '0;                 //! sProbe at once
            state_r      <= PROBE_S;
            conflicts_o  <= (&conflicts_o) ? conflicts_o : conflicts_o + 8'd1;
          end
          else if (defend_w) begin              //! sDefend the overlap
            tx_msg_r        <= MSG_DEFEND_C;
            tx_dst_r        <= rx_src_r;
            tx_off_r        <= offset_r;
            tx_conf_start_r <= conf_start_w;
            tx_conf_cnt_r   <= conf_cnt_w;
            tx_busy_r       <= 1'b1;
            defends_o <= (&defends_o) ? defends_o : defends_o + 8'd1;
          end
          else if (timer_ms_r == '0 && !tx_busy_r) begin
            tx_busy_r <= 1'b1;
            tx_off_r  <= offset_r;
            if (state_r == ANNOUNCE_S) begin    //! announcetimer!: sAnnounce
              tx_msg_r   <= MSG_ANNOUNCE_C;
              timer_ms_r <= announce_iv_w;
            end
            else begin                          //! sProbe
              tx_msg_r <= MSG_PROBE_C;
              if (probe_left_r <= 3'd1) begin
                //! probeCount!: the first ANNOUNCE follows at once
                state_r    <= ANNOUNCE_S;
                timer_ms_r <= '0;
              end
              else begin                        //! probetimer! re-armed
                probe_left_r <= probe_left_r - 3'd1;
                timer_ms_r   <= probe_iv_w;
              end
            end
          end
        end

        // verilator coverage_off
        default : begin
          state_r <= IDLE_S;
        end
        // verilator coverage_on
      endcase
    end
  end : maap_sm

endmodule

`default_nettype wire
