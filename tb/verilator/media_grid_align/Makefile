# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_media_grid_align.sv closed over the REAL
# KL_media_nco - the #74 grid-alignment loop, physical grid modelled in C++ -
# with the REAL KL_chan_map_capture junction counters on the same grids.
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
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         +incdir+$(RTL_DIR)/common \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I$(CURDIR)"

CAPTURE = $(RTL_DIR)/ieee1722/aaf/KL_chan_map_capture.sv
SRCS = media_grid_align_wrap.sv \
       $(RTL_DIR)/ieee1722/crf/KL_media_grid_align.sv \
       $(RTL_DIR)/ieee1722/crf/KL_media_nco.sv
CPP  = sim_main.cpp

# MGA_MUT_COIN: the junction detector with its coincidence branch reverted to
# the law before #74 item 2 (a coincident tick drops the pending marker). The
# copy is refused if the substitution found nothing to revert.
MUT_COIN_SV = obj_mut_coin/KL_chan_map_capture.sv

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CAPTURE) $(CPP) -o Vmedia_grid_align_sim
	$(VERILATOR) $(VFLAGS) --Mdir obj_mut_usign +define+MGA_MUT_U_SIGN \
	  $(SRCS) $(CAPTURE) $(CPP) -o Vmedia_grid_align_sim
	$(VERILATOR) $(VFLAGS) --Mdir obj_mut_keepoff +define+MGA_MUT_NO_KEEPOFF \
	  $(SRCS) $(CAPTURE) $(CPP) -o Vmedia_grid_align_sim
	mkdir -p obj_mut_coin
	sed "s/tdm_frame_pend_r <= tdm_frame_pend_r;/tdm_frame_pend_r <= 1'b0;/" \
	  $(CAPTURE) > $(MUT_COIN_SV)
	@if cmp -s $(CAPTURE) $(MUT_COIN_SV); then \
	  echo "SELF-TEST FAILED: MGA_MUT_COIN found no coincidence branch to revert."; \
	  exit 1; \
	fi
	$(VERILATOR) $(VFLAGS) --Mdir obj_mut_coin \
	  $(SRCS) $(MUT_COIN_SV) $(CPP) -o Vmedia_grid_align_sim
	@echo "======================================================================"
	./obj_dir/Vmedia_grid_align_sim
	@echo "---- negative control: the inverted-sign build MUST fail -------------"
	@if ./obj_mut_usign/Vmedia_grid_align_sim > obj_mut_usign/mut.log 2>&1; then \
	  echo "SELF-TEST FAILED: MGA_MUT_U_SIGN PASSED. The sign checks are vacuous."; \
	  exit 1; \
	else \
	  echo "negative control MGA_MUT_U_SIGN: RED as required -- $$(grep -m1 'FAIL' obj_mut_usign/mut.log)"; \
	fi
	@echo "---- negative control: no lock-phase keep-off MUST fail [G7] ---------"
	@./obj_mut_keepoff/Vmedia_grid_align_sim > obj_mut_keepoff/mut.log 2>&1; \
	if ! grep -q '\[FAIL\] G7: zero junction' obj_mut_keepoff/mut.log; then \
	  echo "SELF-TEST FAILED: MGA_MUT_NO_KEEPOFF did not fail the [G7] counters."; \
	  exit 1; \
	else \
	  echo "negative control MGA_MUT_NO_KEEPOFF: RED as required -- $$(grep -m1 '\[FAIL\] G7: zero junction' obj_mut_keepoff/mut.log)"; \
	fi
	@echo "---- negative control: the old coincidence law MUST fail [G9] --------"
	@./obj_mut_coin/Vmedia_grid_align_sim > obj_mut_coin/mut.log 2>&1; \
	if ! grep -q '\[FAIL\] G9: ' obj_mut_coin/mut.log; then \
	  echo "SELF-TEST FAILED: MGA_MUT_COIN did not fail the [G9] passage."; \
	  exit 1; \
	else \
	  echo "negative control MGA_MUT_COIN: RED as required -- $$(grep -m1 '\[FAIL\] G9: ' obj_mut_coin/mut.log)"; \
	fi

clean:
	rm -rf obj_dir obj_mut_usign obj_mut_keepoff obj_mut_coin
