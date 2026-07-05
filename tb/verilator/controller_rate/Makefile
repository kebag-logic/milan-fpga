# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# CBS end-to-end reproduction (OPEN bug) — see README.md / docs/CBS_DATAPATH_BUG.md.
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
C          = $(RTL_DIR)/common
Q          = $(RTL_DIR)/802_1q_traffic_shaper
TOP        = controller_rate_wrap
VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         +incdir+$(C) +incdir+$(Q) +incdir+$(AXIS_DIR) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR \
         -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE -Wno-PINMISSING -Wno-TIMESCALEMOD \
         -Wno-VARHIDDEN -CFLAGS "-std=c++17 -O2"
SRCS = $(C)/ethernet_packet_pkg.sv $(C)/axi_stream_if.sv \
       $(AXIS_DIR)/axis_fifo.v $(AXIS_DIR)/axis_demux.v $(AXIS_DIR)/axis_arb_mux.v \
       $(AXIS_DIR)/arbiter.v $(AXIS_DIR)/priority_encoder.v \
       $(Q)/traffic_class_map.sv $(Q)/traffic_classifier.sv $(Q)/credit_based_shaper.sv \
       $(Q)/traffic_shaping_core.sv $(Q)/traffic_queues.sv $(Q)/traffic_controller_802_1q.sv \
       controller_rate_wrap.sv
.PHONY: all run clean
all: run
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o Vcontroller_rate_sim
	./obj_dir/Vcontroller_rate_sim
clean:
	rm -rf obj_dir
