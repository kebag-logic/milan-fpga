/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_acmp_tlkr_ctx.sv
//  Project     : Milan ACMP  (IEEE 1722.1-2021 Clause 8, AVnu Milan v1.2 §5.5)
//
//  Description : N-source Milan v1.2 talker-side ACMP — generalizes the
//                proven single-source KL_acmp_responder PROBE_TX activation
//                SM (docs/design/MILAN_TALKER_SM.md) to N_SRC_P SOURCE
//                CONTEXTS (talker_unique_id 0..N-1). Milan talkers stay
//                near-stateless: per context only the probe-freshness
//                window exists (armed + 15 s timer).
//
//                Behaviour per context c (talker_unique_id == c):
//                  CONNECT_TX_COMMAND (PROBE_TX, §5.5.4.1) -> SUCCESS, LIVE
//                    stream params (stream_id = {station MAC, c} — the
//                    tuid tail is echoed, so the LIVE id generalizes for
//                    free; dest_mac/vlan from the per-source config
//                    vectors), count = 0, FAST_CONNECT|STREAMING_WAIT
//                    cleared; arms context c + 15 s window re-arm.
//                  DISCONNECT_TX (§5.5.4.2) -> SUCCESS, zeroed stream
//                    fields, NO state change. GET_TX_STATE (§5.5.4.3) ->
//                    LIVE params, three flags cleared. uid >= N ->
//                    TALKER_UNKNOWN_ID. GET_TX_CONNECTION -> NOT_SUPPORTED
//                    (§5.5.4.4).
//
//                TIMER WHEEL: ONE shared 1 s sweep walks the contexts
//                (1 RMW cycle each) instead of N parallel window counters;
//                the per-context 5-bit timers live in a small table with
//                sync-only write + ONE explicit read port (house RAM
//                rules). armed bits are registers (they are outputs).
//                talker_active_o[c] = armed[c] | listener_observed_i[c].
//
//                N_SRC_P = 1 is bit/byte-identical to KL_acmp_responder
//                (the no-regression axiom); the wrapper instantiates that.
//
//  RX          : MONITOR tap (little lane), inputs only, registered once.
//  TX          : 70-byte response frame via the shared TX arbiter chain.
//---------------------------------------------------------------------------//

`default_nettype none

import acmp_pkg::*;

module KL_acmp_tlkr_ctx #(
    parameter int unsigned N_SRC_P = 1
) (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         enable_i,          //! gate (CSR ADP enable)

    // ---- identity (CSR 0x600 group) -----------------------------------
    input  wire [47:0]  station_mac_i,     //! [47:40] = first wire byte
    input  wire [63:0]  entity_id_i,

    // ---- per-source live stream parameters (context c = slice c) -------
    input  wire [N_SRC_P*48-1:0] src_dmac_i, //! stream dest MAC per source
    input  wire [N_SRC_P*12-1:0] src_vid_i,  //! stream VLAN id per source

    // ---- activation contexts -------------------------------------------
    input  wire                  tick_1s_i,  //! 1 s strobe (shared adp tick)
    input  wire [N_SRC_P-1:0]    listener_observed_i, //! lwSRP hook per src
    output wire [N_SRC_P-1:0]    talker_active_o,     //! armed|observed
    output reg  [N_SRC_P-1:0]    probe_armed_o,       //! probe window open

    // ---- RX monitor tap (MAC RX AXIS, little lane, inputs only) -------
    input  wire         rx_tvalid_i,
    input  wire [63:0]  rx_tdata_i,
    input  wire [7:0]   rx_tkeep_i,
    input  wire         rx_tlast_i,

    // ---- response AXIS master (little lane; -> TX arbiter) ------------
    output logic [63:0] m_axis_tdata,
    output logic [7:0]  m_axis_tkeep,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  wire         m_axis_tready,

    // ---- status --------------------------------------------------------
    output reg  [15:0]  cmd_count_o,       //! ACMP commands accepted
    output reg  [15:0]  resp_count_o       //! responses sent
);

  localparam int NUM_BEATS_C = (ACMP_FRAME_BYTES_C + 7) / 8;            //! 9
  localparam int LAST_KEEP_C = ACMP_FRAME_BYTES_C - (NUM_BEATS_C-1)*8;  //! 6
  localparam int IDX_W_C     = (N_SRC_P > 1) ? $clog2(N_SRC_P) : 1;

  // -----------------------------------------------------------------------
  // Registered tap (zero combinational load on datapath nets)
  // -----------------------------------------------------------------------
  reg        rxv_r, rxl_r;
  reg [63:0] rxd_r;
  reg [7:0]  rxk_r;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      rxv_r <= 1'b0; rxl_r <= 1'b0; rxd_r <= '0; rxk_r <= '0;
    end else begin
      rxv_r <= rx_tvalid_i; rxl_r <= rx_tlast_i;
      rxd_r <= rx_tdata_i;  rxk_r <= rx_tkeep_i;
    end
  end

  // -----------------------------------------------------------------------
  // Frame word buffer — beat-aligned distributed RAM
  // -----------------------------------------------------------------------
  typedef enum logic [1:0] { COLLECT_S, CLASSIFY_S, RESPOND_S } st_t;
  st_t st_r;

  logic [63:0] fword_r [0:NUM_BEATS_C-1];
  reg [3:0]    wbeat_r;                 //! ingest beat, saturating at 9
  reg          ovfl_r;                  //! frame longer than the buffer
  reg          len_ok_r;                //! tlast beat carried >= 70 bytes

  // -----------------------------------------------------------------------
  // Classification captures — fixed beat/lane picks on the registered tap
  // -----------------------------------------------------------------------
  reg        dst_ok_r;                  //! ACMP multicast dst
  reg        hdr_ok_r;                  //! ethertype + subtype + sv
  reg [3:0]  msg_r;
  reg        tk_hi_ok_r, tk_lo_ok_r;    //! talker EID == us (split compare)
  reg [15:0] tuid_r;

  wire w_is_cmd = (msg_r == ACMP_CONNECT_TX_COMMAND_C)    ||
                  (msg_r == ACMP_DISCONNECT_TX_COMMAND_C) ||
                  (msg_r == ACMP_GET_TX_STATE_COMMAND_C)  ||
                  (msg_r == ACMP_GET_TX_CONNECTION_COMMAND_C);

  wire w_hit = enable_i && !ovfl_r && len_ok_r && dst_ok_r && hdr_ok_r &&
               w_is_cmd && tk_hi_ok_r && tk_lo_ok_r;

  //! source-context validity: talker_unique_id addresses a real source
  wire w_uid_valid = (tuid_r < 16'(N_SRC_P));
  wire [IDX_W_C-1:0] w_uid_idx = w_uid_valid ? IDX_W_C'(tuid_r) : '0;

  // decision latched in CLASSIFY_S
  typedef enum logic [1:0] { RESP_ECHO_E, RESP_ZERO_E, RESP_LIVE_E } resp_mode_t;
  reg [3:0]    resp_msg_r;
  reg [4:0]    resp_status_r;
  resp_mode_t  resp_mode_r;    //! stream-field source: echo / zeros / live params
  reg [15:0]   flag_clr_r;     //! flag bits cleared in the response (be16 mask)
  reg [47:0]   live_dmac_r;    //! per-source params latched at CLASSIFY
  reg [11:0]   live_vid_r;

  // ------------------------------------------------------------------------
  // Milan §4.3.3.1 probe activation windows, one per source context; ONE
  // shared 1 s sweep (timer wheel) walks them. Timer table: sync-only
  // write, ONE explicit read port. armed bits are output registers.
  // ------------------------------------------------------------------------
  localparam int PROBE_WINDOW_S_C = 15;
  logic [4:0]         tmr_ram [0:N_SRC_P-1];
  logic               tmr_wr_en_w;
  logic [IDX_W_C-1:0] tmr_wr_idx_w;
  logic [4:0]         tmr_wr_data_w;
  logic [IDX_W_C-1:0] tmr_rd_idx_w;
  logic [4:0]         tmr_rd_w;

  always_ff @(posedge clk_i) begin : tmr_ram_wr   // RAM in its own process
    if (tmr_wr_en_w) tmr_ram[tmr_wr_idx_w] <= tmr_wr_data_w;
  end
  assign tmr_rd_w = tmr_ram[tmr_rd_idx_w];        //! the single read port

  assign talker_active_o = probe_armed_o | listener_observed_i;

  //! sweep sequencer: pending 1 s tick -> walk ctx 0..N-1, 1 cycle each;
  //! yields to the CLASSIFY probe-arm write (retries the same index)
  reg               swp_active_r;
  reg [IDX_W_C-1:0] swp_idx_r;
  reg               s1_pend_r;

  //! CLASSIFY probe-arm write request (uid ctx, tmr := 0)
  wire w_arm_wr = (st_r == CLASSIFY_S) && w_hit &&
                  (msg_r == ACMP_CONNECT_TX_COMMAND_C) && w_uid_valid;

  wire w_swp_run = swp_active_r && !w_arm_wr;

  always_comb begin : tmr_port_mux
    tmr_rd_idx_w = w_swp_run ? swp_idx_r : w_uid_idx;
    if (w_arm_wr) begin
      tmr_wr_en_w   = 1'b1;
      tmr_wr_idx_w  = w_uid_idx;
      tmr_wr_data_w = 5'd0;
    end else begin
      //! sweep RMW: increment while inside the window; at the boundary the
      //! timer holds (window stays lapsed while a listener pins the arm)
      tmr_wr_en_w   = w_swp_run && probe_armed_o[swp_idx_r] &&
                      (tmr_rd_w < 5'(PROBE_WINDOW_S_C - 1));
      tmr_wr_idx_w  = swp_idx_r;
      tmr_wr_data_w = tmr_rd_w + 5'd1;
    end
  end

  // -----------------------------------------------------------------------
  // Response beat: the request word (async RAM read) with fixed per-beat
  // lane overrides. Echoed regions pass straight from the RAM.
  // -----------------------------------------------------------------------
  reg [3:0] beat_r;
  wire [63:0] rword_w = fword_r[beat_r];

  //! stream-field byte per mode: LIVE value / zero / request echo
  function automatic [7:0] sf(input [7:0] live, input [7:0] echo);
    unique case (resp_mode_r)
      RESP_LIVE_E: sf = live;
      RESP_ZERO_E: sf = 8'h00;
      default:     sf = echo;
    endcase
  endfunction

  logic [63:0] w_beat;
  always_comb begin
    w_beat = rword_w;                                   // default: echo
    unique case (beat_r)
      4'd0: begin                                       // bytes 0-7
        w_beat[8*6 +: 8] = station_mac_i[47:40];        // src MAC hi
        w_beat[8*7 +: 8] = station_mac_i[39:32];
      end
      4'd1: begin                                       // bytes 8-15
        w_beat[8*0 +: 8] = station_mac_i[31:24];
        w_beat[8*1 +: 8] = station_mac_i[23:16];
        w_beat[8*2 +: 8] = station_mac_i[15:8];
        w_beat[8*3 +: 8] = station_mac_i[7:0];
        w_beat[8*7 +: 8] = {4'h0, resp_msg_r};
      end
      4'd2: begin                                       // bytes 16-23
        w_beat[8*0 +: 8] = {resp_status_r, ACMP_CDL_C[10:8]};
        w_beat[8*1 +: 8] = ACMP_CDL_C[7:0];
        // stream_id bytes 18-23: LIVE = station MAC ({mac,uid} formula)
        w_beat[8*2 +: 8] = sf(station_mac_i[47:40], rword_w[8*2 +: 8]);
        w_beat[8*3 +: 8] = sf(station_mac_i[39:32], rword_w[8*3 +: 8]);
        w_beat[8*4 +: 8] = sf(station_mac_i[31:24], rword_w[8*4 +: 8]);
        w_beat[8*5 +: 8] = sf(station_mac_i[23:16], rword_w[8*5 +: 8]);
        w_beat[8*6 +: 8] = sf(station_mac_i[15:8],  rword_w[8*6 +: 8]);
        w_beat[8*7 +: 8] = sf(station_mac_i[7:0],   rword_w[8*7 +: 8]);
      end
      4'd3: begin                                       // bytes 24-31
        // stream_id tail = echoed unique_id (LIVE) / zero / echo
        w_beat[8*0 +: 8] = sf(tuid_r[15:8], rword_w[8*0 +: 8]);
        w_beat[8*1 +: 8] = sf(tuid_r[7:0],  rword_w[8*1 +: 8]);
      end
      4'd6: begin                                       // bytes 48-55
        w_beat[8*6 +: 8] = sf(live_dmac_r[47:40], rword_w[8*6 +: 8]);
        w_beat[8*7 +: 8] = sf(live_dmac_r[39:32], rword_w[8*7 +: 8]);
      end
      4'd7: begin                                       // bytes 56-63
        w_beat[8*0 +: 8] = sf(live_dmac_r[31:24], rword_w[8*0 +: 8]);
        w_beat[8*1 +: 8] = sf(live_dmac_r[23:16], rword_w[8*1 +: 8]);
        w_beat[8*2 +: 8] = sf(live_dmac_r[15:8],  rword_w[8*2 +: 8]);
        w_beat[8*3 +: 8] = sf(live_dmac_r[7:0],   rword_w[8*3 +: 8]);
        // connection_count: ALWAYS 0 on the SUCCESS paths (Milan talker);
        // echo on errors
        if (resp_mode_r != RESP_ECHO_E) begin
          w_beat[8*4 +: 8] = 8'h00;
          w_beat[8*5 +: 8] = 8'h00;
        end
        // bytes 62-63 sequence_id: echo
      end
      4'd8: begin                                       // bytes 64-69
        // flags: echo with the per-message clear mask applied
        w_beat[8*0 +: 8] = rword_w[8*0 +: 8] & ~flag_clr_r[15:8];
        w_beat[8*1 +: 8] = rword_w[8*1 +: 8] & ~flag_clr_r[7:0];
        w_beat[8*2 +: 8] = sf({4'h0, live_vid_r[11:8]}, rword_w[8*2 +: 8]);
        w_beat[8*3 +: 8] = sf(live_vid_r[7:0],          rword_w[8*3 +: 8]);
        // bytes 68-69 reserved: echo
      end
      default: ;                                        // beats 4-5: pure echo
    endcase
  end

  assign m_axis_tdata  = w_beat;
  assign m_axis_tvalid = (st_r == RESPOND_S);
  assign m_axis_tlast  = (st_r == RESPOND_S) && (beat_r == 4'(NUM_BEATS_C-1));
  assign m_axis_tkeep  = (beat_r == 4'(NUM_BEATS_C-1)) ? 8'((1 << LAST_KEEP_C) - 1)
                                                       : 8'hFF;

  // -----------------------------------------------------------------------
  // FSM
  // -----------------------------------------------------------------------
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      st_r <= COLLECT_S; wbeat_r <= '0; ovfl_r <= 1'b0; len_ok_r <= 1'b0;
      beat_r <= '0;
      dst_ok_r <= 1'b0; hdr_ok_r <= 1'b0; msg_r <= '0;
      tk_hi_ok_r <= 1'b0; tk_lo_ok_r <= 1'b0; tuid_r <= '0;
      resp_msg_r <= 4'd0; resp_status_r <= 5'd0;
      resp_mode_r <= RESP_ECHO_E; flag_clr_r <= 16'h0;
      live_dmac_r <= '0; live_vid_r <= '0;
      probe_armed_o <= '0;
      swp_active_r <= 1'b0; swp_idx_r <= '0; s1_pend_r <= 1'b0;
      cmd_count_o <= 16'd0; resp_count_o <= 16'd0;
    end else begin
      // ---- shared window sweep (one wheel over all source contexts) ---
      //! a pass starts ON the strobe cycle when idle (first RMW the next
      //! cycle — the original per-tick window update cadence)
      begin : sweep_seq
        logic start;
        start = !swp_active_r && (s1_pend_r || tick_1s_i);
        if (start) begin
          swp_active_r <= 1'b1;
          swp_idx_r    <= '0;
        end else if (w_swp_run) begin
          //! boundary reached with no listener pin -> the arm drops; a
          //! fresh probe below re-arms + zeroes the timer either way
          if (probe_armed_o[swp_idx_r] &&
              (tmr_rd_w >= 5'(PROBE_WINDOW_S_C - 1)) &&
              !listener_observed_i[swp_idx_r])
            probe_armed_o[swp_idx_r] <= 1'b0;
          if (swp_idx_r == IDX_W_C'(N_SRC_P-1)) swp_active_r <= 1'b0;
          else                                  swp_idx_r    <= swp_idx_r + 1'b1;
        end
        s1_pend_r <= (tick_1s_i | s1_pend_r) & ~start;
      end

      //! ALWAYS-ARMED capture (07-18, same fix as the listener): field
      //! captures run through CLASSIFY_S so zero-gap back-to-back frames
      //! are not lost. Capture stays off in RESPOND_S to protect the
      //! fword echo source.
      if (rxv_r && (st_r == COLLECT_S || st_r == CLASSIFY_S)) begin
            if (wbeat_r < 4'(NUM_BEATS_C))
              fword_r[wbeat_r[3:0]] <= rxd_r;
            else
              ovfl_r <= 1'b1;

            //! fresh-frame hygiene: beat 0 clears the previous frame's ovfl
            if (wbeat_r == 4'd0) ovfl_r <= 1'b0;

            // fixed-position classification captures
            unique case (wbeat_r)
              4'd0: begin
                dst_ok_r <= ({rxd_r[7:0],   rxd_r[15:8],  rxd_r[23:16],
                              rxd_r[31:24], rxd_r[39:32], rxd_r[47:40]}
                             == 48'h91E0_F001_0000);
              end
              4'd1: begin
                // bytes 12-15: ethertype, subtype, sv/msg_type
                hdr_ok_r <= ({rxd_r[39:32], rxd_r[47:40]} == 16'h22F0) &&
                            (rxd_r[55:48] == ACMP_SUBTYPE_C) &&
                            (rxd_r[63:60] == 4'h0);
                msg_r <= rxd_r[59:56];
              end
              4'd4: begin   // talker EID bytes 34-39
                tk_hi_ok_r <= ({rxd_r[23:16], rxd_r[31:24], rxd_r[39:32],
                                rxd_r[47:40], rxd_r[55:48], rxd_r[63:56]}
                               == entity_id_i[63:16]);
              end
              4'd5: begin   // talker EID bytes 40-41
                tk_lo_ok_r <= ({rxd_r[7:0], rxd_r[15:8]}
                               == entity_id_i[15:0]);
              end
              4'd6: begin   // talker_unique_id bytes 50-51
                tuid_r <= {rxd_r[23:16], rxd_r[31:24]};
              end
              default: ;
            endcase

            wbeat_r <= (wbeat_r == 4'd9) ? 4'd9 : wbeat_r + 4'd1;
            if (rxl_r) begin
              // >= 70 bytes: 8 full beats + at least 6 tail lanes
              len_ok_r <= (wbeat_r == 4'd8) && rxk_r[5];
              wbeat_r  <= '0;              //! capture owns the beat counter
              if (st_r == COLLECT_S) st_r <= CLASSIFY_S;   // runt-in-classify dropped
            end
      end

      case (st_r)
        COLLECT_S: ;    //! transitions come from the capture block above

        CLASSIFY_S: begin
          if (w_hit) begin
            cmd_count_o   <= cmd_count_o + 16'd1;
            resp_msg_r    <= {msg_r[3:1], 1'b1};          // command+1
            resp_mode_r   <= RESP_ECHO_E;
            flag_clr_r    <= 16'h0;
            //! per-source live params (uid-indexed config slices)
            live_dmac_r   <= src_dmac_i[48*32'(w_uid_idx) +: 48];
            live_vid_r    <= src_vid_i[12*32'(w_uid_idx) +: 12];
            unique case (msg_r)
              // Milan PROBE_TX (§4.3.3.1/§5.5.4.1): live params + activate
              ACMP_CONNECT_TX_COMMAND_C: begin
                if (w_uid_valid) begin
                  resp_status_r <= ACMP_STATUS_SUCCESS_C;
                  resp_mode_r   <= RESP_LIVE_E;
                  flag_clr_r    <= ACMP_FLAG_FAST_CONNECT_C |
                                   ACMP_FLAG_STREAMING_WAIT_C;
                  probe_armed_o[w_uid_idx] <= 1'b1;
                  // context timer zeroed through the table write port
                end else begin
                  resp_status_r <= ACMP_STATUS_TALKER_UNKNOWN_ID_C;
                end
              end
              // §5.5.4.2: always SUCCESS, zeroed fields, NO state change
              ACMP_DISCONNECT_TX_COMMAND_C: begin
                if (w_uid_valid) begin
                  resp_status_r <= ACMP_STATUS_SUCCESS_C;
                  resp_mode_r   <= RESP_ZERO_E;
                end else begin
                  resp_status_r <= ACMP_STATUS_TALKER_UNKNOWN_ID_C;
                end
              end
              // §5.5.4.3: live params, count=0, three flags cleared
              ACMP_GET_TX_STATE_COMMAND_C: begin
                if (w_uid_valid) begin
                  resp_status_r <= ACMP_STATUS_SUCCESS_C;
                  resp_mode_r   <= RESP_LIVE_E;
                  flag_clr_r    <= ACMP_FLAG_FAST_CONNECT_C |
                                   ACMP_FLAG_STREAMING_WAIT_C |
                                   ACMP_FLAG_SRP_REG_FAILED_C;
                end else begin
                  resp_status_r <= ACMP_STATUS_TALKER_UNKNOWN_ID_C;
                end
              end
              // §5.5.4.4: GET_TX_CONNECTION not supported by talkers
              default: resp_status_r <= ACMP_STATUS_NOT_SUPPORTED_C;
            endcase
            beat_r <= '0;
            st_r   <= RESPOND_S;
          end else begin
            st_r <= COLLECT_S;   //! capture owns wbeat/ovfl/len now
          end
        end

        RESPOND_S: begin
          if (m_axis_tready) begin
            if (beat_r == 4'(NUM_BEATS_C-1)) begin
              resp_count_o <= resp_count_o + 16'd1;
              wbeat_r <= '0; ovfl_r <= 1'b0; len_ok_r <= 1'b0;
              st_r <= COLLECT_S;
            end else begin
              beat_r <= beat_r + 4'd1;
            end
          end
        end

        default: st_r <= COLLECT_S;
      endcase
    end
  end

endmodule

`default_nettype wire
