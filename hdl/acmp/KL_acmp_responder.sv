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
  // Frame capture (little lane: tdata[7:0] = first wire byte)
  // -----------------------------------------------------------------------
  typedef enum logic [1:0] { COLLECT_S, CLASSIFY_S, RESPOND_S } st_t;
  st_t st_r;

  reg [7:0] fbuf [0:NUM_BEATS_C*8-1];   //! 72 B; ACMP frames are exactly 70
  reg [6:0] wr_r;                       //! byte write pointer
  reg       ovfl_r;                     //! frame longer than the buffer

  // -----------------------------------------------------------------------
  // Classification (on the captured frame)
  // -----------------------------------------------------------------------
  wire [47:0] w_dst  = {fbuf[0], fbuf[1], fbuf[2], fbuf[3], fbuf[4], fbuf[5]};
  wire [15:0] w_etype= {fbuf[12], fbuf[13]};
  wire [3:0]  w_msg  = fbuf[15][3:0];
  wire        w_sv0  = (fbuf[15][7:4] == 4'h0);
  wire [63:0] w_talker = {fbuf[34], fbuf[35], fbuf[36], fbuf[37],
                          fbuf[38], fbuf[39], fbuf[40], fbuf[41]};
  wire [15:0] w_tuid = {fbuf[50], fbuf[51]};

  wire w_is_cmd = (w_msg == ACMP_CONNECT_TX_COMMAND_C)    ||
                  (w_msg == ACMP_DISCONNECT_TX_COMMAND_C) ||
                  (w_msg == ACMP_GET_TX_STATE_COMMAND_C)  ||
                  (w_msg == ACMP_GET_TX_CONNECTION_COMMAND_C);

  wire w_hit = enable_i && !ovfl_r &&
               (w_dst == 48'h91E0_F001_0000) && (w_etype == 16'h22F0) &&
               (fbuf[14] == ACMP_SUBTYPE_C) && w_sv0 && w_is_cmd &&
               (w_talker == entity_id_i) && (wr_r >= 7'd70);

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
  // Response byte assembly (combinational over fbuf + latched decision).
  // resp_mode selects the stream-field source; flag_clr_r masks flag bits
  // (the reference clears different sets per message type).
  // -----------------------------------------------------------------------
  logic [7:0] rb [0:NUM_BEATS_C*8-1];
  always_comb begin
    for (int k = 0; k < NUM_BEATS_C*8; k++) rb[k] = 8'h00;
    // dst = echoed ACMP multicast; src = us
    for (int k = 0; k < 6; k++) rb[k] = fbuf[k];
    rb[6]  = station_mac_i[47:40]; rb[7]  = station_mac_i[39:32];
    rb[8]  = station_mac_i[31:24]; rb[9]  = station_mac_i[23:16];
    rb[10] = station_mac_i[15:8];  rb[11] = station_mac_i[7:0];
    rb[12] = 8'h22; rb[13] = 8'hF0;
    rb[14] = ACMP_SUBTYPE_C;
    rb[15] = {4'h0, resp_msg_r};
    rb[16] = {resp_status_r, ACMP_CDL_C[10:8]};
    rb[17] = ACMP_CDL_C[7:0];
    // stream_id (18-25): LIVE -> {station_mac, talker_unique_id} — the
    // stream.c formula (mac<<16|index), byte-identical to the AVTP header
    // aaf_talker_i2s emits; ZERO -> 0; else echo
    unique case (resp_mode_r)
      RESP_LIVE_E: begin
        rb[18] = station_mac_i[47:40]; rb[19] = station_mac_i[39:32];
        rb[20] = station_mac_i[31:24]; rb[21] = station_mac_i[23:16];
        rb[22] = station_mac_i[15:8];  rb[23] = station_mac_i[7:0];
        rb[24] = fbuf[50];             rb[25] = fbuf[51];   // unique_id (be16)
      end
      RESP_ZERO_E: for (int k = 18; k < 26; k++) rb[k] = 8'h00;
      default:     for (int k = 18; k < 26; k++) rb[k] = fbuf[k];
    endcase
    // controller/talker/listener EIDs + unique ids (26-53): echo
    for (int k = 26; k < 54; k++) rb[k] = fbuf[k];
    // stream_dest_mac (54-59): LIVE -> the CSR AAF DMAC (the framer's)
    unique case (resp_mode_r)
      RESP_LIVE_E: begin
        rb[54] = aaf_dmac_i[47:40]; rb[55] = aaf_dmac_i[39:32];
        rb[56] = aaf_dmac_i[31:24]; rb[57] = aaf_dmac_i[23:16];
        rb[58] = aaf_dmac_i[15:8];  rb[59] = aaf_dmac_i[7:0];
      end
      RESP_ZERO_E: begin rb[54]=8'h00; rb[55]=8'h00; rb[56]=8'h00;
                         rb[57]=8'h00; rb[58]=8'h00; rb[59]=8'h00; end
      default:     begin rb[54]=fbuf[54]; rb[55]=fbuf[55]; rb[56]=fbuf[56];
                         rb[57]=fbuf[57]; rb[58]=fbuf[58]; rb[59]=fbuf[59]; end
    endcase
    // connection_count (60-61): ALWAYS 0 from a Milan talker on the
    // SUCCESS paths (reference hard-codes htons(0)); echo on errors
    if (resp_mode_r == RESP_ECHO_E) begin
      rb[60] = fbuf[60]; rb[61] = fbuf[61];
    end else begin
      rb[60] = 8'h00; rb[61] = 8'h00;
    end
    // sequence_id (62-63): echo
    rb[62] = fbuf[62]; rb[63] = fbuf[63];
    // flags (64-65): echo with the per-message clear mask applied
    {rb[64], rb[65]} = {fbuf[64], fbuf[65]} & ~flag_clr_r;
    // stream_vlan_id (66-67): LIVE -> the CSR AAF VID; ZERO -> 0; else echo
    unique case (resp_mode_r)
      RESP_LIVE_E: begin rb[66] = {4'h0, aaf_vid_i[11:8]}; rb[67] = aaf_vid_i[7:0]; end
      RESP_ZERO_E: begin rb[66] = 8'h00; rb[67] = 8'h00; end
      default:     begin rb[66] = fbuf[66]; rb[67] = fbuf[67]; end
    endcase
    rb[68] = fbuf[68]; rb[69] = fbuf[69];
  end

  // -----------------------------------------------------------------------
  // Serialiser (little lane out)
  // -----------------------------------------------------------------------
  reg [3:0] beat_r;
  logic [63:0] w_beat;
  always_comb begin
    for (int l = 0; l < 8; l++)
      w_beat[8*l +: 8] = rb[{beat_r, 3'b000} + l[3:0]];
  end

  assign m_axis_tdata  = w_beat;
  assign m_axis_tvalid = (st_r == RESPOND_S);
  assign m_axis_tlast  = (st_r == RESPOND_S) && (beat_r == NUM_BEATS_C-1);
  assign m_axis_tkeep  = (beat_r == NUM_BEATS_C-1) ? 8'((1 << LAST_KEEP_C) - 1)
                                                   : 8'hFF;

  // -----------------------------------------------------------------------
  // FSM
  // -----------------------------------------------------------------------
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      st_r <= COLLECT_S; wr_r <= '0; ovfl_r <= 1'b0; beat_r <= '0;
      resp_msg_r <= 4'd0; resp_status_r <= 5'd0;
      resp_mode_r <= RESP_ECHO_E; flag_clr_r <= 16'h0;
      probe_armed_o <= 1'b0; probe_tmr_r <= 5'd0;
      cmd_count_o <= 16'd0; resp_count_o <= 16'd0;
      for (int k = 0; k < NUM_BEATS_C*8; k++) fbuf[k] <= 8'h00;
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

      case (st_r)
        COLLECT_S: begin
          if (rxv_r) begin
            for (int l = 0; l < 8; l++) begin
              if (rxk_r[l] && ({1'b0, wr_r} + 8'(l) < 8'(NUM_BEATS_C*8)))
                fbuf[wr_r + 7'(l)] <= rxd_r[8*l +: 8];
            end
            if ({1'b0, wr_r} + 8'(kcount(rxk_r)) > 8'(NUM_BEATS_C*8))
              ovfl_r <= 1'b1;
            wr_r <= ({1'b0, wr_r} + 8'(kcount(rxk_r)) > 8'(NUM_BEATS_C*8))
                    ? 7'(NUM_BEATS_C*8) : wr_r + 7'(kcount(rxk_r));
            if (rxl_r) st_r <= CLASSIFY_S;
          end
        end

        CLASSIFY_S: begin
          if (w_hit) begin
            cmd_count_o   <= cmd_count_o + 16'd1;
            resp_msg_r    <= {w_msg[3:1], 1'b1};          // command+1
            resp_mode_r   <= RESP_ECHO_E;
            flag_clr_r    <= 16'h0;
            unique case (w_msg)
              // Milan PROBE_TX (§4.3.3.1/§5.5.4.1): live params + activate
              ACMP_CONNECT_TX_COMMAND_C: begin
                if (w_tuid == 16'd0) begin
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
                if (w_tuid == 16'd0) begin
                  resp_status_r <= ACMP_STATUS_SUCCESS_C;
                  resp_mode_r   <= RESP_ZERO_E;
                end else begin
                  resp_status_r <= ACMP_STATUS_TALKER_UNKNOWN_ID_C;
                end
              end
              // §5.5.4.3: live params, count=0, three flags cleared
              ACMP_GET_TX_STATE_COMMAND_C: begin
                if (w_tuid == 16'd0) begin
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
            wr_r <= '0; ovfl_r <= 1'b0;
            st_r <= COLLECT_S;
          end
        end

        RESPOND_S: begin
          if (m_axis_tready) begin
            if (beat_r == NUM_BEATS_C-1) begin
              resp_count_o <= resp_count_o + 16'd1;
              wr_r <= '0; ovfl_r <= 1'b0;
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

  //! number of set tkeep bits (contiguous low-aligned keeps assumed)
  function automatic [3:0] kcount(input [7:0] k);
    kcount = 4'(k[0]) + 4'(k[1]) + 4'(k[2]) + 4'(k[3]) +
             4'(k[4]) + 4'(k[5]) + 4'(k[6]) + 4'(k[7]);
  endfunction

endmodule

`default_nettype wire
