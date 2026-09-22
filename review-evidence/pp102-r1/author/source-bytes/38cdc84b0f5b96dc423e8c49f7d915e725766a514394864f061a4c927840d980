# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_pp_prng suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl/common
TOP        = KL_pp_prng

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/KL_pp_prng.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vprng_sim
	./obj_dir/Vprng_sim

lint:
	$(VERILATOR) --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
	    -Wno-UNUSEDPARAM $(SRCS)

clean:
	rm -rf obj_dir

.PHONY: run lint clean
