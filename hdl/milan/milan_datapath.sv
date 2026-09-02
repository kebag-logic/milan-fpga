// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
//! # milan_datapath — Milan TSN fabric endpoint
//!
//! This is the single clean hardware boundary instantiated by the LiteX SoC. It
//! contains the complete vendor-neutral protocol and media fabric and is fully
//! open-toolchain verifiable (Verilator + Yosys). Its external boundaries are
//! AXI-Lite control, protocol memory, MAC AXIS and physical audio.
//!
//! What it owns:
//!   milan_csr · the PHC (timestamp_counter + ptp_csr_sync) ·
//!   rx_mac_filter (TCAM) · the AVTP/AAF/CRF stream engines · KL_maap ·
//!   adp_tx_arbiter · ethernet_events · **KL_pp_shadow**, the protocol
//!   processor, which is this device's entire IEEE 1722.1 / SRP control plane.
//!
//! THE CONTROL PLANE IS THE PROTOCOL PROCESSOR, AND ONLY THAT (2026-08-13).
//! This repository's own ADP advertiser, AECP/AEM engine, ACMP talker and
//! listener, and lwSRP applicant are DELETED - no parameter, no fallback, no
//! shadow arm (USER, explicit and repeated: "remove the old code AECP/ACMP/ADP
//! the lwSRP shall be removed as well. Only use the uCPU code"; "do not leave
//! the option, remove everything out of the code base that is legacy").
//!
//! WHAT A CONTROLLER GETS, STATED ONCE SO NO READER HAS TO DISCOVER IT:
//! the entity DISCOVERS over ADP, connects over ACMP, reserves over SRP, and
//! serves the protocol processor's implemented AECP inventory. That includes
//! READ_DESCRIPTOR, solicited GET_COUNTERS, selected getters and setters,
//! Identify control, the unsolicited registration pair,
//! GET_AUDIO_MAP, GET_DYNAMIC_INFO, and Milan GET_MILAN_INFO. Unsupported operations receive the
//! conformant NOT_IMPLEMENTED fallback. IDENTIFY_NOTIFICATION sent as a command
//! is BAD_ARGUMENTS.
//! AN ECHO IS NOT AN IMPLEMENTATION - and since 0x0002_0054 no MANDATORY
//! command answers the echo: the stream setters landed at 0x0053 and name
//! access at 0x0054, and 0x0055 wires the Table 5.22 observed triggers
//! (the per-descriptor counter-change arbiter and the complete served-state
//! comparators for GET_AVB_INFO and GET_AS_PATH) into the
//! processor's notification scheduler beside the command-driven pushes
//! and the 5.4.5.3 controller monitor. Live audio-map mutation is
//! implemented, but saved-state persistence is absent. SET_CLOCK_SOURCE is
//! stored by the processor AND consumed by the media plane (#74): the
//! resolved selection gates the MMCM servo, the grid-align loop and the mr
//! machinery - see the media-clock banner. If the descriptor image was never
//! loaded at PP_DESC_BASE_P the
//! range check fails before any locate runs, so an unloaded image answers
//! BAD_ARGUMENTS - not NO_SUCH_DESCRIPTOR. That difference is the bench
//! discriminator: BAD_ARGUMENTS everywhere = no image. Legacy CSR faces with no
//! live processor output read STRUCTURAL ZEROS and are documented at their
//! tie-offs. The current compliance blockers are recorded in
//! docs/testing/MILAN_V12_AUDIT_2026-08-16.md.
//! What moved OUT to the integration layer:
//!   * the **1G RGMII MAC** → exposed as a **MAC-facing AXIS pair** + MAC cfg/status
//!     ports, so the MAC is attached at the board layer (LiteEth `LiteEthMAC`, or
//!     Forencich `eth_mac_1g_rgmii_fifo`). This keeps the wrapper synth/sim-clean.
//!
//! Boundary summary:
//!   CPU  ── AXI4-Lite slave (s_axi_*, 16-bit offset) ─────► control plane
//!   MAC  ── m_axis_mac_tx_* (→MAC) / s_axis_mac_rx_* (MAC→) + o_mac_* cfg / i_mac_* status
//!   MEM  ── protocol-processor descriptor and response-buffer request/response faces
//!   IRQ  ── o_irq_csr (diagnostic aggregate; the product firmware polls its CSR state)

`default_nettype none
`include "ethernet_events.svh"

module milan_datapath import ethernet_packet_pkg::*; #(
  parameter int TDATA_WIDTH = 64,
  //! axis_clk frequency (AX7101 100 MHz, Arty 50 MHz) — AECP lock-timer divider.
  parameter int MILAN_CLK_FREQ_HZ = 100_000_000,
  //! the fabric gPTP plane (issue #110/#114): elaboration-time option.
  //! Fabric owns gPTP in the product shape; the 0 side is permanently
  //! ownerless and publishes uncertainty. ON splices
  //! KL_gptp_shadow onto the control TX (gasket-free, like CRF) and hands it
  //! the PHC's adjfine/adjtime; settime stays with the CSR face.
  parameter bit GPTP_PLANE_EN_P = 1'b1,
  //! Absolute in SoC builds, relative in self-contained Verilator benches.
  //! The image bakes in the config's station MAC, priority1 and fabric clock.
  parameter string GPTP_UCODE_HEX_P = "gptp_ucode.hex",
  //! NxN dataplane width (docs/fpga/FPGA_DESIGN.md section 2): AAF stream contexts
  //! per shared engine (listener sinks = talker sources = N_STREAMS). The
  //! N = 1 default is today's shape, bit-compatible (no-regression axiom).
  parameter int N_STREAMS = 1,
  //! THE WIRE CHANNEL CONSTANT (docs/ENDSTATION_BUILDER.md section 3).
  //! channels_per_frame this fabric puts in every talker's AAF PDU - the
  //! 7.3.3 field and the 24*C payload both. It sits beside N_STREAMS
  //! deliberately: a stream COUNT and a stream WIDTH are the same kind of
  //! fact about a built bitstream, and until 2026-07-27 only the count was
  //! expressed. The width lived in a `4'd2` inside KL_aaf_packetizer, so the
  //! 8x8 config could advertise 8-channel AAF with every gate in this repo
  //! green - config, svh, CSR and descriptor counts all agreed with each
  //! other, and not one of them could see the wire. A Milan-validated
  //! listener bound to talker 0, passed the 5.5.1.2 format check, returned
  //! ACMP SUCCESS, and discarded 296,294 of 296,294 frames as
  //! UNSUPPORTED_FORMAT.
  //!
  //! It is NOT a free declaration. It DRIVES the packetizer (the chans reset
  //! for every talker), and the elaboration guard below refuses any value the
  //! selected capture front-end cannot actually feed. Raising
  //! it therefore requires raising the framer - which is roadmap item 5.
  //! Default 2 = today's stereo framer, byte-identical.
  parameter int TALKER_WIRE_CHANS_P = 2,
  //! item-4 audio-interface family: capture front-end generate select.
  //! 0 = stereo I2S master (KL_aaf_capture_i2s, the default - byte/pin
  //! compatible); 8/16/32 = TDM slave with that many slots
  //! (KL_tdm_capture; tdm_* pins live, i2s sclk/lrck parked, i2s_mclk_o
  //! carries the codec MCLK, TONE_CTRL pilot override has no effect).
  parameter int AUDIO_IF_SLOTS_P = 0,
  //! item-4 audio-interface family: the TDM bus ROLE, and the reason the TDM
  //! front-end can be a fabric fact instead of a declaration. 0 (default) =
  //! SLAVE (KL_tdm_capture) - it waits for a codec/DSP to drive bclk/fsync,
  //! and on EVERY SoC in this tree those are tied to 0, so its fsync never
  //! toggles, it yields no pairs, and a talker built on it emits NO FRAME AT
  //! ALL. 1 = MASTER (KL_tdm_capture_master) - the fabric GENERATES bclk and
  //! fsync out of clk_tdm_i and needs nobody to drive it, which is what turns
  //! the interface into something the wire-accountability gate can count.
  //! Only meaningful with AUDIO_IF_SLOTS_P > 0.
  parameter int AUDIO_IF_MASTER_P = 0,
  //! MASTER-only: the frequency of clk_tdm_i, in Hz, and the sample rate its
  //! frame sync must run at. Together with AUDIO_IF_SLOTS_P they FIX the bclk
  //! divider - bclk = SLOTS x 32 x fs and clk_tdm_i = 2 x BCLK_HALF x bclk -
  //! and the guard below REFUSES any combination that is not an exact integer
  //! division. That refusal is the whole point: TDM32 x 32-bit slots at 48 kHz
  //! needs a 49.152 MHz bit clock and therefore a 98.304 MHz clk_tdm_i, which
  //! the shipping 24.576 MHz audio MMCM cannot divide down to. A silent
  //! wrong-rate front-end is exactly the class of defect roadmap item 00
  //! exists to make loud. Defaults describe the shipping audio clock, at which
  //! only TDM8 x 32 @ 48 kHz is realisable (24.576 MHz = 2 x 1 x 12.288 MHz).
  parameter int AUDIO_IF_CLK_HZ_P = 24576000,
  parameter int AUDIO_IF_FS_HZ_P  = 48000,
  //! HANDOVER 8.3b (USER 2026-07-28) - the Arty audio shape: 1 = keep the
  //! stereo I2S front-end ALIVE BESIDE a TDM MASTER and blend the two pair
  //! streams (KL_pair_blend): the I2S pair is pair slot 0 - "channels 1/2
  //! stay the I2S Pmod", the bench analog loop - and the TDM pairs follow at
  //! slots 1..S/2. Supply = 1 + S/2 pairs. Only meaningful with
  //! AUDIO_IF_MASTER_P = 1 (a SLAVE bus shares the i2s mclk pin; the guard
  //! below refuses the combination). 0 (default) = every existing shape,
  //! byte-identical.
  parameter int AUDIO_IF_I2S_PAIR_P = 0,
parameter int PB_PREFILL_C = 0,    //! playback prefill release (0 = midpoint;
                                   //! TBs shrink it to keep injections short)
  //! task #65: wire KL_chan_map_capture's rx -> talker LOOPBACK bucket
  //! (SRC_LOOP = 5) to the depacketizer payload clone, so a talker slot
  //! naming a loopback AUDIO_CLUSTER really carries that received channel
  //! pair. 0 (default) ties the feed off AND elaborates the bucket at its
  //! minimum: functionally identical to the pre-task-#65 shape (the bucket
  //! could never be fed there either) and measurably 36 LUT SMALLER than it,
  //! because that shape elaborated the 8x8 bank and relied on the tie-off to
  //! prune it. Priced at the instantiation below (+2303 LUT / +1542 FF OOC
  //! at 8x8) - a real feature with a real bill, not a free connection.
  parameter int LOOPBACK_P = 0,
  //! BANKED AREA LEVER (docs/CHANNEL_MAP_64.md): 1 (default) keeps the
  //! render-tap Butterworth LPF; 0 prunes KL_pcm_lpf and ties its outputs to
  //! the exact nets the runtime bypass (LPF_CTRL[0] = 0) already produces, so
  //! a pruned build behaves like a shipped build with the filter switched
  //! off - no new state, no new behaviour. Priced from the shipping place
  //! report at 428 LUT / 756 FF / 0 DSP; spend it only when space-bound, and
  //! remember the -72.7 dB analog loop record was measured THROUGH the
  //! filter, so a pruned bitstream is not the one that number belongs to.
  parameter int LPF_P = 1,
  //! KL_ptp_clock_validity time base: cycles per 250 ms quarter-tick. The
  //! real value is MILAN_CLK_FREQ_HZ/4; simulation shapes shrink it so a
  //! grandmaster holdover and an observation interval are reachable in a TB run
  //! (the -GPB_PREFILL_C precedent). Never shrink it in a real build - the
  //! Milan Annex B.1.1 holdover is 0.25 s of WALL time.
  parameter int CLKV_QTICK_CYC_P = MILAN_CLK_FREQ_HZ / 4,
  // ==========================================================================
  //  OPTIONAL-BLOCK PRUNE PARAMETERS (docs/design/AREA_BUDGET.md tier 1).
  //  Every one of them DEFAULTS TO 1 = PRESENT, so a build that passes none
  //  of them elaborates the exact shape that ships today - a parameter that
  //  changed a shipping build merely by existing would be a behaviour change
  //  in disguise. They are ELABORATION-TIME: 0 makes synthesis DROP the
  //  instance, which a runtime CSR enable never does. Where a runtime enable
  //  already exists the two compose - the parameter decides whether the logic
  //  is BUILT, the CSR bit decides whether the built logic RUNS - and a
  //  pruned block behaves exactly as its runtime-disabled self does today
  //  (each tie-off below states the term-by-term equivalence).
  //  sw/builder/endstation_builder.py refuses a config that asks for a
  //  feature one of these pruned (board.features), so an absent block is
  //  never silent.
  // ==========================================================================
  //! Media-clock servo (KL_mmcm_drp_servo, 933 LUT / 807 FF measured).
  //! 0 prunes it and parks the MMCM control ports: no DRP access, no phase
  //! step, MMCM never reset, A_MCSRV_STAT 0x8F8 reads 0. Legal ONLY when the
  //! media clock is INTERNAL - the servo is the actuator for clock_source ==
  //! 2 (CRF recovered) and for input_stream lock, so a pruned build cannot
  //! discipline the audio MMCM to a remote grandmaster at all. The builder
  //! gate keys on clocking.media_clock_sources == [internal].
  //! Milan Table 5.4 observation interval (KL_talker_diag_ctx), in datapath
  //! clock cycles; the clause bounds it at <= 1 s. TBs shrink it.
  parameter int DIAG_TICK_CYC_P = MILAN_CLK_FREQ_HZ,
  //! Milan Table 5.6 observation interval (every server of the Stream
  //! Input clause: KL_avtp_rx_monitor_ctx for the AAF listeners AND
  //! KL_crf_rx for the CRF Media Clock Input), in datapath clock cycles;
  //! <= 1 s. TBs shrink it so counter checks see interval boundaries.
  parameter int LDIAG_IVAL_CYC_P = MILAN_CLK_FREQ_HZ,
  parameter int MCSERVO_P = 1,
  //! AAF latency taps (KL_aaf_latency_taps, 696 LUT / 614 FF measured).
  //! PURE INSTRUMENTATION: nothing in the media path reads a tap output -
  //! the whole block feeds the LTAP CSR window 0x870-0x8B0 and nothing else.
  //! 0 prunes it and every LTAP word reads 0 (a STRUCTURAL zero, not a
  //! measurement - the same distinction STATS_CAP draws for the RMON lanes).
  //! Pruning FORCES RE-MEASUREMENT of nothing in the media path and of
  //! EVERYTHING in docs/AAF_LATENCY_TAPS.md: the CAP-SOF/SOF-EOF/EOF-MAC
  //! silicon numbers cannot be reproduced on a pruned bitstream.
  parameter int LTAP_P = 1,
  //! MAAP engine (KL_maap, 621 LUT / 268 FF measured). 0 prunes it, ties
  //! addr_valid_o = 0 and parks its low-rate TX port. Term-by-term that is
  //! the state a build with MAAP_CTRL.en = 0 is in today: eff_aaf_dmac falls
  //! back to the CSR-provisioned AAF_DMAC and the admission gate's MAAP term
  //! (~cfg_maap_enable | maap_addr_valid) is satisfied by its first half.
  //! CAUTION: with the engine pruned, setting MAAP_CTRL.en = 1 would pin
  //! admission SHUT (the claim can never complete), so the CSR bit is
  //! effectively reserved - the builder gate keys on a config that asks for
  //! dynamic (srp.stream_dmac_base: maap) rather than static addresses.
  parameter int MAAP_P = 1,
  //! KL_maap's millisecond base, for SIMULATION time compression only (the
  //! CLKV_QTICK_CYC_P / PP_TIM_DIV_*_P precedent). DERIVED from the real
  //! clock declaration, never mirrored, so a silicon build is bit-identical
  //! to what shipped. A harness lowers it so the 3-probe / 500 ms Annex B
  //! claim walk completes in a few hundred thousand cycles instead of the
  //! 1.5e8 a real 100 MHz clock needs - the ONLY way a testbench can see
  //! addr_valid_o assert at all.
  parameter int MAAP_CLK_HZ_P = MILAN_CLK_FREQ_HZ,
  //! I2S DAC playback (KL_i2s_playback, 552 LUT / 624 FF measured). 0 prunes
  //! the serializer and its rate servo: the four i2s_dac_* pins park at 0 and
  //! the I2SPB CSR group (0x6D8 stat / 0x6E0 trim+fill / 0x6F0 dbg) reads 0.
  //! Legal when the board has no DAC. NOTE the second-order effect:
  //! i2spb_converged is KL_avtp_rx_monitor(_ctx)'s servo_conv_i, and its
  //! media-lock rule is `clk_src == 0 || servo_conv` - so on a pruned build
  //! an EXTERNAL media clock NEVER reaches media lock. That is consistent
  //! (there is no render device to converge) but it IS a behavioural
  //! consequence; internal-clock media lock is immediate and unaffected.
  parameter int I2SPB_P = 1,
  //! RX station-address filter (rx_mac_filter + tcam, 504-569 LUT /
  //! 1568-1570 FF measured). 0 prunes it and wires the post-PTP RX stream
  //! STRAIGHT to the fabric-observer tap - which is bit-for-bit what the shipping
  //! filter does with promisc_i = 1 (or with TCAM_CTRL[1] = 0 and
  //! default_pass = 1). Legal when the port is promiscuous or address
  //! filtering is deliberately disabled; the TCAM_* CSR window keeps its
  //! addresses but nothing consumes them, so the builder gate keys on
  //! platform.rx_address_filter being declared 'promiscuous'.
  parameter int RXFILT_P = 1,
  //! Area-budget static-conversion record (2026-07-29): the APRB
  //! (0x8B4-0x8C4) and PBK (0x8C8-0x8D0) probe groups - closed-finding
  //! diagnostics whose counters/latches die with the parameter; the CSR
  //! range reads 0 on a pruned build (the LTAP precedent).
  parameter int DPROBES_P = 1,
  //! Protocol-processor timer compression for SIMULATION only (the
  //! CLKV_QTICK_CYC_P precedent). Defaults are REAL time and are what silicon
  //! builds use: at 100 MHz, 100 clk = 1 us and 1000 us = 1 ms. A harness
  //! overrides them so a 5 s ADP cadence is reachable in a few thousand
  //! cycles. THERE IS NO PP_PLANE_P: the processor is not optional, it is the
  //! control plane (the legacy 1722.1/SRP plane is deleted, USER 2026-08-13).
  parameter int PP_TIM_DIV_US_P = MILAN_CLK_FREQ_HZ / 1_000_000,
  parameter int PP_TIM_DIV_MS_P = 1000,
  //! ACMP listener transition-ROM image. The processor $readmemh's it by this
  //! name, and Vivado resolves a RELATIVE name against its own run directory -
  //! so the integration hands over an ABSOLUTE path and the build stops
  //! depending on where the tool was launched from.
  parameter string PP_TROM_HEX_P = "ltn_rom.hex",
  //! ---- AECP descriptor store (protocol-processor 07 §3.3) ----------------
  //! The uCPU microcode image and the geometry/base of the entity-model image
  //! the descriptor store FETCHES FROM MAIN MEMORY. On this board that memory
  //! is DDR3 and the SoC bridges the master (sw/litex/milan_soc.py); the base
  //! is COMPILE-TIME by the processor's design, so there is no base register
  //! for software to get wrong. The integration overrides PP_DESC_BASE_P to a
  //! region the SoC reserves and software loads before enabling the entity.
  parameter string PP_UCODE_HEX_P        = "ucode.hex",
  parameter logic [31:0] PP_DESC_BASE_P  = 32'h2000_0000,
  parameter int PP_DESC_LINE_BYTES_P     = 576,
  parameter int PP_DESC_IDX_ENTRIES_P    = 32,
  parameter int PP_DESC_MEM_TMO_CYC_P    = 4096,
  //! ---- AECP response buffer (protocol-processor 03 §7) -------------------
  //! Base of the response buffer's own main-memory region - a SECOND window,
  //! 16 + PP_DESC_LINE_BYTES_P bytes wide, that the processor WRITES as well
  //! as reads. Compile-time for the same reason PP_DESC_BASE_P is, and the
  //! integration overrides it to a region reserved for the processor alone:
  //! unlike the read-only descriptor image, an overlap here is silent
  //! corruption of whatever it lands on. The SoC derives BOTH bases from its
  //! own main_ram map and states why they cannot collide.
  parameter logic [31:0] PP_RESP_BASE_P  = 32'h2010_0000
)(
  //! ---- AECP descriptor-image READ master (to the SoC's main memory) -----
  //! The protocol processor's entity model lives in DDR3. This is its fetch
  //! path, surfaced at the wrapper boundary rather than tied off inside it:
  //! ONE outstanding request, responses IN ORDER, `rsp_last` ends the burst,
  //! and a beat carries its LOWEST byte address in bits [63:56].
  //! o_desc_mem_rsp_ready is tied 1 by the processor - it always sinks.
  //! An integration with no memory to offer may tie i_desc_mem_req_ready to
  //! 0: the store's watchdog then abandons the burst and every
  //! READ_DESCRIPTOR degrades to NO_SUCH_DESCRIPTOR instead of hanging. That
  //! is a legal wiring, but it must be DELIBERATE and stated, because the
  //! entity then serves no descriptors at all.
  output wire        o_desc_mem_req_valid,
  input  wire        i_desc_mem_req_ready,
  output wire [31:0] o_desc_mem_req_addr,
  output wire [8:0]  o_desc_mem_req_beats,
  input  wire        i_desc_mem_rsp_valid,
  output wire        o_desc_mem_rsp_ready,
  input  wire [63:0] i_desc_mem_rsp_data,
  input  wire        i_desc_mem_rsp_last,
  input  wire        i_desc_mem_rsp_err,

  //! ---- AECP response-buffer READ+WRITE master (to the SoC's main memory) -
  //! The SECOND main-memory master, and the reason it exists is area: the
  //! response an AECP command builds is up to 16 + PP_DESC_LINE_BYTES_P bytes
  //! and, held as fabric flops, it was the state that failed placement on a
  //! die whose block RAM was already 100% used. It is a separate face from the
  //! descriptor image above BY CONTRACT, not by convenience - both are
  //! watchdog-bounded one-transaction clients and the SoC's memory system is
  //! the arbiter.
  //!
  //! READ: same shape as the descriptor face - ONE outstanding request,
  //! responses IN ORDER, `rsp_last` ends the burst, a beat carries its LOWEST
  //! byte address in bits [63:56] - EXCEPT that o_resp_mem_rsp_ready is REAL
  //! BACKPRESSURE and is NOT tied 1. A bridge SHALL hold a beat until it is
  //! taken.
  //! WRITE: ONE outstanding SINGLE-BEAT write. o_resp_mem_wr_addr is 8-byte
  //! aligned, o_resp_mem_wr_data is the same big-endian lane as a read beat
  //! (byte addr+n = bits [63-8n -: 8]), o_resp_mem_wr_strb bit n enables byte
  //! n and A ZERO-STROBE BYTE SHALL NOT BE MODIFIED. i_resp_mem_wr_done is a
  //! ONE-CYCLE COMMIT PULSE - same cycle as i_resp_mem_wr_ready for a posted
  //! bridge, any later cycle for an acknowledged one - and no further write is
  //! issued until it arrives. ORDERING: a read accepted after a write reported
  //! done SHALL observe that write.
  //! An integration with no memory to offer may tie i_resp_mem_req_ready and
  //! i_resp_mem_wr_ready to 0: the buffer's watchdog then voids the response
  //! and the AECP engine answers a well-formed ENTITY_MISBEHAVING instead of
  //! hanging. Legal, but it must be DELIBERATE and stated - every AECP
  //! response the entity builds is lost that way.
  output wire        o_resp_mem_req_valid,
  input  wire        i_resp_mem_req_ready,
  output wire [31:0] o_resp_mem_req_addr,
  output wire [8:0]  o_resp_mem_req_beats,
  input  wire        i_resp_mem_rsp_valid,
  output wire        o_resp_mem_rsp_ready,
  input  wire [63:0] i_resp_mem_rsp_data,
  input  wire        i_resp_mem_rsp_last,
  input  wire        i_resp_mem_rsp_err,
  output wire        o_resp_mem_wr_valid,
  input  wire        i_resp_mem_wr_ready,
  output wire [31:0] o_resp_mem_wr_addr,
  output wire [63:0] o_resp_mem_wr_data,
  output wire [7:0]  o_resp_mem_wr_strb,
  input  wire        i_resp_mem_wr_done,
  input  wire        i_resp_mem_wr_err,

  //! axis_clk domain (system clock, ~100 MHz) + active-low sync reset
  input  wire axis_clk,
  input  wire        clk_audio_i,      //! clean MMCM audio clock (24.576 MHz nominal) for the I2S DAC serializer
  //! item-4 TDM MASTER serial-domain clock (AUDIO_IF_MASTER_P != 0 only).
  //! A SEPARATE net from clk_audio_i on purpose: clk_audio_i is 24.576 MHz by
  //! CONTRACT, not by convention - KL_crf_tx divides it by 512 for the 48 kHz
  //! CRF event, KL_i2s_playback divides it /2 /8 /512 for the DAC, and
  //! KL_mmcm_drp_servo measures it. A TDM32 master needs 98.304 MHz and
  //! re-rating clk_audio_i would silently move all three. Left open on every
  //! slave/I2S build (AUDIO_IF_CLK_HZ_P then only describes a divider nothing
  //! uses).
  input  wire        clk_tdm_i,
  input  wire axis_resetn,
  //! gtx_clk domain (125 MHz) used by the MAC-RX timestamping in ptp_ts_top
  input  wire gtx_clk,
  input  wire gtx_resetn,

  // ---- AXI4-Lite CSR slave (from the CPU bus bridge; low 16 bits = offset) ----
  input  wire [15:0] s_axi_awaddr,
  input  wire        s_axi_awvalid,
  output wire        s_axi_awready,
  input  wire [31:0] s_axi_wdata,
  input  wire [3:0]  s_axi_wstrb,
  input  wire        s_axi_wvalid,
  output wire        s_axi_wready,
  output wire [1:0]  s_axi_bresp,
  output wire        s_axi_bvalid,
  input  wire        s_axi_bready,
  input  wire [15:0] s_axi_araddr,
  input  wire        s_axi_arvalid,
  output wire        s_axi_arready,
  output wire [31:0] s_axi_rdata,
  output wire [1:0]  s_axi_rresp,
  output wire        s_axi_rvalid,
  input  wire        s_axi_rready,

  // ---- Pmod I2S2 (AAF talker audio in; fabric is I2S clock master) ----
  output wire                     i2s_mclk_o,
  output wire                     i2s_sclk_o,
  output wire                     i2s_lrck_o,
  input  wire                     i2s_sdout_i,
  // ---- TDM bus (AUDIO_IF_SLOTS_P > 0) ------------------------------------
  //  BOTH ROLES ARE WIRED OUT AND BOTH SETS OF PINS ALWAYS EXIST: a port's
  //  DIRECTION cannot be parameterized in SystemVerilog, so a build that is
  //  the bus MASTER cannot turn tdm_bclk_i around into an output. The slave
  //  inputs are read only when AUDIO_IF_MASTER_P == 0 and the master outputs
  //  are driven to 0 otherwise, so the SoC connects the pair its role needs
  //  and leaves the other open (an unconnected port does not appear in the
  //  generated top .v at all - the no-regression axiom holds by construction).
  input  wire                     tdm_bclk_i,     //! SLAVE role: bit clock in
  input  wire                     tdm_fsync_i,    //! SLAVE role: frame sync in
  output wire                     tdm_bclk_o,     //! MASTER role: generated bit clock
  output wire                     tdm_fsync_o,    //! MASTER role: generated frame sync (1-bclk pulse)
  //! MEDIA-GRID TEST POINT (AX7101 J11.9). Toggles on every media sample
  //! tick, so it is a 50%-duty square at fs/2 = 24 kHz. This is the ONLY
  //! external view of media_tick_p: no CSR carries the grid's rate, and on a
  //! TDM8-master shape tdm_fsync_o above rides clk_audio instead - a
  //! different clock, -10.64 ppm by construction. Probing the two together
  //! measures that difference with no peer device involved.
  output wire                     media_lrclk_o,
  output wire                     tdm_mclk_o,     //! MASTER role: codec master clock (clk_tdm_i/2). On a blend build (AUDIO_IF_I2S_PAIR_P) the TDM header gets its OWN mclk pad so i2s_mclk_o can stay on the Pmod I2S2 (Arty D13, the CS5343 - HANDOVER 8.3b work item 1); solo-master builds keep mclk on i2s_mclk_o exactly as before and may leave this open.
  output wire                     tdm_dout_o,     //! chmap follow-up 4: KL_tdm_render serial out (TDM8, ext-clocked by tdm_bclk/fsync)
  input  wire                     tdm_data_i,
  // ---- Pmod I2S2 DAC (line-out): zero-CPU playback of the bound stream ----
  output wire                     i2s_dac_mclk_o,
  output wire                     i2s_dac_sclk_o,
  output wire                     i2s_dac_lrck_o,
  output wire                     i2s_dac_sdin_o,

  // ---- MAC-facing TX: datapath (shaper→PTP→ADP arbiter) → external MAC ----
  output wire [TDATA_WIDTH-1:0]   m_axis_mac_tx_tdata,
  output wire [TDATA_WIDTH/8-1:0] m_axis_mac_tx_tkeep,
  output wire                     m_axis_mac_tx_tvalid,
  output wire                     m_axis_mac_tx_tlast,
  input  wire                     m_axis_mac_tx_tready,

  // ---- MAC-facing RX: external MAC → datapath (into PTP-RX timestamping) ----
  input  wire [TDATA_WIDTH-1:0]   s_axis_mac_rx_tdata,
  input  wire [TDATA_WIDTH/8-1:0] s_axis_mac_rx_tkeep,
  input  wire                     s_axis_mac_rx_tvalid,
  input  wire                     s_axis_mac_rx_tlast,
  output wire                     s_axis_mac_rx_tready,

  // ---- MAC configuration (to the external MAC) ----
  output wire        o_mac_tx_en,
  output wire        o_mac_rx_en,
  output wire        o_mac_promisc,
  output wire        o_mac_allmulti,
  output wire        o_mac_is_1g,
  output wire [7:0]  o_mac_ifg,
  output wire [47:0] o_mac_addr,
  output wire [63:0] o_mc_hash,
  output wire        o_phy_reset_n,

  // ---- MAC status (from the external MAC) ----
  input  wire [1:0]  i_mac_speed,
  input  wire        i_link_up,
  output wire        o_mac_reinit,     //! link guard | LINK_CTRL[1] -> SoC MAC sys-side reset
  output wire        o_eth_rst,        //! link guard sequenced eth-side CDC reset request
  output wire        o_eth_guard,      //! ETH GUARD (CSR 0x7D8): 1 = CPU eth-disruption levers refused
                                       //! (SoC syncs it into eth_tx/eth_rx as the MAC's
                                       //! eth-domain reset; released BEFORE o_mac_reinit)
  input  wire        i_full_duplex,
  //! async divide-by-2 toggles from the SoC's eth clock domains (link guard
  //! liveness sensing; tie high on TBs/tops without a PHY - a static level
  //! reads as a dead clock only until the guard is disabled via LINK_CTRL[2])
  input  wire        i_ethrx_tgl,
  input  wire        i_ethtx_tgl,
  input  wire        i_ethact_tgl,
  //! RMON event pulses from the external MAC (lane index == ethernet_events_t
  //! enum). Lanes TX_FIFO_GOOD_FRAME/RX_FIFO_GOOD_FRAME are IGNORED here: the
  //! datapath derives them itself from the MAC AXIS boundary handshake (RMON
  //! never-worked-on-silicon fix, 2026-07-22 - the LiteX SoC glue tied this
  //! whole bus to 0 because LiteEth exposes no Forencich-style event pulses,
  //! so every lane counted nothing on both boards). Integrations supply only
  //! the MAC-internal lanes (underflow/overflow/bad-frame/bad-FCS); tie 0
  //! when the MAC exposes none.
  input  wire [_ETH_EVENT_COUNTER-1:0] i_mac_events,
  //! RMON per-lane CAPABILITY mask from the integration (CSR 0x204 STATS_CAP):
  //! bit n = 1 means lane n has a real event source in THIS build. A lane whose
  //! bit is 0 is structurally silent - its STAT word is not a measurement, and
  //! software must report "not supported" rather than "no errors". The two
  //! good-frame lanes are OR-ed in below because the datapath derives them
  //! itself, so they are supported on every integration by construction. Tie 0
  //! together with i_mac_events when no MAC is attached at this boundary; the
  //! SoC's KL_mac_rmon_events publishes the real mask.
  input  wire [_ETH_EVENT_COUNTER-1:0] i_mac_events_cap,

  // ---- interrupt (milan_csr aggregate: tx_ts_ready | link_change | rmon_rollover) ----
  output wire        o_irq_csr,

  // ---- AECP IDENTIFY control (Milan FR-MGT-01): board LED blink hook ----
  output wire        o_identify,

  // ---- audio-MMCM media-clock servo (KL_mmcm_drp_servo -> MMCME2_ADV at
  //      the SoC layer; UG472 PS + XAPP888 DRP interfaces). i_ps_clk is
  //      the MMCM PSCLK domain (SoC: 200 MHz idelay; DS181 MMCM_FMAX_PSCLK
  //      450 MHz at -1); the DRP DCLK is axis_clk. Tops without the MMCM
  //      tie: ps_clk = axis_clk, drp_rdy/do = 0, locked = 1, ps_done = 0
  //      The current root cannot select CRF, so the servo stays idle. ----
  input  wire        i_ps_clk,
  output wire [6:0]  o_mmcm_drp_addr,
  output wire        o_mmcm_drp_en,
  output wire        o_mmcm_drp_we,
  output wire [15:0] o_mmcm_drp_di,
  input  wire [15:0] i_mmcm_drp_do,
  input  wire        i_mmcm_drp_rdy,
  output wire        o_mmcm_rst,
  input  wire        i_mmcm_locked,
  output wire        o_mmcm_ps_en,
  output wire        o_mmcm_ps_incdec,
  input  wire        i_mmcm_ps_done
);
  // P12 (docs/fpga/FPGA_DESIGN.md section 2): the 0x800 window's LCTX/TCTX port-B
  // read/snap/write bundles and the ACMP context-table port are wired to
  // the REAL engines inside this module (KL_avtp_rx_monitor_ctx /
  // KL_aaf_packetizer / KL_acmp_lstn_ctx via its wrapper) — the P11
  // boundary ports and their SoC inert ties are GONE.

  // ==========================================================================
  //  Internal AXIS hops for the fabric endpoint
  // ==========================================================================
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_to_mac();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) rx_axis_from_mac();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) rx_axis_fabric();

  //! NO GENERAL-DATA TX CHAIN. The 802.1Q classifier / per-queue FIFOs /
  //! 802.1Qav CBS shaper (traffic_controller_802_1q) and the ptp_ts_top TX/RX
  //! record stampers left this wrapper with the retired target (#259): removing
  //! the retired transmit path left the shaper's ONLY input structurally idle, and
  //! every product source - the AAF talkers, the CRF talker, MAAP, the
  //! protocol processor and the fabric gPTP plane - joins the TX trunk in the
  //! arbiter cascade below, AFTER the point the shaper occupied, so no frame
  //! could ever reach it. An elaborated chain on a tied-off input is silicon
  //! spent on nothing in a packing-bound build and a CSR face advertising a
  //! shaper the product cannot exercise. The modules stay verified stand-alone
  //! (tb/verilator/{classifier,queues,cbs,shaper_core,datapath,
  //! controller_rate,ptp_ts}) as the building blocks of a class-A shaping lane
  //! for the fabric's own streams, which is a separate lane. The CSR words
  //! that configured the chain (0x300 CLS_*, 0x400 CBS_*, 0x540/0x544
  //! PTP_*_LAT) are WRITE-ONLY SCRATCH and CAP.CBS / IRQ_STATUS[0] are
  //! structural zero - docs/reference/REGISTER_MAP.md records each.

  //! I2S divider scale: mclk = clk/2^N ~= 12.5 MHz -> 48.8 kHz sample rate
  //! on EITHER datapath clock. Un-parameterized, the 100 MHz AX sampled at
  //! 97.7 kHz while advertising 48 k (silicon: 16.9k fr/s, servo pegged).
  localparam int MCLK_DIV_LOG2_C = $clog2(MILAN_CLK_FREQ_HZ / 12_500_000);

  //! chmap media grid: THE 48 kHz strobe on the datapath clock. It paces the
  //! render/capture map walks (docs/CHANNEL_MAP_64.md §3/§4) and their tone
  //! source below - one grid for every fabric audio channel in both
  //! directions, which is the precondition for a single selected clock master
  //! meaning anything. The generator is KL_media_nco
  //! below; the grid it used to be (a fixed localparam divider that no clock
  //! source could reach) is why a listener draining a stream on this fabric
  //! slipped one sample per beat period.

  //! ONE-GRID rule (task #59, bench 2026-08-02): a tone producer must step
  //! on the grid its consumer drains. THIS instance steps on clk_audio_i/512
  //! and feeds ONLY the I2S front-end pilot override, which samples on its
  //! own /512 LRCK - the same grid. Feeding the capture crossbar from here
  //! put two FREE-RUNNING 48 kHz grids against each other (this one vs the
  //! media_tick_p divider below): ~4-12 sample repeats/drops per second,
  //! THD+N capped at -32 dB on a -147.7 dB-clean loop. The crossbar now has
  //! its own media-grid instance below.
  //! ------------------------------------------------------------------------
  //! CONSTANTS THAT USED TO LIVE IN A DELETED PACKAGE.
  //! lwsrp_pkg.sv is gone with the lwSRP engine, so the one constant this file
  //! still needs from it is named here. IEEE 802.1Q-2018 34.5 / Milan v1.2
  //! 4.2.7.2: SR class A rides priority 3 by default, and the OPERATIONAL
  //! priority the processor adopts (pp_cd_srp_class_a_prio_w) overrides it
  //! wherever a declaration exists - this is the pre-adoption fallback only.
  localparam logic [2:0] SR_CLASS_A_PRIO_C = 3'd3;
  //! ------------------------------------------------------------------------
  //! THE MEDIA CLOCK SOURCE - LIVE, AND RESOLVED EXACTLY ONCE (#74).
  //! The protocol processor accepts and stores IEEE 1722.1 SET_CLOCK_SOURCE
  //! and KL_pp_shadow exports the stored selection into this root as
  //! pp_aecp_clk_src_index_w. The compare against THIS SHAPE'S CRF index -
  //! AEM_CRF_CLKSRC_C, generated into gen/adp_shape_defaults.svh by the same
  //! pass that builds the AEM model, 16'hFFFF on a shape with no CRF source -
  //! happens in ONE registered block (media_clk_resolve, after the shape
  //! include below), and every consumer reads the resolved nets:
  //!   media_clk_src_r     the selected CLOCK_SOURCE index, registered
  //!   crf_clk_selected_r  the one-bit verdict "the CRF source is in use"
  //!
  //! THE TRAP THE OLD CONSTANTS EXISTED TO AVOID stays honoured in the new
  //! form. The first cut of the plane deletion kept two 16-bit nets with the
  //! live one tied to 0, and every consumer compared 0 == 0 = TRUE - a build
  //! claiming CRF selected while INTERNAL (measured: A_MCSRV_STAT = 0x21;
  //! the undriven net slipped past -Werror-UNDRIVEN through its
  //! public_flat_rd attribute). Hence: ONE compare, in one block, with the
  //! 0xFFFF no-descriptor fold making a CRF-less shape structurally false -
  //! and the verdict REGISTERED, so every gate downstream sees a clean
  //! transition, never a decode glitch.
  wire [15:0] pp_aecp_clk_src_index_w /* verilator public_flat_rd */;
  logic        crf_clk_selected_r /* verilator public_flat_rd */;
  logic [15:0] media_clk_src_r    /* verilator public_flat_rd */;
  //! the station MAC as a NUMERIC EUI-48 ([47:40] = first wire byte).
  //! cfg_mac_addr is the platform LSB-first CSR convention (firmware writes
  //! MAC_ADDR_LO/HI that way and the RX filter consumes it that way), and
  //! every protocol engine here wants the other one. Byte-reversed ONCE.
  //! cfg_mac_addr belongs to the CSR <-> datapath block below; it is
  //! declared here because this is its first reader and Vivado's front-end
  //! rejects a use before the declaration (#193).
  wire [47:0] cfg_mac_addr;
  wire [47:0] station_mac_be_w = {cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                                  cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                                  cfg_mac_addr[39:32], cfg_mac_addr[47:40]};

  KL_tone_gen #(.MCLK_DIV_LOG2(MCLK_DIV_LOG2_C)) tone_gen (
    .clk_i (clk_audio_i), .rst_n (axis_resetn), .adv_i (1'b1),
    .enable_i (cfg_tone_enable), .att_i (cfg_tone_att), .smp_o (tone_smp)
  );

  //! ONE-GRID rule, arithmetic half: render, capture, and the mapped tone use
  //! this SAME 48 kHz strobe. A second floored clk/48000 divider would drift
  //! by 160 ppm at 100 MHz, recreating the producer/consumer mismatch above.
  //!
  //! The divider is KL_media_nco: same Bresenham, same remainder, same
  //! denominator, plus a signed runtime trim. With mnco_trim_w tied to 0 it is
  //! bit-for-bit the block it replaced (tb/verilator/media_nco pins that
  //! tick-for-tick against a transcription of the old code), which is what
  //! keeps clock_source = INTERNAL the free-running grid every bench number on
  //! record was measured against.
  //! public_flat_rd: the media-grid checks in tb/verilator/milan_dp sim_nxn
  //! count this directly. The grid's rate is the one thing no CSR can show.
  wire        media_tick_p /* verilator public_flat_rd */;
  //! sub-sample phase of the grid. Not consumed by the fabric: it is a TB tap,
  //! and it is the only way to watch a trim take effect faster than the beat
  //! period (a 0.01 ppm step needs ~48000 ticks to move the tick pattern, but
  //! moves the accumulator on the very next one).
  wire [15:0] media_tick_phase_w /* verilator public_flat_rd */;

  //! driven far below, beside KL_mmcm_drp_servo: ONE error signal, two
  //! actuators. Declared here because the grid is built long before the
  //! clock-source selection exists.
  //! the two signals that steer the grid, driven far below beside
  //! KL_mmcm_drp_servo. public_flat_rd because neither reaches a CSR, so a
  //! harness is the only place the steering can be observed at all.
  wire signed [15:0] mnco_servo_trim_w /* verilator public_flat_rd */;
  wire               mnco_servo_en_w   /* verilator public_flat_rd */;

  //! the J11.9 test point: a 50%-duty square at fs/2, so a counter or a scope
  //! reads the grid directly. Deliberately a toggle rather than the raw
  //! one-clock strobe - a 10 ns spike at 48 kHz is hard to trigger on and
  //! easy to mis-count, and the ppm resolution is identical either way.
  logic media_lrclk_r;
  always_ff @(posedge axis_clk) begin : media_lrclk_tp
    if (!axis_resetn)        media_lrclk_r <= 1'b0;
    else if (media_tick_p)   media_lrclk_r <= ~media_lrclk_r;
  end : media_lrclk_tp
  assign media_lrclk_o = media_lrclk_r;

  KL_media_nco #(
    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ),
    .FS_HZ_P       (48_000),
    .TRIMW_P       (18)
  ) media_nco (
    .clk_i        (axis_clk),
    .rst_n        (axis_resetn),
    //! the direct trim is unused here: the grid follows the servo or it
    //! free-runs, and nothing else in this design commands it in LSB
    .trim_i       (18'sd0),
    .servo_trim_i (mnco_servo_trim_w),
    .servo_en_i   (mnco_servo_en_w),
    .tick_o       (media_tick_p),
    .phase_o      (media_tick_phase_w)
  );

  //! media-grid pilot for the capture crossbar: the SAME table, stepped by
  //! the SAME media_tick_p the crossbar's walk drains on - producer and
  //! consumer share one grid by construction. Also an axis-domain
  //! register, so the raw clk_audio -> axis crossing into the walk's mux is
  //! gone. TONE_CTRL 0x6DC en/att semantics unchanged (shared with the
  //! front-end instance above).
  KL_tone_gen #(.MCLK_DIV_LOG2(MCLK_DIV_LOG2_C), .USE_EXT_ADV_P(1'b1))
  tone_gen_media (
    .clk_i (axis_clk), .rst_n (axis_resetn), .adv_i (media_tick_p),
    .enable_i (cfg_tone_enable), .att_i (cfg_tone_att),
    .smp_o (tone_smp_media)
  );

  //! NXN P4: the flat aaf_talker_i2s splits into the physical capture
  //! front-end (x1) + the shared N-context packetizer (TCTX). Talker 0
  //! aliases the legacy CSR config (golden byte-compare proven); talkers
  //! 1..N-1 arm via the TCTX window in P11.
  wire        aafcap_pv_w;
  wire [3:0]  aafcap_slot_w;
  wire [23:0] aafcap_l_w, aafcap_r_w;

  // ==========================================================================
  //  WIRE-CHANNEL ACCOUNTABILITY GUARD (roadmap item 00).
  //
  //  TALKER_WIRE_CHANS_P says how many channels a talker's AAF PDU carries.
  //  The pair stream is 2-channel-granular and the packetizer partitions its
  //  pair-slot space by a prefix sum of chans/2, so ONE talker at C channels
  //  needs C/2 pair slots fed with samples. The selected capture front-end is
  //  what feeds them, and it supplies exactly:
  //
  //    AUDIO_IF_SLOTS_P == 0  KL_aaf_capture_i2s - ONE stereo pair, and it
  //                           hardwires `pair_slot_o = 4'd0`, so slot 0 only
  //    AUDIO_IF_SLOTS_P == S  KL_tdm_capture - S/2 pairs on slots 0..S/2-1
  //
  //  This is the check the repo did not have. Every other consistency gate
  //  here compares a declaration against ANOTHER declaration (config ->
  //  generated svh -> CSR -> descriptor counts); this one compares the
  //  emitted width against the RTL that has to produce it, and it is why
  //  TALKER_WIRE_CHANS_P cannot be raised to silence the build gate without
  //  raising the framer first (roadmap item 5 owns that).
  //
  //  SCOPE, MEASURED FROM THE RTL RATHER THAN ASSUMED. The rule is per
  //  TALKER, not N_STREAMS*C/2 for the whole engine. Historically a talker
  //  whose pair slots were never driven never advanced nsamp_r, so pend_r
  //  never set and it emitted NO FRAME AT ALL after answering ACMP SUCCESS -
  //  the W3 finding, and a violation of Milan 5.3.7.3's first sentence for a
  //  bound Stream Output. CLOSED 2026-07-28 by KL_pair_zero_fill (below the
  //  capture/playback mux): every consumed pair slot now strobes at the
  //  media rate, silence where no source feeds it, so an armed talker always
  //  frames. What remains a REPORTED fact - by
  //  scripts/check_wire_accountability.py, as information rather than a
  //  compliance failure - is physical SOURCE COVERAGE: which of those slots
  //  carry a real capture channel (AX7101: 16 of 32; Arty TDM8+I2S: 5 of 8),
  //  a product truth that no clause turns into a defect. Making the width
  //  rule an elaboration error stays correct (this guard); making COVERAGE
  //  one would refuse every shipping shape over unpatched inputs - the
  //  2026-07-27 wrong attempt (a) again.
  //
  //  ONE format string ($error takes later arguments as VALUES - a "wrapped"
  //  message prints its continuation strings as integers).
  // ==========================================================================
  //! blend (HANDOVER 8.3b): the I2S pair rides at slot 0 and the TDM pairs
  //! shift up one, so the supply grows by exactly one pair
  localparam int AIF_PAIRS_C = (AUDIO_IF_SLOTS_P == 0)
                             ? 1
                             : AUDIO_IF_SLOTS_P / 2 +
                               ((AUDIO_IF_I2S_PAIR_P != 0) ? 1 : 0);
  localparam int WIRE_PAIRS_NEEDED_C = TALKER_WIRE_CHANS_P / 2;
  if (AUDIO_IF_I2S_PAIR_P != 0 &&
      (AUDIO_IF_MASTER_P == 0 || AUDIO_IF_SLOTS_P == 0))
    $error("milan_datapath: AUDIO_IF_I2S_PAIR_P=1 blends the stereo I2S front-end beside a TDM MASTER (HANDOVER 8.3b). With AUDIO_IF_MASTER_P=%0d / AUDIO_IF_SLOTS_P=%0d there is no master to blend with: a SLAVE shares the i2s mclk pin and the plain I2S build already IS the I2S front-end.",
           AUDIO_IF_MASTER_P, AUDIO_IF_SLOTS_P);
  else if (TALKER_WIRE_CHANS_P < 2 || TALKER_WIRE_CHANS_P > 8 ||
      (TALKER_WIRE_CHANS_P % 2) != 0)
    $error("milan_datapath: TALKER_WIRE_CHANS_P=%0d is not an even 2..8. It is the channels_per_frame the framer emits (IEEE 1722-2016 7.3.3) and the pair stream is 2-channel-granular.",
           TALKER_WIRE_CHANS_P);
  else if (WIRE_PAIRS_NEEDED_C > AIF_PAIRS_C)
    $error("milan_datapath: the fabric cannot emit what this build declares. TALKER_WIRE_CHANS_P=%0d needs %0d fed pair slots per talker and the capture front-end selected by AUDIO_IF_SLOTS_P=%0d supplies %0d in total. Raise the framer per docs/ENDSTATION_BUILDER.md section 3. Do NOT lower the entity's declared format, which was tried on 2026-07-27 (dade536) and reverted (e103d8e): it makes an 8x8 board advertise itself as stereo forever.",
           TALKER_WIRE_CHANS_P, WIRE_PAIRS_NEEDED_C, AUDIO_IF_SLOTS_P,
           AIF_PAIRS_C);

  // ==========================================================================
  //  TDM MASTER CLOCK ACCOUNTABILITY (the same rule as above, one layer down).
  //
  //  A master GENERATES the bus, so its sample rate is not something a codec
  //  hands us - it is an arithmetic consequence of the clock we divide:
  //
  //      bclk      = SLOTS x WORD_BITS x fs          (the TDM frame is fs)
  //      clk_tdm_i = 2 x BCLK_HALF x bclk            (a toggle divider)
  //
  //  so clk_tdm_i must be an EXACT even multiple of SLOTS*32*fs. If it is not,
  //  the front-end still runs - it just frames at the wrong rate, and a talker
  //  whose media clock is off by percent is a talker whose listener throws
  //  every frame away with a timestamp error instead of a format error. That
  //  is the same shape of defect as the 8ch-vs-2ch gap: a build that looks
  //  green and does not work on the wire. So it is refused HERE.
  //
  //  Worked, because the numbers are the reason this guard exists (2026-07-28):
  //    TDM8  x 32 @ 48 kHz -> bclk 12.288 MHz -> clk_tdm_i 24.576 MHz  (HALF 1)
  //    TDM16 x 32 @ 48 kHz -> bclk 24.576 MHz -> clk_tdm_i 49.152 MHz  (HALF 1)
  //    TDM32 x 32 @ 48 kHz -> bclk 49.152 MHz -> clk_tdm_i 98.304 MHz  (HALF 1)
  //  The shipping audio MMCM is 24.576 MHz, so ONLY the first is reachable
  //  from it and the other two need their own MMCM output - see the
  //  `audio_tdm_hz` plan in sw/litex/milan_soc.py _CRG, which re-derives the
  //  two-stage integer chain so one VCO serves 24.576 MHz (the CRF/DAC/servo
  //  contract, untouched in Hz) and 98.304/49.152 MHz (this clock).
  //
  //  ONE format string.
  // ==========================================================================
  localparam int AIF_WORD_BITS_C = 32;                   //! bclks per TDM slot
  localparam int AIF_BCLK_HZ_C   = AUDIO_IF_SLOTS_P * AIF_WORD_BITS_C *
                                   AUDIO_IF_FS_HZ_P;
  //! guarded against 0 so the DEFAULT (I2S, SLOTS 0) elaboration never divides
  //! by zero - it is the shape every lint run and every shipping build uses.
  localparam int AIF_BCLK_HALF_C = (AIF_BCLK_HZ_C <= 0) ? 1
                                 : AUDIO_IF_CLK_HZ_P / (2 * AIF_BCLK_HZ_C);
  if (AUDIO_IF_MASTER_P != 0 && AUDIO_IF_SLOTS_P == 0)
    $error("milan_datapath: AUDIO_IF_MASTER_P=1 with AUDIO_IF_SLOTS_P=0 asks for a TDM bus master on a build whose capture front-end is the stereo I2S one (KL_aaf_capture_i2s, which is already its own I2S clock master). Select a TDM slot count or leave the master off.");
  else if (AUDIO_IF_MASTER_P != 0 &&
           (AIF_BCLK_HALF_C < 1 ||
            AUDIO_IF_CLK_HZ_P != 2 * AIF_BCLK_HALF_C * AIF_BCLK_HZ_C))
    $error("milan_datapath: the TDM MASTER cannot generate the bus this build declares. AUDIO_IF_SLOTS_P=%0d x %0d-bit slots at AUDIO_IF_FS_HZ_P=%0d Hz needs a %0d Hz bit clock, so clk_tdm_i must be an exact even multiple of it, and AUDIO_IF_CLK_HZ_P=%0d is not (nearest half-period divider %0d). Give the master its own MMCM output at 2 x the bit clock (sw/litex/milan_soc.py _CRG audio_tdm_hz) - do NOT re-rate clk_audio_i, which is 24.576 MHz by contract for KL_crf_tx /512, KL_i2s_playback and KL_mmcm_drp_servo.",
           AUDIO_IF_SLOTS_P, AIF_WORD_BITS_C, AUDIO_IF_FS_HZ_P, AIF_BCLK_HZ_C,
           AUDIO_IF_CLK_HZ_P, AIF_BCLK_HALF_C);

  //! item-4 front-end select: the pair-stream contract is identical, so only
  //! the physical half swaps (I2S master / TDM slave / TDM master). The two
  //! TDM roles are SIBLING MODULES rather than one module with a role
  //! parameter because KL_tdm_capture genuinely clocks on `posedge
  //! tdm_bclk_i` and a master cannot: it would have to synthesise a clock net
  //! and close timing on it. The master runs in clk_tdm_i and treats bclk as
  //! a generated SIGNAL with a rising-edge enable (the clean-clock discipline,
  //! KL_aaf_capture_i2s 07-18 lineage), so the proven slave path is untouched.
  generate if (AUDIO_IF_SLOTS_P == 0) begin : g_aif_i2s
    KL_aaf_capture_i2s aaf_capture (
      .clk_i (axis_clk), .rst_n (axis_resetn),
      .clk_audio_i (clk_audio_i),
      .tone_en_i (cfg_tone_enable), .tone_smp_i (tone_smp),
      .i2s_mclk_o (i2s_mclk_o), .i2s_sclk_o (i2s_sclk_o),
      .i2s_lrck_o (i2s_lrck_o), .i2s_sdout_i (i2s_sdout_i),
      .pair_valid_o (aafcap_pv_w), .pair_slot_o (aafcap_slot_w),
      .pair_l_o (aafcap_l_w), .pair_r_o (aafcap_r_w),
      .pairs_captured_o (aaf_pairs_w)
    );
    //! no TDM bus on this build: the master pins park (the SoC leaves them
    //! open, so this constant costs nothing after synthesis)
    assign tdm_bclk_o  = 1'b0;
    assign tdm_fsync_o = 1'b0;
    assign tdm_mclk_o  = 1'b0;
  end else if (AUDIO_IF_MASTER_P != 0) begin : g_aif_tdm_master
    //! TDM MASTER: we make bclk and fsync, so the front-end needs nobody to
    //! drive it - which is the difference between an interface the config
    //! DECLARES and one the fabric BACKS. Same {pair_slot, L, R} contract.
    if (AUDIO_IF_I2S_PAIR_P == 0) begin : g_solo
    KL_tdm_capture_master #(
      .SLOTS_P      (AUDIO_IF_SLOTS_P),
      .WORD_BITS_P  (AIF_WORD_BITS_C),
      .BCLK_HALF_P  (AIF_BCLK_HALF_C),
      .DATA_DELAY_P (1'b1)
    ) aaf_capture (
      .clk_i (axis_clk), .rst_n (axis_resetn),
      .clk_audio_i (clk_tdm_i),
      .tdm_mclk_o (i2s_mclk_o), .tdm_bclk_o (tdm_bclk_o),
      .tdm_fsync_o (tdm_fsync_o), .tdm_data_i (tdm_data_i),
      .pair_valid_o (aafcap_pv_w), .pair_slot_o (aafcap_slot_w),
      .pair_l_o (aafcap_l_w), .pair_r_o (aafcap_r_w),
      .pairs_captured_o (aaf_pairs_w)
    );
    assign i2s_sclk_o = 1'b0;
    assign i2s_lrck_o = 1'b0;
    //! solo master: mclk rides i2s_mclk_o exactly as before (the AX7101 J11
    //! binding); the dedicated pad is for the blend shape only
    assign tdm_mclk_o = 1'b0;
    end else begin : g_blend
    //! HANDOVER 8.3b - the Arty audio shape: BOTH front-ends live. The I2S
    //! capture keeps every Pmod I2S2 pin (mclk on D13 - the CS5343, the
    //! bench analog loop) and feeds pair slot 0 ("channels 1/2 stay the I2S
    //! Pmod", USER 2026-07-28); the TDM master gets its OWN mclk pad and its
    //! pairs ride slots 1..S/2 (KL_pair_blend). At TDM8 off the shipping
    //! 24.576 MHz audio clock this adds NO new clock domain: clk_tdm_i IS
    //! clk_audio_i's rate, BCLK_HALF_P = 1, bclk = 12.288 MHz exactly.
    wire        bl_i2s_pv_w;
    wire [23:0] bl_i2s_l_w, bl_i2s_r_w;
    wire        bl_tdm_pv_w;
    wire [3:0]  bl_tdm_slot_w;
    wire [23:0] bl_tdm_l_w, bl_tdm_r_w;
    KL_aaf_capture_i2s aaf_capture_i2s (
      .clk_i (axis_clk), .rst_n (axis_resetn),
      .clk_audio_i (clk_audio_i),
      .tone_en_i (cfg_tone_enable), .tone_smp_i (tone_smp),
      .i2s_mclk_o (i2s_mclk_o), .i2s_sclk_o (i2s_sclk_o),
      .i2s_lrck_o (i2s_lrck_o), .i2s_sdout_i (i2s_sdout_i),
      .pair_valid_o (bl_i2s_pv_w), .pair_slot_o (),
      .pair_l_o (bl_i2s_l_w), .pair_r_o (bl_i2s_r_w),
      .pairs_captured_o ()
    );
    KL_tdm_capture_master #(
      .SLOTS_P      (AUDIO_IF_SLOTS_P),
      .WORD_BITS_P  (AIF_WORD_BITS_C),
      .BCLK_HALF_P  (AIF_BCLK_HALF_C),
      .DATA_DELAY_P (1'b1)
    ) aaf_capture (
      .clk_i (axis_clk), .rst_n (axis_resetn),
      .clk_audio_i (clk_tdm_i),
      .tdm_mclk_o (tdm_mclk_o), .tdm_bclk_o (tdm_bclk_o),
      .tdm_fsync_o (tdm_fsync_o), .tdm_data_i (tdm_data_i),
      .pair_valid_o (bl_tdm_pv_w), .pair_slot_o (bl_tdm_slot_w),
      .pair_l_o (bl_tdm_l_w), .pair_r_o (bl_tdm_r_w),
      .pairs_captured_o ()
    );
    KL_pair_blend #(.TDM_SLOTS_P (AUDIO_IF_SLOTS_P)) pair_blend (
      .clk_i (axis_clk), .rst_n (axis_resetn),
      .i2s_pair_valid_i (bl_i2s_pv_w),
      .i2s_pair_l_i (bl_i2s_l_w), .i2s_pair_r_i (bl_i2s_r_w),
      .tdm_pair_valid_i (bl_tdm_pv_w), .tdm_pair_slot_i (bl_tdm_slot_w),
      .tdm_pair_l_i (bl_tdm_l_w), .tdm_pair_r_i (bl_tdm_r_w),
      .pair_valid_o (aafcap_pv_w), .pair_slot_o (aafcap_slot_w),
      .pair_l_o (aafcap_l_w), .pair_r_o (aafcap_r_w),
      //! A_AAF_PAIRS: the merged PHYSICAL supply (5 pairs x 48 kHz ~=
      //! 240,000/s on the Arty TDM8+I2S build - the 8.3b acceptance number)
      .pairs_merged_o (aaf_pairs_w)
    );
    end
  end else begin : g_aif_tdm
    //! TDM slave (pulse or 50%-duty fsync, Philips-heritage 1-bit data
    //! delay, 32-bclk slots). The TONE_CTRL pilot override is an I2S-bench
    //! feature and does not reach this front-end (tone_smp unused here).
    KL_tdm_capture #(
      .SLOTS_P      (AUDIO_IF_SLOTS_P),
      .WORD_BITS_P  (32),
      .DATA_DELAY_P (1'b1)
    ) aaf_capture (
      .clk_i (axis_clk), .rst_n (axis_resetn),
      .clk_audio_i (clk_audio_i),
      .tdm_mclk_o (i2s_mclk_o), .tdm_bclk_i (tdm_bclk_i),
      .tdm_fsync_i (tdm_fsync_i), .tdm_data_i (tdm_data_i),
      .pair_valid_o (aafcap_pv_w), .pair_slot_o (aafcap_slot_w),
      .pair_l_o (aafcap_l_w), .pair_r_o (aafcap_r_w),
      .pairs_captured_o (aaf_pairs_w)
    );
    assign i2s_sclk_o  = 1'b0;
    assign i2s_lrck_o  = 1'b0;
    //! SLAVE role: the codec owns bclk/fsync, so our master pins park
    assign tdm_bclk_o  = 1'b0;
    assign tdm_fsync_o = 1'b0;
    assign tdm_mclk_o  = 1'b0;
  end endgenerate

  //  Channel-map CAPTURE mux (docs/CHANNEL_MAP_64.md §4), added alongside.
  //  Sits between the physical capture front-end and the shared packetizer.
  //  cfg_chmap_enable = 0 (reset default) selects the front-end pair stream
  //  BIT-IDENTICALLY (today's compliance wiring); = 1 selects the CMAP-routed source
  //  per media tick. The map RAM resets all-zero, so the enable bit is the
  //  single bypass truth (program CMAP through the 0x900 port, then arm).
  //  Sources are physical capture (I2S/TDM), tone and listener loopback;
  //  source encoding 3 remains reserved and resolves to silence.
  // ==========================================================================
  wire        cmap_pv_w;
  wire [4:0]  cmap_slot_w;
  wire [23:0] cmap_l_w, cmap_r_w;

  //! Capture-side AECP map-write leg. The processor's atomic
  //! ADD/REMOVE_AUDIO_MAPPINGS transaction server drives it after every row
  //! has passed validation. The CSR 0x900 window remains a diagnostic writer.
  //! A slot past N_STREAMS*4 is refused, never wrapped.
  wire        aecp_odmap_wr_p_w;
  wire [5:0]  aecp_odmap_wr_slot_w;
  wire [12:0] aecp_odmap_wr_word_w;
  logic       amap_edit_owr_p_r;
  logic [5:0] amap_edit_owr_slot_r;
  logic [12:0] amap_edit_owr_word_r;
  logic       amap_edit_txn_active_r;
  //! task #26 shape truth from the AECP builder (the one module that
  //! compiles the generated ROM): 1 = this build carries the dynamic-map
  //! writers + boot seeder for that side. Elaboration constants.
  wire        aecp_dmap_dyn_w;
  wire        aecp_odmap_dyn_w;

  //! The RX wire-channel space BOTH channel crossbars de-interleave, defined
  //! ONCE and read twice (KL_chan_map_render.N_CH_P below, and the LOOP
  //! bucket's N_LB_CH_P here). It was a bare literal 8 at the render site; a
  //! second bare 8 here would be a constant mirrored into two places, which
  //! agrees on day one and diverges in silence.
  localparam int RX_WIRE_CHANS_C = 8;

  //! task #65 - the rx -> talker LOOPBACK feed. KL_chan_map_capture's LOOP
  //! bucket (SRC_LOOP = 3'd5) has existed since 2026-07-28, and the AEM
  //! advertises 8 loopback AUDIO_CLUSTERs per talker port - but these five
  //! inputs were never connected here, so they took their `= 0` defaults and
  //! EVERY loopback cluster selected silence. The clusters were an
  //! advertisement the fabric could not back.
  //!
  //! LOOPBACK_P is what backs it, and it is OFF by default because the lane
  //! is NOT free. Measured OOC on the leaf at the 8x8 ship shape (yosys
  //! synth_xilinx xc7, N_LB_STREAMS_P=8 / N_LB_CH_P=8):
  //!
  //!     pre-queue driven (0x0030 era)  3735 LUT / 3021 FF
  //!     0x0036 paced-replay driven     5874 LUT / 4172 FF / 1 RAMB36
  //!
  //! The 0x0036 delta is the audible-defect-C fix: the per-pair elastic
  //! queues (256 x 48 b array = the RAMB36) plus their per-pair pointer
  //! sets, the commit skid and the pre-walk pop engine (see the module's
  //! LOOP QUEUE banner). The 32 x 48 b hold bank itself stays flops (it
  //! takes a full-clear reset and the bind-wipe flush). At 61,039/63,400
  //! LUT and packing-bound the ON lane does not fit today - hence the
  //! lever, and hence the power-on mapper skipping this unbacked pool
  //! (endstation_builder PRIMARY_ROLE_ORDER). OFF still prunes: the feed
  //! strobe folds to constant 0, so queues, skid and holds never toggle
  //! and synthesis sweeps the bucket. The two are driven by ONE declared
  //! fact (cluster_mapping.fabric.loopback_lane), so the model can never
  //! advertise a lane this parameter did not build.
  localparam int LB_STREAMS_C = (LOOPBACK_P != 0) ? N_STREAMS : 1;
  localparam int LB_CH_C      = (LOOPBACK_P != 0) ? RX_WIRE_CHANS_C : 2;

  //! Declared at the point of USE: the depacketizer that drives them is
  //! elaborated ~3000 lines below, so the nets are declared here and driven
  //! by single-driver continuous assigns down there (search lb_tap_).
  wire [TDATA_WIDTH-1:0]  lb_tap_tdata_w;
  //! tap strobes TB-observable (the rend_pcm_tvalid_w discipline): the tap
  //! is a clone with no counter of its own, so desk legs need the nets
  wire                    lb_tap_tvalid_w /* verilator public_flat_rd */;
  wire                    lb_tap_tlast_w  /* verilator public_flat_rd */;
  wire [3:0]              lb_tap_tuser_w  /* verilator public_flat_rd */;
  wire [LB_STREAMS_C*4-1:0] lb_tap_chans_w;
  //! 0x0036 queue slip evidence, TB-observable (same discipline as
  //! rend_pcm_tvalid_w below): not CSR-mapped yet - the debug-window word
  //! is the documented follow-up
  wire [15:0] lb_dup_cnt_w  /* verilator public_flat_rd */;
  wire [15:0] lb_skip_cnt_w /* verilator public_flat_rd */;
  //! #74: the fsync-grid-vs-media-grid slip at the TDM hold junction. The
  //! LOOP counters above watch only the queue bucket; this pair is the
  //! observable that makes "no sample slip" falsifiable at the root.
  wire [15:0] tdm_dup_cnt_w  /* verilator public_flat_rd */;
  wire [15:0] tdm_skip_cnt_w /* verilator public_flat_rd */;

  wire [N_STREAMS*8*13-1:0] cmap_flat_w;   //! GET_AUDIO_MAP OUTPUT walk
  logic [N_STREAMS*8-1:0] amap_out_owner_v_r;
  logic [N_STREAMS*8*16-1:0] amap_out_owner_r;
  logic [N_STREAMS*8*16-1:0] amap_out_cluster_r;

  KL_chan_map_capture #(
    .N_SLOTS_P (N_STREAMS*4),
    .N_TDM_P   (8),
    //! ON: sized to exactly what the AEM declares - talker t's loopback pool
    //! is rx stream t's wire channels, so the bucket keeps every listener
    //! stream at the full rx wire width. Anything smaller would re-open the
    //! same gap for the streams it dropped. OFF: the smallest legal bucket,
    //! with the feed tied off below, so synthesis prunes the bank entirely.
    .N_LB_STREAMS_P (LB_STREAMS_C),
    .N_LB_CH_P      (LB_CH_C)
  ) chan_map_capture (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    //! PER-CHANNEL store (0x0027, USER "one cluster == one audio channel"):
    //! the key space is N_STREAMS*8 channels. The live AECP transaction leg
    //! passes a 13-bit word straight through. The CSR window composes
    //! {en=WORD[15], half=WORD[8], src=WORD[14:12],
    //! idxh=WORD[7:4], idx=WORD[3:0]} - WORD[8] was reserved.
    .map_wr_en_i   ((aecp_odmap_wr_p_w &&
                     32'(aecp_odmap_wr_slot_w) < N_STREAMS*8) ||
                    (!aecp_odmap_wr_p_w && !amap_edit_txn_active_r
                     && !aecp_locked
                     && cfg_chmap_wr_en &&
                     cfg_chmap_wr_side &&
                     32'(cfg_chmap_wr_addr) < N_STREAMS*8)),
    .map_wr_addr_i (aecp_odmap_wr_p_w
                    ? aecp_odmap_wr_slot_w[$clog2(N_STREAMS*8)-1:0]
                    : cfg_chmap_wr_addr[$clog2(N_STREAMS*8)-1:0]),
    .map_wr_data_i (aecp_odmap_wr_p_w
                    ? aecp_odmap_wr_word_w
                    : {cfg_chmap_wr_data[15], cfg_chmap_wr_data[8],
                       cfg_chmap_wr_data[14:12], cfg_chmap_wr_data[7:4],
                       cfg_chmap_wr_data[3:0]}),
    //! map-RAM readback -> CSR 0x910/0x914. The CSR holds map_rd_en_i with a
    //! stable address until map_rd_valid_o; this port is the ONLY way software
    //! can tell a mapped-and-never-fed channel from a mapped-and-quiet one.
    .map_rd_en_i   (cfg_chmap_rd_en && cfg_chmap_rd_side),
    .map_rd_addr_i (cfg_chmap_rd_addr[$clog2(N_STREAMS*8)-1:0]),
    .map_rd_data_o (cmap_rd_data_w), .map_rd_valid_o (cmap_rd_valid_w),
    .map_flat_o    (cmap_flat_w),
    .i2s_pair_valid_i (aafcap_pv_w),
    .i2s_l_i (aafcap_l_w), .i2s_r_i (aafcap_r_w),
    //! THE SLOT-INDEXED PHYSICAL BUCKET. i2s_pair_valid_i above lands in a
    //! SINGLE 48-bit hold (KL_chan_map_capture.sv:444 "the single stereo I2S
    //! pair", read with the cluster's idx IGNORED), so it can only ever carry
    //! two channels - feed a 4-pair TDM8 master into it and all four slots
    //! collapse onto whichever pair was written last. tdm_hold_r[] is the
    //! bucket sized for the job (N_TDM_P=8 -> 4 pairs, already elaborated),
    //! and it was tied off, so a physical cluster beyond channels 0..1 could
    //! never be backed on ANY shape. Every front end - I2S capture, TDM
    //! slave, TDM master, blend - emits the same {pair_valid, pair_slot, L, R}
    //! contract, so one wiring serves all of them; an I2S-only front end just
    //! parks at slot 0.
    .tdm_pair_valid_i (aafcap_pv_w), .tdm_pair_slot_i (aafcap_slot_w),
    .tdm_l_i (aafcap_l_w), .tdm_r_i (aafcap_r_w),
    //! the media-grid pilot (task #59): stepped by the same media_tick_p as
    //! the walk below, never the clk_audio-grid tone_smp
    .tone_smp_i (tone_smp_media),
    //! task #65: the LOOP bucket's feed - the depacketizer payload clone,
    //! same accepted-beat discipline as the render crossbar's tap
    //! (tvalid && tready; this port never backpressures).
    .lb_tdata_i (lb_tap_tdata_w), .lb_tvalid_i (lb_tap_tvalid_w),
    .lb_tlast_i (lb_tap_tlast_w), .lb_tuser_i (lb_tap_tuser_w),
    .lb_wire_chans_i (lb_tap_chans_w),
    //! 0x0036 paced-replay rework: a sink's bind wipe (task #32 eviction
    //! pulse, declared at the stream table below) flushes that stream's
    //! LOOP pair queues, so no stale samples replay on a rebind
    .lb_flush_i (strtbl_bind_fall_w[LB_STREAMS_C-1:0]),
    .tick_i (media_tick_p),
    .pair_valid_o (cmap_pv_w), .pair_slot_o (cmap_slot_w),
    .pair_l_o (cmap_l_w), .pair_r_o (cmap_r_w),
    //! honest-slip evidence (dup-on-empty / drop-oldest, ZERO at lock)
    .lb_dup_cnt_o (lb_dup_cnt_w), .lb_skip_cnt_o (lb_skip_cnt_w),
    //! #74 junction evidence: fsync-frame writes vs media-tick reads
    .tdm_dup_cnt_o (tdm_dup_cnt_w), .tdm_skip_cnt_o (tdm_skip_cnt_w)
  );

  // ==========================================================================
  //  Milan 5.3.7.3 silence fill (KL_pair_zero_fill): every pair slot the
  //  packetizer consumes strobes at the media rate, so a BOUND talker frames
  //  whether or not a physical source feeds it - real audio where fed, legal
  //  PCM silence where not. Before this, a talker whose slots were never
  //  strobed emitted NO FRAME AT ALL after answering ACMP SUCCESS (the W3
  //  finding: AX7101 talkers 4-7, Arty 4x4 talkers 2-3), which is the state
  //  the clause's first sentence forbids. Admission is untouched: an UNBOUND
  //  talker still emits nothing, because stream_en_i gates the packetizer -
  //  the fill only matters for a talker that is armed and unfed.
  //
  //  The fill grid is clk_audio_i/512 = 48.000 kHz EXACTLY - the same VCO
  //  every front-end divides - never the milan-clk media_tick_p divider
  //  (48.03 kHz at 50 MHz): a +640 ppm silence stream would drift against
  //  its own declared rate and collect LATE_TIMESTAMP at the listener.
  // ==========================================================================
  localparam int ZF_TOTAL_C = N_STREAMS * (TALKER_WIRE_CHANS_P / 2);
  logic [8:0] zf_adiv_r;
  logic       zf_apulse_r;
  //! clk_audio domain with the axis reset - the KL_tone_gen precedent above
  always_ff @(posedge clk_audio_i) begin : zf_audio_div
    if (!axis_resetn) begin
      zf_adiv_r   <= '0;
      zf_apulse_r <= 1'b0;
    end else begin
      zf_adiv_r   <= zf_adiv_r + 1'b1;
      zf_apulse_r <= (zf_adiv_r == 9'd511);
    end
  end : zf_audio_div
  wire zf_tick_w;
  cdc_pulse zf_tick_cdc (
    .src_clk (clk_audio_i), .src_rst_n (axis_resetn),
    .src_pulse (zf_apulse_r),
    .dest_clk (axis_clk), .dest_rst_n (axis_resetn),
    .dest_pulse (zf_tick_w)
  );
  wire        zf_pv_w;
  wire [4:0]  zf_slot_w;
  wire [23:0] zf_l_w, zf_r_w;
  KL_pair_zero_fill #(.TOTAL_P (ZF_TOTAL_C), .SLOT_W_P (5)) pair_zero_fill (
    .clk_i (axis_clk), .rst_n (axis_resetn), .tick_i (zf_tick_w),
    .pair_valid_i (aafcap_pv_w), .pair_slot_i ({1'b0, aafcap_slot_w}),
    .pair_l_i (aafcap_l_w), .pair_r_i (aafcap_r_w),
    .pair_valid_o (zf_pv_w), .pair_slot_o (zf_slot_w),
    .pair_l_o (zf_l_w), .pair_r_o (zf_r_w),
    //! fills are deliberately NOT in A_AAF_PAIRS (that instrument counts
    //! captured physical pairs - R5); the observable is the bound talker's
    //! FRAMES_TX and the wire itself
    .fill_cnt_o ()
  );

  //! task #26 (USER: the ATDECC map IS the model): on a shape that
  //! compiled the capture-map machinery the crossbar is IN-CIRCUIT BY
  //! CURRENT CONSTRUCTION: the map RAM resets to silence and has no AECP
  //! writer or boot seeder. The declared front-end routing stays selected
  //! after reset. Software writes the map through the CSR window and then
  //! uses CHMAP_CTRL[0] to select that crossbar in place of the front end.
  //! cfg_chmap_enable (CHMAP_CTRL[0], documented with the chmap 0x900 fabric
  //! below) is declared here ahead of its first reader (#193).
  wire        cfg_chmap_enable;
  wire        cap_xbar_live_w = aecp_odmap_dyn_w | cfg_chmap_enable;
  wire        pkt_pv_w   = cap_xbar_live_w ? cmap_pv_w   : zf_pv_w;
  wire [4:0]  pkt_slot_w = cap_xbar_live_w ? cmap_slot_w : zf_slot_w;
  wire [23:0] pkt_l_w    = cap_xbar_live_w ? cmap_l_w    : zf_l_w;
  wire [23:0] pkt_r_w    = cap_xbar_live_w ? cmap_r_w    : zf_r_w;

  //! lwsrp_adopt_valid/lwsrp_op_prio/lwsrp_op_vid: the Domain adoption
  //! pair the AAF C-TAG muxes read, declared ahead of aaf_packetizer,
  //! their first reader (#193); documented with the LWSRP_DOM 0x788
  //! block below.
  wire        lwsrp_adopt_valid;
  wire [7:0]  lwsrp_op_prio;
  wire [11:0] lwsrp_op_vid;
  KL_aaf_packetizer #(.N_TALKERS_P(N_STREAMS),
                      .WIRE_CHANS_P(TALKER_WIRE_CHANS_P)) aaf_packetizer (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .pair_valid_i (pkt_pv_w), .pair_slot_i (pkt_slot_w),
    .pair_l_i (pkt_l_w), .pair_r_i (pkt_r_w),
    //! t0 = the legacy admission gate bit-identically; t>0 = TCTX CTRL[0]
    //! (window) & per-stream lwSRP gate & the engine-wide MAAP term (the
    //! composed aaf_stream_en_w - see its comment for the honest gaps)
    .stream_en_i (aaf_stream_en_w),
    .dest_mac_i (eff_aaf_dmac),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    //! the AAF C-TAG {PCP, VID}: the Milan 4.2.7.2.1 OPERATIONAL pair while
    //! a Domain is adopted (dom_ovr_i also bypasses the per-talker TCTX vid
    //! - the reservation declares the adopted VID, so the frames must carry
    //! it), the software defaults otherwise. AAF_CTRL[27:16] stays the
    //! software-owned default VID.
    .vlan_vid_i (lwsrp_adopt_valid ? lwsrp_op_vid : cfg_aaf_vid),
    .vlan_pcp_i (lwsrp_adopt_valid ? lwsrp_op_prio[2:0]
                                   : SR_CLASS_A_PRIO_C[2:0]),
    .dom_ovr_i  (lwsrp_adopt_valid),
    //! per-talker slice of the AECP per-STREAM_OUTPUT offset file: talker
    //! t stamps its avtp_timestamp with ITS OWN entry t
    .transit_ns_i (aecp_pres_offset[N_STREAMS*32-1:0]),
    .ptp_ns_i (ptp_now_w),
    .ts_uncertain_i (clkv_tu_w),
    //! P12: TCTX window port <- the CSR 0x800 window (talker dir)
    .tctx_wr_en_i (csr_tctx_wr_p_w), .tctx_wr_addr_i (csr_tctx_wr_addr_w),
    .tctx_wr_data_i (csr_tctx_wr_data_w), .tctx_wr_rdy_o (tctx_wr_rdy_w),
    .tctx_rd_en_i (csr_tctx_rd_en_w), .tctx_rd_addr_i (csr_tctx_rd_addr_w),
    .tctx_rd_data_o (tctx_rd_data_w), .tctx_rd_valid_o (tctx_rd_valid_w),
    .m_axis_tdata (aaf_tx_tdata), .m_axis_tkeep (aaf_tx_tkeep),
    .m_axis_tvalid(aaf_tx_tvalid), .m_axis_tlast (aaf_tx_tlast),
    .m_axis_tready(aaf_tx_tready),
    .frames_sent_o (aaf_frames_w),
    //! IEEE 1722-2016 4.4.4.3 media clock restart level, per talker
    .mr_i (aaf_mr_w),
    //! Milan Table 5.4 event feed (KL_talker_diag_ctx): the strobe, the
    //! talker, and the tu/mr bits that PDU actually carried
    .frame_p_o (aaf_frame_p_w), .frame_idx_o (aaf_frame_idx_w),
    .frame_tu_o (aaf_frame_tu_w),
    .frame_mr_o (aaf_frame_mr_w)
  );
  // arbiter out -> MAC-facing TX
  assign m_axis_mac_tx_tdata  = tx_axis_to_mac.tdata;
  assign m_axis_mac_tx_tkeep  = tx_axis_to_mac.tkeep;
  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;
  assign m_axis_mac_tx_tlast  = tx_axis_to_mac.tlast;
  assign tx_axis_to_mac.tready = m_axis_mac_tx_tready;
  //! MAC-facing RX -> the shared pre-filter tap. The ptp_ts_top RX stamper
  //! that sat on this hop was a combinational pass-through whose records
  //! nothing consumed; the fabric gPTP plane stamps its own ingress off
  //! rx_axis_fabric and its egress at the MAC boundary (KL_gptp_txstamp).
  assign rx_axis_from_mac.tdata  = s_axis_mac_rx_tdata;
  assign rx_axis_from_mac.tkeep  = s_axis_mac_rx_tkeep;
  assign rx_axis_from_mac.tvalid = s_axis_mac_rx_tvalid;
  assign rx_axis_from_mac.tlast  = s_axis_mac_rx_tlast;
  assign s_axis_mac_rx_tready = rx_axis_from_mac.tready;
  //! The filtered RX stream is consumed only by fabric observers. They are
  //! handshake-qualified but never apply backpressure, so the shared tap is
  //! permanently ready.
  assign rx_axis_fabric.tready = 1'b1;

  // ==========================================================================
  //  CSR <-> datapath signals
  // ==========================================================================
  wire        cfg_mac_tx_en, cfg_mac_rx_en, cfg_mac_promisc, cfg_mac_allmulti, cfg_mac_is_1g;
  wire [7:0]  cfg_mac_ifg;
  //! cfg_mac_addr is declared above station_mac_be_w (its first reader)
  wire [63:0] cfg_mc_hash;
  wire        cfg_phy_reset_n;

  wire        cfg_stats_snapshot, cfg_stats_reset;
  wire [32*9-1:0] stats_counts;
  wire        stats_rollover;

  wire        cfg_ptp_enable;
  wire [31:0] cfg_ptp_incr, cfg_ptp_adj;
  wire [63:0] cfg_ptp_tod_wr, cfg_ptp_offset;
  wire        cfg_ptp_cmd_load, cfg_ptp_cmd_adjust, cfg_ptp_cmd_snapshot;
  wire [63:0] ptp_tod_rd;
  wire        ptp_tod_rd_valid;

  wire        cfg_adp_enable;
  wire [63:0] cfg_adp_entity_id, cfg_adp_entity_model_id;
  //! The gPTP engine's publication bank. These declarations live beside the
  //! consumers rather than the late generate block so clock validity, CSR,
  //! and protocol answers all select the same compile-time owner.
  wire [63:0] gptp_pub_gm_w, gptp_pub_parent_w, gptp_pub_annq_w;
  wire [31:0] gptp_pub_flags_w, gptp_pub_pdelay_w, gptp_pub_offset_w;
  wire [7*64-1:0] gptp_pub_path_w;
  wire [3:0] gptp_pub_path_count_w, gptp_pub_path_gen_w;
  wire        gptp_pub_disc_w;
  wire signed [31:0] gptp_adj_w;
  wire               gptp_step_we_w;
  wire        [63:0] gptp_step_w;
  //! One owner for every consumer and the CSR live-read face. With the gPTP
  //! engine absent every publication output is zero; no alternate publisher
  //! exists.
  wire [63:0] cfg_adp_gptp_gm = (GPTP_PLANE_EN_P != 1'b0)
                              ? gptp_pub_gm_w : 64'd0;
  wire [31:0] cfg_gptp_pdelay = (GPTP_PLANE_EN_P != 1'b0)
                              ? gptp_pub_pdelay_w : 32'd0;
  //! Keep the notification and gather faces on the exact selected-owner
  //! value. This alias retains the post-#227 name used by both consumers.
  wire [31:0] eff_gptp_pdelay_w = cfg_gptp_pdelay;
  wire [15:0] cfg_adp_talker_sources, cfg_adp_talker_caps;
  wire [15:0] cfg_adp_listener_sinks, cfg_adp_listener_caps;
  wire [7:0]  cfg_adp_gptp_domain;
  wire [15:0] cfg_adp_current_config, cfg_adp_identify_index;
  wire [31:0] adp_available_index;
  wire [7:0]  adp_depart_cnt, adp_rearm_cnt;
  wire [1:0]  adp_depart_src;
  //! A_ADP_DIAG2 (0x674) sources: egress count, accepted-discover count, last
  //! message_type and the {send_pending, busy, disc_pend, available} nibble
  wire [7:0]  adp_sent_cnt, adp_disc_rx_cnt;
  wire [3:0]  adp_last_msg, adp_state;
  wire        adp_disc_seen_p;   //! any ENTITY_DISCOVER on the wire (counted in milan_csr)

  //! Live processor LOCK_ENTITY level, in the same axis_clk domain as every
  //! local mapping writer and the CSR status mux.
  wire                     aecp_locked;
  wire [15:0]              aecp_current_config, aecp_cmd_count, aecp_resp_count;
  //! gh #59 departing-controller detection (Milan v1.2 §5.4.5.3), CSR 0x6F4
  //! A_CTLR_DIAG: {evictions[31:24], CONTROLLER_AVAILABLE replies seen[23:12],
  //! CONTROLLER_AVAILABLE probes sent[11:0]}
  wire [31:0]              aecp_ctlr_diag;
  //! ACMP stateless responder (KL_acmp_responder) — response AXIS + counters.
  wire [15:0]              acmp_cmd_count, acmp_resp_count;
  //! AAF talker (aaf_talker_i2s): CSR control + frame stream + PHC time
  wire                     cfg_aaf_enable;
  wire                     cfg_aaf_bypass;
  wire [47:0]              cfg_aaf_dmac;
  wire [11:0]              cfg_aaf_vid;
  //! Milan talker SM (docs/overview/ARCHITECTURE.md): ACMP probe state,
  //! the lwSRP listener socket (CSR override retained as the manual lever),
  //! the AECP presentation offset, and the resolved AAF gate.
  wire                     cfg_acmp_lobs;
  //! N-context ACMP talker activation (2026-07-26: the responder runs
  //! KL_acmp_tlkr_ctx at N_SRC_P = N_STREAMS - probes answer for every
  //! talker_unique_id 0..N-1). Bit 0 keeps the legacy scalar consumers.
  //! ACMP talker source contexts = the N audio talkers plus, at N > 1, the
  //! CRF Media Clock Output at talker_unique_id = N_STREAMS (see
  //! g_acmp_crf_src). N = 1 keeps the byte-identical single-source shape.
  //! THE ENTITY SHAPE IS DEFINED BY THE CONFIG, NOT BY THIS FILE.
  //! gen/adp_shape_defaults.svh is GENERATED from configs/endstation_*.yaml
  //! by sw/builder/endstation_builder.py, in the same pass that emits this
  //! shape's AEM descriptor ROM. It gives ADP_TALKER_SRC_C /
  //! ADP_LISTENER_SINK_C - the 1722.1 STREAM_OUTPUT / STREAM_INPUT counts -
  //! and the two capability words. milan_csr `include-s the SAME file and
  //! serves them read-only at 0x618/0x61C, so the number a controller is
  //! told and the number of contexts that can answer it are ONE constant.
  //! Point +incdir at configs/generated/<config>/ to elaborate a different
  //! shape; the tracked hdl/common/gen/ copy is whichever config was
  //! last written with `endstation_builder.py --write-rtl`.
  `include "gen/adp_shape_defaults.svh"
  //! the ONE clock-source compare (see the media-clock banner above; the
  //! block lives here because AEM_CRF_CLKSRC_C exists only after the shape
  //! include). Registered: a SET_CLOCK_SOURCE lands as a clean gate
  //! transition at every consumer, and KL_media_clock_restart's own
  //! clk_src_q_r edge detector sees exactly one change per command.
  always_ff @(posedge axis_clk) begin : media_clk_resolve
    if (!axis_resetn) begin
      media_clk_src_r    <= 16'd0;
      crf_clk_selected_r <= 1'b0;
    end
    else begin
      media_clk_src_r    <= pp_aecp_clk_src_index_w;
      crf_clk_selected_r <= (pp_aecp_clk_src_index_w == AEM_CRF_CLKSRC_C)
                            && (AEM_CRF_CLKSRC_C != 16'hFFFF);
    end
  end : media_clk_resolve
  //! ACMP talker source contexts: the AAF talkers, then the CRF Media Clock
  //! Output at talker_unique_id = the AAF talker count (see g_acmp_crf_src).
  localparam int ACMP_SRC_C = ADP_TALKER_SRC_C;
  localparam int CRF_TUID_C = N_STREAMS;   //! only when ACMP_SRC_C > N_STREAMS
  //! ELABORATION GUARD. g_acmp_src drives sources 0..N_STREAMS-1 and
  //! g_acmp_crf_src drives exactly ONE more, so the only shapes this module
  //! can actually implement are ACMP_SRC_C == N_STREAMS (no CRF output) and
  //! ACMP_SRC_C == N_STREAMS + 1 (with it). Any other value leaves sources
  //! N_STREAMS+1 .. ACMP_SRC_C-1 with an undriven dmac/vid, which Verilator
  //! reports as UNDRIVEN but SYNTHESIS SILENTLY TIES TO ZERO - i.e. talker
  //! sources advertising a null destination MAC. That is not hypothetical:
  //! regenerating the tracked entity definition for the 8x8 ship shape put
  //! ACMP_SRC_C = 9 in front of every N_STREAMS=1 elaboration in the tree.
  //! The 0x0015 claim that a gateware "cannot be handed another shape's
  //! entity definition and still elaborate" was only true by accident; this
  //! makes it true by construction.
  //! ONE format string: $error takes the first argument as the format and
  //! every later one as a VALUE, so a "wrapped" message silently prints the
  //! continuation strings as integers (measured: ADP_TALKER_SRC_C=6253896...).
  if (ACMP_SRC_C != N_STREAMS && ACMP_SRC_C != N_STREAMS + 1)
    $error("milan_datapath: entity definition declares ADP_TALKER_SRC_C=%0d, which is neither N_STREAMS (%0d) nor N_STREAMS+1. Point +incdir at the configs/generated/<config>/ whose shape matches this elaboration (it must come BEFORE hdl/common/csr on the include path), or rebuild the tracked include with endstation_builder.py --write-rtl.",
           ACMP_SRC_C, N_STREAMS);
  //! ACMP listener sink contexts (see the KL_acmp_listener banner below):
  //! the AAF sinks plus the pinned CRF sink at listener_unique_id =
  //! N_STREAMS.
  localparam int ACMP_SINKS_C = ADP_LISTENER_SINK_C;
  localparam int ACMP_SIDXW_C = $clog2(ACMP_SINKS_C);
  wire [ACMP_SRC_C-1:0]    acmp_talker_active_v, acmp_probe_armed_v;
  wire                     acmp_talker_active, acmp_probe_armed;
  //! per-STREAM_OUTPUT presentation offsets from the AECP responder's
  //! register file (SET/GET_MAX_TRANSIT_TIME / SET_STREAM_INFO ACC_LAT):
  //! entry k = talker k's transit offset; the CRF Media Clock Output's
  //! entry sits at CRF_TUID_C. Unbacked entries read the 2 ms default.
  logic [16*32-1:0]        aecp_pres_offset;
  //! SRP CSR bits (0x680). THE ENGINE THEY USED TO ENABLE IS DELETED and the
  //! processor's SRP engine has no enable - it runs whenever the entity does.
  //! What survives is their SECOND job, which is the one the fabric reads:
  //!   cfg_lwsrp_enable    - "a reservation is REQUIRED before this device
  //!                          streams" (FR-SRP-03). Clear it and the AAF/CRF
  //!                          gates stop consulting the admission verdict;
  //!                          it does not stop the processor declaring.
  //!   cfg_lwsrp_talker_en - the same, for the CRF Media Clock Output's
  //!                          emission licence.
  //! Read them as STREAM-ADMISSION POLICY, not as an engine on/off switch.
  wire        cfg_lwsrp_enable, cfg_lwsrp_talker_en;
  //! LWSRP_CTRL[5], reset 0: declare-always bypass of the 4.3.3.1
  //! TalkerAdvertise gate (the pre-gate posture, bring-up escape only)
  wire [11:0] cfg_lwsrp_vid;
  wire [31:0] cfg_lwsrp_latency;
  // ------------------------------------------------------------------------
  //  SR CLASS A FOR THE CRF MEDIA CLOCK OUTPUT (2026-07-28).
  //  Milan v1.2 7.3.3 requires the CRF Media Clock Stream to be carried under
  //  an SRP reservation of class A. It was not: the PDUs left untagged on the
  //  control lane with no MSRP declaration, so the bridge had nothing to
  //  classify and flooded them to every port (measured 2026-07-28: 4001
  //  untagged AVTP/CRF frames in 8 s on a port with no CRF listener, exactly
  //  the 500 PDU/s KL_crf_tx rate, while the same capture saw ZERO AAF frames
  //  - the bridge prunes what IS declared and floods what is not).
  //
  //  THE TALKER ROW IS THE WHOLE POINT. Adding the C-TAG alone would move the
  //  stream from "flooded" to "dropped": 802.1Q 35.1.2 - a declared stream is
  //  forwarded only toward registered Listeners, and an SR-tagged stream with
  //  NO declaration is pruned to zero ports. So the CRF output becomes a real
  //  lwSRP TALKER CONTEXT here, and the tag is derived FROM that row's
  //  provisioning (crft_class_a_w below) - the tagged-but-undeclared state is
  //  unreachable, not merely discouraged.
  //
  //  Row map (KL_lwsrp_top's N_CTX_P banner): listener k -> row k, talker
  //  t -> row (L-1)+t, so the CRF talker at t = N_STREAMS lands on row
  //  (N_STREAMS-1) + N_STREAMS = 2*N_STREAMS-1, one past the AAF talkers,
  //  and the table needs L+T-1 = 2*N_STREAMS rows. Widening N_TALKERS_P by
  //  one is what puts the CRF stream's slope into the bw-gate's Sigma - the
  //  class A queue must budget for the media clock like any other stream.
  //
  //  Only when this shape HAS a CRF Media Clock Output (ACMP_SRC_C >
  //  N_STREAMS, the same condition as g_acmp_crf_src). Configs without one
  //  (arty_current: 1 talker, no CRF output) keep today's row count exactly.
  localparam int SRP_CRF_TK_C   = (ACMP_SRC_C > N_STREAMS) ? 1 : 0;
  localparam int SRP_TALKERS_C  = N_STREAMS + SRP_CRF_TK_C;
  localparam int SRP_CRF_ROW_C  = (N_STREAMS - 1) + N_STREAMS;   //! (L-1)+t
  //! the DEDICATED sink-0 listener row + its (appended) fabric slot - the
  //! ax-rv32-g return-leg fix. Row 0 stays the legacy pair for the TALKER-0
  //! side only; sink 0's Listener attribute now lives one row past the CRF
  //! talker, fabric-provisioned like every other sink's.
  localparam int SRP_LSN0_ROW_C   = N_STREAMS + (N_STREAMS + ((ACMP_SRC_C > N_STREAMS) ? 1 : 0)) - 1;
  localparam int SRP_LSN0_SLOT_C  = (N_STREAMS + ((ACMP_SRC_C > N_STREAMS) ? 1 : 0)) + N_STREAMS - 1;
  //! Reserved legacy row arithmetic for the CRF Media Clock Input sink.
  //! These constants have no consumer after SRP ownership moved to the
  //! protocol processor and do not prove a CRF listener declaration.
  localparam int SRP_CRFSNK_C      = (ADP_LISTENER_SINK_C > N_STREAMS) ? 1 : 0;
  localparam int SRP_CRFSNK_ROW_C  = SRP_LSN0_ROW_C + 1;
  localparam int SRP_CRFSNK_SLOT_C = SRP_LSN0_SLOT_C + 1;
  //! per-stream admission gates from the bw-gate ([0] = legacy CSR row,
  //! [t] = ctx-table talker rows - the P5 vector, plumbed in the P12
  //! follow-up); the flat CSR status keeps bit 0 only. The top slot is the
  //! CRF Media Clock Output when this shape has one.
  wire [SRP_TALKERS_C-1:0] lwsrp_stream_gate;
  //! per-TALKER "registering a Listener Asking Failed attribute", SAME
  //! index law as lwsrp_stream_gate (gh #56 A2: -> ACMP REGISTERING_FAILED)
  wire        lwsrp_slope_en, lwsrp_res_active;
  //! sticky ctx-table shortfall -> LWSRP_STATUS[11]
  wire        lwsrp_ctx_oor_w;
  wire [31:0] lwsrp_idle_slope;
  wire        lwsrp_listener_ready, lwsrp_listener_reg;
  wire [1:0]  lwsrp_listener_decl;
  wire        lwsrp_domain_ok, lwsrp_over_limit, lwsrp_talker_declared;
  //! Milan 4.2.7.2.1 Domain adoption surface (KL_lwsrp_registrar): the
  //! OPERATIONAL {priority, VID} every declaration serializes; when
  //! adopt_valid the AAF/CRF C-TAG muxes below take the same pair, so the
  //! reservation and the frames can never diverge. LWSRP_DOM 0x788.
  //! (lwsrp_adopt_valid, lwsrp_op_prio and lwsrp_op_vid are declared above
  //! aaf_packetizer, their first reader, #193)
  wire        lwsrp_tfail_valid;
  wire [7:0]  lwsrp_tfail_code, lwsrp_rx_drops;
  wire [15:0] lwsrp_tx_count, lwsrp_rx_pdus;
  //! CRF sink-1 bind record (same listener SM) + 0x4B BSCAN forensics
  //! THE CRF MEDIA CLOCK INPUT SINK's bind record. The entity pins it LAST
  //! (listener_unique_id = the AAF sink count), which the deleted listener's
  //! "view1" port got right only at N_STREAMS = 1: on a 4x4 or 8x8 shape it
  //! published AAF sink 1's binding and the CRF receiver locked to an audio
  //! stream. Indexed by the documented law here instead.
  localparam int CRF_SNK_IDX_C = (ACMP_SINKS_C > N_STREAMS) ? N_STREAMS : 0;
  wire        acmpl1_bound;
  wire [63:0] acmpl1_sid;
  wire [31:0] aecp_bdbg0_w, aecp_bdbg1_w, aecp_bdbg2_w;
  //! pp_cd_acmp_bound_vlan_w belongs to the protocol processor class-D
  //! face below; it is declared here because acmpl_vlan_w is its first
  //! reader (#193).
  wire [ACMP_SINKS_C*12-1:0] pp_cd_acmp_bound_vlan_w;
  //! the bound stream's VLAN, kept only for the 0x6A4 status word's field
  wire [11:0] acmpl_vlan_w = pp_cd_acmp_bound_vlan_w[11:0];
  //! ACMP listener bind record, republished from the protocol processor's
  //! class-D face (the legacy KL_acmp_listener state machine is deleted, so
  //! there is no acmp_pkg enum to carry any more - see the ACMP section).
  //! acmpl_state keeps its net so ACMPL_STATE 0x6E0 keeps its shape; it reads
  //! a STRUCTURAL ZERO because no state machine here has a state.
  wire [2:0]  acmpl_state;
  wire        acmpl_bound;
  wire [63:0] acmpl_sid;
  wire [15:0] acmpl_tuid;
  wire [4:0]  acmpl_status;
  wire [1:0]  acmpl_probing;
  wire        acmpl_tk_avail, acmpl_lstn_declare, acmpl_active;
  wire [15:0] acmpl_cmd_count, acmpl_probe_count;
  wire [7:0]  acmpl_tx_wedge;
  wire [31:0] acmpl_dbg;
  //! per-sink ACMP bind view (task-21 fabric half): the lwSRP LISTENER-row
  //! provisioner below derives ctx rows 1..N-1 from these — bound level,
  //! bound stream_id, and a 1-cycle pulse per bind-record write
  wire [ACMP_SINKS_C-1:0]    acmpl_bound_v_w;
  wire [ACMP_SINKS_C*64-1:0] acmpl_sid_v_w;
  //! per-sink probed SRP {dmac, vlan} (record shadows, same write edge as
  //! the sid lane) — the lwSRP listener rows' EXPECTED pair for the
  //! walker's Table 5.29 three-parameter registrar match
  wire        lwsrp_ta_registered, lwsrp_ta_failed;
  //! per-ROW lwSRP registrar levels (KL_lwsrp_ctx): bit 0 = the legacy row-0
  //! registrar, bits 1..15 = the extension lanes. A LISTENER row's bit is
  //! its TalkerAdvertise / TalkerFailed registration, which is exactly the
  //! event Milan 5.5.3.5.42 / 5.5.3.5.48 move a settled sink on.
  //! ...projected onto the ACMP sink index. Sink k's attribute row IS k for
  //! 1..N_STREAMS-1 (srp_fab_row_w's listener branch); sink 0's is the
  //! DEDICATED listener-0 row (SRP_LSN0_ROW_C, the 5-bit-widened space).
  //! This legacy projection has no CRF Media Clock Input listener row. SRP is
  //! now processor-owned, so these fabric bits are not processor SRP evidence.
  wire [7:0]  lwsrp_ta_fail_code;
  //! AVTP RX monitor (KL_avtp_rx_monitor, STREAM_INPUT[0] Table 7-156)
  wire        avtprx_match, avtprx_tu_bit, avtprx_tv_bit, avtprx_mr_bit;
  wire [7:0]  avtprx_subtype, avtprx_seq;
  wire        avtprx_parse_p;
  wire [7:0]  avtprx_b3;
  wire [63:0] avtprx_sid_frame, avtprx_fsh2;
  wire signed [31:0] crf_delta_w, crf_rate_w;
  //! public_flat_rd: [31:16] is the servo's signed 1/16 ppm trim, and it is
  //! the INPUT to the NCO conversion below. A harness that cannot see it
  //! cannot tell "the gate held the trim at zero" from "the servo was idle
  //! and zero anyway" - which is the difference between a check and a
  //! tautology (tb/verilator/milan_dp reports that vacuity rather than
  //! passing through it).
  wire [31:0] mcsrv_stat_w /* verilator public_flat_rd */;   //! KL_mmcm_drp_servo status (A_MCSRV_STAT 0x8F8)
  wire        mcsrv_ps_invert_w;  //! MCSRV_CTRL 0x8FC[0] bench sign knob
  wire        mcsrv_auto_repair_w;//! MCSRV_CTRL 0x8FC[1] bench-gated DRP repair enable (default 0)
  //! chmap 0x900 fabric (docs/CHANNEL_MAP_64.md §6): CSR map-RAM write port +
  //! bypass arm. Default (cfg_chmap_enable=0) leaves the compliance audio path
  //! bit-identical (render/capture crossbars are muxed OUT of both the
  //! packetizer feed and the i2s_playback feed). cfg_chmap_enable itself is
  //! declared above cap_xbar_live_w, its first reader.
  //! Render-side AECP map-write leg. Accepted input transactions project
  //! backed model clusters here; the CSR 0x900 window shares the writer.
  wire        aecp_dmap_wr_p_w;
  wire [5:0]  aecp_dmap_wr_addr_w;
  wire [7:0]  aecp_dmap_wr_word_w;
  logic       amap_edit_iwr_p_r;
  logic [5:0] amap_edit_iwr_addr_r;
  logic [7:0] amap_edit_iwr_word_r;
  wire        cfg_chmap_wr_en;
  wire        cfg_chmap_wr_side;
  wire [5:0]  cfg_chmap_wr_addr;
  wire [15:0] cfg_chmap_wr_data;
  logic [6:0] cfg_chmap_rphys_w;
  always_comb begin : cfg_chmap_rphys
    cfg_chmap_rphys_w = 7'd0;
    for (int k = 0; k < ADP_DMAP_IN_KEYS_C; k++) begin
      if (cfg_chmap_wr_addr == 6'(k))
        cfg_chmap_rphys_w = ADP_DMAP_IN_RPHYS_C[k];
    end
  end : cfg_chmap_rphys
  //! chmap map-RAM READBACK (CSR 0x910/0x914). Both RAM read ports were tied
  //! off here, so the ONLY view software had of the channel map was
  //! CHMAP_WORD 0x908 - which is milan_csr's own shadow of what software last
  //! wrote, not the RAM. A capture slot that is mapped but never fed emits
  //! 24'd0, bit-identical to a slot that is working and quiet, and that
  //! ambiguity is the entire diagnosis on a board with no audio pins.
  wire        cfg_chmap_rd_en;
  wire        cfg_chmap_rd_side;
  wire [5:0]  cfg_chmap_rd_addr;
  //! {loop_fed[14], loop_mapped[13], entry[12:0]} (0x0027 per-channel)
  wire [14:0] cmap_rd_data_w;
  wire        cmap_rd_valid_w;
  wire [7:0]  rmap_rd_data_w;     //! render entry only - that RAM has no mask
  logic       rmap_rd_valid_r;
  //! The two RAMs answer differently and the CSR sees ONE port: CMAP has a
  //! REGISTERED read port with its own valid; RMAP's is COMBINATIONAL with no
  //! valid at all, so register the request to give it the same 1-clock shape.
  //! Both then satisfy the CSR's level-request/valid contract and its
  //! watchdog sees one timing for both sides.
  always_ff @(posedge axis_clk) begin : rmap_rd_valid_S
    if (!axis_resetn) rmap_rd_valid_r <= 1'b0;
    else              rmap_rd_valid_r <= cfg_chmap_rd_en && !cfg_chmap_rd_side;
  end : rmap_rd_valid_S
  wire [15:0] cfg_chmap_rd_data  = cfg_chmap_rd_side ? {1'b0, cmap_rd_data_w}
                                                     : {8'd0, rmap_rd_data_w};
  wire        cfg_chmap_rd_valid = cfg_chmap_rd_side ? cmap_rd_valid_w
                                                     : rmap_rd_valid_r;
  //! all ten CRF sink tallies full-width (gh #61 G1: 32-bit wrapping
  //! backing; CRF_STATUS 0x74C serves documented truncated slices below)
  wire [31:0] crf_pducnt_w;
  wire [31:0] crf_fmterr_w, crf_seqerr_w;
  wire        crf_locked_w;
  //! IEEE 1722-2016 10.4.3 restart echo: the received mr bit TOGGLED on an
  //! accepted PDU of the followed CRF stream (gh #62 H2a)
  wire        crf_mr_toggle_p_w;
  //! the four Table 5.6 interval tallies the CRF sink used to advertise as
  //! valid and never move (traceability AVTP-5t)
  //! CRF talker (KL_crf_tx): CSR control + PDU stream into the control merge
  wire        cfg_crft_en;
  wire [63:0] cfg_crft_sid;
  wire [47:0] cfg_crft_dmac;
  wire [31:0] crft_count_w, crft_stat_w;
  //! the 10.4.3 mr level the CRF Media Clock Output stamps, and the level its
  //! last COMPLETED PDU carried (gh #62 H2b)
  wire        crft_mr_w, crft_tu_last_w, crft_mr_last_w;
  wire [TDATA_WIDTH-1:0]   crft_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] crft_tx_tkeep;
  wire                     crft_tx_tvalid, crft_tx_tlast, crft_tx_tready;
  wire [63:0] avtprx_fsh;
  wire [63:0] aecp_in0_fmt;
  //! public_flat_rd: the media-grid checks assert the trim is pinned BECAUSE
  //! the source is INTERNAL, rather than assuming the harness left it there

  wire        i2spb_converged;
  wire [31:0] i2spb_dbg_frame;
  wire [31:0] avtprx_locked_c, avtprx_unlocked_c, avtprx_intr_c;
  wire [31:0] avtprx_seqmm_c, avtprx_tu_c, avtprx_unsupp_c, avtprx_frx_c;
  wire        avtprx_locked;
  //! per-context Table 5.22 counter-change pulses (gh #60 F2), the
  //! STREAM_INPUT source of the descriptor arbiter feeding the processor
  wire [N_STREAMS-1:0] avtprx_dirty_p_w;
  wire        avtprx_accept_p;
  wire [31:0] avtprx_ts, avtprx_last_ts, avtprx_last_tsd;
  wire [15:0] pcmrx_pdus, pcmrx_drops;
  wire [15:0] i2spb_underruns, i2spb_overruns;
  wire        cfg_i2spb_clru, cfg_i2spb_clro;   //! I2SPB_STAT W1C strobes
  wire signed [15:0] i2spb_trim;
  wire [15:0] i2spb_fill;
  wire [31:0] avtprx_mreset_c, avtprx_late_c, avtprx_early_c;
  wire [31:0] avtprx_tv_c, avtprx_tnv_c;   //! Milan 1.3 tv tallies (in0)
  wire        cfg_tone_enable;
  wire [2:0]  cfg_tone_att;
  wire [23:0] tone_smp;        //! clk_audio/512 grid (I2S front-end override)
  wire [23:0] tone_smp_media;  //! media_tick_p grid (capture crossbar)
  //! MAAP engine (KL_maap, IEEE 1722 Annex B; docs/design/MAAP_FABRIC.md)
  wire        cfg_maap_enable, cfg_maap_seed_valid;
  wire [7:0]  cfg_maap_count;
  wire [15:0] cfg_maap_seed_offset;
  wire [47:0] maap_addr;
  wire        maap_addr_valid;
  wire [1:0]  maap_state;
  wire [15:0] maap_offset;
  wire [7:0]  maap_conflicts, maap_defends;
  wire [TDATA_WIDTH-1:0]   maap_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] maap_tx_tkeep;
  wire                     maap_tx_tvalid, maap_tx_tlast, maap_tx_tready;
  //! effective stream DMAC: MAAP claim when enabled+valid, CSR value else
  //! (en=0 keeps the static-provisioning behavior bit-exact)
  wire [47:0] eff_aaf_dmac = (cfg_maap_enable && maap_addr_valid)
                             ? maap_addr : cfg_aaf_dmac;
  //! "a valid Destination MAC Address is available" is no longer composed
  //! here: KL_pp_maap_shim answers the processor's per-source ALLOC_DA out
  //! of the same KL_maap block claim, so a source without an address simply
  //! never reaches acmp_declaring_o. One decision, one place.
  //! listener_observed: the lwSRP Listener registrar is the real source once
  //! the engine is enabled; A_ACMP_LOBS stays as the manual override socket.
  wire listener_observed_w = cfg_acmp_lobs |
                             (cfg_lwsrp_enable & lwsrp_listener_ready);

  //! per-source ACMP talker parameters. The DMAC/VID/observed/asking-failed
  //! vectors that used to be composed here fed KL_acmp_tlkr_ctx, which is
  //! deleted: the processor resolves a source's destination MAC through its
  //! own ALLOC_DA (KL_pp_maap_shim -> KL_maap, the same block+uid law) and
  //! its own SRP registrar tells it when a Listener is ready. Composing them
  //! here as well would be a second copy of a decision the plane already
  //! makes. Only the per-AAF-talker activity slice survives, because the
  //! FRAMER admission gate below reads it.
  wire [N_STREAMS-1:0]     acmp_talker_active_aaf_w =
                               acmp_talker_active_v[N_STREAMS-1:0];
  //! A_ACMP_LOBS + the SRP Listener-Ready level, kept for the 0x6E8
  //! forensics word only (i_tlk_lobs_v): "a listener is observed for
  //! talker j", composed from the manual socket and the reservation.
  wire [ACMP_SRC_C-1:0] acmp_lobs_v_w;
  generate
    for (genvar gj = 0; gj < ACMP_SRC_C; gj++) begin : g_acmp_lobs
      if (gj == 0) begin : g_lobs0
        assign acmp_lobs_v_w[gj] = listener_observed_w;
      end else begin : g_lobsn
        assign acmp_lobs_v_w[gj] = cfg_acmp_lobs |
                                   (cfg_lwsrp_enable & lwsrp_stream_gate[gj]);
      end
    end
  endgenerate

  //! CRF talker identity follows the ACMP answer when the CSR fields are
  //! left at 0: a controller that probe-binds tuid = N_STREAMS is told
  //! {station MAC, N_STREAMS} / MAAP base+N_STREAMS, and the CRF PDUs the
  //! fabric emits then carry exactly that - firmware does not have to
  //! recompute the pair and no mismatch is possible. A non-zero CRFT_SID /
  //! CRFT_DMAC still wins outright (today's static provisioning, exact).
  wire [47:0] crft_auto_dmac_w = eff_aaf_dmac + 48'(CRF_TUID_C);
  //! ...and this IS the law the protocol processor is handed for every
  //! source (pp_src_sid_w): {station MAC, talker_unique_id}. Stated once.
  wire [63:0] crft_auto_sid_w  = {station_mac_be_w, 16'(CRF_TUID_C)};
  wire [47:0] eff_crft_dmac_w = (|cfg_crft_dmac || (ACMP_SRC_C == N_STREAMS))
                                ? cfg_crft_dmac : crft_auto_dmac_w;
  wire [63:0] eff_crft_sid_w  = (|cfg_crft_sid  || (ACMP_SRC_C == N_STREAMS))
                                ? cfg_crft_sid  : crft_auto_sid_w;
  //! AAF admission, UNCHANGED IN SHAPE, repointed in source: the talker is
  //! live only while the processor declares it (acmp_talker_active is the
  //! processor's acmp_declaring_o, which is itself only reachable through an
  //! ALLOC_DA success) and, when a reservation is required, only while the
  //! processor's SRP admission has granted this stream (FR-SRP-03: no
  //! reservation -> no stream tx). The bypass bit stays the legacy
  //! stream-whenever-enabled escape hatch.
  wire aaf_gate = cfg_aaf_enable & (~cfg_maap_enable | maap_addr_valid) &
                  (cfg_aaf_bypass |
                  (acmp_talker_active &
                   (~cfg_lwsrp_enable | lwsrp_stream_gate[0])));

  // ==========================================================================
  //  CLOCK VALIDITY - the AVTP "tu" verdict for every talker.
  //  Milan v1.2 5.3.7.3 forbids stopping a Stream Output, so this is NOT a
  //  stream gate: the standard's lever for "my clock may be wrong" is the tu
  //  bit (Milan 4.3.5.2 -> IEEE 1722-2016 4.4.4.7, Annex B.1.1). Reset state
  //  is tu = 1 (no valid active-owner claim): unknown clock == not valid.
  //  docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md
  // ==========================================================================
  //! public: the milan_dp bench reads the verdict directly (Verilator
  //! folds the wire into its readers once the counter-edge terms use it)
  wire        clkv_tu_w /* verilator public_flat_rd */;
  //! IEEE 802.1AS-2020 10.2.5.1 asCapable is sourced beside tu from the
  //! selected owner. The option-off shape has no owner; the default fabric
  //! owner supplies both claims from its committed bank.
  wire        clkv_as_cap_w;
  wire [31:0] clkv_stat_w, clkv_tucnt_w;
  KL_ptp_clock_validity #(
    .QTICK_CYC_P   (CLKV_QTICK_CYC_P),
    .FABRIC_GPTP_P (GPTP_PLANE_EN_P)
  ) ptp_clock_validity (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    //! A settime / adjtime IS a gPTP time discontinuity (4.4.4.7). In the
    //! default shape adjtime comes from the engine, not CLKV software.
    .phc_load_p_i (cfg_ptp_cmd_load),
    .phc_adj_p_i  ((GPTP_PLANE_EN_P != 1'b0)
                   ? gptp_step_we_w : cfg_ptp_cmd_adjust),
    .gm_id_i      (cfg_adp_gptp_gm),
    .fabric_sync_ok_i (gptp_pub_flags_w[3]),
    .fabric_as_cap_i  (gptp_pub_flags_w[2]),
    .fabric_disc_p_i  (gptp_pub_disc_w),
    .ts_uncertain_o (clkv_tu_w),
    .as_capable_o   (clkv_as_cap_w),
    .stat_o         (clkv_stat_w),
    .tu_ivals_o     (clkv_tucnt_w)
  );

  //! ---- per-stream talker admission (P12 follow-up: t>0 arming) ----------
  //! [0] = aaf_gate above, bit-identical (the N=1 axiom). t>0 mirrors the
  //! t0 composition TERM BY TERM:
  //!   * enable        : cfg_aaf_enable (AAF_CTRL[0]) - the SAME flat bit
  //!                     t0's aaf_gate uses, and NOTHING per-context.
  //!                     Until 2026-07-30 there was a per-context ENABLE
  //!                     (TCTX w0 CTRL[0] shadow, RESET 0) that no board
  //!                     software writes, so on the shape-static builds
  //!                     (VERSION >= 0x0015: stream counts are read-only
  //!                     from elaboration) NO talker above 0 could ever
  //!                     egress - bound, SRP-granted and clock-valid made
  //!                     no difference. Measured on m001g: the soak's
  //!                     t0.s0 leg fully green while t1/t2/t3 all sat at
  //!                     tx-interval 0 despite CONNECT SUCCESS. The 0x001E
  //!                     round had already dropped that term from the SRP
  //!                     -declaration want for exactly this reason; the
  //!                     egress AND kept it, and that kept the matrix dark
  //!                     above stream 0.
  //!                     IT IS GONE RATHER THAN INVERTED, because a
  //!                     per-stream software enable is not ours to have:
  //!                     1722.1-2021 Table 8-4 bit 12 makes STREAMING_WAIT
  //!                     an OPTION, Milan v1.2 5.4.2.19/5.4.2.20 require
  //!                     NOT_SUPPORTED for START_/STOP_STREAMING on a
  //!                     Stream Output, 5.3.7.3 "excludes the possibility
  //!                     for a Stream Output to be stopped", and 5.5.4.1
  //!                     says a Talker "shall always stream AVTP packets as
  //!                     long as bandwidth is reserved for its stream". A
  //!                     disarm lever could only ever park a stream in the
  //!                     state the specification excludes (its Talker
  //!                     Advertise stays up while egress stops), so the
  //!                     honest fix is no lever at all: a context the shape
  //!                     elaborated streams when SRP licenses it, exactly
  //!                     like t0 under AAF_CTRL[0]. TCTX w0 stays writable
  //!                     for chans/vid; its bit 0 is simply not consulted.
  //!   * MAAP term     : ENGINE-WIDE, same expression as t0: ONE KL_maap
  //!                     instance claims ONE BLOCK of N_STREAMS addresses;
  //!                     stream j uses base+j (probe answers, the SRP row
  //!                     and now the packetizer all derive that same rule).
  //!   * ACMP term     : per-stream talker-active state from the processor's
  //!                     class-D face, with t0's cfg_aaf_bypass escape hatch
  //!                     mirrored.
  //!   * SRP term      : the processor's per-stream bandwidth gate, REQUIRED.
  //!                     Allowing an engine-off escape would make every talker
  //!                     admissible out of reset on a bare PROBE_TX with no
  //!                     reservation and therefore no CBS pacing. It could
  //!                     transmit about 56 k frames/s without reservation,
  //!                     which can overwhelm the peer softcore. The historical
  //!                     mitigation used to be "never arm a t>0 context
  //!                     with the engine off" and is unenforceable once
  //!                     arming is implicit. Requiring the gate is strictly
  //!                     narrowing and costs no conformance: 5.3.7.3's
  //!                     licence has no "unless SRP is off" branch, and it
  //!                     keeps the board safety rail meaningful (engine off
  //!                     => t>0 dark, so an armed-with-engine-off state
  //!                     cannot exist).
  //! An output mapping transaction reserves every referenced AAF stream
  //! after its successful phase-1 recheck. Raw 0-to-1 admission changes are
  //! held until the complete map transaction finishes, so ACMP, SRP and the
  //! local bypass cannot make a target stream live between validation and a
  //! later phase-5 write. A stream already live is rejected before reserve.
  logic [N_STREAMS-1:0] amap_edit_out_resv_r /* verilator public_flat_rd */;
  wire [N_STREAMS-1:0] aaf_stream_en_raw_w /* verilator public_flat_rd */;
  wire [N_STREAMS-1:0] aaf_stream_en_w /* verilator public_flat_rd */;
  assign aaf_stream_en_raw_w[0] = aaf_gate;
  assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;
  generate
    for (genvar gs = 1; gs < N_STREAMS; gs++) begin : g_aaf_stream_en
      assign aaf_stream_en_raw_w[gs] =
          cfg_aaf_enable &
          (~cfg_maap_enable | maap_addr_valid) &
          (cfg_aaf_bypass |
           (acmp_talker_active_aaf_w[gs] & lwsrp_stream_gate[gs]));
    end
  endgenerate
  wire [63:0]              ptp_now_w;
  wire [31:0]              aaf_frames_w, aaf_pairs_w;
  wire [TDATA_WIDTH-1:0]   aaf_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] aaf_tx_tkeep;
  wire                     aaf_tx_tvalid, aaf_tx_tlast, aaf_tx_tready;
  //! merged low-rate control stream (ADP advertise + AECP response)

  wire        cfg_sw_link, cfg_mac_reinit;
  wire        cfg_lpf_enable;
  wire        cfg_crf_en;
  wire [63:0] cfg_crf_sid;
  //! gh #64 J4 selected PathTrace: the published tail GET_AS_PATH serves
  //! behind the grandmaster. The notification edge is
  //! derived below from the complete LIVE served sequence, not a raw CSR
  //! generation. Product fabric mode preserves the donor's raw distinction:
  //! count zero is an absent PathTrace and count one is `[GM]`. The
  //! option-off shape has no path owner. Every owner aliases to empty while no
  //! grandmaster exists.
  //! Slot count DERIVED from the port width (one source, as the CSR does).
  wire [7*64-1:0] asp_path_w /* verilator public_flat_rd */;
  wire [3:0]      asp_count_w /* verilator public_flat_rd */;
  wire [3:0]      asp_gen_w   /* verilator public_flat_rd */;
  localparam int unsigned ASP_SLOTS_C = $bits(asp_path_w) / 64;
  //! milan_csr owner-selects o_asp_*: the engine's complete committed
  //! PathTrace in product mode and structural zero in option-off mode.
  //! Fabric count zero means empty even with a separately known GM.
  //! The conditional head below is the exact entry-zero value GET_AS_PATH
  //! serves and the Table 5.22 comparator observes.
  wire [3:0] asp_owner_count_w = GPTP_PLANE_EN_P ? asp_count_w : 4'd0;
  wire [3:0] asp_live_count_w = !(|cfg_adp_gptp_gm) ? 4'd0
      : asp_owner_count_w;
  wire [7*64-1:0] asp_live_path_w = !(|cfg_adp_gptp_gm) ? '0
      : asp_path_w;
  wire [63:0] asp_live_gm_w = (|asp_live_count_w) ? cfg_adp_gptp_gm
      : 64'd0;
  wire [63:0] pcm_lpf_tdata;
  wire        pcm_lpf_tvalid;
  wire        pcm_lpf_active;
  //! effective PHY link: the SoC's i_link_up (constant 1 on boards without
  //! HW tracking) gated by firmware's LINK_CTRL[0] qualification - drives the
  //! AVB_INTERFACE LinkUp/LinkDown counters and the ADP link behavior
  wire        eff_link_w;
  wire        cfg_tcam_default_pass, cfg_tcam_addr_filt_en, cfg_tcam_wr_en, cfg_tcam_wr_valid;
  wire [4:0]  cfg_tcam_wr_index;
  wire [47:0] cfg_tcam_wr_key, cfg_tcam_wr_mask;
  wire [7:0]  cfg_tcam_wr_action;

  // ---- MAC config outputs (driven by milan_csr) ----
  assign o_mac_tx_en    = cfg_mac_tx_en;
  assign o_mac_rx_en    = cfg_mac_rx_en;
  assign o_mac_promisc  = cfg_mac_promisc;
  assign o_mac_allmulti = cfg_mac_allmulti;
  assign o_mac_is_1g    = cfg_mac_is_1g;
  assign o_mac_ifg      = cfg_mac_ifg;
  assign o_mac_addr     = cfg_mac_addr;
  assign o_mc_hash      = cfg_mc_hash;
  assign o_phy_reset_n  = cfg_phy_reset_n;
  //! csr_irq: declared ahead of the o_irq_csr assign, its first reader (#193)
  wire   csr_irq;
  assign o_irq_csr      = csr_irq;

  //! Synchronise the MAC speed[] indication (i_mac_speed, gtx_clk-domain) into
  //! axis_clk before it is used by the CSR readback and link-change detector.
  (* ASYNC_REG = "TRUE" *) reg [1:0] speed_meta, speed_sync;
  always_ff @(posedge axis_clk) begin : mac_speed_cdc
    if (!axis_resetn) begin
      speed_meta <= 2'b10; speed_sync <= 2'b10;
    end else begin
      speed_meta <= i_mac_speed;
      speed_sync <= speed_meta;
    end
  end

  //! Link-status change detector (for IRQ / stats), on the synchronised speed.
  reg  [1:0] speed_q;
  reg        evt_link_change;
  always_ff @(posedge axis_clk) begin : link_change_detect
    if (!axis_resetn) begin
      speed_q <= 2'b10; evt_link_change <= 1'b0;
    end else begin
      speed_q <= speed_sync;
      evt_link_change <= (speed_q != speed_sync);
    end
  end

  // ==========================================================================
  //  Memory-mapped control plane
  // ==========================================================================
  //! P11 window -> lwSRP attribute-context provisioning port (the one
  //! context engine that exists in the datapath today)
  wire        srp_ctx_gnt_w;
  wire [63:0] srp_ctx_rd_sid_w;
  wire [15:0] srp_ctx_rd_stat_w;

  // ---- P12: CSR 0x800 window <-> engine wiring (NXN §1.5) ----
  //! LCTX = KL_avtp_rx_monitor_ctx window port, TCTX = KL_aaf_packetizer
  //! window port, ACMP tbl = KL_acmp_lstn_ctx tbl_* through the wrapper.
  //! SNAP grant is immediate: the engines serve each burst word only when
  //! fully event-drained (their window arbitration), so every WORD of the
  //! snap block is event-atomic; burst-level freeze is not implemented by
  //! the engines — the latched block is bounded by the engine state at
  //! burst start/end (documented coherence level, [M-5.4.2.25] served by
  //! per-word atomicity + the monotonic counter rule).
  wire        csr_lctx_rd_en_w;
  wire [7:0]  csr_lctx_rd_addr_w;
  wire [31:0] lctx_rd_data_w;
  wire        lctx_rd_valid_w;
  wire        csr_lctx_snap_req_w;
  wire        csr_lctx_wr_p_w;
  wire [7:0]  csr_lctx_wr_addr_w;
  wire [31:0] csr_lctx_wr_data_w;
  //! LCTX CTRL keeps its historical route[2:1] shape, but route bit 0
  //! (CSR bit 1) named a retired secondary media sink. Store and fan out zero
  //! for that reserved position so write/readback cannot advertise a path
  //! the fabric no longer implements.
  wire [31:0] lctx_wr_data_sane_w = (csr_lctx_wr_addr_w[4:0] == 5'd4)
                                      ? (csr_lctx_wr_data_w & ~32'h0000_0002)
                                      : csr_lctx_wr_data_w;
  wire        lctx_wr_rdy_w;
  wire        csr_tctx_rd_en_w;
  wire [6:0]  csr_tctx_rd_addr_w;
  wire [31:0] tctx_rd_data_w;
  wire        tctx_rd_valid_w;
  wire        csr_tctx_snap_req_w;
  wire        csr_tctx_wr_p_w;
  wire [6:0]  csr_tctx_wr_addr_w;
  wire [31:0] csr_tctx_wr_data_w;
  wire        tctx_wr_rdy_w;
  wire        acmp_tbl_gnt_w;
  //! The 0x800 window's ACMP context record. There is no context table in
  //! this fabric any more (the processor keeps its bind state internally and
  //! publishes only the bound record), so the window's grant never asserts
  //! and this reads a STRUCTURAL ZERO. The width is the CSR window's own
  //! literal-offset map, which is what it always consumed.
  localparam int ACMP_LSTN_CTX_W_C = 338;
  wire [ACMP_LSTN_CTX_W_C-1:0] acmp_tbl_ctx_w;
  //! E1 bind-restore master (0x7A0 group) -> ACMP listener ctx injection
  wire        acmp_rest_ack_w;
  wire [1:0]  acmp_rest_status_w;
  //! Persistence-journal ingest (E3) is DELETED with KL_persist_journal. The
  //! 0x7B8-0x7C4 CSR strobes still exist as a write port - milan_csr owns
  //! them - but nothing consumes them and JNL_STAT/JNL_SEQ read STRUCTURAL
  //! ZEROS: this build restores no saved binding, ever.
  wire [31:0] jnl_stat_w, jnl_seq_w;
  //! E4 AEM dynamic-state patch port (0x7C8-0x7D4). No current engine
  //! consumes its CSR strobes, and its status is tied to structural zero.
  wire [31:0] aemp_stat_w;

  //! item-11 AAF per-stage latency taps (LTAP CSR group, base 0x870):
  //! 16 packed RO words + status feed milan_csr; en/clr come back from it.
  wire [16*32-1:0] ltap_regs_w;
  wire [31:0]      ltap_status_w;
  wire             ltap_en_w, ltap_clr_w;

  //! RX stream-parser probe (APRB CSR group, base 0x8B4): the pre-match view
  //! of the listener path - 5 packed RO words, see the probe block below.
  wire [5*32-1:0]  aprb_regs_w;
  wire [31:0]      aprb_parsed_w, aprb_matched_w;

  //! ------------------------------------------------------------------------
  //! SATURATING narrow views of the 32-bit STREAM_INPUT counters.
  //!
  //! AVTPRX_STAT (0x6B8) and AVTPRX_ERR (0x6C0) pack several 32-bit counters
  //! into one word, so they can only ever show the low byte / half-word. Until
  //! now that was a plain TRUNCATION, i.e. a silent modulo: silicon 2026-07-26
  //! read SEQ_NUM_MISMATCH = 51,523 on a board up 81 h - 79 % of the way to
  //! the 16-bit roll, after which the field would have counted DOWN from zero
  //! and looked healthier the worse the link got. Saturating instead makes the
  //! narrow view an honest FLOOR: all-ones means ">= that many, read the full
  //! 32-bit counter", which lives at the per-stream window A_STRMW_CNT
  //! (0x830 + 4*k, SEQ_NUM_MISMATCH at 0x83C). Values below the ceiling are
  //! bit-identical to the old behaviour, so no reader regresses.
  //! ------------------------------------------------------------------------
  function automatic logic [15:0] sat16_f(input logic [31:0] c);
    sat16_f = (c > 32'h0000_FFFF) ? 16'hFFFF : c[15:0];
  endfunction
  function automatic logic [7:0] sat8_f(input logic [31:0] c);
    sat8_f = (c > 32'h0000_00FF) ? 8'hFF : c[7:0];
  endfunction

  //! ---- protocol-processor shadow plane nets (PP_PLANE_P; see below) ----
  logic        pp_enable_w, pp_restore_go_w;
  logic        pp_req_w, pp_we_w;
  logic [19:0] pp_addr_w;
  logic [31:0] pp_wdata_w, pp_rdata_w;
  logic        pp_ack_w, pp_err_w;
  logic        pp_restore_busy_w, pp_restore_done_w, pp_restore_fail_w;
  //! the two levels that keep the saved-state verdict honest: a walk that
  //! validated nothing, and whether any persistent media exists at all
  logic        pp_restore_blank_w, pp_nvm_backed_w;
  logic        pp_nvm_alarm_w;
  logic [15:0] pp_rx_frames_w, pp_tx_frames_w;
  logic [7:0]  pp_rx_drops_w;
  //! the processor's packed control-lane egress; unconsumed while draining
  //! the control lane's backpressure into the processor's packed TX
  wire                      pp_tx_tready_w;
  //! per-source stream_id handed to the processor: the fabric's {station MAC,
  //! talker_unique_id} law, the SAME 64 bits KL_aaf_packetizer stamps on the
  //! wire, with the CRF Media Clock Output's CSR override applied where the
  //! CRF engine applies it (eff_crft_sid_w) so the answer and the stream can
  //! never disagree. Derive, never mirror.
  wire [ACMP_SRC_C*64-1:0]  pp_src_sid_w;
  //! 1722.1-2021 6.2.6 GM_CHANGE: an edge on the committed grandmaster pair
  //! (id OR domain - both are ADPDU fields a re-advertise has to carry) and,
  //! separately, an edge on the grandmaster IDENTITY alone. The two are not
  //! the same fact and the consumers below do not want the same one.
  logic [63:0]              pp_gm_id_q_r;
  logic [7:0]               pp_gm_dom_q_r;
  logic                     pp_gm_change_p_w /* verilator public_flat_rd */;
  logic                     pp_gm_id_change_p_w /* verilator public_flat_rd */;
  logic [TDATA_WIDTH-1:0]   pp_tx_tdata_w;
  logic [TDATA_WIDTH/8-1:0] pp_tx_tkeep_w;
  logic                     pp_tx_tvalid_w, pp_tx_tlast_w;

  //! ---- the control plane's CLASS-D FABRIC FACE (02 §6, F02.10) ----
  //! Landed as datapath nets rather than as new module ports: the consumers -
  //! the AAF talker gate, the CBS slope MUX, the RX stream filter, the ACMP
  //! bind record every listener path reads - all live INSIDE this file, so
  //! publishing them at the LiteX boundary would be a detour through the SoC
  //! for signals that never leave. Marked public_flat_rd (the media_tick_p /
  //! aaf_stream_en_w precedent in this file) so the pp_shadow harness can
  //! grade them without a CSR window.
  //!
  //! Flat packing, index s at [W*s +: W] — the processor's own convention,
  //! carried through unchanged. WIDTHS ARE THE ENTITY'S DESCRIPTOR COUNTS
  //! (ACMP_SRC_C / ACMP_SINKS_C), not the AAF stream count: a STREAM_OUTPUT
  //! the entity advertises must have a source context that can answer for it.
  wire [2:0]                 pp_cd_srp_class_a_prio_w;
  wire [11:0]                pp_cd_srp_class_a_vid_w;
  wire                       pp_cd_srp_domain_adopted_w;
  wire                       pp_cd_srp_domain_change_w;
  wire [ACMP_SRC_C*2-1:0]    pp_cd_srp_tk_decl_state_w;
  wire [ACMP_SRC_C*2-1:0]    pp_cd_srp_lstn_reg_state_w;
  wire [ACMP_SRC_C-1:0]      pp_cd_srp_active_w;
  wire [ACMP_SRC_C-1:0]      pp_cd_srp_sr_admitted_w;
  wire [ACMP_SRC_C*32-1:0]   pp_cd_srp_granted_slope_bps_w;
  wire [ACMP_SRC_C*8-1:0]    pp_cd_srp_src_fail_code_w;
  wire [ACMP_SRC_C*64-1:0]   pp_cd_srp_src_fail_bridge_w;
  wire [31:0]                pp_cd_srp_sum_slope_bps_w;
  wire                       pp_cd_srp_over_limit_w;
  wire [ACMP_SINKS_C*2-1:0]  pp_cd_srp_tk_reg_state_w;
  wire [ACMP_SINKS_C*2-1:0]  pp_cd_srp_lstn_decl_state_w;
  wire [ACMP_SINKS_C*32-1:0] pp_cd_srp_acc_latency_w;
  wire [ACMP_SINKS_C*8-1:0]  pp_cd_srp_snk_fail_code_w;
  wire [ACMP_SRC_C-1:0]      pp_cd_acmp_declaring_w /* verilator public_flat_rd */;
  wire [ACMP_SINKS_C-1:0]    pp_cd_acmp_bound_w     /* verilator public_flat_rd */;
  wire [ACMP_SINKS_C*64-1:0] pp_cd_acmp_bound_eid_w;
  wire [ACMP_SINKS_C*64-1:0] pp_cd_acmp_bound_sid_w;
  wire [ACMP_SINKS_C*48-1:0] pp_cd_acmp_bound_dmac_w;
  //! (pp_cd_acmp_bound_vlan_w is declared above acmpl_vlan_w, its first
  //! reader, #193)
  wire [31:0]                pp_cd_adp_avail_index_w /* verilator public_flat_rd */;

  //! ---- the shadow plane's maap request face, and the shim's answers ----
  //! PP_SRC_IDX_W_C clamps exactly as protocol_processor_top and
  //! KL_acmp_talker clamp their own: the shipping board elaborates at
  //! N_STREAMS = 1 and an unclamped $clog2(1) declares [-1:0].
  localparam int PP_SRC_IDX_W_C = (N_STREAMS > 1) ? $clog2(N_STREAMS) : 1;
  wire                       pp_maap_req_valid_w   /* verilator public_flat_rd */;
  wire                       pp_maap_req_ready_w   /* verilator public_flat_rd */;
  //! observed by tb/verilator/pp_shadow: this shape pins every talker source
  //! enabled, so the processor's RELEASE_DA arc is unreachable here and the
  //! suite grades that as a fact rather than leaving it an untested gap.
  wire                       pp_maap_req_release_w /* verilator public_flat_rd */;
  wire [PP_SRC_IDX_W_C-1:0]  pp_maap_req_src_w;
  wire                       pp_maap_rsp_valid_w   /* verilator public_flat_rd */;
  wire                       pp_maap_rsp_ok_w      /* verilator public_flat_rd */;
  wire [47:0]                pp_maap_rsp_da_w      /* verilator public_flat_rd */;
  wire                       pp_maap_confl_valid_w;
  wire [PP_SRC_IDX_W_C-1:0]  pp_maap_confl_src_w;
  wire                       pp_maap_confl_ack_w;
  //! the processor's INTERNAL Annex B claim - all-zero while
  //! cfg_maap_internal_i is tied 0 below (_nc: no consumer until the
  //! KL_maap-retirement round)
  wire [47:0]                pp_maap_int_addr_nc_w;
  wire                       pp_maap_int_valid_nc_w;
  wire [1:0]                 pp_maap_int_state_nc_w;
  wire [7:0]                 pp_maap_int_confl_nc_w;
  wire [7:0]                 pp_maap_int_dfnd_nc_w;

  //! ------------------------------------------------------------------------
  //! CSR OUTPUTS LEFT DELIBERATELY OPEN. A group of config words below has no
  //! consumer any more because the plane that consumed it is deleted: the ADP
  //! advertiser's timing/identity extras (valid_time, entity_capabilities,
  //! controller_capabilities, association_id, interface_index, the
  //! advertise/depart strobes), the AEM patch port (0x7C8), the AS_PATH
  //! staging group (0x7DC), the lwSRP provisioning words the applicant read
  //! (DMAC, MaxFrameSize, MaxIntervalFrames, the declare-bypass bit), the
  //! 0x7A0 ACMP bind-restore master, and the 0x800 window's ACMP table and
  //! SRP attribute-row ports.
  //!
  //! They are OPEN rather than bound to a net, so a reader sees AT THE
  //! CONNECTION that nothing consumes them - a named net going nowhere is
  //! exactly the "dead RTL that looks alive" shape. Ordinary retained staging
  //! words still read back what firmware wrote, but owner-selected gPTP
  //! publications are the deliberate exception: AS_PATH and its peers read
  //! fabric state in the product shape and structural zero in option-off.
  //! Writing an open staging word never changes anything on the wire.
  //!
  //! FIVE ADPDU FIELDS ARE NOW BEYOND SOFTWARE'S REACH, and that is a real
  //! loss rather than a tidy-up: entity_capabilities, valid_time,
  //! association_id, controller_capabilities and interface_index are
  //! CONSTANTS inside the protocol processor's KL_adp_engine, which exposes
  //! no port for them. The 0x600 words are accepted and ignored; the ADPDU
  //! carries the processor's values. Closing that needs a port on the
  //! submodule, which is pinned.
  milan_csr #(
    //! the retained 0x400 window geometry and CAP.num_queues: the package
    //! constant, not a wrapper parameter, since no queue is elaborated here
    .NUM_QUEUES(NUMBER_OF_QUEUES),
    .ADDR_WIDTH(16),
    .N_LISTENERS_P(N_STREAMS),
    .N_TALKERS_P(N_STREAMS),
    .SRP_LSN0_ROW_P(SRP_LSN0_ROW_C),
    .GPTP_PLANE_EN_P(GPTP_PLANE_EN_P),
    //! PHC scale truth (t532 wire-scale audit): the PTP_INCR reset value is
    //! derived from THIS clock declaration, so a free-run PHC ticks true ns
    //! on every shape without waiting for software
    .MILAN_CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ),
    //! both chmap map-RAM read ports are wired below, and the CAPTURE side
    //! carries the {loop_fed, loop_mapped} mask. Published at CHMAP_SNAP[9:8]
    //! so software reads UNSUPPORTED rather than a structural zero on a build
    //! that does not wire them (the parameter's default is 0 for that reason).
    .CHMAP_RDBK_P(3)
    //! No ADP shape parameters: milan_csr `include-s the SAME generated
    //! gen/adp_shape_defaults.svh this module does, so the config is the
    //! one definition and nothing threads a second copy through a port map.
  ) csr (
    .aclk    (axis_clk),
    .aresetn (axis_resetn),
    .s_axi_awaddr (s_axi_awaddr),
    .s_axi_awvalid(s_axi_awvalid),
    .s_axi_awready(s_axi_awready),
    .s_axi_wdata  (s_axi_wdata),
    .s_axi_wstrb  (s_axi_wstrb),
    .s_axi_wvalid (s_axi_wvalid),
    .s_axi_wready (s_axi_wready),
    .s_axi_bresp  (s_axi_bresp),
    .s_axi_bvalid (s_axi_bvalid),
    .s_axi_bready (s_axi_bready),
    .s_axi_araddr (s_axi_araddr),
    .s_axi_arvalid(s_axi_arvalid),
    .s_axi_arready(s_axi_arready),
    .s_axi_rdata  (s_axi_rdata),
    .s_axi_rresp  (s_axi_rresp),
    .s_axi_rvalid (s_axi_rvalid),
    .s_axi_rready (s_axi_rready),
    // MAC control/status
    .o_mac_tx_en   (cfg_mac_tx_en),
    .o_mac_rx_en   (cfg_mac_rx_en),
    .o_mac_promisc (cfg_mac_promisc),
    .o_mac_allmulti(cfg_mac_allmulti),
    .o_mac_is_1g   (cfg_mac_is_1g),
    .o_mac_ifg     (cfg_mac_ifg),
    .o_mac_addr    (cfg_mac_addr),
    .o_mc_hash     (cfg_mc_hash),
    .o_phy_reset_n (cfg_phy_reset_n),
    .i_link_up     (i_link_up),
    .i_speed       (speed_sync),
    .i_full_duplex (i_full_duplex),
    // statistics
    .o_stats_snapshot(cfg_stats_snapshot),
    .o_stats_reset   (cfg_stats_reset),
    .i_stats         (stats_counts),
    .i_stats_cap     ({{(32-_ETH_EVENT_COUNTER){1'b0}}, stats_cap_w}),
    // PTP
    .o_ptp_enable      (cfg_ptp_enable),
    .o_ptp_incr        (cfg_ptp_incr),
    .o_ptp_adj         (cfg_ptp_adj),
    .o_ptp_tod_wr      (cfg_ptp_tod_wr),
    .o_ptp_offset      (cfg_ptp_offset),
    .i_clkv_stat       (clkv_stat_w),
    .i_clkv_tucnt      (clkv_tucnt_w),
    .o_ptp_cmd_load    (cfg_ptp_cmd_load),
    .o_ptp_cmd_adjust  (cfg_ptp_cmd_adjust),
    .o_ptp_cmd_snapshot(cfg_ptp_cmd_snapshot),
    .i_ptp_tod         (ptp_tod_rd),
    .i_ptp_tod_valid   (ptp_tod_rd_valid),
    // ADP advertiser identity/control (0x600 group, FR-DISC-*)
    .o_adp_enable         (cfg_adp_enable),
    .o_adp_valid_time     (),
    .o_adp_entity_id      (cfg_adp_entity_id),
    .o_adp_entity_model_id(cfg_adp_entity_model_id),
    .o_adp_entity_caps    (),
    .o_adp_talker_sources (cfg_adp_talker_sources),
    .o_adp_talker_caps    (cfg_adp_talker_caps),
    .o_adp_listener_sinks (cfg_adp_listener_sinks),
    .o_adp_listener_caps  (cfg_adp_listener_caps),
    .o_adp_controller_caps(),
    .i_gptp_gm_id         (gptp_pub_gm_w),
    .i_gptp_parent_id     (gptp_pub_parent_w),
    .i_gptp_pdelay_ns     (gptp_pub_pdelay_w),
    .i_gptp_asp_path      (gptp_pub_path_w),
    .i_gptp_asp_count     (gptp_pub_path_count_w),
    .i_gptp_asp_gen       (gptp_pub_path_gen_w),
    .i_gptp_tap_drop      (gptp_tap_drop_w),
    .i_gptp_rx_drop       (gptp_rx_drop_w),
    .i_gptp_ev_drop       (gptp_ev_drop_w),
    .o_adp_gptp_domain    (cfg_adp_gptp_domain),
    .o_adp_current_config (cfg_adp_current_config),
    .o_adp_identify_index (cfg_adp_identify_index),
    .o_adp_interface_index(),
    .o_adp_association_id (),
    .o_adp_advertise_p    (),
    .o_adp_depart_p       (),
    .i_adp_available_index(adp_available_index),
    .i_adp_depart_cnt     (adp_depart_cnt),
    .i_adp_rearm_cnt      (adp_rearm_cnt),
    .i_adp_depart_src     (adp_depart_src),
    .i_adp_sent_cnt       (adp_sent_cnt),
    .i_adp_disc_rx_cnt    (adp_disc_rx_cnt),
    .i_adp_disc_seen_p    (adp_disc_seen_p),
    .i_adp_last_msg       (adp_last_msg),
    .i_adp_state          (adp_state),
    .i_aecp_locked        (aecp_locked),
    .i_aecp_current_config(aecp_current_config),
    .i_aecp_cmd_count     (aecp_cmd_count),
    .i_aecp_resp_count    (aecp_resp_count),
    .i_acmp_cmd_count     (acmp_cmd_count),
    .i_acmp_resp_count    (acmp_resp_count),
    .o_aaf_enable         (cfg_aaf_enable),
    .o_aaf_bypass         (cfg_aaf_bypass),
    .o_acmp_lobs          (cfg_acmp_lobs),
    .i_acmp_probe_armed   (acmp_probe_armed),
    .i_acmp_talker_active (acmp_talker_active),
    //! per-stream talker truth vectors (window honesty, 2026-07-26)
    .i_tlk_gate_v         (8'(aaf_stream_en_w)),
    //! the 8-bit CSR view is the AUDIO sources only; the CRF context at
    //! tuid = N_STREAMS would not fit the field at N = 8 (g_acmp_crf_src)
    .i_tlk_active_v       (8'(acmp_talker_active_aaf_w)),
    .i_tlk_probe_v        (8'(acmp_probe_armed_v[N_STREAMS-1:0])),
    .i_tlk_lobs_v         (8'(acmp_lobs_v_w[N_STREAMS-1:0])),
    .i_aaf_gate           (aaf_gate),
    .o_aaf_dest_mac       (cfg_aaf_dmac),
    .o_aaf_vid            (cfg_aaf_vid),
    .i_aaf_frames         (aaf_frames_w),
    .i_aaf_pairs          (aaf_pairs_w),
    // lwSRP engine (0x680 group)
    .o_lwsrp_enable       (cfg_lwsrp_enable),
    .o_lwsrp_talker_en    (cfg_lwsrp_talker_en),
    .o_lwsrp_decl_bypass  (),
    .o_lwsrp_vid          (cfg_lwsrp_vid),
    .o_lwsrp_dest_mac     (),
    .o_lwsrp_max_frame    (),
    .o_lwsrp_interval     (),
    .o_lwsrp_latency      (cfg_lwsrp_latency),
    //! [11] = ctx-table shortfall (sticky): a provisioning request named an
    //! attribute row this build does not have. It is 0 on a correctly-sized
    //! engine and the ONLY software-visible symptom when it is not - a
    //! refused row silently drops the reservation everywhere else.
    .i_lwsrp_status       ({lwsrp_rx_drops, lwsrp_tfail_code, 4'd0,
                            lwsrp_ctx_oor_w,
                            lwsrp_tfail_valid, lwsrp_slope_en,
                            lwsrp_stream_gate[0], lwsrp_over_limit,
                            lwsrp_res_active, lwsrp_domain_ok,
                            lwsrp_talker_declared, lwsrp_listener_ready,
                            lwsrp_listener_reg, lwsrp_listener_decl}),
    .i_lwsrp_slope        (lwsrp_idle_slope),
    .i_lwsrp_cnt          ({lwsrp_rx_pdus, lwsrp_tx_count}),
    //! LWSRP_DOM 0x788: the Milan 4.2.7.2.1 operational Domain pair -
    //! software FOLLOWS this (never mirrors it into its own config)
    .i_lwsrp_dom          ({7'd0, lwsrp_adopt_valid, lwsrp_op_prio,
                            4'd0, lwsrp_op_vid}),
    //! ACMP listener status (0x6A4 group, RO); bit 31 = CRF sink bound.
    //! MOST OF THIS WORD IS A STRUCTURAL ZERO NOW. The processor publishes a
    //! BOUND RECORD, not a state machine, so the fields that described the
    //! ladder (state, probing, acmp_status, tk_avail, lstn_declare) and the
    //! per-sink SRP registrar levels have no source. What is still real:
    //! bit 31 (CRF sink bound), acmpl_bound and acmpl_active.
    .i_acmpl_state        ({acmpl1_bound, 3'd0, acmpl_vlan_w, acmpl_tk_avail,
                            acmpl_probing, acmpl_status,
                            lwsrp_ta_failed, lwsrp_ta_registered,
                            acmpl_lstn_declare, acmpl_active,
                            acmpl_bound, acmpl_state}),
    .i_acmpl_talker_lo    (acmpl_talker[31:0]),
    .i_acmpl_talker_hi    (acmpl_talker[63:32]),
    .i_acmpl_cnt          ({acmpl_probe_count, acmpl_cmd_count}),
    .i_acmpl_tuid         ({acmpl_tx_wedge, lwsrp_ta_fail_code, acmpl_tuid}),
    .i_acmpl_dbg          (acmpl_dbg),
    .i_avtprx_tsd         (avtprx_last_tsd),
    .i_i2spb_dbg          (i2spb_dbg_frame),
    .i_ctlr_diag          (aecp_ctlr_diag),
    .i_avtprx_stat        ({sat8_f(avtprx_intr_c), sat8_f(avtprx_unlocked_c),
                            sat8_f(avtprx_locked_c), 7'd0, avtprx_locked}),
    .i_avtprx_frx         (avtprx_frx_c),
    //! full-width Table 7-157 counters for the 0x800 window's index-0 words
    //! (the packed 0x6B8/0x6C0 views above are saturating summaries of these)
    .i_avtprx_cnt10       ({avtprx_frx_c, avtprx_early_c, avtprx_late_c,
                            avtprx_unsupp_c, avtprx_tu_c, avtprx_mreset_c,
                            avtprx_seqmm_c, avtprx_intr_c, avtprx_unlocked_c,
                            avtprx_locked_c}),
    .i_avtprx_err         ({sat16_f(avtprx_seqmm_c), sat8_f(avtprx_unsupp_c),
                            sat8_f(avtprx_tu_c)}),
    .i_pcmrx_cnt          ({pcmrx_drops, pcmrx_pdus}),
    .i_pcmrx_ts           (avtprx_last_ts),
    .i_i2spb_stat         ({i2spb_underruns, i2spb_overruns}),
    .o_i2spb_clr_under    (cfg_i2spb_clru),
    .o_i2spb_clr_over     (cfg_i2spb_clro),
    .i_i2spb_trim         ({i2spb_trim, i2spb_fill}),
    .i_maap_stat0         ({maap_conflicts, maap_defends, maap_offset}),
    .i_maap_stat1         ({29'd0, maap_addr_valid, maap_state}),
    .o_maap_enable        (cfg_maap_enable),
    .o_maap_seed_valid    (cfg_maap_seed_valid),
    .o_maap_count         (cfg_maap_count),
    .o_maap_seed_offset   (cfg_maap_seed_offset),
    .o_tone_enable        (cfg_tone_enable),
    .o_tone_att           (cfg_tone_att),
    // RX dest-MAC TCAM filter programming (0x700 group)
    .o_sw_link          (cfg_sw_link),
    .o_mac_reinit       (cfg_mac_reinit),
    .o_entity_name8     (),
    .o_lpf_enable       (cfg_lpf_enable),
    .o_crf_en           (cfg_crf_en),
    .o_crf_sid          (cfg_crf_sid),
    .i_crf_delta        (crf_delta_w),
    .i_crf_rate         (crf_rate_w),
    //! documented TRUNCATED slices of the 32-bit backing (gh #61 G1):
    //! the packed {pdu16, fmt8, seq8} ABI is byte-identical to the old
    //! narrow counters; the AECP wire serves the full width
    .i_crf_status       ({crf_pducnt_w[15:0], crf_fmterr_w[7:0],
                          crf_seqerr_w[7:0]}),
    .i_crf_locked       (crf_locked_w),
    .i_mcsrv_stat       (mcsrv_stat_w),
    .o_mcsrv_ps_invert  (mcsrv_ps_invert_w),
    .o_mcsrv_auto_repair (mcsrv_auto_repair_w),
    // item-11 AAF per-stage latency taps (LTAP group 0x870)
    .i_ltap_regs        (ltap_regs_w),
    .i_ltap_status      (ltap_status_w),
    .i_aprb_regs        (aprb_regs_w),
    .o_ltap_en          (ltap_en_w),
    .o_ltap_clr         (ltap_clr_w),
    .o_chmap_enable     (cfg_chmap_enable),
    .o_chmap_wr_en      (cfg_chmap_wr_en),
    .o_chmap_wr_side    (cfg_chmap_wr_side),
    .o_chmap_wr_addr    (cfg_chmap_wr_addr),
    .o_chmap_wr_data    (cfg_chmap_wr_data),
    .o_chmap_rd_en      (cfg_chmap_rd_en),
    .o_chmap_rd_side    (cfg_chmap_rd_side),
    .o_chmap_rd_addr    (cfg_chmap_rd_addr),
    .i_chmap_rd_data    (cfg_chmap_rd_data),
    .i_chmap_rd_valid   (cfg_chmap_rd_valid),
    .o_crft_en          (cfg_crft_en),
    //! CRFT_CTRL's manual class-A bit: the tag is now the PROCESSOR's Talker
    //! Advertise state (crft_class_a_w), never a bare CSR bit, so a tagged
    //! stream that no bridge would forward is unreachable. Left open.
    .o_crft_class_a     (),
    .o_crft_sid         (cfg_crft_sid),
    .o_crft_dest_mac    (cfg_crft_dmac),
    .i_crft_stat        (crft_stat_w),
    .i_crft_count       (crft_count_w),
    // P12 indexed window (0x800): LCTX/TCTX/ACMP-tbl wired to the live
    // engines (monitor_ctx / packetizer / acmp wrapper); snap grant is
    // immediate (see the wire-block comment); the lwSRP ctx master wires
    // to the live KL_lwsrp_top provisioning port below
    .o_lctx_rd_en       (csr_lctx_rd_en_w),
    .o_lctx_rd_addr     (csr_lctx_rd_addr_w),
    .i_lctx_rd_data     (lctx_rd_data_w),
    .i_lctx_rd_valid    (lctx_rd_valid_w),
    .o_lctx_snap_req    (csr_lctx_snap_req_w),
    .i_lctx_snap_ok     (csr_lctx_snap_req_w),
    .o_lctx_wr_p        (csr_lctx_wr_p_w),
    .o_lctx_wr_addr     (csr_lctx_wr_addr_w),
    .o_lctx_wr_data     (csr_lctx_wr_data_w),
    .i_lctx_wr_rdy      (lctx_wr_rdy_w),
    .o_tctx_rd_en       (csr_tctx_rd_en_w),
    .o_tctx_rd_addr     (csr_tctx_rd_addr_w),
    .i_tctx_rd_data     (tctx_rd_data_w),
    .i_tctx_rd_valid    (tctx_rd_valid_w),
    .o_tctx_snap_req    (csr_tctx_snap_req_w),
    .i_tctx_snap_ok     (csr_tctx_snap_req_w),
    .o_tctx_wr_p        (csr_tctx_wr_p_w),
    .o_tctx_wr_addr     (csr_tctx_wr_addr_w),
    .o_tctx_wr_data     (csr_tctx_wr_data_w),
    .i_tctx_wr_rdy      (tctx_wr_rdy_w),
    .o_acmp_tbl_req     (),
    .o_acmp_tbl_idx     (),
    .i_acmp_tbl_gnt     (acmp_tbl_gnt_w),
    .i_acmp_tbl_ctx     (acmp_tbl_ctx_w[316:0]),
    .o_acmp_rest_req    (),
    .o_acmp_rest_idx    (),
    .o_acmp_rest_talker (),
    .o_acmp_rest_tuid   (),
    .o_acmp_rest_ctlr   (),
    .o_acmp_rest_flags  (),
    //! the E1 bind-restore port has no engine behind it any more: the ACMP
    //! context table it injected into is deleted, so the ack is a STRUCTURAL
    //! ZERO and a 0x7A0 commit never completes
    .i_acmp_rest_ack    (acmp_rest_ack_w),
    .i_acmp_rest_status (acmp_rest_status_w),
    //! Persistence-journal ingest group 0x7B8-0x7C4 (E3). KL_persist_journal
    //! is deleted, so these strobes land nowhere: software may still write
    //! the group and the writes are accepted and DISCARDED, and JNL_STAT /
    //! JNL_SEQ below read structural zeros. No image is ever verified and no
    //! binding is ever restored.
    .o_jnl_start        (),
    .o_jnl_wr           (),
    .o_jnl_data         (),
    .o_jnl_end          (),
    .o_jnl_abort        (),
    .i_jnl_stat         (jnl_stat_w),
    .i_jnl_seq          (jnl_seq_w),
    //! AEM dynamic-state patch port 0x7C8-0x7D4 (E4)
    .o_aemp_wdata       (),
    .o_aemp_sel_p       (),
    .o_aemp_field_p     (),
    .o_aemp_data_p      (),
    .o_aemp_commit_p    (),
    .o_aemp_abort_p     (),
    .i_aemp_stat        (aemp_stat_w),
    .o_srp_ctx_req      (),
    .o_srp_ctx_we       (),
    .o_srp_ctx_idx      (),
    .o_srp_ctx_valid    (),
    .o_srp_ctx_dir      (),
    .o_srp_ctx_sid      (),
    .o_srp_ctx_dmac     (),
    .o_srp_ctx_prio_rank(),
    .o_srp_ctx_max_frame(),
    .o_srp_ctx_interval (),
    .o_srp_ctx_latency  (),
    //! The 0x800 window's SRP attribute-row port has no engine and no
    //! fabric requester behind it any more: no grant is ever issued and no
    //! write is ever stolen. Both read STRUCTURAL ZEROS - a write to the
    //! window is accepted by the CSR and lands nowhere.
    .i_srp_ctx_gnt      (srp_ctx_gnt_w),
    .i_srp_ctx_stolen   (1'b0),
    .i_srp_ctx_rd_sid   (srp_ctx_rd_sid_w),
    .i_srp_ctx_rd_stat  (srp_ctx_rd_stat_w),
    .i_bdbg0            (aecp_bdbg0_w),
    .i_bdbg1            (aecp_bdbg1_w),
    .i_bdbg2            (aecp_bdbg2_w),
    .i_linkg_stat       (linkg_stat_w),
    .i_txarb_diag       (txarb_diag_w),
    .i_mac_reinit       (linkg_reinit_w),
    .o_linkg_dis        (cfg_linkg_dis),
    .o_linkg_freeze     (cfg_linkg_freeze),
    .o_asp_path         (asp_path_w),
    .o_asp_count        (asp_count_w),
    .o_asp_gen          (asp_gen_w),
    .o_tcam_default_pass(cfg_tcam_default_pass),
    .o_tcam_addr_filt_en(cfg_tcam_addr_filt_en),
    .o_tcam_wr_en       (cfg_tcam_wr_en),
    .o_tcam_wr_index    (cfg_tcam_wr_index),
    .o_tcam_wr_valid    (cfg_tcam_wr_valid),
    .o_tcam_wr_key      (cfg_tcam_wr_key),
    .o_tcam_wr_mask     (cfg_tcam_wr_mask),
    .o_tcam_wr_action   (cfg_tcam_wr_action),
    // protocol-processor shadow plane (0x920 window; tied off when absent)
    .o_pp_enable        (pp_enable_w),
    .o_pp_restore_go    (pp_restore_go_w),
    .o_pp_req           (pp_req_w),
    .o_pp_we            (pp_we_w),
    .o_pp_addr          (pp_addr_w),
    .o_pp_wdata         (pp_wdata_w),
    .i_pp_rdata         (pp_rdata_w),
    .i_pp_ack           (pp_ack_w),
    .i_pp_err           (pp_err_w),
    .i_pp_restore_busy  (pp_restore_busy_w),
    .i_pp_restore_done  (pp_restore_done_w),
    .i_pp_restore_fail  (pp_restore_fail_w),
    .i_pp_nvm_backed    (pp_nvm_backed_w),
    .i_pp_nvm_blank     (pp_restore_blank_w),
    .i_pp_nvm_alarm     (pp_nvm_alarm_w),
    .i_pp_rx_frames     (pp_rx_frames_w),
    .i_pp_rx_drops      (pp_rx_drops_w),
    .i_pp_tx_frames     (pp_tx_frames_w),
    // interrupts
    .i_evt_link_change  (evt_link_change),
    .i_evt_rmon_rollover(stats_rollover),
    .o_eth_guard        (o_eth_guard),
    .o_irq              (csr_irq)
  );

  // ==========================================================================
  //  PTP hardware clock (CSR-configured)
  // ==========================================================================
  //! PHC knob ownership: the plane owns adjfine/adjtime when enabled
  //! (constant-folds to the CSR face when the option is off); settime
  //! (tod_wr/cmd_load) always stays with software -- boot sets the epoch.
  wire [31:0] eff_ptp_adj_w    = (GPTP_PLANE_EN_P != 1'b0)
                               ? unsigned'(gptp_adj_w)   : cfg_ptp_adj;
  wire [63:0] eff_ptp_offset_w = (GPTP_PLANE_EN_P != 1'b0)
                               ? gptp_step_w             : cfg_ptp_offset;
  wire        eff_ptp_adjust_w = (GPTP_PLANE_EN_P != 1'b0)
                               ? gptp_step_we_w          : cfg_ptp_cmd_adjust;

  //! The PHC is the counter and its CSR crossing, nothing else. ptp_ts_top's
  //! TX/RX record stampers, their record FIFOs and the tx_ts_ready pulse left
  //! with the general-data chain (see the TX-trunk note at the interface
  //! declarations): the TX stamper only ever saw the shaper's idle output and
  //! both directions' records drained into an always-ready sink, so
  //! IRQ_STATUS[0] and PTP_INGRESS/EGRESS_LAT had no consumer. o_ptp_now is
  //! what the AAF/CRF talkers, the latency taps and the fabric gPTP plane
  //! read; the plane stamps its own frames (KL_gptp_txstamp at the MAC
  //! boundary, its ingress tap off rx_axis_fabric).
  wire        phc_enable_ts_w;
  wire [31:0] phc_incr_ts_w, phc_adj_ts_w;
  wire [63:0] phc_tod_wr_ts_w, phc_offset_ts_w, phc_tod_snap_ts_w;
  wire        phc_load_ts_w, phc_adjust_ts_w, phc_snapshot_ts_w;
  wire        phc_tod_snap_valid_ts_w;

  //! CSR -> PHC clock-domain crossing (axis_clk -> gtx_clk + snapshot return).
  ptp_csr_sync #(
    .TS_WIDTH   (64),
    .INCR_WIDTH (32)
  ) ptp_sync (
    .aclk           (axis_clk),
    .aresetn        (axis_resetn),
    .a_enable       (cfg_ptp_enable),
    .a_incr         (cfg_ptp_incr),
    .a_adj          (eff_ptp_adj_w),
    .a_tod_wr       (cfg_ptp_tod_wr),
    .a_offset       (eff_ptp_offset_w),
    .a_cmd_load     (cfg_ptp_cmd_load),
    .a_cmd_adjust   (eff_ptp_adjust_w),
    .a_cmd_snapshot (cfg_ptp_cmd_snapshot),
    .a_tod_rd       (ptp_tod_rd),
    .a_tod_rd_valid (ptp_tod_rd_valid),

    .ts_clk         (gtx_clk),
    .ts_resetn      (gtx_resetn),
    .t_enable       (phc_enable_ts_w),
    .t_incr         (phc_incr_ts_w),
    .t_adj          (phc_adj_ts_w),
    .t_tod_wr       (phc_tod_wr_ts_w),
    .t_cmd_load     (phc_load_ts_w),
    .t_offset       (phc_offset_ts_w),
    .t_cmd_adjust   (phc_adjust_ts_w),
    .t_cmd_snapshot (phc_snapshot_ts_w),
    .t_tod_snapshot       (phc_tod_snap_ts_w),
    .t_tod_snapshot_valid (phc_tod_snap_valid_ts_w)
  );

  //! the 64-bit PHC (REQ-PTP-01/02): gtx_clk == axis_clk in every real
  //! instantiation, which is what lets ptp_now_w be read synchronously
  timestamp_counter #(
    .COUNTER_WIDTH (64),
    .INCR_WIDTH    (32),
    .FRAC_WIDTH    (24)
  ) ts_counter (
    .clk                  (gtx_clk),
    .resetn               (gtx_resetn),
    .enable_i             (phc_enable_ts_w),
    .incr_i               (phc_incr_ts_w),
    .adj_i                (phc_adj_ts_w),
    .tod_wr_i             (phc_tod_wr_ts_w),
    .cmd_load_i           (phc_load_ts_w),
    .offset_i             (phc_offset_ts_w),
    .cmd_adjust_i         (phc_adjust_ts_w),
    .cmd_snapshot_i       (phc_snapshot_ts_w),
    .timestamp_out        (ptp_now_w),
    .tod_snapshot_o       (phc_tod_snap_ts_w),
    .tod_snapshot_valid_o (phc_tod_snap_valid_ts_w)
  );

  // ==========================================================================
  //  RX destination-MAC filter (TCAM, REQ-MAC-02)
  // ==========================================================================
  //! link guard: hardware eth-clock liveness -> automatic MAC reinit across
  //! link bounces (the 2026-07-19 TX-wedge class), plus the first hardware
  //! link estimate. LINK_CTRL[1] stays OR-ed in as a firmware fallback.
  wire [31:0] linkg_stat_w;
  wire        cfg_linkg_dis, cfg_linkg_freeze;
  wire        linkg_reinit_w, linkg_eth_rst_w, linkg_est_w;

  KL_link_guard link_guard (
    .clk_i        (axis_clk),
    .rst_n        (axis_resetn),
    .rx_tgl_i     (i_ethrx_tgl),
    .tx_tgl_i     (i_ethtx_tgl),
    .act_tgl_i    (i_ethact_tgl),
    .dis_i        (cfg_linkg_dis),
    .freeze_i     (cfg_linkg_freeze),
    .man_reinit_i (cfg_mac_reinit),
    .reinit_o     (linkg_reinit_w),
    .eth_rst_o    (linkg_eth_rst_w),
    .link_est_o   (linkg_est_w),
    .stat_o       (linkg_stat_w)
  );

  assign eff_link_w = i_link_up & cfg_sw_link &
                      (cfg_linkg_dis | linkg_est_w);
  //! Counter-only link view: PHY + guard, without firmware qualification.
  //! One physical flap = guard pair (41us detect/21ms settle) + a second
  //! delayed firmware qualification pair (if any) -> the
  //! Milan LINK_UP/LINK_DOWN counters read +2 per flap on eff_link. The
  //! counters follow the physical event; eff_link keeps gating ADP/datapath.
  wire cnt_link_w;
  assign cnt_link_w = i_link_up & (cfg_linkg_dis | linkg_est_w);
  assign o_mac_reinit = linkg_reinit_w;
  assign o_eth_rst    = linkg_eth_rst_w;

  //! REQ-MAC-02: the station-address filter inputs the CSR has exported since
  //! 2026-07-01 (promisc/allmulti/MAC_ADDR/MC_HASH) go INTO the RX filter here;
  //! before this they only left milan_datapath as ports for a MAC that does no
  //! address filtering, so non-matching unicast was never dropped in HW.
  //! Armed by TCAM_CTRL[1] (reset 0 = legacy default_pass miss policy).
  //! RXFILT_P = 0 prunes the filter AND its TCAM (see the parameter note).
  //! The tie-off is a straight wire, which is EXACTLY what the shipping
  //! filter emits with promisc_i = 1: every beat forwarded, tready passed
  //! back combinationally, no drop. The TCAM_* CSR window still accepts
  //! writes; nothing reads them, so a pruned build is explicitly promiscuous.
  generate if (RXFILT_P != 0) begin : g_rx_filter
  rx_mac_filter #(.TDATA_WIDTH(TDATA_WIDTH)) rx_filter (
    .clk_i(axis_clk), .rst_n(axis_resetn),
    .addr_filter_en_i(cfg_tcam_addr_filt_en),
    .promisc_i      (cfg_mac_promisc),
    .allmulti_i     (cfg_mac_allmulti),
    //! BYTE ORDER: cfg_mac_addr = {MAC_ADDR_HI[15:0], MAC_ADDR_LO} holds the
    //! station MAC LSB-first (wire byte 0 in [7:0], matching the CSR words);
    //! rx_mac_filter compares MSB-first
    //! against the wire, same as the TCAM key. Swap, exactly as the AAF talker
    //! instantiation above does.
    .station_mac_i  ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                      cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                      cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    .mc_hash_i      (cfg_mc_hash),
    .default_pass_i (cfg_tcam_default_pass),
    .tcam_wr_en_i   (cfg_tcam_wr_en),
    .tcam_wr_index_i(cfg_tcam_wr_index[3:0]),
    .tcam_wr_valid_i(cfg_tcam_wr_valid),
    .tcam_wr_key_i  (cfg_tcam_wr_key),
    .tcam_wr_mask_i (cfg_tcam_wr_mask),
    .tcam_wr_action_i(cfg_tcam_wr_action),
    .s_tdata (rx_axis_from_mac.tdata),
    .s_tkeep (rx_axis_from_mac.tkeep),
    .s_tvalid(rx_axis_from_mac.tvalid),
    .s_tlast (rx_axis_from_mac.tlast),
    .s_tready(rx_axis_from_mac.tready),
    .m_tdata (rx_axis_fabric.tdata),
    .m_tkeep (rx_axis_fabric.tkeep),
    .m_tvalid(rx_axis_fabric.tvalid),
    .m_tlast (rx_axis_fabric.tlast),
    .m_tready(rx_axis_fabric.tready),
    //! Verdict rails are observation-only levels (rx_mac_filter.sv contract);
    //! nothing in this datapath consumes them, so they stay open rather than
    //! being routed to a consumer that would ignore them.
    .frame_action_o(), .frame_match_o(), .frame_dropped_o()
  );
  end else begin : g_no_rx_filter
    assign rx_axis_fabric.tdata        = rx_axis_from_mac.tdata;
    assign rx_axis_fabric.tkeep        = rx_axis_from_mac.tkeep;
    assign rx_axis_fabric.tvalid       = rx_axis_from_mac.tvalid;
    assign rx_axis_fabric.tlast        = rx_axis_from_mac.tlast;
    assign rx_axis_from_mac.tready  = rx_axis_fabric.tready;
  end endgenerate

  // ==========================================================================
  //  ADP — served by the protocol processor (KL_pp_shadow), not here
  // ==========================================================================
  //! adp_advertiser.sv, KL_adp_parser.sv and adp_pkg.sv are DELETED. The
  //! processor's KL_adp_engine owns ENTITY_AVAILABLE/DEPARTING, the
  //! ENTITY_DISCOVER answer and the available_index, off the SAME 0x600 CSR
  //! identity group this file used to feed the advertiser from.
  //!
  //! WHAT MOVED, AND WHAT DIED WITH IT:
  //!   - available_index: LIVE, published by the processor
  //!     (adp_next_avail_index_o -> pp_cd_adp_avail_index_w).
  //!   - the 1 Hz re-advertise tick, the link-edge -> advertise/depart pulses
  //!     and the ENTITY_DISCOVER decode: INTERNAL to the processor now. It
  //!     takes link_up_i as a LEVEL and runs its own timer service, so this
  //!     file no longer synthesises an edge for it.
  //!   - A_ADP_DIAG 0x668's depart/rearm/sent/discover-rx counters, the last
  //!     message word and the advertiser state: STRUCTURAL ZERO. The
  //!     processor publishes no equivalent through the class-D face, and a
  //!     plausible-looking count here would be a mirror of nothing.
  assign adp_available_index = pp_cd_adp_avail_index_w;
  assign adp_depart_cnt = 8'd0;
  assign adp_rearm_cnt = 8'd0;
  assign adp_depart_src = 2'd0;
  assign adp_sent_cnt = 8'd0;
  assign adp_disc_rx_cnt = 8'd0;
  assign adp_last_msg = 4'd0;
  assign adp_state = 4'd0;
  assign adp_disc_seen_p = 1'b0;

  // ==========================================================================
  //  AECP / AEM listener (IEEE 1722.1 / Milan v1.2). The local legacy engine
  //  is deleted; KL_pp_shadow below integrates the protocol processor's active
  //  responder and its live gather faces.
  // ==========================================================================

  // ==========================================================================
  //  Milan Table 5.4 diagnostic counters, one context per Stream Output
  //  (AAF talkers + the CRF Media Clock Output). Serves AECP GET_COUNTERS
  //  per index - 5.4.2.25 Table 5.17 "implement and return" - with the
  //  clause's interval + reset-on-start semantics. The streaming level is
  //  the COMPOSED per-talker admission gate; the CRF context's level is its
  //  enable (a CRF output emits whenever enabled - the untagged fallback is
  //  deliberately alive), and its PDU event derives from the tx counter.
  // ==========================================================================
  wire        aaf_frame_p_w;
  wire [3:0]  aaf_frame_idx_w;
  wire        aaf_frame_tu_w;
  wire        aaf_frame_mr_w;
  wire [N_STREAMS-1:0] aaf_mr_w;
  wire [3:0]  aecp_diag_idx_w;
  wire [5*32-1:0] tkdiag_cnt_w;
  wire [ACMP_SRC_C-1:0] tkd_dirty_p_w /* verilator public_flat_rd */;
  //! the processor's GET_COUNTERS read face (served further down)
  wire        pp_ctr_req_w;
  wire [15:0] pp_ctr_desc_type_w;
  wire [15:0] pp_ctr_desc_index_w;
  wire  [5:0] pp_ctr_word_w;
  wire [31:0] pp_ctr_data_w;
  wire        pp_ctr_wait_w;
  //! ...and its GET_AUDIO_MAP read face (served beside the counters mux)
  wire        pp_amap_req_w;
  wire [15:0] pp_amap_desc_type_w;
  wire [15:0] pp_amap_desc_index_w;
  wire [15:0] pp_amap_map_index_w;
  wire  [1:0] pp_amap_sel_w;
  wire  [7:0] pp_amap_rec_w;
  logic [63:0] pp_amap_data_w;
  wire        pp_amap_wait_w;
  //! ADD/REMOVE_AUDIO_MAPPINGS transaction face
  wire        pp_amap_edit_req_w;
  wire  [2:0] pp_amap_edit_phase_w;
  wire        pp_amap_edit_remove_w;
  wire [15:0] pp_amap_edit_desc_type_w, pp_amap_edit_desc_index_w;
  wire [15:0] pp_amap_edit_count_w;
  wire  [7:0] pp_amap_edit_rec_w;
  wire [63:0] pp_amap_edit_record_w, pp_amap_edit_value_w;
  logic [63:0] pp_amap_edit_data_w;
  wire        pp_amap_edit_wait_w;
  // Milan-info gather face (GET_STREAM_INFO / GET_AVB_INFO / GET_AS_PATH)
  wire        pp_gsi_req_w;
  wire  [1:0] pp_gsi_kind_w;
  wire [15:0] pp_gsi_desc_type_w, pp_gsi_desc_index_w;
  wire  [3:0] pp_gsi_sel_w;
  wire  [7:0] pp_gsi_ord_w;
  wire [63:0] pp_gsi_prop_fmt_w;
  logic [63:0] pp_gsi_data_w;
  wire        pp_gsi_wait_w;
  //! CRF PDU strobe from the tx counter delta; deferred one cycle when an
  //! AAF frame pulse occupies the diag event port (events are ~8.5 k/s
  //! against a 50+ MHz clock, so the skid never accumulates)
  logic [31:0] tkd_crfq_r;
  logic        tkd_crf_pend_r;
  wire         tkd_crf_p_w = tkd_crf_pend_r & ~aaf_frame_p_w;
  always_ff @(posedge axis_clk) begin : tkd_crf_evt
    if (!axis_resetn) begin
      tkd_crfq_r     <= 32'd0;
      tkd_crf_pend_r <= 1'b0;
    end else begin
      tkd_crfq_r <= crft_count_w;
      if (crft_count_w != tkd_crfq_r) tkd_crf_pend_r <= 1'b1;
      else if (tkd_crf_p_w)           tkd_crf_pend_r <= 1'b0;
    end
  end : tkd_crf_evt
  //! context vector: AAF talkers 0..N-1, CRF (when this shape has one) at N
  //! (a generate, not a width-bending conditional: the two arms have
  //! different exact widths and the ternary form lints as trunc+expand)
  wire [ACMP_SRC_C-1:0] tkd_streaming_w;
  generate if (ACMP_SRC_C > N_STREAMS) begin : g_tkd_crf
    assign tkd_streaming_w = {crft_emit_en_w, aaf_stream_en_w};
  end else begin : g_tkd_nocrf
    assign tkd_streaming_w = aaf_stream_en_w;
  end endgenerate
  // --------------------------------------------------------------------------
  //  IEEE 1722-2016 4.4.4.3: the mr (media clock restart) level. The clause
  //  is a shall for a talker whose timestamps come from a received CRF
  //  stream - "any streams deriving timestamps from the CRF stream shall
  //  toggle the mr bit if a disruption of the CRF stream occurs" - and that
  //  is exactly this fabric when clk_src selects the CRF media clock (2).
  //  crf_locked_w falling IS the disruption: KL_crf_rx drops lock after
  //  100 ms of CRF silence (and needs 8 clean PDUs to re-lock), so the edge
  //  is the debounced verdict, not a per-PDU twitch.
  //
  //  Restart requests are IGNORED unless the CRF clock is the one in use: on
  //  an internal media clock there is no CRF stream to be disrupted, so
  //  toggling mr would be a false alarm to every listener.
  // --------------------------------------------------------------------------
  //! IEEE 1722-2016 4.4.4.3 disruption pulse: crf_locked_w falls while CRF is
  //! the selected media clock source. The clause's OTHER mandatory trigger, a
  //! change of the media clock SOURCE (PICS Table F.7 AAF-5, AAF:M), is
  //! detected INSIDE KL_media_clock_restart from clk_src_i, so all of 4.4.4.3
  //! lives in the one module.
  logic tkd_crflk_q_r;
  always_ff @(posedge axis_clk) begin : mcr_trigger
    if (!axis_resetn) tkd_crflk_q_r <= 1'b0;
    else              tkd_crflk_q_r <= crf_locked_w;
  end : mcr_trigger
  //! ... and the THIRD trigger, the one 4.4.4.3 names beside the disruption:
  //! "or if the mr bit in the CRF stream has been toggled". crf_mr_toggle_p_w
  //! is that echo, straight off the accepted PDU (gh #62 H2a). It joins the
  //! disruption pulse INSIDE the same clock-source gate, which is 10.4.3's
  //! own scoping and not a convenience: "If a Listener is receiving both a
  //! media stream and a CRF stream, only the mr bit from the stream being
  //! used by the Listener for recovering the media clock is valid" - on an
  //! internal media clock the received CRF bit governs nothing here, and
  //! echoing it would restart every listener's clock over a stream this
  //! device is not slaved to.
  //! crf_clk_selected_r - the LIVE verdict (#74): with INTERNAL selected,
  //! 4.4.4.3's "disruption of the CRF stream" is not a disruption of OUR
  //! clock and must not toggle mr on our streams; with the CRF source
  //! selected, it is exactly the mandatory trigger, now reachable.
  wire mcr_restart_p_w = crf_clk_selected_r
                       & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w);

  //! the 4.4.4.3 / 10.4.3 level, for EVERY stream this fabric can emit -
  //! the AAF talkers AND the CRF Media Clock Output, which is a Talker in
  //! its own right (PICS Table F.16 CRF-3/CRF-5) and whose stream is exactly
  //! the one 10.4.3 writes the clause for. One engine, because the TARGET is
  //! a property of the media clock and not of a stream: two outputs on one
  //! clock must never end up on opposite levels. The per-stream half - the
  //! ">= 8 AVTPDUs for a given continuous stream" hold - stays per context,
  //! so the CRF output's 500 PDU/s hold and an AAF talker's 8 kPDU/s hold
  //! run independently and neither can rush the other.
  //!
  //! THE WIDTH IS N_STREAMS + 1, NOT ACMP_SRC_C, and the difference is a
  //! real one on a shape whose entity declares no CRF Stream Output
  //! (ACMP_SRC_C == N_STREAMS - the tracked 1x1 config is one). KL_crf_tx is
  //! instantiated UNCONDITIONALLY and still emits there under the bring-up
  //! free-run escape (CRFT_CTRL 0x750 with lwSRP off), so it is a CRF Talker
  //! on the wire whatever the AEM says. Sizing this by the descriptor count
  //! would hand that talker a tied-off mr = 0 - a stream telling every
  //! listener "the media clock never restarted" straight through a source
  //! change, which is the exact defect this round closes. What the
  //! descriptor count governs is the COUNTER block below (a Stream Output
  //! that does not exist has no GET_COUNTERS row to serve), not the wire.
  localparam int MCR_CTX_C = N_STREAMS + 1;
  wire [MCR_CTX_C-1:0] mcr_streaming_w = {cfg_crft_en, aaf_stream_en_w};
  wire [MCR_CTX_C-1:0] mcr_mr_v_w;
  KL_media_clock_restart #(.N_TALKERS_P(MCR_CTX_C)) media_clock_restart (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .restart_p_i (mcr_restart_p_w),
    //! LIVE (#74): the 4.4.4.3 source-change trigger fires on a real
    //! SET_CLOCK_SOURCE now - the module's clk_src_q_r edge detector was
    //! built for this and spent its first months watching a constant
    .clk_src_i   (media_clk_src_r),
    .streaming_i (mcr_streaming_w),
    //! the SAME muxed PDU feed KL_talker_diag_ctx takes below (AAF strobe or
    //! the deferred CRF strobe, never both in a cycle) ...
    .frame_p_i   (aaf_frame_p_w | tkd_crf_p_w),
    .frame_idx_i (aaf_frame_p_w ? aaf_frame_idx_w : 4'(N_STREAMS)),
    //! ... and the mr bit the announced PDU really carried, per side: the
    //! packetizer's stamped bit for an AAF frame, KL_crf_tx's mr_last_o for
    //! the CRF PDU. Feeding the wire's own bit (not the granted level) is
    //! what makes the hold count eight TRANSMITTED PDUs at the new value.
    .frame_mr_i  (aaf_frame_p_w ? aaf_frame_mr_w : crft_mr_last_w),
    .mr_o        (mcr_mr_v_w)
  );
  assign aaf_mr_w  = mcr_mr_v_w[N_STREAMS-1:0];
  assign crft_mr_w = mcr_mr_v_w[N_STREAMS];

  //! Milan Table 5.4 per-Stream Output counters. The context count follows
  //! the generated descriptor shape, not the unconditional CRF transmitter:
  //! an output absent from AEM has no counter row to serve. AAF and CRF events
  //! share the same feed as the media-clock-restart generator so MEDIA_RESET
  //! observes the bit that actually reached the wire.
  KL_talker_diag_ctx #(
    .N_CTX_P    (ACMP_SRC_C),
    .TICK_CYC_P (DIAG_TICK_CYC_P)
  ) talker_diag (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .streaming_i (tkd_streaming_w),
    .frame_p_i   (aaf_frame_p_w | tkd_crf_p_w),
    .frame_idx_i (aaf_frame_p_w ? aaf_frame_idx_w : 4'(N_STREAMS)),
    //! Match the completion strobe to the bit frozen into that PDU. The live
    //! PHC verdict may change while an AAF frame is draining or while a CRF
    //! completion event waits behind the AAF event port.
    .tu_i        (aaf_frame_p_w ? aaf_frame_tu_w : crft_tu_last_w),
    .frame_mr_i  (aaf_frame_p_w ? aaf_frame_mr_w : crft_mr_last_w),
    .rd_idx_i    (ctrq_index_r[3:0]),
    .rd_start_o  (tkdiag_cnt_w[0*32 +: 32]),
    .rd_stop_o   (tkdiag_cnt_w[1*32 +: 32]),
    .rd_mreset_o (tkdiag_cnt_w[2*32 +: 32]),
    .rd_tu_o     (tkdiag_cnt_w[3*32 +: 32]),
    .rd_ftx_o    (tkdiag_cnt_w[4*32 +: 32]),
    //! The lossless per-descriptor arbiter below consumes this pulse and
    //! drives the processor's Table 5.22 GET_COUNTERS notification (#69).
    .dirty_p_o   (tkd_dirty_p_w)
  );

  //! gh #58 stream-command law truth vectors — the LIVE gates, never
  //! mirrors. Outputs: aaf_stream_en_w IS the composed 5.3.7.3 wire gate
  //! (talker_active & lwsrp_stream_gate, bypass/MAAP escapes included -
  //! a cfg_aaf_bypass build truthfully counts its outputs as streaming,
  //! so SET_CONFIG / SET_FMT(out) refuse there); the CRF Media Clock
  //! Output (when this shape has one) contributes crft_emit_en_w, the
  //! LICENCE-gated emission enable, not the bare CSR bit. A generate,
  //! not a width-bending ternary (the tkd_streaming_w precedent).
  //! (the composed per-source streaming truth the deleted AECP stream-command
  //! law read; no reader remains)
  generate if (ACMP_SRC_C > N_STREAMS) begin : g_aecp_ostrm_crf
  end else begin : g_aecp_ostrm
  end endgenerate

  //! ------------------------------------------------------------------------
  //! The deleted local AECP plane has no fallback instance. KL_pp_shadow below
  //! is the active processor responder and consumes the counter, audio-map, and
  //! Milan-info gather faces in this file. The assignments below preserve only
  //! legacy CSR ABI locations for state that has no root integration output.
  //! Structural zero means "no connected source", not "an active engine is
  //! idle".
  assign aecp_bdbg0_w = 32'd0, aecp_bdbg1_w = 32'd0, aecp_bdbg2_w = 32'd0;
  //! Driven by KL_pp_shadow below. This is the processor's authoritative
  //! LOCK_ENTITY level and gates every local, non-ATDECC map writer.
  assign aecp_current_config = 16'd0;  //! exported config state is not wired into this legacy CSR
  assign aecp_cmd_count = 16'd0;
  assign aecp_resp_count = 16'd0;
  assign aecp_ctlr_diag = 32'd0;
  assign aemp_stat_w = 32'd0;  //! no AEM patch ingest
  //! pp_aecp_pt_offset_*/pp_aecp_fmt_in_*/pp_aecp_fmt_out_*: the
  //! processor per-row settings faces, declared ahead of the
  //! aecp_in0_fmt fold, their first reader (#193); documented with the
  //! KL_pp_shadow block below.
  logic [ACMP_SRC_C*32-1:0]   pp_aecp_pt_offset_w;
  logic [ACMP_SRC_C-1:0]      pp_aecp_pt_offset_v_w;
  logic [ACMP_SINKS_C*64-1:0] pp_aecp_fmt_in_w;
  logic [ACMP_SINKS_C-1:0]    pp_aecp_fmt_in_v_w;
  logic [ACMP_SRC_C*64-1:0]   pp_aecp_fmt_out_w;
  logic [ACMP_SRC_C-1:0]      pp_aecp_fmt_out_v_w;
  //! STREAM_INPUT[0]'s stream_format. NOT ZERO: KL_avtp_rx_monitor_ctx
  //! accepts frames against this value, so 0 rejects every conformant AAF
  //! PDU and stream 0 accepts NOTHING. The DEFAULT is the AEM ROM's old
  //! AEM_STRIN_FMT_C[0], regenerated from the same config through the
  //! entity-shape header - and since issue #67 a controller's
  //! SET_STREAM_FORMAT overrides it through the processor's published
  //! settings row: the acceptance filter follows the format the controller
  //! set, which is the command's whole purpose (the verdict face already
  //! refused anything this build cannot serve). Row 0 only, matching the
  //! one monitor context this signal feeds.
  assign aecp_in0_fmt = pp_aecp_fmt_in_v_w[0]
                        ? pp_aecp_fmt_in_w[63:0] : ADP_STRIN0_FMT_C;
  //! per-STREAM_OUTPUT presentation offset. SET_STREAM_INFO(ACC_LAT) is a
  //! WRITER AGAIN (issue #67): entry k folds the processor's published
  //! SEL_PTOFF row k when a controller has set it, and holds the Milan v1.2
  //! default otherwise. The default is a DEFAULT, not a zero: 0 ns would be
  //! a presentation time in the past and every listener would drop every
  //! frame as late. The CRF Media Clock Output consumes ITS OWN row through
  //! its transit entry (talker_unique_id CRF_TUID_C = N_STREAMS), so a
  //! controller can move the CRF presentation offset by the same command.
  //! This fold is the ONE derivation point: GET_STREAM_INFO's latency word
  //! serves these same entries below, so the wire the talker stamps and the
  //! answer a controller reads cannot disagree.
  localparam logic [31:0] PRES_DFLT_C = 32'd2_000_000;   //! 2 ms
  always_comb begin : pres_offset_fold
    for (int k = 0; k < ACMP_SRC_C; k++)
      aecp_pres_offset[32*k +: 32] = pp_aecp_pt_offset_v_w[k]
                                     ? pp_aecp_pt_offset_w[32*k +: 32]
                                     : PRES_DFLT_C;
    for (int k = ACMP_SRC_C; k < 16; k++)
      aecp_pres_offset[32*k +: 32] = PRES_DFLT_C;
  end
  //! (the media clock source is LIVE (#74) - see media_clk_resolve and the
  //!  media-clock banner at the top of this file. The CRF Media Clock Input
  //!  engine parses, counts, reports - and, with the CRF source selected,
  //!  steers: the MMCM servo takes the rate error and the packet grid
  //!  follows the physical one through KL_media_grid_align.)
  //! The AEM descriptor-map write ports are driven by the transactional
  //! ADD/REMOVE_AUDIO_MAPPINGS block beside GET_AUDIO_MAP below. Dynamic map
  //! ownership is generated from the same YAML that emits number_of_maps=0,
  //! so a static output never enables an empty crossbar by accident.
  assign aecp_dmap_wr_p_w    = amap_edit_iwr_p_r;
  assign aecp_dmap_wr_addr_w = amap_edit_iwr_addr_r;
  assign aecp_dmap_wr_word_w = amap_edit_iwr_word_r;
  assign aecp_dmap_dyn_w     = |ADP_DMAP_IN_MASK_C;
  assign aecp_odmap_wr_p_w    = amap_edit_owr_p_r;
  assign aecp_odmap_wr_slot_w = amap_edit_owr_slot_r;
  assign aecp_odmap_wr_word_w = amap_edit_owr_word_r;
  assign aecp_odmap_dyn_w     = |ADP_DMAP_OUT_MASK_C;
  // ------------------------------------------------------------------------
  //  GET_COUNTERS (1722.1-2021 7.4.42, Milan v1.2 5.4.2.25 / Table 5.16)
  // ------------------------------------------------------------------------
  //! The processor parses the command and lays out the response; THIS file
  //! says what the numbers mean, because the events Table 5.6 counts happen
  //! here. One quadlet is asked for at a time on ctr_word_o: 0..31 is the
  //! Table 7-157 counters_block quadlet at block byte 4*n, and 32 is the
  //! counters_valid mask itself.
  //!
  //! TWO ORDERS, AND THEY DIFFER. KL_avtp_rx_monitor_ctx publishes its twelve
  //! tallies in its OWN order (its C_*_C localparams: ..., UF, LT, ET, FRX,
  //! then TV, TNV last, because the tv pair was added after the rest). The
  //! standard interleaves them: TIMESTAMP_VALID and TIMESTAMP_NOT_VALID sit
  //! at offsets 24 and 28, BEFORE UNSUPPORTED_FORMAT at 32. The case below is
  //! written in the standard's offset order with the monitor's own symbol
  //! names on the right, so the two orderings are visible side by side rather
  //! than fused into a transcribed table of numbers.
  //!
  //! MASK BIT == QUADLET INDEX. Table 7-156 numbers MEDIA_LOCKED bit #31 and
  //! Table 7-157 puts it at offset 0; TIMESTAMP_VALID is bit #25 at offset
  //! 24. So the table's bit # is 31 - n and its weight is 2^n, which makes
  //! the counters_valid bit for quadlet n exactly bit n of a conventional
  //! LSB-0 word. 0xFFF is quadlets 0..11 = every counter Table 7-157 defines
  //! for a STREAM_INPUT before the reserved span at offset 48.
  //!
  //! ALL TWELVE, not the ten Milan makes mandatory. Milan v1.2 Table 5.6
  //! does not require TIMESTAMP_VALID / TIMESTAMP_NOT_VALID (they are an IEEE
  //! set Milan declines to compel, NOT a Milan addition), but this monitor
  //! genuinely counts them per sink, and 7.4.42.2's bit means "this counter
  //! exists and is valid". Claiming a counter we keep is honest; the failure
  //! mode this face exists to avoid is the reverse - a mask of ones over a
  //! block that never moves.
  localparam int MON_ML_C  = 0, MON_MU_C  = 1, MON_SI_C = 2, MON_SM_C  = 3,
                 MON_MR_C  = 4, MON_TU_C  = 5, MON_UF_C = 6, MON_LT_C  = 7,
                 MON_ET_C  = 8, MON_FRX_C = 9, MON_TV_C = 10, MON_TNV_C = 11;
  localparam logic [31:0] CTR_VALID_SIN_C = 32'h0000_0FFF;
  localparam logic [15:0] DESC_STREAM_INPUT_C = 16'h0005;  //! Table 7-4

  wire [12*32-1:0] mon_diag_cnt_w;

  //! WHICH OBJECT WE ARE ALLOWED TO ANSWER FOR. There is no NO_SUCH_DESCRIPTOR
  //! arm on this face - it carries data and a mask, nothing else - so an
  //! index the monitor has no context for MUST come back as an empty mask
  //! rather than as some other sink's numbers. aecp_diag_idx_w is only four
  //! bits and KL_avtp_rx_monitor_ctx CLAMPS an out-of-range value to 0, so
  //! feeding it ctr_desc_index_o unguarded would answer a GET_COUNTERS for
  //! STREAM_INPUT 9 with sink 0's counters under a full mask: a wrong-object
  //! answer, which is the same class of lie as an advertised zero. The guard
  //! is the reason the index is qualified before it is narrowed.
  //!
  //! N_STREAMS is the monitor's N_LISTENERS_P. A CRF sink appended after the
  //! AAF inputs has no monitor context and so reports an empty mask, which is
  //! true: this build keeps no Table 5.6 counters for it.
  //! -------------------------------------------------------------------
  //! REGISTERED ANSWER SERVER (USER 2026-08-15: pipeline the failing
  //! endpoints). The v48 route failed at WNS -1.7 on ONE cone: the engine's
  //! captured selectors left the processor, ran the answer muxes below
  //! combinationally (the audio-map page scans and the Tables 5.9-5.12 flag
  //! terms are over a nanosecond deep), and landed back in the engine's
  //! gather register in the same cycle. The faces' OWN wait contract is the
  //! cut: selectors register HERE, the deep mux computes from the REGISTERED
  //! copy into a data register, and wait holds each beat for the two cycles
  //! that takes. The engine's gather beats are HOLD-tolerant by design (the
  //! integrator-hold checks in the harnesses), and the per-beat cost is two
  //! 10 ns cycles against millisecond commands.
  wire  [31:0] ctr_ans_raw_w;
  logic [15:0] ctrq_type_r, ctrq_index_r;
  logic  [5:0] ctrq_word_r;
  logic        ctr_srv1_r, ctr_srv2_r;
  logic [31:0] ctr_data_r;
  wire ctr_sel_match_w = (ctrq_type_r  == pp_ctr_desc_type_w)
                      && (ctrq_index_r == pp_ctr_desc_index_w)
                      && (ctrq_word_r  == pp_ctr_word_w);
  always_ff @(posedge axis_clk or negedge axis_resetn) begin : ctr_answer_srv
    if (!axis_resetn) begin
      ctrq_type_r <= 16'd0; ctrq_index_r <= 16'd0; ctrq_word_r <= 6'd0;
      ctr_srv1_r  <= 1'b0;  ctr_srv2_r   <= 1'b0;  ctr_data_r  <= 32'd0;
    end else begin
      ctrq_type_r  <= pp_ctr_desc_type_w;
      ctrq_index_r <= pp_ctr_desc_index_w;
      ctrq_word_r  <= pp_ctr_word_w;
      ctr_srv1_r   <= pp_ctr_req_w && ctr_sel_match_w;
      ctr_srv2_r   <= pp_ctr_req_w && ctr_sel_match_w && ctr_srv1_r;
      ctr_data_r   <= ctr_ans_raw_w;
    end
  end

  wire ctr_sin_w = (ctrq_type_r == DESC_STREAM_INPUT_C)
                && (ctrq_index_r < 16'(N_STREAMS));

  assign aecp_diag_idx_w = ctr_sin_w ? ctrq_index_r[3:0] : 4'd0;

  logic [31:0] ctr_blk_w;
  always_comb begin
    unique case (ctrq_word_r)
      6'd0    : ctr_blk_w = mon_diag_cnt_w[MON_ML_C  * 32 +: 32]; // @0   MEDIA_LOCKED
      6'd1    : ctr_blk_w = mon_diag_cnt_w[MON_MU_C  * 32 +: 32]; // @4   MEDIA_UNLOCKED
      6'd2    : ctr_blk_w = mon_diag_cnt_w[MON_SI_C  * 32 +: 32]; // @8   STREAM_INTERRUPTED
      6'd3    : ctr_blk_w = mon_diag_cnt_w[MON_SM_C  * 32 +: 32]; // @12  SEQ_NUM_MISMATCH
      6'd4    : ctr_blk_w = mon_diag_cnt_w[MON_MR_C  * 32 +: 32]; // @16  MEDIA_RESET
      6'd5    : ctr_blk_w = mon_diag_cnt_w[MON_TU_C  * 32 +: 32]; // @20  TIMESTAMP_UNCERTAIN
      6'd6    : ctr_blk_w = mon_diag_cnt_w[MON_TV_C  * 32 +: 32]; // @24  TIMESTAMP_VALID
      6'd7    : ctr_blk_w = mon_diag_cnt_w[MON_TNV_C * 32 +: 32]; // @28  TIMESTAMP_NOT_VALID
      6'd8    : ctr_blk_w = mon_diag_cnt_w[MON_UF_C  * 32 +: 32]; // @32  UNSUPPORTED_FORMAT
      6'd9    : ctr_blk_w = mon_diag_cnt_w[MON_LT_C  * 32 +: 32]; // @36  LATE_TIMESTAMP
      6'd10   : ctr_blk_w = mon_diag_cnt_w[MON_ET_C  * 32 +: 32]; // @40  EARLY_TIMESTAMP
      6'd11   : ctr_blk_w = mon_diag_cnt_w[MON_FRX_C * 32 +: 32]; // @44  FRAMES_RX
      6'd32   : ctr_blk_w = CTR_VALID_SIN_C;                      //      counters_valid
      default : ctr_blk_w = 32'd0;   // @48..@92 reserved, @96.. ENTITY_SPECIFIC
    endcase
  end

  // ------------------------------------------------------------------------
  //  AVB_INTERFACE and CLOCK_DOMAIN counters (Milan v1.2 5.3.6.3 Table 5.1,
  //  5.3.11.2 Table 5.7; IEEE 1722.1-2021 Tables 7-158..7-161)
  // ------------------------------------------------------------------------
  //! The two counter families la_avdecc's Milan gate demands beside the
  //! Stream Input set (avdeccControllerImplHandlers.cpp: LinkUp + LinkDown +
  //! GptpGmChanged for the interface, Locked + Unlocked for the clock
  //! domain). Until this block they answered an EMPTY mask - honest, and
  //! DIRTY: 5.3.6.3 and 5.3.11.2 are shalls.
  //!
  //! EVERY COUNT IS AN EDGE OF ONE LEVEL, and that construction IS the
  //! clause's invariant: 5.3.6.3 requires "at any time, either
  //! LINK_UP=LINK_DOWN (the link is currently down) or LINK_UP=LINK_DOWN+1"
  //! and 5.3.11.2 the same of LOCKED/UNLOCKED. Two counters incremented on
  //! opposite edges of the SAME registered level can never diverge by more
  //! than one, and both levels reset LOW (link down, clock not valid), which
  //! is the equal-counts arm. Nothing enforces the invariant; it is
  //! structural.
  //!
  //! THE LEVELS, and why these are the honest ones:
  //!   * link:   eff_link_w - the ENTITY-VISIBLE link (PHY link AND the
  //!     software link gate), the same level the protocol processor, the
  //!     link guard consumers and the ADP availability logic already treat
  //!     as "the AVB interface is up". Counting the raw PHY here would let
  //!     LINK_UP outrun what every other part of this device reports.
  //!   * GM:     pp_gm_id_change_p_w - a change of the nonzero grandmaster
  //!     identity the product fabric owner publishes, and nothing else. Milan Table 5.1
  //!     defines GPTP_GM_CHANGED as "Number of gPTP GM changes, since
  //!     boot", so the only edge that may move it is an edge of
  //!     gptp_grandmaster_id. The ADP duty pp_gm_change_p_w is a WIDER
  //!     strobe - it also rises when gptp_domain_number moves, because
  //!     that is an ADPDU field and 1722.1-2021 6.2.6 re-advertises on it -
  //!     and counting it here would report grandmaster changes that never
  //!     happened. Two duties, two strobes, ONE shared identity compare
  //!     (pp_gm_id_edge_w) so they can never disagree about the identity.
  //!   * media clock: ~clkv_tu_w. Milan leaves "locked" explicitly open
  //!     ("the definition of locked is left open to each manufacturer",
  //!     5.3.11.2); this build's definition is the active-owner CLKV verdict -
  //!     the SAME truth the tu bit stamps into every AVTPDU (VERSION 0x0056).
  //!     One clock-validity authority, two views; a LOCKED count that
  //!     disagreed with the tu bit on the wire would be two answers to one
  //!     question. tu resets 1 (unknown is NOT valid), so locked resets LOW.
  localparam logic [15:0] DESC_AVB_INTERFACE_C = 16'h0009;  //! Table 7-4
  localparam logic [15:0] DESC_CLOCK_DOMAIN_C  = 16'h0024;  //! Table 7-4
  //! Table 7-158 numbers LINK_UP bit #31 (quadlet 0), LINK_DOWN #30 (1),
  //! GPTP_GM_CHANGED #26 (5, block byte 20); Table 7-160 LOCKED #31 (0),
  //! UNLOCKED #30 (1). Mask bit n = quadlet n, LSB-0 (the Table 7-156
  //! arithmetic in the Stream Input section above).
  localparam logic [31:0] CTR_VALID_AVB_C  = 32'h0000_0023;
  localparam logic [31:0] CTR_VALID_CKD_C  = 32'h0000_0003;

  logic        ctr_link_q_r, ctr_mclk_q_r;
  //! THE EDGES THE TWO FAMILIES COUNT, named once so the Milan Table 5.22
  //! counter-change pulses below are the very conditions that increment a
  //! served counter (derive, never mirror): a link edge moves LINK_UP or
  //! LINK_DOWN, a lock edge moves LOCKED or UNLOCKED, and the GM strobe
  //! moves GPTP_GM_CHANGED in the same always_ff.
  wire ctr_avb_link_edge_w = eff_link_w != ctr_link_q_r;
  wire ctr_ckd_lock_edge_w = (~clkv_tu_w) != ctr_mclk_q_r;
  wire ctr_avb_dirty_w = ctr_avb_link_edge_w || pp_gm_id_change_p_w;
  wire ctr_ckd_dirty_w = ctr_ckd_lock_edge_w;
  logic [31:0] ctr_linkup_r, ctr_linkdn_r;
  logic [31:0] ctr_gmchg_r /* verilator public_flat_rd */;
  logic [31:0] ctr_mlock_r, ctr_munlock_r;
  always_ff @(posedge axis_clk or negedge axis_resetn) begin : itf_ctrs
    if (!axis_resetn) begin
      ctr_link_q_r <= 1'b0;
      ctr_mclk_q_r <= 1'b0;
      ctr_linkup_r <= 32'd0;
      ctr_linkdn_r <= 32'd0;
      ctr_gmchg_r  <= 32'd0;
      ctr_mlock_r  <= 32'd0;
      ctr_munlock_r<= 32'd0;
    end else begin
      ctr_link_q_r <= eff_link_w;
      ctr_mclk_q_r <= ~clkv_tu_w;
      //! 32-bit and wrapping, exactly as both clauses specify ("wraps over
      //! to zero when it reaches the maximum value")
      if (ctr_avb_link_edge_w &&  eff_link_w) ctr_linkup_r <= ctr_linkup_r + 32'd1;
      if (ctr_avb_link_edge_w && !eff_link_w) ctr_linkdn_r <= ctr_linkdn_r + 32'd1;
      if (pp_gm_id_change_p_w)          ctr_gmchg_r  <= ctr_gmchg_r  + 32'd1;
      if (ctr_ckd_lock_edge_w && ~clkv_tu_w) ctr_mlock_r  <= ctr_mlock_r  + 32'd1;
      if (ctr_ckd_lock_edge_w &&  clkv_tu_w) ctr_munlock_r<= ctr_munlock_r+ 32'd1;
    end
  end

  //! ONE interface and ONE clock domain in every shipped shape, so index 0
  //! is the only object either family can answer for - the same
  //! wrong-object rule as the Stream Input clamp above: any other index is
  //! an EMPTY mask over a zero block, never quadlets that belong to 0.
  wire ctr_avb_w = (ctrq_type_r == DESC_AVB_INTERFACE_C)
                && (ctrq_index_r == 16'd0);
  wire ctr_ckd_w = (ctrq_type_r == DESC_CLOCK_DOMAIN_C)
                && (ctrq_index_r == 16'd0);

  logic [31:0] ctr_avb_blk_w;
  always_comb begin
    unique case (ctrq_word_r)
      6'd0    : ctr_avb_blk_w = ctr_linkup_r;    // @0   LINK_UP
      6'd1    : ctr_avb_blk_w = ctr_linkdn_r;    // @4   LINK_DOWN
      6'd5    : ctr_avb_blk_w = ctr_gmchg_r;     // @20  GPTP_GM_CHANGED
      6'd32   : ctr_avb_blk_w = CTR_VALID_AVB_C; //      counters_valid
      default : ctr_avb_blk_w = 32'd0;  // FRAMES_TX/RX + RX_CRC_ERROR live
                                        // in mac_rmon's domain: unclaimed
                                        // here rather than claimed-zero
    endcase
  end

  logic [31:0] ctr_ckd_blk_w;
  always_comb begin
    unique case (ctrq_word_r)
      6'd0    : ctr_ckd_blk_w = ctr_mlock_r;     // @0   LOCKED
      6'd1    : ctr_ckd_blk_w = ctr_munlock_r;   // @4   UNLOCKED
      6'd32   : ctr_ckd_blk_w = CTR_VALID_CKD_C; //      counters_valid
      default : ctr_ckd_blk_w = 32'd0;
    endcase
  end

  //! Stream Output uses Milan Table 5.17, not IEEE Table 7-159. Milan removes
  //! three IEEE counters and compacts the surviving five into quadlets 0..4.
  localparam logic [15:0] DESC_STREAM_OUTPUT_C = 16'h0006; //! Table 7-4
  localparam logic [31:0] CTR_VALID_SOUT_C = 32'h0000_001F;
  wire ctr_sout_w = (ctrq_type_r == DESC_STREAM_OUTPUT_C)
                 && (32'(ctrq_index_r) < ACMP_SRC_C);
  logic [31:0] ctr_sout_blk_w;
  always_comb begin
    unique case (ctrq_word_r)
      6'd0    : ctr_sout_blk_w = tkdiag_cnt_w[0*32 +: 32]; // STREAM_START
      6'd1    : ctr_sout_blk_w = tkdiag_cnt_w[1*32 +: 32]; // STREAM_STOP
      6'd2    : ctr_sout_blk_w = tkdiag_cnt_w[2*32 +: 32]; // MEDIA_RESET
      6'd3    : ctr_sout_blk_w = tkdiag_cnt_w[3*32 +: 32]; // TIMESTAMP_UNCERTAIN
      6'd4    : ctr_sout_blk_w = tkdiag_cnt_w[4*32 +: 32]; // FRAMES_TX
      6'd32   : ctr_sout_blk_w = CTR_VALID_SOUT_C;
      default : ctr_sout_blk_w = 32'd0;
    endcase
  end

  //! Everything else, including ENTITY and out-of-range indices, answers zero data
  //! AND an empty mask on the same term, so the two can never disagree.
  assign ctr_ans_raw_w = ctr_sin_w ? ctr_blk_w
                       : ctr_sout_w ? ctr_sout_blk_w
                       : ctr_avb_w ? ctr_avb_blk_w
                       : ctr_ckd_w ? ctr_ckd_blk_w
                       : 32'd0;
  //! HOLD per the face contract: two cycles per beat while the registered
  //! server settles, then the answer is stable in ctr_data_r.
  assign pp_ctr_data_w = ctr_data_r;
  //! the LIVE match term closes the stale-beat window: the engine may
  //! advance its selector in the same cycle it consumes a beat, and srv2
  //! stays high one cycle past the change - without this term that one
  //! cycle accepted the NEW word with the OLD answer
  assign pp_ctr_wait_w = pp_ctr_req_w && !(ctr_srv2_r && ctr_sel_match_w);

  // ------------------------------------------------------------------------
  //  GET_AUDIO_MAP (1722.1-2021 7.4.44, Milan v1.2 5.4.2.26 / 5.3.3.9)
  // ------------------------------------------------------------------------
  //! The processor parses the command, enforces the 7.4.44.1 page rule and
  //! lays out the response; THIS file says what a dynamic mapping IS,
  //! because the live state is the render crossbar's map RAM - the same
  //! flops CHMAP_LOOP 0x914 reads back, so the wire answer and the CSR
  //! readback are two independent readers of one store.
  //!
  //! THE INDEX LAW IS 0x001C's: the dynamic map is keyed by the GLOBAL
  //! cluster index = the addressed port's base_cluster + the record's
  //! port-relative mapping_cluster_offset, and that global index IS the
  //! render map RAM's address. A global index this board does not render
  //! (>= 10 keys
  //! on an 8x8 model) has no RAM behind it and truthfully answers
  //! "not mapped" - those clusters cannot be routed, so no mapping exists.
  //!
  //! WHAT A RECORD MEANS IN THIS BUILD, and what is NOT represented: the
  //! map entry is {en[7], src[6], idx[5:0]}. A reported dynamic mapping exists
  //! iff en = 1 AND src = 0 (an AVB listener source): mapping_stream_index
  //! = idx[5:3], mapping_stream_channel = idx[2:0], mapping_cluster_offset
  //! = the port-relative offset, mapping_cluster_channel = 0 - every
  //! cluster of this model is MONO (one cluster == one audio channel, the
  //! 0x0027 law), so channel 0 is the only channel a cluster has. NOT
  //! represented: any en = 1 entry whose source is not 0. Source 0 is the
  //! fabric AVB-listener namespace; all other source codes are reserved and
  //! GET_AUDIO_MAP truthfully reports them as unmapped.
  //!
  //! WHO SUPPLIES THE PER-PORT GEOMETRY: this fabric, from elaboration
  //! constants, because it CANNOT come from anywhere else - the µISA has no
  //! subtract (a store-read base_cluster could never produce port-relative
  //! offsets) and the gather face carries no µCPU operands. The constants
  //! The generated entity definition carries the exact STREAM_PORT_INPUT
  //! geometry used by the AEM image. The live protocol store therefore has
  //! one entry for every declared input cluster, including fabric-only
  //! clusters that do not project onto the physical render crossbar. A generated
  //! RPHYS entry controls that projection and prevents a non-physical global
  //! cluster key from aliasing one of the ten physical render slots.
  //! EXISTENCE is not decided here at all: the processor locates the
  //! STREAM_PORT_INPUT descriptor in the image first, so an index the image
  //! lacks answers NO_SUCH_DESCRIPTOR whatever these constants claim, and
  //! this face's own guard only ever ADDS refusals (empty pages), never
  //! objects.
  localparam int AMAP_IN_PORTS_C = ADP_DMAP_IN_NPORTS_C;
  localparam int AMAP_IN_KEYS_C  = ADP_DMAP_IN_KEYS_C;
  localparam int AMAP_IN_KEY_W_C = (AMAP_IN_KEYS_C <= 2)
                                  ? 1 : $clog2(AMAP_IN_KEYS_C);
  localparam int AMAP_PAGE_C     = ADP_DMAP_IN_PAGE_C;
  localparam logic [15:0] DESC_STREAM_PORT_IN_C = 16'h000E;  //! Table 7-1

  //! Protocol-visible input mapping image. The render map RAM is a physical
  //! projection of this store, not the model itself.
  logic [AMAP_IN_KEYS_C*8-1:0] amap_in_store_r;

  //! WHICH OBJECT WE ARE ALLOWED TO ANSWER FOR - the counters-face rule
  //! restated: a port or page this fabric has no context for answers an
  //! EMPTY page (number_of_mappings 0, zero records), never another
  //! object's data. number_of_maps 0 for an unknown port is what lets the
  //! processor agree with its descriptor store instead of this guard.
  //! REGISTERED ANSWER SERVER - same cut as the counters face above (the
  //! v48 -1.7 ns cone): selectors register in, the page walks below compute
  //! from the registered copy, the answer lands in a register, wait holds
  //! two cycles per beat under the face's own HOLD contract.
  logic [15:0] amapq_type_r, amapq_index_r, amapq_map_r;
  logic  [1:0] amapq_sel_r;
  logic  [7:0] amapq_rec_r;
  logic [63:0] amap_data_r;
  logic [63:0] amap_ans_raw_w;  //! written by the amap_answer comb block
  wire amap_sel_match_w = (amapq_type_r  == pp_amap_desc_type_w)
                       && (amapq_index_r == pp_amap_desc_index_w)
                       && (amapq_map_r   == pp_amap_map_index_w)
                       && (amapq_sel_r   == pp_amap_sel_w)
                       && (amapq_rec_r   == pp_amap_rec_w);
  //! SEQUENTIAL page walk (v48b verdict: the 8-slot combinational scans -
  //! eight parallel indexed reads of the flat map exports - were the
  //! worst path at WNS -1.3 all by themselves; registering the selectors
  //! in front changed nothing about the scan's own depth). One slot per
  //! cycle under the face's hold: per-cycle logic is ONE indexed read plus
  //! an increment, and a beat costs ten cycles against ms-scale commands.
  localparam int AMAP_OUT_KEYS_C = N_STREAMS * 8;
  localparam int AMAP_OUT_KEY_W_C = (AMAP_OUT_KEYS_C <= 2)
                                   ? 1 : $clog2(AMAP_OUT_KEYS_C);
  localparam int AMAP_WALK_W_C = (AMAP_OUT_KEYS_C <= 2)
                                ? 1 : $clog2(AMAP_OUT_KEYS_C + 1);
  logic [AMAP_WALK_W_C-1:0] amap_walk_j_r;  //! stage-A slot cursor
  logic [AMAP_WALK_W_C-1:0] amap_walk_jq_r; //! stage-B cursor (one behind)
  logic        amap_stageb_v_r;    //! stage B holds a valid entry
  logic [7:0]  amap_in_ent_q_r;    //! stage-A registered render-map entry
  logic [12:0] amap_out_ent_q_r;   //! stage-A registered capture-map entry
  logic        amap_out_owner_v_q_r;
  logic [15:0] amap_out_owner_q_r;
  logic [15:0] amap_out_cluster_q_r;
  logic        amap_done_r;
  logic [7:0]  amap_seen_r;
  logic [15:0] amap_cnt_r;
  logic [63:0] amap_rec_r2;
  //! amap_in_ent_w: the stage-A render-map entry, declared ahead of the
  //! amap_answer_srv pipeline, its first reader (#193); driven by
  //! amap_page_slot below.
  logic [7:0] amap_in_ent_w;
  //! amap_out_ent_w/amap_out_owner_v_w/amap_out_owner_w/amap_out_cluster_w:
  //! the stage-A capture-map entry terms, declared ahead of
  //! amap_answer_srv, their first reader (#193); driven by amap_out_slot
  //! below.
  logic [12:0] amap_out_ent_w;
  logic        amap_out_owner_v_w;
  logic [15:0] amap_out_owner_w;
  logic [15:0] amap_out_cluster_w;
  //! amap_slot_hit_w/amap_slot_rec_w: the direction select the sequential
  //! accumulator consumes, declared ahead of amap_answer_srv, their first
  //! reader (#193); the expressions stay below, past the terms they read.
  wire        amap_slot_hit_w;
  wire [63:0] amap_slot_rec_w;
  //! amap_spo_w: the STREAM_PORT_OUTPUT selector, declared ahead of
  //! amap_answer_srv, its first reader (#193); the expression stays below
  //! with the OUTPUT-half constants it reads.
  wire amap_spo_w;
  always_ff @(posedge axis_clk or negedge axis_resetn) begin : amap_answer_srv
    if (!axis_resetn) begin
      amapq_type_r <= 16'd0; amapq_index_r <= 16'd0; amapq_map_r <= 16'd0;
      amapq_sel_r  <= 2'd0;  amapq_rec_r   <= 8'd0;
      amap_walk_j_r <= '0; amap_walk_jq_r <= '0; amap_done_r <= 1'b0;
      amap_stageb_v_r <= 1'b0; amap_in_ent_q_r <= 8'd0; amap_out_ent_q_r <= 13'd0;
      amap_out_owner_v_q_r <= 1'b0; amap_out_owner_q_r <= 16'd0;
      amap_out_cluster_q_r <= 16'd0;
      amap_seen_r <= 8'd0; amap_cnt_r <= 16'd0; amap_rec_r2 <= 64'd0;
      amap_data_r <= 64'd0;
    end else begin
      amapq_type_r  <= pp_amap_desc_type_w;
      amapq_index_r <= pp_amap_desc_index_w;
      amapq_map_r   <= pp_amap_map_index_w;
      amapq_sel_r   <= pp_amap_sel_w;
      amapq_rec_r   <= pp_amap_rec_w;
      if (!amap_sel_match_w) begin
        //! a fresh beat restarts the walk against the newly latched selector
        amap_walk_j_r <= '0;
        amap_walk_jq_r <= '0;
        amap_stageb_v_r <= 1'b0;
        amap_done_r   <= 1'b0;
        amap_seen_r   <= 8'd0;
        amap_cnt_r    <= 16'd0;
        amap_rec_r2   <= 64'd0;
      end else if (!amap_done_r) begin
        //! two-stage overlapped slot pipeline (v48c verdict: the per-slot
        //! logic alone - the 512-bit indexed read PLUS the resolver, range
        //! compares and record formatting - was still 0.7 ns over). Stage A
        //! registers the RAW entry for slot j; stage B, one cycle behind on
        //! j_q, formats and accumulates from the registered entry. The walk
        //! grows to nine cycles; the per-cycle depth halves.
        amap_in_ent_q_r  <= amap_in_ent_w;
        amap_out_ent_q_r <= amap_out_ent_w;
        amap_out_owner_v_q_r <= amap_out_owner_v_w;
        amap_out_owner_q_r <= amap_out_owner_w;
        amap_out_cluster_q_r <= amap_out_cluster_w;
        amap_walk_jq_r   <= amap_walk_j_r;
        amap_stageb_v_r  <= 1'b1;
        if (amap_stageb_v_r && amap_slot_hit_w) begin
          if (amap_seen_r == amapq_rec_r) amap_rec_r2 <= amap_slot_rec_w;
          amap_seen_r <= amap_seen_r + 8'd1;
          amap_cnt_r  <= amap_cnt_r + 16'd1;
        end
        if (amap_stageb_v_r
            && (((!amap_spo_w)
                 && (32'(amap_walk_jq_r) == AMAP_PAGE_C - 1))
                || (amap_spo_w
                    && (32'(amap_walk_jq_r) == AMAP_OUT_KEYS_C - 1))))
          amap_done_r <= 1'b1;
        if (((!amap_spo_w) && (32'(amap_walk_j_r) < AMAP_PAGE_C))
            || (amap_spo_w && (32'(amap_walk_j_r) < AMAP_OUT_KEYS_C)))
          amap_walk_j_r <= amap_walk_j_r + AMAP_WALK_W_C'(1);
      end else begin
        amap_data_r <= amap_ans_raw_w;
      end
    end
  end
  //! served = walked + one data-register cycle behind it
  logic amap_srv_r;
  always_ff @(posedge axis_clk or negedge axis_resetn) begin : amap_srv_track
    if (!axis_resetn) amap_srv_r <= 1'b0;
    else amap_srv_r <= amap_done_r && amap_sel_match_w;
  end

  logic [6:0] amap_in_pbase_w, amap_in_pcls_w, amap_in_nmaps_w;
  always_comb begin : amap_in_port_shape
    amap_in_pbase_w = 7'd0;
    amap_in_pcls_w = 7'd0;
    amap_in_nmaps_w = 7'd0;
    for (int p = 0; p < AMAP_IN_PORTS_C; p++) begin
      if (amapq_index_r == 16'(p)) begin
        amap_in_pbase_w = ADP_DMAP_IN_PBASE_C[p];
        amap_in_pcls_w = ADP_DMAP_IN_PCLS_C[p];
        amap_in_nmaps_w = ADP_DMAP_IN_PNMAPS_C[p];
      end
    end
  end : amap_in_port_shape

  wire amap_spi_w = (amapq_type_r == DESC_STREAM_PORT_IN_C)
                 && (32'(amapq_index_r) < AMAP_IN_PORTS_C)
                 && (amapq_index_r < 16'd64)
                 && ADP_DMAP_IN_MASK_C[amapq_index_r[5:0]];
  wire amap_page_ok_w = amap_spi_w
                     && (32'(amapq_map_r) < 32'(amap_in_nmaps_w));

  //! the page walk, combinational over the flat map export: page P covers
  //! port-relative offsets [P*PAGE, min((P+1)*PAGE, clusters)); the generated
  //! base translates that offset into the model's global cluster key.
  //! At most PAGE (<= 8) candidate slots, so the popcount and the k-th
  //! select are a handful of LUTs, and the answer never holds the beat.
  //! per-slot terms of the SEQUENTIAL walk: slot j of the queried page,
  //! one indexed read per cycle (the whole point of the sequential form)
  //! stage A of the slot pipeline: the ADDRESS MATH and the 512-bit
  //! indexed read, nothing else - the result registers into
  //! amap_in_ent_q_r and stage B consumes it a cycle later
  //! (amap_in_ent_w is declared above amap_answer_srv, its first
  //! reader, #193)
  always_comb begin : amap_page_slot
    int unsigned off_c, g_c;
    off_c = (amap_page_ok_w ? 32'(amapq_map_r) : 32'd0)
            * AMAP_PAGE_C + 32'(amap_walk_j_r);
    g_c   = 32'(amap_in_pbase_w) + off_c;
    //! A slot outside the page, port or protocol store reads as
    //! UNMAPPED - its en bit is 0, so stage B cannot count or match it
    amap_in_ent_w = (amap_page_ok_w && (32'(amap_walk_j_r) < AMAP_PAGE_C)
                     && (off_c < 32'(amap_in_pcls_w))
                     && (g_c < AMAP_IN_KEYS_C))
                    ? amap_in_store_r[g_c*8 +: 8] : 8'd0;
  end : amap_page_slot

  //! stage B: hit + record formatting from the REGISTERED entry and the
  //! stage-B cursor. en && !src: an AVB listener mapping (the banner above)
  logic        amap_in_hit_w;
  logic [63:0] amap_in_rec_w;
  always_comb begin : amap_page_fmt
    int unsigned offq_c;
    amap_in_hit_w = 1'b0;
    amap_in_rec_w = 64'd0;
    offq_c = (amap_page_ok_w ? 32'(amapq_map_r) : 32'd0)
             * AMAP_PAGE_C + 32'(amap_walk_jq_r);
    if (amap_in_ent_q_r[7] && !amap_in_ent_q_r[6]) begin
      amap_in_hit_w = 1'b1;
      amap_in_rec_w = {13'd0, amap_in_ent_q_r[5:3], // mapping_stream_index
                       13'd0, amap_in_ent_q_r[2:0], // mapping_stream_channel
                       16'(offq_c),                 // mapping_cluster_offset
                       16'd0};                      // mapping_cluster_channel
    end
  end : amap_page_fmt

  //! Output mappings need one fixed subset because a Stream Output has at
  //! most eight audio channels (the OUTPUT half of the answer is below);
  //! declared ahead of amap_answer, its first reader, because Vivado's
  //! front-end rejects a constant used before its declaration (#193).
  localparam int AMAP_OUT_NMAPS_C = 1;

  //! amap_opage_ok_w belongs to the OUTPUT half below; it is declared
  //! here because amap_answer is its first reader (#193).
  wire amap_opage_ok_w = amap_spo_w
                      && (amapq_map_r == 16'd0);
  always_comb begin : amap_answer
    unique case (amapq_sel_r)
      2'd0:    amap_ans_raw_w = {48'd0,
                                 amap_spi_w ? {9'd0, amap_in_nmaps_w}
                               : amap_spo_w ? 16'(AMAP_OUT_NMAPS_C)
                                            : 16'd0};
      2'd1:    amap_ans_raw_w = {32'd0,
                                 amap_spi_w ? {9'd0, amap_in_nmaps_w}
                               : amap_spo_w ? 16'(AMAP_OUT_NMAPS_C) : 16'd0,
                                 (amap_page_ok_w || amap_opage_ok_w)
                                   ? amap_cnt_r : 16'd0};
      2'd2:    amap_ans_raw_w = (amap_page_ok_w || amap_opage_ok_w)
                                   ? amap_rec_r2 : 64'd0;
      default: amap_ans_raw_w = 64'd0;
    endcase
  end : amap_answer
  //! ---- the OUTPUT half of the same answer (Milan 5.4.2.26's second
  //! sentence: "for each Stream Port Output of the currently set
  //! Configuration"). The capture-side RAM is STREAM-channel indexed while
  //! the command names a port-relative cluster. The generated CSRC table is
  //! the exact bridge between those coordinate systems and is emitted from
  //! the same role pools as the descriptor image. Output mappings need one
  //! fixed subset because a Stream Output has at most eight audio channels.
  localparam int AMAP_OUT_PORTS_C = ADP_DMAP_OUT_NPORTS_C;
  localparam logic [15:0] DESC_STREAM_PORT_OUT_C = 16'h000F;

  //! (amap_spo_w is declared above amap_answer_srv, its first reader, #193)
  assign amap_spo_w = (amapq_type_r == DESC_STREAM_PORT_OUT_C)
                   && (32'(amapq_index_r) < AMAP_OUT_PORTS_C)
                   && (amapq_index_r < 16'd64)
                   && ADP_DMAP_OUT_MASK_C[amapq_index_r[5:0]];
  //! (amap_opage_ok_w is declared above amap_answer, its first reader, #193)

  //! Resolve a vendor CSR write back into the addressed output port's AEM
  //! cluster coordinate. Transactional AECP writes already carry that
  //! coordinate and store it directly. The first exact CSRC match wins;
  //! disabled fabric templates cannot be inferred from a live CSR word.
  function automatic logic [16:0] amap_out_cluster(
      input logic [12:0] e, input logic [15:0] port_i);
    logic [16:0] r;
    begin
      r = 17'd0;
      for (int p = 0; p < AMAP_OUT_PORTS_C; p++) begin
        if (port_i == 16'(p)) begin
          for (int c = 0; c < ADP_DMAP_OUT_NSRC_C; c++) begin
            if (!r[16]
                && (c >= 32'(ADP_DMAP_OUT_PCBASE_C[p]))
                && (c < (32'(ADP_DMAP_OUT_PCBASE_C[p])
                         + 32'(ADP_DMAP_OUT_PCLS_C[p])))
                && e[12] && (ADP_DMAP_OUT_CSRC_C[c] == e))
              r = {1'b1, 16'(c - 32'(ADP_DMAP_OUT_PCBASE_C[p]))};
          end
        end
      end
      amap_out_cluster = r;
    end
  endfunction

  //! page walk over the port's 8 stream channels: a record exists where the
  //! entry is enabled, its source resolves to a cluster, and that cluster
  //! falls inside the queried page - 7.4.44.2.1 read back off live routing
  //! per-slot terms of the OUTPUT walk, same sequential form
  //! stage A, output side: the 13-bit indexed read only
  //! (amap_out_ent_w, amap_out_owner_v_w, amap_out_owner_w and
  //! amap_out_cluster_w are declared above amap_answer_srv, their first
  //! reader, #193)
  always_comb begin : amap_out_slot
    amap_out_ent_w = (amap_opage_ok_w
             && (32'(amap_walk_j_r) < AMAP_OUT_KEYS_C))
            ? cmap_flat_w[32'(amap_walk_j_r) * 13 +: 13]
            : 13'd0;
    amap_out_owner_v_w = (amap_opage_ok_w
                           && (32'(amap_walk_j_r) < AMAP_OUT_KEYS_C))
                          ? amap_out_owner_v_r[
                              amap_walk_j_r[AMAP_OUT_KEY_W_C-1:0]] : 1'b0;
    amap_out_owner_w = (amap_opage_ok_w
                        && (32'(amap_walk_j_r) < AMAP_OUT_KEYS_C))
                       ? amap_out_owner_r[32'(amap_walk_j_r) * 16 +: 16]
                       : 16'd0;
    amap_out_cluster_w = (amap_opage_ok_w
                          && (32'(amap_walk_j_r) < AMAP_OUT_KEYS_C))
                         ? amap_out_cluster_r[32'(amap_walk_j_r) * 16 +: 16]
                         : 16'd0;
  end : amap_out_slot

  //! stage B, output side: resolver + page range + record, off the
  //! registered entry and the stage-B cursor
  logic        amap_out_hit_w;
  logic [63:0] amap_out_rec_w;
  always_comb begin : amap_out_fmt
    logic port_cluster_ok_c;
    amap_out_hit_w = 1'b0;
    amap_out_rec_w = 64'd0;
    port_cluster_ok_c = 1'b0;
    for (int p = 0; p < AMAP_OUT_PORTS_C; p++) begin
      if ((amapq_index_r == 16'(p))
          && (32'(amap_out_cluster_q_r)
              < 32'(ADP_DMAP_OUT_PCLS_C[p])))
        port_cluster_ok_c = 1'b1;
    end
    if (amap_out_owner_v_q_r && (amap_out_owner_q_r == amapq_index_r)
        && port_cluster_ok_c) begin
      amap_out_hit_w = 1'b1;
      amap_out_rec_w = {16'(32'(amap_walk_jq_r) / 8), // stream_index
                        16'(32'(amap_walk_jq_r) % 8), // stream_channel
                        amap_out_cluster_q_r,    // cluster_offset
                        16'd0};                  // cluster_channel
    end
  end : amap_out_fmt

  //! the direction select the sequential accumulator consumes
  //! (both nets are declared above amap_answer_srv, their first reader, #193)
  assign      amap_slot_hit_w = amap_spi_w ? amap_in_hit_w
                              : amap_spo_w ? amap_out_hit_w : 1'b0;
  assign      amap_slot_rec_w = amap_spi_w ? amap_in_rec_w : amap_out_rec_w;

  //! HOLD, not a ready - combinational flops again, never held
  assign pp_amap_data_w = amap_data_r;
  assign pp_amap_wait_w = pp_amap_req_w && !(amap_srv_r && amap_sel_match_w);  //! live-match: see the counters face

  //! ======================================================================
  //! ADD/REMOVE_AUDIO_MAPPINGS transaction server
  //! ======================================================================
  //! Every record is checked against the live map and the command-local
  //! claims before any phase-5 write is possible. The claim vectors model
  //! the command's final value at each routing key. They catch two records
  //! that assign one key differently and also make duplicate REMOVE records
  //! idempotent without treating an unrelated absent mapping as present.
  //!
  //! The CSR debug writer is held out while amap_edit_txn_active_r is set.
  //! This freezes the live baseline between the validation and commit passes,
  //! so a concurrent CSR write cannot create a time-of-check/time-of-use partial edit.
  //! Phase 1 rechecks that baseline and reserves the complete commit. This
  //! root never asserts wait, so phases 5 and 2 complete without a timeout
  //! point between live writes.
  logic        amap_edit_seen_r;
  logic  [2:0] amap_edit_seen_phase_r;
  logic  [7:0] amap_edit_seen_rec_r;
  logic        amap_edit_remove_r;
  logic [15:0] amap_edit_type_r, amap_edit_index_r, amap_edit_count_r;
  logic        amap_edit_changed_r;
  logic [AMAP_IN_KEYS_C-1:0] amap_edit_iclaim_v_r;
  logic [AMAP_IN_KEYS_C*8-1:0] amap_edit_iclaim_word_r;
  logic [AMAP_IN_KEYS_C*8-1:0] amap_edit_iclaim_expect_r;
  logic [N_STREAMS*8-1:0] amap_edit_oclaim_v_r;
  logic [N_STREAMS*8*13-1:0] amap_edit_oclaim_word_r;
  logic [N_STREAMS*8*13-1:0] amap_edit_oclaim_expect_r;
  logic [N_STREAMS*8*16-1:0] amap_edit_oclaim_cluster_r;
  wire [N_STREAMS-1:0] amap_edit_out_claim_stream_w;
  for (genvar ar = 0; ar < N_STREAMS; ar++) begin : g_amap_edit_resv
    assign amap_edit_out_claim_stream_w[ar] =
        |amap_edit_oclaim_v_r[ar*8 +: 8];
  end

  wire [15:0] amap_edit_si_w = pp_amap_edit_record_w[63:48];
  wire [15:0] amap_edit_sc_w = pp_amap_edit_record_w[47:32];
  wire [15:0] amap_edit_co_w = pp_amap_edit_record_w[31:16];
  wire [15:0] amap_edit_cc_w = pp_amap_edit_record_w[15:0];

  //! Convert one port-relative cluster into the exact capture-source word
  //! generated beside the AEM descriptor geometry. Every cluster inside the
  //! published port geometry is a legal protocol mapping target. CSRC bit 12
  //! remains the separate live-fabric enable, so a mapping can be stored and
  //! read back even when this build does not elaborate its media source.
  function automatic logic [13:0] amap_edit_out_encode(
      input logic [15:0] off_i, input logic [15:0] port_i);
    logic [13:0] r;
    begin
      r = 14'd0;
      for (int p = 0; p < AMAP_OUT_PORTS_C; p++) begin
        if ((port_i == 16'(p))
            && (32'(off_i) < 32'(ADP_DMAP_OUT_PCLS_C[p]))) begin
          for (int c = 0; c < ADP_DMAP_OUT_NSRC_C; c++) begin
            if (c == (32'(ADP_DMAP_OUT_PCBASE_C[p]) + 32'(off_i)))
              r = {1'b1, ADP_DMAP_OUT_CSRC_C[c]};
          end
        end
      end
      amap_edit_out_encode = r;
    end
  endfunction

  logic        amap_edit_context_w, amap_edit_dynamic_w;
  logic        amap_edit_commit_ok_w;
  logic        amap_edit_accept_w, amap_edit_in_key_v_w, amap_edit_out_key_v_w;
  logic [AMAP_IN_KEY_W_C-1:0]  amap_edit_in_key_w;
  logic [AMAP_OUT_KEY_W_C-1:0] amap_edit_out_key_w;
  logic  [7:0] amap_edit_in_word_w, amap_edit_in_live_w;
  logic [12:0] amap_edit_out_word_w, amap_edit_out_live_w;
  logic        amap_edit_out_owner_v_w;
  logic [15:0] amap_edit_out_owner_w;
  logic [15:0] amap_edit_out_cluster_w;
  logic [13:0] amap_edit_out_enc_w;

  always_comb begin : amap_edit_validate
    int unsigned ikey_c, okey_c, ipbase_c, ipcls_c;
    logic [7:0] ibase_c, iexpect_c;
    logic [12:0] obase_c, oexpect_c;
    logic [15:0] obase_cluster_c;
    logic istream_ok_c, ostream_ok_c, ostreaming_c;
    logic iclaim_c, oclaim_c;

    pp_amap_edit_data_w = 64'd0;
    amap_edit_dynamic_w = 1'b0;
    amap_edit_context_w = amap_edit_txn_active_r
                          && (pp_amap_edit_remove_w == amap_edit_remove_r)
                          && (pp_amap_edit_desc_type_w == amap_edit_type_r)
                          && (pp_amap_edit_desc_index_w == amap_edit_index_r)
                          && (pp_amap_edit_count_w == amap_edit_count_r);
    amap_edit_commit_ok_w = amap_edit_context_w;
    if (pp_amap_edit_desc_type_w == DESC_STREAM_PORT_OUT_C) begin
      amap_edit_commit_ok_w = amap_edit_context_w
                              && (32'(pp_amap_edit_desc_index_w)
                                  < AMAP_OUT_PORTS_C);
      for (int k = 0; k < N_STREAMS*8; k++) begin
        if (amap_edit_oclaim_v_r[k]
            && tkd_streaming_w[k/8])
          amap_edit_commit_ok_w = 1'b0;
      end
    end
    amap_edit_accept_w = 1'b0;
    amap_edit_in_key_v_w = 1'b0;
    amap_edit_out_key_v_w = 1'b0;
    amap_edit_in_key_w = '0;
    amap_edit_out_key_w = '0;
    amap_edit_in_word_w = {1'b1, 1'b0, amap_edit_si_w[2:0],
                           amap_edit_sc_w[2:0]};
    amap_edit_out_enc_w = amap_edit_out_encode(amap_edit_co_w,
                                                pp_amap_edit_desc_index_w);
    amap_edit_out_word_w = amap_edit_out_enc_w[12:0];
    amap_edit_in_live_w = 8'd0;
    amap_edit_out_live_w = 13'd0;
    amap_edit_out_owner_v_w = 1'b0;
    amap_edit_out_owner_w = 16'd0;
    amap_edit_out_cluster_w = 16'd0;
    ikey_c = 0;
    okey_c = 0;
    ipbase_c = 0;
    ipcls_c = 0;
    ibase_c = 8'd0;
    iexpect_c = 8'd0;
    obase_c = 13'd0;
    oexpect_c = 13'd0;
    obase_cluster_c = 16'd0;
    istream_ok_c = 1'b0;
    ostream_ok_c = 1'b0;
    ostreaming_c = 1'b0;
    iclaim_c = 1'b0;
    oclaim_c = 1'b0;

    for (int p = 0; p < AMAP_IN_PORTS_C; p++) begin
      if (pp_amap_edit_desc_index_w == 16'(p)) begin
        ipbase_c = 32'(ADP_DMAP_IN_PBASE_C[p]);
        ipcls_c = 32'(ADP_DMAP_IN_PCLS_C[p]);
      end
    end
    //! TWO bounds per record since issue #67, and the record needs both:
    //! the GENERATED wire shape (a channel the fabric cannot carry is
    //! never mappable, whatever a format claims) AND the stream's CURRENT
    //! format through the settings fold - IEEE §7.4.45.2 bounds
    //! mapping_stream_channel by "the stream format currently set", and
    //! without this term a SET_STREAM_FORMAT to 2ch followed by an ADD of
    //! channel 3 would reach exactly the orphaned state the verdict's
    //! survives bit exists to refuse in the other order.
    for (int s = 0; s < ADP_DMAP_IN_NSTRIN_C; s++) begin
      if ((amap_edit_si_w == 16'(s)) && ADP_DMAP_IN_SAAF_C[s]
          && (32'(amap_edit_sc_w) < 32'(ADP_DMAP_IN_SCH_C[s]))
          && ((s >= ACMP_SINKS_C) || !pp_aecp_fmt_in_v_w[s]
              || (32'(amap_edit_sc_w)
                  < 32'(pp_aecp_fmt_in_w[64*s + 22 +: 10]))))
        istream_ok_c = 1'b1;
    end
    for (int s = 0; s < AMAP_OUT_PORTS_C; s++) begin
      if ((amap_edit_si_w == 16'(s))
          && (32'(amap_edit_sc_w) < 32'(ADP_DMAP_OUT_SCH_C[s]))
          && ((s >= ACMP_SRC_C) || !pp_aecp_fmt_out_v_w[s]
              || (32'(amap_edit_sc_w)
                  < 32'(pp_aecp_fmt_out_w[64*s + 22 +: 10]))))
        ostream_ok_c = 1'b1;
    end
    for (int s = 0; s < N_STREAMS; s++) begin
      if (amap_edit_si_w == 16'(s))
        ostreaming_c = tkd_streaming_w[s];
    end

    if ((pp_amap_edit_desc_type_w == DESC_STREAM_PORT_IN_C)
        && (32'(pp_amap_edit_desc_index_w) < AMAP_IN_PORTS_C)
        && (pp_amap_edit_desc_index_w < 16'd64)) begin
      amap_edit_dynamic_w =
          ADP_DMAP_IN_MASK_C[pp_amap_edit_desc_index_w[5:0]];
    end else if ((pp_amap_edit_desc_type_w == DESC_STREAM_PORT_OUT_C)
                 && (32'(pp_amap_edit_desc_index_w) < AMAP_OUT_PORTS_C)
                 && (pp_amap_edit_desc_index_w < 16'd64)) begin
      amap_edit_dynamic_w =
          ADP_DMAP_OUT_MASK_C[pp_amap_edit_desc_index_w[5:0]];
    end

    if ((pp_amap_edit_desc_type_w == DESC_STREAM_PORT_IN_C)
        && amap_edit_dynamic_w && (amap_edit_cc_w == 16'd0)
        && (32'(amap_edit_co_w) < ipcls_c)
        && istream_ok_c
        && (amap_edit_si_w < 16'd8) && (amap_edit_sc_w < 16'd8)) begin
      ikey_c = ipbase_c + 32'(amap_edit_co_w);
      if (ikey_c < AMAP_IN_KEYS_C) begin
        amap_edit_in_key_v_w = 1'b1;
        amap_edit_in_key_w = AMAP_IN_KEY_W_C'(ikey_c);
        amap_edit_in_live_w = amap_in_store_r[ikey_c*8 +: 8];
        iclaim_c = amap_edit_iclaim_v_r[ikey_c];
        ibase_c = iclaim_c ? amap_edit_iclaim_word_r[ikey_c*8 +: 8]
                           : amap_in_store_r[ikey_c*8 +: 8];
        iexpect_c = amap_edit_iclaim_expect_r[ikey_c*8 +: 8];
        if (!pp_amap_edit_remove_w)
          amap_edit_accept_w = iclaim_c
                               ? (ibase_c == amap_edit_in_word_w)
                               : (!ibase_c[7]
                                  || (ibase_c == amap_edit_in_word_w));
        else
          amap_edit_accept_w = iclaim_c
                               ? ((ibase_c == 8'd0)
                                  && (iexpect_c == amap_edit_in_word_w))
                               : (ibase_c == amap_edit_in_word_w);
      end
    end else if ((pp_amap_edit_desc_type_w == DESC_STREAM_PORT_OUT_C)
                 && amap_edit_dynamic_w && amap_edit_out_enc_w[13]
                 && (amap_edit_cc_w == 16'd0)
                 && (32'(amap_edit_si_w) < N_STREAMS)
                 && (amap_edit_sc_w < 16'd8) && ostream_ok_c) begin
      okey_c = 32'(amap_edit_si_w) * 8 + 32'(amap_edit_sc_w);
      if (okey_c < N_STREAMS*8) begin
        amap_edit_out_key_v_w = 1'b1;
        amap_edit_out_key_w = AMAP_OUT_KEY_W_C'(okey_c);
        amap_edit_out_live_w = cmap_flat_w[okey_c*13 +: 13];
        amap_edit_out_owner_v_w = amap_out_owner_v_r[okey_c];
        amap_edit_out_owner_w = amap_out_owner_r[okey_c*16 +: 16];
        amap_edit_out_cluster_w = amap_out_cluster_r[okey_c*16 +: 16];
        oclaim_c = amap_edit_oclaim_v_r[okey_c];
        obase_c = oclaim_c ? amap_edit_oclaim_word_r[okey_c*13 +: 13]
                           : cmap_flat_w[okey_c*13 +: 13];
        obase_cluster_c = oclaim_c
                          ? amap_edit_oclaim_cluster_r[okey_c*16 +: 16]
                          : amap_out_cluster_r[okey_c*16 +: 16];
        oexpect_c = amap_edit_oclaim_expect_r[okey_c*13 +: 13];
        if (!pp_amap_edit_remove_w)
          amap_edit_accept_w = !ostreaming_c
                               && (oclaim_c
                               ? ((obase_c == amap_edit_out_word_w)
                                  && (obase_cluster_c == amap_edit_co_w))
                               : (!amap_edit_out_owner_v_w
                                  || (amap_edit_out_owner_v_w
                                      && (amap_edit_out_owner_w
                                          == pp_amap_edit_desc_index_w)
                                      && (amap_edit_out_cluster_w
                                          == amap_edit_co_w)
                                      && (obase_c == amap_edit_out_word_w))));
        else
          amap_edit_accept_w = !ostreaming_c
                               && (oclaim_c
                               ? ((obase_c == 13'd0)
                                  && (oexpect_c == amap_edit_out_word_w)
                                  && (obase_cluster_c == amap_edit_co_w))
                               : (amap_edit_out_owner_v_w
                                  && (amap_edit_out_owner_w
                                      == pp_amap_edit_desc_index_w)
                                  && (amap_edit_out_cluster_w
                                      == amap_edit_co_w)
                                  && (obase_c == amap_edit_out_word_w)));
      end
    end

    unique case (pp_amap_edit_phase_w)
      3'd0: pp_amap_edit_data_w[0] = amap_edit_dynamic_w;
      3'd1: pp_amap_edit_data_w[0] = amap_edit_commit_ok_w;
      3'd2: pp_amap_edit_data_w[0] = amap_edit_context_w
                                            && amap_edit_changed_r;
      3'd3: pp_amap_edit_data_w[0] = 1'b1;
      3'd4: pp_amap_edit_data_w[0] = amap_edit_context_w
                                            && (pp_amap_edit_rec_w
                                                < amap_edit_count_r[7:0])
                                            && amap_edit_accept_w;
      3'd5: pp_amap_edit_data_w[0] = amap_edit_context_w;
      default: pp_amap_edit_data_w = 64'd0;
    endcase
  end : amap_edit_validate

  assign pp_amap_edit_wait_w = 1'b0;

  wire [12:0] cfg_cmap_entry_w = {cfg_chmap_wr_data[15],
                                   cfg_chmap_wr_data[8],
                                   cfg_chmap_wr_data[14:12],
                                   cfg_chmap_wr_data[7:4],
                                   cfg_chmap_wr_data[3:0]};
  wire [15:0] cfg_cmap_port_w = 16'(32'(cfg_chmap_wr_addr) / 8);
  wire [16:0] cfg_cmap_cluster_w = amap_out_cluster(cfg_cmap_entry_w,
                                                    cfg_cmap_port_w);

  always_ff @(posedge axis_clk or negedge axis_resetn) begin : amap_edit_commit
    if (!axis_resetn) begin
      amap_edit_seen_r <= 1'b0;
      amap_edit_seen_phase_r <= 3'd0;
      amap_edit_seen_rec_r <= 8'd0;
      amap_edit_txn_active_r <= 1'b0;
      amap_edit_remove_r <= 1'b0;
      amap_edit_type_r <= 16'd0;
      amap_edit_index_r <= 16'd0;
      amap_edit_count_r <= 16'd0;
      amap_edit_changed_r <= 1'b0;
      amap_edit_iclaim_v_r <= '0;
      amap_edit_iclaim_word_r <= '0;
      amap_edit_iclaim_expect_r <= '0;
      amap_edit_oclaim_v_r <= '0;
      amap_edit_oclaim_word_r <= '0;
      amap_edit_oclaim_expect_r <= '0;
      amap_edit_oclaim_cluster_r <= '0;
      amap_edit_out_resv_r <= '0;
      amap_in_store_r <= '0;
      amap_out_owner_v_r <= '0;
      amap_out_owner_r <= '0;
      amap_out_cluster_r <= '0;
      amap_edit_iwr_p_r <= 1'b0;
      amap_edit_iwr_addr_r <= 6'd0;
      amap_edit_iwr_word_r <= 8'd0;
      amap_edit_owr_p_r <= 1'b0;
      amap_edit_owr_slot_r <= 6'd0;
      amap_edit_owr_word_r <= 13'd0;
    end else begin
      amap_edit_iwr_p_r <= 1'b0;
      amap_edit_owr_p_r <= 1'b0;
      if (!pp_amap_edit_req_w) begin
        amap_edit_seen_r <= 1'b0;
      end else if (!amap_edit_seen_r
                   || (amap_edit_seen_phase_r != pp_amap_edit_phase_w)
                   || (amap_edit_seen_rec_r != pp_amap_edit_rec_w)) begin
        amap_edit_seen_r <= 1'b1;
        amap_edit_seen_phase_r <= pp_amap_edit_phase_w;
        amap_edit_seen_rec_r <= pp_amap_edit_rec_w;
        unique case (pp_amap_edit_phase_w)
          3'd0: begin
            amap_edit_txn_active_r <= amap_edit_dynamic_w;
            amap_edit_remove_r <= pp_amap_edit_remove_w;
            amap_edit_type_r <= pp_amap_edit_desc_type_w;
            amap_edit_index_r <= pp_amap_edit_desc_index_w;
            amap_edit_count_r <= pp_amap_edit_count_w;
            amap_edit_changed_r <= 1'b0;
            amap_edit_iclaim_v_r <= '0;
            amap_edit_iclaim_word_r <= '0;
            amap_edit_iclaim_expect_r <= '0;
            amap_edit_oclaim_v_r <= '0;
            amap_edit_oclaim_word_r <= '0;
            amap_edit_oclaim_expect_r <= '0;
            amap_edit_oclaim_cluster_r <= '0;
            amap_edit_out_resv_r <= '0;
          end
          3'd1: begin
            if (amap_edit_commit_ok_w
                && (amap_edit_type_r == DESC_STREAM_PORT_OUT_C))
              amap_edit_out_resv_r <= amap_edit_out_claim_stream_w;
            else
              amap_edit_out_resv_r <= '0;
          end
          3'd2, 3'd3: begin
            amap_edit_txn_active_r <= 1'b0;
            amap_edit_out_resv_r <= '0;
          end
          3'd4: begin
            if (amap_edit_context_w && amap_edit_accept_w
                && (pp_amap_edit_rec_w < amap_edit_count_r[7:0])) begin
              if (amap_edit_in_key_v_w
                  && !amap_edit_iclaim_v_r[amap_edit_in_key_w]) begin
                amap_edit_iclaim_v_r[amap_edit_in_key_w] <= 1'b1;
                amap_edit_iclaim_expect_r[amap_edit_in_key_w*8 +: 8]
                  <= amap_edit_in_word_w;
                amap_edit_iclaim_word_r[amap_edit_in_key_w*8 +: 8]
                  <= amap_edit_remove_r ? 8'd0 : amap_edit_in_word_w;
              end else if (amap_edit_out_key_v_w
                           && !amap_edit_oclaim_v_r[amap_edit_out_key_w]) begin
                amap_edit_oclaim_v_r[amap_edit_out_key_w] <= 1'b1;
                amap_edit_oclaim_expect_r[amap_edit_out_key_w*13 +: 13]
                  <= amap_edit_out_word_w;
                amap_edit_oclaim_word_r[amap_edit_out_key_w*13 +: 13]
                  <= amap_edit_remove_r ? 13'd0 : amap_edit_out_word_w;
                amap_edit_oclaim_cluster_r[
                  amap_edit_out_key_w*16 +: 16] <= amap_edit_co_w;
              end
            end
          end
          3'd5: begin
            if (amap_edit_context_w && amap_edit_in_key_v_w
                && amap_edit_iclaim_v_r[amap_edit_in_key_w]
                && (amap_edit_in_live_w
                    != amap_edit_iclaim_word_r[amap_edit_in_key_w*8 +: 8])) begin
              amap_in_store_r[amap_edit_in_key_w*8 +: 8]
                <= amap_edit_iclaim_word_r[amap_edit_in_key_w*8 +: 8];
              if (ADP_DMAP_IN_RPHYS_C[amap_edit_in_key_w][6]) begin
                amap_edit_iwr_p_r <= 1'b1;
                amap_edit_iwr_addr_r
                  <= ADP_DMAP_IN_RPHYS_C[amap_edit_in_key_w][5:0];
                amap_edit_iwr_word_r
                  <= amap_edit_iclaim_word_r[amap_edit_in_key_w*8 +: 8];
              end
              amap_edit_changed_r <= 1'b1;
            end else if (amap_edit_context_w && amap_edit_out_key_v_w
                         && amap_edit_oclaim_v_r[amap_edit_out_key_w]
                         && ((amap_edit_out_live_w
                              != amap_edit_oclaim_word_r[
                                   amap_edit_out_key_w*13 +: 13])
                             || (amap_edit_out_owner_v_w
                                 != !amap_edit_remove_r)
                             || (!amap_edit_remove_r
                                 && ((amap_edit_out_owner_w
                                      != amap_edit_index_r)
                                     || (amap_edit_out_cluster_w
                                         != amap_edit_oclaim_cluster_r[
                                              amap_edit_out_key_w*16
                                              +: 16]))))) begin
              amap_edit_owr_p_r <= 1'b1;
              amap_edit_owr_slot_r <= 6'(amap_edit_out_key_w);
              amap_edit_owr_word_r
                <= amap_edit_oclaim_word_r[amap_edit_out_key_w*13 +: 13];
              amap_out_owner_v_r[amap_edit_out_key_w]
                <= !amap_edit_remove_r;
              amap_out_owner_r[amap_edit_out_key_w*16 +: 16]
                <= amap_edit_remove_r ? 16'd0 : amap_edit_index_r;
              amap_out_cluster_r[amap_edit_out_key_w*16 +: 16]
                <= amap_edit_remove_r ? 16'd0
                                      : amap_edit_oclaim_cluster_r[
                                          amap_edit_out_key_w*16 +: 16];
              amap_edit_changed_r <= 1'b1;
            end
          end
          default: ;
        endcase
      end
      if (!pp_amap_edit_req_w && !amap_edit_txn_active_r
          && !aecp_locked
          && cfg_chmap_wr_en && cfg_chmap_wr_side
          && (32'(cfg_chmap_wr_addr) < AMAP_OUT_KEYS_C)) begin
        amap_out_owner_v_r[
          cfg_chmap_wr_addr[AMAP_OUT_KEY_W_C-1:0]]
          <= cfg_cmap_cluster_w[16];
        amap_out_owner_r[32'(cfg_chmap_wr_addr)*16 +: 16]
          <= 16'(32'(cfg_chmap_wr_addr) / 8);
        amap_out_cluster_r[32'(cfg_chmap_wr_addr)*16 +: 16]
          <= cfg_cmap_cluster_w[15:0];
      end
      if (!pp_amap_edit_req_w && !amap_edit_txn_active_r
          && !aecp_locked
          && cfg_chmap_wr_en && !cfg_chmap_wr_side
          && (32'(cfg_chmap_wr_addr) < AMAP_IN_KEYS_C)) begin
        amap_in_store_r[32'(cfg_chmap_wr_addr)*8 +: 8]
          <= {cfg_chmap_wr_data[15], cfg_chmap_wr_data[12],
              cfg_chmap_wr_data[6:4], cfg_chmap_wr_data[2:0]};
      end
    end
  end : amap_edit_commit

  //! ==== the Milan-info answer block (06 SS6.2/SS6.10) ====================
  //! GET_STREAM_INFO / GET_AVB_INFO / GET_AS_PATH, one word at a time; the
  //! processor lays the responses out and THIS fabric owns every value and
  //! every validity flag, because the truth lives here: the pp's own
  //! class-D binding view and SRP registrars (read back on the same nets
  //! every other consumer reads), the declared stream identities, the gPTP
  //! CSR pair and the clock-validator's asCapable.
  //!
  //! HONESTY LEDGER (what this face says and why):
  //!  - a sink is SETTLED when it is bound and its settled stream_id is
  //!    nonzero (the binding view latches identity at settle and zeroes it
  //!    at unbind) - while actively probing, pbsta reports PASSIVE (1),
  //!    never ACTIVE, and acmpsta is therefore 0 by Milan 5.3.8.6's own
  //!    "otherwise" arm: the listener's probe-retry detail never leaves the
  //!    processor, and claiming ACTIVE without the matching acmpsta would
  //!    be the invented half of a truth.
  //!  - msrp_failure_bridge_id for a SINK reads 0: the processor exports
  //!    the registered failure CODE but not the bridge id; MSRP_FAILURE_
  //!    VALID still follows the FAILED registration so a controller sees
  //!    the failure, with the code carried and the bridge honestly zero.
  //!  - stream_format at reset is the addressed ROW's generated declared
  //!    format (ADP_STRIN_FMT_C / ADP_STROUT_FMT_C - the config accepts
  //!    independent per-row format lists, so row 0's fact must never
  //!    answer for row k), and a SET_STREAM_FORMAT setting overlays it
  //!    through the processor's published rows.
  //!  - a source's declared DA is the block-allocator law the maap shim
  //!    already applies (blk_addr + source), valid while a claim is held.
  //!  - propagation_delay is the fabric gPTP measurement when that owner is
  //!    present, otherwise zero.
  //!  - GET_AS_PATH answers one coherent selected-owner snapshot. Fabric mode
  //!    serves the engine-selected full bounded PathTrace; option off serves
  //!    an empty sequence.

  //! CLAMPED index widths - a 1-sink shape's 2-bit vectors must never be
  //! part-selected with a wider index (the lint ratchet's own catch)
  localparam int GSI_SNK_W_C = (ACMP_SINKS_C > 1) ? $clog2(ACMP_SINKS_C) : 1;
  localparam int GSI_SRC_W_C = (ACMP_SRC_C  > 1) ? $clog2(ACMP_SRC_C)  : 1;
  wire [3:0]             gsi_ix_w  = pp_gsi_desc_index_w[3:0];
  wire [GSI_SNK_W_C-1:0] gsi_six_w = pp_gsi_desc_index_w[GSI_SNK_W_C-1:0];
  //! REGISTERED ANSWER SERVER - the third face, same v48 cut. The info
  //! flags (Tables 5.9-5.12) and the iterated AVB/path records compute from
  //! REGISTERED selectors into a register; wait holds two cycles per beat.
  logic  [1:0] gsiq_kind_r;
  logic [15:0] gsiq_type_r, gsiq_index_r;
  logic  [3:0] gsiq_sel_r;
  logic  [7:0] gsiq_ord_r;
  logic        gsi_srv1_r, gsi_srv2_r;
  logic [63:0] gsi_data_r;
  logic [63:0] gsi_ans_raw_w;   //! written by the answer comb block below
  //! A GET_AS_PATH response gathers its count and then each entry on separate
  //! requests. Snapshot the complete published path at the first count request
  //! so a concurrent PUBLISH can select the next response but cannot splice
  //! its bytes into one already in flight.
  logic        gsi_req_q_r;
  logic [63:0] asp_resp_gm_r;
  logic [3:0]  asp_resp_count_r;
  logic [7*64-1:0] asp_resp_path_r;
  logic [63:0] gsi_gm_snap_r;
  logic [31:0] gsi_pdelay_snap_r;
  logic  [7:0] gsi_domain_snap_r;
  logic        gsi_link_snap_r, gsi_ascap_snap_r;
  logic  [2:0] gsi_prio_snap_r;
  logic [11:0] gsi_vid_snap_r;
  //! Public to the integration harness so it can place a PUBLISH on the exact
  //! edge between the count capture and the remaining in-flight gathers.
  wire asp_resp_capture_w /* verilator public_flat_rd */ =
       pp_gsi_req_w && !gsi_req_q_r && (pp_gsi_kind_w == 2'd2)
       && (pp_gsi_sel_w == 4'd0);
  wire gsi_avb_capture_w = pp_gsi_req_w && !gsi_req_q_r
       && (pp_gsi_kind_w == 2'd1) && (pp_gsi_sel_w == 4'd0);
  //! The harness watches this independently of TX backpressure. Its in-flight
  //! cut must complete PUBLISH after the count snapshot but before the first
  //! path-entry request, otherwise an all-old response would be a false-green
  //! consequence of publishing after the gather had already finished.
  wire asp_resp_entry_w /* verilator public_flat_rd */ =
       pp_gsi_req_w && (pp_gsi_kind_w == 2'd2) && (pp_gsi_sel_w == 4'd8);
  wire gsi_sel_match_w = (gsiq_kind_r  == pp_gsi_kind_w)
                      && (gsiq_type_r  == pp_gsi_desc_type_w)
                      && (gsiq_index_r == pp_gsi_desc_index_w)
                      && (gsiq_sel_r   == pp_gsi_sel_w)
                      && (gsiq_ord_r   == pp_gsi_ord_w);
  always_ff @(posedge axis_clk or negedge axis_resetn) begin : gsi_answer_srv
    if (!axis_resetn) begin
      gsiq_kind_r <= 2'd0;  gsiq_type_r <= 16'd0; gsiq_index_r <= 16'd0;
      gsiq_sel_r  <= 4'd0;  gsiq_ord_r  <= 8'd0;
      gsi_srv1_r  <= 1'b0;  gsi_srv2_r  <= 1'b0;  gsi_data_r <= 64'd0;
      gsi_req_q_r <= 1'b0;
      asp_resp_gm_r <= 64'd0;
      asp_resp_count_r <= 4'd0;
      asp_resp_path_r <= '0;
      gsi_gm_snap_r     <= 64'd0;
      gsi_pdelay_snap_r <= 32'd0;
      gsi_domain_snap_r <= 8'd0;
      gsi_link_snap_r   <= 1'b0;
      gsi_ascap_snap_r  <= 1'b0;
      gsi_prio_snap_r   <= 3'd0;
      gsi_vid_snap_r    <= 12'd0;
    end else begin
      gsi_req_q_r  <= pp_gsi_req_w;
      gsiq_kind_r  <= pp_gsi_kind_w;
      gsiq_type_r  <= pp_gsi_desc_type_w;
      gsiq_index_r <= pp_gsi_desc_index_w;
      gsiq_sel_r   <= pp_gsi_sel_w;
      gsiq_ord_r   <= pp_gsi_ord_w;
      gsi_srv1_r   <= pp_gsi_req_w && gsi_sel_match_w;
      gsi_srv2_r   <= pp_gsi_req_w && gsi_sel_match_w && gsi_srv1_r;
      gsi_data_r   <= gsi_ans_raw_w;
      if (asp_resp_capture_w) begin
        asp_resp_gm_r    <= asp_live_gm_w;
        asp_resp_count_r <= asp_live_count_w;
        asp_resp_path_r  <= asp_live_path_w;
      end
      if (gsi_avb_capture_w) begin
        gsi_gm_snap_r     <= cfg_adp_gptp_gm;
        gsi_pdelay_snap_r <= eff_gptp_pdelay_w;
        gsi_domain_snap_r <= cfg_adp_gptp_domain;
        gsi_link_snap_r   <= eff_link_w;
        gsi_ascap_snap_r  <= clkv_as_cap_w;
        gsi_prio_snap_r   <= pp_cd_srp_class_a_prio_w;
        gsi_vid_snap_r    <= pp_cd_srp_class_a_vid_w;
      end
    end
  end

  wire [GSI_SRC_W_C-1:0] gsi_oix_w = gsiq_index_r[GSI_SRC_W_C-1:0];
  wire        gsi_in_w   = (gsiq_type_r == 16'h0005)
                           && (32'(gsiq_index_r) < ACMP_SINKS_C);
  wire        gsi_out_w  = (gsiq_type_r == 16'h0006)
                           && (32'(gsiq_index_r) < ACMP_SRC_C);
  wire        gsi_bnd_w  = gsi_in_w && pp_cd_acmp_bound_w[gsi_six_w];
  wire [63:0] gsi_sid_w  = pp_cd_acmp_bound_sid_w[64*gsi_six_w +: 64];
  wire        gsi_setl_w = gsi_bnd_w && (gsi_sid_w != 64'd0);
  wire [1:0]  gsi_tkreg_w = pp_cd_srp_tk_reg_state_w[2*gsi_six_w +: 2];
  wire        gsi_tkfail_w = gsi_in_w && (gsi_tkreg_w == 2'd2);
  wire        gsi_reging_w = gsi_in_w && (gsi_tkreg_w != 2'd0);
  wire        gsi_decl_w  = gsi_out_w && pp_cd_acmp_declaring_w[gsi_oix_w];
  wire [1:0]  gsi_lreg_w  = pp_cd_srp_lstn_reg_state_w[2*gsi_oix_w +: 2];
  wire [1:0]  gsi_tkdcl_w = pp_cd_srp_tk_decl_state_w[2*gsi_oix_w +: 2];
  wire        gsi_oreging_w = gsi_decl_w && (gsi_lreg_w != 2'd0);
  wire        gsi_ofail_w   = gsi_out_w && (gsi_tkdcl_w == 2'd2);

  //! Milan Tables 5.9/5.11 flags + Tables 5.10/5.12 flags_ex, per direction
  logic [31:0] gsi_flags_w, gsi_flags_ex_w;
  //! pp_aecp_strm_started_w belongs to the KL_pp_shadow face below; it
  //! is declared here because gsi_flag_law is its first reader (#193).
  logic [ACMP_SINKS_C-1:0]  pp_aecp_strm_started_w;
  always_comb begin : gsi_flag_law
    gsi_flags_w    = 32'd0;
    gsi_flags_ex_w = 32'd0;
    if (gsi_in_w) begin
      gsi_flags_w = {1'b1,                    // STREAM_FORMAT_VALID
                     gsi_setl_w,              // STREAM_ID_VALID
                     gsi_reging_w,            // MSRP_ACC_LAT_VALID
                     gsi_setl_w,              // STREAM_DEST_MAC_VALID
                     gsi_tkfail_w,            // MSRP_FAILURE_VALID
                     gsi_bnd_w,               // BOUND
                     gsi_setl_w,              // STREAM_VLAN_ID_VALID
                     18'd0,
                     gsi_tkfail_w,            // REGISTERING_FAILED
                     2'b0,
                     //! Milan Table 5.9 bit 28: "0 if the Stream Input is
                     //! bound and started, 1 if the Stream Input is bound and
                     //! stopped, undefined if the Stream Input is not bound."
                     //! This was a hardcoded 0 justified as "bound = started",
                     //! which was true only while stopped was unreachable;
                     //! with §5.4.2.20 served it would report a stopped sink
                     //! as started. It reads the SAME bit the admission gate
                     //! above does, so the answer and the behaviour cannot
                     //! disagree.
                     gsi_bnd_w && !pp_aecp_strm_started_w[gsi_six_w],
                     gsi_bnd_w,               // SAVED_STATE (recommended)
                     gsi_bnd_w,               // FAST_CONNECT (= bound, T5.9)
                     1'b0};                   // CLASS_B
      gsi_flags_ex_w = {31'd0, gsi_reging_w}; // REGISTERING
    end else if (gsi_out_w) begin
      gsi_flags_w = {1'b1,                    // STREAM_FORMAT_VALID
                     gsi_decl_w,              // STREAM_ID_VALID
                     1'b1,                    // MSRP_ACC_LAT_VALID (always)
                     gsi_decl_w,              // STREAM_DEST_MAC_VALID
                     gsi_ofail_w,             // MSRP_FAILURE_VALID
                     1'b0,                    // BOUND (outputs: always 0)
                     gsi_decl_w,              // STREAM_VLAN_ID_VALID
                     18'd0,
                     gsi_decl_w && (gsi_lreg_w == 2'd1),  // REGISTERING_FAILED
                     6'd0};
      gsi_flags_ex_w = {31'd0, gsi_oreging_w};
    end
  end : gsi_flag_law

  wire [47:0] gsi_odmac_w = maap_addr + 48'(gsi_ix_w);
  wire [63:0] gsi_osid_w  = pp_src_sid_w[64*gsi_oix_w +: 64];

  //! ---- the SET_STREAM_FORMAT verdict (kind 0 selector 15, issue #67) ----
  //! The processor presents the PROPOSED format on `pp_gsi_prop_fmt_w` and
  //! asks this fabric to judge it: bit 0 = a format this build can serve for
  //! the addressed stream, bit 1 = every channel an existing audio mapping
  //! references still exists in it (Milan §5.4.2.7's SHALL). Anything less
  //! than 3 refuses BAD_ARGUMENTS processor-side.
  //!
  //! SUPPORTED is a family decode, not a list walk: the descriptors
  //! advertise the generated base (`ADP_STRIN0_FMT_C`) plus Milan §6.2's
  //! 48 kHz channel family {1,2,4,6,8} through the ut-bit entry, so a
  //! proposal is supported when it equals the base outside the
  //! channels_per_frame field (qword [31:22]) with the ut bit CLEAR (a SET
  //! names one concrete format, never a family string) and its channel
  //! count is a family member. Inputs take the whole family - the RX
  //! monitor already adapts to any wire count 1..8 under the declared base.
  //! An OUTPUT is talker truth: the framer emits exactly the generated wire
  //! shape, so only the base's own channel count is accepted until talker
  //! adaptation exists. The CRF rows admit exactly the advertised CRF
  //! format (`ADP_CRF_FMT_C`) - §5.3.3.4 keeps the AAF and CRF families
  //! disjoint per stream.
  //! channels_per_frame lives at qword [31:22] (the builder's aaf_pcm32
  //! encoder is the gate-proven authority; the generated 2/4/8ch constants
  //! differ ONLY there). The first cut read [47:38] - the format octet plus
  //! bit_depth - which froze the family compare shut and the channel counts
  //! at a constant 8; the review's mutation run is what caught it.
  localparam logic [63:0] SFMT_VAR_MASK_C = (64'h3FF << 22) | (64'h1 << 52);
  wire [63:0] sfv_prop_w  = pp_gsi_prop_fmt_w;
  wire [9:0]  sfv_ch_w    = sfv_prop_w[31:22];
  //! the addressed ROW's declared first format, per direction: the config
  //! accepts independent per-row format lists, so row k's verdict base and
  //! the current format its GET serves at reset are row k's OWN generated
  //! fact, never row 0's. Out-of-range rows read zero and fail closed.
  logic [63:0] sfv_decl_in_w, sfv_decl_out_w;
  always_comb begin : sfv_decl_rows
    sfv_decl_in_w  = 64'd0;
    sfv_decl_out_w = 64'd0;
    for (int r = 0; r < ADP_STRIN_NFMT_C; r++)
      if (gsiq_index_r == 16'(r)) sfv_decl_in_w = ADP_STRIN_FMT_C[r];
    for (int r = 0; r < ADP_STROUT_NFMT_C; r++)
      if (gsiq_index_r == 16'(r)) sfv_decl_out_w = ADP_STROUT_FMT_C[r];
  end
  wire [63:0] sfv_decl_w = gsi_in_w ? sfv_decl_in_w
                         : gsi_out_w ? sfv_decl_out_w : 64'd0;
  wire sfv_base_ok_w = ((sfv_prop_w & ~SFMT_VAR_MASK_C)
                        == (sfv_decl_w & ~SFMT_VAR_MASK_C))
                       && !sfv_prop_w[52];
  wire sfv_fam_ch_w  = (sfv_ch_w == 10'd1) || (sfv_ch_w == 10'd2)
                    || (sfv_ch_w == 10'd4) || (sfv_ch_w == 10'd6)
                    || (sfv_ch_w == 10'd8);
  wire sfv_crf_row_w = (gsi_in_w  && (32'(gsiq_index_r) == CRF_SNK_IDX_C)
                        && (ACMP_SINKS_C > N_STREAMS))
                    || (gsi_out_w && (32'(gsiq_index_r) == CRF_TUID_C));
  wire sfv_supported_w =
      sfv_crf_row_w ? (sfv_prop_w == (gsi_out_w ? ADP_CRF_OUT_FMT_C
                                                : ADP_CRF_FMT_C))
    : gsi_in_w      ? (sfv_base_ok_w && sfv_fam_ch_w)
    //! talker truth, per row: an output admits exactly the format its own
    //! descriptor declares (base AND channel count) until talker adaptation
    //! exists - the framer emits the declared wire shape and nothing else
    : gsi_out_w     ? (sfv_base_ok_w
                       && (sfv_ch_w == sfv_decl_w[31:22]))
                    : 1'b0;
  //! sfv_need_in_r belongs to the INPUT-side reduction below; it is
  //! declared here because sfv_need_w is its first reader (#193).
  logic [3:0] sfv_need_in_r [N_STREAMS];
  //! sfv_need_out_w belongs to the OUTPUT-side reduction below; it is
  //! declared here because sfv_need_w is its first reader (#193).
  logic [ACMP_SRC_C*4-1:0] sfv_need_out_w;
  //! SURVIVES: the per-stream channels-required reductions below, judged
  //! against the proposal's channel count. The CRF rows carry no audio
  //! mappings, so they survive by construction.
  wire [3:0] sfv_need_w = sfv_crf_row_w ? 4'd0
                        : gsi_in_w  ? sfv_need_in_r[gsi_six_w]
                        : gsi_out_w ? sfv_need_out_w[4*gsi_oix_w +: 4]
                                    : 4'd0;
  wire sfv_survives_w = 32'(sfv_need_w) <= 32'(sfv_ch_w);
  wire [63:0] sfv_verdict_w = {62'd0, sfv_survives_w, sfv_supported_w};

  //! ---- channels-required reductions feeding the verdict ------------------
  //! INPUT side: the render map is keyed by global cluster and its 8-bit
  //! entries carry {en, src, stream[2:0], channel[2:0]}, so the per-stream
  //! maximum needs a scan. One ROLLING key per cycle into per-stream
  //! accumulators, published at each wrap: a full sweep is
  //! ADP_DMAP_IN_KEYS_C cycles, far under any command's lifetime, and map
  //! edits cannot race the verdict - the engine runs one AECP command at a
  //! time, and the vendor-CSR chmap path is bring-up-only (state is set
  //! over ATDECC). One shared read mux instead of per-stream trees: the
  //! amap page walk's timing verdict priced parallel indexed reads out.
  localparam int SFV_KEYS_C = ADP_DMAP_IN_KEYS_C;
  localparam int SFV_KW_C = (SFV_KEYS_C <= 2) ? 1 : $clog2(SFV_KEYS_C);
  logic [SFV_KW_C-1:0] sfv_cur_r;
  logic [3:0] sfv_acc_r     [N_STREAMS];
  //! (sfv_need_in_r is declared above sfv_need_w, its first reader, #193)
  logic [3:0] sfv_nxt_w     [N_STREAMS];
  wire  [7:0] sfv_ent_w = amap_in_store_r[32'(sfv_cur_r)*8 +: 8];
  wire  [3:0] sfv_ent_need_w = {1'b0, sfv_ent_w[2:0]} + 4'd1;
  always_comb begin : sfv_in_next
    for (int s = 0; s < N_STREAMS; s++) begin
      sfv_nxt_w[s] = sfv_acc_r[s];
      if (sfv_ent_w[7] && !sfv_ent_w[6] && (32'(sfv_ent_w[5:3]) == s)
          && (sfv_ent_need_w > sfv_acc_r[s]))
        sfv_nxt_w[s] = sfv_ent_need_w;
    end
  end
  always_ff @(posedge axis_clk or negedge axis_resetn) begin : sfv_in_sweep
    if (!axis_resetn) begin
      sfv_cur_r <= '0;
      for (int s = 0; s < N_STREAMS; s++) begin
        sfv_acc_r[s]     <= 4'd0;
        sfv_need_in_r[s] <= 4'd0;
      end
    end else if (32'(sfv_cur_r) == SFV_KEYS_C - 1) begin
      sfv_cur_r <= '0;
      for (int s = 0; s < N_STREAMS; s++) begin
        sfv_need_in_r[s] <= sfv_nxt_w[s];
        sfv_acc_r[s]     <= 4'd0;
      end
    end else begin
      sfv_cur_r <= sfv_cur_r + SFV_KW_C'(1);
      for (int s = 0; s < N_STREAMS; s++)
        sfv_acc_r[s] <= sfv_nxt_w[s];
    end
  end
  //! OUTPUT side: the capture map is ALREADY stream-channel keyed
  //! (key = stream*8 + channel), so the requirement is a per-stream
  //! priority over eight enable bits - combinational, no sweep. The CRF
  //! row's nibble stays zero: no audio mapping can reference it.
  //! (sfv_need_out_w is declared above sfv_need_w, its first reader, #193)
  always_comb begin : sfv_out_need
    sfv_need_out_w = '0;
    for (int s = 0; s < N_STREAMS; s++)
      for (int c = 0; c < 8; c++)
        if (cmap_flat_w[(s*8 + c)*13 + 12])
          sfv_need_out_w[4*s +: 4] = 4'(c + 1);
  end

  //! ---- the served 802.1AS path (Milan 5.4.2.17 GET_AS_PATH) ----------
  //! Entry 0, when count is nonzero, is the selected owner's grandmaster;
  //! entries 1.. are its PathTrace tail. No grandmaster is always empty. With
  //! a fabric GM, count zero is also empty because the selected Announce had
  //! no PathTrace TLV. Option-off aliases are structural zero, so software
  //! writes cannot create either a count or an entry.
  wire [3:0] asp_served_count_w = asp_resp_count_r;
  logic [63:0] asp_served_entry_w;
  always_comb begin : asp_entry_pick
    asp_served_entry_w = 64'd0;
    if (32'(gsiq_ord_r) < 32'(asp_served_count_w)) begin
      if (gsiq_ord_r == 8'd0) asp_served_entry_w = asp_resp_gm_r;
      else
        for (int unsigned k = 1; k < ASP_SLOTS_C + 1; k++)
          if (32'(gsiq_ord_r) == k)
            asp_served_entry_w = asp_resp_path_r[64*(k-1) +: 64];
    end
  end : asp_entry_pick

  always_comb begin : gsi_answer
    gsi_ans_raw_w = 64'd0;
    unique case (gsiq_kind_r)
      2'd0: begin                            // ---- GET_STREAM_INFO ----
        unique case (gsiq_sel_r)
          4'd0: gsi_ans_raw_w = {32'd0, gsi_flags_w};
          //! the CURRENT format: a valid settings row IS the current format
          //! (SET_STREAM_FORMAT stored it); until then the generated base -
          //! and the CRF rows report the CRF format, never the AAF base
          4'd1: gsi_ans_raw_w =
                    gsi_in_w
                      ? (sfv_crf_row_w ? ADP_CRF_FMT_C
                         : pp_aecp_fmt_in_v_w[gsi_six_w]
                           ? pp_aecp_fmt_in_w[64*gsi_six_w +: 64]
                           : sfv_decl_in_w)
                  : gsi_out_w
                      ? (sfv_crf_row_w ? ADP_CRF_OUT_FMT_C
                         : pp_aecp_fmt_out_v_w[gsi_oix_w]
                           ? pp_aecp_fmt_out_w[64*gsi_oix_w +: 64]
                           : sfv_decl_out_w)
                      : 64'd0;
          4'd2: gsi_ans_raw_w = gsi_in_w  ? gsi_sid_w
                              : gsi_decl_w ? gsi_osid_w : 64'd0;
          //! an output's accumulated latency reads the SAME folded transit
          //! entry the framer stamps (SET_STREAM_INFO's landing point), so
          //! the answer and the wire cannot disagree
          4'd3: gsi_ans_raw_w = gsi_in_w
                              ? {32'd0, gsi_reging_w
                                 ? pp_cd_srp_acc_latency_w[32*gsi_six_w +: 32]
                                 : 32'd0}
                              : {32'd0, gsi_out_w
                                 ? aecp_pres_offset[32*gsi_oix_w +: 32]
                                 : 32'd0};
          4'd4: gsi_ans_raw_w = gsi_setl_w
                              ? {pp_cd_acmp_bound_dmac_w[48*gsi_six_w +: 48],
                                 gsi_tkfail_w
                                 ? pp_cd_srp_snk_fail_code_w[8*gsi_six_w +: 8]
                                 : 8'd0, 8'd0}
                              : gsi_decl_w
                              ? {(maap_addr_valid ? gsi_odmac_w : 48'd0),
                                 gsi_ofail_w
                                 ? pp_cd_srp_src_fail_code_w[8*gsi_oix_w +: 8]
                                 : 8'd0, 8'd0}
                              : {48'd0,
                                 gsi_tkfail_w
                                 ? pp_cd_srp_snk_fail_code_w[8*gsi_six_w +: 8]
                                 : 8'd0, 8'd0};
          4'd5: gsi_ans_raw_w = gsi_ofail_w
                              ? pp_cd_srp_src_fail_bridge_w[64*gsi_oix_w +: 64]
                              : 64'd0;       // sink bridge id: honest zero
          4'd6: gsi_ans_raw_w = {gsi_setl_w
                                 ? {4'd0, pp_cd_acmp_bound_vlan_w[12*gsi_six_w +: 12]}
                                 : gsi_decl_w
                                 ? {4'd0, pp_cd_srp_class_a_vid_w}
                                 : 16'd0,
                                 16'd0, gsi_flags_ex_w};
          4'd7: gsi_ans_raw_w = {32'd0,
                                 gsi_in_w
                                 ? {(!gsi_bnd_w ? 3'd0
                                     : gsi_setl_w ? 3'd3 : 3'd1), 5'd0}
                                 : 8'd0,
                                 24'd0};
          //! SET_STREAM_FORMAT's verdict on the proposed format (issue #67)
          4'd15: gsi_ans_raw_w = sfv_verdict_w;
          default: gsi_ans_raw_w = 64'd0;
        endcase
      end
      2'd1: begin                            // ---- GET_AVB_INFO ----
        unique case (gsiq_sel_r)
          4'd0: gsi_ans_raw_w = gsi_gm_snap_r;
          4'd1: gsi_ans_raw_w = {gsi_pdelay_snap_r,
                                 gsi_domain_snap_r,
                                 {3'd0, 1'b1, !gsi_link_snap_r, 1'b1, 1'b1,
                                  gsi_ascap_snap_r},
                                 16'd1};     // one msrp mapping: class A
          4'd8: gsi_ans_raw_w = (gsiq_ord_r == 8'd0)
                              ? {32'd0, 8'd6,       // SRclassID A
                                 {5'd0, gsi_prio_snap_r},
                                 {4'd0, gsi_vid_snap_r}}
                              : 64'd0;
          default: gsi_ans_raw_w = 64'd0;
        endcase
      end
      default: begin                         // ---- GET_AS_PATH ----
        unique case (gsiq_sel_r)
          4'd0: gsi_ans_raw_w = {60'd0, asp_served_count_w};
          4'd8: gsi_ans_raw_w = asp_served_entry_w;
          default: gsi_ans_raw_w = 64'd0;
        endcase
      end
    endcase
  end : gsi_answer
  assign pp_gsi_data_w = gsi_data_r;
  assign pp_gsi_wait_w = pp_gsi_req_w && !(gsi_srv2_r && gsi_sel_match_w);  //! live-match: see the counters face

  //! ---- the Table 5.22 trigger pins this fabric owns -------------------
  //! ONE effective source per served GET_AVB_INFO field, and the SAME wire
  //! feeds the answer mux above and the detector below. Milan Table 5.22
  //! names six GET_AVB_INFO triggers; the root serves and detects four of
  //! them here, and the remaining two are the processor's own:
  //!
  //!   gptp_grandmaster_id  cfg_adp_gptp_gm      served 4'd0, snapped here
  //!   propagation_delay    eff_gptp_pdelay_w    served 4'd1, snapped here
  //!   gptp_domain_number   cfg_adp_gptp_domain  served 4'd1, snapped here
  //!   as_capable (flags)   clkv_as_cap_w        served 4'd1, snapped here
  //!   SR class A priority  srp_class_a_prio     served 4'd8, detected in
  //!   SR class A VLAN ID   srp_class_a_vid      the processor off the SAME
  //!                                             wires it publishes here
  //!                                             (evt_domain_change_o), and
  //!                                             AVTP_DOWN likewise off the
  //!                                             eff_link_w it is handed.
  //!
  //! NONE of the four is conditioned on grandmaster presence. That matters
  //! because pp_gm_change_p_w - the ADP duty, 1722.1-2021 6.2.6 - is
  //! deliberately silent while the PREVIOUS grandmaster id is zero, so that
  //! no boot announces a GM_CHANGE that never happened. Routing the AEM
  //! notification duty through that strobe made reset and GM-loss windows
  //! swallow a real domain change: the two duties are kept apart here, and
  //! the ADP strobe keeps its re-advertise semantics untouched.
  //!
  //! A snapshot compare also gives the no-op rule for free: a write that
  //! stores the value already held moves nothing and strobes nothing, which
  //! is the same silence 5.4.5.2 requires of a no-op SET.
  //!
  //! gsi_snap_v_r suppresses the reset cycle itself. The snapshots and the
  //! Milan domain both start at structural zero, so reset cannot manufacture
  //! a change into an empty registry.
  //!
  //! GET_AS_PATH keeps its own served-tuple comparator and never uses the ADP
  //! strobe or the unconditional grandmaster-identity edge.
  //! Milan Table 5.22 triggers GET_AS_PATH on "the path sequence changes",
  //! and this fabric serves that sequence from one selected owner. Compare
  //! exactly `(count ? GM : 0, count, active tails)`, not a raw publication
  //! generation. Thus fabric count 0 <-> 1 is a real sequence edge; GM A->B
  //! while both fabric counts are zero is silent; every tail aliases to empty
  //! while GM=0. Option OFF is ownerless and has no staging state to compare.
  //!
  //! What is NOT a term is the gPTP domain number. It is a GET_AVB_INFO
  //! field (below) and an ADPDU field, but it is not a path entry, so a
  //! domain-only write with a stable grandmaster must push nothing here.
  //! Routing pp_gm_change_p_w - the ADP duty, which carries the domain -
  //! into an AS_PATH event is exactly that defect, and the processor's
  //! ev_asp_i takes gsi_asp_chg_i alone for the same reason.
  //!
  //! All of these are one-cycle strobes; the processor coalesces them into
  //! one push per class.
  logic gsi_ascap_q_r;
  logic [63:0] gsi_asp_gm_q_r;
  logic [3:0] gsi_asp_count_q_r;
  logic [7*64-1:0] gsi_asp_path_q_r;
  logic gsi_snap_v_r;
  logic [63:0] gsi_gm_q_r;
  logic [31:0] gsi_pdly_q_r;
  logic [7:0]  gsi_dom_q_r;
  always_ff @(posedge axis_clk) begin : gsi_change_edges
    if (!axis_resetn) begin
      gsi_ascap_q_r <= 1'b0;
      gsi_asp_gm_q_r <= 64'd0;
      gsi_asp_count_q_r <= 4'd0;
      gsi_asp_path_q_r  <= '0;
      gsi_snap_v_r  <= 1'b0;
      gsi_gm_q_r    <= 64'd0;
      gsi_pdly_q_r  <= 32'd0;
      gsi_dom_q_r   <= 8'd0;
    end else begin
      gsi_ascap_q_r <= clkv_as_cap_w;
      gsi_asp_gm_q_r <= asp_live_gm_w;
      gsi_asp_count_q_r <= asp_live_count_w;
      gsi_asp_path_q_r  <= asp_live_path_w;
      gsi_snap_v_r  <= 1'b1;
      gsi_gm_q_r    <= cfg_adp_gptp_gm;
      gsi_pdly_q_r  <= eff_gptp_pdelay_w;
      gsi_dom_q_r   <= cfg_adp_gptp_domain;
    end
  end
  //! the grandmaster-identity term, named once because BOTH detectors need
  //! it and only one of them may see the domain
  wire gsi_gm_chg_w  = gsi_snap_v_r && (cfg_adp_gptp_gm != gsi_gm_q_r);
  wire gsi_avb_chg_w = gsi_gm_chg_w
                    || (gsi_snap_v_r
                        && ((clkv_as_cap_w      != gsi_ascap_q_r)
                            || (eff_gptp_pdelay_w   != gsi_pdly_q_r)
                            || (cfg_adp_gptp_domain != gsi_dom_q_r)));
  //! One source for the event and the answer: compare the complete served
  //! sequence. gsi_gm_chg_w remains the AVB_INFO/counter identity edge, but
  //! AS_PATH sees the GM only when its count makes entry zero present.
  wire gsi_asp_chg_w = gsi_snap_v_r
                    && ((asp_live_gm_w != gsi_asp_gm_q_r)
                        || (asp_live_count_w != gsi_asp_count_q_r)
                        || (asp_live_path_w != gsi_asp_path_q_r));

  //! IDENTIFY: the processor serves the CONTROL descriptor and stores its
  //! dynamic value. KL_pp_shadow exports aecp_identify_o into
  //! pp_aecp_identify_w, but no root consumer drives the public indication
  //! from that wire yet. The physical output remains structurally dark.
  assign o_identify = 1'b0;

  // ==========================================================================
  //  ACMP — talker AND listener, served by the protocol processor
  // ==========================================================================
  //! KL_acmp_tlkr_ctx, KL_acmp_responder, KL_acmp_listener, KL_acmp_lstn_ctx
  //! and acmp_pkg.sv are DELETED. The processor's KL_acmp_talker /
  //! KL_pp_acmp_listener pair answers CONNECT_TX/PROBE_TX/GET_TX_STATE and
  //! runs the BIND_RX ladder, and republishes the result through the class-D
  //! face - which is what every consumer in this file reads now.
  //!
  //! THE DA GATE IS THE TALKER GATE. acmp_declaring_o asserts only after an
  //! ALLOC_DA success through KL_pp_maap_shim, so the composed AAF admission
  //! below is still "a destination address exists AND the source is
  //! declaring", exactly as it was.
  assign acmp_talker_active_v = pp_cd_acmp_declaring_w;
  assign acmp_talker_active   = acmp_talker_active_v[0];
  //! PROBE_ARMED was the legacy talker SM's "a probe window is open" level,
  //! read only by the 0x6E8 forensics word. The processor exposes no
  //! equivalent through the class-D face: STRUCTURAL ZERO.
  assign acmp_probe_armed_v   = {ACMP_SRC_C{1'b0}};
  assign acmp_probe_armed     = 1'b0;
  assign acmp_cmd_count = 16'd0;
  assign acmp_resp_count = 16'd0;

  //! ---- the listener half's bind record, per sink -------------------------
  //! Same index law the deleted listener used: sink k is listener_unique_id
  //! k, sinks 0..N_STREAMS-1 the AAF sinks and the last one the CRF Media
  //! Clock Input when this shape declares it.
  assign acmpl_bound_v_w = pp_cd_acmp_bound_w;

  //! Milan v1.2 §5.3.8.7: "A PAAD-AE having a started Stream Input shall
  //! process the incoming stream data ... A PAAD-AE having a stopped Stream
  //! Input shall DISCARD the Stream AVTPDUs it receives." Both halves are
  //! shalls, and until START/STOP_STREAMING landed (issue #78) neither was
  //! implemented — `pp_aecp_strm_started_w` was connected and read by nothing.
  //!
  //! The admission view is SEPARATE from `acmpl_bound_v_w` rather than folded
  //! into it: bind level drives the CRF sink and the entry-0 alias below, and
  //! stopping an AAF sink must not disturb either. Nor does it touch SRP —
  //! a stopped Stream Input is still BOUND, so its reservation stands; the
  //! clause discards the AVTPDUs, it does not withdraw the registration.
  //! It is NOT routed through the classification table. That was the first
  //! cut and it was wrong: the table's bind level feeds the bind edges, and
  //! Milan Table 5.6 makes a not-bound->bound edge the counter RESET event,
  //! so a stop/start pair wiped all ten counters on a sink that never
  //! unbound. The discard is on the accept pulse instead - see the comment
  //! at `avtprx_accept_p` below, which is the authority on this.
  //! The sinks §5.3.8.7 says to DISCARD for: bound AND stopped. Stated as
  //! the stop condition rather than as "bound and started" on purpose - the
  //! clause calls the state "undefined when the Stream Input is not bound",
  //! so an entry that is NOT ACMP-bound is outside its scope entirely and
  //! must keep flowing. A classification entry provisioned through the
  //! `0x800` override window has no binding behind it, and gating it on
  //! `bound & started` would silence every one of them.
  wire [ACMP_SINKS_C-1:0] acmpl_stopped_v_w = acmpl_bound_v_w
                                              & ~pp_aecp_strm_started_w;

  //! ...and the CRF Media Clock Input's own bit, guarded by whether that sink
  //! EXISTS. `CRF_SNK_IDX_C` falls back to 0 on a shape with `crf_sink:
  //! false` (ACMP_SINKS_C == N_STREAMS), and reading index 0 there would let
  //! a STOP_STREAMING aimed at AAF Stream Input 0 reach into the media-clock
  //! receiver's consumption ladder - a controller command touching clock
  //! recovery on a sink it never named. Every tracked config sets
  //! `crf_sink: true`, so no shipping shape takes the fallback; the guard is
  //! here so that stays true of shapes nobody has built yet.
  //! `acmpl_stopped_v_w` has TWO consumers: the listener accept gate (the
  //! AAF sinks, where stopped DISCARDS payload) and, through this wire,
  //! `KL_crf_rx`'s `stop_i` (the CRF Media Clock Input, which has no
  //! classification-table entry of its own). The CRF side is NOT a frame
  //! gate: `frame_p_i` stays raw so a stopped sink keeps observing and
  //! counting per §5.3.8.10, and `stop_i` gates only consumption - the
  //! settle/lock ladder and the mr restart echo. Between the two consumers
  //! every Stream Input the entity advertises is covered, which is what
  //! §5.4.2.19's "For each Stream Input" and §5.3.8.7's discard rule
  //! together require.
  wire crf_snk_stopped_w = (ACMP_SINKS_C > N_STREAMS)
                           && acmpl_stopped_v_w[CRF_SNK_IDX_C];

  assign acmpl_sid_v_w   = pp_cd_acmp_bound_sid_w;
  //! the scalar sink-0 shadows every legacy consumer here still reads
  assign acmpl_bound = acmpl_bound_v_w[0];
  assign acmpl_sid   = acmpl_sid_v_w [63:0];
  //! ...and sink 1's, the 0x4B BSCAN forensics pair
  assign acmpl1_bound = (ACMP_SINKS_C > N_STREAMS) &
                        acmpl_bound_v_w[CRF_SNK_IDX_C];
  assign acmpl1_sid   = (ACMP_SINKS_C > N_STREAMS)
                        ? acmpl_sid_v_w[64*CRF_SNK_IDX_C +: 64] : 64'd0;
  //! The legacy listener SM's observable surface. There is no state machine
  //! here any more - the processor runs the ladder internally and publishes
  //! only the BOUND record - so everything that described the ladder itself
  //! reads a STRUCTURAL ZERO. ACMPL_STATE 0x6E0 in particular no longer
  //! tracks PROBING/SETTLED: a reader must take acmpl_bound as the truth.
  assign acmpl_state = 3'd0;
  wire [63:0] acmpl_talker = 64'd0;
  assign acmpl_tuid = 16'd0;
  assign acmpl_status = 5'd0;
  assign acmpl_probing = 2'd0;
  assign acmpl_tk_avail = 1'b0;
  assign acmpl_lstn_declare = 1'b0;
  assign acmpl_active = acmpl_bound;
  assign acmpl_cmd_count = 16'd0;
  assign acmpl_probe_count = 16'd0;
  assign acmpl_tx_wedge = 8'd0;
  assign acmpl_dbg = 32'd0;
  //! the 0x800 window's ACMP table master: no context table to serve
  assign acmp_tbl_gnt_w = 1'b0;
  assign acmp_tbl_ctx_w = {ACMP_LSTN_CTX_W_C{1'b0}};
  //! E1/E3 saved-state fast-connect: the journal AND the restore port are
  //! deleted. The processor has its own NVM restore walk, answered here by a
  //! BLANK-FLASH responder inside KL_pp_shadow, so nothing is restored.
  assign acmp_rest_ack_w = 1'b0;
  assign acmp_rest_status_w = 2'd0;
  assign jnl_stat_w = 32'd0;
  assign jnl_seq_w = 32'd0;

  // ==========================================================================
  //  AVTP RX monitor (Milan v1.2 §5.4.5.3, Table 7-156) — non-intrusive
  //  parser on the same RX tap, matched to the BOUND stream_id the protocol
  //  processor publishes. Its counters reach local software through the 0x6B8
  //  A_STRMW_CNT CSR window and supported controller targets through solicited
  //  GET_COUNTERS and through the lossless dirty arbiter into the processor's
  //  live Table 5.22 notification scheduler (#69).
  // ==========================================================================
  //! NXN §1.1 (P1): stream-table classification authority. Entry 0 aliases
  //! the processor's ACMP bound record combinationally; entries
  //! 1..N-1 + bench overrides arrive via the 0x800 CSR window (P12 glue
  //! below).
  localparam int NSIDX_W_C = (N_STREAMS <= 1) ? 1 : $clog2(N_STREAMS);
  wire [64*N_STREAMS-1:0] strtbl_sid_w;
  wire [N_STREAMS-1:0]    strtbl_en_w;
  wire [N_STREAMS-1:0]    strtbl_bind_rise_w;
  wire [N_STREAMS-1:0]    strtbl_bind_fall_w;  //! task #32: the wipe pulse
  wire [NSIDX_W_C-1:0]    avtprx_idx;

  //! P12 window commit glue (NXN §1.1/§1.3): the CSR window's listener
  //! writes land in the LCTX (monitor CFG words); the classification table
  //! and the route policy shadow the SAME accepted writes here — SID_LO/HI
  //! (w0/w1) stage, a CTRL (w4) write COMMITS {sid, en} into the stream
  //! table entry and [2:1] into the route table (mirrors the CSR's own
  //! SEL-then-words staging ABI).
  //!
  //! The staging pair is ONE register set shared by every index, so it MUST
  //! carry the index it was staged for: a CTRL commit only overrides the
  //! table when a sid was staged FOR THAT INDEX. Testing "some sid is staged"
  //! instead (the pre-2026-07-26 form) let a route-flags-only CTRL write at
  //! idx 0 arm entry 0 with another listener's sid, permanently detaching the
  //! ACMP alias -> bound-but-never-matching. See `tb/verilator/milan_dp`
  //! TRAP-1 and the current stream-table integration notes.
  logic [31:0] wing_sid_lo_r, wing_sid_hi_r;
  logic        wing_tbl_we_r, wing_route_we_r;
  logic [3:0]  wing_idx_r;
  logic [63:0] wing_sid_r;
  logic        wing_en_r;
  logic [1:0]  wing_route_r;
  //! which index the staged sid belongs to, and whether it is still unspent
  logic [2:0]  wing_stg_idx_r;
  logic        wing_stg_vld_r;
  wire lctx_wr_acc_w = csr_lctx_wr_p_w && lctx_wr_rdy_w;
  //! the index carried by the window write currently being accepted
  wire [2:0] wing_wr_idx_w = csr_lctx_wr_addr_w[7:5];
  //! staging is only spendable by a commit to the SAME index
  wire wing_stg_hit_w = wing_stg_vld_r && (wing_stg_idx_r == wing_wr_idx_w);

  always_ff @(posedge axis_clk) begin : win_commit_glue
    if (!axis_resetn) begin
      wing_sid_lo_r <= '0; wing_sid_hi_r <= '0;
      wing_tbl_we_r <= 1'b0; wing_route_we_r <= 1'b0;
      wing_idx_r <= '0; wing_sid_r <= '0; wing_en_r <= 1'b0;
      wing_route_r <= '0;
      wing_stg_idx_r <= '0; wing_stg_vld_r <= 1'b0;
    end
    else begin
      wing_tbl_we_r   <= 1'b0;
      wing_route_we_r <= 1'b0;
      if (lctx_wr_acc_w) begin
        unique case (csr_lctx_wr_addr_w[4:0])
          //! staging a sid half BINDS the staging set to that index; a half
          //! aimed at a different index restarts the set rather than mixing
          //! two listeners' halves into one 64-bit value
          5'd0 : begin
            wing_sid_lo_r  <= csr_lctx_wr_data_w;
            if (!wing_stg_hit_w) wing_sid_hi_r <= '0;
            wing_stg_idx_r <= wing_wr_idx_w;
            wing_stg_vld_r <= 1'b1;
          end
          5'd1 : begin
            wing_sid_hi_r  <= csr_lctx_wr_data_w;
            if (!wing_stg_hit_w) wing_sid_lo_r <= '0;
            wing_stg_idx_r <= wing_wr_idx_w;
            wing_stg_vld_r <= 1'b1;
          end
          5'd4 : begin              //! CTRL commit: {en[0], route[2:1]}
            //! Override the table ONLY when a sid was staged FOR THIS INDEX,
            //! or on an eviction (en=0). Testing "some sid is staged" instead
            //! let a route-flags-only CTRL=en at idx 0 arm entry 0 with
            //! another listener's stale sid and detach the ACMP alias for
            //! good (bound-but-never-matching). 2026-07-23 bench: the
            //! zero-sid variant of the same write froze a locked stream.
            wing_tbl_we_r   <= wing_stg_hit_w | ~lctx_wr_data_sane_w[0];
            wing_route_we_r <= 1'b1;
            wing_idx_r      <= {1'b0, wing_wr_idx_w};
            //! an eviction with nothing staged for this index commits the
            //! ZERO sid, which is `KL_stream_table`'s release-to-alias code
            wing_sid_r      <= wing_stg_hit_w ? {wing_sid_hi_r, wing_sid_lo_r}
                                              : 64'd0;
            wing_en_r       <= lctx_wr_data_sane_w[0];
            wing_route_r    <= lctx_wr_data_sane_w[2:1];
            wing_stg_vld_r  <= 1'b0;   //! staging is spent by its commit
          end
          default : ;
        endcase
      end
    end
  end : win_commit_glue

  //! The TCTX CTRL[0] shadow that lived here (tctx_en_r, the t>0 admission
  //! enable) is DELETED, 2026-07-30. It reset to 0 with no board-software
  //! writer, so it held every talker above 0 dark forever on the
  //! shape-static builds, and a per-stream software enable is not ours to
  //! have in the first place (Milan v1.2 5.3.7.3 / 5.4.2.19 / 5.4.2.20 /
  //! 5.5.4.1 - see the g_aaf_stream_en banner). TCTX w0 writes still land
  //! in the packetizer's context RAM, so chans and VID stay provisionable;
  //! bit 0 of that word is simply no longer consulted by anything.

  // ==========================================================================
  //  PER-ROW lwSRP TSpec (2026-07-26): MaxFrameSize is a property of the
  //  STREAM, not of the engine. The 0x800 window has no per-stream TSpec
  //  word, so every ctx row used to be provisioned from the shared
  //  LWSRP_TSPEC (0x690) and a 2-channel and an 8-channel talker reserved
  //  identically — one of them always wrong, and the reservation could not
  //  match the frames the packetizer actually emits.
  //
  //  The honest source is the geometry the packetizer itself uses: TCTX w0
  //  `chans` (same field, same clamp), so reservation and wire can never
  //  disagree. For the AAF-PCM32 frame this datapath builds,
  //    payload = SAMPLES_PER_FRAME x C x 4 = 24*C octets
  //    MSDU (AVTPDU) = 24 + 24*C  <- the MSRP TSpec MaxFrameSize
  //    L2 frame      = 42 + 24*C  = MaxFrameSize + the 802.1Q overhead of 42
  //  which is exactly sw/builder's `srp_frame_geometry` (gate: talker rows
  //  in lwsrp_table.json carry avtpdu_bytes).
  //
  //  Row 0 (the legacy talker+listener pair) is untouched: it keeps
  //  LWSRP_TSPEC verbatim, silicon-proven, per the no-regression axiom.
  localparam int unsigned AAF_SPF_C        = 6;   //! 48 kHz / 8000 per s
  localparam int unsigned AAF_SMP_OCTETS_C = 4;   //! AAF INT_32BIT
  localparam int unsigned AVTP_AAF_HDR_C   = 24;  //! common + format header

  //! same clamp as KL_aaf_packetizer's chn_clamp (even, 2..8)
  function automatic [3:0] aaf_chn_clamp(input [3:0] c);
    aaf_chn_clamp = (c < 4'd2)  ? 4'd2
                  : (c >= 4'd8) ? 4'd8
                  : (c[0] ? (c + 4'd1) : c);
  endfunction

  //! RESET VALUE OF THE TSPEC GEOMETRY = THE ELABORATED WIRE WIDTH, and this
  //! is load-bearing rather than tidy. tctx_chans_r shadows TCTX w0 `chans`,
  //! but NO board software writes that window - it is provisioned by the
  //! fabric (srp_fab_rec_mux below), so on silicon this register never leaves
  //! its reset value. It used to reset to 4'd2 while KL_aaf_packetizer reset
  //! its own chans_r to the elaborated WIRE_CHANS_C, so on the shipping
  //! 4-channel Arty the wire carried a 120-octet AAF frame and talkers
  //! 1..N-1 DECLARED the 2-channel TSpec (73), reserving 7.36 Mb/s against
  //! the 10.368 Mb/s the stream actually occupies - a 29% under-reservation,
  //! i.e. the bridge grants less CBS credit than the traffic needs. Slot 0
  //! escaped it because the fabric mux starts at s=1 and slot 0 keeps
  //! cfg_lwsrp_max_frame, which is exactly the index-0-works / 1..N-1-broken
  //! signature of 0x001F. Deriving the reset from the SAME parameter the
  //! framer is given makes wire and reservation agree by construction at any
  //! width, 8 channels included, and a CSR write still overrides.
  localparam logic [3:0] TCTX_CHANS_RST_C =
      aaf_chn_clamp(4'(TALKER_WIRE_CHANS_P));

  logic [3:0] tctx_chans_r [N_STREAMS];
  //! the window raises tctx_wr_p AND the SRP provisioning request on the
  //! SAME CTRL write, and the ctx record samples max_frame one cycle before
  //! the accepted TCTX handshake retires — so the in-flight write is
  //! bypassed here, never sampled a commit late
  wire       tctx_w0_wr_w = csr_tctx_wr_p_w &&
                            (csr_tctx_wr_addr_w[3:0] == 4'd0) &&
                            (32'(csr_tctx_wr_addr_w[6:4]) < N_STREAMS);
  wire [3:0] tctx_chans_w [N_STREAMS];
  wire [15:0] tctx_maxf_w [N_STREAMS];
  generate
    for (genvar gc = 0; gc < N_STREAMS; gc++) begin : g_tctx_tspec
      assign tctx_chans_w[gc] =
          (tctx_w0_wr_w && (32'(csr_tctx_wr_addr_w[6:4]) == gc))
              ? aaf_chn_clamp(csr_tctx_wr_data_w[4:1]) : tctx_chans_r[gc];
      //! MILAN v1.2 4.3.3.2 Table 4.4, "AAF PCM32, 48kHz, N channels":
      //! MaxFrameSize = 24*N + 24 + 1. The trailing +1 is NOT slack we may
      //! round away - the table's own note says "One more byte is added to
      //! take the fact into account, that the sampling clock of the PAAD may
      //! be a bit faster than the nominal frequency". Omitting it (2026-07-30)
      //! declared 72 bytes for a 2-channel stream where the clause says 73,
      //! and since MaxFrameSize is what the bandwidth is computed from, the
      //! reservation came out at 7296 kbps against the mandated 7360 - an
      //! UNDER-reservation, i.e. the bridge grants less credit than the
      //! stream actually occupies.
      assign tctx_maxf_w[gc] =
          16'(AVTP_AAF_HDR_C) + 16'd1 +
          16'(AAF_SPF_C * AAF_SMP_OCTETS_C) * 16'(tctx_chans_w[gc]);
    end
  endgenerate

  always_ff @(posedge axis_clk) begin : tctx_chans_shadow
    if (!axis_resetn) begin
      for (int t = 0; t < N_STREAMS; t++) tctx_chans_r[t] <= TCTX_CHANS_RST_C;
    end else if (tctx_w0_wr_w && tctx_wr_rdy_w) begin
      for (int t = 0; t < N_STREAMS; t++) begin
        if (32'(csr_tctx_wr_addr_w[6:4]) == t)
          tctx_chans_r[t] <= aaf_chn_clamp(csr_tctx_wr_data_w[4:1]);
      end
    end
  end : tctx_chans_shadow

  // ==========================================================================
  //  THE lwSRP FABRIC PROVISIONER IS DELETED WITH THE ENGINE IT FED.
  // ==========================================================================
  //! Roughly 780 lines lived here: the per-AAF-talker, per-CRF-output and
  //! per-AAF-sink requesters, the two-deep launch pipeline that resolved one
  //! of them per rotation, the record muxes that composed {sid, dmac, vlan,
  //! maxframe, interval, latency} for an attribute row, and the CSR-window
  //! arbitration between them. Every one of them existed to write a
  //! KL_lwsrp_ctx attribute ROW, and there is no attribute row table any
  //! more: the protocol processor keeps its own per-source and per-sink SRP
  //! state and is provisioned by the quasi-static ports on KL_pp_shadow
  //! (cfg_stream_id_i, cfg_src_en_i, cfg_tspec_max_frame_i) plus the ACMP
  //! binds it resolves itself. Provisioning a row is not something this file
  //! does any longer, so nothing here mirrors it.
  //!
  //! The tctx_maxf_w derivation above SURVIVES and is now consumed directly:
  //! it is the Milan Table 4.4 MaxFrameSize the processor declares with.

  //! THE INTERLOCK, repointed. Frames are tagged only while THIS STREAM's
  //! MSRP Talker Advertise is on the wire - otherwise 802.1Q 35.1.2 prunes a
  //! tagged-but-undeclared stream to zero ports, which is strictly worse than
  //! the untagged flood. The level used to be "the fabric provisioned the row
  //! AND the applicant is running"; it is now the processor's own declaration
  //! state for the CRF source, which is the same fact one step closer to the
  //! wire. Shapes with no CRF Stream Output have no source to declare and
  //! keep the untagged fallback.
  //! ...and the select must stay LEGAL at a shape that has no CRF source:
  //! at ACMP_SRC_C == N_STREAMS the vector is 2*N_STREAMS wide and slot
  //! CRF_TUID_C = N_STREAMS is one past its end. Verilator called that out as
  //! SELRANGE; synthesis would have taken the out-of-range bits as X/0 and
  //! the guard above would have hidden it. Clamp the INDEX, not the answer.
  localparam int CRF_DECL_SLOT_C = (ACMP_SRC_C > N_STREAMS) ? CRF_TUID_C : 0;
  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &
                        (|pp_cd_srp_tk_decl_state_w[2*CRF_DECL_SLOT_C +: 2]);
  //! the CRF talker's own bw-gate slot (top of the vector when it exists)
  wire crft_res_active_w = (SRP_CRF_TK_C != 0) &
                           lwsrp_stream_gate[SRP_TALKERS_C-1];
  //! the C-TAG's {PCP, VID}: SR class A defaults {3, LWSRP_VID} (802.1Q
  //! 34.5 / Table 34-1; Milan v1.2 4.2.7.2.1 starts the Domain triple at
  //! {class A, priority 3, VID 2}) - and the OPERATIONAL pair once a
  //! received Domain FirstValue is ADOPTED (4.2.7.2.1's update clause):
  //! the lwSRP applicant serializes op_{prio,vid} into the Domain, the
  //! MVRP VID and the TalkerAdvertise DataFrameParameters, so muxing the
  //! SAME pair here keeps the frame and the declaration one wire.
  wire [2:0]  crft_pcp_w = lwsrp_adopt_valid
                           ? lwsrp_op_prio[2:0]
                           : SR_CLASS_A_PRIO_C[2:0];
  wire [11:0] crft_vid_w = lwsrp_adopt_valid ? lwsrp_op_vid : cfg_lwsrp_vid;
  //! THE LICENCE (Milan v1.2 5.3.7.3): a talker streams while it declares a
  //! Talker Advertise AND receives a Listener Ready - the CRF output is a
  //! Stream Output like any other, so its emission rides the same bw-gate
  //! the AAF talkers use (aaf_gate / aaf_stream_en_w), not the bare CSR
  //! enable. ax-rv32-e wire truth: with zero listeners and no reservation
  //! the old bare-CSR gate kept 500 PDU/s on the wire (FRAMES_TX +1/s,
  //! stat[6]=0), which 5.3.7.3 does not license. The bring-up escapes
  //! mirror the AAF term: AAF bypass, or an lwSRP that is not policing
  //! (engine or talker declarations off - no TA can form, so silence would
  //! deadlock the media clock during bring-up, same doctrine as the
  //! untagged-but-alive fallback above).
  wire crft_emit_en_w = cfg_crft_en &
                        (cfg_aaf_bypass | ~cfg_lwsrp_enable |
                         ~cfg_lwsrp_talker_en | crft_res_active_w);

  //! 0x750 live status (see milan_csr A_CRFT_CTRL); [1:0] come from the CSR
  logic [31:0] crft_stat_c;
  always_comb begin : crft_stat_pack
    crft_stat_c        = 32'd0;
    //! [4] used to be "the fabric provisioned this stream's TA row valid".
    //! There is no row to provision: STRUCTURAL ZERO. [5]/[6] below still
    //! carry the real tagged/reserved levels, from the processor.
    crft_stat_c[4]     = 1'b0;
    crft_stat_c[5]     = crft_class_a_w;        //! frames leaving tagged
    crft_stat_c[6]     = crft_res_active_w;     //! reservation ACTIVE
    crft_stat_c[7]     = crft_emit_en_w;        //! emission licensed NOW
    crft_stat_c[19:8]  = crft_class_a_w ? crft_vid_w : 12'd0;
    crft_stat_c[22:20] = crft_class_a_w ? crft_pcp_w : 3'd0;
  end : crft_stat_pack
  assign crft_stat_w = crft_stat_c;

  KL_stream_table #(.N_LISTENERS_P(N_STREAMS)) stream_table (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    //! entry 0 is the ACMP alias and it gets the PURE bind level, exactly
    //! like the vector below and for the same reason: this port feeds the
    //! bind edges that Table 5.6 resets counters on. The started gate is on
    //! the accept pulse further down.
    .bound0_i (acmpl_bound), .sid0_i (acmpl_sid),
    //! task #32: every entry rides its own sink's bind level, so an UNBIND
    //! evicts the classification entry and the departed stream's frames
    //! become foreign at the parser (the AAF slice of the ACMP view - the
    //! CRF sink classifies in its own path).
    //!
    //! It is the PURE bind level and deliberately NOT the started gate: this
    //! port feeds `bind_rise_o`/`bind_fall_o`, and Milan Table 5.6 resets the
    //! Stream Input counters "each time the Stream Input changes its state
    //! from not bound to bound" - a STOP_STREAMING is not that. Gating here
    //! synthesised a fake unbind/rebind pair around every stop/start, which
    //! wiped all ten counters and flushed the loopback queues on a sink that
    //! never left its binding. The started gate is on ACCEPT instead, below.
    .bound_v_i (acmpl_bound_v_w[N_STREAMS-1:0]),
    .sid_v_i   (acmpl_sid_v_w[64*N_STREAMS-1:0]),
    .wr_en_i (wing_tbl_we_r), .wr_idx_i (wing_idx_r),
    .wr_sid_i (wing_sid_r), .wr_valid_i (wing_en_r),
    .tbl_sid_o (strtbl_sid_w), .tbl_en_o (strtbl_en_w),
    .bind_rise_o (strtbl_bind_rise_w),
    .bind_fall_o (strtbl_bind_fall_w)
  );

  avtp_stream_parser #(
    .TDATA_WIDTH (TDATA_WIDTH), .BIG_ENDIAN (0), .N_STREAMS (N_STREAMS)
  ) avtp_rx_parser (
    .clk (axis_clk), .resetn (axis_resetn),
    .cfg_stream_id_i (strtbl_sid_w),
    .cfg_stream_en_i (strtbl_en_w),
    //! PRE-FILTER tap: an accepted AVTP stream is a fabric-media input and must
    //! not depend on the station-address policy applied to protocol observers.
    .s_tdata_i  (rx_axis_from_mac.tdata),
    .s_tkeep_i  (rx_axis_from_mac.tkeep),
    .s_tvalid_i (rx_axis_from_mac.tvalid),
    .s_tready_i (rx_axis_from_mac.tready),
    .s_tlast_i  (rx_axis_from_mac.tlast),
    .match_valid_o (avtprx_match),
    .match_index_o (avtprx_idx),
    .stream_id_o   (avtprx_sid_frame),
    .avtp_ts_o     (avtprx_ts),
    .subtype_o     (avtprx_subtype),
    .ts_valid_o    (avtprx_tv_bit),
    .media_restart_o(avtprx_mr_bit),
    .seq_num_o     (avtprx_seq),
    .ts_uncertain_o(avtprx_tu_bit),
    .fsh_o         (avtprx_fsh),
    .fsh2_o        (avtprx_fsh2),
    .parse_valid_o (avtprx_parse_p),
    .b3_o          (avtprx_b3),
    .avtp_frames_o (aprb_parsed_w),
    .matched_frames_o (aprb_matched_w)
  );

  // ==========================================================================
  //  RX parser probe (APRB CSR group 0x8B4, 2026-07-26). Every other RX
  //  counter in this datapath lives DOWNSTREAM of the stream-table match
  //  (AVTPRX_*, PCMRX_*): when a bound listener accepts nothing they all
  //  read 0 and say nothing about why. These words are the pre-match view -
  //  how many AVTP frames the parser saw, how many matched an armed table
  //  entry, and the stream_id it actually lifted off the wire for the last
  //  STREAM-subtype frame (subtype[7]=0; control subtypes ADP/ACMP/MAAP are
  //  excluded so they cannot overwrite the media evidence).
  // ==========================================================================
  //! DPROBES_P (docs/design/AREA_BUDGET.md, 2026-07-29): the
  //! APRB/PBK groups are closed-finding diagnostics (fabric-listener
  //! blocker + item-7 chain, both TB-pinned since); a build that prunes
  //! them reads the whole 0x8B4-0x8D0 range as 0 - the LTAP precedent, an
  //! absent block declares itself. Counting/latching logic dies with it.
  generate if (DPROBES_P != 0) begin : g_aprb
    logic [63:0] aprb_sid_r;      //! stream_id of the last stream-subtype frame
    logic [7:0]  aprb_subtype_r;  //! its subtype
    logic        aprb_hit_r;      //! did that frame match a table entry
    logic [3:0]  aprb_idx_r;      //! matched entry index (valid with aprb_hit_r)
    logic [7:0]  aprb_armed_w;    //! table entries currently armed (live popcount)

    always_comb begin : aprb_armed_count
      aprb_armed_w = '0;
      for (int unsigned k = 0; k < N_STREAMS; k++)
        if (strtbl_en_w[k]) aprb_armed_w = aprb_armed_w + 8'd1;
    end : aprb_armed_count

    always_ff @(posedge axis_clk) begin : aprb_probe
      if (!axis_resetn) begin
        aprb_sid_r     <= '0;
        aprb_subtype_r <= '0;
        aprb_hit_r     <= 1'b0;
        aprb_idx_r     <= '0;
      end
      else if (avtprx_parse_p && !avtprx_subtype[7]) begin
        aprb_sid_r     <= avtprx_sid_frame;
        aprb_subtype_r <= avtprx_subtype;
        aprb_hit_r     <= avtprx_match;
        aprb_idx_r     <= 4'(avtprx_idx);
      end
    end : aprb_probe

    assign aprb_regs_w[32*0 +: 32] = aprb_parsed_w;
    assign aprb_regs_w[32*1 +: 32] = aprb_matched_w;
    assign aprb_regs_w[32*2 +: 32] = aprb_sid_r[31:0];
    assign aprb_regs_w[32*3 +: 32] = aprb_sid_r[63:32];
    assign aprb_regs_w[32*4 +: 32] = {8'd0, aprb_armed_w, 3'd0, aprb_idx_r,
                                      aprb_hit_r, aprb_subtype_r};
  end else begin : g_no_aprb
    assign aprb_regs_w = '0;
  end endgenerate

  // ==========================================================================
  //  CRF Media Clock Input engine (Milan 7.3.2) - measurement half: parses
  //  and validates the Avnu Pro Audio CRF stream selected by the CRF CSRs,
  //  produces the phase/frequency error the media-clock servo consumes and
  //  the CLOCK_DOMAIN lock events for clock_source = CRF. The ACMP sink-1
  //  remaining CRF integration gaps are recorded in
  //  docs/testing/MILAN_V12_AUDIT_2026-08-16.md B3 and B4.
  // ==========================================================================
  KL_crf_rx #(
    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ),
    .IVAL_CYC_P    (LDIAG_IVAL_CYC_P)
  ) crf_rx (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    //! the RAW parse strobe, deliberately UNGATED by the stopped state:
    //! Milan 5.3.8.7's verb is discard, not ignore, and 5.3.8.10 defines
    //! Table 5.6 counters on AVTPDUs "received on this Stream Input" - so a
    //! stopped, bound CRF sink keeps matching, validating and counting.
    .frame_p_i   (avtprx_parse_p),
    .subtype_i   (avtprx_subtype),
    .seq_i       (avtprx_seq),
    .sid_frame_i (avtprx_sid_frame),
    .pullbase_i  (avtprx_ts),
    .fsh_i       (avtprx_fsh),
    .fsh2_i      (avtprx_fsh2),
    .type_i      (avtprx_b3),
    .mr_i        (avtprx_mr_bit),
    //! IEEE 1722-2016 10.4.3's second duty for that bit: the restart the
    //! outgoing streams have to echo. Consumed by mcr_restart_p_w above,
    //! under the clock-source gate the clause itself scopes it with.
    .mr_toggle_p_o (crf_mr_toggle_p_w),
    //! IEEE 1722-2016 10.4.5: the CRF ALTERNATIVE header puts tu at frame
    //! byte o+1 bit 0 - the bit the parser publishes as tv for the common
    //! stream header. avtprx_tu_bit (byte o+3 bit 0) is the CRF `type`
    //! field's LSB and would read 1 on every conformant CRF_AUDIO_SAMPLE
    .tu_i        (avtprx_tv_bit),
    .ptp_now_i   (ptp_now_w),
    //! ACMP sink-1 bind wins; the CSR pair stays the manual bench lever
    .en_i        (cfg_crf_en | acmpl1_bound),
    .sid_i       (acmpl1_bound ? acmpl1_sid : cfg_crf_sid),
    //! Milan 5.3.8.7 STOP for this descriptor gates CONSUMPTION inside the
    //! module (lock machinery + the 10.4.3 restart echo), never observation.
    //! This sink has no classification-table entry (it keys on subtype, off
    //! the parser), so the listener accept gate above cannot reach it and
    //! the predicate arrives on its own port. It costs nothing in normal
    //! operation: the state is `bound & ~started`, a bind lands started
    //! unless the BIND_RX asked for STREAMING_WAIT, and an unbound CRF sink
    //! is outside the clause and ungated - a controller command aimed at
    //! this descriptor on purpose, not a command in the path of clock
    //! recovery.
    .stop_i      (crf_snk_stopped_w),
    .delta_o     (crf_delta_w),
    .rate_o      (crf_rate_w),
    .pdu_count_o (crf_pducnt_w),
    .fmt_err_o   (crf_fmterr_w),
    .seq_err_o   (crf_seqerr_w),
    //! Milan Table 5.16's CRF Media Clock Input counters are not connected to
    //! the current solicited gather face. Leave the unserved outputs open rather
    //! than create a shadow with no reader. The three values that do reach local
    //! software keep their CSR window below (0x738: pdu, fmt_err, seq_err).
    .mr_cnt_o    (),
    .tu_cnt_o    (),
    .late_cnt_o  (),
    .early_cnt_o (),
    .locked_o    (crf_locked_w),
    .cnt_locked_o   (),
    .cnt_unlocked_o (),
    .cnt_intr_o     (),
    //! The CRF sink's Table 5.22 dirty source is also unconnected. The
    //! processor has registration support, but the rate-limited counter-change
    //! scheduler does not yet consume this source.
    .dirty_p_o      ()
  );

  // ==========================================================================
  //  CRF media-clock recovery ACTUATOR (Milan 7.3.4): the audio-MMCM servo.
  //  The actuator can consume the KL_crf_rx rate measurement, but the current
  //  root hardwires INTERNAL against NONE and cannot select it. If selected by
  //  a future dynamic root connection, it steers the SoC audio MMCM through
  //  the UG472 fine-phase-shift port
  //  (ppm-fine, glitch-free) + the XAPP888 DRP engine (verified divider
  //  reprogramming, reset-sequenced). auto_repair defaults OFF for silicon
  //  bring-up (MCSRV_CTRL 0x8FC[1] resets 0): the DRP limb read-verifies but
  //  never writes until the bench confirms the expected ClkReg encoding (see
  //  the module header) and sets 0x8FC[1] = 1. TB: tb/verilator/
  //  mmcm_servo_autorepair (47/47) proves the enabled repair path.
  // ==========================================================================
  //! MCSERVO_P = 0 prunes the servo (see the parameter note). The tie-off is
  //! the servo's own IDLE state, term by term: it drives drp_en/we = 0 and
  //! ps_en = 0 while CRF is unselected, and mmcm_rst_o is asserted only
  //! inside a REPAIR sequence that a pruned build never enters. status_o = 0
  //! makes A_MCSRV_STAT 0x8F8 a STRUCTURAL zero - REGISTER_MAP records that
  //! this window already has a dead-read carve-out, so a reader cannot tell
  //! "no servo built" from "servo idle" there and must not try.
  generate if (MCSERVO_P != 0) begin : g_mmcm_servo
  KL_mmcm_drp_servo #(.CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ)) mmcm_servo (
    .clk_i         (axis_clk),
    .rst_n         (axis_resetn),
    .clk_audio_i   (clk_audio_i),
    .ps_clk_i      (i_ps_clk),
    .ptp_now_i     (ptp_now_w),
    //! servo_sel_w is (clk_src_i == crf_src_idx_i) INSIDE the servo, and
    //! both sides are LIVE now (#74): the stored selection against this
    //! shape's generated CRF index. On a shape with no CRF source the
    //! generated index is 16'hFFFF - the AEM no-descriptor value the live
    //! index can never store - so the select stays structurally false there,
    //! which is the same trap-proofing the old constant pair encoded.
    .clk_src_i     (media_clk_src_r),
    .crf_src_idx_i (AEM_CRF_CLKSRC_C),
    .crf_locked_i  (crf_locked_w),
    .crf_rate_i    (crf_rate_w),
    .auto_repair_i (mcsrv_auto_repair_w),
    .ps_invert_i   (mcsrv_ps_invert_w),
    .drp_addr_o    (o_mmcm_drp_addr),
    .drp_en_o      (o_mmcm_drp_en),
    .drp_we_o      (o_mmcm_drp_we),
    .drp_di_o      (o_mmcm_drp_di),
    .drp_do_i      (i_mmcm_drp_do),
    .drp_rdy_i     (i_mmcm_drp_rdy),
    .mmcm_rst_o    (o_mmcm_rst),
    .mmcm_locked_i (i_mmcm_locked),
    .ps_en_o       (o_mmcm_ps_en),
    .ps_incdec_o   (o_mmcm_ps_incdec),
    .ps_done_i     (i_mmcm_ps_done),
    .status_o      (mcsrv_stat_w)
  );
  end else begin : g_no_mmcm_servo
    assign o_mmcm_drp_addr  = 7'd0;
    assign o_mmcm_drp_en    = 1'b0;
    assign o_mmcm_drp_we    = 1'b0;
    assign o_mmcm_drp_di    = 16'd0;
    assign o_mmcm_rst       = 1'b0;
    assign o_mmcm_ps_en     = 1'b0;
    assign o_mmcm_ps_incdec = 1'b0;
    assign mcsrv_stat_w     = 32'd0;
  end endgenerate

  // --------------------------------------------------------------------------
  //  ONE GRID, AS A CHAIN (#74 - the actuator seam, rewritten).
  //
  //  The previous wiring here handed the NCO the MMCM servo's own command
  //  ("one error signal, two actuators"), which kept the two actuators from
  //  diverging in RESPONSE but could never close their NOMINAL gap: the
  //  physical grid is clk_tdm through an integer divider (47,999.4893 Hz on
  //  the shipping plan) and the packet grid was an exact 48,000.0000 Hz, so
  //  a shared command moved both by the same ppm and left the -10.64 ppm
  //  difference - one slipped sample every 1.96 s at the capture holds -
  //  fully intact. That residual is the "independent-divider drift" issue
  //  #74 names, and its bounded-phase-alignment branch is what lands here.
  //
  //  The one-grid rule now holds in its strongest form, as a CHAIN with one
  //  master per link: CRF -> KL_mmcm_drp_servo -> the physical audio clock
  //  and its fsync grid -> KL_media_grid_align -> the packet grid. The MMCM
  //  consumes the CRF rate error and publishes its command on
  //  A_MCSRV_STAT[31:16] (that slice is the MMCM's alone now - the CRF arm
  //  in tb/verilator/milan_dp grades it non-zero under CRF stimulus); the
  //  align loop consumes the FRAME MARKER the front-end already delivers in
  //  this clock domain (aafcap slot-0, the same event the junction counters
  //  key on) and holds the packet grid inside a fraction of a sample of the
  //  physical one - proven closed-loop at the true 391/1591 ratio in
  //  tb/verilator/media_grid_align, both rate directions, zero junction
  //  slips.
  //
  //  INTERNAL. clock_source 0 is free-run by USER rule ("internal media
  //  clock = free-run, slips accepted"): crf_clk_selected_r low disengages
  //  the align loop entirely and the grid is bit-for-bit the divider that
  //  shipped at 0x0040, so every bench measurement on record stands. The
  //  junction slip counters keep counting there - the INTERNAL slip is
  //  accepted, not hidden.
  // --------------------------------------------------------------------------
  wire        mga_engaged_w /* verilator public_flat_rd */;
  wire signed [15:0] mga_err_w /* verilator public_flat_rd */;
  KL_media_grid_align #(
    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ),
    .FS_HZ_P       (48_000)
  ) media_grid_align (
    .clk_i      (axis_clk),
    .rst_n      (axis_resetn),
    .sel_i      (crf_clk_selected_r),
    .frame_ev_i (aafcap_pv_w && (aafcap_slot_w == 4'd0)),
    .tick_i     (media_tick_p),
    .u_o        (mnco_servo_trim_w),
    .engaged_o  (mga_engaged_w),
    .err_o      (mga_err_w)
  );
  assign mnco_servo_en_w = crf_clk_selected_r;

  // ==========================================================================
  //  CRF Media Clock Output engine (Milan 7.3.1) - talker half: emits the
  //  Avnu Pro Audio CRF stream (500 PDU/s) with gPTP timestamps captured on
  //  the REAL audio-MMCM 96-sample event grid. Joins the low-rate control
  //  merge untagged (no MSRP TA yet - see the module header).
  // ==========================================================================
  KL_crf_tx crf_tx (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .clk_audio_i (clk_audio_i),
    //! licence-gated, never the bare CSR bit: see crft_emit_en_w
    .enable_i      (crft_emit_en_w),
    .sid_i         (eff_crft_sid_w),
    .dest_mac_i    (eff_crft_dmac_w),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    //! Milan: the presentation time offset applies to CRF like any stream -
    //! same source of truth as the AAF framers (SET_STREAM_INFO ACC_LAT/
    //! MTT), reading ITS OWN per-STREAM_OUTPUT entry: the CRF output is
    //! talker_unique_id CRF_TUID_C = N_STREAMS. Shapes without a CRF
    //! output leave the entry at its 2 ms default and cfg_crft_en low.
    .transit_ns_i  (aecp_pres_offset[32*CRF_TUID_C +: 32]),
    .ptp_ns_i      (ptp_now_w),
    .ts_uncertain_i (clkv_tu_w),
    //! IEEE 1722-2016 10.4.3 mr: the level KL_media_clock_restart grants this
    //! Stream Output, and the level the last completed PDU carried going back
    //! to it (the eight-PDU hold counts transmitted PDUs, not grants)
    .mr_i          (crft_mr_w),
    .tu_last_o     (crft_tu_last_w),
    .mr_last_o     (crft_mr_last_w),
    //! SR class A C-TAG. vlan_en is the RESERVATION's shadow, never a bare
    //! CSR bit: see crf_srp_prov / crft_class_a_w. {PCP, VID} come from
    //! crft_{pcp,vid}_w - the OPERATIONAL Domain pair while adopted (Milan
    //! 4.2.7.2.1), LWSRP_VID/priority-3 defaults otherwise - literally the
    //! same pair KL_lwsrp_ctx_tx puts in this stream's Talker Advertise
    //! DataFrameParameters (802.1Q 35.2.2.4), so the frame and the
    //! declaration name one VLAN by construction.
    .vlan_en_i  (crft_class_a_w),
    .vlan_pcp_i (crft_pcp_w),
    .vlan_vid_i (crft_vid_w),
    .m_axis_tdata (crft_tx_tdata), .m_axis_tkeep (crft_tx_tkeep),
    .m_axis_tvalid(crft_tx_tvalid), .m_axis_tlast (crft_tx_tlast),
    .m_axis_tready(crft_tx_tready),
    .tx_count_o (crft_count_w)
  );

  //! wire-truth channel count (USER 1-to-1 rule): the RENDER path follows
  //! the last accepted PDU's channels_per_frame, never the AEM store
  wire [7:0] mon_wire_chans_w;
  wire [N_STREAMS*4-1:0] mon_wire_chans_all_w;   //! per-stream (follow-up 3)

  //! NXN P2: the shared monitor engine (LCTX context RAM, N_STREAMS
  //! contexts) replaces the flat single-stream KL_avtp_rx_monitor. All
  //! legacy 0x6B8-group wires alias stream 0 (no-regression axiom); the
  //! LCTX window port serves the 0x800 CSR window (P12).
  wire        avtprx_accept_p_w;
  wire [3:0]  avtprx_accept_idx_w;
  wire        pcmrx_pdu_p_w, pcmrx_drop_p_w;
  wire [3:0]  pcmrx_pdu_idx_w, pcmrx_drop_idx_w;
  //! Milan v1.2 §5.3.8.7: "A PAAD-AE having a stopped Stream Input shall
  //! DISCARD the Stream AVTPDUs it receives." The discard belongs HERE, on
  //! the accept pulse that feeds the depacketizer, not on the classification
  //! entry upstream - because the clause's own wording says a stopped input
  //! RECEIVES. Table 5.6 defines FRAMES_RX, SEQ_NUM_MISMATCH, LATE/EARLY_
  //! TIMESTAMP and the rest on frames "received on this Stream Input", so
  //! they go on counting while the media path gets nothing;
  //! `KL_avtp_rx_monitor_ctx` sits upstream of this gate for exactly that
  //! reason. Gating the classifier instead ALSO forged a not-bound->bound
  //! edge on the next start, and Table 5.6 makes that edge the counter-reset
  //! event - so a stop/start pair wiped every counter on a sink that never
  //! unbound.
  //! selected without a variable bit-select: `avtprx_accept_idx_w` is four
  //! bits and this vector is ACMP_SINKS_C wide, so indexing it directly is a
  //! width truncation Verilator is right to flag.
  logic avtprx_stopped_w;
  always_comb begin : accept_stop_sel
    avtprx_stopped_w = 1'b0;
    for (int unsigned k = 0; k < ACMP_SINKS_C; k++) begin
      if (32'(avtprx_accept_idx_w) == k) avtprx_stopped_w = acmpl_stopped_v_w[k];
    end
  end : accept_stop_sel

  assign avtprx_accept_p = avtprx_accept_p_w && !avtprx_stopped_w;

  KL_avtp_rx_monitor_ctx #(
    .N_LISTENERS_P (N_STREAMS),
    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ),
    .IVAL_CYC_P    (LDIAG_IVAL_CYC_P)
  ) avtp_rx_monitor (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .match_valid_i  (avtprx_match),
    .match_index_i  (4'(avtprx_idx)),
    .subtype_i      (avtprx_subtype),
    .seq_num_i      (avtprx_seq),
    .ts_uncertain_i (avtprx_tu_bit),
    .ts_valid_i     (avtprx_tv_bit),
    .media_restart_i(avtprx_mr_bit),
    .avtp_ts_i      (avtprx_ts),
    .fsh_i          (avtprx_fsh),
    .bound_i        (strtbl_en_w),
    .bind_rise_i    (strtbl_bind_rise_w),
    .bind_fall_i    (strtbl_bind_fall_w),
    .sid0_i         (acmpl_sid),
    .fmt0_i         (aecp_in0_fmt),
    .ptp_now_i      (ptp_now_w[31:0]),
    //! LISTENER-side presentation window, deliberately entry 0 (the
    //! index-0/global value, exactly what this port has always been fed):
    //! pres_ofs_i scales the RX monitor's LATE/EARLY acceptance window and
    //! is a property of OUR sink, not of any talker's transit time - the
    //! per-index file above is TALKER state (per STREAM_OUTPUT), so keying
    //! this by a talker index would conflate the two. A per-SINK window
    //! is future LCTX work, not a per-talker mux.
    .pres_ofs_i     (aecp_pres_offset[31:0]),
    //! LIVE wiring, INERT consumer (#74, [R1] finding 2): the monitor
    //! declares these ports for a media-lock rule it does not implement
    //! yet - clk_src_i/servo_conv_i are folded unused inside. Wired live
    //! anyway, like i2s_playback's servo_en_i below, so the day the rule
    //! lands the truth is already at the port and no root edit can be
    //! forgotten. No behavior rides on this today.
    .clk_src_i      (media_clk_src_r),
    .servo_conv_i   (i2spb_converged),
    .render_sel_i   (route_render_sel_w),  //! route policy's RENDER stream
    .depkt_pdu_p_i    (pcmrx_pdu_p_w),
    .depkt_pdu_idx_i  (pcmrx_pdu_idx_w),
    .depkt_drop_p_i   (pcmrx_drop_p_w),
    .depkt_drop_idx_i (pcmrx_drop_idx_w),
    //! P12: LCTX window port <- the CSR 0x800 window (listener dir)
    .lctx_wr_en_i (csr_lctx_wr_p_w), .lctx_wr_addr_i (csr_lctx_wr_addr_w),
    .lctx_wr_data_i (lctx_wr_data_sane_w), .lctx_wr_rdy_o (lctx_wr_rdy_w),
    .lctx_rd_en_i (csr_lctx_rd_en_w), .lctx_rd_addr_i (csr_lctx_rd_addr_w),
    .lctx_rd_data_o (lctx_rd_data_w), .lctx_rd_valid_o (lctx_rd_valid_w),
    .cnt_media_locked_o       (avtprx_locked_c),
    .cnt_media_unlocked_o     (avtprx_unlocked_c),
    .cnt_stream_interrupted_o (avtprx_intr_c),
    .cnt_seq_mismatch_o       (avtprx_seqmm_c),
    .cnt_ts_uncertain_o       (avtprx_tu_c),
    .cnt_unsupported_fmt_o    (avtprx_unsupp_c),
    .cnt_frames_rx_o          (avtprx_frx_c),
    .wire_chans_o             (mon_wire_chans_w),
    .wire_chans_all_o         (mon_wire_chans_all_w),
    //! Milan 5.4.2.25: every sink's Table 5.6 set, muxed by the AECP's
    //! GET_COUNTERS descriptor index
    .diag_idx_i               (aecp_diag_idx_w),
    //! Milan Table 5.16 STREAM_INPUT counters, muxed by diag_idx_i above.
    //! Its reader is the protocol processor's GET_COUNTERS face; the 0x6B8
    //! A_STRMW_CNT CSR window is served from the per-context counters beside
    //! it, NOT from this port, so the two views are independent readers of
    //! the same flops and a divergence between them is a real defect.
    .diag_cnt_o               (mon_diag_cnt_w),
    .cnt_media_reset_o (avtprx_mreset_c),
    .cnt_late_ts_o     (avtprx_late_c),
    .cnt_early_ts_o    (avtprx_early_c),
    .cnt_ts_valid_o     (avtprx_tv_c),
    .cnt_ts_not_valid_o (avtprx_tnv_c),
    .media_locked_o (avtprx_locked),
    //! per-sink Table 5.22 counter-change pulses, one STREAM_INPUT source
    //! of the pp_ctr_event arbiter below (the processor's GET_COUNTERS push)
    .dirty_p_o      (avtprx_dirty_p_w),
    .pdu_accept_p_o   (avtprx_accept_p_w),
    .pdu_accept_idx_o (avtprx_accept_idx_w),
    .last_ts_o      (avtprx_last_ts),
    .last_tsd_o     (avtprx_last_tsd)
  );

  // ==========================================================================
  //  AAF RX depacketizer (listener media path) — same RX tap; the monitor's
  //  accept pulse is the commit verdict, so fabric render receives exactly
  //  the PDUs FRAMES_RX counts. Payload leaves as full 8-byte beats in wire
  //  order (S32BE interleaved) toward the render path.
  // ==========================================================================
  KL_aaf_rx_depacketizer aaf_rx_depkt (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    //! pre-filter tap - see avtp_rx_parser note
    .s_tdata_i  (rx_axis_from_mac.tdata),
    .s_tkeep_i  (rx_axis_from_mac.tkeep),
    .s_tvalid_i (rx_axis_from_mac.tvalid),
    .s_tready_i (rx_axis_from_mac.tready),
    .s_tlast_i  (rx_axis_from_mac.tlast),
    .pdu_accept_p_i (avtprx_accept_p),
    //! NXN §1.1 tuser tag: the shared monitor's per-stream accept index
    .pdu_accept_idx_i (avtprx_accept_idx_w),
    .m_axis_tdata (dpkt_pcm_tdata_w),
    .m_axis_tkeep (), //! Listener PCM output is always a full 8-byte beat.
    .m_axis_tvalid(dpkt_pcm_tvalid_w),
    .m_axis_tlast (dpkt_pcm_tlast_w),
    .m_axis_tuser (dpkt_pcm_tuser_w),
    .m_axis_tready(dpkt_pcm_tready_w),
    .pdus_o  (pcmrx_pdus),
    .drops_o (pcmrx_drops),
    .pdu_out_p_o (pcmrx_pdu_p_w), .pdu_out_idx_o (pcmrx_pdu_idx_w),
    .drop_p_o (pcmrx_drop_p_w), .drop_idx_o (pcmrx_drop_idx_w)
  );

  // ==========================================================================
  //  PCM routing policy — per-stream route field between the shared
  //  depacketizer and fabric render. Bit 1 enables RENDER (lowest-indexed
  //  wins); bit 0 is a reserved-zero ABI position. Writes arrive from the
  //  listener-window CTRL[2:1] commit (wing glue above).
  // ==========================================================================
  wire [TDATA_WIDTH-1:0] dpkt_pcm_tdata_w;
  wire                   dpkt_pcm_tvalid_w, dpkt_pcm_tlast_w;
  wire [3:0]             dpkt_pcm_tuser_w;
  wire                   dpkt_pcm_tready_w;

  //! task #65: drive the capture crossbar's LOOP bucket (declared far above,
  //! at its point of use). A CLONE, never a consumer - the strobe is the
  //! ACCEPTED beat (tvalid && tready) and no tready comes back, so the rx
  //! chain's flow control is untouched and this tap cannot stall a listener.
  //! Identical discipline to KL_chan_map_render's tap below; that module is
  //! why the clone is safe to take twice.
  //! LOOPBACK_P = 0 folds the strobe to a constant 0, which prunes the hold
  //! bank and its read mux to nothing - the behaviour the shipping bitstream
  //! already had, since the bucket was never fed there either.
  assign lb_tap_tdata_w  = dpkt_pcm_tdata_w;
  assign lb_tap_tvalid_w = (LOOPBACK_P != 0)
                           && dpkt_pcm_tvalid_w && dpkt_pcm_tready_w;
  assign lb_tap_tlast_w  = dpkt_pcm_tlast_w;
  assign lb_tap_tuser_w  = dpkt_pcm_tuser_w;
  //! per-stream wire channels_per_frame (1722-2016 7.3.3), the LIVE value
  //! each RX monitor decoded - so the bucket de-interleaves a 2ch stream as
  //! 2ch and an 8ch stream as 8ch, exactly like the render crossbar.
  assign lb_tap_chans_w  = mon_wire_chans_all_w[LB_STREAMS_C*4-1:0];
  wire [TDATA_WIDTH-1:0] rend_pcm_tdata_w;
  //! render-tap valid is TB-observable (route-flag truth in sim_nxn)
  wire                   rend_pcm_tvalid_w /* verilator public_flat_rd */;
  wire                   rend_pcm_tlast_w;
  wire [3:0]             route_render_sel_w;

  KL_pcm_route #(
    .N_LISTENERS_P (N_STREAMS)
  ) pcm_route (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_tdata_i (dpkt_pcm_tdata_w), .s_tvalid_i (dpkt_pcm_tvalid_w),
    .s_tlast_i (dpkt_pcm_tlast_w), .s_tuser_i (dpkt_pcm_tuser_w),
    .s_tready_o (dpkt_pcm_tready_w),
    //! P12: route field <- the window CTRL[2:1] commit (glue above)
    .route_wr_en_i (wing_route_we_r), .route_wr_idx_i (wing_idx_r),
    .route_wr_val_i (wing_route_r),
    .render_tvalid_o (rend_pcm_tvalid_w), .render_tdata_o (rend_pcm_tdata_w),
    .render_tlast_o (rend_pcm_tlast_w),
    .render_sel_o (route_render_sel_w), .render_active_o ()
  );

  // ==========================================================================
  //  I2S playback (Pmod I2S2 DAC) — zero-CPU audible listener: taps the
  //  depacketizer PCM transfers and serializes ch0/ch1 on the line-out.
  //  Free-running local 48 kHz (MVP): drift vs the talker is absorbed by
  //  the FIFO rails and MEASURED via I2SPB_STAT until CRF media-clock
  //  discipline lands.
  // ==========================================================================
  //! 2nd-order Butterworth LPF on the DAC render tap only (AVB data stays
  //! bit-true): band-limits the analog output feeding the
  //! loop ADC. LPF_CTRL 0x72C[0], default on; auto-bypass for !=2ch.
  //! render tap = the route policy's selected RENDER stream.
  //! LPF_P = 0 prunes the filter (see the parameter's note). The tie-off is
  //! the runtime-bypass state, term by term: active_o = 0 makes
  //! KL_i2s_playback take the RAW AXIS path, and m_tvalid = 0 means the
  //! lpf_tdata port it then ignores never strobes - exactly what
  //! LPF_CTRL[0] = 0 produces today.
  generate if (LPF_P != 0) begin : g_pcm_lpf
    KL_pcm_lpf pcm_lpf (
      .clk_i (axis_clk), .rst_n (axis_resetn),
      .enable_i (cfg_lpf_enable),
      .chans_i  ({2'b0, mon_wire_chans_w}),   //! wire truth (2ch engages)
      .s_tdata  (rend_pcm_tdata_w),
      .s_tvalid (rend_pcm_tvalid_w),
      .s_tready (1'b1), //! The filter observes a clone and cannot stall routing.
      .m_tdata  (pcm_lpf_tdata),
      .m_tvalid (pcm_lpf_tvalid),
      .active_o (pcm_lpf_active)
    );
  end else begin : g_no_pcm_lpf
    assign pcm_lpf_tdata  = 64'd0;
    assign pcm_lpf_tvalid = 1'b0;
    assign pcm_lpf_active = 1'b0;
  end endgenerate

  //! item-7 DAC feed selector (KL_i2s_feed_mux, instanced with the render
  //! fabric below - nets resolve module-wide): CHMAP_CTRL[0]=0 passes the
  //! compliance render tap through BIT- and CYCLE-identically; =1 selects the
  //! render crossbar's phys{0,1} pair paced by the 48 kHz media tick (and
  //! masks the LPF, which belongs to the listener tap it filters).
  wire [TDATA_WIDTH-1:0] i2s_feed_tdata_w;
  wire                   i2s_feed_tvalid_w, i2s_feed_tready_w, i2s_feed_tlast_w;
  wire [7:0]             i2s_feed_chans_w;
  wire                   i2s_feed_lpf_act_w;

  //! I2SPB_P = 0 prunes the DAC serializer (see the parameter note). The
  //! tie-off is what a board with no DAC already shows: the four i2s_dac_*
  //! pins park low (the shipping serializer holds sclk/lrck/sdin at 0 until
  //! the first prefilled frame, which never arrives without a DAC to clock),
  //! every I2SPB counter reads 0 and converged
  //! stays 0 - the identical set of values the block presents before its
  //! first stream. It does NOT backpressure: the render tap is a clone tap,
  //! so pruning the sink cannot stall the listener path.
  generate if (I2SPB_P != 0) begin : g_i2s_player
  //! task #22 (USER 08-06, measured 2 min): a grandmaster change means
  //! the PHC - the presentation timebase - may just have STEPPED by
  //! seconds. Nothing in the media path reacted, so the playback FIFO
  //! walked back into its convergence band at the residual rate error.
  //! One pulse per GM-identity change re-centers it instead; the first
  //! fabric GM publication out of reset (0 -> id) is exempt
  //! (prefill owns boot).
  logic [63:0] gm_recentre_q_r;
  logic        gm_recentre_p_r;
  always_ff @(posedge axis_clk) begin : g_gm_recentre
    if (!axis_resetn) begin
      gm_recentre_q_r <= '0;
      gm_recentre_p_r <= 1'b0;
    end else begin
      gm_recentre_q_r <= cfg_adp_gptp_gm;
      gm_recentre_p_r <= (cfg_adp_gptp_gm != gm_recentre_q_r) &&
                         (gm_recentre_q_r != 64'd0);
    end
  end : g_gm_recentre

  KL_i2s_playback #(.MCLK_DIV_LOG2(MCLK_DIV_LOG2_C),
                    .CLK_FREQ_HZ(MILAN_CLK_FREQ_HZ),
                    .PREFILL_C(PB_PREFILL_C),
                    //! task #28 (USER: constant source-invariant latency,
                    //! samples picked as soon as possible): the setpoint =
                    //! the packetization floor - one class-A frame of this
                    //! stereo lane (6 events x 2 samples = 12) plus a
                    //! 4-sample CDC/jitter allowance = 16 samples (8 pairs,
                    //! ~167 us at 48 kHz), inside the USER 125-200 us band.
                    //! DERIVED from the frame shape, not a mirrored literal.
                    .SETPOINT_P((6 * 2) + 4)) i2s_player (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .clk_audio_i  (clk_audio_i),
    .servo_en_i   (crf_clk_selected_r),
    .recenter_p_i (gm_recentre_p_r),
    .pcm_tdata_i  (i2s_feed_tdata_w),
    .lpf_tdata_i  (pcm_lpf_tdata),
    .lpf_tvalid_i (pcm_lpf_tvalid),
    .lpf_active_i (i2s_feed_lpf_act_w),
    .pcm_tvalid_i (i2s_feed_tvalid_w),
    .pcm_tready_i (i2s_feed_tready_w),
    .pcm_tlast_i  (i2s_feed_tlast_w),
    .wire_chans_i (i2s_feed_chans_w),
    .i2s_mclk_o (i2s_dac_mclk_o), .i2s_sclk_o (i2s_dac_sclk_o),
    .i2s_lrck_o (i2s_dac_lrck_o), .i2s_sdin_o (i2s_dac_sdin_o),
    .clr_under_i (cfg_i2spb_clru), .clr_over_i (cfg_i2spb_clro),
    .underruns_o (i2spb_underruns), .overruns_o (i2spb_overruns),
    .trim_o (i2spb_trim), .fill_o (i2spb_fill),
    //! the playback buffer's overrun/underrun rail is LOCAL health, not the
    //! Milan Table 5.6 MEDIA_RESET trigger (that is the received mr bit, see
    //! KL_avtp_rx_monitor_ctx); it stays counted by I2SPB_STAT's own
    //! underrun/overrun tallies, which is where a local rail belongs
    .media_reset_p_o (),
    .converged_o     (i2spb_converged),
    .dbg_frame_o     (i2spb_dbg_frame)
  );
  end else begin : g_no_i2s_player
    assign i2s_dac_mclk_o  = 1'b0;
    assign i2s_dac_sclk_o  = 1'b0;
    assign i2s_dac_lrck_o  = 1'b0;
    assign i2s_dac_sdin_o  = 1'b0;
    assign i2spb_underruns = 16'd0;
    assign i2spb_overruns  = 16'd0;
    assign i2spb_trim      = 16'sd0;
    assign i2spb_fill      = 16'd0;
    assign i2spb_converged = 1'b0;
    assign i2spb_dbg_frame = 32'd0;
  end endgenerate

  // ==========================================================================
  //  Channel-map RENDER crossbar (docs/CHANNEL_MAP_64.md §3) — ADD-ALONGSIDE.
  //  A parallel, NEVER-backpressuring tap on the depacketizer PCM AXIS: it
  //  latches every (stream, wire-channel) sample and, on each media tick,
  //  renders CHMAP_PHYS_C physical channels through RMAP. phys{0,1} feed the
  //  optional mapped-I2S path above; phys{2..9} feed the parked TDM8 render
  //  lane. cfg_chmap_enable = 0 leaves rend_pcm_tdata_w -> i2s_playback
  //  untouched (the assign below resolves to the exact compliance net).
  // ==========================================================================
  localparam int CHMAP_PHYS_C = 10;
  wire [CHMAP_PHYS_C*24-1:0] chmap_phys_w;
  wire                       chmap_phys_v_w;
  wire [CHMAP_PHYS_C-1:0]    chmap_mapped_mask_w;
  //! the whole render map, exported for the GET_AUDIO_MAP page walk (the
  //! single map_rd_* readback port stays the CSR CHMAP_SNAP path's - two
  //! independent readers of the same flops, by construction)
  wire [CHMAP_PHYS_C*8-1:0]  rmap_flat_w;

  KL_chan_map_render #(
    .N_STREAMS_P  (N_STREAMS),
    //! the rx wire-channel space, defined once beside the capture crossbar
    //! (RX_WIRE_CHANS_C) and read here - the LOOP bucket keeps the same
    //! space, and the two must not be able to drift apart
    .N_CH_P       (RX_WIRE_CHANS_C),
    .N_PHYS_P     (CHMAP_PHYS_C)
  ) chan_map_render (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    //! clone tap: accepted-beat strobe (tvalid && tready); never backpressures
    .s_tdata_i  (dpkt_pcm_tdata_w),
    .s_tvalid_i (dpkt_pcm_tvalid_w && dpkt_pcm_tready_w),
    .s_tlast_i  (dpkt_pcm_tlast_w),
    .s_tuser_i  (dpkt_pcm_tuser_w),
    //! per-stream LCTX wire-truth fan-out (follow-up 3 DONE: each stream
    //! de-interleaves by its OWN wire channels_per_frame)
    .wire_chans_i (mon_wire_chans_all_w),
    .tick_i (media_tick_p),
    //! write mux with the live AECP transaction leg and CSR 0x900 writer.
    //! The map key is the GLOBAL cluster index and the model may declare
    //! MORE input clusters than this board renders (8x8 = 64 keys against
    //! CHMAP_PHYS_C = 10), so an out-of-range key must be DROPPED, not
    //! truncated - truncation would silently alias key 16 onto the I2S L
    //! channel. KL_chan_map_render bounds its own write too; this gate is
    //! what stops the narrow address bus from wrapping before it gets there.
    //!
    //! BOTH arms need it. The CSR debug port carries the SAME 0..63 key
    //! space (A_CHMAP_SEL[5:0], cfg_chmap_wr_addr is 6 bits), so
    //! CHMAP_SEL = 16 truncated to [3:0] landed on phys 0 = the I2S L
    //! channel just as surely as an AEM key 16 would have - a bring-up poke
    //! at a cluster this board does not render would silently retune the
    //! DAC's left channel.
    //!
    //! The compares are 32-BIT, not 6'(CHMAP_PHYS_C): the literal is only
    //! six bits wide by accident of today's value 10, and 6'(64) is 0, so a
    //! future depth of 64 would turn the guard into "refuse everything".
    .map_wr_en_i   ((aecp_dmap_wr_p_w &&
                     32'(aecp_dmap_wr_addr_w) < CHMAP_PHYS_C) ||
                    (!aecp_dmap_wr_p_w && !amap_edit_txn_active_r
                     && !aecp_locked
                     && cfg_chmap_wr_en &&
                     !cfg_chmap_wr_side &&
                     cfg_chmap_rphys_w[6]
                     && (32'(cfg_chmap_rphys_w[5:0]) < CHMAP_PHYS_C))),
    .map_wr_addr_i (aecp_dmap_wr_p_w
                    ? aecp_dmap_wr_addr_w[$clog2(CHMAP_PHYS_C)-1:0]
                    : cfg_chmap_rphys_w[$clog2(CHMAP_PHYS_C)-1:0]),
    //! §5 16-bit word -> render 8-bit {en[7], src[6], idx[5:0]}. SRC[12] of
    //! the §5 word selects the source bank (0 = AVB listener {stream,ch});
    //! source 1 is retained as a reserved-zero ABI encoding. The AECP leg
    //! carries the already projected store word.
    .map_wr_data_i (aecp_dmap_wr_p_w ? aecp_dmap_wr_word_w
                    : {cfg_chmap_wr_data[15], cfg_chmap_wr_data[12],
                       cfg_chmap_wr_data[6:4], cfg_chmap_wr_data[2:0]}),
    //! map-RAM readback -> CSR 0x910/0x914. Combinational read port with no
    //! valid of its own; rmap_rd_valid_r above supplies the 1-clock valid.
    .map_rd_addr_i (cfg_chmap_rd_addr[$clog2(CHMAP_PHYS_C)-1:0]),
    .map_rd_data_o (rmap_rd_data_w),
    .map_flat_o (rmap_flat_w),
    .phys_smp_o (chmap_phys_w), .phys_valid_o (chmap_phys_v_w),
    .mapped_mask_o (chmap_mapped_mask_w)
  );

  // ---- DAC feed selector (item-7): the one place the DAC's source AND its
  //      pace are decided, and the one place the render chain is counted.
  //      enable=0 -> the compliance tap passes through bit-/cycle-identically;
  //      enable=1 -> phys{0,1} on the 48 kHz media tick (the ONLY pace at
  //      which mapped fabric playback reaches the line-out). -------------
  KL_i2s_feed_mux i2s_feed_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    //! The crossbar has no current boot seeder. The bring-up tap passes
    //! through unless CHMAP_CTRL[0] selects the CSR-programmed crossbar.
    .sel_render_i (aecp_dmap_dyn_w | cfg_chmap_enable),
    .tap_tdata_i  (rend_pcm_tdata_w),
    .tap_tvalid_i (rend_pcm_tvalid_w),
    .tap_tready_i (1'b1), //! The feed selector observes a non-blocking clone.
    .tap_tlast_i  (rend_pcm_tlast_w),
    .tap_chans_i  (mon_wire_chans_w),
    .lpf_active_i (pcm_lpf_active),
    .phys_l_i     (chmap_phys_w[0*24 +: 24]),
    .phys_r_i     (chmap_phys_w[1*24 +: 24]),
    .phys_valid_i (chmap_phys_v_w),
    .phys_armed_i (|chmap_mapped_mask_w[1:0]),
    .pcm_tdata_o (i2s_feed_tdata_w), .pcm_tvalid_o (i2s_feed_tvalid_w),
    .pcm_tready_o (i2s_feed_tready_w), .pcm_tlast_o (i2s_feed_tlast_w),
    .chans_o (i2s_feed_chans_w), .lpf_active_o (i2s_feed_lpf_act_w),
    .feeds_o (),   //! Optional selector activity diagnostic is not published.
    .unarmed_o (), //! Optional unarmed diagnostic is not published.
    .src_render_o () //! Optional source diagnostic is not published.
  );

  // ---- parked TDM8 render lane (docs §8): phys{2..9} -> 8 slot writes -------
  //! The render xbar emits the whole phys vector once per media tick; the TDM
  //! slave serializer wants slot-indexed writes + a frame commit. A tiny burst
  //! adapter walks phys{2..9} into the bank on each phys_valid, then commits.
  //! tdm_dout_o IS BONDED - AX7101 J11.5, ball A20, claimed by tdm_pads.dout
  //! on a master build (milan_soc.py:5233). What keeps the lane dark is the
  //! CLOCK, not the pin: KL_tdm_render is a bus SLAVE whose serializer runs on
  //! posedge tdm_bclk_i, and a MASTER build ties tdm_bclk_i/tdm_fsync_i to 0
  //! (milan_soc.py:751) because the master generates bclk/fsync on the OUTPUT
  //! side. There is no KL_tdm_render_master sibling - capture got one, render
  //! did not. So the adapter below fills the bank correctly and the bank never
  //! shifts. See the `render: 0` note in the AX7101 configs for the other two
  //! blockers (AEM_DMAP_PHYS_C key cap, CHMAP_PHYS_C blend layout).
  logic        tdmr_wr_en_r;
  logic [2:0]  tdmr_slot_r;
  logic [23:0] tdmr_data_r;
  logic        tdmr_tick_r;
  logic        tdmr_busy_r;
  always_ff @(posedge axis_clk) begin : chmap_tdm_adapter
    if (!axis_resetn) begin
      tdmr_wr_en_r <= 1'b0; tdmr_slot_r <= 3'd0; tdmr_data_r <= 24'd0;
      tdmr_tick_r  <= 1'b0; tdmr_busy_r <= 1'b0;
    end else begin
      tdmr_wr_en_r <= 1'b0;
      tdmr_tick_r  <= 1'b0;
      if (!tdmr_busy_r) begin
        if (chmap_phys_v_w) begin
          tdmr_busy_r  <= 1'b1;
          tdmr_slot_r  <= 3'd0;
          tdmr_wr_en_r <= 1'b1;
          tdmr_data_r  <= chmap_phys_w[2*24 +: 24];   //! slot 0 <- phys 2
        end
      end else if (tdmr_slot_r == 3'd7) begin
        tdmr_busy_r <= 1'b0;
        tdmr_tick_r <= 1'b1;                           //! commit after slot 7
      end else begin
        tdmr_slot_r  <= tdmr_slot_r + 3'd1;
        tdmr_wr_en_r <= 1'b1;
        tdmr_data_r  <= chmap_phys_w[(2 + 32'(tdmr_slot_r) + 1)*24 +: 24];
      end
    end
  end : chmap_tdm_adapter

  wire chmap_tdm_dout_w;   //! parked serial output (no board pin yet)
  KL_tdm_render #(.SLOTS_P(8), .SLOT_BITS_P(32)) chan_tdm_render (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .smp_wr_en_i   (tdmr_wr_en_r),
    .smp_wr_slot_i (tdmr_slot_r),
    .smp_wr_data_i (tdmr_data_r),
    .tick_i        (tdmr_tick_r),
    .tdm_bclk_i    (tdm_bclk_i),
    .tdm_fsync_i   (tdm_fsync_i),
    .tdm_dout_o    (chmap_tdm_dout_w),   //! exported as tdm_dout_o below
    .frames_o (), .underruns_o (), .overruns_o ()
  );

  assign tdm_dout_o = chmap_tdm_dout_w;

  // ==========================================================================
  //  MAAP engine (IEEE 1722 Annex B) — dynamic stream-DMAC allocation.
  //  Same monitor-tap + low-rate-TX recipe; addr_valid gates AAF admission
  //  and muxes the effective stream DMAC when MAAP_CTRL.en=1.
  // ==========================================================================
  //! MAAP_P = 0 prunes the engine (see the parameter note). The tie-off is
  //! the engine's RESET state, term by term: state_o = INITIAL (2'd0),
  //! addr_valid_o = 0, no conflicts, no defends, offset 0, and a TX port
  //! that never asserts tvalid (the ADP arbiter's MAAP leg simply never
  //! wins). eff_aaf_dmac therefore always resolves to the CSR-provisioned
  //! AAF_DMAC, and MAAP_STAT0/1 (0x6D0/0x6D4) read 0.
  generate if (MAAP_P != 0) begin : g_maap
  KL_maap #(.CLK_FREQ_HZ_P(MAAP_CLK_HZ_P)) maap_engine (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .enable_i (cfg_maap_enable),
    .count_i  (cfg_maap_count),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    .seed_offset_i (cfg_maap_seed_offset),
    .seed_valid_i  (cfg_maap_seed_valid),
    .rx_tdata_i  (rx_axis_fabric.tdata),
    .rx_tkeep_i  (rx_axis_fabric.tkeep),
    .rx_tvalid_i (rx_axis_fabric.tvalid),
    .rx_tready_i (rx_axis_fabric.tready),
    .rx_tlast_i  (rx_axis_fabric.tlast),
    .m_axis_tdata (maap_tx_tdata), .m_axis_tkeep (maap_tx_tkeep),
    .m_axis_tvalid(maap_tx_tvalid), .m_axis_tlast (maap_tx_tlast),
    .m_axis_tready(maap_tx_tready),
    .addr_o (maap_addr), .addr_valid_o (maap_addr_valid),
    .state_o (maap_state), .offset_o (maap_offset),
    .conflicts_o (maap_conflicts), .defends_o (maap_defends)
  );
  end else begin : g_no_maap
    assign maap_tx_tdata   = {TDATA_WIDTH{1'b0}};
    assign maap_tx_tkeep   = {(TDATA_WIDTH/8){1'b0}};
    assign maap_tx_tvalid  = 1'b0;
    assign maap_tx_tlast   = 1'b0;
    assign maap_addr       = 48'd0;
    assign maap_addr_valid = 1'b0;
    assign maap_state      = 2'd0;
    assign maap_offset     = 16'd0;
    assign maap_conflicts  = 8'd0;
    assign maap_defends    = 8'd0;
  end endgenerate

  // ==========================================================================
  //  SRP — served by the protocol processor, not by an lwSRP engine here
  // ==========================================================================
  //! hdl/ieee8021q/srp/ is DELETED in full - the applicant, the registrar, the
  //! TA registrar, the walker, the ingress/rx path, the context table, the
  //! MRPDU serializer, the timers and KL_lwsrp_bw_gate. The processor's SRP
  //! engine declares Talker Advertise and Listener Ready, registers the
  //! bridge's answers, adopts the Domain and publishes the result through the
  //! class-D face.
  //!
  //! THE CBS SLOPE ORDERING CHANGED. RECORDED HONESTLY, WITH THE ANSWER.
  //!
  //! KL_lwsrp_bw_gate sequenced the two edges explicitly, with a settling
  //! HOLD between them: on activation the stream's idleSlope joined the
  //! running Sigma, then HOLD_CYCLES_C elapsed, then the gate opened; on
  //! teardown the gate closed, then HOLD_CYCLES_C, then the slope left the
  //! Sigma. The invariant it bought is "no stream ever transmits against a
  //! slope the shaper has not budgeted".
  //!
  //! The processor has no hold. KL_srp_admission walks its sources and
  //! latches grant_r, gslope_r and sum_r TOGETHER at round end; the published
  //! sr_admitted_o is grant_r AND the live request. So:
  //!
  //!   OPENING EDGE - a source's gate can only rise once a round has granted
  //!   it, and that same round is what put its slope into sum_r. Gate and
  //!   Sigma therefore change on the SAME edge, never gate-first. The hold
  //!   existed to let the slope settle through the CSR mux; that mux is
  //!   combinational and in this clock domain, so there is nothing to settle.
  //!   EQUAL, not worse.
  //!
  //!   CLOSING EDGE - sr_admitted_o drops the cycle the request drops (the
  //!   live AND), but sum_r is ROUND-LATCHED and keeps the stopped stream's
  //!   slope until the next round completes. The shaper goes on budgeting
  //!   bandwidth for a stream that has already stopped: MORE conservative
  //!   than the bw-gate, not less.
  //!
  //! ANSWER: the invariant HOLDS on both edges. What is genuinely lost is the
  //! bw-gate's explicit hold as a named, testable behaviour - the ordering is
  //! now a consequence of the admission round's structure rather than a
  //! sequencer anyone can point at.
  assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];
  //! the class-A idleSlope the CBS mux takes: the SUM across admitted
  //! sources, which is what a single shaped queue's idleSlope must be
  assign lwsrp_slope_en    = |pp_cd_srp_sr_admitted_w;
  assign lwsrp_idle_slope  = pp_cd_srp_sum_slope_bps_w;
  //! Milan 4.2.7.2.1 Domain adoption surface: the OPERATIONAL {priority, VID}
  //! every declaration serializes, and which the AAF/CRF C-TAG muxes take.
  assign lwsrp_adopt_valid = pp_cd_srp_domain_adopted_w;
  assign lwsrp_op_prio     = {5'd0, pp_cd_srp_class_a_prio_w};
  assign lwsrp_op_vid      = pp_cd_srp_class_a_vid_w;
  assign lwsrp_domain_ok   = pp_cd_srp_domain_adopted_w;
  assign lwsrp_over_limit  = pp_cd_srp_over_limit_w;
  assign lwsrp_res_active  = |pp_cd_srp_active_w;
  //! per-source Talker failure (802.1Q 35.2.2.8.6 FailureCode + BridgeID)
  assign lwsrp_tfail_code   = pp_cd_srp_src_fail_code_w[7:0];
  assign lwsrp_tfail_valid  = |pp_cd_srp_src_fail_code_w[7:0];
  //! SINK 0's registrar levels - the flat 0x6A4/0x690 status words are
  //! scalars and always described sink 0. [2*k +: 2] is the per-sink slice;
  //! bit 1 of it is "a Talker Advertise for this sink's stream is REGISTERED"
  //! (802.1Q 35.2.4.4.1), which is exactly what the deleted TA registrar
  //! published. The per-sink Failure BridgeID and registered VLAN are NOT on
  //! the class-D face (it carries the per-SOURCE bridge id only), so the CSR
  //! fields that carried them are gone from this file rather than wearing a
  //! source's value under a sink's name.
  assign lwsrp_ta_registered = pp_cd_srp_tk_reg_state_w[1];
  assign lwsrp_ta_failed     = |pp_cd_srp_snk_fail_code_w[7:0];
  assign lwsrp_ta_fail_code  = pp_cd_srp_snk_fail_code_w[7:0];
  assign lwsrp_listener_reg   = pp_cd_srp_lstn_reg_state_w[1];
  assign lwsrp_listener_decl  = pp_cd_srp_lstn_decl_state_w[1:0];
  assign lwsrp_listener_ready = (pp_cd_srp_lstn_decl_state_w[1:0] == 2'd1);
  assign lwsrp_talker_declared= |pp_cd_srp_tk_decl_state_w;
  //! GONE, and worth naming: the per-talker "a Listener Asking Failed
  //! attribute is registered" level (gh #56 A2) that promoted an ACMP talker
  //! context to REGISTERING_FAILED. The class-D face reports a per-source
  //! failure CODE, not the attribute type it arrived on, so this fabric can
  //! no longer observe that level at all - it is not tied to zero here, it
  //! has no net.
  //! MRPDU tx/rx accounting lived in the deleted serializer/ingress pair
  assign lwsrp_tx_count = 16'd0;
  assign lwsrp_rx_pdus  = 16'd0;
  assign lwsrp_rx_drops = 8'd0;
  //! the 0x800 window's SRP context-table master and its per-row readback:
  //! there is no attribute-row table in this fabric any more
  assign lwsrp_ctx_oor_w   = 1'b0;
  assign srp_ctx_gnt_w     = 1'b0;
  assign srp_ctx_rd_sid_w  = 64'd0;
  assign srp_ctx_rd_stat_w = 16'd0;

  //! A_TXARB_DIAG 0x784 lock supervision, one lane per TX-trunk arbiter.
  //!
  //! THE LANE MAP RENUMBERED when the legacy 1722.1/SRP plane was deleted.
  //! It used to be eight muxes - 0 aecp_acmp, 1 ctl_tx, 2 srp_ctl, 3 lstn_ctl,
  //! 4 maap_ctl, 5 aaf_final, 6 crf_dp, 7 adp_tx - because five independent
  //! control sources (AECP responses, ACMP talker answers, ADP advertisements,
  //! lwSRP MRPDUs, ACMP listener probes) each needed a merge step. The
  //! protocol processor emits ONE byte stream for every protocol it owns and
  //! arbitrates internally, so four of those merges have no second source left
  //! and are gone with the planes that fed them.
  //!
  //! Lane order (LSB first): 0 ctl_tx (processor + MAAP -> the control lane),
  //! 1 aaf_final, 2 crf_dp, 3 adp_tx (= the MAC boundary mux).
  //! Bits 7:4 read a STRUCTURAL ZERO - there is no fifth..eighth arbiter to
  //! supervise, as opposed to four arbiters that happen never to have locked.
  //! Anything decoding 0x784 by the old lane numbers reads the WRONG mux.
  //!
  //! Watchdog windows stay STAGGERED shortest-upstream (control chain 2^15,
  //! data merges 2^16, MAC boundary 2^17): an abandoned source starves every
  //! downstream mux on the SAME cycle (the IFG gasket passes tvalid
  //! combinationally), so equal windows would expire together and each level
  //! would inject its own close beat - runts on the wire per event. With the
  //! stagger only the true origin fires; its injected tlast propagates down as
  //! an accepted beat and clears every downstream counter normally.
  wire [7:0] txarb_locked_w, txarb_abort_w, txarb_stall_w;
  //! lanes 0..3 as documented above; lane 4 = the gPTP plane's merge
  //! (a structural zero while GPTP_PLANE_EN_P is off); 7:5 structural
  //! zero. Lane 1 WAS aaf_final_mux, the merge of the shaped general-data
  //! lane with AAF: with the general-data chain gone AAF enters crf_dp_mux
  //! directly, so lane 1 is a structural zero too. The lane numbers are an
  //! ABI (REGISTER_MAP 0x784), so nothing is renumbered.
  assign txarb_locked_w[7:5] = 3'd0;
  assign txarb_abort_w [7:5] = 3'd0;
  assign txarb_stall_w [7:5] = 3'd0;
  assign txarb_locked_w[1]   = 1'b0;
  assign txarb_abort_w [1]   = 1'b0;
  assign txarb_stall_w [1]   = 1'b0;

  //! THE control merge: the protocol processor's packed TX (s_data - ADP,
  //! ACMP and SRP, internally arbitrated) + the fabric KL_maap
  //! announce/probe/defend lane (s_adp). The selected processor pin also
  //! contains KL_pp_maap, but this integration ties cfg_maap_internal_i low,
  //! selects the fabric allocator, and presents it through KL_pp_maap_shim.
  wire [TDATA_WIDTH-1:0]   ctlh_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] ctlh_tx_tkeep;
  wire                     ctlh_tx_tvalid, ctlh_tx_tlast, ctlh_tx_tready;
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH), .TO_LOG2_P(15)) ctl_tx_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_data_tdata (pp_tx_tdata_w),  .s_data_tkeep (pp_tx_tkeep_w),
    .s_data_tvalid(pp_tx_tvalid_w), .s_data_tlast (pp_tx_tlast_w),
    .s_data_tready(pp_tx_tready_w),
    .s_adp_tdata (maap_tx_tdata),  .s_adp_tkeep (maap_tx_tkeep),
    .s_adp_tvalid(maap_tx_tvalid), .s_adp_tlast (maap_tx_tlast),
    .s_adp_tready(maap_tx_tready),
    .m_tdata (ctlh_tx_tdata), .m_tkeep (ctlh_tx_tkeep),
    .m_tvalid(ctlh_tx_tvalid), .m_tlast (ctlh_tx_tlast), .m_tready(ctlh_tx_tready),
    .diag_locked_o(txarb_locked_w[0]),
    .abort_evt_o (txarb_abort_w[0]), .stall_evt_o (txarb_stall_w[0])
  );

  //! The AAF talkers head the DATA lane of the trunk: they are the first
  //! source of the data-side merges (the shaped general-data lane that used to
  //! sit beside them is gone - TX-trunk note at the interface declarations).
  //! The CRF talker's PDUs join them here - on the DATA lane beside AAF, NOT on the
  //! low-rate control merge (docs/overview/ARCHITECTURE.md section 3,
  //! moved 2026-07-28). The CRF PDU is a STREAM carrying a gPTP timestamp
  //! that a listener steers its 48 kHz recovery clock against; behind the
  //! control lane's min-IFG gasket it inherited a 512-cycle spacing PER
  //! FRAME and queued behind whatever ADP/AECP/ACMP/MAAP/lwSRP burst was in
  //! flight - a Hive enumeration storm is hundreds of AECP responses, and
  //! every one of them added ~10 us of delay to the media clock's
  //! presentation margin. The data lane is gasket-free and already carries
  //! the 8 AAF talkers, which is where a class A stream belongs.
  //!
  //! HONEST BOUND: neither AAF nor CRF is credit-shaped. The 802.1Qav shaper
  //! is not in this wrapper any more (it only ever shaped the retired target's
  //! general-data lane), so class-A shaping of the fabric's own stream
  //! sources is a separate lane, not something this merge quietly claims.
  wire [TDATA_WIDTH-1:0]   dpcrf_tdata;
  wire [TDATA_WIDTH/8-1:0] dpcrf_tkeep;
  wire                     dpcrf_tvalid, dpcrf_tlast, dpcrf_tready;
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH), .TO_LOG2_P(16)) crf_dp_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_data_tdata (aaf_tx_tdata),  .s_data_tkeep (aaf_tx_tkeep),
    .s_data_tvalid(aaf_tx_tvalid), .s_data_tlast (aaf_tx_tlast),
    .s_data_tready(aaf_tx_tready),
    .s_adp_tdata (crft_tx_tdata),  .s_adp_tkeep (crft_tx_tkeep),
    .s_adp_tvalid(crft_tx_tvalid), .s_adp_tlast (crft_tx_tlast),
    .s_adp_tready(crft_tx_tready),
    .m_tdata (dpcrf_tdata), .m_tkeep (dpcrf_tkeep),
    .m_tvalid(dpcrf_tvalid), .m_tlast (dpcrf_tlast), .m_tready(dpcrf_tready),
    .diag_locked_o(txarb_locked_w[2]),
    .abort_evt_o (txarb_abort_w[2]), .stall_evt_o (txarb_stall_w[2])
  );

  //! min-IFG gasket on the CONTROL lane ONLY (2026-07-19): the MilanMAC
  //! (cut-through core + milan_cd->sys CDC) silently eats a frame that
  //! enters back-to-back behind another (silicon: the MVRP half of the
  //! MSRP+MVRP pair, and the intermittent ACMP CONNECT_RX_RESPONSE that
  //! follows another control frame). Spacing every control frame here fixes
  //! ALL of them WITHOUT touching data/AAF throughput (the data lane
  //! bypasses this gasket). Replaces lwSRP's local gap workaround.
  wire [TDATA_WIDTH-1:0]   ctlg2_tdata;
  wire [TDATA_WIDTH/8-1:0] ctlg2_tkeep;
  wire                     ctlg2_tvalid, ctlg2_tlast, ctlg2_tready;
  tx_ifg_gasket #(.DATA_WIDTH(TDATA_WIDTH), .GAP_CYCLES(512)) ctl_ifg (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_tdata (ctlh_tx_tdata),  .s_tkeep (ctlh_tx_tkeep),
    .s_tvalid(ctlh_tx_tvalid), .s_tlast (ctlh_tx_tlast), .s_tready(ctlh_tx_tready),
    .m_tdata (ctlg2_tdata),  .m_tkeep (ctlg2_tkeep),
    .m_tvalid(ctlg2_tvalid), .m_tlast (ctlg2_tlast), .m_tready(ctlg2_tready)
  );

  // ==========================================================================
  //  the fabric gPTP plane (issue #114, product default ON since #116)
  // ==========================================================================
  //! Joins the control lane AFTER the min-IFG gasket (the CRF rationale:
  //! a time-critical frame must not queue 512 cycles per control burst)
  //! through its own staggered merge (ctl 2^15 -> this 2^16 -> boundary
  //! 2^17). The egress stamper observes the TRUE MAC boundary; ingress
  //! rides the same rx_axis_fabric tap every plane uses (input only,
  //! tvalid && tready qualified). The publication bank directly owns the GM,
  //! parent, pdelay, tu/asCapable, CSR, and protocol-answer faces. The direct
  //! option-OFF arm has no owner: those publications are zero, tu is one, and
  //! every retained publication write is inert.
  wire [TDATA_WIDTH-1:0]   ctlg3_tdata;
  wire [TDATA_WIDTH/8-1:0] ctlg3_tkeep;
  wire                     ctlg3_tvalid, ctlg3_tlast, ctlg3_tready;
  wire [15:0] gptp_tap_drop_w, gptp_rx_drop_w, gptp_ev_drop_w;

  generate if (GPTP_PLANE_EN_P) begin : g_gptp_plane
    wire [TDATA_WIDTH-1:0]   gtx_tdata_w;
    wire [TDATA_WIDTH/8-1:0] gtx_tkeep_w;
    wire                     gtx_tvalid_w, gtx_tlast_w, gtx_tready_w;
    wire                     gtx_sent_w;
    wire                     gts_valid_w;
    wire [63:0]              gts_ns_w;
    wire [15:0]              gts_seq_w;
    wire [3:0]               gts_type_w;

    KL_gptp_shadow #(
        .TDATA_WIDTH_P (TDATA_WIDTH),
        .CLK_HZ_P      (MILAN_CLK_FREQ_HZ),
        .UCODE_HEX_P   (GPTP_UCODE_HEX_P)
    ) u_gptp_shadow (
        .clk_i           (axis_clk),
        .rst_n           (axis_resetn),
        .rx_tdata_i      (rx_axis_fabric.tdata),
        .rx_tkeep_i      (rx_axis_fabric.tkeep),
        .rx_tvalid_i     (rx_axis_fabric.tvalid),
        .rx_tready_i     (rx_axis_fabric.tready),
        .rx_tlast_i      (rx_axis_fabric.tlast),
        .phc_ns_i        (ptp_now_w),
        .phc_adj_o       (gptp_adj_w),
        .phc_step_we_o   (gptp_step_we_w),
        .phc_step_o      (gptp_step_w),
        .tx_tdata_o      (gtx_tdata_w),
        .tx_tkeep_o      (gtx_tkeep_w),
        .tx_tvalid_o     (gtx_tvalid_w),
        .tx_tlast_o      (gtx_tlast_w),
        .tx_tready_i     (gtx_tready_w),
        .txts_valid_i    (gts_valid_w),
        .txts_ns_i       (gts_ns_w),
        .txts_seq_i      (gts_seq_w),
        .txts_type_i     (gts_type_w),
        .tx_sent_o       (gtx_sent_w),
        .pub_gm_id_o     (gptp_pub_gm_w),
        .pub_parent_id_o (gptp_pub_parent_w),
        .pub_flags_o     (gptp_pub_flags_w),
        .pub_pdelay_ns_o (gptp_pub_pdelay_w),
        .pub_offset_o    (gptp_pub_offset_w),
        .pub_annq_o      (gptp_pub_annq_w),
        .pub_path_count_o(gptp_pub_path_count_w),
        .pub_path_o      (gptp_pub_path_w),
        .pub_path_gen_o  (gptp_pub_path_gen_w),
        .pub_commit_o    (),
        .pub_disc_o      (gptp_pub_disc_w),
        .dbg_tap_drop_o  (gptp_tap_drop_w),
        .dbg_rx_drop_o   (gptp_rx_drop_w),
        .dbg_ev_drop_o   (gptp_ev_drop_w),
        .dbg_busy_o      (),
        .dbg_rx_ts_o     (),
        .dbg_tspush_v_o  (),
        .dbg_tspush_o    (),
        .dbg_tspop_v_o   (),
        .dbg_txts_type_o ()
    );

    adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH), .TO_LOG2_P(16)) gptp_ctl_mux (
      .clk_i (axis_clk), .rst_n (axis_resetn),
      .s_data_tdata (ctlg2_tdata),  .s_data_tkeep (ctlg2_tkeep),
      .s_data_tvalid(ctlg2_tvalid), .s_data_tlast (ctlg2_tlast),
      .s_data_tready(ctlg2_tready),
      .s_adp_tdata (gtx_tdata_w),  .s_adp_tkeep (gtx_tkeep_w),
      .s_adp_tvalid(gtx_tvalid_w), .s_adp_tlast (gtx_tlast_w),
      .s_adp_tready(gtx_tready_w),
      .m_tdata (ctlg3_tdata), .m_tkeep (ctlg3_tkeep),
      .m_tvalid(ctlg3_tvalid), .m_tlast (ctlg3_tlast),
      .m_tready(ctlg3_tready),
      .diag_locked_o(txarb_locked_w[4]),
      .abort_evt_o (txarb_abort_w[4]), .stall_evt_o (txarb_stall_w[4])
    );

    KL_gptp_txstamp #(.TDATA_WIDTH_P (TDATA_WIDTH)) u_gptp_txstamp (
        .clk_i      (axis_clk),
        .rst_n      (axis_resetn),
        .tx_tdata_i (tx_axis_to_mac.tdata),
        .tx_tvalid_i(tx_axis_to_mac.tvalid),
        .tx_tready_i(tx_axis_to_mac.tready),
        .tx_tlast_i (tx_axis_to_mac.tlast),
        .phc_ns_i   (ptp_now_w),
        .armed_i    (gtx_sent_w),
        .ts_valid_o (gts_valid_w),
        .ts_ns_o    (gts_ns_w),
        .ts_seq_o   (gts_seq_w),
        .ts_type_o  (gts_type_w)
    );
  end else begin : g_gptp_off
    //! option off: the control lane passes straight through, the PHC
    //! knobs constant-fold to the CSR face, the publish words read zero
    assign txarb_locked_w[4] = 1'b0;
    assign txarb_abort_w [4] = 1'b0;
    assign txarb_stall_w [4] = 1'b0;
    assign ctlg3_tdata  = ctlg2_tdata;
    assign ctlg3_tkeep  = ctlg2_tkeep;
    assign ctlg3_tvalid = ctlg2_tvalid;
    assign ctlg3_tlast  = ctlg2_tlast;
    assign ctlg2_tready = ctlg3_tready;
    assign gptp_adj_w = '0;
    assign gptp_step_we_w = 1'b0;
    assign gptp_step_w = '0;
    assign gptp_pub_gm_w = '0;
    assign gptp_pub_parent_w = '0;
    assign gptp_pub_annq_w = '0;
    assign gptp_pub_flags_w = '0;
    assign gptp_pub_pdelay_w = '0;
    assign gptp_pub_offset_w = '0;
    assign gptp_pub_path_w = '0;
    assign gptp_pub_path_count_w = '0;
    assign gptp_pub_path_gen_w = '0;
    assign gptp_pub_disc_w = 1'b0;
    assign gptp_tap_drop_w = '0;
    assign gptp_rx_drop_w = '0;
    assign gptp_ev_drop_w = '0;
  end endgenerate

  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) adp_tx_mux (
    .clk_i (axis_clk),
    .rst_n (axis_resetn),
    .s_data_tdata (dpcrf_tdata),
    .s_data_tkeep (dpcrf_tkeep),
    .s_data_tvalid(dpcrf_tvalid),
    .s_data_tlast (dpcrf_tlast),
    .s_data_tready(dpcrf_tready),
    .s_adp_tdata (ctlg3_tdata),
    .s_adp_tkeep (ctlg3_tkeep),
    .s_adp_tvalid(ctlg3_tvalid),
    .s_adp_tlast (ctlg3_tlast),
    .s_adp_tready(ctlg3_tready),
    .m_tdata (tx_axis_to_mac.tdata),
    .m_tkeep (tx_axis_to_mac.tkeep),
    .m_tvalid(tx_axis_to_mac.tvalid),
    .m_tlast (tx_axis_to_mac.tlast),
    .m_tready(tx_axis_to_mac.tready),
    .diag_locked_o(txarb_locked_w[3]),
    .abort_evt_o (txarb_abort_w[3]),
    .stall_evt_o (txarb_stall_w[3])
  );

  //! Sticky event capture for A_TXARB_DIAG: which mux ever fired which
  //! verdict since reset. Reset-only clear - the register is forensics for
  //! a wedge class that by definition outlives every soft recovery path.
  logic [7:0] txarb_abort_sticky_r, txarb_stall_sticky_r;
  always_ff @(posedge axis_clk) begin : txarb_sticky
    if (!axis_resetn) begin
      txarb_abort_sticky_r <= 8'h0;
      txarb_stall_sticky_r <= 8'h0;
    end else begin
      txarb_abort_sticky_r <= txarb_abort_sticky_r | txarb_abort_w;
      txarb_stall_sticky_r <= txarb_stall_sticky_r | txarb_stall_w;
    end
  end : txarb_sticky
  wire [31:0] txarb_diag_w = {8'hA7, txarb_stall_sticky_r,
                              txarb_abort_sticky_r, txarb_locked_w};

  // ==========================================================================
  //  RMON event counters
  // ==========================================================================
  //! Good-frame lanes are derived HERE from the MAC AXIS boundary handshake
  //! (one accepted `tlast` beat = one frame), so they count on every
  //! integration - including the LiteX SoCs, whose glue has no MAC event
  //! pulses to offer (i_mac_events tied 0 there = the "RMON never worked on
  //! silicon" root cause). The remaining MAC-internal lanes pass through from
  //! i_mac_events; its good-frame bits are ignored to make double-counting
  //! structurally impossible.
  wire tx_mac_good_w = m_axis_mac_tx_tvalid & m_axis_mac_tx_tready
                     & m_axis_mac_tx_tlast;
  wire rx_mac_good_w = s_axis_mac_rx_tvalid & s_axis_mac_rx_tready
                     & s_axis_mac_rx_tlast;
  logic [_ETH_EVENT_COUNTER-1:0] mac_events_w;
  always_comb begin : mac_event_merge
    mac_events_w = i_mac_events;
    mac_events_w[TX_FIFO_GOOD_FRAME] = tx_mac_good_w;
    mac_events_w[RX_FIFO_GOOD_FRAME] = rx_mac_good_w;
  end : mac_event_merge

  //! Capability mask published at CSR 0x204. The two good-frame lanes are
  //! forced supported because they are derived RIGHT HERE (same override that
  //! makes double-counting impossible); every other lane is only claimed if
  //! the integration says it drives it. A zero bit is the honest statement
  //! "this counter is structurally silent", as opposed to a zero COUNT, which
  //! means "nothing happened" - the distinction the RMON tie-off erased.
  wire [_ETH_EVENT_COUNTER-1:0] stats_cap_w = i_mac_events_cap
                                            | (1 << TX_FIFO_GOOD_FRAME)
                                            | (1 << RX_FIFO_GOOD_FRAME);

  ethernet_events ethernet_counters(
    .clk(axis_clk),
    .resetn(axis_resetn),
    .stats_reset(cfg_stats_reset),
    .events(mac_events_w),
    .counts_o(stats_counts),
    .rollover_o(stats_rollover)
  );

  // ==========================================================================
  //  AAF per-stage latency taps (roadmap item 11) — the observation-point
  //  adapter and the LTAP CSR word order live in KL_aaf_latency_tap_bank; the
  //  datapath only names the points it is observed at. The bank is a pure
  //  observer: every port below is an input except the two CSR rails.
  // ==========================================================================
  KL_aaf_latency_tap_bank #(
    .ENABLE_P  (LTAP_P),
    .TIMEOUT_C (MILAN_CLK_FREQ_HZ / 2000)   //! ~0.5 ms per-stage re-arm guard
  ) aaf_latency_tap_bank (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .en_i  (ltap_en_w), .clr_i (ltap_clr_w),
    .now_i (ptp_now_w[31:0]),

    .cap_pair_p_i    (aafcap_pv_w),
    .aaf_tx_tvalid_i (aaf_tx_tvalid),
    .aaf_tx_tready_i (aaf_tx_tready),
    .aaf_tx_tlast_i  (aaf_tx_tlast),
    .mac_tx_tvalid_i (m_axis_mac_tx_tvalid),
    .mac_tx_tready_i (m_axis_mac_tx_tready),
    .mac_tx_tlast_i  (m_axis_mac_tx_tlast),

    .mac_rx_tvalid_i (s_axis_mac_rx_tvalid),
    .mac_rx_tready_i (s_axis_mac_rx_tready),
    .mac_rx_tlast_i  (s_axis_mac_rx_tlast),
    .avtp_accept_p_i (avtprx_accept_p),
    .dpkt_tvalid_i   (dpkt_pcm_tvalid_w),
    .dpkt_tready_i   (dpkt_pcm_tready_w),
    .dpkt_tlast_i    (dpkt_pcm_tlast_w),
    //! Final RX stage: selected listener payload accepted by fabric render.
    .render_tvalid_i (rend_pcm_tvalid_w),
    .render_tready_i (1'b1), //! Latency observer cannot backpressure render.
    .render_tlast_i  (rend_pcm_tlast_w),

    .regs_o   (ltap_regs_w),
    .status_o (ltap_status_w)
  );

  // ==========================================================================
  //  protocol-processor plane inputs the fabric computes
  // ==========================================================================
  //! GM_CHANGE (1722.1-2021 6.2.6). The deleted advertiser took a grandmaster
  //! change as a level-driven re-advertise off cfg_adp_advertise_p; the
  //! processor wants a STROBE, so the edge is detected here, on the committed
  //! pair the 0x624/0x628/0x62C CSR words carry. An all-zero pair is "no
  //! commitment yet" and its first write is NOT a change - otherwise every
  //! boot would announce a grandmaster change that never happened.
  //!
  //! TWO FACTS, from ONE identity compare. pp_gm_id_edge_w is the
  //! grandmaster IDENTITY moving; pp_gm_dom_edge_w is the gPTP domain
  //! number moving under the same "a prior grandmaster existed" rule.
  //!
  //!   pp_gm_change_p_w    = id | domain  -> the ADP duty. Both fields are
  //!     carried by the ADPDU, so either one changing is a re-advertise
  //!     (1722.1-2021 6.2.6, Milan 5.6.3.5.7) and a GET_AVB_INFO trigger
  //!     (Milan Table 5.22 names gptp_grandmaster_id AND
  //!     gptp_domain_number).
  //!   pp_gm_id_change_p_w = id           -> the GRANDMASTER moved, and
  //!     only that. Milan Table 5.1 GPTP_GM_CHANGED counts "gPTP GM
  //!     changes"; the served AS path's entry 0 is the grandmaster, so
  //!     Table 5.22's "the path sequence changes" is an identity fact too.
  //!     A domain-only write with a stable grandmaster must move NEITHER.
  //!
  //! Reusing one strobe for both made a domain write claim the grandmaster
  //! and the path had changed when neither had; the compare is shared so the
  //! two can never disagree about the identity, and the domain term is added
  //! to exactly one of them.
  wire pp_gm_id_edge_w  = (|pp_gm_id_q_r) & (pp_gm_id_q_r  != cfg_adp_gptp_gm);
  wire pp_gm_dom_edge_w = (|pp_gm_id_q_r) & (pp_gm_dom_q_r != cfg_adp_gptp_domain);
  always_ff @(posedge axis_clk) begin : pp_gm_edge
    if (!axis_resetn) begin
      pp_gm_id_q_r        <= 64'd0;
      pp_gm_dom_q_r       <= 8'd0;
      pp_gm_change_p_w    <= 1'b0;
      pp_gm_id_change_p_w <= 1'b0;
    end else begin
      pp_gm_id_q_r        <= cfg_adp_gptp_gm;
      pp_gm_dom_q_r       <= cfg_adp_gptp_domain;
      pp_gm_change_p_w    <= pp_gm_id_edge_w | pp_gm_dom_edge_w;
      pp_gm_id_change_p_w <= pp_gm_id_edge_w;
    end
  end : pp_gm_edge

  //! THE STREAM-ID LAW, computed once for every talker source. It is the same
  //! law KL_aaf_packetizer stamps onto the wire ({station_mac, uid}) and the
  //! same one crft_auto_sid_w computes for the CRF Media Clock Output, so a
  //! controller that binds source s is told the stream_id the frames of
  //! source s actually carry. The CRF source additionally honours its CSR
  //! override (eff_crft_sid_w), which is the provisioning lever that already
  //! exists; without that arm a provisioned CRFT_SID would put one number on
  //! the wire and a different one in the ACMP answer and the SRP declaration.
  generate
    for (genvar gsid = 0; gsid < ACMP_SRC_C; gsid++) begin : g_pp_sid
      if (gsid == CRF_TUID_C) begin : g_sid_crf
        assign pp_src_sid_w[64*gsid +: 64] = eff_crft_sid_w;
      end else begin : g_sid_aaf
        assign pp_src_sid_w[64*gsid +: 64] = {station_mac_be_w, 16'(gsid)};
      end
    end
  endgenerate

  // ==========================================================================
  //  protocol-processor CONTROL plane — THE control plane, unconditional
  // ==========================================================================
  //! The scenario-B P5 seam, substituted. There is no PP_PLANE_P: the legacy
  //! ADP advertiser, ACMP talker/listener, AECP/AEM engine and lwSRP
  //! applicant are DELETED from this repository (USER, explicit: "remove the
  //! old code AECP/ACMP/ADP the lwSRP shall be removed as well. Only use the
  //! uCPU code"), so there is nothing to fall back to and no option to leave.
  //! KL_pp_shadow's banner carries the full rationale; the facts that matter
  //! HERE are:
  //!
  //!   1. It taps rx_axis_fabric the same way every other plane does -
  //!      INPUT ONLY, qualified on tvalid && tready. The shared fabric tap is
  //!      permanently ready now; retaining handshake qualification prevents a
  //!      future sink policy from re-eating a held beat.
  //!   2. Its packed TX is the ONE control-lane leg beside MAAP
  //!      (ctl_tx_mux). tx_drain_i is 0: the processor owns the wire.
  //!   3. Its class-D face IS this fabric's ACMP bind record, talker
  //!      declaration and SRP reservation - every consumer that used to read
  //!      a deleted plane reads pp_cd_* now.
  //!   4. Its AECP engine serves the implemented AEM command set documented
  //!      in protocol-processor/docs/architecture/06_aecp_engine.md.
  //!      Integrator-owned counters, mappings and Milan information come
  //!      from the answer blocks above. Unsupported mandatory commands remain
  //!      explicit compliance blockers in the current Milan audit.

  //! The AECP settings face, republished by KL_pp_shadow (see the instance).
  //! `public_flat_rd` because no consumer reads these yet: without a probe a
  //! review found that `cur_config` and `clk_src_index` are both 16 bits, so
  //! the two could be swapped at the port map and every suite would stay
  //! green. The milan_dp bench now moves the clock-source and IDENTIFY faces
  //! through real AECP commands and reads them back here, asserting the
  //! configuration face does NOT move with them. It cannot move the
  //! configuration face itself: the image declares one configuration, so the
  //! only legal index is also the reset value — the bench prints that as an
  //! explicit gap rather than implying coverage it does not have.
  logic [15:0]              pp_aecp_cur_config_w /* verilator public_flat_rd */;
  logic  [7:0]              pp_aecp_identify_w /* verilator public_flat_rd */;
  //! ACMP_SINKS_C, not N_STREAMS: KL_pp_shadow is elaborated at the ACMP
  //! shape (see the .N_STREAM_IN_P connection below), which is deliberately
  //! wider than N_STREAMS — a bare N_STREAMS-wide array would have truncated
  //! the started vector and silently dropped the top sinks' state.
  //! (pp_aecp_strm_started_w is declared above gsi_flag_law, its first
  //! reader, #193)
  //! the per-row settings faces (issue #67): value beside valid bit, sized
  //! at the processor's ACMP shape so the CRF rows ride along (the CRF
  //! output's offset row IS its transit entry's source below). A value
  //! whose valid bit is clear is a reset zero - every consumer here FOLDS.
  //! (pp_aecp_pt_offset_w, pp_aecp_pt_offset_v_w, pp_aecp_fmt_in_w,
  //! pp_aecp_fmt_in_v_w, pp_aecp_fmt_out_w and pp_aecp_fmt_out_v_w are
  //! declared above the aecp_in0_fmt fold, their first reader, #193)
  logic                     pp_aecp_dyn_dirty_w;

  //! ---- Milan Table 5.22 GET_COUNTERS trigger: the descriptor arbiter ----
  //! The processor's face is SCALAR (one {type, index} per cycle) and it
  //! keeps one dirty bit per served descriptor behind it, so this fabric
  //! only has to hand over every changed tuple at least once. The sources
  //! are the per-descriptor pulses of the blocks whose counters the
  //! GET_COUNTERS face above serves: one bit per STREAM_INPUT (the rx
  //! monitor), one per STREAM_OUTPUT (the talker diag, CRF output
  //! included), AVB_INTERFACE 0 and CLOCK_DOMAIN 0 (the edge terms named
  //! beside their counters). Each source bit stays PENDING until the
  //! round-robin selects it, so simultaneous changes are all delivered and
  //! a continuously changing low index cannot starve a higher one; a
  //! re-pulse while pending is absorbed (the processor re-reads current
  //! state, never history). Reviewed on PR 121 (its R1 mutation checks:
  //! dropped accumulation and a lossy clear-all picker both red).
  localparam int unsigned PP_CTR_EVT_N_C = N_STREAMS + ACMP_SRC_C + 2;
  localparam int unsigned PP_CTR_RR_W_C = (PP_CTR_EVT_N_C > 1)
                                         ? $clog2(PP_CTR_EVT_N_C) : 1;
  logic [N_STREAMS-1:0]  pp_ctr_sin_pend_r,  pp_ctr_sin_pend_n;
  logic [ACMP_SRC_C-1:0] pp_ctr_sout_pend_r, pp_ctr_sout_pend_n;
  logic pp_ctr_avb_pend_r, pp_ctr_avb_pend_n;
  logic pp_ctr_ckd_pend_r, pp_ctr_ckd_pend_n;
  logic [PP_CTR_RR_W_C-1:0] pp_ctr_rr_r;
  logic [PP_CTR_EVT_N_C-1:0] pp_ctr_all_pend_w;
  logic        pp_ctr_evt_valid_w /* verilator public_flat_rd */;
  logic [15:0] pp_ctr_evt_type_w  /* verilator public_flat_rd */;
  logic [15:0] pp_ctr_evt_index_w /* verilator public_flat_rd */;

  assign pp_ctr_all_pend_w = {pp_ctr_ckd_pend_r, pp_ctr_avb_pend_r,
                              pp_ctr_sout_pend_r, pp_ctr_sin_pend_r};

  always_comb begin : pp_ctr_event_pick
    int unsigned pick;
    pp_ctr_evt_valid_w = 1'b0;
    pp_ctr_evt_type_w  = 16'd0;
    pp_ctr_evt_index_w = 16'd0;
    for (int unsigned off = 0; off < PP_CTR_EVT_N_C; off++) begin
      pick = 32'(pp_ctr_rr_r) + off;
      if (pick >= PP_CTR_EVT_N_C) pick = pick - PP_CTR_EVT_N_C;
      if (!pp_ctr_evt_valid_w && pp_ctr_all_pend_w[pick]) begin
        pp_ctr_evt_valid_w = 1'b1;
        if (pick < N_STREAMS) begin
          pp_ctr_evt_type_w  = DESC_STREAM_INPUT_C;
          pp_ctr_evt_index_w = 16'(pick);
        end else if (pick < (N_STREAMS + ACMP_SRC_C)) begin
          pp_ctr_evt_type_w  = DESC_STREAM_OUTPUT_C;
          pp_ctr_evt_index_w = 16'(pick - N_STREAMS);
        end else if (pick == (N_STREAMS + ACMP_SRC_C)) begin
          pp_ctr_evt_type_w  = DESC_AVB_INTERFACE_C;
        end else begin
          pp_ctr_evt_type_w  = DESC_CLOCK_DOMAIN_C;
        end
      end
    end
  end : pp_ctr_event_pick

  always_comb begin : pp_ctr_event_next
    pp_ctr_sin_pend_n  = pp_ctr_sin_pend_r  | avtprx_dirty_p_w;
    pp_ctr_sout_pend_n = pp_ctr_sout_pend_r | tkd_dirty_p_w;
    pp_ctr_avb_pend_n  = pp_ctr_avb_pend_r  | ctr_avb_dirty_w;
    pp_ctr_ckd_pend_n  = pp_ctr_ckd_pend_r  | ctr_ckd_dirty_w;
    for (int unsigned s = 0; s < N_STREAMS; s++) begin
      if (pp_ctr_evt_valid_w
          && (pp_ctr_evt_type_w == DESC_STREAM_INPUT_C)
          && (pp_ctr_evt_index_w == 16'(s))) pp_ctr_sin_pend_n[s] = 1'b0;
    end
    for (int unsigned s = 0; s < ACMP_SRC_C; s++) begin
      if (pp_ctr_evt_valid_w
          && (pp_ctr_evt_type_w == DESC_STREAM_OUTPUT_C)
          && (pp_ctr_evt_index_w == 16'(s))) pp_ctr_sout_pend_n[s] = 1'b0;
    end
    if (pp_ctr_evt_valid_w && (pp_ctr_evt_type_w == DESC_AVB_INTERFACE_C))
      pp_ctr_avb_pend_n = 1'b0;
    if (pp_ctr_evt_valid_w && (pp_ctr_evt_type_w == DESC_CLOCK_DOMAIN_C))
      pp_ctr_ckd_pend_n = 1'b0;
  end : pp_ctr_event_next

  always_ff @(posedge axis_clk or negedge axis_resetn) begin : pp_ctr_event_queue
    if (!axis_resetn) begin
      pp_ctr_sin_pend_r  <= '0;
      pp_ctr_sout_pend_r <= '0;
      pp_ctr_avb_pend_r  <= 1'b0;
      pp_ctr_ckd_pend_r  <= 1'b0;
      pp_ctr_rr_r        <= '0;
    end else begin
      pp_ctr_sin_pend_r  <= pp_ctr_sin_pend_n;
      pp_ctr_sout_pend_r <= pp_ctr_sout_pend_n;
      pp_ctr_avb_pend_r  <= pp_ctr_avb_pend_n;
      pp_ctr_ckd_pend_r  <= pp_ctr_ckd_pend_n;
      //! the round-robin pointer moves past whatever was just delivered
      if (pp_ctr_evt_valid_w) begin
        if (pp_ctr_evt_type_w == DESC_CLOCK_DOMAIN_C)
          pp_ctr_rr_r <= '0;
        else if (pp_ctr_evt_type_w == DESC_STREAM_INPUT_C)
          pp_ctr_rr_r <= PP_CTR_RR_W_C'(32'(pp_ctr_evt_index_w) + 1);
        else if (pp_ctr_evt_type_w == DESC_STREAM_OUTPUT_C)
          pp_ctr_rr_r <= PP_CTR_RR_W_C'(N_STREAMS
                                        + 32'(pp_ctr_evt_index_w) + 1);
        else
          pp_ctr_rr_r <= PP_CTR_RR_W_C'(N_STREAMS + ACMP_SRC_C + 1);
      end
    end
  end : pp_ctr_event_queue

  KL_pp_shadow #(
      .TDATA_WIDTH_P  (TDATA_WIDTH),
      .CLK_HZ_P       (MILAN_CLK_FREQ_HZ),
      //! THE PROCESSOR'S ARRAYS ARE THE ENTITY'S DESCRIPTOR COUNTS, not the
      //! AAF stream count. ACMP_SINKS_C / ACMP_SRC_C come from the generated
      //! shape header, which is the same pass that emitted the descriptors a
      //! controller enumerates, so a STREAM_OUTPUT the entity advertises
      //! always has a source context that can answer a CONNECT_TX for it -
      //! including the CRF Media Clock Output at talker_unique_id
      //! N_STREAMS, which a bare N_STREAMS-wide array would have left
      //! unanswerable exactly the way the pre-0x0027 shapes did.
      .N_STREAM_IN_P  (ACMP_SINKS_C),
      .N_STREAM_OUT_P (ACMP_SRC_C),
      .TIM_DIV_US_P   (PP_TIM_DIV_US_P),
      .TIM_DIV_MS_P   (PP_TIM_DIV_MS_P),
      .TROM_HEX_P     (PP_TROM_HEX_P),
      .UCODE_HEX_P         (PP_UCODE_HEX_P),
      .DESC_BASE_P         (PP_DESC_BASE_P),
      .DESC_LINE_BYTES_P   (PP_DESC_LINE_BYTES_P),
      .DESC_IDX_ENTRIES_P  (PP_DESC_IDX_ENTRIES_P),
      //! Generated beside the descriptor image from the same AEM model.
      //! Large configured models therefore cannot inherit a small default.
      .DESC_NAME_ENTRIES_P (AEM_NAME_ENTRIES_C),
      .DESC_MEM_TMO_CYC_P  (PP_DESC_MEM_TMO_CYC_P),
      .RESP_BASE_P         (PP_RESP_BASE_P)
    ) pp_shadow (
      .clk_i             (axis_clk),
      .rst_n             (axis_resetn),
      //! ---- the AECP settings face (Milan §5.3.x) ----------------------
      //! What a controller has SET. Most of these landed as observable state
      //! ahead of their consumers ON PURPOSE: they read a reset default until
      //! a controller writes them, so wiring them changed no behaviour and
      //! gave the media clock, the listener gate and the talker offset a
      //! settled place to read from when each is converted.
      //!
      //! `aecp_strm_started_o` is NO LONGER one of them. It is LOAD-BEARING
      //! since issue #78 and has three consumers in this file: the listener
      //! accept gate, `KL_crf_rx`'s `stop_i` (consumption only - the frame
      //! strobe stays raw so a stopped CRF sink still observes and counts,
      //! §5.3.8.10), and GET_STREAM_INFO's Table 5.9 bit 28. A stopped sink
      //! really does stop feeding the media path - payload discarded, no
      //! lock, no restart echo - so do not read this block as "wiring these
      //! is inert".
      //!
      //! CONSUMED since #74: `pp_aecp_clk_src_index_w` is the value
      //! SET_CLOCK_SOURCE writes, and media_clk_resolve (beside the shape
      //! include) turns it into the media plane's one registered verdict -
      //! the round the old note here promised.
      .aecp_cur_config_o   (pp_aecp_cur_config_w),
      .aecp_identify_o     (pp_aecp_identify_w),
      .aecp_clk_src_index_o(pp_aecp_clk_src_index_w),
      .aecp_strm_started_o (pp_aecp_strm_started_w),
      .aecp_pt_offset_o    (pp_aecp_pt_offset_w),
      .aecp_pt_offset_v_o  (pp_aecp_pt_offset_v_w),
      .aecp_fmt_in_o       (pp_aecp_fmt_in_w),
      .aecp_fmt_in_v_o     (pp_aecp_fmt_in_v_w),
      .aecp_fmt_out_o      (pp_aecp_fmt_out_w),
      .aecp_fmt_out_v_o    (pp_aecp_fmt_out_v_w),
      .aecp_dyn_dirty_o    (pp_aecp_dyn_dirty_w),
      //! Same live lock level as the processor AECP engine. Milan 5.4.2.27
      //! and 5.4.2.28 prohibit local map changes while it is asserted.
      .aecp_lock_held_o    (aecp_locked),
      //! GET_COUNTERS: the processor asks, this file answers (see the
      //! Table 7-157 mux above)
      .ctr_req_o         (pp_ctr_req_w),
      .ctr_desc_type_o   (pp_ctr_desc_type_w),
      .ctr_desc_index_o  (pp_ctr_desc_index_w),
      .ctr_word_o        (pp_ctr_word_w),
      .ctr_data_i        (pp_ctr_data_w),
      .ctr_wait_i        (pp_ctr_wait_w),
      //! Table 5.22 GET_COUNTERS trigger: the descriptor arbiter above
      .ctr_change_i      (pp_ctr_evt_valid_w),
      .ctr_change_desc_type_i (pp_ctr_evt_type_w),
      .ctr_change_desc_index_i(pp_ctr_evt_index_w),
      //! GET_AUDIO_MAP: the processor asks, this file answers from the
      //! render map RAM (see the 7.4.44 answer block above)
      .amap_req_o        (pp_amap_req_w),
      .amap_desc_type_o  (pp_amap_desc_type_w),
      .amap_desc_index_o (pp_amap_desc_index_w),
      .amap_map_index_o  (pp_amap_map_index_w),
      .amap_sel_o        (pp_amap_sel_w),
      .amap_rec_o        (pp_amap_rec_w),
      .amap_data_i       (pp_amap_data_w),
      .amap_wait_i       (pp_amap_wait_w),
      .amap_edit_req_o   (pp_amap_edit_req_w),
      .amap_edit_phase_o (pp_amap_edit_phase_w),
      .amap_edit_remove_o(pp_amap_edit_remove_w),
      .amap_edit_desc_type_o(pp_amap_edit_desc_type_w),
      .amap_edit_desc_index_o(pp_amap_edit_desc_index_w),
      .amap_edit_count_o (pp_amap_edit_count_w),
      .amap_edit_rec_o   (pp_amap_edit_rec_w),
      .amap_edit_record_o(pp_amap_edit_record_w),
      .amap_edit_value_o (pp_amap_edit_value_w),
      .amap_edit_data_i  (pp_amap_edit_data_w),
      .amap_edit_wait_i  (pp_amap_edit_wait_w),
      //! the Milan-info face: GET_STREAM_INFO / GET_AVB_INFO / GET_AS_PATH
      //! answered from the gsi_answer block above
      .gsi_req_o         (pp_gsi_req_w),
      .gsi_kind_o        (pp_gsi_kind_w),
      .gsi_desc_type_o   (pp_gsi_desc_type_w),
      .gsi_desc_index_o  (pp_gsi_desc_index_w),
      .gsi_sel_o         (pp_gsi_sel_w),
      .gsi_ord_o         (pp_gsi_ord_w),
      .gsi_prop_fmt_o    (pp_gsi_prop_fmt_w),
      .gsi_data_i        (pp_gsi_data_w),
      .gsi_wait_i        (pp_gsi_wait_w),
      .gsi_avb_chg_i     (gsi_avb_chg_w),
      .gsi_asp_chg_i     (gsi_asp_chg_w),
      //! identity comes from the 0x600 CSR group, which is also what the
      //! generated entity model wrote - derive, never mirror.
      .entity_id_i       (cfg_adp_entity_id),
      .entity_model_id_i (cfg_adp_entity_model_id),
      //! numeric EUI-48 ([47:40] = first wire byte); cfg_mac_addr is the
      //! platform LSB-first convention, so byte-reverse exactly as the MAAP
      //! engine and the AAF/CRF framers do.
      .station_mac_i     (station_mac_be_w),
      .talker_sources_i  (cfg_adp_talker_sources),
      .talker_caps_i     (cfg_adp_talker_caps),
      .listener_sinks_i  (cfg_adp_listener_sinks),
      .listener_caps_i   (cfg_adp_listener_caps),
      //! the two ADPDU index fields the processor DOES expose a port for
      //! (0x600 group). The other five - entity_capabilities, valid_time,
      //! association_id, controller_capabilities, interface_index - have no
      //! port on protocol_processor_top and are beyond software's reach; see
      //! the milan_csr instantiation banner.
      .current_cfg_i     (cfg_adp_current_config),
      .identify_index_i  (cfg_adp_identify_index),
      //! WHICH SOURCES EXIST — derived from the entity shape, never a
      //! hand-set mask. ACMP_SRC_C is ADP_TALKER_SRC_C out of the generated
      //! header, so every declared STREAM_OUTPUT is enabled and no other
      //! index is. This is the gate the whole talker half hangs off: at 0 the
      //! walk never allocates a DA, acmp_declaring_o is stuck 0 and nothing
      //! this device owns ever transmits.
      .cfg_src_en_i      ({ACMP_SRC_C{1'b1}}),
      //! ...and the per-source stream_id the processor DECLAREs and ANSWERs
      //! with. Tied '0 (the shadow value) ACMP would answer, and SRP would
      //! declare, stream_id 0 for every source.
      .cfg_stream_id_i   (pp_src_sid_w),
      //! Milan v1.2 4.3.3.2 Table 4.4 MaxFrameSize, DERIVED from the wire
      //! width the framer was elaborated with (tctx_maxf_w) - never an
      //! independent constant, or the declaration and the frame disagree.
      //! Talker 0's value: every AAF talker in a build shares one width.
      .cfg_tspec_max_frame_i (tctx_maxf_w[0]),
      .cfg_acc_lat_ns_i  (cfg_lwsrp_latency),
      //! the SRP admission ceiling follows the negotiated link rate
      .port_rate_bps_i   (cfg_mac_is_1g ? 32'd1_000_000_000 : 32'd100_000_000),
      //! THE ENTITY ENABLE, from EITHER gate. ADP_CTRL.en (0x600 bit 0) is
      //! the historic entity-enable every board script and every bring-up
      //! recipe in this repository writes, and it used to start the ADP
      //! advertiser, the AECP listener and both ACMP halves at once. PP_CTRL.en
      //! (0x920 bit 0) is the plane's own. There is exactly ONE control plane
      //! now, so demanding both would strand every existing script and having
      //! only the new one would silently ignore the old bit: either enables
      //! the entity, and REGISTER_MAP records that.
      .enable_i          (pp_enable_w | cfg_adp_enable),
      .restore_go_i      (pp_restore_go_w),
      .link_up_i         (eff_link_w),
      //! GM_CHANGE: an edge on the committed grandmaster pair (CSR 0x624/8 +
      //! 0x62C). 1722.1-2021 6.2.6 makes a gPTP grandmaster change one of the
      //! events an entity re-advertises on, and with the legacy advertiser
      //! deleted this is the ONLY path to it - the old plane took the same
      //! fact as a level-driven re-advertise off cfg_adp_advertise_p.
      .gm_change_i       (pp_gm_change_p_w),
      .gm_id_i           (cfg_adp_gptp_gm),
      .gptp_domain_i     (cfg_adp_gptp_domain),
      .rx_tdata_i        (rx_axis_fabric.tdata),
      .rx_tkeep_i        (rx_axis_fabric.tkeep),
      .rx_tvalid_i       (rx_axis_fabric.tvalid),
      .rx_tready_i       (rx_axis_fabric.tready),
      .rx_tlast_i        (rx_axis_fabric.tlast),
      //! SUBSTITUTED: the drain is OFF and the packed AXIS port is this
      //! device's control egress (ctl_tx_mux, the leg the deleted
      //! aecp/acmp/acmpl/adp/lwsrp legs used to occupy).
      .tx_drain_i        (1'b0),
      .m_axis_tx_tdata   (pp_tx_tdata_w),
      .m_axis_tx_tkeep   (pp_tx_tkeep_w),
      .m_axis_tx_tvalid  (pp_tx_tvalid_w),
      .m_axis_tx_tlast   (pp_tx_tlast_w),
      .m_axis_tx_tready  (pp_tx_tready_w),
      //! the descriptor-image read master, straight out to the SoC
      .desc_mem_req_valid_o (o_desc_mem_req_valid),
      .desc_mem_req_ready_i (i_desc_mem_req_ready),
      .desc_mem_req_addr_o  (o_desc_mem_req_addr),
      .desc_mem_req_beats_o (o_desc_mem_req_beats),
      .desc_mem_rsp_valid_i (i_desc_mem_rsp_valid),
      .desc_mem_rsp_ready_o (o_desc_mem_rsp_ready),
      .desc_mem_rsp_data_i  (i_desc_mem_rsp_data),
      .desc_mem_rsp_last_i  (i_desc_mem_rsp_last),
      .desc_mem_rsp_err_i   (i_desc_mem_rsp_err),
      //! ...and the response buffer's own master, read AND write
      .resp_mem_req_valid_o (o_resp_mem_req_valid),
      .resp_mem_req_ready_i (i_resp_mem_req_ready),
      .resp_mem_req_addr_o  (o_resp_mem_req_addr),
      .resp_mem_req_beats_o (o_resp_mem_req_beats),
      .resp_mem_rsp_valid_i (i_resp_mem_rsp_valid),
      .resp_mem_rsp_ready_o (o_resp_mem_rsp_ready),
      .resp_mem_rsp_data_i  (i_resp_mem_rsp_data),
      .resp_mem_rsp_last_i  (i_resp_mem_rsp_last),
      .resp_mem_rsp_err_i   (i_resp_mem_rsp_err),
      .resp_mem_wr_valid_o  (o_resp_mem_wr_valid),
      .resp_mem_wr_ready_i  (i_resp_mem_wr_ready),
      .resp_mem_wr_addr_o   (o_resp_mem_wr_addr),
      .resp_mem_wr_data_o   (o_resp_mem_wr_data),
      .resp_mem_wr_strb_o   (o_resp_mem_wr_strb),
      .resp_mem_wr_done_i   (i_resp_mem_wr_done),
      .resp_mem_wr_err_i    (i_resp_mem_wr_err),
      .host_req_i        (pp_req_w),
      .host_we_i         (pp_we_w),
      .host_addr_i       (pp_addr_w),
      .host_wdata_i      (pp_wdata_w),
      .host_rdata_o      (pp_rdata_w),
      .host_ack_o        (pp_ack_w),
      .host_err_o        (pp_err_w),
      .restore_busy_o    (pp_restore_busy_w),
      .restore_done_o    (pp_restore_done_w),
      .restore_fail_o    (pp_restore_fail_w),
      .nvm_backed_o      (pp_nvm_backed_w),
      .restore_blank_o   (pp_restore_blank_w),
      .nvm_alarm_o       (pp_nvm_alarm_w),
      .rx_frames_o       (pp_rx_frames_w),
      .rx_drops_o        (pp_rx_drops_w),
      .tx_frames_o       (pp_tx_frames_w),
      //! the class-D fabric face, 1:1 onto the datapath nets declared above
      .srp_class_a_prio_o      (pp_cd_srp_class_a_prio_w),
      .srp_class_a_vid_o       (pp_cd_srp_class_a_vid_w),
      .srp_domain_adopted_o    (pp_cd_srp_domain_adopted_w),
      .srp_domain_change_o     (pp_cd_srp_domain_change_w),
      .srp_tk_decl_state_o     (pp_cd_srp_tk_decl_state_w),
      .srp_lstn_reg_state_o    (pp_cd_srp_lstn_reg_state_w),
      .srp_active_o            (pp_cd_srp_active_w),
      .srp_sr_admitted_o       (pp_cd_srp_sr_admitted_w),
      .srp_granted_slope_bps_o (pp_cd_srp_granted_slope_bps_w),
      .srp_src_fail_code_o     (pp_cd_srp_src_fail_code_w),
      .srp_src_fail_bridge_o   (pp_cd_srp_src_fail_bridge_w),
      .srp_sum_slope_bps_o     (pp_cd_srp_sum_slope_bps_w),
      .srp_over_limit_o        (pp_cd_srp_over_limit_w),
      .srp_tk_reg_state_o      (pp_cd_srp_tk_reg_state_w),
      .srp_lstn_decl_state_o   (pp_cd_srp_lstn_decl_state_w),
      .srp_acc_latency_o       (pp_cd_srp_acc_latency_w),
      .srp_snk_fail_code_o     (pp_cd_srp_snk_fail_code_w),
      .acmp_declaring_o        (pp_cd_acmp_declaring_w),
      .acmp_bound_o            (pp_cd_acmp_bound_w),
      .acmp_bound_eid_o        (pp_cd_acmp_bound_eid_w),
      .acmp_bound_sid_o        (pp_cd_acmp_bound_sid_w),
      .acmp_bound_dmac_o       (pp_cd_acmp_bound_dmac_w),
      .acmp_bound_vlan_o       (pp_cd_acmp_bound_vlan_w),
      .adp_next_avail_index_o  (pp_cd_adp_avail_index_w),
      //! the maap request face, answered by KL_pp_maap_shim below
      .maap_req_valid_o        (pp_maap_req_valid_w),
      .maap_req_ready_i        (pp_maap_req_ready_w),
      .maap_req_release_o      (pp_maap_req_release_w),
      .maap_req_src_o          (pp_maap_req_src_w),
      .maap_rsp_valid_i        (pp_maap_rsp_valid_w),
      .maap_rsp_ok_i           (pp_maap_rsp_ok_w),
      .maap_rsp_da_i           (pp_maap_rsp_da_w),
      .maap_conflict_valid_i   (pp_maap_confl_valid_w),
      .maap_conflict_src_i     (pp_maap_confl_src_w),
      .maap_conflict_ack_o     (pp_maap_confl_ack_w),
      //! The processor's INTERNAL Annex B engine stays DARK in this fabric:
      //! KL_maap above is the one allocator on this wire, and two engines
      //! defending one claim is a protocol violation, not a redundancy. The
      //! block config is fed from the SAME CSR words KL_maap consumes, so
      //! the day the internal engine is enabled (the KL_maap-retirement
      //! round) it claims exactly the block the fabric claims today and no
      //! second source of truth appears in the meantime.
      .cfg_maap_internal_i     (1'b0),
      .cfg_maap_count_i        (cfg_maap_count),
      .cfg_maap_seed_offset_i  (cfg_maap_seed_offset),
      .cfg_maap_seed_valid_i   (cfg_maap_seed_valid),
      //! the internal claim: all-zero while the engine is dark. Landed on
      //! named nets rather than open pins so the pp_shadow harness's
      //! no-waiver build stays PINMISSING-clean; the retirement round turns
      //! these into the real eff_aaf_dmac / gate sources.
      .maap_addr_o             (pp_maap_int_addr_nc_w),
      .maap_addr_valid_o       (pp_maap_int_valid_nc_w),
      .maap_state_o            (pp_maap_int_state_nc_w),
      .maap_conflicts_o        (pp_maap_int_confl_nc_w),
      .maap_defends_o          (pp_maap_int_dfnd_nc_w),
      .dbg_now_ms_o      ()
    );

  //! ------------------------------------------------------------------
    //! The block-allocator -> per-source adapter. Instantiated with the
    //! PLANE, not with the ENGINE: its block-side inputs are the maap nets,
    //! which exist in both arms of g_maap (the g_no_maap arm ties
    //! maap_addr_valid to 0), so a MAAP_P = 0 build elaborates unchanged and
    //! the shim answers every request "no address" in one cycle. That is the
    //! refusing value the processor is designed for - ready ASSERTS and the
    //! response says ok = 0 - and NOT ready-stuck-low, which would park the
    //! talker's single walker for 1024 cycles per attempt and make the whole
    //! talker half of ACMP deaf while it waited. See KL_pp_maap_shim.sv's
    //! banner, decision 1.
    KL_pp_maap_shim #(
      .N_SRC_P (ACMP_SRC_C)
    ) pp_maap_shim (
      .clk_i            (axis_clk),
      .rst_n            (axis_resetn),
      .blk_addr_i       (maap_addr),
      .blk_valid_i      (maap_addr_valid),
      .blk_count_i      (cfg_maap_count),
      .req_valid_i      (pp_maap_req_valid_w),
      .req_ready_o      (pp_maap_req_ready_w),
      .req_release_i    (pp_maap_req_release_w),
      .req_src_i        (pp_maap_req_src_w),
      .rsp_valid_o      (pp_maap_rsp_valid_w),
      .rsp_ok_o         (pp_maap_rsp_ok_w),
      .rsp_da_o         (pp_maap_rsp_da_w),
      .conflict_valid_o (pp_maap_confl_valid_w),
      .conflict_src_o   (pp_maap_confl_src_w),
      .conflict_ack_i   (pp_maap_confl_ack_w)
    );


endmodule

`default_nettype wire
