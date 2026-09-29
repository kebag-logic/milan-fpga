# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_media_nco.sv - the steerable media sample grid.
#
#   make        - build and run the self-checking harness
#   make build  - build it alone
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

# NCO_SRC and MDIR are overridable so tb/verilator/capture_coherence's
# mutation arm builds a MUTATED COPY of the grid through this exact recipe,
# into its own directory.
NCO_SRC ?= $(RTL_DIR)/ieee1722/crf/KL_media_nco.sv
MDIR    ?= obj_dir
SRCS = media_nco_wrap.sv $(NCO_SRC)
CPP  = sim_main.cpp

.PHONY: all build run clean
all: run

build:
	$(VERILATOR) $(VFLAGS) --Mdir $(MDIR) $(SRCS) $(CPP) -o Vmedia_nco_sim

run: build
	@echo "======================================================================"
	$(abspath $(MDIR))/Vmedia_nco_sim

clean:
	rm -rf obj_dir
