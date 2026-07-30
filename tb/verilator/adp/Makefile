# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of adp_advertiser.sv (ADP transmit engine).
#   make        - build and run both self-checking harnesses
#   make clean  - remove build artifacts
#
# Two executables, because the discover-response delay can only be judged
# against IEEE 1722.1-2021 6.2.4.2.2 with a REALISTIC base:mask ratio:
#   sim_main.cpp - behaviour + frame bytes + DIAG lanes + the long-run lock,
#                  with a few-cycle delay so the run stays quick
#   sim_dly.cpp  - delay-envelope conformance: bound = 2*valid_time*BASE cycles
#                  (= 0.4*valid_time s, since BASE is instantiated as
#                  MILAN_CLK_FREQ_HZ/5 = 0.2 s), measured over real draws at
#                  valid_time 1..31. BASE:MASK = 1000:4095 = 4.1x sits inside
#                  the shipped 3.36x (100 MHz) .. 6.71x (50 MHz) band.
#
# Pure RTL (only adp_pkg.sv), no XPM/Xilinx primitives -> no Xilinx tools needed.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = adp_advertiser

VFLAGS_COMMON = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"

VFLAGS     = $(VFLAGS_COMMON) -GDISC_DLY_BASE=4    -GDISC_DLY_MASK=3
VFLAGS_DLY = $(VFLAGS_COMMON) -GDISC_DLY_BASE=1000 -GDISC_DLY_MASK=4095

SRCS = $(RTL_DIR)/ieee17221/adp/adp_pkg.sv $(RTL_DIR)/ieee17221/adp/adp_advertiser.sv
CPP  = sim_main.cpp

.PHONY: all run run_dly clean
all: run run_dly

run:
	$(VERILATOR) $(VFLAGS) --Mdir obj_dir $(SRCS) $(CPP) -o Vadp_sim
	@echo "======================================================================"
	./obj_dir/Vadp_sim

run_dly:
	$(VERILATOR) $(VFLAGS_DLY) --Mdir obj_dir_dly $(SRCS) sim_dly.cpp -o Vadp_dly
	@echo "======================================================================"
	./obj_dir_dly/Vadp_dly

clean:
	rm -rf obj_dir obj_dir_dly
