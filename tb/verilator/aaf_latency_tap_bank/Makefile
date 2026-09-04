# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_aaf_latency_tap_bank (LTAP observation-point adapter) harness.
#   make        - build and run the self-checking harness, then the prune arm
#   make clean  - remove build artifacts
#
# Two builds, because pruning is a PARAMETER and the structural zero it
# presents is the thing a reader must not mistake for a measurement:
#   ENABLE_P=1  the measuring build, graded by sim_main.cpp
#   ENABLE_P=0  the pruned build, graded by sim_prune.cpp - every LTAP word
#               and the status rail must read 0 no matter what the
#               observation points do.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_aaf_latency_tap_bank

# TIMEOUT_C shrunk to 64 cycles so the per-stage re-arm guard runs in
# microseconds; the pruned build keeps the same shrink so the two agree.
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
         -GTIMEOUT_C=64

SRCS = $(RTL_DIR)/ieee1722/aaf/KL_aaf_latency_tap_bank.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_latency_taps.sv

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) -GENABLE_P=1 --Mdir obj_dir_en $(SRCS) sim_main.cpp -o Vtap_bank_sim
	./obj_dir_en/Vtap_bank_sim
	$(VERILATOR) $(VFLAGS) -GENABLE_P=0 --Mdir obj_dir_pr $(SRCS) sim_prune.cpp -o Vtap_bank_prune
	./obj_dir_pr/Vtap_bank_prune

clean:
	rm -rf obj_dir_en obj_dir_pr
