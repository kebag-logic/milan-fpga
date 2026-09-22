# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_pp_tx_arbiter suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = tx_arbiter_harness

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv \
       $(HDL)/packet_engine/KL_pp_tx_slots.sv \
       $(HDL)/packet_engine/KL_pp_tx_arbiter.sv \
       tx_arbiter_harness.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vtx_arbiter_sim
	./obj_dir/Vtx_arbiter_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
