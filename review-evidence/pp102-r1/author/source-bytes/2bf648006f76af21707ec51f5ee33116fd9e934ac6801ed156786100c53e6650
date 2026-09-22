# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_srp_talker_fsm + KL_srp_listener_fsm suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = srp_stream_fsms_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/srp/srp_pkg.sv \
       $(HDL)/srp/KL_srp_talker_fsm.sv $(HDL)/srp/KL_srp_listener_fsm.sv \
       srp_stream_fsms_wrap.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vsrp_stream_fsms_sim
	./obj_dir/Vsrp_stream_fsms_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
