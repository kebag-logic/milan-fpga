/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_acmp_responder.sv
//  Project     : Milan ACMP  (IEEE 1722.1-2021 Clause 8, AVnu Milan v1.2 §5.5)
//
//  Description : Milan v1.2 talker-side ACMP — the PROBE_TX activation state
//                machine (docs/design/MILAN_TALKER_SM.md). Milan talkers are
//                NEAR-STATELESS: no connection table, connection_count is
//                ALWAYS 0 in every response; the only state is the probe
//                freshness window that activates the stream source.
//
//                Behaviour (mirrors pipewire module-avb acmp-milan-v12.c):
//                  CONNECT_TX_COMMAND (== Milan PROBE_TX, §4.3.3.1/§5.5.4.1),
//                  talker_unique_id == 0
//                    -> CONNECT_TX_RESPONSE, SUCCESS, LIVE stream_id/
//                       stream_dest_mac/stream_vlan_id, connection_count = 0,
//                       FAST_CONNECT|STREAMING_WAIT flags cleared; SIDE
//                       EFFECT: probe_armed + 15 s window re-arm.
//                  DISCONNECT_TX_COMMAND, unique_id == 0 (§5.5.4.2)
//                    -> DISCONNECT_TX_RESPONSE, SUCCESS, stream fields ZERO,
//                       NO state change (not even deactivation).
//                  GET_TX_STATE_COMMAND, unique_id == 0 (§5.5.4.3)
//                    -> GET_TX_STATE_RESPONSE, SUCCESS, LIVE stream fields,
//                       count = 0, FAST_CONNECT|STREAMING_WAIT|
//                       SRP_REGISTRATION_FAILED cleared.
//                  any of the above with unique_id != 0 -> TALKER_UNKNOWN_ID.
//                  GET_TX_CONNECTION_COMMAND
//                    -> NOT_SUPPORTED (Milan v1.2 §5.5.4.4: not supported by
//                       talkers).
//                Everything else (responses, RX-side commands, other talkers'
//                commands) is ignored.
//
//                AREA NOTE (2026-07-15, the area-70 config-in-RAM recipe):
//                the original 72-byte REGISTER fbuf with adder-indexed
//                write decode and a full combinational echo array cost
//                ~3.5K LUTs (the aecp-ingress disease). The frame now lives
//                in a 9x64 distributed-RAM word buffer written beat-aligned
//                (one 64-bit write per beat, zero byte decode) and read
//                asynchronously at emit; classification fields are captured
//                into registers at FIXED beat/lane positions on ingest, and
//                the response is the RAM word with fixed per-beat lane
//                overrides. Wire behaviour is byte-identical (pinned by
//                tb/verilator/acmp, 71 checks).
//
//                LIVE stream parameters — single source of truth, MUST match
//                the AVTP frames aaf_talker_i2s emits:
//                  stream_id = {station_mac, talker_unique_id} (stream.c
//                  formula mac<<16|index); dest_mac/vlan = the CSR AAF group.
//
//                Activation (§4.3.3.1): probe -> ARMED + timer := 0; each
//                tick_1s_i counts; at 15 ticks with !listener_observed_i the
//                arm drops. talker_active_o = armed | listener_observed —
//                the AAF gate (listener_observed = the lwSRP registrar hook,
//                CSR-driven until lwSRP lands).
//
//  RX          : MONITOR tap on the post-filter RX stream (little lane,
//                Forencich): inputs only, never backpressures, registered
//                once on entry (same timing recipe as KL_aecp_ingress).
//  TX          : 70-byte response frame, little lane, dst = the ACMP
//                multicast (echoed), src = station MAC. One command in
//                flight; frames arriving while responding are dropped
//                (controllers retry, 200 ms per the reference).
//---------------------------------------------------------------------------//

`default_nettype none

import acmp_pkg::*;

module KL_acmp_responder (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         enable_i,          //! gate (CSR ADP enable)

    // ---- identity (CSR 0x600 group) -----------------------------------
    input  wire [47:0]  station_mac_i,     //! [47:40] = first wire byte
    input  wire [63:0]  entity_id_i,

    // ---- live stream parameters (CSR AAF group — the framer's source) --
    input  wire [47:0]  aaf_dmac_i,        //! stream dest MAC ([47:40] first)
    input  wire [11:0]  aaf_vid_i,         //! stream VLAN id

    // ---- activation state machine --------------------------------------
    input  wire         tick_1s_i,         //! 1 s strobe (shared adp tick)
    input  wire         listener_observed_i, //! lwSRP Listener registrar hook
    output wire         talker_active_o,   //! armed | listener_observed (AAF gate)
    output reg          probe_armed_o,     //! probe seen within the 15 s window

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
  // Frame word buffer — beat-aligned distributed RAM (byte b lives at word
  // b>>3 lane b&7; full-word writes are safe: unkept tail lanes are never
  // emitted, the response is always exactly 70 bytes)
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

  // decision latched in CLASSIFY_S
  typedef enum logic [1:0] { RESP_ECHO_E, RESP_ZERO_E, RESP_LIVE_E } resp_mode_t;
  reg [3:0]    resp_msg_r;
  reg [4:0]    resp_status_r;
  resp_mode_t  resp_mode_r;    //! stream-field source: echo / zeros / live params
  reg [15:0]   flag_clr_r;     //! flag bits cleared in the response (be16 mask)

  // ------------------------------------------------------------------------
  // Milan §4.3.3.1 probe activation window: ARMED by a valid PROBE_TX, held
  // 15 s past the last probe, released only when the window lapses AND no
  // Listener attribute is registered. talker_active gates the AAF framer.
  // ------------------------------------------------------------------------
  localparam int PROBE_WINDOW_S_C = 15;
  reg [4:0] probe_tmr_r;
  assign talker_active_o = probe_armed_o | listener_observed_i;

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
        w_beat[8*6 +: 8] = sf(aaf_dmac_i[47:40], rword_w[8*6 +: 8]);
        w_beat[8*7 +: 8] = sf(aaf_dmac_i[39:32], rword_w[8*7 +: 8]);
      end
      4'd7: begin                                       // bytes 56-63
        w_beat[8*0 +: 8] = sf(aaf_dmac_i[31:24], rword_w[8*0 +: 8]);
        w_beat[8*1 +: 8] = sf(aaf_dmac_i[23:16], rword_w[8*1 +: 8]);
        w_beat[8*2 +: 8] = sf(aaf_dmac_i[15:8],  rword_w[8*2 +: 8]);
        w_beat[8*3 +: 8] = sf(aaf_dmac_i[7:0],   rword_w[8*3 +: 8]);
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
        w_beat[8*2 +: 8] = sf({4'h0, aaf_vid_i[11:8]}, rword_w[8*2 +: 8]);
        w_beat[8*3 +: 8] = sf(aaf_vid_i[7:0],          rword_w[8*3 +: 8]);
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
      probe_armed_o <= 1'b0; probe_tmr_r <= 5'd0;
      cmd_count_o <= 16'd0; resp_count_o <= 16'd0;
    end else begin
      // ---- probe freshness window (independent of the frame FSM) ----
      if (tick_1s_i && probe_armed_o) begin
        if (probe_tmr_r >= 5'(PROBE_WINDOW_S_C - 1)) begin
          if (!listener_observed_i) probe_armed_o <= 1'b0;
          // window stays lapsed but armed while a listener holds it; a
          // fresh probe below resets the timer either way
        end else begin
          probe_tmr_r <= probe_tmr_r + 5'd1;
        end
      end

      //! ALWAYS-ARMED capture (07-18, same fix as KL_acmp_listener): field
      //! captures run through CLASSIFY_S so zero-gap back-to-back frames
      //! are not lost (RX FIFOs drain gapless under DMA stalls). Capture
      //! stays off in RESPOND_S to protect the fword echo source.
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
            unique case (msg_r)
              // Milan PROBE_TX (§4.3.3.1/§5.5.4.1): live params + activate
              ACMP_CONNECT_TX_COMMAND_C: begin
                if (tuid_r == 16'd0) begin
                  resp_status_r <= ACMP_STATUS_SUCCESS_C;
                  resp_mode_r   <= RESP_LIVE_E;
                  flag_clr_r    <= ACMP_FLAG_FAST_CONNECT_C |
                                   ACMP_FLAG_STREAMING_WAIT_C;
                  probe_armed_o <= 1'b1;
                  probe_tmr_r   <= 5'd0;
                end else begin
                  resp_status_r <= ACMP_STATUS_TALKER_UNKNOWN_ID_C;
                end
              end
              // §5.5.4.2: always SUCCESS, zeroed fields, NO state change
              ACMP_DISCONNECT_TX_COMMAND_C: begin
                if (tuid_r == 16'd0) begin
                  resp_status_r <= ACMP_STATUS_SUCCESS_C;
                  resp_mode_r   <= RESP_ZERO_E;
                end else begin
                  resp_status_r <= ACMP_STATUS_TALKER_UNKNOWN_ID_C;
                end
              end
              // §5.5.4.3: live params, count=0, three flags cleared
              ACMP_GET_TX_STATE_COMMAND_C: begin
                if (tuid_r == 16'd0) begin
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
