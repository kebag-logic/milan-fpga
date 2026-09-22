# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_pp_event_router suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl/packet_engine
TOP        = KL_pp_event_router

# Shipping shape: N_SRC_P = 16, PAYLOAD_W_P = 16 (no -G overrides — the
# shape we ship is the shape we simulate). The model in sim_main.cpp pins
# the same N=16/PW=16 as enums — change both together.
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/KL_pp_event_router.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vevtr_sim
	./obj_dir/Vevtr_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
