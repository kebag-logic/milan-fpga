# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Item-4 AES3 / S-PDIF ser/des family: KL_aes3_tx (biphase-mark encoder) ->
# one line -> four KL_aes3_rx receivers (24/20/16-bit words, professional and
# consumer channel-status dialects). Cold acquisition, sample-exact pairs,
# channel-status round-trip, V-bit census, injected biphase violation and
# transmitter underrun - see sim_main.cpp for the check list.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
VERILATOR ?= verilator
TOP  = aes3_wrap
RTL  = ../../../hdl
SRCS = $(RTL)/ieee1722/aaf/KL_aes3_tx.sv \
       $(RTL)/ieee1722/aaf/KL_aes3_rx.sv \
       $(RTL)/common/cdc_pair_fifo.sv $(RTL)/common/cdc_pulse.sv \
       aes3_wrap.sv
all: run
obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module $(TOP) \
	  -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM -Wno-DECLFILENAME \
	  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-PINCONNECTEMPTY \
	  -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
	  $(SRCS) sim_main.cpp
run: obj_dir/V$(TOP)
	./obj_dir/V$(TOP)
clean: ; rm -rf obj_dir
.PHONY: all run clean
