# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of ptp_csr_sync.sv (CSR<->PHC clock-domain crossing).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# Plain-FF synchronisers (no XPM), so no Xilinx tools are needed. Both clocks are
# driven together — this is a functional check of the pulse/payload alignment and
# the snapshot return path, not an async-metastability check.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = ptp_csr_sync

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ptp_timestamp/ptp_csr_sync.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vptp_sync_sim
	@echo "======================================================================"
	./obj_dir/Vptp_sync_sim

clean:
	rm -rf obj_dir
