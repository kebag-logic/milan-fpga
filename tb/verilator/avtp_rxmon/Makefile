# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_avtp_rx_monitor verification: Milan STREAM_INPUT counters behind the
# parser (lock/settle/mismatch/interrupt/unlock/format/reset contract).
# Runs at a 10 kHz scaled clock (-GCLK_FREQ_HZ_P) so the 100 ms unlock
# timeout is 1000 cycles.
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
C          = $(RTL_DIR)/common
A          = $(RTL_DIR)/ieee1722/avtp
TOP        = avtp_rxmon_wrap
VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         -GCLK_FREQ_HZ_P=10000 \
         +incdir+$(C) +incdir+$(A) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -CFLAGS "-std=c++17 -O2 -Wall -Wextra"
SRCS = $(C)/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv \
       $(A)/avtp_stream_parser.sv $(A)/KL_avtp_rx_monitor.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_rx_depacketizer.sv \
       ../../../third_party/verilog-axis/rtl/axis_fifo.v \
       avtp_rxmon_wrap.sv
# Multi-stream lane-A stack (docs/overview/ARCHITECTURE.md): table + parser + ctx monitor
# + depacketizer + route at N=4. Scaled clock 100 kHz: 100 ms unlock =
# 10000 cyc, so the Table 5.6 observation interval (IVAL_CYC_P=2000) fits
# WELL INSIDE the silence timeout - a flush over one interval must not
# unlock the stream, exactly like 1 s vs 100 ms at speed.
NXFLAGS = --cc --exe --build -j 0 --top-module avtp_rxmon_nx_wrap \
         -GCLK_FREQ_HZ_P=100000 \
         +incdir+$(C) +incdir+$(A) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2 -Wall -Wextra"
NXSRCS = $(C)/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv \
       $(A)/avtp_stream_parser.sv $(A)/KL_stream_table.sv \
       $(RXMON_SRC) \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_rx_depacketizer.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_pcm_route.sv \
       ../../../third_party/verilog-axis/rtl/axis_fifo.v \
       avtp_rxmon_nx_wrap.sv
# #640 M6 lockstep leg: the shipping context engine beside the pre-change
# reference (reference/KL_avtp_rx_monitor_ctx_ref.sv, dev e8454e27's module
# with its name changed and #762's silence interruption and stop rule applied
# in the engine's own lines), at the shipping N=1 and the 8x8 shape's N=8.
# RXMON_SRC, REF_SRC and LS_MDIR are overridable so lockstep_mutants.py builds
# a MUTATED copy of the engine, and for #762 of the reference too, through
# this exact recipe; RXMON_SRC and NX_MDIR do the same for format_mutants.py
# and the N=4 stack (#765), which for #775's two-copy defects also builds this
# leg from a mutated engine and reference.
RXMON_SRC ?= $(A)/KL_avtp_rx_monitor_ctx.sv
REF_SRC   ?= reference/KL_avtp_rx_monitor_ctx_ref.sv
LS_MDIR   ?= obj_ls
NX_MDIR   ?= obj_nx
LSFLAGS = --cc --exe --build -j 0 --top-module avtp_rxmon_lockstep_wrap \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"
LSSRCS = $(REF_SRC) $(RXMON_SRC) \
         avtp_rxmon_lockstep_wrap.sv
.PHONY: all run clean coverage lockstep-build lockstep nx-build
all: run
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o Vavtp_rxmon_wrap_sim
	./obj_dir/Vavtp_rxmon_wrap_sim
	$(MAKE) nx-build
	./obj_nx/Vavtp_rxmon_nx_sim
	$(MAKE) lockstep
	python3 lockstep_mutants.py
	python3 format_mutants.py
nx-build:
	$(VERILATOR) $(NXFLAGS) --Mdir $(NX_MDIR) $(NXSRCS) sim_main_nx.cpp -o Vavtp_rxmon_nx_sim
lockstep-build:
	$(VERILATOR) $(LSFLAGS) --Mdir $(LS_MDIR)1 -GN_LISTENERS_P=1 \
	  -CFLAGS "-DN_TB=1 -Wall -Wextra" $(LSSRCS) sim_lockstep.cpp -o Vavtp_rxmon_lockstep
	$(VERILATOR) $(LSFLAGS) --Mdir $(LS_MDIR)8 -GN_LISTENERS_P=8 \
	  -CFLAGS "-DN_TB=8 -Wall -Wextra" $(LSSRCS) sim_lockstep.cpp -o Vavtp_rxmon_lockstep
lockstep: lockstep-build
	./$(LS_MDIR)1/Vavtp_rxmon_lockstep
	./$(LS_MDIR)8/Vavtp_rxmon_lockstep

# Line+toggle coverage over the RX stack (parser + monitor + depacketizer).
# Gate: LINE coverage of the two KL_ modules must be >= 95 % (defensive-only arms carry coverage_off pragmas).
coverage:
	rm -rf obj_cov coverage.dat cov_annotated
	$(VERILATOR) $(VFLAGS) --coverage --Mdir obj_cov $(SRCS) sim_main.cpp \
	    -o Vavtp_rxmon_wrap_cov
	./obj_cov/Vavtp_rxmon_wrap_cov +verilator+coverage+file+coverage.dat
	verilator_coverage --annotate cov_annotated --annotate-min 1 coverage.dat \
	    | tail -2
	@python3 cov_gate.py cov_annotated 95
clean:
	rm -rf obj_dir obj_ls1 obj_ls8 obj_cov coverage.dat cov_annotated
