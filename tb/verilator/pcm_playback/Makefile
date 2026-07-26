# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# End-to-end item-7 PLAYBACK harness: host PCM ring -> KL_pcm_tx ->
# KL_chan_map_render (playback source) -> KL_i2s_feed_mux -> KL_i2s_playback
# -> the DAC pin, decoded back with a spec-derived I2S receiver and compared
# BIT-EXACTLY against the ring words that were written. The playback mirror
# of the proven record path.
#
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# Sim-shrunk shape: N_STREAMS_P=2 (stereo each), TICK_DIV_P=1024 so the
# 50 MHz datapath grid (50e6/1024) and the 25 MHz audio domain's frame rate
# (25e6/512) are the SAME 48828.125 Hz - a rate mismatch can never be
# confused with a data error.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
C          = $(RTL_DIR)/common
F          = $(RTL_DIR)/ieee1722/aaf
TOP        = pcm_playback_wrap

VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         +incdir+$(C) +incdir+$(F) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -Wno-PINCONNECTEMPTY -Wno-CASEINCOMPLETE \
         -CFLAGS "-std=c++17 -O2" \
         -GN_STREAMS_P=2 -GTICK_DIV_P=1024 -GN_PHYS_P=10 \
         -GCLK_FREQ_HZ_P=50000000 -GPREFILL_P=4

SRCS = $(C)/cdc_pair_fifo.sv $(C)/cdc_pulse.sv \
       $(F)/KL_pcm_tx.sv $(F)/KL_chan_map_render.sv \
       $(F)/KL_i2s_feed_mux.sv $(F)/KL_i2s_playback.sv \
       pcm_playback_wrap.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpcm_playback_sim
	./obj_dir/Vpcm_playback_sim

clean:
	rm -rf obj_dir
