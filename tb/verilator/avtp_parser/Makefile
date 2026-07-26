# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# avtp_stream_parser DEEP suite - the listener ACCEPT VERDICT, at every shape
# the SoC ships and with the reject leg proved as hard as the accept leg.
#
# tb/verilator/avtp_stream owns the module's first increment (21 checks, one
# shape, accept-biased). This suite owns the verdict itself:
#
#   * the stream_id BYTE ORDER as lifted off the wire (both BIG_ENDIAN modes),
#   * the VLAN-tagged vs untagged header offset, incl. the mis-offset negative,
#   * N=1 / N=4 / N=8 table widths - the index port width changes with N and
#     only N=8 can express entries 4..7 (cfg_ax8x8 is the shipping shape),
#   * the SID compare REJECT leg: byte-swapped sid, transposed halves, armed
#     but disabled, one-bit-off - each with the counter signature the 0x8B4
#     APRB probe group reports, so a silicon read can be told apart,
#   * frame-stream integrity: exactly one verdict per frame, back-to-back
#     frames with no idle gap, mid-frame backpressure, the header-length floor,
#   * a randomised differential leg against an independent C++ model of the
#     documented byte layout (thousands of frames per shape).
#
#   make        - build every shape and run the self-checking harnesses
#   make build  - build only
#   make clean  - remove build artifacts
#
# Born 2026-07-26: the fabric listener accepts nothing on the flashed 8x8
# gateware while both ends agree on the stream_id, and no suite owned the
# compare that issues that verdict at N=8.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
C          = $(RTL_DIR)/common
A          = $(RTL_DIR)/ieee1722/avtp
TOP        = avtp_stream_parser

WAIVERS = -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
          -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
          -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -Wno-TIMESCALEMOD

VFLAGS   = --cc --exe --build -j 0 --top-module $(TOP) \
           +incdir+$(C) +incdir+$(A) $(WAIVERS) -CFLAGS "-std=c++17 -O2"
SRCS     = $(C)/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv \
           $(A)/avtp_stream_parser.sv

# stream-table + parser at FULL index width (N=8): the milan_datapath pairing
TBLFLAGS = --cc --exe --build -j 0 --top-module parser_tbl_wrap \
           +incdir+$(C) +incdir+$(A) $(WAIVERS) -CFLAGS "-std=c++17 -O2"
TBLSRCS  = $(C)/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv \
           $(A)/avtp_stream_parser.sv $(A)/KL_stream_table.sv parser_tbl_wrap.sv

.PHONY: all run build clean banner

all: run

banner:
	@echo "======================================================================"
	@echo " tb/verilator/avtp_parser - listener accept verdict, N=1/4/8 + LE/BE"
	@echo "======================================================================"

build:
	$(VERILATOR) $(VFLAGS) --Mdir obj_n1 -GN_STREAMS=1 \
		-CFLAGS "-DNSTREAMS_TB=1 -DSHAPE_NAME=\\\"N1-LE-legacy\\\"" \
		$(SRCS) sim_parser.cpp -o Vparser_n1
	$(VERILATOR) $(VFLAGS) --Mdir obj_n4 -GN_STREAMS=4 \
		-CFLAGS "-DNSTREAMS_TB=4 -DSHAPE_NAME=\\\"N4-LE-arty4x4\\\"" \
		$(SRCS) sim_parser.cpp -o Vparser_n4
	$(VERILATOR) $(VFLAGS) --Mdir obj_n8 -GN_STREAMS=8 \
		-CFLAGS "-DNSTREAMS_TB=8 -DSHAPE_NAME=\\\"N8-LE-cfg_ax8x8-SHIPPING\\\"" \
		$(SRCS) sim_parser.cpp -o Vparser_n8
	$(VERILATOR) $(VFLAGS) --Mdir obj_be -GN_STREAMS=8 -GBIG_ENDIAN=1 \
		-CFLAGS "-DNSTREAMS_TB=8 -DBIG_ENDIAN_TB=1 -DSHAPE_NAME=\\\"N8-BE-beats\\\"" \
		$(SRCS) sim_parser.cpp -o Vparser_be
	$(VERILATOR) $(TBLFLAGS) --Mdir obj_tbl -GN_LISTENERS_P=8 \
		-CFLAGS "-DNSTREAMS_TB=8" \
		$(TBLSRCS) sim_tbl.cpp -o Vparser_tbl8

# run every shape even when one fails (a red shape must not hide the others);
# the aggregate exit code stays honest.
run: banner build
	@rc=0; \
	./obj_n1/Vparser_n1   || rc=1; \
	./obj_n4/Vparser_n4   || rc=1; \
	./obj_n8/Vparser_n8   || rc=1; \
	./obj_be/Vparser_be   || rc=1; \
	./obj_tbl/Vparser_tbl8 || rc=1; \
	exit $$rc

clean:
	rm -rf obj_n1 obj_n4 obj_n8 obj_be obj_tbl
