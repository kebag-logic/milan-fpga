/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : milan_csr.sv
  Author      : Kebag Logic

  Date        : 2026-07-01
  Description : AXI4-Lite control/status-register (CSR) block for the Milan TSN
                network interface. This is the memory-mapped control plane
                (REQUIREMENTS.md REQ-CSR-*) that the Linux driver binds to; it
                turns the previously compile-time-only TSN knobs (MAC config,
                802.1Q classifier map, 802.1Qav CBS slopes, PTP clock control)
                into runtime-writable registers, and exposes MAC statistics,
                link status and interrupts back to software.

                THE LEGACY 1722.1 / SRP GROUPS ARE INERT SINCE 2026-08-13.
                The RTL that consumed them - this repository's own ADP
                advertiser, AECP/AEM engine, ACMP talker and listener, and
                lwSRP applicant - is DELETED; the protocol-processor submodule
                is the control plane, reached through the 0x920 window. THE
                REGISTERS STAY, because the register map is an ABI and every
                board script writes it, but what they do changed and the
                change is not uniform. Three kinds, all recorded per word in
                docs/reference/REGISTER_MAP.md:

                  * STRUCTURAL ZERO - the status word's source is gone, so it
                    reads 0 and a reader must not mistake that for "idle":
                    the A_ADP_DIAG counters and advertiser state, every AECP
                    status word (lock, config, cmd/resp counts, BDBG 0x768,
                    AEMP 0x7C8 status), the ACMP listener's state-machine
                    fields and ACMPL_DBG, the ACMP cmd/resp counts, the lwSRP
                    MRPDU counters, the journal status/sequence (0x7B8), and
                    both 0x800-window context-table ports.
                  * ACCEPTED AND DISCARDED - the write lands nowhere and
                    nothing observable changes: the AEM patch port, AS_PATH
                    staging, the 0x7A0 bind-restore master, the journal
                    ingest, the lwSRP row-provisioning words, and the five
                    ADPDU fields the processor holds as internal constants
                    (entity_capabilities, valid_time, association_id,
                    controller_capabilities, interface_index).
                  * STILL LIVE, REPOINTED - available_index, ACMP talker
                    active and the listener BOUND record, the SRP Domain
                    pair, granted slope and over-limit bit: all republished
                    from the processor's class-D face.

                The full register map / ABI is documented in
                docs/reference/REGISTER_MAP.md and mirrored by the self-checking harness
                in tb/verilator/csr. Register groups:

                  0x000  ID / VERSION / CAPABILITIES / IRQ
                  0x100  MAC control + status
                  0x200  Statistics (RMON) snapshot window
                  0x300  802.1Q classifier (PCP->TC map, default priority)
                  0x400  802.1Qav CBS, per queue (stride 0x20)
                  0x500  PTP hardware clock (adjfine/adjtime/settime/gettime)

                Design notes:
                  * AXI4-Lite slave uses the combinational-ready, single-
                    outstanding pattern: a transfer commits on the same rising
                    edge that *READY is asserted, so a master that drops *VALID
                    right after the handshake still commits (no lost writes).
                  * Configuration values leave on flat o_* output ports for the
                    rest of milan_top to consume. Status (link, RMON counters,
                    PTP TOD) and event pulses arrive on i_* input ports.
                  * Command strobes (PTP settime/adjtime/snapshot, stats
                    snapshot/reset) are emitted as single-cycle o_*_cmd_* /
                    o_stats_* pulses. Fields consumed in the gtx_clk (PTP/TX)
                    domain must be CDC-synchronised at the consumer using these
                    apply strobes (REQ-CSR-03); this block is purely in the
                    aclk (AXI) domain.
                  * s_axi_wstrb is intentionally ignored: the ABI mandates full
                    32-bit register writes.

  Company     : Kebag Logic
  Project     : Milan FPGA Platform
------------------------------------------------------------------------------
*/

`default_nettype none

module milan_csr #(
  parameter int NUM_QUEUES  = 5,             //! Number of HW traffic-class queues (reported in CAP.num_queues); q4 = highest priority
  parameter int ADDR_WIDTH  = 16,            //! Byte-address width of the AXI-Lite window (16 => 64 KB)
  parameter int N_LISTENERS_P = 1,           //! listener stream contexts addressable by the 0x800 window (A_STRM_SEL dir=0); idx >= N reads 0 / writes ignored
  parameter int N_TALKERS_P   = 1,           //! talker stream contexts (A_STRM_SEL dir=1)
  parameter int unsigned SRP_LSN0_ROW_P = 0, //! dedicated listener-0 lwSRP ctx row (0 = feature absent: the legacy row-0 alias is all sink 0 has)
  //! chmap map-RAM READBACK capability, declared by the INSTANTIATOR because
  //! only the integration knows whether the RAM's read port is actually
  //! wired: [0] = render (RMAP, KL_chan_map_render) readback connected,
  //! [1] = capture (CMAP, KL_chan_map_capture) readback connected AND
  //! carrying the {loop_fed, loop_mapped} loopback mask. DEFAULT 0 = ABSENT,
  //! which is the honest default: an instantiation that does not connect
  //! o_chmap_rd_*/i_chmap_rd_* must not be able to report a map word. The
  //! value is published in CHMAP_SNAP[9:8] so software reads UNSUPPORTED
  //! instead of a structural zero (methodology R5; the STATS_CAP 0x204 rule).
  parameter int unsigned CHMAP_RDBK_P = 0,
  //! PHC clock frequency of the domain ptp_ts_top's counter ticks in.
  //! Sets the PTP_INCR RESET value = the true clock period in Q8.24 ns
  //! (derive, never mirror: the historic hardcoded 8.0 ns was the
  //! RGMII-era 125 MHz assumption and made every other domain's free-run
  //! PHC scale-wrong until software wrote PTP_INCR - the t532 wire-scale
  //! audit's in-tree find). The default keeps the standalone contract
  //! (125 MHz -> 0x08000000); milan_datapath overrides with its own
  //! MILAN_CLK_FREQ_HZ so the two can never disagree.
  parameter int unsigned MILAN_CLK_FREQ_HZ_P = 125_000_000,
  parameter logic [31:0] VERSION = 32'h0002_0053
  //! 0x0053 = GENERATED NAMES ARE LIVE AND COHERENT. SET_NAME and GET_NAME
  //! serve every semantic name in the generated AEM model. ENTITY supports
  //! indices 0 and 1, while every other named descriptor supports index 0.
  //! Responses use the full fixed cdl 84 body on success and refusal, a locked
  //! SET returns the current name, and SET, GET, and READ_DESCRIPTOR observe
  //! one writable overlay. Generated shape data sizes the table and the store
  //! loads large tables in bounded bursts. Persistence remains issue 70;
  //! unsolicited delivery remains issue 69, with change triggers exported.
  //! NO new CSRs.
  //! 0x0052 = START/STOP COMPLETES AT THE RECORD, AND A STOPPED CRF SINK
  //! OBSERVES. START_STREAMING and STOP_STREAMING report success only after
  //! the binding-record commit or a confirmed no-op. A stopped, bound CRF
  //! sink keeps matching, validating, and counting traffic while media-clock
  //! consumption, lock progress, and restart signaling remain gated. The
  //! ACMP response validator also selects the unique_id of the consuming
  //! engine, which fixes listener responses whose talker and listener ids
  //! differ. NO new CSRs. Prior release record follows.
  //! Value returned by the read-only VERSION register ([31:16] major, [15:0] minor; the ENTITY firmware_version renders major.minor.rev). VERSIONING POLICY (USER 2026-08-11): MAJOR = entire redesign of blocks; MINOR = compliance fixes - FLAT and continuous across majors, because the register-map changelog and every >= feature gate key on it; REV (patch, entity.firmware_rev in the config) = bug-fix respins that change no CSR ABI. 0x0002 MAJOR = THE SCENARIO-B ERA OPENS: the protocol-processor architecture of record (v2.0, the protocol-processor submodule) replaces this 1722.1/SRP plane by direct substitution at parity; the minor carries on unbroken. 0x0051 = GET_DYNAMIC_INFO BATCHES FIXED GETTERS. The complete record list is validated before execution, each record reports an independent status, legal unsupported getters copy their command data, oversized responses are omitted without stopping later records, and Milan GET_STREAM_INFO records carry the required 56-byte command data. NO new CSRs. Prior: 0x0050 = AUDIO MAPPING EDITS ARE ATOMIC. ADD_AUDIO_MAPPINGS and REMOVE_AUDIO_MAPPINGS now stage and validate the complete variable-length command before any routing state changes. Input geometry, output source ownership, current stream-channel bounds, static-map scope, lock ownership, running-state restrictions, idempotent ADD, duplicate REMOVE, exact notification bodies and NVM dirty signaling are enforced. Generated topology tables keep the AEM model, protocol readback and live map projections in one coordinate system. NO new CSRs. Prior: 0x004F = STARTED/STOPPED HAS ONE SOURCE OF TRUTH, AND THE DATAPATH READS IT. Milan v1.2 SS5.3.8.7 puts two shalls on a Stream Input - a started one "shall process the incoming stream data", a stopped one "shall DISCARD the Stream AVTPDUs it receives" - and NEITHER was implemented: `aecp_strm_started_o` reached `milan_datapath` and was read by nothing, while the bit behind it lived in a dynamic-store row that had a writer and no lifecycle. The state is a property of the BINDING (the clause calls it "undefined when the Stream Input is not bound"), so it now lives in the ACMP binding record and nowhere else - cleared on unbind, captured by the NVM shadow, restored through the boot preload - PLUMBING, not the shall: `KL_pp_shadow` sets `NVM_BACKED_C = 1'b0` behind a blank-flash stub, so Section 5.3.8.7's third sentence ("saved in a non-volatile memory and restored after a power cycle") is NOT met on any shipping build. Two of the clause's three shalls land here; the persistence one waits on issue 70 - and the dynamic store's selector 6 is RETIRED rather than reused, so a second writable copy cannot return by accident. START_STREAMING (0x0022) and STOP_STREAMING (0x0023) are served for the first time (SS5.4.2.19/.20): a Stream Output, and every other descriptor type, answers NOT_SUPPORTED as the clause requires, a nonexistent index answers NO_SUCH_DESCRIPTOR through the ordinary locate, a different controller under lock answers ENTITY_LOCKED, and every arm - success and refusal alike - carries IEEE Figure 7-59's four bytes at cdl 16, because only NOT_IMPLEMENTED may answer at the command's own size. They reach the record through a WRITE-ONLY microISA state-port region (0x3) that stores nothing and hands the engine backpressure, so a request issued while the ACMP walker is busy is delayed rather than dropped. The holder is ONE DEEP: the wait is deferred, not bounded, and a second request arriving before the first drains still waits - a dropped one would be a false SUCCESS, the command having already settled its status. The bind is what DEFINES the state: a BIND_RX carrying STREAMING_WAIT lands stopped and one without it lands started, which is IEEE SS7.4.35's own premise (START_STREAMING exists for a stream "connected via ACMP with the STREAMING_WAIT flag set") and is what Milan Table 5.9 bit 28 reports back - 1 only for a sink that is "bound and stopped". WIRE-FACING on every board: a stopped Stream Input still RECEIVES, still matches and still counts - Table 5.6 defines FRAMES_RX and its neighbours on frames "received on this Stream Input", and the clause's own verb is discard, not ignore - while the listener ACCEPT pulse that feeds the depacketizer is gated, so the media path gets nothing. The discard is deliberately NOT at the classification table: that forges a not-bound->bound edge on the next START, and Table 5.6 makes that edge the counter RESET event, so a stop/start pair would wipe all ten counters on a sink that never unbound. And GET_STREAM_INFO's STREAMING_WAIT flag stops being a hardcoded 0 justified as "bound = started" - true only while stopped was unreachable - and reads the same bit the admission gate does, so the answer and the behaviour cannot disagree. The CRF Media Clock Input is covered too: it has no classification-table entry (`KL_crf_rx` keys on subtype), so it carries the stopped predicate on its own frame strobe, guarded on the sink existing so a shape with `crf_sink: false` cannot alias it onto AAF sink 0. Stopping that descriptor therefore unlocks the media clock after KL_crf_rx's silence timeout, which is what the clause asks for and is worth knowing before a controller sends it. COVERAGE, stated: the direction that matters for every shipping build - that the gate does NOT fire in normal operation - is held by 20+ milan_dp checks that go red if the predicate is forced true. The stop direction is NOT yet exercised: no suite binds and then stops that sink, because the sim carrying the AECP transactor does not inject CRF receive traffic. Read the claim as 'the predicate reaches it', not 'the stop has been demonstrated on it'. Two things a reader upgrading needs: the ACMP saved-binding record's LAYOUT_VER_P moves 0x01 -> 0x02, so every binding persisted by earlier firmware is REFUSED on restore rather than fast-connected into silence (those records all carry started = 0, because nothing ever wrote the bit); and the IEEE 7.5.2 unsolicited RESPONSE for these two opcodes is NOT sent - Milan Table 5.22's GET_STREAM_INFO push on a started/stopped change IS, and the 7.5.2 half is the same systemic gap the SET_* family has, tracked as issue 69. NO new CSRs. Prior: 0x004E = STREAM OUTPUT COUNTERS REJOIN THE PROCESSOR PATH. GET_COUNTERS now serves every declared STREAM_OUTPUT from KL_talker_diag_ctx with Milan Table 5.17's compact five-quadlet layout and 0x1F mask; each counter is per descriptor, 32-bit wrapping, and driven by the real transmit, streaming, timestamp-uncertain and media-restart events. Nonexistent outputs still refuse NO_SUCH_DESCRIPTOR before the read face is touched, and counter changes expose a per-descriptor dirty pulse for the separately tracked Table 5.22 scheduler connection. NO new CSRs. 0x004D = THE STREAM_IS_RUNNING PREDICATE ARRIVES, AND SET_CONFIGURATION STANDS ON IT. Milan spells "running" two ways and they are NOT interchangeable, so both reach the engine as their own vector: a Stream INPUT is BOUND (SS5.3.8.2's pure ACMP bind level, which "does not necessarily mean that data is flowing"), a Stream OUTPUT is STREAMING (SS5.3.7.3 verbatim: declaring a Talker Advertise AND receiving a Listener Ready or Ready Failed). The reduction happens in protocol_processor_top where the SRP records are, not in a command decoder. SET_CONFIGURATION 0x0006 is its first consumer and its refusal is a REDUCTION over every stream - "if ONE OF the Stream Input is bound or ONE OF the Stream Output is streaming" - never a test of the descriptor named; GET_CONFIGURATION is read-only, correctly exempt, and now reads the dynamic store FIRST so the round trip exists at all (it read the static image before, so a controller set 1 and read back 0). The index is range-checked against configurations_count before storing, and every refusal echoes the CURRENT configuration per 7.4.7.1 ("the old value if it fails"). A uPC-map gate now runs before every suite: the engine's dispatch constants and the ucode's entry points drifted twice in one change, and a wrong uPC does not fail to elaborate - the uCPU executes ROM fill and answers a well-formed response carrying garbage. START_STREAMING and STOP_STREAMING were REMOVED from that round and moved to their own branch behind issue 78, because started/stopped had two candidate homes (the ACMP binding record, which already clears on unbind and persists, versus the dynamic store) and that choice was not a side effect of the predicate landing. SUPERSEDED at 0x004F, which answers it: the record wins and the dynamic store's selector 6 is retired. NO new CSRs. 0x004C = THE FIRST DYNAMIC SETTERS LAND IN THE PROCESSOR. SET_SAMPLING_RATE and SET_CLOCK_SOURCE are lock-protected and store per-descriptor dynamic values, their getters return those values, and SET_CONTROL / GET_CONTROL implement the volatile Identify control. The root wrapper still does not expose the new dynamic outputs to the media plane. NO new CSRs. 0x004B = THE READ-SIDE COMMAND SET LEAVES THE ECHO. Five AECP commands Milan v1.2 makes a SHALL and this entity answered with a conformant NOT_IMPLEMENTED echo are now answered for real, in the protocol processor's AECP engine: ENTITY_AVAILABLE 0x0002 (SS5.4.2.3, IEEE 7.4.3.2 - flags + acquired_controller_id + locked_controller_id, cdl 32; ENTITY_ACQUIRED is invariantly clear because Milan D7 forbids ever granting ACQUIRE, and the holder eid is read off the registry face with rgy_state 1, a query that runs no op), GET_CONFIGURATION 0x0007 (SS5.4.2.6, cdl 16, out of the ENTITY descriptor's current_configuration at offset 310), GET_STREAM_FORMAT 0x0009 (SS5.4.2.8, cdl 24, off the SAME Milan-info face word GET_STREAM_INFO publishes - 7.4.10.2's "current" format is current after a bind adapts it, which no static image knows), GET_SAMPLING_RATE 0x0015 (SS5.4.2.14, cdl 20, COPY_BUF out of AUDIO_UNIT offset 136 because the field opens its lane and the uISA has no shift) and GET_CLOCK_SOURCE 0x0017 (SS5.4.2.16, cdl 20, CLOCK_DOMAIN offset 70, which ENDS its lane and so reads right-justified). Existence is the descriptor store's in all of them, the GET_COUNTERS rule; a wrong target refuses NOT_SUPPORTED in the FULL response body and never at command length, because only NOT_IMPLEMENTED may be command-sized. Five of the Milan end-station test plan's hard gates (es-4.2, es-4.3, es-4.4, es-4.8, es-4.9) become reachable. NO new CSRs. 0x004A = THE FIRST COMMAND IS SERVED, AND EVERY ERROR IS THE SIZE THE REFERENCE STACK EXPECTS. The descriptor store heals BEFORE answering: a locate or a configurations_count read arriving while the image state is invalid triggers the header walk first and stalls the uCPU through it, so the first post-boot command serves when the loaded image is good - both silicon signatures (w3a's first-command BAD_ARGUMENTS through the NCFG path, r49a's first-command NO_SUCH_DESCRIPTOR through the locate path) reproduced in sim and retired. And a counter-less type's NOT_SUPPORTED now carries the full 7.4.42.2 fixed body (type/index echoed, zero mask, zero block, cdl 148): la_avdecc's checkResponsePayload reflects ONLY NotImplemented at command length and demands the full response for every other status, so the short echo was the complaint and the full body is the interoperable answer. NO new CSRs. 0x0049 = GET_COUNTERS EARNS ITS EMPTY MASK. A nonexistent {type, index} now refuses NO_SUCH_DESCRIPTOR from the same store locate READ_DESCRIPTOR uses (the image is the one existence authority), carrying 7.4.42.2's single response form zero-flagged; and a type outside the kept set {STREAM_INPUT, AVB_INTERFACE, CLOCK_DOMAIN} refuses NOT_SUPPORTED off the registered re-dispatch (Table 7-141 status 11: implemented command, unsupported target - ENTITY keeps nothing but ENTITY_SPECIFIC slots this build does not use, and STREAM_OUTPUT counters stay the recorded gap, refused plainly instead of succeeding empty). The integrator's wrong-object guard becomes defense in depth behind the store. NO new CSRs. 0x0048 = THE HIVE DEMOTION LIST IS ANSWERED, AND THE NETLIST LEARNED TO CLOSE. Every command the 2026-08-15 Hive session named NOT_IMPLEMENTED is served: REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION (IEEE 7.4.37/7.4.38 both formats; Milan 5.3.4.2's 16-controller registry, NO_RESOURCES on the seventeenth, 5.4.5.1 per-controller unsolicited emission with per-entry sequence ids on the reserved TX lane, 300 s TIME_LIMITED expiry with the targeted DEREGISTER); LOCK_ENTITY for real (one holder, 60 s keep-alive expiry, Table 5.22 notifications, and the ACMP listener's 5.5.2.4 check reads the SAME lock) with ACQUIRE_ENTITY refused NOT_SUPPORTED per Milan 5.4.2.1; GET_STREAM_INFO in Milan 5.4.2.10's 80-byte form with every Tables 5.9-5.12 validity flag computed from class-D truth; GET_AVB_INFO and GET_AS_PATH (asCapable live from the clock validator, the leaf path {grandmaster}, honesty ledger in the submodule's 06 6.10); GET_AUDIO_MAP now both directions (the capture map translated through the D8 role pools). TIMING, same round: the v47 sweep missed on every seed, so the four failing cones are PIPELINED - the CSR read mux is two-stage (one added read cycle on rvalid), the latency-tap stage pulses ride one uniform register, the engine's gather answer and operand shaping land in flops before the uCPU, and the TX arbiter qualifies its slot bus registered (which made it 99 LUT cheaper) - and registers tagged quasi_static get a generic multicycle 4/3 XDC rule, tag once and the placer relaxes forever. NO new CSRs. 0x0047 = THE MILAN MANDATORY SET IS COMPLETE, AND THE MAP IS READABLE. GET_COUNTERS now answers all three families la_avdecc's Milan gate demands: beside 0x0046's STREAM_INPUT twelve, AVB_INTERFACE claims LINK_UP/LINK_DOWN/GPTP_GM_CHANGED (mask 0x23; Milan 5.3.6.3 Table 5.1) and CLOCK_DOMAIN claims LOCKED/UNLOCKED (mask 0x3; 5.3.11.2 Table 5.7). Every count is an edge of one registered level, so each clause's LINK_UP=LINK_DOWN-or-+1 invariant holds structurally: link = eff_link (the entity-visible link), GM = the same strobe that drives the ADP GM_CHANGE re-announce, and locked = the CLKV lease verdict (~tu, the manufacturer-open definition 5.3.11.2 allows - one clock-validity authority for the wire tu bit AND the counter). GET_AUDIO_MAP (0x002B) is served for real on Stream Port Inputs from the render map RAM (7.4.44; Milan 5.4.2.26's fixed per-Configuration paging; NO_SUCH_DESCRIPTOR agrees with READ_DESCRIPTOR because the ucode locates the descriptor first; STREAM_PORT_OUTPUT and ADD/REMOVE stay recorded gaps). The processor also carries its own IEEE 1722-2016 Annex B MAAP engine behind quasi-static cfg_maap_internal_i - DARK in this fabric (KL_maap remains the one allocator on the wire; two Annex B engines defending one claim is a protocol violation), wired for the retirement round. NO new CSRs. 0x0046 = THE AECP ANSWERS STOP BEING ECHOES. GET_COUNTERS (0x0029) is served for real: the protocol processor lays out 1722.1-2021 7.4.42.2's 32-quadlet block and milan_datapath answers its read face from KL_avtp_rx_monitor_ctx's per-sink Table 7-157 counters - counters_valid 0xFFF (quadlets 0..11) for a STREAM_INPUT this shape elaborates, EMPTY mask + zero block for any other index or type (no wrong-object answers: the four-bit clamp is guarded). GET_MILAN_INFO answers the Milan v1.2 Figure 5.4 body, protocol_version 1. A VENDOR_UNIQUE NOT_IMPLEMENTED echo keeps its protocol_id bit-for-bit: the u bit is masked only on AEM message types, because 9.6.2's Figure 9-12 has no u bit at @22 (half the OUI space came back mangled before; Avnu's 00-1B-C5 was immune, which is why nothing saw it). Every NOT_IMPLEMENTED echo is sized by the command it reflects (cdl = 12 + payload). AUDIO_CLUSTER moved to the 2021 90-octet layout (the aes3_* tail 2013 never had), AEM_LAYOUT_REV 3, every hash-derived entity_model_id rotated per 6.2.2.8. NO new CSRs - this bump is the wire-behaviour changelog and the >= gate for software that needs to know 0x0029 is served. 0x0045 = THE SAVED-STATE VERDICT STOPS LYING. This device has NO non-volatile backend: KL_pp_shadow answers the protocol processor's class-F NVM device face with a blank-flash responder (reads 0xFF, discards writes, erase completes), and KL_persist_journal went with the legacy plane, so nothing here survives a power cycle. That is a known Milan v1.2 gap (5.3.8.2 bound state, 5.3.8.3 the four binding parameters, 5.3.8.7 started/stopped, 5.5.2.4 for when the Listener writes them). The DEFECT was that PP_STAT did not say so: the boot walk's per-record vendor default (07 section 5.3) ends with restore_done set and restore_fail clear on EVERY arm, so a device with no media reported the same status word as a device that had genuinely restored eight bindings, and a conformance checklist passed on a restore that never happened. CSR-VISIBLE: PP_STAT 0x924 gains [6] nvm_backed (CONSTANT, 0 on this build = no persistent media behind the device face) and [7] nvm_blank (the completed walk validated ZERO records), and [3] restore_fail is now RAISED when a walk completes with no backend - deliberately an existing not-successful encoding rather than a new code, so software that only knows the old bits still reads it correctly. Blank media behind a REAL backend stays fail=0 with blank=1: nothing was ever saved, which Milan permits. The processor gains restore_blank_o for this; the backend itself is specified but NOT implemented (docs/MILAN_COMPLIANCE_GAPS.md). Prior: 0x0044 = THE LEGACY 1722.1/SRP CONTROL PLANE IS DELETED AND THE PROTOCOL PROCESSOR IS THE ONLY ONE. Scenario B's substitution taken in full, with no escape hatch (USER, explicit and repeated: "remove the old code AECP/ACMP/ADP the lwSRP shall be removed as well. Only use the uCPU code"; "do not leave the option, remove everything out of the code base that is legacy"). hdl/ieee17221/aecp, hdl/ieee17221/acmp, hdl/ieee8021q/srp and the ADP advertiser/parser are GONE from the tree; KL_pp_shadow is instantiated unconditionally, its TX rides the control lane, and its class-D face IS this fabric's ACMP bind record, talker declaration and SRP reservation. WHAT A CONTROLLER SEES: the entity advertises over ADP, answers CONNECT_TX/BIND_RX over ACMP, reserves over SRP, ANSWERS READ_DESCRIPTOR, and answers every other AECP command with a conformant NOT_IMPLEMENTED echo (message_type+1, correct length, correct cdl) - never silence, never malformed. IDENTIFY_NOTIFICATION as a command is BAD_ARGUMENTS (7.4.39.2 beats 9.3.5.3.3). The entity model now lives in MAIN MEMORY: the processor's descriptor store fetches it over a read-only master at a COMPILE-TIME base (no base register to get wrong), which milan_datapath surfaces as o_desc_mem_*/i_desc_mem_* and the SoC bridges to DDR3 at the top 1 MiB of main_ram - software must load the image there before enabling the entity or every locate degrades to NO_SUCH_DESCRIPTOR (the store's watchdog abandons the burst, it never hangs). STILL ABSENT, and each reads a STRUCTURAL ZERO: GET_COUNTERS and the Table 5.22 unsolicited push, entity lock/acquire state, SET_CLOCK_SOURCE (so the media clock is pinned INTERNAL and the CRF servo is structurally off - see CRF_CLK_SELECTED_C), SET_MAX_TRANSIT_TIME (every Stream Output holds the Milan 2 ms default), the audio-map setters, and saved-state persistence. KNOWN GAP: Milan 7 ACQUIRE_ENTITY is not distinguished from the generic echo. CSR-VISIBLE: A_TXARB_DIAG 0x784 RENUMBERS to four lanes (0 ctl_tx, 1 aaf_final, 2 crf_dp, 3 adp_tx; bits 7:4 structural zero) - an old decoder reads the WRONG mux; the 0x920 processor window is unconditional (milan_csr's PP_PLANE_P is gone) and PP_CTRL[0] is ORed with ADP_CTRL[0] so either bit enables the entity. Prior: 0x0043 = THE TDM8 FRONT END JOINS THE TALKER PORT: the AX7101 declared physical_channels.capture = 0 because "the board routes NOTHING (_connectors = [])" - true before the item-4 J11 header and false since, and the reason the slot-indexed capture bucket looked pointless enough to tie off. With 0x0042 having wired that bucket and made the builder emit a uniform src=2/idx=ch/2, the eight TDM8 channels are genuinely backed, so the config declares them: the talker port goes 17 -> 25 clusters as physical 0-7, host 8-15, Pilot 16, loopback 17-24. PILOT MOVES FROM CLUSTER 8 TO 16 and entity_model_id changes 0x001BC52F5F0628F8 -> 0x001BC5441BC55569, so controllers re-discover and any bench recipe keyed on "cluster 8 = Pilot" must be re-pointed. The LISTENER port is deliberately unchanged at 8 clusters: physical_channels.render stays 0 because KL_tdm_render is a bus SLAVE whose serializer clock (tdm_bclk_i/tdm_fsync_i) a MASTER build ties to 0 (milan_soc.py:751) so it never runs, there is no KL_tdm_render_master sibling, and 8 physical + 8 host would exceed the render map's 10-key cap (AEM_DMAP_PHYS_C, KL_aecp_response_builder.sv:1533) and return BAD_ARGUMENTS for six HOST clusters - a regression, not a gap. Prior: 0x0042 = THE CRF CLOCK SOURCE STOPS BEING INDEX 2 (Milan v1.2 7.2.2, the mandatory CRF Media Clock Input): the CLOCK_SOURCE set is internal, then ONE PER AAF LISTENER, then CRF, so its index MOVES with the shape - 2 on the 1-listener shipping shape, 5 on arty_4x4, 9 on ax7101_8x8. Four places hardcoded 2 and SET_CLOCK_SOURCE rejected anything >= 3, so on every multi-listener shape a controller could not select the CRF clock at all (BAD_ARGUMENTS), the servo would have engaged on 'Stream Clock 1', and the CLOCK_DOMAIN LOCKED/UNLOCKED counters muxed the wrong source - the mandatory feature was unreachable on exactly the shapes that ship it. gen_aem_store now emits AEM_N_CLKSRC_C and AEM_CRF_CLKSRC_C beside the ROM (16'hFFFF when a shape declares no CRF source); KL_aecp_response_builder bounds SET_CLOCK_SOURCE by the DECLARED count and exports the CRF index as an elaboration constant the way it already exports odmap_dyn_o; KL_aecp_top plumbs it; milan_datapath feeds it to the media-clock restart gate, both counter muxes and KL_mmcm_drp_servo, whose servo_sel_w is now a port compare instead of == 16'd2. Derived, never mirrored: the shipping 1x1 shape regenerates to 3/2, byte-identical behaviour. Also this round: the media grid is brought out on AX7101 J11.9 (media_lrclk_o, a 50%-duty square at fs/2) beside the TDM8 fsync on J11.8, because the requirement is that the two stay ALIGNED and no simulation in this tree can check it - milan_dp clocks clk_audio_i at the axis rate, so the 24.576:100 MHz ratio that puts the grids -10.64 ppm apart is absent there, and a two-channel probe on those pins is the only instrument that can see the phase walk. Prior: 0x0041 = ONE GRID, AND IT CAN BE STEERED (Milan v1.2 7.2.2, the media-clock-sink precondition): the 48 kHz sample grid was an inline Bresenham divider whose remainder was a localparam, so it was exact against the board crystal and structurally unable to follow anything else - a talker that cannot be steered cannot be the CRF Media Clock Input Milan makes mandatory, and a listener that cannot be steered drains someone else's stream on its own crystal and slips one sample per beat period (bench 2026-08-10: one 48 kHz sample every 1.96 s through the loopback lane, 10.6 ppm). The divider becomes KL_media_nco - same Bresenham, same remainder, same denominator, plus a signed runtime trim whose LSB is 1/CLK_FREQ_HZ relative (0.01 ppm at 100 MHz) and whose clamp is DERIVED from the shape (32000 LSB at 100 MHz, 16000 at 50 MHz, both +/-320 ppm) rather than mirrored, with elaboration guards that refuse a trim large enough to need a two-step accumulator correction instead of silently dropping a sample. KL_pcm_tx joins that grid on its USE_EXT_TICK_P port - the hook its own banner reserved for "the recovered media clock" and which had been tied off since it was written - so the host playback ring and the capture crossbar are now the SAME strobe rather than two dividers that merely agree, and the ONE-GRID rule holds in phase and not just in ppm. Both actuators of the media clock now take ONE command: the servo's u, already clamped to +/-200 ppm and already published in 1/16 ppm units on A_MCSRV_STAT[31:16], drives the MMCM for the physical audio clock and the NCO for the packet grid, negated because the servo's u > 0 means speed up while the NCO's trim > 0 lengthens the period. clock_source = INTERNAL forces the trim to zero and the grid is then bit-for-bit the block it replaced, which is what lets every bench number measured at 0x0040 stand; tb/verilator/media_nco (214 checks) pins that tick-for-tick against a transcription of the old code and grades the trim against a closed-form phase oracle, because a 1-LSB remainder error does not change the tick pattern for ~144,000 ticks and a run-length check alone would have missed it. Prior: 0x0040 = A PARKED BEAT IS NOT A NEW BEAT (gh #65 CLOSED, the last issue of the conformance campaign): four monitor taps sampled a handshaked lane on VALID alone, so whenever the DMA stalled - the documented softcore-starvation and flood regimes - the producer's parked beat was consumed once per cycle, duplicating and tearing frames and spending the next real PDU on realignment. That is the true root of the recorded 'a 60-byte Listener declaration alone does not register': the MRPDU walker was always correct, the tap under it was not. All four (SRP ingress, both ACMP contexts, AECP ingress) now qualify on the full handshake, the pattern the MAAP engine has always used. The empirical double-feed in the datapath integration test is DELETED - a single feed registers, which is the end-to-end proof - and every suite gained a parked-lane torture leg. Worth recording from the round's own self-review: five of the first-cut checks did not discriminate (a stall placed before the frame so the tlast beat never parked; two more double-feeds rationalised as 'bridges re-declare anyway'; two assertions satisfiable by fields a bounce left stale; one vacuous on a value that was already set) - each was rebuilt and mutation-proven against the reinstated defect, one of them reading 209 re-latches of a single parked frame versus the fixed 1. Prior: 0x003F = A DEAD CONTROLLER IS NOTICED, PROBED TWICE AND SHED (gh #59 CLOSED, Milan 5.4.5.3 + 5.4.2.21, 1722.1-2021 7.4.4 + 9.3.6): the last wholly-absent mandatory feature. Every registered controller now carries a monitor timer reloaded by ANY valid AECP command it sends (reads count, error answers count) with a random 30-60 s draw from an entity-id-seeded LFSR so two boards never probe in lockstep; at expiry the entity sends its FIRST-EVER outbound AECP command - CONTROLLER_AVAILABLE, target = the controller, our id in the controller field, its own initiator sequence space - and the ingress gains a witness for the reply, which the packet validator drops on the floor today. Any reply of any status re-arms; silence through one retry carrying the SAME sequence id evicts the slot and pushes DEREGISTER to the departing controller ONLY, clearing every pending bit in the same cycle so no zombie slot can win arbitration and unicast at a dead MAC (the bookkeeping sits after the push arms deliberately - last-assignment-wins would otherwise re-raise a bit on the slot being freed). A refused registration force-expires the monitors so dead slots free within a second; a responding controller can never be evicted, by construction. Diagnostics at 0x6F4 (probes, replies, evictions); the timers module's staleness stub is finally the engine it always promised. sim_ctrlavail 94 checks, sim_unsol frozen at 161. Prior: 0x003E = THE LISTENER SWEEP STOPS COMPUTING INSIDE ITS OWN MEMORY CYCLE (timing, not conformance - the fix for the path Vivado named): the per-context record walk was a single-cycle read-modify-write, RAM out through fourteen levels of logic (five carry chains: the timer decrement, the one-second age increment and its limit compare, the sixty-four-bit talker match, the thirty-two-bit available-index regression) and straight back into the RAM's write port - 9.724 ns of a 10 ns budget, and the reason the design fell from +0.06 to -0.001 as the conformance work grew. It becomes three stages at unchanged throughput: FETCH addresses the record, CAPTURE registers it TOGETHER WITH every comparison and adder the transition table needs, APPLY is pure selection over flops with not one bit coming out of the RAM. The write cone drops from fourteen LUT levels with five carry chains to three or four with NONE, the module's longest topological path from thirty-nine gate levels to twenty-eight, and LUT count actually FALLS (183 fewer at the shipping shape, 599 at the default) because the mutually-exclusive classify and launch writes now share one source. A pass costs one extra cycle (eleven of a hundred thousand per wheel tick on silicon). No output pulse moved relative to its cause; a sweep visit preempted by a frame write is DISCARDED and re-fetched, never delayed, so causes still apply exactly once - and removing that single line makes the new sixteen-phase unbind sweep fail while the other five hundred checks notice nothing. Prior: 0x003D = THE MEDIA CLOCK RESTART REACHES THE WIRE IN BOTH DIRECTIONS (gh #62 items H2+H3, 1722-2016 4.4.4.3 + 10.4.3 + 10.7 Eq 14, PICS CRF-3/4/5): a restart toggled by the CRF stream we recover from now PROPAGATES - the receiver's existing toggle detector (the same term MEDIA_RESET folds, so counter and echo can never drift) drives the restart engine under the clock-source gate, and the engine widens to cover the CRF talker context so our own CRF output finally stamps the bit instead of a constant zero, inheriting the 8-PDU hold and the engine-wide single toggle target for free; the talker diagnostics' restart mux is fixed alongside (it was ANDed with the AAF frame pulse, i.e. constant zero for the CRF descriptor, so that stream output's MEDIA_RESET counted nothing). The CRF timestamp offset is rounded UP to a media-clock multiple per Equation 14 (a two-pass sequential divider on Max-Transit-Time changes, the previous rounded value held while a conversion is in flight - byte-identical at the 2 ms default, which is exactly 96 periods). SIZING NOTE worth keeping: the engine spans N_STREAMS+1, not the ACMP source count - on the shipping 1x1 shape the entity declares no CRF Stream Output, and sizing by the descriptor count hands the CRF talker a tied-off zero, which is the very defect H2b closes (KL_crf_tx emits under its own free-run escape whatever the model says). crf_rx 13475, crf_tx 123, tkdiag 77. Prior: 0x003C = THE ENTITY REPORTS THE REAL asCapable AND THE WHOLE PATH (gh #64 fabric halves J3+J4, 802.1AS-2020 10.2.5.1 + 1722.1-2021 7.4.41.2 + Milan Table 5.22): GET_AVB_INFO's AS_CAPABLE bit stops being the 'a nonzero propagation delay was written once' proxy - the daemon publishes the real per-port variable in CLKV_CTRL[2] (a LEVEL on the same lease as SYNC_OK, so a dead daemon clears the claim by construction rather than reporting healthy forever), it reads back live at CLKV_STAT[16], and it drives both the solicited flags byte and the push signature (the proxy failed in BOTH directions: stale-true after daemon death, and flapping when a starved management read published a zero delay - the new aecp mutation checks pin exactly those two cases). GET_AS_PATH grows from the two entries a single-parent register could express to EIGHT: slots 1-7 live in a staged-write group (ASP_LO 0x7DC / ASP_HI 0x7E0 / ASP_CMD 0x7E4 - commit into a slot, then publish count and bump a generation for the atomic cutover that also arms the Table 5.22 push), entry 0 stays the grandmaster identity it always was (never duplicated), a zero count reproduces the legacy derivation byte-for-byte so an old daemon regresses nothing, and the count saturates in BOTH the CSR at publish and the builder at serve. The response length is 16 + 8 per entry (descriptor_index + count behind the AEM header), reaching exactly 80 at depth 8. clkvalid 112, csr 491, aecp 2189, dp 1826, hostplane 98, behave 598 scenarios. Prior: 0x003B = THE TALKER DECLARES ONLY WHAT IS VALID AND THE NETWORK TEACHES THE DOMAIN (gh #63 CLOSED, Milan 4.3.3.1 + 4.2.7.2.1 + 802.1Q 8.6.8.2): TalkerAdvertise waits for validity - a probe window, ANY registered Listener attribute (registration not readiness, so AskingFailed can open the licence), or the reset-0 bypass LWSRP_CTRL[5], ANDed with the MAAP term (cold boot = Domain declared, ZERO talker attributes on the wire until asked); a received class-A Domain with different parameters is ADOPTED operationally (the declared Domain, the MVRP membership, the TalkerAdvertise DataFrameParameters AND the AAF/CRF C-TAGs all follow the adopted {priority, VID} pair - live at RO LWSRP_DOM 0x788, reverting on enable-fall or link-down); and the CBS credits follow WIRE TIME (per-queue Q16 debt: bytes + 24-per-frame overhead + min-frame pad, drained at the port byte rate; accrual and queue-empty decay suppressed while debt outstanding). The shipped debt law is deliberately CONSERVATIVE: client egress lands the overhead fraction BELOW idleSlope/8 (about 3.7 percent at 100 Mb/s with 64-byte frames, never above; the reservation math already carries per-frame overhead so reserved streams still fit) - the one-line alternative (overhead out of the debt) is documented in the RTL if exact client-rate shaping is ever preferred. Adjacent gaps recorded: the TA PriorityAndRank octet and the AVB_INFO msrp mapping still carry the configured pair, and the withdraw LV on enable-fall names the default pair (ages out at LeaveTime). cbs 130256, shaper_core 1.52M, lwsrp 92. Prior: 0x003A = THE LISTENER TRUSTS ONLY ITS OWN TALKER (gh #54 + #55 CLOSED, Milan Table 5.29 + 5.3.8.9 + 5.6.4): the lwSRP walker matches Talker attributes on ALL THREE SRP parameters - the FirstValue destination MAC rides the same +k borrow-out law as the stream id (802.1Q 35.2.2.8.1: they increment together) and the VLAN is equality, with the expected pair staged per listener row from the ACMP record (a mismatching TA never registers; NO_TK lawfully reprobes; an all-zero expected pair stands down per 5.3.8.9's not-settled zeros). The settled exits now zero the stream id WITH dmac/vlan (the 0x0035 deferral closed) and every fabric listener want term gained the |sid guard - a withdrawn sink withdraws its row instead of declaring stream 0. The per-sink ADP watch goes 5.6.4-true: a grandmaster/domain-mismatching ENTITY_AVAILABLE never reaches the availability latch, and an available_index regression departs the talker (record grew to 370 bits, offsets preserved; interface_index skipped - single-AVB-interface platform, rationale at the port). acmp_lstn 255+250, lwsrp_rx 182, lwsrp_ctx 109. Prior: 0x0039 = EVERY DESCRIPTOR PUSHES AND NOTHING SHOUTS (gh #58 D4 + gh #60 F1-F4 + gh #61 G1, Milan Table 5.22 + 5.3.8.10): the 60 s lock auto-expiry finally notifies every registered controller (u=1 LOCK_ENTITY, UNLOCK flag, locked_id 0 - an explicit UNLOCK never pushes); the AVB_INTERFACE push gains the per-descriptor 1 s window it alone lacked (reset saturated, raw LINK/GM totals unthrottled); the ctx monitor's dirty pulse becomes a per-context vector and KL_crf_rx raises its own (events + anomaly intervals + the bind-rise wipe, never healthy FRAMES_RX - and TV joins the exclusion while TNV stays armed, the task-21 narrowing extended), so STREAM_INPUTs 1..N-1 and the CRF Media Clock Input each own a pend class with per-descriptor limiters; sink 0 retires its legacy shadow payload and reads the SAME per-context mirror the solicited arm serves (under clk_src=2 the CRF lock tallies no longer splice into a STREAM_INPUT[0] frame - CLOCK_DOMAIN keeps the one lawful active-source mux); and the CRF sink's seven counters go 32-bit wrapping (the 255 peg and the 18-hour 16-bit wrap retired; CRF_STATUS 0x74C keeps its byte-identical ABI as documented truncated slices). sim_unsol 87->161, rxmon nx 121, crf_rx 13200, behave 588 scenarios. Prior: 0x0038 = THE TALKER TELLS THE WHOLE TRUTH (gh #56 CLOSED, commits 2+3): a PROBE_TX during a MAAP conflict window answers TALKER_DEST_MAC_FAILED with the full command echo while the probe window still arms (Milan 5.5.4.1 step 3 + Table 5.42; per-source dmac-valid = ~cfg_maap_enable | maap_addr_valid), and GET_TX_STATE_RESPONSE reports REGISTERING_FAILED live from the reservation fabric (Table 5.47: the lwSRP rows export a per-talker Listener-Asking-Failed lane, same index law as the streaming gate; the PROBE response still forces the bit to 0 - the two tables differ on purpose). acmp suite 116+83, lwsrp_ctx 96+49 with the row-map LAF leg. Prior: 0x0037 = THE LOOP REPLAYS EVERY SAMPLE ONCE (the brokensine round, user-audio-proven): the capture crossbar's LOOP source stops sampling a burst-written latest-sample latch with a paced reader (the 5-dups-and-a-jump staircase at the PDU rate - 10000 glitches/s with 8 kHz +/- 1 kHz sidebands on the certified peer's output) and gains a per-pair elastic queue (32 pairs x depth 8 x 48 bits, one BRAM36; push = complete L/R event commits off the de-interleave with a 4-deep skid, pop = a 33-cycle pre-walk delivering exactly one event per fed pair per media tick into the unchanged hold bank; walk budget 866 of 1041). The slip law goes honest and bounded: empty tick = repeat last (counted), full push = drop oldest (counted), both zero with locked clocks; a bind wipe flushes the pair's queue so a rebind never replays stale audio. Rides with: the loopback_latch hoist (the LAST always_ff automatic-temporary hazard on the runtime map path, 0x0030 class) + the NETCHECK gate (yosys-lowered netlist sim pinning the map write decode and source select exactly - the class RTL sims cannot see); four new desk pins ([T66] runtime map writes reach the RAM, [T67] PDU cadence 50 ppm + ts deltas track a live PTP_INCR rewrite, [T68/LB_SEQ_FIXED] zero-dup zero-skip ramp loop, [TSL] ts delta = 125000 never 123750); PTP_INCR's reset now DERIVES from MILAN_CLK_FREQ_HZ (the 125 MHz mirror retired) and every SoC clkout requests margin=0 (the LiteX default 1 percent request window retired; the milan PLL was always exactly 100 MHz - the wire's 123750 era was a ptp4l servo railed at the driver's 1 percent clamp, historical). Prior: 0x0036 = A RUNNING STREAM REFUSES TO CHANGE SHAPE (gh #58, Milan 5.4.2.5/5.4.2.7/5.4.2.9 + task #34): the builder finally sees the per-sink ACMP bind level and the per-output streaming licence (two 16-bit vectors, the same wires the hardware obeys - with cfg_aaf_bypass set an output truthfully counts as streaming) and speaks STREAM_IS_RUNNING - SET_STREAM_FORMAT refuses on a bound input or a streaming output (value-independent: a same-format SET while bound refuses too; the pre-bind adaptation window stays fully writable), SET_CONFIGURATION refuses while ANY served lane is bound or streaming, SET_STREAM_INFO's door widens from index 0 to every served output with the per-index streaming gate. The shrink-prune inverts to the 5.4.2.7 letter: a channel-count shrink that would orphan mappings refuses BAD_ARGUMENTS in a pre-commit check sweep (DMAP_FCHK_S) and the silent prune write path is DELETED. And the u=1 replay of a succeeded REMOVE_AUDIO_MAPPINGS re-runs its walk as a replay (both demote sites gated) so it broadcasts the SUCCESS that actually happened, never a fabricated BAD_ARGUMENTS. aecp 1968->2051 checks, dp nxn legs +7 each incl the end-to-end real-bind SET refusal, behave 585 scenarios. Prior: 0x0035 = THE LISTENER ANSWERS BY THE TABLES (gh #54+#55, the task #33 round, Milan Tables 5.27-5.39): ONE authoritative response-field law replaces the scattered echoes - refusals are pure command echo (the invalid-index path can no longer leak sink 0's bound talker into another sink's answer; a locked entity refuses BIND/UNBIND from a foreign controller with CONTROLLER_NOT_AUTHORIZED while reads stay exempt), BIND success pins dmac 0, UNBIND success pins tuid and flags 0, settled reads serve the RECORD's SRP parameters, and the flag matrix goes clause-true (FAST_CONNECT=1 in every bound state - it was NEVER set before; STREAMING_WAIT = the saved level; REGISTERING_FAILED only in RSV_OK from the live TalkerFailed). The settled machine goes Table 5.30-true: the invented TalkerFailed RSV_OK->NO_RSV arc is DELETED (it landed with a dead timer = permanent wedge on an MRPDU ordering race), EVT_TK_(UN)REGISTERED rides the COMBINED TalkerAdvertise|TalkerFailed level, and the settled exits finally CLEAR the SRP parameters (dmac/vlan zeroed, declaration dropped; sid stays until the #32 teardown story closes). The probe response is matched on all four identity fields with the sequence id captured and the RESP2 resend a byte-exact duplicate; unbind wipes the ADP availability view (no more inherited tk_avail fast-ladders); ADP aging scales at valid_time x 2 s (vt 0 clamps to 4 s). Record 317->338 bits, new fields at the MSBs so every stored offset survives. Prior: 0x0034 = THE ADVERTISER KEEPS MILAN TIME (gh #57, Milan 5.6.2 + 5.6.3.5.9): ADP_CTRL resets with valid_time 10 (wire byte 16 = 0x50 from power-on - the bench no longer provisions conformance; the write-reset literal AND the csr_default readback ROM both moved, they must mirror) and TMR_ADVERTISE is clause-true - it cannot fire while a delay window is open (Table 5.51) and restarts at EVERY ENTITY_AVAILABLE frame start (a discover response or GM re-advertise now pushes the next periodic a full period out; quantization makes that 4-5 s, early-biased, legal under the 5 s bound). Deviation banner: D1 monotonic available_index KEPT with the sharpened rationale, D2 un-jittered periodic KEPT as the bench liveness oracle (startup/link-up conform = follow-up), stale D3 retired (the MIN clamp closed it). Bite-proven: the old trigger logic fails 10 of the new checks. Prior: 0x0033 = AN UNSUPPORTED VERSION IS DISCARDED WHOLE (gh #62 item H1, 1722-2016 4.4.3.4): the AVTP stream parser gains the version-nibble gate - a PDU with version other than 0 never parses, never matches, never ticks a stream counter (version is not a format mismatch; only the interface RMON tally may move), and lock/sequence tracking free-wheel straight through interleaved wrong-version PDUs carrying wild sequence numbers. The two golden-frame builders had stamped version 1 into EVERY frame since their birth - the suites re-baseline (avtp_parser grows 536 checks incl the Group V version sweep 0-7 x AAF/CRF x tagged/untagged; rxmon [31a] flips from the recorded gap to the law + [31b] settle-first interleave). Traceability AVTP-3 CLOSED. Prior: 0x0032 = A BARE In NEVER REGISTERS (gh #63 item I3, 802.1Q-2018 Table 10-4): the three lwSRP registrars stop treating a received In event as registering or refreshing - the row-0 registrar no longer cancels its leave timer on In (a drained listener now ages out at LeaveTime instead of holding the streaming licence open one LeaveTime per hop), the ctx table's listener direction no longer registers a Talker attribute from empty on a bare In (In means the sender holds it registered but is NOT declaring - registering on it fabricated a declaration nobody made), and the listener-side TA registrar drops In from its join set (the echo of our own declaration on a loop bench read as a remote talker). Registering events are exactly New/JoinIn/JoinMt; Milan 4.2.7.2.2 modifies only the IN/rLv! cell. Mutation-proven: the new pins fail 15 ways against the old RTL. Prior: 0x0031 = THE TALKER SUCCESS TABLES SPEAK THE SPEC'S FLAG LAW (gh #56 commit 1, Milan Tables 5.43/5.45/5.47): PROBE_TX_RESPONSE echoes FAST_CONNECT and STREAMING_WAIT and forces REGISTERING_FAILED to 0 (the pipewire-lineage inversion retired - the reference cleared the echoes and echoed the failure bit); DISCONNECT_TX_RESPONSE pins all three named flags to 0; GET_TX_STATE_RESPONSE zeroes listener_entity_id and listener_unique_id (talker_unique_id still echoes; the REGISTERING_FAILED-from-registrar half and the valid-DMAC step-3 check land as gh #56 commits 2-3). Error rows keep the full command echo. Prior: 0x0030 = AN UNBIND REACHES THE PARSER AND THE LOCK LAW (task #32, the t531 campaign trio; silicon 08-07: after DISCONNECT_RX+TX SUCCESS the peer kept transmitting and OUR parser kept classifying - the stream table aliased only ENTRY 0 to the ACMP bind view while entries 1..N-1 were CSR-window-only, so the departed stream stayed enabled, LATE events armed the 0x0028 push law into 1-per-second unsolicited GET_COUNTERS to every registered controller, and Hive rendered the churn as input FLAPPING; and MEDIA_UNLOCKED never fired, parking Table 5.6's LOCKED = UNLOCKED+1 invariant at +1 forever). New law: (1) EVERY stream-table entry rides its own sink's ACMP bind level (entry 0's alias generalized; the CSR-window override still WINS while armed and release-to-alias eviction is per-entry) so an unbind evicts the classification entry and the departed stream's frames become foreign at the filter; (2) the table exports bind_fall pulses and the ctx monitor treats a wipe-while-locked as the 0x002B law's second unlock cause, riding the PROVEN silence-unlock walk - unlock increments before any later bind zeroes counters; (3) the odmap boot seeder's key/template resolve is hoisted from always_ff automatic temporaries to module-scope wires (the synthesis-hazard class behind the tdm8 ADD_AUDIO_MAPPINGS key+1 silicon shift - the source key math was PROVEN correct on both table geometries, the store/GET served from the same register read true while the RAM write address shifted per-bitstream; the 07-21 LUTRAM-replica lineage) and the aecp suite gains the tdm8-shape leg (51 checks) that pins the seed and the byte-exact silicon ADDs on the SHIPPING tables. Prior: 0x002F = THE LISTENER LATENCY IS A SETPOINT, NOT A MIDPOINT (task #28; USER final form: 'once the clock is locked, the latency must be always the same regardless of the clock domain source. the system should pick the sample as soon as possible and feed the audio sink'). KL_i2s_playback gains SETPOINT_P: the elasticity FIFO's steady-state fill IS the input->cluster latency, so it runs at the packetization floor the integration passes in - milan_datapath passes (6*2)+4 = 16 samples (one class-A stereo frame + a 4-sample CDC allowance = 8 pairs, ~167 microseconds at 48 kHz, inside the USER 125-200 microsecond band) - instead of the RAM midpoint; the 512-deep RAM keeps its full depth as TRANSIENT margin above the setpoint. Uniform law: the prefill default releases at the setpoint, the 0x002A GM recenter snaps rptr to wptr-SETPOINT, the convergence band is +/-12 samples (the USER +/-6-pair wander budget) with the reset rail at +/-24 and the LOWER rails CLAMPED at zero (16-24 must mean 'the underrun rail owns everything below', never an unsigned wrap). NOTHING in the sample path varies with clk_src - source selection changes who disciplines the media clock, never the delay. SETPOINT_P=0 keeps the proven legacy midpoint (bring-up shapes); the pcm_playback suite runs BOTH legs (43 checks each). Prior: 0x002E = GET_STREAM_INFO FLAGS OBEY MILAN TABLES 5.9/5.11 (task #31; silicon 08-07: Hive on t531 showed identity valids + BOUND on every DISCONNECTED stream - the response builder hardcoded 0xF2/0xF6 flag words regardless of state). New law, INPUTS (Table 5.9): a disconnected sink answers STREAM_FORMAT_VALID alone (0x80000000); identity valids (STREAM_ID|DEST_MAC|VLAN) iff SETTLED (probing status PROBING_COMPLETED per Table 5.5; the CRF sink's bound-with-record level stands in - it has no probing view), ACC_LAT_VALID iff registering a matching TA/TF, MSRP_FAILURE_VALID + REGISTERING_FAILED (bit 25, same value per the table note) iff TF, BOUND = the bind level, FAST_CONNECT SHALL be 1 when bound + SAVED_STATE recommended 1 when bound (the old code claimed both FORBIDDEN - Table 5.9 says the opposite), STREAMING_WAIT only while bound. OUTPUTS (Table 5.11, a DIFFERENT law): FORMAT + ACC_LAT ALWAYS valid (an idle talker answers 0xA0000000, never bare format - the presentation offset is always real), identity valids iff DECLARING a TA/TF (proxy: talker_active|tk_fail - exact on the 1-talker ship shape, the per-index declare vector is the documented follow-on), MSRP_FAILURE iff TF, and BOUND/FAST_CONNECT/SAVED_STATE/STREAMING_WAIT shall be ALWAYS 0 on an output (the old word set BOUND unconditionally - wrong even while streaming). The payload fields were already gated right upstream; only the flag words lied. Prior: 0x002D = THE CRF MEDIA CLOCK INPUT SINK GETS ITS OWN lwSRP LISTENER ROW (task #27; closes MILAN_COMPLIANCE_GAPS.md 3; silicon 08-07: the DS20's CRF output was BOUND to our CRF sink over ACMP - connect-tx OK, one PDU arrived - and then went silent, because our Listener Ready structurally could not go out: the pinned-LAST CRF sink had NO lwSRP attribute row to declare into, so the certified talker rightly stood down per 5.3.7.3's licence law and the MMCM servo sat IDLE forever on clk_src=CRF). New law: an SRP_CRFSNK row+slot pair is appended past the dedicated sink-0 pair exactly the way THAT pair was appended in 0x0023 (rows never renumber; the 5-bit widening already made the room - the old '4-bit space exactly full' note predated it), the lsn_srp_prov provisioner gains lane N_STREAMS deriving the row from the CRF sink's own ACMP bind record (want = the BIND level, upstream terms only), and the sink's SETTLED_RSV_OK feedback reads its own row's registrar instead of constant 0. ALSO: KL_acmp_lstn_ctx's view1 compatibility record (the CRF servo's DMAC filter + ACMPL_STATE[31]) re-aims from the literal ctx 1 to the pinned-LAST ctx N_SINKS_P-1 - identical on 2-sink shapes (the shipping 1x1_tdm8), the WRONG AAF sink before on wider shapes. With #26's crossbars and this row, a CONNECT_RX on the CRF sink now yields: row provisioned, Listener declared, Ready on the talker's TA, CRF PDUs flow, and the clock-followership chain (USER: 'we follow whatever the clock_domain is set to') has its enabler. Prior: 0x002C = THE CROSSBARS ARE IN-CIRCUIT BY CONSTRUCTION ON DYNAMIC-MAP SHAPES (task #26; USER 'the ATDECC map IS the model' - silicon 08-07: the Pilot tone sat mapped-and-committed in the map RAM for hours while CHMAP_CTRL[0]=0, a DEBUG-classed bit that resets 0, kept the wire on silence-fill; the ATDECC-authoritative cleanup had removed the bench poke that hid the gap since bring-up). New law: the AECP response builder - the ONE module that compiles the generated AEM ROM - exports dmap_dyn_o/odmap_dyn_o shape-truth constants (deriving beats mirroring an order-fragile compilation-unit `define), and milan_datapath's two feed muxes follow the SHAPE: a shape that compiled the dynamic-map machinery (writers + boot identity seeder) routes the capture crossbar into the packetizer and the render crossbar into the DAC feed UNCONDITIONALLY - power-on reproduces the legacy front-end THROUGH the seeded identity map with no software arm to forget - while a STATIC shape (no writer, no seeder, the RAM would stay silent forever) keeps its declared front-end routing with CHMAP_CTRL[0] retaining its bring-up meaning: arm the debug-written crossbar. 0x900[0] is thereby debug-only on every shape. Prior: 0x002B = MEDIA_LOCKED FREE-WHEELS THROUGH gPTP CHANGES (task #25, USER 'fix the lock related to gPTP change first'; Milan 5.3.8.10 + 4.4.2.3 + 1722-2016 E.2.1 + the es-12.11 test-plan invariant). MEDIA_LOCKED is now the stream-vs-timebase CAPABILITY predicate: an accepted in-format PDU with a placeable timestamp locks the stream for EVERY clock source ('whatever where the media clock comes from'), and convergence loss - a grandmaster handover, a clock-source change, a playback-FIFO excursion - NEVER unlocks a flowing stream (free-wheel). The old law gated the render stream's lock on i2spb convergence: every gPTP change dropped lock, withdrew nothing in SRP (correct) but flapped every controller's view and, through the old acquire gate, held fresh binds unlocked for the whole re-convergence walk. MEDIA_UNLOCKED remains for genuine stream loss only (100 ms silence, bind wipe); the playback pipeline keeps its own I2SPB counters and the 0x002A recenter's MEDIA_RESET; servo state stays on CLOCK_DOMAIN.LOCKED. The rxmon suites' [26] block and the IV9f era-boundary sweep now prove churn is pure noise. Prior: 0x002A = A GRANDMASTER CHANGE RE-CENTERS THE PLAYBACK FIFO (task #22 fabric half; USER 08-06 'make the gptp react faster to change', measured ~2 min re-lock on silicon). A GM-identity change means the PHC - the presentation timebase - may just have STEPPED by seconds; nothing in the media path reacted, so KL_i2s_playback's convergence observer walked its fill back into MID+-64 at the residual rate error (133 s at 10 ppm) while every frame missed presentation. milan_datapath now edge-detects the leased GM identity (first lease out of reset exempt - prefill owns boot) and pulses the new KL_i2s_playback recenter_p_i: the read pointer snaps to wptr-MID THIS cycle (fill = MID exactly), media_reset_p_o pulses honestly (one audible discontinuity instead of two silent minutes), and converged re-confirms in its normal 100 ms. The software half (PipeWire-style DLL, no phc2sys) stays on the roadmap. Prior: 0x0029 = THE LISTENER ACCEPTS EVERY CHANNEL COUNT (Milan BAF v1.1 Section 4 + USER 08-07: 'the stream input format must accept every format, but does not need to route all channels'). The RX monitors' format gate becomes a FAMILY compare - subtype, encoding, rate, bit depth, sparse - and the wire's channels_per_frame leaves the acceptance test entirely: the configured format is the NOMINAL selection, the depacketizer de-interleaves by the PDU's own count, and the input maps route the subset (channels beyond the wire render silent). Decoded live 08-07: the DS20's wire vs a 4ch-set sink produced an 8000/s UNSUPPORTED_FORMAT flood the old bound manufactured; a Base Listener supporting a rate family SHALL support all its channel counts. Prior: 0x0028 = COUNTER PUSHES ARE FOR EVENTS, AND FRAMES_TX MEANS INTERVALS (task #21, both decoded LIVE on 0x0026 silicon 08-06 with the first registered controller). (1) The Table 5.22 change-detectors in KL_talker_diag_ctx / KL_avtp_rx_monitor(_ctx) armed on the FRAMES_TX/FRAMES_RX tallies - counters that grow on every healthy interval by construction - so ONE REGISTER_UNSOL bought a permanent 1/s GET_COUNTERS push per stream descriptor forever (4/s measured on the wire). The dirty law is now EVENT-ONLY: lock/unlock, start/stop, seq-mismatch/interrupted, late/early, tu, media-reset, format-reject and the bind wipe arm a push; routine frame tallies never do (an ACTIVE anomaly interval still pushes - that state IS changing). (2) KL_talker_diag_ctx's FRAMES_TX added the interval's FRAME TOTAL (facc accumulator) instead of the Table 5.4 +1-per-observation-interval - the header's own '8000x off' warning, live on the wire (11M read where ~1.4k intervals had elapsed); the accumulator is retired and the counter advances at most 1/s. tkdiag T3/T14 pin both at desk. Prior: 0x0027 = ONE CLUSTER == ONE AUDIO CHANNEL (USER 08-06). The capture crossbar's map RAM re-keys from N*4 pair slots to N*8 CHANNELS - one 13-bit {en, half, src, idxh, idx} entry per stream channel - so every Stream Output channel independently selects any cluster (any source pair, either half). ADD/REMOVE_AUDIO_MAPPINGS drops the last two pair-geometry vendor rules (half-parity, sibling-of-slot): what remains is own-stream, channel < format count, cluster in pool with cc=0, and no duplicate channel per command; a one-record Hive edit on any channel now succeeds. Remove writes a zero entry - silencing one channel touches only it. The 0x900 debug window re-keys to channels with it (WORD[8] = half, was reserved). Prior: 0x0026 = THE ETHERNET IS GUARDED FROM ITS OWN SOFTWARE (USER 08-06: 'a kill switch that should let the ethernet up on running until the software un-guards it'). A_ETH_GUARD 0x7D8, ARMED FROM POWER-ON: while armed, A_PHY_RST writes are dropped, A_LINK_CTRL[1] (mac_reinit) is masked, both read back their TRUE flops (live_mux carve-out - a refused write must never read back as accepted), and o_eth_guard exports for the SoC to gate the LiteEth phy_crg chain (v2; v1 pairs with milan-statd reading the CSR before its reinit). Unguard = the magic 'UNLK' (0x554E4C4B); any other write re-arms - a lease posture, not a boot flag, per the CLKV precedent. Prior: 0x0025 = ANY HALF ONTO ANY CHANNEL (USER 08-06: the half-swap mux). The capture crossbar's pair-slot word grows per-channel half-select bits [15:14] (legacy writers say 'natural' bit-for-bit); the ADD/REMOVE_AUDIO_MAPPINGS commit derives the swap from cluster-half XOR lane-parity (mono TONE pinned natural - the canonical word), and vendor rule 2 (source-half parity, the one route the crossbar could not make) RETIRES - cluster 16 onto channel 6 is now one lawful edit. Rules 1/3/4 stand: one source pair per slot remains physics. Prior: 0x0024 = THE ENTITY VOLUNTEERS ITS STATE (Milan v1.2 Table 5.22 closed). The registered-controller push set covered only {STREAM_OUTPUT info on ta/lo edges, input-0 counters, AVB_INTERFACE counters on link/GM edges, per-talker counters}, so a controller watching a LISTENER saw bound state / probing status / ACMP status / stream ID / MSRP latency / started state freeze until it happened to re-poll - the 08-06 field report (Hive panes stale on every input stream). Four push classes close the table: GET_STREAM_INFO(STREAM_INPUT) for sink 0 AND the CRF sink, armed by a change-signature register over EXACTLY the fields load_input_stream_info_consts serves, with a 16 ms settle dwell so a bind burst lands as ONE frame carrying the settled state; GET_AVB_INFO off {GM, pdelay/asCapable, domain, SR VID} (1 Hz-bounded - pdelay is a measured value); GET_AS_PATH off {GM, parent bridge} (payload builder shared with the solicited arm); GET_COUNTERS(CLOCK_DOMAIN) off the media-lock tallies under Table 5.22's own per-descriptor 1/s bound. Lawful residue, in the matrix: per-sink input counter pushes above sink 0 (monitor dirty is sink-0-only), CRF-input counter pushes, the 5.4.5.3 controller monitor. Prior: 0x0023 = THE ACMP LISTENER'S SINK 0 OWNS A REAL lwSRP ROW. The legacy flat pair (row 0, the 0x694 word) is the talker-0/software-owned attribute, and sink 0's TA coupling used to read THAT row's registrar, so a bind on sink 0 could never see the peer's Talker Advertise register against its OWN stream: the SM re-probed forever, no Listener Ready was ever declared, and the licence never opened - the 07-28..08-05 return-leg cluster, root-caused live at the inline tap. The attribute table grows ONE dedicated listener-0 row at index L+T-1 (SRP_LSN0_ROW_C), fabric-provisioned by the same rotating requester the k>0 sinks use (want = ACMP-bound & engine-on & ~software-owned), declared on the wire at bind time with the DERIVED sid {talker_entity_id, talker_unique_id} (the probe answer re-provisions the same row with the authoritative sid/dmac per Milan v1.2 5.5.3.5.18), and sink 0's SETTLED_RSV_OK promotion (5.5.3.5.27) now reads ITS OWN row. The 0x800 window gains A_STRM_SEL[9] = listener-0 row select ({dir=0, idx=0} is the park state and cannot carry the meaning); A_STRMW_SRP's idx-0 hard alias of 0x694 YIELDS to [9]. Same pass, wire-facing on wide shapes: KL_lwsrp_ctx_tx's batch walker kept a 4-bit row cursor whose 4'hF doubled as both no-more-rows and REAL LANE 15, so any build whose extension-lane count reached 16 - this round's 8x8 + CRF + listener-0 = 17 rows - could NEVER serialize its top lane's attribute and re-emitted a stale row's sid in its place (found by the milan_dp 4c leg: the dedicated row provisioned, registered and promoted while the wire carried a two-tests-old stream_id); the sentinel moved OUTSIDE the lane space (6'd63) and every row index in the ctx/walker path widened to 5 bits with a <=32-row elaboration guard. Prior: 0x0022 = THE AEM STORE HAS A SECOND WRITE MASTER, SO MILAN PERSISTENCE CAN ACTUALLY BE REPLAYED. Milan v1.2 puts eleven unconditional persistence SHALLs on a PAAD-AE and every one of them could already be READ; most could not be PUT BACK, because KL_aecp_aem_store's write port had exactly one master - KL_aecp_response_builder's SET_* write-back. No CSR reached it, and a self-addressed AECP command cannot reach it either (the parser taps the RX path; a frame the board sends to its own MAC is never forwarded back to the sending port). The new group 0x7C8-0x7D4 is that master: software names a DESCRIPTOR and a FIELD - never a byte address - and the fabric resolves the range from the SAME generated WB_STRIN_FMT_ADDR_C / WB_STROUT_FMT_ADDR_C / WB_SAMPLING_RATE_C / WB_CLOCK_SRC_IDX_C tables SET_STREAM_FORMAT itself uses, so a config regeneration can never leave a shell script pointing at a stale offset. The payload runs through the SAME acceptance the AECP setter applies (the 5.3.8.1 supported-format family test against that descriptor's own generated reference, the AEM_RATES_C table, the 0..2 clock-source bound), because a restore that installs a format the entity does not declare is a worse conformance break than the revert it fixes. And the whole group is REFUSED - never queued - while ADP_CTRL[0] is set, which turns "replay before the entity advertises" from an init-script convention into a property of the hardware. Closes 5.3.8.1, 5.3.7.1, 5.3.5.1 and the descriptor half of 5.3.11.1; 5.3.7.6 and 5.3.13 are answered by NAME (verdict VD_FIELD) because they live in response-builder register files with no slave port yet, and 5.3.4.1 / 5.3.4.2 - which require the OPPOSITE, being CLEARED by a power cycle - are unreachable by construction since no field code resolves to either. Gated by tb/verilator/aempatch, 92 checks, 10 of 10 injected defects caught. PRIOR (0x0021) = THE TSPEC NOW DESCRIBES THE FRAME THIS BUILD ACTUALLY EMITS. 0x0020 made the Talker TSpec arithmetic Milan's; this one makes its INPUT the elaborated wire width instead of a register nothing writes. milan_datapath computes every talker row's MaxFrameSize from tctx_chans_r, a shadow of the TCTX w0 `chans` field - and no board software writes that window, because the rows are provisioned by the fabric (srp_fab_rec_mux). The shadow reset to 4'd2 while KL_aaf_packetizer reset ITS per-talker chans to the elaborated WIRE_CHANS_C, so on the shipping 4-channel Arty the wire carried a 120-octet AAF AVTPDU and talkers 1..N-1 DECLARED 73 - reserving 7.36 Mb/s for a stream occupying 10.368, and CBS grants credit against the declaration, so the under-reservation lands as drops under load rather than as an error anywhere. Talker 0 escaped it because the fabric mux loop starts at s=1 and slot 0 keeps cfg_lwsrp_max_frame, which is the same index-0-works / 1..N-1-broken signature as 0x001F. The reset is now aaf_chn_clamp(TALKER_WIRE_CHANS_P), the SAME parameter the framer is handed, so reservation and wire agree by construction at 2, 4 or 8 channels and a CSR write still overrides. The tb/verilator/milan_dp suite gained an obj_nxn4c leg that elaborates the shipping Arty shape (4 streams x 4 wire channels over the TDM8+I2S blend) - nothing in the suite had ever elaborated a build whose framer width differed from the shadow's reset, which is exactly why two equal numbers hid a defect. PRIOR (0x0020) = THE TSPEC IS MILAN'S, NOT OUR OWN ARITHMETIC. Milan v1.2 4.3.3.2 Table 4.4 fixes the Talker TSpec per stream format and 4.3.3.2's note fixes the four-step bandwidth recipe that turns it into kbps; we matched neither exactly, and both errors ran in the UNDER-reserving direction, which is the one that starves CBS credit and drops frames under load. (1) MaxFrameSize omitted the mandated trailing +1 octet - the table reads 24*N + 24 + 1 for AAF PCM32 48 kHz and its note explains the byte exists because "the sampling clock of the PAAD may be a bit faster than the nominal frequency" - so a 2-channel stream declared 72 where the clause says 73 and reserved 7296 kbps against the mandated 7360. (2) The bandwidth gate folded the recipe into one +42 constant, which is steps 1 and 3 added together and silently DROPPED step 2, the 68-octet tagged-minimum-frame clamp; every stream short enough to be padded on the wire therefore reserved less than it occupies. The CRF Media Clock stream is the one that bites: Table 4.4 gives it MaxFrameSize 28 + 1 and 5632 kbps, we declared the padded MSDU 42 with no clamp and reserved 5376, and starving CRF destabilises the media clock of every listener downstream. The gate now runs the clause verbatim (F = MaxFrameSize + 22; if F < 68 then F = 68; W = F + 20; bits/s = W * MaxIntervalFrames * 8000 * 8) and the CRF row declares the table's 29, whose clamped reservation of 88 octets covers this stream's real 84 - so the table value and the padding stop being in tension. Found by integrating an independently written 802.1Q/Milan conformance lane, whose TSpec expectations were right and ours were not. PRIOR (0x001F) = EVERY AAF TALKER EGRESSES, WITH ITS OWN IDENTITY. The companion to 0x001E: that round gave every AAF talker row an lwSRP DECLARATION, and the streams still never left. Two survivors of the same root cause - per-talker state that only the 0x800 CSR window writes, which no board software drives - were found by an adversarial review round before the fix ever ran (silicon m001g: the bind soak's t0 leg fully green, listener FRAMES_RX ~18 k/s, while t1/t2/t3 all sat at tx-interval 0 despite CONNECT SUCCESS, declared SRP rows and tu=0). (1) ADMISSION: aaf_stream_en_w[t>0] ANDed a TCTX w0 CTRL[0] shadow that RESET TO 0, so on a shape-static build (0x0015+, stream counts read-only from elaboration) no talker above 0 could ever egress. It is DELETED, not inverted: 1722.1-2021 Table 8-4 bit 12 makes STREAMING_WAIT an option, Milan v1.2 5.4.2.19/5.4.2.20 require NOT_SUPPORTED for START_/STOP_STREAMING on a Stream Output, 5.3.7.3 'excludes the possibility for a Stream Output to be stopped' and 5.5.4.1 says a Talker 'shall always stream AVTP packets as long as bandwidth is reserved', so a per-stream software enable is not ours to have and the old reset-0 term was itself a SHALL violation. AAF_CTRL[0] is now the one enable for every talker, exactly as it always was for t0, and the per-stream lwSRP gate is REQUIRED for t>0 (t0's ~cfg_lwsrp_enable escape is deliberately not mirrored: LWSRP_CTRL resets to engine-OFF, so mirroring it would admit unpaced PROBE_TX-only streams out of reset - the ~56 kframe/s board-killer whose only mitigation was the software arming step that no longer exists). (2) IDENTITY: KL_aaf_packetizer read dmac/vid/unique_id for t>0 ONLY from TCTX w0/w1/w2, the same never-written window, so an armed talker framed to dmac 00:00:00:00:00:00 on VID 0 with stream_id {station_mac, uid 0} - colliding with t0 and reaching no listener - while its own lwSRP row declared {station_mac, uid t} and the ACMP answer promised dmac base+t: three sources of truth for one stream. The packetizer now DERIVES the same identity the other two publish (dmac = MAAP block base + t, vid = the engine VID, unique_id = t) with software-named-wins per field (the CRFT_SID precedent), so advertisement, ACMP answer and wire cannot disagree. SOFTWARE-VISIBLE: a talker above 0 now streams as soon as SRP licenses it with no window write at all, and TCTX w0 bit 0 no longer gates egress (the word still carries chans/VID). PRIOR (0x001E) = EVERY AAF TALKER ROW IS ADVERTISED. WIRE-FACING and the whole point: the lwSRP provisioning port had exactly two writers - this window (which no board software drives) and the fabric's CRF Media Clock Output row - so no AAF talker row above 0 ever held a reservation. Measured twice: A_STRMW_SRP 0x85C read 0x0000_037E at talker idx 0 (a live hard alias of the legacy flat row, which is why idx-0-only reads looked healthy) and 0x0000_0000 at idx 1/2/3 on a 4x4 board, and a ProfiShark capture inline on the board link with a licensed stream running showed MSRP declaring a Talker Advertise for exactly {02:00:00:00:00:02, uid 0x0000} and {..., uid 0x0004} (uid 4 = N_STREAMS = the CRF output) and NOTHING for uid 1/2/3 - the two stream_ids on the wire were precisely the two rows that had a provisioner. Milan v1.2 5.3.7.3 conditions streaming on declaring a Talker Advertise AND receiving a Listener Ready/Ready Failed, so an unadvertised stream can never be licensed: no talker but 0 could stream, whatever the registrar computed. milan_datapath now gives every AAF talker row its own fabric requester, wanting on that row's own TCTX CTRL[0] enable (never on the bw-gate, which is an OUTPUT of the engine, and deliberately not on ACMP talker_active - 5.5.2.7 licences a stream on SRP alone, so the advertisement must exist BEFORE a controller binds or fast-connect finds no reservation to register against) and deriving stream_id {station MAC, uid = idx} + DMAC MAAP base+idx + TSpec MaxFrameSize 24 + 24*C from that row's own chans field. SOFTWARE-VISIBLE CHANGES AT THE 0x800 WINDOW: SRP and SID_* at talker idx>0 now read a fabric-provisioned row instead of 0, and the lwSRP provisioning record obeys the SAME {dir, idx} staging guard the stream-table side has carried since 0x000F - it used to take the shared staging set unconditionally, so a sid staged for one selection was written into whatever row was committed next (desk-measured: talker idx2's row read back the sid staged for listener idx2). A commit naming no sid for its own selection provisions the ZERO sid, which is RELEASE-TO-FABRIC for an AAF talker row; a non-zero named sid still wins outright, per the CRFT_SID precedent. 0x001D = ADP LIVENESS IS READABLE. SAME MINOR, WIRE-FACING: the ADP re-announce period becomes MIN(5, MAX(1, valid_time/2)) seconds - the FASTER of Milan v1.2 Table 5.50 (TMR_ADVERTISE "a timer with a fixed value of 5 seconds", restarted on every send by 5.6.3.5.9, under the 5.6.3 "shall implement an independent instance of the Advertise state machine") and IEEE 1722.1-2021 Figure 6-2 (reannounceTimerTimeout = MAX(1, valid_time/2) SECONDS) - where it used to be valid_time seconds: 10.000 s measured on the wire at valid_time 10 and 31 s at the ADP_CTRL reset value, 2x and 6x slow, which is what made a 5 s passive discovery pass hit 1/0/1 and read as "the advertiser goes dormant" while a capture proved 7.4 h of unbroken advertising. The advertised valid_time FIELD is deliberately untouched (a controller told 62 s and refreshed every 5 s is safe; shrinking the field would cut the validity horizon). Arming is a LEVEL per Milan 5.6.3.5.2 "Startup of the PAAD-AE with link status up" + 5.6.3.5.3, so no swallowed link_up pulse or S50 init order can leave an ENABLED entity on a LIVE link silent and no devmem toggle is ever needed; ADP_CTRL[0] = 0 is now Table 5.49 DOWN, so re-enabling re-advertises. BEHAVIOUR CHANGE VISIBLE AT 0x668: rearm_cnt counts LEVEL arms, so a clean cold boot reads 1 (the STARTUP arm, not an anomaly) and the enable 0->1 recovery adds one - a count that keeps CLIMBING while depart_cnt stands still is still the state-upset signature. Milan Table 5.50 GM_CHANGE (5.6.3.5.7; IEEE Figure 6-5 UPDATE GM) is implemented in fabric for the first time - milan_datapath ties gm_change_i to 1'b0, so a grandmaster election reached the wire only at the next periodic even though 5.6.4.5.2 step 2b makes a Milan listener test that field - by latching advertisedGrandmasterID/domain at start-of-frame and treating a difference as the event. New RO live register A_ADP_DIAG2 (0x674) = {[31:28] state {send_pending, busy, disc_pend, available}, [27:24] last message_type sent, [23:16] ENTITY_DISCOVERs SEEN on the wire (any target), [15:8] ENTITY_DISCOVERs ACCEPTED for this entity (IEEE 1722.1-2021 6.2.7 target test passed), [7:0] ADPDUs EGRESSED}, all wrapping 8-bit counters and all zero at reset. WHY: on 2026-07-30 a whole investigation ran on the premise that the advertiser goes dormant, and the only ADP diagnostic register, A_ADP_DIAG 0x668, could not refute it - depart_cnt 0 and rearm_cnt 0 are the TRUTHFUL reading of a healthy advertiser that never departed and never self-re-armed, and they are ALSO what a stalled one would read, so distinguishing the two took a peer-side wire capture (which found ADPDUs at exactly 10.000 s spacing and available_index 2681->2682->2683 = 7.4 h unbroken). 0x674 answers it from one devmem read: sent_cnt moves or it does not, and state[0] IS the available_r the hunt was asking about. The two discover lanes separate the three cases that look identical from the entity's side - nobody is discovering (seen = 0, which is what the peer tool's PASSIVE 5 s discover verb actually does), discovers arrive for other entities (seen > 0, accepted = 0), discovers arrive for us (both move). SAME-VERSION RTL, NO CSR-VISIBLE CHANGE: the discover-response random delay now scales with valid_time per 6.2.4.2.2 ("a random delay with a uniform distribution across the range of zero (0) to 1/5 of the valid time of the ATDECC Entity in milliseconds", and 6.2.2.5 makes the valid time 2*valid_time seconds, so the bound is 0.4*valid_time s): valid_time >= 4 draws the identical [0.2 s, 1.542 s] envelope it always did, valid_time <= 3 - where the old fixed envelope exceeded the bound and could answer a discover after the entity's own validity horizon - shrinks to [0.1 s, 0.268 s]. Every shipped config and the ADP_CTRL reset (valid_time 31; the bench runs 10) take the unchanged arm. NOTE FOR THE MERGER: this branch forked at 0x001C, so if a parallel lane lands another minor first, renumber this entry rather than dropping it; 0x001C = DYNAMIC AUDIO MAPPING ON EVERY LISTENER STREAM PORT. The AEM command surface changes, and on the NxN boards the power-on audio routing changes with it. Milan v1.2 5.3.3.9 is a shall and it is plural: "The Stream Port Input of a Configuration shall not contain any AUDIO_MAP descriptor. Note: this means that a PAAD-AE implements dynamic mappings on all of its Stream Port Inputs." Until this version the fabric engine served exactly ONE port - STREAM_PORT_INPUT[0] - and no shipped config even armed it, so every listener port advertised a static AUDIO_MAP and ADD_AUDIO_MAPPINGS (0x2C) / REMOVE_AUDIO_MAPPINGS (0x2D) answered NOT_SUPPORTED on all of them. A controller therefore could not re-route a received channel at runtime at all, which is what the loopback / tone / 8-channel work needs. Now: the `AEM_DYNMAP store in KL_aecp_response_builder is keyed by the GLOBAL cluster index (the addressed port's base_cluster + the record's mapping_cluster_offset, mono clusters per 5.3.3.8 so one key IS one Audio-Cluster channel), which is EXACTLY the render crossbar's map-RAM address - the model, the fabric and the CSR 0x900 debug window share one index space. GET_AUDIO_MAP pages each port's own fixed partition and reports that port's own number_of_maps (5.4.2.26); mapping_cluster_offset stays PORT-RELATIVE on the wire (1722.1-2021 7.2.19) while the store stays global, so the ports cannot alias each other and an offset past the addressed port's own cluster block is BAD_ARGUMENTS rather than a write into its neighbour. An entry now also carries mapping_stream_index, because 1722.1-2021 Table 7-33 defines it as "the STREAM_INPUT or STREAM_OUTPUT descriptor index for the stream carrying this channel" - any Stream Input may feed any port - and the 5.4.2.27 channel bound is taken from THAT stream's current format through a per-STREAM_INPUT live channel-count file that follows SET_STREAM_FORMAT (5.3.10.1: "the index of the mapped Stream Input's channel shall be lower than the number of channels in the current format of the Stream Input"). A CRF Stream Input carries no audio channels and is rejected. Stream Port Outputs keep their static AUDIO_MAP and keep answering NOT_SUPPORTED, which is what 5.4.2.26-28 mandate for a port that HAS Audio Maps; a static input port in a mixed shape answers the same way. CONFIG CHANGE: configs/endstation_arty_4x4.yaml and configs/endstation_ax7101_8x8.yaml now carry map_mode: dynamic on every listener (16 and 64 store keys), so those gateware images advertise number_of_maps=0 on each STREAM_PORT_INPUT and their render crossbar POWERS UP UNMAPPED - the mapping list is fabric state with no non-volatile plane behind it, so 5.3.10.1's "saved in a non-volatile memory and restored after a power cycle" is a recorded deviation and a controller (or the 0x900 debug port) must program the routing after every boot. configs/endstation_arty_current.yaml stays static, so the TRACKED entity definition and its golden are byte-identical and scripts/check_entity_shape.py is unmoved. DEFECT FIXED IN THE SAME PASS: milan_datapath drove the render map RAM's write address as aecp_dmap_wr_addr_w truncated to $clog2(CHMAP_PHYS_C) = 4 bits. With one 8-key port that was unreachable; with 8 ports of 8 clusters the 8x8 model declares 64 keys against CHMAP_PHYS_C = 10 physical render channels, and key 16 would have silently aliased onto the I2S L channel. The write is now GATED on addr < CHMAP_PHYS_C - an out-of-range key is dropped, and the AEM answer stays truthful about a mapping the board has no pad for. 0x001B = THE TX-TRUNK SUPERVISION ROUND (2026-07-29, the m001a/m001c silicon TX wedge): every one of the eight cascaded adp_tx_arbiter frame-locks is SUPERVISED - a held grant making no progress for 2^17 axis clocks (~2.6 ms at 50 MHz; legal stalls are frame time + the 512-cycle IFG gasket, orders of magnitude shorter) is adjudicated at expiry by the granted source's tvalid: LOW = the source ABANDONED its frame, so the arbiter closes the frame itself (one injected zero-data all-keep tlast beat; HONEST BOUND: the MAC recomputes a VALID CRC over the truncated bytes, so one well-formed runt with corrupt content egresses per abort event - traded against a permanently dead port), releases the lock and sets its abort-sticky lane; HIGH = the refusal is BELOW the mux (CDC/MAC), releasing cannot help, so only the stall-sticky lane is set. The lock point STAYS at first accepted beat: a lock-at-presentation experiment (same day) let the first presenter capture the cascade for a whole 512-cycle gasket stall and the convoy starved the ACMP walker's responses until its single-FSM front-end ate every other inbound command - withdrawn on a desk bisect; the known bounded deviation (gsel may re-evaluate under a stalled presentation, every in-tree consumer latches on accept only) is documented at the mux, and the watchdog also arms on a PRESENTED-but-refused beat so a between-frames CDC-full wedge still reports. NEW REGISTER: A_TXARB_DIAG 0x784 RO live {tag 0xA7, stall-sticky[7:0], abort-sticky[7:0], locked[7:0]}, lane order LSB-first 0 aecp_acmp / 1 ctl_tx / 2 srp_ctl / 3 lstn_ctl / 4 maap_ctl / 5 aaf_final / 6 crf_dp / 7 adp_tx (the MAC boundary mux). WEDGE CONTEXT, silicon 2026-07-29 asl-m001c: ALL TX dead ~40 s after SRP enable - lwSRP sent frozen at 92, kernel tx_packets frozen at 136 across ping bursts, ADP silent, AECP timing out, STAT_TX_FIFO_GOOD_FRAME frozen at 0x3CC5 - while every RX lane climbed; at 0x001A LINK_CTRL[1]'s macsys reinit reached NEITHER the datapath muxes NOR the milan_cd<->sys CDCs; this release closes BOTH holes - recovery lives IN the lock (per-mux watchdogs, windows STAGGERED 2^15/2^16/2^17 shortest-upstream so a cascade starvation fires only at its true origin and one close beat, not six runts, egresses), and mac_tx_cdc/mac_rx_cdc move into reinit-scoped shadow domains (macsys gains an AsyncResetSynchronizer release, new macdp extends the datapath-side domain) so LINK_CTRL[1] now resets BOTH SIDES of BOTH crossings (safe only because reinit is held ~21 ms - the KL_link_guard SETTLE - while the reset_less gray-pointer synchronizers converge); the sticky lanes are the H1(CDC-full)-vs-H2(arbiter-lock) verdict the forensics lacked. SAME RELEASE: the LiteX builds gain create_clock period constraints + single-group asynchronous clock-groups (emitted via additional_xdc_commands, AFTER the finalize-time create_clock lines) for the PHY eth_rx/eth_tx domains - internal endpoints only, pad input/output-delay constraints remain future work (the Arty XDC held exactly ONE create_clock - clk100 - leaving 328 Ethernet-interface endpoints UNTIMED in every bitstream ever shipped, a placement lottery that voids every past 'STA-clean' claim about the MAC edge). PRIOR: 0x001A = THE HIVE FIELD ROUND (2026-07-29, five desk lanes off one bench session): (1) STREAM_INPUT GET_COUNTERS serves the 1722.1-2021 twelve - TIMESTAMP_VALID/NOT_VALID as per-context FLOPS counted at the accept verdict (a 12th serial-RMW walk step delayed verdicts enough to drop back-to-back frames at the depacketizer commit; flops cost zero walk cycles), mask 0xF3F -> 0xFFF, TV+TNV == FRAMES_RX, mirror slices 10/11 + virtual LCTX w26/w27; (2) the CRF Media Clock Input answers the Milan-mandatory ten behind 0xF3F straight from KL_crf_rx's counters instead of the truthful-but-badge-killing empty mask (la_avdecc removes CompatibilityFlag::Milan on ANY input's missing mandatory mask - 5.3.8.10 'for EACH Stream Input' has no CRF exemption); (3) SET/GET_MAX_TRANSIT_TIME is PER STREAM_OUTPUT (pres register file in the response builder, per-talker transit vector to the packetizer, the CRF output owns entry N_STREAMS; the RX monitor's pres_ofs stays entry 0 = the LISTENER-side window, deliberately not conflated); (4) an MVRP LeaveAll no longer ages MSRP registrations - the lwSRP walker's leaveall pulse is split per MRP application (802.1Q 10.7.1/10.7.9: LeaveAll scope is one Participant), killing the silicon licence flap (STREAM_START=16/STOP=15 behind a gap-free wire); (5) Milan 5.5.3.5.43 implicit-rebind exactness - a same-talker rebind refreshing STREAMING_WAIT never tears the stream, stale ACMP status and stale dmac/vlan are cleared into the new probe window; (6) the pcm-dma bank publishes the geometry capability word at +0x1c ({0x4D, stride0=driver-programmed, T=0, L=N_STREAMS}) so snd-kl-milan binds L>1 shapes. PRIOR: 0x0019 = SAVED BINDS SURVIVE A REBOOT: the persistence-journal ingest group 0x7B8-0x7C4 is WIRED (saved-state fast-connect E3). Milan v1.2 5.3.8.2 verbatim: 'The current bound state shall be saved in a non-volatile memory and restored after a power cycle', and 5.3.8.3 names the four binding parameters (talker entity id, source index, controller entity id, started/stopped) - exactly one KL_persist_journal record. Software lifts one flash slot image VERBATIM through A_JNL_DATA between A_JNL_CTRL start and end strobes; the engine verifies magic 'KLJ1' / format / shape / OWNING ENTITY / CRC-32 - the CRC is the LAST word of the image, so a torn, foreign or stale (SEQ-non-monotonic) image yields ZERO restores and a half-applied listener context table is not representable - and only then replays Milan 5.5.3.5.2 entry records through the E1 bind-restore port (PRB_W_AVAIL/PASSIVE, SRP params CLEARED per 5.5.2.6 step 1: sid/dmac/vlan are re-probed, never restored). The E1 0x7A0 direct path and the journal SHARE the restore port with journal-wins arbitration and owner-routed acks; both are boot-software-sequenced. The executable spec of the group is tb/verilator/persist/persist_wrap.sv, and tb/verilator/persist proves torn/foreign/stale rejection whole. NEW REGISTERS: A_JNL_CTRL 0x7B8 (W1S [0] start [1] end [2] abort; R = {stat[31:30],0}), A_JNL_DATA 0x7BC (write-only image word), A_JNL_STAT 0x7C0 (RO live), A_JNL_SEQ 0x7C4 (RO live watermark). SAME RELEASE, no ABI change of their own: Milan 5.4.2.25 GET_COUNTERS became PER-INDEX in both directions (KL_talker_diag_ctx = Table 5.4 with real interval + reset-on-start semantics incl the previously-never-served TIMESTAMP_UNCERTAIN; the RX monitor's all-context mirror serves every AAF sink's Table 5.6 set - sink 1 used to answer a full mask over constant zeros), the 5.3.7.3 silence fill (KL_pair_zero_fill - a BOUND talker always frames, silence where no source feeds it), the 8.3b Arty TDM8+I2S blend (KL_pair_blend), and the TSpec now derives from the WIRE constant (802.1Q 35.2.2.8.4 a: the frame the talker WILL PRODUCE). PRIOR: 0x0018 = AAF_CTRL RESET IS 0x0002_0000, i.e. the gate bypass is OFF at power-on. AAF_CTRL[1] is cfg_aaf_bypass and it ORs past BOTH qualifying terms of the AAF admission gate (acmp_talker_active AND the lwSRP stream gate), so with it set the talker streams whether or not any Listener Ready is registered - and its reset value was 1, making unconditional streaming the POWER-ON DEFAULT. Milan v1.2 5.3.7.3 conditions streaming on 'declaring a Talker Advertise attribute AND RECEIVING a Listener Ready or Listener Ready Failed attribute'; only its second sentence (STREAMING_WAIT shall not be implemented) is unconditional, and this repo's own traceability had flattened the whole clause into an unconditional 'a Stream Output SHALL NOT be stopped' - the paraphrase that licensed the bypass. Measured on silicon 2026-07-28 via an inline tap per board link: bypass set with nothing bound = 15,503 tagged AAF frames in 6 s from an unregistered stream, cleared = 0, bound = 18,012 (gating costs a bound stream nothing); MSRP TalkerAdvertise/Domain continue either way so 5.3.7.2 stays satisfied. Software that wants the legacy bring-up behaviour must now ASK for it. PRIOR: value returned by the read-only VERSION register ([31:16] major, [15:0] minor); 0x0017 = the CHANNEL-MAP RAMs ARE READABLE. CHMAP_WORD 0x908 always read back milan_csr's OWN SHADOW of the last word software wrote, never the RAM, and both map RAMs' read ports were tied off in milan_datapath (`map_rd_en_i = 1'b0`, `map_rd_data_o ()`), so NOTHING about the deployed channel map was observable from software - a slot emitting 24'd0 is bit-identical whether it is mapped-and-quiet or not connected at all, which is exactly the structural zero methodology R5 forbids. NEW REGISTERS: CHMAP_SNAP 0x910 (W1S [0] arm a readback of the entry named by CHMAP_SEL; R busy/valid/timeout/unsupported/armed + the CHMAP_RDBK_P capability in [9:8] + the latched {side,index} + a CONSTANT 0xC5 tag in [31:24] so a read of 0 means "this gateware predates the register", the 0x7A0 feature-probe pattern) and CHMAP_LOOP 0x914 (RO: the fabric's map word, [16] mapped, [17] fed, [18] LOOP_SUSPECT = mapped & ~fed - a slot advertised in the map that no audio has ever reached). THE UNARMED STATE IS POISON, NOT ZERO: CHMAP_LOOP reads 0xDEADDEAD until a snapshot completes, and reverts to 0xDEADDEAD if one times out or is refused, so the "reads 0 until SNAP is armed" trap of the 0x800 window is NOT reproduced here. NEW PARAMETER CHMAP_RDBK_P (default 0 = no readback port in this build) is the declaration, and the watchdog is what holds it accountable: a build that claims the capability and does not answer within 15 clocks sets CHMAP_SNAP[2] timeout and poisons the data word rather than latching whatever the bus happened to hold. 0x0016 = the AVTP "tu" (timestamp uncertain) bit is DRIVEN, and the 0x778 clock-validity group exists to drive it. Until this version every talker in the fabric stamped tu = 0 unconditionally - measured on 2026-07-27 streaming 31 M AAF frames from a PHC 216,446 s out of the gPTP domain while telling the listener the timestamps were fine (docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md). Milan v1.2 5.3.7.3 forbids stopping the Stream Output and IEEE 1722-2016 7.5 forbids tv = 0 on AAF at sp = 0, so tu is the ONLY conformant lever, and Milan v1.2 4.3.5.2 makes setting it a shall. NEW REGISTERS: CLKV_CTRL 0x778 RW ([0] SYNC_OK, [1] W1S discontinuity report, [15:4] lease in quarter-seconds; reset 0x00000080 = lease 2 s with SYNC_OK CLEAR), CLKV_STAT 0x77C RO live, CLKV_TUCNT 0x780 RO live (Milan Table 5.4 TIMESTAMP_UNCERTAIN, one count per 1 s observation interval in which tu was set). BEHAVIOUR CHANGE ON EVERY BOARD: the reset state is tu = 1, so a build whose software never writes CLKV_CTRL emits tu = 1 on every AAF and CRF frame - that is deliberate, unknown clock state means NOT valid, and the fix is for the gPTP daemon to lease the claim (the gptp2csr.sh pattern), not for the fabric to assume it. 0x0015 = the ADP SHAPE REGISTERS ARE READ-ONLY. ADP_TALKER (0x618) and ADP_LISTENER (0x61C) used to be plain RW words resetting to ZERO, so the entity's advertised talker_stream_sources / listener_stream_sinks came from a hand-typed boot script. On silicon 2026-07-27 the 8x8 AX7101 advertised 1 source / 2 sinks - the numbers that were true when the script was written at 1x1 - next to a reference device advertising 4/10 and a peer host advertising 8/8, so every controller on the segment, including a validated one, could see and bind exactly ONE of its eight streams, and the CRF Media Clock Output at talker_unique_id = N_STREAMS was outside the advertised range and therefore invisible even though its PDUs were on the wire every 2 ms. A stream count is a physical fact about the built gateware - software cannot create a ninth stream engine by writing a register - so a writable count buys nothing and buys a way for the device to LIE about itself, invisibly, because the register faithfully holds what was written. Both words are now RO and SOFTWARE-DEFINED IN THE DECLARATIVE SENSE: their values come from gen/adp_shape_defaults.svh, GENERATED from configs/endstation_*.yaml by sw/builder/endstation_builder.py in the same pass that emits the AEM descriptor ROM, exactly like the 0x680 lwSRP words come from gen/lwsrp_csr_defaults.svh. 0x618 = {ADP_TALKER_CAPS_C, ADP_TALKER_SRC_C}, 0x61C = {ADP_LISTENER_CAPS_C, ADP_LISTENER_SINK_C}. There is no parameter and no register: the config is the single definition of how many streams this entity HAS, and it drives the gateware, the AEM model and lwSRP alike. milan_datapath `include-s the SAME file and sizes its ACMP talker/listener context arrays from those constants (ACMP_SRC_C = ADP_TALKER_SRC_C, ACMP_SINKS_C = ADP_LISTENER_SINK_C), so the advertised range IS the addressable range IS the descriptor set - a gateware cannot be handed another shape's entity definition and still elaborate. Writes are silently ignored (the shadow is not armed for them) exactly like CAP and VERSION. The listener context count ALSO changes: it was max(N_STREAMS, 2), which reserved the pinned CRF sink only up to N = 2 and then silently dropped it, so a 4x4 or 8x8 build had N sinks where its own AEM model declares N + 1 (N AAF + CRF); the config now says N + 1 directly. talker_capabilities loses MEDIA_CLOCK_SOURCE at 1x1 (0x4801 -> 0x4001): that config has no CRF STREAM_OUTPUT, so the bit was never backed. scripts/check_entity_shape.py is the gate - it asserts config -> generated svh -> CSR -> AEM descriptor counts all agree, for every config, and that the tracked entity definition names the config it came from; 0x0014 = FIVE egress queues, compactly renumbered. The 0x0013 six-queue map DID NOT FIT the xc7a200t: three Vivado seeds failed placement identically at 11955 slices required against 11673 available (282 short) with LUTs at 99.84 % of capacity and flip-flops at 42 %, so the constraint was combinational area, not state. The queue that went is the one that carried no traffic - q1, the deliberate spare. Every other class keeps its rank, its shaping and its bandwidth share; only the indices shift down: q4 CBS SR class A, q3 CBS SR class B, q2 gPTP, q1 MAAP/MSRP/MVRP + 1722.1 ADP/ACMP/AECP, q0 best effort. gPTP still sits BELOW both shaped classes (802.1Q credit accounting assumes the shaped queues top the strict-priority order) and ALL queues still power up UNSHAPED (CBS_EN_RST = 5'b00000). The CBS window at 0x400 now runs to 0x49F (was 0x4BF) and 0x4A0 reads 0; CAP.num_queues reads 5; the reset idleSlopes are 25/50/50/150/450 Mb/s = 725 Mb/s = 72.5 %, under the 75 % REQ-CBS-03 ceiling, with the dropped spare's 2.5 % deliberately left unallocated rather than reassigned; CLS_TC_QUEUE_MAP still packs 3 bits per traffic class ($clog2(5) = 3) and resets to 0x004898C0 (TC0/1 -> q0, TC2 -> q3, TC3 -> q4, TC4/5 -> q1, TC6/7 -> q2); LWSRP_CTRL[4:2] keeps its width and its reset drops from 5 to 4 so the granted class-A slope still muxes into the top queue. The out-of-range queue clamp in traffic_class_map is still load-bearing - 5 is not a power of two either, and axis_demux silently drops select >= M_COUNT. NOTE the recovery is an ESTIMATE, not a Vivado result: open synthesis puts it at -812..-1224 LUT / -590 FF / -3 BRAM / -3 DSP on milan_datapath = roughly 147..314 slices against the 282 required, so placement is UNPROVEN and the banked LPF_P=0 lever (428 LUT / 756 FF) may still be needed - see docs/reference/EGRESS_QUEUE_MAP.md; 0x0013 = RMON is ALIVE and self-declaring, plus saturating narrow counter views. New RO STATS_CAP (0x204) is the per-lane capability mask for the 0x210-0x230 STAT window: bit n = 1 means lane n has a real event source in this build, bit n = 0 means the lane is STRUCTURALLY silent and its zero is not a measurement - the distinction the tied-off i_mac_events erased (both boards read the whole group as zero for months while every TB passed). KL_mac_rmon_events synthesises the pulse vector at the SoC's MAC boundary from what a soft MAC actually exposes - the TX/RX frame AXIS handshakes, the per-frame bad-frame flag (FCS failure or runt) and the monotonic FCS/preamble error counts - so RX_ERROR_BAD_FCS, RX_ERROR_BAD_FRAME and RX_FIFO_BAD_FRAME now count on LiteEth builds alongside the two good-frame lanes the datapath already derived; TX_ERROR_UNDERFLOW, TX_FIFO_OVERFLOW, TX_FIFO_BAD_FRAME and RX_FIFO_OVERFLOW stay MAC-internal and are declared unsupported in STATS_CAP rather than faked from AXIS backpressure. AVTPRX_STAT (0x6B8) and AVTPRX_ERR (0x6C0) now SATURATE their packed byte/half-word views of the 32-bit STREAM_INPUT counters instead of truncating (silicon 2026-07-26: SEQ_NUM_MISMATCH 51,523 was 79 % of the way to a 16-bit roll that would have counted DOWN); all-ones = "at least this many, read the full 32-bit value at A_STRMW_CNT 0x830 + 4*k", and every value below the ceiling is bit-identical to 0x0012; 0x0012 = the q2 CONTROL_CLASS row is IMPLEMENTED, and it is keyed on the DESTINATION MAC rather than on a PCP that these frames do not carry: MAAP, MSRP, MVRP and 1722.1 ADP/ACMP/AECP are untagged link-local control PDUs, so at the 0x0011 reset configuration (CLS_CTRL[0] use_pcp = 1) they fell through default_pcp into the ordinary tables and landed on BEST EFFORT - q2 was dead on the wire. traffic_class_map now carries a table of reserved control group addresses (01-80-C2-00-00-0E, 01-80-C2-00-00-21, 91-E0-F0-01-00-00, 91-E0-F0-00-FF-00) with NO EtherType precondition, so an untagged frame to any of them takes CONTROL_CLASS in BOTH classifier modes; the EtherType refines exactly one address - 01-80-C2-00-00-0E carries gPTP 0x88F7 (q3) AND MSRP 0x22EA (q2), and the gPTP arm wins the priority chain so the two do not collapse; AECP has no group address (it is addressed to the peer entity's individual MAC) so it is covered by the one EtherType-keyed arm, untagged 0x22F0 to a unicast destination; a TAGGED 0x22F0 is an AVTP stream and still rides the shaped SR queues. New CLS_CTRL[2] ctrl_class enables the fast path and RESETS TO 1 (CLS_CTRL reset value 0x1 -> 0x5); clearing it restores 0x0011 behaviour bit-for-bit. ETH_TYPE_MSRP/ETH_TYPE_MVRP and the four reserved addresses are new ethernet_packet_pkg constants; 0x0011 = SIX egress queues in 802.1Q order (higher index = higher priority): q5 CBS SR class A, q4 CBS SR class B, q3 gPTP, q2 MAAP/MSRP/MVRP + 1722.1 ADP/ACMP/AECP, q1 spare, q0 best effort. The CBS window at 0x400 therefore runs to 0x4BF (was 0x47F), CAP.num_queues reads 6, the CBS reset slopes are re-derived per queue (25/25/50/50/150/450 Mb/s, still summing to the 75 % REQ-CBS-03 ceiling; ALL queues still unshaped at reset per CBS_DEFAULT_SHAPING_BUG), CLS_TC_QUEUE_MAP packs 3 bits per traffic class and resets to 0x006D2B00 (TC0/1 -> q0, TC2 -> q4, TC3 -> q5, TC4/5 -> q2, TC6/7 -> q3) instead of the 2-bit identity 0xE4, and LWSRP_CTRL's class-A queue field WIDENS from [3:2] to [4:2] with reset 5 so the granted slope can mux into q5; 0x0010 = lwSRP attribute rows sized L+T-1 instead of max(L,T) - the 0x800 window maps listener k to ctx row k and talker t to ctx row (L-1)+t, so EVERY t>0 talker row sat above N_CTX_P and was refused, pinning those admission gates shut whenever lwSRP was enabled; out-of-range rows now read 0xDEAD at A_STRMW_SRP instead of aliasing row 0's live status and stream_id, LWSRP_STATUS[11] is the sticky shortfall flag, LWSRP_TSPEC (0x690) MaxFrameSize scopes to row 0 + listener rows while a talker row derives 24 + 24*C from its own TCTX w0 chans under the packetizer's clamp, and the CRF media clock output is a bindable ACMP talker source at talker_unique_id = N_STREAMS with CRFT_SID/CRFT_DMAC reset 0 meaning AUTO; the saved-state fast-connect journal RTL (KL_persist_journal, CSR group 0x7B8-0x7C4) is PRESENT IN THE TREE BUT NOT YET WIRED INTO milan_csr - see the REGISTER_MAP banner; 0x000F = fabric-listener blocker fix: the 0x800 window's sid staging is qualified by the index it was staged for (a CTRL commit only overrides the stream table when a sid was staged FOR THAT INDEX), and KL_stream_table treats an eviction carrying the ZERO sid as RELEASE-TO-ALIAS so entry 0 returns to the ACMP bound record at runtime instead of staying detached until reset; 0x000E = item-7 playback chain closed in fabric - the render crossbar gains a HOST-RING source (map entry src bit; KL_pcm_tx pair bus latched alongside the AVB stream-channels) and KL_i2s_feed_mux picks the DAC source AND its pace (48 kHz media tick for the crossbar, LPF masked there) so an ALSA playback ring reaches the line-out with no inbound stream, plus the PBK probe group 0x8C8-0x8D0 (delivered frames / disarmed-render frames / KL_pcm_tx rails); 0x000D = RX stream-parser probe group 0x8B4-0x8C4 (frames parsed / matched / last stream-subtype stream_id + subtype, match flag, index and the count of armed table entries) - the first view UPSTREAM of the stream-table match, for the fabric-listener accept blocker; 0x000C = N-context ACMP talker responder (probes answered per uid 0..N-1, dmac = MAAP base+uid), t>0 admission mirrors t0 term-by-term (per-stream ACMP term + cfg_aaf_bypass escape), talker-window honesty (idx>0 STATE bits [3:0] live, not-backed words read 0xDEADDEAD), LTAP same-cycle cascade; 0x000B = chmap64 follow-ups: AEM dynamic-map projector wired to the render map RAM (CHMAP64_AEM_BINDING.md; CSR 0x900 demoted to debug port), KL_pcm_tx as capture-mux ring source, per-stream wire_chans fan-out, tdm_dout exported; 0x000A = saved-state fast-connect enablers (SAVED_STATE_FASTCONNECT.md): E1 bind-restore group 0x7A0-0x7B4 (commit injects a Milan 5.5.3.5.2 PRB_W_AVAIL/PASSIVE record into the ACMP listener ctx table) + E2 window words 0x860/0x864/0x868 (per-context controller_entity_id + {flags incl. STREAMING_WAIT, tuid}); 0x0009 = P12 NxN integration: the 0x800 window is ENGINE-BACKED (LCTX/TCTX port-B reads return live context words, CFG writes provision the real engines + stream table/route; same map); 0x0008 = P11 indexed per-stream CSR window 0x800 (NXN_ARCHITECTURE.md §1.5: SEL/SNAP + 0x810-0x85C, legacy flat regs alias index 0); 0x0007 = robustness round (I2SPB_STAT W1C halves, STAT0-8 invalidate-on-MAC-reset, LINKG_STAT[2] eth_rst); 0x0006 = link guard (LINKG_STAT 0x774, LINK_CTRL[3:2]); 0x0005 = CRF talker CSRs 0x750+
)(
  input  wire                    aclk,           //! AXI-Lite clock (aclk / axis_clk domain)
  input  wire                    aresetn,        //! AXI-Lite active-low synchronous reset

  // ---- AXI4-Lite slave ----
  input  wire [ADDR_WIDTH-1:0]   s_axi_awaddr,   //! Write address (byte offset into the register window)
  input  wire                    s_axi_awvalid,  //! Write address valid
  output wire                    s_axi_awready,  //! Write address ready (combinational)
  input  wire [31:0]             s_axi_wdata,    //! Write data
  input  wire [3:0]              s_axi_wstrb,    //! Write byte strobes (ignored; full 32-bit writes only)
  input  wire                    s_axi_wvalid,   //! Write data valid
  output wire                    s_axi_wready,   //! Write data ready (combinational)
  output wire [1:0]              s_axi_bresp,    //! Write response (always OKAY)
  output wire                    s_axi_bvalid,   //! Write response valid
  input  wire                    s_axi_bready,   //! Write response ready
  input  wire [ADDR_WIDTH-1:0]   s_axi_araddr,   //! Read address (byte offset into the register window)
  input  wire                    s_axi_arvalid,  //! Read address valid
  output wire                    s_axi_arready,  //! Read address ready (combinational)
  output wire [31:0]             s_axi_rdata,    //! Read data
  output wire [1:0]              s_axi_rresp,    //! Read response (always OKAY)
  output wire                    s_axi_rvalid,   //! Read data valid
  input  wire                    s_axi_rready,   //! Read data ready

  // ---- MAC control / status (REQ-MAC-01..03) ----
  output wire                    o_mac_tx_en,    //! MAC transmit enable (MAC_CTRL[0])
  output wire                    o_mac_rx_en,    //! MAC receive enable (MAC_CTRL[1])
  output wire                    o_mac_promisc,  //! Promiscuous mode: accept all frames (MAC_CTRL[2])
  output wire                    o_mac_allmulti, //! Accept all multicast (MAC_CTRL[3])
  output wire                    o_mac_is_1g,    //! Link-rate select: 1 = 1 Gb/s, 0 = 100 Mb/s (from i_speed unless MAC_CTRL[5])
  output wire [7:0]              o_mac_ifg,      //! Inter-frame gap, bytes (MAC_IFG)
  output wire [47:0]             o_mac_addr,     //! Station MAC address {MAC_ADDR_HI[15:0], MAC_ADDR_LO}
  output wire [63:0]             o_mc_hash,      //! Multicast hash filter {MC_HASH_HI, MC_HASH_LO}
  output wire                    o_phy_reset_n,  //! PHY reset, active-low (PHY_RESET[0])
  input  wire                    i_link_up,      //! Link status from PHY/MAC (MAC_STATUS[0])
  input  wire [1:0]              i_speed,        //! Negotiated speed 0=10,1=100,2=1000 (MAC_STATUS[2:1])
  input  wire                    i_full_duplex,  //! Full-duplex indication (MAC_STATUS[3])

  // ---- Statistics / RMON (REQ-MAC-04) ----
  output wire                    o_stats_snapshot, //! 1-cycle pulse: latch live counters into the read window
  output wire                    o_stats_reset,    //! 1-cycle pulse: clear the external event counters
  input  wire [32*9-1:0]         i_stats,          //! Live RMON counters, packed {STAT8,...,STAT0}, 9x32b
  //! Per-lane CAPABILITY mask for the STAT window, published RO at 0x204
  //! (STATS_CAP). Bit n = 1: lane n at 0x210+4n has a real event source in
  //! this build. Bit n = 0: the lane is STRUCTURALLY silent - its zero is not
  //! a measurement. Without this, "0 errors" and "no counter" are the same
  //! read, which is exactly how the tied-off i_mac_events went unnoticed on
  //! silicon for months (docs/limitations/RECURRING_DEFECT_PATTERNS.md 1).
  input  wire [31:0]             i_stats_cap,

  // ---- 802.1Q classifier (REQ-CLS-01..04) ----
  output wire                    o_cls_use_pcp,      //! 1 = classify by PCP table, 0 = legacy EtherType (CLS_CTRL[0])
  output wire                    o_cls_dmac_check,   //! Enable reserved-DMAC validation (CLS_CTRL[1])
  output wire                    o_cls_ctrl_class,   //! Enable the untagged-control DMAC fast path (CLS_CTRL[2])
  output wire [2:0]              o_cls_default_pcp,  //! Default port priority for untagged frames (CLS_DEFAULT_PCP)
  output wire [23:0]             o_cls_pcp_tc_map,   //! Priority->traffic-class table, 8x3 bits (CLS_PCP_TC_MAP)
  output wire [23:0]             o_cls_prio_regen,   //! Priority regeneration table, 8x3 bits (CLS_PRIO_REGEN)
  output wire [31:0]             o_cls_tc_queue_map, //! Traffic-class->queue map (CLS_TC_QUEUE_MAP)

  // ---- 802.1Qav CBS, per queue, packed [q*32 +: 32] (REQ-CBS-01..03) ----
  output wire [32*NUM_QUEUES-1:0] o_cbs_idle_slope, //! Per-queue idleSlope, bits/s (CBS_IDLE_SLOPE)
  output wire [32*NUM_QUEUES-1:0] o_cbs_hi_credit,  //! Per-queue hiCredit, signed bytes (CBS_HI_CREDIT)
  output wire [32*NUM_QUEUES-1:0] o_cbs_lo_credit,  //! Per-queue loCredit, signed bytes (CBS_LO_CREDIT)
  output wire [NUM_QUEUES-1:0]    o_cbs_enable,     //! Per-queue shaped-enable; 0 = strict priority (CBS_CTRL[0])

  // ---- PTP hardware clock (REQ-PTP-01..04,06) ----
  output wire                    o_ptp_enable,      //! PTP counter enable (PTP_CTRL[0])
  output wire [31:0]             o_ptp_incr,        //! Nominal per-tick increment, ns.frac (PTP_INCR)
  output wire [31:0]             o_ptp_adj,         //! Signed adjfine addend added each tick (PTP_ADJ)
  output wire [63:0]             o_ptp_tod_wr,      //! settime target TOD {PTP_TOD_WR_HI, PTP_TOD_WR_LO}
  output wire [63:0]             o_ptp_offset,      //! adjtime signed delta {PTP_OFFSET_HI, PTP_OFFSET_LO}
  output wire                    o_ptp_cmd_load,    //! settime apply strobe (1-cycle pulse, PTP_CMD[0])
  output wire                    o_ptp_cmd_adjust,  //! adjtime apply strobe (1-cycle pulse, PTP_CMD[1])
  output wire                    o_ptp_cmd_snapshot,//! gettime latch strobe (1-cycle pulse, PTP_CMD[2])
  output wire [31:0]             o_ptp_ingress_lat, //! Ingress latency correction, ns (PTP_INGRESS_LAT)
  output wire [31:0]             o_ptp_egress_lat,  //! Egress latency correction, ns (PTP_EGRESS_LAT)
  input  wire [63:0]             i_ptp_tod,         //! gettime snapshot value from the PHC (gtx_clk, synchronised)
  input  wire                    i_ptp_tod_valid,   //! 1-cycle pulse: latch i_ptp_tod into PTP_TOD_RD (REQ-PTP-03/CSR-03)

  // ---- ADP advertiser identity/control (IEEE 1722.1 / Milan v1.2, FR-DISC-*) ----
  output wire                    o_adp_enable,        //! ADP advertising enable (ADP_CTRL[0])
  output wire [4:0]              o_adp_valid_time,    //! ADP valid_time, units of 2 s (ADP_CTRL[12:8])
  output wire [63:0]             o_adp_entity_id,     //! Entity ID (EUI-64) {ADP_EID_HI, ADP_EID_LO}
  output wire [63:0]             o_adp_entity_model_id, //! Entity model ID (EUI-64) {ADP_MID_HI, ADP_MID_LO}
  output wire [31:0]             o_adp_entity_caps,   //! entity_capabilities (ADP_ECAPS)
  output wire [15:0]             o_adp_talker_sources,//! talker_stream_sources (ADP_TALK[15:0], RO = ADP_TALKER_SRC_C, from the config)
  output wire [15:0]             o_adp_talker_caps,   //! talker_capabilities (ADP_TALK[31:16], RO = ADP_TALKER_CAPS_C, from the config)
  output wire [15:0]             o_adp_listener_sinks,//! listener_stream_sinks (ADP_LIST[15:0], RO = ADP_LISTENER_SINK_C, from the config)
  output wire [15:0]             o_adp_listener_caps, //! listener_capabilities (ADP_LIST[31:16], RO = ADP_LISTENER_CAPS_C, from the config)
  output wire [31:0]             o_adp_controller_caps, //! controller_capabilities (ADP_CCAPS)
  output wire [63:0]             o_adp_gptp_gm,       //! gptp_grandmaster_id {ADP_GM_HI, ADP_GM_LO}
  output wire [31:0]             o_gptp_pdelay_ns,    //! measured propagation delay ns (GPTP_PDELAY)
  input  wire [31:0]             i_acmpl_dbg,         //! listener walker forensics (RO 0x6E8)
  input  wire [31:0]             i_avtprx_tsd,        //! last accepted ts_delta (RO 0x6EC)
  input  wire [31:0]             i_i2spb_dbg,         //! DAC serial forensics (RO 0x6F0)
  //! gh #59 departing-controller detection (Milan v1.2 §5.4.5.3), RO 0x6F4:
  //! {evictions[31:24], CONTROLLER_AVAILABLE replies seen[23:12],
  //!  CONTROLLER_AVAILABLE probes sent[11:0]} — three free-running wrapping
  //! tallies, no state field (the two that climb fastest get 12 bits each)
  input  wire [31:0]             i_ctlr_diag,
  output wire [7:0]              o_adp_gptp_domain,   //! gptp_domain_number (ADP_DOMAIN[7:0])
  output wire [15:0]             o_adp_current_config,//! current_configuration_index (ADP_IDX0[15:0])
  output wire [15:0]             o_adp_identify_index,//! identify_control_index (ADP_IDX0[31:16])
  output wire [15:0]             o_adp_interface_index, //! interface_index (ADP_IDX1[15:0])
  output wire [63:0]             o_adp_association_id,//! association_id {ADP_ASSOC_HI, ADP_ASSOC_LO}
  output wire                    o_adp_advertise_p,   //! 1-cycle: advertise now + bump available_index (ADP_CMD[0])
  output wire                    o_adp_depart_p,      //! 1-cycle: send ENTITY_DEPARTING (ADP_CMD[1])
  input  wire [7:0]              i_adp_depart_cnt,    //! DIAG: depart events taken (A_ADP_DIAG[7:0])
  input  wire [7:0]              i_adp_rearm_cnt,     //! DIAG: dormancy self-re-arms (A_ADP_DIAG[15:8])
  input  wire [1:0]              i_adp_depart_src,    //! DIAG: last depart cause {shutdown, link_down} (A_ADP_DIAG[17:16])
  input  wire [31:0]             i_adp_available_index, //! current available_index from the advertiser (ADP_STATUS)
  input  wire [7:0]              i_adp_sent_cnt,      //! DIAG2: ADPDUs egressed (A_ADP_DIAG2[7:0])
  input  wire [7:0]              i_adp_disc_rx_cnt,   //! DIAG2: ENTITY_DISCOVERs accepted for us (A_ADP_DIAG2[15:8])
  input  wire                    i_adp_disc_seen_p,   //! DIAG2: 1-cycle, any ENTITY_DISCOVER on the wire -> counted at A_ADP_DIAG2[23:16]
  input  wire [3:0]              i_adp_last_msg,      //! DIAG2: message_type of the last ADPDU sent (A_ADP_DIAG2[27:24])
  input  wire [3:0]              i_adp_state,         //! DIAG2: {send_pending, busy, disc_pend, available} (A_ADP_DIAG2[31:28])
  //! AECP/AEM listener status (KL_aecp_top) — read-only, 0x648/0x64C
  input  wire                    i_aecp_locked,         //! entity is LOCK_ENTITY-locked
  input  wire [15:0]             i_aecp_current_config, //! live current_configuration_index
  input  wire [15:0]             i_aecp_cmd_count,      //! AECP commands accepted
  input  wire [15:0]             i_aecp_resp_count,     //! AECP responses sent
  input  wire [15:0]             i_acmp_cmd_count,      //! ACMP commands accepted (0x650)
  input  wire [15:0]             i_acmp_resp_count,     //! ACMP responses sent (0x650)
  output wire                    o_aaf_enable,          //! AAF talker enable (AAF_CTRL[0])
  output wire                    o_aaf_bypass,          //! AAF gate bypass (AAF_CTRL[1]) — 1 = stream whenever enabled (legacy); 0 = Milan probe-gated
  output wire [47:0]             o_aaf_dest_mac,        //! AAF stream DMAC {DMHI[15:0],DMLO}
  output wire [11:0]             o_aaf_vid,             //! AAF SR VID (AAF_CTRL[27:16])
  output wire                    o_acmp_lobs,           //! listener_observed override (A_ACMP_LOBS[0], the lwSRP socket)
  input  wire                    i_acmp_probe_armed,    //! ACMP probe SM state (A_ACMP_TALKER RO)
  input  wire                    i_acmp_talker_active,
  //! per-stream talker truth vectors (2026-07-26 window honesty: the
  //! talker-dir SNAP STATE bits [3:0] at idx>0 were hardwired 0 while
  //! REGISTER_MAP documented them live - silicon-found). Zero-padded to 8
  //! by the datapath (8'(vec)); bit j = talker stream j.
  input  wire [7:0]              i_tlk_gate_v,          //! composed admission (aaf_stream_en)
  input  wire [7:0]              i_tlk_active_v,        //! ACMP talker_active per stream
  input  wire [7:0]              i_tlk_probe_v,         //! probe window open per stream
  input  wire [7:0]              i_tlk_lobs_v,          //! listener observed per stream
  input  wire                    i_aaf_gate,            //! resolved AAF gate
  input  wire [31:0]             i_aaf_frames,          //! AAF frames sent (RO, 0x660)
  input  wire [31:0]             i_aaf_pairs,           //! AAF I2S pairs captured (RO, 0x664)

  // ---- lwSRP engine (0x680 group, docs/LWSRP_FPGA_ARCHITECTURE.md) ----
  output wire                    o_lwsrp_enable,        //! LWSRP_CTRL[0] engine enable
  output wire                    o_lwsrp_talker_en,     //! LWSRP_CTRL[1] TalkerAdvertise declare
  output wire [2:0]              o_lwsrp_qidx,          //! LWSRP_CTRL[4:2] class-A queue (slope MUX target); 3 bits since the 802.1Q-order map put class A on the TOP queue (q4 at N=5)
  output wire                    o_lwsrp_decl_bypass,   //! LWSRP_CTRL[5] declare-always bypass (reset 0: Milan 4.3.3.1 gates the TalkerAdvertise)
  output wire [11:0]             o_lwsrp_vid,           //! LWSRP_VID[11:0] SR VID
  output wire [47:0]             o_lwsrp_dest_mac,      //! stream DMAC {DMHI[15:0], DMLO}
  output wire [15:0]             o_lwsrp_max_frame,     //! LWSRP_TSPEC[15:0] MaxFrameSize
  output wire [15:0]             o_lwsrp_interval,      //! LWSRP_TSPEC[31:16] MaxIntervalFrames
  output wire [31:0]             o_lwsrp_latency,       //! LWSRP_LATENCY AccumulatedLatency (ns)
  input  wire [31:0]             i_lwsrp_dom,           //! LWSRP_DOM 0x788: {7'0, adopt_valid, op_prio[7:0], 4'0, op_vid[11:0]} (Milan 4.2.7.2.1)
  input  wire [31:0]             i_lwsrp_status,        //! packed engine status (RO 0x694)
  input  wire [31:0]             i_lwsrp_slope,         //! granted idleSlope bps (RO 0x698)
  input  wire [31:0]             i_lwsrp_cnt,           //! {rx_pdus[31:16], tx_pdus[15:0]} (RO 0x69C)

  // ---- ACMP listener SM (0x6A4 group, Milan v1.2 §5.5 listener) ----
  input  wire [31:0]             i_acmpl_state,         //! packed SM status (RO 0x6A4)
  input  wire [31:0]             i_acmpl_talker_lo,     //! bound talker EID (RO 0x6A8)
  input  wire [31:0]             i_acmpl_talker_hi,     //! (RO 0x6AC)
  input  wire [31:0]             i_acmpl_cnt,           //! {probes[31:16], cmds[15:0]} (RO 0x6B0)
  input  wire [31:0]             i_acmpl_tuid,          //! {fail_code[23:16], tuid[15:0]} (RO 0x6B4)
  input  wire [31:0]             i_avtprx_stat,         //! AVTP RX monitor status (RO 0x6B8)
  input  wire [31:0]             i_avtprx_frx,          //! STREAM_INPUT FRAMES_RX (RO 0x6BC)
  input  wire [31:0]             i_avtprx_err,          //! packed error counters (RO 0x6C0)
  //! FULL-WIDTH listener-context-0 STREAM_INPUT counters, Table 7-157 word
  //! order {FRAMES_RX, EARLY, LATE, UNSUPPORTED_FORMAT, TIMESTAMP_UNCERTAIN,
  //! MEDIA_RESET, SEQ_NUM_MISMATCH, STREAM_INTERRUPTED, MEDIA_UNLOCKED,
  //! MEDIA_LOCKED}, i.e. lane k at [k*32 +: 32]. The 0x800 window's index-0
  //! CNT words come from HERE, not from the packed 0x6B8/0x6C0 views: those
  //! are 8/16-bit summaries that SATURATE, so they can only ever be a floor
  //! (silicon 2026-07-26: SEQ_NUM_MISMATCH 51,523 was 79 % of the way to a
  //! 16-bit roll). This is the authoritative width - the widening the
  //! index-0 hard-alias branch below always promised.
  input  wire [32*10-1:0]        i_avtprx_cnt10,
  input  wire [31:0]             i_pcmrx_cnt,           //! {drops[31:16], pdus[15:0]} (RO 0x6C4)
  input  wire [31:0]             i_pcmrx_ts,            //! last accepted avtp_ts (RO 0x6C8)
  input  wire [31:0]             i_i2spb_stat,          //! {underruns, overruns} (RO/W1C 0x6D8)
  output wire                    o_i2spb_clr_under,     //! 1-cycle: W1C clear of the underrun rail
                                                        //! (write with any of [31:16] set)
  output wire                    o_i2spb_clr_over,      //! 1-cycle: W1C clear of the overrun rail
                                                        //! (write with any of [15:0] set)
  input  wire [31:0]             i_i2spb_trim,          //! {servo trim, fifo fill} (RO 0x6E0)
  input  wire [31:0]             i_maap_stat0,          //! {conflicts, defends, offset} (RO 0x6D0)
  input  wire [31:0]             i_maap_stat1,          //! {addr_valid, state} (RO 0x6D4)
  output wire                    o_maap_enable,         //! MAAP engine enable
  output wire                    o_maap_seed_valid,     //! first probe uses seed
  output wire [7:0]              o_maap_count,          //! block size (reset 8)
  output wire [15:0]             o_maap_seed_offset,    //! provisioning seed
  output wire                    o_tone_enable,
  output wire [2:0]              o_tone_att,          //! pilot-tone -6dB steps (TONE_CTRL[3:1])         //! 1 kHz 0 dBFS pilot tone

  // ---- RX dest-MAC TCAM filter programming (REQ-MAC-02) ----
  output wire                    o_sw_link,           //! LINK_CTRL[0]: daemon-tracked PHY link
  output wire                    o_mac_reinit,        //! LINK_CTRL[1]: MAC sys-side reset (recovery daemon)
  output wire [63:0]             o_entity_name8,      //! ENT_NAME chars 0-7 (board name overlay)
  output wire                    o_lpf_enable,
  output wire                    o_crf_en,            //! CRF sink enable (0x738)
  output wire [63:0]             o_crf_sid,           //! CRF stream_id (0x73C/0x740)
  input  wire [31:0]             i_crf_delta,         //! RO 0x744
  input  wire [31:0]             i_crf_rate,          //! RO 0x748
  input  wire [31:0]             i_crf_status,        //! RO 0x74C {pdu16,fmt8,seq8}
  input  wire                    i_crf_locked,        //! RO in 0x738 bit 31,        //! LPF_CTRL[0]: playback biquad
  input  wire [31:0]             i_mcsrv_stat,        //! RO 0x8F8: MMCM-DRP media-clock servo status
  output wire                    o_mcsrv_ps_invert,   //! MCSRV_CTRL 0x8FC[0]: PS direction flip
  output wire                    o_mcsrv_auto_repair, //! MCSRV_CTRL 0x8FC[1]: 1 = allow DRP divider repair (bench-gated, default 0)
  //! item-11 AAF per-stage latency taps (LTAP group, base 0x870)
  input  wire [16*32-1:0]        i_ltap_regs,         //! RO 0x874-0x8B0: 16 packed readback words (KL_aaf_latency_taps)
  input  wire [31:0]             i_ltap_status,       //! RO 0x870 status field (active/stage; enable OR-ed in here)
  output wire                    o_ltap_en,           //! LTAP_CTRL[1]: measurement enable (default 1)
  output wire                    o_ltap_clr,          //! LTAP_CTRL[0] W1S: 1-cycle stats clear
  //! RX stream-parser probe (APRB group, base 0x8B4) - the pre-match view
  input  wire [5*32-1:0]         i_aprb_regs,         //! RO 0x8B4-0x8C4: 5 packed readback words (avtp_stream_parser probe)

  //! item-7 playback chain probe (PBK group, base 0x8C8)
  input  wire [3*32-1:0]         i_pbk_regs,          //! RO 0x8C8-0x8D0: 3 packed readback words (host ring -> render -> DAC)
  //! chmap 0x900 window (docs/CHANNEL_MAP_64.md §6): render/capture map-RAM
  //! debug write port + fabric bypass arm. Default 0 = today's audio path.
  output wire                    o_chmap_enable,      //! CHMAP_CTRL 0x900[0]: DEBUG arm - routing lever on STATIC shapes only (0x002C: dynamic-map shapes route the crossbars by construction); always gates the 0x904 debug write window
  output wire                    o_chmap_wr_en,       //! one-cycle map-word write strobe (gated by CHMAP_CTRL[0])
  output wire                    o_chmap_wr_side,     //! CHMAP_SEL[8]: 0 = RMAP (render), 1 = CMAP (capture)
  output wire [5:0]              o_chmap_wr_addr,     //! CHMAP_SEL[5:0]: map entry index
  output wire [15:0]             o_chmap_wr_data,     //! CHMAP_WORD[15:0]: the §5 map word
  //! chmap map-RAM READBACK port (CHMAP_SNAP 0x910 / CHMAP_LOOP 0x914).
  //! LEVEL request, same shape as the LCTX/TCTX port-B contract above:
  //! o_chmap_rd_en is held with a stable o_chmap_rd_side/o_chmap_rd_addr
  //! until i_chmap_rd_valid, then dropped. The first busy cycle is a FLUSH
  //! (a valid still in flight for the PREVIOUS request is ignored) - the
  //! same stale-valid guard the 0x800 window needs. i_chmap_rd_data is the
  //! RAM's word as the fabric holds it; on the capture side (Lane 5's
  //! widening) it is {loop_fed[15], loop_mapped[14], 2'b0, entry[11:0]},
  //! on the render side {8'd0, entry[7:0]}. If the fabric does not answer
  //! within CHMAP_RD_WDOG_C clocks the request is abandoned and the data
  //! word POISONS - it never latches a bus value it did not see valid.
  output wire                    o_chmap_rd_en,       //! held readback request (level)
  output wire                    o_chmap_rd_side,     //! 0 = RMAP (render), 1 = CMAP (capture)
  output wire [5:0]              o_chmap_rd_addr,     //! map entry index
  input  wire [15:0]             i_chmap_rd_data,     //! RAM word (see contract)
  input  wire                    i_chmap_rd_valid,    //! rd_data is the answer
  output wire                    o_crft_en,           //! CRF talker enable (0x750)
  //! CRFT_CTRL[1]: make the CRF Media Clock Output a real SR class A stream
  //! (Milan v1.2 7.3.3) - provision its lwSRP Talker Advertise row AND tag
  //! its frames, in that order. ONE bit for BOTH because tagging without
  //! declaring is the pruned-to-zero state (802.1Q 35.1.2).
  output wire                    o_crft_class_a,
  output wire [63:0]             o_crft_sid,          //! CRF talker stream_id (0x754/0x758)
  output wire [47:0]             o_crft_dest_mac,     //! CRF talker DMAC (0x75C/0x760)
  input  wire [31:0]             i_crft_stat,         //! live 0x750[31:2] status
  input  wire [31:0]             i_crft_count,        //! RO 0x764: CRF PDUs emitted
  input  wire [31:0]             i_bdbg0,             //! RO 0x768-0x770: 0x4B scan forensics
  input  wire [31:0]             i_bdbg1,
  input  wire [31:0]             i_bdbg2,
  input  wire [31:0]             i_linkg_stat,        //! RO 0x774: link-guard status
  //! ---- 0x778 clock-validity group (KL_ptp_clock_validity) --------------
  //! The talker's AVTP "tu" verdict. sw_* is the daemon-published gPTP sync
  //! LEASE (reset = no lease = NOT synchronised, so an un-taught build says
  //! "uncertain" rather than claiming health it cannot prove).
  output wire                    o_clkv_wr_p,         //! 1-cycle: CLKV_CTRL was written (reloads the lease)
  output wire                    o_clkv_sync_ok,      //! CLKV_CTRL[0]: software asserts the PHC is disciplined
  output wire                    o_clkv_disc_p,       //! CLKV_CTRL[1] W1S: software reports a gPTP discontinuity
  output wire                    o_clkv_as_cap,       //! CLKV_CTRL[2]: daemon's 802.1AS-2020 10.2.5.1 asCapable
                                                      //! claim (gh #64 J3; leased in KL_ptp_clock_validity)
  output wire [11:0]             o_clkv_wdog_q,       //! CLKV_CTRL[15:4]: lease, quarter-seconds (0 = never trust)
  input  wire [31:0]             i_clkv_stat,         //! RO 0x77C: {as_cap, lease, hold, no_lease, sync_ok, tu}
  input  wire [31:0]             i_clkv_tucnt,        //! RO 0x780: Milan Table 5.4 TIMESTAMP_UNCERTAIN (talker)
  input  wire [31:0]             i_txarb_diag,        //! RO 0x784: TX-trunk arbiter lock supervision
                                                      //! {tag 0xA7, stall-sticky[7:0], abort-sticky[7:0], locked[7:0]}
  input  wire                    i_mac_reinit,        //! effective MAC-reset line (link guard |
                                                      //! LINK_CTRL[1]); its release invalidates
                                                      //! the STAT0-8 snapshot (stale-shadow fix)
  output wire                    o_linkg_dis,         //! LINK_CTRL[2]: 1 = link guard disabled
  output wire                    o_linkg_freeze,      //! LINK_CTRL[3]: test - fake eth clock death
  output wire [63:0]             o_as_parent_ckid,    //! AS2: 802.1AS parent bridge ckid
  output wire                    o_tcam_default_pass, //! accept frames that miss the TCAM (TCAM_CTRL[0])
  output wire                    o_tcam_addr_filt_en, //! apply the 802.3 station address filter on a TCAM miss (TCAM_CTRL[1], REQ-MAC-02)
  output wire                    o_tcam_wr_en,        //! 1-cycle: commit an entry write to the TCAM
  output wire [4:0]              o_tcam_wr_index,     //! entry index (TCAM_CMD[4:0])
  output wire                    o_tcam_wr_valid,     //! 1 = add/update, 0 = remove (TCAM_CMD[8])
  output wire [47:0]             o_tcam_wr_key,       //! match key {TCAM_KEY_HI[15:0], TCAM_KEY_LO}
  output wire [47:0]             o_tcam_wr_mask,      //! care mask {TCAM_MASK_HI[15:0], TCAM_MASK_LO}
  output wire [7:0]              o_tcam_wr_action,    //! action/tag (TCAM_ACTION[7:0])

  // ---- P11 indexed per-stream CSR window (0x800, NXN_ARCHITECTURE.md §1.5) ----
  //! LCTX context-RAM port B (KL_avtp_rx_monitor_ctx window port; NORMATIVE
  //! contract, P12 shape): the engine arbitrates its single explicit RAM
  //! read port (T2 rule: registered BRAM output, ONE read port, no CSR-side
  //! mux widening) and serves a window read only in fully-idle slots. The
  //! CSR holds o_lctx_rd_en with a stable o_lctx_rd_addr = {s[2:0],
  //! word[4:0]} and completes on i_lctx_rd_valid — but only AFTER a 4-cycle
  //! flush window (the P11 fixed timing constant, kept as the stale-valid
  //! guard: a valid pulse in flight for a PREVIOUS address dies within 2
  //! cycles of its request dropping/changing, so any valid seen after the
  //! flush carries the CURRENT address's word). i_lctx_rd_data is REQUIRED
  //! to hold its value from one valid pulse to the next (the engine's
  //! registered read-data output does). Writes: o_lctx_wr_p is a REQUEST
  //! held (with stable addr/data) until the engine accepts it with a
  //! same-cycle i_lctx_wr_rdy; while a request is pending the AXI write
  //! channel is held off (wr_fire gate) so a request is never clobbered.
  //! o_lctx_snap_req/i_lctx_snap_ok stay a level handshake; the P12 engine
  //! grants immediately (see milan_datapath: the engine serves each burst
  //! word only when fully event-drained, so every WORD is event-atomic and
  //! the burst is bounded by its start/end engine state).
  //! TBs without an engine tie {rd_data=0, rd_valid=1, wr_rdy=1, snap_ok=1}
  //! (window engine words read 0 at the P11 fixed latency).
  output wire                    o_lctx_rd_en,      //! port-B fetch (level)
  output wire [7:0]              o_lctx_rd_addr,    //! {s[2:0], word[4:0]}
  input  wire [31:0]             i_lctx_rd_data,    //! held word (see contract)
  input  wire                    i_lctx_rd_valid,   //! rd_data is the answer
  output wire                    o_lctx_snap_req,   //! coherent-burst request
  input  wire                    i_lctx_snap_ok,    //! engine grant (level)
  output wire                    o_lctx_wr_p,       //! CFG-word write request (w0..w4; held until wr_rdy)
  output wire [7:0]              o_lctx_wr_addr,    //! {s[2:0], word[4:0]}
  output wire [31:0]             o_lctx_wr_data,
  input  wire                    i_lctx_wr_rdy,     //! engine accepted this cycle
  //! TCTX context-RAM port B (KL_aaf_packetizer window port, same contract)
  output wire                    o_tctx_rd_en,
  output wire [6:0]              o_tctx_rd_addr,    //! {t[2:0], word[3:0]}
  input  wire [31:0]             i_tctx_rd_data,
  input  wire                    i_tctx_rd_valid,
  output wire                    o_tctx_snap_req,
  input  wire                    i_tctx_snap_ok,
  output wire                    o_tctx_wr_p,       //! CFG-word write request (w0..w2; held until wr_rdy)
  output wire [6:0]              o_tctx_wr_addr,
  output wire [31:0]             o_tctx_wr_data,
  input  wire                    i_tctx_wr_rdy,
  //! ACMP context-table request/grant (KL_acmp_lstn_ctx tbl_* shape, RO):
  //! req held until the 1-cycle gnt; i_acmp_tbl_ctx (acmp_lstn_ctx_t
  //! flattened, 317 b) is valid WITH gnt and latched here. Tie {gnt=0,
  //! ctx=0} while the single-sink listener is instantiated (dir=0
  //! SID/DMAC/STATE-acmp fields read 0 — index-0 STATE keeps its hard
  //! alias onto the flat 0x6A4/0x6B8 inputs).
  output wire                    o_acmp_tbl_req,
  output wire [3:0]              o_acmp_tbl_idx,
  input  wire                    i_acmp_tbl_gnt,
  input  wire [316:0]            i_acmp_tbl_ctx,
  //! ACMP bind-restore master (E1, SAVED_STATE_FASTCONNECT.md §5): a 0x7B4
  //! commit holds o_acmp_rest_req until the engine's 1-cycle
  //! i_acmp_rest_ack; i_acmp_rest_status is valid WITH the ack (0 =
  //! injected, 1 = target occupied, 2 = bad index). Tie {ack=0, status=0}
  //! with no engine attached: the commit then reads back busy forever —
  //! the honest no-engine behaviour (software must probe VERSION first).
  output wire                    o_acmp_rest_req,
  output wire [3:0]              o_acmp_rest_idx,
  output wire [63:0]             o_acmp_rest_talker,
  output wire [15:0]             o_acmp_rest_tuid,
  output wire [63:0]             o_acmp_rest_ctlr,
  output wire [15:0]             o_acmp_rest_flags,
  input  wire                    i_acmp_rest_ack,
  //! persistence-journal ingest (E3, 0x7B8-0x7C4): 1-cycle command strobes
  //! + the image word; stat/seq are the engine's live words
  output wire                    o_jnl_start,
  output wire                    o_jnl_wr,
  output wire [31:0]             o_jnl_data,
  output wire                    o_jnl_end,
  output wire                    o_jnl_abort,
  input  wire [31:0]             i_jnl_stat,
  input  wire [31:0]             i_jnl_seq,
  //! AEM dynamic-state patch port (E4, 0x7C8-0x7D4): the boot-time restore
  //! master for the AEM store. Same shape as the journal group next door —
  //! one held data word plus one-cycle command strobes. The engine refuses
  //! every one of them while the ADP advertiser is up, which is what makes
  //! "replay before you advertise" structural rather than procedural.
  output wire [31:0]             o_aemp_wdata,
  output wire                    o_aemp_sel_p,
  output wire                    o_aemp_field_p,
  output wire                    o_aemp_data_p,
  output wire                    o_aemp_commit_p,
  output wire                    o_aemp_abort_p,
  input  wire [31:0]             i_aemp_stat,
  input  wire [1:0]              i_acmp_rest_status,
  //! AS_PATH staging store (gh #64 J4, 0x7DC-0x7E4): the published
  //! 802.1AS PathTrace TAIL - slots 1..7 are the traversed bridges, slot 0
  //! is ALWAYS the grandmaster and is never stored here (it lives at
  //! ADP_GM 0x624/0x628; duplicating it is the derive-never-mirror class).
  //! o_asp_path bit [64*(k-1) +: 64] = slot k. count = 0 keeps the legacy
  //! two-entry [GM, parent] derivation in the response builder.
  output wire [7*64-1:0]         o_asp_path,          //! committed slots 1..7
  output wire [3:0]              o_asp_count,         //! published path length (entries incl the GM)
  output wire [3:0]              o_asp_gen,           //! publish generation (bumps per publish)
  //! lwSRP attribute-context provisioning port (KL_lwsrp_top ctx_* shape):
  //! window CTRL commits for idx>0 write a row (sid/dmac staged via the
  //! window SID/DMAC words, TSpec from the legacy 0x690/0x6A0 regs); reads
  //! poll the row status into the window SRP word. Row map: dir=0 -> row
  //! idx, dir=1 -> row N_LISTENERS_P-1+idx; idx 0 = legacy row 0 (RO,
  //! served by the flat 0x694 alias instead).
  output wire                    o_srp_ctx_req,
  output wire                    o_srp_ctx_we,
  output wire [4:0]              o_srp_ctx_idx,
  output wire                    o_srp_ctx_valid,
  output wire                    o_srp_ctx_dir,     //! ctx encoding: 0=talker,1=listener
  output wire [63:0]             o_srp_ctx_sid,
  output wire [47:0]             o_srp_ctx_dmac,
  output wire [7:0]              o_srp_ctx_prio_rank,
  output wire [15:0]             o_srp_ctx_max_frame,
  output wire [15:0]             o_srp_ctx_interval,
  output wire [31:0]             o_srp_ctx_latency,
  input  wire                    i_srp_ctx_gnt,
  //! ANOTHER master took the shared lwSRP ctx port for one service beat (the
  //! fabric's CRF Media Clock Output row). That beat overwrites the engine's
  //! ctx_rd_* snapshot registers with a row THIS window did not select, so
  //! the snapshot must be declared stale: the window then reads 0 ("not
  //! sampled yet", the existing srp_fresh_r contract) until its continuous
  //! poll refills it on the next beat, instead of returning another row's
  //! stream_id as if it were the selected one.
  input  wire                    i_srp_ctx_stolen,
  input  wire [63:0]             i_srp_ctx_rd_sid,
  input  wire [15:0]             i_srp_ctx_rd_stat, //! {valid,dir,declared,reg,ready,failed,decl[1:0],code[7:0]}

  // ---- protocol-processor control plane (0x920 window) ----
  //! Control levels out to KL_pp_shadow.
  output wire                    o_pp_enable,       //! PP_CTRL[0]: Milan 5.6.1 boot gate for the shadow
  output wire                    o_pp_restore_go,   //! PP_CTRL[1]: start the NVM boot-restore walk
  //! Side-port bridge: one outstanding access, ARM -> poll busy -> read, the
  //! 0x800/0x910 window discipline (an AXI read must never wait on a fabric
  //! walk, so the access is posted and its result latched).
  output wire                    o_pp_req,          //! single-cycle request strobe
  output wire                    o_pp_we,           //! 1 = write
  output wire [19:0]             o_pp_addr,         //! 20-bit side-port WORD address
  output wire [31:0]             o_pp_wdata,        //! write data
  input  wire [31:0]             i_pp_rdata,        //! read data, valid with ack
  input  wire                    i_pp_ack,          //! completion strobe
  input  wire                    i_pp_err,          //! access refused (with ack)
  //! Shadow observability (see KL_pp_shadow's banner for what each proves).
  input  wire                    i_pp_restore_busy,
  input  wire                    i_pp_restore_done,
  input  wire                    i_pp_restore_fail,
  //! CONSTANT from the fabric: 1 = persistent media behind the processor's NVM
  //! device face, 0 = none in this build. Without it, restore_done cannot be
  //! read as a verdict, because a walk over an absent backend sets exactly the
  //! bits a walk over real media sets.
  input  wire                    i_pp_nvm_backed,
  //! the completed walk validated ZERO records (blank or unframed media)
  input  wire                    i_pp_nvm_blank,
  input  wire                    i_pp_nvm_alarm,
  input  wire [15:0]             i_pp_rx_frames,    //! control frames handed to the PP
  input  wire [7:0]              i_pp_rx_drops,     //! frames lost to a full FIFO
  input  wire [15:0]             i_pp_tx_frames,    //! frames the PP WOULD have sent

  // ---- Interrupt (REQ-CSR-04) ----
  input  wire                    i_evt_tx_ts_ready,   //! Event: TX egress timestamp available (sets IRQ_STATUS[0])
  input  wire                    i_evt_link_change,   //! Event: link/speed change (sets IRQ_STATUS[1])
  input  wire                    i_evt_rmon_rollover, //! Event: RMON counter rollover (sets IRQ_STATUS[2])
  output wire                    o_eth_guard,         //! ETH GUARD (0x7D8): 1 = CPU eth-disruption levers refused (also gates phy_crg in the SoC)
  output wire                    o_irq                //! Level interrupt to PS = |(IRQ_STATUS & IRQ_MASK)
);

  // ==========================================================================
  //  Local parameters
  // ==========================================================================
  localparam int NS = 9;                         //! Number of RMON statistics counters
  localparam int QW = (NUM_QUEUES <= 1) ? 1 : $clog2(NUM_QUEUES); //! Queue-index width

  // --------------------------------------------------------------------------
  //  Register byte offsets (single HDL source of the map; see docs/reference/REGISTER_MAP.md)
  //
  //    0x000 ID          0x100 MAC_CTRL     0x300 CLS_CTRL     0x500 PTP_CTRL
  //    0x004 VERSION     0x104 MAC_IFG      0x304 CLS_DEF_PCP  0x504 PTP_INCR
  //    0x008 CAP         0x108 MAC_ADDR_LO  0x308 CLS_PCP_TC   0x508 PTP_ADJ
  //    0x00C SCRATCH     0x10C MAC_ADDR_HI  0x30C CLS_REGEN    0x510 PTP_TOD_WR_LO
  //    0x010 IRQ_STATUS  0x110 MAC_STATUS   0x310 CLS_TC_QUEUE 0x514 PTP_TOD_WR_HI
  //    0x014 IRQ_MASK    0x114 MC_HASH_LO                      0x518 PTP_OFFSET_LO
  //    0x018 IRQ_RAW     0x118 MC_HASH_HI   0x400+q*0x20 CBS:  0x51C PTP_OFFSET_HI
  //                      0x11C PHY_RESET      +0x00 IDLE_SLOPE 0x520 PTP_CMD
  //    0x200 STATS_CTRL  0x204 STATS_CAP      +0x04 HI_CREDIT  0x530 PTP_TOD_RD_LO
  //    0x210..0x230 STAT0..STAT8              +0x08 LO_CREDIT  0x534 PTP_TOD_RD_HI
  //                                           +0x0C CTRL       0x540 PTP_INGRESS_LAT
  //                                                            0x544 PTP_EGRESS_LAT
  // --------------------------------------------------------------------------
  localparam [ADDR_WIDTH-1:0]
    A_ID          = 'h000, A_VERSION = 'h004, A_CAP     = 'h008, A_SCRATCH  = 'h00C,
    A_IRQ_STATUS  = 'h010, A_IRQ_MASK= 'h014, A_IRQ_RAW = 'h018,
    A_MAC_CTRL    = 'h100, A_MAC_IFG = 'h104, A_MAC_ALO = 'h108, A_MAC_AHI  = 'h10C,
    A_MAC_STATUS  = 'h110, A_MC_LO   = 'h114, A_MC_HI   = 'h118, A_PHY_RST  = 'h11C,
    A_STATS_CTRL  = 'h200, A_STATS_CAP = 'h204,   //! RO: which STAT lanes are real
    A_CLS_CTRL    = 'h300, A_CLS_DPCP= 'h304, A_CLS_MAP = 'h308, A_CLS_REGEN= 'h30C,
    A_CLS_TCQ     = 'h310,
    A_PTP_CTRL    = 'h500, A_PTP_INCR= 'h504, A_PTP_ADJ = 'h508,
    A_PTP_TWLO    = 'h510, A_PTP_TWHI= 'h514, A_PTP_OFLO= 'h518, A_PTP_OFHI = 'h51C,
    A_PTP_CMD     = 'h520, A_PTP_TRLO= 'h530, A_PTP_TRHI= 'h534,
    A_PTP_ILAT    = 'h540, A_PTP_ELAT= 'h544,
    // ---- 0x600 ADP advertiser (IEEE 1722.1 / Milan v1.2) ----
    A_ADP_CTRL    = 'h600, A_ADP_EIDLO= 'h604, A_ADP_EIDHI= 'h608, A_ADP_MIDLO = 'h60C,
    A_ADP_MIDHI   = 'h610, A_ADP_ECAPS= 'h614, A_ADP_TALK = 'h618, A_ADP_LIST  = 'h61C,
    A_ADP_CCAPS   = 'h620, A_ADP_GMLO = 'h624, A_ADP_GMHI = 'h628, A_ADP_DOMAIN= 'h62C,
    A_ADP_IDX0    = 'h630, A_ADP_IDX1 = 'h634, A_ADP_ASLO = 'h638, A_ADP_ASHI  = 'h63C,
    A_ADP_CMD     = 'h640, A_ADP_STATUS='h644,
    A_AECP_STAT0  = 'h648, A_AECP_STAT1='h64C,   //! AECP listener status (RO)
    A_ACMP_STAT   = 'h650,                        //! ACMP responder status (RO)
    A_AAF_CTRL    = 'h654, A_AAF_DMLO = 'h658, A_AAF_DMHI = 'h65C, //! AAF talker
    A_AAF_FRAMES  = 'h660, A_AAF_PAIRS = 'h664,   //! AAF talker status (RO)
    A_ADP_DIAG    = 'h668,                        //! ADP dormancy diagnostics (RO)
    A_ACMP_TALKER = 'h66C,                        //! Milan talker SM state (RO)
    A_ACMP_LOBS   = 'h670,                        //! listener_observed override (RW, lwSRP socket)
    A_ADP_DIAG2   = 'h674,                        //! ADP liveness + discover diagnostics (RO live)
    // ---- 0x680 lwSRP engine (re-homed from the stale 0x660 sketch) ----
    A_LWSRP_CTRL  = 'h680, A_LWSRP_VID = 'h684, A_LWSRP_DMLO = 'h688,
    A_LWSRP_DMHI  = 'h68C, A_LWSRP_TSPEC = 'h690,
    A_LWSRP_STATUS= 'h694, A_LWSRP_SLOPE = 'h698, A_LWSRP_CNT = 'h69C,
    A_LWSRP_LAT   = 'h6A0,
    // ---- 0x6A4 ACMP listener SM (RO) ----
    A_ACMPL_STATE = 'h6A4, A_ACMPL_TKLO = 'h6A8, A_ACMPL_TKHI = 'h6AC,
    A_ACMPL_CNT   = 'h6B0, A_ACMPL_TUID = 'h6B4,
    A_AVTPRX_STAT = 'h6B8, A_AVTPRX_FRX = 'h6BC, A_AVTPRX_ERR = 'h6C0,
    A_PCMRX_CNT   = 'h6C4, A_PCMRX_TS   = 'h6C8,
    A_MAAP_CTRL   = 'h6CC, A_MAAP_STAT0 = 'h6D0, A_MAAP_STAT1 = 'h6D4,
    A_I2SPB_STAT  = 'h6D8, A_TONE_CTRL = 'h6DC, A_I2SPB_TRIM = 'h6E0,
    A_GPTP_PDELAY = 'h6E4,   //! RW: measured gPTP neighbor propagation delay (ns), written by the softcore gptp daemon
    A_ACMPL_DBG   = 'h6E8,   //! RO live: listener walker forensics {classify_cnt, fc_cnt, fc_flags, base_hits}
    A_AVTPRX_TSD  = 'h6EC,   //! RO live: signed ts_delta at last accepted PDU (stream-sync error signal)
    A_I2SPB_DBG   = 'h6F0,   //! RO live: exact 32 serial bits of the last LEFT half-frame at the DAC pin
    //! gh #59 departing-controller detection (Milan v1.2 §5.4.5.3). RO live,
    //! one word: {evictions[31:24], CONTROLLER_AVAILABLE replies seen[23:12],
    //! CONTROLLER_AVAILABLE probes sent[11:0]}. All three wrap.
    //! 0x6F8 and 0x6FC are the LAST free words of this group — reserved, do
    //! not guess at them without checking here first.
    A_CTLR_DIAG   = 'h6F4,
    // ---- 0x700 RX dest-MAC TCAM filter ----
    A_TCAM_CTRL   = 'h700, A_TCAM_KLO = 'h704, A_TCAM_KHI = 'h708, A_TCAM_MLO  = 'h70C,
    A_TCAM_MHI    = 'h710, A_TCAM_ACT = 'h714, A_TCAM_CMD = 'h718;
  localparam [ADDR_WIDTH-1:0] A_LINK_CTRL = 'h71C;   //! [0] sw_link (daemon), [1] mac_reinit (hold MAC sys-side in reset)
  localparam [ADDR_WIDTH-1:0] A_RST_EPOCH = 'h720;   //! RO live: datapath reset-release count (shadow-lie canary)
  localparam [ADDR_WIDTH-1:0] A_ENT_NAME_LO = 'h724; //! entity_name chars 0-3 (board name; 0 = ROM name)
  localparam [ADDR_WIDTH-1:0] A_ENT_NAME_HI = 'h728; //! entity_name chars 4-7
  localparam [ADDR_WIDTH-1:0] A_LPF_CTRL   = 'h72C;  //! [0] playback biquad LPF enable (default 1)
  localparam [ADDR_WIDTH-1:0] A_AS2_LO     = 'h730;  //! 802.1AS parent bridge ckid [31:0]
  localparam [ADDR_WIDTH-1:0] A_AS2_HI     = 'h734;  //! ...[63:32] (0 = none/unknown)
  localparam [ADDR_WIDTH-1:0] A_CRF_CTRL   = 'h738;  //! [0] CRF sink en; RO [31] locked
  localparam [ADDR_WIDTH-1:0] A_CRF_SIDLO  = 'h73C;  //! CRF stream_id [31:0]
  localparam [ADDR_WIDTH-1:0] A_CRF_SIDHI  = 'h740;  //! CRF stream_id [63:32]
  localparam [ADDR_WIDTH-1:0] A_CRF_DELTA  = 'h744;  //! RO signed crf_ts - ptp_now
  localparam [ADDR_WIDTH-1:0] A_CRF_RATE   = 'h748;  //! RO signed ns err / 512 ms
  localparam [ADDR_WIDTH-1:0] A_CRF_STATUS = 'h74C;  //! RO {pdu16, fmt_err8, seq_err8}
  //! 0x750 CRFT_CTRL - live read (the A_CRF_CTRL pattern: stored control
  //! bits in the low lanes, live status above):
  //!   [0]     RW  CRF talker enable
  //!   [1]     RW  SR class A (declare the lwSRP TA row, then tag)
  //!   [4]     RO  the CRF talker row is PROVISIONED and the lwSRP
  //!               applicant is running = the Talker Advertise is declared
  //!   [5]     RO  frames are leaving 802.1Q-TAGGED right now
  //!   [6]     RO  the reservation is ACTIVE (bw-gate: declared + Listener
  //!               Ready + admitted under the 75 % ceiling)
  //!   [19:8]  RO  VID on the frames (= the declaration's, one wire)
  //!   [22:20] RO  PCP on the frames (SR class A = 3)
  localparam [ADDR_WIDTH-1:0] A_CRFT_CTRL  = 'h750;
  localparam [ADDR_WIDTH-1:0] A_CRFT_SIDLO = 'h754;  //! CRF talker stream_id [31:0]
  localparam [ADDR_WIDTH-1:0] A_CRFT_SIDHI = 'h758;  //! CRF talker stream_id [63:32]
  localparam [ADDR_WIDTH-1:0] A_CRFT_DMLO  = 'h75C;  //! CRF talker DMAC [31:0]
  localparam [ADDR_WIDTH-1:0] A_CRFT_DMHI  = 'h760;  //! CRF talker DMAC [47:32]
  localparam [ADDR_WIDTH-1:0] A_CRFT_COUNT = 'h764;  //! RO live: CRF PDUs emitted
  localparam [ADDR_WIDTH-1:0] A_BDBG0 = 'h768;  //! RO live: 0x4B scan forensics (hdr bytes as scanned)
  localparam [ADDR_WIDTH-1:0] A_BDBG1 = 'h76C;  //! RO live: {0, cmd15, dlen16}
  localparam [ADDR_WIDTH-1:0] A_BDBG2 = 'h770;  //! RO live: {ptr, end}
  localparam [ADDR_WIDTH-1:0] A_LINKG_STAT = 'h774;  //! RO live: link guard {bounce16, flags, alive}
  //! ---- 0x778 clock validity: the AVTP "tu" verdict -----------------------
  //  Whether the PHC is disciplined to the gPTP domain is a SERVO fact and
  //  lives in ptp4l, not in fabric - so software leases it here, the
  //  established gptp2csr.sh pattern (GM 0x624/8, pdelay 0x6E4, AS_PATH
  //  0x730/4). It is a LEASE and not a flag on purpose: on 2026-07-27 the
  //  Arty's PHC was 60 h out of the domain and we streamed 31 M frames
  //  claiming tu=0 the whole time (docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md).
  //  Reset state is sync_ok=0 with an expired lease: unknown == not valid.
  localparam [ADDR_WIDTH-1:0] A_CLKV_CTRL  = 'h778;  //! RW: [0] SYNC_OK, [1] W1S report discontinuity, [15:4] lease in quarter-seconds. ANY write reloads the lease
  localparam [ADDR_WIDTH-1:0] A_CLKV_STAT  = 'h77C;  //! RO live: [0] tu now, [1] sync_ok, [2] no live lease, [3] holdover, [15:4] lease left
  localparam [ADDR_WIDTH-1:0] A_CLKV_TUCNT = 'h780;  //! RO live: Milan Table 5.4 TIMESTAMP_UNCERTAIN - 1 s intervals in which tu was set
  localparam [ADDR_WIDTH-1:0] A_TXARB_DIAG = 'h784;  //! RO live: TX-trunk arbiter lock supervision {0xA7, stall8, abort8, locked8}
  //! lwSRP OPERATIONAL Domain (Milan 4.2.7.2.1 adoption, RO live):
  //!   [11:0]  operational SR class-A VID (the one every serializer and the
  //!           AAF/CRF C-TAG carry)
  //!   [23:16] operational SR class-A priority
  //!   [24]    adopt_valid - the pair above is a RECEIVED FirstValue; 0 =
  //!           the {3, LWSRP_VID} defaults are in force
  localparam [ADDR_WIDTH-1:0] A_LWSRP_DOM = 'h788;
  //! CLKV_CTRL reset: SYNC_OK = 0, lease = 8 quarter-seconds (2 s). A daemon
  //! that stops refreshing therefore loses the claim in <= 2 s. The lease is
  //! NOT reset to 0 - a 0 lease means "expire immediately", which is a valid
  //! software choice but a hostile default for a daemon that never writes.
  localparam [31:0] CLKV_CTRL_RST_C = 32'h0000_0080;
  // ---- 0x7A0 ACMP bind-restore (E1, SAVED_STATE_FASTCONNECT.md §5):
  //  acmp-persist reloads a saved bind at boot — the commit injects a Milan
  //  5.5.3.5.2 entry record {PRB_W_AVAIL, probing PASSIVE, status 0,
  //  sid/dmac/vlan CLEARED per 5.5.2.6 step 1} into the listener ctx table;
  //  the fabric ADP watch + probe ladder take over. Plain-RW staging words
  //  (0x7A0 doubles as the software write/readback feature probe).
  localparam [ADDR_WIDTH-1:0] A_REST_TKLO = 'h7A0;   //! saved talker_entity_id [31:0]
  localparam [ADDR_WIDTH-1:0] A_REST_TKHI = 'h7A4;   //! saved talker_entity_id [63:32]
  localparam [ADDR_WIDTH-1:0] A_REST_META = 'h7A8;   //! {vlan[27:16] informational (ignored on load), tuid[15:0]}
  localparam [ADDR_WIDTH-1:0] A_REST_CTLO = 'h7AC;   //! saved controller_entity_id [31:0]
  localparam [ADDR_WIDTH-1:0] A_REST_CTHI = 'h7B0;   //! saved controller_entity_id [63:32]
  localparam [ADDR_WIDTH-1:0] A_REST_CMD  = 'h7B4;   //! W: [31] W1S commit, [23:8] binding flags, [3:0] sink idx; R live: {[31] busy, [30] done, [9:8] status, [3:0] idx}
  // ---- 0x7B8 persistence-journal ingest (E3, SAVED_STATE_FASTCONNECT.md
  //  §8; executable spec tb/verilator/persist/persist_wrap.sv): software
  //  lifts one flash slot image VERBATIM through DATA between START and
  //  END; the engine verifies magic/format/shape/owning-entity/CRC-32 (the
  //  CRC is the LAST word - a torn, foreign or stale image yields ZERO
  //  restores) and only then replays E1 entry records. Milan v1.2 5.3.8.2:
  //  the bound state SHALL be saved and restored after a power cycle.
  localparam [ADDR_WIDTH-1:0] A_JNL_CTRL = 'h7B8;   //! W1S: [0] start, [1] end, [2] abort; R: {stat[31:30], 0}
  localparam [ADDR_WIDTH-1:0] A_JNL_DATA = 'h7BC;   //! W: next 32-bit image word (write-only)
  localparam [ADDR_WIDTH-1:0] A_JNL_STAT = 'h7C0;   //! RO live: engine status/verdict word
  localparam [ADDR_WIDTH-1:0] A_JNL_SEQ  = 'h7C4;   //! RO live: last ACCEPTED image's SEQ watermark
  // ---- 0x7C8 AEM dynamic-state patch port (E4, SAVED_STATE_FASTCONNECT.md
  //  §10c; executable spec tb/verilator/aempatch/aempatch_wrap.sv): the
  //  write master the AEM store never had. Software names a DESCRIPTOR and a
  //  FIELD, never a byte address — the fabric resolves the range from the
  //  same generated WB_* tables SET_STREAM_FORMAT uses, revalidates the
  //  payload through the same acceptance, and refuses the whole group while
  //  ADP_CTRL[0] is set. Milan v1.2 5.3.5.1 / 5.3.7.1 / 5.3.8.1 / 5.3.11.1:
  //  these fields SHALL be saved and restored after a power cycle.
  localparam [ADDR_WIDTH-1:0] A_AEMP_SEL   = 'h7C8;  //! W: {desc_type[31:16], index[15:0]}
  localparam [ADDR_WIDTH-1:0] A_AEMP_FIELD = 'h7CC;  //! W: [2:0] 0 format, 1 sampling rate, 2 clock source
  localparam [ADDR_WIDTH-1:0] A_AEMP_DATA  = 'h7D0;  //! W: payload word, MSW first (write-only)
  localparam [ADDR_WIDTH-1:0] A_AEMP_CTRL  = 'h7D4;  //! W1S: [0] commit, [1] abort; R live: engine status/verdict
  //! ETHERNET GUARD (USER 2026-08-06: "a kill switch that should let the
  //! ethernet up on running until the software un-guards it"). Reset =
  //! GUARDED: while [0]=1 the CPU's eth-disruption levers are refused -
  //! A_PHY_RST writes are DROPPED, A_LINK_CTRL[1] (mac_reinit) is MASKED,
  //! and o_eth_guard gates the LiteX phy_crg_reset chain in milan_soc.py -
  //! so no software state (statd reinit, ethtool bounce, a corrupt rootfs
  //! poking CSRs) can take the streams' MAC down. The fabric link guard's
  //! own auto-recovery is NOT gated: it is the trusted fabric plane.
  //! UNGUARD by writing the magic 32'h554E_4C4B ("UNLK"); ANY other write
  //! re-arms the guard. Software unguards once healthy and may re-arm
  //! before risky work - the lease idiom, not a boot-once flag.
  localparam [ADDR_WIDTH-1:0] A_ETH_GUARD  = 'h7D8;  //! [0] guarded (RW via magic)
  // ---- 0x7DC AS_PATH staging (gh #64 J4): the daemon publishes the
  //  802.1AS-2020 10.3.9.23 pathTrace it parsed from the latest Announce's
  //  PathTrace TLV (1722.1-2021 7.4.41.2 serves it as GET_AS_PATH). Slot 0
  //  = the grandmaster, NEVER stored here (ADP_GM 0x624/8 is it); slots
  //  1-7 = the traversed bridges, staged 64 bits at a time through LO/HI
  //  and committed one slot per CMD write. A publish latches the path
  //  LENGTH and bumps the generation - the response builder's Table 5.22
  //  w_aspath_sig carries {count, gen}, so the publish edge IS the push
  //  arm even when the slot bytes did not change. count = 0 (reset) keeps
  //  the legacy two-entry [GM, parent] derivation: old daemons that only
  //  write AS2_LO/HI 0x730/4 regress nothing.
  //  NOTE the handover named 0x7B8-0x7C0 for this group; those addresses
  //  were taken by the E3 persistence-journal ingest before J4 landed, so
  //  the group lives at the next free words after ETH_GUARD instead.
  localparam [ADDR_WIDTH-1:0] A_ASP_LO  = 'h7DC;  //! RW: staged clockIdentity [31:0]
  localparam [ADDR_WIDTH-1:0] A_ASP_HI  = 'h7E0;  //! RW: staged clockIdentity [63:32]
  localparam [ADDR_WIDTH-1:0] A_ASP_CMD = 'h7E4;  //! W: [31] commit staged into slot [10:8] (1-7),
                                                  //!    [30] publish {count = [3:0]} + gen bump;
                                                  //! R live: {24'd0, gen[3:0], count[3:0]}
  //! slot count DERIVED from the port that carries them (one source: change
  //! o_asp_path's width and the store, the reset sweep and the published
  //! ceiling all follow). Entries served = the grandmaster + those slots.
  localparam int unsigned     ASP_SLOTS_C     = $bits(o_asp_path) / 64;
  localparam logic [3:0]      ASP_COUNT_MAX_C = 4'(ASP_SLOTS_C + 1);
  //! MMCM-DRP media-clock servo status. Deliberately parked at the 0x8F8
  //! tail (after the 0x800-0x85C indexed window) so parallel feature lanes
  //! extending the 0x700 group cannot collide; 0x8FC stays reserved next
  //! to it for a future servo knob.
  localparam [ADDR_WIDTH-1:0] A_MCSRV_STAT = 'h8F8;  //! RO live: {trim16, flags, state3}
  localparam [ADDR_WIDTH-1:0] A_MCSRV_CTRL = 'h8FC;  //! RW: [0] ps_invert (bench sign knob, 2026-07-23); [1] auto_repair enable (bench-gated DRP divider repair, default 0)
  //! item-11 AAF per-stage latency taps (KL_aaf_latency_taps). Parked just
  //! ABOVE the 0x800 stream window (which ends at A_STRMW_END = 0x870): CTRL
  //! at 0x870 then 16 packed RO words at 0x874-0x8B0. Like the servo, the RO
  //! words need the >=0x800 rd_in_window carve-out below or they read 0.
  localparam [ADDR_WIDTH-1:0] A_LTAP_CTRL = 'h870;   //! RW: [1] enable (def 1); W1S [0] clear stats. RO: {stage/active status}
  localparam [ADDR_WIDTH-1:0] A_LTAP_BASE = 'h874;   //! first RO readback word (16 words, packed)
  localparam [ADDR_WIDTH-1:0] A_LTAP_END  = 'h8B4;   //! one past the last RO word (0x8B0)
  //! RX stream-parser probe: the ONLY view UPSTREAM of the stream-table
  //! match (every other RX counter only exists once a frame matched). Same
  //! >=0x800 carve-out rules as the LTAP group directly below it.
  localparam [ADDR_WIDTH-1:0] A_APRB_BASE = 'h8B4;   //! first RO word (5 packed words 0x8B4-0x8C4)
  localparam [ADDR_WIDTH-1:0] A_APRB_END  = 'h8C8;   //! one past the last RO word (0x8C4)
  //! item-7 playback chain probe: host PCM ring -> KL_pcm_tx -> render
  //! crossbar -> KL_i2s_playback. The migen playback CSRs live in the LiteX
  //! SoC only; this group is the chain's evidence on the fabric control
  //! plane. Same >=0x800 carve-out rules as the two groups below it.
  localparam [ADDR_WIDTH-1:0] A_PBK_BASE  = 'h8C8;   //! first RO word (3 packed words 0x8C8-0x8D0)
  localparam [ADDR_WIDTH-1:0] A_PBK_END   = 'h8D4;   //! one past the last RO word (0x8D0)
  //! chmap map-RAM window (docs/CHANNEL_MAP_64.md §6). Same dedicated-arm
  //! carve-out as MCSRV (0x8F8/0x8FC): NOT in is_plain_rw (a 0x900 shadow
  //! write would alias word 0x100), a live read arm per word, and its own
  //! rd_in_window term (else every read here is the 0x8F8 dead-read trap).
  localparam [ADDR_WIDTH-1:0] A_CHMAP_CTRL = 'h900;  //! RW: [0] debug arm (static-shape routing + debug write window; no routing effect on dynamic-map shapes since 0x002C)
  localparam [ADDR_WIDTH-1:0] A_CHMAP_SEL  = 'h904;  //! RW: [5:0] entry idx, [8] side (0=render,1=capture)
  localparam [ADDR_WIDTH-1:0] A_CHMAP_WORD = 'h908;  //! RW: [15:0] §5 map word; write commits via the shared port (needs CTRL[0])
  localparam [ADDR_WIDTH-1:0] A_CHMAP_STAT = 'h90C;  //! RO: [15:0] commits, [23:16] refused
  //! map-RAM READBACK (the fabric's own contents, NOT the 0x908 shadow).
  //! SEL -> SNAP -> poll busy -> read, the 0x800 window discipline, with the
  //! 0x800 window's ONE trap fixed: the un-armed state is POISON, not zero.
  localparam [ADDR_WIDTH-1:0] A_CHMAP_SNAP = 'h910;  //! W1S [0] arm; R status+cap, [31:24] = 0xC5 tag
  localparam [ADDR_WIDTH-1:0] A_CHMAP_LOOP = 'h914;  //! RO: the latched map word + {fed,mapped,suspect}; 0xDEADDEAD = no measurement
  //! ---- protocol-processor control plane, 0x920-0x930 --------------------
  //! First window past CHMAP (0x914 was the highest decoded word in the map
  //! before this group). PRESENT is a CONSTANT tag in PP_STAT[31:24], so a
  //! read of 0 at 0x924 means "this build has no shadow plane" and can never
  //! be confused with "the plane is present and idle" - the STATS_CAP 0x204
  //! rule, and the reason PP_STAT is the register software must read FIRST.
  localparam [ADDR_WIDTH-1:0] A_PP_CTRL   = 'h920;  //! RW: [0] enable (entity_enable), [1] restore_go
  //! RO: [31:24] 0x5B tag, [7] nvm_blank, [6] nvm_backed, [5] sp_err,
  //! [4:0] {alarm,fail,done,busy,sp_busy}. THE SAVED-STATE VERDICT IS FOUR
  //! BITS, NOT ONE: done says the boot walk sequenced, and every per-record
  //! vendor-default arm sets it, so done alone is identical on a device with
  //! real media, on one with erased media and on one with no media at all.
  //! backed + blank separate the three, and fail is raised on the last of them
  //! so that a reader who knows only the old bits still sees "not successful".
  localparam [ADDR_WIDTH-1:0] A_PP_STAT   = 'h924;
  localparam [ADDR_WIDTH-1:0] A_PP_SPADDR = 'h928;  //! RW: [19:0] side-port WORD address; a WRITE here posts a READ
  localparam [ADDR_WIDTH-1:0] A_PP_SPDATA = 'h92C;  //! RW: read = last posted read's data; write = side-port WRITE to SPADDR
  localparam [ADDR_WIDTH-1:0] A_PP_DIAG   = 'h930;  //! RO: {tx_frames[15:0], drops[7:0], rx_frames[7:0]} shadow evidence
  //! PP_STAT[31:24]: a CONSTANT, so 0 at 0x924 = plane absent (see above).
  localparam logic [7:0] PP_PRESENT_TAG_C = 8'h5B;
  //! Watchdog on the readback handshake. The capture RAM answers one clock
  //! after en (registered read port) and the patched render side the same,
  //! so 15 is ~an order of magnitude of slack; its ONLY job is to make a
  //! declared-but-unwired port report TIMEOUT instead of hanging busy or
  //! latching a bus value it never saw valid.
  localparam logic [3:0] CHMAP_RD_WDOG_C = 4'd15;
  //! CHMAP_RDBK_P as a bit vector: [0] render side wired, [1] capture side
  //! wired (and carrying the {loop_fed, loop_mapped} mask).
  localparam logic [1:0] CHMAP_RDBK_C = 2'(CHMAP_RDBK_P);
  //! CHMAP_SNAP[31:24]: a CONSTANT, so a read of 0 at 0x910 means "this
  //! gateware predates the register" (0x910-0x93C used to read 0 as
  //! reserved). Same feature-probe idea as 0xA5C35A3C at A_REST_STAGE0.
  localparam logic [7:0] CHMAP_SNAP_TAG_C = 8'hC5;
  //! POISON for CHMAP_LOOP: the house "not-backed / not a measurement"
  //! sentinel already used by the 0x800 window's CNT words.
  localparam logic [31:0] CHMAP_LOOP_POISON_C = 32'hDEAD_DEAD;
  // ---- 0x800 indexed per-stream window (P11, NXN_ARCHITECTURE.md §1.5).
  //  SEL picks {dir, idx}; the 0x810-0x85C word block then views ONE stream.
  //  Legacy flat registers stay the authority for index 0 (N=1 bit-compat
  //  axiom); idx >= N_LISTENERS_P/N_TALKERS_P reads 0 and ignores writes.
  localparam [ADDR_WIDTH-1:0] A_STRM_SEL     = 'h800; //! RW live: [3:0] idx, [8] dir (0=listener, 1=talker), [9] listener-0 lwSRP row select (overrides idx/dir for the SRP master)
  localparam [ADDR_WIDTH-1:0] A_STRM_SNAP    = 'h804; //! W1S [0]: latch STATE+CNT0..9+PDUS coherently; R [0] busy
  localparam [ADDR_WIDTH-1:0] A_STRMW_CTRL   = 'h810; //! [0] en, [2:1] route (listener) / [0] en (talker, idx0 = AAF_CTRL[0] alias)
  localparam [ADDR_WIDTH-1:0] A_STRMW_SID_LO = 'h814; //! stream_id (talker RW / listener-bound RO)
  localparam [ADDR_WIDTH-1:0] A_STRMW_SID_HI = 'h818;
  localparam [ADDR_WIDTH-1:0] A_STRMW_DMAC_LO= 'h81C; //! stream DMAC (talker idx0 = AAF_DMLO/HI alias)
  localparam [ADDR_WIDTH-1:0] A_STRMW_DMAC_HI= 'h820;
  localparam [ADDR_WIDTH-1:0] A_STRMW_FMT_LO = 'h824; //! current stream format (LCTX w2/w3)
  localparam [ADDR_WIDTH-1:0] A_STRMW_FMT_HI = 'h828;
  localparam [ADDR_WIDTH-1:0] A_STRMW_STATE  = 'h82C; //! RO (snap-latched): packed per-stream state
  localparam [ADDR_WIDTH-1:0] A_STRMW_CNT0   = 'h830; //! RO (snap-latched): 10 Table 7-157 counters, word offsets 0..36 preserved
  localparam [ADDR_WIDTH-1:0] A_STRMW_CNT_END= 'h858; //! one past CNT9 (0x854)
  localparam [ADDR_WIDTH-1:0] A_STRMW_PDUS   = 'h858; //! RO (snap-latched): {drops,pdus} (listener) / frames_sent (talker)
  localparam [ADDR_WIDTH-1:0] A_STRMW_SRP    = 'h85C; //! RO live: per-stream lwSRP status (idx0 = 0x694 alias)
  //  E2 (SAVED_STATE_FASTCONNECT.md §5): the remaining 5.5.2.4/5.5.3.5.3
  //  persisted binding fields, from the same ACMP ctx snapshot as SID/DMAC
  localparam [ADDR_WIDTH-1:0] A_STRMW_CTLR_LO= 'h860; //! RO: binding controller_entity_id [31:0] (listener dir only)
  localparam [ADDR_WIDTH-1:0] A_STRMW_CTLR_HI= 'h864; //! RO: controller_entity_id [63:32]
  localparam [ADDR_WIDTH-1:0] A_STRMW_BIND   = 'h868; //! RO: {flags[31:16] (bit 3 = STREAMING_WAIT), tuid[15:0]}
  localparam [ADDR_WIDTH-1:0] A_STRMW_END    = 'h870; //! one past the window (0x86C reads 0)
  localparam [ADDR_WIDTH-1:0] A_STATS_BASE = 'h210;                        //! STAT0 base; STAT0..8 at stride 4
  localparam [ADDR_WIDTH-1:0] A_CBS_BASE   = 'h400;                        //! CBS queue 0 base; stride 0x20
  localparam [ADDR_WIDTH-1:0] A_STATS_END  = A_STATS_BASE + ADDR_WIDTH'(NS*4);          //! One past last STAT
  localparam [ADDR_WIDTH-1:0] A_CBS_END    = A_CBS_BASE   + ADDR_WIDTH'(NUM_QUEUES*32); //! One past last CBS reg

  // ==========================================================================
  //  AXI4-Lite slave handshake (combinational-ready, single outstanding).
  //
  //  Area-70 config-in-RAM (USER directive 2026-07-15): reads of plain-RW
  //  configuration registers are served from a write-through SHADOW BRAM
  //  instead of the old ~90-entry combinational mux; only live/W1C/status
  //  registers keep a (much smaller) mux. Because BRAM cannot reset, a
  //  DEFAULTS ROM (config-time init) is swept into the shadow after every
  //  reset (513 cycles; AXI *READY is held low meanwhile), so soft-reset
  //  readback semantics are IDENTICAL to the register file. Reads take one
  //  extra cycle (BRAM latency) — AXI4-Lite handshake absorbs it.
  // ==========================================================================
  logic         b_valid;                 //! Write-response valid, held until BREADY
  logic         r_valid;                 //! Read-data valid, held until RREADY
  logic         rd_pend;                 //! BRAM read latency stage
  //! Second read stage (the mux-split pipeline, 2026-08-15): the v47 route
  //! put the 13-level live/stream read mux on the failing-endpoint list at
  //! 100 MHz (rd_addr_q -> r_data, WNS -0.089). The wide case trees now
  //! LAND in their own registers on rd_pend, and the final four-way select
  //! into r_data runs a cycle later on rd_pend2 - the deep OR-trees and the
  //! AXI output flops no longer have to close in one cycle or one placement
  //! neighbourhood. One added cycle of CSR read latency; every AXI-Lite
  //! consumer in this tree waits on rvalid, and no read has a side effect
  //! keyed to the old timing.
  logic         rd_pend2;                //! staged-mux -> r_data stage
  logic [31:0]  live_mux_q, strm_mux_q, shadow_qq;
  logic         live_hit_q, strm_hit_q, rd_in_window_q;
  logic [31:0]  r_data;                  //! Registered read data
  logic [ADDR_WIDTH-1:0] rd_addr_q;      //! Latched read address (decode stage)
  logic         sweep_busy;              //! defaults -> shadow copy after reset
  logic [9:0]   sweep_cnt;

  //! wr_fire additionally holds off while a P11 engine CFG-word write
  //! request is pending (held until i_*_wr_rdy): a second AXI write landing
  //! mid-request would clobber the held addr/data. The engine accepts
  //! within a bounded walk (a few tens of cycles worst case), invisible to
  //! software except as AWREADY backpressure.
  wire wr_fire = s_axi_awvalid && s_axi_wvalid && !b_valid && !sweep_busy &&
                 !lctx_wr_p_r && !tctx_wr_p_r;
  wire rd_fire = s_axi_arvalid && !r_valid && !rd_pend && !rd_pend2 && !rds_busy_r &&
                 !sweep_busy;
  wire [ADDR_WIDTH-1:0] wr_addr = s_axi_awaddr;             //! Decoded write address
  wire [ADDR_WIDTH-1:0] rd_addr = s_axi_araddr;             //! Decoded read address

  //! P11 window words backed by the LCTX/TCTX context-RAM port B are "slow"
  //! reads: the AXI read stretches >= 4 cycles through the strm_slow_rd_S fetch
  //! (T2 rule: the window is served from the RAM's second port, never a
  //! widened CSR mux). During a SNAP burst they fall back to the fast path
  //! and read 0 (poll A_STRM_SNAP.busy first — documented ABI).
  wire rd_win_w = (rd_addr >= A_STRM_SEL) && (rd_addr < A_STRMW_END);
  wire rd_is_slow_w = rd_win_w && win_in_range_w && !snap_busy_r &&
      (!strm_dir_r
        ? (rd_addr == A_STRMW_CTRL || rd_addr == A_STRMW_FMT_LO ||
           rd_addr == A_STRMW_FMT_HI)
        : ((strm_idx_r != 4'd0) &&
           (rd_addr == A_STRMW_CTRL || rd_addr == A_STRMW_DMAC_LO ||
            rd_addr == A_STRMW_DMAC_HI)));
  //! P12: an engine-backed fetch completes on the engine's rd_valid, but
  //! only after the 4-cycle flush window (stale-valid guard — see the port
  //! contract above). With rd_valid tied 1 (no-engine TBs) this is the P11
  //! fixed 4-cycle timing exactly.
  wire rds_valid_w = rds_dir_r ? i_tctx_rd_valid : i_lctx_rd_valid;
  wire rds_done_w  = rds_busy_r && (rds_cyc_r == 2'd0) && rds_valid_w;

  assign s_axi_awready = wr_fire;
  assign s_axi_wready  = wr_fire;
  assign s_axi_arready = rd_fire;
  assign s_axi_bvalid  = b_valid;
  assign s_axi_bresp   = 2'b00;
  assign s_axi_rvalid  = r_valid;
  assign s_axi_rdata   = r_data;
  assign s_axi_rresp   = 2'b00;

  //! AXI response-channel valids: raise on a transfer, clear when accepted
  always_ff @(posedge aclk) begin : axi_resp_fsm
    if (!aresetn) begin
      b_valid <= 1'b0; r_valid <= 1'b0; rd_pend <= 1'b0; rd_pend2 <= 1'b0;
      rd_addr_q <= '0;
    end else begin
      if (wr_fire)           b_valid <= 1'b1;
      else if (s_axi_bready) b_valid <= 1'b0;
      rd_pend  <= rd_fire && !rd_is_slow_w;
      rd_pend2 <= rd_pend;
      if (rd_fire)           rd_addr_q <= rd_addr;
      if (rd_pend2 || rds_done_w) r_valid <= 1'b1;
      else if (s_axi_rready)     r_valid <= 1'b0;
    end
  end

  // ==========================================================================
  //  Register storage
  // ==========================================================================
  logic [31:0] scratch;                  //! SCRATCH: R/W bus-liveness test register
  logic [31:0] irq_mask;                 //! IRQ_MASK: 1 = interrupt source enabled
  logic [31:0] irq_status;               //! IRQ_STATUS: W1C latched event bits
  logic [31:0] mac_ctrl;                 //! MAC_CTRL: tx/rx enable, promisc, allmulti, is_1g, speed_manual
  //! ------------------------------------------------------------------------
  //! QUASI-STATIC TAGGING (USER 2026-08-15: relax the placer by CLASS, never
  //! by per-endpoint analysis). A register marked (* quasi_static = "yes" *)
  //! is written by boot software before the plane it configures is enabled,
  //! changes rarely-to-never afterwards, and every consumer treats it as a
  //! LEVEL. One generic XDC rule in sw/litex/milan_soc.py gives every tagged
  //! cell set_multicycle_path 4 setup / 3 hold, pruning its whole fan-out
  //! cone from the single-cycle timing graph - tag once at the declaration
  //! and the constraint follows the register through every future sweep.
  //!
  //! TAGGING RULES, and they are load-bearing:
  //!   * NEVER tag a strobe/pulse (*_p), a handshake (r_valid, rd_pend, ...),
  //!     a W1C/W1S event register, or anything a counter or edge-detector
  //!     consumes - multicycle routing may deliver BITS in different cycles,
  //!     and a torn multi-bit value into a != compare mints phantom edges.
  //!     That is exactly why the ADP GM pair (adp_gmlo/gmhi) is NOT tagged:
  //!     pp_gm_edge counts its changes.
  //!   * NEVER tag a register whose value is compared against per-frame wire
  //!     data in the same cycle it can change (the TCAM entries are handled
  //!     by their own structural pipeline instead).
  //!   * A tag is a CLAIM the consumer tolerates 4-cycle skew between bits;
  //!     when in doubt, leave it untagged - the default is the safe side.
  //! ------------------------------------------------------------------------
  (* quasi_static = "yes" *) logic [31:0] mac_ifg;   //! MAC_IFG: inter-frame gap (bytes)
  (* quasi_static = "yes" *) logic [31:0] mac_alo;   //! MAC_ADDR_LO: station MAC [31:0]
  (* quasi_static = "yes" *) logic [31:0] mac_ahi;   //! MAC_ADDR_HI: station MAC [47:32]
  (* quasi_static = "yes" *) logic [31:0] mc_lo;     //! MC_HASH_LO: multicast hash [31:0]
  (* quasi_static = "yes" *) logic [31:0] mc_hi;     //! MC_HASH_HI: multicast hash [63:32]
  logic [31:0] phy_rst;                  //! PHY_RESET: PHY reset (active-low bit 0)
  logic        eth_guard;                //! ETH_GUARD[0]: 1 = CPU eth levers refused
  logic [31:0] cls_ctrl;                 //! CLS_CTRL: classifier mode bits
  (* quasi_static = "yes" *) logic [31:0] cls_dpcp;  //! CLS_DEFAULT_PCP: default port priority
  (* quasi_static = "yes" *) logic [31:0] cls_map;   //! CLS_PCP_TC_MAP: PCP->TC table
  (* quasi_static = "yes" *) logic [31:0] cls_regen; //! CLS_PRIO_REGEN: priority regeneration table
  (* quasi_static = "yes" *) logic [31:0] cls_tcq;   //! CLS_TC_QUEUE_MAP: TC->queue map
  logic [31:0] ptp_ctrl;                 //! PTP_CTRL: PTP clock enable
  //! PTP_INCR reset value: the clock period in Q8.24 ns, derived from the
  //! instantiator's declared PHC clock (never a mirrored per-board constant)
  localparam logic [31:0] PTP_INCR_RST_C =
      32'((64'd1_000_000_000 << 24) / 64'(MILAN_CLK_FREQ_HZ_P));
  logic [31:0] ptp_incr;                 //! PTP_INCR: nominal per-tick increment
  logic [31:0] ptp_adj;                  //! PTP_ADJ: signed adjfine addend
  logic [31:0] ptp_twlo;                 //! PTP_TOD_WR_LO: settime target low
  logic [31:0] ptp_twhi;                 //! PTP_TOD_WR_HI: settime target high
  logic [31:0] ptp_oflo;                 //! PTP_OFFSET_LO: adjtime delta low
  logic [31:0] ptp_ofhi;                 //! PTP_OFFSET_HI: adjtime delta high
  logic [31:0] ptp_ilat;                 //! PTP_INGRESS_LAT: ingress latency correction
  logic [31:0] ptp_elat;                 //! PTP_EGRESS_LAT: egress latency correction
  logic [63:0] ptp_tod_rd;               //! PTP_TOD_RD: TOD latched on snapshot (gettime)
  logic [31:0] stat_snap [0:NS-1];       //! Coherent snapshot of the RMON counters

  logic [31:0] cbs_idle [0:NUM_QUEUES-1];//! Per-queue CBS idleSlope (bits/s)
  logic [31:0] cbs_hi   [0:NUM_QUEUES-1];//! Per-queue CBS hiCredit (signed bytes)
  logic [31:0] cbs_lo   [0:NUM_QUEUES-1];//! Per-queue CBS loCredit (signed bytes)
  logic [NUM_QUEUES-1:0] cbs_en;         //! Per-queue CBS shaped-enable

  logic stats_snap_p;                    //! Stats snapshot command strobe (1 cycle)
  logic stats_rst_p;                     //! Stats reset command strobe (1 cycle)
  logic i2spb_clru_p;                    //! I2SPB underrun-rail W1C strobe (1 cycle)
  logic i2spb_clro_p;                    //! I2SPB overrun-rail W1C strobe (1 cycle)
  logic [31:0] clkv_ctrl;                //! CLKV_CTRL 0x778 (bit 1 is W1S, never stored)
  logic clkv_wr_p;                       //! CLKV_CTRL written (1 cycle) - reloads the lease
  logic clkv_disc_p;                     //! CLKV_CTRL[1] software discontinuity report (1 cycle)
  logic ptp_load_p;                      //! PTP settime apply strobe (1 cycle)
  logic ptp_adj_p;                       //! PTP adjtime apply strobe (1 cycle)
  logic ptp_snap_p;                      //! PTP gettime snapshot strobe (1 cycle)

  // ADP advertiser identity/control registers (0x600 group)
  logic [31:0] adp_ctrl;                 //! ADP_CTRL: [0]=enable, [12:8]=valid_time
  reg   [7:0]  adp_disc_seen_cnt_r;      //! A_ADP_DIAG2[23:16]: ENTITY_DISCOVERs seen on the wire (any target)
  logic [31:0] aaf_ctrl, aaf_dmlo, aaf_dmhi; //! AAF talker: ctrl {vid[27:16], bypass[1], en[0]}, DMAC
  logic [31:0] acmp_lobs;                    //! A_ACMP_LOBS: [0] listener_observed override
  logic [31:0] lwsrp_ctrl;               //! LWSRP_CTRL: [0]=en, [1]=talker, [4:2]=classA queue, [5]=declare-always bypass (reset 0)
  logic [31:0] maap_ctrl;
  logic [31:0] link_ctrl;               //! LINK_CTRL: [0] sw_link
  logic [31:0] ent_name_lo, ent_name_hi; //! board-name overlay chars
  logic [31:0] lpf_ctrl;                 //! LPF_CTRL
  logic [31:0] crf_ctrl, crf_sidlo, crf_sidhi;   //! CRF sink CSRs
  logic [31:0] crft_ctrl, crft_sidlo, crft_sidhi, crft_dmlo, crft_dmhi;  //! CRF talker CSRs
  logic [31:0] as2_lo, as2_hi;           //! parent bridge clockIdentity                //! MAAP_CTRL: [0]=en, [1]=seed_valid, [15:8]=count, [31:16]=seed_offset
  //! TONE_CTRL: [0]=en (pilot tone), [3:1]=att in -6 dB steps (0 = 0 dBFS
  //! full scale, 7 = -42 dB). The table is FULL SCALE; a capture at
  //! amplitude 0.25 means att=2, not a quarter-scale generator.
  logic [31:0] tone_ctrl;
  logic [31:0] mcsrv_ctrl;               //! MCSRV_CTRL 0x8FC: [0]=ps_invert, [1]=auto_repair enable
  logic        ltap_en_r;                //! LTAP_CTRL[1]: latency-tap measurement enable (reset 1)
  logic        ltap_clr_p;               //! LTAP_CTRL[0] W1S: 1-cycle stats-clear strobe
  logic [31:0] chmap_ctrl;               //! CHMAP_CTRL 0x900: [0]=debug arm (see port doc)
  logic [31:0] chmap_sel;                //! CHMAP_SEL 0x904: [5:0]=idx, [8]=side
  logic [31:0] chmap_word;               //! CHMAP_WORD 0x908: last committed §5 word
  logic [15:0] chmap_commits;            //! CHMAP_STAT[15:0]: committed CSR writes (wraps)
  logic [7:0]  chmap_refused;            //! CHMAP_STAT[23:16]: refused writes (saturates)
  logic        chmap_wr_p;               //! one-cycle map-word write strobe
  //! chmap map-RAM readback state (CHMAP_SNAP 0x910 / CHMAP_LOOP 0x914)
  logic        cmrd_busy_r;              //! a readback request is in flight
  logic        cmrd_flush_r;             //! first busy cycle: ignore a stale valid
  logic        cmrd_valid_r;             //! the LAST snapshot carries fabric data
  logic        cmrd_to_r;                //! the LAST snapshot timed out (declared, not wired)
  logic        cmrd_unsup_r;             //! the LAST snapshot was refused (no port in this build)
  logic        cmrd_armed_r;             //! a snapshot has been armed since reset
  logic        cmrd_side_r;              //! side latched at arm time
  logic [5:0]  cmrd_addr_r;              //! entry index latched at arm time
  logic [15:0] cmrd_data_r;              //! the fabric's map word (valid only with cmrd_valid_r)
  logic [3:0]  cmrd_wd_r;                //! handshake watchdog

  //! CHMAP_SNAP 0x910 read view. [31:24] is a CONSTANT tag: a gateware
  //! without this group leaves 0x910 in the reserved-reads-0 range, so
  //! "0x910 reads 0" is an unambiguous "not in this bitstream" probe (the
  //! 0xA5C35A3C feature-probe pattern at A_REST_STAGE0, same idea).
  wire [31:0] chmap_snap_rd_w = {CHMAP_SNAP_TAG_C,              // [31:24]
                                 1'b0,                          // [23]
                                 cmrd_side_r, cmrd_addr_r,      // [22:16]
                                 6'd0,                          // [15:10]
                                 CHMAP_RDBK_C,                  // [9:8]
                                 3'd0,                          // [7:5]
                                 cmrd_armed_r, cmrd_unsup_r,    // [4:3]
                                 cmrd_to_r, cmrd_valid_r,       // [2:1]
                                 cmrd_busy_r};                  // [0]
  //! CHMAP_LOOP 0x914 read view. Without a completed snapshot behind it the
  //! word is POISON - never 0, because 0 is a LEGAL map entry (EN = 0) and
  //! the whole defect being fixed here is a zero that could mean two things.
  //! With one, [18] LOOP_SUSPECT = mapped & ~fed is the register's reason to
  //! exist: a slot the map advertises that no audio has ever reached.
  //!
  //! The word is SELF-DESCRIBING so software never has to cross-read 0x910
  //! to know whether it is looking at a measurement:
  //!   [26] VALID     - 1 on every word that came from the fabric. It is the
  //!                    ONLY register bit that says "this is a measurement",
  //!                    and it makes even an all-zero map entry at index 0
  //!                    read as 0x04000000 rather than 0.
  //!   [27] MASK_VALID- 1 when [18:16] are a measurement. Only the CAPTURE
  //!                    side's readback carries {loop_fed, loop_mapped}; on
  //!                    the render side those three bits are structurally 0
  //!                    and MUST NOT be read as "unmapped, never fed" (the
  //!                    render entry's own EN bit is raw [7]). Same rule as
  //!                    STATS_CAP 0x204: a capability bit is what separates
  //!                    a silent lane from a measured zero.
  //! [31:28] = 0 on every valid word, so no valid word can alias the poison.
  wire [31:0] chmap_loop_rd_w = cmrd_valid_r
      ? {4'd0,                                                  // [31:28]
         cmrd_side_r & CHMAP_RDBK_C[1],                         // [27] mask_valid
         1'b1,                                                  // [26] valid
         cmrd_addr_r, cmrd_side_r,                              // [25:19]
         //! capture raw view is {0, loop_fed[14], loop_mapped[13],
         //! entry[12:0]} since the per-channel store (0x0027) - the
         //! canonical flag positions HERE ([18:16]) are the stable ABI
         cmrd_data_r[13] & ~cmrd_data_r[14],                    // [18] suspect
         cmrd_data_r[14], cmrd_data_r[13],                      // [17] fed, [16] mapped
         cmrd_data_r}                                           // [15:0] raw
      : CHMAP_LOOP_POISON_C;
  logic [31:0] gptp_pdelay;              //! GPTP_PDELAY: neighbor pdelay (ns)
  logic [31:0] lwsrp_vid;                //! LWSRP_VID: [11:0] SR VID
  logic [31:0] lwsrp_dmlo, lwsrp_dmhi;   //! lwSRP stream DMAC {dmhi[15:0], dmlo}
  logic [31:0] lwsrp_tspec;              //! LWSRP_TSPEC: {interval[31:16], max_frame[15:0]}
  logic [31:0] lwsrp_lat;                //! LWSRP_LATENCY: AccumulatedLatency (ns)
  logic [31:0] adp_eidlo, adp_eidhi;     //! ADP_EID: entity_id (EUI-64)
  logic [31:0] adp_midlo, adp_midhi;     //! ADP_MID: entity_model_id (EUI-64)
  logic [31:0] adp_ecaps;                //! ADP_ECAPS: entity_capabilities
  //! ADP_TALK (0x618) / ADP_LIST (0x61C) have NO storage: they are RO shape
  //! words built from the elaboration parameters (see ADP_TALK_C/ADP_LIST_C
  //! below). There is deliberately no register here - a register is what let
  //! the 8x8 board advertise 1 source / 2 sinks for weeks.
  logic [31:0] adp_ccaps;                //! ADP_CCAPS: controller_capabilities
  logic [31:0] adp_gmlo, adp_gmhi;       //! ADP_GM: gptp_grandmaster_id (COMMITTED pair)
  //! GM pair atomic latch: the daemon publishes the 64-bit grandmaster id as
  //! two 32-bit devmem writes (gptp2csr.sh, 0x624 LO then 0x628 HI).
  //! Latching each half straight into the committed pair let every consumer
  //! (ADPDU gptp_grandmaster_id, GET_AVB_INFO, the CLKV holdover arm and the
  //! GPTP_GM_CHANGED edge detectors) sample a half-old/half-new identity
  //! between the writes - an identity NO grandmaster ever had, and a second
  //! counted "change" per real change. Milan v1.2 Table 5.1 defines
  //! GPTP_GM_CHANGED as "Number of gPTP GM changes, since boot" - CSR write
  //! phases are not GM changes. So a GMLO write only STAGES here and the
  //! GMHI write commits both halves in ONE cycle; the deployed LO-then-HI
  //! write order commits unmodified. Shadow-RAM readback is untouched
  //! (readback = last written word, committed or staged).
  logic [31:0] adp_gmlo_stg;
  logic [31:0] adp_domain;               //! ADP_DOMAIN: [7:0]=gptp_domain_number
  logic [31:0] adp_idx0;                 //! ADP_IDX0: {identify_control_index[31:16], current_config[15:0]}
  logic [31:0] adp_idx1;                 //! ADP_IDX1: [15:0]=interface_index
  logic [31:0] adp_aslo, adp_ashi;       //! ADP_ASSOC: association_id
  logic adp_adv_p;                       //! ADP advertise/info-changed strobe (1 cycle)
  logic adp_dep_p;                       //! ADP depart strobe (1 cycle)

  // RX dest-MAC TCAM filter programming (0x700 group)
  logic [31:0] tcam_ctrl;                //! TCAM_CTRL: [0]=default_pass, [1]=addr_filter_en
  logic [31:0] tcam_klo, tcam_khi;       //! TCAM key {khi[15:0], klo}
  logic [31:0] tcam_mlo, tcam_mhi;       //! TCAM mask {mhi[15:0], mlo}
  logic [31:0] tcam_act;                 //! TCAM action ([7:0])
  logic        tcam_wr_p;                //! entry-commit strobe (1 cycle)
  logic [4:0]  tcam_wr_index;            //! latched entry index for the commit
  logic        tcam_wr_valid_r;          //! latched add(1)/remove(0) for the commit

  // ---- 0x800 indexed per-stream window state (P11) ----------------------
  //! acmp_lstn_ctx_t flattened-field LSB offsets (single source: acmp_pkg;
  //! kept as literals so milan_csr stays package-free for the yosys file
  //! lists — the layout is locked by the tbl-port TB in tb/verilator/csr)
  localparam int ACMP_CTX_CTLR_LO_C    = 0;    //! ctlr[63:0]
  localparam int ACMP_CTX_SID_LO_C     = 128;  //! sid[63:0]
  localparam int ACMP_CTX_DMAC_LO_C    = 192;  //! dmac[47:0]
  localparam int ACMP_CTX_FLAGS_LO_C   = 252;  //! flags[15:0]
  localparam int ACMP_CTX_TUID_LO_C    = 268;  //! tuid[15:0]
  localparam int ACMP_CTX_STATUS_LO_C  = 305;  //! status[4:0]
  localparam int ACMP_CTX_PROBING_LO_C = 310;  //! probing[1:0]
  localparam int ACMP_CTX_STATE_LO_C   = 314;  //! state[2:0]
  //! lwSRP deployment constants — the 0x680 group reset words and the
  //! PriorityAndRank byte — GENERATED from the declarative end-station config
  //! by sw/builder/endstation_builder.py (roadmap item 4). They were literals
  //! here up to 11944cd; including them keeps this block package-free while
  //! making the config their single source, so a config edit re-elaborates the
  //! CSR block instead of silently disagreeing with it. Resolved through
  //! +incdir/-I hdl/common/csr, like gen/aecp_aem_rom.svh next door.
  `include "gen/lwsrp_csr_defaults.svh"

  //! ADP SHAPE (READ-ONLY, CONFIG-DEFINED - 2026-07-27, VERSION 0x0015).
  //! ADP_TALKER_SRC_C / ADP_LISTENER_SINK_C / the two capability words are
  //! GENERATED from the declarative end-station config by
  //! sw/builder/endstation_builder.py, exactly like the 0x680 lwSRP words
  //! above: the config says how many streams this entity has, the builder
  //! turns that into the AEM descriptor set AND these constants in one pass,
  //! and milan_datapath sizes its ACMP context arrays from the SAME file - so
  //! the advertised range, the addressable range and the descriptor set
  //! cannot disagree. Nothing here is a parameter and nothing is a register:
  //! a stream count is not something an instantiation or a boot script gets
  //! to choose (docs/findings/ADP_SHAPE_STATIC_0727.md).
  `include "gen/adp_shape_defaults.svh"

  //! The two RO words, assembled once and served from the defaults ROM like
  //! CAP and VERSION: no storage, no write arm.
  localparam logic [31:0] ADP_TALK_C = {ADP_TALKER_CAPS_C,
                                        16'(ADP_TALKER_SRC_C)};
  localparam logic [31:0] ADP_LIST_C = {ADP_LISTENER_CAPS_C,
                                        16'(ADP_LISTENER_SINK_C)};

  logic        strm_dir_r;               //! A_STRM_SEL[8]: 0=listener, 1=talker
  logic        strm_lsn0_r;             //! A_STRM_SEL[9]: select the DEDICATED
                                        //! listener-0 lwSRP row. Its own bit, not
                                        //! {dir=0, idx=0}: that pattern is the
                                        //! reset/park state every driver leaves
                                        //! behind, and treating it as a selection
                                        //! turned the idle window into a
                                        //! continuous row poll (milan_dp's qkill
                                        //! sweep caught the arbitration shift)
  logic [3:0]  strm_idx_r;               //! A_STRM_SEL[3:0]: stream index
  logic [31:0] stg_sid_lo_r, stg_sid_hi_r;   //! window write staging: stream_id
  logic [31:0] stg_dmac_lo_r, stg_dmac_hi_r; //! window write staging: DMAC
  //! WHICH {dir, idx} THE STAGING SET BELONGS TO (2026-07-30). The four
  //! staging words above are ONE register set shared by every index, so a
  //! CTRL commit must only spend them when they were staged FOR THAT
  //! selection - exactly the guard milan_datapath's win_commit_glue already
  //! applies to the stream-table side of the same staging ABI (and the same
  //! defect shape as the VERSION 0x000F stream-table fix: staging for one
  //! index then committing another armed the second with the first's sid).
  //! The SRP provisioning record had no such guard, so ANY leftover staged
  //! sid was written into whatever row was next committed - a Talker
  //! Advertise for a stream this station does not emit, and (since the
  //! fabric requesters landed) a silent claim of a row the fabric owns.
  //! A staging write that rebinds the set to a different selection CLEARS
  //! the other three words rather than mixing two streams' halves.
  logic [4:0]  stg_sel_r;
  logic        stg_vld_r;
  logic        lctx_wr_p_r;              //! LCTX CFG-word write pulse
  logic [7:0]  lctx_wr_addr_r;
  logic [31:0] lctx_wr_data_r;
  logic        tctx_wr_p_r;              //! TCTX CFG-word write pulse
  logic [6:0]  tctx_wr_addr_r;
  logic [31:0] tctx_wr_data_r;
  //! SRP ctx master: one pending provisioning write + continuous status poll
  logic        srp_wr_pend_r;            //! a row write awaits its grant
  logic        srp_wr_valid_r;           //! record valid (CTRL.en at commit)
  logic        srp_wr_dir_r;             //! ctx encoding (0=talker,1=listener)
  logic [4:0]  srp_wr_row_r;
  logic [63:0] srp_wr_sid_r;
  logic [47:0] srp_wr_dmac_r;
  logic        srp_cmd_was_wr_r;         //! we at the engine's service cycle
  logic        srp_fresh_r;              //! i_srp_ctx_rd_* match the selection
  //! ACMP tbl master: continuous poll of the selected listener context
  logic        acmp_fresh_r;
  logic [63:0] acmp_sid_q_r;
  logic [47:0] acmp_dmac_q_r;
  logic [2:0]  acmp_state_q_r;
  logic [1:0]  acmp_probing_q_r;
  logic [4:0]  acmp_status_q_r;
  logic [63:0] acmp_ctlr_q_r;         //! E2: binding controller_entity_id
  logic [15:0] acmp_flags_q_r;        //! E2: binding flags (STREAMING_WAIT)
  logic [15:0] acmp_tuid_q_r;         //! E2: bound talker_unique_id
  //! E3 journal-ingest strobes + image word (0x7B8 group)
  logic        jnl_start_p, jnl_wr_p, jnl_end_p, jnl_abort_p;
  logic [31:0] jnl_data_r;
  //! E4 AEM-patch strobes + the written word (0x7C8 group)
  logic        aemp_sel_p, aemp_field_p, aemp_data_p;
  logic        aemp_commit_p, aemp_abort_p;
  logic [31:0] aemp_wdata_r;
  //! J4 AS_PATH staging store (0x7DC group): 7 x 64 committed slots +
  //! the LO/HI staging pair + the published {count, gen} pair
  logic [31:0] asp_lo_r, asp_hi_r;      //! staged clockIdentity halves
  logic [63:0] asp_slot_r [0:ASP_SLOTS_C-1];  //! committed slots 1..7 (index k-1)
  logic [3:0]  asp_count_r;             //! published path length (0 = legacy)
  logic [3:0]  asp_gen_r;               //! publish generation
  //! ACMP bind-restore commit state (E1): staging regs are plain-RW
  //! shadow-backed; the CMD holds the rest master req until the engine ack
  logic [31:0] rest_tklo, rest_tkhi, rest_meta, rest_ctlo, rest_cthi;
  logic        rest_pend_r, rest_done_r;
  logic [1:0]  rest_stat_r;
  logic [3:0]  rest_idx_r;
  logic [15:0] rest_flags_r;
  //! SNAP shadow: the ONE permitted window shadow ([M-5.4.2.25] coherent
  //! counter block): [0] STATE, [1..10] CNT0..9, [11] PDUS
  logic [31:0] snap_shadow_r [0:11];
  logic        snap_busy_r;
  logic [2:0]  snap_st_r;                //! 0 idle,1 done-pulse,2 wait-free,3 arm,4 fetch
  logic        snap_dir_r;
  logic [3:0]  snap_idx_r;
  logic [3:0]  snap_wi_r;                //! burst word index
  logic [1:0]  snap_cyc_r;               //! per-word port-B latency count
  logic [4:0]  snap_word_r;              //! current engine word address
  logic        snap_req_r;               //! o_*_snap_req (dir-steered)
  logic        snap_rden_r;              //! o_*_rd_en during the burst
  logic [31:0] snap_m8_r;                //! LCTX w8 hold (STATE compose)
  //! slow read: engine port-B backed window words (4-cycle fetch)
  logic        rds_busy_r;
  logic        rds_dir_r;
  logic [1:0]  rds_cyc_r;
  logic [4:0]  rds_word_r;
  logic [2:0]  rds_idx_r;               //! stream index latched at the fetch

  // CBS power-on defaults: slope/credit values mirror ethernet_packet_pkg SR
  // classes (idleSlopes sum to 725 Mb/s = 72.5 %, under the 75 % REQ-CBS-03 ceiling;
  // hi/lo credit are calc_hi/lo_credit(idleSlope, 1e9) for MAX_FRAME_SIZE = 1522) —
  // but NO queue is shaped at reset. CBS shapes RESERVED SR classes only, never
  // best-effort (REQ-CBS-02); software (SRP/AVDECC reservation, `tc ... cbs`) opts a
  // queue in by setting CBS_CTRL[0]. The old default 4'b0011 contradicted the default
  // class map: cls_tcq routes untagged/BE traffic to q0, so shaping q0 at
  // idleSlope 300 Mb/s silently paced ALL best-effort TX to ~250 Mbit/s — measured on
  // silicon 2026-07-07 (datapath-input stall 42 % -> 0.4 % and TX wall moved to the
  // CPU the moment q0's en bit was cleared live via devmem 0x9000_040C).
  //
  // INDEXED BY QUEUE in the 802.1Q-order map, so entry 0 is q0 = BEST EFFORT
  // and entry 4 is q4 = SR class A (the array used to run the other way round,
  // because q0 used to be the highest-priority queue). The bandwidth follows
  // the priority: the two CBS-shaped classes take 45 % + 15 %, the strict-
  // priority remainder 5 % + 5 % + 2.5 %. The 5-queue map dropped the spare
  // queue and its 2.5 % with it - REQ-CBS-03 is a ceiling, so the freed share
  // is left unallocated rather than reassigned. MUST stay bit-identical to
  // ethernet_packet_pkg::IDLE_SLOPE_1G / HI_CREDIT / LO_CREDIT; the two are
  // pinned against each other by tb/verilator/csr and tb/verilator/shaper_core.
  localparam int CBS_IDLE_RST [0:4] = '{25_000_000, 50_000_000, 50_000_000,
                                        150_000_000, 450_000_000}; //! idleSlope bps, q0..q4
  localparam int CBS_HI_RST   [0:4] = '{38, 76, 76, 228, 684};              //! hiCredit bytes, q0..q4
  localparam int CBS_LO_RST   [0:4] = '{-1483, -1445, -1445, -1293, -837};  //! loCredit bytes, q0..q4
  localparam bit [4:0] CBS_EN_RST   = 5'b00000;                   //! ALL unshaped at reset (BE must never be CBS-paced)

  integer i;                             //! Loop index for reset/stats iteration

  //! MAC-reset snapshot invalidate (gaps 5 stale-shadow fix, 2026-07-22): a
  //! MAC reinit (link-guard episode or LINK_CTRL[1]) restarts the MAC path
  //! WITHOUT an aresetn event here, so a pre-reset STAT0-8 snapshot would
  //! keep serving stale counts - the 2026-07-19 "CSR plane lies until live
  //! counters tick" forensics. The reinit RELEASE edge zeroes the snapshot
  //! (0 = "no valid snapshot"); software re-arms it via STATS_CTRL[0].
  logic mac_reinit_q;
  always_ff @(posedge aclk) begin : mac_reinit_edge
    if (!aresetn) mac_reinit_q <= 1'b0;
    else          mac_reinit_q <= i_mac_reinit;
  end : mac_reinit_edge
  wire mac_reinit_rel_w = mac_reinit_q && !i_mac_reinit;

  //! P11 window selection range gate: out-of-range idx reads 0, writes are
  //! ignored, SNAP latches zeros (the defined out-of-range behaviour)
  wire win_in_range_w = strm_dir_r ? (32'(strm_idx_r) < N_TALKERS_P)
                                   : (32'(strm_idx_r) < N_LISTENERS_P);

  //! Register file write path: synchronous reset defaults, hardware event
  //! latching (before W1C), AXI-Lite register writes, W1C on IRQ_STATUS, and
  //! the single-cycle command strobes (stats snapshot/reset, PTP load/adjust/
  //! snapshot). Per-queue CBS registers live in the 0x400 window.
  always_ff @(posedge aclk) begin : register_write
    if (!aresetn) begin
      scratch <= 32'h0; irq_mask <= 32'h0; irq_status <= 32'h0;
      mac_ctrl <= 32'h13; mac_ifg <= 32'h0C; mac_alo <= 32'h0; mac_ahi <= 32'h0;
      mc_lo <= 32'h0; mc_hi <= 32'h0; phy_rst <= 32'h1;
      eth_guard <= 1'b1;                //! guarded from power-on (USER 08-06)
      // CLS_CTRL reset 0x5: [0] use_pcp = 1 (802.1Q tables), [1] dmac_check = 0
      // (REQ-CLS-07 opt-in), [2] ctrl_class = 1 (REQ-CLS-10 - the control fast
      // path ships ON, because the q2 row of EGRESS_QUEUE_MAP.md is the spec and
      // untagged control frames have no PCP the tables could route them by).
      cls_ctrl <= 32'h5; cls_dpcp <= 32'h0; cls_map <= 32'h00FAC688;
      // PRIO_REGEN resets to IDENTITY (0xFAC688 packs p->p at 3 bits/entry).
      // The previous 0x688FAC half-swapped priorities (0..3 <-> 4..7), silently
      // regenerating PCP 1..3 to 5..7 so SR-class frames landed in the wrong
      // queue (HW-diagnosed 2026-07-05 during the CBS interference bring-up).
      // CLS_TC_QUEUE_MAP packs one ceil(log2 NUM_QUEUES)-bit queue index per
      // traffic class. At NUM_QUEUES = 5 that is still 3 bits/entry and the
      // reset word is the 5-queue map (docs/reference/EGRESS_QUEUE_MAP.md):
      //   TC0,TC1 -> q0 (best effort / background)
      //   TC2     -> q3 (SR class B, 802.1Q Table 34-1 default priority 2)
      //   TC3     -> q4 (SR class A, 802.1Q Table 34-1 default priority 3 -
      //                  the PCP the AAF packetizer and lwSRP actually emit)
      //   TC4,TC5 -> q1 (control: MAAP/MSRP/MVRP + 1722.1 ADP/ACMP/AECP)
      //   TC6,TC7 -> q2 (internetwork/network control -> gPTP)
      // Every queue is mapped; the 6-queue map's unmapped spare is gone. A
      // traffic class that still named q5/q6/q7 would be CLAMPED to best
      // effort by traffic_class_map rather than silently dropped in the demux.
      cls_regen <= 32'h00FAC688; cls_tcq <= 32'h004898C0;
      //! free-run increment = the TRUE clock period (see MILAN_CLK_FREQ_HZ_P)
      ptp_ctrl <= 32'h1; ptp_incr <= PTP_INCR_RST_C; ptp_adj <= 32'h0;
      ptp_twlo <= 32'h0; ptp_twhi <= 32'h0; ptp_oflo <= 32'h0; ptp_ofhi <= 32'h0;
      ptp_ilat <= 32'h0; ptp_elat <= 32'h0; ptp_tod_rd <= 64'h0;
      for (i = 0; i < NS; i = i + 1) stat_snap[i] <= 32'h0;
      for (i = 0; i < NUM_QUEUES; i = i + 1) begin
        cbs_idle[i] <= (i < 5) ? CBS_IDLE_RST[i][31:0] : 32'h0;
        cbs_hi[i]   <= (i < 5) ? CBS_HI_RST[i][31:0]   : 32'h0;
        cbs_lo[i]   <= (i < 5) ? CBS_LO_RST[i][31:0]   : 32'h0;
      end
      cbs_en <= CBS_EN_RST[NUM_QUEUES-1:0];
      adp_ctrl <= 32'h0000_0A00;   // enable=0, valid_time=10 (Milan 5.6.2 "shall be set to 10"; validity 20 s)
      // enable=0, bypass=1 (bit1: legacy stream-whenever-enabled — the
      // Milan probe-gated mode is opt-in until silicon-proven), VID=2
      aaf_ctrl <= 32'h0002_0000;   //! bypass OFF at reset (0x0018)
      acmp_lobs <= 32'h0;
      aaf_dmlo <= 32'hF000_FE01;   // MAAP-range default 91:E0:F0:00:FE:01
      aaf_dmhi <= 32'h0000_91E0;
      // lwSRP: disabled; class-A queue 4 (the reset PCP3->TC3->q4 map);
      // VID/DMAC mirror the AAF defaults; TSpec {interval 1, max_frame 224}.
      // All six words come from gen/lwsrp_csr_defaults.svh (the config).
      lwsrp_ctrl <= LWSRP_CTRL_RST_C;
      maap_ctrl  <= 32'h0000_0800;
      link_ctrl  <= 32'h0000_0001;      //! link assumed UP until a daemon says otherwise
      ent_name_lo <= 32'h0; ent_name_hi <= 32'h0;
      lpf_ctrl    <= 32'h1;             //! LPF on by default
      crf_ctrl    <= 32'h0;
      crf_sidlo   <= 32'h0;
      crf_sidhi   <= 32'h0;
      crft_ctrl   <= 32'h0;
      crft_sidlo  <= 32'h0;
      crft_sidhi  <= 32'h0;
      crft_dmlo   <= 32'h0;
      crft_dmhi   <= 32'h0;
      as2_lo <= 32'h0; as2_hi <= 32'h0;
      tone_ctrl  <= 32'h0;
      mcsrv_ctrl <= 32'h0;
      ltap_en_r  <= 1'b1;   //! latency taps measure by default
      ltap_clr_p <= 1'b0;
      chmap_ctrl <= 32'h0; chmap_sel <= 32'h0; chmap_word <= 32'h0;
      chmap_commits <= 16'h0; chmap_refused <= 8'h0; chmap_wr_p <= 1'b0;
      gptp_pdelay <= 32'h0;
      //! lease = 8 quarter-seconds (2 s), SYNC_OK = 0: unknown is NOT valid
      clkv_ctrl  <= CLKV_CTRL_RST_C;
      lwsrp_vid  <= LWSRP_VID_RST_C;
      lwsrp_dmlo <= LWSRP_DMAC_LO_RST_C;
      lwsrp_dmhi <= LWSRP_DMAC_HI_RST_C;
      lwsrp_tspec<= LWSRP_TSPEC_RST_C;
      lwsrp_lat  <= LWSRP_LATENCY_RST_C;
      adp_eidlo <= 32'h0; adp_eidhi <= 32'h0; adp_midlo <= 32'h0; adp_midhi <= 32'h0;
      adp_ecaps <= 32'h0; adp_ccaps <= 32'h0;
      adp_gmlo <= 32'h0; adp_gmhi <= 32'h0; adp_gmlo_stg <= 32'h0;
      //! NOT 32'h0: the gPTP domain is CONFIG-DEFINED (gptp.domain), and the
      //! builder writes the same number into /etc/gptp.<board>.cfg. Boot
      //! holding it so ptp4l's domain and the ADPDU's byte 48 cannot disagree
      //! before any script runs. Still writable - see the csr_default mirror.
      adp_domain <= 32'(ADP_GPTP_DOMAIN_C);
      adp_idx0 <= 32'h0; adp_idx1 <= 32'h0; adp_aslo <= 32'h0; adp_ashi <= 32'h0;
      tcam_ctrl <= 32'h1;   // default_pass = 1 (accept-all until software programs entries)
      tcam_klo <= 32'h0; tcam_khi <= 32'h0; tcam_mlo <= 32'h0; tcam_mhi <= 32'h0;
      tcam_act <= 32'h0; tcam_wr_index <= 5'h0; tcam_wr_valid_r <= 1'b0;
      strm_dir_r <= 1'b0; strm_idx_r <= 4'd0; strm_lsn0_r <= 1'b0;
      stg_sid_lo_r <= 32'h0; stg_sid_hi_r <= 32'h0;
      stg_dmac_lo_r <= 32'h0; stg_dmac_hi_r <= 32'h0;
      stg_sel_r <= 5'h0; stg_vld_r <= 1'b0;
      lctx_wr_p_r <= 1'b0; lctx_wr_addr_r <= 8'h0; lctx_wr_data_r <= 32'h0;
      tctx_wr_p_r <= 1'b0; tctx_wr_addr_r <= 7'h0; tctx_wr_data_r <= 32'h0;
      rest_tklo <= 32'h0; rest_tkhi <= 32'h0; rest_meta <= 32'h0;
      rest_ctlo <= 32'h0; rest_cthi <= 32'h0;
      rest_pend_r <= 1'b0; rest_done_r <= 1'b0; rest_stat_r <= 2'd0;
      rest_idx_r <= 4'd0; rest_flags_r <= 16'h0;
      jnl_start_p <= 1'b0; jnl_wr_p <= 1'b0; jnl_end_p <= 1'b0;
      jnl_abort_p <= 1'b0; jnl_data_r <= 32'h0;
      aemp_sel_p <= 1'b0; aemp_field_p <= 1'b0; aemp_data_p <= 1'b0;
      aemp_commit_p <= 1'b0; aemp_abort_p <= 1'b0; aemp_wdata_r <= 32'h0;
      //! J4: count = 0 at reset is the LEGACY arm - a gateware nobody
      //! teaches to publish a path serves the [GM, parent] derivation, not
      //! a truncated one. Slots stay 0 so a stale bridge id can never be
      //! served by a later publish that names more entries than were
      //! committed.
      asp_lo_r <= 32'h0; asp_hi_r <= 32'h0;
      asp_count_r <= 4'h0; asp_gen_r <= 4'h0;
      for (i = 0; i < ASP_SLOTS_C; i = i + 1) asp_slot_r[i] <= 64'h0;
    end else begin
      // command strobes are single-cycle: default low, pulsed by writes below
      stats_snap_p <= 1'b0; stats_rst_p <= 1'b0;
      i2spb_clru_p <= 1'b0; i2spb_clro_p <= 1'b0;
      ptp_load_p <= 1'b0; ptp_adj_p <= 1'b0; ptp_snap_p <= 1'b0;
      adp_adv_p <= 1'b0; adp_dep_p <= 1'b0;
      clkv_wr_p <= 1'b0; clkv_disc_p <= 1'b0;
      tcam_wr_p <= 1'b0;
      ltap_clr_p <= 1'b0;
      chmap_wr_p <= 1'b0;
      jnl_start_p <= 1'b0; jnl_wr_p <= 1'b0; jnl_end_p <= 1'b0;
      jnl_abort_p <= 1'b0;
      aemp_sel_p <= 1'b0; aemp_field_p <= 1'b0; aemp_data_p <= 1'b0;
      aemp_commit_p <= 1'b0; aemp_abort_p <= 1'b0;
      //! P12: engine CFG-word write requests hold until the engine's
      //! same-cycle accept (the engines arbitrate their single RAM write
      //! port; a one-cycle pulse could be lost to an engine-write slot)
      if (i_lctx_wr_rdy) lctx_wr_p_r <= 1'b0;
      if (i_tctx_wr_rdy) tctx_wr_p_r <= 1'b0;

      // gettime result: latch the PHC snapshot when it returns (crosses CDC
      // asynchronously to the snapshot command, REQ-PTP-03/CSR-03).
      if (i_ptp_tod_valid) ptp_tod_rd <= i_ptp_tod;

      if (wr_fire) begin
        unique case (wr_addr)
          A_SCRATCH:   scratch  <= s_axi_wdata;
          A_IRQ_MASK:  irq_mask <= s_axi_wdata;
          A_IRQ_STATUS: begin // write-1-to-clear
            if (s_axi_wdata[0]) irq_status[0] <= 1'b0;
            if (s_axi_wdata[1]) irq_status[1] <= 1'b0;
            if (s_axi_wdata[2]) irq_status[2] <= 1'b0;
          end
          A_MAC_CTRL:  mac_ctrl <= s_axi_wdata;
          A_MAC_IFG:   mac_ifg  <= s_axi_wdata;
          A_MAC_ALO:   mac_alo  <= s_axi_wdata;
          A_MAC_AHI:   mac_ahi  <= s_axi_wdata;
          A_MC_LO:     mc_lo    <= s_axi_wdata;
          A_MC_HI:     mc_hi    <= s_axi_wdata;
          //! guarded: the write is DROPPED, not an error - the guard is a
          //! kill switch for effects, the bus contract stays boring
          A_PHY_RST:   if (!eth_guard) phy_rst <= s_axi_wdata;
          A_STATS_CTRL: begin
            if (s_axi_wdata[0]) begin // snapshot: latch all counters coherently
              stats_snap_p <= 1'b1;
              for (i = 0; i < NS; i = i + 1)
                stat_snap[i] <= i_stats[i*32 +: 32];
            end
            if (s_axi_wdata[1]) stats_rst_p <= 1'b1; // reset external counters
          end
          A_CLS_CTRL:  cls_ctrl  <= s_axi_wdata;
          A_CLS_DPCP:  cls_dpcp  <= s_axi_wdata;
          A_CLS_MAP:   cls_map   <= s_axi_wdata;
          A_CLS_REGEN: cls_regen <= s_axi_wdata;
          A_CLS_TCQ:   cls_tcq   <= s_axi_wdata;
          A_PTP_CTRL:  ptp_ctrl  <= s_axi_wdata;
          A_PTP_INCR:  ptp_incr  <= s_axi_wdata;
          A_PTP_ADJ:   ptp_adj   <= s_axi_wdata;
          A_PTP_TWLO:  ptp_twlo  <= s_axi_wdata;
          A_PTP_TWHI:  ptp_twhi  <= s_axi_wdata;
          A_PTP_OFLO:  ptp_oflo  <= s_axi_wdata;
          A_PTP_OFHI:  ptp_ofhi  <= s_axi_wdata;
          A_PTP_ILAT:  ptp_ilat  <= s_axi_wdata;
          A_PTP_ELAT:  ptp_elat  <= s_axi_wdata;
          A_PTP_CMD: begin // command strobes, self-clearing (read back 0)
            if (s_axi_wdata[0]) ptp_load_p <= 1'b1;
            if (s_axi_wdata[1]) ptp_adj_p  <= 1'b1;
            if (s_axi_wdata[2]) ptp_snap_p <= 1'b1; // gettime; PTP_TOD_RD latched on i_ptp_tod_valid
          end
          A_AAF_CTRL:   aaf_ctrl  <= s_axi_wdata;
          A_ACMP_LOBS:  acmp_lobs <= s_axi_wdata;
          A_LWSRP_CTRL: lwsrp_ctrl <= s_axi_wdata;
          A_MAAP_CTRL:  maap_ctrl  <= s_axi_wdata;
          //! guarded: [1] (mac_reinit) is masked; [0] (sw_link mirror) stays
          //! writable - it is telemetry into counters/ADP, not a reset lever
          A_LINK_CTRL:  link_ctrl  <= eth_guard
                            ? {s_axi_wdata[31:2], 1'b0, s_axi_wdata[0]}
                            : s_axi_wdata;
          A_ETH_GUARD:  eth_guard  <= (s_axi_wdata != 32'h554E_4C4B);
          //! Any write reloads the validity lease; [1] is a self-clearing
          //! W1S report and is never stored (it reads back 0). [2] IS stored
          //! (gh #64 J3): it is the daemon's IEEE 802.1AS-2020 10.2.5.1
          //! asCapable verdict, a LEVEL that rides the same lease as [0] -
          //! it used to be masked to 0, so a daemon writing it into an older
          //! gateware changed nothing and this stays backward compatible.
          //! [3] and [31:16] remain masked.
          A_CLKV_CTRL: begin
            clkv_ctrl <= {16'h0, s_axi_wdata[15:4], 1'h0, s_axi_wdata[2],
                          1'h0, s_axi_wdata[0]};
            clkv_wr_p <= 1'b1;
            if (s_axi_wdata[1]) clkv_disc_p <= 1'b1;
          end
          A_ENT_NAME_LO: ent_name_lo <= s_axi_wdata;
          A_ENT_NAME_HI: ent_name_hi <= s_axi_wdata;
          A_LPF_CTRL:   lpf_ctrl <= s_axi_wdata;
          A_CRF_CTRL:   crf_ctrl  <= s_axi_wdata;
          A_CRF_SIDLO:  crf_sidlo <= s_axi_wdata;
          A_CRF_SIDHI:  crf_sidhi <= s_axi_wdata;
          A_CRFT_CTRL:  crft_ctrl  <= s_axi_wdata;
          A_CRFT_SIDLO: crft_sidlo <= s_axi_wdata;
          A_CRFT_SIDHI: crft_sidhi <= s_axi_wdata;
          A_CRFT_DMLO:  crft_dmlo  <= s_axi_wdata;
          A_CRFT_DMHI:  crft_dmhi  <= s_axi_wdata;
          A_AS2_LO:     as2_lo   <= s_axi_wdata;
          A_AS2_HI:     as2_hi   <= s_axi_wdata;
          A_TONE_CTRL:  tone_ctrl  <= s_axi_wdata;
          A_MCSRV_CTRL: mcsrv_ctrl <= s_axi_wdata;
          A_LTAP_CTRL: begin              //! [1] enable RW; [0] W1S stats clear
            ltap_en_r <= s_axi_wdata[1];
            if (s_axi_wdata[0]) ltap_clr_p <= 1'b1;
          end
          A_CHMAP_CTRL: chmap_ctrl <= s_axi_wdata;
          A_CHMAP_SEL:  chmap_sel  <= s_axi_wdata;
          //! §6: the map word commits through the shared write port only while
          //! the override is armed (CTRL[0]) and LOCK_ENTITY is not held.
          //! Milan 5.4.2.27 and 5.4.2.28 forbid this non-ATDECC writer while
          //! locked. Every refused write is counted and leaves the map intact.
          A_CHMAP_WORD: begin
            if (chmap_ctrl[0] && !i_aecp_locked) begin
              chmap_word    <= s_axi_wdata;
              chmap_wr_p    <= 1'b1;
              chmap_commits <= chmap_commits + 16'd1;
            end else begin
              chmap_refused <= (&chmap_refused) ? chmap_refused
                                                : chmap_refused + 8'd1;
            end
          end
          //! A_CHMAP_SNAP (0x910) is W1S and has NO storage here: the arm is
          //! decoded combinationally as cmrd_go_w and consumed by chmap_rd_S.
          //! It is deliberately absent from is_plain_rw (a 0x900-range shadow
          //! write would alias word 0x100) and from the shadow write enable
          //! (which already excludes every address with bit 11 set).
          //! I2SPB rail counters W1C (gaps 5b): each half clears on a write
          //! with any bit of that half set - the saturated-and-stuck-forever
          //! rail becomes re-armable without touching the other rail
          A_I2SPB_STAT: begin
            if (|s_axi_wdata[31:16]) i2spb_clru_p <= 1'b1;
            if (|s_axi_wdata[15:0])  i2spb_clro_p <= 1'b1;
          end
          A_GPTP_PDELAY: gptp_pdelay <= s_axi_wdata;
          A_LWSRP_VID:  lwsrp_vid  <= s_axi_wdata;
          A_LWSRP_DMLO: lwsrp_dmlo <= s_axi_wdata;
          A_LWSRP_DMHI: lwsrp_dmhi <= s_axi_wdata;
          A_LWSRP_TSPEC: lwsrp_tspec <= s_axi_wdata;
          A_LWSRP_LAT:  lwsrp_lat  <= s_axi_wdata;
          A_AAF_DMLO:   aaf_dmlo  <= s_axi_wdata;
          A_AAF_DMHI:   aaf_dmhi  <= s_axi_wdata;
          A_ADP_CTRL:   adp_ctrl  <= s_axi_wdata;
          A_ADP_EIDLO:  adp_eidlo <= s_axi_wdata;
          A_ADP_EIDHI:  adp_eidhi <= s_axi_wdata;
          A_ADP_MIDLO:  adp_midlo <= s_axi_wdata;
          A_ADP_MIDHI:  adp_midhi <= s_axi_wdata;
          A_ADP_ECAPS:  adp_ecaps <= s_axi_wdata;
          //! A_ADP_TALK / A_ADP_LIST: NO write arm. The shape is elaborated,
          //! not provisioned (VERSION 0x0015).
          A_ADP_CCAPS:  adp_ccaps <= s_axi_wdata;
          //! GM pair atomic latch (see adp_gmlo_stg): LO stages, HI commits
          //! both halves in one cycle so no consumer ever sees a torn id
          A_ADP_GMLO:   adp_gmlo_stg <= s_axi_wdata;
          A_ADP_GMHI:   begin
            adp_gmlo <= adp_gmlo_stg;
            adp_gmhi <= s_axi_wdata;
          end
          A_ADP_DOMAIN: adp_domain<= s_axi_wdata;
          A_ADP_IDX0:   adp_idx0  <= s_axi_wdata;
          A_ADP_IDX1:   adp_idx1  <= s_axi_wdata;
          A_ADP_ASLO:   adp_aslo  <= s_axi_wdata;
          A_ADP_ASHI:   adp_ashi  <= s_axi_wdata;
          A_ADP_CMD: begin // W1S self-clearing strobes
            if (s_axi_wdata[0]) adp_adv_p <= 1'b1; // advertise now + bump available_index
            if (s_axi_wdata[1]) adp_dep_p <= 1'b1; // send ENTITY_DEPARTING
          end
          //! P11 indexed window (0x800): SEL picks the stream; word writes at
          //! idx 0 dir=talker hard-alias the flat AAF registers, engine-backed
          //! words forward to the LCTX/TCTX CFG write bundles, SID/DMAC writes
          //! additionally stage the lwSRP provisioning record (committed by
          //! the CTRL write, see strm_srp_master_S). Out-of-range: ignored.
          A_STRM_SEL: begin
            strm_dir_r <= s_axi_wdata[8];
            strm_idx_r <= s_axi_wdata[3:0];
            strm_lsn0_r <= s_axi_wdata[9];
          end
          A_STRMW_CTRL: if (win_in_range_w) begin
            if (!strm_dir_r) begin           // listener: LCTX w4 {route, en}
              lctx_wr_p_r    <= 1'b1;
              lctx_wr_addr_r <= {strm_idx_r[2:0], 5'd4};
              lctx_wr_data_r <= s_axi_wdata;
            end else if (strm_idx_r == 4'd0) begin
              aaf_ctrl <= {aaf_ctrl[31:1], s_axi_wdata[0]};  // = AAF_CTRL[0]
            end else begin                   // talker ctx: TCTX w0
              tctx_wr_p_r    <= 1'b1;
              tctx_wr_addr_r <= {strm_idx_r[2:0], 4'd0};
              tctx_wr_data_r <= s_axi_wdata;
            end
          end
          A_STRMW_SID_LO: if (win_in_range_w) begin
            stg_sid_lo_r <= s_axi_wdata;
            if (!stg_hit_w) begin        //! rebind: never mix two selections
              stg_sid_hi_r <= 32'h0;
              stg_dmac_lo_r <= 32'h0; stg_dmac_hi_r <= 32'h0;
            end
            stg_sel_r <= {strm_dir_r, strm_idx_r};
            stg_vld_r <= 1'b1;
            if (!strm_dir_r) begin
              lctx_wr_p_r    <= 1'b1;
              lctx_wr_addr_r <= {strm_idx_r[2:0], 5'd0};
              lctx_wr_data_r <= s_axi_wdata;
            end
          end
          A_STRMW_SID_HI: if (win_in_range_w) begin
            stg_sid_hi_r <= s_axi_wdata;
            if (!stg_hit_w) begin
              stg_sid_lo_r <= 32'h0;
              stg_dmac_lo_r <= 32'h0; stg_dmac_hi_r <= 32'h0;
            end
            stg_sel_r <= {strm_dir_r, strm_idx_r};
            stg_vld_r <= 1'b1;
            if (!strm_dir_r) begin
              lctx_wr_p_r    <= 1'b1;
              lctx_wr_addr_r <= {strm_idx_r[2:0], 5'd1};
              lctx_wr_data_r <= s_axi_wdata;
            end
          end
          A_STRMW_DMAC_LO: if (win_in_range_w) begin
            stg_dmac_lo_r <= s_axi_wdata;
            if (!stg_hit_w) begin
              stg_sid_lo_r <= 32'h0; stg_sid_hi_r <= 32'h0;
              stg_dmac_hi_r <= 32'h0;
            end
            stg_sel_r <= {strm_dir_r, strm_idx_r};
            stg_vld_r <= 1'b1;
            if (strm_dir_r) begin
              if (strm_idx_r == 4'd0) aaf_dmlo <= s_axi_wdata;  // = AAF_DMLO
              else begin
                tctx_wr_p_r    <= 1'b1;
                tctx_wr_addr_r <= {strm_idx_r[2:0], 4'd1};
                tctx_wr_data_r <= s_axi_wdata;
              end
            end
          end
          A_STRMW_DMAC_HI: if (win_in_range_w) begin
            stg_dmac_hi_r <= s_axi_wdata;
            if (!stg_hit_w) begin
              stg_sid_lo_r <= 32'h0; stg_sid_hi_r <= 32'h0;
              stg_dmac_lo_r <= 32'h0;
            end
            stg_sel_r <= {strm_dir_r, strm_idx_r};
            stg_vld_r <= 1'b1;
            if (strm_dir_r) begin
              if (strm_idx_r == 4'd0) aaf_dmhi <= s_axi_wdata;  // = AAF_DMHI
              else begin
                tctx_wr_p_r    <= 1'b1;
                tctx_wr_addr_r <= {strm_idx_r[2:0], 4'd2};
                tctx_wr_data_r <= s_axi_wdata;
              end
            end
          end
          A_STRMW_FMT_LO: if (win_in_range_w && !strm_dir_r) begin
            lctx_wr_p_r    <= 1'b1;      // talker format is AECP-owned: dir=1 ignored
            lctx_wr_addr_r <= {strm_idx_r[2:0], 5'd2};
            lctx_wr_data_r <= s_axi_wdata;
          end
          A_STRMW_FMT_HI: if (win_in_range_w && !strm_dir_r) begin
            lctx_wr_p_r    <= 1'b1;
            lctx_wr_addr_r <= {strm_idx_r[2:0], 5'd3};
            lctx_wr_data_r <= s_axi_wdata;
          end
          //! E3 journal-ingest group (0x7B8): 1-cycle command strobes +
          //! the write-only image word - persist_wrap.sv is the executable
          //! spec this decode must match strobe-for-strobe
          A_JNL_CTRL: begin
            jnl_start_p <= s_axi_wdata[0];
            jnl_end_p   <= s_axi_wdata[1];
            jnl_abort_p <= s_axi_wdata[2];
          end
          A_JNL_DATA: begin
            jnl_wr_p   <= 1'b1;
            jnl_data_r <= s_axi_wdata;
          end
          //! E4 AEM-patch group (0x7C8): one held data word + one-cycle
          //! strobes - aempatch_wrap.sv is the executable spec this decode
          //! must match strobe-for-strobe. NOTE none of these addresses is
          //! in is_plain_rw: the engine's state is not a shadow register,
          //! and a SEL that read back would invite software to believe a
          //! selection survived a refusal it did not survive.
          A_AEMP_SEL:   begin aemp_wdata_r <= s_axi_wdata; aemp_sel_p   <= 1'b1; end
          A_AEMP_FIELD: begin aemp_wdata_r <= s_axi_wdata; aemp_field_p <= 1'b1; end
          A_AEMP_DATA:  begin aemp_wdata_r <= s_axi_wdata; aemp_data_p  <= 1'b1; end
          A_AEMP_CTRL: begin
            aemp_commit_p <= s_axi_wdata[0];
            aemp_abort_p  <= s_axi_wdata[1];
          end
          //! E1 bind-restore group (0x7A0): plain-RW staging + the commit.
          //! A commit is only accepted while idle (busy readback covers the
          //! re-commit race); done/status stick until the next commit.
          A_REST_TKLO: rest_tklo <= s_axi_wdata;
          A_REST_TKHI: rest_tkhi <= s_axi_wdata;
          A_REST_META: rest_meta <= s_axi_wdata;
          A_REST_CTLO: rest_ctlo <= s_axi_wdata;
          A_REST_CTHI: rest_cthi <= s_axi_wdata;
          A_REST_CMD: begin
            if (s_axi_wdata[31] && !rest_pend_r) begin
              rest_pend_r  <= 1'b1;
              rest_done_r  <= 1'b0;
              rest_stat_r  <= 2'd0;
              rest_idx_r   <= s_axi_wdata[3:0];
              rest_flags_r <= s_axi_wdata[23:8];
            end
          end
          //! J4 AS_PATH staging group (0x7DC): LO/HI are plain-RW staging
          //! (is_plain_rw, readback via the shadow); CMD is the atomic
          //! cutover. A COMMIT ([31]) moves the staged 64-bit clockIdentity
          //! into the slot named by [10:8] - slot 0 is REFUSED because slot
          //! 0 is the grandmaster and already lives at ADP_GM 0x624/8
          //! (derive-never-mirror). A PUBLISH ([30]) latches the path LENGTH
          //! from [3:0] and bumps the generation: that pair is what the
          //! response builder's Milan Table 5.22 signature watches, so the
          //! publish edge is the push arm even when no slot byte moved.
          //! The length is CLAMPED to the eight the store can serve, so the
          //! CMD readback never advertises entries the wire cannot carry.
          A_ASP_LO: asp_lo_r <= s_axi_wdata;
          A_ASP_HI: asp_hi_r <= s_axi_wdata;
          A_ASP_CMD: begin
            if (s_axi_wdata[31] && (s_axi_wdata[10:8] != 3'd0))
              asp_slot_r[s_axi_wdata[10:8] - 3'd1] <= {asp_hi_r, asp_lo_r};
            if (s_axi_wdata[30]) begin
              asp_count_r <= (s_axi_wdata[3:0] > ASP_COUNT_MAX_C)
                           ? ASP_COUNT_MAX_C : s_axi_wdata[3:0];
              asp_gen_r   <= asp_gen_r + 4'd1;
            end
          end
          A_TCAM_CTRL: tcam_ctrl <= s_axi_wdata;
          A_TCAM_KLO:  tcam_klo  <= s_axi_wdata;
          A_TCAM_KHI:  tcam_khi  <= s_axi_wdata;
          A_TCAM_MLO:  tcam_mlo  <= s_axi_wdata;
          A_TCAM_MHI:  tcam_mhi  <= s_axi_wdata;
          A_TCAM_ACT:  tcam_act  <= s_axi_wdata;
          A_TCAM_CMD: begin // [4:0] index, [8] valid, [16] commit (W1S) -> pulse entry write
            if (s_axi_wdata[16]) begin
              tcam_wr_p       <= 1'b1;
              tcam_wr_index   <= s_axi_wdata[4:0];
              tcam_wr_valid_r <= s_axi_wdata[8];
            end
          end
          default: begin
            // per-queue CBS window 0x400 + q*0x20 (stride 0x20 => off[5+:QW] = queue)
            if (wr_addr >= A_CBS_BASE && wr_addr < A_CBS_END) begin
              logic [ADDR_WIDTH-1:0] off;
              off = wr_addr - A_CBS_BASE;
              case (off[4:0])
                5'h00: cbs_idle[off[5 +: QW]] <= s_axi_wdata;
                5'h04: cbs_hi  [off[5 +: QW]] <= s_axi_wdata;
                5'h08: cbs_lo  [off[5 +: QW]] <= s_axi_wdata;
                5'h0C: cbs_en  [off[5 +: QW]] <= s_axi_wdata[0];
                default: ;
              endcase
            end
          end
        endcase
      end

      // E1 bind-restore completion: the engine's 1-cycle ack ends the
      // commit; status is latched with it (0 injected / 1 occupied / 2 bad
      // idx). A CMD write can never coincide with an ack for the SAME
      // commit (the ack only follows a held req = an accepted commit).
      if (i_acmp_rest_ack && rest_pend_r) begin
        rest_pend_r <= 1'b0;
        rest_done_r <= 1'b1;
        rest_stat_r <= i_acmp_rest_status;
      end

      // Hardware-set event latches, applied AFTER the W1C write above so a
      // hardware event coincident with a software acknowledge is NOT lost: the
      // set wins the same-cycle race (REQ-CSR-04).
      if (i_evt_tx_ts_ready)   irq_status[0] <= 1'b1;
      if (i_evt_link_change)   irq_status[1] <= 1'b1;
      if (i_evt_rmon_rollover) irq_status[2] <= 1'b1;

      // MAC-reset snapshot invalidate, applied AFTER the write path so it
      // wins a coincident STATS_CTRL[0] latch: no stale pre-reset counts
      // can survive a MAC reinit into the read window.
      if (mac_reinit_rel_w)
        for (i = 0; i < NS; i = i + 1) stat_snap[i] <= 32'h0;
    end
  end

  // ==========================================================================
  //  Config-in-RAM read path (area-70): shadow BRAM + defaults ROM + sweep
  // ==========================================================================

  //! reset/readback value per byte address — the single source shared by the
  //! defaults ROM init (must mirror the register_write reset block above)
  function automatic [31:0] csr_default(input [10:0] a);
    csr_default = 32'h0;
    unique case (a)
      A_ID[10:0]:         csr_default = 32'h4D49_4C4E;      // "MILN"
      A_VERSION[10:0]:    csr_default = VERSION;
      A_CAP[10:0]:        csr_default = { 8'h00, 8'd64,
                                          1'b0, 1'b1, 1'b1, 1'b1,
                                          1'b1, 1'b1, 1'b1, 1'b1,
                                          4'h0, 4'(NUM_QUEUES) };
      A_MAC_CTRL[10:0]:   csr_default = 32'h13;
      A_MAC_IFG[10:0]:    csr_default = 32'h0C;
      A_PHY_RST[10:0]:    csr_default = 32'h1;
      A_CLS_CTRL[10:0]:   csr_default = 32'h5;
      A_CLS_MAP[10:0]:    csr_default = 32'h00FAC688;
      A_CLS_REGEN[10:0]:  csr_default = 32'h00FAC688;
      A_CLS_TCQ[10:0]:    csr_default = 32'h004898C0;
      A_PTP_CTRL[10:0]:   csr_default = 32'h1;
      //! DERIVED, never mirrored: the write-reset at PTP_INCR uses
      //! PTP_INCR_RST_C, so this readback image must use the SAME
      //! localparam. It carried a hardcoded 0x0800_0000 (the 125 MHz
      //! period) while the flop already derived from the parameter, so on
      //! the shipping 100 MHz milan domain the PHC incremented correctly
      //! and the register REPORTED 8 ns instead of 10. The csr suite never
      //! passed MILAN_CLK_FREQ_HZ_P, so it elaborated at the 125 MHz
      //! default where the two agreed and nothing caught it.
      A_PTP_INCR[10:0]:   csr_default = PTP_INCR_RST_C;
      A_ADP_CTRL[10:0]:   csr_default = 32'h0000_0A00;
      //! RO shape words: the reset value IS the answer, forever (0x0015)
      A_ADP_TALK[10:0]:   csr_default = ADP_TALK_C;
      A_ADP_LIST[10:0]:   csr_default = ADP_LIST_C;
      //! MIRROR of the adp_domain reset above (the rule stated at VERSION
      //! 0x0026: the write-reset literal and this readback ROM move together)
      A_ADP_DOMAIN[10:0]: csr_default = 32'(ADP_GPTP_DOMAIN_C);
      A_AAF_CTRL[10:0]:   csr_default = 32'h0002_0000;
      A_AAF_DMLO[10:0]:   csr_default = 32'hF000_FE01;
      A_AAF_DMHI[10:0]:   csr_default = 32'h0000_91E0;
      A_LWSRP_CTRL[10:0]: csr_default = LWSRP_CTRL_RST_C;
      A_LWSRP_VID[10:0]:  csr_default = LWSRP_VID_RST_C;
      A_LWSRP_DMLO[10:0]: csr_default = LWSRP_DMAC_LO_RST_C;
      A_LWSRP_DMHI[10:0]: csr_default = LWSRP_DMAC_HI_RST_C;
      A_LWSRP_TSPEC[10:0]: csr_default = LWSRP_TSPEC_RST_C;
      A_TCAM_CTRL[10:0]:  csr_default = 32'h1;
      A_LINK_CTRL[10:0]:  csr_default = 32'h1;   // link assumed up at boot
      A_LPF_CTRL[10:0]:   csr_default = 32'h1;   // playback LPF on by default
      A_MAAP_CTRL[10:0]:  csr_default = 32'h0000_0800;   // count=8, en=0
      default: begin
        if (a >= A_CBS_BASE[10:0] && a < A_CBS_END[10:0]) begin
          case (a[4:0])
            5'h00:   csr_default = CBS_IDLE_RST[a[5 +: QW]][31:0];
            5'h04:   csr_default = CBS_HI_RST[a[5 +: QW]][31:0];
            5'h08:   csr_default = CBS_LO_RST[a[5 +: QW]][31:0];
            default: csr_default = 32'h0;   // CTRL: en resets 0
          endcase
        end
      end
    endcase
  endfunction

  //! plain-RW register (readback == stored word): served by the shadow.
  //! Strobe/W1C/live registers and unmapped addresses are NOT shadow-written.
  function automatic logic is_plain_rw(input [ADDR_WIDTH-1:0] a);
    is_plain_rw = 1'b0;
    unique case (a)
      A_SCRATCH, A_IRQ_MASK,
      A_MAC_CTRL, A_MAC_IFG, A_MAC_ALO, A_MAC_AHI, A_MC_LO, A_MC_HI,
      //! A_PHY_RST / A_LINK_CTRL are NOT here (ETH GUARD, USER 08-06): their
      //! writes gate on eth_guard, so the readback serves the FLOPS via
      //! live_mux - a refused write must never read back as accepted
      A_CLS_CTRL, A_CLS_DPCP, A_CLS_MAP, A_CLS_REGEN, A_CLS_TCQ,
      A_PTP_CTRL, A_PTP_INCR, A_PTP_ADJ, A_PTP_TWLO, A_PTP_TWHI,
      A_PTP_OFLO, A_PTP_OFHI, A_PTP_ILAT, A_PTP_ELAT,
      A_ADP_CTRL, A_ADP_EIDLO, A_ADP_EIDHI, A_ADP_MIDLO, A_ADP_MIDHI,
      //! A_ADP_TALK / A_ADP_LIST are NOT here: RO shape (VERSION 0x0015)
      A_ADP_ECAPS, A_ADP_CCAPS, A_ADP_GMLO,
      A_ADP_GMHI, A_ADP_DOMAIN, A_ADP_IDX0, A_ADP_IDX1, A_ADP_ASLO, A_ADP_ASHI,
      A_AAF_CTRL, A_AAF_DMLO, A_AAF_DMHI, A_ACMP_LOBS,
      A_LWSRP_CTRL, A_LWSRP_VID, A_LWSRP_DMLO, A_LWSRP_DMHI,
      A_LWSRP_TSPEC, A_LWSRP_LAT,
      A_TCAM_CTRL, A_TCAM_KLO, A_TCAM_KHI, A_TCAM_MLO, A_TCAM_MHI, A_TCAM_ACT,
      A_MAAP_CTRL, A_TONE_CTRL, A_GPTP_PDELAY,
      A_ENT_NAME_LO, A_ENT_NAME_HI, A_LPF_CTRL, A_AS2_LO, A_AS2_HI,
      A_CRF_SIDLO, A_CRF_SIDHI,
      //! A_CRFT_CTRL is NOT here: live read (status above the RW bits)
      A_CRFT_SIDLO, A_CRFT_SIDHI, A_CRFT_DMLO, A_CRFT_DMHI,
      A_REST_TKLO, A_REST_TKHI, A_REST_META, A_REST_CTLO, A_REST_CTHI,
      //! J4 AS_PATH staging pair: plain-RW like the E1 staging words.
      //! A_ASP_CMD is NOT here - it reads the LIVE {gen, count}, never the
      //! command word that was written.
      A_ASP_LO, A_ASP_HI:
        is_plain_rw = 1'b1;
      default:
        if (a >= A_CBS_BASE && a < A_CBS_END)
          is_plain_rw = (a[4:0] == 5'h00) || (a[4:0] == 5'h04) ||
                        (a[4:0] == 5'h08) || (a[4:0] == 5'h0C);
    endcase
  endfunction

  //! CBS_CTRL readback is masked to bit 0: shadow stores the READBACK value
  wire is_cbs_en_wr = (wr_addr >= A_CBS_BASE) && (wr_addr < A_CBS_END) &&
                      (wr_addr[4:0] == 5'h0C);
  wire [31:0] shadow_wval = is_cbs_en_wr ? {31'h0, s_axi_wdata[0]} : s_axi_wdata;

  //! P11 window hard-alias writes (talker index 0): the window word IS the
  //! flat AAF register, so the flat address's shadow readback must follow —
  //! redirect the shadow write to the flat address with the merged value
  wire win_alias_ctrl_w = wr_fire && (wr_addr == A_STRMW_CTRL) &&
                          strm_dir_r && (strm_idx_r == 4'd0);
  wire win_alias_dmlo_w = wr_fire && (wr_addr == A_STRMW_DMAC_LO) &&
                          strm_dir_r && (strm_idx_r == 4'd0);
  wire win_alias_dmhi_w = wr_fire && (wr_addr == A_STRMW_DMAC_HI) &&
                          strm_dir_r && (strm_idx_r == 4'd0);
  wire win_alias_we_w   = win_alias_ctrl_w || win_alias_dmlo_w || win_alias_dmhi_w;

  (* ram_style = "block" *) logic [31:0] shadow_ram [0:511];
  (* ram_style = "block" *) logic [31:0] dflt_rom   [0:511];
  initial begin
    for (int k = 0; k < 512; k++) dflt_rom[k] = csr_default(11'(k * 4));
  end

  logic [31:0] shadow_q, dflt_q;
  wire         shadow_axi_we = wr_fire && !(|wr_addr[ADDR_WIDTH-1:11]) &&
                               is_plain_rw(wr_addr);
  //! sweep pipeline: ROM word for sweep_cnt lands one cycle later
  wire         sweep_wr = sweep_busy && (sweep_cnt >= 10'd1) && (sweep_cnt <= 10'd512);

  //! single muxed write port: two `if` arms with distinct address expressions
  //! infer TWO write ports and push the RAM to LUTRAM (Synth 8-6849 infeasible)
  wire         sh_we    = sweep_wr || shadow_axi_we || win_alias_we_w;
  wire [8:0]   sh_waddr = sweep_wr         ? 9'(sweep_cnt - 10'd1)
                        : win_alias_ctrl_w ? A_AAF_CTRL[10:2]
                        : win_alias_dmlo_w ? A_AAF_DMLO[10:2]
                        : win_alias_dmhi_w ? A_AAF_DMHI[10:2]
                        : wr_addr[10:2];
  wire [31:0]  sh_wdata = sweep_wr         ? dflt_q
                        : win_alias_ctrl_w ? {aaf_ctrl[31:1], s_axi_wdata[0]}
                        : shadow_wval;

  always_ff @(posedge aclk) begin : shadow_mem
    dflt_q <= dflt_rom[sweep_cnt[8:0]];
    if (sh_we)
      shadow_ram[sh_waddr] <= sh_wdata;
    shadow_q <= shadow_ram[rd_addr[10:2]];
  end

  always_ff @(posedge aclk) begin : shadow_sweep
    if (!aresetn) begin
      sweep_busy <= 1'b1;
      sweep_cnt  <= 10'd0;
    end else if (sweep_busy) begin
      sweep_cnt <= sweep_cnt + 10'd1;
      if (sweep_cnt == 10'd513) sweep_busy <= 1'b0;
    end
  end

  // ==========================================================================
  //  protocol-processor control plane window (0x920-0x930)
  // ==========================================================================
  //! The side port is a FABRIC walk behind a request/ack: an AXI read must
  //! never wait on it (the bus would stall for as long as the processor takes
  //! to answer), so the access is POSTED — write SPADDR to arm a read, poll
  //! PP_STAT[0] (sp_busy), then read SPDATA. A write to SPDATA posts a side-
  //! port WRITE to the address already in SPADDR. One access outstanding: a
  //! request offered while busy is REFUSED, not queued, so software can never
  //! read one address's answer believing it asked for another.
  logic [31:0] pp_rd_data_w;
  logic        pp_rd_hit_w;

  //! UNCONDITIONAL since the legacy 1722.1/SRP plane was deleted: the
  //! processor is not an option, it is the control plane, so there is no
  //! plane-absent arm to fold away and no parameter to elaborate it behind.
  if (1) begin : g_pp_csr
    logic [31:0] pp_ctrl_r;
    logic [19:0] pp_spaddr_r;
    logic [31:0] pp_sprdata_r;
    logic        pp_busy_r, pp_err_r;
    logic        pp_req_r, pp_we_r;
    logic [31:0] pp_wdata_r;

    always_ff @(posedge aclk) begin : pp_regs
      if (!aresetn) begin
        pp_ctrl_r    <= 32'h0;
        pp_spaddr_r  <= 20'h0;
        pp_sprdata_r <= 32'h0;
        pp_busy_r    <= 1'b0;
        pp_err_r     <= 1'b0;
        pp_req_r     <= 1'b0;
        pp_we_r      <= 1'b0;
        pp_wdata_r   <= 32'h0;
      end else begin
        pp_req_r <= 1'b0;               //! single-cycle strobe
        if (wr_fire) begin
          unique case (wr_addr)
            A_PP_CTRL:   pp_ctrl_r <= s_axi_wdata;
            //! arming a read: latch the address AND post the request
            A_PP_SPADDR: begin
              pp_spaddr_r <= s_axi_wdata[19:0];
              if (!pp_busy_r) begin
                pp_req_r  <= 1'b1;
                pp_we_r   <= 1'b0;
                pp_busy_r <= 1'b1;
                pp_err_r  <= 1'b0;
              end
            end
            //! posting a write to the address already armed
            A_PP_SPDATA: begin
              if (!pp_busy_r) begin
                pp_wdata_r <= s_axi_wdata;
                pp_req_r   <= 1'b1;
                pp_we_r    <= 1'b1;
                pp_busy_r  <= 1'b1;
                pp_err_r   <= 1'b0;
              end
            end
            default: ;
          endcase
        end
        if (pp_busy_r && i_pp_ack) begin
          pp_busy_r    <= 1'b0;
          pp_err_r     <= i_pp_err;
          pp_sprdata_r <= i_pp_rdata;
        end
      end
    end

    assign o_pp_enable     = pp_ctrl_r[0];
    assign o_pp_restore_go = pp_ctrl_r[1];
    assign o_pp_req        = pp_req_r;
    assign o_pp_we         = pp_we_r;
    assign o_pp_addr       = pp_spaddr_r;
    assign o_pp_wdata      = pp_wdata_r;

    always_comb begin : pp_read
      pp_rd_hit_w  = 1'b1;
      pp_rd_data_w = 32'h0;
      unique case (rd_addr_q)
        A_PP_CTRL:   pp_rd_data_w = pp_ctrl_r;
        A_PP_STAT:   pp_rd_data_w = {PP_PRESENT_TAG_C, 16'd0,
                                     i_pp_nvm_blank, i_pp_nvm_backed,
                                     pp_err_r,
                                     i_pp_nvm_alarm, i_pp_restore_fail,
                                     i_pp_restore_done, i_pp_restore_busy,
                                     pp_busy_r};
        A_PP_SPADDR: pp_rd_data_w = {12'd0, pp_spaddr_r};
        A_PP_SPDATA: pp_rd_data_w = pp_sprdata_r;
        A_PP_DIAG:   pp_rd_data_w = {i_pp_tx_frames, i_pp_rx_drops,
                                     i_pp_rx_frames[7:0]};
        default:     pp_rd_hit_w  = 1'b0;
      endcase
    end
  end

  // ==========================================================================
  //  Read decode — LIVE registers only (status/W1C/counters/windows); every
  //  plain-RW config register reads from the shadow BRAM.
  // ==========================================================================
  logic [31:0] live_mux;
  logic        live_hit;

  always_comb begin : read_mux
    logic [ADDR_WIDTH-1:0] soff;         //! STAT window offset
    logic [ADDR_WIDTH-1:0] loff;         //! LTAP RO-word offset
    logic [ADDR_WIDTH-1:0] aoff;         //! APRB RO-word offset
    logic [ADDR_WIDTH-1:0] poff;         //! PBK RO-word offset
    live_mux = 32'h0;
    live_hit = 1'b1;
    soff = rd_addr_q - A_STATS_BASE;
    loff = rd_addr_q - A_LTAP_BASE;
    aoff = rd_addr_q - A_APRB_BASE;
    poff = rd_addr_q - A_PBK_BASE;
    unique case (rd_addr_q)
      A_IRQ_STATUS: live_mux = irq_status;
      A_IRQ_RAW:    live_mux = irq_status;
      A_MAC_STATUS: live_mux = { 28'h0, i_full_duplex, i_speed, i_link_up };
      //! RMON lane capability mask - read this BEFORE believing a zero STAT
      A_STATS_CAP:  live_mux = i_stats_cap;
      A_PTP_TRLO:   live_mux = ptp_tod_rd[31:0];
      A_PTP_TRHI:   live_mux = ptp_tod_rd[63:32];
      A_ADP_STATUS: live_mux = i_adp_available_index;       // RO available_index
      A_ADP_DIAG:   live_mux = {14'd0, i_adp_depart_src, i_adp_rearm_cnt, i_adp_depart_cnt};
      //! ADP liveness in ONE read (VERSION 0x001D): sent_cnt moving = the
      //! advertiser is emitting, state[0] = the available_r that 0x668 could
      //! only describe by its absence, disc_seen vs disc_rx = whether anyone
      //! is discovering and whether they mean us.
      A_ADP_DIAG2:  live_mux = {i_adp_state, i_adp_last_msg, adp_disc_seen_cnt_r,
                                i_adp_disc_rx_cnt, i_adp_sent_cnt};
      // AECP: [16]=locked, [15:0]=cmd_count | resp_count[31:16], current_config[15:0]
      A_AECP_STAT0: live_mux = {15'd0, i_aecp_locked, i_aecp_cmd_count};
      A_AECP_STAT1: live_mux = {i_aecp_resp_count, i_aecp_current_config};
      A_ACMP_STAT:  live_mux = {i_acmp_resp_count, i_acmp_cmd_count};
      //! ETH GUARD family: truth from the flops (see is_plain_rw carve-out)
      A_PHY_RST:    live_mux = phy_rst;
      A_LINK_CTRL:  live_mux = link_ctrl;
      A_ETH_GUARD:  live_mux = {31'd0, eth_guard};
      A_ACMP_TALKER: live_mux = {28'd0, i_aaf_gate, o_acmp_lobs, i_acmp_talker_active, i_acmp_probe_armed};
      A_AAF_FRAMES: live_mux = i_aaf_frames;
      A_AAF_PAIRS:  live_mux = i_aaf_pairs;
      A_LWSRP_STATUS: live_mux = i_lwsrp_status;
      A_LWSRP_SLOPE: live_mux = i_lwsrp_slope;
      A_LWSRP_CNT:  live_mux = i_lwsrp_cnt;
      A_LWSRP_DOM:  live_mux = i_lwsrp_dom;
      A_ACMPL_STATE: live_mux = i_acmpl_state;
      A_ACMPL_TKLO: live_mux = i_acmpl_talker_lo;
      A_ACMPL_TKHI: live_mux = i_acmpl_talker_hi;
      A_ACMPL_CNT:  live_mux = i_acmpl_cnt;
      A_ACMPL_TUID: live_mux = i_acmpl_tuid;
      A_AVTPRX_STAT: live_mux = i_avtprx_stat;
      A_AVTPRX_FRX:  live_mux = i_avtprx_frx;
      A_AVTPRX_ERR:  live_mux = i_avtprx_err;
      A_PCMRX_CNT:   live_mux = i_pcmrx_cnt;
      A_PCMRX_TS:    live_mux = i_pcmrx_ts;
      A_MAAP_STAT0:  live_mux = i_maap_stat0;
      A_MAAP_STAT1:  live_mux = i_maap_stat1;
      A_I2SPB_STAT:  live_mux = i_i2spb_stat;
      A_I2SPB_TRIM:  live_mux = i_i2spb_trim;
      A_ACMPL_DBG:  live_mux = i_acmpl_dbg;
      A_AVTPRX_TSD: live_mux = i_avtprx_tsd;
      A_RST_EPOCH:  live_mux = {24'd0, rst_epoch_r};
      A_CRF_CTRL:   live_mux = {i_crf_locked, 30'd0, crf_ctrl[0]};
      A_CRF_DELTA:  live_mux = i_crf_delta;
      A_CRF_RATE:   live_mux = i_crf_rate;
      A_CRF_STATUS: live_mux = i_crf_status;
      //! RW bits verbatim in [1:0], live class-A status above them
      A_CRFT_CTRL:  live_mux = {i_crft_stat[31:2], crft_ctrl[1:0]};
      //! E3 journal ingest: CTRL reads the verdict summary bits, STAT the
      //! engine's whole live word, SEQ the accepted-image watermark; DATA
      //! is write-only and falls through to 0
      A_JNL_CTRL:   live_mux = {i_jnl_stat[31:30], 30'd0};
      A_JNL_STAT:   live_mux = i_jnl_stat;
      A_JNL_SEQ:    live_mux = i_jnl_seq;
      //! E4 AEM patch: CTRL reads the engine's whole live status word;
      //! SEL/FIELD/DATA are write-only and fall through to 0
      A_AEMP_CTRL:  live_mux = i_aemp_stat;
      A_CRFT_COUNT: live_mux = i_crft_count;
      A_BDBG0:      live_mux = i_bdbg0;
      A_BDBG1:      live_mux = i_bdbg1;
      A_BDBG2:      live_mux = i_bdbg2;
      A_LINKG_STAT: live_mux = i_linkg_stat;
      A_CLKV_CTRL:  live_mux = clkv_ctrl;   //! [1] always reads 0 (W1S)
      A_CLKV_STAT:  live_mux = i_clkv_stat;
      A_CLKV_TUCNT: live_mux = i_clkv_tucnt;
      A_TXARB_DIAG: live_mux = i_txarb_diag;
      A_MCSRV_STAT: live_mux = i_mcsrv_stat;
      A_MCSRV_CTRL: live_mux = mcsrv_ctrl;
      //! LTAP_CTRL: module status ({stage,active}) with enable OR-ed into [1]
      A_LTAP_CTRL:  live_mux = i_ltap_status | {30'd0, ltap_en_r, 1'b0};
      A_CHMAP_CTRL: live_mux = chmap_ctrl;
      A_CHMAP_SEL:  live_mux = chmap_sel;
      A_CHMAP_WORD: live_mux = {16'd0, chmap_word[15:0]};
      A_CHMAP_STAT: live_mux = {8'd0, chmap_refused, chmap_commits};
      //! map-RAM readback: status word (tagged, so 0 = "no such register")
      //! and the latched map word (POISON while there is no measurement).
      //! Both are explicit case arms, so they take priority over the
      //! reserved-chmap-words-read-0 branch in the default below.
      A_CHMAP_SNAP: live_mux = chmap_snap_rd_w;
      A_CHMAP_LOOP: live_mux = chmap_loop_rd_w;
      A_I2SPB_DBG:  live_mux = i_i2spb_dbg;
      //! gh #59: probes sent / replies seen / controllers shed. All three
      //! climb together on a healthy bench (each probe is answered); a
      //! climbing eviction count with a static reply count is a controller
      //! that died without deregistering, which is the whole point of
      //! Milan 5.4.5.3.
      A_CTLR_DIAG:  live_mux = i_ctlr_diag;
      //! E1 commit readback: {busy, done, 20'0, status, 4'0, idx}
      A_REST_CMD:   live_mux = {rest_pend_r, rest_done_r, 20'd0,
                                rest_stat_r, 4'd0, rest_idx_r};
      //! J4 publish readback: the LIVE generation and path length, i.e. what
      //! GET_AS_PATH will actually serve - not the command word software
      //! wrote. A read of 0 means "no path published" = the legacy arm.
      A_ASP_CMD:    live_mux = {24'd0, asp_gen_r, asp_count_r};
      default: begin
        if (rd_addr_q >= A_STATS_BASE && rd_addr_q < A_STATS_END)
          live_mux = stat_snap[soff[2 +: 4]];
        else if (rd_addr_q >= A_LTAP_BASE && rd_addr_q < A_LTAP_END)
          live_mux = i_ltap_regs[32*32'(loff[5:2]) +: 32];  //! 16 packed RO words
        else if (rd_addr_q >= A_APRB_BASE && rd_addr_q < A_APRB_END)
          live_mux = i_aprb_regs[32*32'(aoff[4:2]) +: 32];  //! 5 packed RO words
        else if (rd_addr_q >= A_PBK_BASE && rd_addr_q < A_PBK_END)
          live_mux = i_pbk_regs[32*32'(poff[3:2]) +: 32];   //! 3 packed RO words
        else if (rd_addr_q >= A_CHMAP_CTRL &&
                 rd_addr_q <  A_CHMAP_CTRL + 16'h40)
          live_mux = 32'h0;               //! reserved chmap words read 0 (never shadow)
        else
          live_hit = 1'b0;                //! -> shadow (or 0 above the window)
      end
    endcase
    //! The PP window (0x920-0x930) sits INSIDE the chmap 0x900-0x93F carve-out
    //! above, whose reserved arm answers 0 — so this override must come AFTER
    //! the case, not inside it, or every shadow-plane read is a structural
    //! zero indistinguishable from "plane absent". Folds to nothing when
    //! the PP window (pp_rd_hit_w).
    if (pp_rd_hit_w) begin
      live_mux = pp_rd_data_w;
      live_hit = 1'b1;
    end
  end

  // ==========================================================================
  //  P11 indexed per-stream window read view (fast words). Engine port-B
  //  backed words (CTRL/FMT listener side; CTRL/DMAC extra talker contexts)
  //  come through strm_slow_rd_S instead; STATE/CNT0..9/PDUS are served from
  //  the SNAP shadow (the one permitted shadow block); SID/DMAC (listener)
  //  from the ACMP tbl snapshot, SRP from the lwSRP ctx snapshot. Index 0
  //  words with a flat-register twin are HARD ALIASES of those registers.
  // ==========================================================================
  //! station MAC in wire order (first wire byte in [47:40]) — the talker
  //! stream_id derivation {mac, uid = 0} the fabric uses everywhere
  wire [47:0] mac_wire_w = {mac_alo[7:0], mac_alo[15:8], mac_alo[23:16],
                            mac_alo[31:24], mac_ahi[7:0], mac_ahi[15:8]};
  logic [31:0] strm_mux;
  logic        strm_hit;
  always_comb begin : strm_read_mux
    logic [ADDR_WIDTH-1:0] coff;         //! CNT word offset
    coff     = rd_addr_q - A_STRMW_CNT0;
    strm_hit = (rd_addr_q >= A_STRM_SEL) && (rd_addr_q < A_STRMW_END);
    strm_mux = 32'h0;
    if (rd_addr_q == A_STRM_SEL)
      strm_mux = {23'd0, strm_dir_r, 4'd0, strm_idx_r};
    else if (rd_addr_q == A_STRM_SNAP)
      strm_mux = {31'd0, snap_busy_r};
    else if (win_in_range_w) begin       //! out-of-range idx: reads 0
      case (rd_addr_q)
        A_STRMW_CTRL:
          if (strm_dir_r && strm_idx_r == 4'd0)
            strm_mux = {31'd0, aaf_ctrl[0]};              // = AAF_CTRL[0]
        A_STRMW_SID_LO:
          strm_mux = !strm_dir_r
              ? (acmp_fresh_r ? acmp_sid_q_r[31:0] : 32'd0)
              : (strm_idx_r == 4'd0 ? {mac_wire_w[15:0], 16'd0}
                 : (srp_fresh_r ? i_srp_ctx_rd_sid[31:0] : 32'd0));
        A_STRMW_SID_HI:
          strm_mux = !strm_dir_r
              ? (acmp_fresh_r ? acmp_sid_q_r[63:32] : 32'd0)
              : (strm_idx_r == 4'd0 ? mac_wire_w[47:16]
                 : (srp_fresh_r ? i_srp_ctx_rd_sid[63:32] : 32'd0));
        A_STRMW_DMAC_LO:
          if (!strm_dir_r)
            strm_mux = acmp_fresh_r ? acmp_dmac_q_r[31:0] : 32'd0;
          else if (strm_idx_r == 4'd0)
            strm_mux = aaf_dmlo;                          // = AAF_DMLO
        A_STRMW_DMAC_HI:
          if (!strm_dir_r)
            strm_mux = acmp_fresh_r ? {16'd0, acmp_dmac_q_r[47:32]} : 32'd0;
          else if (strm_idx_r == 4'd0)
            strm_mux = {16'd0, aaf_dmhi[15:0]};           // = AAF_DMHI[15:0]
        A_STRMW_STATE: strm_mux = snap_shadow_r[0];
        A_STRMW_PDUS:  strm_mux = snap_shadow_r[11];
        //! talker-side FMT is AECP-owned - POISON (not zero) marks the word
        //! as not-backed-at-this-dir (2026-07-26 rule; listener FMT is a
        //! slow engine read and never reaches this arm)
        A_STRMW_FMT_LO, A_STRMW_FMT_HI:
          if (strm_dir_r) strm_mux = 32'hDEAD_DEAD;
        A_STRMW_SRP:
          //! the idx-0 hard alias of 0x694 yields to the [9] listener-0 row
          //! select, which reads the DEDICATED row through the poll engine
          //! like any extension row
          strm_mux = ((strm_idx_r == 4'd0) && !srp_idx0_ls_w)
                     ? i_lwsrp_status                        // = 0x694
                     : (srp_fresh_r ? {16'd0, i_srp_ctx_rd_stat} : 32'd0);
        //! E2: the remaining persisted binding fields (5.5.2.4/5.5.3.5.3),
        //! listener contexts only — talker dir reads 0
        A_STRMW_CTLR_LO:
          strm_mux = !strm_dir_r
              ? (acmp_fresh_r ? acmp_ctlr_q_r[31:0] : 32'd0)
              : 32'hDEAD_DEAD;           //! talker dir: not backed - POISON
        A_STRMW_CTLR_HI:
          strm_mux = !strm_dir_r
              ? (acmp_fresh_r ? acmp_ctlr_q_r[63:32] : 32'd0)
              : 32'hDEAD_DEAD;
        A_STRMW_BIND:
          strm_mux = !strm_dir_r
              ? (acmp_fresh_r ? {acmp_flags_q_r, acmp_tuid_q_r} : 32'd0)
              : 32'hDEAD_DEAD;
        default:
          if (rd_addr_q >= A_STRMW_CNT0 && rd_addr_q < A_STRMW_CNT_END)
            strm_mux = snap_shadow_r[1 + 32'(coff[5:2])];
          else if (rd_addr_q == ADDR_WIDTH'('h86C))
            strm_mux = 32'hDEAD_DEAD;    //! window hole: POISON, not zero
      endcase
    end
  end

  //! Register read data one cycle after the AR handshake (BRAM latency);
  //! RDATA is held stable while RVALID is asserted. Slow (engine port-B)
  //! window reads latch on the fetch-done beat instead.
  //! reads at/above 0x800 return 0 unless a mapped block claims them: the
  //! 0x800 stream window (strm_hit, priority above) or the servo word at
  //! 0x8F8 (2026-07-23: this term was missing, so A_MCSRV_STAT read 0 on
  //! EVERY build while the servo ran fine - caught by the [SERVO] dp-TB leg)
  wire rd_in_window = ~|rd_addr_q[ADDR_WIDTH-1:11] ||
                      (rd_addr_q == A_MCSRV_STAT) ||
                      (rd_addr_q == A_MCSRV_CTRL) ||
                      //! item-11 LTAP group (CTRL 0x870 + 16 RO words) lives
                      //! >=0x800, so it needs the same carve-out as the servo
                      ((rd_addr_q >= A_LTAP_CTRL) && (rd_addr_q < A_LTAP_END)) ||
                      //! parser-probe group 0x8B4-0x8C4, same carve-out
                      ((rd_addr_q >= A_APRB_BASE) && (rd_addr_q < A_APRB_END)) ||
                      //! item-7 playback-chain probe 0x8C8-0x8D0, same rule
                      ((rd_addr_q >= A_PBK_BASE) && (rd_addr_q < A_PBK_END)) ||
                      //! chmap 0x900-0x93F window (else the 0x8F8 dead-read trap)
                      (rd_addr_q >= A_CHMAP_CTRL &&
                       rd_addr_q <  A_CHMAP_CTRL + 16'h40);
  always_ff @(posedge aclk) begin : read_data_reg
    if (!aresetn) begin
      r_data <= 32'h0;
      live_mux_q <= 32'h0; strm_mux_q <= 32'h0; shadow_qq <= 32'h0;
      live_hit_q <= 1'b0;  strm_hit_q <= 1'b0;  rd_in_window_q <= 1'b0;
    end else begin
      //! stage 1: the wide case trees terminate HERE (their whole cost)
      if (rd_pend) begin
        live_mux_q     <= live_mux;
        live_hit_q     <= live_hit;
        strm_mux_q     <= strm_mux;
        strm_hit_q     <= strm_hit;
        rd_in_window_q <= rd_in_window;
        shadow_qq      <= shadow_q;
      end
      //! stage 2: a four-way select of registered words - shallow by
      //! construction, whatever the register map grows to
      if (rd_pend2)
        r_data <= strm_hit_q      ? strm_mux_q
                : !rd_in_window_q ? 32'h0
                : live_hit_q      ? live_mux_q
                : shadow_qq;
      else if (rds_done_w)
        r_data <= rds_dir_r ? i_tctx_rd_data : i_lctx_rd_data;
    end
  end

  // ==========================================================================
  //  Output wiring (register fields -> flat config ports)
  // ==========================================================================
  assign o_mac_tx_en    = mac_ctrl[0];
  assign o_mac_rx_en    = mac_ctrl[1];
  assign o_mac_promisc  = mac_ctrl[2];
  assign o_mac_allmulti = mac_ctrl[3];
  //! REQ-MAC-03: the link rate now FOLLOWS the MAC's reported speed by default.
  //! It used to be MAC_CTRL[4] alone, whose reset is 1 - so on a 100 Mb/s port
  //! (the Arty MII DP83848, i_speed = 01) every is_1g consumer believed it was
  //! on a gigabit link until software wrote the register. That is not cosmetic:
  //! `is_1g` sets the lwSRP bandwidth gate's admission limit (750 Mb/s vs
  //! 75 Mb/s) and the CBS sendSlope denominator, so a 100 Mb/s port was
  //! admitting reservations against a 10x-too-large budget and computing
  //! sendSlope against the wrong line rate. MAC_CTRL[5] = speed_manual keeps
  //! the old behaviour available (1 = use MAC_CTRL[4] verbatim); reset 0 =
  //! follow the PHY/MAC. i_speed is already the CDC-synced value that
  //! MAC_STATUS reports, so the register and the datapath can no longer
  //! disagree about the link rate.
  assign o_mac_is_1g    = mac_ctrl[5] ? mac_ctrl[4] : (i_speed == 2'd2);
  assign o_mac_ifg      = mac_ifg[7:0];
  assign o_mac_addr     = {mac_ahi[15:0], mac_alo};
  assign o_mc_hash      = {mc_hi, mc_lo};
  assign o_phy_reset_n  = phy_rst[0];

  assign o_stats_snapshot = stats_snap_p;
  assign o_stats_reset    = stats_rst_p;

  assign o_cls_use_pcp      = cls_ctrl[0];
  assign o_cls_dmac_check   = cls_ctrl[1];
  assign o_cls_ctrl_class   = cls_ctrl[2];
  assign o_cls_default_pcp  = cls_dpcp[2:0];
  assign o_cls_pcp_tc_map   = cls_map[23:0];
  assign o_cls_prio_regen   = cls_regen[23:0];
  assign o_cls_tc_queue_map = cls_tcq;

  genvar g;
  generate
    for (g = 0; g < NUM_QUEUES; g = g + 1) begin : gen_cbs_out
      assign o_cbs_idle_slope[g*32 +: 32] = cbs_idle[g];
      assign o_cbs_hi_credit [g*32 +: 32] = cbs_hi[g];
      assign o_cbs_lo_credit [g*32 +: 32] = cbs_lo[g];
      assign o_cbs_enable[g]              = cbs_en[g];
    end
  endgenerate

  assign o_ptp_enable       = ptp_ctrl[0];
  assign o_ptp_incr         = ptp_incr;
  assign o_ptp_adj          = ptp_adj;
  assign o_ptp_tod_wr       = {ptp_twhi, ptp_twlo};
  assign o_ptp_offset       = {ptp_ofhi, ptp_oflo};
  assign o_ptp_cmd_load     = ptp_load_p;
  assign o_ptp_cmd_adjust   = ptp_adj_p;
  assign o_ptp_cmd_snapshot = ptp_snap_p;
  assign o_ptp_ingress_lat  = ptp_ilat;
  assign o_ptp_egress_lat   = ptp_elat;

  assign o_aaf_enable          = aaf_ctrl[0];
  assign o_aaf_bypass          = aaf_ctrl[1];
  assign o_acmp_lobs           = acmp_lobs[0];
  assign o_tone_enable      = tone_ctrl[0];
  assign o_mcsrv_ps_invert  = mcsrv_ctrl[0];
  assign o_mcsrv_auto_repair = mcsrv_ctrl[1];
  assign o_ltap_en          = ltap_en_r;
  assign o_ltap_clr         = ltap_clr_p;
  assign o_chmap_enable   = chmap_ctrl[0];
  assign o_chmap_wr_en    = chmap_wr_p;
  assign o_chmap_wr_side  = chmap_sel[8];
  assign o_chmap_wr_addr  = chmap_sel[5:0];
  assign o_chmap_wr_data  = chmap_word[15:0];

  // ==========================================================================
  //  chmap map-RAM READBACK (CHMAP_SNAP 0x910 / CHMAP_LOOP 0x914)
  //
  //  WHY THIS EXISTS. CHMAP_WORD 0x908 reads back this block's OWN SHADOW of
  //  the last word software wrote. It has never been able to say what the map
  //  RAM holds, and until now nothing could: milan_datapath tied both RAMs'
  //  read ports off (map_rd_en_i = 1'b0, map_rd_data_o unconnected), so the
  //  AEM projector could rewrite the render map underneath software and the
  //  0x908 readback would not move, and a CAPTURE slot that is mapped but has
  //  never been fed emits 24'd0 - bit-identical to a working-and-quiet slot.
  //  That is the structural zero methodology R5 forbids, and it is why a
  //  mis-wired loopback on a board with no audio pins could only be guessed
  //  at from "frames counting but payload all zeros".
  //
  //  ORACLE: the fabric. The value reported here is the word the map RAM
  //  returned on its read port, or nothing at all - never a reconstruction.
  //
  //  DISCIPLINE: CHMAP_SEL 0x904 -> W1S CHMAP_SNAP 0x910 -> poll
  //  CHMAP_SNAP[0] busy -> read CHMAP_LOOP 0x914. That is the 0x800 window's
  //  SEL/SNAP/poll/read shape, deliberately, with its one trap fixed: the
  //  0x800 window's data words read ZERO before their SNAP is armed, which
  //  is indistinguishable from a dead block. CHMAP_LOOP reads
  //  0xDEADDEAD (the house not-a-measurement sentinel) whenever there is no
  //  completed snapshot behind it - un-armed, timed out, or refused.
  //
  //  ACCOUNTABILITY: CHMAP_RDBK_P is a DECLARATION by the instantiator and
  //  the watchdog is what holds it to the wire. Declared-absent -> the arm
  //  is refused outright (CHMAP_SNAP[3] unsup) and no request is issued.
  //  Declared-present but silent -> CHMAP_SNAP[2] timeout after
  //  CHMAP_RD_WDOG_C clocks, and the data word stays POISON. In neither case
  //  does a zero appear that software could mistake for a map entry.
  // ==========================================================================
  wire cmrd_go_w  = wr_fire && (wr_addr == A_CHMAP_SNAP) && s_axi_wdata[0] &&
                    !cmrd_busy_r;
  wire cmrd_cap_w = CHMAP_RDBK_C[chmap_sel[8]];  //! this side's port is wired

  always_ff @(posedge aclk) begin : chmap_rd_S
    if (!aresetn) begin
      cmrd_busy_r  <= 1'b0; cmrd_flush_r <= 1'b0; cmrd_valid_r <= 1'b0;
      cmrd_to_r    <= 1'b0; cmrd_unsup_r <= 1'b0; cmrd_armed_r <= 1'b0;
      cmrd_side_r  <= 1'b0; cmrd_addr_r  <= 6'd0; cmrd_data_r  <= 16'h0;
      cmrd_wd_r    <= 4'd0;
    end else if (cmrd_go_w) begin
      //! a new arm clears the PREVIOUS verdict: a stale valid must never be
      //! read as this snapshot's answer
      cmrd_armed_r <= 1'b1;
      cmrd_valid_r <= 1'b0;
      cmrd_to_r    <= 1'b0;
      cmrd_side_r  <= chmap_sel[8];
      cmrd_addr_r  <= chmap_sel[5:0];
      cmrd_unsup_r <= !cmrd_cap_w;
      if (cmrd_cap_w) begin
        cmrd_busy_r  <= 1'b1;
        cmrd_flush_r <= 1'b1;          //! ignore a valid in flight for the last request
        cmrd_wd_r    <= CHMAP_RD_WDOG_C;
      end
    end else if (cmrd_busy_r) begin
      if (cmrd_flush_r) begin
        cmrd_flush_r <= 1'b0;
        cmrd_wd_r    <= cmrd_wd_r - 4'd1;
      end else if (i_chmap_rd_valid) begin
        cmrd_data_r  <= i_chmap_rd_data;   //! the fabric's word, verbatim
        cmrd_valid_r <= 1'b1;
        cmrd_busy_r  <= 1'b0;
      end else if (cmrd_wd_r == 4'd0) begin
        //! declared but never answered: report it, do NOT latch the bus
        cmrd_to_r   <= 1'b1;
        cmrd_busy_r <= 1'b0;
      end else begin
        cmrd_wd_r <= cmrd_wd_r - 4'd1;
      end
    end
  end : chmap_rd_S

  assign o_chmap_rd_en   = cmrd_busy_r;
  assign o_chmap_rd_side = cmrd_side_r;
  assign o_chmap_rd_addr = cmrd_addr_r;

  assign o_i2spb_clr_under  = i2spb_clru_p;
  assign o_i2spb_clr_over   = i2spb_clro_p;
  assign o_tone_att         = tone_ctrl[3:1];
  //! Reset-epoch canary: counts datapath reset RELEASES in flops WITHOUT a
  //! reset clause (bitstream-init 0, survive axis resets). Software compares
  //! epochs to detect hidden fabric resets that the config shadow masks
  //! (the 2026-07-19 link-bounce forensics: CSR reads lied after a reset).
  reg [7:0] rst_epoch_r = 8'd0;
  reg       rstn_seen_r = 1'b0;
  always @(posedge aclk) begin : epoch_cnt
    rstn_seen_r <= aresetn;
    if (aresetn && !rstn_seen_r) rst_epoch_r <= rst_epoch_r + 8'd1;
  end : epoch_cnt

  //! ENTITY_DISCOVER witness counter (A_ADP_DIAG2[23:16]). The pulse arrives
  //! from KL_aecp_ingress in THIS clock (aclk == the datapath axis_clk in both
  //! integrations - milan_datapath and milan_top wire .aclk(axis_clk)), so no
  //! CDC. It counts every ADP ENTITY_DISCOVER on the wire including the ones
  //! aimed at other entities, which is what makes "nobody is discovering"
  //! readable instead of inferable. Wraps at 256, like every other DIAG lane.
  always_ff @(posedge aclk) begin : adp_disc_seen_cnt
    if (!aresetn) adp_disc_seen_cnt_r <= 8'd0;
    else if (i_adp_disc_seen_p) adp_disc_seen_cnt_r <= adp_disc_seen_cnt_r + 8'd1;
  end : adp_disc_seen_cnt

  //! entity_name8: byte k of the name = the k-th ASCII char; the AEM store
  //! picks big-endian (byte 0 first), so map LO[7:0]=char0 .. HI[31:24]=char7
  assign o_entity_name8     = {ent_name_lo[7:0],  ent_name_lo[15:8],
                               ent_name_lo[23:16], ent_name_lo[31:24],
                               ent_name_hi[7:0],  ent_name_hi[15:8],
                               ent_name_hi[23:16], ent_name_hi[31:24]};
  assign o_lpf_enable       = lpf_ctrl[0];
  assign o_clkv_wr_p        = clkv_wr_p;
  assign o_clkv_sync_ok     = clkv_ctrl[0];
  assign o_clkv_disc_p      = clkv_disc_p;
  assign o_clkv_as_cap      = clkv_ctrl[2];
  assign o_clkv_wdog_q      = clkv_ctrl[15:4];
  assign o_crf_en           = crf_ctrl[0];
  assign o_crf_sid          = {crf_sidhi, crf_sidlo};
  assign o_crft_en          = crft_ctrl[0];
  assign o_crft_class_a     = crft_ctrl[1];
  assign o_crft_sid         = {crft_sidhi, crft_sidlo};
  assign o_crft_dest_mac    = {crft_dmhi[15:0], crft_dmlo};
  assign o_as_parent_ckid   = {as2_hi, as2_lo};
  //! J4: the committed PathTrace tail, flattened slot 1 first. The builder
  //! reads bit [64*(k-1) +: 64] as entry k of the served path sequence;
  //! entry 0 is the grandmaster and comes from ADP_GM, never from here.
  generate
    for (genvar gk = 0; gk < ASP_SLOTS_C; gk++) begin : g_asp_flat
      assign o_asp_path[64*gk +: 64] = asp_slot_r[gk];
    end
  endgenerate
  assign o_asp_count        = asp_count_r;
  assign o_asp_gen          = asp_gen_r;
  assign o_sw_link          = link_ctrl[0];
  assign o_mac_reinit       = link_ctrl[1];
  assign o_linkg_dis        = link_ctrl[2];
  assign o_linkg_freeze     = link_ctrl[3];
  assign o_maap_enable      = maap_ctrl[0];
  assign o_maap_seed_valid  = maap_ctrl[1];
  assign o_maap_count       = maap_ctrl[15:8];
  assign o_maap_seed_offset = maap_ctrl[31:16];

  assign o_lwsrp_enable        = lwsrp_ctrl[0];
  assign o_lwsrp_talker_en     = lwsrp_ctrl[1];
  assign o_lwsrp_qidx          = lwsrp_ctrl[4:2];
  //! [5] declare-always bypass, reset 0 (the generated LWSRP_CTRL_RST_C
  //! never sets it): Milan 4.3.3.1 conditions the TalkerAdvertise on a
  //! PROBE_TX within 15 s or a registered Listener attribute; this bit is
  //! the bring-up escape back to the pre-gate always-declare posture
  assign o_lwsrp_decl_bypass   = lwsrp_ctrl[5];
  assign o_lwsrp_vid           = lwsrp_vid[11:0];
  assign o_lwsrp_dest_mac      = {lwsrp_dmhi[15:0], lwsrp_dmlo};
  assign o_lwsrp_max_frame     = lwsrp_tspec[15:0];
  assign o_lwsrp_interval      = lwsrp_tspec[31:16];
  assign o_lwsrp_latency       = lwsrp_lat;
  assign o_aaf_vid             = aaf_ctrl[27:16];
  assign o_aaf_dest_mac        = {aaf_dmhi[15:0], aaf_dmlo};
  assign o_adp_enable          = adp_ctrl[0];
  assign o_adp_valid_time      = adp_ctrl[12:8];
  assign o_adp_entity_id       = {adp_eidhi, adp_eidlo};
  assign o_adp_entity_model_id = {adp_midhi, adp_midlo};
  assign o_adp_entity_caps     = adp_ecaps;
  assign o_adp_talker_sources  = ADP_TALK_C[15:0];
  assign o_adp_talker_caps     = ADP_TALK_C[31:16];
  assign o_adp_listener_sinks  = ADP_LIST_C[15:0];
  assign o_adp_listener_caps   = ADP_LIST_C[31:16];
  assign o_adp_controller_caps = adp_ccaps;
  assign o_adp_gptp_gm         = {adp_gmhi, adp_gmlo};
  assign o_gptp_pdelay_ns      = gptp_pdelay;
  assign o_adp_gptp_domain     = adp_domain[7:0];
  assign o_adp_current_config  = adp_idx0[15:0];
  assign o_adp_identify_index  = adp_idx0[31:16];
  assign o_adp_interface_index = adp_idx1[15:0];
  assign o_adp_association_id  = {adp_ashi, adp_aslo};
  assign o_adp_advertise_p     = adp_adv_p;
  assign o_adp_depart_p        = adp_dep_p;

  assign o_tcam_default_pass = tcam_ctrl[0];
  //! REQ-MAC-02: reset 0 (tcam_ctrl reset 0x1) so the RX path keeps the legacy
  //! blanket default_pass miss policy until software arms the address filter.
  assign o_tcam_addr_filt_en = tcam_ctrl[1];
  assign o_tcam_wr_en        = tcam_wr_p;
  assign o_tcam_wr_index     = tcam_wr_index;
  assign o_tcam_wr_valid     = tcam_wr_valid_r;
  assign o_tcam_wr_key       = {tcam_khi[15:0], tcam_klo};
  assign o_tcam_wr_mask      = {tcam_mhi[15:0], tcam_mlo};
  assign o_tcam_wr_action    = tcam_act[7:0];

  // ==========================================================================
  //  P11 indexed per-stream window engines (NXN_ARCHITECTURE.md §1.5)
  // ==========================================================================
  localparam logic [2:0] SN_IDLE_C = 3'd0, SN_DONE_C = 3'd1, SN_WAIT_C = 3'd2,
                         SN_ARM_C  = 3'd3, SN_FETCH_C = 3'd4;

  wire snap_go_w  = wr_fire && (wr_addr == A_STRM_SNAP) && s_axi_wdata[0] &&
                    !snap_busy_r;
  wire sel_wr_w   = wr_fire && (wr_addr == A_STRM_SEL);
  //! low 9 bits of the selected stream's SRP status word = the STATE[27:19]
  //! SRP summary (single documented rule for both the flat and ctx sources)
  wire [8:0] snap_srp9_w = (snap_idx_r == 4'd0) ? i_lwsrp_status[8:0]
                         : (srp_fresh_r ? i_srp_ctx_rd_stat[8:0] : 9'd0);

  //! SNAP: one coherent latch of {STATE, CNT0..9, PDUS} for the selection.
  //! Index 0 latches the flat-register hard aliases in a single cycle
  //! (coherent by construction); extra contexts run the engine-arbitrated
  //! port-B burst — the engine freezes the stream's words while snap_ok
  //! answers snap_req, which IS the [M-5.4.2.25] GET_COUNTERS atomicity.
  always_ff @(posedge aclk) begin : strm_snap_S
    if (!aresetn) begin
      snap_busy_r <= 1'b0; snap_st_r <= SN_IDLE_C;
      snap_dir_r  <= 1'b0; snap_idx_r <= 4'd0;
      snap_wi_r   <= 4'd0; snap_cyc_r <= 2'd0; snap_word_r <= 5'd0;
      snap_req_r  <= 1'b0; snap_rden_r <= 1'b0; snap_m8_r <= 32'h0;
      for (int w = 0; w < 12; w++) snap_shadow_r[w] <= 32'h0;
    end else begin
      unique case (snap_st_r)
        SN_IDLE_C: if (snap_go_w) begin
          snap_busy_r <= 1'b1;
          snap_dir_r  <= strm_dir_r;
          snap_idx_r  <= strm_idx_r;
          if (!win_in_range_w) begin     //! out-of-range: shadow zeros
            for (int w = 0; w < 12; w++) snap_shadow_r[w] <= 32'h0;
            snap_st_r <= SN_DONE_C;
          end else if (strm_idx_r == 4'd0) begin
            //! index 0 = flat hard alias, Table 7-157 offset order. STATE
            //! is still assembled from the flat status registers; the ten
            //! CNT words come from the monitor's full-width counters
            //! (i_avtprx_cnt10) - see the port doc.
            if (!strm_dir_r) begin
              snap_shadow_r[0]  <= {4'd0, i_lwsrp_status[8:0], 8'd0,
                                    i_avtprx_stat[0],
                                    i_acmpl_state[12:8], i_acmpl_state[14:13],
                                    i_acmpl_state[2:0]};
              //! CNT0..9 = the FULL 32-bit counters (2026-07-26). They used
              //! to be re-derived from the packed 0x6B8/0x6C0 views, so the
              //! window inherited their 8/16-bit truncation and there was NO
              //! full-width path anywhere - the flat views' documented
              //! "read the window for the real number" was not true. MEDIA_
              //! RESET / LATE / EARLY_TIMESTAMP were hard 0 here while the
              //! monitor had been counting them all along.
              for (int w = 0; w < 10; w++)
                snap_shadow_r[1+w] <= i_avtprx_cnt10[w*32 +: 32];
              snap_shadow_r[11] <= i_pcmrx_cnt;                   // = 0x6C4
            end else begin
              snap_shadow_r[0] <= {4'd0, i_lwsrp_status[8:0], 15'd0,
                                   i_aaf_gate, acmp_lobs[0],
                                   i_acmp_talker_active, i_acmp_probe_armed};
              //! talker CNT words don't exist (no Table 7-157 block):
              //! POISON, not zero, so software can discriminate
              //! "not-backed-here" from a true zero count (2026-07-26)
              for (int w = 1; w < 11; w++) snap_shadow_r[w] <= 32'hDEAD_DEAD;
              snap_shadow_r[11] <= i_aaf_frames;                  // = 0x660
            end
            snap_st_r <= SN_DONE_C;
          end else begin
            //! talker contexts have no Table 7-157 block: pre-POISON CNT
            //! (0xDEADDEAD = not-backed-at-this-index, 2026-07-26 rule)
            if (strm_dir_r)
              for (int w = 1; w < 11; w++) snap_shadow_r[w] <= 32'hDEAD_DEAD;
            snap_st_r <= SN_WAIT_C;
          end
        end
        SN_DONE_C: begin
          snap_busy_r <= 1'b0;
          snap_st_r   <= SN_IDLE_C;
        end
        SN_WAIT_C: if (!rds_busy_r) begin  //! yield the port to a read in flight
          snap_req_r <= 1'b1;
          snap_st_r  <= SN_ARM_C;
        end
        SN_ARM_C: if (snap_dir_r ? i_tctx_snap_ok : i_lctx_snap_ok) begin
          snap_rden_r <= 1'b1;
          snap_wi_r   <= 4'd0;
          snap_cyc_r  <= 2'd3;
          snap_word_r <= snap_dir_r ? 5'd5 : 5'd8;  //! TCTX w5 / LCTX w8 first
          snap_st_r   <= SN_FETCH_C;
        end
        SN_FETCH_C: begin
          //! per-word: 4-cycle flush window, then complete on the engine's
          //! rd_valid (P12 valid-driven contract; tied-1 = P11 timing)
          if (snap_cyc_r != 2'd0) snap_cyc_r <= snap_cyc_r - 2'd1;
          else if (!(snap_dir_r ? i_tctx_rd_valid : i_lctx_rd_valid)) begin
            //! engine busy: hold rd_en/addr, wait for its idle slot
          end
          else if (snap_dir_r) begin
            //! talker burst = ONE word: TCTX w5 FRAMES -> PDUS, then compose
            //! STATE with the LIVE per-stream truth vectors (bits [3:0] were
            //! hardwired 0 until 2026-07-26 - the window-honesty fix)
            snap_shadow_r[11] <= i_tctx_rd_data;
            snap_shadow_r[0]  <= {4'd0, snap_srp9_w, 15'd0,
                                  i_tlk_gate_v[snap_idx_r[2:0]],
                                  i_tlk_lobs_v[snap_idx_r[2:0]],
                                  i_tlk_active_v[snap_idx_r[2:0]],
                                  i_tlk_probe_v[snap_idx_r[2:0]]};
            snap_rden_r <= 1'b0; snap_req_r <= 1'b0;
            snap_st_r   <= SN_DONE_C;
          end else begin
            //! listener burst: w8 (state bits) -> w16..w25 (CNT) -> w11 (PDUS)
            unique case (snap_wi_r)
              4'd0:  snap_m8_r <= i_lctx_rd_data;
              4'd11: begin
                snap_shadow_r[11] <= i_lctx_rd_data;
                snap_shadow_r[0]  <= {4'd0, snap_srp9_w,
                                      snap_m8_r[21:14], snap_m8_r[12],
                                      acmp_fresh_r ? acmp_status_q_r  : 5'd0,
                                      acmp_fresh_r ? acmp_probing_q_r : 2'd0,
                                      acmp_fresh_r ? acmp_state_q_r   : 3'd0};
              end
              default: snap_shadow_r[snap_wi_r] <= i_lctx_rd_data;
            endcase
            if (snap_wi_r == 4'd11) begin
              snap_rden_r <= 1'b0; snap_req_r <= 1'b0;
              snap_st_r   <= SN_DONE_C;
            end else begin
              snap_wi_r   <= snap_wi_r + 4'd1;
              snap_word_r <= (snap_wi_r == 4'd0)  ? 5'd16
                           : (snap_wi_r == 4'd10) ? 5'd11
                           : snap_word_r + 5'd1;
              snap_cyc_r  <= 2'd3;
            end
          end
        end
        default: snap_st_r <= SN_IDLE_C;
      endcase
    end
  end : strm_snap_S

  //! slow window read: port-B fetch of an engine-backed word (>= 4 cycles:
  //! flush window + the engine's idle-slot grant, P12 valid-driven)
  always_ff @(posedge aclk) begin : strm_slow_rd_S
    if (!aresetn) begin
      rds_busy_r <= 1'b0; rds_dir_r <= 1'b0; rds_cyc_r <= 2'd0;
      rds_word_r <= 5'd0; rds_idx_r <= 3'd0;
    end else if (!rds_busy_r) begin
      if (rd_fire && rd_is_slow_w) begin
        rds_busy_r <= 1'b1;
        rds_dir_r  <= strm_dir_r;
        rds_idx_r  <= strm_idx_r[2:0];
        rds_cyc_r  <= 2'd3;
        rds_word_r <= !strm_dir_r
            ? ((rd_addr == A_STRMW_CTRL)   ? 5'd4 :
               (rd_addr == A_STRMW_FMT_LO) ? 5'd2 : 5'd3)
            : ((rd_addr == A_STRMW_CTRL)    ? 5'd0 :
               (rd_addr == A_STRMW_DMAC_LO) ? 5'd1 : 5'd2);
      end
    end else begin
      if (rds_cyc_r != 2'd0)   rds_cyc_r <= rds_cyc_r - 2'd1;
      else if (rds_valid_w)    rds_busy_r <= 1'b0;   //! engine answered
    end
  end : strm_slow_rd_S

  //! lwSRP ctx master: continuous status poll of the selected extra row +
  //! one-deep provisioning write queue (committed by a window CTRL write)
  //! listener idx 0 addresses the DEDICATED sink-0 row when this build has
  //! one (SRP_LSN0_ROW_P != 0) - the row-0 legacy pair keeps the talker-0
  //! side, so talker-dir idx 0 stays excluded (flat CSRs serve it).
  wire       srp_idx0_ls_w = strm_lsn0_r && (SRP_LSN0_ROW_P != 0);
  wire       srp_poll_w    = win_in_range_w &&
                             ((strm_idx_r != 4'd0) || srp_idx0_ls_w);
  wire [4:0] srp_sel_row_w = strm_dir_r
      ? 5'((N_LISTENERS_P - 1) + 32'(strm_idx_r))
      : (srp_idx0_ls_w ? 5'(SRP_LSN0_ROW_P) : {1'b0, strm_idx_r});
  wire       srp_prov_w    = wr_fire && (wr_addr == A_STRMW_CTRL) &&
                             win_in_range_w &&
                             ((strm_idx_r != 4'd0) || srp_idx0_ls_w);
  //! ...and the staging set is only spendable by a commit to the SAME
  //! selection it was staged for (see the stg_sel_r banner). A commit that
  //! names no stream_id of its own provisions the row with a ZERO sid, which
  //! is what hands an AAF talker row to the fabric requester that derives
  //! {station MAC, uid} for it - the CRFT_SID "non-zero wins" rule per row.
  //! Ownership is by SELECTION, not spent by the commit: repeated CTRL writes
  //! at the index a sid was staged for keep that sid, so a re-enable cannot
  //! change a running stream's declared identity underneath it.
  wire       stg_hit_w     = stg_vld_r && (stg_sel_r == {strm_dir_r,
                                                         strm_idx_r});

  always_ff @(posedge aclk) begin : strm_srp_master_S
    if (!aresetn) begin
      srp_wr_pend_r <= 1'b0; srp_wr_valid_r <= 1'b0; srp_wr_dir_r <= 1'b0;
      srp_wr_row_r  <= 5'd0; srp_wr_sid_r <= 64'h0; srp_wr_dmac_r <= 48'h0;
      srp_cmd_was_wr_r <= 1'b0; srp_fresh_r <= 1'b0;
    end else begin
      srp_cmd_was_wr_r <= o_srp_ctx_we;   //! command type at the service beat
      if (i_srp_ctx_gnt) begin
        if (srp_cmd_was_wr_r) begin
          srp_wr_pend_r <= 1'b0;
          srp_fresh_r   <= 1'b0;          //! snapshot predates the write: re-poll
        end else
          srp_fresh_r   <= 1'b1;
      end
      if (sel_wr_w) srp_fresh_r <= 1'b0;
      if (srp_prov_w) begin
        srp_wr_pend_r  <= 1'b1;
        srp_wr_valid_r <= s_axi_wdata[0];
        srp_wr_dir_r   <= ~strm_dir_r;    //! ctx encoding: 0=talker,1=listener
        srp_wr_row_r   <= srp_sel_row_w;
        srp_wr_sid_r   <= stg_hit_w ? {stg_sid_hi_r, stg_sid_lo_r} : 64'h0;
        srp_wr_dmac_r  <= stg_hit_w ? {stg_dmac_hi_r[15:0], stg_dmac_lo_r}
                                    : 48'h0;
        srp_fresh_r    <= 1'b0;
      end
      //! LAST, so it beats the grant above: a beat we did not win cannot
      //! leave a snapshot behind that looks like ours
      if (i_srp_ctx_stolen) srp_fresh_r <= 1'b0;
    end
  end : strm_srp_master_S

  assign o_srp_ctx_req       = srp_wr_pend_r || srp_poll_w;
  assign o_srp_ctx_we        = srp_wr_pend_r;
  assign o_srp_ctx_idx       = srp_wr_pend_r ? srp_wr_row_r : srp_sel_row_w;
  assign o_srp_ctx_valid     = srp_wr_valid_r;
  assign o_srp_ctx_dir       = srp_wr_pend_r ? srp_wr_dir_r : ~strm_dir_r;
  assign o_srp_ctx_sid       = srp_wr_sid_r;
  assign o_srp_ctx_dmac      = srp_wr_dmac_r;
  assign o_srp_ctx_prio_rank = LWSRP_PRIO_RANK_C;
  //! TSpec/latency: shared with the legacy attribute until per-stream TSpec
  //! window words exist (all streams are 48 kHz class A base formats today)
  assign o_srp_ctx_max_frame = lwsrp_tspec[15:0];
  assign o_srp_ctx_interval  = lwsrp_tspec[31:16];
  assign o_srp_ctx_latency   = lwsrp_lat;

  //! ACMP context-table master: continuous poll of the selected listener
  //! context (the engine grants when its RAM port is idle)
  always_ff @(posedge aclk) begin : strm_acmp_master_S
    if (!aresetn) begin
      acmp_fresh_r  <= 1'b0;
      acmp_sid_q_r  <= 64'h0; acmp_dmac_q_r <= 48'h0;
      acmp_state_q_r <= 3'd0; acmp_probing_q_r <= 2'd0; acmp_status_q_r <= 5'd0;
      acmp_ctlr_q_r <= 64'h0; acmp_flags_q_r <= 16'h0; acmp_tuid_q_r <= 16'h0;
    end else begin
      if (i_acmp_tbl_gnt) begin
        acmp_sid_q_r     <= i_acmp_tbl_ctx[ACMP_CTX_SID_LO_C     +: 64];
        acmp_dmac_q_r    <= i_acmp_tbl_ctx[ACMP_CTX_DMAC_LO_C    +: 48];
        acmp_state_q_r   <= i_acmp_tbl_ctx[ACMP_CTX_STATE_LO_C   +: 3];
        acmp_probing_q_r <= i_acmp_tbl_ctx[ACMP_CTX_PROBING_LO_C +: 2];
        acmp_status_q_r  <= i_acmp_tbl_ctx[ACMP_CTX_STATUS_LO_C  +: 5];
        acmp_ctlr_q_r    <= i_acmp_tbl_ctx[ACMP_CTX_CTLR_LO_C    +: 64];
        acmp_flags_q_r   <= i_acmp_tbl_ctx[ACMP_CTX_FLAGS_LO_C   +: 16];
        acmp_tuid_q_r    <= i_acmp_tbl_ctx[ACMP_CTX_TUID_LO_C    +: 16];
        acmp_fresh_r     <= 1'b1;
      end
      if (sel_wr_w) acmp_fresh_r <= 1'b0;
    end
  end : strm_acmp_master_S

  assign o_acmp_tbl_req = !strm_dir_r && win_in_range_w;
  assign o_acmp_tbl_idx = strm_idx_r;

  //! E1 bind-restore master: the commit holds the request until the ack
  assign o_acmp_rest_req    = rest_pend_r;
  //! E3 journal ingest
  assign o_jnl_start = jnl_start_p;
  assign o_jnl_wr    = jnl_wr_p;
  assign o_jnl_data  = jnl_data_r;
  assign o_jnl_end   = jnl_end_p;
  assign o_jnl_abort = jnl_abort_p;
  //! E4 AEM dynamic-state patch port
  assign o_aemp_wdata    = aemp_wdata_r;
  assign o_aemp_sel_p    = aemp_sel_p;
  assign o_aemp_field_p  = aemp_field_p;
  assign o_aemp_data_p   = aemp_data_p;
  assign o_aemp_commit_p = aemp_commit_p;
  assign o_aemp_abort_p  = aemp_abort_p;
  assign o_acmp_rest_idx    = rest_idx_r;
  assign o_acmp_rest_talker = {rest_tkhi, rest_tklo};
  assign o_acmp_rest_tuid   = rest_meta[15:0];
  assign o_acmp_rest_ctlr   = {rest_cthi, rest_ctlo};
  assign o_acmp_rest_flags  = rest_flags_r;

  //! engine port-B buses: the SNAP burst and the slow-read fetch never
  //! overlap (slow reads fall back to fast-0 during a snap; a snap yields
  //! in SN_WAIT until a fetch in flight completes)
  assign o_lctx_rd_en    = (snap_rden_r && !snap_dir_r) ||
                           (rds_busy_r  && !rds_dir_r);
  assign o_lctx_rd_addr  = (snap_rden_r && !snap_dir_r)
                         ? {snap_idx_r[2:0], snap_word_r}
                         : {rds_idx_r, rds_word_r};
  assign o_tctx_rd_en    = (snap_rden_r && snap_dir_r) ||
                           (rds_busy_r  && rds_dir_r);
  assign o_tctx_rd_addr  = (snap_rden_r && snap_dir_r)
                         ? {snap_idx_r[2:0], snap_word_r[3:0]}
                         : {rds_idx_r, rds_word_r[3:0]};
  assign o_lctx_snap_req = snap_req_r && !snap_dir_r;
  assign o_tctx_snap_req = snap_req_r &&  snap_dir_r;
  assign o_lctx_wr_p     = lctx_wr_p_r;
  assign o_lctx_wr_addr  = lctx_wr_addr_r;
  assign o_lctx_wr_data  = lctx_wr_data_r;
  assign o_tctx_wr_p     = tctx_wr_p_r;
  assign o_tctx_wr_addr  = tctx_wr_addr_r;
  assign o_tctx_wr_data  = tctx_wr_data_r;

  assign o_irq = |(irq_status & irq_mask);
  assign o_eth_guard = eth_guard;

  //! wstrb is intentionally ignored (ABI: full 32-bit writes); tie off to satisfy lint
  wire _unused_ok = &{1'b0, s_axi_wstrb};

endmodule

`default_nettype wire
