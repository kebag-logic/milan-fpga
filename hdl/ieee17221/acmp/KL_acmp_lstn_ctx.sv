/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_acmp_lstn_ctx.sv
//  Project     : Milan ACMP  (IEEE 1722.1-2021 Clause 8, AVnu Milan v1.2 §5.5)
//
//  Description : N-context Milan v1.2 LISTENER-side ACMP engine: ONE shared
//                state machine + ONE context RAM serving N_SINKS_P listener
//                BIND CONTEXTS (listener_unique_id 0..N-1). Generalizes the
//                proven single-sink KL_acmp_listener SM (whose behaviour is
//                the byte-exact contract: pipewire acmp-milan-v12.c incl. the
//                REF-BUG fixes documented there) to N sinks.
//
//                Per-context CONFIG (elaboration parameters, one bit each):
//                  PROBE_SM_EN_P[c]  1 = full Milan 5.5.3 binding SM (probe
//                                        ladder, ADP talker watch, SRP
//                                        coupling) — today's sink 0;
//                                    0 = pure bind RECORD (no probe SM, no
//                                        MSRP attach, no ADP watch) — today's
//                                        CRF sink 1.
//                  SID_EXPLICIT_P[c] 1 = honour a nonzero fast-connect
//                                        stream_id in CONNECT_RX (Milan
//                                        5.5.1.2), zero falls back to the
//                                        {talker EID, tuid} derivation;
//                                    0 = always derive sid_from_eid
//                                        (today's sink-0 behaviour).
//                Defaults reproduce today's exact pair: ctx0 = {SM, derive},
//                ctx1 = {record, explicit} — the no-regression axiom.
//
//                STRUCTURE
//                  context RAM : acmp_lstn_ctx_t ctx_ram[N] — sync-only
//                    write, ONE explicit read port (house RAM rules; the
//                    07-21 LUTRAM read-port-replica defect is why). Post-
//                    reset init walk zeroes all records (all-zero = UNBOUND).
//                  cur_r       : working copy of one record, latched from
//                    the read port on the frame-end beat (async distributed
//                    read, zero added response latency vs the single-sink
//                    module) and at probe launch.
//                  sweep       : ONE timer wheel for all contexts. Causes
//                    (1 ms tick, 1 s ADP aging, ADP available/departing,
//                    SRP registrar edges) latch pending flags; a pass walks
//                    ctx 0..N-1 (one RMW cycle each) applying the same
//                    per-state transition table the single-sink SM used.
//                    The pass yields the RAM port to frame classification.
//                  responder   : CONNECT_RX / DISCONNECT_RX / GET_RX_STATE
//                    served for ANY context by listener_unique_id; uid >=
//                    N answers LISTENER_UNKNOWN_ID (fields from the ctx-0
//                    record, matching the single-sink module byte-exactly).
//                  probes      : probe_pend_r vector; one serializer emits
//                    PROBE_TX for the lowest pending context, arming that
//                    context's 200 ms NO_RESP timer on the shared wheel.
//
//                COMPATIBILITY VIEW: contexts 0/1 are shadowed into
//                view0_*/view1_* register outputs (written on the same edge
//                as the RAM, so they never diverge) — the two hardwired
//                status surfaces today's datapath/CSR consume.
//
//                TABLE ACCESS: tbl_req_i/tbl_idx_i -> tbl_gnt_o/tbl_ctx_o
//                request/grant port; the whole record of any context is
//                read out when the RAM port is idle (the NxN CSR
//                integration lane consumes this later). Hold req until gnt.
//
//  RX          : MONITOR tap (little lane), never backpressures.
//  TX          : 70-byte ACMP frames via the shared low-rate TX arbiter.
//---------------------------------------------------------------------------//

`default_nettype none

import acmp_pkg::*;

module KL_acmp_lstn_ctx #(
    parameter int unsigned CLK_FREQ_HZ_P = 100_000_000,
    parameter int unsigned N_SINKS_P     = 2,
    //! per-context probe-SM enable (bit c = context c); default = sink 0 only
    parameter logic [N_SINKS_P-1:0] PROBE_SM_EN_P  = (N_SINKS_P)'(1),
    //! per-context explicit-sid fast-connect policy; default = sink 1 only
    parameter logic [N_SINKS_P-1:0] SID_EXPLICIT_P = (N_SINKS_P)'(2)
) (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         enable_i,          //! gate (CSR ADP enable)

    // ---- identity ------------------------------------------------------
    input  wire [47:0]  station_mac_i,     //! [47:40] = first wire byte
    input  wire [63:0]  entity_id_i,

    // ---- ADP age tick ----------------------------------------------------
    input  wire         tick_1s_i,

    // ---- lwSRP listener-side hooks (per context) ------------------------
    input  wire [N_SINKS_P-1:0] ta_registered_i, //! TalkerAdvertise registered
    input  wire [N_SINKS_P-1:0] ta_failed_i,     //! TalkerFailed registered
    output wire [N_SINKS_P-1:0] lstn_declare_o,  //! declare Listener attribute
    output wire [N_SINKS_P-1:0] stream_active_o, //! sink open (SETTLED_*)

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

    // ---- context-0 compatibility view (today's sink-0 status group) ----
    output acmp_lsm_t   view0_state_o,
    output wire [63:0]  view0_talker_o,
    output wire [15:0]  view0_tuid_o,
    output wire [63:0]  view0_sid_o,
    output wire [11:0]  view0_vlan_o,
    output wire [47:0]  view0_dmac_o,
    output wire [4:0]   view0_status_o,
    output wire [1:0]   view0_probing_o,
    output wire         view0_tk_avail_o,

    // ---- context-1 compatibility view (today's CRF sink-1 record) ------
    output wire         view1_bound_o,
    output wire [63:0]  view1_sid_o,
    output wire [47:0]  view1_dmac_o,

    // ---- counters / walker forensics ------------------------------------
    output reg  [15:0]  cmd_count_o,       //! listener commands accepted
    output reg  [15:0]  probe_count_o,     //! PROBE_TX commands sent
    output reg  [7:0]   tx_wedge_cnt_o,    //! responses abandoned (watchdog)
    output wire [31:0]  dbg_o,             //! {classify_cnt, fc_cnt, fc_flags,
                                           //!  base_hits} walker forensics

    // ---- context-table request/grant port (NxN CSR lane, later) --------
    input  wire                            tbl_req_i,  //! hold until gnt
    input  wire [$clog2(N_SINKS_P)-1:0]    tbl_idx_i,
    output reg                             tbl_gnt_o,  //! 1-cycle strobe
    output acmp_lstn_ctx_t                 tbl_ctx_o   //! valid with gnt
);

  localparam int NUM_BEATS_C = (ACMP_FRAME_BYTES_C + 7) / 8;            //! 9
  localparam int LAST_KEEP_C = ACMP_FRAME_BYTES_C - (NUM_BEATS_C-1)*8;  //! 6
  localparam int IDX_W_C     = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1;

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
  //! randomized 0..1023 ms delay draw (never 0 = disarmed)
  wire [13:0] w_delay_draw = {4'd0, lfsr_r[9:0]} + 14'd1;

  // -----------------------------------------------------------------------
  // Context table: sync-only write, ONE explicit read port (house RAM rule)
  // -----------------------------------------------------------------------
  acmp_lstn_ctx_t ctx_ram [0:N_SINKS_P-1];

  logic                 wr_en_w;
  logic [IDX_W_C-1:0]   wr_idx_w;
  acmp_lstn_ctx_t       wr_data_w;
  logic [IDX_W_C-1:0]   rd_idx_w;
  acmp_lstn_ctx_t       rd_ctx_w;

  always_ff @(posedge clk_i) begin : ctx_ram_wr    // RAM in its own process
    if (wr_en_w) ctx_ram[wr_idx_w] <= wr_data_w;
  end
  assign rd_ctx_w = ctx_ram[rd_idx_w];             //! the single read port

  //! post-reset init walk: all-zero records = UNBOUND everywhere
  reg                 init_done_r;
  reg [IDX_W_C-1:0]   init_idx_r;

  //! compatibility shadows + per-context activity vector — written on the
  //! same edge as the RAM, from the same write data (never diverge)
  acmp_lstn_ctx_t          view0_r, view1_r;
  reg [N_SINKS_P-1:0]      active_vec_r;

  assign view0_state_o    = view0_r.state;
  assign view0_talker_o   = view0_r.talker;
  assign view0_tuid_o     = view0_r.tuid;
  assign view0_sid_o      = view0_r.sid;
  assign view0_vlan_o     = view0_r.vlan;
  assign view0_dmac_o     = view0_r.dmac;
  assign view0_status_o   = view0_r.status;
  assign view0_probing_o  = view0_r.probing;
  assign view0_tk_avail_o = view0_r.tk_avail;
  assign view1_bound_o    = (view1_r.state != LSM_UNBOUND_S);
  assign view1_sid_o      = view1_r.sid;
  assign view1_dmac_o     = view1_r.dmac;
  //! declare the Listener attribute while activated (Ready vs Ready-Failed
  //! is selected downstream from ta_registered_i)
  assign lstn_declare_o   = active_vec_r;
  assign stream_active_o  = active_vec_r;

  // -----------------------------------------------------------------------
  // Working context + probe bookkeeping
  // -----------------------------------------------------------------------
  acmp_lstn_ctx_t       cur_r;       //! record of the context being served
  reg [IDX_W_C-1:0]     cur_idx_r;
  reg [N_SINKS_P-1:0]   probe_pend_r;
  reg [15:0]            probe_seq_r; //! shared across contexts (per-entity)

  //! MSRP stream_id from {talker EID, uid} — the reference
  //! peer_id_from_entity_id: EUI-64 with the FF:FE marker rebuilds the MAC
  //! (drop bytes 3-4), plain MAC|index EIDs just swap the low 16 bits.
  function automatic [63:0] sid_from_eid(input [63:0] eid, input [15:0] uid);
    if (eid[39:24] == 16'hFFFE)
      sid_from_eid = {eid[63:40], eid[23:0], uid};
    else
      sid_from_eid = {eid[63:16], uid};
  endfunction

  // -----------------------------------------------------------------------
  // Frame capture (identical recipe to the single-sink module)
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

  // ---- frame word buffer: beat-aligned distributed RAM (area-70 recipe)
  logic [63:0] fword_r [0:NUM_BEATS_C-1];
  reg [3:0]    wbeat_r;      //! ingest beat, saturating at 10
  reg          ovfl_r;       //! ACMP frame longer than 72 B
  reg          len_ok_r;     //! tlast beat carried >= 70 bytes
  reg          adp_len_ok_r; //! frame reached the ADP entity_id (>= 26 B)

  // -----------------------------------------------------------------------
  // Classification captures (fixed beat/lane picks)
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
  //! listener commands for us; frames addressed to other entities dropped
  wire w_lstn_hit  = w_acmp_base && w_is_lstn_cmd && w_lstnr_us;
  //! uid valid = a real context; >= N answers LISTENER_UNKNOWN_ID with the
  //! ctx-0 record fields (matching the single-sink module byte-exactly)
  wire w_uid_valid = (w_luid < 16'(N_SINKS_P));
  wire [IDX_W_C-1:0] w_luid_idx = w_uid_valid ? IDX_W_C'(w_luid) : '0;

  //! per-context config of the record being served
  wire w_sm_en   = PROBE_SM_EN_P[cur_idx_r];
  wire w_sid_exp = SID_EXPLICIT_P[cur_idx_r];

  //! probe answer: CONNECT_TX_RESPONSE addressed to us, context probing
  wire w_probe_resp = w_acmp_base && (w_msg == ACMP_CONNECT_TX_RESPONSE_C) &&
                      w_lstnr_us && w_uid_valid && w_sm_en &&
                      (cur_r.state == LSM_PRB_W_RESP_S ||
                       cur_r.state == LSM_PRB_W_RESP2_S);

  //! ADP watch: any ENTITY_AVAILABLE/DEPARTING is latched for the sweep,
  //! which applies it per context (bound-talker match happens there)
  wire w_adp_seen  = enable_i && cap_etype_ok_r && (cap_subtype_r == 8'hFA) &&
                     adp_len_ok_r &&
                     (cap_msg_r == 4'd0 || cap_msg_r == 4'd1);

  //! rebind-to-same fast path: same talker + STREAMING_WAIT agreement
  wire w_same_talker = (w_talker == cur_r.talker) && (w_tuid == cur_r.tuid);
  wire w_flags_match = ((cur_r.flags & w_flags & ACMP_FLAG_STREAMING_WAIT_C) != 16'd0)
                       || ((cur_r.flags | w_flags) & ACMP_FLAG_STREAMING_WAIT_C) == 16'd0;

  //! per-context sid policy (Milan 5.5.1.2): explicit fast-connect sid when
  //! configured AND nonzero, else the {talker EID, tuid} derivation
  wire [63:0] w_bind_sid = (w_sid_exp && cap_sid_r != 64'd0)
                         ? cap_sid_r
                         : sid_from_eid(w_talker, w_tuid);

  // -----------------------------------------------------------------------
  // Response / probe frame assembly (from cur_r — the record snapshot)
  // -----------------------------------------------------------------------
  typedef enum logic [1:0] { L_RESP_BIND_E, L_RESP_UNBIND_E, L_RESP_STATE_E } lresp_t;
  reg [3:0]   resp_msg_r;
  reg [4:0]   resp_status_r;
  lresp_t     resp_kind_r;

  reg [3:0] beat_r;
  wire [63:0] rword_w = fword_r[beat_r];   //! async distributed-RAM read

  wire        w_bound   = (cur_r.state != LSM_UNBOUND_S);
  //! dest-MAC echoed in responses: the fresh capture on BIND (the record
  //! loads the same edge the response fires), the stored binding on STATE
  wire [47:0] w_dmac_echo = (resp_kind_r == L_RESP_BIND_E)  ? cap_dmac_r
                          : (resp_kind_r == L_RESP_STATE_E && w_bound)
                            ? cur_r.dmac
                          : 48'd0;
  wire        w_str_echo = (resp_kind_r == L_RESP_STATE_E);   // stream_id/vlan
  //! talker bytes 34-41: BIND echo / UNBIND zero / STATE bound?record:0
  function automatic [7:0] tkb(input int idx, input [7:0] echo);
    unique case (resp_kind_r)
      L_RESP_BIND_E:   tkb = echo;
      L_RESP_UNBIND_E: tkb = 8'h00;
      default:         tkb = !w_bound ? 8'h00 : cur_r.talker[8*(7-idx) +: 8];
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
        if (!w_bound)
          w_resp_flags = 16'h0000;
        else if (cur_r.state == LSM_SETTLED_NO_RSV_S ||
                 cur_r.state == LSM_SETTLED_RSV_OK_S)
          //! settled (and record-only contexts, parked settled): stored SW
          w_resp_flags = cur_r.flags & ACMP_FLAG_STREAMING_WAIT_C;
        else
          w_resp_flags = ACMP_FLAG_STREAMING_WAIT_C |
                         (ta_failed_i[cur_idx_r] ? ACMP_FLAG_SRP_REG_FAILED_C
                                                 : 16'h0);
      end
    endcase
  end

  //! probe flags: STREAMING_WAIT | SRP_REG_FAILED cleared from the binding
  wire [15:0] w_probe_flags = cur_r.flags &
      ~(ACMP_FLAG_STREAMING_WAIT_C | ACMP_FLAG_SRP_REG_FAILED_C);

  //! probe frame byte (positions per the ACMPDU layout)
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
      26,27,28,29,30,31,32,33: probe_byte = cur_r.ctlr[8*(33-b) +: 8];
      34,35,36,37,38,39,40,41: probe_byte = cur_r.talker[8*(41-b) +: 8];
      42,43,44,45,46,47,48,49: probe_byte = entity_id_i[8*(49-b) +: 8];
      50: probe_byte = cur_r.tuid[15:8];
      51: probe_byte = cur_r.tuid[7:0];
      //! listener_unique_id = the probing context (the talker echoes it,
      //! routing the CONNECT_TX_RESPONSE back to this context; ctx 0 = the
      //! single-sink module's constant zero)
      52: probe_byte = 8'(16'(cur_idx_r) >> 8);
      53: probe_byte = 8'(16'(cur_idx_r));
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
          w_resp[8*2 +: 8] = !w_bound ? 8'h00 : cur_r.tuid[15:8];
          w_resp[8*3 +: 8] = !w_bound ? 8'h00 : cur_r.tuid[7:0];
        end
        //! stream_dest_mac 54-59: echo the bound MAAP address (spec Table
        //! 8.2; Hive/la_avdecc display it)
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
                          : (resp_kind_r == L_RESP_STATE_E && w_bound) ? 8'h01
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
  // RAM port scheduling
  //   read : frame-end latch  >  probe launch  >  sweep  >  table port
  //   write: init walk  >  classify writeback  >  probe arm  >  sweep
  // -----------------------------------------------------------------------
  //! frame-end cycle: cur_r latches the addressed record (async read)
  wire w_frame_latch = init_done_r && rxv_r && rxl_r && (st_r == COLLECT_S);

  //! probe launch pick (lowest pending context wins)
  logic [IDX_W_C-1:0] launch_idx_w;
  always_comb begin : launch_pick
    launch_idx_w = '0;
    for (int i = N_SINKS_P-1; i >= 0; i--)
      if (probe_pend_r[i]) launch_idx_w = IDX_W_C'(i);
  end

  //! sweep sequencer state
  reg                  swp_active_r;
  reg [IDX_W_C-1:0]    swp_idx_r;
  reg                  c_ms_r, c_1s_r, c_adp_r;   //! causes of this pass
  reg [1:0]            ms_pend_r;
  reg                  s1_pend_r, adp_pend_r;
  reg [63:0]           adp_eid_r;
  reg                  adp_avail_r;
  reg [N_SINKS_P-1:0]  srv_reg_r, srv_fail_r;     //! last-serviced SRP levels

  wire w_srp_diff = (ta_registered_i != srv_reg_r) || (ta_failed_i != srv_fail_r);
  //! an ADP frame classified THIS cycle (latched + consumable immediately)
  wire w_adp_now  = (st_r == CLASSIFY_S) && w_adp_seen;
  //! live causes so a pass starts ON the strobe cycle (first RMW the next
  //! cycle — the single-sink module's event-application cadence)
  wire w_swp_pending = (ms_pend_r != 2'd0) || tick_1ms_r ||
                       s1_pend_r || tick_1s_i ||
                       adp_pend_r || w_adp_now || w_srp_diff;

  wire w_launch_ok = init_done_r && (st_r == COLLECT_S) && !rxv_r &&
                     (probe_pend_r != '0) && !swp_active_r;
  wire w_swp_run   = swp_active_r && !w_frame_latch && (st_r != CLASSIFY_S);
  wire w_tbl_ok    = init_done_r && tbl_req_i && !w_frame_latch &&
                     !w_launch_ok && !swp_active_r && (st_r != CLASSIFY_S);

  always_comb begin : rd_port_mux
    if      (w_frame_latch) rd_idx_w = w_luid_idx;
    else if (w_launch_ok)   rd_idx_w = launch_idx_w;
    else if (w_swp_run)     rd_idx_w = swp_idx_r;
    else                    rd_idx_w = tbl_idx_i;
  end

  // -----------------------------------------------------------------------
  // Frame-classify writeback (evaluated in CLASSIFY_S)
  // -----------------------------------------------------------------------
  logic           wr_frame_en_w;
  acmp_lstn_ctx_t wr_frame_w;
  logic           probe_set_w;
  always_comb begin : classify_writeback
    wr_frame_en_w = 1'b0;
    probe_set_w   = 1'b0;
    wr_frame_w    = cur_r;
    if (w_lstn_hit && w_uid_valid) begin
      unique case (w_msg)
        // ---------------- BIND_RX ------------------------------------
        ACMP_CONNECT_RX_COMMAND_C: begin
          if (!w_sm_en) begin
            //! record-only context (today's CRF sink 1): pure bind record,
            //! parked SETTLED_NO_RSV (bound, no probe SM, no MSRP attach)
            wr_frame_en_w    = 1'b1;
            wr_frame_w       = '0;
            wr_frame_w.state = LSM_SETTLED_NO_RSV_S;
            wr_frame_w.ctlr  = w_ctlr;
            wr_frame_w.talker= w_talker;
            wr_frame_w.tuid  = w_tuid;
            wr_frame_w.flags = w_flags;
            wr_frame_w.dmac  = cap_dmac_r;
            wr_frame_w.sid   = w_bind_sid;
          end else if (cur_r.state != LSM_UNBOUND_S &&
                       w_same_talker && w_flags_match) begin
            // rebind-same fast path: response only, no state change
          end else begin
            wr_frame_en_w     = 1'b1;
            wr_frame_w.ctlr   = w_ctlr;
            wr_frame_w.talker = w_talker;
            wr_frame_w.tuid   = w_tuid;
            if (cur_r.state == LSM_UNBOUND_S) begin      // full bind
              wr_frame_w.flags  = w_flags;
              wr_frame_w.status = 5'd0;
            end else begin                               // rebind
              wr_frame_w.flags = (cur_r.flags & ~ACMP_FLAG_STREAMING_WAIT_C) |
                                 (w_flags & ACMP_FLAG_STREAMING_WAIT_C);
            end
            wr_frame_w.probing = 2'd2;                   // ACTIVE
            wr_frame_w.sid     = w_bind_sid;
            if (cur_r.state == LSM_SETTLED_NO_RSV_S ||
                cur_r.state == LSM_SETTLED_RSV_OK_S)
              wr_frame_w.active = 1'b0;                  // deactivate
            wr_frame_w.tmr   = 14'd0;   // NO_RESP armed at probe launch
            wr_frame_w.state = LSM_PRB_W_RESP_S;
            probe_set_w      = 1'b1;    // PROBE after the response drains
          end
        end
        // ---------------- UNBIND_RX ----------------------------------
        ACMP_DISCONNECT_RX_COMMAND_C: begin
          wr_frame_en_w = 1'b1;
          wr_frame_w    = '0;           // probing DISABLED (REF-BUG 3 rule)
          if (w_sm_en) begin
            //! the ADP availability view survives an unbind (aging clears)
            wr_frame_w.tk_avail = cur_r.tk_avail;
            wr_frame_w.adp_age  = cur_r.adp_age;
          end
        end
        // ---------------- GET_RX_STATE: no state change ---------------
        default: ;
      endcase
    end else if (w_probe_resp) begin
      wr_frame_en_w = 1'b1;
      if (w_status == ACMP_STATUS_SUCCESS_C) begin
        wr_frame_w.sid     = w_sid;      // authoritative stream_id
        wr_frame_w.dmac    = cap_dmac_r;
        wr_frame_w.vlan    = cap_vlan_r;
        wr_frame_w.active  = 1'b1;
        wr_frame_w.probing = 2'd3;       // COMPLETED
        wr_frame_w.status  = 5'd0;
        wr_frame_w.tmr     = LSM_TMR_NO_TK_MS_C;
        wr_frame_w.state   = LSM_SETTLED_NO_RSV_S;
      end else begin
        wr_frame_w.status = w_status;
        wr_frame_w.tmr    = LSM_TMR_RETRY_MS_C;
        wr_frame_w.state  = LSM_PRB_W_RETRY_S;
      end
    end
  end

  // -----------------------------------------------------------------------
  // Sweep compute: ONE timer wheel + ADP watch + SRP edges over all contexts
  // (same per-state transition table as the single-sink SM, incl. the
  // REF-BUG 1/2 fixes)
  // -----------------------------------------------------------------------
  acmp_lstn_ctx_t sn_w;
  logic           sn_wr_w;
  logic           swp_probe_set_w;
  always_comb begin : sweep_next
    logic fire, adp_disc, adp_dep, sm, reg_rise, reg_fall, fail_rise;
    sn_w            = rd_ctx_w;
    sn_wr_w         = 1'b0;
    swp_probe_set_w = 1'b0;
    sm       = PROBE_SM_EN_P[swp_idx_r];
    fire     = 1'b0;
    adp_disc = 1'b0;
    adp_dep  = 1'b0;
    // ---- 1 s ADP availability aging --------------------------------
    if (c_1s_r && rd_ctx_w.tk_avail) begin
      if (rd_ctx_w.adp_age >= LSM_ADP_AGE_S_C) sn_w.tk_avail = 1'b0;
      else                                     sn_w.adp_age  = rd_ctx_w.adp_age + 7'd1;
      sn_wr_w = 1'b1;
    end
    // ---- 1 ms countdown (fire on the 1 -> 0 edge) --------------------
    if (c_ms_r && rd_ctx_w.tmr != 14'd0) begin
      fire     = (rd_ctx_w.tmr == 14'd1);
      sn_w.tmr = rd_ctx_w.tmr - 14'd1;
      sn_wr_w  = 1'b1;
    end
    // ---- ADP available/departing for THIS context's bound talker -----
    if (c_adp_r && sm && rd_ctx_w.state != LSM_UNBOUND_S &&
        rd_ctx_w.talker == adp_eid_r) begin
      if (adp_avail_r) begin
        adp_disc      = !rd_ctx_w.tk_avail;
        sn_w.tk_avail = 1'b1;
        sn_w.adp_age  = 7'd0;
      end else begin
        adp_dep       = rd_ctx_w.tk_avail;
        sn_w.tk_avail = 1'b0;
      end
      sn_wr_w = 1'b1;
    end
    // ---- SRP registrar edges (levels vs last-serviced snapshots) -----
    reg_rise  = sm &&  ta_registered_i[swp_idx_r] && !srv_reg_r[swp_idx_r];
    reg_fall  = sm && !ta_registered_i[swp_idx_r] &&  srv_reg_r[swp_idx_r];
    fail_rise = sm &&  ta_failed_i[swp_idx_r]     && !srv_fail_r[swp_idx_r];
    // ---- per-state transitions (single-sink SM table, per context) ---
    if (sm) begin
      unique case (rd_ctx_w.state)
        LSM_PRB_W_DELAY_S: begin
          if (fire) begin
            swp_probe_set_w = 1'b1;
            sn_w.probing    = 2'd2;
            sn_w.state      = LSM_PRB_W_RESP_S;
            sn_wr_w         = 1'b1;
          end else if (adp_dep) begin
            sn_w.tmr = 14'd0; sn_w.probing = 2'd1;       // PASSIVE
            sn_w.state = LSM_PRB_W_AVAIL_S; sn_wr_w = 1'b1;
          end
        end
        LSM_PRB_W_AVAIL_S: begin
          if (adp_disc) begin                            // REF-BUG 1 fixed
            sn_w.tmr = w_delay_draw; sn_w.probing = 2'd2;
            sn_w.state = LSM_PRB_W_DELAY_S; sn_wr_w = 1'b1;
          end
        end
        LSM_PRB_W_RESP_S: begin
          if (fire) begin
            swp_probe_set_w = 1'b1;                      // resend
            sn_w.state = LSM_PRB_W_RESP2_S; sn_wr_w = 1'b1;
          end else if (adp_dep) begin
            sn_w.tmr = 14'd0; sn_w.probing = 2'd1;
            sn_w.state = LSM_PRB_W_AVAIL_S; sn_wr_w = 1'b1;
          end
        end
        LSM_PRB_W_RESP2_S: begin
          if (fire) begin
            sn_w.tmr    = LSM_TMR_RETRY_MS_C;
            sn_w.status = ACMP_STATUS_LSTN_TALKER_TIMEOUT_C;
            sn_w.state  = LSM_PRB_W_RETRY_S; sn_wr_w = 1'b1;
          end else if (adp_dep) begin
            sn_w.tmr = 14'd0; sn_w.probing = 2'd1;
            sn_w.state = LSM_PRB_W_AVAIL_S; sn_wr_w = 1'b1;
          end
        end
        LSM_PRB_W_RETRY_S: begin
          if (fire) begin                                // REF-BUG 2 fixed
            if (sn_w.tk_avail) begin
              sn_w.tmr = w_delay_draw; sn_w.probing = 2'd2;
              sn_w.state = LSM_PRB_W_DELAY_S;
            end else begin
              sn_w.probing = 2'd1;
              sn_w.state   = LSM_PRB_W_AVAIL_S;
            end
            sn_wr_w = 1'b1;
          end else if (adp_dep) begin
            sn_w.tmr = 14'd0; sn_w.probing = 2'd1;
            sn_w.state = LSM_PRB_W_AVAIL_S; sn_wr_w = 1'b1;
          end
        end
        LSM_SETTLED_NO_RSV_S: begin
          if (reg_rise) begin
            sn_w.tmr    = 14'd0;                         // remove NO_TK
            sn_w.active = 1'b1;
            sn_w.state  = LSM_SETTLED_RSV_OK_S; sn_wr_w = 1'b1;
          end else if (fire) begin                       // NO_TK lapsed
            if (sn_w.tk_avail) begin
              sn_w.tmr = w_delay_draw; sn_w.probing = 2'd2;
              sn_w.state = LSM_PRB_W_DELAY_S;
            end else begin
              sn_w.probing = 2'd1;
              sn_w.state   = LSM_PRB_W_AVAIL_S;
            end
            sn_wr_w = 1'b1;
          end
        end
        LSM_SETTLED_RSV_OK_S: begin
          if (reg_fall) begin
            sn_w.active = 1'b0;                          // deactivate
            if (sn_w.tk_avail) begin
              sn_w.tmr = w_delay_draw; sn_w.probing = 2'd2;
              sn_w.state = LSM_PRB_W_DELAY_S;
            end else begin
              sn_w.probing = 2'd1;
              sn_w.state   = LSM_PRB_W_AVAIL_S;
            end
            sn_wr_w = 1'b1;
          end else if (fail_rise) begin
            sn_w.state = LSM_SETTLED_NO_RSV_S; sn_wr_w = 1'b1;
          end
        end
        default: ;   // UNBOUND: nothing time-driven
      endcase
    end
  end

  // ---- write-port arbitration (exactly one writer per cycle) ------------
  always_comb begin : wr_port_mux
    wr_en_w   = 1'b0;
    wr_idx_w  = '0;
    wr_data_w = '0;
    if (!init_done_r) begin
      wr_en_w  = 1'b1;
      wr_idx_w = init_idx_r;
    end else if (st_r == CLASSIFY_S && wr_frame_en_w) begin
      wr_en_w   = 1'b1;
      wr_idx_w  = cur_idx_r;
      wr_data_w = wr_frame_w;
    end else if (w_launch_ok) begin                      // probe arm
      wr_en_w        = 1'b1;
      wr_idx_w       = launch_idx_w;
      wr_data_w      = rd_ctx_w;
      wr_data_w.tmr  = LSM_TMR_NO_RESP_MS_C;
    end else if (w_swp_run && sn_wr_w) begin
      wr_en_w   = 1'b1;
      wr_idx_w  = swp_idx_r;
      wr_data_w = sn_w;
    end
  end

  // -----------------------------------------------------------------------
  // Main FSM + shadows + sweep sequencer
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
      resp_msg_r <= 4'd0; resp_status_r <= 5'd0; resp_kind_r <= L_RESP_STATE_E;
      cur_r <= '0; cur_idx_r <= '0;
      probe_pend_r <= '0; probe_seq_r <= 16'd0;
      init_done_r <= 1'b0; init_idx_r <= '0;
      view0_r <= '0; view1_r <= '0; active_vec_r <= '0;
      swp_active_r <= 1'b0; swp_idx_r <= '0;
      c_ms_r <= 1'b0; c_1s_r <= 1'b0; c_adp_r <= 1'b0;
      ms_pend_r <= 2'd0; s1_pend_r <= 1'b0; adp_pend_r <= 1'b0;
      adp_eid_r <= '0; adp_avail_r <= 1'b0;
      srv_reg_r <= '0; srv_fail_r <= '0;
      cmd_count_o <= 16'd0; probe_count_o <= 16'd0;
      tx_wedge_cnt_o <= 8'd0; txwd_r <= '0;
      tbl_gnt_o <= 1'b0; tbl_ctx_o <= '0;
      dbg_classify_r <= '0; dbg_fc_r <= '0; dbg_flags_r <= '0; dbg_basehit_r <= '0;
    end else begin
      // ---- post-reset context-table init walk --------------------------
      if (!init_done_r) begin
        if (init_idx_r == IDX_W_C'(N_SINKS_P-1)) init_done_r <= 1'b1;
        else                                     init_idx_r  <= init_idx_r + 1'b1;
      end

      // ---- compatibility shadows (same edge as the RAM write) ----------
      if (wr_en_w) begin
        if (wr_idx_w == IDX_W_C'(0)) view0_r <= wr_data_w;
        if (N_SINKS_P > 1 && wr_idx_w == IDX_W_C'(1)) view1_r <= wr_data_w;
        active_vec_r[wr_idx_w] <= wr_data_w.active;
      end

      // ---- table request/grant port ------------------------------------
      tbl_gnt_o <= w_tbl_ok;
      if (w_tbl_ok) tbl_ctx_o <= rd_ctx_w;

      // ---- sweep cause accumulation + sequencer ------------------------
      begin : sweep_seq
        logic [1:0] mp;
        logic start;
        mp = ms_pend_r;
        if (tick_1ms_r && mp != 2'd3) mp = mp + 2'd1;
        start = init_done_r && !swp_active_r && w_swp_pending;
        if (start) begin
          swp_active_r <= 1'b1;
          swp_idx_r    <= '0;
          c_ms_r       <= (mp != 2'd0);
          c_1s_r       <= s1_pend_r | tick_1s_i;
          c_adp_r      <= adp_pend_r | w_adp_now;
          if (mp != 2'd0) mp = mp - 2'd1;
        end else if (w_swp_run) begin
          //! service SRP snapshots at every visit (self-clears pending)
          srv_reg_r[swp_idx_r]  <= ta_registered_i[swp_idx_r];
          srv_fail_r[swp_idx_r] <= ta_failed_i[swp_idx_r];
          if (swp_probe_set_w) probe_pend_r[swp_idx_r] <= 1'b1;
          if (swp_idx_r == IDX_W_C'(N_SINKS_P-1)) swp_active_r <= 1'b0;
          else                                    swp_idx_r    <= swp_idx_r + 1'b1;
        end
        ms_pend_r  <= mp;
        s1_pend_r  <= (tick_1s_i | s1_pend_r) & ~start;
        adp_pend_r <= (w_adp_now | adp_pend_r) & ~start;
      end

      // ================= frame engine ===================================

      //! ALWAYS-ARMED capture (07-18 silicon deafness): field captures run
      //! in CLASSIFY_S too, so a frame arriving ZERO-GAP behind the one
      //! being classified is not lost. During RESPOND_S/PROBE_S capture
      //! stays off to protect the fword echo source.
      if (init_done_r && rxv_r && (st_r == COLLECT_S || st_r == CLASSIFY_S)) begin
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
              //! COLLECT -> classify + latch the addressed context; a frame
              //! ENDING during CLASSIFY (runt) is dropped
              if (st_r == COLLECT_S) begin
                st_r      <= CLASSIFY_S;
                cur_r     <= rd_ctx_w;     // w_frame_latch owns the read port
                cur_idx_r <= w_luid_idx;
              end
            end
      end

      case (st_r)
        COLLECT_S: begin
          if (w_launch_ok) begin
            //! probe launch: snapshot the context, arm NO_RESP (RAM write
            //! this same cycle via the write-port mux)
            probe_pend_r[launch_idx_w] <= 1'b0;
            probe_count_o <= probe_count_o + 16'd1;
            cur_r     <= rd_ctx_w;
            cur_idx_r <= launch_idx_w;
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

          // ---- ADP watch: latch the event for the sweep ---------------
          if (w_adp_seen) begin
            adp_eid_r   <= cap_sid_r;    // entity_id at wire byte 18
            adp_avail_r <= (cap_msg_r == 4'd0);
          end

          if (w_lstn_hit) begin
            cmd_count_o   <= cmd_count_o + 16'd1;
            resp_msg_r    <= {w_msg[3:1], 1'b1};
            resp_status_r <= w_uid_valid ? ACMP_STATUS_SUCCESS_C
                                         : ACMP_STATUS_LISTENER_UNKNOWN_ID_C;
            unique case (w_msg)
              ACMP_CONNECT_RX_COMMAND_C:    resp_kind_r <= L_RESP_BIND_E;
              ACMP_DISCONNECT_RX_COMMAND_C: resp_kind_r <= L_RESP_UNBIND_E;
              default:                      resp_kind_r <= L_RESP_STATE_E;
            endcase
            //! probe_pend set here; the context writeback happens through
            //! the write-port mux (classify_writeback) this same cycle
            if (probe_set_w) probe_pend_r[cur_idx_r] <= 1'b1;
            beat_r <= '0;
            st_r   <= RESPOND_S;
          end else begin
            // probe answers write back through the mux; no response frame
            st_r <= COLLECT_S;
          end
        end

        RESPOND_S, PROBE_S: begin
          if (m_axis_tready) begin
            txwd_r <= '0;
            if (beat_r == NUM_BEATS_C-1) begin
              // post-increment the probe sequence per emission
              if (st_r == PROBE_S) probe_seq_r <= probe_seq_r + 16'd1;
              wbeat_r <= '0; ovfl_r <= 1'b0;
              beat_r <= '0;
              st_r <= COLLECT_S;
            end else begin
              beat_r <= beat_r + 4'd1;
            end
          end
          else if (txwd_r == TXWD_MAX_C) begin
            //! grant never came: drop the frame, stay alive (07-18 walker)
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

  assign dbg_o = {dbg_classify_r, dbg_fc_r, dbg_flags_r, dbg_basehit_r};

endmodule

`default_nettype wire
