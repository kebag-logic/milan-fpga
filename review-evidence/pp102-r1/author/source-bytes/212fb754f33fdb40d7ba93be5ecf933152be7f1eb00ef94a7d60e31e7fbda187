# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_srp_encoder + KL_srp_domain + KL_srp_vlan suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = srp_tb_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/packet_engine/KL_pp_tx_slots.sv \
       $(HDL)/srp/KL_srp_encoder.sv $(HDL)/srp/KL_srp_domain.sv \
       $(HDL)/srp/KL_srp_vlan.sv srp_tb_wrap.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vsrp_sim
	./obj_dir/Vsrp_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
