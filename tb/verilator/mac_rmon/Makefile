# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_mac_rmon_events: the block that turns MAC-boundary facts into the
# `ethernet_events` pulse vector (the RMON "decorative ABI" fix - the counters
# were tested, wired and documented while every SoC tied i_mac_events to 0).
#
# Two shapes, because the capability mask is the honesty contract and it MUST
# follow the parameters:
#   full     - a MAC that checks FCS + preamble and flags bad frames
#   nochk    - a MAC that exposes none of that (HAS_*_P = 0): the three
#              optional lanes must go silent AND drop out of cap_o
#
#   make        - build and run both shapes
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL        = ../../../hdl
E          = $(RTL)/common/eth_event_counter
TOP        = KL_mac_rmon_events

VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         +incdir+$(E) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-UNUSEDPARAM -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-EOFNEWLINE \
         -Wno-TIMESCALEMOD \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

SRCS = $(E)/KL_mac_rmon_events.sv $(RTL)/common/cdc_pulse.sv

run: full nochk

full:
	$(VERILATOR) $(VFLAGS) --Mdir obj_full $(SRCS) sim_main.cpp -o Vfull
	./obj_full/Vfull

nochk:
	$(VERILATOR) $(VFLAGS) --Mdir obj_nochk \
	  -GHAS_FCS_CHECK_P=0 -GHAS_ALIGN_CHECK_P=0 -GHAS_RX_ERR_FLAG_P=0 \
	  $(SRCS) sim_main.cpp -o Vnochk
	./obj_nochk/Vnochk --nochk

clean:
	rm -rf obj_full obj_nochk

.PHONY: run full nochk clean
