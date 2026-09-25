# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_talker_diag_ctx (Milan v1.2 Table 5.4 - the
# per-Stream-Output diagnostic counters, interval + reset-on-start semantics).
#   make        - build and run the self-checking harness, then its mutation
#                 arm (mcr_mutants.py: the #387 pending-restart merge)
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = tkdiag_tb_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-GENUNNAMED \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

# #387: the restart engine and the build directory, overridable so
# mcr_mutants.py elaborates a MUTATED copy through this same recipe
MCR_SRC     ?= $(RTL_DIR)/ieee1722/avtp/KL_media_clock_restart.sv
TKDIAG_MDIR ?= obj_dir

SRCS = $(RTL_DIR)/ieee1722/avtp/KL_talker_diag_ctx.sv \
       $(MCR_SRC) \
       tkdiag_tb_top.sv
CPP  = sim_main.cpp

.PHONY: all run build clean
all: run

build:
	$(VERILATOR) $(VFLAGS) --Mdir $(TKDIAG_MDIR) $(SRCS) $(CPP) -o Vtkdiag_sim

run: build
	@echo "======================================================================"
	./$(TKDIAG_MDIR)/Vtkdiag_sim
	python3 mcr_mutants.py

clean:
	rm -rf obj_dir
