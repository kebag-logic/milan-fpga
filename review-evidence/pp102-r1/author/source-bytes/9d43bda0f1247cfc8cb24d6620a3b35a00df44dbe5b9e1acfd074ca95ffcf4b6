# SPDX-License-Identifier: CERN-OHL-W-2.0
# F08.4 timer-slot map + 02 §5 event-router map suite — exit 0 = PASS.
#
# Two independent gates, both required:
#   shapes  the REAL protocol_processor_top elaborated at every shape in
#           shape_elab.sh, zero-tolerance -Wall, plus the negative test that
#           the elaboration guard FIRES on an over-large shape
#   run     the map arithmetic graded against an independent re-derivation
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = timer_map_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv timer_map_wrap.sv
CPP  = sim_main.cpp

run: shapes
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vtimer_map_sim
	./obj_dir/Vtimer_map_sim

# the shape sweep over the real top (see shape_elab.sh for what each proves)
shapes:
	@VERILATOR=$(VERILATOR) ./shape_elab.sh

clean:
	rm -rf obj_dir

.PHONY: run shapes clean
