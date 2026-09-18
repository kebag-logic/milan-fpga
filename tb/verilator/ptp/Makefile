# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of timestamp_counter.sv (PTP hardware clock).
#   make        - build and run both self-checking harnesses
#   make clean  - remove build artifacts
#
# timestamp_counter is single-clock pure RTL (the CSR->PHC CDC lives in
# ptp_csr_sync / ptp_ts_top), so no Xilinx tools are needed.
#
# TWO SHAPES, because the PPS output (#260) is parameter-gated and the two arms
# make DIFFERENT claims that one binary cannot hold at once:
#
#   obj_dir  PPS_P=0 - the shipping default. The PHC scenarios, plus the proof
#                      that the option-off pin is a STRUCTURAL zero: it stays
#                      low while the PPS inputs are driven hard.
#   obj_pps  PPS_P=1 - the alarm itself: the edge lands within one counter
#                      increment of the boundary and the grid is an exact
#                      1e9 ns over twelve pulses, with the addend negative
#                      control beside it.
#
# The PPS build's pulse width is shortened to 1000 clock cycles so the stretcher can be
# measured exactly without dominating the run; pps_main.cpp carries the same
# number, so the two drifting apart reddens the width check rather than being
# absorbed.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = timestamp_counter
PPS_WIDTH_CYC ?= 1000

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

SRCS = $(RTL_DIR)/ieee8021as/ptp_timestamp/timestamp_counter.sv
CPP  = sim_main.cpp
PPS_CPP = pps_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) --Mdir obj_dir $(SRCS) $(CPP) -o Vptp_sim
	$(VERILATOR) $(VFLAGS) --Mdir obj_pps -GPPS_P=1 \
	    -GPPS_WIDTH_CYC_P=$(PPS_WIDTH_CYC) $(SRCS) $(PPS_CPP) -o Vpps_sim
	@echo "======================================================================"
	./obj_dir/Vptp_sim
	@echo "======================================================================"
	./obj_pps/Vpps_sim

clean:
	rm -rf obj_dir obj_pps
