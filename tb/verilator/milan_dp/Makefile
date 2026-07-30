# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Integration harness for milan_datapath.sv (the PS-less §A.9 wrapper). Builds the
# whole TSN core (csr + classify/CBS + PTP + rx-filter + ADP + events) and drives
# it over the AXI4-Lite CSR + the DMA/MAC AXIS ports.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
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
# ...and as PREREQUISITES: make cannot see through a `include, so a
# regenerated shape must still force a rebuild or the harness keeps testing
# the previous entity definition out of a stale objdir.
GEN_CSR     = $(RTL_DIR)/common/csr/gen/lwsrp_csr_defaults.svh
SHAPE_DEF   = $(RTL_DIR)/common/csr/gen/adp_shape_defaults.svh
SHAPE_4x4_F = $(CFG_DIR)/endstation_arty_4x4/gen/adp_shape_defaults.svh
SHAPE_8x8_F = $(CFG_DIR)/endstation_ax7101_8x8/gen/adp_shape_defaults.svh
GEN_ALL     = $(GEN_CSR) $(SHAPE_DEF) $(SHAPE_4x4_F) $(SHAPE_8x8_F)

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/common/csr +incdir+$(RTL_DIR)/common/eth_event_counter \
         +incdir+$(RTL_DIR)/ieee17221/adp +incdir+$(RTL_DIR)/ieee8021q/ts \
         +incdir+$(RTL_DIR)/ieee8021as/ptp_timestamp +incdir+$(AXIS_DIR) \
         +incdir+$(RTL_DIR)/ieee17221/aecp +incdir+$(RTL_DIR)/ieee17221/aecp/gen \
         -Wall -Wno-fatal -Werror-USERERROR -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR \
         -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE -Wno-PINMISSING -Wno-SELRANGE \
         -Wno-TIMESCALEMOD \
         -GPB_PREFILL_C=2 -GCLKV_QTICK_CYC_P=4096 \
         -CFLAGS "-std=c++17 -O2"

C  = $(RTL_DIR)/common
Q  = $(RTL_DIR)/ieee8021q/ts
P  = $(RTL_DIR)/ieee8021as/ptp_timestamp

SRCS = $(C)/ethernet_packet_pkg.sv $(C)/axi_stream_if.sv $(RTL_DIR)/ieee17221/adp/adp_pkg.sv \
       $(AXIS_DIR)/axis_fifo.v $(AXIS_DIR)/axis_demux.v $(AXIS_DIR)/axis_arb_mux.v \
       $(AXIS_DIR)/arbiter.v $(AXIS_DIR)/priority_encoder.v \
       $(Q)/traffic_class_map.sv $(Q)/traffic_classifier.sv $(Q)/credit_based_shaper.sv \
       $(Q)/traffic_shaping_core.sv $(Q)/traffic_queues.sv $(Q)/traffic_controller_802_1q.sv \
       $(P)/timestamp_counter.sv $(P)/ptp_csr_sync.sv \
       $(C)/cdc_pulse.sv $(C)/cdc_handshake.sv $(C)/axis_mux_rr_2in_1out.sv \
       $(P)/ptp_ts_core.sv $(P)/ptp_ts_top.sv $(P)/KL_ptp_clock_validity.sv \
       $(RTL_DIR)/ieee8021q/filtering/tcam.sv $(RTL_DIR)/ieee8021q/filtering/rx_mac_filter.sv $(C)/tx_ifg_gasket.sv $(RTL_DIR)/ieee1722/aaf/KL_pcm_lpf.sv $(RTL_DIR)/ieee1722/aaf/KL_pcm_route.sv \
       $(C)/KL_link_guard.sv \
       $(RTL_DIR)/ieee17221/adp/adp_advertiser.sv $(RTL_DIR)/ieee17221/adp/adp_tx_arbiter.sv \
       $(RTL_DIR)/ieee17221/aecp/aecp_pkg.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_packet_validator.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_common_parser.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_l0_state.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_timers.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_accessor.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_aem_store.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_aem_dyn_mux.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_response_builder.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_ingress.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_top.sv \
       $(RTL_DIR)/ieee17221/acmp/acmp_pkg.sv $(RTL_DIR)/ieee17221/acmp/KL_acmp_tlkr_ctx.sv $(RTL_DIR)/ieee17221/acmp/KL_acmp_responder.sv \
       $(RTL_DIR)/ieee17221/acmp/KL_acmp_lstn_ctx.sv $(RTL_DIR)/ieee17221/acmp/KL_acmp_listener.sv \
       $(RTL_DIR)/ieee8021q/srp/lwsrp_pkg.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_timers.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_tx.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ingress.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_walker.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_registrar.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ta_registrar.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_rx.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_bw_gate.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ctx.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ctx_tx.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_top.sv \
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
       $(RTL_DIR)/ieee1722/avtp/KL_talker_diag_ctx.sv \
       $(RTL_DIR)/ieee1722/avtp/KL_media_clock_restart.sv \
	$(RTL_DIR)/ieee1722/crf/KL_crf_rx.sv \
	$(RTL_DIR)/ieee1722/crf/KL_crf_tx.sv \
	$(RTL_DIR)/ieee1722/crf/KL_mmcm_drp_servo.sv \
       $(RTL_DIR)/ieee1722/maap/KL_maap.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_i2s_playback.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_i2s_feed_mux.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_tone_gen.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_latency_taps.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_media_adv.sv \
       $(RTL_DIR)/common/cdc_pair_fifo.sv \
       $(RTL_DIR)/common/eth_event_counter/ethernet_events.sv \
       $(RTL_DIR)/common/csr/milan_csr.sv \
       $(RTL_DIR)/milan/milan_datapath.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

# tier-1 optional blocks, ALL pruned at once (docs/design/AREA_BUDGET.md).
# Every one defaults to 1 = PRESENT, so the two builds above are untouched;
# this third build is the only place the 0 side is elaborated - and a prune
# that was never elaborated is not a prune.
PRUNE_G = -GMCSERVO_P=0 -GLTAP_P=0 -GMAAP_P=0 -GI2SPB_P=0 -GRXFILT_P=0 -GLPF_P=0

run: $(GEN_ALL)
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS) $(SRCS) $(CPP) -o Vmilan_dp_sim
	$(VERILATOR) $(SHAPE_4x4) $(VFLAGS) --Mdir obj_nxn -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
	$(VERILATOR) $(SHAPE_8x8) $(VFLAGS) --Mdir obj_nxn8 -GN_STREAMS=8 -CFLAGS -DNSTREAMS_TB=8 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn8
# LPF_P=0 is the SPENT area lever (docs/NXN_ARCHITECTURE.md 6.2/6.3): the
# ax7101 shipping argv carries --no-render-lpf, so the pruned shape is a
# SHIPPING shape and has to be in the suite. The claim being proved is
# "no digital acceptance surface moves" - so this leg runs the SAME
# self-checking harness, unchanged, and every check must give the same
# answer. It does not merely elaborate: it re-runs the whole legacy leg.
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS) --Mdir obj_nolpf -GLPF_P=0 $(SRCS) $(CPP) -o Vmilan_dp_nolpf
# obj_prune is the OTHER direction: all six tier-1 blocks pruned at once, on a
# dedicated harness that proves the inert values are STRUCTURAL zeros rather
# than not-armed-yet zeros. The two legs answer different questions and both
# stay.
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS) --Mdir obj_prune $(PRUNE_G) $(SRCS) sim_prune.cpp -o Vmilan_dp_prune
	@echo "======================================================================"
	./obj_dir/Vmilan_dp_sim
	./obj_nxn/Vmilan_dp_nxn
	./obj_nxn8/Vmilan_dp_nxn8
	@echo "---- LPF_P=0 (pruned render tap, the ax7101 shipping shape) ----"
	./obj_nolpf/Vmilan_dp_nolpf
	@echo "---- all six tier-1 blocks pruned ----"
	./obj_prune/Vmilan_dp_prune

clean:
	rm -rf obj_dir obj_nxn obj_nxn8 obj_nolpf obj_prune
