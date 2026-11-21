# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The gPTP port's timestamp unit (hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv,
# #884, #665 F6), self-checking at the GMII and MII shapes.
#   make            build and run
#   make mutants    plant each defect of tsu_mutants.py, require its check to fail
VERILATOR ?= verilator
RTL ?= ../../../hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv
SPLIT ?= ../../../hdl/milan/KL_ctrl_split.sv
AXIS = ../../../third_party/verilog-axis/rtl/axis_fifo.v
MDIR ?= ./obj_dir
VFLAGS = --cc --exe --build -j 0 -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Werror-UNDRIVEN \
         -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

all: run

build:
	$(VERILATOR) $(VFLAGS) --top-module tb_gptp_tsu --Mdir $(MDIR) $(RTL) $(SPLIT) $(AXIS) tb_gptp_tsu.sv sim_main.cpp -o Vtb_gptp_tsu

run: build
	$(MDIR)/Vtb_gptp_tsu

mutants:
	python3 tsu_mutants.py

clean:
	rm -rf obj_dir obj_mut_*

.PHONY: all build run mutants clean
