# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_pp_side_port + KL_pp_trace_ring suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = side_port_tb_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/packet_engine/KL_pp_trace_ring.sv \
       $(HDL)/packet_engine/KL_pp_side_port.sv \
       side_port_tb_wrap.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vside_port_sim
	./obj_dir/Vside_port_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
