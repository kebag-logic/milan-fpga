# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_media_grid_align.sv closed over the REAL
# KL_media_nco - the #74 grid-alignment loop, physical grid modelled in C++.
#
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# Requires: verilator (>= 5.0), a C++17 compiler. No Xilinx tools needed.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = media_grid_align_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         +incdir+$(RTL_DIR)/common \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR)"

SRCS = media_grid_align_wrap.sv \
       $(RTL_DIR)/ieee1722/crf/KL_media_grid_align.sv \
       $(RTL_DIR)/ieee1722/crf/KL_media_nco.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vmedia_grid_align_sim
	$(VERILATOR) $(VFLAGS) --Mdir obj_mut_usign +define+MGA_MUT_U_SIGN \
	  $(SRCS) $(CPP) -o Vmedia_grid_align_sim
	@echo "======================================================================"
	./obj_dir/Vmedia_grid_align_sim
	@echo "---- negative control: the inverted-sign build MUST fail -------------"
	@if ./obj_mut_usign/Vmedia_grid_align_sim > obj_mut_usign/mut.log 2>&1; then \
	  echo "SELF-TEST FAILED: MGA_MUT_U_SIGN PASSED. The sign checks are vacuous."; \
	  exit 1; \
	else \
	  echo "negative control MGA_MUT_U_SIGN: RED as required -- $$(grep -m1 'FAIL' obj_mut_usign/mut.log)"; \
	fi

clean:
	rm -rf obj_dir obj_mut_usign
