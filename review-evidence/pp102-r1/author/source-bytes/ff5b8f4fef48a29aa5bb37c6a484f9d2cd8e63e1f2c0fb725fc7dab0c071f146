# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_adp_engine suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = tb_adp_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/adp/pp_adp_pkg.sv \
       $(HDL)/common/KL_pp_prng.sv $(HDL)/adp/KL_adp_engine.sv \
       tb_adp_top.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vadp_sim
	./obj_dir/Vadp_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
