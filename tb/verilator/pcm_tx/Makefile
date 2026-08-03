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
#
# WIDE leg (task #31): the 8x8x8 SHIP shape - N_STREAMS_P=8, CHANS_P=8 =>
# 32 pair slots. Pins the widened 5-bit pair_slot space (ids 28..31 exist
# un-truncated) and the per-stream hold isolation a 4-bit bus broke.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_pcm_tx

VFLAGS_COMMON = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2"

VFLAGS      = $(VFLAGS_COMMON) \
              -GN_STREAMS_P=2 -GCHANS_P=4 -GSAMPLE_DIV_C=32 -GUSE_EXT_TICK_P=0
VFLAGS_WIDE = $(VFLAGS_COMMON) --Mdir obj_wide \
              -GN_STREAMS_P=8 -GCHANS_P=8 -GSAMPLE_DIV_C=64 -GUSE_EXT_TICK_P=0
# FRAC leg: the SHIPPING ratio 100 MHz / 48 kHz = 2083 + 16000/48000. Every
# other leg uses a whole-number ratio (32, 64), where the remainder is 0 and a
# floored divider is indistinguishable from an exact one - which is how a
# +160 ppm media clock shipped. See sim_frac.cpp.
VFLAGS_FRAC = $(VFLAGS_COMMON) --Mdir obj_frac \
              -GN_STREAMS_P=2 -GCHANS_P=2 -GUSE_EXT_TICK_P=0 \
              -GSAMPLE_DIV_C=2083 -GSAMPLE_REM_P=16000 -GSAMPLE_DEN_P=48000

SRCS = $(RTL_DIR)/ieee1722/aaf/KL_pcm_tx.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpcm_tx_sim
	./obj_dir/Vpcm_tx_sim
	$(VERILATOR) $(VFLAGS_WIDE) $(SRCS) sim_wide.cpp -o Vpcm_tx_wide
	./obj_wide/Vpcm_tx_wide
	$(VERILATOR) $(VFLAGS_FRAC) $(SRCS) sim_frac.cpp -o Vpcm_tx_frac
	./obj_frac/Vpcm_tx_frac

clean:
	rm -rf obj_dir obj_wide obj_frac
