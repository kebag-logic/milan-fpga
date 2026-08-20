# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
GPTP_DIR   = ../../../gptp-processor
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = gptp_shadow_wrap
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -Wno-TIMESCALEMOD -Wno-GENUNNAMED -Wno-PROCASSINIT -Wno-SELRANGE \
         -Wno-PINCONNECTEMPTY \
         -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR)"
SRCS = gptp_shadow_wrap.sv \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/timestamp_counter.sv \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_shadow.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_txstamp.sv \
       $(AXIS_DIR)/axis_fifo.v \
       $(GPTP_DIR)/hdl/ucpu/gptp_ucpu_pkg.sv \
       $(GPTP_DIR)/hdl/ucpu/KL_gptp_ucpu.sv \
       $(GPTP_DIR)/hdl/wire/KL_gptp_rx_parser.sv \
       $(GPTP_DIR)/hdl/wire/KL_gptp_tx_slot.sv \
       $(GPTP_DIR)/hdl/common/KL_gptp_timer.sv \
       $(GPTP_DIR)/hdl/top/KL_gptp_engine.sv
CPP  = sim_main.cpp

run: gptp_ucode.hex
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vgptp_shadow_sim
	./obj_dir/Vgptp_shadow_sim

gptp_ucode.hex: $(GPTP_DIR)/hdl/ucode/gen_gptp_ucode.py
	python3 $< --clk-hz 2000000 --cease-ms 3000 -o $@

clean:
	rm -rf obj_dir gptp_ucode.hex
