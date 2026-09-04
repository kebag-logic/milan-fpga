# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_media_nco.sv - the steerable media sample grid.
#
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# Requires: verilator (>= 5.0), a C++17 compiler. No Xilinx tools needed.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = media_nco_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         +incdir+$(RTL_DIR)/common \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = media_nco_wrap.sv $(RTL_DIR)/ieee1722/crf/KL_media_nco.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vmedia_nco_sim
	@echo "======================================================================"
	./obj_dir/Vmedia_nco_sim

clean:
	rm -rf obj_dir
