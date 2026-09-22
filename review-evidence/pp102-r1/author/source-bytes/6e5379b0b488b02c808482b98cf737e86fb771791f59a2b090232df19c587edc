# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_pp_timer_service suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl/common
TOP        = KL_pp_timer_service

# Compressed time (09 §3 TIM): 4 clk per µs tick x 5 µs ticks per ms tick
# = 20 clk per compressed ms; 12 slots so a full sweep (14 cycles) fits
# inside one compressed ms. These -G values are mirrored as enums at the
# top of sim_main.cpp — change both together.
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -GSLOTS_P=12 -GDIV_US_P=4 -GDIV_MS_P=5 \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/pp_pkg.sv $(HDL)/KL_pp_timer_service.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vtimer_sim
	./obj_dir/Vtimer_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
