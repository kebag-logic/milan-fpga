# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_aecp_resp_buf suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = KL_aecp_resp_buf

# MEM_TIMEOUT_CYC_P is compressed from its 4096 default so the "no bridge at
# all" arm runs in a few hundred clocks instead of tens of thousands; the
# BFM's 29/23-clock latencies stay well inside it.
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -GMEM_TIMEOUT_CYC_P=96 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/aecp/KL_aecp_resp_buf.sv
CPP  = sim_main.cpp

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vresp_buf_sim
	./obj_dir/Vresp_buf_sim

clean:
	rm -rf obj_dir

.PHONY: run clean
