# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_link_guard (L1/L2 link-bounce supervisor) module harness.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_link_guard

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2" \
         -GDEAD_CYC_C=64 -GSETTLE_CYC_C=256

SRCS = $(RTL_DIR)/common/KL_link_guard.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vlink_guard_sim
	./obj_dir/Vlink_guard_sim

clean:
	rm -rf obj_dir
