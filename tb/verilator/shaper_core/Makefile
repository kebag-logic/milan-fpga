# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of traffic_shaping_core.sv (802.1Qav arbiter + CBS).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# Pure RTL (credit_based_shaper + traffic_shaping_core + axi_stream_if); no
# XPM/DSP primitives are instantiated, so no Xilinx tools are needed.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = shaper_core_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINMISSING \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/ieee8021q/ts \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR)"

SRCS = shaper_core_wrap.sv \
       $(RTL_DIR)/ieee8021q/ts/traffic_shaping_core.sv \
       $(RTL_DIR)/ieee8021q/ts/credit_based_shaper.sv \
       $(RTL_DIR)/common/axi_stream_if.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vshaper_sim
	@echo "======================================================================"
	./obj_dir/Vshaper_sim

clean:
	rm -rf obj_dir
