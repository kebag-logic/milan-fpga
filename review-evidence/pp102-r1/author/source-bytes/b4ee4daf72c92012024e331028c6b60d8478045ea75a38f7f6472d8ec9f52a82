# SPDX-License-Identifier: CERN-OHL-W-2.0
# CONTROLLER_AVAILABLE frame-builder suite, exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = KL_aecp_ca_originator

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/aecp/KL_aecp_ca_originator.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vca_originator_sim
	./obj_dir/Vca_originator_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
