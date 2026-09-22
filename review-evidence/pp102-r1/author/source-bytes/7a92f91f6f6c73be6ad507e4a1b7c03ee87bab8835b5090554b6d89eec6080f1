/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : protocol_processor_top.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/01 §7 F01.5, 02 §2-§6, 03 in full,
//                 04/05/10 engines, 07 §2/§5, 08 §4-§5)
//
//  Description : The processor top — ONE MAC trunk byte stream in, ONE MAC
//                byte stream out, everything of the landed tree wired
//                between them:
//                  RX: trunk -> KL_pp_rx_validator (+ KL_pp_rx_slots pool)
//                      -> parsed-header beat -> KL_pp_normalizer ->
//                      KL_pp_dispatch -> {KL_adp_engine, KL_pp_acmp_listener +
//                      KL_acmp_talker by message-type steer, AECP pop as a
//                      TOP-LEVEL face for the P4 uCPU}.
//                  V9 seam: the validator's MRP pass-through emits the whole
//                      frame from DA byte 0; KL_srp_top wants
//                      ProtocolVersion-first — KL_mrp_strip drops the 14
//                      header bytes, derives the msrp/mvrp select from the
//                      stripped EtherType and buffers P-MRPDU-QUEUE-BYTES.
//                  TX: engine faces -> KL_pp_tx_slots (via the pool-access
//                      arbiter below) -> KL_pp_tx_arbiter -> the ACMP
//                      Ethernet-header prepend shim -> MAC out.
//                  Services: KL_pp_timer_service (arm-port priority mux),
//                      KL_pp_prng (draw-port owner mux), KL_pp_scoreboard,
//                      KL_pp_event_router, KL_pp_originator, KL_pp_trace_ring,
//                      KL_pp_side_port, KL_acmp_nvm_shadow -> KL_pp_nvm_port.
//                  The F02.10 class-D status dictionary is aggregated into
//                      the side-port snapshot window (0x20000).
//
//                Seams recorded as glue here (each bannered at its block):
//                  - hdr-beat latch: the validator's one-cycle parsed-header
//                    beat vs the normalizer's held-until-ready producer face;
//                  - ACMP Ethernet prepend: KL_pp_acmp_listener (and the talker
//                    response builder) commit 56-byte ACMPDUs while ADP/SRP
//                    commit whole wire frames — TX lanes 2/5 get the 14-byte
//                    header injected on the way to the MAC;
//                  - dispatch-ROM stub: hazard class answered from a
//                    protocol-keyed default until the P4 dispatch ROM lands;
//                  - TX-pool access arbiter: one alloc+write port, four
//                    builders — ownership from alloc grant to commit, the
//                    engines' own alloc retry loops absorb the wait;
//                  - timer arm mux: fixed-priority drain of per-engine arm
//                    queues (listener > talker > ADP > SRP > originator),
//                    depth 4 each, drops counted (never silent);
//                  - PRNG draw mux: pending-latch per client with owner
//                    routing of draw_valid (a broadcast valid would complete
//                    the wrong client's draw).
//
//                The one design decision that matters: the RX slot pool is
//                REPLICATED once per reader (ADP / listener / talker / AECP
//                face / ACMP steer prefetch) instead of arbitrating its
//                single read port. Every
//                landed engine assumes byte-data-one-cycle-after-rd_en with
//                no stall path, so a shared port would silently interleave
//                addresses under concurrent pops; replicas receive the
//                identical alloc/write/commit/free stream cycle-by-cycle
//                (frees serialized through one queue and broadcast), so
//                their occupancy state is lock-step by construction and
//                reads never mutate — divergence is structurally impossible,
//                at the price of three extra small RAMs.
//---------------------------------------------------------------------------//
`default_nettype none

module protocol_processor_top
  import pp_pkg::*;
#(
    //! P-N-STREAM-IN (F01.5): sinks / listener SMs
    parameter int unsigned N_STREAM_IN_P       = 8,
    //! P-N-STREAM-OUT (F01.5): sources / talker gates
    parameter int unsigned N_STREAM_OUT_P      = 8,
    //! the rest of the shape the AECP dynamic-state store rows on: Milan
    //! v1.2 keeps one setting per Audio Unit (§5.3.5.1), per Clock Domain
    //! (§5.3.11.1) and per IDENTIFY CONTROL (§5.3.12)
    parameter int unsigned N_AUDIO_UNIT_P      = 1,
    parameter int unsigned N_CLK_DOMAIN_P      = 1,
    parameter int unsigned N_CONTROL_P         = 1,
    //! P-RX-SLOTS x P-RX-SLOT-BYTES (F01.5)
    parameter int unsigned RX_SLOTS_P          = 4,
    parameter int unsigned RX_SLOT_BYTES_P     = 576,
    //! P-TX-STD-SLOTS / P-TX-OVERSIZE-BYTES (F01.5)
    parameter int unsigned TX_STD_SLOTS_P      = 4,
    parameter int unsigned TX_OVERSIZE_BYTES_P = 1600,
    //! P-CLK-HZ (F01.5) — feeds the timer prescaler default
    parameter int unsigned CLK_HZ_P            = 100_000_000,
    //! timer prescaler overrides (09 §3 TIM time compression)
    parameter int unsigned TIM_DIV_US_P        = CLK_HZ_P / 32'd1_000_000,
    parameter int unsigned TIM_DIV_MS_P        = 1000,
    //! ACMP listener transition-ROM image (rom/gen_ltn_rom.py output)
    parameter string       TROM_HEX_P          = "ltn_rom.hex",
    //! AECP µcode ROM image (hdl/aecp/ucode/gen_ucode.py output). Same trap as
    //! TROM_HEX_P: a RELATIVE name resolves against the TOOL'S RUN DIRECTORY,
    //! which is why the parameter exists at all — an integrator hands over an
    //! absolute path.
    parameter string       UCODE_HEX_P         = "ucode.hex",
    //! ---- descriptor image in the integrator's MAIN MEMORY (07 §3.3) ------
    //! The entity model does NOT live on chip: the reference consumer's is
    //! 22,561 bytes at the 8x8 shape and the reference part measured 131 of
    //! 135 block-RAM tiles used. It lives in DDR3 on the reference board,
    //! reached through the vendor-neutral read-only master below.
    //!
    //! Every address is a COMPILE-TIME parameter — the DRAM map is fixed when
    //! the bitstream is built, so a runtime base would only buy a 32-bit port
    //! and the flops behind it. Software loads the image at DESC_BASE_P before
    //! entity_enable; if it has not (or loaded a truncated one), the store's
    //! magic + version + checksum header check fails and reports zero
    //! configurations. READ_DESCRIPTOR then answers BAD_ARGUMENTS before
    //! locate, never a garbage descriptor on the wire.
    parameter logic [31:0] DESC_BASE_P         = 32'h2000_0000,
    //! on-chip line buffer for ONE located descriptor (07 §3.2 worst case)
    parameter int unsigned DESC_LINE_BYTES_P   = 576,
    //! cached index-map entries, one per (configuration, descriptor_type)
    parameter int unsigned DESC_IDX_ENTRIES_P  = 32,
    //! 64-byte name-table entries held on chip (07 §3.4 overlay)
    parameter int unsigned DESC_NAME_ENTRIES_P = 32,
    //! no-progress watchdog on the descriptor memory face, in clocks
    parameter int unsigned DESC_MEM_TMO_CYC_P  = 4096,
    //! IEEE §7.4.37.2's 300 s TIME_LIMITED registration window and IEEE
    //! §7.4.2's 60 s lock, in ms of the (possibly TIM-compressed) timebase.
    //! Parameters for the same reason TIM_DIV_* are: a suite that needs to
    //! SEE the expiry cannot wait 30 million compressed cycles for it.
    parameter int unsigned REG_TL_TIMEOUT_MS_P = 300_000,
    parameter int unsigned LOCK_TIMEOUT_MS_P   = 60_000,
    //! ---- AECP response buffer in the integrator's MAIN MEMORY (03 §7) ---
    //! The response an AECP command builds is up to 592 bytes and it does not
    //! live on chip either. Held as fabric state it measured 5,079 flip-flops
    //! on the reference part and was the state the placer could not pack on a
    //! die whose block RAM was already 100 % used. Same rule as the image
    //! above: a COMPILE-TIME base, never a register. UNLIKE the image this
    //! region is WRITTEN by the processor, so the integrator must reserve
    //! `16 + DESC_LINE_BYTES_P` bytes there that nothing else writes, and it
    //! must not overlap `DESC_BASE_P`.
    parameter logic [31:0] RESP_BASE_P         = 32'h2010_0000,
    //! ---- SRP Class A Domain default (10 §6.1 F10.2) --------------------
    //! P-SRP-DOM-DEF-VID (F01.5): the SRclassVID the Domain FSM declares at
    //! startup and on every LINK_UP, and returns to on LINK_DOWN (Milan
    //! §4.2.7.2.1). A bridge's differing Class A Domain is still adopted
    //! over it at run time. Milan fixes the shipping value at 2, so any other
    //! value is a verification fixture proving this binding, never a product
    //! profile. Bound to KL_srp_top.DOM_DEF_VID_P at the same 16-bit width.
    parameter logic [15:0] SRP_DOM_DEF_VID_P   = 16'd2,
    //! derived — do not override
    //! F08.4 timer-slot map for THIS shape. Every base below is the running
    //! sum of the group extents before it (pp_pkg::pp_timer_map is the ONE
    //! place that arithmetic exists), so the map is correct at any
    //! P-N-STREAM-IN / P-N-STREAM-OUT — see the banner at the bases.
    localparam pp_timer_map_t TMR_MAP_C =
        pp_timer_map(PP_N_IF_C, N_STREAM_IN_P, N_STREAM_OUT_P,
                     PP_N_CTRL_C, PP_CA_POOL_C),
    //! P-TIMER-SLOTS for this shape (= pp_timer_slots(..., en_srp = 1)).
    //! At the F01.5 default shape this is exactly PP_TIMER_SLOTS_C = 89.
    localparam int unsigned TMR_SLOTS_C  = TMR_MAP_C.srp_end,
    localparam int unsigned TMR_AW_C     = $clog2(TMR_SLOTS_C),             // 7 at 8x8
    localparam int unsigned RXS_W_C      = (RX_SLOTS_P > 1) ? $clog2(RX_SLOTS_P) : 1,
    //! Sink/source index widths, CLAMPED exactly as the engines clamp their
    //! own (KL_pp_acmp_listener SINK_W_C :76, KL_acmp_talker SRC_W_C :95).
    //! Without the clamp a 1-stream shape declares [-1:0], and the consumer
    //! elaborates this processor at N_STREAMS = 1 on its shipping board.
    localparam int unsigned SINK_IDX_W_C = (N_STREAM_IN_P  > 1) ? $clog2(N_STREAM_IN_P)  : 1,
    localparam int unsigned SRC_IDX_W_C  = (N_STREAM_OUT_P > 1) ? $clog2(N_STREAM_OUT_P) : 1,
    localparam int unsigned RXA_W_C      = $clog2(RX_SLOT_BYTES_P),
    localparam int unsigned RXL_W_C      = $clog2(RX_SLOT_BYTES_P + 1),
    localparam int unsigned TXS_W_C      = $clog2(TX_STD_SLOTS_P + 1),      // 3
    localparam int unsigned TXA_W_C      = $clog2(TX_OVERSIZE_BYTES_P + 1)  // 11
) (
    input  wire         clk_i,                 //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,                 //! synchronous active-low reset

    //! ---- identity + model registers (quasi-static, 02 §2 rule 4) ----
    input  wire  [63:0] entity_id_i,           //! own entity_id
    input  wire  [63:0] entity_model_id_i,     //! entity_model_id
    input  wire  [47:0] own_mac_i,             //! own unicast MAC
    input  wire  [15:0] talker_sources_i,      //! ADPDU talker_stream_sources
    input  wire  [15:0] talker_caps_i,         //! ADPDU talker_capabilities
    input  wire  [15:0] listener_sinks_i,      //! ADPDU listener_stream_sinks
    input  wire  [15:0] listener_caps_i,       //! ADPDU listener_capabilities
    input  wire  [15:0] current_cfg_i,         //! current_configuration_index
    input  wire  [15:0] identify_index_i,      //! identify_control_index

    //! ---- level controls + class-D inputs (02 §6) ----
    input  wire         entity_enable_i,       //! Milan §5.6.1 boot gate (level)
    input  wire         link_up_i,             //! link status (2FF-synced upstream)
    //! one-cycle ADP/GET_AVB_INFO gPTP-pair change strobe. Raise it after
    //! publishing a changed gm_id_i OR gptp_domain_i. A GM identity change
    //! also changes AS_PATH entry 0, so pulse gsi_asp_chg_i once that path
    //! snapshot is atomically published; a domain-only change does not.
    input  wire         gm_change_i,
    input  wire  [63:0] gm_id_i,               //! gm_id (interface 0)
    input  wire  [7:0]  gptp_domain_i,         //! gptp_domain (interface 0)

    //! ---- SRP quasi-static configuration (10) ----
    input  wire         p2p_i,                 //! operPointToPointMAC (Milan: 1)
    input  wire         cfg_rank_i,            //! declared rank bit (F10.7)
    input  wire  [31:0] cfg_acc_lat_ns_i,      //! initial accumulated_latency
    input  wire  [31:0] port_rate_bps_i,       //! port rate for the admission ceiling
    input  wire  [15:0] cfg_tspec_max_frame_i, //! TSpec MaxFrameSize for engine-driven DECLARE_TALKER

    //! ---- talker source configuration (05 quasi-static) ----
    input  wire  [N_STREAM_OUT_P-1:0]    cfg_src_en_i,     //! source exists in current config
    input  wire  [N_STREAM_OUT_P*2-1:0]  cfg_src_iface_i,  //! per-source AVB interface
    input  wire  [N_STREAM_OUT_P*64-1:0] cfg_stream_id_i,  //! per-source stream_id

    //! ---- MAC trunk RX (byte stream, frames delimited by rx_last_i) ----
    input  wire         rx_valid_i,            //! byte strobe from the RX async FIFO
    input  wire  [7:0]  rx_data_i,             //! frame byte (byte 0 = first DA octet)
    input  wire         rx_last_i,             //! final byte of the frame

    //! ---- MAC TX (merged byte stream, 02 §2 class A) ----
    output logic        tx_valid_o,            //! stream byte valid
    output logic        tx_sof_o,              //! first byte of each frame
    output logic [7:0]  tx_data_o,             //! frame byte (byte 0 = first DA octet)
    output logic        tx_eof_o,              //! final byte of the frame
    input  wire         tx_ready_i,            //! downstream MAC FIFO consumes

    //! ---- descriptor-image memory master (07 §3.3; READ-ONLY) -------------
    //! The AECP engine's entity model lives in the integrator's main memory at
    //! DESC_BASE_P. Vendor-neutral by contract (hdl/README rule 1): the
    //! integrator bridges this to whatever it has — this repository does not
    //! know it is DDR3. ONE outstanding request, responses IN ORDER,
    //! `rsp_last` marks the final beat, and a beat carries its lowest byte
    //! address in bits [63:56] (1722.1 wire order). Leaving `req_ready` tied 0
    //! is a LEGAL wiring: the store's watchdog degrades every direct locate to
    //! NO_SUCH_DESCRIPTOR instead of hanging the µCPU. READ_DESCRIPTOR first
    //! sees zero configurations and answers BAD_ARGUMENTS.
    output logic        desc_mem_req_valid_o,  //! request, held until ready
    input  wire         desc_mem_req_ready_i,  //! bridge accepts the request
    output logic [31:0] desc_mem_req_addr_o,   //! byte address, 8-byte aligned
    output logic  [8:0] desc_mem_req_beats_o,  //! 64-bit beats in this burst
    input  wire         desc_mem_rsp_valid_i,  //! response beat present
    output logic        desc_mem_rsp_ready_o,  //! processor consumes the beat
    input  wire  [63:0] desc_mem_rsp_data_i,   //! beat data (big-endian lane)
    input  wire         desc_mem_rsp_last_i,   //! final beat of the burst
    input  wire         desc_mem_rsp_err_i,    //! read failed — abort the burst

    //! ---- AECP response-buffer memory master (03 §7; READ + WRITE) -------
    //! A SECOND, independent main-memory master, dedicated to the AECP
    //! response buffer at RESP_BASE_P. It is separate from the descriptor face
    //! above ON PURPOSE: both are watchdog-bounded clients with one
    //! outstanding transaction each, and sharing one channel would mean an
    //! arbiter whose grant has to be released correctly on every timeout arm
    //! of both. The integrator's memory system already arbitrates.
    //!
    //! READ channel — identical contract to `desc_mem_*` above (one
    //! outstanding request, responses IN ORDER, `rsp_last` on the final beat,
    //! a beat carries its lowest byte address in bits [63:56]) with ONE
    //! difference that matters: `rsp_ready` here is REAL backpressure. The
    //! buffer accepts a beat only once the frame builder has consumed the
    //! previous one, so the bridge SHALL hold a beat until it is taken.
    //!
    //! WRITE channel — ONE outstanding single-beat write. `wr_data` is a
    //! 64-bit lane in the same big-endian byte order as a read beat (byte
    //! `addr + n` is bits [63-8n -: 8]); `wr_strb` bit n enables that byte and
    //! a byte whose strobe is 0 SHALL NOT be modified. `wr_done` is a
    //! one-cycle pulse when the write is COMMITTED — same cycle as `wr_ready`
    //! for a posted bridge, any later cycle for an acknowledged one — and the
    //! processor issues no further write until it arrives.
    //!
    //! ORDERING — a read request accepted after a write reported done SHALL
    //! observe that write. Nothing else in this processor addresses the
    //! region, so no further rule is needed.
    //!
    //! Leaving `req_ready` and `wr_ready` tied 0 is a LEGAL wiring, exactly as
    //! it is for the descriptor face: the buffer's watchdog voids the response
    //! and the engine answers ENTITY_MISBEHAVING instead of hanging.
    output logic        resp_mem_req_valid_o,  //! read request, held until ready
    input  wire         resp_mem_req_ready_i,  //! bridge accepts the request
    output logic [31:0] resp_mem_req_addr_o,   //! byte address, 8-byte aligned
    output logic  [8:0] resp_mem_req_beats_o,  //! 64-bit beats in this burst
    input  wire         resp_mem_rsp_valid_i,  //! response beat present
    output logic        resp_mem_rsp_ready_o,  //! processor consumes the beat
    input  wire  [63:0] resp_mem_rsp_data_i,   //! beat data (big-endian lane)
    input  wire         resp_mem_rsp_last_i,   //! final beat of the burst
    input  wire         resp_mem_rsp_err_i,    //! read failed — abort the burst
    output logic        resp_mem_wr_valid_o,   //! write presented, held until ready
    input  wire         resp_mem_wr_ready_i,   //! bridge accepts the write
    output logic [31:0] resp_mem_wr_addr_o,    //! byte address, 8-byte aligned
    output logic [63:0] resp_mem_wr_data_o,    //! lane data (big-endian lane)
    output logic  [7:0] resp_mem_wr_strb_o,    //! per-byte enable, bit n = byte n
    input  wire         resp_mem_wr_done_i,    //! write committed (one-cycle pulse)
    input  wire         resp_mem_wr_err_i,     //! ... and it failed

    //! ---- AECP pop face --------------------------------------------------
    //! NO LONGER THE ONLY CONSUMER: KL_aecp_engine below pops this queue and
    //! answers on TX lane 0. These ports stay because an integrator may want
    //! to observe the head (or drain it itself), but `aecp_txn_ready_i` is now
    //! an ADDITIONAL drain OR-ed with the engine's — tie it 0 unless you mean
    //! to steal records from the engine.
    output logic                    aecp_txn_valid_o, //! head record valid
    output logic [PP_TXN_W_C-1:0]   aecp_txn_o,       //! head pp_txn_t record
    input  wire                     aecp_txn_ready_i, //! extra consumer pops the head
    input  wire  [RXS_W_C-1:0]      aecp_rxs_rd_slot_i, //! payload slot to read
    input  wire  [RXA_W_C-1:0]      aecp_rxs_rd_addr_i, //! byte address in the slot
    input  wire                     aecp_rxs_rd_en_i,   //! sync-read enable
    output logic [7:0]              aecp_rxs_rd_data_o, //! byte, one cycle later
    output logic [RXL_W_C-1:0]      aecp_rxs_slot_len_o,//! committed slot length
    input  wire                     aecp_rxs_free_i,    //! return the consumed slot
    input  wire  [RXS_W_C-1:0]      aecp_rxs_free_slot_i, //! which slot

    //! ---- GET_COUNTERS read face (06 §6.6; IEEE §7.4.42, Milan §5.4.2.25) ----
    //! The processor parses the command and lays out §7.4.42.2's 32-quadlet
    //! block; the INTEGRATOR owns what the numbers mean, because the events
    //! Milan Table 5.6 counts happen in its stream datapath. One quadlet is
    //! asked for at a time: `ctr_word_o` 0..31 is the block quadlet at block
    //! byte 4·n and `ctr_word_o` = 32 is the counters_valid mask itself, so
    //! there is one place to say what this build actually measures.
    //!
    //! LEAVING IT UNWIRED IS SAFE AND HONEST, by the polarity of the hold: an
    //! undriven `ctr_wait_i` is 0, every quadlet answers 0 immediately, and a
    //! counters_valid of 0 is §7.4.42.2's own way of saying "no counter here".
    //! What it must never be is a mask of ones over a block that never moves.
    output logic        ctr_req_o,            //! a quadlet is being asked for
    output logic [15:0] ctr_desc_type_o,      //! AECPDU @24
    output logic [15:0] ctr_desc_index_o,     //! AECPDU @26
    output logic  [5:0] ctr_word_o,           //! 0..31 = block quadlet, 32 = counters_valid
    input  wire  [31:0] ctr_data_i,           //! that quadlet
    input  wire         ctr_wait_i,           //! HOLD the beat (not a ready)
    input  wire         ctr_change_i,         //! one served descriptor counter changed
    input  wire  [15:0] ctr_change_desc_type_i,
    input  wire  [15:0] ctr_change_desc_index_i,

    //! ---- GET_AUDIO_MAP read face (06 §6.5; IEEE §7.4.44, Milan §5.4.2.26) ----
    //! The processor parses the command, enforces §7.4.44.1's page rule and
    //! lays out §7.4.44.2's response; the INTEGRATOR owns the dynamic
    //! mappings and the Milan §5.4.2.26 partition, because they live in its
    //! routing fabric. One word is asked for at a time: `amap_sel_o` 0 is
    //! the addressed port's number_of_maps (0 = no such port in the fabric -
    //! turned into NO_SUCH_DESCRIPTOR only where the descriptor image
    //! agrees), 1 is {number_of_maps, number_of_mappings} for the page
    //! `amap_map_index_o` (a page the fabric has no data for MUST answer 0
    //! mappings - the wrong-object guard), and 2 is mapping record
    //! `amap_rec_o` of that page as one big-endian §7.4.44.2.1 qword
    //! {stream_index, stream_channel, cluster_offset, cluster_channel}.
    //!
    //! LEAVING IT UNWIRED IS SAFE AND HONEST, same polarity as the counters
    //! face: an undriven `amap_wait_i` is 0, number_of_maps answers 0, and
    //! every GET_AUDIO_MAP resolves against the descriptor image alone.
    output logic        amap_req_o,           //! a word is being asked for
    output logic [15:0] amap_desc_type_o,     //! AECPDU @24 (STREAM_PORT_INPUT or _OUTPUT - route on it)
    output logic [15:0] amap_desc_index_o,    //! AECPDU @26
    output logic [15:0] amap_map_index_o,     //! AECPDU @28 - the page
    output logic  [1:0] amap_sel_o,           //! 0 NMAPS, 1 GEOM, 2 RECORD
    output logic  [7:0] amap_rec_o,           //! record ordinal within the page
    input  wire  [63:0] amap_data_i,          //! the word (upper 32 zero unless RECORD)
    input  wire         amap_wait_i,          //! HOLD the beat (not a ready)

    //! ---- ADD/REMOVE_AUDIO_MAPPINGS transaction face --------------------
    //! The processor has already checked exact wire length, lock ownership
    //! and descriptor existence. The integrator validates every record before
    //! phase 5 can write one. Accepting phase 1 reserves the complete commit;
    //! phases 5 and 2 must then complete without back-pressure, and the
    //! processor ignores `amap_edit_wait_i` on those phases. Refuse phase 1
    //! if that guarantee cannot be made.
    output logic        amap_edit_req_o,
    output logic  [2:0] amap_edit_phase_o,
    output logic        amap_edit_remove_o,
    output logic [15:0] amap_edit_desc_type_o,
    output logic [15:0] amap_edit_desc_index_o,
    output logic [15:0] amap_edit_count_o,
    output logic  [7:0] amap_edit_rec_o,
    output logic [63:0] amap_edit_record_o,
    output logic [63:0] amap_edit_value_o,
    input  wire  [63:0] amap_edit_data_i,
    input  wire         amap_edit_wait_i,

    //! ---- Milan-info gather face (06 §6.2/§6.10; IEEE §7.4.16/§7.4.40/
    //! §7.4.41, Milan §5.4.2.10/§5.4.2.23/§5.4.2.24) ----
    //! The processor parses GET_STREAM_INFO / GET_AVB_INFO / GET_AS_PATH and
    //! lays out their responses; the INTEGRATOR owns every word, because the
    //! truth lives in its binding view, SRP registrars, format registers and
    //! gPTP plane. One word at a time: `gsi_kind_o` names the command family
    //! (0 STRI / 1 AVB / 2 ASP), `gsi_sel_o` the word, `gsi_ord_o` the
    //! GET_AS_PATH array ordinal. Word tables: docs/architecture/06
    //! §6.2/§6.10.
    //!
    //! LEAVING IT UNWIRED IS SAFE AND HONEST, same polarity as the other
    //! faces: an undriven `gsi_wait_i` is 0, every word answers 0, and the
    //! responses carry cleared validity flags, zero fields and a zero path
    //! count - absent, never invented.
    output logic        gsi_req_o,            //! a word is being asked for
    output logic [1:0]  gsi_kind_o,           //! 0 STRI / 1 AVB / 2 ASP
    output logic [15:0] gsi_desc_type_o,      //! addressed descriptor_type
    output logic [15:0] gsi_desc_index_o,     //! addressed descriptor_index
    output logic  [3:0] gsi_sel_o,            //! word selector within the kind
    output logic  [7:0] gsi_ord_o,            //! ASP path entry ordinal
    //! the PROPOSED stream format while a SET_STREAM_FORMAT is in flight.
    //! Kind 0 selector 15 asks the integrator to judge it for the addressed
    //! stream: answer bit 0 = the format is one this build can serve, bit 1
    //! = every channel an existing audio mapping references still exists in
    //! it (Milan §5.4.2.7). ANSWER THE TWO BITS ALONE: the µprogram compares
    //! the answer's low byte against exactly 0x03, so any other bit set in
    //! it refuses the command. An unwired face answers 0 and the command
    //! refuses BAD_ARGUMENTS - a setter no integrator vouches for must not
    //! claim SUCCESS.
    output logic [63:0] gsi_prop_fmt_o,
    input  wire  [63:0] gsi_data_i,           //! the word
    input  wire         gsi_wait_i,           //! HOLD the beat (not a ready)
    //! one-cycle strobe: a face-served GET_AVB_INFO word changed outside
    //! this processor's sight (asCapable, propagation delay). The gm/domain/
    //! link triggers are derived internally; this pin covers the remainder,
    //! and tying it 0 just narrows the Table 5.22 trigger set to what the
    //! processor sees itself.
    input  wire         gsi_avb_chg_i,
    //! one-cycle strobe after the integrator atomically publishes ANY changed
    //! PathTrace sequence, including entry 0 when the GM identity changes.
    //! This is the sole GET_AS_PATH trigger: gm_change_i also covers a domain
    //! change, which does not by itself change the path sequence.
    input  wire         gsi_asp_chg_i,

    //! ---- NVM boot restore + alarm (07 §5.3) ----
    input  wire         restore_go_i,          //! start boot restore
    output logic        restore_busy_o,        //! restore walk running
    output logic        restore_done_o,        //! level: restore complete
    output logic        restore_fail_o,        //! level: torn read-back aborted restore
    //! done says the walk SEQUENCED; blank says it validated nothing. An
    //! integrator whose device face is unbacked or whose media is erased sees
    //! done with no fail on every path, so this is the only pin that tells it
    //! apart from a walk that actually put Milan 5.3.8.2/5.3.8.3 state back.
    output logic        restore_blank_o,       //! level: completed walk validated ZERO records
    output logic        nvm_alarm_o,           //! sticky: commit retries exhausted
    //! per-sink UNFLUSHED binding state, the manager's own dirty vector
    //! (KL_acmp_nvm_shadow dirty_r, a clk_i register read combinationally).
    //! Bit k rises on the cycle the manager ACCEPTS a changed persisted set
    //! for sink k — two clk_i cycles after cap_wr_i, because the capture is
    //! pipelined one stage and the accept is the compare against the shadow,
    //! so a write-back that changes no persisted field never raises it — and
    //! falls on the cycle its commit reports done, or, on retry exhaustion,
    //! on the same cycle nvm_alarm_o rises. A tainted commit (a capture that
    //! hit the sink mid-flush) holds it: the burst re-serializes fresh data.
    //! An integrator publishing a "saved state pending" bit ORs this vector
    //! with aecp_dyn_dirty_o; without it a binding taken inside the
    //! manager's debounce window reads durable.
    output logic [N_STREAM_IN_P-1:0] nvm_unflushed_o,

    //! ---- NVM device face (external backend; KL_pp_nvm_port initiator) ----
    output logic        nvm_dev_req_o,         //! command request, held until gnt
    input  wire         nvm_dev_gnt_i,         //! backend accepts the command
    output logic [1:0]  nvm_dev_op_o,          //! READ / WRITE / ERASE
    output logic [7:0]  nvm_dev_region_o,      //! region id = record id
    output logic [15:0] nvm_dev_offset_o,      //! byte offset within the region
    output logic [15:0] nvm_dev_len_o,         //! byte count
    output logic        nvm_dev_wvalid_o,      //! write byte present
    input  wire         nvm_dev_wready_i,      //! backend accepts the write byte
    output logic [7:0]  nvm_dev_wdata_o,       //! write byte
    input  wire         nvm_dev_rvalid_i,      //! read byte present
    input  wire  [7:0]  nvm_dev_rdata_i,       //! read byte
    output logic        nvm_dev_rready_o,      //! port accepts the read byte
    input  wire         nvm_dev_busy_i,        //! backend busy (informational)
    input  wire         nvm_dev_done_i,        //! one-cycle: command complete
    input  wire         nvm_dev_err_i,         //! one-cycle: command failed

    //! ---- side-port host face (class E, F02.7) ----
    input  wire         host_req_valid_i,      //! request present (hold until rvalid)
    input  wire         host_we_i,             //! 1 = write
    input  wire  [19:0] host_addr_i,           //! 20-bit WORD address
    input  wire  [31:0] host_wdata_i,          //! write data
    output logic [31:0] host_rdata_o,          //! read data (0 on error)
    output logic        host_rvalid_o,         //! completion strobe
    output logic        host_err_o,            //! access refused

    //! ---- SRP service face (02 §4.1 class B; config-plane seam) ----
    input  wire         svc_valid_i,           //! request offered, held until ready
    output logic        svc_ready_o,           //! stage free this cycle
    input  wire  [2:0]  svc_op_i,              //! KL_srp_top req_op_i code
    input  wire  [7:0]  svc_index_i,           //! source/sink index / class id
    input  wire  [63:0] svc_stream_id_i,       //! stream_id
    input  wire  [47:0] svc_da_i,              //! destination MAC
    input  wire  [11:0] svc_vid_i,             //! VLAN id
    input  wire  [15:0] svc_max_frame_i,       //! DECLARE_TALKER TSpec MaxFrameSize
    input  wire  [1:0]  svc_lstn_state_i,      //! DECLARE_LISTENER state
    output logic        svc_rsp_valid_o,       //! one response per svc request
    output logic [1:0]  svc_rsp_status_o,      //! 0 OK / 1 FAIL / 2 UNSUPPORTED
    output logic [31:0] svc_rsp_data_o,        //! GET_DOMAIN answer

    //! ---- class-D status levels (02 §6, F02.10) — THE FABRIC FACE --------
    //! Everything this engine knows used to be reachable only through a
    //! side-port READ TRANSACTION. That is a software-paced path, and the
    //! integrating fabric consumes this state as WIRES, every clock: the
    //! consumer's AAF talker gate is a per-cycle AND of the talker-active and
    //! stream-gate terms, and its CBS slope MUX needs the granted idleSlope.
    //! Publishing nothing here is exactly the NC-5 defect the resource study
    //! called out — "its replacement publishes no granted bandwidth, so the
    //! consumer's CBS slope MUX and its Σ-limit admission decision would have
    //! no source under this contract". These ports are that source.
    //!
    //! Per-index vectors are FLAT packed bit-vectors, index s at [W*s +: W] —
    //! the cfg_stream_id_i / cfg_src_iface_i convention already used above.
    //! All are combinational reads of clk_i-domain registers: a consumer in
    //! another clock domain owns its own 2FF synchroniser.
    output logic [2:0]                   srp_class_a_prio_o,      //! SRclassPriority, DEFAULTS until adopted
    output logic [11:0]                  srp_class_a_vid_o,       //! SRclassVID, DEFAULTS until adopted
    output logic                         srp_domain_adopted_o,    //! F10.2: 1 = ADOPTED a bridge Domain, 0 = still DEFAULTS
    output logic                         srp_domain_change_o,     //! one-cycle DOMAIN_CHANGE, pairs with the two levels above
    output logic [N_STREAM_OUT_P*2-1:0]  srp_tk_decl_state_o,     //! per-source self-declared {0 NONE, 1 ADVERTISE, 2 FAILED}
    output logic [N_STREAM_OUT_P*2-1:0]  srp_lstn_reg_state_o,    //! per-source registered Listener attr (srp_pkg::srp_decl_e)
    //! THE AVTP transmit gate: declaring AND not failed AND a listener is
    //! READY AND admitted. Use THIS — never rebuild it from the terms below,
    //! which carry an optimistic window (see srp_sr_admitted_o).
    output logic [N_STREAM_OUT_P-1:0]    srp_active_o,
    //! RAW Σ-slope verdict. It lags srp_active_o by up to three admission
    //! rounds after a fresh declare, because the FSM admits optimistically
    //! (KL_srp_top: sr_adm_fsm = opt_r | adm_admitted). A consumer that gates
    //! on this instead of srp_active_o mutes a legal stream for those rounds.
    output logic [N_STREAM_OUT_P-1:0]    srp_sr_admitted_o,
    output logic [N_STREAM_OUT_P*32-1:0] srp_granted_slope_bps_o, //! per-source granted idleSlope, 0 when not admitted (802.1Q §34.6.1.1); same optimistic lag
    output logic [N_STREAM_OUT_P*8-1:0]  srp_src_fail_code_o,     //! per-source SELF-declared Failed code; valid only with tk_decl_state == FAILED
    output logic [N_STREAM_OUT_P*64-1:0] srp_src_fail_bridge_o,   //! per-source SELF-declared FailureInformation; same validity
    output logic [31:0]                  srp_sum_slope_bps_o,     //! Σ granted idleSlope over admitted sources — the CBS slope-MUX value
    output logic                         srp_over_limit_o,        //! at least one source was refused against the port ceiling
    output logic [N_STREAM_IN_P*2-1:0]   srp_tk_reg_state_o,      //! per-sink registered Talker attr {0 NONE, 1 ADVERTISE, 2 FAILED}
    output logic [N_STREAM_IN_P*2-1:0]   srp_lstn_decl_state_o,   //! per-sink OUR Listener declaration
    output logic [N_STREAM_IN_P*32-1:0]  srp_acc_latency_o,       //! per-sink registered accumulated_latency, ns, RAW — the consumer adds its own ingress delay
    output logic [N_STREAM_IN_P*8-1:0]   srp_snk_fail_code_o,     //! per-sink registered Failed code; valid only with tk_reg_state == FAILED

    //! ---- class-D ACMP / ADP status levels --------------------------------
    //! per-source DA gate open. THE talker egress gate a fabric ANDs with its
    //! own stream enable every clock.
    output logic [N_STREAM_OUT_P-1:0]    acmp_declaring_o,
    //! per-sink binding installed, DEBOUNCED. The internal binding register
    //! dips 1->0->1 inside a single executor transaction on every re-bind
    //! (the F05.3 BIND_NEW row runs an unbind action before the bind action),
    //! so the raw register is not safe for a fabric to edge-detect. This port
    //! holds through the transaction; the raw one still drives the ADP
    //! engine's own edge detector, which must keep seeing it.
    output logic [N_STREAM_IN_P-1:0]     acmp_bound_o,
    output logic [N_STREAM_IN_P*64-1:0]  acmp_bound_eid_o,        //! per-sink bound talker entity_id, valid with acmp_bound_o
    //! The bound stream's IDENTITY ON THE WIRE. entity_id above says WHO the
    //! talker is; these say WHICH STREAM to receive and on WHAT address — an
    //! integrating fabric needs them to arm its RX filter and its stream
    //! table, and cannot derive either from the entity_id. Latched at A15
    //! settle, held while acmp_bound_o.
    output logic [N_STREAM_IN_P*64-1:0]  acmp_bound_sid_o,        //! per-sink bound stream_id
    output logic [N_STREAM_IN_P*48-1:0]  acmp_bound_dmac_o,       //! per-sink bound stream destination MAC
    output logic [N_STREAM_IN_P*12-1:0]  acmp_bound_vlan_o,       //! per-sink bound stream VLAN id
    //! 32 BITS, not 16. KL_adp_engine keeps a 32-bit counter and puts all
    //! 32 on the wire, and the AEM ENTITY descriptor's available_index is a
    //! 32-bit field that is visible in every READ_DESCRIPTOR response.
    //! Truncating here would wrap the CSR and the AEM readback at 65536
    //! advertisements while the ADPDU kept counting — a controller would see
    //! available_index step BACKWARDS, which is exactly the signal it uses to
    //! decide an entity restarted.
    output logic [31:0]                  adp_next_avail_index_o,  //! available_index the NEXT ENTITY_AVAILABLE will carry

    //! ---- maap face (02 §4.2) — THE ADDRESS ALLOCATOR SEAM --------------
    //! Two legal answers now exist. With cfg_maap_internal_i = 0 (the
    //! default and the landed behaviour, byte-identical), the processor
    //! disables its internal allocator and selects the external seam.
    //! Address allocation then lives in the integrating fabric (the consumer
    //! ships a KL_maap engine behind KL_pp_maap_shim). With
    //! cfg_maap_internal_i = 1 the in-scope KL_pp_maap engine (11, IEEE
    //! 1722-2016 Annex B) answers the talker internally under the SAME
    //! contract, the port group is quiesced (req_valid held 0, every input
    //! ignored), and the claim is published on the maap_addr_o group below
    //! so the fabric can gate talker egress and retire its own allocator.
    //! Either way, nothing else can open the talker DA gate, because
    //! GS_DECLARING is reachable only through GS_DA_OK and GS_DA_OK is
    //! written only on an ALLOC_DA success (KL_acmp_talker EVC_GRANT): with
    //! this face unconnected AND the internal engine disabled,
    //! acmp_declaring_o above is STRUCTURALLY stuck at 0 and no source ever
    //! declares a Talker attribute to SRP either. So it is published rather
    //! than tied off — a processor whose talker half is dead by
    //! construction is not a contract a fabric can integrate.
    //!
    //! Single-outstanding: one ALLOC_DA / RELEASE_DA at a time, req held
    //! until ready, exactly one rsp per accepted req, conflicts as a sticky
    //! event acked combinationally. An absent OR BROKEN allocator is a LEGAL
    //! wiring, because BOTH halves are bounded in KL_acmp_talker: ready may
    //! sit at 0 (abandoned after P-MAAP-ACCEPT-CYC), and an accepted request
    //! may go unanswered (abandoned after P-MAAP-RSP-MS, a bound derived
    //! from the IEEE 1722-2016 Annex B claim walk). Either way the source
    //! degrades to "no DA" — PROBE_TX then answers TALKER_DEST_MAC_FAILED,
    //! which is the honest answer — instead of wedging the talker walker or,
    //! for the second case, stranding allocation for EVERY source while the
    //! processor keeps answering commands normally. A response arriving
    //! after an abandon is swallowed and can never install a DA.
    output logic                         maap_req_valid_o,      //! ALLOC/RELEASE request, held until ready or the accept window
    input  wire                          maap_req_ready_i,      //! allocator accepts the request (tie 0 = no allocator)
    output logic                         maap_req_release_o,    //! 0 = ALLOC_DA, 1 = RELEASE_DA
    output logic [SRC_IDX_W_C-1:0]       maap_req_src_o,        //! source index of the request
    input  wire                          maap_rsp_valid_i,      //! exactly one response per accepted request
    input  wire                          maap_rsp_ok_i,         //! ALLOC_DA succeeded (ignored on RELEASE_DA)
    input  wire  [47:0]                  maap_rsp_da_i,         //! allocated stream destination MAC (with ok)
    input  wire                          maap_conflict_valid_i, //! MAAP_CONFLICT{source} event, sticky until acked
    input  wire  [SRC_IDX_W_C-1:0]       maap_conflict_src_i,   //! conflicted source
    output logic                         maap_conflict_ack_o,   //! event ack (combinational)

    //! ---- internal MAAP engine (11; IEEE 1722-2016 Annex B) --------------
    //! Quasi-static (02 §2 rule 4: set before entity_enable, stable after).
    //! 0 = the landed behaviour above, byte-identical; 1 = KL_pp_maap owns
    //! the whole-entity block claim and answers the talker's ALLOC/RELEASE
    //! internally under the shim's exact contract.
    input  wire                          cfg_maap_internal_i,    //! 1 = internal allocator
    input  wire  [7:0]                   cfg_maap_count_i,       //! block size to claim (>= 1)
    input  wire  [15:0]                  cfg_maap_seed_offset_i, //! footnote-a provisioning: preferred pool offset
    input  wire                          cfg_maap_seed_valid_i,  //! 1 = first walk probes the seed
    //! The claim, published for the integrating fabric (KL_maap's
    //! addr_o/addr_valid_o naming so the substitution is mechanical): gate
    //! talker egress on maap_addr_valid_o, read source s's DA as
    //! maap_addr_o + s. All-zero while cfg_maap_internal_i = 0.
    output logic [47:0]                  maap_addr_o,        //! claimed base DMAC (source 0)
    output logic                         maap_addr_valid_o,  //! 1 = Annex B DEFEND state (claim held)
    output logic [1:0]                   maap_state_o,       //! 0 INITIAL / 1 PROBE / 2 DEFEND
    output logic [7:0]                   maap_conflicts_o,   //! re-address events (saturating)
    output logic [7:0]                   maap_defends_o,     //! DEFEND frames sent (saturating)

    //! ---- the AECP dynamic state a controller has SET (Milan §5.3.x) ----
    //! The settings face. Each reads its reset default until a controller
    //! writes it, so an integrator that leaves these unconnected behaves
    //! exactly as it did before the store existed.
    output logic [15:0]                  aecp_cur_config_o,   //! current_configuration
    output logic  [7:0]                  aecp_identify_o,     //! IDENTIFY, 0 or 255
    output logic [15:0]                  aecp_clk_src_index_o,//! clock_source_index
    output logic [N_STREAM_IN_P-1:0]     aecp_strm_started_o, //! 1 = started
    //! per-row settings, value beside valid: presentation offsets at
    //! [32k +: 32] and stream formats at [64k +: 64]. The offsets feed the
    //! talker's transit entries, the formats the RX acceptance and the
    //! served "current format"; a value whose valid bit is clear is a reset
    //! zero and must not be consumed.
    output logic [N_STREAM_OUT_P*32-1:0] aecp_pt_offset_o,
    output logic [N_STREAM_OUT_P-1:0]    aecp_pt_offset_v_o,
    output logic [N_STREAM_IN_P*64-1:0]  aecp_fmt_in_o,
    output logic [N_STREAM_IN_P-1:0]     aecp_fmt_in_v_o,
    output logic [N_STREAM_OUT_P*64-1:0] aecp_fmt_out_o,
    output logic [N_STREAM_OUT_P-1:0]    aecp_fmt_out_v_o,
    output logic                         aecp_dyn_dirty_o,    //! a persisted field moved
    //! the AECP engine's NVM COMMIT MARK, the µprogram effect that names the
    //! record group a committed command changed (KL_aecp_ucpu OP_NVM_MARK:
    //! both are combinational reads of the E-stage registers, one clk_i
    //! cycle wide, and the mark is only meaningful while the strobe is 1).
    //! The mark is the micro-op immediate: 1 dynamic-state field (sampling
    //! rate, clock source, configuration index, stream format, stream info),
    //! 6 channel maps (ADD/REMOVE_AUDIO_MAPPINGS), 7 user names (SET_NAME).
    //! Nothing inside this processor consumes them: no record writer exists
    //! for groups 6 and 7, so an integrator that persists those groups has
    //! to see the mark to know a change happened at all.
    output logic                         aecp_nvm_stb_o,      //! one cycle: a committed command marked a record group
    output logic  [7:0]                  aecp_nvm_mark_o,     //! that group's mark code, valid with the strobe
    output logic                         aecp_lock_held_o,    //! LOCK_ENTITY ownership is live

    //! ---- observability ----
    output logic [31:0] dbg_now_ms_o           //! absolute ms timebase
);

  // ---- F08.4 timer-slot allocation (08 §5 order; bases are the contract) --
  //! DERIVED, never literals. The 08 §5 ORDER is the contract; the SIZES are
  //! the shape. A literal map is only correct at the F01.5 default shape:
  //! with SI = SO = 9 (the reference platform's 8x8 build, where the CRF
  //! Media Clock Output is itself a source and a sink) the old literals
  //! aliased listener sink 8 onto the talker base and SRP talker 8 onto the
  //! SRP listener base — the first SILENTLY LOSES a deadline (distinct owner
  //! tags, and the ACMP engines filter by owner) and the second MISDELIVERS
  //! one (ADP and SRP filter by slot, so SRP listener 0 would act on SRP
  //! talker 8's expiry). Neither raises an error or moves a counter; on
  //! silicon they read as an intermittent ACMP timeout and a reservation
  //! that leaves at the wrong moment. The guard below is what makes an
  //! over-large shape fail LOUDLY instead.
  localparam int unsigned TMR_ADP_ADV_BASE_C   = TMR_MAP_C.adp_adv;    // IF slots
  localparam int unsigned TMR_ADP_NOADP_BASE_C = TMR_MAP_C.adp_noadp;  // SI slots
  localparam int unsigned TMR_LSTN_BASE_C      = TMR_MAP_C.lstn;       // SI (shared SM)
  localparam int unsigned TMR_TKR_BASE_C       = TMR_MAP_C.tkr;        // SO (DAFRESH/LA2)
  // TMR_MAP_C.regmon (2*CTRL*IF registry monitors, P4), .capool (CA pool,
  // originator) and .single (5 singletons, P4) are reserved and unused this
  // phase — but they are SPACED, so landing them cannot move anything below.
  localparam int unsigned TMR_MAAP_BASE_C      = TMR_MAP_C.maap;       // 2: probe + announce
  localparam int unsigned TMR_SRP_CAD_BASE_C   = TMR_MAP_C.srp_cad;    // 5 cadence + 2 fixed
  localparam int unsigned TMR_SRP_TK_BASE_C    = TMR_MAP_C.srp_tk;     // SO registrar-leave
  localparam int unsigned TMR_SRP_LS_BASE_C    = TMR_MAP_C.srp_ls;     // SI registrar-leave

  // owner tags must be disjoint across the shared expiry bus: the listener
  // (0x20 + sink) and talker (0x50 + source) filter BY OWNER; ADP and SRP
  // filter by slot. KL_srp_top's default cadence owner base 0x20 collides
  // with the listener's range, so it is moved to 0x80 here. Unlike the slot
  // map these are a fixed allocation of a fixed 8-bit space (pp_pkg), so the
  // shape is BOUNDED against them by the guard below rather than re-spacing
  // tags that landed engines already publish as their defaults.
  localparam logic [7:0] SRP_CAD_OWNER_C = PP_OWN_SRP_CAD_C;
  localparam logic [7:0] SRP_TK_OWNER_C  = PP_OWN_SRP_TK_C;
  localparam logic [7:0] SRP_LS_OWNER_C  = PP_OWN_SRP_LS_C;

  // ---- elaboration guard: the map must FIT and stay DISJOINT -------------
  //! The numbers above can be re-derived by hand; what nothing did before is
  //! NOTICE when they collide. These are IEEE 1800 §20.11 elaboration system
  //! tasks: an over-large shape stops the build here instead of aliasing a
  //! timer slot or an owner tag in silence.
  //!
  //! ADP publishes its SLOT as its owner tag (KL_adp_engine tmr_arm_owner_o
  //! is a zero-extension of tmr_arm_slot_o), so the ADP group constrains the
  //! owner space as well as the slot space.
  localparam int unsigned OWN_ADP_END_C   = TMR_MAP_C.lstn;                        // ADP owners = ADP slots
  localparam int unsigned OWN_LSTN_END_C  = 32'(PP_OWN_LSTN_C)   + N_STREAM_IN_P;
  localparam int unsigned OWN_SRPTK_END_C = 32'(PP_OWN_SRP_TK_C) + N_STREAM_OUT_P;
  localparam int unsigned OWN_TKR_END_C   = 32'(PP_OWN_TKR_C)    + N_STREAM_OUT_P;
  localparam int unsigned OWN_SRPLS_END_C = 32'(PP_OWN_SRP_LS_C) + N_STREAM_IN_P;
  localparam int unsigned OWN_SRPCAD_END_C = 32'(PP_OWN_SRP_CAD_C) + PP_SRP_CAD_SLOTS_C;
  localparam int unsigned OWN_MAAP_END_C   = 32'(PP_OWN_MAAP_C) + PP_MAAP_SLOTS_C;

  if (TMR_SLOTS_C > (32'd1 << TMR_AW_C)) begin : gen_g_tmr_aw
    $error("F08.4: TMR_AW_C=%0d cannot index P-TIMER-SLOTS=%0d",
           TMR_AW_C, TMR_SLOTS_C);
  end
  if (TMR_MAP_C.srp_ls + N_STREAM_IN_P > TMR_SLOTS_C) begin : gen_g_tmr_fit
    $error("F08.4: slot map ends at %0d but P-TIMER-SLOTS=%0d",
           TMR_MAP_C.srp_ls + N_STREAM_IN_P, TMR_SLOTS_C);
  end
  if ((TMR_ADP_NOADP_BASE_C < TMR_ADP_ADV_BASE_C + PP_N_IF_C)
      || (TMR_LSTN_BASE_C    < TMR_ADP_NOADP_BASE_C + N_STREAM_IN_P)
      || (TMR_TKR_BASE_C     < TMR_LSTN_BASE_C      + N_STREAM_IN_P)
      || (TMR_MAP_C.regmon   < TMR_TKR_BASE_C       + N_STREAM_OUT_P)
      || (TMR_MAAP_BASE_C    < TMR_MAP_C.single     + PP_SINGLETON_SLOTS_C)
      || (TMR_MAP_C.base_end < TMR_MAAP_BASE_C      + PP_MAAP_SLOTS_C)
      || (TMR_SRP_CAD_BASE_C < TMR_MAP_C.base_end)
      || (TMR_SRP_TK_BASE_C  < TMR_SRP_CAD_BASE_C   + PP_SRP_CAD_SLOTS_C)
      || (TMR_SRP_LS_BASE_C  < TMR_SRP_TK_BASE_C    + N_STREAM_OUT_P))
  begin : gen_g_tmr_overlap
    $error("F08.4: timer-slot groups OVERLAP at SI=%0d SO=%0d",
           N_STREAM_IN_P, N_STREAM_OUT_P);
  end
  if ((OWN_ADP_END_C   > 32'(PP_OWN_LSTN_C))
      || (OWN_LSTN_END_C  > 32'(PP_OWN_SRP_TK_C))
      || (OWN_SRPTK_END_C > 32'(PP_OWN_TKR_C))
      || (OWN_TKR_END_C   > 32'(PP_OWN_SRP_LS_C))
      || (OWN_SRPLS_END_C > 32'(PP_OWN_SRP_CAD_C))
      || (OWN_SRPCAD_END_C > 32'(PP_OWN_MAAP_C))
      || (OWN_MAAP_END_C   > 32'(PP_OWN_NTFY_C))
      || (32'(PP_OWN_NTFY_C) + PP_N_CTRL_C > 32'(PP_OWN_LOCK_C))
      || (32'(PP_OWN_LOCK_C) + 32'd1 > 32'h0000_00C0)  // originator tag nibble
      || (OWN_MAAP_END_C   > 32'd256)) begin : gen_g_owner_overlap
    $error("F08.4: owner tags OVERLAP at SI=%0d SO=%0d (8-bit expiry bus)",
           N_STREAM_IN_P, N_STREAM_OUT_P);
  end

  // ---- 08 §4 class budgets fed to the normalizer --------------------------
  localparam logic [15:0] BUDGET_ADP_MS_C  = 16'd4000;  // T-ADP-DELAY bound
  localparam logic [15:0] BUDGET_ACMP_MS_C = 16'd50;    // T-BUDGET-ACMP-RESP
  localparam logic [15:0] BUDGET_AECP_MS_C = 16'd100;   // T-BUDGET-AECP-WC

  // ---- TX arbiter lane map (F03.5) ----------------------------------------
  localparam int unsigned LANE_AECP_SOL_C = 0;  // idle until P4
  localparam int unsigned LANE_AECP_UNS_C = 1;  // idle until P4
  localparam int unsigned LANE_ACMP_C     = 2;  // listener PDUs (56 B)
  localparam int unsigned LANE_ADP_C      = 3;  // whole 82 B frames
  localparam int unsigned LANE_SRP_C      = 4;  // whole MRPDU frames
  localparam int unsigned LANE_TKRSP_C    = 5;  // talker response PDUs (56 B)
  localparam int unsigned LANE_MAAP_C     = 6;  // whole 60 B MAAP frames (11)
  localparam int unsigned LANE_ORIG_C     = 7;  // originated AECP commands
  localparam int unsigned LANE_N_C        = 8;

  // =========================================================================
  // shared services: timer, PRNG, scoreboard, trace ring, originator
  // =========================================================================
  logic        tick_ms_w;
  logic [31:0] now_ms_w;
  logic        tmr_arm_valid_w, tmr_arm_cancel_w;
  logic [TMR_AW_C-1:0] tmr_arm_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] tmr_arm_owner_w;
  logic [31:0] tmr_arm_deadline_w;
  logic        exp_valid_w;
  logic [TMR_AW_C-1:0] exp_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] exp_owner_w;

  KL_pp_timer_service #(
      .CLK_HZ_P (CLK_HZ_P),
      .SLOTS_P  (TMR_SLOTS_C),
      .DIV_US_P (TIM_DIV_US_P),
      .DIV_MS_P (TIM_DIV_MS_P)
  ) u_timer (
      .clk_i             (clk_i),
      .rst_n             (rst_n),
      .tick_ms_o         (tick_ms_w),
      .now_ms_o          (now_ms_w),
      .arm_valid_i       (tmr_arm_valid_w),
      .arm_cancel_i      (tmr_arm_cancel_w),
      .arm_slot_i        (tmr_arm_slot_w),
      .arm_owner_i       (tmr_arm_owner_w),
      .arm_deadline_ms_i (tmr_arm_deadline_w),
      .exp_valid_o       (exp_valid_w),
      .exp_slot_o        (exp_slot_w),
      .exp_owner_o       (exp_owner_w)
  );

  assign dbg_now_ms_o = now_ms_w;

  // =========================================================================
  //  class-D fabric face (02 §6). Flat packing: index s at [W*s +: W].
  // =========================================================================
  //! These are plain reads of state this engine already maintains. The only
  //! reason they did not exist is that the interface published none of it —
  //! see the port banner. A `assign flat = packed;` of a [N-1:0][W-1:0] array
  //! onto a [N*W-1:0] vector is bit-exact in this element order.
  assign srp_class_a_prio_o      = srp_class_a_prio_w;
  assign srp_class_a_vid_o       = srp_class_a_vid_w;
  assign srp_domain_adopted_o    = srp_domain_adopted_w;
  assign srp_domain_change_o     = srp_evt_domain_change_w;
  assign srp_tk_decl_state_o     = srp_tk_decl_state_w;
  assign srp_lstn_reg_state_o    = srp_lstn_reg_state_w;
  assign srp_active_o            = srp_active_w;
  assign srp_sr_admitted_o       = srp_sr_admitted_w;
  assign srp_granted_slope_bps_o = srp_granted_slope_w;
  assign srp_src_fail_code_o     = srp_src_fail_code_nc_w;
  assign srp_src_fail_bridge_o   = srp_src_fail_bridge_nc_w;
  assign srp_sum_slope_bps_o     = srp_sum_slope_w;
  assign srp_over_limit_o        = srp_over_limit_w;
  assign srp_tk_reg_state_o      = srp_tk_reg_state_w;
  assign srp_lstn_decl_state_o   = srp_lstn_decl_state_w;
  assign srp_acc_latency_o       = srp_acc_latency_w;
  assign srp_snk_fail_code_o     = srp_snk_fail_code_w;

  assign acmp_declaring_o = tkr_declaring_w;

  //! Debounced binding view. bound_r dips 1->0->1 within ONE executor
  //! transaction on a re-bind, so it is republished held: it may only fall
  //! while the executor is idle. bound_r itself is untouched — KL_adp_engine
  //! edge-detects it and that behaviour must not change.
  logic [N_STREAM_IN_P-1:0] bound_hold_r;
  always_ff @(posedge clk_i) begin : bound_debounce
    if (!rst_n)                    bound_hold_r <= '0;
    else if (!lstn_dbg_busy_nc_w)  bound_hold_r <= bound_r;   // idle: track
    else                           bound_hold_r <= bound_hold_r | bound_r;
  end
  assign acmp_bound_o     = bound_hold_r;
  assign acmp_bound_eid_o  = bound_eid_r;
  assign acmp_bound_sid_o  = bound_sid_r;
  assign acmp_bound_dmac_o = bound_dmac_r;
  assign acmp_bound_vlan_o = bound_vlan_r;

  //! The ADP engine's dbg_avail_index is the PRE-INCREMENT value — the index
  //! the next ENTITY_AVAILABLE will actually carry, which is what a consumer
  //! wants to publish. Full width: see the port comment.
  assign adp_next_avail_index_o = adp_dbg_aidx_nc_w;

  logic        prng_req_w;
  logic [2:0]  prng_kind_w;
  logic        prng_busy_w, prng_valid_w;
  logic [15:0] prng_ms_w;
  logic [63:0] prng_lfsr_nc_w;
  logic        prng_seeded_w;

  KL_pp_prng u_prng (
      .clk_i        (clk_i),
      .rst_n        (rst_n),
      .entity_id_i  (entity_id_i),
      .link_up_i    (link_up_i),
      .draw_req_i   (prng_req_w),
      .draw_kind_i  (prng_kind_w),
      .draw_busy_o  (prng_busy_w),
      .draw_valid_o (prng_valid_w),
      .draw_ms_o    (prng_ms_w),
      .dbg_lfsr_o   (prng_lfsr_nc_w),
      .dbg_seeded_o (prng_seeded_w)
  );

  // One admission port arbitrates the live ACMP and AECP dispatch heads.
  // Each single-issue engine keeps its granted hold until it returns the RX
  // slot, which occurs only after its response is committed or after a
  // standards-permitted silent retirement.
  logic       sb_adm_req_w, sb_gnt_w;
  logic [3:0] sb_adm_class_w;
  logic [15:0] sb_adm_key_w;
  logic [2:0] sb_id_w;
  logic       sb_rel_valid_w;
  logic [2:0] sb_rel_id_w;
  logic       sb_kill_ack_nc_w;
  logic [7:0] sb_holds_w;
  logic       sb_full_w, sb_barrier_w;
  logic       acmp_sb_grant_w, aecp_sb_grant_w;
  logic       acmp_sb_active_r, aecp_sb_active_r;
  logic       acmp_sb_done_pending_r, aecp_sb_done_pending_r;
  logic       sb_prefer_aecp_r;
  logic [2:0] acmp_sb_id_r, aecp_sb_id_r;
  logic [RXS_W_C-1:0] acmp_sb_slot_r, aecp_sb_slot_r;
  logic       aecp_eng_ready_w;

  KL_pp_scoreboard #(.MAX_HOLDS_P(8)) u_scoreboard (
      .clk_i              (clk_i),
      .rst_n              (rst_n),
      .adm_req_i          (sb_adm_req_w),
      .adm_class_i        (sb_adm_class_w),
      .adm_key_i          (sb_adm_key_w),
      .adm_gnt_o          (sb_gnt_w),
      .adm_id_o           (sb_id_w),
      .rel_valid_i        (sb_rel_valid_w),
      .rel_id_i           (sb_rel_id_w),
      .kill_valid_i       (1'b0),
      .kill_id_i          (3'd0),
      .kill_resp_queued_i (1'b0),
      .kill_ack_o         (sb_kill_ack_nc_w),
      .holds_o            (sb_holds_w),
      .full_o             (sb_full_w),
      .barrier_pend_o     (sb_barrier_w)
  );

  logic         trc_wr_valid_w;
  logic [127:0] trc_wr_data_w;
  logic [15:0]  trc_wr_count_w;
  logic         trc_rd_en_w;
  logic [7:0]   trc_rd_addr_w;
  logic [1:0]   trc_rd_lane_w;
  logic [31:0]  trc_rd_data_w;

  KL_pp_trace_ring #(.RECORDS_P(256), .RECORD_W_P(128)) u_trace (
      .clk_i      (clk_i),
      .rst_n      (rst_n),
      .wr_valid_i (trc_wr_valid_w),
      .wr_data_i  (trc_wr_data_w),
      .wr_count_o (trc_wr_count_w),
      .rd_en_i    (trc_rd_en_w),
      .rd_addr_i  (trc_rd_addr_w),
      .rd_lane_i  (trc_rd_lane_w),
      .rd_data_o  (trc_rd_data_w)
  );

  // Milan 5.4.5.3 CONTROLLER_AVAILABLE originator. The registry monitor
  // supplies one owner per registered-controller row; the generic originator
  // owns independent sequence counters, the one retry and response routing.
  logic        org_iss_ready_w, org_iss_gnt_w;
  logic [15:0] org_iss_seq_w;
  logic [3:0]  org_iss_id_w;
  logic        org_rt_valid_w, org_fail_valid_w;
  logic [3:0]  org_rt_owner_w, org_rt_id_nc_w;
  logic [3:0]  org_fail_owner_w, org_fail_id_nc_w;
  logic        org_send_valid_w, org_resend_valid_w;
  logic [2:0]  org_send_slot_w, org_resend_slot_w;
  logic        org_hold_valid_w, org_release_valid_w;
  logic [2:0]  org_hold_slot_w, org_release_slot_w;
  logic [7:0]  org_withdraw_slot_mask_w;
  logic        org_arm_valid_w, org_arm_cancel_w;
  logic [TMR_AW_C-1:0] org_arm_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] org_arm_owner_w;
  logic [31:0] org_arm_deadline_w;
  logic [7:0]  org_rsp_ign_nc_w;
  logic [PP_CA_POOL_C-1:0] org_busy_nc_w;
  logic        ntfy_ca_cancel_valid_w;
  logic [3:0]  ntfy_ca_cancel_owner_w;

  logic        ca_txs_alloc_req_w, ca_txs_gnt_w;
  logic [TXS_W_C-1:0] ca_txs_gnt_slot_w, ca_txs_wr_slot_w;
  logic [TXA_W_C-1:0] ca_txs_wr_addr_w, ca_txs_wr_len_w;
  logic        ca_txs_wr_valid_w, ca_txs_wr_commit_w;
  logic        ca_txs_abort_w;
  logic [7:0]  ca_txs_wr_data_w;
  logic        ca_iss_valid_w;
  logic [3:0]  ca_iss_owner_w;
  logic [2:0]  ca_iss_slot_w;
  logic [111:0] ca_iss_key_w;
  logic [15:0] ca_iss_timeout_w;
  logic [TMR_AW_C-1:0] ca_iss_tmr_slot_w;
  logic        ca_issued_nc_w;
  logic [3:0]  ca_issued_owner_nc_w;
  logic        ca_cancel_release_valid_w;
  logic [TXS_W_C-1:0] ca_cancel_release_slot_w;

  KL_pp_originator #(
      .CA_POOL_P     (PP_CA_POOL_C),
      .PROBE_SLOTS_P (0),
      .INFLIGHT_P    (PP_CA_POOL_C),
      .KEY_W_P       (112),
      .TMR_SLOTS_P   (TMR_SLOTS_C)
  ) u_originator (
      .clk_i                 (clk_i),
      .rst_n                 (rst_n),
      .iss_valid_i           (ca_iss_valid_w),
      .iss_owner_i           (ca_iss_owner_w),
      .iss_tx_slot_i         (ca_iss_slot_w),
      .iss_key_i             (ca_iss_key_w),
      .iss_tmr_slot_i        (ca_iss_tmr_slot_w),
      .iss_timeout_ms_i      (ca_iss_timeout_w),
      .iss_ready_o           (org_iss_ready_w),
      .iss_gnt_o             (org_iss_gnt_w),
      .iss_seq_o             (org_iss_seq_w),
      .iss_id_o              (org_iss_id_w),
      .cancel_valid_i        (ntfy_ca_cancel_valid_w),
      .cancel_owner_i        (ntfy_ca_cancel_owner_w),
      .rsp_valid_i           (v_hdr_valid_w
                              && (v_hdr_protocol_w == 3'(PP_PROTO_AEM))
                              && (v_hdr_msg_type_w == 4'd1)
                              && (v_hdr_opcode_w == 16'h0003)
                              && (v_hdr_ctlr_eid_w == entity_id_i)),
      .rsp_seq_i             (v_hdr_seq_w),
      .rsp_key_i             ({v_hdr_target_eid_w, v_hdr_src_mac_w}),
      .rt_valid_o            (org_rt_valid_w),
      .rt_owner_o            (org_rt_owner_w),
      .rt_id_o               (org_rt_id_nc_w),
      .fail_valid_o          (org_fail_valid_w),
      .fail_owner_o          (org_fail_owner_w),
      .fail_id_o             (org_fail_id_nc_w),
      .send_valid_o          (org_send_valid_w),
      .send_slot_o           (org_send_slot_w),
      .resend_valid_o        (org_resend_valid_w),
      .resend_slot_o         (org_resend_slot_w),
      .send_accept_valid_i   (arb_gnt_w[LANE_ORIG_C]),
      .send_accept_slot_i    (laneq_org_r[0]),
      .hold_valid_o          (org_hold_valid_w),
      .hold_slot_o           (org_hold_slot_w),
      .release_valid_o       (org_release_valid_w),
      .release_slot_o        (org_release_slot_w),
      .withdraw_slot_mask_o  (org_withdraw_slot_mask_w),
      .tmr_arm_valid_o       (org_arm_valid_w),
      .tmr_arm_cancel_o      (org_arm_cancel_w),
      .tmr_arm_slot_o        (org_arm_slot_w),
      .tmr_arm_owner_o       (org_arm_owner_w),
      .tmr_arm_deadline_ms_o (org_arm_deadline_w),
      .now_ms_i              (now_ms_w),
      .exp_valid_i           (exp_valid_w),
      .exp_slot_i            (exp_slot_w),
      .exp_owner_i           (exp_owner_w),
      .rsp_ign_cnt_o         (org_rsp_ign_nc_w),
      .inflight_busy_o       (org_busy_nc_w)
  );

  KL_aecp_ca_originator #(
      .TMR_SLOTS_P    (TMR_SLOTS_C),
      .TMR_CA_BASE_P  (TMR_MAP_C.capool),
      .TX_STD_SLOTS_P (TX_STD_SLOTS_P),
      .TX_OVERSIZE_BYTES_P(TX_OVERSIZE_BYTES_P)
  ) u_ca_builder (
      .clk_i             (clk_i),
      .rst_n             (rst_n),
      .entity_id_i       (entity_id_i),
      .own_mac_i         (own_mac_i),
      .req_valid_i       (ntfy_ca_valid_w),
      .req_owner_i       (ntfy_ca_owner_w),
      .req_ctlr_eid_i    (ntfy_ca_eid_w),
      .req_mac_i         (ntfy_ca_mac_w),
      .req_ready_o       (ntfy_ca_ready_w),
      .cancel_valid_i    (ntfy_ca_cancel_valid_w),
      .cancel_owner_i    (ntfy_ca_cancel_owner_w),
      .cancel_release_valid_o(ca_cancel_release_valid_w),
      .cancel_release_slot_o(ca_cancel_release_slot_w),
      .issued_valid_o    (ca_issued_nc_w),
      .issued_owner_o    (ca_issued_owner_nc_w),
      .txs_alloc_req_o   (ca_txs_alloc_req_w),
      .txs_alloc_gnt_i   (ca_txs_gnt_w),
      .txs_alloc_slot_i  (ca_txs_gnt_slot_w),
      .txs_wr_slot_o     (ca_txs_wr_slot_w),
      .txs_wr_addr_o     (ca_txs_wr_addr_w),
      .txs_wr_valid_o    (ca_txs_wr_valid_w),
      .txs_wr_data_o     (ca_txs_wr_data_w),
      .txs_wr_commit_o   (ca_txs_wr_commit_w),
      .txs_wr_len_o      (ca_txs_wr_len_w),
      .txs_abort_o       (ca_txs_abort_w),
      .iss_valid_o       (ca_iss_valid_w),
      .iss_owner_o       (ca_iss_owner_w),
      .iss_tx_slot_o     (ca_iss_slot_w),
      .iss_key_o         (ca_iss_key_w),
      .iss_tmr_slot_o    (ca_iss_tmr_slot_w),
      .iss_timeout_ms_o  (ca_iss_timeout_w),
      .iss_ready_i       (org_iss_ready_w),
      .iss_gnt_i         (org_iss_gnt_w),
      .iss_seq_i         (org_iss_seq_w),
      .iss_id_i          (org_iss_id_w)
  );

  // =========================================================================
  // RX: validator + replicated slot pools
  // =========================================================================
  logic        v_mrp_valid_w, v_mrp_last_w;
  logic [7:0]  v_mrp_data_w;
  logic        v_alloc_req_w, v_alloc_gnt_w;
  logic [RXS_W_C-1:0] v_alloc_slot_w;
  logic        v_wr_valid_w, v_wr_last_w, v_wr_abort_w, v_wr_commit_w;
  logic [7:0]  v_wr_data_w;
  logic        v_hdr_valid_w;
  logic [2:0]  v_hdr_protocol_w;
  logic [3:0]  v_hdr_msg_type_w;
  logic [4:0]  v_hdr_status_w;
  logic [10:0] v_hdr_cdl_w;
  logic [47:0] v_hdr_src_mac_w;
  logic [63:0] v_hdr_ctlr_eid_w, v_hdr_target_eid_w;
  logic [15:0] v_hdr_seq_w, v_hdr_opcode_w;
  logic        v_hdr_u_w, v_hdr_cr_w;
  pp_operands_t v_hdr_operands_w;
  logic [2:0]  v_hdr_rx_slot_w;
  logic [15:0] cnt_rx_da_w, cnt_rx_ethertype_w, cnt_rx_subtype_w;
  logic [15:0] cnt_rx_version_w, cnt_rx_length_w;

  KL_pp_rx_validator #(
      .SLOTS_P (RX_SLOTS_P),
      .BYTES_P (RX_SLOT_BYTES_P)
  ) u_rx_validator (
      .clk_i                (clk_i),
      .rst_n                (rst_n),
      .rx_valid_i           (rx_valid_i),
      .rx_data_i            (rx_data_i),
      .rx_last_i            (rx_last_i),
      .own_mac_i            (own_mac_i),
      .mrp_valid_o          (v_mrp_valid_w),
      .mrp_data_o           (v_mrp_data_w),
      .mrp_last_o           (v_mrp_last_w),
      .alloc_req_o          (v_alloc_req_w),
      .alloc_gnt_i          (v_alloc_gnt_w),
      .alloc_slot_i         (v_alloc_slot_w),
      .wr_valid_o           (v_wr_valid_w),
      .wr_data_o            (v_wr_data_w),
      .wr_last_o            (v_wr_last_w),
      .wr_abort_o           (v_wr_abort_w),
      .wr_commit_o          (v_wr_commit_w),
      .hdr_valid_o          (v_hdr_valid_w),
      .hdr_protocol_o       (v_hdr_protocol_w),
      .hdr_msg_type_o       (v_hdr_msg_type_w),
      .hdr_status_o         (v_hdr_status_w),
      .hdr_cdl_o            (v_hdr_cdl_w),
      .hdr_src_mac_o        (v_hdr_src_mac_w),
      .hdr_controller_eid_o (v_hdr_ctlr_eid_w),
      .hdr_target_eid_o     (v_hdr_target_eid_w),
      .hdr_sequence_id_o    (v_hdr_seq_w),
      .hdr_u_o              (v_hdr_u_w),
      .hdr_cr_o             (v_hdr_cr_w),
      .hdr_opcode_o         (v_hdr_opcode_w),
      .hdr_operands_o       (v_hdr_operands_w),
      .hdr_rx_slot_o        (v_hdr_rx_slot_w),
      .rx_da_count_o        (cnt_rx_da_w),
      .rx_ethertype_count_o (cnt_rx_ethertype_w),
      .rx_subtype_count_o   (cnt_rx_subtype_w),
      .rx_version_count_o   (cnt_rx_version_w),
      .rx_length_count_o    (cnt_rx_length_w)
  );

  // ---- RX free-return queue: 4 clients -> one serialized broadcast --------
  // Each engine frees at most once per processed frame (many cycles apart),
  // so a 1-deep latch per client drains within 4 cycles; a same-client
  // overrun is counted, never silent.
  localparam int unsigned RXF_ADP_C  = 0;
  localparam int unsigned RXF_LSTN_C = 1;
  localparam int unsigned RXF_TKR_C  = 2;
  localparam int unsigned RXF_AECP_C = 3;   // the TOP-LEVEL pop face
  localparam int unsigned RXF_UCPU_C = 4;   // KL_aecp_engine
  localparam int unsigned RXF_MAAP_C = 5;   // KL_pp_maap (free-only: records are self-contained)
  localparam int unsigned RXF_N_C    = 6;

  logic [RXF_N_C-1:0]              rxf_vld_r;
  logic [RXF_N_C-1:0][RXS_W_C-1:0] rxf_slot_r;
  logic [15:0]                     rxf_drop_r;
  logic                            rxf_free_w;
  logic [RXS_W_C-1:0]              rxf_free_slot_w;
  logic [2:0]                      rxf_pick_ix_w;
  logic [RXF_N_C-1:0]              rxf_req_w;
  logic [RXF_N_C-1:0][RXS_W_C-1:0] rxf_req_slot_w;

  logic adp_rxs_free_w,  lstn_rxs_free_w,  tkr_rxs_free_w, aecp_rxs_free_w;
  logic [RXS_W_C-1:0] adp_rxs_free_slot_w, lstn_rxs_free_slot_w,
                      tkr_rxs_free_slot_w, aecp_rxs_free_slot_w;
  logic        maapeng_rxs_free_w;
  logic [2:0]  maapeng_rxs_free_slot_w;   // pp_pkg handle space (engine port)

  assign rxf_req_w      = {maapeng_rxs_free_w,
                           aecp_rxs_free_w, aecp_rxs_free_i, tkr_rxs_free_w,
                           lstn_rxs_free_w, adp_rxs_free_w};
  assign rxf_req_slot_w = {maapeng_rxs_free_slot_w[RXS_W_C-1:0],
                           aecp_rxs_free_slot_w, aecp_rxs_free_slot_i,
                           tkr_rxs_free_slot_w,
                           lstn_rxs_free_slot_w, adp_rxs_free_slot_w};

  always_comb begin : rxf_pick
    rxf_free_w      = 1'b0;
    rxf_pick_ix_w   = 3'd0;
    rxf_free_slot_w = '0;
    for (int unsigned i = 0; i < RXF_N_C; i++) begin
      if (!rxf_free_w && rxf_vld_r[i]) begin
        rxf_free_w      = 1'b1;
        rxf_pick_ix_w   = 3'(i);
        rxf_free_slot_w = rxf_slot_r[i];
      end
    end
  end

  always_ff @(posedge clk_i) begin : rxf_queue
    if (!rst_n) begin
      rxf_vld_r  <= '0;
      rxf_slot_r <= '0;
      rxf_drop_r <= 16'd0;
    end else begin
      // drain the picked entry (lowest valid index; broadcast this cycle)
      if (rxf_free_w) begin
        rxf_vld_r[rxf_pick_ix_w] <= 1'b0;
      end
      // capture new frees (a later assignment wins: a same-cycle refill of
      // the drained entry lands correctly)
      for (int unsigned i = 0; i < RXF_N_C; i++) begin
        if (rxf_req_w[i]) begin
          if (rxf_vld_r[i] && !(rxf_free_w && (rxf_pick_ix_w == 3'(i)))) begin
            if (rxf_drop_r != 16'hFFFF) rxf_drop_r <= rxf_drop_r + 16'd1;
          end else begin
            rxf_vld_r[i]  <= 1'b1;
            rxf_slot_r[i] <= rxf_req_slot_w[i];
          end
        end
      end
    end
  end

  // ---- the five lock-step pool replicas (see file banner): four readers
  // plus the ACMP steer prefetch below
  localparam int unsigned RXP_ADP_C   = 0;
  localparam int unsigned RXP_LSTN_C  = 1;
  localparam int unsigned RXP_TKR_C   = 2;
  localparam int unsigned RXP_AECP_C  = 3;   // the TOP-LEVEL pop face
  localparam int unsigned RXP_STEER_C = 4;
  //! KL_aecp_engine gets its OWN replica rather than sharing the pop face's:
  //! two readers on one port would silently interleave addresses mid-payload
  //! (the file banner's rule), and the pop face must keep working for an
  //! integrator that still uses it.
  localparam int unsigned RXP_UCPU_C  = 5;
  localparam int unsigned RXP_N_C     = 6;

  logic [RXP_N_C-1:0]              rxp_alloc_gnt_w;
  logic [RXP_N_C-1:0][RXS_W_C-1:0] rxp_alloc_slot_w;
  logic [RXP_N_C-1:0][RXS_W_C-1:0] rxp_rd_slot_w;
  logic [RXP_N_C-1:0][RXA_W_C-1:0] rxp_rd_addr_w;
  logic [RXP_N_C-1:0]              rxp_rd_en_w;
  logic [RXP_N_C-1:0][7:0]         rxp_rd_data_w;
  logic [RXP_N_C-1:0][RXL_W_C-1:0] rxp_slot_len_w;
  logic [RXP_N_C-1:0][$clog2(RX_SLOTS_P+1)-1:0] rxp_slots_free_w;
  logic [RXP_N_C-1:0][15:0]        rxp_overrun_w;

  for (genvar g = 0; g < RXP_N_C; g++) begin : g_rx_pool
    KL_pp_rx_slots #(
        .SLOTS_P (RX_SLOTS_P),
        .BYTES_P (RX_SLOT_BYTES_P)
    ) u_rx_slots (
        .clk_i              (clk_i),
        .rst_n              (rst_n),
        .alloc_req_i        (v_alloc_req_w),
        .alloc_gnt_o        (rxp_alloc_gnt_w[g]),
        .alloc_slot_o       (rxp_alloc_slot_w[g]),
        .wr_valid_i         (v_wr_valid_w),
        .wr_data_i          (v_wr_data_w),
        .wr_last_i          (v_wr_last_w),
        .wr_abort_i         (v_wr_abort_w),
        .wr_commit_i        (v_wr_commit_w),
        .rd_slot_i          (rxp_rd_slot_w[g]),
        .rd_addr_i          (rxp_rd_addr_w[g]),
        .rd_en_i            (rxp_rd_en_w[g]),
        .rd_data_o          (rxp_rd_data_w[g]),
        .slot_len_o         (rxp_slot_len_w[g]),
        .free_i             (rxf_free_w),
        .free_slot_i        (rxf_free_slot_w),
        .slots_free_o       (rxp_slots_free_w[g]),
        .rx_overrun_count_o (rxp_overrun_w[g])
    );
  end

  assign v_alloc_gnt_w  = rxp_alloc_gnt_w[RXP_ADP_C];
  assign v_alloc_slot_w = rxp_alloc_slot_w[RXP_ADP_C];

  assign aecp_rxs_rd_data_o  = rxp_rd_data_w[RXP_AECP_C];
  assign aecp_rxs_slot_len_o = rxp_slot_len_w[RXP_AECP_C];
  assign rxp_rd_slot_w[RXP_AECP_C] = aecp_rxs_rd_slot_i;
  assign rxp_rd_addr_w[RXP_AECP_C] = aecp_rxs_rd_addr_i;
  assign rxp_rd_en_w[RXP_AECP_C]   = aecp_rxs_rd_en_i;

  // =========================================================================
  // hdr-beat latch -> normalizer -> dispatch
  // =========================================================================
  // The validator emits a ONE-CYCLE parsed-header beat with wr_commit; the
  // normalizer's RX producer face holds until accepted. Frames are >= 26
  // wire bytes apart while the normalizer accepts within a 4-producer
  // round, so one holding register suffices; an overrun is counted.
  logic        hdr_vld_r;
  logic [2:0]  hdr_protocol_r;
  logic [3:0]  hdr_msg_type_r;
  logic [4:0]  hdr_status_r;
  logic [10:0] hdr_cdl_r;
  logic [47:0] hdr_src_mac_r;
  logic [63:0] hdr_ctlr_eid_r, hdr_target_eid_r;
  logic [15:0] hdr_seq_r, hdr_opcode_r;
  logic        hdr_u_r, hdr_cr_r;
  logic [63:0] hdr_operands_r;
  logic [2:0]  hdr_rx_slot_r;
  logic [15:0] hdr_drop_r;
  logic        nrm_rx_ready_w;

  always_ff @(posedge clk_i) begin : hdr_latch
    if (!rst_n) begin
      hdr_vld_r      <= 1'b0;
      hdr_protocol_r <= 3'd0;
      hdr_msg_type_r <= 4'd0;
      hdr_status_r   <= 5'd0;
      hdr_cdl_r      <= 11'd0;
      hdr_src_mac_r  <= 48'd0;
      hdr_ctlr_eid_r <= 64'd0;
      hdr_target_eid_r <= 64'd0;
      hdr_seq_r      <= 16'd0;
      hdr_opcode_r   <= 16'd0;
      hdr_u_r        <= 1'b0;
      hdr_cr_r       <= 1'b0;
      hdr_operands_r <= 64'd0;
      hdr_rx_slot_r  <= 3'd0;
      hdr_drop_r     <= 16'd0;
    end else begin
      if (hdr_vld_r && nrm_rx_ready_w) begin
        hdr_vld_r <= 1'b0;
      end
      if (v_hdr_valid_w) begin
        if (hdr_vld_r && !nrm_rx_ready_w) begin
          if (hdr_drop_r != 16'hFFFF) hdr_drop_r <= hdr_drop_r + 16'd1;
        end else begin
          hdr_vld_r        <= 1'b1;
          hdr_protocol_r   <= v_hdr_protocol_w;
          hdr_msg_type_r   <= v_hdr_msg_type_w;
          hdr_status_r     <= v_hdr_status_w;
          hdr_cdl_r        <= v_hdr_cdl_w;
          hdr_src_mac_r    <= v_hdr_src_mac_w;
          hdr_ctlr_eid_r   <= v_hdr_ctlr_eid_w;
          hdr_target_eid_r <= v_hdr_target_eid_w;
          hdr_seq_r        <= v_hdr_seq_w;
          hdr_opcode_r     <= v_hdr_opcode_w;
          hdr_u_r          <= v_hdr_u_w;
          hdr_cr_r         <= v_hdr_cr_w;
          hdr_operands_r   <= 64'(v_hdr_operands_w);
          hdr_rx_slot_r    <= v_hdr_rx_slot_w;
        end
      end
    end
  end

  // dispatch-ROM stub (banner): hazard class from protocol and the AECP
  // opcode until the P4 dispatch ROM lands. ACMP serializes as STREAM_CFG;
  // ADD/REMOVE_AUDIO_MAPPINGS serialize as MAP_CFG so the scoreboard applies
  // its class-wide MAP_CFG x STREAM_CFG exclusion. Other commands remain
  // read-only snapshots. The key spreads protocols apart where the hazard
  // matrix intentionally permits parallel execution.
  logic        hz_valid_nc_w;
  logic [2:0]  hz_protocol_w;
  logic [15:0] hz_opcode_w;
  logic [3:0]  hz_class_w;
  logic [15:0] hz_key_w;

  localparam logic [15:0] HZ_OP_ADD_AUDIO_MAP_C    = 16'h002C;
  localparam logic [15:0] HZ_OP_REMOVE_AUDIO_MAP_C = 16'h002D;

  always_comb begin : hz_stub
    unique case (hz_protocol_w)
      3'(PP_PROTO_ACMP): hz_class_w = 4'(PP_HZ_STREAM_CFG);
      3'(PP_PROTO_AEM): begin
        if ((hz_opcode_w == HZ_OP_ADD_AUDIO_MAP_C)
            || (hz_opcode_w == HZ_OP_REMOVE_AUDIO_MAP_C))
          hz_class_w = 4'(PP_HZ_MAP_CFG);
        else
          hz_class_w = 4'(PP_HZ_RO_SNAPSHOT);
      end
      default:           hz_class_w = 4'(PP_HZ_RO_SNAPSHOT);
    endcase
    hz_key_w = {13'd0, hz_protocol_w};
  end

  logic                  nrm_txn_valid_w;
  logic [PP_TXN_W_C-1:0] nrm_txn_w;
  logic                  nrm_txn_ready_w;
  logic nrm_tmr_ready_nc_w, nrm_self_ready_nc_w, nrm_mgmt_ready_nc_w;

  KL_pp_normalizer u_normalizer (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .now_ms_i            (now_ms_w),
      .budget_adp_ms_i     (BUDGET_ADP_MS_C),
      .budget_acmp_ms_i    (BUDGET_ACMP_MS_C),
      .budget_aecp_ms_i    (BUDGET_AECP_MS_C),
      .rx_valid_i          (hdr_vld_r),
      .rx_ready_o          (nrm_rx_ready_w),
      .rx_if_index_i       (2'd0),
      .rx_protocol_i       (hdr_protocol_r),
      .rx_msg_type_i       (hdr_msg_type_r),
      .rx_status_i         (hdr_status_r),
      .rx_cdl_i            (hdr_cdl_r),
      .rx_src_mac_i        (hdr_src_mac_r),
      .rx_controller_eid_i (hdr_ctlr_eid_r),
      .rx_target_eid_i     (hdr_target_eid_r),
      .rx_sequence_id_i    (hdr_seq_r),
      .rx_u_i              (hdr_u_r),
      .rx_cr_i             (hdr_cr_r),
      .rx_opcode_i         (hdr_opcode_r),
      .rx_operands_i       (hdr_operands_r),
      .rx_slot_i           (hdr_rx_slot_r),
      .hz_valid_o          (hz_valid_nc_w),
      .hz_protocol_o       (hz_protocol_w),
      .hz_opcode_o         (hz_opcode_w),
      .hz_class_i          (hz_class_w),
      .hz_key_i            (hz_key_w),
      .tmr_valid_i         (1'b0),                 // TIMER producer: P4
      .tmr_txn_i           ({PP_TXN_W_C{1'b0}}),
      .tmr_ready_o         (nrm_tmr_ready_nc_w),
      .self_valid_i        (1'b0),                 // SELF producer: P4 (CA)
      .self_txn_i          ({PP_TXN_W_C{1'b0}}),
      .self_ready_o        (nrm_self_ready_nc_w),
      .mgmt_valid_i        (1'b0),                 // MGMT producer: P4
      .mgmt_txn_i          ({PP_TXN_W_C{1'b0}}),
      .mgmt_ready_o        (nrm_mgmt_ready_nc_w),
      .txn_valid_o         (nrm_txn_valid_w),
      .txn_o               (nrm_txn_w),
      .txn_ready_i         (nrm_txn_ready_w)
  );

  logic                  adp_txn_valid_w, acmp_txn_valid_w;
  logic [PP_TXN_W_C-1:0] adp_txn_w, acmp_txn_w;
  logic                  adp_txn_ready_w, acmp_txn_ready_w;
  logic                  aecp_txn_valid_w, aecp_txn_ready_w;
  logic [PP_TXN_W_C-1:0] aecp_txn_w;
  logic                  maap_txn_valid_w, maap_txn_ready_w;
  logic [PP_TXN_W_C-1:0] maap_txn_w;
  logic [7:0]  disp_adp_level_w, disp_acmp_level_w, disp_aecp_level_w;
  logic [7:0]  disp_maap_level_nc_w;
  logic [15:0] disp_adp_stall_w, disp_acmp_stall_w, disp_aecp_stall_w;
  logic [15:0] disp_maap_stall_nc_w;

  KL_pp_dispatch u_dispatch (
      .clk_i              (clk_i),
      .rst_n              (rst_n),
      .enq_valid_i        (nrm_txn_valid_w),
      .enq_txn_i          (nrm_txn_w),
      .enq_ready_o        (nrm_txn_ready_w),
      .adp_txn_valid_o    (adp_txn_valid_w),
      .adp_txn_o          (adp_txn_w),
      .adp_txn_ready_i    (adp_txn_ready_w),
      .acmp_txn_valid_o   (acmp_txn_valid_w),
      .acmp_txn_o         (acmp_txn_w),
      .acmp_txn_ready_i   (acmp_txn_ready_w),
      .aecp_txn_valid_o   (aecp_txn_valid_w),
      .aecp_txn_o         (aecp_txn_w),
      //! The live scoreboard grants before either the engine or the optional
      //! top-level drain can pop this head.
      .aecp_txn_ready_i   (aecp_txn_ready_w),
      .maap_txn_valid_o   (maap_txn_valid_w),
      .maap_txn_o         (maap_txn_w),
      .maap_txn_ready_i   (maap_txn_ready_w),
      .adp_level_o        (disp_adp_level_w),
      .acmp_level_o       (disp_acmp_level_w),
      .aecp_level_o       (disp_aecp_level_w),
      .maap_level_o       (disp_maap_level_nc_w),
      .adp_stall_count_o  (disp_adp_stall_w),
      .acmp_stall_count_o (disp_acmp_stall_w),
      .aecp_stall_count_o (disp_aecp_stall_w),
      .maap_stall_count_o (disp_maap_stall_nc_w)
  );

  assign aecp_txn_valid_o = aecp_txn_valid_w && aecp_sb_grant_w;
  assign aecp_txn_o       = aecp_txn_w;

  // ---- ACMP pop steer (RECORDED SEAM): talker commands {0,2,4,12} to the
  // talker, everything else (BIND/UNBIND/GET_RX + probe responses) to the
  // listener. The validator's F03.4 extraction fills txn.target_eid with
  // the ACMPDU's @4 stream_id, while BOTH engines discriminate multicast
  // ACMP traffic on target_eid == the ADDRESSED entity id (listener_
  // entity_id @28 / talker_entity_id @20, PDU offsets). The steer therefore
  // PREFETCHES those eight bytes from its own pool replica and presents the
  // head with target_eid rewritten from the wire — the discriminator stays
  // wire-true, no engine or validator file is touched (doc conflict
  // reported; 03 §4 only says "as applicable").
  pp_txn_t acmp_head_w;
  pp_txn_t steer_txn_w;
  logic    acmp_is_tkr_w;
  logic    lstn_txn_ready_w, tkr_txn_ready_w;

  typedef enum logic [1:0] { PF_WAIT, PF_RD, PF_DONE } pf_state_e;
  pf_state_e   pf_st_r;
  logic [3:0]  pf_idx_r;
  logic [63:0] pf_eid_r;
  logic        pf_ready_w;

  assign acmp_head_w   = pp_txn_t'(acmp_txn_w);
  assign acmp_is_tkr_w = (acmp_head_w.msg_type == 4'd0)
                       || (acmp_head_w.msg_type == 4'd2)
                       || (acmp_head_w.msg_type == 4'd4)
                       || (acmp_head_w.msg_type == 4'd12);
  assign pf_ready_w = (pf_st_r == PF_DONE);

  // engines see the head only once the prefetch stands; their level-high
  // idle readies pop the dispatch head exactly at their consume cycle
  assign acmp_txn_ready_w = acmp_sb_grant_w && pf_ready_w
                          && (acmp_is_tkr_w ? tkr_txn_ready_w
                                            : lstn_txn_ready_w);

  assign rxp_rd_slot_w[RXP_STEER_C] = acmp_head_w.rx_slot[RXS_W_C-1:0];
  assign rxp_rd_addr_w[RXP_STEER_C] =
      RXA_W_C'((acmp_is_tkr_w ? 32'd20 : 32'd28) + 32'(pf_idx_r));
  assign rxp_rd_en_w[RXP_STEER_C]   = (pf_st_r == PF_RD) && (pf_idx_r < 4'd8);

  always_ff @(posedge clk_i) begin : steer_prefetch
    if (!rst_n) begin
      pf_st_r  <= PF_WAIT;
      pf_idx_r <= 4'd0;
      pf_eid_r <= 64'd0;
    end else begin
      unique case (pf_st_r)
        PF_WAIT: begin
          if (acmp_txn_valid_w) begin
            if (acmp_head_w.rx_slot == PP_SLOT_NULL_C) begin
              pf_eid_r <= acmp_head_w.target_eid;  // no payload: pass as-is
              pf_st_r  <= PF_DONE;
            end else begin
              pf_idx_r <= 4'd0;
              pf_st_r  <= PF_RD;
            end
          end
        end
        PF_RD: begin
          pf_idx_r <= pf_idx_r + 4'd1;
          if (pf_idx_r != 4'd0) begin     // sync read: byte k lands at k+1
            pf_eid_r <= {pf_eid_r[55:0], rxp_rd_data_w[RXP_STEER_C]};
          end
          if (pf_idx_r == 4'd8) begin
            pf_st_r <= PF_DONE;
          end
        end
        PF_DONE: begin
          if (acmp_txn_valid_w && acmp_txn_ready_w) begin
            pf_st_r <= PF_WAIT;           // head popped; next head refetches
          end
        end
        default: pf_st_r <= PF_WAIT;
      endcase
    end
  end

  always_comb begin : steer_head
    steer_txn_w            = acmp_head_w;
    steer_txn_w.target_eid = pf_eid_r;
  end

  // =========================================================================
  // engines: ADP, ACMP listener, ACMP talker
  // =========================================================================
  // ---- binding view (07 §4): realized as top-held registers driven by the
  // listener's A4/A9 discovery strobes, read as levels by the ADP engine.
  logic [N_STREAM_IN_P-1:0]        bound_r;
  logic [N_STREAM_IN_P-1:0][63:0]  bound_sid_r;
  logic [N_STREAM_IN_P-1:0][47:0]  bound_dmac_r;
  logic [N_STREAM_IN_P-1:0][11:0]  bound_vlan_r;
  logic [N_STREAM_IN_P-1:0][63:0]  bound_eid_r;

  logic        lstn_disc_arm_w, lstn_disc_disarm_w;
  logic [63:0] lstn_disc_eid_w;
  //! CLAMPED like the engine's own SINK_W_C (KL_pp_acmp_listener.sv:76):
  //! at N_STREAM_IN_P = 1, $clog2(1) = 0 and a bare $clog2-1:0 declares
  //! [-1:0]. The consumer elaborates this processor at N_STREAMS = 1 on the
  //! shipping AX7101 shape, so that is not a hypothetical corner.
  logic [SINK_IDX_W_C-1:0] lstn_act_sink_w;

  always_ff @(posedge clk_i) begin : binding_view
    if (!rst_n) begin
      bound_r      <= '0;
      bound_eid_r  <= '0;
      bound_sid_r  <= '0;
      bound_dmac_r <= '0;
      bound_vlan_r <= '0;
    end else begin
      if (lstn_disc_arm_w) begin
        bound_r[lstn_act_sink_w]     <= 1'b1;
        bound_eid_r[lstn_act_sink_w] <= lstn_disc_eid_w;
      end
      //! The A15 settle carries the stream's wire identity. Latch it beside
      //! the entity_id so a fabric can arm an RX filter from one coherent
      //! view instead of reconstructing it from the ACMPDU itself.
      if (lstn_act_settle_w) begin
        bound_sid_r [lstn_act_sink_w] <= lstn_act_settle_sid_w;
        bound_dmac_r[lstn_act_sink_w] <= lstn_act_settle_da_w;
        bound_vlan_r[lstn_act_sink_w] <= lstn_act_settle_vlan_w;
      end
      if (lstn_disc_disarm_w) begin
        bound_r[lstn_act_sink_w] <= 1'b0;
        //! CLEAR THE STREAM IDENTITY WITH THE BINDING. Leaving it behind is
        //! not a harmless stale debug value: acmp_bound_o is DEBOUNCED, so
        //! across an unbind+rebind it can stay high while these still name
        //! the PREVIOUS stream — and a fabric arms its RX filter, stream
        //! table and CRF receiver from them. Stale stream-X parameters must
        //! never describe stream Y (Milan §5.3.8.9).
        bound_sid_r [lstn_act_sink_w] <= 64'd0;
        bound_dmac_r[lstn_act_sink_w] <= 48'd0;
        bound_vlan_r[lstn_act_sink_w] <= 12'd0;
      end
    end
  end

  // ADP faces
  logic        adp_prng_req_w;
  logic [2:0]  adp_prng_kind_w;
  logic        adp_prng_busy_w, adp_prng_valid_w;
  logic        adp_arm_valid_w, adp_arm_cancel_w;
  logic [TMR_AW_C-1:0] adp_arm_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] adp_arm_owner_w;
  logic [31:0] adp_arm_deadline_w;
  logic        adp_txs_alloc_req_w, adp_txs_oversize_nc_w;
  logic [TXS_W_C-1:0] adp_txs_wr_slot_w;
  logic [TXA_W_C-1:0] adp_txs_wr_addr_w, adp_txs_wr_len_w;
  logic        adp_txs_wr_valid_w, adp_txs_wr_commit_w;
  logic [7:0]  adp_txs_wr_data_w;
  logic        adp_txreq_valid_w;
  logic [TXS_W_C-1:0] adp_txreq_slot_w;
  logic [0:0]  adp_txreq_if_nc_w;
  logic        adp_evt_valid_w, adp_evt_departed_w;
  logic [SINK_IDX_W_C-1:0] adp_evt_sink_w;  //! CLAMPED (KL_adp_engine SNK_W_C)
  logic [0:0]  adp_gm_tick_nc_w;
  logic [1:0]  adp_dbg_adv_state_w;
  //! not "nc" any more: this is the live available_index, published below.
  logic [31:0] adp_dbg_aidx_nc_w;
  logic [N_STREAM_IN_P-1:0] adp_dbg_tkdisc_nc_w;
  logic        adp_txs_gnt_w;
  logic [TXS_W_C-1:0] adp_txs_gnt_slot_w;

  KL_adp_engine #(
      .N_IF_P                (1),
      .N_SINK_P              (N_STREAM_IN_P),
      .TMR_SLOTS_P           (TMR_SLOTS_C),
      .TMR_SLOT_ADV_BASE_P   (TMR_ADP_ADV_BASE_C),
      .TMR_SLOT_NOADP_BASE_P (TMR_ADP_NOADP_BASE_C),
      .RX_SLOTS_P            (RX_SLOTS_P),
      .RX_BYTES_P            (RX_SLOT_BYTES_P),
      .TX_STD_SLOTS_P        (TX_STD_SLOTS_P),
      .TX_OVERSIZE_BYTES_P   (TX_OVERSIZE_BYTES_P)
  ) u_adp (
      .clk_i                 (clk_i),
      .rst_n                 (rst_n),
      .entity_enable_i       (entity_enable_i),
      .link_up_i             (link_up_i),
      .gm_change_i           (gm_change_i),
      .gm_id_i               (gm_id_i),
      .gptp_domain_i         (gptp_domain_i),
      .entity_id_i           (entity_id_i),
      .entity_model_id_i     (entity_model_id_i),
      .own_mac_i             (own_mac_i),
      .talker_sources_i      (talker_sources_i),
      .talker_caps_i         (talker_caps_i),
      .listener_sinks_i      (listener_sinks_i),
      .listener_caps_i       (listener_caps_i),
      .current_cfg_i         (current_cfg_i),
      .identify_index_i      (identify_index_i),
      .txn_valid_i           (adp_txn_valid_w),
      .txn_i                 (adp_txn_w),
      .txn_ready_o           (adp_txn_ready_w),
      .rxs_rd_slot_o         (rxp_rd_slot_w[RXP_ADP_C]),
      .rxs_rd_addr_o         (rxp_rd_addr_w[RXP_ADP_C]),
      .rxs_rd_en_o           (rxp_rd_en_w[RXP_ADP_C]),
      .rxs_rd_data_i         (rxp_rd_data_w[RXP_ADP_C]),
      .rxs_free_o            (adp_rxs_free_w),
      .rxs_free_slot_o       (adp_rxs_free_slot_w),
      .prng_draw_req_o       (adp_prng_req_w),
      .prng_draw_kind_o      (adp_prng_kind_w),
      .prng_draw_busy_i      (adp_prng_busy_w),
      .prng_draw_valid_i     (adp_prng_valid_w),
      .prng_draw_ms_i        (prng_ms_w),
      .now_ms_i              (now_ms_w),
      .tmr_arm_valid_o       (adp_arm_valid_w),
      .tmr_arm_cancel_o      (adp_arm_cancel_w),
      .tmr_arm_slot_o        (adp_arm_slot_w),
      .tmr_arm_owner_o       (adp_arm_owner_w),
      .tmr_arm_deadline_ms_o (adp_arm_deadline_w),
      .tmr_exp_valid_i       (exp_valid_w),
      .tmr_exp_slot_i        (exp_slot_w),
      .tmr_exp_owner_i       (exp_owner_w),
      .txs_alloc_req_o       (adp_txs_alloc_req_w),
      .txs_oversize_o        (adp_txs_oversize_nc_w),
      .txs_alloc_gnt_i       (adp_txs_gnt_w),
      .txs_alloc_slot_i      (adp_txs_gnt_slot_w),
      .txs_wr_slot_o         (adp_txs_wr_slot_w),
      .txs_wr_addr_o         (adp_txs_wr_addr_w),
      .txs_wr_valid_o        (adp_txs_wr_valid_w),
      .txs_wr_data_o         (adp_txs_wr_data_w),
      .txs_wr_commit_o       (adp_txs_wr_commit_w),
      .txs_wr_len_o          (adp_txs_wr_len_w),
      .txreq_valid_o         (adp_txreq_valid_w),
      .txreq_slot_o          (adp_txreq_slot_w),
      .txreq_if_o            (adp_txreq_if_nc_w),
      .bound_i               (bound_r),
      .bound_talker_eid_i    (bound_eid_r),
      .evt_valid_o           (adp_evt_valid_w),
      .evt_departed_o        (adp_evt_departed_w),
      .evt_sink_o            (adp_evt_sink_w),
      .gm_changed_tick_o     (adp_gm_tick_nc_w),
      .dbg_adv_state_o       (adp_dbg_adv_state_w),
      .dbg_avail_index_o     (adp_dbg_aidx_nc_w),
      .dbg_tk_discovered_o   (adp_dbg_tkdisc_nc_w)
  );

  // ACMP listener faces
  logic        lstn_evt_tk_valid_w, lstn_evt_tk_ready_w;
  logic [1:0]  lstn_evt_tk_kind_w;
  logic        lstn_evt_tk_failed_w;
  logic [15:0] lstn_evt_tk_sink_w;
  logic        pre_valid_w, pre_ready_w;
  logic [15:0] pre_sink_w, pre_talker_uid_w;
  logic [63:0] pre_talker_eid_w, pre_ctlr_eid_w;
  logic        pre_sw_w, pre_started_w;
  logic        lstn_arm_valid_w, lstn_arm_cancel_w;
  logic [TMR_AW_C-1:0] lstn_arm_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] lstn_arm_owner_w;
  logic [31:0] lstn_arm_deadline_w;
  logic        lstn_draw_req_w;
  logic [2:0]  lstn_draw_kind_w;
  logic        lstn_draw_busy_w, lstn_draw_valid_w;
  logic        lstn_txs_alloc_req_w, lstn_txs_oversize_nc_w;
  logic [TXS_W_C-1:0] lstn_txs_wr_slot_w;
  logic [TXA_W_C-1:0] lstn_txs_wr_addr_w, lstn_txs_wr_len_w;
  logic        lstn_txs_wr_valid_w, lstn_txs_wr_commit_w;
  logic [7:0]  lstn_txs_wr_data_w;
  logic        lstn_txreq_valid_w;
  logic [TXS_W_C-1:0] lstn_txreq_slot_w;
  logic        lstn_act_settle_w, lstn_act_teardown_w;
  logic [63:0] lstn_act_settle_sid_w;
  logic [47:0] lstn_act_settle_da_w;
  logic [11:0] lstn_act_settle_vlan_w;
  logic        lstn_act_nvm_nc_w, lstn_act_nvm_set_nc_w, lstn_act_notify_nc_w;
  logic        lstn_dbg_busy_nc_w;
  logic        lstn_recwr_w;
  logic [SINK_IDX_W_C-1:0] lstn_recwr_sink_w;  //! CLAMPED (see SINK_IDX_W_C)
  logic [pp_acmp_pkg::ACMP_REC_W_C-1:0] lstn_recwr_rec_w;
  logic        lstn_txs_gnt_w;
  logic [TXS_W_C-1:0] lstn_txs_gnt_slot_w;

  //! the started/stopped handshake: KL_aecp_engine raises it from a
  //! START/STOP_STREAMING µprogram, KL_pp_acmp_listener owns the bit.
  logic        strm_set_valid_w, strm_set_val_w, strm_set_ready_w;
  logic        strm_set_error_w;
  logic [15:0] strm_set_index_w;
  //! out-of-range started/stopped requests dropped by the record walker.
  //! Reads a permanent 0 unless the descriptor image and this shape disagree.
  //!
  //! IT STOPS HERE, deliberately, and that is a limitation not a feature:
  //! nothing at this level reads it, so on silicon it is unreadable - not by
  //! a CSR, not by a bring-up probe. The arm it counts is driven and graded
  //! in tb/acmp_listener (S1n), which is what makes it more than a comment;
  //! carrying it to a register would be a register-map change for a counter
  //! whose only legitimate value is zero. If that arm ever fires on real
  //! hardware, this is the wire to bring out.
  logic [15:0] lstn_strq_drop_w;
  //! Milan Table 5.22: a started/stopped change pushes a GET_STREAM_INFO
  //! unsolicited notification. Issue #69 owns the trigger SET; this is the
  //! one trigger that only exists because START/STOP_STREAMING landed.
  logic        lstn_act_strt_chg_w;
  logic        lstn_act_strt_cmd_chg_w;

  KL_pp_acmp_listener #(
      .N_SINKS_P           (N_STREAM_IN_P),
      .TROM_HEX_P          (TROM_HEX_P),
      .RX_SLOTS_P          (RX_SLOTS_P),
      .RX_SLOT_BYTES_P     (RX_SLOT_BYTES_P),
      .TX_STD_SLOTS_P      (TX_STD_SLOTS_P),
      .TX_OVERSIZE_BYTES_P (TX_OVERSIZE_BYTES_P),
      .TMR_SLOT_AW_P       (TMR_AW_C),
      .TMR_BASE_SLOT_P     (TMR_LSTN_BASE_C),
      .TMR_OWNER_BASE_P    (32),
      .STRM_TIMEOUT_CYC_P  (DESC_MEM_TMO_CYC_P)
  ) u_listener (
      .clk_i                 (clk_i),
      .rst_n                 (rst_n),
      .entity_id_i           (entity_id_i),
      .txn_valid_i           (acmp_txn_valid_w && acmp_sb_grant_w && pf_ready_w
                              && !acmp_is_tkr_w),
      .txn_i                 (steer_txn_w),
      .txn_ready_o           (lstn_txn_ready_w),
      .evt_tk_valid_i        (lstn_evt_tk_valid_w),
      .evt_tk_kind_i         (lstn_evt_tk_kind_w),
      .evt_tk_failed_i       (lstn_evt_tk_failed_w),
      .evt_tk_sink_i         (lstn_evt_tk_sink_w),
      .evt_tk_ready_o        (lstn_evt_tk_ready_w),
      .pre_valid_i           (pre_valid_w),
      .pre_sink_i            (pre_sink_w),
      .pre_talker_eid_i      (pre_talker_eid_w),
      .pre_talker_uid_i      (pre_talker_uid_w),
      .pre_ctlr_eid_i        (pre_ctlr_eid_w),
      .pre_sw_i              (pre_sw_w),
      .pre_started_i         (pre_started_w),
      .strm_set_valid_i      (strm_set_valid_w),
      .strm_set_sink_i       (strm_set_index_w),
      .strm_set_val_i        (strm_set_val_w),
      .strm_set_ready_o      (strm_set_ready_w),
      .strm_set_error_o      (strm_set_error_w),
      .strm_started_o        (aecp_strm_started_o),
      .dbg_strq_drop_o       (lstn_strq_drop_w),
      .act_strt_chg_o        (lstn_act_strt_chg_w),
      .act_strt_cmd_chg_o    (lstn_act_strt_cmd_chg_w),
      .pre_ready_o           (pre_ready_w),
      .now_ms_i              (now_ms_w),
      .tmr_arm_valid_o       (lstn_arm_valid_w),
      .tmr_arm_cancel_o      (lstn_arm_cancel_w),
      .tmr_arm_slot_o        (lstn_arm_slot_w),
      .tmr_arm_owner_o       (lstn_arm_owner_w),
      .tmr_arm_deadline_ms_o (lstn_arm_deadline_w),
      .tmr_exp_valid_i       (exp_valid_w),
      .tmr_exp_slot_i        (exp_slot_w),
      .tmr_exp_owner_i       (exp_owner_w),
      .draw_req_o            (lstn_draw_req_w),
      .draw_kind_o           (lstn_draw_kind_w),
      .draw_busy_i           (lstn_draw_busy_w),
      .draw_valid_i          (lstn_draw_valid_w),
      .draw_ms_i             (prng_ms_w),
      .rxs_rd_slot_o         (rxp_rd_slot_w[RXP_LSTN_C]),
      .rxs_rd_addr_o         (rxp_rd_addr_w[RXP_LSTN_C]),
      .rxs_rd_en_o           (rxp_rd_en_w[RXP_LSTN_C]),
      .rxs_rd_data_i         (rxp_rd_data_w[RXP_LSTN_C]),
      .rxs_free_o            (lstn_rxs_free_w),
      .rxs_free_slot_o       (lstn_rxs_free_slot_w),
      .txs_alloc_req_o       (lstn_txs_alloc_req_w),
      .txs_oversize_o        (lstn_txs_oversize_nc_w),
      .txs_alloc_gnt_i       (lstn_txs_gnt_w),
      .txs_alloc_slot_i      (lstn_txs_gnt_slot_w),
      .txs_wr_slot_o         (lstn_txs_wr_slot_w),
      .txs_wr_addr_o         (lstn_txs_wr_addr_w),
      .txs_wr_valid_o        (lstn_txs_wr_valid_w),
      .txs_wr_data_o         (lstn_txs_wr_data_w),
      .txs_wr_commit_o       (lstn_txs_wr_commit_w),
      .txs_wr_len_o          (lstn_txs_wr_len_w),
      .txreq_valid_o         (lstn_txreq_valid_w),
      .txreq_slot_o          (lstn_txreq_slot_w),
      //! the 5.5.2.4 lock check reads the SAME lock KL_aecp_notify keeps
      //! for the AECP path - one holder, two gates
      .lock_held_i           (ntfy_lock_held_w),
      .lock_ctlr_i           (ntfy_lock_ctlr_w),
      .act_settle_o          (lstn_act_settle_w),
      .act_settle_sid_o      (lstn_act_settle_sid_w),
      .act_settle_da_o       (lstn_act_settle_da_w),
      .act_settle_vlan_o     (lstn_act_settle_vlan_w),
      .act_teardown_o        (lstn_act_teardown_w),
      .act_disc_arm_o        (lstn_disc_arm_w),
      .act_disc_talker_eid_o (lstn_disc_eid_w),
      .act_disc_disarm_o     (lstn_disc_disarm_w),
      .act_nvm_o             (lstn_act_nvm_nc_w),
      .act_nvm_set_o         (lstn_act_nvm_set_nc_w),
      .act_notify_o          (lstn_act_notify_nc_w),
      .act_sink_o            (lstn_act_sink_w),
      .dbg_busy_o            (lstn_dbg_busy_nc_w),
      .dbg_recwr_o           (lstn_recwr_w),
      .dbg_recwr_sink_o      (lstn_recwr_sink_w),
      .dbg_recwr_rec_o       (lstn_recwr_rec_w)
  );

  // ACMP talker faces
  logic        tkr_resp_valid_w;
  logic [3:0]  tkr_resp_msg_type_w;
  logic [4:0]  tkr_resp_status_w;
  logic [63:0] tkr_resp_sid_w, tkr_resp_ctlr_w, tkr_resp_tkeid_w,
               tkr_resp_lseid_w;
  logic [15:0] tkr_resp_tkuid_w, tkr_resp_lsuid_w, tkr_resp_cc_w,
               tkr_resp_seq_w, tkr_resp_flags_w, tkr_resp_vlan_w;
  logic [47:0] tkr_resp_da_w;
  logic [1:0]  tkr_resp_if_nc_w;
  logic [N_STREAM_OUT_P-1:0] tkr_declaring_w;
  logic        tkr_gate_open_w, tkr_gate_close_w;
  //! CLAMPED to match KL_acmp_talker's own SRC_W_C (:95-96). A fixed [2:0]
  //! only happens to be right at N_STREAM_OUT_P = 8; at any other shape it
  //! is a width mismatch against the engine port it connects to.
  logic [SRC_IDX_W_C-1:0] tkr_gate_src_w;
  logic [63:0] tkr_gate_sid_w;
  logic [47:0] tkr_gate_da_w;
  logic [11:0] tkr_gate_vlan_w;
  logic        tkr_arm_valid_w, tkr_arm_cancel_w;
  logic [TMR_AW_C-1:0] tkr_arm_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] tkr_arm_owner_w;
  logic [31:0] tkr_arm_deadline_w;
  logic        tkr_draw_req_w;
  logic [2:0]  tkr_draw_kind_w;
  logic        tkr_draw_busy_w, tkr_draw_valid_w;

  // talker-side maap face (steered below between the top ports and the
  // internal engine; 02 SS4.2 / 11)
  logic                    tkr_maap_req_valid_w, tkr_maap_req_ready_w;
  logic                    tkr_maap_req_release_w;
  logic [SRC_IDX_W_C-1:0]  tkr_maap_req_src_w;
  logic                    tkr_maap_rsp_valid_w, tkr_maap_rsp_ok_w;
  logic [47:0]             tkr_maap_rsp_da_w;
  logic                    tkr_maap_confl_valid_w;
  logic [SRC_IDX_W_C-1:0]  tkr_maap_confl_src_w;
  logic                    tkr_maap_confl_ack_w;

  // SRP class-D lanes consumed by the talker + snapshot
  logic [2:0]  srp_class_a_prio_w;
  logic [11:0] srp_class_a_vid_w;
  logic        srp_domain_adopted_w;
  logic [N_STREAM_OUT_P-1:0][1:0]  srp_tk_decl_state_w;
  logic [N_STREAM_OUT_P-1:0][1:0]  srp_lstn_reg_state_w;
  logic [N_STREAM_OUT_P-1:0]       srp_active_w;
  logic [N_STREAM_OUT_P-1:0][7:0]  srp_src_fail_code_nc_w;
  logic [N_STREAM_OUT_P-1:0][63:0] srp_src_fail_bridge_nc_w;
  logic [N_STREAM_IN_P-1:0][1:0]   srp_tk_reg_state_w;
  logic [N_STREAM_IN_P-1:0][1:0]   srp_lstn_decl_state_w;
  logic [N_STREAM_IN_P-1:0][31:0]  srp_acc_latency_w;
  logic [N_STREAM_IN_P-1:0][7:0]   srp_snk_fail_code_w;
  logic [N_STREAM_IN_P-1:0][63:0]  srp_snk_fail_bridge_nc_w;
  logic [N_STREAM_OUT_P-1:0][31:0] srp_granted_slope_w;
  logic [N_STREAM_OUT_P-1:0]       srp_sr_admitted_w;
  logic [31:0] srp_sum_slope_w;
  logic        srp_over_limit_w;
  logic        srp_evt_domain_change_w;

  KL_acmp_talker #(
      .N_STREAM_OUT_P   (N_STREAM_OUT_P),
      .RX_SLOTS_P       (RX_SLOTS_P),
      .RX_SLOT_BYTES_P  (RX_SLOT_BYTES_P),
      .TMR_SLOTS_P      (TMR_SLOTS_C),
      .TMR_SLOT_BASE_P  (TMR_TKR_BASE_C),
      .TMR_OWNER_BASE_P (32'h50)
  ) u_talker (
      .clk_i                 (clk_i),
      .rst_n                 (rst_n),
      .own_entity_id_i       (entity_id_i),
      .cfg_src_en_i          (cfg_src_en_i),
      .cfg_src_iface_i       (cfg_src_iface_i),
      .cfg_stream_id_i       (cfg_stream_id_i),
      .srp_lsn_reg_state_i   (srp_lstn_reg_state_w),
      .srp_class_vid_i       (srp_class_a_vid_w),
      .srp_pcp_change_i      (srp_evt_domain_change_w),
      .txn_valid_i           (acmp_txn_valid_w && acmp_sb_grant_w && pf_ready_w
                              && acmp_is_tkr_w),
      .txn_i                 (PP_TXN_W_C'(steer_txn_w)),
      .txn_ready_o           (tkr_txn_ready_w),
      .rxs_rd_slot_o         (rxp_rd_slot_w[RXP_TKR_C]),
      .rxs_rd_addr_o         (rxp_rd_addr_w[RXP_TKR_C]),
      .rxs_rd_en_o           (rxp_rd_en_w[RXP_TKR_C]),
      .rxs_rd_data_i         (rxp_rd_data_w[RXP_TKR_C]),
      .rxs_slot_len_i        (rxp_slot_len_w[RXP_TKR_C]),
      .rxs_free_o            (tkr_rxs_free_w),
      .rxs_free_slot_o       (tkr_rxs_free_slot_w),
      .resp_valid_o          (tkr_resp_valid_w),
      .resp_msg_type_o       (tkr_resp_msg_type_w),
      .resp_status_o         (tkr_resp_status_w),
      .resp_stream_id_o      (tkr_resp_sid_w),
      .resp_controller_eid_o (tkr_resp_ctlr_w),
      .resp_talker_eid_o     (tkr_resp_tkeid_w),
      .resp_listener_eid_o   (tkr_resp_lseid_w),
      .resp_talker_uid_o     (tkr_resp_tkuid_w),
      .resp_listener_uid_o   (tkr_resp_lsuid_w),
      .resp_dest_mac_o       (tkr_resp_da_w),
      .resp_conn_count_o     (tkr_resp_cc_w),
      .resp_seq_id_o         (tkr_resp_seq_w),
      .resp_flags_o          (tkr_resp_flags_w),
      .resp_vlan_id_o        (tkr_resp_vlan_w),
      .resp_if_index_o       (tkr_resp_if_nc_w),
      // the maap face steers by cfg_maap_internal_i (port-group banner):
      // 0 = the top's own port group (the allocator lives in the fabric),
      // 1 = the internal KL_pp_maap engine under the same contract
      .maap_req_valid_o      (tkr_maap_req_valid_w),
      .maap_req_ready_i      (tkr_maap_req_ready_w),
      .maap_req_release_o    (tkr_maap_req_release_w),
      .maap_req_src_o        (tkr_maap_req_src_w),
      .maap_rsp_valid_i      (tkr_maap_rsp_valid_w),
      .maap_rsp_ok_i         (tkr_maap_rsp_ok_w),
      .maap_rsp_da_i         (tkr_maap_rsp_da_w),
      .maap_conflict_valid_i (tkr_maap_confl_valid_w),
      .maap_conflict_src_i   (tkr_maap_confl_src_w),
      .maap_conflict_ack_o   (tkr_maap_confl_ack_w),
      .declaring_o           (tkr_declaring_w),
      .gate_open_o           (tkr_gate_open_w),
      .gate_close_o          (tkr_gate_close_w),
      .gate_src_o            (tkr_gate_src_w),
      .gate_stream_id_o      (tkr_gate_sid_w),
      .gate_da_o             (tkr_gate_da_w),
      .gate_vlan_o           (tkr_gate_vlan_w),
      .now_ms_i              (now_ms_w),
      .tmr_arm_valid_o       (tkr_arm_valid_w),
      .tmr_arm_cancel_o      (tkr_arm_cancel_w),
      .tmr_arm_slot_o        (tkr_arm_slot_w),
      .tmr_arm_owner_o       (tkr_arm_owner_w),
      .tmr_arm_deadline_ms_o (tkr_arm_deadline_w),
      .tmr_exp_valid_i       (exp_valid_w),
      .tmr_exp_slot_i        (exp_slot_w),
      .tmr_exp_owner_i       (exp_owner_w),
      .prng_draw_req_o       (tkr_draw_req_w),
      .prng_draw_kind_o      (tkr_draw_kind_w),
      .prng_draw_busy_i      (tkr_draw_busy_w),
      .prng_draw_valid_i     (tkr_draw_valid_w),
      .prng_draw_ms_i        (prng_ms_w)
  );

  // =========================================================================
  // internal MAAP engine (11; IEEE 1722-2016 Annex B) + the seam steer
  // =========================================================================
  //! The engine always runs its RX pop (a parked queue would wedge the
  //! shared normalizer head — its banner), but its claim walk engages only
  //! while cfg_maap_internal_i (AND link) holds, so the disabled build
  //! transmits nothing and answers nothing: byte-identical to the landed
  //! external-only top.
  logic        maapeng_prng_req_w;
  logic [2:0]  maapeng_prng_kind_w;
  logic        maapeng_prng_busy_w, maapeng_prng_valid_w;
  logic        maapeng_arm_valid_w, maapeng_arm_cancel_w;
  logic [TMR_AW_C-1:0] maapeng_arm_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] maapeng_arm_owner_w;
  logic [31:0] maapeng_arm_deadline_w;
  logic        maapeng_txs_alloc_req_w, maapeng_txs_oversize_nc_w;
  logic        maapeng_txs_gnt_w;
  logic [TXS_W_C-1:0] maapeng_txs_gnt_slot_w;
  logic [TXS_W_C-1:0] maapeng_txs_wr_slot_w;
  logic [TXA_W_C-1:0] maapeng_txs_wr_addr_w, maapeng_txs_wr_len_w;
  logic        maapeng_txs_wr_valid_w, maapeng_txs_wr_commit_w;
  logic [7:0]  maapeng_txs_wr_data_w;
  logic        maapeng_txreq_valid_w, maapeng_txreq_ready_w;
  logic [TXS_W_C-1:0] maapeng_txreq_slot_w;
  logic        maapeng_alloc_valid_w, maapeng_alloc_ready_w;
  logic        maapeng_rsp_valid_w, maapeng_rsp_ok_w;
  logic [47:0] maapeng_rsp_da_w;
  logic        maapeng_confl_valid_w;
  logic [SRC_IDX_W_C-1:0] maapeng_confl_src_w;
  logic        maapeng_confl_ack_w;

  KL_pp_maap #(
      .N_SRC_P             (N_STREAM_OUT_P),
      .RX_SLOTS_P          (RX_SLOTS_P),
      .TMR_SLOTS_P         (TMR_SLOTS_C),
      .TMR_SLOT_BASE_P     (TMR_MAAP_BASE_C),
      .TMR_OWNER_BASE_P    (PP_OWN_MAAP_C),
      .TX_STD_SLOTS_P      (TX_STD_SLOTS_P),
      .TX_OVERSIZE_BYTES_P (TX_OVERSIZE_BYTES_P)
  ) u_maap (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .cfg_en_i            (cfg_maap_internal_i),
      .cfg_count_i         (cfg_maap_count_i),
      .cfg_seed_offset_i   (cfg_maap_seed_offset_i),
      .cfg_seed_valid_i    (cfg_maap_seed_valid_i),
      .own_mac_i           (own_mac_i),
      .link_up_i           (link_up_i),
      .txn_valid_i         (maap_txn_valid_w),
      .txn_i               (maap_txn_w),
      .txn_ready_o         (maap_txn_ready_w),
      .rxs_free_o          (maapeng_rxs_free_w),
      .rxs_free_slot_o     (maapeng_rxs_free_slot_w),
      .prng_draw_req_o     (maapeng_prng_req_w),
      .prng_draw_kind_o    (maapeng_prng_kind_w),
      .prng_draw_busy_i    (maapeng_prng_busy_w),
      .prng_draw_valid_i   (maapeng_prng_valid_w),
      .prng_draw_ms_i      (prng_ms_w),
      .now_ms_i            (now_ms_w),
      .tmr_arm_valid_o     (maapeng_arm_valid_w),
      .tmr_arm_cancel_o    (maapeng_arm_cancel_w),
      .tmr_arm_slot_o      (maapeng_arm_slot_w),
      .tmr_arm_owner_o     (maapeng_arm_owner_w),
      .tmr_arm_deadline_ms_o (maapeng_arm_deadline_w),
      .tmr_exp_valid_i     (exp_valid_w),
      .tmr_exp_slot_i      (exp_slot_w),
      .tmr_exp_owner_i     (exp_owner_w),
      .txs_alloc_req_o     (maapeng_txs_alloc_req_w),
      .txs_oversize_o      (maapeng_txs_oversize_nc_w),
      .txs_alloc_gnt_i     (maapeng_txs_gnt_w),
      .txs_alloc_slot_i    (maapeng_txs_gnt_slot_w),
      .txs_wr_slot_o       (maapeng_txs_wr_slot_w),
      .txs_wr_addr_o       (maapeng_txs_wr_addr_w),
      .txs_wr_valid_o      (maapeng_txs_wr_valid_w),
      .txs_wr_data_o       (maapeng_txs_wr_data_w),
      .txs_wr_commit_o     (maapeng_txs_wr_commit_w),
      .txs_wr_len_o        (maapeng_txs_wr_len_w),
      .txreq_valid_o       (maapeng_txreq_valid_w),
      .txreq_slot_o        (maapeng_txreq_slot_w),
      .txreq_ready_i       (maapeng_txreq_ready_w),
      .alloc_req_valid_i   (maapeng_alloc_valid_w),
      .alloc_req_ready_o   (maapeng_alloc_ready_w),
      .alloc_req_release_i (tkr_maap_req_release_w),
      .alloc_req_src_i     (tkr_maap_req_src_w),
      .alloc_rsp_valid_o   (maapeng_rsp_valid_w),
      .alloc_rsp_ok_o      (maapeng_rsp_ok_w),
      .alloc_rsp_da_o      (maapeng_rsp_da_w),
      .conflict_valid_o    (maapeng_confl_valid_w),
      .conflict_src_o      (maapeng_confl_src_w),
      .conflict_ack_i      (maapeng_confl_ack_w),
      .addr_o              (maap_addr_o),
      .addr_valid_o        (maap_addr_valid_o),
      .state_o             (maap_state_o),
      .conflicts_o         (maap_conflicts_o),
      .defends_o           (maap_defends_o)
  );

  //! the seam steer (quasi-static select, 02 SS2 rule 4): with the internal
  //! engine the top's port group is QUIESCED — req_valid 0, ack 0, every
  //! input ignored — so an external allocator left wired can neither answer
  //! nor ack on behalf of the engine
  assign tkr_maap_req_ready_w  = cfg_maap_internal_i ? maapeng_alloc_ready_w
                                                     : maap_req_ready_i;
  assign tkr_maap_rsp_valid_w  = cfg_maap_internal_i ? maapeng_rsp_valid_w
                                                     : maap_rsp_valid_i;
  assign tkr_maap_rsp_ok_w     = cfg_maap_internal_i ? maapeng_rsp_ok_w
                                                     : maap_rsp_ok_i;
  assign tkr_maap_rsp_da_w     = cfg_maap_internal_i ? maapeng_rsp_da_w
                                                     : maap_rsp_da_i;
  assign tkr_maap_confl_valid_w = cfg_maap_internal_i ? maapeng_confl_valid_w
                                                      : maap_conflict_valid_i;
  assign tkr_maap_confl_src_w  = cfg_maap_internal_i ? maapeng_confl_src_w
                                                     : maap_conflict_src_i;
  assign maapeng_alloc_valid_w = cfg_maap_internal_i ? tkr_maap_req_valid_w
                                                     : 1'b0;
  assign maapeng_confl_ack_w   = cfg_maap_internal_i ? tkr_maap_confl_ack_w
                                                     : 1'b0;
  assign maap_req_valid_o      = cfg_maap_internal_i ? 1'b0
                                                     : tkr_maap_req_valid_w;
  assign maap_req_release_o    = tkr_maap_req_release_w;
  assign maap_req_src_o        = tkr_maap_req_src_w;
  assign maap_conflict_ack_o   = cfg_maap_internal_i ? 1'b0
                                                     : tkr_maap_confl_ack_w;

  // =========================================================================
  // SRP engine + KL_mrp_strip (THE RECORDED SEAM)
  // =========================================================================
  logic        mrp_valid_w, mrp_last_w, mrp_msrp_w, mrp_ready_w;
  logic [7:0]  mrp_data_w;
  logic [15:0] mrp_drop_w;

  KL_mrp_strip u_mrp_strip (
      .clk_i        (clk_i),
      .rst_n        (rst_n),
      .in_valid_i   (v_mrp_valid_w),
      .in_data_i    (v_mrp_data_w),
      .in_last_i    (v_mrp_last_w),
      .out_valid_o  (mrp_valid_w),
      .out_data_o   (mrp_data_w),
      .out_last_o   (mrp_last_w),
      .out_msrp_o   (mrp_msrp_w),
      .out_ready_i  (mrp_ready_w),
      .drop_count_o (mrp_drop_w)
  );

  logic        srp_req_valid_w, srp_req_ready_w;
  logic [2:0]  srp_req_op_w;
  logic [7:0]  srp_req_index_w;
  logic [63:0] srp_req_sid_w;
  logic [47:0] srp_req_da_w;
  logic [11:0] srp_req_vid_w;
  logic [15:0] srp_req_mfs_w;
  logic [1:0]  srp_req_lstn_w;
  logic        srp_rsp_valid_w;
  logic [1:0]  srp_rsp_status_w;
  logic [31:0] srp_rsp_data_w;
  logic        srp_txs_alloc_req_w, srp_txs_oversize_nc_w;
  logic [TXS_W_C-1:0] srp_txs_wr_slot_w;
  logic [TXA_W_C-1:0] srp_txs_wr_addr_w, srp_txs_wr_len_w;
  logic        srp_txs_wr_valid_w, srp_txs_wr_commit_w;
  logic [7:0]  srp_txs_wr_data_w;
  logic        srp_txreq_valid_w;
  logic [TXS_W_C-1:0] srp_txreq_slot_w;
  logic        srp_txreq_ready_w;
  logic        srp_arm_valid_w, srp_arm_cancel_w;
  logic [TMR_AW_C-1:0] srp_arm_slot_w;
  logic [7:0]  srp_arm_owner_w;
  logic [31:0] srp_arm_deadline_w;
  logic        srp_draw_req_w;
  logic [2:0]  srp_draw_kind_w;
  logic        srp_draw_busy_w, srp_draw_valid_w;
  logic [N_STREAM_IN_P-1:0]  srp_evt_tk_reg_w, srp_evt_tk_unreg_w;
  logic [N_STREAM_OUT_P-1:0] srp_lstn_reg_change_w;
  logic [3:0]  srp_dbg_vid_active_w;
  logic        srp_dbg_vlan_err_nc_w, srp_dbg_adm_round_nc_w;
  logic        srp_dbg_pdu_done_nc_w, srp_dbg_pdu_ok_nc_w;
  logic        srp_dbg_pdu_malformed_nc_w;
  logic        srp_txs_gnt_w;
  logic [TXS_W_C-1:0] srp_txs_gnt_slot_w;

  KL_srp_top #(
      .N_SOURCES_P      (N_STREAM_OUT_P),
      .N_SINKS_P        (N_STREAM_IN_P),
      .DOM_DEF_VID_P    (SRP_DOM_DEF_VID_P),
      .TX_STD_BYTES_P   (576),
      .TX_OVERSIZE_BYTES_P (TX_OVERSIZE_BYTES_P),
      .SLOT_AW_P        (TMR_AW_C),
      .CAD_SLOT_BASE_P  (TMR_SRP_CAD_BASE_C),
      .CAD_OWNER_BASE_P (SRP_CAD_OWNER_C),
      .TK_SLOT_BASE_P   (TMR_SRP_TK_BASE_C),
      .TK_OWNER_BASE_P  (SRP_TK_OWNER_C),
      .LS_SLOT_BASE_P   (TMR_SRP_LS_BASE_C),
      .LS_OWNER_BASE_P  (SRP_LS_OWNER_C)
  ) u_srp (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .own_mac_i           (own_mac_i),
      .link_up_i           (link_up_i),
      .p2p_i               (p2p_i),
      .cfg_rank_i          (cfg_rank_i),
      .cfg_acc_lat_ns_i    (cfg_acc_lat_ns_i),
      .port_rate_bps_i     (port_rate_bps_i),
      .mrp_valid_i         (mrp_valid_w),
      .mrp_data_i          (mrp_data_w),
      .mrp_last_i          (mrp_last_w),
      .mrp_msrp_i          (mrp_msrp_w),
      .mrp_ready_o         (mrp_ready_w),
      .req_valid_i         (srp_req_valid_w),
      .req_ready_o         (srp_req_ready_w),
      .req_op_i            (srp_req_op_w),
      .req_index_i         (srp_req_index_w),
      .req_stream_id_i     (srp_req_sid_w),
      .req_da_i            (srp_req_da_w),
      .req_vid_i           (srp_req_vid_w),
      .req_max_frame_i     (srp_req_mfs_w),
      .req_max_interval_i  (16'd1),
      .req_lstn_state_i    (srp_req_lstn_w),
      .rsp_valid_o         (srp_rsp_valid_w),
      .rsp_status_o        (srp_rsp_status_w),
      .rsp_data_o          (srp_rsp_data_w),
      .alloc_req_o         (srp_txs_alloc_req_w),
      .oversize_o          (srp_txs_oversize_nc_w),
      .alloc_slot_i        (srp_txs_gnt_slot_w),
      .alloc_gnt_i         (srp_txs_gnt_w),
      .wr_slot_o           (srp_txs_wr_slot_w),
      .wr_addr_o           (srp_txs_wr_addr_w),
      .wr_valid_o          (srp_txs_wr_valid_w),
      .wr_data_o           (srp_txs_wr_data_w),
      .wr_commit_o         (srp_txs_wr_commit_w),
      .wr_len_o            (srp_txs_wr_len_w),
      .txreq_valid_o       (srp_txreq_valid_w),
      .txreq_slot_o        (srp_txreq_slot_w),
      .txreq_ready_i       (srp_txreq_ready_w),
      .now_ms_i            (now_ms_w),
      .arm_valid_o         (srp_arm_valid_w),
      .arm_cancel_o        (srp_arm_cancel_w),
      .arm_slot_o          (srp_arm_slot_w),
      .arm_owner_o         (srp_arm_owner_w),
      .arm_deadline_ms_o   (srp_arm_deadline_w),
      .exp_valid_i         (exp_valid_w),
      .exp_slot_i          (exp_slot_w),
      .draw_req_o          (srp_draw_req_w),
      .draw_kind_o         (srp_draw_kind_w),
      .draw_busy_i         (srp_draw_busy_w),
      .draw_valid_i        (srp_draw_valid_w),
      .draw_ms_i           (prng_ms_w),
      .evt_tk_registered_o   (srp_evt_tk_reg_w),
      .evt_tk_unregistered_o (srp_evt_tk_unreg_w),
      .lstn_reg_change_o     (srp_lstn_reg_change_w),
      .evt_domain_change_o   (srp_evt_domain_change_w),
      .class_a_prio_o      (srp_class_a_prio_w),
      .class_a_vid_o       (srp_class_a_vid_w),
      .domain_adopted_o    (srp_domain_adopted_w),
      .tk_decl_state_o     (srp_tk_decl_state_w),
      .lstn_reg_state_o    (srp_lstn_reg_state_w),
      .active_o            (srp_active_w),
      .src_fail_code_o     (srp_src_fail_code_nc_w),
      .src_fail_bridge_o   (srp_src_fail_bridge_nc_w),
      .tk_reg_state_o      (srp_tk_reg_state_w),
      .lstn_decl_state_o   (srp_lstn_decl_state_w),
      .acc_latency_o       (srp_acc_latency_w),
      .snk_fail_code_o     (srp_snk_fail_code_w),
      .snk_fail_bridge_o   (srp_snk_fail_bridge_nc_w),
      .granted_slope_bps_o (srp_granted_slope_w),
      .sr_admitted_o       (srp_sr_admitted_w),
      .sum_slope_bps_o     (srp_sum_slope_w),
      .over_limit_o        (srp_over_limit_w),
      .dbg_vid_active_o    (srp_dbg_vid_active_w),
      .dbg_vlan_err_o      (srp_dbg_vlan_err_nc_w),
      .dbg_adm_round_o     (srp_dbg_adm_round_nc_w),
      .dbg_pdu_done_o      (srp_dbg_pdu_done_nc_w),
      .dbg_pdu_ok_o        (srp_dbg_pdu_ok_nc_w),
      .dbg_pdu_malformed_o (srp_dbg_pdu_malformed_nc_w)
  );

  // ---- SRP service adapter: three one-deep producer stages (talker gate,
  // listener settle/teardown, external svc face) drained by fixed priority
  // into the single-outstanding class-B port. Engine-stage overruns are
  // counted; the svc stage backpressures via svc_ready_o instead.
  typedef struct packed {
    logic        from_svc;
    logic [2:0]  op;
    logic [7:0]  index;
    logic [63:0] sid;
    logic [47:0] da;
    logic [11:0] vid;
    logic [15:0] mfs;
    logic [1:0]  lstn;
  } srp_svcreq_t;

  srp_svcreq_t st_tk_r, st_ls_r, st_svc_r, inflight_r;
  logic        st_tk_vld_r, st_ls_vld_r, st_svc_vld_r;
  logic        inflight_vld_r;
  logic [15:0] svc_drop_r;

  assign svc_ready_o = !st_svc_vld_r;

  always_ff @(posedge clk_i) begin : srp_svc_adapter
    if (!rst_n) begin
      st_tk_r  <= '0;  st_tk_vld_r  <= 1'b0;
      st_ls_r  <= '0;  st_ls_vld_r  <= 1'b0;
      st_svc_r <= '0;  st_svc_vld_r <= 1'b0;
      inflight_r     <= '0;
      inflight_vld_r <= 1'b0;
      srp_req_valid_w <= 1'b0;
      svc_drop_r      <= 16'd0;
      svc_rsp_valid_o  <= 1'b0;
      svc_rsp_status_o <= 2'd0;
      svc_rsp_data_o   <= 32'd0;
    end else begin
      svc_rsp_valid_o <= 1'b0;

      // capture producers (mutually-exclusive strobes within each producer)
      if (tkr_gate_open_w || tkr_gate_close_w) begin
        if (st_tk_vld_r) begin
          if (svc_drop_r != 16'hFFFF) svc_drop_r <= svc_drop_r + 16'd1;
        end else begin
          st_tk_vld_r <= 1'b1;
          st_tk_r     <= '{from_svc: 1'b0,
                           op:    tkr_gate_open_w ? 3'd0 : 3'd1,
                           index: 8'(tkr_gate_src_w),
                           sid:   tkr_gate_sid_w,
                           da:    tkr_gate_da_w,
                           vid:   tkr_gate_vlan_w,
                           mfs:   cfg_tspec_max_frame_i,
                           lstn:  2'd0};
        end
      end
      if (lstn_act_settle_w || lstn_act_teardown_w) begin
        if (st_ls_vld_r) begin
          if (svc_drop_r != 16'hFFFF) svc_drop_r <= svc_drop_r + 16'd1;
        end else begin
          st_ls_vld_r <= 1'b1;
          st_ls_r     <= '{from_svc: 1'b0,
                           op:    lstn_act_settle_w ? 3'd2 : 3'd3,
                           index: 8'(lstn_act_sink_w),
                           sid:   lstn_act_settle_sid_w,
                           da:    lstn_act_settle_da_w,
                           vid:   lstn_act_settle_vlan_w,
                           mfs:   16'd0,
                           lstn:  2'd2};
        end
      end
      if (svc_valid_i && !st_svc_vld_r) begin
        st_svc_vld_r <= 1'b1;
        st_svc_r     <= '{from_svc: 1'b1,
                          op:    svc_op_i,
                          index: svc_index_i,
                          sid:   svc_stream_id_i,
                          da:    svc_da_i,
                          vid:   svc_vid_i,
                          mfs:   svc_max_frame_i,
                          lstn:  svc_lstn_state_i};
      end

      // issue: one outstanding request at a time
      if (!inflight_vld_r) begin
        if (st_tk_vld_r) begin
          inflight_r <= st_tk_r;  inflight_vld_r <= 1'b1;
          st_tk_vld_r <= 1'b0;    srp_req_valid_w <= 1'b1;
        end else if (st_ls_vld_r) begin
          inflight_r <= st_ls_r;  inflight_vld_r <= 1'b1;
          st_ls_vld_r <= 1'b0;    srp_req_valid_w <= 1'b1;
        end else if (st_svc_vld_r) begin
          inflight_r <= st_svc_r; inflight_vld_r <= 1'b1;
          st_svc_vld_r <= 1'b0;   srp_req_valid_w <= 1'b1;
        end
      end else begin
        if (srp_req_valid_w && srp_req_ready_w) begin
          srp_req_valid_w <= 1'b0;             // accepted; await response
        end
        if (srp_rsp_valid_w) begin
          inflight_vld_r <= 1'b0;
          if (inflight_r.from_svc) begin
            svc_rsp_valid_o  <= 1'b1;
            svc_rsp_status_o <= srp_rsp_status_w;
            svc_rsp_data_o   <= srp_rsp_data_w;
          end
        end
      end
    end
  end

  assign srp_req_op_w    = inflight_r.op;
  assign srp_req_index_w = inflight_r.index;
  assign srp_req_sid_w   = inflight_r.sid;
  assign srp_req_da_w    = inflight_r.da;
  assign srp_req_vid_w   = inflight_r.vid;
  assign srp_req_mfs_w   = inflight_r.mfs;
  assign srp_req_lstn_w  = inflight_r.lstn;

  // =========================================================================
  // NVM: shadow between the listener record shadow and KL_pp_nvm_port
  // =========================================================================
  logic        nvm_req_w, nvm_we_w, nvm_wvalid_w, nvm_wready_w;
  logic [7:0]  nvm_record_id_w, nvm_wdata_w, nvm_rdata_w;
  logic        nvm_rvalid_w, nvm_rready_w, nvm_busy_w, nvm_done_w, nvm_err_w;
  logic [N_STREAM_IN_P-1:0] nvm_dbg_valid_nc_w, nvm_dbg_touched_nc_w;

  KL_acmp_nvm_shadow #(
      .N_SINKS_P (N_STREAM_IN_P)
  ) u_nvm_shadow (
      .clk_i            (clk_i),
      .rst_n            (rst_n),
      .tick_i           (tick_ms_w),
      .restore_go_i     (restore_go_i),
      .restore_busy_o   (restore_busy_o),
      .restore_done_o   (restore_done_o),
      .restore_fail_o   (restore_fail_o),
      .restore_blank_o  (restore_blank_o),
      .alarm_o          (nvm_alarm_o),
      .cap_wr_i         (lstn_recwr_w),
      .cap_sink_i       (lstn_recwr_sink_w),
      .cap_rec_i        (lstn_recwr_rec_w),
      .pre_valid_o      (pre_valid_w),
      .pre_sink_o       (pre_sink_w),
      .pre_talker_eid_o (pre_talker_eid_w),
      .pre_talker_uid_o (pre_talker_uid_w),
      .pre_ctlr_eid_o   (pre_ctlr_eid_w),
      .pre_sw_o         (pre_sw_w),
      .pre_started_o    (pre_started_w),
      .pre_ready_i      (pre_ready_w),
      .nvm_req_o        (nvm_req_w),
      .nvm_we_o         (nvm_we_w),
      .nvm_record_id_o  (nvm_record_id_w),
      .nvm_wvalid_o     (nvm_wvalid_w),
      .nvm_wready_i     (nvm_wready_w),
      .nvm_wdata_o      (nvm_wdata_w),
      .nvm_rvalid_i     (nvm_rvalid_w),
      .nvm_rready_o     (nvm_rready_w),
      .nvm_rdata_i      (nvm_rdata_w),
      .nvm_busy_i       (nvm_busy_w),
      .nvm_done_i       (nvm_done_w),
      .nvm_err_i        (nvm_err_w),
      .dbg_dirty_o      (nvm_unflushed_o),
      .dbg_valid_o      (nvm_dbg_valid_nc_w),
      .dbg_touched_o    (nvm_dbg_touched_nc_w)
  );

  KL_pp_nvm_port u_nvm_port (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .nvm_req_i       (nvm_req_w),
      .nvm_we_i        (nvm_we_w),
      .nvm_record_id_i (nvm_record_id_w),
      .nvm_wvalid_i    (nvm_wvalid_w),
      .nvm_wready_o    (nvm_wready_w),
      .nvm_wdata_i     (nvm_wdata_w),
      .nvm_rvalid_o    (nvm_rvalid_w),
      .nvm_rready_i    (nvm_rready_w),
      .nvm_rdata_o     (nvm_rdata_w),
      .nvm_busy_o      (nvm_busy_w),
      .nvm_done_o      (nvm_done_w),
      .nvm_err_o       (nvm_err_w),
      .dev_req_o       (nvm_dev_req_o),
      .dev_gnt_i       (nvm_dev_gnt_i),
      .dev_op_o        (nvm_dev_op_o),
      .dev_region_o    (nvm_dev_region_o),
      .dev_offset_o    (nvm_dev_offset_o),
      .dev_len_o       (nvm_dev_len_o),
      .dev_wvalid_o    (nvm_dev_wvalid_o),
      .dev_wready_i    (nvm_dev_wready_i),
      .dev_wdata_o     (nvm_dev_wdata_o),
      .dev_rvalid_i    (nvm_dev_rvalid_i),
      .dev_rdata_i     (nvm_dev_rdata_i),
      .dev_rready_o    (nvm_dev_rready_o),
      .dev_busy_i      (nvm_dev_busy_i),
      .dev_done_i      (nvm_dev_done_i),
      .dev_err_i       (nvm_dev_err_i)
  );

  // =========================================================================
  // timer arm-port priority mux (banner)
  // =========================================================================
  // Eight engine arm faces feed ONE always-accepting arm port. Arms are
  // one-cycle strobes with no ready, so each face gets a 4-deep queue and a
  // fixed-priority drain: listener > talker > ADP > SRP > originator > MAAP
  // > notify (SM correctness first, cadence last; MAAP's ms-scale timers and
  // the notify block's 300 s / 60 s deadlines tolerate any drain latency).
  // Per-face order is preserved (each engine owns
  // disjoint slot ranges, so cross-face order is free); a queue overrun
  // drops the NEWEST arm and counts — never silent.
  localparam int unsigned ARM_N_C = 8;
  localparam int unsigned ARM_W_C = 1 + TMR_AW_C + PP_TIMER_OWNER_W_C + 32;

  logic [ARM_N_C-1:0]              armq_in_vld_w;
  logic [ARM_N_C-1:0][ARM_W_C-1:0] armq_in_w;
  logic [ARM_N_C-1:0][3:0][ARM_W_C-1:0] armq_r;
  logic [ARM_N_C-1:0][2:0]         armq_cnt_r;
  logic [15:0]                     arm_drop_r;

  assign armq_in_vld_w = {ntfy_mon_arm_valid_w, ntfy_arm_valid_w, maapeng_arm_valid_w,
                          org_arm_valid_w, srp_arm_valid_w, adp_arm_valid_w,
                          tkr_arm_valid_w, lstn_arm_valid_w};
  assign armq_in_w[0] = {lstn_arm_cancel_w, lstn_arm_slot_w,
                         lstn_arm_owner_w, lstn_arm_deadline_w};
  assign armq_in_w[1] = {tkr_arm_cancel_w, tkr_arm_slot_w,
                         tkr_arm_owner_w, tkr_arm_deadline_w};
  assign armq_in_w[2] = {adp_arm_cancel_w, adp_arm_slot_w,
                         adp_arm_owner_w, adp_arm_deadline_w};
  assign armq_in_w[3] = {srp_arm_cancel_w, srp_arm_slot_w,
                         srp_arm_owner_w, srp_arm_deadline_w};
  assign armq_in_w[4] = {org_arm_cancel_w, org_arm_slot_w,
                         org_arm_owner_w, org_arm_deadline_w};
  assign armq_in_w[5] = {maapeng_arm_cancel_w, maapeng_arm_slot_w,
                         maapeng_arm_owner_w, maapeng_arm_deadline_w};
  assign armq_in_w[6] = {ntfy_arm_cancel_w, ntfy_arm_slot_w,
                         ntfy_arm_owner_w, ntfy_arm_deadline_w};
  assign armq_in_w[7] = {ntfy_mon_arm_cancel_w, ntfy_mon_arm_slot_w,
                         ntfy_mon_arm_owner_w, ntfy_mon_arm_deadline_w};

  logic [ARM_N_C-1:0]      armq_pop_w;
  logic [ARM_N_C-1:0][2:0] armq_mid_w;    // count after the pop
  logic [ARM_N_C-1:0]      armq_push_ok_w;

  always_comb begin : arm_drain_pick
    armq_pop_w = '0;
    for (int unsigned i = 0; i < ARM_N_C; i++) begin
      if ((armq_pop_w == '0) && (armq_cnt_r[i] != 3'd0)) begin
        armq_pop_w[i] = 1'b1;
      end
    end
    for (int unsigned i = 0; i < ARM_N_C; i++) begin
      armq_mid_w[i]     = armq_cnt_r[i] - (armq_pop_w[i] ? 3'd1 : 3'd0);
      armq_push_ok_w[i] = armq_in_vld_w[i] && (armq_mid_w[i] != 3'd4);
    end
  end

  always_ff @(posedge clk_i) begin : arm_mux
    if (!rst_n) begin
      armq_r     <= '0;
      armq_cnt_r <= '0;
      arm_drop_r <= 16'd0;
      tmr_arm_valid_w    <= 1'b0;
      tmr_arm_cancel_w   <= 1'b0;
      tmr_arm_slot_w     <= '0;
      tmr_arm_owner_w    <= '0;
      tmr_arm_deadline_w <= 32'd0;
    end else begin
      tmr_arm_valid_w <= 1'b0;
      for (int unsigned i = 0; i < ARM_N_C; i++) begin
        if (armq_pop_w[i]) begin
          {tmr_arm_cancel_w, tmr_arm_slot_w, tmr_arm_owner_w,
           tmr_arm_deadline_w} <= armq_r[i][0];
          tmr_arm_valid_w      <= 1'b1;
          armq_r[i][0] <= armq_r[i][1];
          armq_r[i][1] <= armq_r[i][2];
          armq_r[i][2] <= armq_r[i][3];
        end
        // the push write goes past the shifted survivors: later assignment
        // to the same index wins, which is exactly the append position.
        // DECODED, not indexed: `armq_r[i][armq_mid_w[i][1:0]] <= ...` is a
        // dynamic part-write into the flattened queue vector, which yosys
        // lowers as a read-modify-write barrel shift over ALL of armq_r —
        // measured at 13,045 techmap $_MUX_ (about 7,400 mapped LUTs) the
        // cycle the sixth client landed. The equality-decoded write is the
        // same behavior as a 4-way enable per entry and costs a comparator
        // per entry instead.
        for (int unsigned e = 0; e < 4; e++) begin
          if (armq_push_ok_w[i] && (armq_mid_w[i][1:0] == 2'(e))) begin
            armq_r[i][e] <= armq_in_w[i];
          end
        end
        if (armq_in_vld_w[i] && !armq_push_ok_w[i]) begin
          if (arm_drop_r != 16'hFFFF) arm_drop_r <= arm_drop_r + 16'd1;
        end
        armq_cnt_r[i] <= armq_mid_w[i]
                       + (armq_push_ok_w[i] ? 3'd1 : 3'd0);
      end
    end
  end

  // =========================================================================
  // PRNG draw-port owner mux (banner)
  // =========================================================================
  // Six clients; a broadcast draw_valid would complete the WRONG client's
  // draw, so the mux latches one pending request per client, serves them by
  // fixed priority (listener > talker > ADP > SRP > MAAP), and routes
  // draw_valid exclusively to the owner. The shared busy shown to every
  // client is "some draw pending or in flight" — each client's own protocol
  // (issue on not-busy, then wait for valid) remains exactly what its own
  // suite proved.
  localparam int unsigned PRNG_N_C = 6;

  logic [PRNG_N_C-1:0]      pr_pend_r;
  logic [PRNG_N_C-1:0][2:0] pr_kind_r;
  logic                     pr_inflight_r;
  logic [2:0]               pr_owner_r;
  logic [PRNG_N_C-1:0]      pr_req_w;
  logic [PRNG_N_C-1:0][2:0] pr_kind_w;
  logic                     pr_any_pend_w;
  logic                     pr_busy_shared_w;

  assign pr_req_w  = {ntfy_prng_req_w, maapeng_prng_req_w, srp_draw_req_w, adp_prng_req_w,
                      tkr_draw_req_w, lstn_draw_req_w};
  assign pr_kind_w = {ntfy_prng_kind_w, maapeng_prng_kind_w, srp_draw_kind_w, adp_prng_kind_w,
                      tkr_draw_kind_w, lstn_draw_kind_w};
  assign pr_any_pend_w    = |pr_pend_r;
  assign pr_busy_shared_w = pr_inflight_r || pr_any_pend_w || prng_busy_w;

  assign lstn_draw_busy_w = pr_busy_shared_w;
  assign tkr_draw_busy_w  = pr_busy_shared_w;
  assign adp_prng_busy_w  = pr_busy_shared_w;
  assign srp_draw_busy_w  = pr_busy_shared_w;
  assign maapeng_prng_busy_w = pr_busy_shared_w;
  assign ntfy_prng_busy_w = pr_busy_shared_w;

  assign lstn_draw_valid_w = prng_valid_w && pr_inflight_r && (pr_owner_r == 3'd0);
  assign tkr_draw_valid_w  = prng_valid_w && pr_inflight_r && (pr_owner_r == 3'd1);
  assign adp_prng_valid_w  = prng_valid_w && pr_inflight_r && (pr_owner_r == 3'd2);
  assign srp_draw_valid_w  = prng_valid_w && pr_inflight_r && (pr_owner_r == 3'd3);
  assign maapeng_prng_valid_w = prng_valid_w && pr_inflight_r && (pr_owner_r == 3'd4);
  assign ntfy_prng_valid_w = prng_valid_w && pr_inflight_r && (pr_owner_r == 3'd5);

  always_ff @(posedge clk_i) begin : prng_mux
    if (!rst_n) begin
      pr_pend_r     <= '0;
      pr_kind_r     <= '0;
      pr_inflight_r <= 1'b0;
      pr_owner_r    <= 3'd0;
      prng_req_w    <= 1'b0;
      prng_kind_w   <= 3'd0;
    end else begin
      prng_req_w <= 1'b0;
      // capture requests — a client holding its req line while it owns the
      // in-flight draw must not queue a phantom second draw
      for (int unsigned i = 0; i < PRNG_N_C; i++) begin
        if (pr_req_w[i]
            && !(pr_inflight_r && (pr_owner_r == 3'(i)))) begin
          pr_pend_r[i] <= 1'b1;
          pr_kind_r[i] <= pr_kind_w[i];
        end
      end
      if (pr_inflight_r) begin
        if (prng_valid_w) pr_inflight_r <= 1'b0;
      end else if (!prng_busy_w && !prng_req_w) begin
        for (int unsigned i = 0; i < PRNG_N_C; i++) begin
          if (!pr_inflight_r && pr_pend_r[i]) begin
            prng_req_w    <= 1'b1;
            prng_kind_w   <= pr_kind_r[i];
            pr_owner_r    <= 3'(i);
            pr_pend_r[i]  <= 1'b0;
            pr_inflight_r <= 1'b1;
          end
        end
      end
    end
  end

  // =========================================================================
  // event router + consumer split (02 §5 catalog)
  // =========================================================================
  // Source map (banner), in this ORDER — which is the contract; the SIZES
  // are the shape, so every base below is DERIVED exactly like the F08.4
  // timer map. At the F01.5 8x8 default this is the historical numbering:
  // 0..7 SRP TK_ATTR_REGISTERED{sink} (payload bit 15 = Talker Failed at
  // strobe time), 8..15 SRP TK_ATTR_UNREGISTERED{sink}, 16/17 ADP
  // EVT_TK_DISCOVERED/DEPARTED{sink}, 18 DOMAIN_CHANGE, 19..26
  // LISTENER_REG_CHANGE{src}, 27 GM_CHANGE, 28 LINK edge — 29 sources. TK
  // sources (0..ADP_DEP) present to the ACMP listener's evt face; every
  // acked event is traced; non-TK sources trace-and-ack immediately.
  //
  // With literal indices this map aliased exactly as the timer map did: at
  // 9 sinks TK_ATTR_UNREGISTERED{sink 7} lands on the literal 16 that ADP
  // EVT_TK_DISCOVERED owns, and the router has no owner tag to tell them
  // apart — the ACMP listener would be handed a DISCOVERED it must treat as
  // an UNREGISTERED.
  localparam pp_evr_map_t EVR_MAP_C = pp_evr_map(N_STREAM_IN_P,
                                                 N_STREAM_OUT_P);
  localparam int unsigned EVR_TKREG_BASE_C  = EVR_MAP_C.tk_reg;    // SI sources
  localparam int unsigned EVR_TKUNR_BASE_C  = EVR_MAP_C.tk_unreg;  // SI sources
  localparam int unsigned EVR_ADP_DISC_C    = EVR_MAP_C.adp_disc;
  localparam int unsigned EVR_ADP_DEP_C     = EVR_MAP_C.adp_dep;
  localparam int unsigned EVR_DOMAIN_C      = EVR_MAP_C.domain;
  localparam int unsigned EVR_LSNCHG_BASE_C = EVR_MAP_C.lsn_chg;   // SO sources
  localparam int unsigned EVR_GM_C          = EVR_MAP_C.gm_chg;
  localparam int unsigned EVR_LINK_C        = EVR_MAP_C.link;
  localparam int unsigned EVR_N_SRC_C       = EVR_MAP_C.n_src;     // = 29 at 8x8
  localparam int unsigned EVR_SRC_W_C       = (EVR_N_SRC_C > 1)
                                              ? $clog2(EVR_N_SRC_C) : 1;

  logic [EVR_N_SRC_C-1:0]       evr_strobe_w;
  logic [EVR_N_SRC_C-1:0][15:0] evr_payload_w;
  logic                         evr_valid_w;
  logic [EVR_SRC_W_C-1:0]       evr_src_w;
  logic [15:0]        evr_pay_w;
  logic               evr_lost_w;
  logic               evr_ack_w;
  logic               link_q_r;

  always_ff @(posedge clk_i) begin : link_edge
    if (!rst_n) link_q_r <= 1'b0;
    else        link_q_r <= link_up_i;
  end

  always_comb begin : evr_sources
    evr_strobe_w  = '0;
    evr_payload_w = '0;
    for (int unsigned k = 0; k < N_STREAM_IN_P; k++) begin
      evr_strobe_w[EVR_TKREG_BASE_C + k]  = srp_evt_tk_reg_w[k];
      evr_payload_w[EVR_TKREG_BASE_C + k] = {(srp_tk_reg_state_w[k] == 2'd2),
                                             7'd0, 8'(k)};
      evr_strobe_w[EVR_TKUNR_BASE_C + k]  = srp_evt_tk_unreg_w[k];
      evr_payload_w[EVR_TKUNR_BASE_C + k] = {8'd0, 8'(k)};
    end
    evr_strobe_w[EVR_ADP_DISC_C]  = adp_evt_valid_w && !adp_evt_departed_w;
    evr_payload_w[EVR_ADP_DISC_C] = 16'(adp_evt_sink_w);
    evr_strobe_w[EVR_ADP_DEP_C]   = adp_evt_valid_w && adp_evt_departed_w;
    evr_payload_w[EVR_ADP_DEP_C]  = 16'(adp_evt_sink_w);
    evr_strobe_w[EVR_DOMAIN_C]    = srp_evt_domain_change_w;
    evr_payload_w[EVR_DOMAIN_C]   = {4'd0, srp_class_a_vid_w};
    for (int unsigned k = 0; k < N_STREAM_OUT_P; k++) begin
      evr_strobe_w[EVR_LSNCHG_BASE_C + k]  = srp_lstn_reg_change_w[k];
      evr_payload_w[EVR_LSNCHG_BASE_C + k] = {8'd0, 8'(k)};
    end
    evr_strobe_w[EVR_GM_C]    = gm_change_i;
    evr_payload_w[EVR_GM_C]   = 16'd0;
    evr_strobe_w[EVR_LINK_C]  = link_up_i != link_q_r;
    evr_payload_w[EVR_LINK_C] = {15'd0, link_up_i};
  end

  logic [EVR_SRC_W_C-1:0] evr_lost_src_w;
  logic [7:0]             evr_lost_cnt_nc_w;

  KL_pp_event_router #(
      .N_SRC_P     (EVR_N_SRC_C),
      .PAYLOAD_W_P (16)
  ) u_event_router (
      .clk_i         (clk_i),
      .rst_n         (rst_n),
      .src_strobe_i  (evr_strobe_w),
      .src_payload_i (evr_payload_w),
      .evt_valid_o   (evr_valid_w),
      .evt_src_o     (evr_src_w),
      .evt_payload_o (evr_pay_w),
      .evt_lost_o    (evr_lost_w),
      .evt_ack_i     (evr_ack_w),
      .lost_src_i    (evr_lost_src_w),
      .lost_count_o  (evr_lost_cnt_nc_w)
  );

  assign evr_lost_src_w = evr_src_w;   // thin: read the presented source

  logic evr_tk_sel_w;
  assign evr_tk_sel_w = evr_valid_w
                        && (evr_src_w <= EVR_SRC_W_C'(EVR_ADP_DEP_C));

  assign lstn_evt_tk_valid_w = evr_tk_sel_w;
  assign lstn_evt_tk_sink_w  = {8'd0, evr_pay_w[7:0]};
  assign lstn_evt_tk_failed_w = evr_pay_w[15];
  always_comb begin : evt_kind_map
    if (evr_src_w < EVR_SRC_W_C'(EVR_TKUNR_BASE_C)) begin
      lstn_evt_tk_kind_w = pp_acmp_pkg::TK_KIND_REG_C;
    end else if (evr_src_w < EVR_SRC_W_C'(EVR_ADP_DISC_C)) begin
      lstn_evt_tk_kind_w = pp_acmp_pkg::TK_KIND_UNREG_C;
    end else if (evr_src_w == EVR_SRC_W_C'(EVR_ADP_DISC_C)) begin
      lstn_evt_tk_kind_w = pp_acmp_pkg::TK_KIND_DISC_C;
    end else begin
      lstn_evt_tk_kind_w = pp_acmp_pkg::TK_KIND_DEP_C;
    end
  end

  assign evr_ack_w = evr_tk_sel_w ? lstn_evt_tk_ready_w
                                  : (evr_valid_w);      // non-TK: trace + ack

  // trace record: [127:96] now_ms, [95:88] source, [87:80] flags (bit 0 =
  // evt_lost), [79:64] payload, [63:0] reserved 0
  assign trc_wr_valid_w = evr_valid_w && evr_ack_w;
  assign trc_wr_data_w  = {now_ms_w, 8'(evr_src_w),
                           {7'd0, evr_lost_w}, evr_pay_w, 64'd0};

  // =========================================================================
  // talker response builder (banner)
  // =========================================================================
  // The stateless talker answers with F05.13 FIELDS; the wire wants a
  // 56-byte ACMPDU in a TX slot like the listener's. This builder latches
  // one response, allocates through the pool-access arbiter (client 3),
  // writes the PDU image bytes 0..55, commits len 56 and holds TX lane 5
  // until granted. A response arriving while one is being built is dropped
  // AND counted (bounded by design: the talker answers faster than 70
  // cycles only under a same-cycle dispatch storm the 4-slot pool already
  // forbids).
  typedef enum logic [2:0] {
    TKB_IDLE, TKB_ALLOC, TKB_WR, TKB_COMMIT, TKB_REQ
  } tkb_state_e;

  tkb_state_e  tkb_st_r;
  logic        tkb_pend_r;
  logic [3:0]  tkb_msg_r;
  logic [4:0]  tkb_status_r;
  logic [63:0] tkb_sid_r, tkb_ctlr_r, tkb_tkeid_r, tkb_lseid_r;
  logic [15:0] tkb_tkuid_r, tkb_lsuid_r, tkb_cc_r, tkb_seq_r, tkb_flags_r,
               tkb_vlan_r;
  logic [47:0] tkb_da_r;
  logic [15:0] tkb_drop_r;
  logic [TXS_W_C-1:0] tkb_slot_r;
  logic [5:0]  tkb_bidx_r;
  logic        tkb_alloc_req_w;
  logic        tkb_gnt_w;
  logic [TXS_W_C-1:0] tkb_gnt_slot_w;
  logic        tkb_lane_valid_r;
  logic        tkb_lane_gnt_w;
  logic [447:0] tkb_pdu_w;
  logic [7:0]   tkb_pdu_byte_w;

  assign tkb_pdu_w = {8'hFC, 4'h0, tkb_msg_r, tkb_status_r, 11'd44,
                      tkb_sid_r, tkb_ctlr_r, tkb_tkeid_r, tkb_lseid_r,
                      tkb_tkuid_r, tkb_lsuid_r, tkb_da_r, tkb_cc_r,
                      tkb_seq_r, tkb_flags_r, tkb_vlan_r, 16'h0000};
  assign tkb_pdu_byte_w  = tkb_pdu_w[(9'd440 - {tkb_bidx_r, 3'b000}) +: 8];
  assign tkb_alloc_req_w = (tkb_st_r == TKB_ALLOC);

  always_ff @(posedge clk_i) begin : tkb_engine
    if (!rst_n) begin
      tkb_st_r   <= TKB_IDLE;
      tkb_pend_r <= 1'b0;
      tkb_msg_r  <= 4'd0;   tkb_status_r <= 5'd0;
      tkb_sid_r  <= 64'd0;  tkb_ctlr_r <= 64'd0;
      tkb_tkeid_r <= 64'd0; tkb_lseid_r <= 64'd0;
      tkb_tkuid_r <= 16'd0; tkb_lsuid_r <= 16'd0;
      tkb_cc_r    <= 16'd0; tkb_seq_r   <= 16'd0;
      tkb_flags_r <= 16'd0; tkb_vlan_r  <= 16'd0;
      tkb_da_r    <= 48'd0;
      tkb_drop_r  <= 16'd0;
      tkb_slot_r  <= '0;
      tkb_bidx_r  <= 6'd0;
      tkb_lane_valid_r <= 1'b0;
    end else begin
      if (tkr_resp_valid_w) begin
        if (tkb_pend_r) begin
          if (tkb_drop_r != 16'hFFFF) tkb_drop_r <= tkb_drop_r + 16'd1;
        end else begin
          tkb_pend_r  <= 1'b1;
          tkb_msg_r   <= tkr_resp_msg_type_w;
          tkb_status_r <= tkr_resp_status_w;
          tkb_sid_r   <= tkr_resp_sid_w;
          tkb_ctlr_r  <= tkr_resp_ctlr_w;
          tkb_tkeid_r <= tkr_resp_tkeid_w;
          tkb_lseid_r <= tkr_resp_lseid_w;
          tkb_tkuid_r <= tkr_resp_tkuid_w;
          tkb_lsuid_r <= tkr_resp_lsuid_w;
          tkb_cc_r    <= tkr_resp_cc_w;
          tkb_seq_r   <= tkr_resp_seq_w;
          tkb_flags_r <= tkr_resp_flags_w;
          tkb_vlan_r  <= tkr_resp_vlan_w;
          tkb_da_r    <= tkr_resp_da_w;
        end
      end
      unique case (tkb_st_r)
        TKB_IDLE: begin
          if (tkb_pend_r) tkb_st_r <= TKB_ALLOC;
        end
        TKB_ALLOC: begin
          if (tkb_gnt_w) begin
            tkb_slot_r <= tkb_gnt_slot_w;
            tkb_bidx_r <= 6'd0;
            tkb_st_r   <= TKB_WR;
          end
        end
        TKB_WR: begin
          if (tkb_bidx_r == 6'd55) tkb_st_r <= TKB_COMMIT;
          else                     tkb_bidx_r <= tkb_bidx_r + 6'd1;
        end
        TKB_COMMIT: begin
          tkb_st_r         <= TKB_REQ;
          tkb_lane_valid_r <= 1'b1;
        end
        TKB_REQ: begin
          if (tkb_lane_gnt_w) begin
            tkb_lane_valid_r <= 1'b0;
            tkb_pend_r       <= 1'b0;
            tkb_st_r         <= TKB_IDLE;
          end
        end
        default: tkb_st_r <= TKB_IDLE;
      endcase
    end
  end

  // =========================================================================
  // AECP: the µCPU on the dispatch head + its descriptor store (06)
  // =========================================================================
  //! The seam this block closes: the AECP head used to be handed OUT through a
  //! pop face that nothing popped, so a validated, normalized AEM command
  //! reached the end of the pipeline and stopped there. KL_aecp_engine pops
  //! it, runs the 06 §8 µCPU against the 07 §3.3 model store in main memory,
  //! and puts a byte-exact AECPDU on TX lane 0 (LANE_AECP_SOL_C).
  logic [RXS_W_C-1:0]      aecp_eng_free_slot_w;
  logic                    aecp_txs_alloc_req_w, aecp_txs_oversize_w;
  logic [TXS_W_C-1:0]      aecp_txs_wr_slot_w;
  logic [TXA_W_C-1:0]      aecp_txs_wr_addr_w, aecp_txs_wr_len_w;
  logic                    aecp_txs_wr_valid_w, aecp_txs_wr_commit_w;
  logic [7:0]              aecp_txs_wr_data_w;
  logic                    aecp_txreq_valid_w, aecp_txreq_ready_w;
  logic                    aecp_txreq_uns_valid_w, aecp_txreq_uns_ready_w;
  logic [TXS_W_C-1:0]      aecp_txreq_slot_w;
  logic                    aecp_txs_gnt_w;
  logic [TXS_W_C-1:0]      aecp_txs_gnt_slot_w;
  // registry/lock face + unsolicited job face (engine <-> KL_aecp_notify)
  logic        aecp_rgy_req_w, aecp_rgy_state_w, aecp_rgy_tl_w, aecp_rgy_wait_w;
  logic [1:0]  aecp_rgy_op_w;
  logic [63:0] aecp_rgy_eid_w, aecp_rgy_data_w;
  logic [47:0] aecp_rgy_mac_w;
  logic        uns_valid_w, uns_done_w;
  logic [3:0]  uns_kind_w;
  logic [15:0] uns_dt_w, uns_di_w, uns_seq_w;
  logic [15:0] uns_arg0_w, uns_arg1_w;
  logic        uns_amap_remove_w, ntfy_amap_busy_w;
  logic [15:0] uns_amap_count_w;
  logic [63:0] uns_eid_w;
  logic [47:0] uns_mac_w;
  logic        ntfy_lock_held_w;
  logic [63:0] ntfy_lock_ctlr_w;
  logic        ntfy_arm_valid_w, ntfy_arm_cancel_w;
  logic [TMR_AW_C-1:0] ntfy_arm_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] ntfy_arm_owner_w;
  logic [31:0] ntfy_arm_deadline_w;
  logic        ntfy_mon_arm_valid_w, ntfy_mon_arm_cancel_w;
  logic [TMR_AW_C-1:0] ntfy_mon_arm_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] ntfy_mon_arm_owner_w;
  logic [31:0] ntfy_mon_arm_deadline_w;
  logic        ntfy_prng_req_w, ntfy_prng_busy_w, ntfy_prng_valid_w;
  logic [2:0]  ntfy_prng_kind_w;
  logic        ntfy_ca_valid_w, ntfy_ca_ready_w;
  logic [3:0]  ntfy_ca_owner_w;
  logic [63:0] ntfy_ca_eid_w;
  logic [47:0] ntfy_ca_mac_w;
  logic [7:0]  ntfy_reg_cnt_nc_w, ntfy_coalesce_nc_w;
  logic [15:0] ntfy_uns_cnt_nc_w;
  logic [N_STREAM_IN_P-1:0]  ntfy_stri_in_w;
  logic [N_STREAM_OUT_P-1:0] ntfy_stri_out_w;

  //! Publish the notification block's authoritative lock level so local
  //! non-ATDECC mapping paths can enforce Milan 5.4.2.27 and 5.4.2.28.
  assign aecp_lock_held_o = ntfy_lock_held_w;

  always_comb begin : stri_events
    ntfy_stri_in_w  = '0;
    ntfy_stri_out_w = '0;
    for (int unsigned k = 0; k < N_STREAM_IN_P; k++) begin
      ntfy_stri_in_w[k] =
          (32'(lstn_act_sink_w) == k
           && (lstn_disc_arm_w || lstn_disc_disarm_w
               || lstn_act_settle_w || lstn_act_teardown_w
               || (lstn_act_strt_chg_w && !lstn_act_strt_cmd_chg_w)))
          || srp_evt_tk_reg_w[k] || srp_evt_tk_unreg_w[k];
    end
    for (int unsigned k = 0; k < N_STREAM_OUT_P; k++) begin
      ntfy_stri_out_w[k] =
          (32'(tkr_gate_src_w) == k && (tkr_gate_open_w || tkr_gate_close_w))
          || srp_lstn_reg_change_w[k];
    end
  end
  logic                    aecp_eff_commit_nc_w;
  logic [3:0]              aecp_eff_notify_cls_nc_w;
  logic                    aecp_eff_notify_stb_nc_w;
  logic [15:0]             aecp_eff_notify_type_w, aecp_eff_notify_index_w;
  logic [15:0]             aecp_eff_notify_arg0_w, aecp_eff_notify_arg1_w;
  logic [63:0]             aecp_eff_notify_excl_w;
  logic                    aecp_dbg_busy_nc_w, aecp_dbg_img_valid_w;
  logic [15:0]             aecp_dbg_cmd_w, aecp_dbg_resp_w, aecp_dbg_drop_w;
  logic [15:0]             aecp_dbg_miss_w;
  logic  [3:0]             aecp_dbg_fault_w;
  logic  [4:0]             aecp_dbg_status_w;
  logic [10:0]             aecp_dbg_len_w;
  logic  [2:0]             aecp_dbg_rfault_w;
  logic [15:0]             aecp_dbg_rerr_w, aecp_dbg_rlane_w;

  //! ---- the STREAM_IS_RUNNING reduction (Milan §5.3.7.3) ----------------
  //! §5.3.7.3, verbatim: "As long as a PAAD is declaring a Talker Advertise
  //! attribute and receiving a Listener Ready or Listener Ready Failed
  //! attribute for a Stream Output, it shall be streaming AVTP packets."
  //!
  //! So BOTH halves are required, and the Listener half admits two of the
  //! four srp_pkg::srp_decl_e codes — READY (2) and READY_FAILED (3), which
  //! share bit 1, so the test is one bit rather than two compares. The Talker
  //! half is ADVERTISE (1) alone: a Talker FAILED (2) is declaring, but it is
  //! not streaming, and treating it as such would refuse a reconfiguration
  //! the standard permits.
  //!
  //! The reduction lives HERE rather than in the AECP engine because this is
  //! where the SRP records are; the engine consumes a sentence, not a state
  //! machine.
  logic [N_STREAM_OUT_P-1:0] aecp_streaming_w;
  always_comb begin : streaming_reduce
    for (int unsigned s = 0; s < N_STREAM_OUT_P; s++)
      aecp_streaming_w[s] = (srp_tk_decl_state_w[s] == 2'd1)
                            && srp_lstn_reg_state_w[s][1];
  end

  // ---- live dispatch admission and release ------------------------------
  // A refused head stays in its dispatch queue and is not shown to either
  // engine. Round-robin choice between two ready heads prevents a sustained
  // ACMP load from starving a conflicting AECP write. MAP_CFG and STREAM_CFG
  // therefore use the scoreboard's class-wide cross-lock for their complete
  // transaction lifetimes.
  pp_txn_t aecp_head_w;
  logic acmp_sb_candidate_w, aecp_sb_candidate_w;
  logic sb_pick_acmp_w, sb_pick_aecp_w;
  logic acmp_sb_accept_w, aecp_sb_accept_w;
  logic acmp_sb_done_w, aecp_sb_done_w;
  logic sb_rel_acmp_w, sb_rel_aecp_w;

  assign aecp_head_w = pp_txn_t'(aecp_txn_w);
  assign acmp_sb_candidate_w = acmp_txn_valid_w && pf_ready_w
                             && !acmp_sb_active_r
                             && (acmp_is_tkr_w ? tkr_txn_ready_w
                                               : lstn_txn_ready_w);
  assign aecp_sb_candidate_w = aecp_txn_valid_w && !aecp_sb_active_r
                             && (aecp_eng_ready_w || aecp_txn_ready_i);
  assign sb_pick_aecp_w = aecp_sb_candidate_w
                        && (!acmp_sb_candidate_w || sb_prefer_aecp_r);
  assign sb_pick_acmp_w = acmp_sb_candidate_w && !sb_pick_aecp_w;

  always_comb begin : scoreboard_admission_mux
    sb_adm_req_w   = sb_pick_acmp_w || sb_pick_aecp_w;
    sb_adm_class_w = 4'(PP_HZ_RO_SNAPSHOT);
    sb_adm_key_w   = 16'd0;
    if (sb_pick_acmp_w) begin
      sb_adm_class_w = 4'(acmp_head_w.hazard_class);
      sb_adm_key_w   = acmp_head_w.hazard_key;
    end else if (sb_pick_aecp_w) begin
      sb_adm_class_w = 4'(aecp_head_w.hazard_class);
      sb_adm_key_w   = aecp_head_w.hazard_key;
    end
  end

  assign acmp_sb_grant_w = sb_pick_acmp_w && sb_gnt_w;
  assign aecp_sb_grant_w = sb_pick_aecp_w && sb_gnt_w;
  assign acmp_sb_accept_w = acmp_sb_grant_w && acmp_sb_candidate_w;
  assign aecp_sb_accept_w = aecp_sb_grant_w && aecp_sb_candidate_w;
  assign aecp_txn_ready_w = aecp_sb_grant_w
                          && (aecp_eng_ready_w || aecp_txn_ready_i);

  // RX-slot return is the common retirement event for commands with a
  // response and commands that are permitted to retire silently. Match the
  // slot so an optional external AECP drain cannot release the engine's hold.
  assign acmp_sb_done_w = acmp_sb_active_r
                        && ((lstn_rxs_free_w
                             && (lstn_rxs_free_slot_w == acmp_sb_slot_r))
                         || (tkr_rxs_free_w
                             && (tkr_rxs_free_slot_w == acmp_sb_slot_r)));
  assign aecp_sb_done_w = aecp_sb_active_r
                        && ((aecp_rxs_free_w
                             && (aecp_rxs_free_slot_w == aecp_sb_slot_r))
                         || (aecp_rxs_free_i
                             && (aecp_rxs_free_slot_i == aecp_sb_slot_r)));

  // The scoreboard has one release port. If both engines retire together,
  // ACMP releases now and AECP's pending bit releases it on the next cycle.
  assign sb_rel_acmp_w = acmp_sb_active_r
                       && (acmp_sb_done_pending_r || acmp_sb_done_w);
  assign sb_rel_aecp_w = !sb_rel_acmp_w && aecp_sb_active_r
                       && (aecp_sb_done_pending_r || aecp_sb_done_w);
  assign sb_rel_valid_w = sb_rel_acmp_w || sb_rel_aecp_w;
  assign sb_rel_id_w    = sb_rel_acmp_w ? acmp_sb_id_r : aecp_sb_id_r;

  always_ff @(posedge clk_i) begin : scoreboard_owners
    if (!rst_n) begin
      acmp_sb_active_r       <= 1'b0;
      aecp_sb_active_r       <= 1'b0;
      acmp_sb_done_pending_r <= 1'b0;
      aecp_sb_done_pending_r <= 1'b0;
      sb_prefer_aecp_r       <= 1'b0;
      acmp_sb_id_r           <= 3'd0;
      aecp_sb_id_r           <= 3'd0;
      acmp_sb_slot_r         <= '0;
      aecp_sb_slot_r         <= '0;
    end else begin
      if (acmp_sb_accept_w) begin
        acmp_sb_active_r       <= 1'b1;
        acmp_sb_done_pending_r <= 1'b0;
        sb_prefer_aecp_r       <= 1'b1;
        acmp_sb_id_r           <= sb_id_w;
        acmp_sb_slot_r         <= acmp_head_w.rx_slot[RXS_W_C-1:0];
      end else if (acmp_sb_done_w) begin
        acmp_sb_done_pending_r <= 1'b1;
      end
      if (aecp_sb_accept_w) begin
        aecp_sb_active_r       <= 1'b1;
        aecp_sb_done_pending_r <= 1'b0;
        sb_prefer_aecp_r       <= 1'b0;
        aecp_sb_id_r           <= sb_id_w;
        aecp_sb_slot_r         <= aecp_head_w.rx_slot[RXS_W_C-1:0];
      end else if (aecp_sb_done_w) begin
        aecp_sb_done_pending_r <= 1'b1;
      end
      if (sb_rel_acmp_w) begin
        acmp_sb_active_r       <= 1'b0;
        acmp_sb_done_pending_r <= 1'b0;
      end
      if (sb_rel_aecp_w) begin
        aecp_sb_active_r       <= 1'b0;
        aecp_sb_done_pending_r <= 1'b0;
      end
    end
  end

  KL_aecp_engine #(
      .UCODE_HEX_P         (UCODE_HEX_P),
      .DESC_BASE_P         (DESC_BASE_P),
      .RESP_BASE_P         (RESP_BASE_P),
      .LINE_BYTES_P        (DESC_LINE_BYTES_P),
      .IDX_ENTRIES_P       (DESC_IDX_ENTRIES_P),
      .NAME_ENTRIES_P      (DESC_NAME_ENTRIES_P),
      .MEM_TIMEOUT_CYC_P   (DESC_MEM_TMO_CYC_P),
      .N_STREAM_IN_P       (N_STREAM_IN_P),
      .N_STREAM_OUT_P      (N_STREAM_OUT_P),
      .N_AUDIO_UNIT_P      (N_AUDIO_UNIT_P),
      .N_CLK_DOMAIN_P      (N_CLK_DOMAIN_P),
      .N_CONTROL_P         (N_CONTROL_P),
      .RX_SLOTS_P          (RX_SLOTS_P),
      .RX_SLOT_BYTES_P     (RX_SLOT_BYTES_P),
      .TX_STD_SLOTS_P      (TX_STD_SLOTS_P),
      .TX_STD_BYTES_P      (576),
      .TX_OVERSIZE_BYTES_P (TX_OVERSIZE_BYTES_P)
  ) u_aecp (
      .clk_i              (clk_i),
      .rst_n              (rst_n),
      .entity_id_i        (entity_id_i),
      .own_mac_i          (own_mac_i),
      .txn_valid_i        (aecp_txn_valid_w && aecp_sb_grant_w),
      .txn_i              (aecp_txn_w),
      .txn_ready_o        (aecp_eng_ready_w),
      .rxs_rd_slot_o      (rxp_rd_slot_w[RXP_UCPU_C]),
      .rxs_rd_addr_o      (rxp_rd_addr_w[RXP_UCPU_C]),
      .rxs_rd_en_o        (rxp_rd_en_w[RXP_UCPU_C]),
      .rxs_rd_data_i      (rxp_rd_data_w[RXP_UCPU_C]),
      .rxs_slot_len_i     (rxp_slot_len_w[RXP_UCPU_C]),
      .rxs_free_o         (aecp_rxs_free_w),
      .rxs_free_slot_o    (aecp_eng_free_slot_w),
      .txs_alloc_req_o    (aecp_txs_alloc_req_w),
      .txs_oversize_o     (aecp_txs_oversize_w),
      .txs_alloc_gnt_i    (aecp_txs_gnt_w),
      .txs_alloc_slot_i   (aecp_txs_gnt_slot_w),
      .txs_wr_slot_o      (aecp_txs_wr_slot_w),
      .txs_wr_addr_o      (aecp_txs_wr_addr_w),
      .txs_wr_valid_o     (aecp_txs_wr_valid_w),
      .txs_wr_data_o      (aecp_txs_wr_data_w),
      .txs_wr_commit_o    (aecp_txs_wr_commit_w),
      .txs_wr_len_o       (aecp_txs_wr_len_w),
      .txreq_valid_o      (aecp_txreq_valid_w),
      .txreq_slot_o       (aecp_txreq_slot_w),
      .txreq_ready_i      (aecp_txreq_ready_w),
      .rgy_req_o          (aecp_rgy_req_w),
      .rgy_state_o        (aecp_rgy_state_w),
      .rgy_op_o           (aecp_rgy_op_w),
      .rgy_eid_o          (aecp_rgy_eid_w),
      .rgy_mac_o          (aecp_rgy_mac_w),
      .rgy_tl_o           (aecp_rgy_tl_w),
      .rgy_data_i         (aecp_rgy_data_w),
      .rgy_wait_i         (aecp_rgy_wait_w),
      .uns_valid_i        (uns_valid_w),
      .uns_kind_i         (uns_kind_w),
      .uns_desc_type_i    (uns_dt_w),
      .uns_desc_index_i   (uns_di_w),
      .uns_ctlr_eid_i     (uns_eid_w),
      .uns_mac_i          (uns_mac_w),
      .uns_seq_i          (uns_seq_w),
      .uns_amap_remove_i  (uns_amap_remove_w),
      .uns_amap_count_i   (uns_amap_count_w),
      .uns_arg0_i         (uns_arg0_w),
      .uns_arg1_i         (uns_arg1_w),
      .amap_notify_busy_i (ntfy_amap_busy_w),
      .uns_done_o         (uns_done_w),
      .txreq_uns_valid_o  (aecp_txreq_uns_valid_w),
      .txreq_uns_ready_i  (aecp_txreq_uns_ready_w),
      .mem_req_valid_o    (desc_mem_req_valid_o),
      .mem_req_ready_i    (desc_mem_req_ready_i),
      .mem_req_addr_o     (desc_mem_req_addr_o),
      .mem_req_beats_o    (desc_mem_req_beats_o),
      .mem_rsp_valid_i    (desc_mem_rsp_valid_i),
      .mem_rsp_ready_o    (desc_mem_rsp_ready_o),
      .mem_rsp_data_i     (desc_mem_rsp_data_i),
      .mem_rsp_last_i     (desc_mem_rsp_last_i),
      .mem_rsp_err_i      (desc_mem_rsp_err_i),
      .rmem_req_valid_o   (resp_mem_req_valid_o),
      .rmem_req_ready_i   (resp_mem_req_ready_i),
      .rmem_req_addr_o    (resp_mem_req_addr_o),
      .rmem_req_beats_o   (resp_mem_req_beats_o),
      .rmem_rsp_valid_i   (resp_mem_rsp_valid_i),
      .rmem_rsp_ready_o   (resp_mem_rsp_ready_o),
      .rmem_rsp_data_i    (resp_mem_rsp_data_i),
      .rmem_rsp_last_i    (resp_mem_rsp_last_i),
      .rmem_rsp_err_i     (resp_mem_rsp_err_i),
      .rmem_wr_valid_o    (resp_mem_wr_valid_o),
      .rmem_wr_ready_i    (resp_mem_wr_ready_i),
      .rmem_wr_addr_o     (resp_mem_wr_addr_o),
      .rmem_wr_data_o     (resp_mem_wr_data_o),
      .rmem_wr_strb_o     (resp_mem_wr_strb_o),
      .rmem_wr_done_i     (resp_mem_wr_done_i),
      .rmem_wr_err_i      (resp_mem_wr_err_i),
      .ctr_req_o          (ctr_req_o),
      .ctr_desc_type_o    (ctr_desc_type_o),
      .ctr_desc_index_o   (ctr_desc_index_o),
      .ctr_word_o         (ctr_word_o),
      .ctr_data_i         (ctr_data_i),
      .ctr_wait_i         (ctr_wait_i),
      .amap_req_o         (amap_req_o),
      .amap_desc_type_o   (amap_desc_type_o),
      .amap_desc_index_o  (amap_desc_index_o),
      .amap_map_index_o   (amap_map_index_o),
      .amap_sel_o         (amap_sel_o),
      .amap_rec_o         (amap_rec_o),
      .amap_data_i        (amap_data_i),
      .amap_wait_i        (amap_wait_i),
      .amap_edit_req_o    (amap_edit_req_o),
      .amap_edit_phase_o  (amap_edit_phase_o),
      .amap_edit_remove_o (amap_edit_remove_o),
      .amap_edit_desc_type_o(amap_edit_desc_type_o),
      .amap_edit_desc_index_o(amap_edit_desc_index_o),
      .amap_edit_count_o  (amap_edit_count_o),
      .amap_edit_rec_o    (amap_edit_rec_o),
      .amap_edit_record_o (amap_edit_record_o),
      .amap_edit_value_o  (amap_edit_value_o),
      .amap_edit_data_i   (amap_edit_data_i),
      .amap_edit_wait_i   (amap_edit_wait_i),
      .gsi_req_o          (gsi_req_o),
      .gsi_kind_o         (gsi_kind_o),
      .gsi_desc_type_o    (gsi_desc_type_o),
      .gsi_desc_index_o   (gsi_desc_index_o),
      .gsi_sel_o          (gsi_sel_o),
      .gsi_ord_o          (gsi_ord_o),
      .gsi_prop_fmt_o     (gsi_prop_fmt_o),
      .gsi_data_i         (gsi_data_i),
      .gsi_wait_i         (gsi_wait_i),
      .strm_bound_i       (bound_hold_r),
      .strm_started_i     (aecp_strm_started_o),
      .strm_streaming_i   (aecp_streaming_w),
      .lock_held_i        (ntfy_lock_held_w),
      .lock_ctlr_i        (ntfy_lock_ctlr_w),
      .eff_commit_o       (aecp_eff_commit_nc_w),
      .eff_nvm_mark_o     (aecp_nvm_mark_o),
      .eff_nvm_stb_o      (aecp_nvm_stb_o),
      .eff_notify_class_o (aecp_eff_notify_cls_nc_w),
      .eff_notify_stb_o   (aecp_eff_notify_stb_nc_w),
      .eff_notify_type_o  (aecp_eff_notify_type_w),
      .eff_notify_index_o (aecp_eff_notify_index_w),
      .eff_notify_arg0_o  (aecp_eff_notify_arg0_w),
      .eff_notify_arg1_o  (aecp_eff_notify_arg1_w),
      .eff_notify_excl_eid_o(aecp_eff_notify_excl_w),
      .dbg_busy_o         (aecp_dbg_busy_nc_w),
      .dbg_cmd_cnt_o      (aecp_dbg_cmd_w),
      .dbg_resp_cnt_o     (aecp_dbg_resp_w),
      .dbg_drop_cnt_o     (aecp_dbg_drop_w),
      .dbg_status_o       (aecp_dbg_status_w),
      .dbg_len_o          (aecp_dbg_len_w),
      .dbg_img_valid_o    (aecp_dbg_img_valid_w),
      .dbg_img_fault_o    (aecp_dbg_fault_w),
      .dbg_locate_miss_o  (aecp_dbg_miss_w),
      .dbg_resp_fault_o   (aecp_dbg_rfault_w),
      .dbg_resp_err_o     (aecp_dbg_rerr_w),
      .dbg_resp_lane_o    (aecp_dbg_rlane_w),
      .dyn_cur_config_o   (aecp_cur_config_o),
      .dyn_identify_o     (aecp_identify_o),
      .dyn_clk_src_index_o(aecp_clk_src_index_o),
      .strm_set_valid_o   (strm_set_valid_w),
      .strm_set_index_o   (strm_set_index_w),
      .strm_set_val_o     (strm_set_val_w),
      .strm_set_ready_i   (strm_set_ready_w),
      .strm_set_error_i   (strm_set_error_w),
      .dyn_pt_offset_o    (aecp_pt_offset_o),
      .dyn_pt_offset_v_o  (aecp_pt_offset_v_o),
      .dyn_fmt_in_o       (aecp_fmt_in_o),
      .dyn_fmt_in_v_o     (aecp_fmt_in_v_o),
      .dyn_fmt_out_o      (aecp_fmt_out_o),
      .dyn_fmt_out_v_o    (aecp_fmt_out_v_o),
      .dyn_dirty_o        (aecp_dyn_dirty_o)
  );

  assign aecp_rxs_free_slot_w = aecp_eng_free_slot_w;

  // =========================================================================
  // AECP notifications: the registered-controller list + ENTITY lock (06)
  // =========================================================================
  //! The Milan §5.3.4.2 list, the §5.3.4.1 lock and the §5.4.5 emission walk
  //! in one block beside the engine. Event classes whose response programs
  //! have not landed are tied 0 here and come alive with their stages -
  //! wiring an event before its µprogram exists would emit nothing anyway
  //! (the engine's no-send arm), but the tie says so at the seam.
  KL_aecp_notify #(
      .N_CTRL_P          (PP_N_CTRL_C),
      .N_STREAM_IN_P     (N_STREAM_IN_P),
      .N_STREAM_OUT_P    (N_STREAM_OUT_P),
      .TL_TIMEOUT_MS_P   (REG_TL_TIMEOUT_MS_P),
      .LOCK_TIMEOUT_MS_P (LOCK_TIMEOUT_MS_P),
      .TMR_SLOTS_P       (TMR_SLOTS_C),
      //! F08.4: rows own the FIRST half of the registry-monitor group (the
      //! second half stays reserved for the Milan §5.4.5.3 CA monitor);
      //! the lock owns the first singleton (pp_pkg: "LOCK, IDENT-BURST, ...")
      .TMR_REGMON_BASE_P (TMR_MAP_C.regmon),
      .TMR_LOCK_SLOT_P   (TMR_MAP_C.single)
  ) u_notify (
      .clk_i                 (clk_i),
      .rst_n                 (rst_n),
      .rgy_req_i             (aecp_rgy_req_w),
      .rgy_state_i           (aecp_rgy_state_w),
      .rgy_op_i              (aecp_rgy_op_w),
      .rgy_eid_i             (aecp_rgy_eid_w),
      .rgy_mac_i             (aecp_rgy_mac_w),
      .rgy_tl_i              (aecp_rgy_tl_w),
      .rgy_data_o            (aecp_rgy_data_w),
      .rgy_wait_o            (aecp_rgy_wait_w),
      //! Table 5.22 GET_STREAM_INFO triggers this fabric OBSERVES: for a
      //! sink, bound-state changes (arm/disarm), the settled parameters
      //! (settle/teardown - also the probing-status edges) and the
      //! registered Talker attribute events; for a source, its declaration
      //! opening/closing and the registered Listener attribute changes.
      //! What the fabric cannot see, it cannot notify about - the honest
      //! remainder is recorded in 06 §7.
      .ev_stri_in_i          (ntfy_stri_in_w),
      .ev_stri_out_i         (ntfy_stri_out_w),
      //! Table 5.22 GET_AVB_INFO triggers: the grandmaster changed, the
      //! SRP domain (class A priority/VID) changed, the link state flipped
      //! (AVTP_DOWN), or the integrator strobed a face-word change.
      //!
      //! GET_AS_PATH IS NOT ONE OF THEM, and gm_change_i is not a path
      //! event. gm_change_i is the ADP GM_CHANGE duty (Milan 5.6.3.5.7),
      //! and an integrator may legitimately raise it for any change of the
      //! advertised gPTP pair - grandmaster id OR gptp_domain_number -
      //! because both are ADPDU fields that a re-advertise has to carry.
      //! A domain number is not a path entry, so taking that strobe as an
      //! AS_PATH event pushes a path sequence that did not change, which
      //! Table 5.22 conditions on "the path sequence changes". 02 section 6
      //! already lists the GM_CHANGE consumers as the ADP advertise SM, the
      //! counters and GET_AVB_INFO - not GET_AS_PATH - so this restores the
      //! documented contract.
      //!
      //! ev_asp_i therefore takes the integrator's path-source event ALONE.
      //! gsi_asp_chg_i is the one face that can see whether the served path
      //! sequence moved: the integrator owns entry 0 (the grandmaster) and
      //! entries 1.. (the published PathTrace tail), answers them through
      //! gsi_data_i, and raises gsi_asp_chg_i from the SAME sources. An
      //! integrator that does not drive the gsi face answers an empty path
      //! and has nothing to notify about.
      .ev_avb_i              (gm_change_i || srp_evt_domain_change_w
                              || (link_up_i != link_q_r) || gsi_avb_chg_i),
      .ev_asp_i              (gsi_asp_chg_i),
      .ev_amap_i             (aecp_eff_notify_stb_nc_w
                              && (aecp_eff_notify_cls_nc_w == 4'd6)),
      .ev_amap_remove_i      (amap_edit_remove_o),
      .ev_amap_type_i        (amap_edit_desc_type_o),
      .ev_amap_index_i       (amap_edit_desc_index_o),
      .ev_amap_count_i       (amap_edit_count_o),
      .ev_amap_excl_eid_i    (aecp_rgy_eid_w),
      .ev_ctr_i              (ctr_change_i),
      .ev_ctr_type_i         (ctr_change_desc_type_i),
      .ev_ctr_index_i        (ctr_change_desc_index_i),
      .ev_cmd_i              (aecp_eff_notify_stb_nc_w),
      .ev_cmd_class_i        (aecp_eff_notify_cls_nc_w),
      .ev_cmd_type_i         (aecp_eff_notify_type_w),
      .ev_cmd_index_i        (aecp_eff_notify_index_w),
      .ev_cmd_arg0_i         (aecp_eff_notify_arg0_w),
      .ev_cmd_arg1_i         (aecp_eff_notify_arg1_w),
      .ev_cmd_excl_eid_i     (aecp_eff_notify_excl_w),
      //! Enumerate the six defined AECP command message types. PP_PROTO_AEM
      //! is the validator's residual bucket and therefore also carries AVC,
      //! HDCP_APM, EXTENDED, and the reserved 10/12 types. The reserved types
      //! must not refresh a registered controller's liveness timer.
      .rx_cmd_valid_i        (v_hdr_valid_w
                              && ((v_hdr_msg_type_w == 4'd0)
                                  || (v_hdr_msg_type_w == 4'd2)
                                  || (v_hdr_msg_type_w == 4'd4)
                                  || (v_hdr_msg_type_w == 4'd6)
                                  || (v_hdr_msg_type_w == 4'd8)
                                  || (v_hdr_msg_type_w == 4'd14))
                              && ((v_hdr_protocol_w == 3'(PP_PROTO_AEM))
                                  || (v_hdr_protocol_w == 3'(PP_PROTO_MVU))
                                  || (v_hdr_protocol_w == 3'(PP_PROTO_AA)))),
      .rx_cmd_eid_i          (v_hdr_ctlr_eid_w),
      .rx_cmd_mac_i          (v_hdr_src_mac_w),
      .prng_draw_req_o       (ntfy_prng_req_w),
      .prng_draw_kind_o      (ntfy_prng_kind_w),
      .prng_draw_busy_i      (ntfy_prng_busy_w),
      .prng_draw_valid_i     (ntfy_prng_valid_w),
      .prng_draw_ms_i        (prng_ms_w),
      .ca_valid_o            (ntfy_ca_valid_w),
      .ca_owner_o            (ntfy_ca_owner_w),
      .ca_ctlr_eid_o         (ntfy_ca_eid_w),
      .ca_mac_o              (ntfy_ca_mac_w),
      .ca_ready_i            (ntfy_ca_ready_w),
      .ca_cancel_valid_o     (ntfy_ca_cancel_valid_w),
      .ca_cancel_owner_o     (ntfy_ca_cancel_owner_w),
      .ca_rsp_valid_i        (org_rt_valid_w),
      .ca_rsp_owner_i        (org_rt_owner_w),
      .ca_fail_valid_i       (org_fail_valid_w),
      .ca_fail_owner_i       (org_fail_owner_w),
      .uns_valid_o           (uns_valid_w),
      .uns_kind_o            (uns_kind_w),
      .uns_desc_type_o       (uns_dt_w),
      .uns_desc_index_o      (uns_di_w),
      .uns_ctlr_eid_o        (uns_eid_w),
      .uns_mac_o             (uns_mac_w),
      .uns_seq_o             (uns_seq_w),
      .uns_amap_remove_o     (uns_amap_remove_w),
      .uns_amap_count_o      (uns_amap_count_w),
      .uns_arg0_o            (uns_arg0_w),
      .uns_arg1_o            (uns_arg1_w),
      .uns_done_i            (uns_done_w),
      .amap_busy_o           (ntfy_amap_busy_w),
      .lock_held_o           (ntfy_lock_held_w),
      .lock_ctlr_o           (ntfy_lock_ctlr_w),
      .tmr_arm_valid_o       (ntfy_arm_valid_w),
      .tmr_arm_cancel_o      (ntfy_arm_cancel_w),
      .tmr_arm_slot_o        (ntfy_arm_slot_w),
      .tmr_arm_owner_o       (ntfy_arm_owner_w),
      .tmr_arm_deadline_ms_o (ntfy_arm_deadline_w),
      .now_ms_i              (now_ms_w),
      .tmr_exp_valid_i       (exp_valid_w),
      .tmr_exp_slot_i        (exp_slot_w),
      .tmr_exp_owner_i       (exp_owner_w),
      .mon_arm_valid_o       (ntfy_mon_arm_valid_w),
      .mon_arm_cancel_o      (ntfy_mon_arm_cancel_w),
      .mon_arm_slot_o        (ntfy_mon_arm_slot_w),
      .mon_arm_owner_o       (ntfy_mon_arm_owner_w),
      .mon_arm_deadline_ms_o (ntfy_mon_arm_deadline_w),
      .dbg_reg_cnt_o         (ntfy_reg_cnt_nc_w),
      .dbg_uns_cnt_o         (ntfy_uns_cnt_nc_w),
      .dbg_coalesce_o        (ntfy_coalesce_nc_w)
  );

  // =========================================================================
  // TX slot pool + pool-access arbiter (banner)
  // =========================================================================
  // ONE alloc+write port, seven builders (ADP / listener / SRP / talker /
  // AECP / MAAP / CONTROLLER_AVAILABLE). Ownership is taken at selection,
  // one alloc sample is forwarded at a time, and the write lane stays muxed
  // to the owner until its commit or explicit cancellation.
  // Non-owners simply see no grant and keep retrying/holding — that IS
  // their landed behavior. A full pool parks the owner (grant comes when
  // serialization frees a slot); no timeout exists because every landed
  // builder commits unconditionally after grant.
  localparam int unsigned TXC_ADP_C  = 0;
  localparam int unsigned TXC_LSTN_C = 1;
  localparam int unsigned TXC_SRP_C  = 2;
  localparam int unsigned TXC_TKB_C  = 3;
  localparam int unsigned TXC_AECP_C = 4;   // KL_aecp_engine
  localparam int unsigned TXC_MAAP_C = 5;   // KL_pp_maap (11)
  localparam int unsigned TXC_CA_C   = 6;   // CONTROLLER_AVAILABLE builder
  localparam int unsigned TXC_N_C    = 7;

  logic [TXC_N_C-1:0] txc_req_w;
  logic [TXC_N_C-1:0] txc_pend_r;
  logic [2:0] txc_owner_r;
  logic       txc_locked_r;
  logic       txc_alloc_wait_r;
  logic       pool_alloc_req_w, pool_oversize_w;
  logic       pool_alloc_gnt_w;
  logic [TXS_W_C-1:0] pool_alloc_slot_w;
  logic       pool_wr_valid_w, pool_wr_commit_w;
  logic [TXS_W_C-1:0] pool_wr_slot_w;
  logic [TXA_W_C-1:0] pool_wr_addr_w, pool_wr_len_w;
  logic [7:0] pool_wr_data_w;
  logic [TXC_N_C-1:0] txc_commit_w;

  assign txc_req_w = {ca_txs_alloc_req_w, maapeng_txs_alloc_req_w,
                      aecp_txs_alloc_req_w, tkb_alloc_req_w,
                      srp_txs_alloc_req_w,
                      lstn_txs_alloc_req_w, adp_txs_alloc_req_w};
  assign txc_commit_w = {ca_txs_wr_commit_w, maapeng_txs_wr_commit_w,
                         aecp_txs_wr_commit_w, (tkb_st_r == TKB_COMMIT),
                         srp_txs_wr_commit_w,
                         lstn_txs_wr_commit_w, adp_txs_wr_commit_w};

  always_ff @(posedge clk_i) begin : txc_arbiter
    if (!rst_n) begin
      txc_pend_r   <= '0;
      txc_owner_r  <= 3'd0;
      txc_locked_r <= 1'b0;
      txc_alloc_wait_r <= 1'b0;
    end else begin
      for (int unsigned i = 0; i < TXC_N_C; i++) begin
        if (txc_req_w[i]) txc_pend_r[i] <= 1'b1;
      end
      if (!txc_locked_r) begin
        txc_alloc_wait_r <= 1'b0;
        //! fixed priority, 03 §8 order: listener (the 50 ms ACMP budget) >
        //! talker builder > AECP solicited (100 ms) > SRP > ADP periodic
        if (txc_pend_r[TXC_LSTN_C] || txc_req_w[TXC_LSTN_C]) begin
          txc_owner_r <= 3'(TXC_LSTN_C); txc_locked_r <= 1'b1;
        end else if (txc_pend_r[TXC_TKB_C] || txc_req_w[TXC_TKB_C]) begin
          txc_owner_r <= 3'(TXC_TKB_C);  txc_locked_r <= 1'b1;
        end else if (txc_pend_r[TXC_AECP_C] || txc_req_w[TXC_AECP_C]) begin
          txc_owner_r <= 3'(TXC_AECP_C); txc_locked_r <= 1'b1;
        end else if (txc_pend_r[TXC_CA_C] || txc_req_w[TXC_CA_C]) begin
          txc_owner_r <= 3'(TXC_CA_C); txc_locked_r <= 1'b1;
        end else if (txc_pend_r[TXC_SRP_C] || txc_req_w[TXC_SRP_C]) begin
          txc_owner_r <= 3'(TXC_SRP_C);  txc_locked_r <= 1'b1;
        end else if (txc_pend_r[TXC_ADP_C] || txc_req_w[TXC_ADP_C]) begin
          txc_owner_r <= 3'(TXC_ADP_C);  txc_locked_r <= 1'b1;
        end else if (txc_pend_r[TXC_MAAP_C] || txc_req_w[TXC_MAAP_C]) begin
          txc_owner_r <= 3'(TXC_MAAP_C); txc_locked_r <= 1'b1;
        end
      end else begin
        // The pool reports a sampled allocation on the following cycle.
        // Forward only one request while that registered result is pending;
        // otherwise every builder that holds until grant allocates twice.
        if (txc_alloc_wait_r)
          txc_alloc_wait_r <= 1'b0;
        else if (pool_alloc_req_w)
          txc_alloc_wait_r <= 1'b1;
        if (pool_alloc_gnt_w) txc_pend_r[txc_owner_r] <= 1'b0;
        if (txc_commit_w[txc_owner_r]) begin
          txc_locked_r <= 1'b0;
          txc_alloc_wait_r <= 1'b0;
        end
        if ((txc_owner_r == 3'(TXC_CA_C)) && ca_txs_abort_w) begin
          txc_pend_r[TXC_CA_C] <= 1'b0;
          txc_locked_r <= 1'b0;
          txc_alloc_wait_r <= 1'b0;
        end
      end
    end
  end

  //! only the AECP engine can need the Δ8 oversize slot (READ_DESCRIPTOR is
  //! the one response in this build that may exceed a standard 576-byte slot)
  assign pool_oversize_w = txc_locked_r && (txc_owner_r == 3'(TXC_AECP_C))
                         && aecp_txs_oversize_w;

  always_comb begin : txc_mux
    pool_alloc_req_w = 1'b0;
    pool_wr_valid_w  = 1'b0;
    pool_wr_commit_w = 1'b0;
    pool_wr_slot_w   = '0;
    pool_wr_addr_w   = '0;
    pool_wr_data_w   = 8'd0;
    pool_wr_len_w    = '0;
    if (txc_locked_r) begin
      unique case (txc_owner_r)
        3'(TXC_AECP_C): begin
          pool_alloc_req_w = aecp_txs_alloc_req_w;
          pool_wr_valid_w  = aecp_txs_wr_valid_w;
          pool_wr_commit_w = aecp_txs_wr_commit_w;
          pool_wr_slot_w   = aecp_txs_wr_slot_w;
          pool_wr_addr_w   = aecp_txs_wr_addr_w;
          pool_wr_data_w   = aecp_txs_wr_data_w;
          pool_wr_len_w    = aecp_txs_wr_len_w;
        end
        3'(TXC_CA_C): begin
          pool_alloc_req_w = ca_txs_alloc_req_w;
          pool_wr_valid_w  = ca_txs_wr_valid_w;
          pool_wr_commit_w = ca_txs_wr_commit_w;
          pool_wr_slot_w   = ca_txs_wr_slot_w;
          pool_wr_addr_w   = ca_txs_wr_addr_w;
          pool_wr_data_w   = ca_txs_wr_data_w;
          pool_wr_len_w    = ca_txs_wr_len_w;
        end
        3'(TXC_ADP_C): begin
          pool_alloc_req_w = adp_txs_alloc_req_w;
          pool_wr_valid_w  = adp_txs_wr_valid_w;
          pool_wr_commit_w = adp_txs_wr_commit_w;
          pool_wr_slot_w   = adp_txs_wr_slot_w;
          pool_wr_addr_w   = adp_txs_wr_addr_w;
          pool_wr_data_w   = adp_txs_wr_data_w;
          pool_wr_len_w    = adp_txs_wr_len_w;
        end
        3'(TXC_LSTN_C): begin
          pool_alloc_req_w = lstn_txs_alloc_req_w;
          pool_wr_valid_w  = lstn_txs_wr_valid_w;
          pool_wr_commit_w = lstn_txs_wr_commit_w;
          pool_wr_slot_w   = lstn_txs_wr_slot_w;
          pool_wr_addr_w   = lstn_txs_wr_addr_w;
          pool_wr_data_w   = lstn_txs_wr_data_w;
          pool_wr_len_w    = lstn_txs_wr_len_w;
        end
        3'(TXC_SRP_C): begin
          pool_alloc_req_w = srp_txs_alloc_req_w;
          pool_wr_valid_w  = srp_txs_wr_valid_w;
          pool_wr_commit_w = srp_txs_wr_commit_w;
          pool_wr_slot_w   = srp_txs_wr_slot_w;
          pool_wr_addr_w   = srp_txs_wr_addr_w;
          pool_wr_data_w   = srp_txs_wr_data_w;
          pool_wr_len_w    = srp_txs_wr_len_w;
        end
        3'(TXC_MAAP_C): begin
          pool_alloc_req_w = maapeng_txs_alloc_req_w;
          pool_wr_valid_w  = maapeng_txs_wr_valid_w;
          pool_wr_commit_w = maapeng_txs_wr_commit_w;
          pool_wr_slot_w   = maapeng_txs_wr_slot_w;
          pool_wr_addr_w   = maapeng_txs_wr_addr_w;
          pool_wr_data_w   = maapeng_txs_wr_data_w;
          pool_wr_len_w    = maapeng_txs_wr_len_w;
        end
        default: begin  // TXC_TKB_C
          pool_alloc_req_w = tkb_alloc_req_w;
          pool_wr_valid_w  = (tkb_st_r == TKB_WR);
          pool_wr_commit_w = (tkb_st_r == TKB_COMMIT);
          pool_wr_slot_w   = tkb_slot_r;
          pool_wr_addr_w   = {5'd0, tkb_bidx_r};
          pool_wr_data_w   = tkb_pdu_byte_w;
          pool_wr_len_w    = TXA_W_C'(56);
        end
      endcase
      if (txc_alloc_wait_r) pool_alloc_req_w = 1'b0;
    end
  end

  assign adp_txs_gnt_w  = txc_locked_r && (txc_owner_r == 3'(TXC_ADP_C))
                        && pool_alloc_gnt_w;
  assign lstn_txs_gnt_w = txc_locked_r && (txc_owner_r == 3'(TXC_LSTN_C))
                        && pool_alloc_gnt_w;
  assign srp_txs_gnt_w  = txc_locked_r && (txc_owner_r == 3'(TXC_SRP_C))
                        && pool_alloc_gnt_w;
  assign tkb_gnt_w      = txc_locked_r && (txc_owner_r == 3'(TXC_TKB_C))
                        && pool_alloc_gnt_w;
  assign aecp_txs_gnt_w = txc_locked_r && (txc_owner_r == 3'(TXC_AECP_C))
                        && pool_alloc_gnt_w;
  assign maapeng_txs_gnt_w = txc_locked_r && (txc_owner_r == 3'(TXC_MAAP_C))
                        && pool_alloc_gnt_w;
  assign ca_txs_gnt_w = txc_locked_r && (txc_owner_r == 3'(TXC_CA_C))
                        && pool_alloc_gnt_w;
  assign adp_txs_gnt_slot_w  = pool_alloc_slot_w;
  assign lstn_txs_gnt_slot_w = pool_alloc_slot_w;
  assign srp_txs_gnt_slot_w  = pool_alloc_slot_w;
  assign tkb_gnt_slot_w      = pool_alloc_slot_w;
  assign aecp_txs_gnt_slot_w = pool_alloc_slot_w;
  assign maapeng_txs_gnt_slot_w = pool_alloc_slot_w;
  assign ca_txs_gnt_slot_w = pool_alloc_slot_w;

  logic        ser_req_w, ser_valid_w, ser_last_w, ser_ready_w;
  logic [TXS_W_C-1:0] ser_slot_w;
  logic [7:0]  ser_data_w;
  logic [TX_STD_SLOTS_P:0] txs_ready_nc_w;
  logic [$clog2(TX_STD_SLOTS_P+2)-1:0] txs_free_w;
  logic        txs_release_valid_w;
  logic [TXS_W_C-1:0] txs_release_slot_w;

  KL_pp_release_merge #(
      .N_SLOTS_P (TX_STD_SLOTS_P + 1)
  ) u_release_merge (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .a_valid_i       (org_release_valid_w),
      .a_slot_i        (TXS_W_C'(org_release_slot_w)),
      .b_valid_i       (ca_cancel_release_valid_w),
      .b_slot_i        (ca_cancel_release_slot_w),
      .release_valid_o (txs_release_valid_w),
      .release_slot_o  (txs_release_slot_w)
  );

  KL_pp_tx_slots #(
      .TX_STD_SLOTS_P      (TX_STD_SLOTS_P),
      .TX_STD_BYTES_P      (576),
      .TX_OVERSIZE_BYTES_P (TX_OVERSIZE_BYTES_P)
  ) u_tx_slots (
      .clk_i         (clk_i),
      .rst_n         (rst_n),
      .alloc_req_i   (pool_alloc_req_w),
      .oversize_i    (pool_oversize_w),    // Δ8: READ_DESCRIPTOR only
      .alloc_gnt_o   (pool_alloc_gnt_w),
      .alloc_slot_o  (pool_alloc_slot_w),
      .wr_slot_i     (pool_wr_slot_w),
      .wr_addr_i     (pool_wr_addr_w),
      .wr_valid_i    (pool_wr_valid_w),
      .wr_data_i     (pool_wr_data_w),
      .wr_commit_i   (pool_wr_commit_w),
      .wr_len_i      (pool_wr_len_w),
      .hold_valid_i  (org_hold_valid_w),
      .hold_slot_i   (org_hold_slot_w),
      .release_valid_i(txs_release_valid_w),
      .release_slot_i(txs_release_slot_w),
      .ser_req_i     (ser_req_w),
      .ser_slot_i    (ser_slot_w),
      .ser_valid_o   (ser_valid_w),
      .ser_data_o    (ser_data_w),
      .ser_last_o    (ser_last_w),
      .ser_ready_i   (ser_ready_w),
      .slots_ready_o (txs_ready_nc_w),
      .slots_free_o  (txs_free_w)
  );

  // ---- TX lane queues: the ADP engine and the listener pulse one-cycle
  // txreq strobes; the arbiter wants requests HELD until grant. Depth-8
  // slot-handle queues are structurally lossless (at most 5 slots exist).
  logic [7:0][TXS_W_C-1:0] laneq_adp_r, laneq_acmp_r, laneq_org_r;
  logic [7:0][TXS_W_C-1:0] laneq_org_next_w;
  logic [3:0]              laneq_adp_cnt_r, laneq_acmp_cnt_r, laneq_org_cnt_r;
  logic [3:0]              laneq_adp_mid_w, laneq_acmp_mid_w;
  logic [3:0]              laneq_org_next_cnt_w;
  logic                    laneq_adp_push_w, laneq_acmp_push_w;
  logic                    laneq_org_drop_w, laneq_org_pop_w;
  logic                    laneq_org_release_head_w;
  logic                    laneq_org_withdraw_head_w;

  logic [LANE_N_C-1:0]              arb_req_w;
  logic [LANE_N_C-1:0][TXS_W_C-1:0] arb_slot_w;
  logic [LANE_N_C-1:0]              arb_gnt_w;
  logic [LANE_N_C-1:0][15:0]        arb_gnt_cnt_w;

  // count after this cycle's pop; a push appends at that position (a queue
  // deeper than the 5 physical slots can never overflow — see banner)
  assign laneq_adp_mid_w  = laneq_adp_cnt_r
                          - (arb_gnt_w[LANE_ADP_C] ? 4'd1 : 4'd0);
  assign laneq_acmp_mid_w = laneq_acmp_cnt_r
                          - (arb_gnt_w[LANE_ACMP_C] ? 4'd1 : 4'd0);
  // A cancelled exchange releases its slot while its handle may still be
  // queued. Drop a head that is no longer READY before it can block the
  // lane or serialize contents from a later reuse of that physical slot.
  assign laneq_org_release_head_w = (laneq_org_cnt_r != 4'd0)
                                  && txs_release_valid_w
                                  && (txs_release_slot_w
                                      == laneq_org_r[0]);
  assign laneq_org_withdraw_head_w = (laneq_org_cnt_r != 4'd0)
                                   && org_withdraw_slot_mask_w[laneq_org_r[0]];
  assign laneq_org_drop_w = (laneq_org_cnt_r != 4'd0)
                          && (!txs_ready_nc_w[laneq_org_r[0]]
                              || laneq_org_release_head_w
                              || laneq_org_withdraw_head_w);
  assign laneq_org_pop_w  = arb_gnt_w[LANE_ORIG_C] || laneq_org_drop_w;
  assign laneq_adp_push_w  = adp_txreq_valid_w  && (laneq_adp_mid_w != 4'd8);
  assign laneq_acmp_push_w = lstn_txreq_valid_w && (laneq_acmp_mid_w != 4'd8);

  // A response or controller command may cancel any inflight exchange, not
  // only the queue head. Compact every released handle before a physical slot
  // can be reused, while preserving a simultaneous head grant and new push.
  always_comb begin : originator_queue_next
    laneq_org_next_w     = '0;
    laneq_org_next_cnt_w = 4'd0;
    for (int unsigned i = 0; i < 8; i++) begin
      if ((4'(i) < laneq_org_cnt_r)
          && !((i == 0) && laneq_org_pop_w)
          && !(txs_release_valid_w
               && (laneq_org_r[i] == txs_release_slot_w))
          && !org_withdraw_slot_mask_w[laneq_org_r[i]]) begin
        laneq_org_next_w[laneq_org_next_cnt_w[2:0]] = laneq_org_r[i];
        laneq_org_next_cnt_w = laneq_org_next_cnt_w + 4'd1;
      end
    end
    if ((org_send_valid_w || org_resend_valid_w)
        && (laneq_org_next_cnt_w != 4'd8)) begin
      laneq_org_next_w[laneq_org_next_cnt_w[2:0]] = org_resend_valid_w
                                                      ? org_resend_slot_w
                                                      : org_send_slot_w;
      laneq_org_next_cnt_w = laneq_org_next_cnt_w + 4'd1;
    end
  end

  always_ff @(posedge clk_i) begin : lane_queues
    if (!rst_n) begin
      laneq_adp_r      <= '0;
      laneq_acmp_r     <= '0;
      laneq_org_r      <= '0;
      laneq_adp_cnt_r  <= 4'd0;
      laneq_acmp_cnt_r <= 4'd0;
      laneq_org_cnt_r  <= 4'd0;
    end else begin
      if (arb_gnt_w[LANE_ADP_C]) begin
        for (int unsigned i = 0; i < 7; i++) begin
          laneq_adp_r[i] <= laneq_adp_r[i + 1];
        end
      end
      if (laneq_adp_push_w) begin
        laneq_adp_r[laneq_adp_mid_w[2:0]] <= adp_txreq_slot_w;
      end
      laneq_adp_cnt_r <= laneq_adp_mid_w + (laneq_adp_push_w ? 4'd1 : 4'd0);

      if (arb_gnt_w[LANE_ACMP_C]) begin
        for (int unsigned i = 0; i < 7; i++) begin
          laneq_acmp_r[i] <= laneq_acmp_r[i + 1];
        end
      end
      if (laneq_acmp_push_w) begin
        laneq_acmp_r[laneq_acmp_mid_w[2:0]] <= lstn_txreq_slot_w;
      end
      laneq_acmp_cnt_r <= laneq_acmp_mid_w
                        + (laneq_acmp_push_w ? 4'd1 : 4'd0);

      laneq_org_r     <= laneq_org_next_w;
      laneq_org_cnt_r <= laneq_org_next_cnt_w;
    end
  end

  assign arb_req_w[LANE_AECP_SOL_C] = aecp_txreq_valid_w;
  assign arb_req_w[LANE_AECP_UNS_C] = aecp_txreq_uns_valid_w;
  assign arb_req_w[LANE_ACMP_C]     = laneq_acmp_cnt_r != 4'd0;
  assign arb_req_w[LANE_ADP_C]      = laneq_adp_cnt_r != 4'd0;
  assign arb_req_w[LANE_SRP_C]      = srp_txreq_valid_w;
  assign arb_req_w[LANE_TKRSP_C]    = tkb_lane_valid_r;
  assign arb_req_w[LANE_MAAP_C]     = maapeng_txreq_valid_w;
  assign arb_req_w[LANE_ORIG_C]     = (laneq_org_cnt_r != 4'd0)
                                    && txs_ready_nc_w[laneq_org_r[0]]
                                    && !laneq_org_release_head_w
                                    && !laneq_org_withdraw_head_w;
  assign arb_slot_w[LANE_AECP_SOL_C] = aecp_txreq_slot_w;
  assign arb_slot_w[LANE_AECP_UNS_C] = aecp_txreq_slot_w;
  assign arb_slot_w[LANE_ACMP_C]     = laneq_acmp_r[0];
  assign arb_slot_w[LANE_ADP_C]      = laneq_adp_r[0];
  assign arb_slot_w[LANE_SRP_C]      = srp_txreq_slot_w;
  assign arb_slot_w[LANE_TKRSP_C]    = tkb_slot_r;
  assign arb_slot_w[LANE_MAAP_C]     = maapeng_txreq_slot_w;
  assign arb_slot_w[LANE_ORIG_C]     = laneq_org_r[0];
  assign maapeng_txreq_ready_w = arb_gnt_w[LANE_MAAP_C];
  assign srp_txreq_ready_w  = arb_gnt_w[LANE_SRP_C];
  assign aecp_txreq_ready_w = arb_gnt_w[LANE_AECP_SOL_C];
  assign aecp_txreq_uns_ready_w = arb_gnt_w[LANE_AECP_UNS_C];
  assign tkb_lane_gnt_w    = arb_gnt_w[LANE_TKRSP_C];

  logic        arb_tx_valid_w, arb_tx_sof_w, arb_tx_eof_w, arb_tx_ready_w;
  logic [7:0]  arb_tx_data_w;
  logic        arb_start_abort_w;

  assign arb_start_abort_w = org_withdraw_slot_mask_w[ser_slot_w]
                           || (txs_release_valid_w
                               && (txs_release_slot_w == ser_slot_w));

  KL_pp_tx_arbiter #(
      //! lane 6 = MAAP (11): background class like the ADP periodic lane —
      //! Annex B attaches no response deadline to any MAAP PDU, and the
      //! T-TX-AGING guard still bounds its wait under load
      .N_REQ_P          (LANE_N_C),
      .PRIO_MAP_P       ({2'd1, 2'd3, 2'd1, 2'd2, 2'd3, 2'd0, 2'd2, 2'd1}),
      .SOLICITED_MASK_P (8'b10100101),
      .TX_STD_SLOTS_P   (TX_STD_SLOTS_P)
  ) u_tx_arbiter (
      .clk_i       (clk_i),
      .rst_n       (rst_n),
      .tick_ms_i   (tick_ms_w),
      .req_valid_i (arb_req_w),
      .tx_slot_i   (arb_slot_w),
      .start_abort_i(arb_start_abort_w),
      .gnt_o       (arb_gnt_w),
      .gnt_count_o (arb_gnt_cnt_w),
      .ser_req_o   (ser_req_w),
      .ser_slot_o  (ser_slot_w),
      .ser_valid_i (ser_valid_w),
      .ser_data_i  (ser_data_w),
      .ser_last_i  (ser_last_w),
      .ser_ready_o (ser_ready_w),
      .tx_valid_o  (arb_tx_valid_w),
      .tx_sof_o    (arb_tx_sof_w),
      .tx_data_o   (arb_tx_data_w),
      .tx_eof_o    (arb_tx_eof_w),
      .tx_ready_i  (arb_tx_ready_w)
  );

  // ---- ACMP Ethernet-header prepend shim (banner): lanes 2/5 carry bare
  // 56-byte ACMPDUs (the listener and the talker builder commit PDUs, ADP
  // and SRP commit whole frames — the recorded asymmetry of the landed
  // tree). Grants are frame-atomic, so the winning lane latched at gnt time
  // tags the very next frame; the shim stalls the arbiter for 14 cycles
  // while it emits DA 91-E0-F0-01-00-00 + own SA + EtherType 0x22F0 (03 §8
  // destination addressing: ALL ACMP traffic is that multicast).
  typedef enum logic [1:0] { SH_IDLE, SH_HDR, SH_BODY } sh_state_e;

  sh_state_e   sh_st_r;
  logic        sh_need_r;
  logic [3:0]  sh_idx_r;
  logic [111:0] sh_hdr_w;
  logic [7:0]   sh_byte_w;

  assign sh_hdr_w  = {48'h91E0_F001_0000, own_mac_i, 16'h22F0};
  assign sh_byte_w = sh_hdr_w[(7'd104 - {sh_idx_r, 3'b000}) +: 8];

  always_ff @(posedge clk_i) begin : prepend_shim
    if (!rst_n) begin
      sh_st_r   <= SH_IDLE;
      sh_need_r <= 1'b0;
      sh_idx_r  <= 4'd0;
    end else begin
      if (|arb_gnt_w) begin
        sh_need_r <= arb_gnt_w[LANE_ACMP_C] || arb_gnt_w[LANE_TKRSP_C];
      end
      unique case (sh_st_r)
        SH_IDLE: begin
          if (arb_tx_valid_w && sh_need_r) begin
            if (tx_ready_i) begin
              sh_idx_r <= 4'd1;          // header byte 0 went out this cycle
              sh_st_r  <= SH_HDR;
            end
          end
        end
        SH_HDR: begin
          if (tx_ready_i) begin
            if (sh_idx_r == 4'd13) sh_st_r <= SH_BODY;
            else                   sh_idx_r <= sh_idx_r + 4'd1;
          end
        end
        SH_BODY: begin
          if (arb_tx_valid_w && arb_tx_eof_w && tx_ready_i) begin
            sh_st_r  <= SH_IDLE;
            sh_idx_r <= 4'd0;
          end
        end
        default: sh_st_r <= SH_IDLE;
      endcase
    end
  end

  always_comb begin : shim_stream
    unique case (sh_st_r)
      SH_IDLE: begin
        if (arb_tx_valid_w && sh_need_r) begin
          tx_valid_o     = 1'b1;
          tx_sof_o       = 1'b1;
          tx_data_o      = sh_hdr_w[111:104];  // header byte 0
          tx_eof_o       = 1'b0;
          arb_tx_ready_w = 1'b0;
        end else begin
          tx_valid_o     = arb_tx_valid_w;
          tx_sof_o       = arb_tx_sof_w;
          tx_data_o      = arb_tx_data_w;
          tx_eof_o       = arb_tx_eof_w;
          arb_tx_ready_w = tx_ready_i;
        end
      end
      SH_HDR: begin
        tx_valid_o     = 1'b1;
        tx_sof_o       = 1'b0;
        tx_data_o      = sh_byte_w;
        tx_eof_o       = 1'b0;
        arb_tx_ready_w = 1'b0;
      end
      SH_BODY: begin
        tx_valid_o     = arb_tx_valid_w;
        tx_sof_o       = 1'b0;               // sof already emitted
        tx_data_o      = arb_tx_data_w;
        tx_eof_o       = arb_tx_eof_w;
        arb_tx_ready_w = tx_ready_i;
      end
      default: begin
        tx_valid_o     = arb_tx_valid_w;
        tx_sof_o       = arb_tx_sof_w;
        tx_data_o      = arb_tx_data_w;
        tx_eof_o       = arb_tx_eof_w;
        arb_tx_ready_w = tx_ready_i;
      end
    endcase
  end

  // =========================================================================
  // side port + backends: snapshot (class D aggregated), ctrl, trace
  // =========================================================================
  logic        sp_img_req_w, sp_img_we_nc_w;
  logic [15:0] sp_img_addr_nc_w;
  logic [31:0] sp_img_wdata_nc_w;
  logic        sp_img_rvalid_r;
  logic        sp_dbg_req_w;
  logic [15:0] sp_dbg_addr_nc_w;
  logic        sp_dbg_rvalid_r;
  logic        sp_snap_req_w;
  logic [15:0] sp_snap_addr_w;
  logic [31:0] sp_snap_rdata_r;
  logic        sp_snap_rvalid_r;
  logic        sp_ctrl_req_w, sp_ctrl_we_w;
  logic [7:0]  sp_ctrl_addr_w;
  logic [31:0] sp_ctrl_wdata_w;
  logic [31:0] sp_ctrl_rdata_r;
  logic        sp_ctrl_rvalid_r;
  logic        sp_trace_req_w;
  logic [15:0] sp_trace_addr_w;
  logic        sp_trace_rvalid_r;
  logic        sp_fw_req_nc_w, sp_fw_we_nc_w;
  logic [15:0] sp_fw_addr_nc_w;
  logic [31:0] sp_fw_wdata_nc_w;

  KL_pp_side_port #(.EN_FW_ASSIST_P(1'b0)) u_side_port (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .entity_enable_i (entity_enable_i),
      .req_valid_i     (host_req_valid_i),
      .we_i            (host_we_i),
      .addr_i          (host_addr_i),
      .wdata_i         (host_wdata_i),
      .rdata_o         (host_rdata_o),
      .rvalid_o        (host_rvalid_o),
      .err_o           (host_err_o),
      .img_req_o       (sp_img_req_w),
      .img_we_o        (sp_img_we_nc_w),
      .img_addr_o      (sp_img_addr_nc_w),
      .img_wdata_o     (sp_img_wdata_nc_w),
      .img_rdata_i     (32'd0),              // descriptor image RAM: P4
      .img_rvalid_i    (sp_img_rvalid_r),
      .dbg_req_o       (sp_dbg_req_w),
      .dbg_addr_o      (sp_dbg_addr_nc_w),
      .dbg_rdata_i     (32'd0),              // dynamic overlay view: P4
      .dbg_rvalid_i    (sp_dbg_rvalid_r),
      .snap_req_o      (sp_snap_req_w),
      .snap_addr_o     (sp_snap_addr_w),
      .snap_rdata_i    (sp_snap_rdata_r),
      .snap_rvalid_i   (sp_snap_rvalid_r),
      .ctrl_req_o      (sp_ctrl_req_w),
      .ctrl_we_o       (sp_ctrl_we_w),
      .ctrl_addr_o     (sp_ctrl_addr_w),
      .ctrl_wdata_o    (sp_ctrl_wdata_w),
      .ctrl_rdata_i    (sp_ctrl_rdata_r),
      .ctrl_rvalid_i   (sp_ctrl_rvalid_r),
      .trace_req_o     (sp_trace_req_w),
      .trace_addr_o    (sp_trace_addr_w),
      .trace_rdata_i   (trc_rd_data_w),
      .trace_rvalid_i  (sp_trace_rvalid_r),
      .fw_req_o        (sp_fw_req_nc_w),
      .fw_we_o         (sp_fw_we_nc_w),
      .fw_addr_o       (sp_fw_addr_nc_w),
      .fw_wdata_o      (sp_fw_wdata_nc_w),
      .fw_rdata_i      (32'd0),              // P-EN-FIRMWARE-ASSIST = 0
      .fw_rvalid_i     (1'b0)
  );

  assign trc_rd_en_w   = sp_trace_req_w;
  assign trc_rd_addr_w = sp_trace_addr_w[9:2];
  assign trc_rd_lane_w = sp_trace_addr_w[1:0];

  // snapshot window: the F02.10 class-D dictionary + front-end counters,
  // one registered read mux (word map in tb/pp_top/README.md)
  logic [31:0] ctrl_scratch_r;

  always_ff @(posedge clk_i) begin : side_backends
    if (!rst_n) begin
      sp_img_rvalid_r   <= 1'b0;
      sp_dbg_rvalid_r   <= 1'b0;
      sp_snap_rvalid_r  <= 1'b0;
      sp_snap_rdata_r   <= 32'd0;
      sp_ctrl_rvalid_r  <= 1'b0;
      sp_ctrl_rdata_r   <= 32'd0;
      sp_trace_rvalid_r <= 1'b0;
      ctrl_scratch_r    <= 32'd0;
    end else begin
      sp_img_rvalid_r   <= sp_img_req_w;
      sp_dbg_rvalid_r   <= sp_dbg_req_w;
      sp_trace_rvalid_r <= sp_trace_req_w;
      sp_snap_rvalid_r  <= sp_snap_req_w;
      sp_ctrl_rvalid_r  <= sp_ctrl_req_w;

      if (sp_ctrl_req_w && sp_ctrl_we_w && (sp_ctrl_addr_w == 8'd0)) begin
        ctrl_scratch_r <= sp_ctrl_wdata_w;
      end
      unique case (sp_ctrl_addr_w)
        8'd0:    sp_ctrl_rdata_r <= ctrl_scratch_r;
        8'd1:    sp_ctrl_rdata_r <= {28'd0, restore_fail_o, restore_done_o,
                                     restore_busy_o, entity_enable_i};
        default: sp_ctrl_rdata_r <= 32'd0;
      endcase

      unique case (sp_snap_addr_w[5:0])
        6'd0:  sp_snap_rdata_r <= 32'h4B4C_5050;               // "KLPP"
        6'd1:  sp_snap_rdata_r <= {8'(N_STREAM_IN_P), 8'(N_STREAM_OUT_P),
                                   8'(RX_SLOTS_P), 8'(TX_STD_SLOTS_P)};
        6'd2:  sp_snap_rdata_r <= now_ms_w;
        6'd3:  sp_snap_rdata_r <= {26'd0, nvm_alarm_o, srp_over_limit_w,
                                   srp_domain_adopted_w, prng_seeded_w,
                                   link_up_i, entity_enable_i};
        6'd4:  sp_snap_rdata_r <= {cnt_rx_da_w, cnt_rx_ethertype_w};
        6'd5:  sp_snap_rdata_r <= {cnt_rx_subtype_w, cnt_rx_version_w};
        6'd6:  sp_snap_rdata_r <= {cnt_rx_length_w, rxp_overrun_w[RXP_ADP_C]};
        6'd7:  sp_snap_rdata_r <= {disp_adp_level_w, disp_acmp_level_w,
                                   disp_aecp_level_w, 8'd0};
        6'd8:  sp_snap_rdata_r <= {disp_adp_stall_w, disp_acmp_stall_w};
        6'd9:  sp_snap_rdata_r <= {disp_aecp_stall_w, hdr_drop_r};
        6'd10: sp_snap_rdata_r <= {13'd0, srp_class_a_prio_w, 4'd0,
                                   srp_class_a_vid_w};
        6'd11: sp_snap_rdata_r <= srp_sum_slope_w;
        //! The snapshot window is a FIXED 32-bit register map (07 §5),
        //! so each field keeps its documented lane: sources beyond 8 are
        //! not observable here, they are on the per-source class-D ports.
        6'd12: sp_snap_rdata_r <= {8'(srp_sr_admitted_w), 8'(srp_active_w),
                                   16'(srp_tk_reg_state_w)};
        6'd13: sp_snap_rdata_r <= {16'(srp_tk_decl_state_w),
                                   16'(srp_lstn_reg_state_w)};
        6'd14: sp_snap_rdata_r <= {16'(srp_lstn_decl_state_w), 12'd0,
                                   srp_dbg_vid_active_w};
        6'd15: sp_snap_rdata_r <= {sb_holds_w, 6'd0, sb_full_w, sb_barrier_w,
                                   trc_wr_count_w};
        6'd16, 6'd17, 6'd18, 6'd19, 6'd20, 6'd21, 6'd22, 6'd23:
               sp_snap_rdata_r <= srp_acc_latency_w[sp_snap_addr_w[2:0]];
        6'd24: sp_snap_rdata_r <= {arm_drop_r, mrp_drop_w};
        6'd25: sp_snap_rdata_r <= {13'd0, 16'(rxp_slots_free_w[RXP_ADP_C]),
                                   txs_free_w};
        6'd26: sp_snap_rdata_r <= {arb_gnt_cnt_w[LANE_ACMP_C],
                                   arb_gnt_cnt_w[LANE_ADP_C]};
        6'd27: sp_snap_rdata_r <= {arb_gnt_cnt_w[LANE_SRP_C],
                                   arb_gnt_cnt_w[LANE_TKRSP_C]};
        6'd28: sp_snap_rdata_r <= {8'(bound_r), tkb_drop_r, svc_drop_r[7:0]};
        6'd29: sp_snap_rdata_r <= {rxf_drop_r, 8'd0,
                                   srp_snk_fail_code_w[0]};
        6'd30: sp_snap_rdata_r <= srp_granted_slope_w[0];
        6'd31: sp_snap_rdata_r <= {30'd0, adp_dbg_adv_state_w};
        //! AECP engine + descriptor store (06, 07 §3.3)
        6'd32: sp_snap_rdata_r <= {aecp_dbg_cmd_w, aecp_dbg_resp_w};
        6'd33: sp_snap_rdata_r <= {aecp_dbg_drop_w, aecp_dbg_miss_w};
        6'd34: sp_snap_rdata_r <= {11'd0, aecp_dbg_len_w, aecp_dbg_status_w,
                                   aecp_dbg_fault_w, aecp_dbg_img_valid_w};
        //! AECP response buffer in main memory (03 §7). A bridge that is
        //! absent, wedged or erroring voids every response the µCPU builds,
        //! and the wire only shows ENTITY_MISBEHAVING — this window is where
        //! an integrator sees WHICH channel failed and how often.
        6'd35: sp_snap_rdata_r <= {aecp_dbg_rerr_w, aecp_dbg_rlane_w};
        6'd36: sp_snap_rdata_r <= {29'd0, aecp_dbg_rfault_w};
        default: sp_snap_rdata_r <= 32'd0;
      endcase
    end
  end

endmodule : protocol_processor_top
`default_nettype wire
