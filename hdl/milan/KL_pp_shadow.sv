/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_pp_shadow.sv
  Description : Consumer-side integration wrapper for the protocol-processor
                submodule (protocol_processor_top, architecture of record
                v2.0) — the scenario-B P5 seam, in its FIRST landing shape:
                SHADOW MODE.

                WHY SHADOW AND NOT SUBSTITUTION. Scenario B's contract is
                "direct substitution at parity, old planes deleted". That is
                not reachable at this pin: the processor's AECP engine is the
                P4 micro-coded uCPU, which has NOT landed at its top — the
                AECP pop face is tied ready = 0 there and TX arbiter lanes 0
                and 1 (LANE_AECP_SOL_C / LANE_AECP_UNS_C) are, in the top's
                own words, "idle until P4". Deleting this repository's AECP
                plane against that pin would delete a shipping, live-validated
                AEM/AECP implementation and replace it with silence. So the
                first landing runs the processor ALONGSIDE the shipping
                planes and lets it drive NOTHING:

                  - it sees every control frame the shipping planes see, from
                    the same monitor tap, on real silicon and real traffic;
                  - its MAC TX byte stream is drained and COUNTED, never
                    merged into the control lane, so the wire is bit-for-bit
                    what it is today (no duplicate ADPDU, no second answer to
                    a controller — the failure mode a naive coexistence would
                    ship);
                  - its state is read out over the side port, so its ADP,
                    ACMP and SRP state machines can be compared against the
                    shipping planes' CSRs and against the wire.

                That comparison is the point. Two independent implementations
                observing one live stream is an INDEPENDENT observation in the
                sense the conformance rules demand — unlike a plane grading
                its own CSRs. When P4 lands, the substitution flips this
                wrapper's TX from the drain to the control-lane arbiter and
                deletes the old planes; nothing else here changes.

                RATE. protocol_processor_top eats a 1 byte/clk stream, which
                at 100 MHz is 100 MB/s against gigabit's 125 MB/s: a byte
                serializer fed from the raw tap CANNOT keep up with line rate,
                and would corrupt frames by lagging rather than by dropping
                them. So the tap is CLASSIFIED FIRST, at aligned beat/lane
                positions (the KL_aecp_ingress recipe), and only control
                frames enter a BRAM frame FIFO ahead of the serializer:
                EtherType 0x22F0 (any DA — the processor's own validator does
                the DA work), plus the two MRP pairs its V9 rule passes,
                DA 01-80-C2-00-00-0E + 0x22EA (MSRP) and
                DA 01-80-C2-00-00-21 + 0x88F5 (MVRP). Everything else is
                terminated into the FIFO after at most two words and reclaimed
                atomically by DROP_BAD_FRAME. Control traffic is orders of
                magnitude below the serializer's rate; a frame lost to a full
                FIFO is COUNTED (drop counter, side-port diag) and never
                silently absorbed.

                TAP DISCIPLINE. Like every other plane here this is a pure
                monitor: it drives nothing back onto rx_axis. It qualifies on
                tvalid && tready — the gh #65 handshake hazard: a stalled DMA
                parks a beat with tvalid held, and a tvalid-only tap re-eats
                it.

                NVM. The device face is answered by a BLANK-FLASH responder
                (reads 0xFF, writes accepted and discarded, erase completes).
                That is the processor's documented no-saved-binding path, and
                it is deliberately NOT persistent: shadow mode must not write
                the board's flash, and it has no business owning a region of
                it while the shipping planes own binding persistence.

                CLASS-D FABRIC FACE. Everything the processor knows used to be
                reachable only through a side-port READ TRANSACTION - a
                software-paced path. An integrating fabric consumes that state
                as WIRES, every clock: a talker gate is a per-cycle AND of the
                DA gate and the stream enable, a CBS slope MUX needs the
                granted idleSlope, an RX filter needs the bound stream's DMAC.
                So every class-D output protocol_processor_top publishes is
                republished here, 1:1, same names and same flat packing. This
                wrapper adds NO logic on that path and NO interpretation: it
                is a port list, and the point of it being a port list is that
                the two files read as one contract.

                ADDRESS ALLOCATION. The processor implements no MAAP by
                design (its 01 section 3 puts allocation in the integrating
                fabric) and publishes a per-source ALLOC/RELEASE face instead.
                This fabric's allocator is KL_maap, which claims one BLOCK.
                KL_pp_maap_shim.sv bridges the two models and
                milan_datapath.sv wires it between them; the 10 maap pins here
                are a pass-through so the shim can live outside this wrapper,
                next to the engine it adapts. Note what depends on it: the DA
                gate (acmp_declaring_o) is reachable ONLY through an ALLOC_DA
                success, so with the face unconnected the processor's talker
                half is dead by construction.

  Interfaces  : monitor tap on the MAC RX AXIS stream (input only);
                a simple request/ack host bridge for the side port;
                the class-D status levels and the maap request face;
                a diagnostic bundle for the CSR.

  Parameters  : see below; N_STREAM_IN_P/N_STREAM_OUT_P size the processor's
                sink/source arrays and must not exceed what the entity model
                declares.
------------------------------------------------------------------------------
*/

`default_nettype none
//! The vendored Forencich .v sources carry a timescale; a build that mixes
//! them with timescale-less SystemVerilog is flagged (IEEE 1800-2023 3.14.2.3).
//! Simulation-only — synthesis ignores it.
`timescale 1ns/1ps

module KL_pp_shadow #(
    //! MAC RX AXIS data width (the datapath's TDATA_WIDTH). 64 only.
    parameter int unsigned TDATA_WIDTH_P  = 64,
    //! core clock, feeds the processor's timer prescaler
    parameter int unsigned CLK_HZ_P       = 100_000_000,
    //! processor sink/source array sizes (F01.5 P-N-STREAM-IN/OUT)
    parameter int unsigned N_STREAM_IN_P  = 8,
    parameter int unsigned N_STREAM_OUT_P = 8,
    //! control-frame FIFO, bytes. One 1522 B frame fits with margin for the
    //! serializer's lag; 4096 is one RAMB36 at 64 b.
    parameter int unsigned RX_FIFO_BYTES_P = 4096,
    //! Timer-prescaler pass-through (09 §3 TIM time compression). The defaults
    //! are REAL time and are what silicon builds use; a testbench overrides
    //! them so a 5 s ADP cadence is reachable in a simulation, exactly as the
    //! datapath already does for CLKV_QTICK_CYC_P / LDIAG_IVAL_CYC_P. They are
    //! DERIVED from CLK_HZ_P here, never mirrored as a second literal.
    parameter int unsigned TIM_DIV_US_P = CLK_HZ_P / 32'd1_000_000,
    parameter int unsigned TIM_DIV_MS_P = 1000,
    //! ACMP listener transition-ROM image (hdl/acmp/rom/gen_ltn_rom.py)
    parameter string       TROM_HEX_P      = "ltn_rom.hex",
    //! Which talker SOURCES the processor is told exist in the current
    //! configuration (its cfg_src_en_i, bit s = source s). DEFAULT 0 = none,
    //! and that default is the shadow contract: with no source enabled the
    //! processor never allocates a DA, never declares a Talker attribute and
    //! never touches a stream the shipping lwSRP/ACMP planes already own, so
    //! every existing build keeps exactly the behaviour it has today.
    //!
    //! A non-zero mask turns the talker half ON inside the shadow. It stays
    //! wire-safe - the processor's TX is drained by tx_drain_i, so its SRP
    //! declarations and ACMP responses are counted and thrown away - but it
    //! is the only way to EXERCISE the maap face and the DA gate, so the
    //! pp_shadow harness elaborates with it set.
    //!
    //! It is a PARAMETER and not a CSR bit on purpose. Which sources exist is
    //! a property of the entity model, which is elaboration-static in this
    //! repository (the shape is READ-ONLY from build parameters, never poked
    //! at runtime). At the P4 substitution this is where the generated entity
    //! model's talker count gets wired in; until then a live CSR bit would be
    //! a second, drifting copy of a number the AEM already owns.
    parameter int unsigned SRC_EN_MASK_P   = 0,
    //! derived source-index width for the maap face — do not override.
    //! CLAMPED exactly as protocol_processor_top clamps its own SRC_IDX_W_C,
    //! because the shipping board elaborates this at N_STREAM_OUT_P = 1 and
    //! an unclamped $clog2(1) declares [-1:0].
    localparam int unsigned SRC_IDX_W_C = (N_STREAM_OUT_P > 32'd1)
                                          ? $clog2(N_STREAM_OUT_P) : 32'd1
) (
    input  wire        clk_i,              //! axis_clk
    input  wire        rst_n,              //! active-low reset

    //! ---- quasi-static identity (from the CSR / entity model) ----
    input  wire [63:0] entity_id_i,        //! own entity_id
    input  wire [63:0] entity_model_id_i,  //! entity_model_id
    input  wire [47:0] station_mac_i,      //! own unicast MAC, NUMERIC EUI-48
                                           //! ([47:40] = first wire byte)
    input  wire [15:0] talker_sources_i,   //! ADPDU talker_stream_sources
    input  wire [15:0] talker_caps_i,      //! ADPDU talker_capabilities
    input  wire [15:0] listener_sinks_i,   //! ADPDU listener_stream_sinks
    input  wire [15:0] listener_caps_i,    //! ADPDU listener_capabilities

    //! ---- level controls ----
    input  wire        enable_i,           //! Milan 5.6.1 boot gate (CSR bit)
    input  wire        restore_go_i,       //! start the NVM boot restore walk
    input  wire        link_up_i,          //! link status (already synced)
    input  wire        gm_change_i,        //! GM_CHANGE strobe from gptp
    input  wire [63:0] gm_id_i,            //! current gm_id
    input  wire [7:0]  gptp_domain_i,      //! current gptp domain number

    //! ---- MAC RX monitor tap (INPUT ONLY — never drives tready) ----
    input  wire [TDATA_WIDTH_P-1:0]     rx_tdata_i,  //! little lane order
    input  wire [TDATA_WIDTH_P/8-1:0]   rx_tkeep_i,  //! final-beat byte mask
    input  wire                         rx_tvalid_i, //! beat valid
    input  wire                         rx_tready_i, //! consumer accepts (gh #65)
    input  wire                         rx_tlast_i,  //! final beat of frame

    //! ---- side-port host bridge (CSR-driven, one outstanding access) ----
    input  wire        host_req_i,         //! single-cycle request strobe
    input  wire        host_we_i,          //! 1 = write
    input  wire [19:0] host_addr_i,        //! 20-bit WORD address
    input  wire [31:0] host_wdata_i,       //! write data
    output logic [31:0] host_rdata_o,      //! read data, valid with ack
    output logic       host_ack_o,         //! completion strobe
    output logic       host_err_o,         //! access refused (with ack)

    //! ---- MAC TX, packed to AXIS (the control-lane leg) ----
    //! The processor emits ONE merged byte stream for every protocol it
    //! owns; its per-protocol arbitration is internal. Today that stream
    //! carries ADP + ACMP + SRP only — the AECP lanes are idle until P4 —
    //! so it can ride the control cascade as a single leg alongside the
    //! shipping AECP leg, which is what makes a partial substitution work.
    //!
    //! SHADOW: while nothing consumes this port the wrapper still drains the
    //! processor (see tx_drain_i), so the wire is unchanged. Connecting it to
    //! the arbiter is the substitution step, and the ONLY step.
    output logic [TDATA_WIDTH_P-1:0]   m_axis_tx_tdata,  //! little lane order
    output logic [TDATA_WIDTH_P/8-1:0] m_axis_tx_tkeep,  //! contiguous from lane 0
    output logic                       m_axis_tx_tvalid,
    output logic                       m_axis_tx_tlast,
    input  wire                        m_axis_tx_tready,
    //! 1 = discard the processor's frames and count them (shadow mode);
    //! 0 = the packed AXIS port above is the real egress.
    input  wire                        tx_drain_i,

    //! ---- maap face (02 §4.2) — THE ADDRESS ALLOCATOR SEAM ----
    //! Passed straight through to protocol_processor_top, names and
    //! directions unchanged. The fabric's allocator is a BLOCK allocator
    //! (KL_maap) and this is a PER-SOURCE face; KL_pp_maap_shim.sv bridges
    //! the two and milan_datapath.sv wires it between them. Leaving these
    //! unconnected is legal but structurally kills the talker half: the DA
    //! gate below is reachable only through an ALLOC_DA success, so
    //! acmp_declaring_o would be stuck at 0 and no source would ever declare
    //! a Talker attribute to SRP either.
    output logic                       maap_req_valid_o,      //! ALLOC/RELEASE, held until ready
    input  wire                        maap_req_ready_i,      //! allocator accepts (0 = no allocator)
    output logic                       maap_req_release_o,    //! 0 = ALLOC_DA, 1 = RELEASE_DA
    output logic [SRC_IDX_W_C-1:0]     maap_req_src_o,        //! source index of the request
    input  wire                        maap_rsp_valid_i,      //! exactly one response per accepted request
    input  wire                        maap_rsp_ok_i,         //! ALLOC_DA succeeded (ignored on RELEASE_DA)
    input  wire  [47:0]                maap_rsp_da_i,         //! allocated stream destination MAC
    input  wire                        maap_conflict_valid_i, //! MAAP_CONFLICT{source}, sticky until acked
    input  wire  [SRC_IDX_W_C-1:0]     maap_conflict_src_i,   //! conflicted source
    output logic                       maap_conflict_ack_o,   //! event ack (combinational)

    //! ---- class-D SRP status levels (02 §6, F02.10) — THE FABRIC FACE ----
    //! Every one of these is a straight pass-through of the identically named
    //! protocol_processor_top output: same name, same width, same flat
    //! packing (index s at [W*s +: W]), so the two port lists read as ONE
    //! contract and a divergence is a compile error rather than a silent
    //! re-interpretation. They are combinational reads of clk_i-domain
    //! registers; a consumer in another clock domain owns its own 2FF
    //! synchroniser. Read protocol_processor_top.sv's own banner for what
    //! each level MEANS - it is not repeated here, because a second copy of
    //! that prose is a second copy that drifts.
    output logic [2:0]                   srp_class_a_prio_o,      //! SRclassPriority, DEFAULTS until adopted
    output logic [11:0]                  srp_class_a_vid_o,       //! SRclassVID, DEFAULTS until adopted
    output logic                         srp_domain_adopted_o,    //! 1 = adopted a bridge Domain
    output logic                         srp_domain_change_o,     //! one-cycle DOMAIN_CHANGE
    output logic [N_STREAM_OUT_P*2-1:0]  srp_tk_decl_state_o,     //! per-source self-declared Talker attr
    output logic [N_STREAM_OUT_P*2-1:0]  srp_lstn_reg_state_o,    //! per-source registered Listener attr
    //! THE AVTP transmit gate — never rebuild it from the terms below
    output logic [N_STREAM_OUT_P-1:0]    srp_active_o,
    //! RAW Sigma-slope verdict; lags srp_active_o by up to three admission rounds
    output logic [N_STREAM_OUT_P-1:0]    srp_sr_admitted_o,
    output logic [N_STREAM_OUT_P*32-1:0] srp_granted_slope_bps_o, //! per-source granted idleSlope
    output logic [N_STREAM_OUT_P*8-1:0]  srp_src_fail_code_o,     //! per-source self-declared Failed code
    output logic [N_STREAM_OUT_P*64-1:0] srp_src_fail_bridge_o,   //! per-source self-declared FailureInformation
    output logic [31:0]                  srp_sum_slope_bps_o,     //! Sigma granted idleSlope over admitted sources
    output logic                         srp_over_limit_o,        //! a source was refused against the port ceiling
    output logic [N_STREAM_IN_P*2-1:0]   srp_tk_reg_state_o,      //! per-sink registered Talker attr
    output logic [N_STREAM_IN_P*2-1:0]   srp_lstn_decl_state_o,   //! per-sink our Listener declaration
    output logic [N_STREAM_IN_P*32-1:0]  srp_acc_latency_o,       //! per-sink registered accumulated_latency, ns, RAW
    output logic [N_STREAM_IN_P*8-1:0]   srp_snk_fail_code_o,     //! per-sink registered Failed code

    //! ---- class-D ACMP / ADP status levels ----
    output logic [N_STREAM_OUT_P-1:0]    acmp_declaring_o,        //! per-source DA gate open (THE talker egress gate)
    output logic [N_STREAM_IN_P-1:0]     acmp_bound_o,            //! per-sink binding installed, DEBOUNCED
    output logic [N_STREAM_IN_P*64-1:0]  acmp_bound_eid_o,        //! per-sink bound talker entity_id
    output logic [N_STREAM_IN_P*64-1:0]  acmp_bound_sid_o,        //! per-sink bound stream_id
    output logic [N_STREAM_IN_P*48-1:0]  acmp_bound_dmac_o,       //! per-sink bound stream destination MAC
    output logic [N_STREAM_IN_P*12-1:0]  acmp_bound_vlan_o,       //! per-sink bound stream VLAN id
    output logic [31:0]                  adp_next_avail_index_o,  //! available_index the NEXT ENTITY_AVAILABLE carries

    //! ---- observability ----
    output logic       restore_busy_o,     //! restore walk running
    output logic       restore_done_o,     //! restore complete
    output logic       restore_fail_o,     //! torn read-back aborted restore
    output logic       nvm_alarm_o,        //! commit retries exhausted
    output logic [15:0] rx_frames_o,       //! control frames handed to the PP
    output logic [7:0] rx_drops_o,         //! frames lost to a full FIFO
    output logic [15:0] tx_frames_o,       //! frames the PP WOULD have sent
    output logic [31:0] dbg_now_ms_o       //! the processor's ms timebase
);

  localparam int unsigned KEEP_W_C = TDATA_WIDTH_P/8;

  // V9 / EtherType constants — MUST match KL_pp_rx_validator's own
  // (DA_MSRP_C / DA_MVRP_C / ET_1722_C / ET_MSRP_C / ET_MVRP_C). A frame this
  // filter drops is a frame the processor can never see, so a divergence here
  // is silent starvation, not a wrong answer.
  localparam logic [47:0] DA_MSRP_C = 48'h01_80_C2_00_00_0E;
  localparam logic [47:0] DA_MVRP_C = 48'h01_80_C2_00_00_21;
  localparam logic [15:0] ET_1722_C = 16'h22F0;
  localparam logic [15:0] ET_MSRP_C = 16'h22EA;
  localparam logic [15:0] ET_MVRP_C = 16'h88F5;

  // ======================================================================= //
  //  RX classify + forward (aligned lanes only, no variable byte muxes)     //
  // ======================================================================= //
  //! A beat is consumed by the stream only when both sides handshake.
  logic beat_w;
  assign beat_w = rx_tvalid_i & rx_tready_i;

  //! beat 0: DA lanes 0-5. beat 1: EtherType lanes 4-5 (wire bytes 12,13).
  logic [47:0] da_num_w;
  logic [15:0] etype_w;
  assign da_num_w = {rx_tdata_i[7:0],   rx_tdata_i[15:8],
                     rx_tdata_i[23:16], rx_tdata_i[31:24],
                     rx_tdata_i[39:32], rx_tdata_i[47:40]};
  //! EtherType is wire bytes 12,13 = beat-1 LANES 4 and 5, i.e. tdata[39:32]
  //! and tdata[47:40] (lane j = tdata[8j +: 8]). Getting this one lane wrong
  //! reads bytes 13,14 instead and NOTHING is ever classified as control —
  //! the tap goes silently deaf, which is exactly how the pp_shadow suite
  //! found it: every accept check read a structural zero while the processor
  //! itself was demonstrably alive on the side port and transmitting.
  //! KL_maap.sv:275-277 is the silicon-proven reference: lane 4 == 0x22,
  //! lane 5 == 0xF0.
  assign etype_w  = {rx_tdata_i[39:32], rx_tdata_i[47:40]};

  typedef enum logic [1:0] {FW_HEAD0, FW_HEAD1, FW_BODY, FW_SKIP} fw_state_e;
  fw_state_e fw_S;

  logic [47:0] da_r;      //! DA latched at beat 0, tested at beat 1

  logic                     fw_valid_w, fw_last_w, fw_user_w;
  logic [TDATA_WIDTH_P-1:0] fw_data_w;
  logic [KEEP_W_C-1:0]      fw_keep_w;
  logic                     fw_ready_w;

  //! accept decision, evaluated at beat 1 against the latched DA
  logic accept_w;
  assign accept_w = (etype_w == ET_1722_C)
                 || ((da_r == DA_MSRP_C) && (etype_w == ET_MSRP_C))
                 || ((da_r == DA_MVRP_C) && (etype_w == ET_MVRP_C));

  always_comb begin
    fw_valid_w = 1'b0;
    fw_data_w  = rx_tdata_i;
    fw_keep_w  = rx_tkeep_i;
    fw_last_w  = rx_tlast_i;
    fw_user_w  = 1'b0;
    unique case (fw_S)
      FW_HEAD0: begin
        // Always write beat 0 — the decision is not available until beat 1.
        // A frame ending here is a runt (< 8 B): mark it bad.
        fw_valid_w = beat_w;
        fw_user_w  = rx_tlast_i;
      end
      FW_HEAD1: begin
        fw_valid_w = beat_w;
        // Reject: terminate the frame into the FIFO NOW (2 words spent,
        // reclaimed atomically) instead of streaming the whole thing.
        if (!accept_w) begin
          fw_last_w = 1'b1;
          fw_user_w = 1'b1;
        end
      end
      FW_BODY: begin
        fw_valid_w = beat_w;
      end
      default: begin  // FW_SKIP — the rest of a rejected frame
        fw_valid_w = 1'b0;
      end
    endcase
  end

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      fw_S <= FW_HEAD0;
      da_r <= 48'd0;
    end else if (beat_w) begin
      unique case (fw_S)
        FW_HEAD0: begin
          da_r <= da_num_w;
          fw_S <= rx_tlast_i ? FW_HEAD0 : FW_HEAD1;
        end
        FW_HEAD1: fw_S <= rx_tlast_i ? FW_HEAD0
                                     : (accept_w ? FW_BODY : FW_SKIP);
        FW_BODY:  if (rx_tlast_i) fw_S <= FW_HEAD0;
        default:  if (rx_tlast_i) fw_S <= FW_HEAD0;  // FW_SKIP
      endcase
    end
  end

  //! A control frame offered while the FIFO cannot take it is LOST. The tap
  //! cannot backpressure the NIC, so this is counted, never hidden: fw_ready
  //! low during an accepted write is the only way a frame goes missing.
  logic drop_evt_w;
  assign drop_evt_w = fw_valid_w & ~fw_ready_w
                    & ((fw_S == FW_HEAD0) || (fw_S == FW_HEAD1)
                       || (fw_S == FW_BODY));

  logic [TDATA_WIDTH_P-1:0] ff_data_w;
  logic [KEEP_W_C-1:0]      ff_keep_w;
  logic                     ff_valid_w, ff_last_w, ff_ready_w;

  axis_fifo #(
    .DEPTH               (RX_FIFO_BYTES_P),
    .DATA_WIDTH          (TDATA_WIDTH_P),
    .KEEP_ENABLE         (1),
    .KEEP_WIDTH          (KEEP_W_C),
    .LAST_ENABLE         (1),
    .ID_ENABLE           (0),
    .DEST_ENABLE         (0),
    .USER_ENABLE         (1),
    .USER_WIDTH          (1),
    .FRAME_FIFO          (1),
    .USER_BAD_FRAME_VALUE(1'b1),
    .USER_BAD_FRAME_MASK (1'b1),
    .DROP_BAD_FRAME      (1),
    .DROP_OVERSIZE_FRAME (1),
    .DROP_WHEN_FULL      (1)
  ) ctl_fifo (
    .clk                (clk_i),
    .rst                (~rst_n),
    .s_axis_tdata       (fw_data_w),
    .s_axis_tkeep       (fw_keep_w),
    .s_axis_tvalid      (fw_valid_w),
    .s_axis_tready      (fw_ready_w),
    .s_axis_tlast       (fw_last_w),
    .s_axis_tid         ('0),
    .s_axis_tdest       ('0),
    .s_axis_tuser       (fw_user_w),
    .m_axis_tdata       (ff_data_w),
    .m_axis_tkeep       (ff_keep_w),
    .m_axis_tvalid      (ff_valid_w),
    .m_axis_tready      (ff_ready_w),
    .m_axis_tlast       (ff_last_w),
    .m_axis_tid         (),
    .m_axis_tdest       (),
    .m_axis_tuser       (),
    .status_overflow    (),
    .status_bad_frame   (),
    .status_good_frame  (),
    .status_depth       (),
    .status_depth_commit(),
    .pause_req          (1'b0),
    .pause_ack          ()
  );

  // ======================================================================= //
  //  Byte serializer — 64 b words out of the FIFO, 1 B/clk into the PP      //
  // ======================================================================= //
  logic [TDATA_WIDTH_P-1:0] ser_data_r;
  logic [KEEP_W_C-1:0]      ser_keep_r;
  logic                     ser_last_r;
  logic                     ser_busy_r;
  logic [2:0]               ser_idx_r;

  //! last valid lane of the held word (keep is contiguous from lane 0)
  logic [2:0] ser_top_w;
  always_comb begin
    ser_top_w = 3'd0;
    for (int unsigned i = 0; i < KEEP_W_C; i++) begin
      if (ser_keep_r[i]) ser_top_w = 3'(i);
    end
  end

  //! pop only when idle: one word in flight at a time
  assign ff_ready_w = ~ser_busy_r;

  logic       pp_rx_valid_w;
  logic [7:0] pp_rx_data_w;
  logic       pp_rx_last_w;

  assign pp_rx_valid_w = ser_busy_r;
  assign pp_rx_data_w  = ser_data_r[8*ser_idx_r +: 8];
  assign pp_rx_last_w  = ser_busy_r & ser_last_r & (ser_idx_r == ser_top_w);

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      ser_busy_r <= 1'b0;
      ser_idx_r  <= 3'd0;
      ser_data_r <= '0;
      ser_keep_r <= '0;
      ser_last_r <= 1'b0;
    end else if (!ser_busy_r) begin
      if (ff_valid_w) begin
        ser_data_r <= ff_data_w;
        ser_keep_r <= ff_keep_w;
        ser_last_r <= ff_last_w;
        ser_idx_r  <= 3'd0;
        ser_busy_r <= 1'b1;
      end
    end else begin
      if (ser_idx_r == ser_top_w) ser_busy_r <= 1'b0;
      else                        ser_idx_r  <= ser_idx_r + 3'd1;
    end
  end

  // ======================================================================= //
  //  Blank-flash NVM responder (NOT persistent — see the banner)            //
  // ======================================================================= //
  localparam logic [1:0] NVMP_OP_READ_C  = 2'd0;
  localparam logic [1:0] NVMP_OP_WRITE_C = 2'd1;

  logic        nvm_req_w, nvm_wvalid_w, nvm_rready_w;
  logic [1:0]  nvm_op_w;
  logic [15:0] nvm_len_w;
  logic        nvm_gnt_r, nvm_done_r, nvm_rvalid_r, nvm_wready_r;
  logic [15:0] nvm_cnt_r;
  logic        nvm_busy_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      nvm_busy_r   <= 1'b0;
      nvm_gnt_r    <= 1'b0;
      nvm_done_r   <= 1'b0;
      nvm_rvalid_r <= 1'b0;
      nvm_wready_r <= 1'b0;
      nvm_cnt_r    <= 16'd0;
    end else begin
      nvm_gnt_r  <= 1'b0;
      nvm_done_r <= 1'b0;
      if (!nvm_busy_r) begin
        nvm_rvalid_r <= 1'b0;
        nvm_wready_r <= 1'b0;
        if (nvm_req_w) begin
          nvm_gnt_r  <= 1'b1;
          nvm_cnt_r  <= nvm_len_w;
          nvm_busy_r <= 1'b1;
          // ERASE (and any zero-length command) completes with no data phase
          if ((nvm_op_w != NVMP_OP_READ_C && nvm_op_w != NVMP_OP_WRITE_C)
              || (nvm_len_w == 16'd0)) begin
            nvm_busy_r <= 1'b0;
            nvm_done_r <= 1'b1;
          end else begin
            nvm_rvalid_r <= (nvm_op_w == NVMP_OP_READ_C);
            nvm_wready_r <= (nvm_op_w == NVMP_OP_WRITE_C);
          end
        end
      end else begin
        // one byte per accepted handshake, blank flash reads as 0xFF
        if ((nvm_rvalid_r & nvm_rready_w) | (nvm_wready_r & nvm_wvalid_w)) begin
          if (nvm_cnt_r <= 16'd1) begin
            nvm_busy_r   <= 1'b0;
            nvm_rvalid_r <= 1'b0;
            nvm_wready_r <= 1'b0;
            nvm_done_r   <= 1'b1;
          end else begin
            nvm_cnt_r <= nvm_cnt_r - 16'd1;
          end
        end
      end
    end
  end

  // ======================================================================= //
  //  The processor                                                          //
  // ======================================================================= //
  logic        pp_tx_valid_w, pp_tx_eof_w;
  logic [7:0]  pp_tx_data_w;
  logic        pp_host_rvalid_w, pp_host_err_w;
  logic [31:0] pp_host_rdata_w;

  //! one outstanding side-port access: hold the request until it completes
  logic        hb_pend_r, hb_we_r;
  logic [19:0] hb_addr_r;
  logic [31:0] hb_wdata_r;

  protocol_processor_top #(
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .CLK_HZ_P       (CLK_HZ_P),
      .TIM_DIV_US_P   (TIM_DIV_US_P),
      .TIM_DIV_MS_P   (TIM_DIV_MS_P),
      .TROM_HEX_P     (TROM_HEX_P)
  ) u_pp (
      .clk_i               (clk_i),
      .rst_n               (rst_n),

      .entity_id_i         (entity_id_i),
      .entity_model_id_i   (entity_model_id_i),
      .own_mac_i           (station_mac_i),
      .talker_sources_i    (talker_sources_i),
      .talker_caps_i       (talker_caps_i),
      .listener_sinks_i    (listener_sinks_i),
      .listener_caps_i     (listener_caps_i),
      .current_cfg_i       (16'd0),
      .identify_index_i    (16'd0),

      .entity_enable_i     (enable_i),
      .link_up_i           (link_up_i),
      .gm_change_i         (gm_change_i),
      .gm_id_i             (gm_id_i),
      .gptp_domain_i       (gptp_domain_i),

      //! SRP quasi-static: Milan mandates point-to-point; the rest are the
      //! engine's own defaults and are inert while the service face is idle.
      .p2p_i               (1'b1),
      .cfg_rank_i          (1'b0),
      .cfg_acc_lat_ns_i    (32'd0),
      .port_rate_bps_i     (32'd1_000_000_000),
      .cfg_tspec_max_frame_i(16'd0),

      //! Which talker sources exist, from SRC_EN_MASK_P (default 0 = none;
      //! see the parameter's banner for why a source-enable is elaboration
      //! static here and what turning it on does).
      .cfg_src_en_i        (N_STREAM_OUT_P'(SRC_EN_MASK_P)),
      //! ONE AVB interface on this board, so every source sits on interface
      //! 0. This is not a placeholder: KL_acmp_talker SILENTLY IGNORES a
      //! PROBE_TX whose interface_index disagrees with the source's, and the
      //! processor's own rx_if_index is 0, so any other value here would make
      //! the talker deaf with no counter moving anywhere.
      .cfg_src_iface_i     ('0),
      //! stream_id stays 0: it is consumed only by the processor's SRP
      //! DECLARE_TALKER, and the shipping lwSRP plane owns the reservation
      //! for these streams. A shadow that declared a real stream_id would be
      //! a second applicant for the same stream on the same port.
      .cfg_stream_id_i     ('0),

      .rx_valid_i          (pp_rx_valid_w),
      .rx_data_i           (pp_rx_data_w),
      .rx_last_i           (pp_rx_last_w),

      .tx_valid_o          (pp_tx_valid_w),
      .tx_sof_o            (),
      .tx_data_o           (pp_tx_data_w),
      .tx_eof_o            (pp_tx_eof_w),
      .tx_ready_i          (pp_tx_ready_w),

      //! P4 uCPU seam — unlanded at this pin, tied per the top's contract
      .aecp_txn_valid_o    (),
      .aecp_txn_o          (),
      .aecp_txn_ready_i    (1'b0),
      .aecp_rxs_rd_slot_i  ('0),
      .aecp_rxs_rd_addr_i  ('0),
      .aecp_rxs_rd_en_i    (1'b0),
      .aecp_rxs_rd_data_o  (),
      .aecp_rxs_slot_len_o (),
      .aecp_rxs_free_i     (1'b0),
      .aecp_rxs_free_slot_i('0),

      .restore_go_i        (restore_go_i),
      .restore_busy_o      (restore_busy_o),
      .restore_done_o      (restore_done_o),
      .restore_fail_o      (restore_fail_o),
      .nvm_alarm_o         (nvm_alarm_o),

      .nvm_dev_req_o       (nvm_req_w),
      .nvm_dev_gnt_i       (nvm_gnt_r),
      .nvm_dev_op_o        (nvm_op_w),
      .nvm_dev_region_o    (),
      .nvm_dev_offset_o    (),
      .nvm_dev_len_o       (nvm_len_w),
      .nvm_dev_wvalid_o    (nvm_wvalid_w),
      .nvm_dev_wready_i    (nvm_wready_r),
      .nvm_dev_wdata_o     (),
      .nvm_dev_rvalid_i    (nvm_rvalid_r),
      .nvm_dev_rdata_i     (8'hFF),
      .nvm_dev_rready_o    (nvm_rready_w),
      .nvm_dev_busy_i      (nvm_busy_r),
      .nvm_dev_done_i      (nvm_done_r),
      .nvm_dev_err_i       (1'b0),

      .host_req_valid_i    (hb_pend_r),
      .host_we_i           (hb_we_r),
      .host_addr_i         (hb_addr_r),
      .host_wdata_i        (hb_wdata_r),
      .host_rdata_o        (pp_host_rdata_w),
      .host_rvalid_o       (pp_host_rvalid_w),
      .host_err_o          (pp_host_err_w),

      //! config-plane seam: unused in shadow mode
      .svc_valid_i         (1'b0),
      .svc_ready_o         (),
      .svc_op_i            ('0),
      .svc_index_i         ('0),
      .svc_stream_id_i     ('0),
      .svc_da_i            ('0),
      .svc_vid_i           ('0),
      .svc_max_frame_i     ('0),
      .svc_lstn_state_i    ('0),
      .svc_rsp_valid_o     (),
      .svc_rsp_status_o    (),
      .svc_rsp_data_o      (),

      //! ---- class-D fabric face: straight through, 1:1 ------------------
      //! Deliberately NOT repacked, NOT reduced and NOT renamed. A consumer
      //! needs the per-index values (its CBS slope MUX reads one source's
      //! granted slope, its RX filter reads one sink's DMAC), and the flat
      //! [W*s +: W] packing is the same convention cfg_stream_id_i already
      //! uses in the other direction.
      .srp_class_a_prio_o      (srp_class_a_prio_o),
      .srp_class_a_vid_o       (srp_class_a_vid_o),
      .srp_domain_adopted_o    (srp_domain_adopted_o),
      .srp_domain_change_o     (srp_domain_change_o),
      .srp_tk_decl_state_o     (srp_tk_decl_state_o),
      .srp_lstn_reg_state_o    (srp_lstn_reg_state_o),
      .srp_active_o            (srp_active_o),
      .srp_sr_admitted_o       (srp_sr_admitted_o),
      .srp_granted_slope_bps_o (srp_granted_slope_bps_o),
      .srp_src_fail_code_o     (srp_src_fail_code_o),
      .srp_src_fail_bridge_o   (srp_src_fail_bridge_o),
      .srp_sum_slope_bps_o     (srp_sum_slope_bps_o),
      .srp_over_limit_o        (srp_over_limit_o),
      .srp_tk_reg_state_o      (srp_tk_reg_state_o),
      .srp_lstn_decl_state_o   (srp_lstn_decl_state_o),
      .srp_acc_latency_o       (srp_acc_latency_o),
      .srp_snk_fail_code_o     (srp_snk_fail_code_o),
      .acmp_declaring_o        (acmp_declaring_o),
      .acmp_bound_o            (acmp_bound_o),
      .acmp_bound_eid_o        (acmp_bound_eid_o),
      .acmp_bound_sid_o        (acmp_bound_sid_o),
      .acmp_bound_dmac_o       (acmp_bound_dmac_o),
      .acmp_bound_vlan_o       (acmp_bound_vlan_o),
      .adp_next_avail_index_o  (adp_next_avail_index_o),

      //! ---- maap face: straight through to KL_pp_maap_shim outside -------
      .maap_req_valid_o        (maap_req_valid_o),
      .maap_req_ready_i        (maap_req_ready_i),
      .maap_req_release_o      (maap_req_release_o),
      .maap_req_src_o          (maap_req_src_o),
      .maap_rsp_valid_i        (maap_rsp_valid_i),
      .maap_rsp_ok_i           (maap_rsp_ok_i),
      .maap_rsp_da_i           (maap_rsp_da_i),
      .maap_conflict_valid_i   (maap_conflict_valid_i),
      .maap_conflict_src_i     (maap_conflict_src_i),
      .maap_conflict_ack_o     (maap_conflict_ack_o),

      .dbg_now_ms_o        (dbg_now_ms_o)
  );

  // ======================================================================= //
  //  TX packer — the processor's 1 B/clk stream into 64 b AXIS beats        //
  // ======================================================================= //
  //! Little lane order, matching the RX tap and every plane on this board:
  //! wire byte n of a beat lands in lane n, tdata[8n +: 8].
  //!
  //! The processor offers at most one byte per clock and a beat carries
  //! eight, so a single beat register is always faster than the source; it
  //! only has to stall the processor while a completed beat waits for the
  //! arbiter. That stall is the whole backpressure story — there is no FIFO
  //! here and none is needed.
  //!
  //! In drain mode the packer still runs, so the frame COUNTER and the
  //! packing logic are exercised identically to the wired case; only the
  //! egress is thrown away. A drain that bypassed the packer would leave it
  //! untested until the day it first mattered.
  logic [TDATA_WIDTH_P-1:0]   txp_data_r;
  logic [KEEP_W_C-1:0]        txp_keep_r;
  logic                       txp_valid_r, txp_last_r;
  logic [2:0]                 txp_idx_r;

  //! a completed beat is consumed by the arbiter, or swallowed when draining
  logic txp_take_w;
  assign txp_take_w = txp_valid_r & (tx_drain_i | m_axis_tx_tready);

  //! room for another byte: only when no completed beat is waiting
  logic pp_tx_ready_w;
  assign pp_tx_ready_w = ~txp_valid_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      txp_data_r  <= '0;
      txp_keep_r  <= '0;
      txp_valid_r <= 1'b0;
      txp_last_r  <= 1'b0;
      txp_idx_r   <= 3'd0;
    end else begin
      if (txp_take_w) begin
        txp_valid_r <= 1'b0;
        txp_keep_r  <= '0;
        txp_data_r  <= '0;
      end
      if (pp_tx_valid_w & pp_tx_ready_w) begin
        txp_data_r[8*txp_idx_r +: 8] <= pp_tx_data_w;
        txp_keep_r[txp_idx_r]        <= 1'b1;
        //! close the beat on the 8th byte OR at end of frame, whichever
        //! comes first — tkeep then marks exactly the bytes that are real
        if (pp_tx_eof_w || (txp_idx_r == 3'd7)) begin
          txp_valid_r <= 1'b1;
          txp_last_r  <= pp_tx_eof_w;
          txp_idx_r   <= 3'd0;
        end else begin
          txp_idx_r <= txp_idx_r + 3'd1;
        end
      end
    end
  end

  //! tvalid is held low while draining so a stray connection cannot put a
  //! shadow frame on the wire: the drain is structural, not a convention.
  assign m_axis_tx_tdata  = txp_data_r;
  assign m_axis_tx_tkeep  = txp_keep_r;
  assign m_axis_tx_tvalid = txp_valid_r & ~tx_drain_i;
  assign m_axis_tx_tlast  = txp_last_r;

  // ======================================================================= //
  //  Side-port host bridge                                                  //
  // ======================================================================= //
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      hb_pend_r    <= 1'b0;
      hb_we_r      <= 1'b0;
      hb_addr_r    <= 20'd0;
      hb_wdata_r   <= 32'd0;
      host_rdata_o <= 32'd0;
      host_ack_o   <= 1'b0;
      host_err_o   <= 1'b0;
    end else begin
      host_ack_o <= 1'b0;
      if (!hb_pend_r) begin
        if (host_req_i) begin
          hb_pend_r  <= 1'b1;
          hb_we_r    <= host_we_i;
          hb_addr_r  <= host_addr_i;
          hb_wdata_r <= host_wdata_i;
        end
      end else if (pp_host_rvalid_w) begin
        hb_pend_r    <= 1'b0;
        host_rdata_o <= pp_host_rdata_w;
        host_err_o   <= pp_host_err_w;
        host_ack_o   <= 1'b1;
      end
    end
  end

  // ======================================================================= //
  //  Shadow counters — the only evidence that the processor is alive        //
  // ======================================================================= //
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      rx_frames_o <= 16'd0;
      rx_drops_o  <= 8'd0;
      tx_frames_o <= 16'd0;
    end else begin
      if (pp_rx_valid_w & pp_rx_last_w)      rx_frames_o <= rx_frames_o + 16'd1;
      if (drop_evt_w & (rx_drops_o != 8'hFF)) rx_drops_o <= rx_drops_o + 8'd1;
      //! count on the ACCEPTED final byte: the processor now sees real
      //! backpressure, so tx_valid alone no longer means the byte moved
      if (pp_tx_valid_w & pp_tx_ready_w & pp_tx_eof_w)
        tx_frames_o <= tx_frames_o + 16'd1;
    end
  end

endmodule

`default_nettype wire
