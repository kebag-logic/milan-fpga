# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of rx_mac_filter.sv (TCAM-driven RX dest-MAC filter).
# Pure RTL (tcam.sv), no Xilinx tools needed.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = rx_mac_filter

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/common/tcam.sv $(RTL_DIR)/common/rx_mac_filter.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vrx_filter_sim
	@echo "======================================================================"
	./obj_dir/Vrx_filter_sim

clean:
	rm -rf obj_dir
