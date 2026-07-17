/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_maap.sv
  Author      : Kebag Logic

  Date        : 2026-07-17
  Description : MAAP (IEEE 1722 Annex B) dynamic multicast-DMAC allocation —
                Milan-mandatory for talkers. Contract byte-extracted from the
                pipewire module-avb reference (maap.c/maap.h), normative plan
                in docs/design/MAAP_FABRIC.md:

                  pool 91:E0:F0:00:00:00 + 16-bit offset, size 0xFE00;
                  dst MAC 91:E0:F0:00:FF:00, ethertype 0x22F0, subtype 0xFE,
                  maap_version 1 (status field), length 28 (reference bytes;
                  strict 1722 says 16 - the TB goldens vs the REFERENCE).

                  SM: IDLE -> PROBE (offset = rand % (0xFE00-count), 3 PROBEs
                  every 500 ms + jitter) -> ANNOUNCE (every 3000 ms + jitter;
                  address VALID only here).
                  RX PROBE conflicting: PROBING -> re-address;
                  ANNOUNCED -> send DEFEND with the overlapping sub-range.
                  RX DEFEND/ANNOUNCE conflicting -> re-address always
                  (reference checks the CONFLICT fields of both).
                  Conflict = first 4 bytes == pool base AND 16-bit range
                  overlap with the reference's inclusive-end compares.

                Deviations (documented): interval jitter is LFSR-based
                0..127 ms / 0..2047 ms (reference drand48 0..100 / 0..2000 -
                spec allows any); RX parse is untagged-only (the reference
                transmits untagged; a tagged MAAP PDU is ignored).

                Persistence (reference load/save_state) is softcore
                provisioning: software may seed offset_i + kick_p_i before
                enable to re-probe the previously won block.

  Company     : Kebag Logic
  Project     : Milan AVTP

  Notes       :
    - RX side is the standard non-intrusive monitor tap (never backpressures).
    - TX emits one 60-byte padded frame per event through the low-rate
      adp_tx_arbiter chain.
------------------------------------------------------------------------------
*/

//! MAAP (IEEE 1722 Annex B) probe/defend/announce state machine allocating a
//! block of multicast destination MACs from the 91:E0:F0 pool. `addr_o` /
//! `addr_valid_o` (valid only in ANNOUNCE) feed the AAF framer's DMAC mux;
//! conflicts with received PROBE/DEFEND/ANNOUNCE PDUs re-randomize the block
//! per the pipewire module-avb reference contract.

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

  // ---- reference constants -------------------------------------------------
  localparam logic [31:0] POOL_BASE_HI_C = 32'h91E0_F000;  //! bytes 0..3
  localparam logic [15:0] POOL_SIZE_C    = 16'hFE00;
  localparam logic [47:0] MAAP_DST_C     = 48'h91E0_F000_FF00;
  localparam int unsigned PROBE_N_C      = 3;
  localparam int unsigned PROBE_MS_C     = 500;
  localparam int unsigned ANNOUNCE_MS_C  = 3000;

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
  logic [7:0]   probe_left_r;
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

  //! probe interval: 500 + lfsr[6:0] ms; announce: 3000 + lfsr[10:0] ms
  wire [15:0] probe_iv_w    = 16'(PROBE_MS_C)    + {9'd0, lfsr_r[6:0]};
  wire [15:0] announce_iv_w = 16'(ANNOUNCE_MS_C) + {5'd0, lfsr_r[10:0]};

  // ---- RX parse (untagged control AVTPDU, aligned lanes) --------------------
  //! frame bytes: 12..13 ethertype, 14 subtype, 15 msg_type[3:0],
  //! 26..31 request_start, 32..33 request_count,
  //! 34..39 conflict_start, 40..41 conflict_count
  wire in_acc_w = rx_tvalid_i && rx_tready_i;

  logic [2:0]   rbeat_r;
  logic         is_maap_r;
  logic [3:0]   rx_msg_r;
  logic [47:0]  rx_req_start_r, rx_conf_start_r;
  logic [15:0]  rx_req_cnt_r,   rx_conf_cnt_r;
  logic         rx_done_p;               //! pulse: full PDU parsed

  //! byte lane accessor (little lane order: lane j = wire byte 8b+j)
  function automatic [7:0] lane(input [63:0] w, input [2:0] j);
    lane = w[8*j +: 8];
  endfunction

  // ---- conflict math (reference maap_check_conflict, inclusive ends) --------
  function automatic logic conflict_hit(
      input [47:0] start_a, input [15:0] cnt_a);
    logic [15:0] our_s, our_e, req_s, req_e;
    our_s = offset_r; our_e = 16'(offset_r + 16'(count_i));
    req_s = start_a[15:0]; req_e = 16'(req_s + cnt_a);
    conflict_hit = (start_a[47:16] == POOL_BASE_HI_C) &&
                   ((our_s >= req_s && our_s <= req_e) ||
                    (req_s >= our_s && req_s <= our_e));
  endfunction

  function automatic [31:0] conflict_range(  //! {start16, count16}
      input [47:0] start_a, input [15:0] cnt_a);
    logic [15:0] our_s, our_e, req_s, req_e, c_s, c_c;
    our_s = offset_r; our_e = 16'(offset_r + 16'(count_i));
    req_s = start_a[15:0]; req_e = 16'(req_s + cnt_a);
    if (our_s >= req_s && our_s <= req_e) begin
      c_s = our_s;
      c_c = ((our_e < req_e) ? our_e : req_e) - our_s;
    end
    else begin
      c_s = req_s;
      c_c = ((req_e < our_e) ? req_e : our_e) - req_s;
    end
    conflict_range = {c_s, c_c};
  endfunction

  // ---- TX frame builder -----------------------------------------------------
  //! 60-byte padded frame, 8 beats, last keep 0x0F; msg/conflict latched at
  //! send request. Layout per the reference (length field = 28).
  logic        tx_busy_r;
  logic [3:0]  tx_msg_r;
  logic [15:0] tx_conf_start_r, tx_conf_cnt_r;
  logic [2:0]  tx_beat_r;

  function automatic [63:0] tx_beat(input [2:0] b);
    logic [7:0] f [0:63];
    for (int i = 0; i < 64; i++) f[i] = 8'h00;
    {f[0],f[1],f[2],f[3],f[4],f[5]} = MAAP_DST_C;
    {f[6],f[7],f[8],f[9],f[10],f[11]} = station_mac_i;
    f[12] = 8'h22; f[13] = 8'hF0;
    f[14] = 8'hFE;                                   // subtype MAAP
    f[15] = {4'h0, tx_msg_r};                        // sv=0, ver=0, msg
    f[16] = 8'h08;                                   // maap_version=1, len[10:8]
    f[17] = 8'h1C;                                   // length = 28 (reference)
    // stream_id bytes 18..25 = 0
    {f[26],f[27],f[28],f[29]} = POOL_BASE_HI_C;      // request_start
    f[30] = offset_r[15:8]; f[31] = offset_r[7:0];
    f[32] = 8'h00; f[33] = count_i;                  // request_count
    if (tx_msg_r == 4'd2) begin                      // DEFEND: conflict fields
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

  // ---- main SM ---------------------------------------------------------------
  //! re-address helper values (applied via the re_addr_w strobe in the FSM)
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
      tx_conf_start_r <= '0;
      tx_conf_cnt_r   <= '0;
      tx_beat_r    <= '0;
      rbeat_r      <= '0;
      is_maap_r    <= 1'b0;
      rx_msg_r     <= '0;
      rx_req_start_r  <= '0;
      rx_conf_start_r <= '0;
      rx_req_cnt_r    <= '0;
      rx_conf_cnt_r   <= '0;
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
        if (rbeat_r == 3'd1) begin
          is_maap_r <= (lane(rx_tdata_i, 3'd4) == 8'h22) &&
                       (lane(rx_tdata_i, 3'd5) == 8'hF0) &&
                       (lane(rx_tdata_i, 3'd6) == 8'hFE);
          rx_msg_r  <= lane(rx_tdata_i, 3'd7) & 8'h0F;
        end
        if (rbeat_r == 3'd3) begin
          rx_req_start_r[47:16] <= {lane(rx_tdata_i, 3'd2), lane(rx_tdata_i, 3'd3),
                                    lane(rx_tdata_i, 3'd4), lane(rx_tdata_i, 3'd5)};
          rx_req_start_r[15:0]  <= {lane(rx_tdata_i, 3'd6), lane(rx_tdata_i, 3'd7)};
        end
        if (rbeat_r == 3'd4) begin
          rx_req_cnt_r          <= {lane(rx_tdata_i, 3'd0), lane(rx_tdata_i, 3'd1)};
          rx_conf_start_r[47:16] <= {lane(rx_tdata_i, 3'd2), lane(rx_tdata_i, 3'd3),
                                     lane(rx_tdata_i, 3'd4), lane(rx_tdata_i, 3'd5)};
          rx_conf_start_r[15:0]  <= {lane(rx_tdata_i, 3'd6), lane(rx_tdata_i, 3'd7)};
        end
        if (rbeat_r == 3'd5)
          rx_conf_cnt_r <= {lane(rx_tdata_i, 3'd0), lane(rx_tdata_i, 3'd1)};
        if (rx_tlast_i) begin
          rbeat_r   <= '0;
          rx_done_p <= is_maap_r && (rbeat_r >= 3'd5) && enable_i;
          is_maap_r <= 1'b0;
        end
      end

      // ---- protocol reactions (one parsed PDU per rx_done_p) --------------
      if (rx_done_p && state_r != IDLE_S) begin
        case (rx_msg_r)
          4'd1: begin  //! PROBE received
            if (conflict_hit(rx_req_start_r, rx_req_cnt_r)) begin
              if (state_r == PROBE_S) begin
                //! both unproven: we yield and re-randomize
                offset_r     <= rand_offset(lfsr_r, count_i);
                probe_left_r <= 8'(PROBE_N_C);
                timer_ms_r   <= probe_iv_w;
                conflicts_o  <= (&conflicts_o) ? conflicts_o : conflicts_o + 8'd1;
              end
              else if (!tx_busy_r) begin
                //! announced: defend the overlap
                {tx_conf_start_r, tx_conf_cnt_r}
                            <= conflict_range(rx_req_start_r, rx_req_cnt_r);
                tx_msg_r    <= 4'd2;
                tx_busy_r   <= 1'b1;
                defends_o   <= (&defends_o) ? defends_o : defends_o + 8'd1;
              end
            end
          end
          4'd2, 4'd3: begin  //! DEFEND / ANNOUNCE received
            //! reference passes the CONFLICT fields of both message types
            if (conflict_hit(rx_conf_start_r, rx_conf_cnt_r)) begin
              offset_r     <= rand_offset(lfsr_r, count_i);
              probe_left_r <= 8'(PROBE_N_C);
              timer_ms_r   <= probe_iv_w;
              state_r      <= PROBE_S;
              conflicts_o  <= (&conflicts_o) ? conflicts_o : conflicts_o + 8'd1;
            end
          end
          default : begin
            //! unknown message type: ignored
          end
        endcase
      end

      // ---- state walk -------------------------------------------------------
      case (state_r)
        IDLE_S : begin
          if (!enable_i) seed_used_r <= 1'b0;   //! re-arm the seed on disable
          if (enable_i) begin
            offset_r     <= new_off_w;
            seed_used_r  <= 1'b1;
            probe_left_r <= 8'(PROBE_N_C);
            timer_ms_r   <= probe_iv_w;
            state_r      <= PROBE_S;
          end
        end

        PROBE_S : begin
          if (!enable_i) state_r <= IDLE_S;
          else if (timer_ms_r == '0 && !tx_busy_r) begin
            tx_msg_r  <= 4'd1;
            tx_busy_r <= 1'b1;
            if (probe_left_r <= 8'd1) begin
              state_r    <= ANNOUNCE_S;
              timer_ms_r <= announce_iv_w;
            end
            else begin
              probe_left_r <= probe_left_r - 8'd1;
              timer_ms_r   <= probe_iv_w;
            end
          end
        end

        ANNOUNCE_S : begin
          if (!enable_i) state_r <= IDLE_S;
          else if (timer_ms_r == '0 && !tx_busy_r) begin
            tx_msg_r   <= 4'd3;
            tx_busy_r  <= 1'b1;
            timer_ms_r <= announce_iv_w;
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
