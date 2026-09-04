# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_pair_blend + KL_pair_zero_fill (HANDOVER 8.3b /
# Milan v1.2 5.3.7.3 - the capture pair blend and the silence filler).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = pair_fill_tb_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

SRCS = $(RTL_DIR)/ieee1722/aaf/KL_pair_blend.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_pair_zero_fill.sv \
       pair_fill_tb_top.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpair_fill_sim
	@echo "======================================================================"
	./obj_dir/Vpair_fill_sim

clean:
	rm -rf obj_dir
