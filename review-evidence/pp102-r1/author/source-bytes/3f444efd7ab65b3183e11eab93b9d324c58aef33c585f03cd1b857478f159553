# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_srp_decoder suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = KL_srp_decoder

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/srp/srp_pkg.sv $(HDL)/srp/KL_srp_decoder.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vsrp_decoder_sim
	./obj_dir/Vsrp_decoder_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
