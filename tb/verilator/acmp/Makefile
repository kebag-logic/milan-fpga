# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of the Milan v1.2 talker-side ACMP.
# Two executables:
#   sim_main.cpp -> VKL_acmp_responder : the single-source compatibility
#     wrapper, byte-identical regression of the original sequences.
#   sim_ctx.cpp  -> VKL_acmp_tlkr_ctx  : the N-source core at N=4 —
#     per-uid probe windows on ONE shared 1 s sweep, per-source stream
#     params, TALKER_UNKNOWN_ID beyond N.
#   make run    - build and run both self-checking harnesses
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_acmp_responder
TOPC       = KL_acmp_tlkr_ctx

VFLAGS = --cc --exe --build -j 0 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee17221/acmp/acmp_pkg.sv \
       $(RTL_DIR)/ieee17221/acmp/KL_acmp_tlkr_ctx.sv \
       $(RTL_DIR)/ieee17221/acmp/KL_acmp_responder.sv

all: run

obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) $(VFLAGS) --top-module $(TOP) $(SRCS) sim_main.cpp

obj_ctx/V$(TOPC): $(SRCS) sim_ctx.cpp
	$(VERILATOR) $(VFLAGS) --Mdir obj_ctx --top-module $(TOPC) -GN_SRC_P=4 \
	  $(SRCS) sim_ctx.cpp

run: obj_dir/V$(TOP) obj_ctx/V$(TOPC)
	./obj_dir/V$(TOP)
	./obj_ctx/V$(TOPC)

clean:
	rm -rf obj_dir obj_ctx

.PHONY: all run clean
