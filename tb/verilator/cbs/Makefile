# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of credit_based_shaper.sv (802.1Qav CBS).
#
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# Requires: verilator (>= 5.0), a C++17 compiler. No Xilinx tools needed:
# credit_based_shaper.sv is pure RTL (no XPM/DSP primitives are instantiated).

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = cbs_ver_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/ieee8021q/ts \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR)"

SRCS = cbs_ver_wrap.sv $(RTL_DIR)/ieee8021q/ts/credit_based_shaper.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vcbs_sim
	@echo "======================================================================"
	./obj_dir/Vcbs_sim

clean:
	rm -rf obj_dir
