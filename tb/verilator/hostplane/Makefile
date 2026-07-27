# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Host-plane coverage harness for milan_datapath.sv in the SILICON SHAPE.
#
# The milan_dp suite proves the wrapper at the RTL DEFAULT shape (N_STREAMS=1,
# PB_PREFILL_C shrunk); this suite elaborates the exact parameter set the
# cfg_ax8x8 build ships (sw/litex/build.sh -> milan_soc.py argv mapping, see
# README.md) and asserts on the HOST-FACING lanes: host RX AXIS delivery,
# ts-record production, filter no-leak both ways, observer purity under host
# backpressure - the lane family whose silicon regression class the green
# default-shape suites cannot see.
#
#   make        - build all shapes and run the self-checking harnesses
#   make build  - build only (the "suite BUILDS" gate)
#   make clean  - remove build artifacts
#
# Born 2026-07-25 on a known-broken tree (host RX dead on silicon while every
# fabric-autonomous path ran); the LTAP same-cycle KNOWN-FAIL was fixed
# 2026-07-26 (KL_aaf_latency_taps cascade walk) - expected green everywhere.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = milan_datapath

# Waiver set mirrors tb/verilator/milan_dp (same DUT, same third-party cores).
VFLAGS_COMMON = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/common/csr +incdir+$(RTL_DIR)/common/eth_event_counter \
         +incdir+$(RTL_DIR)/ieee17221/adp +incdir+$(RTL_DIR)/ieee8021q/ts \
         +incdir+$(RTL_DIR)/ieee8021as/ptp_timestamp +incdir+$(AXIS_DIR) \
         +incdir+$(RTL_DIR)/ieee17221/aecp +incdir+$(RTL_DIR)/ieee17221/aecp/gen \
         -Wall -Wno-fatal -Werror-USERERROR -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR \
         -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE -Wno-PINMISSING -Wno-SELRANGE \
         -Wno-TIMESCALEMOD \
         -CFLAGS "-std=c++17 -O2"

# ---- silicon shape (cfg_ax8x8, sw/litex/build.sh -> milan_soc.py; README.md
#      documents the argv->parameter derivation so drift is visible) --------
#   --num-streams 8        -> N_STREAMS=8
#   --milan-clk-freq 100e6 -> MILAN_CLK_FREQ_HZ=100000000
#   (no --audio-interface) -> AUDIO_IF_SLOTS_P=0   (i2s_philips default)
#   (no --aaf-playback)    -> AAF_PLAYBACK_P=0     (SV default, generate off)
#   (never set by the SoC) -> PB_PREFILL_C=0       (silicon default kept -
#                             milan_dp shrinks it to 2; we do NOT)
G_AX8X8 = -GN_STREAMS=8 -GMILAN_CLK_FREQ_HZ=100000000 -GAUDIO_IF_SLOTS_P=0

# ---- cfg-sweep smoke shapes (case e) ---------------------------------------
G_SMALL = -GN_STREAMS=1 -GMILAN_CLK_FREQ_HZ=50000000  -GAUDIO_IF_SLOTS_P=0
G_N4    = -GN_STREAMS=4 -GMILAN_CLK_FREQ_HZ=100000000 -GAUDIO_IF_SLOTS_P=0
G_TDM8  = -GN_STREAMS=8 -GMILAN_CLK_FREQ_HZ=100000000 -GAUDIO_IF_SLOTS_P=8

C  = $(RTL_DIR)/common
Q  = $(RTL_DIR)/ieee8021q/ts
P  = $(RTL_DIR)/ieee8021as/ptp_timestamp

# Source set = milan_soc.py _MILAN_DATAPATH_SOURCES (the silicon truth),
# de-duplicated (the Python list carries a few doubles Vivado tolerates) and
# minus KL_pcm_ring_bram.sv (SoC-layer --pcm-ring bram glue, not instantiated
# inside milan_datapath). event_counter.sv resolves via +incdir like Vivado.
SRCS = $(C)/ethernet_packet_pkg.sv $(C)/axi_stream_if.sv $(RTL_DIR)/ieee17221/adp/adp_pkg.sv \
       $(AXIS_DIR)/axis_fifo.v $(AXIS_DIR)/axis_demux.v $(AXIS_DIR)/axis_arb_mux.v \
       $(AXIS_DIR)/arbiter.v $(AXIS_DIR)/priority_encoder.v \
       $(Q)/traffic_class_map.sv $(Q)/traffic_classifier.sv $(Q)/credit_based_shaper.sv \
       $(Q)/traffic_shaping_core.sv $(Q)/traffic_queues.sv $(Q)/traffic_controller_802_1q.sv \
       $(P)/timestamp_counter.sv $(P)/ptp_csr_sync.sv \
       $(C)/cdc_pulse.sv $(C)/cdc_handshake.sv $(C)/axis_mux_rr_2in_1out.sv \
       $(P)/ptp_ts_core.sv $(P)/ptp_ts_top.sv $(P)/KL_ptp_clock_validity.sv \
       $(RTL_DIR)/ieee8021q/filtering/tcam.sv $(RTL_DIR)/ieee8021q/filtering/rx_mac_filter.sv \
       $(C)/tx_ifg_gasket.sv $(RTL_DIR)/ieee1722/aaf/KL_pcm_lpf.sv \
       $(C)/KL_link_guard.sv \
       $(RTL_DIR)/ieee17221/adp/adp_advertiser.sv $(RTL_DIR)/ieee17221/adp/adp_tx_arbiter.sv \
       $(RTL_DIR)/ieee17221/aecp/aecp_pkg.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_packet_validator.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_common_parser.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_l0_state.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_timers.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_accessor.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_aem_store.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_aem_dyn_mux.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_response_builder.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_aecp_ingress.sv $(RTL_DIR)/ieee17221/aecp/KL_aecp_top.sv \
       $(RTL_DIR)/ieee17221/acmp/acmp_pkg.sv \
       $(RTL_DIR)/ieee17221/acmp/KL_acmp_tlkr_ctx.sv $(RTL_DIR)/ieee17221/acmp/KL_acmp_responder.sv \
       $(RTL_DIR)/ieee17221/acmp/KL_acmp_lstn_ctx.sv $(RTL_DIR)/ieee17221/acmp/KL_acmp_listener.sv \
       $(RTL_DIR)/ieee8021q/srp/lwsrp_pkg.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_timers.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_tx.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ingress.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_walker.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_registrar.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ta_registrar.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ctx.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ctx_tx.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_rx.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_bw_gate.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_top.sv \
       $(RTL_DIR)/ieee1722/aaf/aaf_talker_i2s.sv $(RTL_DIR)/ieee1722/aaf/KL_aaf_rx_depacketizer.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_i2s_playback.sv $(RTL_DIR)/ieee1722/aaf/KL_i2s_feed_mux.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_tone_gen.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_latency_taps.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_media_adv.sv $(C)/cdc_pair_fifo.sv \
       $(RTL_DIR)/ieee1722/avtp/avtp_subtype_pkg.sv $(RTL_DIR)/ieee1722/avtp/avtp_stream_parser.sv \
       $(RTL_DIR)/ieee1722/avtp/KL_stream_table.sv \
       $(RTL_DIR)/ieee1722/avtp/KL_avtp_rx_monitor.sv \
       $(RTL_DIR)/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_pcm_route.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_capture_i2s.sv $(RTL_DIR)/ieee1722/aaf/KL_tdm_capture.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_tdm_render.sv $(RTL_DIR)/ieee1722/aaf/KL_chan_map_render.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_chan_map_capture.sv $(RTL_DIR)/ieee1722/aaf/KL_aaf_packetizer.sv \
       $(RTL_DIR)/ieee1722/crf/KL_crf_rx.sv $(RTL_DIR)/ieee1722/crf/KL_crf_tx.sv \
       $(RTL_DIR)/ieee1722/crf/KL_mmcm_drp_servo.sv $(RTL_DIR)/ieee1722/maap/KL_maap.sv \
       $(RTL_DIR)/common/eth_event_counter/ethernet_events.sv \
       $(RTL_DIR)/common/eth_event_counter/event_counter.sv \
       $(RTL_DIR)/common/csr/milan_csr.sv \
       $(RTL_DIR)/milan/milan_datapath.sv

.PHONY: all run build clean banner

all: run

banner:
	@echo "======================================================================"
	@echo " tb/verilator/hostplane - host-plane lanes in the SILICON SHAPE"
	@echo "======================================================================"

# Entity definition per shape. hdl/common/csr/gen/ + hdl/ieee17221/aecp/gen/
# hold whichever config was last written with --write-rtl, so every leg must
# name the shape it is actually elaborating or it inherits a foreign one.
CFG_DIR    = ../../../configs/generated
SHAPE_1x1  = +incdir+$(CFG_DIR)/endstation_arty_current
SHAPE_4x4  = +incdir+$(CFG_DIR)/endstation_arty_4x4
SHAPE_8x8  = +incdir+$(CFG_DIR)/endstation_ax7101_8x8

build:
	$(VERILATOR) $(SHAPE_8x8) $(VFLAGS_COMMON) --Mdir obj_ax8x8 $(G_AX8X8) \
		-CFLAGS "-DNSTREAMS_TB=8 -DMILAN_CLK_TB=100000000" \
		$(SRCS) sim_hostplane.cpp -o Vhostplane_ax8x8
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS_COMMON) --Mdir obj_small $(G_SMALL) \
		-CFLAGS "-DNSTREAMS_TB=1 -DMILAN_CLK_TB=50000000 -DSHAPE_NAME=\\\"small-1x-50MHz\\\"" \
		$(SRCS) sim_smoke.cpp -o Vhostplane_smoke_small
	$(VERILATOR) $(SHAPE_4x4) $(VFLAGS_COMMON) --Mdir obj_n4 $(G_N4) \
		-CFLAGS "-DNSTREAMS_TB=4 -DMILAN_CLK_TB=100000000 -DSHAPE_NAME=\\\"mid-4x-100MHz\\\"" \
		$(SRCS) sim_smoke.cpp -o Vhostplane_smoke_n4
	$(VERILATOR) $(SHAPE_8x8) $(VFLAGS_COMMON) --Mdir obj_tdm8 $(G_TDM8) \
		-CFLAGS "-DNSTREAMS_TB=8 -DMILAN_CLK_TB=100000000 -DTDM_SHAPE_TB=1 -DSHAPE_NAME=\\\"tdm8-8x-100MHz\\\"" \
		$(SRCS) sim_smoke.cpp -o Vhostplane_smoke_tdm8

# run every shape even when one fails (a red shape must not hide the others);
# the aggregate exit code stays honest.
run: banner build
	@rc=0; \
	./obj_ax8x8/Vhostplane_ax8x8        || rc=1; \
	./obj_small/Vhostplane_smoke_small  || rc=1; \
	./obj_n4/Vhostplane_smoke_n4        || rc=1; \
	./obj_tdm8/Vhostplane_smoke_tdm8    || rc=1; \
	exit $$rc

clean:
	rm -rf obj_ax8x8 obj_small obj_n4 obj_tdm8
