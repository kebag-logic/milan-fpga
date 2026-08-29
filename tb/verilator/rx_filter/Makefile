# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of rx_mac_filter.sv (TCAM-driven RX dest-MAC filter).
# Pure RTL (tcam.sv), no Xilinx tools needed.
#   make        - run the clean harness, then prove a missing, swapped, tied-off
#                 and direction-wrong binding of the real TCAM seam is rejected
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = rx_mac_filter

# -Werror-PINMISSING / -Werror-UNDRIVEN: a missing binding or a port with the
# wrong direction is refused BY NAME even under -Wno-fatal. Verilator inlines
# the child, so no harness check can see a direction error; these two are what
# let binding_mutant.py tell "direction-wrong" from "did not compile".
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -Werror-PINMISSING -Werror-UNDRIVEN \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee8021q/filtering/tcam.sv $(RTL_DIR)/ieee8021q/filtering/rx_mac_filter.sv
CPP  = sim_main.cpp

.PHONY: all run binding-negative print-vflags clean
all: binding-negative

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vrx_filter_sim
	@echo "======================================================================"
	./obj_dir/Vrx_filter_sim

# Rule 5: the TCAM lookup key is a real production seam, not an internal
# observation backdoor. binding_mutant.py applies one mutation at a time -
# missing, swapped, tied-off, direction-wrong - to a COPY of the RTL, builds it
# with the recipe below and requires the named refusal or the SAME harness's
# own FAIL. The run prerequisite is the positive control: the unmodified
# boundary must pass before a deliberate misbinding is meaningful.
binding-negative: run
	@echo "======================================================================"
	python3 binding_mutant.py

# Rule 3: the seam arms build with THIS recipe, read through this target, never
# a copy of it. One word per line so the shell's quoting of -CFLAGS survives.
print-vflags:
	@printf '%s\n' $(VERILATOR) $(VFLAGS)

clean:
	rm -rf obj_dir
