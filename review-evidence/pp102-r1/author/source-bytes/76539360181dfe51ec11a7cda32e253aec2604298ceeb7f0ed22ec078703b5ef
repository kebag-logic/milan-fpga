# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_pp_acmp_listener MTXW suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = KL_pp_acmp_listener

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -GSTRM_TIMEOUT_CYC_P=32 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/acmp/pp_acmp_pkg.sv \
       $(HDL)/acmp/KL_pp_acmp_listener.sv
CPP  = sim_main.cpp

run: ltn_rom.hex
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vacmp_lsm_sim
	./obj_dir/Vacmp_lsm_sim

ltn_rom.hex: $(HDL)/acmp/rom/gen_ltn_rom.py
	python3 $< -o $@

clean:
	rm -rf obj_dir ltn_rom.hex

.PHONY: run clean
