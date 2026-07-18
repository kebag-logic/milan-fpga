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

                Implemented command set (Milan v1.2):
                  READ_DESCRIPTOR                      (full 34-descriptor model)
                  LOCK_ENTITY (+UNLOCK, 60 s timeout)  ACQUIRE -> NOT_SUPPORTED
                  ENTITY_AVAILABLE
                  GET/SET_CONFIGURATION                (single configuration)
                  GET/SET_NAME                         (generated name directory)
                  GET/SET_SAMPLING_RATE                (validated, write-back)
                  GET/SET_STREAM_FORMAT                (validated, write-back)
                  GET/SET_CLOCK_SOURCE                 (CLOCK_DOMAIN[0], 0..2)
                  GET/SET_CONTROL                      (IDENTIFY, identify_o)
                  GET_AUDIO_MAP                        (static maps; ADD/REMOVE
                                                        -> NOT_SUPPORTED)
                  GET/SET_STREAM_INFO                  GET_AVB_INFO
                  GET_COUNTERS  GET_AS_PATH  START/STOP_STREAMING (NOT_SUPPORTED)
                  REGISTER/DEREGISTER_UNSOLICITED      (4-slot push engine)
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
  input  wire [31:0]   pdelay_ns_i,        //! measured neighbor propagation delay ns (CSR 0x6E4, gptp daemon)
  input  wire [7:0]    gptp_domain_i,

  // ---- live talker stream state (docs/design/MILAN_TALKER_SM.md) ------
  input  wire [47:0]   aaf_dmac_i,         //! stream dest MAC (the framer's)
  input  wire [11:0]   aaf_vid_i,          //! stream VLAN id
  input  wire          talker_active_i,    //! ACMP probe SM: declaring
  input  wire          listener_observed_i,//! lwSRP registrar hook
  input  wire [31:0]   pres_offset_i,      //! msrp_accumulated_latency (ns)
  output logic         pres_wr_p_o,        //! 1-cycle: SET_STREAM_INFO update
  output logic [31:0]  pres_wr_val_o,
  output logic         identify_o,         //! IDENTIFY control active (LED hook)
  input  wire          link_up_i,          //! PHY link (AVB_INTERFACE counters)
  input  wire [31:0]   frames_tx_i,        //! AAF frames sent (STREAM_OUTPUT)

  // ---- listener sink state (KL_acmp_listener; STREAM_INPUT[0]) --------
  input  wire          lstn_bound_i,       //! listener SM not UNBOUND
  input  wire [63:0]   lstn_sid_i,         //! bound stream_id
  input  wire [47:0]   lstn_dmac_i,
  input  wire [11:0]   lstn_vlan_i,
  input  wire [1:0]    lstn_pbsta_i,       //! probing status
  input  wire [4:0]    lstn_acmpsta_i,     //! last ACMP status
  input  wire          lstn_ta_reg_i,      //! TalkerAdvertise registered
  input  wire          lstn_ta_fail_i,     //! TalkerFailed registered

  // ---- STREAM_INPUT[0] diagnostics (KL_avtp_rx_monitor; Table 7-156) --
  input  wire          tick_1khz_i,        //! ms tick (counter-push rate limit)
  input  wire [31:0]   in0_cnt_locked_i,
  input  wire [31:0]   in0_cnt_unlocked_i,
  input  wire [31:0]   in0_cnt_interrupted_i,
  input  wire [31:0]   in0_cnt_seqmm_i,
  input  wire [31:0]   in0_cnt_tu_i,
  input  wire [31:0]   in0_cnt_unsupp_i,
  input  wire [31:0]   in0_cnt_frx_i,
  input  wire [31:0]   in0_cnt_mreset_i,   //! MEDIA_RESET (bit 4)
  input  wire [31:0]   in0_cnt_late_i,     //! LATE_TIMESTAMP (bit 9)
  input  wire [31:0]   in0_cnt_early_i,    //! EARLY_TIMESTAMP (bit 10)
  input  wire          in0_cnt_dirty_p_i,  //! monitor: a counter changed
  output logic [63:0]  in0_fmt_o,          //! live STREAM_INPUT[0] format u64
  output logic [15:0]  clk_src_o,          //! live CLOCK_DOMAIN clock_source_index

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
  // Payload capture: stripped-frame bytes 24..151 -> capture word RAM    //
  // (byte 24 = AEM u/command_type hi; AEM payload starts at buf byte 2). //
  // Area-70 config-in-RAM recipe: the old 128-byte register buf_r was    //
  // ~1K FFs + wide echo muxes. The words now live in a 16x64 distributed //
  // RAM written beat-aligned; the DECODE fields (buf bytes 0..15, 24..31)//
  // are additionally captured into three plain registers so the decode   //
  // cones read registers, and only the echo-emit and store-write-back    //
  // paths read the RAM (two async ports).                                //
  // ------------------------------------------------------------------ //
  localparam int unsigned BUF_BYTES_C = 128;

  logic [63:0] cbuf_r [0:15];              //! big-lane capture words (RAM)
  logic [63:0] cw0_r, cw1_r, cw3_r;        //! decode captures: bytes 0-15, 24-31
  logic [4:0]  beat_r;                     //! frame beat counter (sat at 31)

  //! buf byte accessor (big lane order: byte j of word w = tdata[8*(7-j)])
  function automatic [7:0] bufb(input [63:0] w, input [2:0] j);
    bufb = w[8*(3'd7 - j) +: 8];
  endfunction

  //! state-changing SETs whose SUCCESS response is replayed u=1 to the other
  //! registered controllers (IEEE 1722.1-2021 unsolicited rule; reference
  //! reply-unsol-helpers.c). SET_STREAM_INFO keeps its dedicated pend path.
  function automatic logic is_replay_cmd(input [14:0] c);
    is_replay_cmd = (c == CMD_SET_STREAM_FORMAT) || (c == CMD_SET_NAME) ||
                    (c == CMD_SET_SAMPLING_RATE) || (c == CMD_SET_CLOCK_SOURCE) ||
                    (c == CMD_SET_CONTROL) || (c == CMD_START_STREAMING) ||
                    (c == CMD_STOP_STREAMING) || (c == CMD_SET_MAX_TRANSIT_TIME);
  endfunction

  wire w_cap_hs = s_axis_tvalid & s_axis_tready;

  wire [6:0] w_eaddr  = emseg_addr_r[6:0] + emsoff_r[6:0];  //! echo RAM addr
  wire [6:0] w_wbaddr = 7'(wb_src_q + wb_cnt_r);           //! wb RAM addr
  wire [7:0] w_b0  = bufb(cw0_r, 3'd0);
  wire [7:0] w_b1  = bufb(cw0_r, 3'd1);
  wire [7:0] w_b2  = bufb(cw0_r, 3'd2);
  wire [7:0] w_b3  = bufb(cw0_r, 3'd3);
  wire [7:0] w_b4  = bufb(cw0_r, 3'd4);
  wire [7:0] w_b5  = bufb(cw0_r, 3'd5);
  wire [7:0] w_b6  = bufb(cw0_r, 3'd6);
  wire [7:0] w_b7  = bufb(cw0_r, 3'd7);
  wire [7:0] w_b8  = bufb(cw1_r, 3'd0);
  wire [7:0] w_b9  = bufb(cw1_r, 3'd1);
  wire [7:0] w_b10  = bufb(cw1_r, 3'd2);
  wire [7:0] w_b11  = bufb(cw1_r, 3'd3);
  wire [7:0] w_b12  = bufb(cw1_r, 3'd4);
  wire [7:0] w_b13  = bufb(cw1_r, 3'd5);
  wire [7:0] w_b14  = bufb(cw1_r, 3'd6);
  wire [7:0] w_b15  = bufb(cw1_r, 3'd7);
  wire [7:0] w_b24 = bufb(cw3_r, 3'd0);
  wire [7:0] w_b25 = bufb(cw3_r, 3'd1);
  wire [7:0] w_b26 = bufb(cw3_r, 3'd2);
  wire [7:0] w_b27 = bufb(cw3_r, 3'd3);
  wire [7:0] w_b28 = bufb(cw3_r, 3'd4);
  wire [7:0] w_b29 = bufb(cw3_r, 3'd5);
  wire [7:0] w_b30 = bufb(cw3_r, 3'd6);
  wire [7:0] w_b31 = bufb(cw3_r, 3'd7);

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
  //! replays must drain before a new command may overwrite the capture
  //! buffer the replayed response is rebuilt from
  assign s_axis_tready = (state_r == IDLE_S && unsol_pend4_r == '0) ||
                         (state_r == CAPTURE_S);

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
  wire [15:0] w_rd_cfg   = {w_b2, w_b3};   //! READ_DESCRIPTOR config
  wire [15:0] w_rd_type  = {w_b6, w_b7};
  wire [15:0] w_rd_index = {w_b8, w_b9};
  wire [15:0] w_gs_type  = {w_b2, w_b3};   //! GET/SET_* desc type
  wire [15:0] w_gs_index = {w_b4, w_b5};
  //! SET_STREAM_INFO (Milan §5.4.2.9): payload byte n = buf_r[n+2] — flags at
  //! payload 4-7, msrp_accumulated_latency at payload 24-27.
  wire [31:0] w_si_flags = {w_b6,  w_b7,  w_b8,  w_b9};
  wire [31:0] w_si_lat   = {w_b26, w_b27, w_b28, w_b29};
  //! Spec-defined sub-command bits (reference valid_mask: aecp-aem.h bits 0-9
  //! + 25-31) minus the ONE supported (MSRP_ACC_LAT_VALID, bit 29): any of
  //! these requested -> NOT_SUPPORTED for the whole command (§5.4.2.9).
  localparam [31:0] SI_UNSUPPORTED_MASK_C = 32'hDE00_03FF;
  wire [15:0] w_name_idx = {w_b6, w_b7};   //! SET/GET_NAME name_index
  wire [15:0] w_as_path_idx = {w_b2, w_b3};  //! GET_AS_PATH descriptor_index (no type field)
  //! live gPTP state (USER bugs 1-4, 07-18): GM + pdelay are daemon-written
  //! CSRs; a nonzero foreign GM turns the AS path into [GM, us]
  wire        w_gm_present = (gptp_gm_id_i != 64'd0);
  wire [63:0] w_self_ckid  = {station_mac_i[47:24], 16'hFFFE, station_mac_i[23:0]};
  wire        w_gm_foreign = w_gm_present && (gptp_gm_id_i != w_self_ckid);
  wire [15:0] w_name_cfg = {w_b8, w_b9};
  wire [31:0] w_set_rate = {w_b6, w_b7, w_b8, w_b9};
  wire [63:0] w_set_fmt  = {w_b6, w_b7, w_b8,  w_b9,
                            w_b10, w_b11, w_b12, w_b13};
  //! VU frames have NO u/command_type after sequence_id: buf_r[0..5] =
  //! protocol_id, buf_r[6:7] = command_type, buf_r[8:9] = reserved,
  //! buf_r[10..] = command payload (AEM frames instead put command_type in
  //! buf_r[0:1] and the payload in buf_r[2..]).
  wire        w_vu_proto_ok =
      (w_b0 == MILAN_PROTOCOL_ID_C[47:40]) &&
      (w_b1 == MILAN_PROTOCOL_ID_C[39:32]) &&
      (w_b2 == MILAN_PROTOCOL_ID_C[31:24]) &&
      (w_b3 == MILAN_PROTOCOL_ID_C[23:16]) &&
      (w_b4 == MILAN_PROTOCOL_ID_C[15:8])  &&
      (w_b5 == MILAN_PROTOCOL_ID_C[7:0]);
  wire [14:0] w_vu_cmd = {w_b6[6:0], w_b7};

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

  // function result captured in a net: indexing a call expression directly
  // (aem_name_lookup(...)[16]) is SV-only — sv2v keeps it and Yosys' V2005
  // reader rejects it, breaking the open-toolchain portability gate. The
  // lookup itself is generated (gen/aecp_aem_rom.svh) so the name directory
  // always matches the descriptor image.
  wire [16:0] w_name_ptr =
      aem_name_lookup(w_gs_type, w_gs_index, w_name_idx);   //! {valid, wb addr}

  wire w_rate_ok = (w_set_rate == AEM_RATES_C[0]) ||
                   (w_set_rate == AEM_RATES_C[1]) ||
                   (w_set_rate == AEM_RATES_C[2]);
  //! Milan adaptive listener (FR-STR-03; USER 07-17): the listener adapts
  //! to the TALKER's stream format — accept any channel count 1..8 on the
  //! three base rates (the audio maps route the mapped channels; the RX
  //! monitor / I2S player re-stride from the live format's channel field)
  wire [9:0]  w_fmt_ch    = w_set_fmt[31:22];
  wire [63:0] w_fmt_chm   = w_set_fmt & ~(64'h3FF << 22);
  wire w_fmt_ok  = (w_fmt_ch >= 10'd1) && (w_fmt_ch <= 10'd8) &&
                   ((w_fmt_chm == (AEM_FMTS_C[0] & ~(64'h3FF << 22))) ||
                    (w_fmt_chm == (AEM_FMTS_C[1] & ~(64'h3FF << 22))) ||
                    (w_fmt_chm == (AEM_FMTS_C[2] & ~(64'h3FF << 22))));
  //! talker truth: the framer is hardwired stereo 48k - STREAM_OUTPUT
  //! accepts ONLY the wire-true format (declared == transmitted, user bug 5)
  localparam [63:0] AAF_OUT_FMT_C =
      (AEM_FMTS_C[0] & ~(64'h3FF << 22)) | (64'd2 << 22);
  wire w_out_fmt_ok = (w_set_fmt == AAF_OUT_FMT_C);
  wire w_crf_fmt_ok = (w_set_fmt == AEM_CRF_FMTS_C[0]) ||
                      (w_set_fmt == AEM_CRF_FMTS_C[1]) ||
                      (w_set_fmt == AEM_CRF_FMTS_C[2]);

  // ------------------------------------------------------------------ //
  // Response plan (filled in DECIDE_S)                                   //
  // ------------------------------------------------------------------ //
  typedef enum logic [1:0] { SEG_NONE, SEG_ECHO, SEG_STORE, SEG_CONST } seg_kind_t;

  localparam int unsigned SEGN_C = 16;   //! response segments (0x4B needs 15)
  seg_kind_t   seg_kind_q [0:SEGN_C-1];
  logic [15:0] seg_addr_q [0:SEGN_C-1]; //! ECHO: buf offset · STORE: store addr · CONST: const offset
  logic [15:0] seg_len_q  [0:SEGN_C-1];
  logic [7:0]  const_q [0:95];   //! scratch for CONST segments (0x4B uses 78)
  logic [10:0] cdl_q;
  logic [4:0]  status_q;
  logic [3:0]  msg_resp_q;
  logic [47:0] dst_mac_q;

  //! cumulative payload offsets (registered one cycle after DECIDE_S)
  logic [15:0] cum_q [0:SEGN_C-1]; //! start offset of each segment
  logic [1:0]  cum_ph_r;           //! pipelined cum compute: 4 segs/cycle
  logic [15:0] cum_acc_r;
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
  logic [3:0]  w_seg;
  logic [15:0] w_soff;
  always_comb begin
    w_seg  = 4'd0;
    w_soff = w_pi;
    for (int k = 1; k < SEGN_C; k++)
      if (w_pi >= cum_q[k] && seg_len_q[k] != 16'd0) begin
        w_seg  = 4'(k);
        w_soff = w_pi - cum_q[k];
      end
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

  //! IDENTIFY control level (SET_CONTROL 255 -> on, 0 -> off)
  logic identify_r;
  assign identify_o = identify_r;

  //! Milan MVU state: system unique id (32-bit on the 1.2 wire) + the user
  //! media-clock-reference priority (domain name lives in the store scratch)
  logic [31:0] sysuid_r;
  logic [7:0]  mcr_user_prio_r;

  //! GET_COUNTERS live counters (FR-CTRL-04). STREAM_OUTPUT start/stop come
  //! from the talker-SM activation edges; AVB_INTERFACE link/GM from the
  //! link level and the CSR-provisioned gPTP GM id (first provisioning
  //! write counts as one GM change — documented).
  logic [31:0] cnt_start_r, cnt_stop_r;
  logic [31:0] cnt_linkup_r, cnt_linkdn_r, cnt_gmchg_r;
  logic        link_prev_r;
  logic [63:0] gm_prev_r;

  //! live STREAM_INPUT[0] current format: resets to the ROM's current_format
  //! (AEM_FMTS_C[0]) and follows SET_STREAM_FORMAT — the RX monitor's
  //! format-compare reference (the store scratch keeps the readback copy)
  logic [63:0] fmt_in0_r;
  assign in0_fmt_o = fmt_in0_r;
  logic [15:0] clk_src_r;                 //! follows SET_CLOCK_SOURCE (reset 0 = internal)
  assign clk_src_o = clk_src_r;

  //! STREAM_INPUT counter push state (Milan §5.4.5: unsolicited GET_COUNTERS
  //! only when a counter changed, at most once per second per descriptor).
  //! in0_rl_ms_r resets SATURATED so the first change pushes immediately
  //! (reference: last_emit == 0 -> elapsed).
  logic        in0_dirty_r;
  logic [9:0]  in0_rl_ms_r;
  wire         in0_rl_ok = (in0_rl_ms_r >= 10'd1000);

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
  logic [UNSOL_SLOTS_C-1:0] unsol_pend_r;   //! slots owed a stream-info push
  logic [UNSOL_SLOTS_C-1:0] unsol_pend2_r;  //! slots owed a GET_COUNTERS push
  logic [UNSOL_SLOTS_C-1:0] unsol_pend4_r;  //! slots owed a SET-response replay
                                            //! (u=1 copy of the causing SET's
                                            //! response - reference
                                            //! reply-unsol-helpers rule)
  logic                  unsol_frame_r;     //! current emit is a push (u=1, no meta pop)
  logic                  ta_prev_r, lo_prev_r;  //! edge detectors

  //! REGISTER helper wires: dedup match + lowest free slot + lowest pend
  logic [UNSOL_SLOTS_C-1:0] w_unsol_match;
  logic [UNSOL_SLOTS_C-1:0] w_unsol_free;
  logic [1:0]               w_unsol_fill_idx;   //! lowest free slot
  logic [1:0]               w_unsol_push_idx;   //! lowest pending slot
  logic [1:0]               w_unsol_push2_idx;  //! lowest counters-pending slot
  logic [1:0]               w_unsol_push4_idx;  //! lowest replay-pending slot
  always_comb begin
    for (int s = 0; s < UNSOL_SLOTS_C; s++) begin
      w_unsol_match[s] = unsol_valid_r[s] &&
                         (unsol_eid_r[s] == hdr_q.controller_entity_id);
      w_unsol_free[s]  = !unsol_valid_r[s];
    end
    w_unsol_fill_idx = 2'd0;
    w_unsol_push_idx = 2'd0;
    w_unsol_push2_idx = 2'd0;
    w_unsol_push4_idx = 2'd0;
    for (int s = UNSOL_SLOTS_C-1; s >= 0; s--) begin
      if (w_unsol_free[s]) w_unsol_fill_idx = 2'(s);   // lowest wins
      if (unsol_pend_r[s])  w_unsol_push_idx  = 2'(s);
      if (unsol_pend2_r[s]) w_unsol_push2_idx = 2'(s);
      if (unsol_pend4_r[s]) w_unsol_push4_idx = 2'(s);
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
  // STREAM_INPUT stream-info payload (reference populate_input_response:
  // identity fields always valid, bound adds FAST_CONNECT|SAVED_STATE|
  // CONNECTED|STREAMING_WAIT, TalkerFailed adds SRP_REGISTERING_FAILED|
  // MSRP_FAILURE_VALID; trailer flags_ex REGISTERING + {pbsta,acmpsta}).
  // sink0 = the ACMP listener SM; sink1 (CRF) reads as unbound.          //
  // ------------------------------------------------------------------ //
  task automatic load_input_stream_info_consts(input logic sink0);
    logic        bnd, ta_r, ta_f;
    logic [31:0] fl;
    begin
      bnd  = sink0 & lstn_bound_i;
      ta_r = sink0 & lstn_ta_reg_i;
      ta_f = sink0 & lstn_ta_fail_i;
      // FORMAT|STREAM_ID|ACC_LAT|DEST_MAC|VLAN always valid
      fl = 32'hF200_0000;
      if (bnd) begin
        fl = fl | 32'h0400_0000              // CONNECTED
                | 32'h0000_0002              // FAST_CONNECT
                | 32'h0000_0004;             // SAVED_STATE
        if (!started_in_r) fl = fl | 32'h0000_0008;   // STREAMING_WAIT
      end
      if (ta_f) fl = fl | 32'h0800_0000      // MSRP_FAILURE_VALID
                       | 32'h0000_0040;      // SRP_REGISTERING_FAILED
      const_q[0] <= fl[31:24]; const_q[1] <= fl[23:16];
      const_q[2] <= fl[15:8];  const_q[3] <= fl[7:0];
      for (int k = 0; k < 8; k++)
        const_q[8+k] <= sink0 ? lstn_sid_i[8*(7-k) +: 8] : 8'h00;
      for (int k = 16; k < 20; k++) const_q[k] <= 8'h00;  // acc_lat (0 valid)
      for (int k = 0; k < 6; k++)
        const_q[20+k] <= sink0 ? lstn_dmac_i[8*(5-k) +: 8] : 8'h00;
      for (int k = 26; k < 36; k++) const_q[k] <= 8'h00;  // fail code + bridge
      const_q[36] <= sink0 ? {4'h0, lstn_vlan_i[11:8]} : 8'h00;
      const_q[37] <= sink0 ? lstn_vlan_i[7:0] : 8'h00;
      const_q[38] <= 8'h00; const_q[39] <= 8'h00;
      const_q[40] <= 8'h00; const_q[41] <= 8'h00; const_q[42] <= 8'h00;
      const_q[43] <= {7'b0, ta_r | ta_f};                 // flags_ex REGISTERING
      const_q[44] <= sink0 ? {1'b0, lstn_pbsta_i, lstn_acmpsta_i} : 8'h00;
      const_q[45] <= 8'h00; const_q[46] <= 8'h00; const_q[47] <= 8'h00;
    end
  endtask

  // ------------------------------------------------------------------ //
  // STREAM_INPUT GET_COUNTERS payload (Table 7-156; shared by the         //
  // solicited command and the unsolicited push): valid mask 0xF3F at      //
  // const 0..3, counter for valid bit n at const 4+4n (block byte 4n).   //
  // sink0 = live monitor counters; sink 1 (CRF, no listener SM) = zeros.  //
  // MEDIA_RESET / LATE / EARLY are advertised valid but always 0, exactly //
  // the pipewire reference (no media clock recovery in fabric yet).       //
  // ------------------------------------------------------------------ //
  task automatic load_input_counters_consts(input logic sink0);
    begin
      for (int k = 0; k < 52; k++) const_q[k] <= 8'h00;
      const_q[2] <= 8'h0F; const_q[3] <= 8'h3F;   // valid mask 0x00000F3F
      if (sink0) begin
        for (int k = 0; k < 4; k++) begin
          const_q[4+k]  <= in0_cnt_locked_i     [8*(3-k) +: 8];  // bit0
          const_q[8+k]  <= in0_cnt_unlocked_i   [8*(3-k) +: 8];  // bit1
          const_q[12+k] <= in0_cnt_interrupted_i[8*(3-k) +: 8];  // bit2
          const_q[16+k] <= in0_cnt_seqmm_i      [8*(3-k) +: 8];  // bit3
          const_q[20+k] <= in0_cnt_mreset_i    [8*(3-k) +: 8];  // bit4
          const_q[24+k] <= in0_cnt_tu_i         [8*(3-k) +: 8];  // bit5
          const_q[36+k] <= in0_cnt_unsupp_i     [8*(3-k) +: 8];  // bit8
          const_q[40+k] <= in0_cnt_late_i       [8*(3-k) +: 8];  // bit9
          const_q[44+k] <= in0_cnt_early_i      [8*(3-k) +: 8];  // bit10
          const_q[48+k] <= in0_cnt_frx_i        [8*(3-k) +: 8];  // bit11
        end
      end
    end
  endtask

  //! per-input "started" (START/STOP_STREAMING, Milan input-only commands)
  logic started_in_r;

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
      identify_r   <= 1'b0;
      started_in_r <= 1'b1;
      sysuid_r     <= 32'd0;
      mcr_user_prio_r <= MCR_DEFAULT_PRIO_C;
      cnt_start_r  <= 32'd0;
      cnt_stop_r   <= 32'd0;
      cnt_linkup_r <= 32'd0;
      cnt_linkdn_r <= 32'd0;
      cnt_gmchg_r  <= 32'd0;
      link_prev_r  <= 1'b0;
      gm_prev_r    <= 64'd0;
      unsol_pend_r  <= '0;
      unsol_pend2_r <= '0;
      unsol_pend4_r <= '0;
      unsol_frame_r <= 1'b0;
      ta_prev_r     <= 1'b0;
      lo_prev_r     <= 1'b0;
      fmt_in0_r     <= AEM_FMTS_C[0];
      clk_src_r     <= 16'd0;
      in0_dirty_r   <= 1'b0;
      in0_rl_ms_r   <= 10'd1000;   // saturated: first change pushes at once
      for (int s = 0; s < UNSOL_SLOTS_C; s++) begin
        unsol_valid_r[s] <= 1'b0;
        unsol_eid_r[s]   <= 64'd0;
        unsol_mac_r[s]   <= 48'd0;
        unsol_seq_r[s]   <= 16'd0;
      end
      pay_len_q    <= 16'd0;
      cum_done_q   <= 1'b0;
      cum_ph_r     <= 2'd0;
      cum_acc_r    <= 16'd0;
      cw0_r <= 64'd0; cw1_r <= 64'd0; cw3_r <= 64'd0;
      for (int k = 0; k < 96; k++) const_q[k] <= 8'h00;
      for (int s = 0; s < SEGN_C; s++) begin
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

      // ---- STREAM_INPUT counter push (Milan §5.4.5): dirty + 1 s window --
      if (tick_1khz_i && !in0_rl_ok) in0_rl_ms_r <= in0_rl_ms_r + 10'd1;
      if (in0_cnt_dirty_p_i)         in0_dirty_r <= 1'b1;
      if (in0_dirty_r && in0_rl_ok) begin
        for (int s = 0; s < UNSOL_SLOTS_C; s++)
          if (unsol_valid_r[s]) unsol_pend2_r[s] <= 1'b1;
        in0_dirty_r <= 1'b0;
        in0_rl_ms_r <= 10'd0;
      end

      // ---- GET_COUNTERS event counting (edges) ------------------------
      if (talker_active_i & ~ta_prev_r) cnt_start_r <= cnt_start_r + 32'd1;
      if (~talker_active_i & ta_prev_r) cnt_stop_r  <= cnt_stop_r  + 32'd1;
      link_prev_r <= link_up_i;
      if (link_up_i & ~link_prev_r) cnt_linkup_r <= cnt_linkup_r + 32'd1;
      if (~link_up_i & link_prev_r) cnt_linkdn_r <= cnt_linkdn_r + 32'd1;
      gm_prev_r <= gptp_gm_id_i;
      if (gptp_gm_id_i != gm_prev_r) cnt_gmchg_r <= cnt_gmchg_r + 32'd1;
      if (pres_wr_p_o) begin   // hdr_q still holds the causing SET command
        for (int s = 0; s < UNSOL_SLOTS_C; s++)
          if (unsol_valid_r[s] &&
              unsol_eid_r[s] != hdr_q.controller_entity_id)
            unsol_pend_r[s] <= 1'b1;
      end

      // ---------------- capture (runs in IDLE/CAPTURE) ----------------
      if (w_cap_hs) begin
        if (beat_r >= 5'd3 && beat_r < 5'd19)
          cbuf_r[4'(beat_r - 5'd3)] <= s_axis_tdata;
        if (beat_r == 5'd3) cw0_r <= s_axis_tdata;   // buf bytes 0-7
        if (beat_r == 5'd4) cw1_r <= s_axis_tdata;   // buf bytes 8-15
        if (beat_r == 5'd6) cw3_r <= s_axis_tdata;   // buf bytes 24-31
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
        //! 4 segments per cycle over 4 cycles: a single-cycle 15-term chain
        //! was the AX 100 MHz WNS -5.6 violator (milanfinal sweep); payload
        //! emission first consults cum_q >= 10 cycles after WRITE_S entry,
        //! so the pipelined compute is always done in time
        begin
          automatic logic [15:0] a = cum_acc_r;
          for (int k = 0; k < 4; k++) begin
            cum_q[{cum_ph_r, 2'(k)}] <= a;
            a = a + seg_len_q[{cum_ph_r, 2'(k)}];
          end
          cum_acc_r <= a;
          cum_ph_r  <= cum_ph_r + 2'd1;
          if (cum_ph_r == 2'd3) begin
            pay_len_q  <= a;
            cum_done_q <= 1'b1;
          end
        end
      end

      case (state_r)
        // ---------------------------------------------------------- //
        IDLE_S: begin
          discard_q <= !enable_i;
          unsol_frame_r <= 1'b0;
          if (enable_i && unsol_pend4_r != '0) begin
            // SET-response replay: hdr_q/capture RAM still hold the causing
            // command (tready is gated while pend4 != 0); re-run DECIDE with
            // the registered controller's identity and u=1. Store/level
            // side effects re-run idempotently (same written values).
            unsol_pend4_r[w_unsol_push4_idx] <= 1'b0;
            unsol_seq_r[w_unsol_push4_idx]   <= unsol_seq_r[w_unsol_push4_idx] + 16'd1;
            unsol_frame_r <= 1'b1;
            dst_mac_q     <= unsol_mac_r[w_unsol_push4_idx];
            hdr_q.controller_entity_id <= unsol_eid_r[w_unsol_push4_idx];
            hdr_q.sequence_id          <= unsol_seq_r[w_unsol_push4_idx];
            cum_done_q <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
            fi_r       <= 16'd0;
            state_r    <= DECIDE_S;
          end else if (w_cap_hs) begin
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
            for (int s = 4; s < SEGN_C; s++) begin
              seg_kind_q[s] <= SEG_NONE; seg_len_q[s] <= 16'd0;
            end
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
            cum_done_q <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
            fi_r       <= 16'd0;
            state_r    <= WRITE_S;
          end else if (enable_i && unsol_pend2_r != '0) begin
            // Synthesized unsolicited GET_COUNTERS response for
            // STREAM_INPUT[0] (u=1), same full-136B shape as the solicited
            // path. type/index ride const bytes 56..59 (the counter task
            // owns 0..51).
            unsol_pend2_r[w_unsol_push2_idx] <= 1'b0;
            unsol_seq_r[w_unsol_push2_idx]   <= unsol_seq_r[w_unsol_push2_idx] + 16'd1;
            unsol_frame_r <= 1'b1;
            dst_mac_q     <= unsol_mac_r[w_unsol_push2_idx];
            hdr_q.controller_entity_id <= unsol_eid_r[w_unsol_push2_idx];
            hdr_q.sequence_id          <= unsol_seq_r[w_unsol_push2_idx];
            hdr_q.command_type         <= CMD_GET_COUNTERS;
            vu_q       <= 1'b0;
            msg_resp_q <= MSG_AEM_RESPONSE;
            status_q   <= STATUS_SUCCESS;
            for (int s = 4; s < SEGN_C; s++) begin
              seg_kind_q[s] <= SEG_NONE; seg_len_q[s] <= 16'd0;
            end
            seg_kind_q[0] <= SEG_CONST; seg_addr_q[0] <= 16'd56; seg_len_q[0] <= 16'd4;
            seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0;  seg_len_q[1] <= 16'd52;
            seg_kind_q[2] <= SEG_NONE;  seg_addr_q[2] <= 16'd0;  seg_len_q[2] <= 16'd80;
            seg_kind_q[3] <= SEG_NONE;  seg_addr_q[3] <= 16'd0;  seg_len_q[3] <= 16'd0;
            const_q[56] <= 8'h00; const_q[57] <= 8'h05;   // STREAM_INPUT
            const_q[58] <= 8'h00; const_q[59] <= 8'h00;   // index 0
            load_input_counters_consts(1'b1);
            cdl_q      <= 11'd148;   // 12 + 136
            wb_len_q   <= 7'd0; wb_cnt_r <= 7'd0;
            cum_done_q <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
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
          for (int s = 0; s < SEGN_C; s++) begin
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
          cum_done_q <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
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

            // SET/GET_SYSTEM_UNIQUE_ID (FR-MVU-02; Milan 1.2 payload =
            // reserved16 + 32-bit id, la_avdecc protocolMvuPayloadSizes 6/2/6).
            // Volatile mirror — NV persistence is the standing store follow-up.
            end else if (w_vu_cmd == VU_SET_SYSTEM_UNIQUE_ID) begin
              status_q      <= STATUS_SUCCESS;
              seg_kind_q[0] <= SEG_ECHO; seg_addr_q[0] <= 16'd0; seg_len_q[0] <= 16'd14;
              sysuid_r      <= {w_b10, w_b11, w_b12, w_b13};
              cdl_q         <= 11'd24;
            end else if (w_vu_cmd == VU_GET_SYSTEM_UNIQUE_ID) begin
              status_q      <= STATUS_SUCCESS;
              seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd0; seg_len_q[0] <= 16'd10;
              seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd4;
              const_q[0] <= sysuid_r[31:24]; const_q[1] <= sysuid_r[23:16];
              const_q[2] <= sysuid_r[15:8];  const_q[3] <= sysuid_r[7:0];
              cdl_q         <= 11'd24;

            // SET/GET_MEDIA_CLOCK_REFERENCE_INFO (FR-MVU-02; Milan 1.3
            // §5.4.4.4 layout, 74-byte info block): clock_domain_index(2) +
            // flags(1: bit0 user-prio-valid, bit1 domain-name-valid) +
            // reserved(1) + default_prio(1) + user_prio(1) + reserved(4) +
            // domain_name(64). default_prio = 192 (audio-interface class).
            // The domain name lives in the store's scratch tail.
            end else if (w_vu_cmd == VU_GET_MEDIA_CLOCK_REF_INFO ||
                         w_vu_cmd == VU_SET_MEDIA_CLOCK_REF_INFO) begin
              seg_kind_q[0] <= SEG_ECHO; seg_addr_q[0] <= 16'd0; seg_len_q[0] <= 16'd10;
              if ({w_b8, w_b9} != 16'd0) begin
                status_q <= STATUS_BAD_ARGUMENTS;   // only CLOCK_DOMAIN[0]
                cdl_q    <= 11'd20;
              end else begin
                status_q      <= STATUS_SUCCESS;
                seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd8;
                seg_kind_q[2] <= SEG_STORE;
                seg_addr_q[2] <= WB_MCR_DOMNAME_C; seg_len_q[2] <= 16'd64;
                const_q[0] <= (w_vu_cmd == VU_SET_MEDIA_CLOCK_REF_INFO)
                              ? w_b10 : 8'h03;   // SET echoes its flags
                const_q[1] <= 8'h00;                 // reserved
                const_q[2] <= MCR_DEFAULT_PRIO_C;
                const_q[3] <= (w_vu_cmd == VU_SET_MEDIA_CLOCK_REF_INFO &&
                               w_b10[0]) ? w_b13 : mcr_user_prio_r;
                const_q[4] <= 8'h00; const_q[5] <= 8'h00;
                const_q[6] <= 8'h00; const_q[7] <= 8'h00;
                cdl_q <= 11'd92;   // 18 + 74
                if (w_vu_cmd == VU_SET_MEDIA_CLOCK_REF_INFO) begin
                  if (w_b10[0]) mcr_user_prio_r <= w_b13;
                  if (w_b10[1]) begin
                    wb_addr_q <= WB_MCR_DOMNAME_C;
                    wb_len_q  <= 7'd64;
                    wb_src_q  <= 7'd18;
                  end
                end
              end
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
                  const_q[16] <= w_b2; const_q[17] <= w_b3;   // cfg echo
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
              // SET/GET_CLOCK_SOURCE (§7.4.23/24, FR-CLK-03): addresses
              // CLOCK_DOMAIN[0]; the selected index is dynamic state in the
              // store (write-back, reads back through the STORE segment) —
              // sources 0..2 = Internal / AAF stream / CRF stream.
              CMD_GET_CLOCK_SOURCE, CMD_SET_CLOCK_SOURCE: begin
                cdl_q <= 11'd20;   // 12 + 4 + 4
                if (l0_reject_q) begin
                  status_q     <= l0_status_q;
                  seg_len_q[0] <= 16'd8;
                end else if (w_gs_type != DESC_CLOCK_DOMAIN || w_gs_index != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd8;
                end else if (hdr_q.command_type == CMD_SET_CLOCK_SOURCE &&
                             {w_b6, w_b7} >= 16'd3) begin
                  status_q     <= STATUS_BAD_ARGUMENTS;   // only sources 0..2
                  seg_len_q[0] <= 16'd8;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_STORE;
                  seg_addr_q[1] <= WB_CLOCK_SRC_IDX_C; seg_len_q[1] <= 16'd2;
                  if (hdr_q.command_type == CMD_SET_CLOCK_SOURCE)
                    clk_src_r <= {w_b6, w_b7};
                  seg_kind_q[2] <= SEG_CONST; seg_addr_q[2] <= 16'd0; seg_len_q[2] <= 16'd2;
                  const_q[0] <= 8'h00; const_q[1] <= 8'h00;   // reserved
                  if (hdr_q.command_type == CMD_SET_CLOCK_SOURCE) begin
                    wb_addr_q <= WB_CLOCK_SRC_IDX_C;
                    wb_len_q  <= 7'd2;
                    wb_src_q  <= 7'd6;
                  end
                end
              end

              // -------------------------------------------------- //
              // SET/GET_CONTROL (§7.4.25/26, FR-MGT-01): CONTROL[0] is the
              // Milan IDENTIFY control (LINEAR_UINT8, step 255 -> legal
              // values 0/255). The entity stays in identify mode while the
              // value is non-zero (reset_time advisory — the JSON model
              // note); identify_o is the board LED / blink hook.
              CMD_GET_CONTROL, CMD_SET_CONTROL: begin
                cdl_q <= 11'd17;   // 12 + 4 + 1 value
                if (l0_reject_q) begin
                  status_q     <= l0_status_q;
                  seg_len_q[0] <= (hdr_q.command_type == CMD_SET_CONTROL)
                                  ? 16'd5 : 16'd4;
                  cdl_q        <= hdr_q.control_data_length;
                end else if (w_gs_type != DESC_CONTROL || w_gs_index != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= (hdr_q.command_type == CMD_SET_CONTROL)
                                  ? 16'd5 : 16'd4;
                  cdl_q        <= hdr_q.control_data_length;
                end else if (hdr_q.command_type == CMD_SET_CONTROL &&
                             w_b6 != 8'h00 && w_b6 != 8'hFF) begin
                  status_q     <= STATUS_BAD_ARGUMENTS;    // step 255: 0 or 255
                  seg_len_q[0] <= 16'd5;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_STORE;
                  seg_addr_q[1] <= WB_CONTROL_CUR_C; seg_len_q[1] <= 16'd1;
                  if (hdr_q.command_type == CMD_SET_CONTROL) begin
                    wb_addr_q  <= WB_CONTROL_CUR_C;
                    wb_len_q   <= 7'd1;
                    wb_src_q   <= 7'd6;
                    identify_r <= (w_b6 != 8'h00);
                  end
                end
              end

              // -------------------------------------------------- //
              // GET_AUDIO_MAP (§7.4.44): addresses STREAM_PORT_IN/OUT[0];
              // this entity's maps are the static power-on defaults
              // (AUDIO_MAP[0]/[1] in the store) — number_of_maps=1,
              // map_index 0 only. ADD/REMOVE (dynamic mapping edit) is
              // NOT_SUPPORTED on the fixed 8-channel mapping.
              CMD_GET_AUDIO_MAP: begin
                if ((w_gs_type != DESC_STREAM_PORT_INPUT &&
                     w_gs_type != DESC_STREAM_PORT_OUTPUT) ||
                    w_gs_index != 16'd0 || {w_b6, w_b7} != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd8;
                  cdl_q        <= 11'd20;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd6;
                  seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                  const_q[0] <= 8'h00; const_q[1] <= 8'h01;   // number_of_maps
                  const_q[2] <= 8'h00; const_q[3] <= 8'h08;   // number_of_mappings
                  const_q[4] <= 8'h00; const_q[5] <= 8'h00;   // reserved
                  seg_kind_q[2] <= SEG_STORE;
                  seg_addr_q[2] <= ((w_gs_type == DESC_STREAM_PORT_INPUT)
                                    ? WB_AUDIO_MAP_0_C : WB_AUDIO_MAP_1_C) + 16'd8;
                  seg_len_q[2]  <= 16'd64;                    // 8 mappings x 8 B
                  cdl_q <= 11'd88;   // 12 + 6 + 6 + 64
                end
              end

              CMD_ADD_AUDIO_MAPPINGS, CMD_REMOVE_AUDIO_MAPPINGS: begin
                status_q <= STATUS_NOT_SUPPORTED;   // static default maps
              end

              // -------------------------------------------------- //
              // GET/SET_STREAM_FORMAT: STREAM_OUTPUT[0] + the two listener
              // sinks (Milan adaptive listener, FR-STR-03) — sink0 validates
              // against the AAF set, sink1 against the CRF set.
              CMD_GET_STREAM_FORMAT, CMD_SET_STREAM_FORMAT: begin
                cdl_q <= 11'd24;   // 12 + 4 + 8
                if (l0_reject_q) begin
                  status_q     <= l0_status_q;
                  seg_len_q[0] <= 16'd12;
                end else if (!((w_gs_type == DESC_STREAM_OUTPUT && w_gs_index == 16'd0) ||
                               (w_gs_type == DESC_STREAM_INPUT  && w_gs_index < 16'd2))) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd12;
                end else if (hdr_q.command_type == CMD_SET_STREAM_FORMAT &&
                             !((w_gs_type == DESC_STREAM_OUTPUT)
                               ? w_out_fmt_ok
                               : (w_gs_type == DESC_STREAM_INPUT && w_gs_index == 16'd1)
                                 ? w_crf_fmt_ok : w_fmt_ok)) begin
                  status_q     <= STATUS_BAD_ARGUMENTS;
                  seg_len_q[0] <= 16'd12;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_STORE;
                  seg_addr_q[1] <= (w_gs_type == DESC_STREAM_OUTPUT) ? WB_STREAM_FORMAT_C
                                   : (w_gs_index == 16'd0) ? WB_STREAM_IN0_FMT_C
                                                           : WB_STREAM_IN1_FMT_C;
                  seg_len_q[1]  <= 16'd8;
                  if (hdr_q.command_type == CMD_SET_STREAM_FORMAT) begin
                    wb_addr_q <= (w_gs_type == DESC_STREAM_OUTPUT) ? WB_STREAM_FORMAT_C
                                 : (w_gs_index == 16'd0) ? WB_STREAM_IN0_FMT_C
                                                         : WB_STREAM_IN1_FMT_C;
                    wb_len_q  <= 7'd8;
                    wb_src_q  <= 7'd6;
                    // live copy for the RX monitor's format compare
                    if (w_gs_type == DESC_STREAM_INPUT && w_gs_index == 16'd0)
                      fmt_in0_r <= {w_b6, w_b7, w_b8, w_b9,
                                    w_b10, w_b11, w_b12, w_b13};
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
                if (w_gs_type == DESC_STREAM_OUTPUT && w_gs_index == 16'd0) begin
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
                end else if (w_gs_type == DESC_STREAM_INPUT && w_gs_index < 16'd2) begin
                  // Listener sinks (reference populate_input_response):
                  // identity fields exposed unconditionally (*_VALID means
                  // "meaningful", zero is a valid value); CONNECTED/
                  // FAST_CONNECT/SAVED_STATE/STREAMING_WAIT when bound;
                  // SRP failure flags from the TalkerFailed registrar;
                  // trailer = flags_ex REGISTERING + {pbsta, acmpsta}.
                  // Sink 1 (CRF) has no listener SM yet: unbound shape.
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2;  seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0;  seg_len_q[1] <= 16'd4;
                  seg_kind_q[2] <= SEG_STORE;
                  seg_addr_q[2] <= (w_gs_index == 16'd0) ? WB_STREAM_IN0_FMT_C
                                                         : WB_STREAM_IN1_FMT_C;
                  seg_len_q[2]  <= 16'd8;
                  seg_kind_q[3] <= SEG_CONST; seg_addr_q[3] <= 16'd8;  seg_len_q[3] <= 16'd40;
                  load_input_stream_info_consts(w_gs_index == 16'd0);
                  cdl_q <= 11'd68;
                end else begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd4;
                  cdl_q        <= 11'd16;
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
              // commands (the reference replies not-supported for outputs).
              // The input "started" level feeds the STREAMING_WAIT flag in
              // GET_STREAM_INFO; power-on started (no STREAMING_WAIT bind
              // plumbing yet — documented simplification).
              CMD_START_STREAMING, CMD_STOP_STREAMING: begin
                if (w_gs_type == DESC_STREAM_INPUT && w_gs_index < 16'd2) begin
                  status_q     <= l0_reject_q ? l0_status_q : STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO; seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  cdl_q        <= 11'd16;
                  if (!l0_reject_q && w_gs_index == 16'd0)
                    started_in_r <= (hdr_q.command_type == CMD_START_STREAMING);
                end else begin
                  status_q <= STATUS_NOT_SUPPORTED;
                end
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
                  //! propagation delay = live measured value (CSR, USER bug 3)
                  const_q[8]  <= pdelay_ns_i[31:24]; const_q[9]  <= pdelay_ns_i[23:16];
                  const_q[10] <= pdelay_ns_i[15:8];  const_q[11] <= pdelay_ns_i[7:0];
                  const_q[12] <= gptp_domain_i;
                  //! flags: SRP_ENABLED (0x04) | GPTP_GM_SUPPORTED-present
                  //! (0x02) once the daemon publishes a grandmaster
                  const_q[13] <= w_gm_present ? 8'h06 : 8'h04;
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
                // valid mask + counters 0..5 ride one 28-byte CONST segment
                // (block byte 4n = counter for valid-mask bit n); the rest of
                // the 128-byte block is zeros via SEG_NONE.
                seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd28;
                seg_kind_q[2] <= SEG_NONE;  seg_addr_q[2] <= 16'd0; seg_len_q[2] <= 16'd104;
                for (int k = 0; k < 28; k++) const_q[k] <= 8'h00;
                cdl_q <= 11'd148;   // 12 + 136
                if (w_gs_type == DESC_STREAM_OUTPUT && w_gs_index == 16'd0) begin
                  status_q   <= STATUS_SUCCESS;
                  const_q[3] <= 8'h1F;   // START|STOP|MEDIA_RESET|TS_UNC|FRAMES_TX
                  for (int k = 0; k < 4; k++) begin
                    const_q[4+k]  <= cnt_start_r [8*(3-k) +: 8];  // bit0
                    const_q[8+k]  <= cnt_stop_r  [8*(3-k) +: 8];  // bit1
                    const_q[20+k] <= frames_tx_i [8*(3-k) +: 8];  // bit4
                  end
                end else if (w_gs_type == DESC_AVB_INTERFACE && w_gs_index == 16'd0) begin
                  status_q   <= STATUS_SUCCESS;
                  const_q[3] <= 8'h23;   // LINK_UP|LINK_DOWN|GPTP_GM_CHANGED
                  for (int k = 0; k < 4; k++) begin
                    const_q[4+k]  <= cnt_linkup_r[8*(3-k) +: 8];  // bit0
                    const_q[8+k]  <= cnt_linkdn_r[8*(3-k) +: 8];  // bit1
                    const_q[24+k] <= cnt_gmchg_r [8*(3-k) +: 8];  // bit5
                  end
                end else if (w_gs_type == DESC_CLOCK_DOMAIN && w_gs_index == 16'd0) begin
                  // Milan 5.4.4 mandatory (la_avdecc field report): the
                  // domain's media clock locks with the bound input stream,
                  // so LOCKED/UNLOCKED mirror the RX monitor's media-lock
                  // events (talker-only operation reads 0 - never locked)
                  status_q   <= STATUS_SUCCESS;
                  const_q[3] <= 8'h03;   // LOCKED|UNLOCKED
                  for (int k = 0; k < 4; k++) begin
                    const_q[4+k] <= in0_cnt_locked_i  [8*(3-k) +: 8];  // bit0
                    const_q[8+k] <= in0_cnt_unlocked_i[8*(3-k) +: 8];  // bit1
                  end
                end else if (w_gs_type == DESC_STREAM_INPUT && w_gs_index < 16'd2) begin
                  // sinks: live KL_avtp_rx_monitor counters (Table 7-156);
                  // the mask+counters need block bytes 0..47 (FRAMES_RX =
                  // bit 11 at 44), so the CONST segment grows to 52
                  status_q     <= STATUS_SUCCESS;
                  seg_len_q[1] <= 16'd52;
                  seg_len_q[2] <= 16'd80;
                  load_input_counters_consts(w_gs_index == 16'd0);
                end else if (w_gs_type == DESC_ENTITY && w_gs_index == 16'd0) begin
                  // Hive/la_avdecc queries ENTITY counters: no entity-level
                  // counters defined -> SUCCESS with an EMPTY valid mask
                  // (BAD_ARGUMENTS logged as a bad-values error, field report)
                  status_q <= STATUS_SUCCESS;
                end else if (acc_found) begin
                  status_q <= STATUS_BAD_ARGUMENTS;      // descriptor w/o counters
                end else begin
                  status_q <= STATUS_NO_SUCH_DESCRIPTOR;
                end
              end

              // -------------------------------------------------- //
              // GET_DYNAMIC_INFO (Milan v1.2 0x4B; reference
              // cmd-get-dynamic-info.c): aggregate of every mutable
              // descriptor field. Our fixed entity => FIXED 116-B payload:
              // cfg_idx(2)+rsvd(2), then ENTITY(8) AUDIO_UNIT(8)
              // STREAM_IN0/IN1/OUT(28 each: sid=0, format from store,
              // flags=FORMAT_VALID only, tail 0 - reference behavior)
              // CLOCK_DOMAIN(8). CDL 128.
              CMD_GET_DYNAMIC_INFO: begin
                if ({w_b2, w_b3} != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd4;
                  cdl_q        <= 11'd16;
                end
                else begin
                  status_q <= STATUS_SUCCESS;
                  cdl_q    <= 11'd124;   // 12 + 4 + 108 record bytes
                  // seg0 = default ECHO(2,4) = config_index + reserved
                  seg_kind_q[1]  <= SEG_CONST; seg_addr_q[1]  <= 16'd0;  seg_len_q[1]  <= 16'd12;
                  seg_kind_q[2]  <= SEG_STORE; seg_addr_q[2]  <= WB_SAMPLING_RATE_C; seg_len_q[2] <= 16'd4;
                  seg_kind_q[3]  <= SEG_CONST; seg_addr_q[3]  <= 16'd12; seg_len_q[3]  <= 16'd12;
                  seg_kind_q[4]  <= SEG_STORE; seg_addr_q[4]  <= WB_STREAM_IN0_FMT_C; seg_len_q[4] <= 16'd8;
                  seg_kind_q[5]  <= SEG_CONST; seg_addr_q[5]  <= 16'd24; seg_len_q[5]  <= 16'd8;
                  seg_kind_q[6]  <= SEG_CONST; seg_addr_q[6]  <= 16'd32; seg_len_q[6]  <= 16'd12;
                  seg_kind_q[7]  <= SEG_STORE; seg_addr_q[7]  <= WB_STREAM_IN1_FMT_C; seg_len_q[7] <= 16'd8;
                  seg_kind_q[8]  <= SEG_CONST; seg_addr_q[8]  <= 16'd44; seg_len_q[8]  <= 16'd8;
                  seg_kind_q[9]  <= SEG_CONST; seg_addr_q[9]  <= 16'd52; seg_len_q[9]  <= 16'd12;
                  seg_kind_q[10] <= SEG_STORE; seg_addr_q[10] <= WB_STREAM_FORMAT_C;  seg_len_q[10] <= 16'd8;
                  seg_kind_q[11] <= SEG_CONST; seg_addr_q[11] <= 16'd64; seg_len_q[11] <= 16'd8;
                  seg_kind_q[12] <= SEG_CONST; seg_addr_q[12] <= 16'd72; seg_len_q[12] <= 16'd4;
                  seg_kind_q[13] <= SEG_STORE; seg_addr_q[13] <= WB_CLOCK_SRC_IDX_C;  seg_len_q[13] <= 16'd2;
                  seg_kind_q[14] <= SEG_CONST; seg_addr_q[14] <= 16'd76; seg_len_q[14] <= 16'd2;
                  // const image (zeros elsewhere): record headers + flags
                  for (int k = 0; k < 78; k++) const_q[k] <= 8'h00;
                  const_q[9]  <= 8'h02;                     // AUDIO_UNIT type
                  const_q[13] <= 8'h05;                     // STREAM_INPUT
                  const_q[33] <= 8'h05; const_q[35] <= 8'h01; // IN idx 1
                  const_q[53] <= 8'h06;                     // STREAM_OUTPUT
                  const_q[24] <= 8'h80;                     // IN0 FORMAT_VALID
                  const_q[44] <= 8'h80;                     // IN1 FORMAT_VALID
                  const_q[64] <= 8'h80;                     // OUT FORMAT_VALID
                  const_q[72] <= 8'h00; const_q[73] <= 8'h24; // CLOCK_DOMAIN
                end
              end

              // -------------------------------------------------- //
              // SET/GET_MAX_TRANSIT_TIME (1722.1-2021 §7.4.39 at the
              // la_avdecc-verified codes 0x4C/0x4D; payload = type(2)+
              // index(2)+max_transit_time u64 ns): reflects/updates the same
              // presentation offset SET_STREAM_INFO(ACC_LAT) drives — one
              // source of truth for the framer's timestamp offset.
              CMD_SET_MAX_TRANSIT_TIME, CMD_GET_MAX_TRANSIT_TIME: begin
                cdl_q <= 11'd24;   // 12 + 12
                if (l0_reject_q) begin
                  status_q     <= l0_status_q;
                  seg_len_q[0] <= 16'd12;
                end else if (w_gs_type != DESC_STREAM_OUTPUT || w_gs_index != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd12;
                end else if (hdr_q.command_type == CMD_SET_MAX_TRANSIT_TIME &&
                             ({w_b6, w_b7, w_b8, w_b9} != 32'd0 ||
                              w_b10[7])) begin
                  status_q     <= STATUS_BAD_ARGUMENTS;   // > 0x7FFFFFFF ns
                  seg_len_q[0] <= 16'd12;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd8;
                  const_q[0] <= 8'h00; const_q[1] <= 8'h00;
                  const_q[2] <= 8'h00; const_q[3] <= 8'h00;
                  if (hdr_q.command_type == CMD_SET_MAX_TRANSIT_TIME) begin
                    const_q[4] <= w_b10; const_q[5] <= w_b11;
                    const_q[6] <= w_b12; const_q[7] <= w_b13;
                    pres_wr_p_o   <= 1'b1;
                    pres_wr_val_o <= {w_b10, w_b11, w_b12, w_b13};
                  end else begin
                    const_q[4] <= pres_offset_i[31:24];
                    const_q[5] <= pres_offset_i[23:16];
                    const_q[6] <= pres_offset_i[15:8];
                    const_q[7] <= pres_offset_i[7:0];
                  end
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
              //! USER bug 4 (07-18): with a foreign GM published (CSR) the
              //! path is [GM, our clock] (count=2); GM-is-us / no GM keeps
              //! the self-only path. Errors keep the legacy 12 B payload.
              CMD_GET_AS_PATH: begin
                seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd2;
                seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd10;
                cdl_q <= 11'd24;   // 12 + 12
                const_q[0] <= 8'h00;
                for (int k = 2; k < 18; k++) const_q[k] <= 8'h00;
                if (w_as_path_idx == 16'd0) begin
                  status_q   <= STATUS_SUCCESS;
                  if (w_gm_foreign) begin
                    seg_len_q[1] <= 16'd18;
                    cdl_q        <= 11'd32;   // 12 + 4 + 16
                    const_q[1]   <= 8'h02;                    // count = 2
                    for (int k = 0; k < 8; k++)
                      const_q[2+k] <= gptp_gm_id_i[8*(7-k) +: 8];
                    for (int k = 0; k < 8; k++)
                      const_q[10+k] <= w_self_ckid[8*(7-k) +: 8];
                  end else begin
                    const_q[1] <= 8'h01;                      // count = 1
                    for (int k = 0; k < 8; k++)
                      const_q[2+k] <= w_self_ckid[8*(7-k) +: 8];
                  end
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
            st_wdata_o <= bufb(cbuf_r[w_wbaddr[6:3]], w_wbaddr[2:0]);
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
              SEG_ECHO:  b = bufb(cbuf_r[w_eaddr[6:3]], w_eaddr[2:0]);
              SEG_STORE: b = st_byte_i;       // store byte (1-cycle read latency)
              SEG_CONST: b = const_q[7'(emseg_addr_r[6:0] + emsoff_r[6:0])];
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
            // a SUCCESS state-changing SET: replay its response (u=1) to
            // every registered controller except the originator
            if (!unsol_frame_r && !vu_q && status_q == STATUS_SUCCESS &&
                is_replay_cmd(hdr_q.command_type))
              for (int sl = 0; sl < UNSOL_SLOTS_C; sl++)
                if (unsol_valid_r[sl] &&
                    unsol_eid_r[sl] != hdr_q.controller_entity_id)
                  unsol_pend4_r[sl] <= 1'b1;
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
