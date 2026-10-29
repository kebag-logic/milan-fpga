# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_reboot_ctrl module harness (issue #787): the end-station reset on the
# protocol processor's AECP REBOOT request.
#   make          - build and run the harness, then every planted mutant
#   make run      - the harness alone
#   make mutants  - the planted mutants alone (mutants.py)
#   make clean    - remove build artifacts
#
# The module keeps its SHIPPING waits; the harness compresses the millisecond
# by driving ms_tick_i itself. No -Wno-*: warnings are fatal.

VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR    = ../../../hdl
TOP        = KL_reboot_ctrl

# CTRL_SRC and MDIR are overridable so mutants.py builds a mutated copy of the
# module through this exact recipe, into its own directory.
CTRL_SRC ?= $(RTL_DIR)/milan/KL_reboot_ctrl.sv
MDIR     ?= obj_dir

VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) \
         --top-module $(TOP) -Wall \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

CPP = sim_main.cpp

.PHONY: all build run mutants clean
all: run mutants

build:
	$(VERILATOR) $(VFLAGS) --Mdir $(MDIR) $(CTRL_SRC) $(CPP) -o Vreboot_ctrl_sim

run: build
	$(abspath $(MDIR))/Vreboot_ctrl_sim

mutants:
	python3 mutants.py

clean:
	rm -rf obj_dir obj_mut_*
