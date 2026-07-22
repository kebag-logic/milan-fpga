# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of milan_csr.sv (AXI4-Lite TSN CSR block).
# Three executables:
#   sim_main.cpp -> Vmilan_csr        : legacy map regression at the N=1
#     silicon shape + the P11 0x800 window index-0 hard aliases and the
#     out-of-range rule (lane-K engine inputs at their datapath ties).
#   sim_win.cpp  -> obj_win/Vcsr_win  : the window at N_LISTENERS_P=4 /
#     N_TALKERS_P=4 against MODELED lane-K engines - LCTX/TCTX port-B
#     pipeline + snap arbitration (SNAP atomicity under a free-running
#     event pump), lwSRP-ctx/ACMP-tbl master protocols, CFG write bundles.
#   sim_live.cpp -> obj_live/Vcsr_win_live: the window against LIVE
#     engines - KL_lwsrp_top (N_CTX_P=3) row provisioning through the
#     window, KL_acmp_lstn_ctx (N=2) fast-connect bind read back via the
#     window (csr_win_live.sv wrapper).
#   make        - build and run all three self-checking harnesses
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = milan_csr
TOPL       = csr_win_live

VFLAGS = --cc --exe --build -j 0 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"

LIVEFLAGS = -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-PINCONNECTEMPTY \
            -Wno-PINMISSING -Wno-IMPORTSTAR -Wno-TIMESCALEMOD

SRCS = $(RTL_DIR)/common/csr/milan_csr.sv
LIVE_SRCS = $(RTL_DIR)/ieee8021q/srp/lwsrp_pkg.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_timers.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_tx.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ingress.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_walker.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_registrar.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ta_registrar.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_rx.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_bw_gate.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ctx.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ctx_tx.sv \
            $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_top.sv \
            $(AXIS_DIR)/axis_fifo.v \
            $(RTL_DIR)/ieee17221/acmp/acmp_pkg.sv \
            $(RTL_DIR)/ieee17221/acmp/KL_acmp_lstn_ctx.sv \
            $(SRCS) csr_win_live.sv

.PHONY: all run clean
all: run

obj_dir/Vcsr_sim: $(SRCS) sim_main.cpp
	$(VERILATOR) $(VFLAGS) --top-module $(TOP) $(SRCS) sim_main.cpp -o Vcsr_sim

obj_win/Vcsr_win: $(SRCS) sim_win.cpp
	$(VERILATOR) $(VFLAGS) --Mdir obj_win --top-module $(TOP) \
	  -GN_LISTENERS_P=4 -GN_TALKERS_P=4 \
	  $(SRCS) sim_win.cpp -o Vcsr_win

obj_live/V$(TOPL): $(LIVE_SRCS) sim_live.cpp
	$(VERILATOR) $(VFLAGS) $(LIVEFLAGS) --Mdir obj_live --top-module $(TOPL) \
	  -GCLK_FREQ_HZ_P=10000 \
	  $(LIVE_SRCS) sim_live.cpp -o V$(TOPL)

run: obj_dir/Vcsr_sim obj_win/Vcsr_win obj_live/V$(TOPL)
	@echo "======================================================================"
	./obj_dir/Vcsr_sim
	./obj_win/Vcsr_win
	./obj_live/V$(TOPL)

clean:
	rm -rf obj_dir obj_win obj_live
