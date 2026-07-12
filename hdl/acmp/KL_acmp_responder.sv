/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_acmp_responder.sv
//  Project     : Milan ACMP  (IEEE 1722.1-2021 Clause 8, AVnu Milan v1.2 §5.5)
//
//  Description : STATELESS talker-side ACMP responder — the fabric half of
//                the HW/SW delimitation (docs/ARCHITECTURE_HW_SW_SPLIT.md):
//                the fabric answers connection-state queries with zero CPU;
//                connection POLICY (CONNECT/DISCONNECT acceptance) belongs to
//                the softcore and arrives later via a mailbox.
//
//                Behaviour (mirrors pipewire module-avb acmp-milan-v12.c):
//                  GET_TX_STATE_COMMAND, talker_unique_id == 0
//                    -> GET_TX_STATE_RESPONSE, SUCCESS, connection_count = 0,
//                       stream_id / stream_dest_mac / stream_vlan_id = 0 (no
//                       stream configured yet), FAST_CONNECT|STREAMING_WAIT|
//                       SRP_REGISTRATION_FAILED flags cleared.
//                  GET_TX_STATE_COMMAND, unique_id != 0
//                    -> TALKER_UNKNOWN_ID, command body echoed.
//                  GET_TX_CONNECTION_COMMAND
//                    -> NOT_SUPPORTED (Milan v1.2 §5.5.4.4: not supported by
//                       talkers).
//                  CONNECT_TX / DISCONNECT_TX COMMANDs
//                    -> NOT_SUPPORTED until the softcore mailbox increment
//                       (Milan PROBE_TX/fast-connect is SW policy).
//                Everything else (responses, RX-side commands, other talkers'
//                commands) is ignored.
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
  reg [3:0] resp_msg_r;
  reg [4:0] resp_status_r;
  reg       zero_stream_r;   //! zero stream_id/dmac/vlan + count (success path)

  // -----------------------------------------------------------------------
  // Response byte assembly (combinational over fbuf + latched decision)
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
    // stream_id (18-25): success -> ours (none configured = 0); else echo
    for (int k = 18; k < 26; k++) rb[k] = zero_stream_r ? 8'h00 : fbuf[k];
    // controller/talker/listener EIDs + unique ids (26-53): echo
    for (int k = 26; k < 54; k++) rb[k] = fbuf[k];
    // stream_dest_mac (54-59) + connection_count (60-61): success -> 0
    for (int k = 54; k < 62; k++) rb[k] = zero_stream_r ? 8'h00 : fbuf[k];
    // sequence_id (62-63): echo
    rb[62] = fbuf[62]; rb[63] = fbuf[63];
    // flags (64-65): clear FAST_CONNECT|STREAMING_WAIT|SRP_REG_FAILED on
    // the state-response path (reference behaviour), echo otherwise
    if (zero_stream_r) begin
      {rb[64], rb[65]} = {fbuf[64], fbuf[65]} &
                         ~(ACMP_FLAG_FAST_CONNECT_C |
                           ACMP_FLAG_STREAMING_WAIT_C |
                           ACMP_FLAG_SRP_REG_FAILED_C);
    end else begin
      rb[64] = fbuf[64]; rb[65] = fbuf[65];
    end
    // stream_vlan_id (66-67): success -> 0; reserved (68-69): echo
    rb[66] = zero_stream_r ? 8'h00 : fbuf[66];
    rb[67] = zero_stream_r ? 8'h00 : fbuf[67];
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
      resp_msg_r <= 4'd0; resp_status_r <= 5'd0; zero_stream_r <= 1'b0;
      cmd_count_o <= 16'd0; resp_count_o <= 16'd0;
      for (int k = 0; k < NUM_BEATS_C*8; k++) fbuf[k] <= 8'h00;
    end else begin
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
            zero_stream_r <= 1'b0;
            if (w_msg == ACMP_GET_TX_STATE_COMMAND_C) begin
              if (w_tuid == 16'd0) begin
                resp_status_r <= ACMP_STATUS_SUCCESS_C;
                zero_stream_r <= 1'b1;
              end else begin
                resp_status_r <= ACMP_STATUS_TALKER_UNKNOWN_ID_C;
              end
            end else begin
              // GET_TX_CONNECTION (Milan 5.5.4.4) + CONNECT/DISCONNECT_TX
              // (softcore policy, not present yet)
              resp_status_r <= ACMP_STATUS_NOT_SUPPORTED_C;
            end
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
