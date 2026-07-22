# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_maap verification: IEEE 1722 Annex B probe/defend/announce vs the
# pipewire maap.c reference contract (golden frames + SM walk + conflicts).
# 10 kHz scaled clock: 1 ms tick = 10 cycles (probe 500 ms ~ 5k cycles).
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_maap
VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         -GCLK_FREQ_HZ_P=10000 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -CFLAGS "-std=c++17 -O2"
SRCS = $(RTL_DIR)/ieee1722/maap/KL_maap.sv
.PHONY: all run clean coverage
all: run
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o VKL_maap_sim
	./obj_dir/VKL_maap_sim

# Line coverage, gated at 95 % (defensive arms carry coverage_off pragmas)
coverage:
	rm -rf obj_cov coverage.dat cov_annotated
	$(VERILATOR) $(VFLAGS) --coverage --Mdir obj_cov $(SRCS) sim_main.cpp \
	    -o VKL_maap_cov
	./obj_cov/VKL_maap_cov
	verilator_coverage --annotate cov_annotated --annotate-min 1 coverage.dat \
	    | tail -2
	@python3 ../avtp_rxmon/cov_gate.py cov_annotated 95 KL_maap.sv
clean:
	rm -rf obj_dir obj_cov coverage.dat cov_annotated
