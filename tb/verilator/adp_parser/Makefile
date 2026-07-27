# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_adp_parser.sv (ADP receive/decapsulate engine).
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts
#
# THIS SUITE IS THE GATE ON THE ENUM CAST. Note the deliberate ABSENCE of
# `-Wno-fatal`: Verilator rates ENUMVALUE as an %Error, so an uncast
# `rcv_entity_info_o.adp_message_type <= s_axis.tdata[35:32]` makes this
# target FAIL TO BUILD. Every other suite in the tree carries -Wno-fatal;
# that, plus this module having had no Verilator suite at all (only the
# Vivado xsim TB under tb/utests/adp/kl-adp-parser/), is how the uncast
# assignment survived. Do not add -Wno-fatal or -Wno-ENUMVALUE here.
#
# -Wno-CASEINCOMPLETE is the ONE suppression here, and it is scoped by that:
# `case (adp_state)` has no default branch and state_t is a 3-member enum in a
# 3-bit base type, so codes 3..7 are formally uncovered. They are unreachable -
# adp_state is reset to IDLE_S and only ever assigned enum members - and the
# whole-of-hdl sweep (scripts/lint_rtl.py, no -Wall) does not report it, so
# narrowing the enum or adding a default would be an unproven synthesis change
# made to please a linter. Recorded, not silently dropped.
#
# Pure RTL (adp_pkg.sv + axi_stream_if.sv), no XPM/Xilinx primitives.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = adp_parser_wrap

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
         -Wno-IMPORTSTAR -Wno-PINCONNECTEMPTY -Wno-EOFNEWLINE \
         -Wno-CASEINCOMPLETE \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee17221/adp/adp_pkg.sv \
       $(RTL_DIR)/common/axi_stream_if.sv \
       $(RTL_DIR)/ieee17221/adp/KL_adp_parser.sv \
       adp_parser_wrap.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vadp_parser_sim
	@echo "======================================================================"
	./obj_dir/Vadp_parser_sim

clean:
	rm -rf obj_dir
