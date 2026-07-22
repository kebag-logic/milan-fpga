# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of the Milan v1.2 ACMP listener SM.
# Two executables:
#   sim_main.cpp -> VKL_acmp_listener  : the 2-sink compatibility wrapper,
#     byte-identical regression of the original single-sink sequences.
#   sim_ctx.cpp  -> VKL_acmp_lstn_ctx  : the N-context core at N=4 with
#     MIXED per-context policies (PROBE_SM_EN=0101, SID_EXPLICIT=0110) —
#     shared SM + context RAM + one timer wheel + table req/grant port.
# Runs at a 10 kHz scaled clock (-GCLK_FREQ_HZ_P) so the 200 ms / 4 s / 10 s
# timers are simulable (1 ms = 10 cycles).
#   make run    - build and run both self-checking harnesses
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_acmp_listener
TOPC       = KL_acmp_lstn_ctx

VFLAGS = --cc --exe --build -j 0 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-MULTIDRIVEN -Wno-IMPORTSTAR \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee17221/acmp/acmp_pkg.sv \
       $(RTL_DIR)/ieee17221/acmp/KL_acmp_lstn_ctx.sv \
       $(RTL_DIR)/ieee17221/acmp/KL_acmp_listener.sv

all: run

obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) $(VFLAGS) --top-module $(TOP) -GCLK_FREQ_HZ_P=10000 \
	  $(SRCS) sim_main.cpp

obj_ctx/V$(TOPC): $(SRCS) sim_ctx.cpp
	$(VERILATOR) $(VFLAGS) --Mdir obj_ctx --top-module $(TOPC) \
	  -GCLK_FREQ_HZ_P=10000 -GN_SINKS_P=4 \
	  -GPROBE_SM_EN_P=5 -GSID_EXPLICIT_P=6 \
	  $(SRCS) sim_ctx.cpp

run: obj_dir/V$(TOP) obj_ctx/V$(TOPC)
	./obj_dir/V$(TOP)
	./obj_ctx/V$(TOPC)

clean:
	rm -rf obj_dir obj_ctx

.PHONY: all run clean
