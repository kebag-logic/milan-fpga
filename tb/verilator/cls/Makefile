# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of traffic_class_map.sv (802.1Q PCP->queue mapping).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# traffic_class_map is pure combinational RTL (no XPM/FIFO), so no Xilinx tools
# are needed. The surrounding traffic_classifier's FIFO/parsing is out of scope
# here; this harness targets the standards-relevant classification decode.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = traffic_class_map

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/ieee8021q/ts \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee8021q/ts/traffic_class_map.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vcls_sim
	@echo "======================================================================"
	./obj_dir/Vcls_sim

clean:
	rm -rf obj_dir
