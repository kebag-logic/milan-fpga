# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_tdm_render verification: TDM8 output serializer (item-4 audio front-end,
# OUTPUT side). The TB drives bclk/fsync per the frame geometry, writes known
# slot samples on clk_i, and de-serializes tdm_dout_o with a golden model that
# samples exactly like KL_tdm_capture (rising edge, Philips-heritage delay-1) -
# asserting bit-exact slots, frame alignment, double-buffer latching, pad-zero,
# 24-bit sign preservation, a multi-frame run and stale-frame repeat.
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
C          = $(RTL_DIR)/common
AAF        = $(RTL_DIR)/ieee1722/aaf
TOP        = KL_tdm_render
VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         +incdir+$(C) +incdir+$(AAF) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -CFLAGS "-std=c++17 -O2"
SRCS = $(C)/cdc_pair_fifo.sv $(AAF)/KL_tdm_render.sv
.PHONY: all run clean
all: run
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o VKL_tdm_render_sim
	./obj_dir/VKL_tdm_render_sim
clean:
	rm -rf obj_dir
