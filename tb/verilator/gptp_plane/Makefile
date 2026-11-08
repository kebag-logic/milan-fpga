# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
GPTP_DIR   = ../../../gptp-processor
UCODE_GEN  = $(GPTP_DIR)/hdl/ucode/gen_gptp_ucode.py
#: The clockQuality this harness's image announces (#843): the generator's
#: CQ_C, read from the generator the image is built with. The image rule
#: below passes no --clock-accuracy, so CQ_C's octet (0x22 since FPGA-gPTP
#: #100) is the one on the wire, and sim_main.cpp's OUR_CQ is this value.
OUR_CQ := $(shell python3 -I -c 'import runpy, sys; print(hex(runpy.run_path(sys.argv[1])["CQ_C"]))' $(UCODE_GEN))
TOP        = gptp_plane_wrap
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra -DOUR_CQ_TB=$(OUR_CQ)"
SRCS = gptp_plane_wrap.sv \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/timestamp_counter.sv \
       $(GPTP_DIR)/hdl/ucpu/gptp_ucpu_pkg.sv \
       $(GPTP_DIR)/hdl/ucpu/KL_gptp_ucpu.sv \
       $(GPTP_DIR)/hdl/wire/KL_gptp_rx_parser.sv \
       $(GPTP_DIR)/hdl/wire/KL_gptp_tx_slot.sv \
       $(GPTP_DIR)/hdl/common/KL_gptp_timer.sv \
       $(GPTP_DIR)/hdl/top/KL_gptp_engine.sv
CPP  = sim_main.cpp

.PHONY: all phc-step
.DEFAULT_GOAL := all
all: run phc-step

phc-step:
	python3 phc_step.py --mutants

run: gptp_ucode.hex
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vgptp_plane_sim
	./obj_dir/Vgptp_plane_sim

gptp_ucode.hex: $(UCODE_GEN)
	python3 $< --clk-hz 2000000 -o $@

clean:
	rm -rf obj_dir gptp_ucode.hex
