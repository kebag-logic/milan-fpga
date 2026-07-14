# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_acmp_listener.sv (Milan v1.2 listener SM).
# Runs at a 10 kHz scaled clock (-GCLK_FREQ_HZ_P) so the 200 ms / 4 s / 10 s
# timers are simulable (1 ms = 10 cycles).
#   make run    - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_acmp_listener

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -GCLK_FREQ_HZ_P=10000 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-MULTIDRIVEN -Wno-IMPORTSTAR \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/acmp/acmp_pkg.sv $(RTL_DIR)/acmp/KL_acmp_listener.sv

all: run

obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp

run: obj_dir/V$(TOP)
	./obj_dir/V$(TOP)

clean:
	rm -rf obj_dir

.PHONY: all run clean
