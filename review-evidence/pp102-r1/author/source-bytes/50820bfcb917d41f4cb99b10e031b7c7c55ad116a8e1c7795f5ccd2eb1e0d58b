# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_acmp_talker suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = KL_acmp_talker

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/srp/srp_pkg.sv $(HDL)/acmp/KL_acmp_talker.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vacmp_talker_sim
	./obj_dir/Vacmp_talker_sim

# the repo's zero-warning gate (no width waivers)
lint:
	$(VERILATOR) --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
	  -Wno-UNUSEDPARAM $(SRCS)

clean:
	rm -rf obj_dir

.PHONY: run lint clean
