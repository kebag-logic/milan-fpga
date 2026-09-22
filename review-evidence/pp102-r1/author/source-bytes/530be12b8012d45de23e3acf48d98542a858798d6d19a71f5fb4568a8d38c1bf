# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_aecp_dyn_state suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = KL_aecp_dyn_state

# The SHIPPING shape (1x1) is the one the width guards bite on: a count of 1
# still needs a 1-bit index, and a zero-width one would not elaborate. The
# 8x8 arm is covered by a second build below.
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/aecp/KL_aecp_dyn_state.sv
CPP  = sim_main.cpp

run:
	@rm -f shape_tally.txt
	$(VERILATOR) $(VFLAGS) -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 \
	    --Mdir obj_dir $(SRCS) $(CPP) -o Vdyn_state_sim
	./obj_dir/Vdyn_state_sim
	$(VERILATOR) $(VFLAGS) -GN_STREAM_IN_P=1 -GN_STREAM_OUT_P=1 \
	    -CFLAGS "-DSHAPE_1x1=1 -Wall -Wextra" --Mdir obj_1x1 $(SRCS) $(CPP) -o Vdyn_state_1x1
	./obj_1x1/Vdyn_state_1x1
	@awk '{c+=$$1; f+=$$2} END {printf "%d checks: %d PASS, %d FAIL\n", c, c-f, f}' \
	    shape_tally.txt

clean:
	rm -rf obj_dir obj_1x1 shape_tally.txt

.PHONY: run clean
