# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of ptp_ts_top's METADATA pipeline (parse -> capture ->
# record -> fifos -> RR mux -> ts_m_axis). Written 2026-07-13 when phase B found
# ZERO records on silicon: the block had no metadata-path coverage anywhere
# (tb/verilator/ptp_sync only covers the CSR CDC). Reproduces the ingress-rate
# races (slow MII beats vs the SOP->timestamp CDC handshake) and gates the fix.
# Since #372 the suite also runs that RR mux on its own, with a bound SVA
# checker, and proves the checker's assertions can fail
# (docs/testing/ASSERTIONS.md).
#   make              - all three legs below, in order
#   make run          - build and run the ptp_ts_top self-checking harness
#   make mux-sva      - axis_mux_rr_2in_1out with its bound checker, at
#                       TDATA_WIDTH 8 and 64
#   make sva-campaign - the assertion detection campaign (sva_campaign.py)
#   make clean        - remove build artifacts

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
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

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

# ---- axis_mux_rr_2in_1out with its bound SVA checker (#372) -----------------
# ONE recipe builds every shape: the two below, and every scratch mutant and
# lost-coverage control sva_campaign.py asks for by overriding the MUX_SVA_*
# variables, so the campaign cannot drift from these flags.
#  --assert  explicit, although Verilator 5.050 enables assertions by default
#            (since 5.038): before 5.038 a build without it compiled every
#            assertion out and still passed. --no-assert is the campaign's
#            assertions-disabled control.
#  -j 8      bounds the C++ build's parallelism.
#  no -Wno-fatal: a new warning in the checker or the bind fails the build.
#            CASEINCOMPLETE is the mux's own standing finding, waived exactly
#            as VFLAGS above waives it.
SVA_DIR         = ../../common/sva
MUX_SVA_WIDTH  ?= 64
MUX_SVA_OBJ    ?= obj_dir_mux_sva_w$(MUX_SVA_WIDTH)
MUX_SVA_DUT    ?= $(RTL_DIR)/common/axis_mux_rr_2in_1out.sv
MUX_SVA_BIND   ?= $(SVA_DIR)/axis_mux_rr_2in_1out_bind.sv
MUX_SVA_ASSERT ?= --assert
MUX_SVA_VFLAGS = --cc --exe --build -j 8 $(MUX_SVA_ASSERT) \
                 --top-module axis_mux_rr_2in_1out -GTDATA_WIDTH=$(MUX_SVA_WIDTH) \
                 -Wall -Wno-CASEINCOMPLETE \
                 -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DAXIS_MUX_TDATA_WIDTH=$(MUX_SVA_WIDTH)"
MUX_SVA_SRCS = $(MUX_SVA_DUT) \
               $(SVA_DIR)/axis_stream_source_sva.sv \
               $(SVA_DIR)/axis_mux_rr_2in_1out_sva.sv \
               $(MUX_SVA_BIND)

.PHONY: all run mux-sva mux-sva-build sva-campaign clean
all: run mux-sva sva-campaign

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vptp_ts_sim
	@echo "======================================================================"
	./obj_dir/Vptp_ts_sim

mux-sva-build:
	$(VERILATOR) $(MUX_SVA_VFLAGS) -Mdir $(MUX_SVA_OBJ) $(MUX_SVA_SRCS) mux_sva_main.cpp -o Vmux_sva

mux-sva:
	@echo "======================================================================"
	$(MAKE) --no-print-directory mux-sva-build MUX_SVA_WIDTH=8
	./obj_dir_mux_sva_w8/Vmux_sva
	@echo "======================================================================"
	$(MAKE) --no-print-directory mux-sva-build MUX_SVA_WIDTH=64
	./obj_dir_mux_sva_w64/Vmux_sva

# Rule 8: every property must be seen to fail. Expected failures stay in
# obj_dir_sva_campaign/; only the verdict table reaches this log.
sva-campaign: mux-sva
	@echo "======================================================================"
	python3 sva_campaign.py --verilator "$(VERILATOR)"

clean:
	rm -rf obj_dir obj_dir_mux_sva_w8 obj_dir_mux_sva_w64 obj_dir_sva_campaign
