/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_response_builder.sv
  Description : AECP AEM/MVU response engine — the entity's command brain.

                Consumes the validated/parsed command stream, captures the
                command-specific payload into a byte buffer (this absorbs the
                planned KL_aecp_cmd_specific_extract stage: one generic
                capture + per-command combinational decode), classifies the
                command, applies SET_* write-backs to the AEM store, and
                serialises the full response Ethernet frame (little lane
                order, tdata[7:0] = first wire byte — the MAC convention).

                Implemented command set (Milan v1.2 baseline):
                  READ_DESCRIPTOR                      (5-descriptor model)
                  LOCK_ENTITY (+UNLOCK, 60 s timeout)  ACQUIRE -> NOT_SUPPORTED
                  ENTITY_AVAILABLE
                  GET/SET_CONFIGURATION                (single configuration)
                  GET/SET_NAME                         (write-back to store)
                  GET/SET_SAMPLING_RATE                (validated, write-back)
                  GET/SET_STREAM_FORMAT                (validated, write-back)
                  GET_STREAM_INFO                      GET_AVB_INFO
                  REGISTER/DEREGISTER_UNSOLICITED      (accepted; no push yet)
                  MVU GET_MILAN_INFO                   (protocol_id checked)
                Everything else answers NOT_IMPLEMENTED with the command
                payload echoed (clamped to the capture buffer).

                Response payloads are emitted from up to 4 SEGMENTS, each
                sourced from the echo buffer, the AEM store (through the
                dynamic overlay mux), or a constants scratch register; the
                (segment, offset) for a payload byte is resolved from
                cumulative segment lengths, so empty segments cost nothing.
                The byte engine runs a 2-cycle cadence (address, data) — a
                worst-case READ_DESCRIPTOR(ENTITY) response is ~7 us at
                100 MHz, far inside any controller timeout.

  Spec refs   : IEEE Std 1722.1-2021 §7.4, §9.2; Milan v1.2 §5.4
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_response_builder (
  input  wire          clk_i,
  input  wire          rst_n,
  input  wire          enable_i,           //! entity enable (CSR, same as ADP)

  // ---- command side --------------------------------------------------
  input  aecp_hdr_t    hdr_i,              //! from common_parser (hdr_valid)
  input  wire          mismatch_i,         //! parser: target != our entity_id
  input  wire          frame_ok_i,         //! validator: good frame complete
  input  wire          frame_bad_i,        //! validator: frame dropped
  input  wire [3:0]    message_type_i,     //! validator: latched message_type
  input  wire          s_axis_tvalid,
  output logic         s_axis_tready,
  input  wire [63:0]   s_axis_tdata,
  input  wire [7:0]    s_axis_tkeep,
  input  wire          s_axis_tlast,

  // ---- per-frame requester MAC (tap meta FIFO, [47:40]=first wire byte)
  input  wire [47:0]   req_src_mac_i,
  input  wire          req_meta_valid_i,
  output logic         req_meta_pop_o,

  // ---- entity state ---------------------------------------------------
  input  aecp_l0_state_t l0_state_i,
  input  wire [4:0]    l0_status_i,        //! valid during hdr_valid
  input  wire          l0_reject_i,

  // ---- live identity (CSR 0x600 group; [47:40]=first wire byte for MACs)
  input  wire [47:0]   station_mac_i,
  input  wire [63:0]   entity_id_i,
  input  wire [63:0]   gptp_gm_id_i,
  input  wire [7:0]    gptp_domain_i,

  // ---- live talker stream state (docs/design/MILAN_TALKER_SM.md) ------
  input  wire [47:0]   aaf_dmac_i,         //! stream dest MAC (the framer's)
  input  wire [11:0]   aaf_vid_i,          //! stream VLAN id
  input  wire          talker_active_i,    //! ACMP probe SM: declaring
  input  wire          listener_observed_i,//! lwSRP registrar hook
  input  wire [31:0]   pres_offset_i,      //! msrp_accumulated_latency (ns)
  output logic         pres_wr_p_o,        //! 1-cycle: SET_STREAM_INFO update
  output logic [31:0]  pres_wr_val_o,

  // ---- AEM store (read data arrives THROUGH KL_aecp_aem_dyn_mux) ------
  output logic [15:0]  st_addr_o,
  output logic         st_rd_o,
  input  wire  [7:0]   st_byte_i,          //! overlaid read byte (1-cycle lat)
  output logic [15:0]  st_waddr_o,
  output logic         st_wr_o,
  output logic [7:0]   st_wdata_o,

  // ---- response frame out (little lane order, full Ethernet frame) ----
  output logic [63:0]  m_axis_tdata,
  output logic [7:0]   m_axis_tkeep,
  output logic         m_axis_tvalid,
  output logic         m_axis_tlast,
  input  wire          m_axis_tready,

  // ---- events ----------------------------------------------------------
  output logic         evt_cmd_o,          //! good command frame received
  output logic         evt_resp_o,         //! response frame sent
  output logic         evt_drop_o          //! frame discarded (bad/mismatch)
);

  `include "gen/aecp_aem_rom.svh"

  // ------------------------------------------------------------------ //
  // Payload capture: stripped-frame bytes 24..151 -> buf_r[0..127]       //
  // (byte 24 = AEM u/command_type hi; AEM payload starts at buf[2])      //
  // ------------------------------------------------------------------ //
  localparam int unsigned BUF_BYTES_C = 128;

  logic [7:0]  buf_r [0:BUF_BYTES_C-1];
  logic [4:0]  beat_r;                     //! frame beat counter (sat at 31)

  wire w_cap_hs = s_axis_tvalid & s_axis_tready;

  // ------------------------------------------------------------------ //
  // FSM                                                                  //
  // ------------------------------------------------------------------ //
  typedef enum logic [3:0] {
    IDLE_S, CAPTURE_S, DECIDE_S, WRITE_S, EMIT_ADDR_S, EMIT_DATA_S,
    CONCLUDE_S
  } state_t;
  state_t state_r;

  //! accept command beats only while idle/capturing (backpressures the
  //! pipeline — and therefore the tap FIFO — while a response is in flight)
  assign s_axis_tready = (state_r == IDLE_S) || (state_r == CAPTURE_S);

  // latched command context
  aecp_hdr_t   hdr_q;
  logic [4:0]  l0_status_q;
  logic        l0_reject_q;
  logic        discard_q;                  //! mismatch/disabled -> no response
  logic        vu_q;                       //! vendor-unique frame

  // ------------------------------------------------------------------ //
  // Command decode (combinational over the capture buffer; DECIDE_S runs //
  // one cycle after the final beat was written, so buf_r is complete)    //
  // ------------------------------------------------------------------ //
  wire [15:0] w_rd_cfg   = {buf_r[2], buf_r[3]};   //! READ_DESCRIPTOR config
  wire [15:0] w_rd_type  = {buf_r[6], buf_r[7]};
  wire [15:0] w_rd_index = {buf_r[8], buf_r[9]};
  wire [15:0] w_gs_type  = {buf_r[2], buf_r[3]};   //! GET/SET_* desc type
  wire [15:0] w_gs_index = {buf_r[4], buf_r[5]};
  //! SET_STREAM_INFO (Milan §5.4.2.9): payload byte n = buf_r[n+2] — flags at
  //! payload 4-7, msrp_accumulated_latency at payload 24-27.
  wire [31:0] w_si_flags = {buf_r[6],  buf_r[7],  buf_r[8],  buf_r[9]};
  wire [31:0] w_si_lat   = {buf_r[26], buf_r[27], buf_r[28], buf_r[29]};
  //! Spec-defined sub-command bits (reference valid_mask: aecp-aem.h bits 0-9
  //! + 25-31) minus the ONE supported (MSRP_ACC_LAT_VALID, bit 29): any of
  //! these requested -> NOT_SUPPORTED for the whole command (§5.4.2.9).
  localparam [31:0] SI_UNSUPPORTED_MASK_C = 32'hDE00_03FF;
  wire [15:0] w_name_idx = {buf_r[6], buf_r[7]};   //! SET/GET_NAME name_index
  wire [15:0] w_as_path_idx = {buf_r[2], buf_r[3]};  //! GET_AS_PATH descriptor_index (no type field)
  wire [15:0] w_name_cfg = {buf_r[8], buf_r[9]};
  wire [31:0] w_set_rate = {buf_r[6], buf_r[7], buf_r[8], buf_r[9]};
  wire [63:0] w_set_fmt  = {buf_r[6], buf_r[7], buf_r[8],  buf_r[9],
                            buf_r[10], buf_r[11], buf_r[12], buf_r[13]};
  //! VU frames have NO u/command_type after sequence_id: buf_r[0..5] =
  //! protocol_id, buf_r[6:7] = command_type, buf_r[8:9] = reserved,
  //! buf_r[10..] = command payload (AEM frames instead put command_type in
  //! buf_r[0:1] and the payload in buf_r[2..]).
  wire        w_vu_proto_ok =
      (buf_r[0] == MILAN_PROTOCOL_ID_C[47:40]) &&
      (buf_r[1] == MILAN_PROTOCOL_ID_C[39:32]) &&
      (buf_r[2] == MILAN_PROTOCOL_ID_C[31:24]) &&
      (buf_r[3] == MILAN_PROTOCOL_ID_C[23:16]) &&
      (buf_r[4] == MILAN_PROTOCOL_ID_C[15:8])  &&
      (buf_r[5] == MILAN_PROTOCOL_ID_C[7:0]);
  wire [14:0] w_vu_cmd = {buf_r[6][6:0], buf_r[7]};

  //! descriptor lookup — inputs muxed combinationally by command layout
  wire w_is_read_desc = !vu_q && (hdr_q.command_type == CMD_READ_DESCRIPTOR);
  wire [15:0] acc_type  = w_is_read_desc ? w_rd_type  : w_gs_type;
  wire [15:0] acc_index = w_is_read_desc ? w_rd_index : w_gs_index;
  wire         acc_found;
  wire [15:0]  acc_base, acc_len;
  KL_aecp_accessor u_acc (
    .config_idx_i (16'd0),
    .desc_type_i  (acc_type),
    .desc_index_i (acc_index),
    .found_o      (acc_found),
    .base_o       (acc_base),
    .len_o        (acc_len)
  );

  //! SET/GET_NAME write-back address for (desc_type, name_index)
  function automatic [16:0] name_addr(input [15:0] t, input [15:0] nidx);
    name_addr = 17'd0;   // {valid, addr}
    case (t)
      DESC_ENTITY:
        if (nidx == 16'd0)      name_addr = {1'b1, WB_NAME_ENTITY_0_C};
        else if (nidx == 16'd1) name_addr = {1'b1, WB_NAME_ENTITY_1_C};
      DESC_CONFIGURATION: if (nidx == 16'd0) name_addr = {1'b1, WB_NAME_CONFIG_C};
      DESC_AUDIO_UNIT:    if (nidx == 16'd0) name_addr = {1'b1, WB_NAME_AUDIO_C};
      DESC_STREAM_OUTPUT: if (nidx == 16'd0) name_addr = {1'b1, WB_NAME_STREAM_C};
      DESC_AVB_INTERFACE: if (nidx == 16'd0) name_addr = {1'b1, WB_NAME_AVBIF_C};
      default: name_addr = 17'd0;
    endcase
  endfunction

  // function result captured in a net: indexing a call expression directly
  // (name_addr(...)[16]) is SV-only — sv2v keeps it and Yosys' V2005 reader
  // rejects it, breaking the open-toolchain portability gate.
  wire [16:0] w_name_ptr = name_addr(w_gs_type, w_name_idx);   //! {valid, wb addr}

  wire w_rate_ok = (w_set_rate == AEM_RATES_C[0]) ||
                   (w_set_rate == AEM_RATES_C[1]) ||
                   (w_set_rate == AEM_RATES_C[2]);
  wire w_fmt_ok  = (w_set_fmt == AEM_FMTS_C[0]) ||
                   (w_set_fmt == AEM_FMTS_C[1]) ||
                   (w_set_fmt == AEM_FMTS_C[2]);

  // ------------------------------------------------------------------ //
  // Response plan (filled in DECIDE_S)                                   //
  // ------------------------------------------------------------------ //
  typedef enum logic [1:0] { SEG_NONE, SEG_ECHO, SEG_STORE, SEG_CONST } seg_kind_t;

  seg_kind_t   seg_kind_q [0:3];
  logic [15:0] seg_addr_q [0:3];   //! ECHO: buf offset · STORE: store addr · CONST: const offset
  logic [15:0] seg_len_q  [0:3];
  logic [7:0]  const_q [0:63];   //! scratch for CONST segments (GET_STREAM_INFO
                                 //! needs 40: stream_id + msrp/mac/vlan/flags_ex/sta)
  logic [10:0] cdl_q;
  logic [4:0]  status_q;
  logic [3:0]  msg_resp_q;
  logic [47:0] dst_mac_q;

  //! cumulative payload offsets (registered one cycle after DECIDE_S)
  logic [15:0] cum_q [0:3];        //! start offset of each segment
  logic [15:0] pay_len_q;
  logic        cum_done_q;

  // write-back plan
  logic [15:0] wb_addr_q;
  logic [6:0]  wb_len_q;
  logic [6:0]  wb_src_q;
  logic [6:0]  wb_cnt_r;

  // ------------------------------------------------------------------ //
  // Emit engine                                                          //
  // ------------------------------------------------------------------ //
  localparam [15:0] HDR_AEM_C = 16'd38;
  localparam [15:0] HDR_VU_C  = 16'd36;
  wire [15:0] w_hdr_len   = vu_q ? HDR_VU_C : HDR_AEM_C;
  wire [15:0] w_frame_len = w_hdr_len + pay_len_q;

  logic [15:0] fi_r;               //! frame byte index
  logic [7:0]  emit_byte_r;        //! byte resolved in EMIT_ADDR/DATA

  //! payload byte index -> (segment, offset within segment)
  wire [15:0] w_pi = fi_r - w_hdr_len;
  logic [1:0]  w_seg;
  logic [15:0] w_soff;
  always_comb begin
    w_seg  = 2'd0;
    w_soff = w_pi;
    if      (w_pi >= cum_q[3]) begin w_seg = 2'd3; w_soff = w_pi - cum_q[3]; end
    else if (w_pi >= cum_q[2]) begin w_seg = 2'd2; w_soff = w_pi - cum_q[2]; end
    else if (w_pi >= cum_q[1]) begin w_seg = 2'd1; w_soff = w_pi - cum_q[1]; end
  end

  //! Store READ port is COMBINATIONAL: presenting the address in EMIT_ADDR_S
  //! (and holding it through EMIT_DATA_S) gives 1-cycle data latency that lands
  //! exactly on EMIT_DATA_S. A registered address would add a second cycle and
  //! deliver a stale byte. The write port stays registered (WRITE_S).
  wire w_emit_store = (state_r == EMIT_ADDR_S || state_r == EMIT_DATA_S) &&
                      (fi_r >= w_hdr_len) && (seg_kind_q[w_seg] == SEG_STORE);
  assign st_addr_o = seg_addr_q[w_seg] + w_soff;
  assign st_rd_o   = w_emit_store;

  // byte -> beat packer
  logic [63:0] pack_r;
  logic [2:0]  pack_n_r;
  logic        beat_pend_r;
  logic        beat_last_r;
  logic [7:0]  beat_keep_r;

  assign m_axis_tvalid = beat_pend_r;
  assign m_axis_tdata  = pack_r;
  assign m_axis_tkeep  = beat_keep_r;
  assign m_axis_tlast  = beat_last_r;

  //! frame header byte generator (bytes 0..37 AEM / 0..35 VU)
  function automatic [7:0] hdr_byte(input [15:0] fi);
    logic [7:0] b;
    b = 8'h00;
    if      (fi <  6) b = dst_mac_q[8*(5-(32)'(fi)) +: 8];
    else if (fi < 12) b = station_mac_i[8*(11-(32)'(fi)) +: 8];
    else if (fi == 12) b = 8'h22;
    else if (fi == 13) b = 8'hF0;
    else if (fi == 14) b = AECP_SUBTYPE_C;
    else if (fi == 15) b = {4'b0000, msg_resp_q};
    else if (fi == 16) b = {status_q, cdl_q[10:8]};
    else if (fi == 17) b = cdl_q[7:0];
    else if (fi < 26) b = entity_id_i[8*(25-(32)'(fi)) +: 8];
    else if (fi < 34) b = hdr_q.controller_entity_id[8*(33-(32)'(fi)) +: 8];
    else if (fi == 34) b = hdr_q.sequence_id[15:8];
    else if (fi == 35) b = hdr_q.sequence_id[7:0];
    else if (fi == 36) b = {unsol_frame_r, hdr_q.command_type[14:8]};  // u=1 on pushes
    else               b = hdr_q.command_type[7:0];
    return b;
  endfunction

  //! Emit byte-select PIPELINE registers. EMIT_ADDR_S resolves the byte
  //! source for fi_r (header byte, or segment kind/addr/offset) and REGISTERS
  //! it; EMIT_DATA_S then only muxes registered values plus the store byte
  //! (whose 1-cycle read latency lands on EMIT_DATA). This keeps the deep
  //! fi -> {cumulative-offset arithmetic, positional header mux} cone OFF the
  //! path into pack_r, which is the 100 MHz critical path.
  logic        is_hdr_r;
  logic [7:0]  hdrbyte_r;
  seg_kind_t   emseg_kind_r;
  logic [15:0] emseg_addr_r;
  logic [15:0] emsoff_r;

  //! meta-FIFO pop bookkeeping: pops can be requested by a concluded
  //! response AND an asynchronously dropped frame in the same cycle
  logic [1:0] pop_pend_r;

  // ------------------------------------------------------------------ //
  // Unsolicited notifications (Milan §5.4.2.21 / IEEE 1722.1-2021 §7.5.2)
  // 4-slot registration table (reference uses 16; 4 bounds the fabric and
  // covers the bench). A push is a synthesized GET_STREAM_INFO response
  // (u=1) emitted through the NORMAL segment engine from the IDLE hook —
  // per registered controller, UNICAST to its stored MAC, with its own
  // per-controller sequence counter (reference reply-unsol-helpers.c).
  // ------------------------------------------------------------------ //
  localparam int unsigned UNSOL_SLOTS_C = 4;
  logic                  unsol_valid_r [0:UNSOL_SLOTS_C-1];
  logic [63:0]           unsol_eid_r   [0:UNSOL_SLOTS_C-1];
  logic [47:0]           unsol_mac_r   [0:UNSOL_SLOTS_C-1];
  logic [15:0]           unsol_seq_r   [0:UNSOL_SLOTS_C-1];
  logic [UNSOL_SLOTS_C-1:0] unsol_pend_r;   //! slots owed a push
  logic                  unsol_frame_r;     //! current emit is a push (u=1, no meta pop)
  logic                  ta_prev_r, lo_prev_r;  //! edge detectors

  //! REGISTER helper wires: dedup match + lowest free slot + lowest pend
  logic [UNSOL_SLOTS_C-1:0] w_unsol_match;
  logic [UNSOL_SLOTS_C-1:0] w_unsol_free;
  logic [1:0]               w_unsol_fill_idx;   //! lowest free slot
  logic [1:0]               w_unsol_push_idx;   //! lowest pending slot
  always_comb begin
    for (int s = 0; s < UNSOL_SLOTS_C; s++) begin
      w_unsol_match[s] = unsol_valid_r[s] &&
                         (unsol_eid_r[s] == hdr_q.controller_entity_id);
      w_unsol_free[s]  = !unsol_valid_r[s];
    end
    w_unsol_fill_idx = 2'd0;
    w_unsol_push_idx = 2'd0;
    for (int s = UNSOL_SLOTS_C-1; s >= 0; s--) begin
      if (w_unsol_free[s]) w_unsol_fill_idx = 2'(s);   // lowest wins
      if (unsol_pend_r[s]) w_unsol_push_idx = 2'(s);
    end
  end

  // ------------------------------------------------------------------ //
  // Stream-info payload constants (shared by the GET_STREAM_INFO command
  // path and the unsolicited push): flags + the live 40-byte tail. The
  // caller still owns segments/cdl/status.                               //
  // ------------------------------------------------------------------ //
  task automatic load_stream_info_consts;
    begin
      const_q[0] <= 8'hF6; const_q[1] <= 8'h00;   // flags 0xF6000000
      const_q[2] <= 8'h00; const_q[3] <= 8'h00;
      // stream_id = {station_mac, unique_id=0} — the stream.c formula,
      // byte-identical to the AVTP header and the ACMP PROBE_TX response
      const_q[8]  <= station_mac_i[47:40];
      const_q[9]  <= station_mac_i[39:32];
      const_q[10] <= station_mac_i[31:24];
      const_q[11] <= station_mac_i[23:16];
      const_q[12] <= station_mac_i[15:8];
      const_q[13] <= station_mac_i[7:0];
      const_q[14] <= 8'h00; const_q[15] <= 8'h00;
      const_q[16] <= pres_offset_i[31:24];        // msrp_accumulated_latency
      const_q[17] <= pres_offset_i[23:16];
      const_q[18] <= pres_offset_i[15:8];
      const_q[19] <= pres_offset_i[7:0];
      const_q[20] <= aaf_dmac_i[47:40];           // stream_dest_mac
      const_q[21] <= aaf_dmac_i[39:32];
      const_q[22] <= aaf_dmac_i[31:24];
      const_q[23] <= aaf_dmac_i[23:16];
      const_q[24] <= aaf_dmac_i[15:8];
      const_q[25] <= aaf_dmac_i[7:0];
      for (int k = 26; k < 36; k++) const_q[k] <= 8'h00;  // fail code + bridge
      const_q[36] <= {4'h0, aaf_vid_i[11:8]};     // stream_vlan_id
      const_q[37] <= aaf_vid_i[7:0];
      const_q[38] <= 8'h00; const_q[39] <= 8'h00;
      const_q[40] <= 8'h00; const_q[41] <= 8'h00; const_q[42] <= 8'h00;
      const_q[43] <= {7'b0, talker_active_i & listener_observed_i};
      for (int k = 44; k < 48; k++) const_q[k] <= 8'h00;  // pbsta/acmpsta
    end
  endtask

  // ------------------------------------------------------------------ //
  // Main FSM                                                             //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      state_r      <= IDLE_S;
      beat_r       <= 5'd0;
      discard_q    <= 1'b0;
      vu_q         <= 1'b0;
      hdr_q        <= '0;
      l0_status_q  <= STATUS_SUCCESS;
      l0_reject_q  <= 1'b0;
      cdl_q        <= 11'd0;
      status_q     <= STATUS_SUCCESS;
      msg_resp_q   <= MSG_AEM_RESPONSE;
      dst_mac_q    <= 48'd0;
      fi_r         <= 16'd0;
      emit_byte_r  <= 8'd0;
      is_hdr_r     <= 1'b0;
      hdrbyte_r    <= 8'd0;
      emseg_kind_r <= SEG_NONE;
      emseg_addr_r <= 16'd0;
      emsoff_r     <= 16'd0;
      pack_r       <= 64'd0;
      pack_n_r     <= 3'd0;
      beat_pend_r  <= 1'b0;
      beat_last_r  <= 1'b0;
      beat_keep_r  <= 8'd0;
      wb_addr_q    <= 16'd0;
      wb_len_q     <= 7'd0;
      wb_src_q     <= 7'd0;
      wb_cnt_r     <= 7'd0;
      st_wr_o      <= 1'b0;
      st_waddr_o   <= 16'd0;
      st_wdata_o   <= 8'd0;
      req_meta_pop_o <= 1'b0;
      pop_pend_r   <= 2'd0;
      evt_cmd_o    <= 1'b0;
      evt_resp_o   <= 1'b0;
      evt_drop_o   <= 1'b0;
      pres_wr_p_o  <= 1'b0;
      pres_wr_val_o <= 32'd0;
      unsol_pend_r  <= '0;
      unsol_frame_r <= 1'b0;
      ta_prev_r     <= 1'b0;
      lo_prev_r     <= 1'b0;
      for (int s = 0; s < UNSOL_SLOTS_C; s++) begin
        unsol_valid_r[s] <= 1'b0;
        unsol_eid_r[s]   <= 64'd0;
        unsol_mac_r[s]   <= 48'd0;
        unsol_seq_r[s]   <= 16'd0;
      end
      pay_len_q    <= 16'd0;
      cum_done_q   <= 1'b0;
      for (int k = 0; k < BUF_BYTES_C; k++) buf_r[k] <= 8'h00;
      for (int k = 0; k < 64; k++) const_q[k] <= 8'h00;
      for (int s = 0; s < 4; s++) begin
        seg_kind_q[s] <= SEG_NONE;
        seg_addr_q[s] <= 16'd0;
        seg_len_q[s]  <= 16'd0;
        cum_q[s]      <= 16'd0;
      end
    end else begin
      // default strobes
      evt_cmd_o  <= 1'b0;
      evt_resp_o <= 1'b0;
      evt_drop_o <= 1'b0;
      st_wr_o    <= 1'b0;
      pres_wr_p_o <= 1'b0;

      // ---- output beat handshake (runs EVERY cycle, independent of the
      //      ADDR/DATA assembly sub-state, so a beat transfers exactly once) --
      if (beat_pend_r && m_axis_tready) begin
        beat_pend_r <= 1'b0;
        beat_last_r <= 1'b0;
      end

      // ---- meta pop service (one per cycle) --------------------------
      req_meta_pop_o <= 1'b0;
      if (pop_pend_r != 2'd0 && req_meta_valid_i && !req_meta_pop_o) begin
        req_meta_pop_o <= 1'b1;
        pop_pend_r     <= pop_pend_r - 2'd1;
      end

      // ---- frames the validator dropped never reach the FSM ----------
      if (frame_bad_i) begin
        evt_drop_o <= 1'b1;
        pop_pend_r <= pop_pend_r + 2'd1;
      end

      // ---- unsolicited push triggers (stream-output state changes) ---
      // Edge of the ACMP probe/listener state -> notify every registered
      // controller; a SET_STREAM_INFO write -> notify all EXCEPT the
      // controller that issued it (reference reply-unsol-helpers.c rule).
      ta_prev_r <= talker_active_i;
      lo_prev_r <= listener_observed_i;
      if ((talker_active_i ^ ta_prev_r) | (listener_observed_i ^ lo_prev_r)) begin
        for (int s = 0; s < UNSOL_SLOTS_C; s++)
          if (unsol_valid_r[s]) unsol_pend_r[s] <= 1'b1;
      end
      if (pres_wr_p_o) begin   // hdr_q still holds the causing SET command
        for (int s = 0; s < UNSOL_SLOTS_C; s++)
          if (unsol_valid_r[s] &&
              unsol_eid_r[s] != hdr_q.controller_entity_id)
            unsol_pend_r[s] <= 1'b1;
      end

      // ---------------- capture (runs in IDLE/CAPTURE) ----------------
      if (w_cap_hs) begin
        if (beat_r >= 5'd3 && beat_r < 5'd19) begin
          for (int k = 0; k < 8; k++)
            buf_r[((32)'(beat_r) - 3) * 8 + k] <= s_axis_tdata[8*(7-k) +: 8];
        end
        beat_r <= s_axis_tlast ? 5'd0 : (beat_r == 5'd31 ? 5'd31 : beat_r + 5'd1);
      end

      if (hdr_i.hdr_valid && (state_r == IDLE_S || state_r == CAPTURE_S)) begin
        hdr_q       <= hdr_i;
        l0_status_q <= l0_status_i;
        l0_reject_q <= l0_reject_i;
        vu_q        <= (message_type_i == MSG_VENDOR_UNIQUE_COMMAND);
        if (mismatch_i || !enable_i) discard_q <= 1'b1;
      end

      // ---- cumulative segment offsets, one cycle after DECIDE --------
      if (!cum_done_q && state_r == WRITE_S) begin
        // WRITE_S lasts >= 4 cycles, plenty; compute once
        cum_q[0]   <= 16'd0;
        cum_q[1]   <= seg_len_q[0];
        cum_q[2]   <= seg_len_q[0] + seg_len_q[1];
        cum_q[3]   <= seg_len_q[0] + seg_len_q[1] + seg_len_q[2];
        pay_len_q  <= seg_len_q[0] + seg_len_q[1] + seg_len_q[2] + seg_len_q[3];
        cum_done_q <= 1'b1;
      end

      case (state_r)
        // ---------------------------------------------------------- //
        IDLE_S: begin
          discard_q <= !enable_i;
          unsol_frame_r <= 1'b0;
          if (w_cap_hs) begin
            state_r <= CAPTURE_S;
          end else if (enable_i && unsol_pend_r != '0) begin
            // Synthesize an unsolicited GET_STREAM_INFO response (u=1) to
            // the lowest pending slot, through the NORMAL segment engine:
            // send with the slot's current sequence, then bump (reference
            // sends next_seq_id and post-increments).
            unsol_pend_r[w_unsol_push_idx] <= 1'b0;
            unsol_seq_r[w_unsol_push_idx]  <= unsol_seq_r[w_unsol_push_idx] + 16'd1;
            unsol_frame_r <= 1'b1;
            dst_mac_q     <= unsol_mac_r[w_unsol_push_idx];
            hdr_q.controller_entity_id <= unsol_eid_r[w_unsol_push_idx];
            hdr_q.sequence_id          <= unsol_seq_r[w_unsol_push_idx];
            hdr_q.command_type         <= CMD_GET_STREAM_INFO;
            vu_q       <= 1'b0;
            msg_resp_q <= MSG_AEM_RESPONSE;
            status_q   <= STATUS_SUCCESS;
            seg_kind_q[0] <= SEG_CONST; seg_addr_q[0] <= 16'd48; seg_len_q[0] <= 16'd4;
            seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0;  seg_len_q[1] <= 16'd4;
            seg_kind_q[2] <= SEG_STORE;
            seg_addr_q[2] <= WB_STREAM_FORMAT_C; seg_len_q[2] <= 16'd8;
            seg_kind_q[3] <= SEG_CONST; seg_addr_q[3] <= 16'd8;  seg_len_q[3] <= 16'd40;
            const_q[48] <= 8'h00; const_q[49] <= 8'h06;   // STREAM_OUTPUT
            const_q[50] <= 8'h00; const_q[51] <= 8'h00;   // index 0
            load_stream_info_consts();
            cdl_q      <= 11'd68;
            wb_len_q   <= 7'd0; wb_cnt_r <= 7'd0;
            cum_done_q <= 1'b0;
            fi_r       <= 16'd0;
            state_r    <= WRITE_S;
          end
        end

        // ---------------------------------------------------------- //
        CAPTURE_S: begin
          if (frame_ok_i) begin
            if (discard_q) begin
              evt_drop_o <= 1'b1;
              pop_pend_r <= pop_pend_r + 2'd1;
              discard_q  <= 1'b0;
              state_r    <= IDLE_S;
            end else begin
              evt_cmd_o <= 1'b1;
              dst_mac_q <= req_src_mac_i;
              state_r   <= DECIDE_S;
            end
          end
        end

        // ---------------------------------------------------------- //
        DECIDE_S: begin
          // defaults: NOT_IMPLEMENTED echo of the command payload
          for (int s = 0; s < 4; s++) begin
            seg_kind_q[s] <= SEG_NONE; seg_addr_q[s] <= 16'd0; seg_len_q[s] <= 16'd0;
          end
          msg_resp_q <= vu_q ? MSG_VENDOR_UNIQUE_RESPONSE : MSG_AEM_RESPONSE;
          status_q   <= STATUS_NOT_IMPLEMENTED;
          seg_kind_q[0] <= SEG_ECHO;
          seg_addr_q[0] <= 16'd2;
          seg_len_q[0]  <= (hdr_q.control_data_length > 11'd12)
                           ? ((hdr_q.control_data_length > 11'd138)
                              ? 16'd126
                              : 16'(hdr_q.control_data_length) - 16'd12)
                           : 16'd0;
          cdl_q      <= hdr_q.control_data_length;
          cum_done_q <= 1'b0;
          wb_len_q   <= 7'd0;
          wb_cnt_r   <= 7'd0;
          state_r    <= WRITE_S;   // WRITE_S is a no-op when wb_len_q == 0

          if (vu_q) begin
            if (!w_vu_proto_ok) begin
              // not Milan MVU: ignore silently
              evt_drop_o <= 1'b1;
              pop_pend_r <= pop_pend_r + 2'd1;
              state_r    <= IDLE_S;
            end else if (w_vu_cmd == VU_GET_MILAN_INFO) begin
              status_q      <= STATUS_SUCCESS;
              seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd0;  seg_len_q[0] <= 16'd10;
              seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0;  seg_len_q[1] <= 16'd12;
              const_q[0] <= 8'h00; const_q[1] <= 8'h00;   // protocol_version = 1
              const_q[2] <= 8'h00; const_q[3] <= 8'h01;
              const_q[4] <= 8'h00; const_q[5] <= 8'h00;   // features_flags = 0
              const_q[6] <= 8'h00; const_q[7] <= 8'h00;
              // certification_version MUST stay 0 until AVnu-certified (the
              // pipewire module-avb reference forces 0 with a CRITICAL comment;
              // a non-zero value falsely claims certification).
              const_q[8] <= 8'h00; const_q[9] <= 8'h00;
              const_q[10] <= 8'h00; const_q[11] <= 8'h00;
              cdl_q <= 11'd32;    // ctlr(8)+seq(2)+proto/cmd/rsvd(10)+info(12)
            end else begin
              // NOT_IMPLEMENTED: echo protocol_id + command_type + reserved
              seg_addr_q[0] <= 16'd0;
              seg_len_q[0]  <= 16'd10;
              cdl_q         <= 11'd20;
            end
          end else begin
            case (hdr_q.command_type)
              // -------------------------------------------------- //
              CMD_ACQUIRE_ENTITY, CMD_LOCK_ENTITY: begin
                status_q      <= l0_status_q;  // NOT_SUPPORTED/LOCKED/SUCCESS
                seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2;  seg_len_q[0] <= 16'd4;
                seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0;  seg_len_q[1] <= 16'd8;
                seg_kind_q[2] <= SEG_ECHO;  seg_addr_q[2] <= 16'd14; seg_len_q[2] <= 16'd4;
                for (int k = 0; k < 8; k++)
                  const_q[k] <= (hdr_q.command_type == CMD_LOCK_ENTITY)
                    ? l0_state_i.locking_controller_id[8*(7-k) +: 8] : 8'h00;
                cdl_q <= 11'd28;
              end

              // -------------------------------------------------- //
              CMD_ENTITY_AVAILABLE: begin
                status_q      <= STATUS_SUCCESS;
                seg_kind_q[0] <= SEG_NONE; seg_len_q[0] <= 16'd0;
                cdl_q         <= 11'd12;
              end

              // -------------------------------------------------- //
              CMD_READ_DESCRIPTOR: begin
                if (acc_found && w_rd_cfg == 16'd0) begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_CONST; seg_addr_q[0] <= 16'd16; seg_len_q[0] <= 16'd4;
                  const_q[16] <= buf_r[2]; const_q[17] <= buf_r[3];   // cfg echo
                  const_q[18] <= 8'h00;    const_q[19] <= 8'h00;      // reserved
                  seg_kind_q[1] <= SEG_STORE; seg_addr_q[1] <= acc_base; seg_len_q[1] <= acc_len;
                  cdl_q <= 11'(16 + (32)'(acc_len));
                end else begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd8;
                  cdl_q        <= 11'd20;
                end
              end

              // -------------------------------------------------- //
              CMD_GET_CONFIGURATION, CMD_SET_CONFIGURATION: begin
                status_q <= (hdr_q.command_type == CMD_SET_CONFIGURATION &&
                             l0_reject_q) ? l0_status_q : STATUS_SUCCESS;
                seg_kind_q[0] <= SEG_CONST; seg_addr_q[0] <= 16'd0; seg_len_q[0] <= 16'd4;
                const_q[0] <= 8'h00; const_q[1] <= 8'h00;
                const_q[2] <= l0_state_i.current_configuration_index[15:8];
                const_q[3] <= l0_state_i.current_configuration_index[7:0];
                cdl_q <= 11'd16;
              end

              // -------------------------------------------------- //
              CMD_GET_NAME, CMD_SET_NAME: begin
                cdl_q <= 11'd84;   // 12 + 8 + 64
                if (l0_reject_q) begin
                  status_q     <= l0_status_q;
                  seg_len_q[0] <= (hdr_q.command_type == CMD_SET_NAME)
                                  ? 16'd72 : 16'd8;
                end else if (!acc_found || w_name_cfg != 16'd0 ||
                             !w_name_ptr[16]) begin
                  status_q     <= acc_found ? STATUS_BAD_ARGUMENTS
                                            : STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= (hdr_q.command_type == CMD_SET_NAME)
                                  ? 16'd72 : 16'd8;
                  cdl_q        <= hdr_q.control_data_length;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd8;
                  seg_kind_q[1] <= SEG_STORE;
                  seg_addr_q[1] <= w_name_ptr[15:0];
                  seg_len_q[1]  <= 16'd64;
                  if (hdr_q.command_type == CMD_SET_NAME) begin
                    wb_addr_q <= w_name_ptr[15:0];
                    wb_len_q  <= 7'd64;
                    wb_src_q  <= 7'd10;
                  end
                end
              end

              // -------------------------------------------------- //
              CMD_GET_SAMPLING_RATE, CMD_SET_SAMPLING_RATE: begin
                cdl_q <= 11'd20;   // 12 + 4 + 4
                if (l0_reject_q) begin
                  status_q     <= l0_status_q;
                  seg_len_q[0] <= 16'd8;
                end else if (w_gs_type != DESC_AUDIO_UNIT || w_gs_index != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd8;
                end else if (hdr_q.command_type == CMD_SET_SAMPLING_RATE &&
                             !w_rate_ok) begin
                  status_q     <= STATUS_BAD_ARGUMENTS;
                  seg_len_q[0] <= 16'd8;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_STORE;
                  seg_addr_q[1] <= WB_SAMPLING_RATE_C; seg_len_q[1] <= 16'd4;
                  if (hdr_q.command_type == CMD_SET_SAMPLING_RATE) begin
                    wb_addr_q <= WB_SAMPLING_RATE_C;
                    wb_len_q  <= 7'd4;
                    wb_src_q  <= 7'd6;
                  end
                end
              end

              // -------------------------------------------------- //
              CMD_GET_STREAM_FORMAT, CMD_SET_STREAM_FORMAT: begin
                cdl_q <= 11'd24;   // 12 + 4 + 8
                if (l0_reject_q) begin
                  status_q     <= l0_status_q;
                  seg_len_q[0] <= 16'd12;
                end else if (w_gs_type != DESC_STREAM_OUTPUT || w_gs_index != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd12;
                end else if (hdr_q.command_type == CMD_SET_STREAM_FORMAT &&
                             !w_fmt_ok) begin
                  status_q     <= STATUS_BAD_ARGUMENTS;
                  seg_len_q[0] <= 16'd12;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_STORE;
                  seg_addr_q[1] <= WB_STREAM_FORMAT_C; seg_len_q[1] <= 16'd8;
                  if (hdr_q.command_type == CMD_SET_STREAM_FORMAT) begin
                    wb_addr_q <= WB_STREAM_FORMAT_C;
                    wb_len_q  <= 7'd8;
                    wb_src_q  <= 7'd6;
                  end
                end
              end

              // -------------------------------------------------- //
              // GET_STREAM_INFO: Milan mandates the FIXED 56-byte payload
              // (pipewire cmd-get-set-stream-info.c; la_avdecc rejects any
              // other size as "Incorrect payload size"). STREAM_OUTPUT flags =
              // STREAM_FORMAT_VALID|STREAM_ID_VALID|MSRP_ACC_LAT_VALID|
              // STREAM_DEST_MAC_VALID|CONNECTED|STREAM_VLAN_ID_VALID =
              // 0xF6000000; pbsta=acmpsta=0 for a talker. Layout: type(2)+
              // index(2)+flags(4)+format(8)+stream_id(8)+msrp_lat(4)+dest_mac(6)
              // +msrp_fail(1)+rsvd(1)+bridge(8)+vlan(2)+rsvd(2)+flags_ex(4)+
              // pbsta_acmpsta(4) = 56.  CDL = 56 + 12 = 68.
              CMD_GET_STREAM_INFO: begin
                if (w_gs_type != DESC_STREAM_OUTPUT || w_gs_index != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd4;
                  cdl_q        <= 11'd16;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2;  seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0;  seg_len_q[1] <= 16'd4;
                  seg_kind_q[2] <= SEG_STORE;
                  seg_addr_q[2] <= WB_STREAM_FORMAT_C; seg_len_q[2] <= 16'd8;
                  seg_kind_q[3] <= SEG_CONST; seg_addr_q[3] <= 16'd8;  seg_len_q[3] <= 16'd40;
                  // flags + live 40-byte tail (stream_id = {mac,0} — the
                  // previous entity_id here could never match the stream)
                  load_stream_info_consts();
                  cdl_q <= 11'd68;   // 12 + 4+4+8+40
                end
              end

              // -------------------------------------------------- //
              // SET_STREAM_INFO (Milan §5.4.2.9): STREAM_OUTPUT only; the
              // sole supported sub-command is MSRP_ACC_LAT_VALID (updates the
              // presentation-time offset the framer stamps); any other
              // spec-defined sub-command -> NOT_SUPPORTED; gated while a
              // listener is registered (STREAM_IS_RUNNING); response echoes
              // the command payload with the same flags (default echo seg).
              CMD_SET_STREAM_INFO: begin
                if (l0_reject_q) begin
                  status_q <= l0_status_q;
                end else if (w_gs_type == DESC_STREAM_INPUT) begin
                  status_q <= STATUS_NOT_SUPPORTED;   // not implemented for inputs
                end else if (w_gs_type != DESC_STREAM_OUTPUT) begin
                  status_q <= STATUS_BAD_ARGUMENTS;
                end else if (w_gs_index != 16'd0) begin
                  status_q <= STATUS_NO_SUCH_DESCRIPTOR;
                end else if ((w_si_flags & SI_UNSUPPORTED_MASK_C) != 32'd0) begin
                  status_q <= STATUS_NOT_SUPPORTED;
                end else if (listener_observed_i) begin
                  status_q <= STATUS_STREAM_IS_RUNNING;
                end else if (!w_si_flags[29]) begin
                  status_q <= STATUS_SUCCESS;         // nothing requested: no-op
                end else if (w_si_lat[31]) begin
                  status_q <= STATUS_BAD_ARGUMENTS;   // > 0x7FFFFFFF ns
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  pres_wr_p_o   <= 1'b1;
                  pres_wr_val_o <= w_si_lat;
                end
              end

              // -------------------------------------------------- //
              // START/STOP_STREAMING (Milan §5.4.2.19/20): Stream-INPUT-only
              // commands — NOT_SUPPORTED on this talker-only entity (the
              // reference replies not-supported for Stream Outputs; the old
              // NOT_IMPLEMENTED default was the wrong status).
              CMD_START_STREAMING, CMD_STOP_STREAMING: begin
                status_q <= STATUS_NOT_SUPPORTED;
              end

              // -------------------------------------------------- //
              CMD_GET_AVB_INFO: begin
                if (w_gs_type != DESC_AVB_INTERFACE || w_gs_index != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd4;
                  cdl_q        <= 11'd16;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd16;
                  for (int k = 0; k < 8; k++)
                    const_q[k] <= gptp_gm_id_i[8*(7-k) +: 8];
                  const_q[8]  <= 8'h00; const_q[9]  <= 8'h00;   // propagation delay
                  const_q[10] <= 8'h00; const_q[11] <= 8'h00;
                  const_q[12] <= gptp_domain_i;
                  const_q[13] <= 8'h04;   // flags: SRP_ENABLED (bit2); the
                                          // pipewire ref sets 0x04, |0x02 when a
                                          // gPTP grandmaster is present
                  const_q[14] <= 8'h00; const_q[15] <= 8'h00;    // msrp count = 0
                  cdl_q <= 11'd32;   // 12 + 4 + 16
                end
              end

              // -------------------------------------------------- //
              // GET_COUNTERS: Milan-mandatory (v1.2 §5.4.2.25; la_avdecc
              // "mandatory dynamic info"). The response payload is ALWAYS the
              // full 136 B — type(2)+id(2)+counters_valid(4)+128 B block —
              // for EVERY status: la_avdecc/Hive reject undersized non-success
              // responses (the 2026-07-11 pipewire field-report class).
              // Valid masks mirror the pipewire reference (all counter values
              // zero until HW counters are wired): STREAM_OUTPUT = 0x1F
              // (STREAM_START|STOP|MEDIA_RESET|TS_UNCERTAIN|FRAMES_TX),
              // AVB_INTERFACE = 0x23 (LINK_UP|LINK_DOWN|GPTP_GM_CHANGED).
              // The zeroed block rides a SEG_NONE segment (emit default 0x00).
              CMD_GET_COUNTERS: begin
                seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd4;
                seg_kind_q[2] <= SEG_NONE;  seg_addr_q[2] <= 16'd0; seg_len_q[2] <= 16'd128;
                for (int k = 0; k < 4; k++) const_q[k] <= 8'h00;
                cdl_q <= 11'd148;   // 12 + 136
                if (w_gs_type == DESC_STREAM_OUTPUT && w_gs_index == 16'd0) begin
                  status_q   <= STATUS_SUCCESS;
                  const_q[3] <= 8'h1F;
                end else if (w_gs_type == DESC_AVB_INTERFACE && w_gs_index == 16'd0) begin
                  status_q   <= STATUS_SUCCESS;
                  const_q[3] <= 8'h23;
                end else if (acc_found) begin
                  status_q <= STATUS_BAD_ARGUMENTS;      // descriptor w/o counters
                end else begin
                  status_q <= STATUS_NO_SUCH_DESCRIPTOR;
                end
              end

              // -------------------------------------------------- //
              // GET_AS_PATH: Milan-mandatory dynamic info (la_avdecc
              // "Milan 1.3 - 5.4.4"; queried once per AVB_INTERFACE).
              // Response = descriptor_index(2) + count(2) + path_sequence
              // (count x EUI64). With no gPTP stack in HW yet the entity
              // acts as its own clock (the pipewire reference's is-GM
              // branch): count=1, path[0] = clock_identity = the same
              // MAC-derived EUI64 the AVB_INTERFACE descriptor overlay
              // reports ({MAC[47:24], FFFE, MAC[23:0]}). Payload stays
              // 12 B on errors too (full-size-on-error, as GET_COUNTERS).
              CMD_GET_AS_PATH: begin
                seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd2;
                seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd10;
                cdl_q <= 11'd24;   // 12 + 12
                const_q[0] <= 8'h00;
                for (int k = 2; k < 10; k++) const_q[k] <= 8'h00;
                if (w_as_path_idx == 16'd0) begin
                  status_q   <= STATUS_SUCCESS;
                  const_q[1] <= 8'h01;                        // count = 1
                  const_q[2] <= station_mac_i[47:40];         // clock_identity
                  const_q[3] <= station_mac_i[39:32];
                  const_q[4] <= station_mac_i[31:24];
                  const_q[5] <= 8'hFF;
                  const_q[6] <= 8'hFE;
                  const_q[7] <= station_mac_i[23:16];
                  const_q[8] <= station_mac_i[15:8];
                  const_q[9] <= station_mac_i[7:0];
                end else begin
                  status_q   <= STATUS_NO_SUCH_DESCRIPTOR;
                  const_q[1] <= 8'h00;                        // count = 0
                end
              end

              // -------------------------------------------------- //
              // REGISTER (Milan §5.4.2.21): dedup -> SUCCESS (sequence
              // preserved); free slot -> fill {controller_id, src MAC,
              // seq=0}; table full -> NO_RESOURCES. DEREGISTER clears the
              // matching slot; idempotent SUCCESS either way (reference).
              CMD_REGISTER_UNSOLICITED_NOTIFICATION: begin
                seg_kind_q[0] <= SEG_NONE; seg_len_q[0] <= 16'd0;
                cdl_q         <= 11'd12;
                if (w_unsol_match != '0) begin
                  status_q <= STATUS_SUCCESS;              // already registered
                end else if (w_unsol_free != '0) begin
                  status_q <= STATUS_SUCCESS;
                  unsol_valid_r[w_unsol_fill_idx] <= 1'b1;
                  unsol_eid_r[w_unsol_fill_idx]   <= hdr_q.controller_entity_id;
                  unsol_mac_r[w_unsol_fill_idx]   <= req_src_mac_i;
                  unsol_seq_r[w_unsol_fill_idx]   <= 16'd0;
                end else begin
                  status_q <= STATUS_NO_RESOURCES;
                end
              end

              CMD_DEREGISTER_UNSOLICITED_NOTIFICATION: begin
                status_q      <= STATUS_SUCCESS;           // idempotent
                seg_kind_q[0] <= SEG_NONE; seg_len_q[0] <= 16'd0;
                cdl_q         <= 11'd12;
                for (int s = 0; s < UNSOL_SLOTS_C; s++) begin
                  if (w_unsol_match[s]) begin
                    unsol_valid_r[s] <= 1'b0;
                    unsol_pend_r[s]  <= 1'b0;
                  end
                end
              end

              default: ;   // NOT_IMPLEMENTED echo (defaults above)
            endcase
          end
        end

        // ---------------------------------------------------------- //
        WRITE_S: begin   // SET_* write-back (no-op when wb_len_q == 0);
                         // also the cycle where cum_q/pay_len_q settle
          if (wb_len_q == 7'd0) begin
            if (cum_done_q) state_r <= EMIT_ADDR_S;
          end else begin
            st_wr_o    <= 1'b1;
            st_waddr_o <= wb_addr_q + 16'(wb_cnt_r);
            st_wdata_o <= buf_r[wb_src_q + wb_cnt_r];
            if (wb_cnt_r == wb_len_q - 7'd1) begin
              wb_cnt_r <= 7'd0;
              wb_len_q <= 7'd0;
            end else begin
              wb_cnt_r <= wb_cnt_r + 7'd1;
            end
          end
        end

        // ---------------------------------------------------------- //
        // Byte engine, 2-cycle cadence:                                //
        //   EMIT_ADDR: resolve the byte source; issue store read       //
        //   EMIT_DATA: capture the byte, feed the beat packer          //
        // ---------------------------------------------------------- //
        EMIT_ADDR_S: begin
          // Resolve + REGISTER the byte source for fi_r (the store read addr/
          // enable are driven combinationally via w_emit_store, so store data
          // lands next cycle). This moves the deep fi->{offset arithmetic,
          // header positional mux} cone off the path into pack_r.
          is_hdr_r     <= (fi_r < w_hdr_len);
          hdrbyte_r    <= hdr_byte(fi_r);
          emseg_kind_r <= seg_kind_q[w_seg];
          emseg_addr_r <= seg_addr_q[w_seg];
          emsoff_r     <= w_soff;
          state_r      <= EMIT_DATA_S;
        end

        EMIT_DATA_S: begin
          logic [7:0] b;
          if (is_hdr_r) begin
            b = hdrbyte_r;                    // registered header byte
          end else begin
            unique case (emseg_kind_r)        // registered segment select
              SEG_ECHO:  b = buf_r[emseg_addr_r[6:0] + emsoff_r[6:0]];
              SEG_STORE: b = st_byte_i;       // store byte (1-cycle read latency)
              SEG_CONST: b = const_q[emseg_addr_r[5:0] + emsoff_r[5:0]];
              default:   b = 8'h00;
            endcase
          end

          // Assemble one byte per EMIT_DATA, but STALL while a completed beat
          // still occupies pack_r (the top-level handshake drains it). This
          // keeps the transmit register and the assembly register from
          // aliasing and guarantees one transfer per beat.
          if (!beat_pend_r) begin
            pack_r[8*pack_n_r +: 8] <= b;             // little lane order out
            if (pack_n_r == 3'd7 || fi_r == w_frame_len - 16'd1) begin
              beat_pend_r <= 1'b1;
              beat_last_r <= (fi_r == w_frame_len - 16'd1);
              beat_keep_r <= 8'((9'd1 << ((9)'(pack_n_r) + 9'd1)) - 9'd1);
              pack_n_r    <= 3'd0;
            end else begin
              pack_n_r <= pack_n_r + 3'd1;
            end

            if (fi_r == w_frame_len - 16'd1) begin
              state_r <= CONCLUDE_S;
            end else begin
              fi_r    <= fi_r + 16'd1;
              state_r <= EMIT_ADDR_S;
            end
          end
        end

        // ---------------------------------------------------------- //
        CONCLUDE_S: begin   // wait for the final beat to drain, then clean up
          if (!beat_pend_r) begin   // top-level handshake sent the last beat
            evt_resp_o  <= 1'b1;
            // pushes are self-generated: there is no ingress meta to pop
            if (!unsol_frame_r) pop_pend_r <= pop_pend_r + 2'd1;
            unsol_frame_r <= 1'b0;
            fi_r        <= 16'd0;
            state_r     <= IDLE_S;
          end
        end

        default: state_r <= IDLE_S;
      endcase
    end
  end

  // verilator lint_off UNUSED
  wire unused_ok = &{1'b0, s_axis_tkeep, emit_byte_r, l0_state_i.acquired,
                     l0_state_i.acquiring_controller_id, l0_state_i.entity_id,
                     l0_state_i.locked, req_src_mac_i};
  // verilator lint_on  UNUSED

endmodule

`default_nettype wire
