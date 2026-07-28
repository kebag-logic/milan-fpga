# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_talker_diag_ctx (Milan v1.2 Table 5.4 - the
# per-Stream-Output diagnostic counters, interval + reset-on-start semantics).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = tkdiag_tb_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-GENUNNAMED \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee1722/avtp/KL_talker_diag_ctx.sv \
       tkdiag_tb_top.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vtkdiag_sim
	@echo "======================================================================"
	./obj_dir/Vtkdiag_sim

clean:
	rm -rf obj_dir
