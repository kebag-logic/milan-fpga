# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of milan_csr.sv (AXI4-Lite TSN CSR block).
# Default builds:
#   obj_dir/Vcsr_sim     : sim_main.cpp, flat map and N=1 window aliases.
#   obj_100m/Vcsr_sim100 : sim_main.cpp, frequency-derived resets at 100 MHz.
#   obj_win/Vcsr_win     : sim_win.cpp, 4x4 window against modelled engines.
#   obj_gptp/Vcsr_gptp   : sim_gptp.cpp, fabric gPTP publication enabled.
#   obj_pps/Vcsr_pps     : sim_main.cpp, PPS alarm enabled.
#   obj_reset/Vcsr_reset: sim_main.cpp, generated nonzero SRP reset bits.
# CHMAP_RDBK_P stays 0 in sim_main for the unsupported-path control.
# sim_win sets it to 3 and exercises both modelled map-RAM read ports.
#   make        - build and run every default leg above
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
# ENTITY SHAPE: milan_csr `include-s gen/adp_shape_defaults.svh, GENERATED
# from an end-station config by sw/builder/endstation_builder.py.
# sim_main uses endstation_arty_current, sim_win uses endstation_arty_4x4,
# and sim_gptp uses endstation_ax7101_8x8. The reset-bits leg regenerates
# arty_current with both SRP admission reset bits set.
# Entity counts come from each config, independently of the CSR window's
# N_TALKERS_P/N_LISTENERS_P parameters.
CFG_DIR    = ../../../configs/generated
# The N=1 default target needs its shape named just as much as the NxN ones:
# without it the include falls through to hdl/common/gen/, which is
# whichever config was last --write-rtl'd, so regenerating for the 8x8 ship
# shape made this suite assert the 1x1 ADP words against an 8x8 entity.
SHAPE_1x1  = +incdir+$(CFG_DIR)/endstation_arty_current
SHAPE_4x4  = +incdir+$(CFG_DIR)/endstation_arty_4x4
SHAPE_8x8  = +incdir+$(CFG_DIR)/endstation_ax7101_8x8
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = milan_csr

# The PPS alarm's elaborated pulse width (#260), passed to BOTH the RTL
# parameter and the harness's expectation from this one variable so the two
# cannot drift. 125_000 is the RTL default: at 125 MHz it is the shipping 1 ms.
PPS_WIDTH_CYC ?= 125000

# milan_csr.sv `include-s gen/lwsrp_csr_defaults.svh (generated from the
# end-station config by sw/builder/endstation_builder.py), so hdl/common/csr
# must be an include dir here exactly as it already is in tb/verilator/milan_dp,
# tb/verilator/milan_dp and sw/litex/milan_soc.py.
VFLAGS = --cc --exe --build -j 0 \
         +incdir+$(RTL_DIR)/common/csr \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"


# GENERATED INCLUDES ARE PREREQUISITES. milan_csr.sv `include-s these; make
# cannot see through a `include, so without naming them here a regenerated
# shape leaves a stale objdir behind and the harness silently keeps testing
# the PREVIOUS entity definition. (Caught exactly that way 2026-07-27: the
# suite ran a 1x1 harness against an 8x8 objdir and reported 9/9.)
GEN_CSR   = $(RTL_DIR)/common/csr/gen/lwsrp_csr_defaults.svh
SHAPE_DEF = $(RTL_DIR)/common/gen/adp_shape_defaults.svh
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

.PHONY: all run reset-bits clean
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
	  -CFLAGS "-DCSR_MILAN_CLK_HZ=100000000ULL -Wall -Wextra" \
	  $(SRCS) sim_main.cpp -o Vcsr_sim100

obj_win/Vcsr_win: $(SRCS) $(GEN_CSR) $(SHAPE_4x4_F) sim_win.cpp
	$(VERILATOR) $(SHAPE_4x4) $(VFLAGS) --Mdir obj_win --top-module $(TOP) \
	  -GN_LISTENERS_P=4 -GN_TALKERS_P=4 -GCHMAP_RDBK_P=3 \
	  $(SRCS) sim_win.cpp -o Vcsr_win

obj_gptp/Vcsr_gptp: $(SRCS) $(GEN_CSR) $(SHAPE_8x8_F) sim_gptp.cpp
	$(VERILATOR) $(SHAPE_8x8) $(VFLAGS) --Mdir obj_gptp --top-module $(TOP) \
	  -GGPTP_PLANE_EN_P=1 $(SRCS) sim_gptp.cpp -o Vcsr_gptp

# The SAME sim_main with the PPS alarm ELABORATED (#260). The registers at
# 0x548..0x55C decode in every build, but PPS_P gates what software is
# allowed to see: CTRL[0]'s readback, the built bit CTRL[16] and PPS_WIDTH.
# The default leg above therefore proves the UNSUPPORTED arm (a structural
# zero at o_pps_enable no matter what is written) and this one proves the
# supported arm, from one harness rather than two that drift. Without it the
# only elaboration anywhere in the suites had PPS_P=0 and the three gated
# bits were never observed in their 1 state.
obj_pps/Vcsr_pps: $(SRCS) $(GEN_CSR) $(SHAPE_DEF) sim_main.cpp
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS) --Mdir obj_pps --top-module $(TOP) \
	  -GPPS_P=1 -GPPS_WIDTH_CYC_P=$(PPS_WIDTH_CYC) \
	  -CFLAGS "-DCSR_PPS_P=1 -DCSR_PPS_WIDTH_CYC=$(PPS_WIDTH_CYC)u -Wall -Wextra" \
	  $(SRCS) sim_main.cpp -o Vcsr_pps


run: obj_dir/Vcsr_sim obj_100m/Vcsr_sim100 obj_win/Vcsr_win obj_gptp/Vcsr_gptp \
     obj_pps/Vcsr_pps
	@echo "======================================================================"
	./obj_dir/Vcsr_sim
	./obj_100m/Vcsr_sim100
	./obj_win/Vcsr_win
	./obj_gptp/Vcsr_gptp
	./obj_pps/Vcsr_pps
	$(MAKE) reset-bits

# Generated cold-reset admission bits differ from the ordinary zero fixture.
# The expected mask is independent of the emitted header.
reset-bits:
	python3 ../../common/gen_declaration_fixture.py fixtures/reset_bits.yaml obj_reset/fixture
	$(VERILATOR) +incdir+obj_reset/fixture $(VFLAGS) --Mdir obj_reset --top-module $(TOP) \
	  -CFLAGS "-DCSR_SRP_RESET_BITS=3u -Wall -Wextra" $(SRCS) sim_main.cpp -o Vcsr_reset
	./obj_reset/Vcsr_reset

clean:
	rm -rf obj_dir obj_100m obj_win obj_gptp obj_pps obj_reset
