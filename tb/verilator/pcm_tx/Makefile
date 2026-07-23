# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_pcm_tx (host PCM ring -> AAF pair-stream source) module harness.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# Shrunk config so full playback episodes run in microseconds of sim time:
#   N_STREAMS_P=2  CHANS_P=4 (2 channel-pairs/stream) => 4 pair slots
#   SAMPLE_DIV_C=32  (fast media tick; the walk finishes well inside it)

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_pcm_tx

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2" \
         -GN_STREAMS_P=2 -GCHANS_P=4 -GSAMPLE_DIV_C=32 -GUSE_EXT_TICK_P=0

SRCS = $(RTL_DIR)/ieee1722/aaf/KL_pcm_tx.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpcm_tx_sim
	./obj_dir/Vpcm_tx_sim

clean:
	rm -rf obj_dir
