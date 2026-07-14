# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_lwsrp_tx.sv (lwSRP applicant transmit engine:
# byte-exact MSRP Domain/TalkerAdvertise + MVRP VID MRPDUs, NEW/JOININ/LV
# lifecycle, LeaveAll turn). Pure RTL, no Xilinx tools needed.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_lwsrp_tx

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/lwsrp/lwsrp_pkg.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_tx.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vlwsrp_tx_sim
	@echo "======================================================================"
	./obj_dir/Vlwsrp_tx_sim

clean:
	rm -rf obj_dir
