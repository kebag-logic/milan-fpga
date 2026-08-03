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
                  GET_AUDIO_MAP                        (Milan 5.4.2.26 splits
                                                        by direction: EVERY
                                                        STREAM_PORT_INPUT is
                                                        served from its OWN
                                                        base_map via
                                                        AEM_SMAP_*, and a
                                                        STREAM_PORT_OUTPUT
                                                        that HAS a map is
                                                        NOT_SUPPORTED, as
                                                        ADD/REMOVE already
                                                        were. Under
                                                        `AEM_DYNMAP EVERY
                                                        map_mode-dynamic
                                                        STREAM_PORT_INPUT is
                                                        served from the shared
                                                        mappings store keyed by
                                                        GLOBAL cluster index:
                                                        ADD/REMOVE/GET per
                                                        Milan 5.4.2.26-28,
                                                        5.3.3.9, 5.3.10.1)
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
  //! ACQUIRE/LOCK target descriptor is ENTITY/0 (KL_aecp_common_parser).
  //! Settled two beats AFTER hdr_valid and then held for the frame, so it is
  //! read live in DECIDE_S rather than latched with the rest of the header.
  input  wire          al_desc_ok_i,

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
  //! per-STREAM_OUTPUT presentation offsets (max transit time /
  //! msrp_accumulated_latency, ns): flat 16-entry vector; entry k is the
  //! offset talker k stamps into its avtp_timestamp (the CRF Media Clock
  //! Output's entry included). The register file itself lives in this
  //! module (see pres_file_r); entries past the shape's STREAM_OUTPUT
  //! count are tied to the reset default.
  output wire [16*32-1:0] pres_offset_all_o,
  output logic         identify_o,         //! IDENTIFY control active (LED hook)

  // ---- dynamic audio-map render taps (gaps item 8; live only under ----
  // ---- `AEM_DYNMAP - static shapes tie the defaults ch0/ch1, en=0) ----
  output wire [3:0]    dmap_l_ch_o,        //! cluster 0 (render L) stream ch
  output wire          dmap_l_en_o,        //! cluster 0 mapping valid
  output wire [3:0]    dmap_r_ch_o,        //! cluster 1 (render R) stream ch
  output wire          dmap_r_en_o,        //! cluster 1 mapping valid
  //! chmap64 fabric binding (docs/CHMAP64_AEM_BINDING.md): every ACCEPTED
  //! ADD/REMOVE commit is mirrored into the render crossbar's map RAM as a
  //! one-write-per-record strobe stream. Word = the render RAM format
  //! {en[7], 1'b0, stream[5:3], ch[2:0]}; REMOVE writes 0 (en=0).
  output logic         dmap_wr_p_o,        //! 1-cycle map-RAM write strobe
  output logic [5:0]   dmap_wr_addr_o,     //! cluster_offset = phys channel idx
  output logic [7:0]   dmap_wr_word_o,     //! render map word (see above)
  //! talker-side mirror (USER 08-01): every ACCEPTED output-map record commit
  //! is one CAPTURE-crossbar map write. Word = KL_chan_map_capture's entry
  //! {half[13:12], idxh[11:8], en[7], src[6:4], idx[3:0]}. The write is a
  //! READ-MODIFY-WRITE of the addressed PAIR SLOT: the record names ONE
  //! stream channel, so half[] is rebuilt from the live store for BOTH of
  //! the slot's channels and the sibling's arming survives untouched. A
  //! REMOVE that empties the slot writes 0 (en=0, half=0).
  output logic         odmap_wr_p_o,       //! 1-cycle capture-map write strobe
  output logic [4:0]   odmap_wr_slot_o,    //! packetizer pair slot
  output logic [13:0]  odmap_wr_word_o,    //! capture map word (see above)
  input  wire          link_up_i,          //! PHY link (AVB_INTERFACE counters)

  // ---- listener sink state (KL_acmp_listener; STREAM_INPUT[0]) --------
  input  wire          lstn_bound_i,       //! listener SM not UNBOUND
  input  wire [63:0]   lstn_sid_i,         //! bound stream_id
  input  wire [47:0]   lstn_dmac_i,
  // ---- CRF sink state (sink 1 record in the same listener SM) ---------
  input  wire          lstn1_bound_i,
  input  wire [63:0]   lstn1_sid_i,
  input  wire [47:0]   lstn1_dmac_i,
  output wire [31:0]   bdbg0_o,            //! BSCAN forensics (CSR RO)
  output wire [31:0]   bdbg1_o,
  output wire [31:0]   bdbg2_o,
  input  wire [11:0]   lstn_vlan_i,
  input  wire [1:0]    lstn_pbsta_i,       //! probing status
  input  wire [4:0]    lstn_acmpsta_i,     //! last ACMP status
  input  wire [63:0]   as_parent_ckid_i,   //! 802.1AS parent bridge ckid (0=none)
  input  wire [7:0]    lstn_fail_code_i,
  input  wire [63:0]   lstn_fail_bridge_i,
  input  wire [11:0]   lstn_ta_vlan_i,
  input  wire [31:0]   lstn_ta_acclat_i,
  input  wire          tk_fail_valid_i,
  input  wire [7:0]    tk_fail_code_i,
  input  wire [63:0]   tk_fail_bridge_i,
  input  wire [11:0]   srp_domain_vid_i,
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
  input  wire [31:0]   in0_cnt_tv_i,       //! TIMESTAMP_VALID (bit 6, Milan 1.3)
  input  wire [31:0]   in0_cnt_tnv_i,      //! TIMESTAMP_NOT_VALID (bit 7)
  input  wire          in0_cnt_dirty_p_i,  //! monitor: a counter changed
  output logic [63:0]  in0_fmt_o,          //! live STREAM_INPUT[0] format u64
  output logic [15:0]  clk_src_o,          //! live CLOCK_DOMAIN clock_source_index

  // ---- Milan 5.4.2.25 per-index counters (Tables 5.16/5.17) -----------
  //! "shall implement and return the counters" for EACH stream descriptor:
  //! the builder presents the descriptor_index it is serving and latches
  //! the pre-muxed counters in its const-load cycle. rxdiag = the RX
  //! monitor's ten Table 5.6 counters plus the two Milan 1.3 tv tallies
  //! (C_ML..C_FRX,C_TV,C_TNV order) for that sink;
  //! tkdiag = KL_talker_diag_ctx's five Table 5.4 counters
  //! {FTX, TU, MRESET, STOP, START} for that source (CRF included).
  output logic [3:0]   gs_diag_idx_o,
  input  wire [12*32-1:0] rxdiag_cnt_i,
  input  wire [5*32-1:0]  tkdiag_cnt_i,
  //! per-STREAM_OUTPUT "a Table 5.4 counter was written" pulses
  //! (KL_talker_diag_ctx.dirty_p_o, zero-extended to the 4-bit index
  //! space; unwired indexes stay tied 0 and their limiters synth away).
  //! Milan 5.4.5 Table 5.22: each pulse owes every registered controller
  //! an unsolicited GET_COUNTERS(STREAM_OUTPUT, idx), at most one per
  //! descriptor per second.
  input  wire [15:0]   tkdiag_dirty_p_i,
  //! AAF sink count: the sink at it (the CRF Media Clock Input) has no
  //! monitor context and answers the Milan-mandatory ten from KL_crf_rx
  input  wire [15:0]   n_aaf_sinks_i,
  // ---- CRF Media Clock Input counters (KL_crf_rx; Milan Table 5.16) ---
  input  wire [31:0]   crf_cnt_locked_i,    //! MEDIA_LOCKED (bit 0)
  input  wire [31:0]   crf_cnt_unlocked_i,  //! MEDIA_UNLOCKED (bit 1)
  input  wire [31:0]   crf_cnt_intr_i,      //! STREAM_INTERRUPTED (bit 2)
  input  wire [7:0]    crf_cnt_seqerr_i,    //! SEQ_NUM_MISMATCH (bit 3)
  input  wire [15:0]   crf_cnt_mreset_i,    //! MEDIA_RESET (bit 4)
  input  wire [15:0]   crf_cnt_tu_i,        //! TIMESTAMP_UNCERTAIN (bit 5)
  input  wire [7:0]    crf_cnt_fmterr_i,    //! UNSUPPORTED_FORMAT (bit 8)
  input  wire [15:0]   crf_cnt_late_i,      //! LATE_TIMESTAMP (bit 9)
  input  wire [15:0]   crf_cnt_early_i,     //! EARLY_TIMESTAMP (bit 10)
  input  wire [15:0]   crf_cnt_pdu_i,       //! FRAMES_RX (bit 11)

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
  localparam int unsigned BUF_BYTES_C = 512;   //! grown for 7.4.76 batches

  logic [63:0] cbuf_r [0:63];              //! big-lane capture words (RAM)
  logic [63:0] cw0_r, cw1_r, cw3_r;        //! decode captures: bytes 0-15, 24-31
  logic [6:0]  beat_r;                     //! frame beat counter (sat at 127)

  //! buf byte accessor (big lane order: byte j of word w = tdata[8*(7-j)])
  function automatic [7:0] bufb(input [63:0] w, input [2:0] j);
    bufb = w[8*(3'd7 - j) +: 8];
  endfunction

  //! state-changing SETs whose SUCCESS response is replayed u=1 to the other
  //! registered controllers (IEEE 1722.1-2021 unsolicited rule; reference
  //! reply-unsol-helpers.c). The ta/lo state-edge push path is separate.
  function automatic logic is_replay_cmd(input [14:0] c);
    is_replay_cmd = (c == CMD_SET_STREAM_FORMAT) || (c == CMD_SET_NAME) ||
                    (c == CMD_SET_SAMPLING_RATE) || (c == CMD_SET_CLOCK_SOURCE) ||
                    (c == CMD_SET_CONTROL) || (c == CMD_START_STREAMING) ||
                    (c == CMD_STOP_STREAMING) || (c == CMD_SET_MAX_TRANSIT_TIME) ||
                    (c == CMD_SET_CONFIGURATION) ||  // CERT es-4.3
                    // dynamic audio maps (7.4.45/46 "On success this command
                    // also sends an unsolicited notification"). SUCCESS-gated
                    // in CONCLUDE_S, so static shapes (NOT_SUPPORTED) never
                    // replay - behavior-identical for the deployed build.
                    (c == CMD_ADD_AUDIO_MAPPINGS) ||
                    (c == CMD_REMOVE_AUDIO_MAPPINGS) ||
                    (c == CMD_SET_STREAM_INFO);      // CERT es-4.5: replay the
                                                     // SET response u=1 (the
                                                     // echo-based rebuild
                                                     // handles its payload
                                                     // like SET_STREAM_FORMAT)
  endfunction

  //! no-change SET: SUCCESS but nothing changed -> suppress the u=1 replay
  //! (1722.1 unsolicited rule notifies STATE CHANGES; CERT es-4.5 asserts a
  //! same-value SET_STREAM_INFO does NOT notify)
  logic nochg_q;

  wire w_cap_hs = s_axis_tvalid & s_axis_tready;

  wire [8:0] w_eaddr  = 9'(emseg_addr_r + emsoff_r
                           + (batch_q ? brec_abase_q : 16'd0)); //! echo RAM addr
                           //! (batch: arm echo addrs are record-virtual)
  wire [8:0] w_wbaddr = 9'(wb_src_q + wb_cnt_r);           //! wb RAM addr
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
  //! (buf bytes 14-15 were the ACQUIRE/LOCK descriptor_type decode; that
  //! whole field now arrives on al_desc_ok_i, so cw1_r's last two bytes have
  //! no reader and synthesis prunes them)
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
    CONCLUDE_S,
    BSCAN_S,        //! 0x4B pass 1: validate records, size the response
    BREC_SETUP_S,   //! 0x4B pass 2: parse/classify one record
    RECHDR_EMIT_S,  //! 0x4B pass 2: pack the 8-byte record header
    DMAP_SCAN_S,    //! `AEM_DYNMAP: ADD/REMOVE mapping walk (validate/commit)
    DMAP_GET_S,     //! `AEM_DYNMAP: GET_AUDIO_MAP page scan -> const scratch
    DMAP_PRUNE_S    //! `AEM_DYNMAP: withdraw mappings a format shrink orphaned
  } state_t;
  state_t state_r;

  //! accept command beats only while idle/capturing (backpressures the
  //! pipeline — and therefore the tap FIFO — while a response is in flight)
  //! replays must drain before a new command may overwrite the capture
  //! buffer the replayed response is rebuilt from
  //! BSCAN_S hold: a padded frame's cdl is satisfied (frame_ok -> DECIDE)
  //! BEFORE its tlast, so the pad tail is still in flight when the batch
  //! scan starts - keep draining it (the capture block runs in any state)
  //! or cap_done never sets and the scan would read unwritten cbuf words
  //! (silicon-caught: every record parsed as garbage -> BAD_ARGUMENTS
  //! while the TB's back-to-back feed won the race).
  assign s_axis_tready = (state_r == IDLE_S && unsol_pend4_r == '0) ||
                         (state_r == CAPTURE_S) ||
                         (state_r == BSCAN_S && !cap_done_q);

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
  //! DECIDE_S case selector: a batch sub-command substitutes the record's
  //! command_type (the arms' internal GET/SET disambiguation still reads
  //! hdr_q.command_type = 0x4B, which never equals a SET - GET semantics)
  wire [14:0] w_cmd_eff = bsub_q ? brec_cmd_q : hdr_q.command_type;

  //! ECHOED control_data_length, clamped to what the response can actually
  //! carry. The echo segment is already capped at 494 octets (the capture
  //! buffer holds 64 beats = 512 B from beat 3, and 12 of the AECPDU header
  //! precede the echo), so the HEADER field must be capped at the matching
  //! 506 = 12 + 494. Echoing the command's raw value made the length field
  //! LIE for any command declaring more: the response carried 506 octets
  //! while announcing up to 2047, and a conformant receiver reading
  //! control_data_length octets walks off the end of the frame. Raising the
  //! 60-mapping ADD/REMOVE cap without this clamp in place would put that
  //! path back in reach, which is why the two travel together.
  wire [10:0] w_cdl_echo = (hdr_q.control_data_length > 11'd506)
                           ? 11'd506 : hdr_q.control_data_length;

  wire [15:0] w_gs_type  = {w_b2, w_b3};   //! GET/SET_* desc type
  wire [15:0] w_gs_index = {w_b4, w_b5};
  //! per-index counter mux select for the datapath (monitor mirror +
  //! talker diag): valid whenever w_gs_index is, i.e. through the whole
  //! const-load cycle of a GET_COUNTERS dispatch. Pre-mux: while a
  //! STREAM_OUTPUT counter push waits in IDLE_S the read port serves the
  //! PUSH's index instead (no command stands behind w_gs_index there, and
  //! the push branch latches tkdiag_cnt_i in its own IDLE cycle); every
  //! dispatched command samples from DECIDE_S onward, where the override
  //! is structurally inactive.
  assign gs_diag_idx_o = (state_r == IDLE_S && w_pend5_any)
                       ? w_unsol_push5_oidx
                       : w_gs_index[3:0];
  //! SET_STREAM_INFO (Milan §5.4.2.9): payload byte n = buf_r[n+2] — flags at
  //! payload 4-7, msrp_accumulated_latency at payload 24-27.
  wire [31:0] w_si_flags = {w_b6,  w_b7,  w_b8,  w_b9};
  wire [31:0] w_si_lat   = {w_b26, w_b27, w_b28, w_b29};
  //! Spec-defined sub-command bits (reference valid_mask: aecp-aem.h bits 0-9
  //! + 25-31) minus the ONE supported (MSRP_ACC_LAT_VALID, bit 29): any of
  //! these requested -> NOT_SUPPORTED for the whole command (§5.4.2.9).
  localparam [31:0] SI_UNSUPPORTED_MASK_C = 32'hDE00_03FF;
  //! ACQUIRE/LOCK target descriptor: the type is at payload bytes 14-15 but
  //! the INDEX is at 16-17, which this module never captures (cw2_r is
  //! deliberately not registered). KL_aecp_common_parser sees both on the
  //! wire and publishes the whole verdict on al_desc_ok_i, held for the
  //! frame — one decode, shared with the entity state machine, and no
  //! second 64-bit capture register in the block that owns the critical
  //! path.
  wire        w_lock_desc_ok = al_desc_ok_i;
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

  // ------------------------------------------------------------------ //
  // REGISTERED directory oracle (AX 100 MHz WNS -0.384, 157 endpoints;  //
  // then the placer round: distributed ROM broke slice packing).        //
  //                                                                      //
  // History in two cuts. (1) The lookups were LINEAR SCANS over the     //
  // generated entity image - AEM_DESC_N_C is 252 on the 8x8 ship shape  //
  // - evaluated INSIDE the DECIDE_S dispatch: one unbroken 14-16 level  //
  // cone from cw0_r through the 252-entry match tree into the ~40-arm   //
  // case. DECIDE_S got TWO phases: phase 0 resolved the oracles into    //
  // registers, phase 1 dispatched on the registers. (2) The scans then  //
  // became a generated two-level table; its level-2 directory now lives //
  // in BLOCK RAM inside KL_aecp_accessor, so the resolve is a           //
  // SYNCHRONOUS read: phase 0 strobes u_acc.en_i (the BRAM latches      //
  // address + hit), and the accessor's outputs ARE the phase-0          //
  // registers - frozen until the next strobe, same cycle count, same    //
  // bits. The name lookup no longer reads any ROM at all: object_name   //
  // sits at base + 4 for every structurally-named descriptor            //
  // (generator-asserted), so aem_name_qual derives it from the          //
  // accessor's registered answer during dispatch.                       //
  //                                                                      //
  // The split is coherent because every oracle input (cw0_r/cw3_r,      //
  // hdr_q, vu_q) is latched BEFORE DECIDE_S is entered and nothing      //
  // inside DECIDE_S writes one: s_axis_tready is low in DECIDE_S so no  //
  // beat can land, hdr_q is captured in IDLE_S/CAPTURE_S, and the batch //
  // record's virtual arg window is loaded in BREC_SETUP_S phase 4 (the  //
  // last write before its state_r <= DECIDE_S). One extra cycle per     //
  // command - free at AECP command pace, microseconds apart.            //
  //                                                                      //
  // Invariant: every entry into DECIDE_S arrives with dc_ph_r == 0. It  //
  // is SET only in phase 0 and CLEARED unconditionally in phase 1, so a //
  // dispatch arm that re-enters DECIDE_S still starts at phase 0.       //
  logic        dc_ph_r;       //! DECIDE_S phase (0 = resolve, 1 = dispatch)

  //! descriptor lookup — inputs muxed combinationally by command layout
  wire w_is_read_desc = !vu_q && (hdr_q.command_type == CMD_READ_DESCRIPTOR);
  wire [15:0] acc_type  = w_is_read_desc ? w_rd_type  : w_gs_type;
  wire [15:0] acc_index = w_is_read_desc ? w_rd_index : w_gs_index;
  wire         w_acc_en = (state_r == DECIDE_S) && !dc_ph_r;
  wire         acc_found;
  wire [15:0]  acc_base, acc_len;
  KL_aecp_accessor u_acc (
    .clk_i        (clk_i),
    .rst_n        (rst_n),
    .en_i         (w_acc_en),
    .config_idx_i (16'd0),
    .desc_type_i  (acc_type),
    .desc_index_i (acc_index),
    .found_o      (acc_found),
    .base_o       (acc_base),
    .len_o        (acc_len)
  );

  // function result captured in a net: indexing a call expression directly
  // (aem_name_qual(...)[16]) is SV-only — sv2v keeps it and Yosys' V2005
  // reader rejects it, breaking the open-toolchain portability gate. The
  // qualifier itself is generated (gen/aecp_aem_rom.svh) so the name rule
  // always matches the descriptor image. Valid during dispatch (phase 1),
  // when acc_found/acc_base hold the answer for (w_gs_type, w_gs_index) —
  // any command that reads it resolves the accessor with exactly those
  // inputs (only READ_DESCRIPTOR muxes others in, and it never reads this).
  wire [16:0] w_name_ptr =
      aem_name_qual(w_gs_type, w_gs_index, w_name_idx,
                    acc_found, acc_base);   //! {valid, wb addr}

  //! A SET_SAMPLING_RATE is accepted iff the rate is one this entity actually
  //! ADVERTISES, so the check must range over the generated table, not over a
  //! hardcoded three. It read AEM_RATES_C[0], [1] and [2] literally, which was
  //! only ever correct while every config published exactly three rates: the
  //! 8x8 ship config publishes ONE (audio_unit_rates_hz: [48000]), making [1]
  //! and [2] reads off the end of a [0:0] array. Synthesis returns zero for an
  //! out-of-range read, so the accept still worked - by accident, and it would
  //! have ACCEPTED a SET of rate 0 on any entity whose table is short. Loop to
  //! the generated bound instead (gen/aecp_aem_rom.svh AEM_RATES_N_C).
  logic w_rate_ok;
  always_comb begin
    w_rate_ok = 1'b0;
    for (int unsigned ri = 0; ri < AEM_RATES_N_C; ri++)
      if (w_set_rate == AEM_RATES_C[ri]) w_rate_ok = 1'b1;
  end
  //! Milan adaptive listener (FR-STR-03; USER 07-17) + Milan 6.4 family
  //! coverage (USER-caught 2026-07-21): the advertised list is the 48k
  //! ut-string (all counts 1..8 in one entry); a SET must be CONCRETE
  //! (ut=0) with channels 1..8 on the 48k base. The mask clears both the
  //! channels field (bits 31:22) and the ut bit (52) so concrete SETs
  //! compare against either list entry. 96k/192k dropped with the
  //! honesty pass (the render path is 48k-only).
  localparam [63:0] FMT_BASE_MASK_C = ~((64'h3FF << 22) | (64'h1 << 52));
  wire [9:0]  w_fmt_ch    = w_set_fmt[31:22];
  wire [63:0] w_fmt_chm   = w_set_fmt & FMT_BASE_MASK_C;
`ifdef AEM_PER_STREAM_FMT
  //! per-descriptor format references (multi-stream svh layout): the
  //! addressed descriptor's own table entry drives validation and the WB
  //! address. Index clamped for the constant-array mux; range validity is
  //! decided separately in the STREAM_FORMAT arm.
  wire [3:0] w_in_fidx  = (w_gs_index < 16'(AEM_N_STRIN_C))
                        ? w_gs_index[3:0] : 4'd0;
  wire [3:0] w_out_fidx = (w_gs_index < 16'(AEM_N_STROUT_C))
                        ? w_gs_index[3:0] : 4'd0;
  wire [63:0] w_in_ref_fmt  = AEM_STRIN_FMT_C[w_in_fidx];
  wire [63:0] w_out_ref_fmt = AEM_STROUT_FMT_C[w_out_fidx];
  //! AAF sinks: the Milan 6.4 family rule against THIS descriptor's base;
  //! CRF sinks: exact match (same rules as the legacy pair, per descriptor)
  wire w_fmt_ok = AEM_STRIN_CRF_C[w_in_fidx]
                ? (w_set_fmt == w_in_ref_fmt)
                : ((w_fmt_ch >= 10'd1) && (w_fmt_ch <= 10'd8) &&
                   !w_set_fmt[52] &&
                   (w_fmt_chm == (w_in_ref_fmt & FMT_BASE_MASK_C)));
  //! talker truth per descriptor: outputs accept ONLY their declared format
  wire w_out_fmt_ok = (w_set_fmt == w_out_ref_fmt);
  //! which STREAM_INPUT descriptor carries the CRF (media-clock) sink — the
  //! generated flag, so the GET_STREAM_INFO live-record pick never hardcodes
  //! an index (NxN shapes put the CRF sink LAST: index 4 at 4x4, 8 at 8x8)
  wire w_si_in_crf = (w_gs_index < 16'(AEM_N_STRIN_C)) &&
                     AEM_STRIN_CRF_C[w_in_fidx];
`else
  wire w_fmt_ok  = (w_fmt_ch >= 10'd1) && (w_fmt_ch <= 10'd8) &&
                   !w_set_fmt[52] &&
                   (w_fmt_chm == (AEM_FMTS_C[0] & FMT_BASE_MASK_C));
  //! talker truth: the framer is hardwired stereo 48k - STREAM_OUTPUT
  //! accepts ONLY the wire-true format (declared == transmitted, user bug 5)
  localparam [63:0] AAF_OUT_FMT_C =
      (AEM_FMTS_C[0] & FMT_BASE_MASK_C) | (64'd2 << 22);
  wire w_out_fmt_ok = (w_set_fmt == AAF_OUT_FMT_C);
  wire w_crf_fmt_ok = (w_set_fmt == AEM_CRF_FMTS_C[0]);
  //! deployed 1-AAF-input shape: STREAM_INPUT[1] IS the CRF sink
  wire w_si_in_crf = (w_gs_index == 16'd1);
`endif

  // ------------------------------------------------------------------ //
  // GET_STREAM_INFO addressing (defect D1, silicon 2026-07-27 gw 0x0016) //
  //                                                                      //
  // IEEE Std 1722.1-2021 §7.4.16.2 defines ONE GET_STREAM_INFO_RESPONSE  //
  // per {descriptor_type, descriptor_index}; §7.4.5 makes the descriptor //
  // DIRECTORY the statement of which of those pairs exist. This arm used //
  // to key off literal indices (STREAM_OUTPUT == 0, STREAM_INPUT < 2)    //
  // while READ_DESCRIPTOR keyed off the directory, so the 8x8 entity     //
  // served STREAM_OUTPUT.0-8 and STREAM_INPUT.0-8 byte-exact and then    //
  // answered NO_SUCH_DESCRIPTOR to GET_STREAM_INFO on 1-8 — the device   //
  // contradicting itself between two commands about the same descriptor  //
  // (Hive: 8x STREAM_OUTPUT + 7x STREAM_INPUT). Both commands now ask    //
  // the SAME oracle: KL_aecp_accessor's acc_found/acc_base.              //
  // ------------------------------------------------------------------ //
  wire w_si_is_stream = (w_gs_type == DESC_STREAM_INPUT) ||
                        (w_gs_type == DESC_STREAM_OUTPUT);
  //! current_format sits at descriptor offset 74 in BOTH STREAM_INPUT and
  //! STREAM_OUTPUT (1722.1-2021 §7.2.6: descriptor_type 2 + descriptor_index
  //! 2 + object_name 64 + localized_description 2 + clock_domain_index 2 +
  //! stream_flags 2 = 74). acc_base + this offset is byte-identical to the
  //! generated WB_STREAM_*_FMT_C / WB_ST*_FMT_ADDR_C addresses for every
  //! index of every shipped shape, and needs no per-config table — the TB
  //! asserts GET_STREAM_INFO.current_format == the READ_DESCRIPTOR bytes.
  localparam [15:0] STREAM_CUR_FMT_OFF_C = 16'd74;
  //! stream_dest_mac per talker source: MAAP claims ONE contiguous block and
  //! milan_datapath hands ACMP source uid k the address base+k
  //! (acmp_src_dmac_w[k] = eff_aaf_dmac + k; the CRF output takes uid
  //! N_STREAMS, same rule). GET_STREAM_INFO must report the address ACMP
  //! hands out or the two commands disagree about the same stream.
  wire [47:0] w_out_dmac = aaf_dmac_i + 48'(w_gs_index);

  // ------------------------------------------------------------------ //
  // Per-STREAM_OUTPUT presentation-offset file (IEEE 1722.1-2021 §7.4.39 //
  // SET/GET_MAX_TRANSIT_TIME + Milan SET_STREAM_INFO MSRP_ACC_LAT +      //
  // GET_STREAM_INFO's msrp_accumulated_latency field).                   //
  //                                                                      //
  // One 32-bit ns entry per directory-served STREAM_OUTPUT (the CRF      //
  // Media Clock Output included), each reset to the 2 ms class-A default //
  // the single global register always held. Entry k is talker k's        //
  // avtp_timestamp offset (KL_aaf_packetizer transit_ns_i entry k /      //
  // KL_crf_tx for the CRF uid). All three commands read/write the SAME   //
  // entry for a given descriptor_index — the one-source-of-truth         //
  // property of the old register, now per index. Until 2026-07-29 ONE    //
  // global register backed every talker and MAX_TRANSIT_TIME             //
  // hard-rejected any index != 0 that the directory served (the D1       //
  // defect class). Reads are combinational (the const-load cycle needs   //
  // zero latency — same contract as the gs_diag_idx_o pre-mux); the      //
  // directory oracle (acc_found) bounds every served index to the file.  //
  // ------------------------------------------------------------------ //
`ifdef AEM_PER_STREAM_FMT
  localparam int unsigned PRES_N_C = AEM_N_STROUT_C;
`else
  //! legacy svh layout = the deployed 1-STREAM_OUTPUT shape (see the
  //! AAF_OUT_FMT_C branch above: this arm already hardcodes that shape)
  localparam int unsigned PRES_N_C = 1;
`endif
  localparam logic [31:0] PRES_DFLT_C = 32'd2_000_000;
  logic [31:0] pres_file_r [0:PRES_N_C-1];
  //! the addressed index's entry (valid whenever w_gs_index is, i.e.
  //! through the whole const-load cycle of a dispatch)
  logic [31:0] w_gs_pres;
  always_comb begin : pres_pick
    w_gs_pres = PRES_DFLT_C;
    for (int k = 0; k < int'(PRES_N_C); k++)
      if (w_gs_index == 16'(k)) w_gs_pres = pres_file_r[k];
  end : pres_pick
  //! flat export: entry k feeds talker k's framer; unbacked slots tie to
  //! the default so the port shape never depends on the entity shape
  generate
    for (genvar gp = 0; gp < 16; gp++) begin : g_pres_all
      if (gp < int'(PRES_N_C)) begin : g_live
        assign pres_offset_all_o[32*gp +: 32] = pres_file_r[gp];
      end else begin : g_dflt
        assign pres_offset_all_o[32*gp +: 32] = PRES_DFLT_C;
      end
    end
  endgenerate

  // ------------------------------------------------------------------ //
  // GET_AUDIO_MAP addressing (defect A, silicon 2026-07-28)              //
  //                                                                      //
  // The clauses, QUOTED from the standards on this machine (the earlier  //
  // rounds paraphrased them because $STANDARDS_DIR was unset and the      //
  // text was believed unavailable - it is /home/alex/standards).          //
  //                                                                      //
  // IEEE Std 1722.1-2021 Table 7-162 (and Table 7-33), field             //
  // mapping_cluster_offset:                                               //
  //   "The offset from the base_cluster of the STREAM_PORT_INPUT or       //
  //    STREAM_PORT_OUTPUT for mapping[0]."                                //
  // The offsets are therefore PORT-RELATIVE: two ports legitimately       //
  // publish the SAME offsets onto DIFFERENT global AUDIO_CLUSTERs, which  //
  // is exactly why serving one port's map from another port's descriptor  //
  // cannot be seen by comparing any two declarations - only against THE   //
  // ANSWERING PORT'S OWN bounds.                                          //
  //                                                                      //
  // Milan Specification v1.2, 5.4.2.26 GET_AUDIO_MAP:                     //
  //   "For each Stream Port Input and for each Stream Port Output that    //
  //    has no Audio Map, the PAAD-AE shall implement the GET_AUDIO_MAP    //
  //    command as specified in [ATDECC, Clause 7.4.44]. If a PAAD-AE      //
  //    receives a GET_AUDIO_MAP command for a Stream Port Output that     //
  //    has Audio Map(s), the PAAD-AE shall reply with the NOT_SUPPORTED   //
  //    error code."                                                       //
  // Our STREAM_PORT_OUTPUTs DO carry Audio Map descriptors, so the        //
  // Milan-conformant answer on them is NOT_SUPPORTED - and that is also   //
  // the port the over-read was measured on.                               //
  //                                                                      //
  // IEEE Std 1722.1-2021 7.4.44.1:                                        //
  //   "If the map_index is beyond the range of available maps then it     //
  //    returns a BAD_ARGUMENT status in the response."                    //
  // (This arm used to answer NO_SUCH_DESCRIPTOR there.)                   //
  //                                                                      //
  // IEEE Std 1722.1-2021 7.2.13:                                          //
  //   "These Entities set the number_of_maps field to zero (0) and the    //
  //    base_map field is ignored when read."                              //
  // ROWS = 0 in the generated table IS that condition: no static Audio    //
  // Map on this port.                                                     //
  //                                                                      //
  // IEEE Std 1722.1-2021 7.2.19:                                          //
  //   "The mappings field is variable length data and shall be accessed   //
  //    by using the mappings_offset field as any fields added in the      //
  //    future will be added before the mappings field."                   //
  // So the mapping region start is the descriptor's OWN mappings_offset   //
  // (AEM_SMAP_*_MOFF_C), not a hardcoded 8, even though Table 7-32 fixes  //
  // it at 8 "for this version of AEM".                                    //
  //                                                                      //
  // WHAT WAS WRONG. This arm hardcoded BOTH ends: descriptor index 1      //
  // (WB_AUDIO_MAP_1_C), 8 mappings, 64 bytes. At the deployed 1x1 shape   //
  // AUDIO_MAP[1] IS the output port's map and holds 8 rows, so the        //
  // constants were accidentally right and every harness passed. At the    //
  // 8x8 ship shape AUDIO_MAP[1] belongs to STREAM_PORT_INPUT[1] and the   //
  // output port's map is AUDIO_MAP[8] - 24 bytes, 2 rows - so a           //
  // controller asking STREAM_PORT_OUTPUT[0] for its map got 8 mappings    //
  // with cluster_offset 0..7 out of a port declaring number_of_clusters   //
  // = 2, read 48 bytes past the end of a 24-byte descriptor, and put      //
  // whatever followed in the ROM on the wire. It also answered port       //
  // index 0 only, so 14 of the 16 ports READ_DESCRIPTOR serves refused    //
  // their own dynamic-info command.                                       //
  //                                                                      //
  // Both ends now come from the addressed port's OWN generated row:       //
  // AEM_SMAP_*_ADDR_C[port] is the ROM address its base_map names,        //
  // AEM_SMAP_*_ROWS_C[port] is THAT descriptor's own number_of_mappings   //
  // and AEM_SMAP_*_MOFF_C[port] its own mappings_offset - all emitted by  //
  // avdecc/gen_aem_store.py, which additionally refuses a model whose     //
  // mappings fall outside their port's bounds.                            //
  // ------------------------------------------------------------------ //
  wire w_smap_is_in  = (w_gs_type == DESC_STREAM_PORT_INPUT);
  wire w_smap_is_out = (w_gs_type == DESC_STREAM_PORT_OUTPUT);
  //! Index width per DIRECTION, from that direction's own table size. One
  //! shared 5-bit index would be a wider select than either array can be
  //! addressed with, which Verilator flags and which is the shape of a
  //! genuine out-of-range read on any table whose size is not a power of 2.
  localparam int unsigned SMAP_IW_C =
      (AEM_SMAP_IN_N_C  <= 1) ? 1 : $clog2(AEM_SMAP_IN_N_C);
  localparam int unsigned SMAP_OW_C =
      (AEM_SMAP_OUT_N_C <= 1) ? 1 : $clog2(AEM_SMAP_OUT_N_C);
  //! port index in range for ITS OWN direction; the truncation below is
  //! lossless exactly because it is guarded by this compare
  wire w_smap_in_ok  = w_smap_is_in  && (w_gs_index < 16'(AEM_SMAP_IN_N_C));
  wire w_smap_out_ok = w_smap_is_out && (w_gs_index < 16'(AEM_SMAP_OUT_N_C));
  wire w_smap_ir     = w_smap_in_ok || w_smap_out_ok;
  wire [SMAP_IW_C-1:0] w_smap_pi_in  =
      w_smap_in_ok  ? w_gs_index[SMAP_IW_C-1:0] : '0;
  wire [SMAP_OW_C-1:0] w_smap_pi_out =
      w_smap_out_ok ? w_gs_index[SMAP_OW_C-1:0] : '0;
  wire [15:0] w_smap_addr = w_smap_is_out ? AEM_SMAP_OUT_ADDR_C[w_smap_pi_out]
                                          : AEM_SMAP_IN_ADDR_C[w_smap_pi_in];
  wire [15:0] w_smap_rows = w_smap_is_out ? AEM_SMAP_OUT_ROWS_C[w_smap_pi_out]
                                          : AEM_SMAP_IN_ROWS_C[w_smap_pi_in];
  //! the descriptor's OWN mappings_offset (7.2.19 "shall be accessed by
  //! using the mappings_offset field"), not a hardcoded 8
  wire [15:0] w_smap_moff = w_smap_is_out ? AEM_SMAP_OUT_MOFF_C[w_smap_pi_out]
                                          : AEM_SMAP_IN_MOFF_C[w_smap_pi_in];
  //! mapping region length: 8 octets per mapping (7.2.19 Table 7-162 /
  //! 7.4.44.2.1 Table 7-162, four 2-octet fields per mapping)
  wire [15:0] w_smap_blen = {w_smap_rows[12:0], 3'd0};
  //! Milan v1.2 5.4.2.26: a Stream Port OUTPUT that HAS Audio Map(s) must
  //! answer NOT_SUPPORTED - the command is not implemented on that port.
  wire w_smap_milan_ns = w_smap_out_ok && (w_smap_rows != 16'd0);
  //! this port has a static Audio Map to serve at all (7.2.13: ROWS = 0 is
  //! "number_of_maps ... zero (0)", the dynamic-mapping signal)
  wire w_smap_has     = w_smap_ir && (w_smap_rows != 16'd0);
  //! 7.4.44.1: map_index beyond the range of available maps -> BAD_ARGUMENT.
  //! A statically-mapped port publishes number_of_maps = 1, so 0 is the only
  //! index in range (gen_aem_store refuses any other count).
  wire w_smap_badidx  = w_smap_has && ({w_b6, w_b7} != 16'd0);
  //! serveable: an input port of this shape carrying a static map, page 0
  wire w_smap_ok = w_smap_has && !w_smap_milan_ns && !w_smap_badidx;

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
  logic        wbp_r;       //! WRITE_S phase (0 = read old byte, 1 = write+cmp)
  logic        wb_used_q;   //! a store writeback ran for this command
  logic        wb_diff_q;   //! ...and at least one byte actually changed

  // ---- GET_DYNAMIC_INFO batch engine (1722.1-2021 7.4.76) ------------
  //! the command payload is an array of records {len u16, rsvd u16,
  //! status u8, rsvd u8, command_type u16, data[len]}; each is processed
  //! as an independent fixed-size GET and answered in the same shape.
  logic         batch_q;      //! response under construction is a batch
  logic         bsub_q;       //! DECIDE_S is running a batch sub-command
  logic [8:0]   bscan_ptr_q;  //! pass-1 scan pointer (cbuf offset)
  logic [2:0]   bscan_ph_r;   //! pass-1 phase (len hi/lo, cmd hi/lo, verdict)
  logic [7:0]   bsc_lo_q;     //! phase-3-captured cmd low byte (verdict input)
  logic [7:0]   bslh_r;       //! latched len hi byte
  logic [6:0]   bsch_r;       //! latched cmd hi byte (7 bits, r-bit dropped)
  logic [15:0]  bcdl_acc_q;   //! accumulated response payload bytes
  logic [63:0]  bfit_map_q;   //! record k fits the response cap
  logic [5:0]   bidx_q;       //! record index (scan + emit passes)
  logic [8:0]   bpay_end_q;   //! cbuf offset one past the record array
  logic [8:0]   brec_ptr_q;   //! pass-2: current record header cbuf offset
  logic [2:0]   brec_ph_r;    //! pass-2 parse phase
  logic [14:0]  brec_cmd_q;   //! current record command_type
  logic [15:0]  brec_dlen_q;  //! current record command data length
  logic [15:0]  brec_rlen_q;  //! current record RESPONSE data length
  logic [15:0]  brec_base_q;  //! frame-payload offset of the record DATA
  logic [15:0]  brec_abase_q; //! echo virtual base = brec_ptr + 6
  logic [7:0]   rec_hdr_q [0:7]; //! record header image
  logic [2:0]   bh_i_r;       //! RECHDR_EMIT byte index
  logic [10:0]  bcdl_q;       //! batch frame cdl (sub-arm cdl_q writes are
                              //! record-scoped noise once the header is out)
  logic         cap_done_q;   //! the command frame's tlast has been captured
                              //! (hdr_valid fires at beat 3 MID-FRAME - the
                              //! batch scan must not outrun the capture;
                              //! silicon-caught: paced ingress drain made
                              //! BSCAN read unwritten cbuf words = every
                              //! record parsed as garbage -> BAD_ARGUMENTS)
  logic [31:0]  bdbg0_q;      //! BSCAN forensics: header bytes as scanned
  logic [31:0]  bdbg1_q;      //! {1'b0, cmd15, dlen16} at the verdict
  logic [31:0]  bdbg2_q;      //! {ptr9, end9} at the verdict

  //! response data length of an implemented fixed-size GET (0 = the
  //! command is answered by echoing its data with NOT_SUPPORTED status;
  //! the spec's fixed-size set membership is checked separately)
  function automatic logic [15:0] batch_rlen(input [14:0] c);
    unique case (c)
      CMD_GET_CONFIGURATION:  batch_rlen = 16'd4;
      CMD_GET_STREAM_FORMAT:  batch_rlen = 16'd12;
      CMD_GET_STREAM_INFO:    batch_rlen = 16'd56;
      CMD_GET_NAME:           batch_rlen = 16'd72;
      CMD_GET_SAMPLING_RATE:  batch_rlen = 16'd8;
      CMD_GET_CLOCK_SOURCE:   batch_rlen = 16'd8;
      CMD_GET_COUNTERS:       batch_rlen = 16'd136;
      default:                batch_rlen = 16'd0;
    endcase
  endfunction

  //! 1722.1-2021 7.4.76.2 fixed-size GET set (batch-legal command types)
  function automatic logic batch_legal(input [14:0] c);
    batch_legal = (c == CMD_GET_CONFIGURATION) || (c == CMD_GET_STREAM_FORMAT)
               || (c == 15'd11) || (c == 15'd13)                // VIDEO/SENSOR_FORMAT
               || (c == CMD_GET_STREAM_INFO) || (c == CMD_GET_NAME)
               || (c == 15'd19)                                 // GET_ASSOCIATION_ID
               || (c == CMD_GET_SAMPLING_RATE) || (c == CMD_GET_CLOCK_SOURCE)
               || (c == 15'd29)                                 // GET_SIGNAL_SELECTOR
               || (c == CMD_GET_COUNTERS)
               || (c == 15'd71) || (c == 15'd74);   // MEM_OBJ_LEN / STREAM_BACKUP
  endfunction

`ifdef AEM_DYNMAP
  // ---- dynamic audio-map engine (gaps item 8 + roadmap 23) ------------
  //! Mappings store for EVERY map_mode-dynamic STREAM_PORT_INPUT, so the
  //! entity satisfies Milan v1.2 5.3.3.9 ("The Stream Port Input of a
  //! Configuration shall not contain any AUDIO_MAP descriptor. Note: this
  //! means that a PAAD-AE implements dynamic mappings on all of its Stream
  //! Port Inputs"). DIRECT-MAPPED by GLOBAL cluster key = the addressed
  //! port's base_cluster + mapping_cluster_offset; clusters are mono
  //! (channel_count 1, Milan 5.3.3.8) so one key IS one Audio-Cluster
  //! channel and 5.4.2.26's "at most one dynamic mapping per Audio
  //! Cluster's channel" holds by construction. That key is ALSO the render
  //! crossbar's map-RAM address - model and fabric share one index space.
  //! An entry keeps {valid, stream_index, stream_channel}: 1722.1-2021
  //! Table 7-33 defines mapping_stream_index as "the STREAM_INPUT or
  //! STREAM_OUTPUT descriptor index for the stream carrying this channel",
  //! so a port may be fed from ANY Stream Input and the channel bound is
  //! taken from THAT stream's current format (5.4.2.27 / 5.3.10.1).
  //! Small FLOP array (<= 64 x 8 b), not a RAM: reset-initialized, written
  //! by the commit walk, read by the GET page scan and the render taps
  //! (no inference hazard class).
  localparam int unsigned DMAP_KW_C =
      (AEM_DMAP_KEYS_C <= 1) ? 1 : $clog2(AEM_DMAP_KEYS_C);
  localparam int unsigned DMAP_PW_C =
      (AEM_DMAP_NPORTS_C <= 1) ? 1 : $clog2(AEM_DMAP_NPORTS_C);
  localparam int unsigned DMAP_SW_C =
      (AEM_DMAP_NSTRIN_C <= 1) ? 1 : $clog2(AEM_DMAP_NSTRIN_C);
  //! fabric projection bound: the render map word carries ch[2:0], so a
  //! mapping past stream channel 7 has nowhere to land (documented; every
  //! Milan 6.4 base format this entity declares is <= 8 channels)
  localparam int unsigned DMAP_CHMAX_C = 8;
  logic                       dmap_v_r  [0:AEM_DMAP_KEYS_C-1];
  logic [3:0]                 dmap_ch_r [0:AEM_DMAP_KEYS_C-1];
  logic [2:0]                 dmap_si_r [0:AEM_DMAP_KEYS_C-1];
  logic [AEM_DMAP_KEYS_C-1:0] dmap_claim_r; //! intra-command same-key guard

  //! Power-on IDENTITY default (USER directive 08-01): STREAM_PORT_INPUT p
  //! wakes mapping ITS OWN stream's (Stream Input p's) channels 0..C-1
  //! onto its own clusters 0..C-1, so a bare bind carries audio with no
  //! mapping surgery. C is DERIVED, never restated: min(port clusters,
  //! that stream's reset-format channel count, the ch[2:0] fabric bound),
  //! and the key must clear the SAME physical-reachability bound
  //! ADD_AUDIO_MAPPINGS enforces - the default is exactly a map a
  //! controller could have ADDed, so store and render crossbar stay
  //! wire-true. Clause basis: Milan 5.3.3.9 forbids static AUDIO_MAPs on
  //! inputs (the default must live in the DYNAMIC store's reset image) and
  //! 5.3.10.1 mandates restore-after-power-cycle while leaving the factory
  //! contents open. A controller's ADD/REMOVE overrides; reset restores.
  //! returns {v, ch[3:0], si[2:0]} for key k; the loops unroll at
  //! elaboration so the reset image is constant in synthesis
  function automatic logic [7:0] dmap_init_key(input int unsigned k);
    logic [7:0]  r;
    int unsigned c;
    r = 8'd0;
    for (int p = 0; p < AEM_DMAP_NPORTS_C; p++) begin
      if (AEM_DMAP_PDYN_C[p] &&
          k >= AEM_DMAP_PBASE_C[p] &&
          k <  AEM_DMAP_PBASE_C[p] + AEM_DMAP_PCLS_C[p]) begin
        c = k - AEM_DMAP_PBASE_C[p];
        if (p < AEM_DMAP_NSTRIN_C && AEM_DMAP_SAAF_C[p] &&
            c < AEM_DMAP_SCH_C[p] && c < DMAP_CHMAX_C &&
            k < AEM_DMAP_PHYS_C)
          r = {1'b1, 4'(c), 3'(p)};
      end
    end
    return r;
  endfunction
  //! post-reset fabric seed cursor: replays the identity image into the
  //! render crossbar (which resets EMPTY on its own side), one key per
  //! IDLE_S cycle; == KEYS when done
  logic [6:0] dmseed_r;

`ifdef AEM_ODYNMAP
  // ------------------------------------------------------------------ //
  // Talker-side dynamic maps (USER 08-01: "enable dynamic mapping on    //
  // stream_output as well"). Key = port*8 + STREAM channel: Milan       //
  // 5.4.2.26's "at most one dynamic mapping per Stream Output's         //
  // channel" makes the stream channel the unique key; the value is the  //
  // cluster_offset feeding it. AEM_ODMAP_CSRC_C resolves a cluster to   //
  // its capture-crossbar source pair {valid, half, src, idxh, idx}.     //
  //                                                                     //
  // ONE RECORD IS ONE CHANNEL. 1722.1-2021 7.4.45 bounds a command only //
  // by "the number of mappings which are contained in the mappings      //
  // field"; Milan 5.4.2.27/28 enumerate every BAD_ARGUMENTS condition   //
  // and none of them is a record COUNT. This engine used to refuse an   //
  // odd number_of_mappings ("half a pair"), which is our capture        //
  // crossbar's pair-slot geometry leaking into protocol acceptance: a   //
  // controller that maps one channel at a time - the normal case - had  //
  // every command rejected. The count rule is gone; what remains are    //
  // PER-MAPPING rules, which is the only thing 7.4.45.1 delegates       //
  // ("what constitutes a valid mapping AT A PARTICULAR POINT IN TIME    //
  // is governed by a set of vendor defined rules"):                     //
  //   1. mapping_stream_index must be the port's OWN stream (the        //
  //      capture fabric routes port j's clusters into stream j);        //
  //   2. the cluster's source HALF must match the stream channel's      //
  //      parity - slot p emits its source pair's L into channel 2p and  //
  //      its R into 2p+1, so "cluster 4 onto channel 5" is a route this //
  //      crossbar physically cannot make (the mono TONE bucket is       //
  //      exempt: it carries the same value on both halves);             //
  //   3. the sibling channel of the same pair slot, AS THIS COMMAND     //
  //      WILL LEAVE IT, must be unmapped or fed by the SAME source      //
  //      pair - one slot holds one {src, idxh, idx}. Accepting          //
  //      otherwise would silently re-point a channel whose mapping      //
  //      GET_AUDIO_MAP still reports.                                   //
  // Rule 3 is why the walk validates in TWO passes before committing:   //
  // pass A judges each record alone and records its intent, pass B      //
  // judges each record against the command's POST state, pass C         //
  // commits. All three run to completion, so 7.4.45.1's "none of the    //
  // mappings are added" still holds.                                    //
  //                                                                     //
  // COMMIT is a READ-MODIFY-WRITE of the pair slot: the record owns ONE //
  // half of it and the sibling's half-enable is rebuilt from the live   //
  // store, so mapping channel 5 alone leaves channel 4 exactly as it    //
  // was and removing channel 5 alone silences only channel 5. That is   //
  // what KL_chan_map_capture's map_wr_half_i pin exists for.            //
  // ------------------------------------------------------------------ //
  localparam int unsigned ODMAP_KW_C =
      (AEM_ODMAP_KEYS_C <= 1) ? 1 : $clog2(AEM_ODMAP_KEYS_C);
  logic                  ov_r  [0:AEM_ODMAP_KEYS_C-1];
  logic [4:0]            oco_r [0:AEM_ODMAP_KEYS_C-1];
  //! NOTE no live channel-count follower here: w_out_fmt_ok accepts ONLY
  //! the declared output format (FR-STR-03 wire truth), so the Milan
  //! 5.4.2.27 current-format bound IS the elaboration constant
  //! AEM_ODMAP_SCH_C - derived once, never shadowed.
  //! this command's intent, per stream channel of the addressed port:
  //! oclaim_r = "a record of this command writes this channel" (ADD also
  //! REJECTS a second record on a claimed channel - Milan 5.4.2.27's
  //! same-stream-channel conflict), opend_co_r = the cluster it will leave
  //! there. Together they are the POST-COMMAND view rule 3 must judge
  //! against, and they are what lets the RMW compose WITHIN one command
  //! whatever order the records arrive in.
  logic [7:0]            oclaim_r;
  logic [4:0]            opend_co_r [0:7];
  logic [1:0]            od_pass_q;  //! 0 = judge alone, 1 = judge pair, 2 = commit
  logic                  dm_out_q;   //! walk direction: 1 = output port
  //! dispatch-latched addressed-port facts (the walk reads no descriptor)
  logic [3:0]            od_pidx_q;
  logic [ODMAP_KW_C-1:0] od_kb_q;    //! key base = pidx * 8
  logic [6:0]            od_cb_q;    //! CSRC base (AEM_ODMAP_PCBASE_C)
  logic [4:0]            od_pcls_q;
  logic [3:0]            od_pstr_q;
  logic [4:0]            od_slotb_q;
  logic [9:0]            od_schx_q;
  logic [7:0]            odseed_r;   //! post-reset capture-fabric seed

  //! addressed-port decode (DISPATCH cone)
  wire [3:0] w_od_pidx = (w_gs_index < 16'(AEM_ODMAP_NPORTS_C))
                         ? 4'(w_gs_index) : '0;
  wire w_od_ok  = (w_gs_type == DESC_STREAM_PORT_OUTPUT) &&
                  (w_gs_index < 16'(AEM_ODMAP_NPORTS_C));
  wire w_od_dyn = w_od_ok && AEM_ODMAP_PDYN_C[w_od_pidx];

  // ---- KEY-RESOLVE terms: read in DMAP_SCAN_S phases 8-9, consumed ONLY -
  // ---- by the odk_* registers below (never by the phase-10 verdict) -----
  wire w_od_co_ok = (dm_co_q < {11'd0, od_pcls_q});
  //! the SIBLING channel: the other half of this record's pair slot
  wire [2:0] w_od_sib  = dm_sc_q[2:0] ^ 3'd1;
  wire [ODMAP_KW_C-1:0] w_od_key  =
      od_kb_q | ODMAP_KW_C'(dm_sc_q[2:0]);
  wire [ODMAP_KW_C-1:0] w_od_keyp =
      od_kb_q | ODMAP_KW_C'(w_od_sib);
  //! the sibling AS THIS COMMAND WILL LEAVE IT (rule 3, and the half-enable
  //! the RMW writes): a channel this command touches ends up mapped exactly
  //! when the command is an ADD, whatever order the records arrived in.
  wire w_od_sv  = oclaim_r[w_od_sib] ? !dm_remove_q : ov_r[w_od_keyp];
  wire [4:0] w_od_sco = oclaim_r[w_od_sib] ? opend_co_r[w_od_sib]
                                           : oco_r[w_od_keyp];
  //! ONE source-table mux, addressed by the phase: 8 resolves the RECORD's
  //! own cluster, 9 the SIBLING's. Time-multiplexing the address costs a
  //! 7-bit mux; a second AEM_ODMAP_CSRC_C read would cost a second 13-bit
  //! one, in the module that already owns the critical path.
  wire [4:0] w_od_ca   = (dmph_r == 4'd8) ? dm_co_q[4:0] : odk_sco_q;
  wire       w_od_ca_ok = (dmph_r == 4'd8) ? w_od_co_ok
                                           : (odk_sco_q < od_pcls_q);
  wire [12:0] w_od_t =
      AEM_ODMAP_CSRC_C[w_od_ca_ok ? 32'(od_cb_q) + 32'(w_od_ca) : 0];

  //! phase-8 resolution of everything the verdict reaches through a KEY:
  //! the CSRC source table (an adder off dm_co_q into a per-cluster table)
  //! and the two pair-key reads of the output store. The odmap twin of the
  //! w_dm_* split below - same reason, same phase, so neither branch can
  //! become the other's critical path.
  logic [12:0]           odk_t_q;      //! AEM_ODMAP_CSRC_C[..] for this record
  logic [12:0]           odk_ts_q;     //! ...and for its SIBLING channel
  logic                  odk_coq_ok_q; //! cluster_offset inside the port
  logic [ODMAP_KW_C-1:0] odk_key_q;    //! this record's store key
  logic                  odk_v_q;      //! ov_r at this record's key
  logic [4:0]            odk_co_q;     //! oco_r at this record's key
  logic                  odk_sv_q;     //! sibling mapped AFTER this command
  logic [4:0]            odk_sco_q;    //! ...and the cluster it will carry

  //! the mono pilot bucket (KL_chan_map_capture SRC_TONE_C) puts the same
  //! value on BOTH halves of a slot, so it is the one source a cluster can
  //! feed from either channel parity
  wire w_od_mono = (odk_t_q[10:8] == 3'd4);
  //! PER-RECORD validity (rules 1 and 2 at the block comment above). Every
  //! term is a property of THIS mapping - none of them counts records.
  wire w_od_rec_ok =
      (dm_si_q == {12'd0, od_pstr_q}) &&
      (dm_sc_q < od_schx_q) && (dm_sc_q < 16'd8) &&
      odk_coq_ok_q && (dm_cc_q == 16'd0) && odk_t_q[12] &&
      (w_od_mono || (odk_t_q[11] == dm_sc_q[0]));
  //! rule 3: one pair slot holds ONE {src, idxh, idx}. Judged against the
  //! sibling as the command LEAVES it, so a command that re-points both
  //! channels of a slot together is accepted whatever order it lists them.
  wire w_od_sib_ok =
      !odk_sv_q || (odk_ts_q[12] &&
                    (odk_ts_q[10:8] == odk_t_q[10:8]) &&
                    (odk_ts_q[7:0]  == odk_t_q[7:0]));
  //! REMOVE present-check (7.4.46.1: "invalid or not present" refuses).
  //! Exact on all four record fields: stream_index, stream_channel,
  //! cluster_offset (the stored value) and cluster_channel.
  wire w_od_rm_hit =
      (dm_si_q == {12'd0, od_pstr_q}) && (dm_sc_q < 16'd8) &&
      (dm_cc_q == 16'd0) && odk_v_q &&
      (odk_co_q == dm_co_q[4:0]);
  //! did this record change the store (nochg replay suppressor)
  wire w_od_chg = !odk_v_q || (odk_co_q != dm_co_q[4:0]);
  //! the RMW's half-enable {L, R}: this record's own channel armed, the
  //! sibling's exactly as the command leaves it
  wire [1:0] w_od_half_add = dm_sc_q[0] ? {odk_sv_q, 1'b1}
                                        : {1'b1, odk_sv_q};
  wire [1:0] w_od_half_rm  = dm_sc_q[0] ? {odk_sv_q, 1'b0}
                                        : {1'b0, odk_sv_q};
`endif
  //! live per-STREAM_INPUT channel count: resets to the ROM current_format
  //! and follows SET_STREAM_FORMAT, because 5.3.10.1 bounds a mapping by
  //! "the number of channels in the current format of the Stream Input"
  logic [9:0]  dm_sch_r [0:AEM_DMAP_NSTRIN_C-1];
  logic [5:0]  dmi_r;          //! mapping index in the ADD/REMOVE walk
  logic [5:0]  dmn_q;          //! number_of_mappings of the command
  logic [3:0]  dmph_r;         //! walk phase: 0..7 field bytes, 8 verdict
  logic [7:0]  dm_hi_r;        //! captured hi byte of the current field
  logic [15:0] dm_si_q;        //! mapping_stream_index
  logic [15:0] dm_sc_q;        //! mapping_stream_channel
  logic [15:0] dm_co_q;        //! mapping_cluster_offset (port-relative)
  logic [15:0] dm_cc_q;        //! mapping_cluster_channel
  logic        dm_commit_q;    //! 0 = validate pass, 1 = commit pass
  logic        dm_remove_q;    //! REMOVE (single lenient commit pass)
  logic        dmap_diff_q;    //! a commit changed the store (nochg gate)
  //! addressed port, latched at dispatch: the walk reads no descriptor
  logic [6:0]  dm_pbase_q;     //! base_cluster of the addressed port
  logic [6:0]  dm_pcls_q;      //! clusters of the addressed port
  //! Format-shrink prune (Milan 5.3.10.1). The clause is a STANDING
  //! invariant on device state, not just an ADD-time test: "At a given
  //! time, each channel of each Audio Cluster of each Stream Port Input is
  //! either not mapped, or mapped to a channel of a Stream Input (in this
  //! case, the index of the mapped Stream Input's channel shall be lower
  //! than the number of channels in the current format of the Stream
  //! Input)." A SET_STREAM_FORMAT that SHRINKS a stream (8ch -> 2ch) would
  //! otherwise leave a live mapping on channel 5 of a 2-channel stream,
  //! violating it for as long as the format holds - and in the fabric the
  //! render word carries ch[2:0], so the crossbar would keep de-interleaving
  //! a channel the wire no longer has.
  //!
  //! JUDGMENT CALL, conservative reading: PRUNE rather than REFUSE. Nothing
  //! in 1722.1-2021 7.4.9 or Milan 5.4.2.6 lets an entity fail an otherwise
  //! valid SET_STREAM_FORMAT because of mapping state, and the ATDECC order
  //! of operations is set-format-then-map, so refusing would break a legal
  //! sequence for a reason the standard never lists. The withdrawal is
  //! observable: GET_AUDIO_MAP stops reporting the pruned rows. No
  //! REMOVE_AUDIO_MAPPING unsolicited notification is fabricated - 5.4.2.27
  //! offers that only for the ADD accept-and-replace case.
  logic [6:0]  dmp_key_r;      //! prune sweep cursor (GLOBAL key)
  logic [DMAP_SW_C-1:0] dmp_sidx_q;  //! the reformatted Stream Input
  logic [9:0]  dmp_ch_q;       //! its NEW channel count (the new bound)
  logic [6:0]  dmg_key_r;      //! GET page-scan key (GLOBAL)
  logic [6:0]  dmg_end_r;      //! GET page-scan end key (exclusive, global)
  logic [6:0]  dmg_base_r;     //! addressed port's base (offset subtrahend)
  logic [7:0]  dmg_nmaps_q;    //! addressed port's number_of_maps (echoed)
  logic [3:0]  dmg_n_r;        //! mappings emitted into the scratch
`endif

  //! ---- SINGLE async cbuf read port (2026-07-21 silicon forensics) ----
  //! Implicit multi-port LUTRAM inference replicated cbuf into RAM64M x66
  //! and the SCAN's replica read stale zeros while the ECHO's replica was
  //! byte-perfect (BDBG 0x768 caught it: header {00 00 / 00 00} scanned
  //! at the correct {ptr 2, end 10} while the wire carried cmd 0x0007 and
  //! the later echo agreed - the mf37..mf40 0x4B BAD_ARGUMENTS story).
  //! Every reader is state-exclusive, so ONE port behind an explicit
  //! state mux is semantics-identical - and one RAM copy instead of six.
  logic [3:0] cwld_r;          //! BREC arg-window byte loader (16 cycles)
  logic [8:0] cbuf_raddr;
  always_comb begin : cbuf_amux
    unique case (state_r)
      BSCAN_S:      cbuf_raddr = (bscan_ph_r == 3'd0) ? bscan_ptr_q
                               : (bscan_ph_r == 3'd1) ? bscan_ptr_q + 9'd1
                               : (bscan_ph_r == 3'd2) ? bscan_ptr_q + 9'd6
                                                      : bscan_ptr_q + 9'd7;
      BREC_SETUP_S: cbuf_raddr = (brec_ph_r == 3'd0) ? brec_ptr_q
                               : (brec_ph_r == 3'd1) ? brec_ptr_q + 9'd1
                               : (brec_ph_r == 3'd2) ? brec_ptr_q + 9'd6
                               : (brec_ph_r == 3'd3) ? brec_ptr_q + 9'd7
                               : 9'(brec_abase_q + 16'(cwld_r));
      WRITE_S:      cbuf_raddr = w_wbaddr;
`ifdef AEM_DYNMAP
      //! mapping i field byte j: payload mappings start at cbuf offset 10
      //! (cmd_type 0-1, desc 2-5, number_of_mappings 6-7, reserved 8-9)
      DMAP_SCAN_S:  cbuf_raddr = 9'(16'd10 + {7'd0, dmi_r, 3'd0}
                                   + {13'd0, dmph_r[2:0]});
`endif
      default:      cbuf_raddr = ec_addr_q;  //! EMIT_DATA_S SEG_ECHO
                                             //! (registered w_eaddr, ph1)
    endcase
  end
  wire [63:0] cbuf_rword_w = cbuf_r[cbuf_raddr[8:3]];
  wire [7:0]  cbuf_rbyte_w = bufb(cbuf_rword_w, cbuf_raddr[2:0]);

  //! batch phase-3 record terms as PLAIN COMB WIRES (the earlier
  //! block-local `automatic` temporaries were themselves a synthesis
  //! hazard class - both suspects stay fixed; the wires now read the
  //! single port, valid in phase 3 only where they are consumed)
  //! verdict terms from REGISTERS only (AX27 -1.98: the phase-select ->
  //! addr mux -> RAM -> rlen table -> fit compare cone; phase 3 now only
  //! CAPTURES the byte, the added verdict phase computes from bsc_lo_q)
  wire [14:0] w_bscan_c  = {bsch_r, bsc_lo_q};
  wire [15:0] w_bscan_rl = (batch_rlen(w_bscan_c) != 16'd0)
                         ? batch_rlen(w_bscan_c) : brec_dlen_q;
  wire [14:0] w_brec_c   = {bsch_r, bsc_lo_q};
  wire [15:0] w_brec_rl  = batch_rlen(w_brec_c);

  // ------------------------------------------------------------------ //
  // Emit engine                                                          //
  // ------------------------------------------------------------------ //
  localparam [15:0] HDR_AEM_C = 16'd38;
  localparam [15:0] HDR_VU_C  = 16'd36;
  wire [15:0] w_hdr_len   = vu_q ? HDR_VU_C : HDR_AEM_C;
  wire [15:0] w_frame_len = w_hdr_len + pay_len_q;

  logic [15:0] fi_r;               //! frame byte index
  logic [7:0]  emit_byte_r;        //! byte resolved in EMIT_ADDR/DATA

  //! payload byte index -> (segment, offset within segment); in batch
  //! mode the walk is relative to the current record's data region
  wire [15:0] w_pi = fi_r - w_hdr_len - (batch_q ? brec_base_q : 16'd0);
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

  //! Store READ address is REGISTERED (AX 100 MHz WNS -0.124: batch_q ->
  //! segment walk -> store-address adder reached the BRAM address port in
  //! one combinational cone). EMIT_ADDR_S runs TWO phases: phase 0 resolves
  //! the byte source and registers the store address (st_addr_q, below with
  //! the emit pipeline registers); phase 1 issues the store read from that
  //! register, so the 1-cycle data latency lands exactly on EMIT_DATA_S -
  //! the same landing cycle as the old combinational shape, one address
  //! cycle earlier. Emit costs 3 cycles per byte instead of 2, free at
  //! command pace. The qualifier terms come from the phase-0 registers too
  //! (!is_hdr_r <=> fi_r >= w_hdr_len, emseg_kind_r <=> seg_kind_q[w_seg]),
  //! so the read enable is register-shallow as well.
  wire w_emit_store = (state_r == EMIT_ADDR_S) && ea_ph_r &&
                      !is_hdr_r && (emseg_kind_r == SEG_STORE);
  //! WRITE_S phase-0 read of the OLD byte (nochg detection: a SET whose
  //! writeback changes nothing suppresses the u=1 replay - the 1722.1
  //! unsolicited rule notifies STATE CHANGES; generalizes the es-4.5
  //! SET_STREAM_INFO case to every store-writeback SET). Its address stays
  //! combinational: wb_addr_q + wb_cnt_r is a single register-fed adder.
  wire w_wb_read = (state_r == WRITE_S) && (wb_len_q != 7'd0) && !wbp_r;
  assign st_addr_o = w_wb_read ? (wb_addr_q + 16'(wb_cnt_r))
                               : st_addr_q;
  assign st_rd_o   = w_emit_store || w_wb_read;

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
    else if (fi == 16) b = {status_q, batch_q ? bcdl_q[10:8] : cdl_q[10:8]};
    else if (fi == 17) b = batch_q ? bcdl_q[7:0] : cdl_q[7:0];
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
  //! EMIT_ADDR_S phase bit (0 = resolve+register, 1 = store read issue) and
  //! the registered emit-path store address it decouples from the BRAM.
  //! Invariant: every entry into EMIT_ADDR_S arrives with ea_ph_r == 0 -
  //! it is set only in phase 0 and cleared on phase 1's single exit, and
  //! the EMIT loop has no other way out (the batch record branches leave
  //! from phase 0).
  logic        ea_ph_r;
  logic [15:0] st_addr_q;
  //! ...and the matching ECHO read address. The capture-RAM read was still
  //! combinational off w_eaddr, so a batch response paid
  //! brec_abase_q -> 9-bit adder -> cbuf LUTRAM -> byte mux -> pack_r in
  //! ONE cycle (AX 100 MHz -0.298, the second-worst cone on the board).
  //! Phase 1 registers the sum - by then emseg_addr_r/emsoff_r hold phase
  //! 0's resolution - and EMIT_DATA_S addresses the RAM from the register,
  //! so the echo byte lands on the SAME cycle it always did.
  logic [8:0]  ec_addr_q;

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
  //! STREAM_OUTPUT counters live in KL_talker_diag_ctx since 2026-07-28
  //! (Milan Table 5.4 semantics per index); only the AVB_INTERFACE set
  //! stays local
  logic [31:0] cnt_linkup_r, cnt_linkdn_r, cnt_gmchg_r;
  logic        link_prev_r;
  logic [63:0] gm_prev_r;

  //! live STREAM_INPUT[0] current format: resets to the ROM's current_format
  //! (descriptor 0's own table entry — AEM_STRIN_FMT_C[0] on multi-stream
  //! layouts, AEM_FMTS_C[0] on the deployed one; same bytes) and follows
  //! SET_STREAM_FORMAT — the RX monitor's format-compare reference (the
  //! store scratch keeps the readback copy)
  logic [63:0] fmt_in0_r;
`ifdef AEM_PER_STREAM_FMT
  localparam [63:0] FMT_IN0_RST_C = AEM_STRIN_FMT_C[0];
`else
  localparam [63:0] FMT_IN0_RST_C = AEM_FMTS_C[0];
`endif
  assign in0_fmt_o = fmt_in0_r;
  logic [15:0] clk_src_r;                 //! follows SET_CLOCK_SOURCE (reset 0 = internal)
  assign clk_src_o = clk_src_r;

`ifdef AEM_DYNMAP
  // ---- dynamic-map walk, KEY-RESOLVE terms (DMAP_SCAN_S phase 8) -------
  //                                                                       //
  // AX 100 MHz WNS -0.130, and eight of the ten worst paths on the board: //
  // dm_co_q -> w_dm_gkey adder -> w_dm_key (fanout 94) -> the key-indexed //
  // reads of the mapping store -> w_dm_rm_hit -> status_q/state_r ENABLE, //
  // all inside the single verdict cycle. A key that indexes a 64-entry    //
  // flop array is a mux as deep as the directory scans upstream, so it    //
  // gets the same treatment the BSCAN walk already documents (AX27): the  //
  // walk grows ONE phase - 8 RESOLVES the key and every value read        //
  // THROUGH it, 9 renders the verdict from those registers. Free at       //
  // command pace, and the store still sees pre-record contents because    //
  // the resolve reads before the same record's commit writes.             //
  // ---- these feed the dmk_* registers ONLY, never the verdict ----------
  //! GLOBAL store key = the latched port base + the record's cluster
  //! offset; a record outside the addressed port's own cluster block is
  //! invalid (7.2.19: the offset is "from the base_cluster of the
  //! STREAM_PORT_INPUT", so it can never reach another port's clusters)
  wire [15:0] w_dm_gkey   = dm_co_q + {9'd0, dm_pbase_q};
  wire        w_dm_key_ok = (dm_co_q < {9'd0, dm_pcls_q}) &&
                            (w_dm_gkey < 16'(AEM_DMAP_KEYS_C));
  wire [DMAP_KW_C-1:0] w_dm_key =
      w_dm_key_ok ? DMAP_KW_C'(w_dm_gkey) : '0;
  wire        w_dm_si_in  = (dm_si_q < 16'(AEM_DMAP_NSTRIN_C));
  wire [DMAP_SW_C-1:0] w_dm_sidx = w_dm_si_in ? DMAP_SW_C'(dm_si_q) : '0;
  //! 5.4.2.27 validity: cluster_channel 0 (mono clusters), cluster key
  //! inside the addressed port, a MAPPABLE (AAF, not CRF) Stream Input,
  //! a stream channel present in THAT stream's current format, and a
  //! cluster this gateware can PHYSICALLY render.
  //!
  //! The physical term is a vendor validity rule, which 7.4.45.1 delegates
  //! explicitly: "The ADDING of a mapping is subject to the validity of the
  //! mapping as defined by the vendor of the ATDECC Entity." The AEM model
  //! declares one Audio Cluster per stream channel (up to 64 on the 8x8
  //! shape) while the render crossbar has AEM_DMAP_PHYS_C physical output
  //! channels behind it. Accepting a mapping onto a cluster with no pad
  //! behind it would have the entity report, through GET_AUDIO_MAP, a route
  //! that silently carries no audio - so it is refused at the door instead.
  wire w_dm_phys_ok  = (w_dm_gkey < 16'(AEM_DMAP_PHYS_C));

  //! phase-8 resolution: the key itself, the two stream-indexed table
  //! reads, and the four key-indexed store reads the verdict needs
  logic [DMAP_KW_C-1:0] dmk_key_q;    //! this record's GLOBAL store key
  logic                 dmk_keyok_q;  //! ...and whether it was in range
  logic                 dmk_physok_q; //! cluster is physically renderable
  logic                 dmk_siin_q;   //! stream index inside the model
  logic                 dmk_saaf_q;   //! ...and that Stream Input is AAF
  logic [9:0]           dmk_sch_q;    //! its live channel count
  logic                 dmk_v_q;      //! dmap_v_r  at the key
  logic [3:0]           dmk_ch_q;     //! dmap_ch_r at the key
  logic [2:0]           dmk_si_q;     //! dmap_si_r at the key
  logic                 dmk_claim_q;  //! dmap_claim_r at the key

  // ---- phase-9 verdict: registers only --------------------------------
  wire w_dm_shape_ok = (dm_cc_q == 16'd0) && dmk_keyok_q && dmk_physok_q
                       && dmk_siin_q && dmk_saaf_q;
  wire w_dm_ch_ok    = (dm_sc_q < {6'd0, dmk_sch_q}) &&
                       (dm_sc_q < 16'(DMAP_CHMAX_C));
  wire w_dm_add_bad  = !w_dm_shape_ok || !w_dm_ch_ok || dmk_claim_q;
  //! 7.4.46.1, verbatim: "If any of the mappings in the command are invalid
  //! or not present then the command shall fail with a BAD_ARGUMENTS status
  //! and none of the mappings shall be removed." Only *invalid* is
  //! vendor-delegated; NOT PRESENT is the standard's own word, and Milan
  //! 5.4.2.28 overrides it for DUPLICATES only ("shall ignore duplicate
  //! mappings that may be present in a REMOVE_AUDIO_MAPPINGS command").
  //! Duplicates still pass because validation runs to completion BEFORE any
  //! commit, so every copy sees the entry still present.
  wire w_dm_rm_bad   = !w_dm_rm_hit;
  wire w_dm_add_chg  = !dmk_v_q ||
                       (dmk_ch_q != dm_sc_q[3:0]) ||
                       (dmk_si_q != dm_si_q[2:0]);
  wire w_dm_rm_hit   = w_dm_shape_ok && (dm_sc_q < 16'd16) &&
                       dmk_v_q &&
                       (dmk_ch_q == dm_sc_q[3:0]) &&
                       (dmk_si_q == dm_si_q[2:0]);
  wire [15:0] w_dm_n = {w_b6, w_b7};     //! number_of_mappings field
  wire [6:0]  w_dmg_base = 7'd6 + {dmg_n_r, 3'd0};  //! GET scratch cursor

  // ---- addressed-port lookups (DISPATCH cone only: these read the ------
  // ---- descriptor type/index the command carries, never the walk) ------
  wire [DMAP_PW_C-1:0] w_dm_pidx =
      (w_gs_index < 16'(AEM_DMAP_NPORTS_C)) ? DMAP_PW_C'(w_gs_index) : '0;
  wire w_dm_pin_ok   = (w_gs_type == DESC_STREAM_PORT_INPUT) &&
                       (w_gs_index < 16'(AEM_DMAP_NPORTS_C));
  wire w_dm_pin_dyn  = w_dm_pin_ok && AEM_DMAP_PDYN_C[w_dm_pidx];
  //! GET_AUDIO_MAP page window for the addressed dynamic input port
  //! (Milan 5.4.2.26 fixed partition: page P covers cluster offsets
  //! [P*PAGE, min((P+1)*PAGE, clusters)) of THAT port)
  wire [15:0] w_dmg_p    = {w_b6, w_b7};
  wire [15:0] w_dmg_beg  = w_dmg_p * 16'(AEM_DMAP_PAGE_C);
  wire [15:0] w_dmg_stop = w_dmg_beg + 16'(AEM_DMAP_PAGE_C);
  wire [15:0] w_dmg_cls  = 16'(AEM_DMAP_PCLS_C[w_dm_pidx]);
  wire [15:0] w_dmg_pb   = 16'(AEM_DMAP_PBASE_C[w_dm_pidx]);
  wire [6:0]  w_dmg_kbeg = 7'(w_dmg_pb + w_dmg_beg);
  wire [6:0]  w_dmg_kend = 7'(w_dmg_pb +
                              ((w_dmg_stop < w_dmg_cls) ? w_dmg_stop
                                                        : w_dmg_cls));
  //! SET_STREAM_FORMAT channel-bound follower index
  wire [DMAP_SW_C-1:0] w_dm_fidx =
      (w_gs_index < 16'(AEM_DMAP_NSTRIN_C)) ? DMAP_SW_C'(w_gs_index) : '0;
`endif

`ifndef AEM_ODYNMAP
  //! no dynamic output ports in this shape: the capture-map write port is
  //! quiescent by construction (same tie discipline as -Werror-UNDRIVEN
  //! demands of every conditional engine)
  assign odmap_wr_p_o    = 1'b0;
  assign odmap_wr_slot_o = 5'd0;
  assign odmap_wr_word_o = 14'd0;
`endif

  //! STREAM_INPUT counter push state (Milan §5.4.5: unsolicited GET_COUNTERS
  //! only when a counter changed, at most once per second per descriptor).
  //! in0_rl_ms_r resets SATURATED so the first change pushes immediately
  //! (reference: last_emit == 0 -> elapsed).
  logic        in0_dirty_r;
  logic [9:0]  in0_rl_ms_r;
  wire         in0_rl_ok = (in0_rl_ms_r >= 10'd1000);

  //! STREAM_OUTPUT counter push state: the same dirty + 1 s window, PER
  //! DESCRIPTOR - Table 5.22's restriction is "per descriptor per second"
  //! and the talker has one Table 5.4 context per Stream Output (every
  //! AAF source + the CRF Media Clock Output). Sized to the full 4-bit
  //! index space; indexes the datapath never wires are tied 0 at the
  //! instance and their limiters constant-propagate away.
  localparam int unsigned TKD_MAX_C = 16;
  logic [TKD_MAX_C-1:0] out_dirty_r;
  logic [9:0]           out_rl_ms_r [TKD_MAX_C];
  logic [TKD_MAX_C-1:0] w_out_rl_ok;
  always_comb begin : out_rl_cmp
    for (int k = 0; k < TKD_MAX_C; k++)
      w_out_rl_ok[k] = (out_rl_ms_r[k] >= 10'd1000);
  end : out_rl_cmp

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
  logic [UNSOL_SLOTS_C-1:0] unsol_pend3_r;  //! slots owed an AVB_INTERFACE
                                            //! GET_COUNTERS push (link/GM edge)
  logic [UNSOL_SLOTS_C-1:0] unsol_pend4_r;  //! slots owed a SET-response replay
                                            //! (u=1 copy of the causing SET's
                                            //! response - reference
                                            //! reply-unsol-helpers rule)
  //! per-slot bitmap of STREAM_OUTPUT descriptor indexes owed a
  //! GET_COUNTERS push (Milan 5.4.5 Table 5.22, talker side)
  logic [TKD_MAX_C-1:0]     unsol_pend5_r [0:UNSOL_SLOTS_C-1];
  logic                  unsol_frame_r;     //! current emit is a push (u=1, no meta pop)
  logic                  ta_prev_r, lo_prev_r;  //! edge detectors

  //! REGISTER helper wires: dedup match + lowest free slot + lowest pend
  logic [UNSOL_SLOTS_C-1:0] w_unsol_match;
  logic [UNSOL_SLOTS_C-1:0] w_unsol_free;
  logic [1:0]               w_unsol_fill_idx;   //! lowest free slot
  logic [1:0]               w_unsol_push_idx;   //! lowest pending slot
  logic [1:0]               w_unsol_push2_idx;  //! lowest counters-pending slot
  logic [1:0]               w_unsol_push3_idx;  //! lowest AVB_IF-pending slot
  logic [1:0]               w_unsol_push4_idx;  //! lowest replay-pending slot
  logic                     w_unsol_anyvalid;   //! any registered controller
  logic                     w_pend5_any;        //! any talker-counters push owed
  logic [3:0]               w_unsol_push5_oidx; //! its lowest descriptor index
  logic [1:0]               w_unsol_push5_idx;  //! lowest slot owing THAT index
  always_comb begin
    for (int s = 0; s < UNSOL_SLOTS_C; s++) begin
      w_unsol_match[s] = unsol_valid_r[s] &&
                         (unsol_eid_r[s] == hdr_q.controller_entity_id);
      w_unsol_free[s]  = !unsol_valid_r[s];
    end
    w_unsol_fill_idx = 2'd0;
    w_unsol_push_idx = 2'd0;
    w_unsol_push2_idx = 2'd0;
    w_unsol_push3_idx = 2'd0;
    w_unsol_push4_idx = 2'd0;
    for (int s = UNSOL_SLOTS_C-1; s >= 0; s--) begin
      if (w_unsol_free[s]) w_unsol_fill_idx = 2'(s);   // lowest wins
      if (unsol_pend_r[s])  w_unsol_push_idx  = 2'(s);
      if (unsol_pend2_r[s]) w_unsol_push2_idx = 2'(s);
      if (unsol_pend3_r[s]) w_unsol_push3_idx = 2'(s);
      if (unsol_pend4_r[s]) w_unsol_push4_idx = 2'(s);
    end
    w_unsol_anyvalid = 1'b0;
    for (int s = 0; s < UNSOL_SLOTS_C; s++)
      if (unsol_valid_r[s]) w_unsol_anyvalid = 1'b1;
    //! talker-counters push pick: lowest pending descriptor index, then
    //! the lowest slot owing it (descending loops - last assignment wins)
    w_pend5_any        = 1'b0;
    w_unsol_push5_oidx = 4'd0;
    w_unsol_push5_idx  = 2'd0;
    for (int k = TKD_MAX_C-1; k >= 0; k--)
      for (int s = UNSOL_SLOTS_C-1; s >= 0; s--)
        if (unsol_pend5_r[s][k]) begin
          w_pend5_any        = 1'b1;
          w_unsol_push5_oidx = 4'(k);
          w_unsol_push5_idx  = 2'(s);
        end
  end

  // ------------------------------------------------------------------ //
  // Stream-info payload constants (shared by the GET_STREAM_INFO command
  // path and the unsolicited push): flags + the live 40-byte tail. The
  // caller still owns segments/cdl/status.                               //
  // ------------------------------------------------------------------ //
  //! uid  = the addressed STREAM_OUTPUT's descriptor_index = the ACMP
  //!        talker_unique_id (the two MUST agree — see w_out_dmac)
  //! dmac = that source's stream_dest_mac (MAAP block base + uid)
  //! acc_lat = THAT index's presentation-offset entry (pres_file_r): the
  //!        command path passes w_gs_pres, the unsolicited push (which
  //!        runs from IDLE with a stale capture buffer) passes entry 0
  //!        directly — never the w_gs_index-keyed mux
  task automatic load_stream_info_consts(input logic [15:0] uid,
                                         input logic [47:0] dmac,
                                         input logic [31:0] acc_lat);
    begin
      //! flags: FORMAT|STREAM_ID|ACC_LAT|DEST_MAC|VLAN|CONNECTED
      //! + MSRP_FAILURE_VALID when the bridge re-declared OUR stream as
      //! TalkerFailed (Milan: the talker reports the FailureInformation)
      const_q[0] <= tk_fail_valid_i ? 8'hFE : 8'hF6;
      const_q[1] <= 8'h00;
      const_q[2] <= 8'h00; const_q[3] <= 8'h00;
      // stream_id = {station_mac, unique_id} — the stream.c formula,
      // byte-identical to the AVTP header and the ACMP PROBE_TX response
      // (KL_acmp_tlkr_ctx echoes the talker_unique_id into the id tail)
      const_q[8]  <= station_mac_i[47:40];
      const_q[9]  <= station_mac_i[39:32];
      const_q[10] <= station_mac_i[31:24];
      const_q[11] <= station_mac_i[23:16];
      const_q[12] <= station_mac_i[15:8];
      const_q[13] <= station_mac_i[7:0];
      const_q[14] <= uid[15:8]; const_q[15] <= uid[7:0];
      const_q[16] <= acc_lat[31:24];              // msrp_accumulated_latency
      const_q[17] <= acc_lat[23:16];              // (per-index pres_file_r)
      const_q[18] <= acc_lat[15:8];
      const_q[19] <= acc_lat[7:0];
      const_q[20] <= dmac[47:40];                 // stream_dest_mac
      const_q[21] <= dmac[39:32];
      const_q[22] <= dmac[31:24];
      const_q[23] <= dmac[23:16];
      const_q[24] <= dmac[15:8];
      const_q[25] <= dmac[7:0];
      const_q[26] <= tk_fail_valid_i ? tk_fail_code_i : 8'h00;
      const_q[27] <= 8'h00;
      for (int k = 0; k < 8; k++)
        const_q[28+k] <= tk_fail_valid_i ? tk_fail_bridge_i[8*(7-k) +: 8] : 8'h00;
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
  //                                                                      //
  // D1 (index coverage): sinks with NO live record — every AAF sink above //
  // index 0 until the KL_acmp_lstn_ctx table port reaches this module     //
  // (docs/NXN_ARCHITECTURE.md §3.6, "GET_STREAM_INFO ... keying the §1.5  //
  // window by descriptor index") — take crf=0/sink0=0 and read as an      //
  // UNBOUND sink: identity fields valid (that is what *_VALID means —     //
  // "meaningful", and zero is a meaningful value), connection flags 0.    //
  // That is a weaker answer than a live record, and it is the answer the  //
  // fabric can actually back; NO_SUCH_DESCRIPTOR for a descriptor         //
  // READ_DESCRIPTOR serves is not an answer at all.                       //
  // ------------------------------------------------------------------ //
  task automatic load_input_stream_info_consts(input logic sink0,
                                               input logic sink1);
    logic        bnd, ta_r, ta_f;
    logic [31:0] fl;
    begin
      //! sink 1 = the CRF input's bind record (no MSRP attach: ta flags 0)
      bnd  = sink0 ? lstn_bound_i : (sink1 & lstn1_bound_i);
      ta_r = sink0 & lstn_ta_reg_i;
      ta_f = sink0 & lstn_ta_fail_i;
      // FORMAT|STREAM_ID|ACC_LAT|DEST_MAC|VLAN always valid. Milan v1.2:
      // NO FastConnect (forbidden) and NO SavedState - CONNECTED (+
      // STREAMING_WAIT while stopped) are the only connection flags.
      fl = 32'hF200_0000;
      if (bnd) begin
        fl = fl | 32'h0400_0000;             // CONNECTED
        //! per-input started level, keyed by the command's own index
        if (!started_in_r[w_gs_index[3:0]])
          fl = fl | 32'h0000_0008;           // STREAMING_WAIT
      end
      //! MSRP_FAILURE_VALID **with the real FailureInformation** (the
      //! Hive-visible "MSRP Failure" line: code + bridge_id from the
      //! registered TalkerFailed - zeroed fields with the flag set were
      //! the 2026-07-19 Hive complaint). Flag bit 6 (SrpRegistrationFailed)
      //! is an ACMP get-state flag, NOT a stream_info flag - removed.
      if (ta_f) fl = fl | 32'h0800_0000;     // MSRP_FAILURE_VALID
      const_q[0] <= fl[31:24]; const_q[1] <= fl[23:16];
      const_q[2] <= fl[15:8];  const_q[3] <= fl[7:0];
      for (int k = 0; k < 8; k++)
        const_q[8+k] <= sink0 ? lstn_sid_i[8*(7-k) +: 8]
                              : ((sink1 & lstn1_bound_i)
                                 ? lstn1_sid_i[8*(7-k) +: 8] : 8'h00);
      //! msrp_accumulated_latency = from the registered Talker attribute
      //! (Milan 5.4.2.7); zero until one is registered
      const_q[16] <= (ta_r|ta_f) ? lstn_ta_acclat_i[31:24] : 8'h00;
      const_q[17] <= (ta_r|ta_f) ? lstn_ta_acclat_i[23:16] : 8'h00;
      const_q[18] <= (ta_r|ta_f) ? lstn_ta_acclat_i[15:8]  : 8'h00;
      const_q[19] <= (ta_r|ta_f) ? lstn_ta_acclat_i[7:0]   : 8'h00;
      for (int k = 0; k < 6; k++)
        const_q[20+k] <= sink0 ? lstn_dmac_i[8*(5-k) +: 8]
                               : ((sink1 & lstn1_bound_i)
                                  ? lstn1_dmac_i[8*(5-k) +: 8] : 8'h00);
      const_q[26] <= ta_f ? lstn_fail_code_i : 8'h00;     // msrp_failure_code
      const_q[27] <= 8'h00;                               // reserved
      for (int k = 0; k < 8; k++)                          // failing bridge_id
        const_q[28+k] <= ta_f ? lstn_fail_bridge_i[8*(7-k) +: 8] : 8'h00;
      //! stream_vlan_id: the registered Talker attribute's vlan when one
      //! exists, else the ACMP-bound vlan
      const_q[36] <= (ta_r|ta_f) ? {4'h0, lstn_ta_vlan_i[11:8]}
                   : sink0      ? {4'h0, lstn_vlan_i[11:8]} : 8'h00;
      const_q[37] <= (ta_r|ta_f) ? lstn_ta_vlan_i[7:0]
                   : sink0      ? lstn_vlan_i[7:0] : 8'h00;
      const_q[38] <= 8'h00; const_q[39] <= 8'h00;
      const_q[40] <= 8'h00; const_q[41] <= 8'h00; const_q[42] <= 8'h00;
      const_q[43] <= {7'b0, ta_r | ta_f};                 // flags_ex REGISTERING
      const_q[44] <= sink0 ? {1'b0, lstn_pbsta_i, lstn_acmpsta_i} : 8'h00;
      const_q[45] <= 8'h00; const_q[46] <= 8'h00; const_q[47] <= 8'h00;
    end
  endtask

  // ------------------------------------------------------------------ //
  // STREAM_INPUT GET_COUNTERS payload (Table 7-156; shared by the         //
  // solicited command and the unsolicited push): valid mask 0xFFF at      //
  // const 0..3, counter for valid bit n at const 4+4n (block byte 4n).   //
  // AAF sinks = live monitor counters; the CRF sink = KL_crf_rx counters  //
  // behind the mandatory-ten mask (its own task below).                   //
  // Every one of the twelve is DRIVEN: MEDIA_RESET counts the received   //
  // mr bit's toggles (Milan Table 5.6), LATE/EARLY the presentation-time  //
  // compare. None of them is an advertised-valid constant zero.           //
  // ------------------------------------------------------------------ //
  //! Milan Table 5.16 counters for the sink named by gs_diag_idx_o -
  //! rxdiag_cnt_i is that sink's twelve-counter slice out of the monitor's
  //! all-context mirror, so EVERY AAF sink serves live values (sink 1 used
  //! to answer this full mask over constant zeros - the R5 lie; sinks >= 2
  //! an empty mask, against 5.4.2.25's "implement and return").
  //! Mirror order C_ML..C_FRX,C_TV,C_TNV maps to the 1722.1 block offsets:
  //! bits 0-5 from slices 0-5, bits 6/7 (TIMESTAMP_VALID/NOT_VALID, Milan
  //! 1.3 5.3.8.10 mandatory) from the APPENDED slices 10/11, bits 8-11
  //! from slices 6-9.
  //! sink-0 flavour for the UNSOLICITED GET_COUNTERS push: that path fires
  //! with no command on the wire, so the gs_diag_idx_o mux (fed from the
  //! solicited command's descriptor_index) has nothing valid to say - it
  //! reads the dedicated stream-0 legacy ports instead, which the monitor
  //! maintains write-through regardless.
  task automatic load_input0_counters_consts;
    begin
      for (int k = 0; k < 52; k++) const_q[k] <= 8'h00;
      const_q[2] <= 8'h0F; const_q[3] <= 8'hFF;   // valid mask 0x00000FFF
      for (int k = 0; k < 4; k++) begin
        const_q[4+k]  <= in0_cnt_locked_i     [8*(3-k) +: 8];  // bit0
        const_q[8+k]  <= in0_cnt_unlocked_i   [8*(3-k) +: 8];  // bit1
        const_q[12+k] <= in0_cnt_interrupted_i[8*(3-k) +: 8];  // bit2
        const_q[16+k] <= in0_cnt_seqmm_i      [8*(3-k) +: 8];  // bit3
        const_q[20+k] <= in0_cnt_mreset_i     [8*(3-k) +: 8];  // bit4
        const_q[24+k] <= in0_cnt_tu_i         [8*(3-k) +: 8];  // bit5
        const_q[28+k] <= in0_cnt_tv_i         [8*(3-k) +: 8];  // bit6
        const_q[32+k] <= in0_cnt_tnv_i        [8*(3-k) +: 8];  // bit7
        const_q[36+k] <= in0_cnt_unsupp_i     [8*(3-k) +: 8];  // bit8
        const_q[40+k] <= in0_cnt_late_i       [8*(3-k) +: 8];  // bit9
        const_q[44+k] <= in0_cnt_early_i      [8*(3-k) +: 8];  // bit10
        const_q[48+k] <= in0_cnt_frx_i        [8*(3-k) +: 8];  // bit11
      end
    end
  endtask

  task automatic load_input_counters_consts;
    begin
      for (int k = 0; k < 52; k++) const_q[k] <= 8'h00;
      const_q[2] <= 8'h0F; const_q[3] <= 8'hFF;   // valid mask 0x00000FFF
      for (int k = 0; k < 4; k++) begin
        const_q[4+k]  <= rxdiag_cnt_i[0*32 + 8*(3-k) +: 8];  // bit0  ML
        const_q[8+k]  <= rxdiag_cnt_i[1*32 + 8*(3-k) +: 8];  // bit1  MU
        const_q[12+k] <= rxdiag_cnt_i[2*32 + 8*(3-k) +: 8];  // bit2  SI
        const_q[16+k] <= rxdiag_cnt_i[3*32 + 8*(3-k) +: 8];  // bit3  SM
        const_q[20+k] <= rxdiag_cnt_i[4*32 + 8*(3-k) +: 8];  // bit4  MR
        const_q[24+k] <= rxdiag_cnt_i[5*32 + 8*(3-k) +: 8];  // bit5  TU
        const_q[28+k] <= rxdiag_cnt_i[10*32 + 8*(3-k) +: 8]; // bit6  TV
        const_q[32+k] <= rxdiag_cnt_i[11*32 + 8*(3-k) +: 8]; // bit7  TNV
        const_q[36+k] <= rxdiag_cnt_i[6*32 + 8*(3-k) +: 8];  // bit8  UF
        const_q[40+k] <= rxdiag_cnt_i[7*32 + 8*(3-k) +: 8];  // bit9  LT
        const_q[44+k] <= rxdiag_cnt_i[8*32 + 8*(3-k) +: 8];  // bit10 ET
        const_q[48+k] <= rxdiag_cnt_i[9*32 + 8*(3-k) +: 8];  // bit11 FRX
      end
    end
  endtask

  //! Milan Table 5.16 for the CRF Media Clock Input (the sink at index
  //! n_aaf_sinks_i): the v1.2 ten behind mask 0x0F3F. Milan 5.3.8.10 keeps
  //! counters "for each Stream Input" with NO CRF exemption, and la_avdecc's
  //! mandatory set (s_MilanMandatoryStreamInputCounters) is exactly these
  //! ten - SUCCESS + the empty mask cost the entity its Milan badge.
  //! MEDIA_LOCKED/UNLOCKED are the KL_crf_rx lock/unlock events,
  //! STREAM_INTERRUPTED its >= 2-PDU sequence losses, SEQ_NUM_MISMATCH its
  //! sequence_num discontinuities, MEDIA_RESET the RECEIVED mr toggle,
  //! TIMESTAMP_UNCERTAIN the received tu bit, UNSUPPORTED_FORMAT its 7.3.2
  //! profile-validation rejects, LATE/EARLY_TIMESTAMP the CRF reference
  //! timestamp against gPTP now, FRAMES_RX its accepted-PDU count. Every
  //! bit of the advertised mask is now a MEASUREMENT - the five that used
  //! to be advertised-valid-but-constant-zero (traceability AVTP-5t) were
  //! worse than an unserved bit: a controller cannot tell a healthy stream
  //! from an instrument that never moves. TV/TNV (bits 6/7, Milan 1.3)
  //! stay UNCLAIMED: no tv tracking exists for the CRF stream.
  wire [31:0] w_crf_cnt_seqmm  = {24'h0, crf_cnt_seqerr_i};
  wire [31:0] w_crf_cnt_unsupp = {24'h0, crf_cnt_fmterr_i};
  wire [31:0] w_crf_cnt_frx    = {16'h0, crf_cnt_pdu_i};
  wire [31:0] w_crf_cnt_mreset = {16'h0, crf_cnt_mreset_i};
  wire [31:0] w_crf_cnt_tu     = {16'h0, crf_cnt_tu_i};
  wire [31:0] w_crf_cnt_late   = {16'h0, crf_cnt_late_i};
  wire [31:0] w_crf_cnt_early  = {16'h0, crf_cnt_early_i};
  task automatic load_crf_input_counters_consts;
    begin
      for (int k = 0; k < 52; k++) const_q[k] <= 8'h00;
      const_q[2] <= 8'h0F; const_q[3] <= 8'h3F;   // valid mask 0x00000F3F
      for (int k = 0; k < 4; k++) begin
        const_q[4+k]  <= crf_cnt_locked_i  [8*(3-k) +: 8];  // bit0  ML
        const_q[8+k]  <= crf_cnt_unlocked_i[8*(3-k) +: 8];  // bit1  MU
        const_q[12+k] <= crf_cnt_intr_i    [8*(3-k) +: 8];  // bit2  SI
        const_q[16+k] <= w_crf_cnt_seqmm   [8*(3-k) +: 8];  // bit3  SM
        const_q[20+k] <= w_crf_cnt_mreset  [8*(3-k) +: 8];  // bit4  MR
        const_q[24+k] <= w_crf_cnt_tu      [8*(3-k) +: 8];  // bit5  TU
        const_q[36+k] <= w_crf_cnt_unsupp  [8*(3-k) +: 8];  // bit8  UF
        const_q[40+k] <= w_crf_cnt_late    [8*(3-k) +: 8];  // bit9  LT
        const_q[44+k] <= w_crf_cnt_early   [8*(3-k) +: 8];  // bit10 ET
        const_q[48+k] <= w_crf_cnt_frx     [8*(3-k) +: 8];  // bit11 FRX
      end
    end
  endtask

  //! per-input "started" levels (START/STOP_STREAMING, Milan input-only
  //! commands). Milan v1.2 5.4.2.19/20: "for EACH Stream Input, the PAAD-AE
  //! shall implement" the pair - one bit per stream_input index (AAF sinks
  //! 0..n_aaf_sinks_i-1 plus the CRF input at n_aaf_sinks_i). The former
  //! single bit latched index 0 only and answered NOT_SUPPORTED above
  //! index 1 (ax-rv32-e triage).
  logic [15:0] started_in_r;

  // ------------------------------------------------------------------ //
  // Main FSM                                                             //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      state_r      <= IDLE_S;
      beat_r       <= 7'd0;   //! beat_r is [6:0] - reset it at its own width
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
      ea_ph_r      <= 1'b0;
      st_addr_q    <= 16'd0;
      ec_addr_q    <= 9'd0;
      dc_ph_r      <= 1'b0;
      pack_r       <= 64'd0;
      pack_n_r     <= 3'd0;
      beat_pend_r  <= 1'b0;
      beat_last_r  <= 1'b0;
      beat_keep_r  <= 8'd0;
      wb_addr_q    <= 16'd0;
      wb_len_q     <= 7'd0;
      wb_src_q     <= 7'd0;
      wb_cnt_r     <= 7'd0;
      wbp_r        <= 1'b0;
      wb_used_q    <= 1'b0;
      wb_diff_q    <= 1'b0;
      batch_q      <= 1'b0;
      bsub_q       <= 1'b0;
      bscan_ptr_q  <= 9'd0; bscan_ph_r <= 3'd0;
      bsc_lo_q     <= 8'd0;
      bslh_r       <= 8'd0; bsch_r <= 7'd0;
      bcdl_acc_q   <= 16'd0; bfit_map_q <= 64'd0; bidx_q <= 6'd0;
      bpay_end_q   <= 9'd0;
      brec_ptr_q   <= 9'd0; brec_ph_r <= 3'd0;
      brec_cmd_q   <= 15'd0; brec_dlen_q <= 16'd0; brec_rlen_q <= 16'd0;
      brec_base_q  <= 16'd0; brec_abase_q <= 16'd0;
      bh_i_r       <= 3'd0;
      bcdl_q       <= 11'd0;
      cap_done_q   <= 1'b0;
      bdbg0_q      <= 32'd0;
      bdbg1_q      <= 32'd0;
      bdbg2_q      <= 32'd0;
      cwld_r       <= 4'd0;
      for (int k = 0; k < 8; k++) rec_hdr_q[k] <= 8'd0;
      st_wr_o      <= 1'b0;
      st_waddr_o   <= 16'd0;
      st_wdata_o   <= 8'd0;
      req_meta_pop_o <= 1'b0;
      pop_pend_r   <= 2'd0;
      evt_cmd_o    <= 1'b0;
      evt_resp_o   <= 1'b0;
      evt_drop_o   <= 1'b0;
      for (int k = 0; k < int'(PRES_N_C); k++) pres_file_r[k] <= PRES_DFLT_C;
      identify_r   <= 1'b0;
      started_in_r <= 16'hFFFF;   //! power-on: every input started
      sysuid_r     <= 32'd0;
      mcr_user_prio_r <= MCR_DEFAULT_PRIO_C;
      cnt_linkup_r <= 32'd0;
      cnt_linkdn_r <= 32'd0;
      cnt_gmchg_r  <= 32'd0;
      link_prev_r  <= 1'b0;
      gm_prev_r    <= 64'd0;
      unsol_pend_r  <= '0;
      unsol_pend3_r <= '0;
      unsol_pend2_r <= '0;
      unsol_pend4_r <= '0;
      unsol_frame_r <= 1'b0;
      ta_prev_r     <= 1'b0;
      lo_prev_r     <= 1'b0;
      fmt_in0_r     <= FMT_IN0_RST_C;
      clk_src_r     <= 16'd0;
      in0_dirty_r   <= 1'b0;
      in0_rl_ms_r   <= 10'd1000;   // saturated: first change pushes at once
      out_dirty_r   <= '0;
      for (int k = 0; k < TKD_MAX_C; k++)
        out_rl_ms_r[k] <= 10'd1000; // saturated, same first-change rule
      for (int s = 0; s < UNSOL_SLOTS_C; s++)
        unsol_pend5_r[s] <= '0;
      for (int s = 0; s < UNSOL_SLOTS_C; s++) begin
        unsol_valid_r[s] <= 1'b0;
        unsol_eid_r[s]   <= 64'd0;
        unsol_mac_r[s]   <= 48'd0;
        unsol_seq_r[s]   <= 16'd0;
      end
`ifdef AEM_DYNMAP
      dmap_wr_p_o    <= 1'b0;
      dmap_wr_addr_o <= 6'd0;
      dmap_wr_word_o <= 8'd0;
      //! the IDENTITY default, not empty: port p's clusters wake mapped to
      //! stream p's channels (DMAP_INIT_C derivation above). Milan
      //! 5.3.10.1 wants the CONTROLLER-set list restored after a power
      //! cycle; with no non-volatile plane behind this store yet, the
      //! restored image is the identity baseline - still the documented
      //! deviation for controller edits, see the doc header.
      for (int k = 0; k < AEM_DMAP_KEYS_C; k++) begin
        automatic logic [7:0] ini = dmap_init_key(k);
        dmap_v_r[k]  <= ini[7];
        dmap_ch_r[k] <= ini[6:3];
        dmap_si_r[k] <= ini[2:0];
      end
      dmseed_r <= 7'd0;
`ifdef AEM_ODYNMAP
      //! the talker maps wake as the identity image too (same rule, same
      //! derivation - AEM_ODMAP_INIT_C is generator-computed from the
      //! port's primary cluster run, kept only where the source projects)
      odmap_wr_p_o    <= 1'b0;
      odmap_wr_slot_o <= 5'd0;
      odmap_wr_word_o <= 14'd0;
      for (int k = 0; k < AEM_ODMAP_KEYS_C; k++) begin
        ov_r[k]  <= AEM_ODMAP_INIT_C[k][5];
        oco_r[k] <= AEM_ODMAP_INIT_C[k][4:0];
      end
      oclaim_r  <= '0;
      for (int c = 0; c < 8; c++) opend_co_r[c] <= 5'd0;
      od_pass_q <= 2'd0;
      dm_out_q  <= 1'b0;
      od_pidx_q <= 4'd0;  od_kb_q <= '0;   od_cb_q <= 7'd0;
      od_pcls_q <= 5'd0;  od_pstr_q <= 4'd0;
      od_slotb_q <= 5'd0; od_schx_q <= 10'd0;
      odseed_r   <= 8'd0;
      odk_t_q <= 13'd0;  odk_ts_q <= 13'd0; odk_coq_ok_q <= 1'b0;
      odk_key_q <= '0;
      odk_v_q <= 1'b0;   odk_sv_q <= 1'b0;
      odk_co_q <= 5'd0;  odk_sco_q <= 5'd0;
`endif
      for (int s = 0; s < AEM_DMAP_NSTRIN_C; s++)
        dm_sch_r[s] <= AEM_DMAP_SCH_C[s];
      dmap_claim_r <= '0;
      dmk_key_q <= '0;      dmk_keyok_q <= 1'b0; dmk_physok_q <= 1'b0;
      dmk_siin_q <= 1'b0;   dmk_saaf_q <= 1'b0;  dmk_sch_q <= 10'd0;
      dmk_v_q <= 1'b0;      dmk_ch_q <= 4'd0;    dmk_si_q <= 3'd0;
      dmk_claim_q <= 1'b0;
      dmi_r <= 6'd0; dmn_q <= 6'd0; dmph_r <= 4'd0; dm_hi_r <= 8'd0;
      dm_si_q <= 16'd0; dm_sc_q <= 16'd0;
      dm_co_q <= 16'd0; dm_cc_q <= 16'd0;
      dm_commit_q <= 1'b0; dm_remove_q <= 1'b0; dmap_diff_q <= 1'b0;
      dm_pbase_q <= 7'd0; dm_pcls_q <= 7'd0;
      dmp_key_r <= 7'd0; dmp_sidx_q <= '0; dmp_ch_q <= 10'd0;
      dmg_key_r <= 7'd0; dmg_end_r <= 7'd0; dmg_base_r <= 7'd0;
      dmg_nmaps_q <= 8'd0; dmg_n_r <= 4'd0;
`endif
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
`ifdef AEM_DYNMAP
      dmap_wr_p_o <= 1'b0;

      // ---- post-reset fabric seed: mirror the identity default into ----
      //      the render crossbar, one key per IDLE_S cycle. The store is
      //      the truth (it woke as DMAP_INIT_C); the crossbar wakes empty
      //      on its own reset, and the wire-truth rule forbids the two
      //      disagreeing. Commits own dmap_wr_* only in DMAP_SCAN_S /
      //      DMAP_PRUNE_S, never in IDLE_S, so the walker cannot collide;
      //      a command edit that lands mid-walk is still served truthfully
      //      because the walker reads the LIVE store, not the constant.
      if (dmseed_r < 7'(AEM_DMAP_KEYS_C) && state_r == IDLE_S) begin
        dmap_wr_p_o    <= dmap_v_r[dmseed_r[DMAP_KW_C-1:0]];
        dmap_wr_addr_o <= 6'(dmseed_r);
        dmap_wr_word_o <= {dmap_v_r[dmseed_r[DMAP_KW_C-1:0]], 1'b0,
                           dmap_si_r[dmseed_r[DMAP_KW_C-1:0]],
                           dmap_ch_r[dmseed_r[DMAP_KW_C-1:0]][2:0]};
        dmseed_r <= dmseed_r + 7'd1;
      end
`ifdef AEM_ODYNMAP
      odmap_wr_p_o <= 1'b0;
      //! the capture-crossbar seed: one PAIR slot per IDLE_S cycle. The
      //! template comes from the LIVE store so a pre-seed edit is still
      //! truthful, and the half-enable is read off the two keys rather
      //! than assumed - the identity image is pair-complete today, but a
      //! seed that could only express a WHOLE pair is the same assumption
      //! that made an odd command unrepresentable.
      if (odseed_r < 8'(AEM_ODMAP_KEYS_C) && state_r == IDLE_S) begin
        automatic logic vl = ov_r[odseed_r[ODMAP_KW_C-1:0]];
        automatic logic vr = ov_r[odseed_r[ODMAP_KW_C-1:0] + 1'b1];
        automatic logic [12:0] t = AEM_ODMAP_CSRC_C[
            32'(AEM_ODMAP_PCBASE_C[32'(odseed_r) / 8])
            + 32'(vl ? oco_r[odseed_r[ODMAP_KW_C-1:0]]
                     : oco_r[odseed_r[ODMAP_KW_C-1:0] + 1'b1])];
        if (vl || vr) begin
          odmap_wr_p_o    <= 1'b1;
          odmap_wr_slot_o <= 5'(AEM_ODMAP_SLOTB_C[32'(odseed_r) / 8])
                             + 5'(odseed_r[2:1]);
          odmap_wr_word_o <= {vl, vr, t[7:4], 1'b1, t[10:8], t[3:0]};
        end
        odseed_r <= odseed_r + 8'd2;
      end
`endif
`endif

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

      // ---- STREAM_OUTPUT counter push (Milan §5.4.5): the same window,
      //      PER descriptor - Table 5.22 restricts per descriptor --------
      for (int k = 0; k < TKD_MAX_C; k++) begin
        if (tick_1khz_i && !w_out_rl_ok[k])
          out_rl_ms_r[k] <= out_rl_ms_r[k] + 10'd1;
        if (tkdiag_dirty_p_i[k]) out_dirty_r[k] <= 1'b1;
        if (out_dirty_r[k] && w_out_rl_ok[k]) begin
          for (int s = 0; s < UNSOL_SLOTS_C; s++)
            if (unsol_valid_r[s]) unsol_pend5_r[s][k] <= 1'b1;
          out_dirty_r[k] <= 1'b0;
          //! the window is consumed by SENDING (Table 5.22 restricts the
          //! notifications), so an update with nobody registered neither
          //! burns it nor leaves a stale push armed for a later REGISTER
          if (w_unsol_anyvalid) out_rl_ms_r[k] <= 10'd0;
        end
      end

      // ---- GET_COUNTERS event counting (edges) ------------------------
      link_prev_r <= link_up_i;
      if (link_up_i & ~link_prev_r) cnt_linkup_r <= cnt_linkup_r + 32'd1;
      if (~link_up_i & link_prev_r) cnt_linkdn_r <= cnt_linkdn_r + 32'd1;
      gm_prev_r <= gptp_gm_id_i;
      if (gptp_gm_id_i != gm_prev_r) cnt_gmchg_r <= cnt_gmchg_r + 32'd1;
      //! AVB_INTERFACE counter change -> unsolicited GET_COUNTERS push to
      //! the registered controllers (Milan 5.4.5; CERT link-flap test)
      if ((link_up_i ^ link_prev_r) || (gptp_gm_id_i != gm_prev_r)) begin
        for (int s = 0; s < UNSOL_SLOTS_C; s++)
          if (unsol_valid_r[s]) unsol_pend3_r[s] <= 1'b1;
      end
      //! (SET_STREAM_INFO notification: handled by the is_replay_cmd path -
      //! the SET response replays u=1 to the other controllers, which is the
      //! CERT-es-4.5-required shape. The old GET-shaped push on the offset write
      //! double-notified and was removed 2026-07-20.)

      // ---------------- capture (runs in IDLE/CAPTURE) ----------------
      //! the cbuf RAM write itself lives in its OWN sync-only process
      //! below: written inside this async-reset block, Vivado refuses RAM
      //! inference (Synth 8-4767 "RAM is sensitive to asynchronous reset")
      //! and falls back to 4 K flops with mangled set/reset priority
      //! (Synth 8-7137 "may cause simulation mismatches") = the mf37/mf38
      //! silicon 0x4B garbage-scan that no TB could reproduce (empty batch
      //! passed, any record read garbage, classic/cw* paths untouched)
      if (w_cap_hs) begin
        if (s_axis_tlast) cap_done_q <= 1'b1;
        else if (beat_r == 7'd0) cap_done_q <= 1'b0;
        if (beat_r == 7'd3) cw0_r <= s_axis_tdata;   // buf bytes 0-7
        if (beat_r == 7'd4) cw1_r <= s_axis_tdata;   // buf bytes 8-15
        if (beat_r == 7'd6) cw3_r <= s_axis_tdata;   // buf bytes 24-31
        beat_r <= s_axis_tlast ? 7'd0 : (beat_r == 7'd127 ? 7'd127 : beat_r + 7'd1);
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
            if (!batch_q) pay_len_q <= a;   // batch: sized in BSCAN_S
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
            //! the push is STREAM_OUTPUT[0]: uid 0, MAAP block base,
            //! presentation-offset entry 0 (w_gs_index is stale here)
            load_stream_info_consts(16'd0, aaf_dmac_i, pres_file_r[0]);
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
            load_input0_counters_consts;
            cdl_q      <= 11'd148;   // 12 + 136
            wb_len_q   <= 7'd0; wb_cnt_r <= 7'd0;
            cum_done_q <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
            fi_r       <= 16'd0;
            state_r    <= WRITE_S;
          end else if (enable_i && unsol_pend3_r != '0) begin
            //! Unsolicited GET_COUNTERS for AVB_INTERFACE[0] (u=1) on a
            //! link/GM edge - Milan 5.4.5 / CERT link-flap. Same full-136B
            //! shape as the solicited path.
            unsol_pend3_r[w_unsol_push3_idx] <= 1'b0;
            unsol_seq_r[w_unsol_push3_idx]   <= unsol_seq_r[w_unsol_push3_idx] + 16'd1;
            unsol_frame_r <= 1'b1;
            dst_mac_q     <= unsol_mac_r[w_unsol_push3_idx];
            hdr_q.controller_entity_id <= unsol_eid_r[w_unsol_push3_idx];
            hdr_q.sequence_id          <= unsol_seq_r[w_unsol_push3_idx];
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
            const_q[56] <= 8'h00; const_q[57] <= 8'h09;   // AVB_INTERFACE
            const_q[58] <= 8'h00; const_q[59] <= 8'h00;   // index 0
            for (int k = 0; k < 52; k++) const_q[k] <= 8'h00;
            const_q[3] <= 8'h23;   // LINK_UP|LINK_DOWN|GPTP_GM_CHANGED
            for (int k = 0; k < 4; k++) begin
              const_q[4+k]  <= cnt_linkup_r[8*(3-k) +: 8];  // bit0
              const_q[8+k]  <= cnt_linkdn_r[8*(3-k) +: 8];  // bit1
              const_q[24+k] <= cnt_gmchg_r [8*(3-k) +: 8];  // bit5
            end
            cdl_q      <= 11'd148;   // 12 + 136
            wb_len_q   <= 7'd0; wb_cnt_r <= 7'd0;
            cum_done_q <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
            fi_r       <= 16'd0;
            state_r    <= WRITE_S;
          end else if (enable_i && w_pend5_any) begin
            //! Unsolicited GET_COUNTERS for STREAM_OUTPUT[k] (u=1): one of
            //! source k's Table 5.4 counters was updated (Milan 5.4.5 Table
            //! 5.22; rate-limited per descriptor above). Payload = the
            //! solicited arm's exact shape - mask 0x1F + the five live
            //! KL_talker_diag_ctx counters, which tkdiag_cnt_i carries for
            //! THIS k because gs_diag_idx_o is pre-muxed to the pending
            //! index for as long as the push waits in IDLE_S.
            unsol_pend5_r[w_unsol_push5_idx][w_unsol_push5_oidx] <= 1'b0;
            unsol_seq_r[w_unsol_push5_idx] <= unsol_seq_r[w_unsol_push5_idx] + 16'd1;
            unsol_frame_r <= 1'b1;
            dst_mac_q     <= unsol_mac_r[w_unsol_push5_idx];
            hdr_q.controller_entity_id <= unsol_eid_r[w_unsol_push5_idx];
            hdr_q.sequence_id          <= unsol_seq_r[w_unsol_push5_idx];
            hdr_q.command_type         <= CMD_GET_COUNTERS;
            vu_q       <= 1'b0;
            msg_resp_q <= MSG_AEM_RESPONSE;
            status_q   <= STATUS_SUCCESS;
            for (int s = 4; s < SEGN_C; s++) begin
              seg_kind_q[s] <= SEG_NONE; seg_len_q[s] <= 16'd0;
            end
            seg_kind_q[0] <= SEG_CONST; seg_addr_q[0] <= 16'd56; seg_len_q[0] <= 16'd4;
            seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0;  seg_len_q[1] <= 16'd28;
            seg_kind_q[2] <= SEG_NONE;  seg_addr_q[2] <= 16'd0;  seg_len_q[2] <= 16'd104;
            seg_kind_q[3] <= SEG_NONE;  seg_addr_q[3] <= 16'd0;  seg_len_q[3] <= 16'd0;
            const_q[56] <= 8'h00; const_q[57] <= 8'h06;   // STREAM_OUTPUT
            const_q[58] <= 8'h00;
            const_q[59] <= {4'd0, w_unsol_push5_oidx};    // its index
            for (int k = 0; k < 28; k++) const_q[k] <= 8'h00;
            const_q[3] <= 8'h1F;   // START|STOP|MEDIA_RESET|TS_UNC|FRAMES_TX
            for (int k = 0; k < 4; k++) begin
              const_q[4+k]  <= tkdiag_cnt_i[0*32 + 8*(3-k) +: 8]; // bit0 START
              const_q[8+k]  <= tkdiag_cnt_i[1*32 + 8*(3-k) +: 8]; // bit1 STOP
              const_q[12+k] <= tkdiag_cnt_i[2*32 + 8*(3-k) +: 8]; // bit2 MR
              const_q[16+k] <= tkdiag_cnt_i[3*32 + 8*(3-k) +: 8]; // bit3 TU
              const_q[20+k] <= tkdiag_cnt_i[4*32 + 8*(3-k) +: 8]; // bit4 FTX
            end
            cdl_q      <= 11'd148;   // 12 + 136
            wb_len_q   <= 7'd0; wb_cnt_r <= 7'd0;
            cum_done_q <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
            fi_r       <= 16'd0;
            state_r    <= WRITE_S;
          end
        end

        // ---------------------------------------------------------- //
        CAPTURE_S: begin
          //! The validator REJECTED this frame, so frame_ok_i is never
          //! coming (KL_aecp_packet_validator.sv PASS_S raises drop_o
          //! instead when the frame under-delivers its own declared
          //! 6 + control_data_length). Without this arm the builder parks
          //! here for good, which skips IDLE_S's `discard_q <= !enable_i`
          //! re-arm below - and discard_q was already LATCHED from the
          //! rejected frame's header a few beats earlier. The next frame
          //! captures on top of it and SPENDS that discard at its own
          //! frame_ok_i, so a foreign or arrive-while-disabled reject
          //! silently eats one good command addressed to us (1722.1-2021
          //! 9.2.1.1 owes it a response; the controller sees a timeout).
          //! Re-arm exactly as IDLE_S would, in the same cycle it would.
          //! pop_pend_r is deliberately NOT touched: the unconditional
          //! frame_bad_i handler above already counted the drop and queued
          //! the meta pop, and a second increment here would over-pop.
          //! hdr_q needs no scrub either - the validator only ever raises
          //! frame_ok_i for a frame that delivered >= 26 octets (cdl >= 12
          //! plus the 14-octet origin), so beat 3 and its hdr_valid always
          //! land first and overwrite the rejected frame's header.
          if (frame_bad_i) begin
            discard_q <= !enable_i;
            state_r   <= IDLE_S;
          end else if (frame_ok_i) begin
            if (discard_q || (hdr_i.hdr_valid && (mismatch_i || !enable_i))) begin
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
          if (!dc_ph_r) begin
          // Phase 0: RESOLVE the directory oracle and do nothing else (see
          // the declaration block for why the split is coherent). w_acc_en
          // is high exactly this cycle, so u_acc latches its BRAM read +
          // hit on the edge that ends it; the dispatch below reads the
          // accessor's registered outputs (and w_name_ptr derived from
          // them), so no ROM read ever appears in the same cone as the
          // ~40-arm case that drives status_q / wb_* / const_q.
          dc_ph_r     <= 1'b1;
          end else begin
          // Phase 1: the dispatch. Cleared unconditionally, so an arm that
          // re-enters DECIDE_S still resolves before it dispatches.
          dc_ph_r <= 1'b0;
          // defaults: NOT_IMPLEMENTED echo of the command payload
          for (int s = 0; s < SEGN_C; s++) begin
            seg_kind_q[s] <= SEG_NONE; seg_addr_q[s] <= 16'd0; seg_len_q[s] <= 16'd0;
          end
          msg_resp_q <= vu_q ? MSG_VENDOR_UNIQUE_RESPONSE : MSG_AEM_RESPONSE;
          status_q   <= STATUS_NOT_IMPLEMENTED;
          nochg_q    <= 1'b0;
`ifdef AEM_ODYNMAP
          dm_out_q <= 1'b0;
`endif
          wbp_r      <= 1'b0;
          wb_used_q  <= 1'b0;
          wb_diff_q  <= 1'b0;
          seg_kind_q[0] <= SEG_ECHO;
          seg_addr_q[0] <= 16'd2;
          seg_len_q[0]  <= (hdr_q.control_data_length > 11'd12)
                           ? ((hdr_q.control_data_length > 11'd506)
                              ? 16'd494
                              : 16'(hdr_q.control_data_length) - 16'd12)
                           : 16'd0;
          cdl_q      <= w_cdl_echo;
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
            case (w_cmd_eff)
              // -------------------------------------------------- //
              CMD_ACQUIRE_ENTITY, CMD_LOCK_ENTITY: begin
                //! DESCRIPTOR SCOPE. Both commands name a target descriptor
                //! at payload bytes 14-17 (AECPDU 36-39, Figures 7-27/7-28),
                //! and for a PAAD-AE the only lockable one is the ENTITY
                //! descriptor at index 0 - 1722.1-2021 Table 7-2: its
                //! descriptor_index "is always set to zero (0) for the ENTITY
                //! descriptor as there is only ever one in an ATDECC Entity",
                //! so ENTITY/n>0 names no descriptor at all.
                //!
                //! The refusal is NOT_SUPPORTED, not NO_SUCH_DESCRIPTOR.
                //! Milan v1.2 5.4.2.2 spells it out for LOCK: "The PAAD-AE
                //! shall not allow locking another descriptor than the ENTITY
                //! descriptor (NOT_SUPPORTED shall be returned in this
                //! case)". For ACQUIRE, 5.4.2.1 makes NOT_SUPPORTED the
                //! answer to EVERY acquire ("shall not reply SUCCESS ...
                //! should reply with the NOT_SUPPORTED error code"), which
                //! 1722.1-2021 7.4.1.2 expressly permits: "it may always
                //! reply with the NOT_SUPPORTED error code if it does not
                //! support being acquired". l0_status_q is already
                //! NOT_SUPPORTED for acquire, so this arm is uniform.
                //!
                //! The other half of 5.4.2.2 - "shall not ALLOW locking" - is
                //! enforced in KL_aecp_l0_state, which defers the commit to
                //! the parser's al_gate_p_o for exactly this reason. Refusing
                //! in the response while locking the entity anyway would deny
                //! every other controller for 60 s on a command we rejected.
                status_q      <= (w_lock_desc_ok) ? l0_status_q
                                                  : STATUS_NOT_SUPPORTED;
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
                //! single-config entity: an accepted SET_CONFIGURATION is
                //! always to the current index = never a state change
                nochg_q  <= (hdr_q.command_type == CMD_SET_CONFIGURATION);
                seg_kind_q[0] <= SEG_CONST; seg_addr_q[0] <= 16'd0; seg_len_q[0] <= 16'd4;
                const_q[0] <= 8'h00; const_q[1] <= 8'h00;
                const_q[2] <= l0_state_i.current_configuration_index[15:8];
                const_q[3] <= l0_state_i.current_configuration_index[7:0];
                cdl_q <= 11'd16;
              end

              // -------------------------------------------------- //
              //! D2 same class as GET_STREAM_INFO: SET/GET_NAME Response is
              //! 72 B (1722.1 §7.4.17.1/§7.4.18.2 — descriptor_type(2)+
              //! descriptor_index(2)+name_index(2)+configuration_index(2)+
              //! object_name(64); la_avdecc AecpAemGetNameResponsePayloadSize
              //! = 72) on EVERY status. The error exits used to declare
              //! cdl 84 while emitting an 8-byte payload (a frame SHORTER
              //! than its own control_data_length — worse than a short cdl),
              //! or echo the 20-byte GET command. Both now emit the echo
              //! plus a zero object_name tail so the declared and emitted
              //! lengths agree at 72.
              CMD_GET_NAME, CMD_SET_NAME: begin
                cdl_q <= 11'd84;   // 12 + 8 + 64
                if (l0_reject_q || !acc_found || w_name_cfg != 16'd0 ||
                    !w_name_ptr[16]) begin
                  status_q      <= l0_reject_q ? l0_status_q
                                 : acc_found ? STATUS_BAD_ARGUMENTS
                                               : STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0]  <= (hdr_q.command_type == CMD_SET_NAME)
                                   ? 16'd72 : 16'd8;
                  seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0;
                  seg_len_q[1]  <= (hdr_q.command_type == CMD_SET_NAME)
                                   ? 16'd0 : 16'd64;
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
                  cdl_q        <= w_cdl_echo;
                end else if (w_gs_type != DESC_CONTROL || w_gs_index != 16'd0) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= (hdr_q.command_type == CMD_SET_CONTROL)
                                  ? 16'd5 : 16'd4;
                  cdl_q        <= w_cdl_echo;
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
              // GET_AUDIO_MAP (§7.4.44). Milan v1.2 5.4.2.26 splits this by
              // DIRECTION, and the split is quoted at the w_smap_*
              // declarations: an INPUT port must implement the command per
              // 7.4.44, an OUTPUT port that HAS Audio Map(s) "shall reply
              // with the NOT_SUPPORTED error code". A STATIC port of either
              // direction is served from the AUDIO_MAP its OWN base_map
              // names (AEM_SMAP_*_ADDR/ROWS/MOFF). Under `AEM_DYNMAP every
              // map_mode-dynamic STREAM_PORT_INPUT carries NO Audio Map
              // (7.2.13 number_of_maps=0) and is served from the shared
              // mappings store instead: GET pages THAT port's own fixed
              // partition (5.4.2.26; map_index beyond its own
              // number_of_maps -> BAD_ARGUMENT per 7.4.44.1) and ADD/REMOVE
              // edit it (5.4.2.27/28). Every non-success exit keeps the
              // 7.4.44.2 12-octet response-payload floor (D2): the status
              // changes, the shape does not.
`ifdef AEM_DYNMAP
              CMD_GET_AUDIO_MAP: begin
                if (w_dm_pin_dyn) begin
                  if (w_dmg_p >= 16'(AEM_DMAP_PNMAPS_C[w_dm_pidx])) begin
                    //! 7.4.44.1 paging, at the 7.4.44.2 12-octet floor
                    status_q      <= STATUS_BAD_ARGUMENTS;
                    seg_len_q[0]  <= 16'd6;
                    seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                    cdl_q         <= 11'd24;
                  end else begin
                    //! dynamic input port: the page scan fills the const
                    //! scratch; DMAP_GET_S finalizes seg1 length + cdl
                    status_q      <= STATUS_SUCCESS;
                    seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd6;
                    seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                    dmg_base_r  <= 7'(w_dmg_pb);
                    dmg_key_r   <= w_dmg_kbeg;
                    dmg_end_r   <= w_dmg_kend;
                    dmg_nmaps_q <= 8'(AEM_DMAP_PNMAPS_C[w_dm_pidx]);
                    dmg_n_r     <= 4'd0;
                    state_r     <= DMAP_GET_S;
                  end
`ifdef AEM_ODYNMAP
                end else if (w_od_dyn) begin
                  //! dynamic OUTPUT port (Milan 5.4.2.26: a Stream Port
                  //! Output with NO Audio Map SHALL implement this). The
                  //! output partition is over the Stream Output's channels
                  //! - at most 8, so every port is ONE page.
                  if (w_dmg_p != 16'd0) begin
                    status_q      <= STATUS_BAD_ARGUMENTS;
                    seg_len_q[0]  <= 16'd6;
                    seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0;
                    seg_len_q[1]  <= 16'd6;
                    cdl_q         <= 11'd24;
                  end else begin
                    status_q      <= STATUS_SUCCESS;
                    seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2;
                    seg_len_q[0]  <= 16'd6;
                    seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0;
                    seg_len_q[1]  <= 16'd6;
                    dm_out_q    <= 1'b1;
                    od_pstr_q   <= 4'(AEM_ODMAP_PSTR_C[w_od_pidx]);
                    od_kb_q     <= ODMAP_KW_C'(32'(w_od_pidx) * 8);
                    dmg_key_r   <= 7'(32'(w_od_pidx) * 8);
                    dmg_end_r   <= 7'(32'(w_od_pidx) * 8 + 8);
                    dmg_nmaps_q <= 8'd1;
                    dmg_n_r     <= 4'd0;
                    state_r     <= DMAP_GET_S;
                  end
`endif
                end else if (w_smap_milan_ns) begin
                  //! Milan v1.2 5.4.2.26: "If a PAAD-AE receives a
                  //! GET_AUDIO_MAP command for a Stream Port Output that has
                  //! Audio Map(s), the PAAD-AE shall reply with the
                  //! NOT_SUPPORTED error code."
                  status_q      <= STATUS_NOT_SUPPORTED;
                  seg_len_q[0]  <= 16'd6;
                  seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                  cdl_q         <= 11'd24;   // 12 + 12
                end else if (w_smap_badidx) begin
                  //! 7.4.44.1: "If the map_index is beyond the range of
                  //! available maps then it returns a BAD_ARGUMENT status in
                  //! the response."
                  status_q      <= STATUS_BAD_ARGUMENTS;
                  seg_len_q[0]  <= 16'd6;
                  seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                  cdl_q         <= 11'd24;
                end else if (!w_smap_ok) begin
                  //! not a STREAM_PORT of this shape at all
                  status_q      <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0]  <= 16'd6;
                  seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                  cdl_q         <= 11'd24;   // 12 + 12
                end else begin
                  //! a STATIC port in a mixed shape: served from its OWN
                  //! base_map, its own number_of_mappings and its own
                  //! mappings_offset - never a hardcoded descriptor index
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd6;
                  seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                  const_q[0] <= 8'h00; const_q[1] <= 8'h01;   // number_of_maps
                  const_q[2] <= w_smap_rows[15:8];            // number_of_mappings
                  const_q[3] <= w_smap_rows[7:0];             //   = the descriptor's own
                  const_q[4] <= 8'h00; const_q[5] <= 8'h00;   // reserved
                  seg_kind_q[2] <= SEG_STORE;
                  seg_addr_q[2] <= w_smap_addr + w_smap_moff;
                  seg_len_q[2]  <= w_smap_blen;               // rows x 8 B
                  cdl_q <= 11'(16'd24 + w_smap_blen);
                end
              end

              //! ADD/REMOVE_AUDIO_MAPPINGS (§7.4.45/46, Milan 5.4.2.27/28)
              //! on any dynamic input port; a port that HAS Audio Maps —
              //! every output port, and a static input port in a mixed
              //! shape — keeps the mandated NOT_SUPPORTED. The frame must
              //! carry exactly number_of_mappings records; the walk
              //! validates then commits (ADD all-or-nothing, REMOVE
              //! lenient: unmatched and duplicate entries are ignored per
              //! 5.4.2.28).
              CMD_ADD_AUDIO_MAPPINGS, CMD_REMOVE_AUDIO_MAPPINGS: begin
                if (l0_reject_q) begin
                  status_q <= l0_status_q;   //! lock rule (5.4.2.27/28)
`ifdef AEM_ODYNMAP
                end else if (w_od_dyn) begin
                  //! dynamic OUTPUT port (Milan 5.4.2.27/28 SHALL when the
                  //! port has no Audio Map). Same command framing as the
                  //! input engine. NOTE what is NOT here: a parity test on
                  //! number_of_mappings. 7.4.45/7.4.46 bound this field
                  //! only by what the PDU carries and Milan 5.4.2.27/28
                  //! list every legal BAD_ARGUMENTS condition without ever
                  //! mentioning a count - a controller that maps ONE
                  //! channel (the normal case, and 5.4.2.26's own "at most
                  //! one dynamic mapping per Stream Output's channel"
                  //! granularity) is sending a conformant command.
                  if (w_dm_n > 16'd60) begin
                    status_q <= STATUS_BAD_ARGUMENTS;
                  end else if (16'(hdr_q.control_data_length) !=
                               16'd20 + {w_dm_n[12:0], 3'd0}) begin
                    status_q <= STATUS_BAD_ARGUMENTS;   //! malformed length
                  end else if (w_dm_n == 16'd0) begin
                    status_q <= STATUS_SUCCESS;         //! empty edit
                    nochg_q  <= 1'b1;
                  end else begin
                    status_q    <= STATUS_SUCCESS;      //! walk may demote
                    dmn_q       <= 6'(w_dm_n);
                    dmi_r       <= 6'd0;
                    dmph_r      <= 4'd0;
                    dm_out_q    <= 1'b1;
                    od_pidx_q   <= w_od_pidx;
                    od_kb_q     <= ODMAP_KW_C'(32'(w_od_pidx) * 8);
                    od_cb_q     <= 7'(AEM_ODMAP_PCBASE_C[w_od_pidx]);
                    od_pcls_q   <= 5'(AEM_ODMAP_PCLS_C[w_od_pidx]);
                    od_pstr_q   <= 4'(AEM_ODMAP_PSTR_C[w_od_pidx]);
                    od_slotb_q  <= 5'(AEM_ODMAP_SLOTB_C[w_od_pidx]);
                    od_schx_q   <= 10'(AEM_ODMAP_SCH_C[w_od_pidx]);
                    dm_remove_q <= (w_cmd_eff == CMD_REMOVE_AUDIO_MAPPINGS);
                    dm_commit_q <= 1'b0;
                    od_pass_q   <= 2'd0;
                    oclaim_r    <= '0;
                    dmap_diff_q <= 1'b0;
                    state_r     <= DMAP_SCAN_S;
                  end
`endif
                end else if (w_smap_milan_ns ||
                             (w_dm_pin_ok && !w_dm_pin_dyn)) begin
                  //! a port that HAS Audio Map(s): Milan 5.4.2.27/28 word
                  //! this identically to 5.4.2.26 - "the PAAD-AE shall
                  //! reply with the NOT_SUPPORTED error code"
                  status_q <= STATUS_NOT_SUPPORTED;
                end else if (!w_dm_pin_dyn) begin
                  status_q <= STATUS_NO_SUCH_DESCRIPTOR;
                end else if (w_dm_n > 16'd60) begin
                  //! engine bound: 60 mappings/command (a 176-mapping edit
                  //! cannot fit one AECPDU anyway; documented)
                  status_q <= STATUS_BAD_ARGUMENTS;
                end else if (16'(hdr_q.control_data_length) !=
                             16'd20 + {w_dm_n[12:0], 3'd0}) begin
                  status_q <= STATUS_BAD_ARGUMENTS;   //! malformed length
                end else if (w_dm_n == 16'd0) begin
                  status_q <= STATUS_SUCCESS;         //! empty edit
                  nochg_q  <= 1'b1;
                end else begin
                  status_q     <= STATUS_SUCCESS;     //! walk may demote
                  dmn_q        <= 6'(w_dm_n);
                  dmi_r        <= 6'd0;
                  dmph_r       <= 4'd0;
                  dm_pbase_q   <= 7'(AEM_DMAP_PBASE_C[w_dm_pidx]);
                  dm_pcls_q    <= 7'(AEM_DMAP_PCLS_C[w_dm_pidx]);
                  dm_remove_q  <= (w_cmd_eff == CMD_REMOVE_AUDIO_MAPPINGS);
                  //! BOTH directions validate first (7.4.45.1 / 7.4.46.1
                  //! are all-or-nothing in identical words) — REMOVE used
                  //! to jump straight to the commit pass, which made
                  //! "invalid or not present" unenforceable
                  dm_commit_q  <= 1'b0;
                  dmap_claim_r <= '0;
                  dmap_diff_q  <= 1'b0;
                  state_r      <= DMAP_SCAN_S;
                end
              end
`else
              CMD_GET_AUDIO_MAP: begin
                //! D3 (defect A): the served map, its length and its start
                //! all come from the ADDRESSED PORT'S OWN row (w_smap_addr /
                //! w_smap_rows / w_smap_moff, from its base_map) instead of
                //! a hardcoded descriptor index, 8 mappings and 64 bytes -
                //! see the w_smap_* declarations for the quoted clauses and
                //! the 48-byte over-read the constants caused at 8x8.
                //! Every non-success exit keeps the 7.4.44.2 12-octet
                //! response payload (D2): status changes, shape does not.
                if (w_smap_milan_ns) begin
                  //! Milan v1.2 5.4.2.26: "If a PAAD-AE receives a
                  //! GET_AUDIO_MAP command for a Stream Port Output that has
                  //! Audio Map(s), the PAAD-AE shall reply with the
                  //! NOT_SUPPORTED error code."
                  status_q      <= STATUS_NOT_SUPPORTED;
                  seg_len_q[0]  <= 16'd6;
                  seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                  cdl_q         <= 11'd24;   // 12 + 12
                end else if (w_smap_badidx) begin
                  //! 7.4.44.1: "If the map_index is beyond the range of
                  //! available maps then it returns a BAD_ARGUMENT status in
                  //! the response."
                  status_q      <= STATUS_BAD_ARGUMENTS;
                  seg_len_q[0]  <= 16'd6;
                  seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                  cdl_q         <= 11'd24;
                end else if (!w_smap_ok) begin
                  //! not a STREAM_PORT of this shape at all
                  status_q      <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0]  <= 16'd6;
                  seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                  cdl_q         <= 11'd24;   // 12 + 12
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd6;
                  seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd6;
                  const_q[0] <= 8'h00; const_q[1] <= 8'h01;   // number_of_maps
                  const_q[2] <= w_smap_rows[15:8];            // number_of_mappings
                  const_q[3] <= w_smap_rows[7:0];             //   = the descriptor's own
                  const_q[4] <= 8'h00; const_q[5] <= 8'h00;   // reserved
                  seg_kind_q[2] <= SEG_STORE;
                  //! the descriptor's OWN mappings_offset (7.2.19: the
                  //! mappings "shall be accessed by using the mappings_offset
                  //! field as any fields added in the future will be added
                  //! before the mappings field")
                  seg_addr_q[2] <= w_smap_addr + w_smap_moff;
                  seg_len_q[2]  <= w_smap_blen;               // rows x 8 B
                  cdl_q <= 11'(16'd24 + w_smap_blen);         // 12 + 6 + 6 + rows*8
                end
              end

              CMD_ADD_AUDIO_MAPPINGS, CMD_REMOVE_AUDIO_MAPPINGS: begin
                status_q <= STATUS_NOT_SUPPORTED;   // static default maps
              end
`endif

              // -------------------------------------------------- //
              // GET/SET_STREAM_FORMAT: STREAM_OUTPUT[0] + the two listener
              // sinks (Milan adaptive listener, FR-STR-03) — sink0 validates
              // against the AAF set, sink1 against the CRF set. Multi-stream
              // svh layouts (`AEM_PER_STREAM_FMT) serve EVERY descriptor from
              // its own table entry + write-back address instead.
              CMD_GET_STREAM_FORMAT, CMD_SET_STREAM_FORMAT: begin
                cdl_q <= 11'd24;   // 12 + 4 + 8
                if (l0_reject_q) begin
                  status_q     <= l0_status_q;
                  seg_len_q[0] <= 16'd12;
`ifdef AEM_PER_STREAM_FMT
                end else if (!((w_gs_type == DESC_STREAM_OUTPUT &&
                                w_gs_index < 16'(AEM_N_STROUT_C)) ||
                               (w_gs_type == DESC_STREAM_INPUT  &&
                                w_gs_index < 16'(AEM_N_STRIN_C)))) begin
                  status_q     <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0] <= 16'd12;
                end else if (hdr_q.command_type == CMD_SET_STREAM_FORMAT &&
                             !((w_gs_type == DESC_STREAM_OUTPUT)
                               ? w_out_fmt_ok : w_fmt_ok)) begin
                  status_q     <= STATUS_BAD_ARGUMENTS;
                  seg_len_q[0] <= 16'd12;
                end else begin
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  seg_kind_q[1] <= SEG_STORE;
                  seg_addr_q[1] <= (w_gs_type == DESC_STREAM_OUTPUT)
                                   ? WB_STROUT_FMT_ADDR_C[w_out_fidx]
                                   : WB_STRIN_FMT_ADDR_C[w_in_fidx];
                  seg_len_q[1]  <= 16'd8;
                  if (hdr_q.command_type == CMD_SET_STREAM_FORMAT) begin
                    wb_addr_q <= (w_gs_type == DESC_STREAM_OUTPUT)
                                 ? WB_STROUT_FMT_ADDR_C[w_out_fidx]
                                 : WB_STRIN_FMT_ADDR_C[w_in_fidx];
                    wb_len_q  <= 7'd8;
                    wb_src_q  <= 7'd6;
                    // live copy for the RX monitor's format compare
                    if (w_gs_type == DESC_STREAM_INPUT && w_gs_index == 16'd0)
                      fmt_in0_r <= {w_b6, w_b7, w_b8, w_b9,
                                    w_b10, w_b11, w_b12, w_b13};
`ifdef AEM_DYNMAP
                    //! the dynamic-map channel bound follows the CURRENT
                    //! format of THIS Stream Input (Milan 5.3.10.1); the
                    //! AAF channels_per_frame field is format[31:22]
                    if (w_gs_type == DESC_STREAM_INPUT &&
                        w_gs_index < 16'(AEM_DMAP_NSTRIN_C)) begin
                      dm_sch_r[w_dm_fidx] <= {w_b10, w_b11[7:6]};
                      //! a SHRINK orphans every mapping at or above the new
                      //! count: sweep them out so 5.3.10.1 holds for the new
                      //! format too (see the dmp_* declarations)
                      if ({w_b10, w_b11[7:6]} < dm_sch_r[w_dm_fidx]) begin
                        dmp_sidx_q <= w_dm_fidx;
                        dmp_ch_q   <= {w_b10, w_b11[7:6]};
                        dmp_key_r  <= 7'd0;
                        state_r    <= DMAP_PRUNE_S;
                      end
                    end
                    //! NO talker-side follower/prune: w_out_fmt_ok accepts
                    //! ONLY the declared format (FR-STR-03 wire truth - the
                    //! framer's channel count is an elaboration constant),
                    //! so a Stream Output's format can never shrink and the
                    //! output maps' channel bound stays AEM_ODMAP_SCH_C
`endif
                  end
                end
`else
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
`ifdef AEM_DYNMAP
                    //! see above: 5.3.10.1 channel bound per Stream Input,
                    //! and the same shrink prune
                    if (w_gs_type == DESC_STREAM_INPUT &&
                        w_gs_index < 16'(AEM_DMAP_NSTRIN_C)) begin
                      dm_sch_r[w_dm_fidx] <= {w_b10, w_b11[7:6]};
                      if ({w_b10, w_b11[7:6]} < dm_sch_r[w_dm_fidx]) begin
                        dmp_sidx_q <= w_dm_fidx;
                        dmp_ch_q   <= {w_b10, w_b11[7:6]};
                        dmp_key_r  <= 7'd0;
                        state_r    <= DMAP_PRUNE_S;
                      end
                    end
`endif
                  end
                end
`endif
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
              //
              // DEFECT D2, silicon 2026-07-27 gw 0x0001_0016 — THE PAYLOAD IS
              // 56 BYTES ON EVERY STATUS, not only on SUCCESS. This arm used
              // to answer NO_SUCH_DESCRIPTOR with cdl 16 (a 4-byte payload),
              // and Hive logged "Received an invalid non-success
              // GET_STREAM_INFO AEM response (Incorrect payload size)" 15
              // times, continuing only because it was built with
              // IGNORE_INVALID_NON_SUCCESS_AEM_RESPONSES; a strict controller
              // DROPS the frame and the entity looks dead, not incomplete.
              //
              // THE RULE, taken from the controller stack that enforces it
              // rather than from our own behaviour — L-Acoustics avdecc
              // src/protocol/protocolAemPayloads.cpp checkResponsePayload(),
              // the function that raises exactly that log line:
              //   status == NOT_IMPLEMENTED -> the response REFLECTS THE
              //     COMMAND (command payload length);
              //   ANY other status, success or error -> the response carries
              //     the FULL response payload for that command
              //     (>= the clause-defined response length).
              // Its per-command size constants carry the clause: GET_STREAM_
              // INFO Response = IEEE 1722.1-2013/-2021 §7.4.16.2 (48 B at
              // -2013, 84 B at -2021) and Milan 1.2 §7.3.10 = 56 B, which is
              // the size we serve. §7.4.16.2 defines ONE response message
              // format for this command and defines no truncated error
              // variant. NOTE: the IEEE and Milan texts themselves are NOT in
              // this repo (paywalled; docs/traceability/ieee1722_1-2021.md is
              // our own paraphrase), so the SENTENCE stating the size rule is
              // not quoted here — what is quoted is the clause that fixes the
              // response format plus the reference implementation's check.
              // Calibrated against the negative control: the Milan-validated
              // reference device answers a non-existent descriptor with 68
              // bytes, and Hive accepts it. "A non-success response echoes
              // the COMMAND" was an earlier invention of ours, refuted by
              // that same device — it is true only for NOT_IMPLEMENTED.
              CMD_GET_STREAM_INFO: begin
                //! size first, unconditionally: every exit below is 68
                cdl_q         <= 11'd68;   // 12 + 4+4+8+40
                seg_kind_q[0] <= SEG_ECHO;  seg_addr_q[0] <= 16'd2;  seg_len_q[0] <= 16'd4;
                if (w_si_is_stream && acc_found) begin
                  // D1: served iff the DIRECTORY has it — the same oracle
                  // READ_DESCRIPTOR uses, so the two commands cannot
                  // disagree about which descriptors exist.
                  status_q      <= STATUS_SUCCESS;
                  seg_kind_q[1] <= SEG_CONST; seg_addr_q[1] <= 16'd0;  seg_len_q[1] <= 16'd4;
                  seg_kind_q[2] <= SEG_STORE;
                  seg_addr_q[2] <= acc_base + STREAM_CUR_FMT_OFF_C;
                  seg_len_q[2]  <= 16'd8;
                  seg_kind_q[3] <= SEG_CONST; seg_addr_q[3] <= 16'd8;  seg_len_q[3] <= 16'd40;
                  if (w_gs_type == DESC_STREAM_OUTPUT) begin
                    // flags + live 40-byte tail. stream_id = {mac, index}
                    // and dest_mac = MAAP base + index: the SAME pair the
                    // ACMP responder hands a listener for talker_unique_id
                    // = index (the previous entity_id here could never
                    // match the stream; a fixed index 0 could not either
                    // once the board shipped 8 sources).
                    load_stream_info_consts(w_gs_index, w_out_dmac,
                                            w_gs_pres);
                  end else begin
                    // Listener sinks (reference populate_input_response):
                    // identity fields exposed unconditionally (*_VALID means
                    // "meaningful", zero is a valid value); CONNECTED/
                    // STREAMING_WAIT when bound; SRP failure flags from the
                    // TalkerFailed registrar; trailer = flags_ex REGISTERING
                    // + {pbsta, acmpsta}. Sink 0 = the ACMP listener SM, the
                    // CRF sink = its own bind record, every other sink reads
                    // unbound (no per-sink context here yet — see the task).
                    load_input_stream_info_consts(w_gs_index == 16'd0,
                                                  w_si_in_crf);
                  end
                end else begin
                  //! non-success: SAME 56-byte payload, echoed descriptor
                  //! type/index + a zero tail. Zero flags = nothing in the
                  //! block is claimed valid, which is the truthful reading
                  //! of a descriptor that does not exist.
                  status_q      <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_kind_q[1] <= SEG_NONE;  seg_addr_q[1] <= 16'd0;  seg_len_q[1] <= 16'd52;
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
                  //! writes THE ADDRESSED INDEX's pres_file_r entry — the
                  //! same entry SET/GET_MAX_TRANSIT_TIME and
                  //! GET_STREAM_INFO serve for that index (one source of
                  //! truth; this arm still accepts index 0 only, see the
                  //! index gate above)
                  status_q      <= STATUS_SUCCESS;
                  nochg_q       <= (w_si_lat == w_gs_pres);
                  for (int k = 0; k < int'(PRES_N_C); k++)
                    if (w_gs_index == 16'(k)) pres_file_r[k] <= w_si_lat;
                end
              end

              // -------------------------------------------------- //
              // START/STOP_STREAMING (Milan §5.4.2.19/20): Stream-INPUT-only
              // commands (the reference replies not-supported for outputs).
              // The input "started" level feeds the STREAMING_WAIT flag in
              // GET_STREAM_INFO; power-on started (no STREAMING_WAIT bind
              // plumbing yet — documented simplification).
              CMD_START_STREAMING, CMD_STOP_STREAMING: begin
                //! Milan 5.4.2.19/20: EACH Stream Input (AAF sinks plus the
                //! CRF input at index n_aaf_sinks_i) SHALL implement the
                //! pair; outputs answer NOT_SUPPORTED. The bound is derived
                //! from the shape, never a literal - the old `< 16'd2`
                //! matched the 1-sink TB shape by accident and refused
                //! inputs 2..8 on the 8x8 build (ax-rv32-e triage).
                if (w_gs_type == DESC_STREAM_INPUT
                    && w_gs_index <= n_aaf_sinks_i) begin
                  status_q     <= l0_reject_q ? l0_status_q : STATUS_SUCCESS;
                  seg_kind_q[0] <= SEG_ECHO; seg_addr_q[0] <= 16'd2; seg_len_q[0] <= 16'd4;
                  cdl_q        <= 11'd16;
                  if (!l0_reject_q)
                    started_in_r[w_gs_index[3:0]] <=
                        (hdr_q.command_type == CMD_START_STREAMING);
                end else begin
                  status_q <= STATUS_NOT_SUPPORTED;
                end
              end

              // -------------------------------------------------- //
              CMD_GET_AVB_INFO: begin
                //! CERT es-4.13: GET_AVB_INFO applies ONLY to AVB_INTERFACE.
                //! A wrong descriptor TYPE (e.g. CLOCK_DOMAIN, which exists)
                //! is NOT_IMPLEMENTED (the command is not implemented for
                //! that type); only a bad AVB_INTERFACE INDEX is
                //! NO_SUCH_DESCRIPTOR.
                if (w_gs_type != DESC_AVB_INTERFACE) begin
                  //! NOT_IMPLEMENTED is the ONE status that reflects the
                  //! COMMAND rather than the response (la_avdecc
                  //! checkResponsePayload; GET_AVB_INFO command payload =
                  //! type(2)+index(2) = 4 -> cdl 16). Correct as-is.
                  status_q     <= STATUS_NOT_IMPLEMENTED;
                  seg_len_q[0] <= 16'd4;
                  cdl_q        <= 11'd16;
                end else if (w_gs_index != 16'd0) begin
                  //! D2 same class as GET_STREAM_INFO: an ERROR status still
                  //! owes the full response. GET_AVB_INFO Response (1722.1
                  //! §7.4.40.2) = type(2)+index(2)+gptp_grandmaster_id(8)+
                  //! propagation_delay(4)+gptp_domain_number(1)+flags(1)+
                  //! msrp_mappings_count(2) = 20 B minimum + count x 8 B of
                  //! mappings (la_avdecc AecpAemGetAvbInfoResponsePayload
                  //! MinSize = 20). We answered 4. The error response now
                  //! carries the 20-byte minimum with count = 0 — shorter
                  //! than our 24-byte SUCCESS because the mapping list is
                  //! variable-length and declaring a mapping we then zero
                  //! would be a different lie; la_avdecc's rule is a
                  //! MINIMUM, not equality (GET_STREAM_INFO is fixed-size,
                  //! so there minimum and equality coincide).
                  status_q      <= STATUS_NO_SUCH_DESCRIPTOR;
                  seg_len_q[0]  <= 16'd4;
                  seg_kind_q[1] <= SEG_NONE; seg_addr_q[1] <= 16'd0; seg_len_q[1] <= 16'd16;
                  cdl_q         <= 11'd32;   // 12 + 4 + 16
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
                  //! flags (1722.1-2021 7.4.40.2): AS_CAPABLE (0x01, proxied
                  //! by a nonzero measured pdelay = the exchange works) |
                  //! GPTP_ENABLED (0x02) | SRP_ENABLED (0x04)
                  const_q[13] <= {5'b0, 1'b1, 1'b1, |pdelay_ns_i};
                  //! msrp_mappings: ONE entry mirroring our MSRP Domain
                  //! declaration {SRclassID 6 = class A, priority 3, VID}
                  //! (Hive's SRP domain panel; count 0 was the gap)
                  const_q[14] <= 8'h00; const_q[15] <= 8'h01;
                  const_q[16] <= 8'h06;                // traffic_class = A
                  const_q[17] <= 8'h03;                // priority
                  const_q[18] <= {4'h0, srp_domain_vid_i[11:8]};
                  const_q[19] <= srp_domain_vid_i[7:0];
                  seg_len_q[1] <= 16'd20;
                  cdl_q <= 11'd36;   // 12 + 4 + 16 + 4 (one mapping)
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
                if (w_gs_type == DESC_STREAM_OUTPUT && acc_found) begin
                  //! Milan Table 5.17, per 5.4.2.25 "implement and return"
                  //! FOR EACH Stream Output: every directory-served index
                  //! (the CRF Media Clock Output included) answers its own
                  //! KL_talker_diag_ctx context - interval-based, reset-on-
                  //! start Table 5.4 semantics. Until 2026-07-28 only index
                  //! 0 answered, its TS_UNCERTAIN bytes were constant zero
                  //! under a mask that claimed them (the R5 lie), and its
                  //! FRAMES_TX served the raw frame total where the clause
                  //! defines a per-interval count - 8000x off while
                  //! streaming.
                  status_q   <= STATUS_SUCCESS;
                  const_q[3] <= 8'h1F;   // START|STOP|MEDIA_RESET|TS_UNC|FRAMES_TX
                  for (int k = 0; k < 4; k++) begin
                    const_q[4+k]  <= tkdiag_cnt_i[0*32 + 8*(3-k) +: 8]; // bit0 START
                    const_q[8+k]  <= tkdiag_cnt_i[1*32 + 8*(3-k) +: 8]; // bit1 STOP
                    const_q[12+k] <= tkdiag_cnt_i[2*32 + 8*(3-k) +: 8]; // bit2 MR
                    const_q[16+k] <= tkdiag_cnt_i[3*32 + 8*(3-k) +: 8]; // bit3 TU
                    const_q[20+k] <= tkdiag_cnt_i[4*32 + 8*(3-k) +: 8]; // bit4 FTX
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
                end else if (w_gs_type == DESC_STREAM_INPUT && acc_found
                             && w_gs_index < n_aaf_sinks_i) begin
                  // EVERY AAF sink: its own live monitor context out of the
                  // all-stream mirror (Milan Table 5.16, per 5.4.2.25).
                  // Sink 1 used to serve this full mask over constant
                  // zeros; sinks >= 2 fell to the empty-mask arm below.
                  status_q     <= STATUS_SUCCESS;
                  seg_len_q[1] <= 16'd52;
                  seg_len_q[2] <= 16'd80;
                  load_input_counters_consts;
                end else if (w_gs_type == DESC_STREAM_INPUT && acc_found) begin
                  //! The CRF Media Clock Input (index >= n_aaf_sinks_i):
                  //! it answered SUCCESS + the truthful EMPTY mask until
                  //! 2026-07-29, but Milan 5.3.8.10 keeps counters "for
                  //! each Stream Input" with no CRF exemption, and
                  //! la_avdecc's per-enumeration mandatory-set check
                  //! ((mask & 0xF3F) == 0xF3F) dropped the Milan badge on
                  //! it. It now serves the mandatory ten out of the
                  //! KL_crf_rx sink engine (the 0x738 CSR group's own
                  //! counters), advertised-zero where the engine keeps no
                  //! tally - see load_crf_input_counters_consts.
                  status_q     <= STATUS_SUCCESS;
                  seg_len_q[1] <= 16'd52;
                  seg_len_q[2] <= 16'd80;
                  load_crf_input_counters_consts;
                end else if (w_gs_type == DESC_ENTITY && w_gs_index == 16'd0) begin
                  //! ENTITY GET_COUNTERS -> SUCCESS + EMPTY valid mask:
                  //! 1722.1-2021 DEFINES entity-level counters (la_avdecc
                  //! models EntityCounters first-class and Hive queries it
                  //! during enumeration - BAD_ARGUMENTS makes it log
                  //! 'values deemed bad', user-caught 2026-07-20). We
                  //! implement none -> empty mask, full-size payload (the
                  //! 07-11 field report: size matters on every status).
                  status_q <= STATUS_SUCCESS;
                end else if (acc_found) begin
                  status_q <= STATUS_BAD_ARGUMENTS;      // descriptor w/o counters
                end else begin
                  status_q <= STATUS_NO_SUCH_DESCRIPTOR;
                end
              end

              // -------------------------------------------------- //
              // GET_DYNAMIC_INFO (1722.1-2021 7.4.76; Milan 5.4.2.29
              // SHALL): the payload is an ARRAY of packed fixed-size GET
              // sub-commands; each is processed independently and answered
              // in the same record shape. Pass 1 (BSCAN_S) validates the
              // types (any non-fixed-size type = whole-command
              // BAD_ARGUMENTS, 7.4.76.2) and sizes the response, skipping
              // records that would overflow the AECPDU cap; pass 2 emits
              // record-by-record through the normal DECIDE/segment engine.
              CMD_GET_DYNAMIC_INFO: begin
                batch_q     <= 1'b1;
                bscan_ptr_q <= 9'd2;
                bscan_ph_r  <= 3'd0;
                bcdl_acc_q  <= 16'd0;
                bfit_map_q  <= 64'd0;
                bidx_q      <= 6'd0;
                bpay_end_q  <= 9'(16'd2 + 16'(hdr_q.control_data_length)
                                        - 16'd12);
                status_q    <= STATUS_SUCCESS;
                state_r     <= BSCAN_S;
              end

              // -------------------------------------------------- //
              // SET/GET_MAX_TRANSIT_TIME (1722.1-2021 §7.4.39 at the
              // la_avdecc-verified codes 0x4C/0x4D; payload = type(2)+
              // index(2)+max_transit_time u64 ns): reflects/updates THE
              // ADDRESSED INDEX's entry of the same per-STREAM_OUTPUT
              // presentation-offset file SET_STREAM_INFO(ACC_LAT) drives —
              // one source of truth per talker for its framer's timestamp
              // offset. The directory oracle (acc_found) bounds the index
              // exactly as GET_STREAM_INFO's D1 rule; until 2026-07-29 any
              // index != 0 was hard-rejected while READ_DESCRIPTOR served
              // it, and one global register backed every talker.
              CMD_SET_MAX_TRANSIT_TIME, CMD_GET_MAX_TRANSIT_TIME: begin
                cdl_q <= 11'd24;   // 12 + 12
                if (l0_reject_q) begin
                  status_q     <= l0_status_q;
                  seg_len_q[0] <= 16'd12;
                end else if (w_gs_type != DESC_STREAM_OUTPUT || !acc_found) begin
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
                    //! the addressed entry only — every other talker's
                    //! offset is untouched (per-index independence)
                    for (int k = 0; k < int'(PRES_N_C); k++)
                      if (w_gs_index == 16'(k))
                        pres_file_r[k] <= {w_b10, w_b11, w_b12, w_b13};
                  end else begin
                    const_q[4] <= w_gs_pres[31:24];
                    const_q[5] <= w_gs_pres[23:16];
                    const_q[6] <= w_gs_pres[15:8];
                    const_q[7] <= w_gs_pres[7:0];
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
                  //! 1722.1-2021 7.4.41.2: path_sequence = the pathSequence
                  //! of the LATEST Announce's PathTrace TLV = the clock
                  //! identities the Announce TRAVERSED: the grandmaster,
                  //! then each bridge. A receiving end-station is NOT in
                  //! the list (it only appends itself when retransmitting)
                  //! - the old entry 2 wrongly published OUR OWN identity
                  //! and omitted the switch (user-caught 2026-07-20).
                  //! Foreign GM through a bridge: [GM, parent-bridge];
                  //! foreign GM direct-wired (parent == GM or unknown):
                  //! [GM]; we are the GM: [self].
                  status_q   <= STATUS_SUCCESS;
                  if (w_gm_foreign) begin
                    if (as_parent_ckid_i != 64'd0 &&
                        as_parent_ckid_i != gptp_gm_id_i) begin
                      seg_len_q[1] <= 16'd18;
                      cdl_q        <= 11'd32;   // 12 + 4 + 16
                      const_q[1]   <= 8'h02;                  // count = 2
                      for (int k = 0; k < 8; k++)
                        const_q[2+k] <= gptp_gm_id_i[8*(7-k) +: 8];
                      for (int k = 0; k < 8; k++)
                        const_q[10+k] <= as_parent_ckid_i[8*(7-k) +: 8];
                    end else begin
                      const_q[1] <= 8'h01;                    // count = 1
                      for (int k = 0; k < 8; k++)
                        const_q[2+k] <= gptp_gm_id_i[8*(7-k) +: 8];
                    end
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
                    unsol_valid_r[s]  <= 1'b0;
                    unsol_pend_r[s]   <= 1'b0;
                    unsol_pend2_r[s]  <= 1'b0;
                    unsol_pend3_r[s]  <= 1'b0;
                    unsol_pend5_r[s]  <= '0;
                  end
                end
              end

              default: ;   // NOT_IMPLEMENTED echo (defaults above)
            endcase
          end
          end
        end

        // ---------------------------------------------------------- //
        WRITE_S: begin   // SET_* write-back (no-op when wb_len_q == 0);
                         // also the cycle where cum_q/pay_len_q settle
          if (batch_q) rec_hdr_q[4] <= {3'd0, status_q};
          if (wb_len_q == 7'd0) begin
            if (cum_done_q) state_r <= EMIT_ADDR_S;
          end else if (!wbp_r) begin
            wbp_r <= 1'b1;             // old byte read issued (w_wb_read)
          end else begin
            wbp_r      <= 1'b0;
            st_wr_o    <= 1'b1;
            st_waddr_o <= wb_addr_q + 16'(wb_cnt_r);
            st_wdata_o <= cbuf_rbyte_w;
            wb_used_q  <= 1'b1;
            if (st_byte_i != cbuf_rbyte_w)
              wb_diff_q <= 1'b1;
            if (wb_cnt_r == wb_len_q - 7'd1) begin
              wb_cnt_r <= 7'd0;
              wb_len_q <= 7'd0;
            end else begin
              wb_cnt_r <= wb_cnt_r + 7'd1;
            end
          end
        end

        // ---------------------------------------------------------- //
        // Byte engine, 3-cycle cadence:                                //
        //   EMIT_ADDR ph0: resolve the byte source; REGISTER the       //
        //                  store address (st_addr_q)                   //
        //   EMIT_ADDR ph1: issue the store read from the register      //
        //   EMIT_DATA:     capture the byte, feed the beat packer      //
        // ---------------------------------------------------------- //
        EMIT_ADDR_S: begin
          if (batch_q && fi_r == w_hdr_len + brec_base_q - 16'd8) begin
            //! next up: this record's 8-byte header
            bh_i_r  <= 3'd0;
            state_r <= RECHDR_EMIT_S;
          end else
          if (batch_q && fi_r == w_hdr_len + brec_base_q + brec_rlen_q) begin
            //! record data complete (frame end would have concluded in
            //! EMIT_DATA_S): advance to the next record
            brec_base_q <= brec_base_q + 16'd8 + brec_rlen_q;
            brec_ph_r   <= 3'd7;
            bsub_q      <= 1'b0;
            state_r     <= BREC_SETUP_S;
          end else if (!ea_ph_r) begin
          // Phase 0: resolve + REGISTER the byte source for fi_r AND the
          // store read address. Nothing is issued to the store this cycle -
          // the deep batch_q -> w_pi -> segment walk -> adder cone now
          // terminates in st_addr_q, never the BRAM address port.
          is_hdr_r     <= (fi_r < w_hdr_len);
          hdrbyte_r    <= hdr_byte(fi_r);
          emseg_kind_r <= seg_kind_q[w_seg];
          emseg_addr_r <= seg_addr_q[w_seg];
          emsoff_r     <= w_soff;
          st_addr_q    <= seg_addr_q[w_seg] + w_soff;
          ea_ph_r      <= 1'b1;
          end else begin
          // Phase 1: the store read issues from st_addr_q (w_emit_store)
          // and the ECHO read address is registered from the phase-0
          // resolution; both land their byte on EMIT_DATA_S, as the
          // combinational shape did.
          ec_addr_q <= w_eaddr;
          ea_ph_r <= 1'b0;
          state_r <= EMIT_DATA_S;
          end
        end

        EMIT_DATA_S: begin
          logic [7:0] b;
          if (is_hdr_r) begin
            b = hdrbyte_r;                    // registered header byte
          end else begin
            unique case (emseg_kind_r)        // registered segment select
              SEG_ECHO:  b = cbuf_rbyte_w;    // single-port read (w_eaddr)
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
        BSCAN_S: begin   // 0x4B pass 1: validate + size (7.4.76.2)
          if (!cap_done_q) begin
            // hold: the command frame is still streaming into cbuf
          end else if (bscan_ptr_q >= bpay_end_q) begin
            pay_len_q   <= bcdl_acc_q;
            bcdl_q      <= 11'(16'd12 + bcdl_acc_q);
            brec_ptr_q  <= 9'd2;
            brec_ph_r   <= 3'd0;
            bidx_q      <= 6'd0;
            brec_base_q <= 16'd8;   // record 0 data follows its header
            brec_rlen_q <= 16'd0;
            state_r     <= BREC_SETUP_S;
          end else begin
            unique case (bscan_ph_r)
              3'd0: begin
                bslh_r     <= cbuf_rbyte_w;
                bscan_ph_r <= 3'd1;
              end
              3'd1: begin
                brec_dlen_q <= {bslh_r, cbuf_rbyte_w};
                bscan_ph_r  <= 3'd2;
              end
              3'd2: begin
                bsch_r     <= 7'(cbuf_rbyte_w);
                bscan_ph_r <= 3'd3;
              end
              3'd3: begin
                //! capture ONLY (AX27 -1.98 cone split): the verdict math
                //! moves to phase 4 and runs from registers
                bsc_lo_q   <= cbuf_rbyte_w;
                bscan_ph_r <= 3'd4;
              end
              3'd4: begin
                //! record verdict forensics from the PHASE-CAPTURED bytes
                //! (single-port rework: no side reads; cmd-hi keeps 7 bits)
                bdbg0_q <= {bslh_r, brec_dlen_q[7:0],
                            {1'b0, bsch_r}, bsc_lo_q};
                bdbg1_q <= {1'b0, w_bscan_c, brec_dlen_q};
                bdbg2_q <= {7'd0, bscan_ptr_q, 7'd0, bpay_end_q};
                bscan_ph_r <= 3'd0;
                if (!batch_legal(w_bscan_c) ||
                    (16'({7'd0, bscan_ptr_q}) + 16'd8 + brec_dlen_q
                     > 16'({7'd0, bpay_end_q}))) begin
                  //! non-fixed-size type or truncated record: the WHOLE
                  //! command fails BAD_ARGUMENTS, request payload echoed
                  batch_q       <= 1'b0;
                  status_q      <= STATUS_BAD_ARGUMENTS;
                  seg_kind_q[0] <= SEG_ECHO; seg_addr_q[0] <= 16'd2;
                  seg_len_q[0]  <= 16'(hdr_q.control_data_length) - 16'd12;
                  cdl_q         <= hdr_q.control_data_length;
                  cum_done_q    <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
                  wb_len_q      <= 7'd0;
                  state_r       <= WRITE_S;
                end else begin
                  //! append if it fits the AECPDU cap (else skip, 7.4.76.1)
                  if (bcdl_acc_q + 16'd8 + w_bscan_rl <= 16'd494) begin
                    bcdl_acc_q         <= bcdl_acc_q + 16'd8 + w_bscan_rl;
                    bfit_map_q[bidx_q] <= 1'b1;
                  end
                  bidx_q      <= bidx_q + 6'd1;
                  bscan_ptr_q <= bscan_ptr_q + 9'(16'd8 + brec_dlen_q);
                end
              end
              default: bscan_ph_r <= 3'd0;
            endcase
          end
        end

        // ---------------------------------------------------------- //
        BREC_SETUP_S: begin   // 0x4B pass 2: parse/classify one record
          if (brec_ptr_q >= bpay_end_q) begin
            //! empty batch: bare 38-byte header response (cdl 12)
            cum_done_q <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
            wb_len_q   <= 7'd0;
            state_r    <= WRITE_S;
          end else begin
            unique case (brec_ph_r)
              3'd7: begin   //! advance past the completed/skipped record
                brec_ptr_q <= brec_ptr_q + 9'(16'd8 + brec_dlen_q);
                bidx_q     <= bidx_q + 6'd1;
                brec_ph_r  <= 3'd0;
              end
              3'd0: begin
                bslh_r    <= cbuf_rbyte_w;
                brec_ph_r <= 3'd1;
              end
              3'd1: begin
                brec_dlen_q <= {bslh_r, cbuf_rbyte_w};
                brec_ph_r   <= 3'd2;
              end
              3'd2: begin
                bsch_r    <= 7'(cbuf_rbyte_w);
                brec_ph_r <= 3'd3;
              end
              3'd3: begin
                //! capture ONLY (AX27 cone split, as in BSCAN phase 3)
                bsc_lo_q  <= cbuf_rbyte_w;
                brec_ph_r <= 3'd5;
              end
              3'd5: begin
                if (!bfit_map_q[bidx_q]) begin
                  brec_ph_r <= 3'd7;   //! over-cap record: skip
                end else begin
                  brec_cmd_q   <= w_brec_c;
                  brec_abase_q <= 16'({7'd0, brec_ptr_q}) + 16'd6;
                  rec_hdr_q[2] <= 8'h00; rec_hdr_q[3] <= 8'h00;
                  rec_hdr_q[5] <= 8'h00;
                  rec_hdr_q[6] <= {1'b0, w_brec_c[14:8]};
                  rec_hdr_q[7] <= w_brec_c[7:0];
                  if (w_brec_rl != 16'd0) begin
                    //! implemented GET: dispatch through DECIDE_S
                    brec_rlen_q  <= w_brec_rl;
                    rec_hdr_q[0] <= w_brec_rl[15:8];
                    rec_hdr_q[1] <= w_brec_rl[7:0];
                    brec_ph_r    <= 3'd4;
                  end else begin
                    //! fixed-size but unimplemented: NOT_SUPPORTED with
                    //! the request data echoed back (7.4.76.1 example)
                    brec_rlen_q  <= brec_dlen_q;
                    rec_hdr_q[0] <= brec_dlen_q[15:8];
                    rec_hdr_q[1] <= brec_dlen_q[7:0];
                    status_q     <= STATUS_NOT_SUPPORTED;
                    for (int k = 0; k < SEGN_C; k++) begin
                      seg_kind_q[k] <= SEG_NONE;
                      seg_addr_q[k] <= 16'd0; seg_len_q[k] <= 16'd0;
                    end
                    seg_kind_q[0] <= SEG_ECHO; seg_addr_q[0] <= 16'd2;
                    seg_len_q[0]  <= brec_dlen_q;
                    cum_done_q <= 1'b0; cum_ph_r <= 2'd0; cum_acc_r <= 16'd0;
                    wb_len_q   <= 7'd0;
                    brec_ph_r  <= 3'd0;
                    state_r    <= WRITE_S;
                  end
                end
              end
              3'd4: begin
                //! load the record's virtual arg window: virtual byte 0-1 =
                //! its command_type (mirroring the classic frame layout),
                //! byte 2.. = its command data -> w_b2/w_gs_* line up.
                //! SERIALIZED to one byte/cycle through the single cbuf
                //! read port (16 cycles; the AECP budget is milliseconds)
                if (!cwld_r[3]) begin
                  cw0_r[8*(7-cwld_r[2:0]) +: 8] <= cbuf_rbyte_w;
                end
                else begin
                  cw1_r[8*(7-cwld_r[2:0]) +: 8] <= cbuf_rbyte_w;
                end
                if (cwld_r == 4'd15) begin
                  cwld_r    <= 4'd0;
                  bsub_q    <= 1'b1;
                  brec_ph_r <= 3'd0;
                  state_r   <= DECIDE_S;
                end
                else begin
                  cwld_r <= cwld_r + 4'd1;
                end
              end
              default: brec_ph_r <= 3'd0;
            endcase
          end
        end

        // ---------------------------------------------------------- //
        RECHDR_EMIT_S: begin   // 0x4B pass 2: pack the 8-byte record header
          if (!beat_pend_r) begin
            pack_r[8*pack_n_r +: 8] <= rec_hdr_q[bh_i_r];
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
              fi_r <= fi_r + 16'd1;
              if (bh_i_r == 3'd7) state_r <= EMIT_ADDR_S;
              bh_i_r <= bh_i_r + 3'd1;
            end
          end
        end

`ifdef AEM_DYNMAP
        // ---------------------------------------------------------- //
        DMAP_SCAN_S: begin   //! ADD/REMOVE mapping walk (BSCAN pattern:
                             //! one byte/cycle through the single cbuf
                             //! port, verdict from registers only)
                             //! phases 0-7 field bytes · 8 KEY RESOLVE ·
                             //! 9 verdict
          if (dmph_r < 4'd8) begin
            unique case (dmph_r[2:0])
              3'd0: dm_hi_r <= cbuf_rbyte_w;
              3'd1: dm_si_q <= {dm_hi_r, cbuf_rbyte_w};
              3'd2: dm_hi_r <= cbuf_rbyte_w;
              3'd3: dm_sc_q <= {dm_hi_r, cbuf_rbyte_w};
              3'd4: dm_hi_r <= cbuf_rbyte_w;
              3'd5: dm_co_q <= {dm_hi_r, cbuf_rbyte_w};
              3'd6: dm_hi_r <= cbuf_rbyte_w;
              default: dm_cc_q <= {dm_hi_r, cbuf_rbyte_w};
            endcase
            dmph_r <= dmph_r + 4'd1;
          end else if (dmph_r == 4'd8) begin
            //! Phase 8 - KEY RESOLVE. The record's four fields are all
            //! captured by now, so every key and every value the verdict
            //! reaches THROUGH a key is resolved here and nowhere else.
            //! The reads are of the store as it stands BEFORE this
            //! record's own commit, which is what both verdicts mean.
            dmk_key_q    <= w_dm_key;
            dmk_keyok_q  <= w_dm_key_ok;
            dmk_physok_q <= w_dm_phys_ok;
            dmk_siin_q   <= w_dm_si_in;
            dmk_saaf_q   <= AEM_DMAP_SAAF_C[w_dm_sidx];
            dmk_sch_q    <= dm_sch_r[w_dm_sidx];
            dmk_v_q      <= dmap_v_r [w_dm_key];
            dmk_ch_q     <= dmap_ch_r[w_dm_key];
            dmk_si_q     <= dmap_si_r[w_dm_key];
            dmk_claim_q  <= dmap_claim_r[w_dm_key];
`ifdef AEM_ODYNMAP
            odk_t_q      <= w_od_t;      //! address = this record's cluster
            odk_coq_ok_q <= w_od_co_ok;
            odk_key_q    <= w_od_key;
            odk_v_q      <= ov_r [w_od_key];
            odk_co_q     <= oco_r[w_od_key];
            //! the sibling as this command LEAVES it - the post-state rule 3
            //! judges and the half-enable the RMW writes
            odk_sv_q     <= w_od_sv;
            odk_sco_q    <= w_od_sco;
`endif
            dmph_r <= 4'd9;
`ifdef AEM_ODYNMAP
          end else if (dm_out_q && dmph_r == 4'd9) begin
            //! Phase 9 - the OUTPUT walk's second resolve: the same source
            //! table, now addressed by the sibling's post-command cluster
            //! (registered above). Its own phase because chaining
            //! oco_r[sibling] -> AEM_ODMAP_CSRC_C[] inside one cycle is the
            //! exact two-deep array read phase 8 exists to have avoided.
            odk_ts_q <= w_od_t;
            dmph_r   <= 4'd10;
`endif
          end else begin
            dmph_r <= 4'd0;
`ifdef AEM_ODYNMAP
            if (dm_out_q) begin
              //! OUTPUT-port walk, THREE passes over the same records (see
              //! the vendor rules at the odmap declarations):
              //!   0  judge each record ALONE + record what it intends
              //!   1  judge each record against the command's POST state
              //!   2  commit: store key + one READ-MODIFY-WRITE of its slot
              //! Both judging passes run before anything is committed, so
              //! 7.4.45.1/7.4.46.1's "none of the mappings are added /
              //! removed" holds however late the offending record sits.
              if (od_pass_q == 2'd0) begin
                if (dm_remove_q ? !w_od_rm_hit
                                : (!w_od_rec_ok || oclaim_r[dm_sc_q[2:0]]))
                  begin
                  status_q <= STATUS_BAD_ARGUMENTS;
                  state_r  <= WRITE_S;
                end else begin
                  //! REMOVE claims too - not to reject a duplicate (Milan
                  //! 5.4.2.28 says ignore those) but so pass 1 and the RMW
                  //! know this channel ends up UNMAPPED
                  oclaim_r[dm_sc_q[2:0]]   <= 1'b1;
                  opend_co_r[dm_sc_q[2:0]] <= dm_co_q[4:0];
                  if (dmi_r == dmn_q - 6'd1) begin
                    dmi_r     <= 6'd0;
                    od_pass_q <= 2'd1;
                  end else begin
                    dmi_r <= dmi_r + 6'd1;
                  end
                end
              end else if (od_pass_q == 2'd1) begin
                //! REMOVE cannot break rule 3: dropping a channel only
                //! clears a half-enable, it never re-points the slot
                if (!dm_remove_q && !w_od_sib_ok) begin
                  status_q <= STATUS_BAD_ARGUMENTS;
                  state_r  <= WRITE_S;
                end else if (dmi_r == dmn_q - 6'd1) begin
                  dmi_r     <= 6'd0;
                  od_pass_q <= 2'd2;
                end else begin
                  dmi_r <= dmi_r + 6'd1;
                end
              end else begin
                //! COMMIT. One record = one channel = one half of one slot.
                //! The slot word is rebuilt from this record's source and
                //! the sibling's POST-command arming, so every record that
                //! touches a slot writes the SAME final word - the RMW
                //! composes within one command whatever order they arrive.
                if (!dm_remove_q) begin
                  ov_r [odk_key_q] <= 1'b1;
                  oco_r[odk_key_q] <= dm_co_q[4:0];
                  if (w_od_chg) dmap_diff_q <= 1'b1;
                  odmap_wr_p_o    <= 1'b1;
                  odmap_wr_slot_o <= od_slotb_q + 5'(dm_sc_q[3:1]);
                  odmap_wr_word_o <= {w_od_half_add, odk_t_q[7:4], 1'b1,
                                      odk_t_q[10:8], odk_t_q[3:0]};
                end else begin
                  ov_r[odk_key_q] <= 1'b0;
                  dmap_diff_q     <= 1'b1;
                  odmap_wr_p_o    <= 1'b1;
                  odmap_wr_slot_o <= od_slotb_q + 5'(dm_sc_q[3:1]);
                  //! the sibling keeps the slot's source; an emptied slot
                  //! goes fully quiet (en=0), never "enabled with no half"
                  odmap_wr_word_o <= odk_sv_q
                      ? {w_od_half_rm, odk_t_q[7:4], 1'b1,
                         odk_t_q[10:8], odk_t_q[3:0]}
                      : 14'h0000;
                end
                if (dmi_r == dmn_q - 6'd1) begin
                  nochg_q <= !(dmap_diff_q ||
                               (dm_remove_q ? 1'b1 : w_od_chg));
                  state_r <= WRITE_S;
                end else begin
                  dmi_r <= dmi_r + 6'd1;
                end
              end
            end else
`endif
            if (!dm_commit_q) begin
              //! Validate pass — BOTH directions run it, because both
              //! clauses are all-or-nothing in the same words:
              //!   7.4.45.1 / Milan 5.4.2.27 (ADD)    "In this case, no
              //!     mapping shall be added."
              //!   7.4.46.1 (REMOVE)                  "If any of the
              //!     mappings in the command are invalid or not present
              //!     then the command shall fail with a BAD_ARGUMENTS
              //!     status and none of the mappings shall be removed."
              //! ADD additionally claims each key so the same key twice in
              //! one command is the mandated same-cluster-channel conflict
              //! reject (identical duplicates rejected too — a vendor rule
              //! 7.4.45.1 allows; nothing mandates accepting them).
              //! REMOVE deliberately does NOT claim: Milan 5.4.2.28 says
              //! duplicates there "shall be ignored", and since nothing has
              //! been committed yet every copy still sees its entry.
              if (dm_remove_q ? w_dm_rm_bad : w_dm_add_bad) begin
                status_q <= STATUS_BAD_ARGUMENTS;
                state_r  <= WRITE_S;
              end else begin
                if (!dm_remove_q) dmap_claim_r[dmk_key_q] <= 1'b1;
                if (dmi_r == dmn_q - 6'd1) begin
                  dmi_r       <= 6'd0;
                  dm_commit_q <= 1'b1;
                end else begin
                  dmi_r <= dmi_r + 6'd1;
                end
              end
            end else begin
              //! commit pass: ADD writes/replaces the key's entry (replace
              //! = the 5.4.2.27 accept-and-replace option; the extra
              //! REMOVE unsol is a "may" — not sent); REMOVE clears an
              //! exact match and IGNORES everything else (5.4.2.28
              //! duplicate rule). Replays re-run this idempotently.
              if (!dm_remove_q) begin
                dmap_v_r [dmk_key_q] <= 1'b1;
                dmap_ch_r[dmk_key_q] <= dm_sc_q[3:0];
                dmap_si_r[dmk_key_q] <= dm_si_q[2:0];
                if (w_dm_add_chg) dmap_diff_q <= 1'b1;
                //! fabric mirror: one render-map write per accepted record,
                //! addressed by the GLOBAL cluster key = the physical
                //! render channel (docs/CHMAP64_AEM_BINDING.md)
                dmap_wr_p_o    <= 1'b1;
                dmap_wr_addr_o <= 6'(dmk_key_q);
                dmap_wr_word_o <= {1'b1, 1'b0, dm_si_q[2:0], dm_sc_q[2:0]};
              end else if (w_dm_rm_hit) begin
                dmap_v_r[dmk_key_q] <= 1'b0;
                dmap_diff_q <= 1'b1;
                dmap_wr_p_o    <= 1'b1;
                dmap_wr_addr_o <= 6'(dmk_key_q);
                dmap_wr_word_o <= 8'h00;
              end
              if (dmi_r == dmn_q - 6'd1) begin
                //! no state change -> suppress the u=1 replay (the
                //! generalized nochg rule; this-cycle term included)
                nochg_q <= !(dmap_diff_q ||
                             (dm_remove_q ? w_dm_rm_hit : w_dm_add_chg));
                state_r <= WRITE_S;
              end else begin
                dmi_r <= dmi_r + 6'd1;
              end
            end
          end
        end

        // ---------------------------------------------------------- //
        DMAP_GET_S: begin   //! GET_AUDIO_MAP page scan: one key/cycle out
                            //! of the flop store into the const scratch
`ifdef AEM_ODYNMAP
          if (dm_out_q) begin
            //! OUTPUT-port page: rows come from the ov/oco store; the
            //! stream_index is the port's own stream, the stream channel
            //! is the key's low bits, cluster_channel 0 (mono clusters)
            if (dmg_key_r >= dmg_end_r ||
                dmg_key_r >= 7'(AEM_ODMAP_KEYS_C)) begin
              const_q[0] <= 8'h00; const_q[1] <= dmg_nmaps_q;
              const_q[2] <= 8'h00; const_q[3] <= {4'd0, dmg_n_r};
              const_q[4] <= 8'h00; const_q[5] <= 8'h00;
              seg_len_q[1] <= 16'd6 + {9'd0, dmg_n_r, 3'd0};
              cdl_q        <= 11'd24 + {4'd0, dmg_n_r, 3'd0};
              state_r      <= WRITE_S;
            end else begin
              if (ov_r[dmg_key_r[ODMAP_KW_C-1:0]]) begin
                const_q[w_dmg_base + 7'd0] <= 8'h00;
                const_q[w_dmg_base + 7'd1] <= {4'd0, od_pstr_q};
                const_q[w_dmg_base + 7'd2] <= 8'h00;
                const_q[w_dmg_base + 7'd3] <= {5'd0, dmg_key_r[2:0]};
                const_q[w_dmg_base + 7'd4] <= 8'h00;
                const_q[w_dmg_base + 7'd5] <=
                    {3'd0, oco_r[dmg_key_r[ODMAP_KW_C-1:0]]};
                const_q[w_dmg_base + 7'd6] <= 8'h00;
                const_q[w_dmg_base + 7'd7] <= 8'h00;
                dmg_n_r <= dmg_n_r + 4'd1;
              end
              dmg_key_r <= dmg_key_r + 7'd1;
            end
          end else
`endif
          if (dmg_key_r >= dmg_end_r || dmg_key_r >= 7'(AEM_DMAP_KEYS_C)) begin
            //! finalize now that the page's live count is known.
            //! number_of_maps is ALWAYS the addressed port's fixed
            //! partition count, no matter the mapping count (5.4.2.26).
            const_q[0] <= 8'h00; const_q[1] <= dmg_nmaps_q;
            const_q[2] <= 8'h00; const_q[3] <= {4'd0, dmg_n_r};
            const_q[4] <= 8'h00; const_q[5] <= 8'h00;
            seg_len_q[1] <= 16'd6 + {9'd0, dmg_n_r, 3'd0};
            cdl_q        <= 11'd24 + {4'd0, dmg_n_r, 3'd0};
            state_r      <= WRITE_S;
          end else begin
            if (dmap_v_r[dmg_key_r[DMAP_KW_C-1:0]]) begin
              //! Table 7-33 row: stream_index, stream_channel,
              //! cluster_offset = key - the port's base_cluster (7.2.19
              //! offsets are PORT-RELATIVE), cluster_channel 0
              const_q[w_dmg_base + 7'd0] <= 8'h00;
              const_q[w_dmg_base + 7'd1] <=
                  {5'd0, dmap_si_r[dmg_key_r[DMAP_KW_C-1:0]]};
              const_q[w_dmg_base + 7'd2] <= 8'h00;
              const_q[w_dmg_base + 7'd3] <=
                  {4'd0, dmap_ch_r[dmg_key_r[DMAP_KW_C-1:0]]};
              const_q[w_dmg_base + 7'd4] <= 8'h00;
              const_q[w_dmg_base + 7'd5] <= {1'b0, dmg_key_r - dmg_base_r};
              const_q[w_dmg_base + 7'd6] <= 8'h00;
              const_q[w_dmg_base + 7'd7] <= 8'h00;
              dmg_n_r <= dmg_n_r + 4'd1;
            end
            dmg_key_r <= dmg_key_r + 7'd1;
          end
        end

        // ---------------------------------------------------------- //
        DMAP_PRUNE_S: begin  //! Milan 5.3.10.1 after a SET_STREAM_FORMAT
                             //! SHRINK: one key per cycle, withdrawing every
                             //! mapping of the reformatted Stream Input whose
                             //! stream_channel no longer exists. One key per
                             //! cycle because the fabric mirror is a
                             //! one-write-per-cycle port; the response plan
                             //! was already latched at dispatch, so WRITE_S
                             //! still emits the SET_STREAM_FORMAT response.
          if (dmp_key_r >= 7'(AEM_DMAP_KEYS_C)) begin
            state_r <= WRITE_S;
          end else begin
            if (dmap_v_r[dmp_key_r[DMAP_KW_C-1:0]] &&
                (dmap_si_r[dmp_key_r[DMAP_KW_C-1:0]] ==
                 3'(dmp_sidx_q)) &&
                ({6'd0, dmap_ch_r[dmp_key_r[DMAP_KW_C-1:0]]} >= dmp_ch_q)) begin
              dmap_v_r[dmp_key_r[DMAP_KW_C-1:0]] <= 1'b0;
              //! withdraw it from the render crossbar too, or the map word
              //! keeps de-interleaving a wire channel that no longer exists
              dmap_wr_p_o    <= 1'b1;
              dmap_wr_addr_o <= 6'(dmp_key_r);
              dmap_wr_word_o <= 8'h00;
            end
            dmp_key_r <= dmp_key_r + 7'd1;
          end
        end
`endif

        // ---------------------------------------------------------- //
        CONCLUDE_S: begin   // wait for the final beat to drain, then clean up
          if (!beat_pend_r) begin   // top-level handshake sent the last beat
            evt_resp_o  <= 1'b1;
            // a SUCCESS state-changing SET: replay its response (u=1) to
            // every registered controller except the originator
            if (!unsol_frame_r && !vu_q && status_q == STATUS_SUCCESS &&
                is_replay_cmd(hdr_q.command_type) && !nochg_q &&
                !(wb_used_q && !wb_diff_q))
              for (int sl = 0; sl < UNSOL_SLOTS_C; sl++)
                if (unsol_valid_r[sl] &&
                    unsol_eid_r[sl] != hdr_q.controller_entity_id)
                  unsol_pend4_r[sl] <= 1'b1;
            // pushes are self-generated: there is no ingress meta to pop
            if (!unsol_frame_r) pop_pend_r <= pop_pend_r + 2'd1;
            unsol_frame_r <= 1'b0;
            batch_q     <= 1'b0;
            bsub_q      <= 1'b0;
            fi_r        <= 16'd0;
            state_r     <= IDLE_S;
          end
        end

        default: state_r <= IDLE_S;
      endcase
    end
  end

  //! capture RAM write: OWN sync-only process (no async-reset term) so
  //! Vivado infers a true distributed RAM. See the note at the capture
  //! block in `engine` for the silicon mismatch this style prevents.
  always_ff @(posedge clk_i) begin : cbuf_write
    if (w_cap_hs && beat_r >= 7'd3 && beat_r < 7'd67)
      cbuf_r[6'(beat_r - 7'd3)] <= s_axis_tdata;
  end : cbuf_write

  assign bdbg0_o = bdbg0_q;
  assign bdbg1_o = bdbg1_q;
  assign bdbg2_o = bdbg2_q;

  // ------------------------------------------------------------------ //
  // Dynamic-map render taps: GLOBAL cluster keys 0/1 ARE the DAC pair    //
  // (the first input port's first two clusters); the full N-port picture //
  // rides dmap_wr_* into the render map RAM. The playback walker         //
  // generalization that CONSUMES the taps                                //
  // is the documented follow-up (docs/MILAN_COMPLIANCE_GAPS.md §1).      //
  // Static shapes export the wire-truth defaults with en=0.              //
  // ------------------------------------------------------------------ //
`ifdef AEM_DYNMAP
  localparam int unsigned DMAP_RK_C = (AEM_DMAP_KEYS_C > 1) ? 1 : 0;
  assign dmap_l_en_o = dmap_v_r[0];
  assign dmap_l_ch_o = dmap_ch_r[0];
  assign dmap_r_en_o = (AEM_DMAP_KEYS_C > 1) ? dmap_v_r[DMAP_RK_C] : 1'b0;
  assign dmap_r_ch_o = dmap_ch_r[DMAP_RK_C];
`else
  always_comb begin
    dmap_wr_p_o    = 1'b0;
    dmap_wr_addr_o = 6'd0;
    dmap_wr_word_o = 8'd0;
  end
  assign dmap_l_en_o = 1'b0;
  assign dmap_l_ch_o = 4'd0;   //! wire-truth default: stream ch0 -> L
  assign dmap_r_en_o = 1'b0;
  assign dmap_r_ch_o = 4'd1;   //! wire-truth default: stream ch1 -> R
`endif

  // verilator lint_off UNUSED
  wire unused_ok = &{1'b0, s_axis_tkeep, emit_byte_r, l0_state_i.acquired,
                     l0_state_i.acquiring_controller_id, l0_state_i.entity_id,
                     l0_state_i.locked, req_src_mac_i};
  // verilator lint_on  UNUSED

endmodule

`default_nettype wire
