# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_lwsrp_rx.sv (lwSRP receive chain: monitor tap
# -> packet FIFO -> streaming MRPDU walker -> registrar) against hand-built
# bridge-side MRPDUs (multi-value +k vectors, LeaveAll storms, leave-timer
# expiry, domain boundary, TalkerFailed capture). Needs third_party/verilog-axis.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = KL_lwsrp_rx

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/lwsrp/lwsrp_pkg.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_ingress.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_walker.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_registrar.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_rx.sv \
       $(AXIS_DIR)/axis_fifo.v
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vlwsrp_rx_sim
	@echo "======================================================================"
	./obj_dir/Vlwsrp_rx_sim

clean:
	rm -rf obj_dir
