# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of milan_csr.sv (AXI4-Lite TSN CSR block).
# Three executables:
#   sim_main.cpp -> Vmilan_csr        : legacy map regression at the N=1
#     silicon shape + the P11 0x800 window index-0 hard aliases and the
#     out-of-range rule (lane-K engine inputs at their datapath ties).
#   CHMAP_RDBK_P: the chmap map-RAM readback capability (0x910/0x914). The
#     THREE executables deliberately split it - sim_main/sim_live leave it at
#     the honest default 0 ("no read port wired in this build", which is the
#     state milan_datapath actually shipped in) so the UNSUPPORTED path is a
#     negative control that can fail, and sim_win sets 3 (both ports wired)
#     so the measured path is exercised against a modelled map RAM.
#   sim_win.cpp  -> obj_win/Vcsr_win  : the window at N_LISTENERS_P=4 /
#     N_TALKERS_P=4 against MODELED lane-K engines - LCTX/TCTX port-B
#     pipeline + snap arbitration (SNAP atomicity under a free-running
#     event pump), lwSRP-ctx/ACMP-tbl master protocols, CFG write bundles.
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

# milan_csr.sv `include-s gen/lwsrp_csr_defaults.svh (generated from the
# end-station config by sw/builder/endstation_builder.py), so hdl/common/csr
# must be an include dir here exactly as it already is in tb/verilator/milan_dp,
# tb/verilator/hostplane and sw/litex/milan_soc.py.
VFLAGS = --cc --exe --build -j 0 \
         +incdir+$(RTL_DIR)/common/csr \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2"


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
#! THE LIVE-INTEGRATION LEG IS DELETED. obj_live wired milan_csr's 0x800
#! window to the REAL context engines behind it - KL_lwsrp_top's attribute-row
#! table and KL_acmp_lstn_ctx's bind table - and BOTH are deleted with the
#! legacy 1722.1/SRP plane. There is no context table for that window to
#! provision any more: milan_datapath leaves the ports open and the window's
#! grant reads a structural zero. A fixture rebuilt against nothing would
#! prove nothing, so the leg goes rather than being kept green on stubs.
#! (csr_win_live.sv and sim_live.cpp deleted with it.)

.PHONY: all run clean
all: run

obj_dir/Vcsr_sim: $(SRCS) $(GEN_CSR) $(SHAPE_DEF) sim_main.cpp
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS) --top-module $(TOP) $(SRCS) sim_main.cpp -o Vcsr_sim

# The SAME sim_main at the milan clock the AX7101 actually ships (100 MHz)
# rather than the RTL's 125 MHz default. Every frequency-derived reset is
# invisible at the default, because that is the frequency the constants were
# written for: PTP_INCR carried a hardcoded 0x08000000 readback against a
# derived flop and reported 8 ns on a 10 ns domain, and no check could see
# it. This leg is the general guard for that whole class, not just for
# PTP_INCR. The expectation is computed from CSR_MILAN_CLK_HZ, so the two
# legs share one derivation instead of two literals.
obj_100m/Vcsr_sim100: $(SRCS) $(GEN_CSR) $(SHAPE_DEF) sim_main.cpp
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS) --Mdir obj_100m --top-module $(TOP) \
	  -GMILAN_CLK_FREQ_HZ_P=100000000 \
	  -CFLAGS -DCSR_MILAN_CLK_HZ=100000000ULL \
	  $(SRCS) sim_main.cpp -o Vcsr_sim100

obj_win/Vcsr_win: $(SRCS) $(GEN_CSR) $(SHAPE_4x4_F) sim_win.cpp
	$(VERILATOR) $(SHAPE_4x4) $(VFLAGS) --Mdir obj_win --top-module $(TOP) \
	  -GN_LISTENERS_P=4 -GN_TALKERS_P=4 -GCHMAP_RDBK_P=3 \
	  $(SRCS) sim_win.cpp -o Vcsr_win


run: obj_dir/Vcsr_sim obj_100m/Vcsr_sim100 obj_win/Vcsr_win
	@echo "======================================================================"
	./obj_dir/Vcsr_sim
	./obj_100m/Vcsr_sim100
	./obj_win/Vcsr_win

clean:
	rm -rf obj_dir obj_100m obj_win
