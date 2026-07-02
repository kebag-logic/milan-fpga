# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of adp_advertiser.sv (ADP transmit engine).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# Pure RTL (only adp_pkg.sv), no XPM/Xilinx primitives -> no Xilinx tools needed.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = adp_advertiser

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/adp/adp_pkg.sv $(RTL_DIR)/adp/adp_advertiser.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vadp_sim
	@echo "======================================================================"
	./obj_dir/Vadp_sim

clean:
	rm -rf obj_dir
