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
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

SRCS = $(RTL_DIR)/ieee8021as/ptp_timestamp/ptp_csr_sync.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

# TWO SHAPES, for the PPS alarm crossing (#260). The PPS ports are on the
# boundary in both, so one harness serves both and the expectations are
# parameterised on the flag rather than copied:
#
#   obj_dir  PPS_P=0 - the shipping default. The command/snapshot scenarios,
#                      plus the proof that the PARKED arm is a structural
#                      zero while the CSR-side PPS inputs are driven hard.
#   obj_pps  PPS_P=1 - the crossing itself: the enable reaches ts_clk, the arm
#                      lands as exactly one pulse with its 64-bit target
#                      already captured, and the live target publishes back
#                      to aclk on the free-running beat.
run:
	$(VERILATOR) $(VFLAGS) --Mdir obj_dir $(SRCS) $(CPP) -o Vptp_sync_sim
	$(VERILATOR) $(VFLAGS) --Mdir obj_pps -GPPS_P=1 \
	    -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DPTP_SYNC_PPS_P=1" \
	    $(SRCS) $(CPP) -o Vptp_sync_pps_sim
	@echo "======================================================================"
	./obj_dir/Vptp_sync_sim
	@echo "======================================================================"
	./obj_pps/Vptp_sync_pps_sim

clean:
	rm -rf obj_dir obj_pps
