# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_aecp_ucpu skeleton suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl/aecp
TOP        = KL_aecp_ucpu

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/ucpu_pkg.sv $(HDL)/KL_aecp_ucpu.sv
CPP  = sim_main.cpp

run: ucode.hex
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vucpu_sim
	./obj_dir/Vucpu_sim

ucode.hex: $(HDL)/ucode/gen_ucode.py
	python3 $< -o $@

clean:
	rm -rf obj_dir ucode.hex

.PHONY: run clean
