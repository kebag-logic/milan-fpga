# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_crf_rx (Milan CRF Media Clock Input, measurement half) module harness.
# Pins the ts-history-dependent outputs (delta/rate/lock trajectory) against
# an independent C++ ring replica — the regression that guards the
# ts_hist flop-file -> BRAM conversion.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# CLK_FREQ_HZ_P is scaled to 200 kHz so the 100 ms lock timeout is
# 20 000 cycles (drillable in-sim); the ts/rate math is cycle-count-free.
#
# IVAL_CYC: Milan v1.2 Table 5.6 observation interval, shrunk from the
# silicon 1 s (= CLK_FREQ_HZ_P cycles) so counter checks see interval
# commits in sim time. Semantics under test (N events in one interval move
# a counter by 1) are identical at any conformant interval length. ONE
# variable feeds the RTL parameter AND the C++ replica: derive, never
# mirror.
IVAL_CYC ?= 200

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_crf_rx

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -GCLK_FREQ_HZ_P=200000 \
         -GIVAL_CYC_P=$(IVAL_CYC) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -DIVAL_CYC_C=$(IVAL_CYC)u"

SRCS = $(RTL_DIR)/ieee1722/crf/KL_crf_rx.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vcrf_rx_sim
	@echo "======================================================================"
	./obj_dir/Vcrf_rx_sim

clean:
	rm -rf obj_dir
