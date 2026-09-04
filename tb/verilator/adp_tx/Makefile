# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of adp_tx_arbiter.sv (2-input AXIS packet arbiter that
# merges the ADP stream into the MAC TX). Pure RTL, no Xilinx tools needed.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = adp_tx_arbiter

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

SRCS = $(RTL_DIR)/ieee17221/adp/adp_tx_arbiter.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vadp_tx_sim
	@echo "======================================================================"
	./obj_dir/Vadp_tx_sim
	$(VERILATOR) $(VFLAGS) -GTO_LOG2_P=7 -Mdir obj_super \
	    $(SRCS) sim_super.cpp -o Vadp_tx_super
	@echo "======================================================================"
	./obj_super/Vadp_tx_super

clean:
	rm -rf obj_dir obj_super
