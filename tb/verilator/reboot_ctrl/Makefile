# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_reboot_ctrl module harness (issue #787): the end-station reset on the
# protocol processor's AECP REBOOT request.
#   make          - build and run both legs, then every planted mutant
#   make run      - the default leg alone
#   make run-1g   - the leg at a 1 Gb/s MAC statement alone
#   make mutants  - the planted mutants alone (mutants.py)
#   make clean    - remove build artifacts
#
# The module keeps its SHIPPING waits; the harness compresses the millisecond
# by driving ms_tick_i itself. No -Wno-*: warnings are fatal.
#
# TWO MAC STATEMENTS, each with the egress bound it derives written here as
# an independent literal (the harness refuses to build without one):
#   default  the module's own default, 32,768 octets at 10 Mb/s: 262,144
#            bits at 10,000 bits per millisecond is 27 ms rounded up, plus
#            the quiet millisecond, 28 ms. Every scenario runs here.
#   1g       11,656 octets at 1,000 Mb/s (the AX7101 MilanMAC's statement
#            when this leg was written): 93,248 bits at 1,000,000 bits per
#            millisecond is 1 ms rounded up, plus the quiet millisecond,
#            2 ms. Only the bounds run here (--egress-only).

VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR    = ../../../hdl
TOP        = KL_reboot_ctrl

# CTRL_SRC and MDIR are overridable so mutants.py builds a mutated copy of the
# module through this exact recipe, into its own directory.
CTRL_SRC ?= $(RTL_DIR)/milan/KL_reboot_ctrl.sv
MDIR     ?= obj_dir
EGRESS_MS ?= 28
LEG_G    ?=
LEG_ARGS ?=

VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) \
         --top-module $(TOP) -Wall \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DEGRESS_MS=$(EGRESS_MS)"

CPP = sim_main.cpp

.PHONY: all build run run-1g mutants clean
all: run run-1g mutants

build:
	$(VERILATOR) $(VFLAGS) $(LEG_G) --Mdir $(MDIR) $(CTRL_SRC) $(CPP) -o Vreboot_ctrl_sim

run: build
	$(abspath $(MDIR))/Vreboot_ctrl_sim $(LEG_ARGS)

run-1g:
	$(MAKE) --no-print-directory run MDIR=obj_1g EGRESS_MS=2 LEG_ARGS=--egress-only \
	  LEG_G="-GMAC_TX_OCTETS_P=11656 -GMAC_MIN_MBPS_P=1000"

mutants:
	python3 mutants.py

clean:
	rm -rf obj_dir obj_1g obj_mut_*
