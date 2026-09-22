# SPDX-License-Identifier: CERN-OHL-W-2.0
# AECP registry monitor lifecycle suite, exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = KL_aecp_notify

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -GN_CTRL_P=2 -GN_STREAM_IN_P=1 -GN_STREAM_OUT_P=1 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/aecp/KL_aecp_notify.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vaecp_notify_sim
	./obj_dir/Vaecp_notify_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
