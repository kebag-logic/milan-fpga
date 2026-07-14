# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_lwsrp_top.sv — the whole lwSRP engine
# (timers + applicant TX + ingress/walker/registrar + bandwidth gate)
# end-to-end at a 10 kHz scaled clock: declare cadence, reservation
# activation with slope-before-gate ordering, gate-before-slope teardown,
# 75% refusal, LeaveAll turn + re-declare. Needs third_party/verilog-axis.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = KL_lwsrp_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -GCLK_FREQ_HZ_P=10000 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/lwsrp/lwsrp_pkg.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_timers.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_tx.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_ingress.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_walker.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_registrar.sv $(RTL_DIR)/lwsrp/KL_lwsrp_ta_registrar.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_rx.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_bw_gate.sv \
       $(RTL_DIR)/lwsrp/KL_lwsrp_top.sv \
       $(AXIS_DIR)/axis_fifo.v
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vlwsrp_sim
	@echo "======================================================================"
	./obj_dir/Vlwsrp_sim

clean:
	rm -rf obj_dir
