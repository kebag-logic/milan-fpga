/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_acmp_listener.sv
//  Project     : Milan ACMP  (IEEE 1722.1-2021 Clause 8, AVnu Milan v1.2 §5.5)
//
//  Description : Milan v1.2 LISTENER-side ACMP state machine for ONE sink
//                (STREAM_INPUT[0], listener_unique_id == 0). Contract
//                byte-extracted from pipewire module-avb acmp-milan-v12.c
//                (the normative reference); the SM below implements the
//                INTENDED behaviour where the reference has known typos
//                (each deviation is marked REF-BUG).
//
//                States (acmp_pkg::acmp_lsm_t): UNBOUND -> PRB_W_AVAIL /
//                PRB_W_DELAY / PRB_W_RESP / PRB_W_RESP2 / PRB_W_RETRY ->
//                SETTLED_NO_RSV <-> SETTLED_RSV_OK.
//
//                Frame events (all validated listener_entity_id == us,
//                listener_unique_id == 0):
//                  CONNECT_RX_COMMAND (BIND_RX)   -> store binding
//                    {controller, talker, tuid, flags}; respond SUCCESS
//                    conn_count=1, FAST_CONNECT|SRP_REG_FAILED cleared,
//                    stream fields zero; send PROBE_TX; arm 200 ms.
//                    Rebind to the SAME talker with matching STREAMING_WAIT
//                    -> response only, no state change. Wrong listener EID
//                    -> CONTROLLER_NOT_AUTHORIZED, no state change.
//                  DISCONNECT_RX_COMMAND (UNBIND) -> teardown (withdraw
//                    listener declaration when settled), respond SUCCESS
//                    talker=0/tuid=bound/count=0/SW+FC+SRF cleared.
//                  GET_RX_STATE_COMMAND -> Table 5.37 response: bound =
//                    state != UNBOUND; count = bound; talker EID/UID from
//                    the binding; dest_mac ZEROED (reference); stream_id/
//                    vlan echoed; flags: PRB* = STREAMING_WAIT (+SRP_REG_
//                    FAILED when the TalkerFailed attr is registered),
//                    SETTLED* = stored STREAMING_WAIT only.
//                  CONNECT_TX_RESPONSE (probe answer, in PRB_W_RESP/RESP2)
//                    SUCCESS -> capture stream_id/dest_mac/vlan, activate
//                    (stream_active_o + lstn_declare_o), arm 10 s NO_TK,
//                    -> SETTLED_NO_RSV; error -> 4 s RETRY, status stored.
//
//                Timers: NO_RESP 200 ms (probe ladder #1 -> #2 -> RETRY,
//                #2 timeout stores LISTENER_TALKER_TIMEOUT), RETRY 4 s,
//                NO_TK 10 s, DELAY = LFSR 0..1023 ms.
//                REF-BUG fixes: PRB_W_AVAIL+TK_DISCOVERED goes to
//                PRB_W_DELAY (ref writes PRB_W_RESP with a DELAY timer);
//                PRB_W_RETRY+TMR_RETRY talker-visible branch goes to
//                PRB_W_DELAY (ref stalls in RETRY); UNBIND always sets
//                probing DISABLED.
//
//                ADP watch (same tap): ENTITY_AVAILABLE/DEPARTING from the
//                BOUND talker (entity_id at wire byte 18 — the ADP trap)
//                set/clear tk_avail with a 63 s age-out; edges feed
//                TK_DISCOVERED/TK_DEPARTED.
//
//                SRP hooks (lwSRP TalkerAdvertise registrar on the bound
//                stream_id): ta_registered_i rise = TK_REGISTERED ->
//                SETTLED_RSV_OK; fall = TK_UNREGISTERED -> deactivate +
//                (tk_avail ? PRB_W_DELAY : PRB_W_AVAIL); ta_failed_i rise
//                while settled = reservation lost -> SETTLED_NO_RSV.
//                lstn_declare_o requests the lwSRP Listener attribute
//                (Ready when ta_registered_i else Ready-Failed handled by
//                the lwSRP TX'S lstn_ready_i input).
//
//  RX          : MONITOR tap (little lane), never backpressures; one frame
//                at a time, frames during a response are dropped
//                (controllers retry per the reference).
//  TX          : 70-byte ACMP frames (responses + PROBE_TX commands) via
//                the shared low-rate TX arbiter chain.
//---------------------------------------------------------------------------//

`default_nettype none

import acmp_pkg::*;

module KL_acmp_listener #(
    parameter int unsigned CLK_FREQ_HZ_P = 100_000_000
) (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         enable_i,          //! gate (CSR ADP enable)

    // ---- identity ------------------------------------------------------
    input  wire [47:0]  station_mac_i,     //! [47:40] = first wire byte
    input  wire [63:0]  entity_id_i,

    // ---- ADP age tick ----------------------------------------------------
    input  wire         tick_1s_i,

    // ---- lwSRP listener-side hooks --------------------------------------
    input  wire         ta_registered_i,   //! TalkerAdvertise registered (bound sid)
    input  wire         ta_failed_i,       //! TalkerFailed registered (bound sid)
    output wire         lstn_declare_o,    //! declare the MSRP Listener attribute
    output wire [63:0]  bound_sid_o,       //! bound stream_id (walker compare)
    output wire [11:0]  stream_vlan_o,     //! from the talker's probe response
    output wire [47:0]  stream_dmac_o,
    output wire         stream_active_o,   //! sink open (SETTLED_*)

    // ---- RX monitor tap (MAC RX AXIS, little lane, inputs only) -------
    input  wire         rx_tvalid_i,
    input  wire [63:0]  rx_tdata_i,
    input  wire [7:0]   rx_tkeep_i,
    input  wire         rx_tlast_i,

    // ---- TX AXIS master (little lane; -> TX arbiter) -------------------
    output logic [63:0] m_axis_tdata,
    output logic [7:0]  m_axis_tkeep,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  wire         m_axis_tready,

    // ---- status (CSR RO) -------------------------------------------------
    output acmp_lsm_t   state_o,
    output wire [63:0]  bound_talker_o,
    output wire [15:0]  bound_tuid_o,
    output reg  [4:0]   acmp_status_o,     //! last probe status / timeout
    output reg  [1:0]   probing_o,         //! 0 dis / 1 passive / 2 active / 3 done
    output reg          tk_avail_o,        //! bound talker ADP-visible
    output reg  [15:0]  cmd_count_o,       //! listener commands accepted
    output reg  [15:0]  probe_count_o      //! PROBE_TX commands sent
);

  localparam int NUM_BEATS_C = (ACMP_FRAME_BYTES_C + 7) / 8;            //! 9
  localparam int LAST_KEEP_C = ACMP_FRAME_BYTES_C - (NUM_BEATS_C-1)*8;  //! 6

  // -----------------------------------------------------------------------
  // 1 ms tick (timer base) + LFSR for the random DELAY
  // -----------------------------------------------------------------------
  localparam int unsigned MS_DIV_C = CLK_FREQ_HZ_P / 1000;
  reg [$clog2(MS_DIV_C)-1:0] ms_div_r;
  reg                        tick_1ms_r;
  reg [15:0]                 lfsr_r;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      ms_div_r <= '0; tick_1ms_r <= 1'b0; lfsr_r <= 16'hACE1;
    end else begin
      tick_1ms_r <= 1'b0;
      lfsr_r     <= {lfsr_r[14:0], lfsr_r[15] ^ lfsr_r[13] ^ lfsr_r[12] ^ lfsr_r[10]};
      if (ms_div_r == ($clog2(MS_DIV_C))'(MS_DIV_C - 1)) begin
        ms_div_r   <= '0;
        tick_1ms_r <= 1'b1;
      end else begin
        ms_div_r <= ms_div_r + 1'b1;
      end
    end
  end

  // -----------------------------------------------------------------------
  // Listener SM registers
  // -----------------------------------------------------------------------
  acmp_lsm_t st_lsm_r;
  assign state_o = st_lsm_r;

  reg [63:0] bnd_ctlr_r, bnd_talker_r;
  reg [15:0] bnd_tuid_r, bnd_flags_r;
  reg [63:0] sid_r;
  reg [47:0] dmac_r;
  reg [11:0] vlan_r;
  reg        active_r;        //! stream activated (probe completed)
  reg [15:0] probe_seq_r;

  assign bound_talker_o  = bnd_talker_r;
  assign bound_tuid_o    = bnd_tuid_r;
  assign bound_sid_o     = sid_r;
  assign stream_vlan_o   = vlan_r;
  assign stream_dmac_o   = dmac_r;
  assign stream_active_o = active_r;
  //! declare the Listener attribute while activated (Ready vs Ready-Failed
  //! is selected downstream from ta_registered_i)
  assign lstn_declare_o  = active_r;

  //! single running timer (one outstanding per state by construction)
  reg [13:0] tmr_r;           //! ms remaining; 0 = disarmed
  wire       w_tmr_fire = tick_1ms_r && (tmr_r == 14'd1);

  //! ADP availability aging
  reg [6:0]  adp_age_r;

  //! SRP edges
  reg ta_reg_prev_r, ta_fail_prev_r;

  //! ADP discovered/departed event pulses (registered from CLASSIFY_S,
  //! consumed by the SM block one cycle later)
  reg adp_discovered_p, adp_departed_p;

  //! MSRP stream_id from {talker EID, uid} — the reference
  //! peer_id_from_entity_id: EUI-64 with the FF:FE marker rebuilds the MAC
  //! (drop bytes 3-4), plain MAC|index EIDs just swap the low 16 bits.
  //! Provisional until the probe response supplies the authoritative id.
  function automatic [63:0] sid_from_eid(input [63:0] eid, input [15:0] uid);
    if (eid[39:24] == 16'hFFFE)
      sid_from_eid = {eid[63:40], eid[23:0], uid};
    else
      sid_from_eid = {eid[63:16], uid};
  endfunction

  // -----------------------------------------------------------------------
  // Frame capture (identical recipe to KL_acmp_responder)
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

  typedef enum logic [1:0] { COLLECT_S, CLASSIFY_S, RESPOND_S, PROBE_S } st_t;
  st_t st_r;

  reg [7:0] fbuf [0:NUM_BEATS_C*8-1];
  reg [6:0] wr_r;
  reg       ovfl_r;

  // -----------------------------------------------------------------------
  // Classification
  // -----------------------------------------------------------------------
  wire [47:0] w_dst   = {fbuf[0], fbuf[1], fbuf[2], fbuf[3], fbuf[4], fbuf[5]};
  wire [15:0] w_etype = {fbuf[12], fbuf[13]};
  wire [3:0]  w_msg   = fbuf[15][3:0];
  wire        w_sv0   = (fbuf[15][7:4] == 4'h0);
  wire [4:0]  w_status= fbuf[16][7:3];
  wire [63:0] w_sid   = {fbuf[18], fbuf[19], fbuf[20], fbuf[21],
                         fbuf[22], fbuf[23], fbuf[24], fbuf[25]};
  wire [63:0] w_ctlr  = {fbuf[26], fbuf[27], fbuf[28], fbuf[29],
                         fbuf[30], fbuf[31], fbuf[32], fbuf[33]};
  wire [63:0] w_talker= {fbuf[34], fbuf[35], fbuf[36], fbuf[37],
                         fbuf[38], fbuf[39], fbuf[40], fbuf[41]};
  wire [63:0] w_lstnr = {fbuf[42], fbuf[43], fbuf[44], fbuf[45],
                         fbuf[46], fbuf[47], fbuf[48], fbuf[49]};
  wire [15:0] w_tuid  = {fbuf[50], fbuf[51]};
  wire [15:0] w_luid  = {fbuf[52], fbuf[53]};
  wire [15:0] w_flags = {fbuf[64], fbuf[65]};

  wire w_acmp_base = enable_i && !ovfl_r &&
                     (w_dst == 48'h91E0_F001_0000) && (w_etype == 16'h22F0) &&
                     (fbuf[14] == ACMP_SUBTYPE_C) && w_sv0 && (wr_r >= 7'd70);

  wire w_is_lstn_cmd = (w_msg == ACMP_CONNECT_RX_COMMAND_C)    ||
                       (w_msg == ACMP_DISCONNECT_RX_COMMAND_C) ||
                       (w_msg == ACMP_GET_RX_STATE_COMMAND_C);
  //! listener commands for us (EID mismatch still answered NOT_AUTHORIZED
  //! only when the LISTENER EID matches us is it "accessible"; commands
  //! addressed to other listeners are ignored — the reference gates on
  //! listener_guid == entity_id at acmp.c:188 before dispatch, and inside
  //! handlers answers CONTROLLER_NOT_AUTHORIZED when it mismatches. In
  //! fabric we answer NOT_AUTHORIZED only if the frame's listener EID is
  //! ours-with-wrong-uid; frames for other entities are dropped.)
  wire w_lstn_hit = w_acmp_base && w_is_lstn_cmd && (w_lstnr == entity_id_i);
  wire w_uid_ok   = (w_luid == 16'd0);

  //! probe answer: CONNECT_TX_RESPONSE addressed to us as listener
  wire w_probe_resp = w_acmp_base && (w_msg == ACMP_CONNECT_TX_RESPONSE_C) &&
                      (w_lstnr == entity_id_i) && (w_luid == 16'd0) &&
                      (st_lsm_r == LSM_PRB_W_RESP_S || st_lsm_r == LSM_PRB_W_RESP2_S);

  //! ADP watch: available/departing from the bound talker (byte 18 trap)
  wire [63:0] w_adp_eid = {fbuf[18], fbuf[19], fbuf[20], fbuf[21],
                           fbuf[22], fbuf[23], fbuf[24], fbuf[25]};
  wire w_adp_frame = enable_i && (w_etype == 16'h22F0) && (fbuf[14] == 8'hFA) &&
                     (wr_r >= 7'd26) && (st_lsm_r != LSM_UNBOUND_S) &&
                     (w_adp_eid == bnd_talker_r);
  wire w_adp_avail  = w_adp_frame && (fbuf[15][3:0] == 4'd0);
  wire w_adp_depart = w_adp_frame && (fbuf[15][3:0] == 4'd1);

  //! rebind-to-same fast path: same talker + STREAMING_WAIT agreement
  wire w_same_talker = (w_talker == bnd_talker_r) && (w_tuid == bnd_tuid_r);
  wire w_flags_match = ((bnd_flags_r & w_flags & ACMP_FLAG_STREAMING_WAIT_C) != 16'd0)
                       || ((bnd_flags_r | w_flags) & ACMP_FLAG_STREAMING_WAIT_C) == 16'd0;

  // -----------------------------------------------------------------------
  // Response / probe frame assembly
  // -----------------------------------------------------------------------
  typedef enum logic [1:0] { L_RESP_BIND_E, L_RESP_UNBIND_E, L_RESP_STATE_E } lresp_t;
  reg [3:0]   resp_msg_r;
  reg [4:0]   resp_status_r;
  lresp_t     resp_kind_r;
  reg         probe_pend_r;     //! send a PROBE_TX after the current response

  logic [7:0] rb [0:NUM_BEATS_C*8-1];
  always_comb begin
    for (int k = 0; k < NUM_BEATS_C*8; k++) rb[k] = 8'h00;
    if (st_r == PROBE_S) begin
      // ---- PROBE_TX command (reference prepare_probe_tx_command_success):
      // stream fields zero, controller/talker from the binding, us as
      // listener, fresh sequence id, STREAMING_WAIT|SRP_REG_FAILED cleared.
      rb[0]=8'h91; rb[1]=8'hE0; rb[2]=8'hF0; rb[3]=8'h01; rb[4]=8'h00; rb[5]=8'h00;
      rb[6]  = station_mac_i[47:40]; rb[7]  = station_mac_i[39:32];
      rb[8]  = station_mac_i[31:24]; rb[9]  = station_mac_i[23:16];
      rb[10] = station_mac_i[15:8];  rb[11] = station_mac_i[7:0];
      rb[12] = 8'h22; rb[13] = 8'hF0;
      rb[14] = ACMP_SUBTYPE_C;
      rb[15] = {4'h0, ACMP_CONNECT_TX_COMMAND_C};
      rb[16] = {ACMP_STATUS_SUCCESS_C, ACMP_CDL_C[10:8]};
      rb[17] = ACMP_CDL_C[7:0];
      for (int k = 0; k < 8; k++) begin
        rb[26+k] = bnd_ctlr_r[8*(7-k) +: 8];
        rb[34+k] = bnd_talker_r[8*(7-k) +: 8];
        rb[42+k] = entity_id_i[8*(7-k) +: 8];
      end
      rb[50] = bnd_tuid_r[15:8]; rb[51] = bnd_tuid_r[7:0];
      rb[52] = 8'h00; rb[53] = 8'h00;                    // listener_unique_id 0
      rb[62] = probe_seq_r[15:8]; rb[63] = probe_seq_r[7:0];
      {rb[64], rb[65]} = bnd_flags_r &
                         ~(ACMP_FLAG_STREAMING_WAIT_C | ACMP_FLAG_SRP_REG_FAILED_C);
    end else begin
      // ---- responses: echo the command then overwrite per kind ----------
      for (int k = 0; k < ACMP_FRAME_BYTES_C; k++) rb[k] = fbuf[k];
      rb[6]  = station_mac_i[47:40]; rb[7]  = station_mac_i[39:32];
      rb[8]  = station_mac_i[31:24]; rb[9]  = station_mac_i[23:16];
      rb[10] = station_mac_i[15:8];  rb[11] = station_mac_i[7:0];
      rb[15] = {4'h0, resp_msg_r};
      rb[16] = {resp_status_r, ACMP_CDL_C[10:8]};
      rb[17] = ACMP_CDL_C[7:0];
      unique case (resp_kind_r)
        // Table 5.32: count=1, FC+SRF cleared, stream fields zero
        L_RESP_BIND_E: begin
          for (int k = 18; k < 26; k++) rb[k] = 8'h00;
          for (int k = 54; k < 60; k++) rb[k] = 8'h00;
          rb[60] = 8'h00; rb[61] = 8'h01;
          {rb[64], rb[65]} = w_flags &
              ~(ACMP_FLAG_FAST_CONNECT_C | ACMP_FLAG_SRP_REG_FAILED_C);
          rb[66] = 8'h00; rb[67] = 8'h00;
        end
        // Table 5.36: talker=0, tuid=bound, count=0, SW+FC+SRF cleared,
        // stream fields zero
        L_RESP_UNBIND_E: begin
          for (int k = 18; k < 26; k++) rb[k] = 8'h00;
          for (int k = 34; k < 42; k++) rb[k] = 8'h00;
          rb[50] = bnd_tuid_r[15:8]; rb[51] = bnd_tuid_r[7:0];
          for (int k = 54; k < 60; k++) rb[k] = 8'h00;
          rb[60] = 8'h00; rb[61] = 8'h00;
          {rb[64], rb[65]} = w_flags &
              ~(ACMP_FLAG_STREAMING_WAIT_C | ACMP_FLAG_FAST_CONNECT_C |
                ACMP_FLAG_SRP_REG_FAILED_C);
          rb[66] = 8'h00; rb[67] = 8'h00;
        end
        // Table 5.37: talker/tuid from the binding, count=bound, dest_mac
        // ZEROED, stream_id/vlan echoed, per-state flags
        default: begin
          for (int k = 0; k < 8; k++)
            rb[34+k] = (st_lsm_r == LSM_UNBOUND_S) ? 8'h00
                                                   : bnd_talker_r[8*(7-k) +: 8];
          rb[50] = bnd_tuid_r[15:8]; rb[51] = bnd_tuid_r[7:0];
          for (int k = 54; k < 60; k++) rb[k] = 8'h00;
          rb[60] = 8'h00;
          rb[61] = (st_lsm_r == LSM_UNBOUND_S) ? 8'h00 : 8'h01;
          if (st_lsm_r == LSM_UNBOUND_S) begin
            {rb[64], rb[65]} = 16'h0000;
          end else if (st_lsm_r == LSM_SETTLED_NO_RSV_S ||
                       st_lsm_r == LSM_SETTLED_RSV_OK_S) begin
            {rb[64], rb[65]} = bnd_flags_r & ACMP_FLAG_STREAMING_WAIT_C;
          end else begin
            {rb[64], rb[65]} = ACMP_FLAG_STREAMING_WAIT_C |
                               (ta_failed_i ? ACMP_FLAG_SRP_REG_FAILED_C : 16'h0);
          end
        end
      endcase
    end
  end

  // -----------------------------------------------------------------------
  // Serialiser
  // -----------------------------------------------------------------------
  reg [3:0] beat_r;
  logic [63:0] w_beat;
  always_comb begin
    for (int l = 0; l < 8; l++)
      w_beat[8*l +: 8] = rb[{beat_r, 3'b000} + l[3:0]];
  end
  assign m_axis_tdata  = w_beat;
  assign m_axis_tvalid = (st_r == RESPOND_S) || (st_r == PROBE_S);
  assign m_axis_tlast  = m_axis_tvalid && (beat_r == NUM_BEATS_C-1);
  assign m_axis_tkeep  = (beat_r == NUM_BEATS_C-1) ? 8'((1 << LAST_KEEP_C) - 1)
                                                   : 8'hFF;

  // -----------------------------------------------------------------------
  // Helper tasks (SM actions)
  // -----------------------------------------------------------------------
  task automatic do_deactivate;
    begin
      active_r <= 1'b0;   // withdraws lstn_declare_o (lwSRP sends Lv)
    end
  endtask

  task automatic do_full_bind;   //! store the whole binding (UNBOUND path)
    begin
      bnd_ctlr_r   <= w_ctlr;
      bnd_talker_r <= w_talker;
      bnd_tuid_r   <= w_tuid;
      bnd_flags_r  <= w_flags;
      sid_r        <= sid_from_eid(w_talker, w_tuid);
      acmp_status_o <= 5'd0;
      probing_o     <= 2'd2;      // ACTIVE
    end
  endtask

  task automatic do_rebind;      //! non-UNBOUND rebind (ctlr+sid+SW flag)
    begin
      bnd_ctlr_r   <= w_ctlr;
      bnd_talker_r <= w_talker;
      bnd_tuid_r   <= w_tuid;
      bnd_flags_r  <= (bnd_flags_r & ~ACMP_FLAG_STREAMING_WAIT_C) |
                      (w_flags & ACMP_FLAG_STREAMING_WAIT_C);
      sid_r        <= sid_from_eid(w_talker, w_tuid);
      probing_o    <= 2'd2;
    end
  endtask

  task automatic do_unbind;
    begin
      bnd_ctlr_r   <= 64'd0;
      bnd_talker_r <= 64'd0;
      bnd_tuid_r   <= 16'd0;
      bnd_flags_r  <= 16'd0;
      sid_r        <= 64'd0;
      dmac_r       <= 48'd0;
      vlan_r       <= 12'd0;
      probing_o    <= 2'd0;       // DISABLED (REF-BUG 3 fixed: always)
      acmp_status_o <= 5'd0;
      tmr_r        <= 14'd0;
      do_deactivate();
      st_lsm_r     <= LSM_UNBOUND_S;
    end
  endtask

  //! arm helpers (ms)
  task automatic arm(input [13:0] ms);
    tmr_r <= ms;
  endtask
  task automatic arm_delay;      //! randomized 0..1023 ms (never 0 = off)
    tmr_r <= {4'd0, lfsr_r[9:0]} + 14'd1;
  endtask

  // -----------------------------------------------------------------------
  // Main FSM
  // -----------------------------------------------------------------------
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      st_r <= COLLECT_S; wr_r <= '0; ovfl_r <= 1'b0; beat_r <= '0;
      st_lsm_r <= LSM_UNBOUND_S;
      resp_msg_r <= 4'd0; resp_status_r <= 5'd0; resp_kind_r <= L_RESP_STATE_E;
      probe_pend_r <= 1'b0;
      bnd_ctlr_r <= 64'd0; bnd_talker_r <= 64'd0;
      bnd_tuid_r <= 16'd0; bnd_flags_r <= 16'd0;
      sid_r <= 64'd0; dmac_r <= 48'd0; vlan_r <= 12'd0;
      active_r <= 1'b0; probe_seq_r <= 16'd0;
      tmr_r <= 14'd0; adp_age_r <= 7'd0; tk_avail_o <= 1'b0;
      ta_reg_prev_r <= 1'b0; ta_fail_prev_r <= 1'b0;
      acmp_status_o <= 5'd0; probing_o <= 2'd0;
      cmd_count_o <= 16'd0; probe_count_o <= 16'd0;
      for (int k = 0; k < NUM_BEATS_C*8; k++) fbuf[k] <= 8'h00;
    end else begin
      // ---- timer countdown -------------------------------------------
      if (tick_1ms_r && tmr_r != 14'd0) tmr_r <= tmr_r - 14'd1;

      // ---- ADP availability aging -------------------------------------
      if (tick_1s_i && tk_avail_o) begin
        if (adp_age_r >= LSM_ADP_AGE_S_C) tk_avail_o <= 1'b0;
        else                              adp_age_r  <= adp_age_r + 7'd1;
      end

      // ---- SRP edges ----------------------------------------------------
      ta_reg_prev_r  <= ta_registered_i;
      ta_fail_prev_r <= ta_failed_i;

      // ================= listener SM: non-frame events ==================
      // (frame events are applied in CLASSIFY_S below; simultaneous frame
      // handling wins — a stale timer after a transition is a no-op, the
      // reference's rule)
      if (st_r == COLLECT_S || st_r == RESPOND_S || st_r == PROBE_S) begin
        unique case (st_lsm_r)
          LSM_PRB_W_DELAY_S: begin
            if (w_tmr_fire) begin
              probe_pend_r <= 1'b1;             // send probe, arm in PROBE_S
              probing_o    <= 2'd2;
              st_lsm_r     <= LSM_PRB_W_RESP_S;
            end else if (adp_departed_p) begin
              tmr_r    <= 14'd0;
              probing_o<= 2'd1;                 // PASSIVE
              st_lsm_r <= LSM_PRB_W_AVAIL_S;
            end
          end
          LSM_PRB_W_AVAIL_S: begin
            if (adp_discovered_p) begin
              arm_delay();                      // REF-BUG 1 fixed: -> DELAY
              probing_o <= 2'd2;
              st_lsm_r  <= LSM_PRB_W_DELAY_S;
            end
          end
          LSM_PRB_W_RESP_S: begin
            if (w_tmr_fire) begin
              probe_pend_r <= 1'b1;             // resend
              st_lsm_r     <= LSM_PRB_W_RESP2_S;
            end else if (adp_departed_p) begin
              tmr_r <= 14'd0; probing_o <= 2'd1;
              st_lsm_r <= LSM_PRB_W_AVAIL_S;
            end
          end
          LSM_PRB_W_RESP2_S: begin
            if (w_tmr_fire) begin
              arm(LSM_TMR_RETRY_MS_C);
              acmp_status_o <= ACMP_STATUS_LSTN_TALKER_TIMEOUT_C;
              st_lsm_r      <= LSM_PRB_W_RETRY_S;
            end else if (adp_departed_p) begin
              tmr_r <= 14'd0; probing_o <= 2'd1;
              st_lsm_r <= LSM_PRB_W_AVAIL_S;
            end
          end
          LSM_PRB_W_RETRY_S: begin
            if (w_tmr_fire) begin
              // REF-BUG 2 fixed: both branches leave RETRY; visible talker
              // re-delays, invisible talker waits for ADP.
              if (tk_avail_o) begin
                arm_delay();
                probing_o <= 2'd2;
                st_lsm_r  <= LSM_PRB_W_DELAY_S;
              end else begin
                probing_o <= 2'd1;
                st_lsm_r  <= LSM_PRB_W_AVAIL_S;
              end
            end else if (adp_departed_p) begin
              tmr_r <= 14'd0; probing_o <= 2'd1;
              st_lsm_r <= LSM_PRB_W_AVAIL_S;
            end
          end
          LSM_SETTLED_NO_RSV_S: begin
            if (ta_registered_i && !ta_reg_prev_r) begin
              tmr_r    <= 14'd0;                // remove NO_TK
              active_r <= 1'b1;
              st_lsm_r <= LSM_SETTLED_RSV_OK_S;
            end else if (w_tmr_fire) begin      // NO_TK lapsed
              if (tk_avail_o) begin
                arm_delay(); probing_o <= 2'd2;
                st_lsm_r <= LSM_PRB_W_DELAY_S;
              end else begin
                probing_o <= 2'd1;
                st_lsm_r  <= LSM_PRB_W_AVAIL_S;
              end
            end
          end
          LSM_SETTLED_RSV_OK_S: begin
            if (!ta_registered_i && ta_reg_prev_r) begin
              do_deactivate();
              if (tk_avail_o) begin
                arm_delay(); probing_o <= 2'd2;
                st_lsm_r <= LSM_PRB_W_DELAY_S;
              end else begin
                probing_o <= 2'd1;
                st_lsm_r  <= LSM_PRB_W_AVAIL_S;
              end
            end else if (ta_failed_i && !ta_fail_prev_r) begin
              // reservation degraded to TalkerFailed -> re-establishable
              st_lsm_r <= LSM_SETTLED_NO_RSV_S;
            end
          end
          default: ;   // UNBOUND: nothing time-driven
        endcase
      end

      // ================= frame engine ===================================
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
          end else if (probe_pend_r) begin
            probe_pend_r  <= 1'b0;
            probe_count_o <= probe_count_o + 16'd1;
            arm(LSM_TMR_NO_RESP_MS_C);
            beat_r <= '0;
            st_r   <= PROBE_S;
          end
        end

        CLASSIFY_S: begin
          // ---- ADP watch (no response, just availability tracking) -----
          if (w_adp_avail) begin
            tk_avail_o <= 1'b1;
            adp_age_r  <= 7'd0;
          end else if (w_adp_depart) begin
            tk_avail_o <= 1'b0;
          end

          if (w_lstn_hit) begin
            cmd_count_o   <= cmd_count_o + 16'd1;
            resp_msg_r    <= {w_msg[3:1], 1'b1};
            resp_status_r <= ACMP_STATUS_SUCCESS_C;
            unique case (w_msg)
              // ---------------- BIND_RX --------------------------------
              ACMP_CONNECT_RX_COMMAND_C: begin
                resp_kind_r <= L_RESP_BIND_E;
                if (!w_uid_ok) begin
                  resp_status_r <= ACMP_STATUS_LISTENER_UNKNOWN_ID_C;
                end else if (st_lsm_r != LSM_UNBOUND_S &&
                             w_same_talker && w_flags_match) begin
                  // rebind-same fast path: response only, no state change
                end else begin
                  if (st_lsm_r == LSM_UNBOUND_S) do_full_bind();
                  else                           do_rebind();
                  if (st_lsm_r == LSM_SETTLED_NO_RSV_S ||
                      st_lsm_r == LSM_SETTLED_RSV_OK_S)
                    do_deactivate();
                  probe_pend_r <= 1'b1;   // PROBE after the response drains
                  tmr_r        <= 14'd0;  // NO_RESP re-armed in PROBE_S
                  st_lsm_r     <= LSM_PRB_W_RESP_S;
                end
              end
              // ---------------- UNBIND_RX ------------------------------
              ACMP_DISCONNECT_RX_COMMAND_C: begin
                resp_kind_r <= L_RESP_UNBIND_E;
                if (!w_uid_ok) begin
                  resp_status_r <= ACMP_STATUS_LISTENER_UNKNOWN_ID_C;
                end else begin
                  do_unbind();
                end
              end
              // ---------------- GET_RX_STATE ---------------------------
              default: begin
                resp_kind_r <= L_RESP_STATE_E;
                if (!w_uid_ok) resp_status_r <= ACMP_STATUS_LISTENER_UNKNOWN_ID_C;
              end
            endcase
            beat_r <= '0;
            st_r   <= RESPOND_S;
          end else if (w_probe_resp) begin
            // ---------------- probe answer -----------------------------
            tmr_r <= 14'd0;   // remove NO_RESP
            if (w_status == ACMP_STATUS_SUCCESS_C) begin
              sid_r    <= w_sid;
              dmac_r   <= {fbuf[54], fbuf[55], fbuf[56],
                           fbuf[57], fbuf[58], fbuf[59]};
              vlan_r   <= {fbuf[66][3:0], fbuf[67]};
              active_r <= 1'b1;
              probing_o <= 2'd3;          // COMPLETED
              acmp_status_o <= 5'd0;
              arm(LSM_TMR_NO_TK_MS_C);
              st_lsm_r <= LSM_SETTLED_NO_RSV_S;
            end else begin
              acmp_status_o <= w_status;
              arm(LSM_TMR_RETRY_MS_C);
              st_lsm_r <= LSM_PRB_W_RETRY_S;
            end
            wr_r <= '0; ovfl_r <= 1'b0;
            st_r <= COLLECT_S;
          end else begin
            wr_r <= '0; ovfl_r <= 1'b0;
            st_r <= COLLECT_S;
          end
        end

        RESPOND_S, PROBE_S: begin
          if (m_axis_tready) begin
            if (beat_r == NUM_BEATS_C-1) begin
              // post-increment the probe sequence per emission (reference
              // prepare_probe_tx_command_success: send seq, then ++)
              if (st_r == PROBE_S) probe_seq_r <= probe_seq_r + 16'd1;
              wr_r <= '0; ovfl_r <= 1'b0;
              beat_r <= '0;
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

  //! ADP event pulses derive from the frame classification (one cycle later)
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      adp_discovered_p <= 1'b0;
      adp_departed_p   <= 1'b0;
    end else begin
      adp_discovered_p <= (st_r == CLASSIFY_S) && w_adp_avail && !tk_avail_o;
      adp_departed_p   <= (st_r == CLASSIFY_S) && w_adp_depart && tk_avail_o;
    end
  end

  //! number of set tkeep bits (contiguous low-aligned keeps assumed)
  function automatic [3:0] kcount(input [7:0] k);
    kcount = 4'(k[0]) + 4'(k[1]) + 4'(k[2]) + 4'(k[3]) +
             4'(k[4]) + 4'(k[5]) + 4'(k[6]) + 4'(k[7]);
  endfunction

endmodule

`default_nettype wire
