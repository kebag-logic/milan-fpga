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

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/csr +incdir+$(RTL_DIR)/eth_event_counter \
         +incdir+$(RTL_DIR)/adp +incdir+$(RTL_DIR)/802_1q_traffic_shaper \
         +incdir+$(RTL_DIR)/ptp_timestamp +incdir+$(AXIS_DIR) \
         +incdir+$(RTL_DIR)/aecp +incdir+$(RTL_DIR)/aecp/gen \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR \
         -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE -Wno-PINMISSING -Wno-SELRANGE \
         -Wno-TIMESCALEMOD \
         -CFLAGS "-std=c++17 -O2"

C  = $(RTL_DIR)/common
Q  = $(RTL_DIR)/802_1q_traffic_shaper
P  = $(RTL_DIR)/ptp_timestamp

SRCS = $(C)/ethernet_packet_pkg.sv $(C)/axi_stream_if.sv $(RTL_DIR)/adp/adp_pkg.sv \
       $(AXIS_DIR)/axis_fifo.v $(AXIS_DIR)/axis_demux.v $(AXIS_DIR)/axis_arb_mux.v \
       $(AXIS_DIR)/arbiter.v $(AXIS_DIR)/priority_encoder.v \
       $(Q)/traffic_class_map.sv $(Q)/traffic_classifier.sv $(Q)/credit_based_shaper.sv \
       $(Q)/traffic_shaping_core.sv $(Q)/traffic_queues.sv $(Q)/traffic_controller_802_1q.sv \
       $(P)/timestamp_counter.sv $(P)/ptp_csr_sync.sv \
       $(C)/cdc_pulse.sv $(C)/cdc_handshake.sv $(C)/axis_mux_rr_2in_1out.sv \
       $(P)/ptp_ts_core.sv $(P)/ptp_ts_top.sv \
       $(C)/tcam.sv $(C)/rx_mac_filter.sv $(C)/tx_ifg_gasket.sv $(RTL_DIR)/avtp/KL_pcm_lpf.sv \
       $(RTL_DIR)/adp/adp_advertiser.sv $(RTL_DIR)/adp/adp_tx_arbiter.sv \
       $(RTL_DIR)/aecp/aecp_pkg.sv \
       $(RTL_DIR)/aecp/KL_aecp_packet_validator.sv $(RTL_DIR)/aecp/KL_aecp_common_parser.sv \
       $(RTL_DIR)/aecp/KL_aecp_l0_state.sv $(RTL_DIR)/aecp/KL_aecp_timers.sv \
       $(RTL_DIR)/aecp/KL_aecp_accessor.sv $(RTL_DIR)/aecp/KL_aecp_aem_store.sv \
       $(RTL_DIR)/aecp/KL_aecp_aem_dyn_mux.sv $(RTL_DIR)/aecp/KL_aecp_response_builder.sv \
       $(RTL_DIR)/aecp/KL_aecp_ingress.sv $(RTL_DIR)/aecp/KL_aecp_top.sv \
       $(RTL_DIR)/acmp/acmp_pkg.sv $(RTL_DIR)/acmp/KL_acmp_responder.sv $(RTL_DIR)/acmp/KL_acmp_listener.sv \
       $(RTL_DIR)/lwsrp/lwsrp_pkg.sv $(RTL_DIR)/lwsrp/KL_lwsrp_timers.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_tx.sv $(RTL_DIR)/lwsrp/KL_lwsrp_ingress.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_walker.sv $(RTL_DIR)/lwsrp/KL_lwsrp_registrar.sv $(RTL_DIR)/lwsrp/KL_lwsrp_ta_registrar.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_rx.sv $(RTL_DIR)/lwsrp/KL_lwsrp_bw_gate.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_top.sv \
       $(RTL_DIR)/avtp/aaf_talker_i2s.sv \
       $(RTL_DIR)/avtp/KL_aaf_rx_depacketizer.sv \
       $(RTL_DIR)/1722/avtp_subtype_pkg.sv \
       $(RTL_DIR)/1722/avtp_stream_parser.sv \
       $(RTL_DIR)/1722/KL_avtp_rx_monitor.sv \
	$(RTL_DIR)/1722/KL_crf_rx.sv \
       $(RTL_DIR)/maap/KL_maap.sv \
       $(RTL_DIR)/avtp/KL_i2s_playback.sv \
       $(RTL_DIR)/avtp/KL_tone_gen.sv \
       $(RTL_DIR)/avtp/KL_media_adv.sv \
       $(RTL_DIR)/common/cdc_pair_fifo.sv \
       $(RTL_DIR)/eth_event_counter/ethernet_events.sv \
       $(RTL_DIR)/csr/milan_csr.sv \
       $(C)/milan_datapath.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vmilan_dp_sim
	@echo "======================================================================"
	./obj_dir/Vmilan_dp_sim

clean:
	rm -rf obj_dir
