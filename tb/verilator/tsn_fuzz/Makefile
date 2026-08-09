# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# IEEE 1722.1 / 1722 field-validation campaign, tsn-gen driven.
#
#   make            build the co-simulation DUTs and run every campaign
#   make build      build only
#   make aecp|acmp|adp|aaf   run one campaign
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

# ---- ACMP listener state machine ------------------------------------------
ACMP_SRCS = $(RTL)/ieee17221/acmp/acmp_pkg.sv \
            $(RTL)/ieee17221/acmp/KL_acmp_lstn_ctx.sv \
            $(RTL)/ieee17221/acmp/KL_acmp_listener.sv
# 10 kHz scaling: 1 ms = 10 cycles, so the 200 ms / 4 s probe timers are
# reachable inside a simulation the campaign can afford to run.
ACMP_FLAGS = --top-module KL_acmp_listener -GCLK_FREQ_HZ_P=10000 \
             -Wno-MULTIDRIVEN -Wno-IMPORTSTAR --Mdir obj_acmp

# ---- ADP advertiser --------------------------------------------------------
ADP_SRCS = $(RTL)/ieee17221/adp/adp_pkg.sv \
           $(RTL)/ieee17221/adp/adp_advertiser.sv
# shrink the randomised discover-response delay (the adp TB's override)
ADP_FLAGS = --top-module adp_advertiser -GDISC_DLY_BASE=4 -GDISC_DLY_MASK=3 \
            --Mdir obj_adp

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

.PHONY: all build run aecp acmp adp aaf legacy matrix matrix-check clean

all: run

build: obj_acmp/Vacmp_cosim obj_adp/Vadp_cosim obj_aaf/Vaaf_cosim ../aecp/obj_dir/Vaecp_cosim

../aecp/obj_dir/Vaecp_cosim:
	$(MAKE) -C ../aecp cosim

obj_acmp/Vacmp_cosim: cosim_acmp.cpp cosim_axis.h $(ACMP_SRCS)
	$(VERILATOR) $(VCOMMON) $(ACMP_FLAGS) $(ACMP_SRCS) cosim_acmp.cpp -o Vacmp_cosim

obj_adp/Vadp_cosim: cosim_adp.cpp cosim_axis.h $(ADP_SRCS)
	$(VERILATOR) $(VCOMMON) $(ADP_FLAGS) $(ADP_SRCS) cosim_adp.cpp -o Vadp_cosim

obj_aaf/Vaaf_cosim: cosim_aaf.cpp cosim_axis.h $(AAF_SRCS)
	$(VERILATOR) $(VCOMMON) $(AAF_FLAGS) $(AAF_SRCS) cosim_aaf.cpp -o Vaaf_cosim

run: build aecp acmp adp aaf legacy matrix-check
	@echo "== tsn_fuzz: all campaigns passed =="

# regenerate the module<->spec<->test traceability matrix from the tree
matrix:
	$(PY) ../../../docs/traceability/gen_module_matrix.py

# fail if the committed matrix is stale (the no-drift contract)
matrix-check:
	$(PY) ../../../docs/traceability/gen_module_matrix.py --check

aecp: ../aecp/obj_dir/Vaecp_cosim
	$(PY) fuzz_aecp.py

acmp: obj_acmp/Vacmp_cosim
	$(PY) fuzz_acmp.py

adp: obj_adp/Vadp_cosim
	$(PY) fuzz_adp.py

aaf: obj_aaf/Vaaf_cosim
	$(PY) fuzz_aaf.py

# the original 14-command smoke driver that predates this campaign; run it
# too so its expectations cannot drift from the RTL again
legacy: ../aecp/obj_dir/Vaecp_cosim
	@sock=/tmp/tsnfuzz_legacy_$$$$.sock; \
	 root=$${TSN_GEN_ROOT:-$$HOME/tsn-gen}; \
	 pg=$${PACKET_GEN:-$$root/build/traffic-gen/packet_gen}; \
	 if [ ! -x "$$pg" ]; then echo "  SKIP legacy driver: no tsn-gen at $$pg"; \
	   echo "== co-sim: 0 pass, 0 fail (campaigns skipped, tsn-gen absent) =="; \
	   exit 0; fi; \
	 ../aecp/obj_dir/Vaecp_cosim $$sock >/dev/null 2>&1 & dutpid=$$!; \
	 sleep 3; \
	 $(PY) ../aecp/cosim_driver.py $$sock $$pg $$root; rc=$$?; \
	 kill $$dutpid 2>/dev/null; wait $$dutpid 2>/dev/null; rm -f $$sock; \
	 exit $$rc

clean:
	rm -rf obj_acmp obj_adp obj_aaf __pycache__
