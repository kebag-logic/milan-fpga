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
# ENTITY SHAPE: milan_csr `include-s gen/adp_shape_defaults.svh, GENERATED
# from an end-station config by sw/builder/endstation_builder.py. The three
# executables deliberately elaborate THREE DIFFERENT configs, so a value that
# tracked anything other than the config it was built against would show up:
#   sim_main -> the tracked default (arty_current 1x1)  -> 1 src  / 2 sinks
#   sim_win  -> configs/generated/endstation_arty_4x4   -> 5 src  / 5 sinks
#   sim_live -> configs/generated/endstation_ax7101_8x8 -> 9 src  / 9 sinks
# Note sim_win's 0x800 WINDOW is 4x4 and sim_live's is 2x2: the shape numbers
# come from the config, never from N_TALKERS_P/N_LISTENERS_P.
CFG_DIR    = ../../../configs/generated
# The N=1 default target needs its shape named just as much as the NxN ones:
# without it the include falls through to hdl/common/csr/gen/, which is
# whichever config was last --write-rtl'd, so regenerating for the 8x8 ship
# shape made this suite assert the 1x1 ADP words against an 8x8 entity.
SHAPE_1x1  = +incdir+$(CFG_DIR)/endstation_arty_current
SHAPE_4x4  = +incdir+$(CFG_DIR)/endstation_arty_4x4
SHAPE_8x8  = +incdir+$(CFG_DIR)/endstation_ax7101_8x8
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = milan_csr
TOPL       = csr_win_live

# milan_csr.sv `include-s gen/lwsrp_csr_defaults.svh (generated from the
# end-station config by sw/builder/endstation_builder.py), so hdl/common/csr
# must be an include dir here exactly as it already is in tb/verilator/milan_dp,
# tb/verilator/hostplane and sw/litex/milan_soc.py.
VFLAGS = --cc --exe --build -j 0 \
         +incdir+$(RTL_DIR)/common/csr \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"

LIVEFLAGS = -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-PINCONNECTEMPTY \
            -Wno-PINMISSING -Wno-IMPORTSTAR -Wno-TIMESCALEMOD

# GENERATED INCLUDES ARE PREREQUISITES. milan_csr.sv `include-s these; make
# cannot see through a `include, so without naming them here a regenerated
# shape leaves a stale objdir behind and the harness silently keeps testing
# the PREVIOUS entity definition. (Caught exactly that way 2026-07-27: the
# suite ran a 1x1 harness against an 8x8 objdir and reported 9/9.)
GEN_CSR   = $(RTL_DIR)/common/csr/gen/lwsrp_csr_defaults.svh
SHAPE_DEF = $(RTL_DIR)/common/csr/gen/adp_shape_defaults.svh
SHAPE_4x4_F = $(CFG_DIR)/endstation_arty_4x4/gen/adp_shape_defaults.svh
SHAPE_8x8_F = $(CFG_DIR)/endstation_ax7101_8x8/gen/adp_shape_defaults.svh

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

obj_dir/Vcsr_sim: $(SRCS) $(GEN_CSR) $(SHAPE_DEF) sim_main.cpp
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS) --top-module $(TOP) $(SRCS) sim_main.cpp -o Vcsr_sim

obj_win/Vcsr_win: $(SRCS) $(GEN_CSR) $(SHAPE_4x4_F) sim_win.cpp
	$(VERILATOR) $(SHAPE_4x4) $(VFLAGS) --Mdir obj_win --top-module $(TOP) \
	  -GN_LISTENERS_P=4 -GN_TALKERS_P=4 \
	  $(SRCS) sim_win.cpp -o Vcsr_win

obj_live/V$(TOPL): $(LIVE_SRCS) $(GEN_CSR) $(SHAPE_8x8_F) sim_live.cpp
	$(VERILATOR) $(SHAPE_8x8) $(VFLAGS) $(LIVEFLAGS) --Mdir obj_live --top-module $(TOPL) \
	  -GCLK_FREQ_HZ_P=10000 \
	  $(LIVE_SRCS) sim_live.cpp -o V$(TOPL)

run: obj_dir/Vcsr_sim obj_win/Vcsr_win obj_live/V$(TOPL)
	@echo "======================================================================"
	./obj_dir/Vcsr_sim
	./obj_win/Vcsr_win
	./obj_live/V$(TOPL)

clean:
	rm -rf obj_dir obj_win obj_live
