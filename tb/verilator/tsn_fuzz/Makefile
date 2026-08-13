# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# IEEE 1722.1 / 1722 field-validation campaign, tsn-gen driven.
#
#   make            build the co-simulation DUTs and run every campaign
#   make build      build only
#   make aaf                 run the AAF campaign (the only one left)
#   make clean
#
# Each campaign is a Python driver talking to a Verilator server built from
# the REAL RTL over a UNIX socket (see cosim_axis.h for the session protocol).
# tsn-gen supplies the spec field model; exit code is the gate.
#
# tsn-gen location: $TSN_GEN_ROOT (default ~/tsn-gen). When it is absent the
# campaigns SKIP cleanly (exit 0) rather than fail — the suite must stay
# runnable on a machine without the generator installed.
VERILATOR ?= verilator
RTL        = ../../../hdl
TP         = ../../../third_party
PY        ?= python3

VCOMMON = --cc --exe --build -j 0 \
          -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
          -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE \
          -CFLAGS "-std=c++17 -O2 -I.."

# ---- ACMP / ADP / AECP campaigns: DELETED with the RTL they fuzzed --------
# fuzz_acmp, fuzz_adp, fuzz_aecp and the legacy 14-command smoke driver all
# drove hdl/ieee17221/{acmp,adp,aecp} engines that no longer exist: the
# protocol processor is this device's 1722.1 plane now, and its own campaign
# lives with the submodule. The AAF campaign below is untouched - it fuzzes
# hdl/ieee1722, which is data plane and was not replaced.
#
# THIS IS A COVERAGE LOSS AND IT IS NOT PAPERED OVER: 1722.1 field fuzzing
# against THIS repository's RTL is gone because THIS repository no longer has
# any 1722.1 RTL to fuzz.

# ---- AVTP/AAF receive stack (wrapper lives with the avtp_rxmon TB) ---------
AAF_SRCS = $(RTL)/common/ethernet_packet_pkg.sv \
           $(RTL)/ieee1722/avtp/avtp_subtype_pkg.sv \
           $(RTL)/ieee1722/avtp/avtp_stream_parser.sv \
           $(RTL)/ieee1722/avtp/KL_avtp_rx_monitor.sv \
           $(RTL)/ieee1722/aaf/KL_aaf_rx_depacketizer.sv \
           $(TP)/verilog-axis/rtl/axis_fifo.v \
           ../avtp_rxmon/avtp_rxmon_wrap.sv
AAF_FLAGS = --top-module avtp_rxmon_wrap -GCLK_FREQ_HZ_P=10000 \
            +incdir+$(RTL)/common +incdir+$(RTL)/ieee1722/avtp --Mdir obj_aaf

.PHONY: all build run aaf matrix matrix-check clean

all: run

build: obj_aaf/Vaaf_cosim

obj_aaf/Vaaf_cosim: cosim_aaf.cpp cosim_axis.h $(AAF_SRCS)
	$(VERILATOR) $(VCOMMON) $(AAF_FLAGS) $(AAF_SRCS) cosim_aaf.cpp -o Vaaf_cosim

run: build aaf matrix-check
	@echo "== tsn_fuzz: all campaigns passed =="

# regenerate the module<->spec<->test traceability matrix from the tree
matrix:
	$(PY) ../../../docs/traceability/gen_module_matrix.py

# fail if the committed matrix is stale (the no-drift contract)
matrix-check:
	$(PY) ../../../docs/traceability/gen_module_matrix.py --check


aaf: obj_aaf/Vaaf_cosim
	$(PY) fuzz_aaf.py

# the original 14-command smoke driver that predates this campaign; run it
# too so its expectations cannot drift from the RTL again
clean:
	rm -rf obj_aaf __pycache__
