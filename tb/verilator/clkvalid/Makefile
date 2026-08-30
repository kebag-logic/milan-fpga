# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_ptp_clock_validity harness: the AVTP "tu" verdict. Two shapes.
#   fast  - QTICK_CYC_P = 8, so the holdover and observation intervals both
#           complete in a few hundred cycles; every behavioural
#           check lives here.
#   real  - QTICK_CYC_P = 25_000_000 (the 100 MHz build's real 250 ms tick).
#           Proves the divider arithmetic at the shipping value rather than
#           only at a toy one - a scaled-only TB agrees with a scaling bug.
#
#   make        - build and run both shapes
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_ptp_clock_validity

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) --Mdir obj_fast -GQTICK_CYC_P=8 \
	  $(SRCS) $(CPP) -o Vclkv_fast
	$(VERILATOR) $(VFLAGS) --Mdir obj_real -GQTICK_CYC_P=25000000 \
	  $(SRCS) $(CPP) -o Vclkv_real
	$(VERILATOR) $(VFLAGS) --Mdir obj_fabric -GQTICK_CYC_P=8 \
	  -GFABRIC_GPTP_P=1 $(SRCS) $(CPP) -o Vclkv_fabric
	@echo "======================================================================"
	./obj_fast/Vclkv_fast 8
	@echo "----------------------------------------------------------------------"
	./obj_real/Vclkv_real 25000000
	@echo "----------------------------------------------------------------------"
	./obj_fabric/Vclkv_fabric 8 fabric

clean:
	rm -rf obj_fast obj_real obj_fabric
