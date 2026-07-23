# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_pcm_ring_bram (on-chip BRAM PCM ring) self-checking harness.
#   make        - build and run both configs (N=1 and N=4)
#   make clean  - remove build artifacts
#
# Two builds: N_STREAMS=1 (no-shed / wrap / enable / CPU-read coherency) and
# N_STREAMS=4 (tuser routing). Each passes matching -D macros to the C++ so the
# shadow model computes the same addresses the RTL does.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_pcm_ring_bram

VBASE = --cc --exe --build -j 0 \
        --top-module $(TOP) \
        -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
        -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE

SRCS = $(RTL_DIR)/ieee1722/aaf/KL_pcm_ring_bram.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	# ---- N_STREAMS=1, 32 KB ring ----
	$(VERILATOR) $(VBASE) -GDATA_W=64 -GN_STREAMS=1 -GRING_BYTES=32768 \
	    --Mdir obj_dir_n1 \
	    -CFLAGS "-std=c++17 -O2 -DTB_N_STREAMS=1 -DTB_RING_BYTES=32768" \
	    $(SRCS) $(CPP) -o Vpcm_ring_n1
	./obj_dir_n1/Vpcm_ring_n1
	# ---- N_STREAMS=4, 16 KB ring (4 x 512 words) ----
	$(VERILATOR) $(VBASE) -GDATA_W=64 -GN_STREAMS=4 -GRING_BYTES=16384 \
	    --Mdir obj_dir_n4 \
	    -CFLAGS "-std=c++17 -O2 -DTB_N_STREAMS=4 -DTB_RING_BYTES=16384" \
	    $(SRCS) $(CPP) -o Vpcm_ring_n4
	./obj_dir_n4/Vpcm_ring_n4

clean:
	rm -rf obj_dir_n1 obj_dir_n4
