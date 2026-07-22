# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of traffic_classifier.sv after the xpm_fifo_axis ->
# axis_fifo (Forencich verilog-axis) swap. The classifier is now pure open RTL,
# so it Verilates end-to-end (it could not with XPM).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = classifier_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/ieee8021q/ts \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR \
         -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/common/ethernet_packet_pkg.sv \
       $(RTL_DIR)/common/axi_stream_if.sv \
       $(AXIS_DIR)/axis_fifo.v \
       $(RTL_DIR)/ieee8021q/ts/traffic_class_map.sv \
       $(RTL_DIR)/ieee8021q/ts/traffic_classifier.sv \
       classifier_wrap.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vclassifier_sim
	@echo "======================================================================"
	./obj_dir/Vclassifier_sim

clean:
	rm -rf obj_dir
