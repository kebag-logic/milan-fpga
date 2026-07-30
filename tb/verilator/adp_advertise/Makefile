# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of the ADP *advertise state machine* timing contract:
# Milan v1.2 5.6.3 (Table 5.49 states, Table 5.50 events, 5.6.3.5.* transitions)
# and IEEE 1722.1-2021 6.2.4 Figure 6-2 / 6.2.7 Figure 6-5.
#
# Separate from tb/verilator/adp (which locks the ADPDU BYTES) because this
# suite locks the TIMING: the re-announce period, the level arm, the GM_CHANGE
# event and a long run that outlives every internal counter.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# Pure RTL (only adp_pkg.sv), no XPM/Xilinx primitives -> no Xilinx tools needed.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = adp_advertiser

# The delay params are the DUT's TMR_DELAY range in clk cycles; shrink them so a
# 0..4 s wall-time window is a handful of simulated cycles (the integration
# passes MILAN_CLK_FREQ_HZ/5 + a 26-bit mask; see the RTL envelope note).
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -GDISC_DLY_BASE=4 -GDISC_DLY_MASK=3 \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee17221/adp/adp_pkg.sv $(RTL_DIR)/ieee17221/adp/adp_advertiser.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vadp_adv_sim
	@echo "======================================================================"
	./obj_dir/Vadp_adv_sim

clean:
	rm -rf obj_dir
