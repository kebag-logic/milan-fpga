# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_pp_normalizer + KL_pp_dispatch suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = tb_dispatch_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv \
       $(HDL)/packet_engine/KL_pp_normalizer.sv \
       $(HDL)/packet_engine/KL_pp_dispatch.sv \
       tb_dispatch_top.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vdispatch_sim
	./obj_dir/Vdispatch_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
