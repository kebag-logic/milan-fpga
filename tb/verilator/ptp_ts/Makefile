# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of ptp_ts_top's METADATA pipeline (parse -> capture ->
# record -> fifos -> RR mux -> ts_m_axis). Written 2026-07-13 when phase B found
# ZERO records on silicon: the block had no metadata-path coverage anywhere
# (tb/verilator/ptp_sync only covers the CSR CDC). Reproduces the ingress-rate
# races (slow MII beats vs the SOP->timestamp CDC handshake) and gates the fix.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = ptp_ts_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/ieee8021as/ptp_timestamp \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR \
         -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/common/ethernet_packet_pkg.sv \
       $(RTL_DIR)/common/axi_stream_if.sv \
       $(RTL_DIR)/common/cdc_pulse.sv \
       $(RTL_DIR)/common/cdc_handshake.sv \
       $(RTL_DIR)/common/axis_mux_rr_2in_1out.sv \
       $(AXIS_DIR)/axis_fifo.v \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/timestamp_counter.sv \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/ptp_csr_sync.sv \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/ptp_ts_core.sv \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/ptp_ts_top.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vptp_ts_sim
	@echo "======================================================================"
	./obj_dir/Vptp_ts_sim

clean:
	rm -rf obj_dir
