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
    output wire [31:0]  dbg_o,             //! live walker forensics (07-18
                                           //! silicon deafness): {classify_cnt,
                                           //! fc_cnt, fc_flags, base_hits}
    output reg  [7:0]   tx_wedge_cnt_o,    //! responses abandoned: TX grant
                                           //! never came (silicon 07-18: the
                                           //! listener wedged in RESPOND_S
                                           //! after ~2 cmds; watchdog frees
                                           //! it - ACMP is retransmit-safe)
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
  //! walker forensics: where do ACMP frames die on silicon?
  logic [7:0] dbg_classify_r;   //! CLASSIFY entries (any frame)
  logic [7:0] dbg_fc_r;         //! CLASSIFY of subtype-0xFC frames
  logic [7:0] dbg_flags_r;      //! at last FC classify: {dst,etype,sv0,len,
                                //! ovfl,lstnr_hi,lstnr_lo,is_lstn_cmd}
  logic [7:0] dbg_basehit_r;    //! w_acmp_base && is_lstn_cmd hits
  //! TX-grant watchdog: ~10 ms @100 MHz (21 ms @50 MHz) - a healthy grant
  //! arrives in microseconds; expiry = arbiter wedge, abandon the frame
  localparam logic [19:0] TXWD_MAX_C = 20'hFFFFF;
  logic [19:0] txwd_r;
  st_t st_r;

  // ---- frame word buffer: beat-aligned distributed RAM (the area-70
  //      config-in-RAM recipe — the old 72-byte register fbuf with
  //      adder-indexed ports was the 3.9K-LUT cone). Echoed response
  //      regions read back from the RAM; classification fields are
  //      captured into registers at FIXED beat/lane positions below.
  logic [63:0] fword_r [0:NUM_BEATS_C-1];
  reg [3:0]    wbeat_r;      //! ingest beat, saturating at 10
  reg          ovfl_r;       //! ACMP frame longer than 72 B
  reg          len_ok_r;     //! tlast beat carried >= 70 bytes
  reg          adp_len_ok_r; //! frame reached the ADP entity_id (>= 26 B)

  // -----------------------------------------------------------------------
  // Classification captures (fixed beat/lane picks; the w_* names keep the
  // SM code below unchanged)
  // -----------------------------------------------------------------------
  reg        cap_dst_ok_r, cap_etype_ok_r, cap_sv0_r;
  reg [7:0]  cap_subtype_r;
  reg [3:0]  cap_msg_r;
  reg [4:0]  cap_status_r;
  reg [63:0] cap_sid_r, cap_ctlr_r, cap_talker_r;
  reg        cap_lstnr_hi_ok_r, cap_lstnr_lo_ok_r;
  reg [15:0] cap_tuid_r, cap_luid_r, cap_flags_r;
  reg [47:0] cap_dmac_r;
  reg [11:0] cap_vlan_r;

  wire [3:0]  w_msg    = cap_msg_r;
  wire [4:0]  w_status = cap_status_r;
  wire [63:0] w_sid    = cap_sid_r;
  wire [63:0] w_ctlr   = cap_ctlr_r;
  wire [63:0] w_talker = cap_talker_r;
  wire [15:0] w_tuid   = cap_tuid_r;
  wire [15:0] w_luid   = cap_luid_r;
  wire [15:0] w_flags  = cap_flags_r;
  wire        w_lstnr_us = cap_lstnr_hi_ok_r && cap_lstnr_lo_ok_r;

  wire w_acmp_base = enable_i && !ovfl_r && len_ok_r &&
                     cap_dst_ok_r && cap_etype_ok_r &&
                     (cap_subtype_r == ACMP_SUBTYPE_C) && cap_sv0_r;

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
  wire w_lstn_hit = w_acmp_base && w_is_lstn_cmd && w_lstnr_us;
  wire w_uid_ok   = (w_luid == 16'd0);

  //! probe answer: CONNECT_TX_RESPONSE addressed to us as listener
  wire w_probe_resp = w_acmp_base && (w_msg == ACMP_CONNECT_TX_RESPONSE_C) &&
                      w_lstnr_us && (w_luid == 16'd0) &&
                      (st_lsm_r == LSM_PRB_W_RESP_S || st_lsm_r == LSM_PRB_W_RESP2_S);

  //! ADP watch: available/departing from the bound talker (entity_id sits
  //! at wire byte 18 — same capture as the ACMP stream_id)
  wire w_adp_frame = enable_i && cap_etype_ok_r && (cap_subtype_r == 8'hFA) &&
                     adp_len_ok_r && (st_lsm_r != LSM_UNBOUND_S) &&
                     (cap_sid_r == bnd_talker_r);
  wire w_adp_avail  = w_adp_frame && (cap_msg_r == 4'd0);
  wire w_adp_depart = w_adp_frame && (cap_msg_r == 4'd1);

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
  reg         resp_unb_r;      //! GET_RX_STATE for sink 1 (CRF): valid but
                               //! ALWAYS unbound - the AEM advertises 2 sinks,
                               //! so UNKNOWN_ID here is an enumeration-fatal
                               //! inconsistency (la_avdecc field report)
  reg         probe_pend_r;     //! send a PROBE_TX after the current response

  reg [3:0] beat_r;
  wire [63:0] rword_w = fword_r[beat_r];   //! async distributed-RAM read

  //! response field muxes (evaluated live at emit time — the same register
  //! sampling the old echo array had, so wire behaviour is unchanged)
  wire        w_bound   = (st_lsm_r != LSM_UNBOUND_S);
  wire        w_b_eff   = w_bound && !resp_unb_r;   //! sink-0 state masked
  //! dest-MAC echoed in responses: the fresh capture on BIND (dmac_r loads
  //! the same edge the response fires), the stored binding on GET_RX_STATE
  wire [47:0] w_dmac_echo = (resp_kind_r == L_RESP_BIND_E)  ? cap_dmac_r
                          : (resp_kind_r == L_RESP_STATE_E && w_b_eff) ? dmac_r
                          : 48'd0;
                                                    //! out of sink-1 replies
  wire        w_str_echo = (resp_kind_r == L_RESP_STATE_E);   // stream_id/vlan
  //! talker bytes 34-41: BIND echo / UNBIND zero / STATE bound?bnd:0
  function automatic [7:0] tkb(input int idx, input [7:0] echo);
    unique case (resp_kind_r)
      L_RESP_BIND_E:   tkb = echo;
      L_RESP_UNBIND_E: tkb = 8'h00;
      default:         tkb = w_b_eff ? bnd_talker_r[8*(7-idx) +: 8] : 8'h00;
    endcase
  endfunction
  //! response flags bytes 64-65
  logic [15:0] w_resp_flags;
  always_comb begin
    unique case (resp_kind_r)
      L_RESP_BIND_E:   w_resp_flags = w_flags &
          ~(ACMP_FLAG_FAST_CONNECT_C | ACMP_FLAG_SRP_REG_FAILED_C);
      L_RESP_UNBIND_E: w_resp_flags = w_flags &
          ~(ACMP_FLAG_STREAMING_WAIT_C | ACMP_FLAG_FAST_CONNECT_C |
            ACMP_FLAG_SRP_REG_FAILED_C);
      default: begin
        if (!w_b_eff)
          w_resp_flags = 16'h0000;
        else if (st_lsm_r == LSM_SETTLED_NO_RSV_S ||
                 st_lsm_r == LSM_SETTLED_RSV_OK_S)
          w_resp_flags = bnd_flags_r & ACMP_FLAG_STREAMING_WAIT_C;
        else
          w_resp_flags = ACMP_FLAG_STREAMING_WAIT_C |
                         (ta_failed_i ? ACMP_FLAG_SRP_REG_FAILED_C : 16'h0);
      end
    endcase
  end

  //! probe flags: STREAMING_WAIT | SRP_REG_FAILED cleared from the binding
  wire [15:0] w_probe_flags = bnd_flags_r &
      ~(ACMP_FLAG_STREAMING_WAIT_C | ACMP_FLAG_SRP_REG_FAILED_C);

  //! probe frame byte (positions per the ACMPDU layout; the synthesizer
  //! folds the per-lane calls into constant-position muxes)
  function automatic [7:0] probe_byte(input int b);
    probe_byte = 8'h00;
    unique case (b)
      0: probe_byte = 8'h91;  1: probe_byte = 8'hE0;  2: probe_byte = 8'hF0;
      3: probe_byte = 8'h01;
      6:  probe_byte = station_mac_i[47:40];
      7:  probe_byte = station_mac_i[39:32];
      8:  probe_byte = station_mac_i[31:24];
      9:  probe_byte = station_mac_i[23:16];
      10: probe_byte = station_mac_i[15:8];
      11: probe_byte = station_mac_i[7:0];
      12: probe_byte = 8'h22; 13: probe_byte = 8'hF0;
      14: probe_byte = ACMP_SUBTYPE_C;
      15: probe_byte = {4'h0, ACMP_CONNECT_TX_COMMAND_C};
      16: probe_byte = {ACMP_STATUS_SUCCESS_C, ACMP_CDL_C[10:8]};
      17: probe_byte = ACMP_CDL_C[7:0];
      26,27,28,29,30,31,32,33: probe_byte = bnd_ctlr_r[8*(33-b) +: 8];
      34,35,36,37,38,39,40,41: probe_byte = bnd_talker_r[8*(41-b) +: 8];
      42,43,44,45,46,47,48,49: probe_byte = entity_id_i[8*(49-b) +: 8];
      50: probe_byte = bnd_tuid_r[15:8];
      51: probe_byte = bnd_tuid_r[7:0];
      62: probe_byte = probe_seq_r[15:8];
      63: probe_byte = probe_seq_r[7:0];
      64: probe_byte = w_probe_flags[15:8];
      65: probe_byte = w_probe_flags[7:0];
      default: probe_byte = 8'h00;
    endcase
  endfunction

  //! response beat: RAM word + fixed per-beat lane overrides
  logic [63:0] w_resp;
  always_comb begin
    w_resp = rword_w;                                    // default: echo
    unique case (beat_r)
      4'd0: begin                                        // bytes 0-7
        w_resp[8*6 +: 8] = station_mac_i[47:40];
        w_resp[8*7 +: 8] = station_mac_i[39:32];
      end
      4'd1: begin                                        // bytes 8-15
        w_resp[8*0 +: 8] = station_mac_i[31:24];
        w_resp[8*1 +: 8] = station_mac_i[23:16];
        w_resp[8*2 +: 8] = station_mac_i[15:8];
        w_resp[8*3 +: 8] = station_mac_i[7:0];
        w_resp[8*7 +: 8] = {4'h0, resp_msg_r};
      end
      4'd2: begin                                        // bytes 16-23
        w_resp[8*0 +: 8] = {resp_status_r, ACMP_CDL_C[10:8]};
        w_resp[8*1 +: 8] = ACMP_CDL_C[7:0];
        if (!w_str_echo)                                 // stream_id 18-23
          w_resp[63:16] = 48'd0;
      end
      4'd3: begin                                        // bytes 24-31
        if (!w_str_echo) w_resp[15:0] = 16'd0;           // stream_id tail
      end
      4'd4: begin                                        // bytes 32-39
        for (int k = 0; k < 6; k++)                      // talker 34-39
          w_resp[8*(2+k) +: 8] = tkb(k, rword_w[8*(2+k) +: 8]);
      end
      4'd5: begin                                        // bytes 40-47
        w_resp[8*0 +: 8] = tkb(6, rword_w[8*0 +: 8]);    // talker 40-41
        w_resp[8*1 +: 8] = tkb(7, rword_w[8*1 +: 8]);
      end
      4'd6: begin                                        // bytes 48-55
        if (resp_kind_r != L_RESP_BIND_E) begin          // tuid 50-51
          w_resp[8*2 +: 8] = resp_unb_r ? 8'h00 : bnd_tuid_r[15:8];
          w_resp[8*3 +: 8] = resp_unb_r ? 8'h00 : bnd_tuid_r[7:0];
        end
        //! stream_dest_mac 54-59: echo the bound MAAP address (spec Table
        //! 8.2; the reference zeroed it, but Hive/la_avdecc display it and
        //! nothing interops against the zeros)
        w_resp[8*6 +: 8] = w_dmac_echo[47:40];           // dest_mac 54-55
        w_resp[8*7 +: 8] = w_dmac_echo[39:32];
      end
      4'd7: begin                                        // bytes 56-63
        w_resp[8*0 +: 8] = w_dmac_echo[31:24];           // dest_mac 56-59
        w_resp[8*1 +: 8] = w_dmac_echo[23:16];
        w_resp[8*2 +: 8] = w_dmac_echo[15:8];
        w_resp[8*3 +: 8] = w_dmac_echo[7:0];
        w_resp[8*4 +: 8] = 8'h00;                        // count 60-61
        w_resp[8*5 +: 8] = (resp_kind_r == L_RESP_BIND_E) ? 8'h01
                          : (resp_kind_r == L_RESP_STATE_E && w_b_eff) ? 8'h01
                          : 8'h00;
      end
      4'd8: begin                                        // bytes 64-69
        w_resp[8*0 +: 8] = w_resp_flags[15:8];
        w_resp[8*1 +: 8] = w_resp_flags[7:0];
        if (!w_str_echo) begin                           // vlan 66-67
          w_resp[8*2 +: 8] = 8'h00;
          w_resp[8*3 +: 8] = 8'h00;
        end
      end
      default: ;
    endcase
  end

  // -----------------------------------------------------------------------
  // Serialiser
  // -----------------------------------------------------------------------
  logic [63:0] w_beat;
  always_comb begin
    if (st_r == PROBE_S)
      for (int l = 0; l < 8; l++)
        w_beat[8*l +: 8] = probe_byte(32'(beat_r) * 8 + l);
    else
      w_beat = w_resp;
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
      st_r <= COLLECT_S; wbeat_r <= '0; ovfl_r <= 1'b0; beat_r <= '0;
      len_ok_r <= 1'b0; adp_len_ok_r <= 1'b0;
      cap_dst_ok_r <= 1'b0; cap_etype_ok_r <= 1'b0; cap_sv0_r <= 1'b0;
      cap_subtype_r <= '0; cap_msg_r <= '0; cap_status_r <= '0;
      cap_sid_r <= '0; cap_ctlr_r <= '0; cap_talker_r <= '0;
      cap_lstnr_hi_ok_r <= 1'b0; cap_lstnr_lo_ok_r <= 1'b0;
      cap_tuid_r <= '0; cap_luid_r <= '0; cap_flags_r <= '0;
      cap_dmac_r <= '0; cap_vlan_r <= '0;
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
      tx_wedge_cnt_o <= 8'd0; txwd_r <= '0;
      dbg_classify_r <= '0; dbg_fc_r <= '0; dbg_flags_r <= '0; dbg_basehit_r <= '0;
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

      //! ALWAYS-ARMED capture (07-18 silicon deafness): field captures run
      //! in CLASSIFY_S too, so a frame arriving ZERO-GAP behind the one
      //! being classified is not lost (RX FIFOs compress inter-frame gaps
      //! whenever the DMA consumer stalls, so on silicon EVERY queued
      //! command drains gaplessly behind an AAF-flood frame). During
      //! RESPOND_S/PROBE_S capture stays off to protect the fword echo
      //! source - only back-to-back ACMP commands lose a response there
      //! (controller retransmit covers it).
      if (rxv_r && (st_r == COLLECT_S || st_r == CLASSIFY_S)) begin
            // beat-aligned word write (full-word: unkept tail lanes are
            // never echoed — responses are exactly 70 bytes)
            if (wbeat_r < 4'(NUM_BEATS_C))
              fword_r[wbeat_r[3:0]] <= rxd_r;
            else
              ovfl_r <= 1'b1;

            // fixed-position field captures
            unique case (wbeat_r)
              4'd0: begin
                cap_dst_ok_r <= ({rxd_r[7:0],   rxd_r[15:8],  rxd_r[23:16],
                                  rxd_r[31:24], rxd_r[39:32], rxd_r[47:40]}
                                 == 48'h91E0_F001_0000);
              end
              4'd1: begin   // bytes 12-15
                cap_etype_ok_r <= ({rxd_r[39:32], rxd_r[47:40]} == 16'h22F0);
                cap_subtype_r  <= rxd_r[55:48];
                cap_sv0_r      <= (rxd_r[63:60] == 4'h0);
                cap_msg_r      <= rxd_r[59:56];
              end
              4'd2: begin   // bytes 16-23: status + stream_id[63:16]
                cap_status_r <= rxd_r[7:3];
                cap_sid_r[63:16] <= {rxd_r[23:16], rxd_r[31:24], rxd_r[39:32],
                                     rxd_r[47:40], rxd_r[55:48], rxd_r[63:56]};
              end
              4'd3: begin   // bytes 24-31: stream_id tail + ctlr[63:16]
                cap_sid_r[15:0]   <= {rxd_r[7:0], rxd_r[15:8]};
                cap_ctlr_r[63:16] <= {rxd_r[23:16], rxd_r[31:24], rxd_r[39:32],
                                      rxd_r[47:40], rxd_r[55:48], rxd_r[63:56]};
              end
              4'd4: begin   // bytes 32-39: ctlr tail + talker[63:16]
                cap_ctlr_r[15:0]    <= {rxd_r[7:0], rxd_r[15:8]};
                cap_talker_r[63:16] <= {rxd_r[23:16], rxd_r[31:24], rxd_r[39:32],
                                        rxd_r[47:40], rxd_r[55:48], rxd_r[63:56]};
              end
              4'd5: begin   // bytes 40-47: talker tail + listener[63:16]
                cap_talker_r[15:0] <= {rxd_r[7:0], rxd_r[15:8]};
                cap_lstnr_hi_ok_r  <= ({rxd_r[23:16], rxd_r[31:24], rxd_r[39:32],
                                        rxd_r[47:40], rxd_r[55:48], rxd_r[63:56]}
                                       == entity_id_i[63:16]);
              end
              4'd6: begin   // bytes 48-55: listener tail, tuid, luid, dmac hi
                cap_lstnr_lo_ok_r <= ({rxd_r[7:0], rxd_r[15:8]}
                                      == entity_id_i[15:0]);
                cap_tuid_r <= {rxd_r[23:16], rxd_r[31:24]};
                cap_luid_r <= {rxd_r[39:32], rxd_r[47:40]};
                cap_dmac_r[47:32] <= {rxd_r[55:48], rxd_r[63:56]};
              end
              4'd7: begin   // bytes 56-63: dmac tail
                cap_dmac_r[31:0] <= {rxd_r[7:0], rxd_r[15:8],
                                     rxd_r[23:16], rxd_r[31:24]};
              end
              4'd8: begin   // bytes 64-69: flags + vlan
                cap_flags_r <= {rxd_r[7:0], rxd_r[15:8]};
                cap_vlan_r  <= {rxd_r[19:16], rxd_r[31:24]};
              end
              default: ;
            endcase

            //! fresh-frame hygiene: beat 0 clears the previous frame's ovfl
            if (wbeat_r == 4'd0) ovfl_r <= 1'b0;

            wbeat_r <= (wbeat_r == 4'd10) ? 4'd10 : wbeat_r + 4'd1;
            if (rxl_r) begin
              // ACMP >= 70 bytes: 8 full beats + at least 6 tail lanes
              len_ok_r     <= (wbeat_r == 4'd8) && rxk_r[5];
              // ADP >= 26 bytes: entity_id fully captured
              adp_len_ok_r <= (wbeat_r >= 4'd4) ||
                              (wbeat_r == 4'd3 && rxk_r[1]);
              wbeat_r <= '0;               //! capture owns the beat counter
              //! COLLECT -> classify this frame; a frame ENDING during
              //! CLASSIFY (runt) is dropped by the case's own st_r write
              if (st_r == COLLECT_S) st_r <= CLASSIFY_S;
            end
      end

      case (st_r)
        COLLECT_S: begin
          if (!rxv_r && probe_pend_r) begin
            probe_pend_r  <= 1'b0;
            probe_count_o <= probe_count_o + 16'd1;
            arm(LSM_TMR_NO_RESP_MS_C);
            beat_r <= '0;
            st_r   <= PROBE_S;
          end
        end

        CLASSIFY_S: begin
          dbg_classify_r <= dbg_classify_r + 8'd1;
          if (cap_subtype_r == ACMP_SUBTYPE_C) begin
            dbg_fc_r    <= dbg_fc_r + 8'd1;
            dbg_flags_r <= {cap_dst_ok_r, cap_etype_ok_r, cap_sv0_r, len_ok_r,
                            ovfl_r, cap_lstnr_hi_ok_r, cap_lstnr_lo_ok_r,
                            w_is_lstn_cmd};
            if (w_acmp_base && w_is_lstn_cmd)
              dbg_basehit_r <= dbg_basehit_r + 8'd1;
          end

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
      resp_unb_r  <= 1'b0;
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
                resp_unb_r  <= 1'b0;
                if (!w_uid_ok) begin
                  resp_status_r <= ACMP_STATUS_LISTENER_UNKNOWN_ID_C;
                end else begin
                  do_unbind();
                end
              end
              // ---------------- GET_RX_STATE ---------------------------
              default: begin
                resp_kind_r <= L_RESP_STATE_E;
                resp_unb_r  <= (w_luid == 16'd1);
                if (!w_uid_ok && w_luid != 16'd1)
                  resp_status_r <= ACMP_STATUS_LISTENER_UNKNOWN_ID_C;
              end
            endcase
            beat_r <= '0;
            st_r   <= RESPOND_S;
          end else if (w_probe_resp) begin
            // ---------------- probe answer -----------------------------
            tmr_r <= 14'd0;   // remove NO_RESP
            if (w_status == ACMP_STATUS_SUCCESS_C) begin
              sid_r    <= w_sid;
              dmac_r   <= cap_dmac_r;
              vlan_r   <= cap_vlan_r;
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
            st_r <= COLLECT_S;
          end else begin
            st_r <= COLLECT_S;
          end
        end

        RESPOND_S, PROBE_S: begin
          if (m_axis_tready) begin
            txwd_r <= '0;
            if (beat_r == NUM_BEATS_C-1) begin
              // post-increment the probe sequence per emission (reference
              // prepare_probe_tx_command_success: send seq, then ++)
              if (st_r == PROBE_S) probe_seq_r <= probe_seq_r + 16'd1;
              wbeat_r <= '0; ovfl_r <= 1'b0;
              beat_r <= '0;
              st_r <= COLLECT_S;
            end else begin
              beat_r <= beat_r + 4'd1;
            end
          end
          else if (txwd_r == TXWD_MAX_C) begin
            //! grant never came: drop the response, stay alive (the walker
            //! being stuck here is what deafened the listener on silicon)
            txwd_r <= '0;
            tx_wedge_cnt_o <= (&tx_wedge_cnt_o) ? tx_wedge_cnt_o
                                                : tx_wedge_cnt_o + 8'd1;
            wbeat_r <= '0; ovfl_r <= 1'b0;
            beat_r <= '0;
            st_r <= COLLECT_S;
          end
          else begin
            txwd_r <= txwd_r + 20'd1;
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

  assign dbg_o = {dbg_classify_r, dbg_fc_r, dbg_flags_r, dbg_basehit_r};

endmodule

`default_nettype wire
