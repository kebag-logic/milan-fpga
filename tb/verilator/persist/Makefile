# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of the Milan saved-state fast-connect PERSISTENCE
# JOURNAL replay path (roadmap item 9):
#
#   CSR 0x7B8-0x7C4 -> KL_persist_journal -> rest_* (E1) -> KL_acmp_lstn_ctx
#
# persist_wrap.sv carries the CSR decode milan_csr has to reproduce, so the
# suite gates the register ABI as well as the RTL. Runs at a 10 kHz scaled
# clock (-GCLK_FREQ_HZ_P) so the ACMP 200 ms / 4 s ladder is simulable
# (1 ms = 10 cycles) and the restored sink can be driven all the way to a
# bound, streaming listener inside the harness.
#
#   make run    - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = persist_wrap

VFLAGS = --cc --exe --build -j 0 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-MULTIDRIVEN -Wno-IMPORTSTAR \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee17221/acmp/acmp_pkg.sv \
       $(RTL_DIR)/ieee17221/acmp/KL_acmp_lstn_ctx.sv \
       $(RTL_DIR)/ieee17221/aecp/KL_persist_journal.sv \
       persist_wrap.sv

all: run

obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) $(VFLAGS) --top-module $(TOP) -GCLK_FREQ_HZ_P=10000 \
	  $(SRCS) sim_main.cpp

run: obj_dir/V$(TOP)
	./obj_dir/V$(TOP)

clean:
	rm -rf obj_dir

.PHONY: all run clean
