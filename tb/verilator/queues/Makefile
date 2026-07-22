# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of traffic_queues.sv after the axis_switch IP +
# xpm_fifo_axis -> Forencich axis_demux/axis_fifo/axis_arb_mux swap (Track 1.3).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = queues_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/ieee8021q/ts \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR \
         -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/common/axi_stream_if.sv \
       $(AXIS_DIR)/axis_fifo.v \
       $(AXIS_DIR)/axis_demux.v \
       $(AXIS_DIR)/axis_arb_mux.v \
       $(AXIS_DIR)/arbiter.v \
       $(AXIS_DIR)/priority_encoder.v \
       $(RTL_DIR)/ieee8021q/ts/traffic_queues.sv \
       queues_wrap.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vqueues_sim
	@echo "======================================================================"
	./obj_dir/Vqueues_sim

clean:
	rm -rf obj_dir
