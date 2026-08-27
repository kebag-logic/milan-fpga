# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of tcam.sv (register-based ternary CAM MAC table).
# Pure RTL, no Xilinx/vendor primitives -> no Xilinx tools needed.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = tcam

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee8021q/filtering/tcam.sv
CPP  = sim_main.cpp

.PHONY: all run mutants clean
.DEFAULT_GOAL := all
all: run mutants

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vtcam_sim
	@echo "======================================================================"
	./obj_dir/Vtcam_sim

# Rule 8: prove the harness above is load-bearing. Three defects are injected
# into the real RTL, one at a time, and each must make the SAME harness fail;
# the unmutated build must still pass. Mutants are built in a temporary
# directory, so nothing is written into the tree.
mutants:
	@echo "======================================================================"
	python3 mutants.py

clean:
	rm -rf obj_dir
