# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
VERILATOR ?= verilator
BENCH_DIR  = ../../../bench/arty
TOP        = gasket_tb_top
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I$(CURDIR)"
SRCS = $(BENCH_DIR)/bench_afifo.sv $(BENCH_DIR)/bench_mii_tx.sv \
       $(BENCH_DIR)/bench_mii_rx.sv gasket_tb_top.sv
CPP  = sim_main.cpp

.PHONY: all run mutants clean
.DEFAULT_GOAL := all
all: run mutants

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vgasket_sim
	./obj_dir/Vgasket_sim

# Rule 8: prove the 81 checks above are load-bearing. Four defects are
# injected into the real bench RTL, one at a time, and each must make the
# SAME harness fail; the unmutated build must still pass. Mutants are built
# in a temporary directory, so nothing is written into the tree.
mutants:
	python3 mutants.py

clean:
	rm -rf obj_dir
