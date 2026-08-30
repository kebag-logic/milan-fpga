# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Integration harness for milan_datapath.sv. Builds the
# whole TSN core (csr + classify/CBS + PTP + rx-filter + ADP + events) and drives
# it over the AXI4-Lite CSR + MAC AXIS ports.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
PP_DIR     = ../../../protocol-processor/hdl
TOP        = milan_datapath

# ENTITY SHAPE (2026-07-27). milan_datapath and milan_csr both `include
# gen/adp_shape_defaults.svh - the stream counts the entity advertises AND the
# ACMP context-array sizing - and that file is GENERATED from an end-station
# config by sw/builder/endstation_builder.py. The default 1x1 copy lives in
# hdl/common/csr/gen; the NxN legs elaborate a DIFFERENT shape by putting that
# config's generated directory FIRST on the include path. There is no way to
# build an N=8 datapath against the 1x1 entity definition and not notice: the
# ACMP arrays would be sized 1/2 and the harness reads the mismatch straight
# off 0x618/0x61C.
CFG_DIR    = ../../../configs/generated
# The N=1 legs need this JUST AS MUCH as the NxN ones. Without it they fall
# through to hdl/common/csr/gen/, which is whichever config was last written
# with --write-rtl - so regenerating the tree for the 8x8 ship shape made the
# N_STREAMS=1 legs elaborate a 9-source ACMP array with 7 sources undriven,
# and the ONLY thing that caught it was Verilator's -Werror-UNDRIVEN. Vivado
# would have tied those DMAC/VID bits to zero and built a bitstream whose
# talker sources 2..8 advertise a null destination address. Name the shape.
SHAPE_1x1  = +incdir+$(CFG_DIR)/endstation_arty_current
SHAPE_4x4  = +incdir+$(CFG_DIR)/endstation_arty_4x4
SHAPE_8x8  = +incdir+$(CFG_DIR)/endstation_ax7101_8x8
# THE SHAPE THE AX7101 ACTUALLY FLASHES (sw/litex/build.sh cfg_ax7101):
# one AAF talker + one AAF sink over a TDM8 master at 8 wire channels, plus
# the CRF media clock output/input pair, so ADP_TALKER_SRC_C = 2. Nothing in
# this suite elaborated it until now - SHAPE_1x1 is the ARTY entity and the
# NxN legs are 4x4/8x8 - and every defect that needs "1 stream AND 8 wire
# channels AND the CRF source" at the same time lived in that hole.
SHAPE_AX1x1 = +incdir+$(CFG_DIR)/endstation_ax7101_1x1_tdm8
# ...and as PREREQUISITES: make cannot see through a `include, so a
# regenerated shape must still force a rebuild or the harness keeps testing
# the previous entity definition out of a stale objdir.
GEN_CSR     = $(RTL_DIR)/common/csr/gen/lwsrp_csr_defaults.svh
SHAPE_DEF   = $(RTL_DIR)/common/csr/gen/adp_shape_defaults.svh
SHAPE_4x4_F = $(CFG_DIR)/endstation_arty_4x4/gen/adp_shape_defaults.svh
SHAPE_8x8_F = $(CFG_DIR)/endstation_ax7101_8x8/gen/adp_shape_defaults.svh
SHAPE_AX1_F = $(CFG_DIR)/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh
GEN_ALL     = $(GEN_CSR) $(SHAPE_DEF) $(SHAPE_4x4_F) $(SHAPE_8x8_F) $(SHAPE_AX1_F)
# the DIVERGENT-shape leg's generated header + bench expectations: every
# tracked config declares the same first format on every row, so only a
# generated divergent header can prove the per-row verdict base and reset
# GET answer are the ADDRESSED row's and not row 0's (review, issue #67)
SHAPE_DV    = +incdir+gen_divergent
SHAPE_DV_F  = gen_divergent/gen/adp_shape_defaults.svh

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/common/csr +incdir+$(RTL_DIR)/common/eth_event_counter \
         +incdir+$(RTL_DIR)/ieee17221/adp +incdir+$(RTL_DIR)/ieee8021q/ts \
         +incdir+$(RTL_DIR)/ieee8021as/ptp_timestamp +incdir+$(AXIS_DIR) \
         -Wall -Wno-fatal -Werror-USERERROR -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR \
         -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE -Wno-PINMISSING -Wno-SELRANGE \
         -Wno-TIMESCALEMOD \
         -GPB_PREFILL_C=2 -GCLKV_QTICK_CYC_P=4096 -GLDIAG_IVAL_CYC_P=256 \
         -GDIAG_TICK_CYC_P=256 \
         -CFLAGS "-std=c++17 -O2"

# The broad historical integration legs use the direct option-OFF elaboration:
# it is an ownerless verification boundary, not an alternate runtime owner.
# obj_gptp deliberately omits the override and therefore proves the product
# default rather than a forced -G1.
GPTP_OFF_VFLAGS = $(VFLAGS) -GGPTP_PLANE_EN_P=0
DP_VFLAGS = $(GPTP_OFF_VFLAGS)
# The product-on media-wire test needs its compressed hold to outlive one CRF
# interval while remaining below syncReceiptTimeout. Its processor millisecond
# is also compressed to 100 cycles so the one-second GET_COUNTERS limiter can
# reopen without letting that selected Sync expire. Keep both overrides local
# to obj_gptp; option OFF retains the broad-suite 4096-cycle shortcut.
GPTP_MS_CYC = 100
GPTP_ON_VFLAGS = $(filter-out -GCLKV_QTICK_CYC_P=4096,$(VFLAGS)) \
                 -GCLKV_QTICK_CYC_P=131072 \
                 -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=$(GPTP_MS_CYC) \
                 -CFLAGS "-DPP_MS_CYC_TB=$(GPTP_MS_CYC)"

C  = $(RTL_DIR)/common
Q  = $(RTL_DIR)/ieee8021q/ts
P  = $(RTL_DIR)/ieee8021as/ptp_timestamp

# THE PROTOCOL PROCESSOR IS PART OF THE DATAPATH NOW. milan_datapath
# instantiates KL_pp_shadow unconditionally - it is the control plane, the old
# 1722.1/SRP plane is deleted - so the processor's sources are datapath
# sources. They come FIRST: their packages must be declared before the modules
# that import them. This list is exported by `print-srcs`, so tb/verilator/
# pp_shadow gets it without keeping a second copy that could drift.
# The submodule half is DERIVED from the tree, not listed here. Four build
# inputs used to carry it by hand, each naming another as authoritative, and all
# four went stale together the moment the pin moved. The parent's own two files
# stay explicit: they are this repository's, not the submodule's.
PP_DERIVED := $(shell python3 $(CURDIR)/../../../scripts/pp_srcs.py --prefix $(PP_DIR))
# TAKE THE STATUS. $(shell) discards it, so the generator's refusal to emit an
# empty list does not cross the process boundary on its own: without this the
# submodule half simply vanishes from PP_SRCS and make carries on to build a
# datapath with no control plane in it.
ifneq ($(.SHELLSTATUS),0)
$(error scripts/pp_srcs.py failed; the protocol-processor submodule source list could not be derived)
endif
PP_SRCS := $(PP_DERIVED) \
       $(RTL_DIR)/milan/KL_pp_shadow.sv $(RTL_DIR)/milan/KL_pp_maap_shim.sv

# the gPTP plane (issue #114): parsed by every leg (the instantiation
# must resolve), elaborated only where -GGPTP_PLANE_EN_P=1
GPTP_DIR = ../../../gptp-processor/hdl
GPTP_SRCS = $(GPTP_DIR)/ucpu/gptp_ucpu_pkg.sv $(GPTP_DIR)/ucpu/KL_gptp_ucpu.sv \
       $(GPTP_DIR)/wire/KL_gptp_rx_parser.sv $(GPTP_DIR)/wire/KL_gptp_tx_slot.sv \
       $(GPTP_DIR)/common/KL_gptp_timer.sv $(GPTP_DIR)/top/KL_gptp_engine.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_shadow.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_txstamp.sv

SRCS = $(PP_SRCS) $(GPTP_SRCS) $(C)/ethernet_packet_pkg.sv $(C)/axi_stream_if.sv \
       $(AXIS_DIR)/axis_fifo.v $(AXIS_DIR)/axis_demux.v $(AXIS_DIR)/axis_arb_mux.v \
       $(AXIS_DIR)/arbiter.v $(AXIS_DIR)/priority_encoder.v \
       $(Q)/traffic_class_map.sv $(Q)/traffic_classifier.sv $(Q)/credit_based_shaper.sv \
       $(Q)/traffic_shaping_core.sv $(Q)/traffic_queues.sv $(Q)/traffic_controller_802_1q.sv \
       $(P)/timestamp_counter.sv $(P)/ptp_csr_sync.sv \
       $(C)/cdc_pulse.sv $(C)/cdc_handshake.sv $(C)/axis_mux_rr_2in_1out.sv \
       $(P)/ptp_ts_core.sv $(P)/ptp_ts_top.sv $(P)/KL_ptp_clock_validity.sv \
       $(RTL_DIR)/ieee8021q/filtering/tcam.sv $(RTL_DIR)/ieee8021q/filtering/rx_mac_filter.sv $(C)/tx_ifg_gasket.sv $(RTL_DIR)/ieee1722/aaf/KL_pcm_lpf.sv $(RTL_DIR)/ieee1722/aaf/KL_pcm_route.sv \
       $(C)/KL_link_guard.sv \
       $(RTL_DIR)/ieee17221/adp/adp_tx_arbiter.sv \
       $(RTL_DIR)/ieee1722/aaf/aaf_talker_i2s.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_capture_i2s.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_tdm_capture.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_tdm_capture_master.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_pair_blend.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_pair_zero_fill.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_tdm_render.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_chan_map_render.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_chan_map_capture.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_packetizer.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_rx_depacketizer.sv \
       $(RTL_DIR)/ieee1722/avtp/avtp_subtype_pkg.sv \
       $(RTL_DIR)/ieee1722/avtp/avtp_stream_parser.sv \
       $(RTL_DIR)/ieee1722/avtp/KL_stream_table.sv \
       $(RTL_DIR)/ieee1722/avtp/KL_avtp_rx_monitor.sv \
       $(RTL_DIR)/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv \
       $(RTL_DIR)/ieee1722/avtp/KL_media_clock_restart.sv \
       $(RTL_DIR)/ieee1722/avtp/KL_talker_diag_ctx.sv \
	$(RTL_DIR)/ieee1722/crf/KL_crf_rx.sv \
	$(RTL_DIR)/ieee1722/crf/KL_crf_tx.sv \
	$(RTL_DIR)/ieee1722/crf/KL_mmcm_drp_servo.sv \
	$(RTL_DIR)/ieee1722/crf/KL_media_nco.sv \
       $(RTL_DIR)/ieee1722/maap/KL_maap.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_i2s_playback.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_i2s_feed_mux.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_tone_gen.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_latency_taps.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_latency_tap_bank.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_media_adv.sv \
       $(RTL_DIR)/common/cdc_pair_fifo.sv \
       $(RTL_DIR)/common/eth_event_counter/ethernet_events.sv \
       $(RTL_DIR)/common/eth_event_counter/event_counter.sv \
       $(RTL_DIR)/common/csr/milan_csr.sv \
       $(RTL_DIR)/milan/milan_datapath.sv
CPP  = sim_main.cpp

.PHONY: all run gptp option-off clean
all: run

# tier-1 optional blocks, ALL pruned at once (docs/design/AREA_BUDGET.md).
# Every one defaults to 1 = PRESENT, so the two builds above are untouched;
# this third build is the only place the 0 side is elaborated - and a prune
# that was never elaborated is not a prune.
PRUNE_G = -GMCSERVO_P=0 -GLTAP_P=0 -GMAAP_P=0 -GI2SPB_P=0 -GRXFILT_P=0 -GLPF_P=0

# THE SHIPPING ALINX SHAPE, stated ONCE. sim_main.cpp runs three different
# elaborations now, so the geometry it asserts against can no longer be a
# literal in the C++ - and it must not be a SECOND literal in the recipe
# either. Each value below feeds BOTH the -G that builds the gateware and the
# -D that tells the harness what it is driving, so the two cannot drift: a
# copied number is a number that diverges in silence. Anything not named here
# keeps milan_datapath's own default, which is also what the harness assumes.
AX_CHANS = 8
AX_I2SPB = 0
AX_SLOTS = 8

# The ACMP listener transition ROM is GENERATED, and protocol_processor_top
# $$readmemh's it by the relative name below - so it must exist in the RUN
# directory, not just the build one.
ltn_rom.hex: $(PP_DIR)/acmp/rom/gen_ltn_rom.py
	python3 $< -o $@

# ...and the AECP uCPU microcode image, same relative-$readmemh contract.
ucode.hex: $(PP_DIR)/aecp/ucode/gen_ucode.py
	python3 $< -o $@

# ...and the gPTP plane's, generated for the leg's 2 MHz sim clock so the
# boot cadence fires within a runnable window (same relative-$readmemh).
gptp_ucode.hex: $(GPTP_DIR)/ucode/gen_gptp_ucode.py
	python3 $< --clk-hz 2000000 --cease-ms 3000 -o $@

$(SHAPE_DV_F): gen_divergent_shape.py $(SHAPE_4x4_F) ../../../sw/builder/endstation_builder.py
	python3 gen_divergent_shape.py

gptp: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_ON_VFLAGS) --Mdir obj_gptp \
	  -GMILAN_CLK_FREQ_HZ=2000000 \
	  $(SRCS) sim_gptp.cpp -o Vmilan_dp_gptp
	./obj_gptp/Vmilan_dp_gptp

# Focused ownerless boundary: the same 1x1 harness used by the broad suite,
# with the gPTP product plane structurally absent and every legacy write inert.
option-off: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_1x1) $(DP_VFLAGS) $(SRCS) $(CPP) -o Vmilan_dp_sim
	./obj_dir/Vmilan_dp_sim

run: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL) $(SHAPE_DV_F) gptp
	$(VERILATOR) $(SHAPE_1x1) $(DP_VFLAGS) $(SRCS) $(CPP) -o Vmilan_dp_sim
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir obj_nxn -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
# the divergent-shape leg: arty_4x4's entity with input row 1 declaring the
# 96 kHz base - same channel count as row 0, so the ONLY discriminator is
# the base, which is precisely what a row-0 lookup regression would miss
	$(VERILATOR) $(SHAPE_DV) $(DP_VFLAGS) --Mdir obj_nxndv -GN_STREAMS=4 -CFLAGS "-DNSTREAMS_TB=4 -DDIVERGENT_TB=1 -I$(CURDIR)/gen_divergent" $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxndv
# obj_nxn8 is the ONLY leg that elaborates the task #65 loopback lane
# (-GLOOPBACK_P=1, paired with -DLOOPBACK_TB so the C++ side knows which
# gateware it is driving). The other two sim_nxn legs run with the lane OFF
# and pin the other half of the contract - a mapped loopback slot is silent
# by construction when the parameter did not build the bucket, which is why
# the builder may not point a power-on mapping at one.
# -DLB_SEQ_FIXED: the 0x0036 loop-source paced-replay law is IN - [T68]
# asserts zero dup / zero skip / whole-ramp / clean tail instead of the
# pre-fix stair signature.
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir obj_nxn8 -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1" $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn8
# THE SHIPPING ARTY SHAPE, and until 2026-07-30 nothing in the suite
# elaborated it. obj_nxn above builds endstation_arty_4x4's ENTITY (4 streams)
# but leaves TALKER_WIRE_CHANS_P at its default 2, so every leg ran with the
# framer width equal to the TSpec shadow's reset value - and a disagreement
# between those two is invisible when they are the same number. The board
# builds --talker-wire-chans 4 over the TDM8+I2S blend (AUDIO_IF_SLOTS_P=8,
# master, I2S pair at slot 0), which is what these -G flags name. The
# from-reset TSpec bite in sim_nxn.cpp only has teeth here: it compares the
# declared MaxFrameSize against the emitted MSDU, and at width 2 both sides
# agree even with the defect present.
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir obj_nxn4c -GN_STREAMS=4 \
	  -GTALKER_WIRE_CHANS_P=4 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 \
	  -GAUDIO_IF_I2S_PAIR_P=1 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn4c
# LPF_P=0 is the SPENT area lever (docs/design/AREA_BUDGET.md): the
# ax7101 shipping argv carries --no-render-lpf, so the pruned shape is a
# SHIPPING shape and has to be in the suite. The claim being proved is
# "no digital acceptance surface moves" - so this leg runs the SAME
# self-checking harness, unchanged, and every check must give the same
# answer. It does not merely elaborate: it re-runs the whole legacy leg.
	$(VERILATOR) $(SHAPE_1x1) $(DP_VFLAGS) --Mdir obj_nolpf -GLPF_P=0 $(SRCS) $(CPP) -o Vmilan_dp_nolpf
# obj_prune is the OTHER direction: all six tier-1 blocks pruned at once, on a
# dedicated harness that proves the inert values are STRUCTURAL zeros rather
# than not-armed-yet zeros. The two legs answer different questions and both
# stay.
	$(VERILATOR) $(SHAPE_1x1) $(DP_VFLAGS) --Mdir obj_prune $(PRUNE_G) $(SRCS) sim_prune.cpp -o Vmilan_dp_prune
# THE SHIPPING ALINX SHAPE, byte for byte the cfg_ax7101 argv in
# sw/litex/build.sh: 1 stream, 8 wire channels off a TDM8 MASTER front end,
# the loopback lane backed, I2S playback and the render LPF both PRUNED.
# Every one of those had desk coverage on its
# own; the combination - which is the only combination that ever reaches a
# board - had none, and three defects were living in it.
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_OFF_VFLAGS) --Mdir obj_ax1x1 \
	  -GTALKER_WIRE_CHANS_P=$(AX_CHANS) -GAUDIO_IF_SLOTS_P=$(AX_SLOTS) \
	  -GAUDIO_IF_MASTER_P=1 \
	  -GLOOPBACK_P=1 -GI2SPB_P=$(AX_I2SPB) -GLPF_P=0 \
	  -CFLAGS "-DWIRE_CHANS_TB=$(AX_CHANS) -DI2SPB_TB=$(AX_I2SPB) -DAIF_SLOTS_TB=$(AX_SLOTS)" \
	  $(SRCS) $(CPP) -o Vmilan_dp_ax1x1
# THE SAME SHIPPING SHAPE, CLOCKED HONESTLY. Every other leg toggles
# clk_audio_i/clk_tdm_i 1:1 with axis_clk, so the 391/1591 divider plan that
# puts the TDM word clock -10.6393 ppm from the AAF packet grid does not exist
# anywhere in the tree and the ALIGNMENT requirement cannot be observed. This
# leg drives the true ratio and measures the drift RATE (waiting for a whole
# sample of slip would be 195,815,385 axis cycles). Kept a SEPARATE binary
# rather than an #ifdef through sim_nxn's 380-odd checks: none of those care
# about the audio clock's rate, and re-clocking them to find out would be a
# large blast radius for no gain.
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_OFF_VFLAGS) --Mdir obj_aclk \
	  -GTALKER_WIRE_CHANS_P=$(AX_CHANS) -GAUDIO_IF_SLOTS_P=$(AX_SLOTS) \
	  -GAUDIO_IF_MASTER_P=1 \
	  -GLOOPBACK_P=1 -GI2SPB_P=$(AX_I2SPB) -GLPF_P=0 \
	  $(SRCS) sim_aclk.cpp -o Vmilan_dp_aclk
	@echo "======================================================================"
# Milan 5.4.5 TIMED (issue #69): the processor's timebase compressed
# 1000x through its own override parameters (PP_TIM_DIV_US_P = 1 clock per
# microsecond tick, PP_TIM_DIV_MS_P = 100 ticks per millisecond), so one
# processor millisecond is 100 fabric cycles and the GET_COUNTERS one-second
# limit and the 30-60 s departing-controller monitor are both runnable in a
# few million cycles. The fabric clock itself stays at its shipping value.
# -DMS_CYC_TB hands the same number to the harness so the two cannot drift.
# sim_nxn's [NOTIFY] section on the shipping 1x1 shape, exiting right after
# the descriptor image is served (NOTIFY_TIMED_TB); the real-time legs run
# the same section untimed.
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_OFF_VFLAGS) --Mdir obj_notify \
	  -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100 \
	  -CFLAGS "-DNSTREAMS_TB=1 -DNOTIFY_TIMED_TB=1 -DMS_CYC_TB=100" \
	  $(SRCS) sim_nxn.cpp -o Vmilan_dp_notify
	./obj_dir/Vmilan_dp_sim
	@echo "---- Milan 5.4.5 notifications, TIMED on the compressed processor timebase ----"
	./obj_notify/Vmilan_dp_notify
	./obj_nxn/Vmilan_dp_nxn
	@echo "---- the DIVERGENT shape: input row 1 declares the 96 kHz base ----"
	./obj_nxndv/Vmilan_dp_nxndv
	./obj_nxn8/Vmilan_dp_nxn8
	@echo "---- the shipping Arty shape: 4 streams x 4 wire channels ----"
	./obj_nxn4c/Vmilan_dp_nxn4c
	@echo "---- LPF_P=0 (pruned render tap, the ax7101 shipping shape) ----"
	./obj_nolpf/Vmilan_dp_nolpf
	@echo "---- all six tier-1 blocks pruned ----"
	./obj_prune/Vmilan_dp_prune
	@echo "---- THE SHIPPING ALINX SHAPE: 1 stream x 8 wire channels, TDM8 master ----"
	./obj_ax1x1/Vmilan_dp_ax1x1
	@echo "---- the same shape at the TRUE clk_audio ratio (391/1591) ----"
	./obj_aclk/Vmilan_dp_aclk

# The datapath source list, for suites that must elaborate the SAME gateware
# under a different parameter set (tb/verilator/pp_shadow). Exporting it beats
# copying it: a second hand-maintained list is a list that drifts, and the one
# thing every leg here depends on is that SRCS is the list that elaborates.
# Paths are relative to a tb/verilator/<suite>/ directory, which every consumer
# of this target also is.
.PHONY: print-srcs print-pp-srcs
print-srcs:
	@echo $(SRCS)

# ...and the protocol-processor half on its own, for a suite that keeps its
# own datapath list but must still build the plane inside it.
print-pp-srcs:
	@echo $(PP_SRCS)

clean:
	rm -rf ltn_rom.hex ucode.hex gptp_ucode.hex obj_dir obj_nxn obj_nxn8 obj_nxn4c obj_nolpf obj_prune obj_ax1x1 obj_aclk obj_nxndv obj_gptp obj_notify gen_divergent
