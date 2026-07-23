# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_lat_history_ring verification: per-stage AAF latency samples -> fixed
# 16-byte records -> wrapping DRAM ring. The TB plays the DRAM writer: it
# captures every (addr,data,last) write beat, reconstructs each record, and
# checks field byte-exactness, ring wrap, wptr advance, drop-on-full + the
# dropped counter, the gap marker, and timestamp monotonicity.
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
A          = $(RTL_DIR)/ieee1722/aaf
TOP        = KL_lat_history_ring
VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         +incdir+$(A) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -CFLAGS "-std=c++17 -O2"
SRCS = $(A)/KL_lat_history_ring.sv
.PHONY: all run clean
all: run
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o VKL_lat_history_ring_sim
	./obj_dir/VKL_lat_history_ring_sim
clean:
	rm -rf obj_dir
