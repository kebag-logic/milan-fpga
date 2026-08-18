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
                v2.0) — the scenario-B P5 seam. SUBSTITUTION LANDED: this
                wrapper IS this device's IEEE 1722.1 / SRP control plane.

                WHAT THIS REPLACED, AND WHAT IT DID NOT. The repository's own
                ADP advertiser, ACMP talker/listener, AECP/AEM engine and
                lwSRP applicant are DELETED (USER, explicit and repeated:
                "remove the old code AECP/ACMP/ADP the lwSRP shall be removed
                as well. Only use the uCPU code" / "do not leave the option,
                remove everything out of the code base that is legacy"). There
                is no parameter, no fallback and no shadow arm: this module is
                instantiated unconditionally and its TX rides the control lane.

                THE AECP COMMAND SURFACE IS ACTIVE (2026-08-17,
                VERSION 0x004F). This banner said "answers NO AECP/AEM command
                at all" from 2026-08-12 until the micro-coded uCPU landed
                inside protocol_processor_top; that sentence is retired. The
                EXTERNAL AECP pop face this wrapper exposes is still tied
                ready = 0 (see the tie-off below) and that is CORRECT: the
                engine pops that queue INSIDE the processor now, so a second
                consumer here would steal its commands.

                What this entity answers today includes discovery and
                enumeration, solicited counters, selected stream, clock, and
                configuration operations, Identify control, the unsolicited
                registration pair, GET/ADD/REMOVE_AUDIO_MAPPINGS,
                GET_DYNAMIC_INFO, and MVU
                GET_MILAN_INFO. The AUTHORITY is
                protocol-processor/hdl/aecp/KL_aecp_engine.sv's OP_*_C
                constants, never this comment.

                WHAT IS STILL OPEN, and is a compliance gap rather than a
                design choice: SET_STREAM_FORMAT, SET_STREAM_INFO, name access,
                the incomplete unsolicited-notification
                trigger set, the departing-controller monitor and saved-state
                persistence. The current verdict is in
                docs/testing/MILAN_V12_AUDIT_2026-08-16.md. SET_CLOCK_SOURCE is accepted and
                stored by the processor, and this wrapper exports the selected
                value. The media plane does not consume it and therefore remains
                pinned at clock_source_index 0.

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
                That is the processor's documented no-saved-binding path. It
                is deliberately NOT persistent, and with KL_persist_journal
                deleted alongside the rest of the legacy plane NOTHING in this
                device now persists a binding across a power cycle: a restore
                walk always finds blank flash and completes with zero records.
                Milan v1.2 5.3.8.2 wants saved state; this build does not have
                it, and says so structurally rather than by a zeroed counter.

                AND IT MUST SAY SO IN THE STATUS. Until 0x0045 it did not.
                Every arm of the processor's per-record vendor default
                (07 §5.3 F07.9) ends the walk with restore_done and no
                restore_fail, so the responder above produced the SAME status
                word a real restore of eight bindings produces: a device with
                no media reported a completed restore. A report of saved state
                that was never saved is worse than reporting none, because a
                Milan 5.3.8.2/5.3.8.3 checklist passes on it and the failure
                only appears on a bench that cycles the power. So the wrapper
                publishes two more levels beside done/fail:

                  nvm_backed_o   CONSTANT. Derived from the responder below
                                 (NVM_BACKED_C), never a parameter: a port an
                                 integrator can set to 1 while the volatile
                                 stub is still instantiated is the same lie
                                 with a longer reach.
                  restore_blank_o  the walk validated zero records - blank or
                                 unframed media - as opposed to a walk that
                                 put bindings back.

                and restore_fail_o is RAISED on a completed walk with no
                backend. That last choice is deliberate: fail is the bit every
                existing decoder of this status already reads as "not
                successful", and landing in an encoding they understand beats
                inventing a code that only new software can see. Blank media
                behind a REAL backend is not a failure (nothing was ever
                saved, which Milan permits): it reports backed with blank.

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

                ADDRESS ALLOCATION. The processor contains KL_pp_maap, but
                this integration holds it dark through cfg_maap_internal_i=0
                and uses the per-source ALLOC/RELEASE face instead. This
                fabric's selected allocator is KL_maap, which claims one BLOCK.
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
    //! ---- AECP descriptor store (07 §3.3) ---------------------------------
    //! The uCPU microcode image, and the geometry of the entity-model image
    //! the store fetches from the integrator's main memory. DESC_BASE_P is a
    //! COMPILE-TIME base by design - the processor holds no base register, so
    //! there is nothing for software to get wrong at runtime - and the
    //! integrator overrides it to a region of ITS memory map that software
    //! reserves and loads. Passed straight through; this wrapper adds no
    //! policy.
    parameter string       UCODE_HEX_P         = "ucode.hex",
    parameter logic [31:0] DESC_BASE_P         = 32'h2000_0000,
    parameter int unsigned DESC_LINE_BYTES_P   = 576,
    parameter int unsigned DESC_IDX_ENTRIES_P  = 32,
    parameter int unsigned DESC_NAME_ENTRIES_P = 32,
    parameter int unsigned DESC_MEM_TMO_CYC_P  = 4096,
    //! ---- AECP response buffer, also in the integrator's main memory ------
    //! The response an AECP command builds (up to 16 + DESC_LINE_BYTES_P = 592
    //! bytes at the shipping geometry) is not fabric state either: held as
    //! flops it measured 5,079 FF / 3,495 LUT inside KL_aecp_engine and it was
    //! those flops the placer could not pack on a die whose 135 block-RAM tiles
    //! were 100% spoken for. Same rule as DESC_BASE_P - a COMPILE-TIME base,
    //! never a register - with ONE difference that the integrator owns: this
    //! region is WRITTEN by the processor, so it must be reserved for the
    //! processor ALONE and it must not overlap the descriptor image. Passed
    //! straight through; this wrapper adds no policy.
    parameter logic [31:0] RESP_BASE_P         = 32'h2010_0000,
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
    input  wire [15:0] current_cfg_i,      //! ADPDU current_configuration_index
    input  wire [15:0] identify_index_i,   //! ADPDU identify_control_index

    //! ---- per-source quasi-static provisioning (the TALKER HALF's oxygen) --
    //! Both of these were tied off in the shadow landing PRECISELY because a
    //! shadow must not act, and both are load-bearing now that this wrapper
    //! IS the control plane.
    //!
    //! cfg_src_en_i, bit s = "source s exists in this configuration". The
    //! processor's talker walk is gated on it: with the mask at 0 no source
    //! ever allocates a DA, acmp_declaring_o is stuck 0 and NOTHING
    //! transmits. It is a PORT and not a parameter because the number it
    //! encodes belongs to the ENTITY MODEL - milan_datapath drives it from
    //! the generated shape header (ADP_TALKER_SRC_C), so the count a
    //! controller is told at 0x618 and the count of sources that can answer
    //! are one constant, derived and never mirrored.
    input  wire [N_STREAM_OUT_P-1:0]    cfg_src_en_i,
    //! per-source stream_id, flat [64*s +: 64] - the SAME packing the class-D
    //! outputs use. This is what the processor's SRP DECLARE_TALKER puts in
    //! its StreamID and what its ACMP answers a controller; tied '0 it would
    //! declare and answer stream_id 0 for every source. The {station MAC,
    //! talker_unique_id} law is the fabric's (KL_aaf_packetizer stamps the
    //! same 64 bits onto the wire), so the integrator computes it once and
    //! hands it here rather than this wrapper inventing a second copy.
    input  wire [N_STREAM_OUT_P*64-1:0] cfg_stream_id_i,
    //! TSpec MaxFrameSize for the engine-driven DECLARE_TALKER (802.1Q
    //! 35.2.2.4). Milan v1.2 4.3.3.2 Table 4.4 makes it a FUNCTION of the
    //! channel count (24*C + 24 + 1), which the integrator already derives
    //! for the framer - so it arrives here rather than being re-derived. It
    //! was tied 16'd0 in shadow mode, where a declaration nobody sends can
    //! carry any number; on the wire a zero MaxFrameSize is a reservation for
    //! zero bandwidth, which a bridge grants and a stream then overruns.
    input  wire [15:0]                  cfg_tspec_max_frame_i,
    //! initial accumulated_latency for the Listener direction (802.1Q
    //! 35.2.2.8.4). Same story: tied 0 in shadow mode.
    input  wire [31:0]                  cfg_acc_lat_ns_i,
    //! port rate for the SRP admission ceiling (75% of it, 802.1Q 34.3.1)
    input  wire [31:0]                  port_rate_bps_i,

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

    //! ---- GET_COUNTERS read face (1722.1-2021 7.4.42, Milan v1.2 5.4.2.25) ----
    //! Straight through to protocol_processor_top, names and directions
    //! unchanged. The processor parses the command and lays out Table 7-157's
    //! 32-quadlet block; THIS WRAPPER OWNS NOTHING about what the numbers
    //! mean, because the events Milan Table 5.6 counts happen in the
    //! integrator's stream datapath (milan_datapath drives it from
    //! KL_avtp_rx_monitor_ctx's diag_cnt_o).
    //!
    //! `ctr_wait_i` is a HOLD, not a ready: 0 means "the answer is on
    //! ctr_data_i now". The submodule banner offers an unwired face as the
    //! safe state, and in isolation that is true - it answers 0 with an empty
    //! mask. It is NOT available here: this tree's pp_shadow harness is
    //! warnings-are-errors (USER 2026-08-12), so six unconnected ports are six
    //! fatal PINMISSING and the unconnected state does not compile. Wiring is
    //! mandatory, not optional.
    output logic        ctr_req_o,          //! a quadlet is being asked for
    output logic [15:0] ctr_desc_type_o,    //! AECPDU @24
    output logic [15:0] ctr_desc_index_o,   //! AECPDU @26
    output logic  [5:0] ctr_word_o,         //! 0..31 = block quadlet, 32 = mask
    input  wire  [31:0] ctr_data_i,         //! that quadlet, 1722.1 value order
    input  wire         ctr_wait_i,         //! HOLD the beat (not a ready)

    //! ---- GET_AUDIO_MAP read face (1722.1-2021 7.4.44, Milan v1.2 5.4.2.26) ----
    //! Straight through to protocol_processor_top, names and directions
    //! unchanged - the counters bargain again. The processor parses the
    //! command, enforces the 7.4.44.1 page rule and lays out the response;
    //! THIS WRAPPER OWNS NOTHING about the mappings, because they live in
    //! the integrator's routing fabric (milan_datapath answers from the
    //! render crossbar's map RAM, the same flops CHMAP_LOOP 0x914 reads).
    //! Same warnings-are-errors rule as the counters face: wiring is
    //! mandatory, not optional - an unconnected pin is a fatal PINMISSING
    //! in this tree's pp_shadow harness.
    output logic        amap_req_o,         //! a word is being asked for
    output logic [15:0] amap_desc_type_o,   //! AECPDU @24 (STREAM_PORT_INPUT or _OUTPUT)
    output logic [15:0] amap_desc_index_o,  //! AECPDU @26
    output logic [15:0] amap_map_index_o,   //! AECPDU @28 - the page
    output logic  [1:0] amap_sel_o,         //! 0 NMAPS, 1 GEOM, 2 RECORD
    output logic  [7:0] amap_rec_o,         //! record ordinal within the page
    input  wire  [63:0] amap_data_i,        //! the word (upper 32 zero unless RECORD)
    input  wire         amap_wait_i,        //! HOLD the beat (not a ready)

    //! ---- ADD/REMOVE_AUDIO_MAPPINGS transaction face --------------------
    //! Straight through to protocol_processor_top. The integrator validates
    //! the full staged command before accepting any phase-5 write.
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

    //! ---- Milan-info gather face (06 SS6.2/SS6.10) ----
    //! Straight through to protocol_processor_top: GET_STREAM_INFO /
    //! GET_AVB_INFO / GET_AS_PATH ask one word at a time and milan_datapath
    //! answers from its binding view, SRP registrars and gPTP plane - the
    //! same warnings-are-errors rule as the other faces, wiring mandatory.
    output logic        gsi_req_o,          //! a word is being asked for
    output logic [1:0]  gsi_kind_o,         //! 0 STRI / 1 AVB / 2 ASP
    output logic [15:0] gsi_desc_type_o,    //! addressed descriptor_type
    output logic [15:0] gsi_desc_index_o,   //! addressed descriptor_index
    output logic  [3:0] gsi_sel_o,          //! word selector within the kind
    output logic  [7:0] gsi_ord_o,          //! array ordinal (ASP path, AVB maps)
    input  wire  [63:0] gsi_data_i,         //! the word
    input  wire         gsi_wait_i,         //! HOLD the beat (not a ready)
    input  wire         gsi_avb_chg_i,      //! integrator-side AVB-info word changed

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
    //! owns; its per-protocol arbitration is internal. That stream carries
    //! ADP + ACMP + SRP — the AECP lanes are idle until P4 — and it rides
    //! the control cascade as the ONE control leg beside MAAP.
    output logic [TDATA_WIDTH_P-1:0]   m_axis_tx_tdata,  //! little lane order
    output logic [TDATA_WIDTH_P/8-1:0] m_axis_tx_tkeep,  //! contiguous from lane 0
    output logic                       m_axis_tx_tvalid,
    output logic                       m_axis_tx_tlast,
    input  wire                        m_axis_tx_tready,
    //! 1 = discard the processor's frames and count them; 0 = the packed
    //! AXIS port above is the real egress. milan_datapath drives it 0 — the
    //! drain survives only as the harness lever that lets a testbench count
    //! the processor's frames without standing up a MAC.
    input  wire                        tx_drain_i,

    //! ---- descriptor-image memory master (07 §3.3, READ-ONLY) ------------
    //! Straight through to protocol_processor_top, names and directions
    //! unchanged. THE INTEGRATOR OWNS THE BRIDGE: this repository's SoC wires
    //! it to LiteX main memory (sw/litex/milan_soc.py), because on this board
    //! the entity model lives in DDR3. Tying req_ready_i to 0 is legal and
    //! documented - the store's watchdog abandons the burst and every
    //! READ_DESCRIPTOR degrades to NO_SUCH_DESCRIPTOR rather than hanging -
    //! but it must be a DELIBERATE tie with a banner, never an oversight.
    output logic                       desc_mem_req_valid_o,
    input  wire                        desc_mem_req_ready_i,
    output logic [31:0]                desc_mem_req_addr_o,
    output logic [8:0]                 desc_mem_req_beats_o,
    input  wire                        desc_mem_rsp_valid_i,
    output logic                       desc_mem_rsp_ready_o,
    input  wire  [63:0]                desc_mem_rsp_data_i,
    input  wire                        desc_mem_rsp_last_i,
    input  wire                        desc_mem_rsp_err_i,

    //! ---- AECP response-buffer memory master (03 §7, READ + WRITE) -------
    //! A SECOND, INDEPENDENT main-memory master, straight through to
    //! protocol_processor_top with names and directions unchanged. It is not
    //! the descriptor face and it may not share one: both are watchdog-bounded
    //! clients with one outstanding transaction each, and merging them would
    //! mean an arbiter whose grant has to be released correctly on every
    //! timeout arm of BOTH. The integrator's memory system already arbitrates.
    //!
    //! THREE THINGS DIFFER FROM desc_mem_* ABOVE, and all three are the
    //! bridge's obligation (protocol_processor_top's banner is the contract):
    //!   * resp_mem_rsp_ready_o is REAL BACKPRESSURE - it is NOT tied 1 the way
    //!     the descriptor face's is, because the buffer takes a beat only once
    //!     the frame builder has spent the previous one. A bridge SHALL hold a
    //!     beat until it is taken.
    //!   * the WRITE channel is ONE outstanding SINGLE-BEAT write, 8-byte
    //!     aligned, big-endian lane (byte addr+n is wr_data[63-8n -: 8]),
    //!     wr_strb bit n enabling byte n - and a byte whose strobe is 0 SHALL
    //!     NOT be modified. wr_done_i is a ONE-CYCLE COMMIT PULSE, same cycle
    //!     as wr_ready_i for a posted bridge or any later cycle for an
    //!     acknowledged one; no further write is issued until it arrives.
    //!   * ORDERING: a read request accepted after a write reported done SHALL
    //!     observe that write.
    //! Tying req_ready_i and wr_ready_i to 0 is legal and documented - the
    //! buffer's watchdog voids the response and KL_aecp_engine answers a
    //! well-formed ENTITY_MISBEHAVING rather than hanging - but, exactly as for
    //! the descriptor face, it must be a DELIBERATE tie with a banner and never
    //! an oversight. This repository's SoC bridges it to LiteX main memory
    //! (sw/litex/milan_soc.py).
    output logic                       resp_mem_req_valid_o,
    input  wire                        resp_mem_req_ready_i,
    output logic [31:0]                resp_mem_req_addr_o,
    output logic [8:0]                 resp_mem_req_beats_o,
    input  wire                        resp_mem_rsp_valid_i,
    output logic                       resp_mem_rsp_ready_o,
    input  wire  [63:0]                resp_mem_rsp_data_i,
    input  wire                        resp_mem_rsp_last_i,
    input  wire                        resp_mem_rsp_err_i,
    output logic                       resp_mem_wr_valid_o,
    input  wire                        resp_mem_wr_ready_i,
    output logic [31:0]                resp_mem_wr_addr_o,
    output logic [63:0]                resp_mem_wr_data_o,
    output logic [7:0]                 resp_mem_wr_strb_o,
    input  wire                        resp_mem_wr_done_i,
    input  wire                        resp_mem_wr_err_i,

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

    //! ---- the INTERNAL Annex B option (processor 11; quasi-static) ------
    //! The processor now carries its own MAAP engine (KL_pp_maap). With
    //! cfg_maap_internal_i = 0 (this fabric's shipping value) the engine is
    //! dark, the per-source face above stays the seam, and behaviour is
    //! byte-identical to the pre-engine top. 1 answers the talker from the
    //! processor's own Annex B claim and quiesces the external port group -
    //! the KL_maap-retirement option, taken only when the fabric's own
    //! allocator is REMOVED in the same build (two Annex B engines defending
    //! one wire is a protocol violation, not a redundancy).
    input  wire                        cfg_maap_internal_i,    //! 1 = internal allocator
    input  wire  [7:0]                 cfg_maap_count_i,       //! block size to claim
    input  wire  [15:0]                cfg_maap_seed_offset_i, //! preferred pool offset
    input  wire                        cfg_maap_seed_valid_i,  //! 1 = first walk probes the seed
    //! the internal claim, republished (KL_maap-compatible naming; all-zero
    //! while the internal engine is dark)
    output logic [47:0]                maap_addr_o,        //! claimed base DMAC (source 0)
    output logic                       maap_addr_valid_o,  //! 1 = Annex B DEFEND (claim held)
    output logic [1:0]                 maap_state_o,       //! 0 INITIAL / 1 PROBE / 2 DEFEND
    output logic [7:0]                 maap_conflicts_o,   //! re-address events (saturating)
    output logic [7:0]                 maap_defends_o,     //! DEFEND frames sent (saturating)

    //! ---- the AECP SETTINGS face (Milan §5.3.x) ------------------------
    //! NOT the whole dynamic store. It holds eight fields and exposes five.
    //! Absent because KL_aecp_dyn_state has no corresponding output:
    //! current_sampling_rate, which AECP serves, and both current_format
    //! fields, which no microprogram reads or writes yet. What IS below is
    //! republished 1:1 so the fabric can act on a
    //! setting rather than be told about it. Every one reads its reset
    //! default until a controller writes it, so a datapath that leaves these
    //! unread behaves exactly as it did before the store existed — which is
    //! how they land here ahead of their consumers.
    output logic [15:0]                aecp_cur_config_o,   //! ENTITY.current_configuration
    output logic  [7:0]                aecp_identify_o,     //! IDENTIFY, 0 or 255
    output logic [15:0]                aecp_clk_src_index_o,//! CLOCK_DOMAIN[0] clock source
    //! Per sink, 1 = started (Milan §5.3.8.7). LIVE since issue #78 and
    //! LOAD-BEARING: `milan_datapath` gates the listener accept pulse on it,
    //! so a bound sink reading 0 here receives, matches and counts its
    //! AVTPDUs and hands the media path nothing. Its source is the ACMP
    //! BINDING RECORD, not the AECP dynamic-state store - the store's
    //! selector 6 is retired, because the state is a property of the binding
    //! ("undefined when the Stream Input is not bound") and only the record
    //! has that lifecycle. The port name's `aecp_` prefix is historical: the
    //! AECP commands MOVE the bit, the record OWNS it.
    output logic [N_STREAM_IN_P-1:0]   aecp_strm_started_o,
    output logic [31:0]                aecp_pt_offset_o,    //! presentation-time offset
    output logic                       aecp_dyn_dirty_o,    //! a persisted field moved
    output logic                       aecp_lock_held_o,    //! LOCK_ENTITY ownership is live

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
    output logic       restore_done_o,     //! restore sequencing complete (NOT a verdict)
    output logic       restore_fail_o,     //! the completed restore did NOT restore: torn read-back, or no backend at all
    output logic       nvm_backed_o,       //! CONSTANT: 1 = persistent media behind the device face, 0 = none in this build
    output logic       restore_blank_o,    //! the completed walk validated ZERO records
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
  //! The responder below IS this build's whole backend and it holds nothing
  //! across a reset, let alone a power cycle. This constant sits here, beside
  //! it, so the two move together: whoever replaces the responder with real
  //! media edits the line under their cursor. It is deliberately NOT a module
  //! parameter — the fact is a property of the logic in this file, and a
  //! parameter would let an integrator assert persistence the fabric does not
  //! have.
  localparam logic NVM_BACKED_C = 1'b0;

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
  logic        pp_restore_done_w, pp_restore_fail_w, pp_restore_blank_w;

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
      .TROM_HEX_P     (TROM_HEX_P),
      .UCODE_HEX_P         (UCODE_HEX_P),
      .DESC_BASE_P         (DESC_BASE_P),
      .DESC_LINE_BYTES_P   (DESC_LINE_BYTES_P),
      .DESC_IDX_ENTRIES_P  (DESC_IDX_ENTRIES_P),
      .DESC_NAME_ENTRIES_P (DESC_NAME_ENTRIES_P),
      .DESC_MEM_TMO_CYC_P  (DESC_MEM_TMO_CYC_P),
      .RESP_BASE_P         (RESP_BASE_P)
  ) u_pp (
      .clk_i               (clk_i),
      .rst_n               (rst_n),

      .aecp_cur_config_o   (aecp_cur_config_o),
      .aecp_identify_o     (aecp_identify_o),
      .aecp_clk_src_index_o(aecp_clk_src_index_o),
      .aecp_strm_started_o (aecp_strm_started_o),
      .aecp_pt_offset_o    (aecp_pt_offset_o),
      .aecp_dyn_dirty_o    (aecp_dyn_dirty_o),
      .aecp_lock_held_o    (aecp_lock_held_o),

      .entity_id_i         (entity_id_i),
      .entity_model_id_i   (entity_model_id_i),
      .own_mac_i           (station_mac_i),
      .talker_sources_i    (talker_sources_i),
      .talker_caps_i       (talker_caps_i),
      .listener_sinks_i    (listener_sinks_i),
      .listener_caps_i     (listener_caps_i),
      .current_cfg_i       (current_cfg_i),
      .identify_index_i    (identify_index_i),

      .entity_enable_i     (enable_i),
      .link_up_i           (link_up_i),
      .gm_change_i         (gm_change_i),
      .gm_id_i             (gm_id_i),
      .gptp_domain_i       (gptp_domain_i),

      //! SRP quasi-static. Milan mandates point-to-point.
      //!
      //! RANK IS 1, NOT 0. 802.1Q Table 35-6: the Rank bit of PriorityAndRank
      //! is 0 = EMERGENCY, 1 = non-emergency, and this device's declarations
      //! have always carried the non-emergency rank (the deleted lwsrp_pkg
      //! pinned PriorityAndRank at 0x70 = priority 3, rank 1). The 1'b0 here
      //! was a shadow-mode don't-care - a drained declaration can say
      //! anything - and would have put an emergency-rank Talker Advertise on
      //! the wire the moment the drain came off.
      .p2p_i               (1'b1),
      .cfg_rank_i          (1'b1),
      .cfg_acc_lat_ns_i    (cfg_acc_lat_ns_i),
      .port_rate_bps_i     (port_rate_bps_i),
      .cfg_tspec_max_frame_i(cfg_tspec_max_frame_i),

      //! Which talker sources exist — straight from the port, which the
      //! integrator derives from the entity shape (see the port's banner).
      .cfg_src_en_i        (cfg_src_en_i),
      //! ONE AVB interface on this board, so every source sits on interface
      //! 0. This is not a placeholder: KL_acmp_talker SILENTLY IGNORES a
      //! PROBE_TX whose interface_index disagrees with the source's, and the
      //! processor's own rx_if_index is 0, so any other value here would make
      //! the talker deaf with no counter moving anywhere.
      .cfg_src_iface_i     ('0),
      //! the per-source stream_id the SRP DECLARE_TALKER and the ACMP talker
      //! answer with — the fabric's {station MAC, uid} law, computed once by
      //! the integrator and passed straight through (see the port's banner).
      .cfg_stream_id_i     (cfg_stream_id_i),

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

      //! Dynamic state is served by AECP but is not consumed by this wrapper
      //! yet. Name every output explicitly so integration lint cannot mistake
      //! the deliberate boundary for an accidentally omitted connection.

      .ctr_req_o           (ctr_req_o),
      .ctr_desc_type_o     (ctr_desc_type_o),
      .ctr_desc_index_o    (ctr_desc_index_o),
      .ctr_word_o          (ctr_word_o),
      .ctr_data_i          (ctr_data_i),
      .ctr_wait_i          (ctr_wait_i),

      .amap_req_o          (amap_req_o),
      .amap_desc_type_o    (amap_desc_type_o),
      .amap_desc_index_o   (amap_desc_index_o),
      .amap_map_index_o    (amap_map_index_o),
      .amap_sel_o          (amap_sel_o),
      .amap_rec_o          (amap_rec_o),
      .amap_data_i         (amap_data_i),
      .amap_wait_i         (amap_wait_i),
      .amap_edit_req_o     (amap_edit_req_o),
      .amap_edit_phase_o   (amap_edit_phase_o),
      .amap_edit_remove_o  (amap_edit_remove_o),
      .amap_edit_desc_type_o(amap_edit_desc_type_o),
      .amap_edit_desc_index_o(amap_edit_desc_index_o),
      .amap_edit_count_o   (amap_edit_count_o),
      .amap_edit_rec_o     (amap_edit_rec_o),
      .amap_edit_record_o  (amap_edit_record_o),
      .amap_edit_value_o   (amap_edit_value_o),
      .amap_edit_data_i    (amap_edit_data_i),
      .amap_edit_wait_i    (amap_edit_wait_i),
      .gsi_req_o           (gsi_req_o),
      .gsi_kind_o          (gsi_kind_o),
      .gsi_desc_type_o     (gsi_desc_type_o),
      .gsi_desc_index_o    (gsi_desc_index_o),
      .gsi_sel_o           (gsi_sel_o),
      .gsi_ord_o           (gsi_ord_o),
      .gsi_data_i          (gsi_data_i),
      .gsi_wait_i          (gsi_wait_i),
      .gsi_avb_chg_i       (gsi_avb_chg_i),

      .restore_go_i        (restore_go_i),
      .restore_busy_o      (restore_busy_o),
      .restore_done_o      (pp_restore_done_w),
      .restore_fail_o      (pp_restore_fail_w),
      .restore_blank_o     (pp_restore_blank_w),
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

      //! CONFIG-PLANE SEAM, UNUSED. The processor's svc_* face is how a
      //! host would inject a binding or a reservation directly; nothing in
      //! this fabric drives it. Bindings arrive over the wire (ACMP) and
      //! reservations follow them, which is the ATDECC-authoritative shape
      //! this device is built to. Tied off, not forgotten.
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
      //! descriptor-image master: straight through to the integrator
      .desc_mem_req_valid_o (desc_mem_req_valid_o),
      .desc_mem_req_ready_i (desc_mem_req_ready_i),
      .desc_mem_req_addr_o  (desc_mem_req_addr_o),
      .desc_mem_req_beats_o (desc_mem_req_beats_o),
      .desc_mem_rsp_valid_i (desc_mem_rsp_valid_i),
      .desc_mem_rsp_ready_o (desc_mem_rsp_ready_o),
      .desc_mem_rsp_data_i  (desc_mem_rsp_data_i),
      .desc_mem_rsp_last_i  (desc_mem_rsp_last_i),
      .desc_mem_rsp_err_i   (desc_mem_rsp_err_i),

      //! response-buffer master: straight through as well, read AND write
      .resp_mem_req_valid_o (resp_mem_req_valid_o),
      .resp_mem_req_ready_i (resp_mem_req_ready_i),
      .resp_mem_req_addr_o  (resp_mem_req_addr_o),
      .resp_mem_req_beats_o (resp_mem_req_beats_o),
      .resp_mem_rsp_valid_i (resp_mem_rsp_valid_i),
      .resp_mem_rsp_ready_o (resp_mem_rsp_ready_o),
      .resp_mem_rsp_data_i  (resp_mem_rsp_data_i),
      .resp_mem_rsp_last_i  (resp_mem_rsp_last_i),
      .resp_mem_rsp_err_i   (resp_mem_rsp_err_i),
      .resp_mem_wr_valid_o  (resp_mem_wr_valid_o),
      .resp_mem_wr_ready_i  (resp_mem_wr_ready_i),
      .resp_mem_wr_addr_o   (resp_mem_wr_addr_o),
      .resp_mem_wr_data_o   (resp_mem_wr_data_o),
      .resp_mem_wr_strb_o   (resp_mem_wr_strb_o),
      .resp_mem_wr_done_i   (resp_mem_wr_done_i),
      .resp_mem_wr_err_i    (resp_mem_wr_err_i),

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

      .cfg_maap_internal_i     (cfg_maap_internal_i),
      .cfg_maap_count_i        (cfg_maap_count_i),
      .cfg_maap_seed_offset_i  (cfg_maap_seed_offset_i),
      .cfg_maap_seed_valid_i   (cfg_maap_seed_valid_i),
      .maap_addr_o             (maap_addr_o),
      .maap_addr_valid_o       (maap_addr_valid_o),
      .maap_state_o            (maap_state_o),
      .maap_conflicts_o        (maap_conflicts_o),
      .maap_defends_o          (maap_defends_o),

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
  //! untested until the day it first mattered. milan_datapath drives
  //! tx_drain_i = 0 - the drain is a harness lever now, not a mode.
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

  //! tvalid is held low while draining, so a harness that drains cannot put a
  //! frame on the wire by accident: the drain is structural, not a
  //! convention. milan_datapath does not drain.
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

  // ======================================================================= //
  //  Saved-state verdict (Milan v1.2 5.3.8.2/5.3.8.3/5.3.8.7)              //
  // ======================================================================= //
  //! done stays the SEQUENCING level the processor publishes: the walk ran to
  //! the end. Everything below is what the walk is allowed to CLAIM.
  assign restore_done_o  = pp_restore_done_w;
  assign nvm_backed_o    = NVM_BACKED_C;
  assign restore_blank_o = pp_restore_blank_w;

  //! A completed walk with no backend is a FAILED restore, not a successful
  //! one: the bound state Milan 5.3.8.2 requires to survive a power cycle was
  //! not restored and could not have been. Raising the processor's own fail
  //! level is what puts it in the encoding existing readers of this status
  //! already treat as unsuccessful. It is gated on done so the verdict is a
  //! verdict: before a restore has run there is nothing to have failed.
  assign restore_fail_o  = pp_restore_fail_w
                         || (pp_restore_done_w && !NVM_BACKED_C);

endmodule

`default_nettype wire
