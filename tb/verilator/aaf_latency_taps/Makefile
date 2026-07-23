# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_aaf_latency_taps (per-stage AAF pipeline latency taps, item-11) harness.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_aaf_latency_taps

# TIMEOUT_C shrunk to 64 cycles so the token-abort leg runs in microseconds.
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2" \
         -GTIMEOUT_C=64

SRCS = $(RTL_DIR)/ieee1722/aaf/KL_aaf_latency_taps.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vaaf_latency_taps_sim
	./obj_dir/Vaaf_latency_taps_sim

clean:
	rm -rf obj_dir
