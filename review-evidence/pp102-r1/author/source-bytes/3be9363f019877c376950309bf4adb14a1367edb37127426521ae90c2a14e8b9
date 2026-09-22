# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_srp_top end-to-end engine suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = srp_top_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/srp/srp_pkg.sv \
       $(HDL)/common/KL_pp_prng.sv $(HDL)/common/KL_pp_timer_service.sv \
       $(HDL)/packet_engine/KL_pp_tx_slots.sv \
       $(HDL)/srp/KL_srp_decoder.sv $(HDL)/srp/KL_srp_domain.sv \
       $(HDL)/srp/KL_srp_vlan.sv $(HDL)/srp/KL_srp_talker_fsm.sv \
       $(HDL)/srp/KL_srp_listener_fsm.sv $(HDL)/srp/KL_srp_admission.sv \
       $(HDL)/srp/KL_srp_encoder.sv $(HDL)/srp/KL_srp_top.sv \
       srp_top_wrap.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vsrp_top_sim
	./obj_dir/Vsrp_top_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
