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
         -Wno-EOFNEWLINE -CFLAGS "-std=c++17 -O2"
SRCS = $(C)/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv \
       $(A)/avtp_stream_parser.sv $(A)/KL_avtp_rx_monitor.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_rx_depacketizer.sv \
       ../../../third_party/verilog-axis/rtl/axis_fifo.v \
       avtp_rxmon_wrap.sv
# NxN lane-A stack (NXN_ARCHITECTURE P1/P2/P3): table + parser + ctx monitor
# + depacketizer + route at N=4
NXFLAGS = --cc --exe --build -j 0 --top-module avtp_rxmon_nx_wrap \
         -GCLK_FREQ_HZ_P=10000 \
         +incdir+$(C) +incdir+$(A) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2"
NXSRCS = $(C)/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv \
       $(A)/avtp_stream_parser.sv $(A)/KL_stream_table.sv \
       $(A)/KL_avtp_rx_monitor_ctx.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_aaf_rx_depacketizer.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_pcm_route.sv \
       ../../../third_party/verilog-axis/rtl/axis_fifo.v \
       avtp_rxmon_nx_wrap.sv
.PHONY: all run clean coverage
all: run
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o Vavtp_rxmon_wrap_sim
	./obj_dir/Vavtp_rxmon_wrap_sim
	$(VERILATOR) $(NXFLAGS) --Mdir obj_nx $(NXSRCS) sim_main_nx.cpp -o Vavtp_rxmon_nx_sim
	./obj_nx/Vavtp_rxmon_nx_sim

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
	rm -rf obj_dir obj_cov coverage.dat cov_annotated
