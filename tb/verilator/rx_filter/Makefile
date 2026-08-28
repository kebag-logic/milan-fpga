# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of rx_mac_filter.sv (TCAM-driven RX dest-MAC filter).
# Pure RTL (tcam.sv), no Xilinx tools needed.
#   make        - run the clean harness and prove a tied-off real binding fails
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = rx_mac_filter

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee8021q/filtering/tcam.sv $(RTL_DIR)/ieee8021q/filtering/rx_mac_filter.sv
CPP  = sim_main.cpp

.PHONY: all run binding-negative clean
all: binding-negative

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vrx_filter_sim
	@echo "======================================================================"
	./obj_dir/Vrx_filter_sim

# Rule 5: the TCAM lookup key is a real production seam, not an internal
# observation backdoor. Tie that named binding low and require the SAME harness
# to reject the result. The run prerequisite is the positive control: the
# unmodified boundary must pass before the deliberate misbinding is meaningful.
binding-negative: run
	@echo "======================================================================"
	python3 binding_mutant.py

clean:
	rm -rf obj_dir
