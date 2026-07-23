# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_chan_map_capture lane: the per-pair-slot TX source mux feeding the shared
# KL_aaf_packetizer. Lane A (N=2) checks per-slot routing / remap / disabled-
# slot absence + the map readback; lane B (N=8 all-8ch) exercises the widened
# pair_slot up to slot 31.
VERILATOR ?= verilator
TOP = chmap_wrap
SRCS = ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv \
       ../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv \
       chmap_wrap.sv
all: run
obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module $(TOP) \
	  -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
	  -Wno-PINCONNECTEMPTY -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2" \
	  $(SRCS) sim_main.cpp
run: obj_dir/V$(TOP)
	./obj_dir/V$(TOP)
clean: ; rm -rf obj_dir
.PHONY: all run clean
