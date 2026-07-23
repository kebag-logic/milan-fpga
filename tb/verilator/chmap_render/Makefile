# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_chan_map_render verification: 64 stream-channel -> physical render
# crossbar. Drives a depacketizer-clone AXIS with recognizable per-sample
# ramps (stream/ch/seq encoded in the 24-bit payload), programs identity /
# permuted / cross-stream / unmapped maps, and asserts byte-exact routing on
# the phys outputs at each 48 kHz tick (map + cur_r frozen between ticks).
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_chan_map_render
VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -CFLAGS "-std=c++17 -O2"
SRCS = $(RTL_DIR)/ieee1722/aaf/KL_chan_map_render.sv
.PHONY: all run clean
all: run
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o VKL_chan_map_render_sim
	./obj_dir/VKL_chan_map_render_sim
clean:
	rm -rf obj_dir
