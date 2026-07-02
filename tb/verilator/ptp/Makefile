# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of timestamp_counter.sv (PTP hardware clock).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# timestamp_counter is single-clock pure RTL (the CSR->PHC CDC lives in
# ptp_csr_sync / ptp_ts_top), so no Xilinx tools are needed.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = timestamp_counter

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ptp_timestamp/timestamp_counter.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vptp_sim
	@echo "======================================================================"
	./obj_dir/Vptp_sim

clean:
	rm -rf obj_dir
