# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_pp_maap (IEEE 1722-2016 Annex B) suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = maap_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv \
       $(HDL)/common/KL_pp_prng.sv $(HDL)/common/KL_pp_timer_service.sv \
       $(HDL)/packet_engine/KL_pp_tx_slots.sv \
       $(HDL)/maap/KL_pp_maap.sv \
       maap_wrap.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vmaap_sim
	./obj_dir/Vmaap_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
